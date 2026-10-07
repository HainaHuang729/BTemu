"""Finite audit waves and afterany collection; no random-IC production before audit."""
import sys,os,json,time,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,policy,rows
from bt_history.data_control import read_json,write_json,locked,AttemptLedger
from bt_history.submission_accounting import submission_charges

def submit_wave(indices,b,dependency=None):
 sid=str(time.time_ns());sub={'submission_id':sid,'stage':'ic_audit','indices':indices,'slurm_array_indices':indices}
 cmd=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1','--array='+','.join(map(str,indices))+'%'+str(b['max_concurrent']),'--cpus-per-task=16','--mem=16384M','--time=120','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--output='+str(RUN/'scheduler_%A_%a.log')]
 if dependency:cmd+=['--dependency=afterany:'+dependency]
 cmd+=[str(ROOT/'maintenance/ic_audit/worker.sbatch')]
 sub['command']=cmd
 with (RUN/'submissions.jsonl').open('a') as f:f.write(json.dumps(sub)+'\n')
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=30);job=r.stdout.strip().split(';')[0];write_json(RUN/(sid+'_slurm.json'),{'submitted':r.returncode==0,'response':job,'stderr':r.stderr,'exit_code':r.returncode})
 if r.returncode:raise RuntimeError('Audit array submission failed: '+r.stderr)
 collector=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1','--cpus-per-task=1','--mem=4G','--time=15','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--dependency=afterany:'+job,'--output='+str(RUN/'collect_%j.log'),str(ROOT/'maintenance/ic_audit/collect.sbatch')]
 r=subprocess.run(collector,capture_output=True,text=True,timeout=30)
 write_json(RUN/'collectors'/(job+'.json'),{'array_job':job,'collector_job':r.stdout.strip(),'command':collector,'exit_code':r.returncode,'stderr':r.stderr})
 if r.returncode:raise RuntimeError('Audit collector submission failed: '+r.stderr)
 return {'array_job':job,'collector_job':r.stdout.strip(),'indices':indices}

def main():
 RUN.mkdir(parents=True,exist_ok=True)
 with locked(RUN/'controller.lock'):
  c,a,b,spec=policy();allrows=rows();ledger=AttemptLedger(RUN);entries=ledger.entries();latest={x['sample_id']:x for x in entries}
  subs=[json.loads(s) for s in (RUN/'submissions.jsonl').read_text().splitlines()] if (RUN/'submissions.jsonl').exists() else []
  charges=submission_charges(RUN,subs,{'stages':{'ic_audit':spec}});write_json(RUN/'submission_accounting.json',{'rows':charges})
  byindex={}
  for ch in charges:byindex.setdefault(ch['index'],[]).append(ch)
  byid={v['sample_id']:i for i,v in enumerate(allrows)};account=[];failures=[];done=set()
  for at in entries:
   options=byindex.get(byid[at['sample_id']],[]);ordinal=at['ordinal_for_sample']-1
   ch=options[ordinal] if ordinal<len(options) else None;rp=RUN/'receipts'/(at['attempt_id']+'.json')
   if ch and ch['terminal'] and not rp.exists():
    status='infrastructure_failure' if ch['state'] in ['NODE_FAIL','BOOT_FAIL','PREEMPTED'] else 'timeout' if ch['state']=='TIMEOUT' else 'out_of_memory' if ch['state']=='OUT_OF_MEMORY' else 'schema_provenance_failure'
    ledger.finish(at,{'qualified':False,'simulation_status':status,'scheduler_state':ch['state'],'reason':'Terminal allocation with no worker receipt'})
   if ch:account.append({'attempt_id':at['attempt_id'],'terminal':ch['terminal'],'allocation_core_hours':ch['actual_core_hours']})
   if rp.exists():
    rec=read_json(rp)
    if rec.get('qualified'):done.add(byid[at['sample_id']])
    elif latest[at['sample_id']]['attempt_id']==at['attempt_id']:failures.append({**rec,'index':byid[at['sample_id']]})
  write_json(RUN/'allocation_accounting.json',{'rows':account});write_json(RUN/'failure_registry.json',{'failures':failures})
  attempted_indices={v['index'] for v in charges};gate_failures=[ch for ch in charges if ch['terminal'] and allrows[ch['index']]['sample_id'] not in latest]
  state={'version':'IC_AUDIT_V1','planned_theta':128,'planned_IC_realizations':1024,'reused_fixed':128,'qualified_fresh':len(done),'attempts':len(entries),'running_or_pending_or_unresolved':sum(not v['terminal'] for v in charges),'allocated_core_hours':sum(v['actual_core_hours'] or 0 for v in charges),'reserved_core_hours':sum(v['reserved_core_hours'] for v in charges),'failed_latest':len(failures),'gate_failures':gate_failures,'random_IC_production_started':False,'sealed_access':False}
  from report import summarize
  summary=summarize();state['complete_families']=summary['complete_families']
  if sum(f.stat().st_size for f in RUN.rglob('*') if f.is_file())>b['storage_limit_bytes']:raise PermissionError('Audit storage cap reached; no further submission')
  hard=gate_failures or any(x['simulation_status'] in ['schema_provenance_failure','runtime_native_load_failure'] for x in failures)
  if hard:state['status']='AUDIT_SYSTEMIC_FAILURE_REQUIRES_REVIEW'
  elif state['running_or_pending_or_unresolved']:state['status']='AUDIT_RUNNING_OR_PENDING'
  elif len(done)==896:state['status']='AUDIT_COMPLETED';state['decision']=summary['single_IC_production_decision']
  else:
   remaining=[i for i,r in enumerate(allrows) if not r['reuse_fixed_reference'] and i not in attempted_indices]
   retry=[x['index'] for x in failures if x['simulation_status']=='infrastructure_failure' and latest[x['sample_id']]['ordinal_for_sample']==1]
   # First two actual random-IC calls gate all later production on their receipts.
   pilot={1,2}
   if subs and not pilot.issubset(done):state['status']='AUDIT_PILOT_FAILED_NO_EXPANSION'
   elif remaining or retry:
    pending=(retry+remaining)[:2 if not subs else 128]
    state['submission']=submit_wave(pending,b,dependency=sys.argv[1] if len(sys.argv)>1 else None);state['status']='AUDIT_ARRAY_SUBMITTED'
   else:state['status']='AUDIT_INCOMPLETE_FAILURES_RETAINED'
  write_json(ROOT/'results/ic_audit_progress.json',state);print(json.dumps(state))
if __name__=='__main__':main()
