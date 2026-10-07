"""Resume bounded Train/Validation waves only after the complete IC audit passes."""
import sys,json,time,subprocess,statistics,os,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,policy,row,connection,read_json,write_json,file_hash,digest
from bt_history.data_control import locked,AttemptLedger
from bt_history.submission_accounting import submission_charges

def submit(indices,stage,b):
 sid=str(time.time_ns());sub={'submission_id':sid,'stage':stage,'indices':indices,'slurm_array_indices':list(range(len(indices)))}
 wave=RUN/'waves'/(sid+'.json');write_json(wave,sub,exclusive=True)
 cmd=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1','--array=0-'+str(len(indices)-1)+'%'+str(b['max_concurrent']),'--cpus-per-task=16','--mem=16384M','--time=120','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--nodelist=chpc-cn[057-064]','--export=ALL,BT_RANDOM_WAVE_RECORD='+str(wave),'--output='+str(RUN/'scheduler_%A_%a.log'),str(ROOT/'maintenance/random_ic/worker.sbatch')];sub['command']=cmd
 with (RUN/'submissions.jsonl').open('a') as f:f.write(json.dumps(sub)+'\n');f.flush();os.fsync(f.fileno())
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=30);job=r.stdout.strip().split(';')[0];write_json(RUN/(sid+'_slurm.json'),{'submitted':r.returncode==0,'response':job,'stderr':r.stderr,'exit_code':r.returncode})
 if r.returncode:raise RuntimeError('Array submission failed; reconcile reservation before retry: '+r.stderr)
 command=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1','--cpus-per-task=1','--mem=4G','--time=30','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--nodelist=chpc-cn[057-064]','--dependency=afterany:'+job,'--output='+str(RUN/'collect_%j.log'),str(ROOT/'maintenance/random_ic/collect.sbatch')]
 r=subprocess.run(command,capture_output=True,text=True,timeout=30);write_json(RUN/'collectors'/(job+'.json'),{'array_job':job,'collector_job':r.stdout.strip(),'command':command,'exit_code':r.returncode,'stderr':r.stderr})
 if r.returncode:raise RuntimeError('Collector not submitted; manual resume required: '+r.stderr)
 return {'array_job':job,'collector_job':r.stdout.strip(),'unique_indices':len(indices),'split':stage}

def main():
 with locked(RUN/'controller.lock'):
  c,d,b,spec=policy()
  if file_hash(RUN/'design.sqlite')!=d['index_sha256']:raise ValueError('Frozen production index changed')
  ledger=AttemptLedger(RUN);entries=ledger.entries();latest={a['sample_id']:a for a in entries};subs=[json.loads(x) for x in (RUN/'submissions.jsonl').read_text().splitlines()] if (RUN/'submissions.jsonl').exists() else []
  charges=submission_charges(RUN,subs,{'stages':{'train':spec,'validation':spec}});write_json(RUN/'submission_accounting.json',{'rows':charges});byindex={}
  for ch in charges:byindex.setdefault(ch['index'],[]).append(ch)
  accounting=[];receipts={};failures=[];all_failures=[]
  db=sqlite3.connect(RUN/'labels.sqlite');db.execute('CREATE TABLE IF NOT EXISTS labels(idx INTEGER PRIMARY KEY,sample_id TEXT,split TEXT,path TEXT,sha256 TEXT,positive INTEGER,xhi REAL,tau REAL,wall REAL,memory REAL,admitted REAL)')
  for a in entries:
   ix=a['manifest_index'];opts=byindex.get(ix,[]);ordinal=a['ordinal_for_sample']-1;ch=opts[ordinal] if ordinal<len(opts) else None;rp=RUN/'receipts'/(a['attempt_id']+'.json')
   if ch and ch['terminal'] and not rp.exists():
    status='infrastructure_failure' if ch['state'] in ['NODE_FAIL','BOOT_FAIL','PREEMPTED'] else 'timeout' if ch['state']=='TIMEOUT' else 'out_of_memory' if ch['state']=='OUT_OF_MEMORY' else 'schema_provenance_failure';ledger.finish(a,{'qualified':False,'simulation_status':status,'scheduler_state':ch['state'],'reason':'Terminal allocation without receipt'})
   if ch:accounting.append({'attempt_id':a['attempt_id'],'terminal':ch['terminal'],'allocation_core_hours':ch['actual_core_hours']})
   if rp.exists():
    previous=read_json(rp)
    if not previous.get('qualified'):all_failures.append(dict(previous,index=ix))
   if rp.exists() and latest[a['sample_id']]['attempt_id']==a['attempt_id']:
    r=read_json(rp);receipts[ix]=r
    if r.get('qualified'):
     if db.execute('SELECT 1 FROM labels WHERE idx=?',(ix,)).fetchone() is None:
      path=ROOT/r['artifact_path']
      if file_hash(path)!=r['label_sha256']:raise ValueError('Admission checksum mismatch')
      label=read_json(path);design=row(ix)
      if label['canonical_parameters']!=design['canonical_parameters'] or label['effective_ic_seed']!=design['requested_ic_seed'] or label['native_sha256']!=c['native_sha256']:raise ValueError('Admission identity mismatch')
      db.execute('INSERT INTO labels VALUES(?,?,?,?,?,?,?,?,?,?,?)',(ix,a['sample_id'],a['stage'],r['artifact_path'],r['label_sha256'],label['classifier_label'],label['xHI_at_observation_redshifts']['5.9'],label['tau_exact_derived'],label['wall_time'],label['peak_memory_MiB'],time.time()))
    else:failures.append(dict(r,index=ix))
  db.commit();write_json(RUN/'allocation_accounting.json',{'rows':accounting});write_json(RUN/'failure_registry.json',{'failed_attempts':all_failures,'latest_failures':failures,'original_attempts_retained':True})
  counts={};walls=[]
  for split,target in [('train',100000),('validation',10000)]:
   n,pos=db.execute('SELECT count(*),coalesce(sum(positive),0) FROM labels WHERE split=?',(split,)).fetchone();counts[split]={'target':target,'qualified':n,'positive_fraction':pos/n if n else None,'failed':sum(f['stage']==split for f in failures)}
  walls=sorted(r[0] for r in db.execute('SELECT wall FROM labels'));active=[ch for ch in charges if not ch['terminal']];attempted={ch['index'] for ch in charges};unstarted_failure=[ch for ch in charges if ch['terminal'] and ch['index'] not in receipts]
  disk=sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(RUN) for f in fs);stop=[]
  if disk>b['storage_limit_bytes']:stop.append('STORAGE_BUDGET_EXCEEDED')
  if unstarted_failure or any(f['simulation_status'] in ['schema_provenance_failure','runtime_native_load_failure'] for f in failures):stop.append('SYSTEMIC_IDENTITY_RUNTIME_SCHEMA_FAILURE')
  if len(failures)>=3 and len(failures)/max(1,len(entries))>b['failure_rate_stop']:stop.append('FAILURE_RATE_EXCEEDED')
  if len(entries)>=b['max_attempts']:stop.append('ATTEMPT_BUDGET_EXHAUSTED')
  state={'version':'random_ic_v2','updated_at_unix':time.time(),'datasets':counts,'attempts':len(entries),'failed_numerical':sum(f['simulation_status']=='numerical_failure' for f in failures),'failed_infrastructure':sum(f['simulation_status']=='infrastructure_failure' for f in failures),'retry_attempts':len(entries)-len({a['sample_id'] for a in entries}),'allocated_core_hours':sum(ch['actual_core_hours'] or 0 for ch in charges),'reserved_core_hours':sum(ch['reserved_core_hours'] for ch in charges),'running_pending_or_unresolved':len(active),'median_wall_seconds':statistics.median(walls) if walls else None,'q90_wall_seconds':walls[int(.9*(len(walls)-1))] if walls else None,'disk_bytes':disk,'max_array_concurrency':b['max_concurrent'],'native_sha256':c['native_sha256'],'base_science_contract_hash':digest(c),'stop_reasons':stop,'sealed_labels_generated':False,'sealed_labels_read':False}
  if stop:state['status']='STOPPED_REQUIRES_REVIEW'
  elif active:state['status']='RUNNING_OR_PENDING'
  else:
   indices=[];stage=None
   with connection() as designs:
    for split in ['train','validation']:
     if counts[split]['qualified']>=counts[split]['target']:continue
     retry=[f['index'] for f in failures if f['stage']==split and f['simulation_status']=='infrastructure_failure' and f['ordinal_for_sample']==1]
     candidates=[r[0] for r in designs.execute('SELECT idx FROM design WHERE split=? ORDER BY primary_point DESC,idx',(split,)) if r[0] not in attempted]
     indices=(retry+candidates)[:min(8 if not subs else b['wave_size'],counts[split]['target']-counts[split]['qualified'])];stage=split
     if indices:break
   if indices:state['submission']=submit(indices,stage,b);state['status']='ARRAY_SUBMITTED'
   else:state['status']='COMPLETED' if all(v['qualified']>=v['target'] for v in counts.values()) else 'FINITE_DESIGN_EXHAUSTED_FAILURES_RETAINED'
  write_json(ROOT/'results/random_ic_dataset_progress.json',state)
  (ROOT/'reports/random_ic_dataset_progress.md').write_text('# Random-IC v2 dataset status\n\n```json\n'+json.dumps(state,indent=2)+'\n```\n')
  db.close();print(json.dumps(state))
if __name__=='__main__':main()
