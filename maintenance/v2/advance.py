"""Finite v2 waves using the existing native gates, submitter, worker and QA."""
import sys,json,time,sqlite3,subprocess,os,math,statistics,fcntl,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'))
from bt_history.data_control import read_json,write_json,verify_design,assert_development_path
from bt_history.contracts import file_hash,digest
RUN=root/'data_runs/dataset_v2_100k';BUDGET=root/'configs/v2_100k_budget.json'

def attach(db,item,receipt):
 if item['split'] not in ['train','validation']:raise PermissionError('Sealed entry forbidden')
 prior=db.execute('select sha from labels where id=?',(item['sample_id'],)).fetchone()
 if prior:
  if prior[0]!=item['sha256']:raise ValueError('Qualified label changed')
  return
 f=root/item['path'];assert_development_path(f,item['split'])
 if file_hash(f)!=item['sha256']:raise ValueError('Label checksum mismatch')
 if not receipt.get('qualified') or receipt.get('label_sha256')!=item['sha256']:raise ValueError('Receipt mismatch')
 row=read_json(f);c=read_json(root/'contracts/science_contract.json');sel=read_json(root/'contracts/selected_native_contract.json')
 if row['native_sha256']!=sel['native_sha256'] or row['science_contract_hash']!=digest(c) or row['effective_ic_seed']!=c['ic_target']['seed'] or row['config_hash']!=digest(c):raise ValueError('Target identity mismatch')
 if row['pipeline_integrity_sha256'] not in sel['accepted_training_pipeline_sha256']:raise ValueError('Unqualified implementation')
 if row['runtime_fingerprint'] not in sel['allowed_runtime_fingerprints']:raise ValueError('Unqualified runtime')
 x=row['global_xHI'];z=row['redshifts']
 if z!=c['redshift_grid'] or len(x)!=32 or any(not math.isfinite(v) or v<0 or v>1 for v in x):raise ValueError('Invalid physical history')
 obs=float(row['exact_xHI_at_observation_redshifts']['5.9']);tau=float(row['exact_tau'])
 if not math.isfinite(obs) or not math.isfinite(tau):raise ValueError('Invalid downstream reference')
 lf=row.get('original_end_to_end_success') is not False and row.get('LF_reference_status')!='FAILED_ORIGINAL_GRID_COVERAGE_NOT_RECOVERED'
 ll=row.get('history_loglikelihood_references',{}).get('xHI')
 if ll is None:
  refs=row.get('individual_loglikelihood_references_if_computed') or {};ll=refs.get('McGreer_xHI',refs.get('xHI',refs.get('logL_xHI',refs.get('log_likelihood_xHI'))))
 if ll is None or not math.isfinite(float(ll)):raise ValueError('Missing original xHI likelihood reference')
 payload={'sample_id':row['sample_id'],'split':row['split'],'physical_parameters':row['physical_parameters'],'redshifts':z,'global_xHI':x,'xHI_5p9':obs,'classifier_label':int(obs<.31),'classifier_threshold':.31,'derived_tau':tau,'logL_xHI':ll,'history_valid':True,'lf_valid':lf,'tau_valid':True,'native_sha256':row['native_sha256'],'source_fingerprint':row['source_fingerprint'],'config_hash':row['config_hash'],'IC_seed':row['effective_ic_seed'],'label_path':item['path'],'label_sha256':item['sha256'],'receipt_path':item['receipt'],'slurm_job_id':receipt.get('slurm_job_id'),'attempt_id':receipt.get('attempt_id'),'wall_seconds':row['wall_time'],'peak_memory_MiB':row.get('peak_memory_MiB'),'quality_flags':row.get('quality_flags',[]),'original_labels_unchanged':True}
 dest=(RUN/'classifier_metadata'/row['sample_id']).with_suffix('.json')
 if dest.exists():
  if read_json(dest)!=payload:raise ValueError('Existing classifier sidecar differs from unchanged exact label')
 else:write_json(dest,payload)
 db.execute('insert into labels values (?,?,?,?,?,?,?,?,?,?)',(row['sample_id'],row['split'],item['sha256'],obs,int(obs<.31),row['wall_time'],row.get('peak_memory_MiB'),json.dumps(payload),json.dumps(item),time.time()))

def controller(submit):
 RUN.mkdir(parents=True,exist_ok=True)
 with (RUN/'controller.lock').open('a') as lock:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return
  cfg=read_json(BUDGET);design=read_json(root/'contracts/dataset_design_v2_100k.json')
  if file_hash(root/'contracts/dataset_design_v2_100k.json')!=cfg['dataset_design_sha256']:raise ValueError('v2 design changed')
  db=sqlite3.connect(str(RUN/'dataset_manifest.sqlite'));db.execute('create table if not exists labels (id text primary key, split text, sha text, xhi real, positive integer, wall real, memory real, metadata text, item text, admitted_unix real)')
  v1=read_json(root/'manifests/qualified_batch2_development.json')
  for it in v1['files']:
   if it['split']=='train':attach(db,it,read_json(root/it['receipt']))
  db.commit()
  entries=[];ledger=RUN/'attempts.jsonl'
  if ledger.exists():entries=[json.loads(s) for s in ledger.read_text().splitlines()]
  latest={a['sample_id']:a for a in entries};receipts={};new=[]
  for a in entries:
   rp=RUN/'receipts'/(a['attempt_id']+'.json')
   if not rp.exists():continue
   rr=read_json(rp);receipts[a['sample_id']]=rr
   if rr.get('qualified'):
    it={'sample_id':a['sample_id'],'split':a['stage'],'role':'development','path':str(Path(rr['artifact_path'])/'label.json'),'sha256':rr['label_sha256'],'receipt':str(rp.relative_to(root))}
    attach(db,it,rr)
  db.commit()
  submissions=[json.loads(s) for s in (RUN/'submissions.jsonl').read_text().splitlines()] if (RUN/'submissions.jsonl').exists() else []
  from bt_history.submission_accounting import submission_charges,TERMINAL
  charges=submission_charges(RUN,submissions,cfg);write_json(RUN/'submission_accounting.json',{'rows':charges,'as_of_unix':time.time()})
  # A timeout/killed task may have no receipt: materialize its failure, never restart blindly.
  for s in submissions:
   slots=[ch for ch in charges if ch['submission_id']==s['submission_id']]
   if not slots or not all(ch['terminal'] for ch in slots):continue
   rows=verify_design(root,root/s['manifest'])
   for ch in slots:
    sid=rows[ch['index']]['sample_id'];a=latest.get(sid)
    if sid in receipts:continue
    status='infrastructure_failure' if ch['state'] in ['NODE_FAIL','BOOT_FAIL','PREEMPTED'] else 'timeout' if ch['state']=='TIMEOUT' else 'out_of_memory' if ch['state']=='OUT_OF_MEMORY' else 'schema_provenance_failure'
    rr={'sample_id':sid,'split':s['stage'],'qualified':False,'simulation_status':status,'scheduler_state':ch['state'],'reason':'Terminal allocation without worker receipt','attempt_id':a['attempt_id'] if a else None}
    if a:write_json(RUN/'receipts'/(a['attempt_id']+'.json'),{**a,**rr},exclusive=True)
    else:write_json(RUN/'unstarted_failures'/(sid+'.json'),rr)
    receipts[sid]=rr
  failures=[r for r in receipts.values() if not r.get('qualified')]
  write_json(RUN/'failure_registry.json',{'failures':failures,'all_original_receipts_retained':True})
  data={};walls=[]
  for split,target in [('train',100000),('validation',10000)]:
   count,pos=db.execute('select count(*),coalesce(sum(positive),0) from labels where split=?',(split,)).fetchone()
   hist=[db.execute('select count(*) from labels where split=? and xhi>=? and xhi<?',(split,i/20,(i+1)/20 if i<19 else 1.0000000001)).fetchone()[0] for i in range(20)]
   data[split]={'target':target,'qualified':count,'positive_fraction':pos/count if count else None,'negative_fraction':1-pos/count if count else None,'xHI_5p9_histogram_20_equal_bins_0_1':hist,'failed_current_v2':sum(r.get('split')==split for r in failures)}
  walls=sorted(r[0] for r in db.execute('select wall from labels where wall is not null'));memmax=db.execute('select max(memory) from labels').fetchone()[0]
  q90=walls[int(.9*(len(walls)-1))] if walls else None;med=statistics.median(walls) if walls else None
  early=sorted(db.execute('select admitted_unix from labels where id like "v2_%"').fetchall())
  recent=db.execute('select count(*) from labels where id like "v2_%" and admitted_unix>?',(time.time()-3600,)).fetchone()[0]
  held=sum(ch['reserved_core_hours'] for ch in charges);spent=sum(ch['actual_core_hours'] or 0 for ch in charges)
  # Persist per-allocation actual charge so the existing attempt gate releases settled reservations.
  acc=[];slot_by_sample={};manifest_ids={};charge_by_slot={(ch['submission_id'],ch['index']):ch for ch in charges}
  for submission in submissions:
   manifest=submission['manifest']
   if manifest not in manifest_ids:manifest_ids[manifest]=[v['sample_id'] for v in verify_design(root,manifest)]
   for ix in submission['indices']:
    sid=manifest_ids[manifest][ix];slot_by_sample.setdefault(sid,[]).append(charge_by_slot[(submission['submission_id'],ix)])
  for a in entries:
   slots=slot_by_sample.get(a['sample_id'],[]);ordinal=a['ordinal_for_sample']-1
   if ordinal<len(slots):
    ch=slots[ordinal];acc.append({'attempt_id':a['attempt_id'],'terminal':ch['terminal'],'allocation_core_hours':ch['actual_core_hours']})
  write_json(RUN/'allocation_accounting.json',{'rows':acc})
  disk=sum(os.path.getsize(os.path.join(dp,f)) for dp,ds,fs in os.walk(RUN) for f in fs)
  stop=[]
  if disk>cfg['storage_limit_bytes']:stop.append('STORAGE_BUDGET_EXCEEDED')
  hard=[r for r in failures if r['simulation_status'] in ['schema_provenance_failure','runtime_native_load_failure']]
  if hard:stop.append('IDENTITY_SCHEMA_OR_RUNTIME_FAILURE_REQUIRES_REVIEW')
  if len(failures)>=3 and len(failures)/max(1,len(entries))>cfg['failure_rate_stop']:stop.append('FAILURE_RATE_EXCEEDS_PREREGISTERED_LIMIT')
  if submissions:
   last=submissions[-1];ids=[v['sample_id'] for v in verify_design(root,last['manifest'])];recent_receipts=[receipts[ids[i]] for i in last['indices'] if ids[i] in receipts]
   bad=sum(not r.get('qualified') for r in recent_receipts)
   if bad>=3 and bad/max(1,len(recent_receipts))>cfg['failure_rate_stop']:stop.append('RECENT_ARRAY_FAILURE_RATE_EXCEEDS_LIMIT')
  if memmax and memmax>cfg['memory_ramp_limit_MiB']:stop.append('MEMORY_RAMP_UNSAFE_REQUIRES_REVIEW')
  active=[ch for ch in charges if not ch['terminal']]
  concurrency=16 if len(entries)<16 else 32 if len(entries)<512 else cfg['max_array_concurrency']
  queue_counts={'RUNNING':0,'PENDING':0,'OTHER':0};queue_unknown=None
  job_ids=sorted({str(ch['job_id']).split('_')[0] for ch in active if ch.get('job_id')})
  if job_ids:
   try:
    q=subprocess.run(['squeue','--array','-j',','.join(job_ids),'-h','-o','%T'],capture_output=True,text=True,timeout=20)
    if q.returncode:queue_unknown=q.stderr.strip()
    else:
     for line in q.stdout.splitlines():queue_counts[line.strip() if line.strip() in queue_counts else 'OTHER']+=1
   except (OSError,subprocess.TimeoutExpired) as e:queue_unknown=repr(e)
  coverage={}
  for split in ['train','validation']:
   coverage[split]={}
   for name in read_json(root/'contracts/science_contract.json')['parameter_order']:
    lo,hi=db.execute('select min(json_extract(metadata,?)),max(json_extract(metadata,?)) from labels where split=?',('$.physical_parameters.'+name,'$.physical_parameters.'+name,split)).fetchone()
    coverage[split][name]={'min':lo,'max':hi}
  elapsed_hours=(time.time()-min(a['reserved_unix'] for a in entries))/3600 if entries else None
  qualified_v2=sum(r.get('qualified',False) for r in receipts.values())
  throughput=qualified_v2/elapsed_hours if elapsed_hours and elapsed_hours>0 else None
  remaining_points=sum(max(0,d['target']-d['qualified']) for d in data.values())
  result={'updated_at_unix':time.time(),'updated_at_hkt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'throughput_qualified_per_hour_since_v2_start':throughput,'throughput_observation_elapsed_hours':elapsed_hours,'qualified_per_1000_accounted_worker_core_hours':1000*qualified_v2/spent if spent else None,'estimated_remaining_wall_hours_at_observed_ramp_throughput':remaining_points/throughput if throughput else None,'ETA_caveat':'Extrapolation of measured ramp throughput; future concurrency and queue unknown; NOT a deadline','core_hour_accounting_scope':'v2 worker allocations only; v1/preflight/metadata/ML jobs reported separately','version':design['design_version'],'datasets':data,'v2_attempts_reserved':len(entries),'v2_submitted_slots':sum(len(s['indices']) for s in submissions),'v2_failed_current':len(failures),'running_or_pending_or_accounting_unresolved_slots':len(active),'running':queue_counts['RUNNING'],'pending':queue_counts['PENDING'],'queue_query_error':queue_unknown,'parameter_coverage':coverage,'success_rate_v2_receipted':sum(r.get('qualified',False) for r in receipts.values())/len(receipts) if receipts else None,'numerical_failed':sum(r.get('simulation_status')=='numerical_failure' for r in failures),'infrastructure_failed':sum(r.get('simulation_status')=='infrastructure_failure' for r in failures),'retry_success':sum(r.get('qualified',False) and latest[sid]['ordinal_for_sample']>1 for sid,r in receipts.items()),'max_array_concurrency':cfg['max_array_concurrency'],'current_ramp_concurrency':concurrency,'median_wall_seconds':med,'q90_wall_seconds':q90,'peak_memory_MiB':memmax,'new_v2_qualified_last_hour':recent,'v2_actual_core_hours_as_accounted':spent,'v2_reserved_core_hours':held,'disk_usage_bytes':disk,'storage_limit_bytes':cfg['storage_limit_bytes'],'estimated_remaining_core_hours_at_observed_median':sum(max(0,d['target']-d['qualified']) for d in data.values())*16*med/3600 if med else None,'observed_daily_throughput_requires_queue_uncertainty':True,'native_sha256':read_json(root/'contracts/science_contract.json')['native_sha256'],'science_contract_hash':cfg['science_contract_hash'],'sealed_labels_generated':False,'sealed_labels_read':False,'stop_reasons':stop,'status':'REQUIRES_REVIEW' if stop else 'RUNNING_OR_PENDING' if active else 'READY_FOR_NEXT_ARRAY'}
  write_json(root/'results/dataset_progress.json',result)
  text='# BT-xHI Dataset v2 生产进度\n\n更新时间（Unix）：%s\n\n| Split | Qualified | Target |\n|---|---:|---:|\n'%result['updated_at_unix']
  for split,d in data.items():text+='| %s | %d | %d |\n'%(split,d['qualified'],d['target'])
  text+='\n状态：%s；当前 ramp 并发 %d，上限 %d。\n\n完整运行、资源、classifier 比例与失败统计见 dataset_progress.json。\n\n封存设计保留，标签未生成、未读取；未启动生产 MCMC。\n'%(result['status'],concurrency,cfg['max_array_concurrency'])
  text+='\n| V2 attempts reserved | RUNNING | PENDING | Current failed | Retry success |\n|---:|---:|---:|---:|---:|\n| %d | %d | %d | %d | %d |\n'%(len(entries),queue_counts['RUNNING'],queue_counts['PENDING'],len(failures),result['retry_success'])
  for split,d in data.items():text+='\n%s classifier positive fraction: %s（negative histories 全保留）\n'%(split,d['positive_fraction'])
  text+='\nWall time median/q90: %s / %s seconds; max peak RSS: %s MiB.\n'%(med,q90,memmax)
  text+='\nV2 worker actual/reserved: %.3f / %.3f core-hours; projected remaining at observed median: %s core-hours. Metadata/v1/ML成本不含在此数内。\n'%(spent,held,result['estimated_remaining_core_hours_at_observed_median'])
  text+='\nMeasured ramp throughput: %s qualified/hour over %s hours; estimated remaining wall-hours at this early ramp rate: %s。未来并发及queue未知，此数不是完成时限。\n'%(throughput,elapsed_hours,result['estimated_remaining_wall_hours_at_observed_ramp_throughput'])
  text+='\nDisk: %d bytes / %d bytes cap; native: `%s`; config: `%s`.\n'%(disk,cfg['storage_limit_bytes'],result['native_sha256'],result['science_contract_hash'])
  text+='\nStop reasons: '+str(stop)+'\n'
  dest=root/'results/dataset_progress.md';tmp=dest.with_suffix('.tmp');tmp.write_text(text);tmp.replace(dest)
  for milestone in [10000,25000,50000,75000,100000]:
   path=RUN/'milestone_reports'/('%06d.json'%milestone)
   if data['train']['qualified']>=milestone and not path.exists():write_json(path,result,exclusive=True)
  if not stop and submit:
   try:
    sys.path.insert(0,str(root/'maintenance/v2'));from learning import advance
    advance()
   except Exception as error:write_json(RUN/'learning_curve_error.json',{'error':repr(error),'data_generation_continues':True})
  if stop or active or not submit:return
  if (RUN/'STOP_AUTOMATION').exists():return
  # Primary shards first, then finite reserve shards; original failures stay in denominator.
  stage='validation' if len(submissions)%4==3 and data['validation']['qualified']<10000 else 'train'
  if data[stage]['qualified']>=data[stage]['target']:stage='validation' if stage=='train' else 'train'
  if all(d['qualified']>=d['target'] for d in data.values()):return
  pick=None
  for reserve_phase in [False,True]:
   for shard in design['stages'][stage]:
    rows=verify_design(root,root/shard['manifest']);ix=[]
    for i,row in enumerate(rows):
     if (row['stratum']=='reserve_broad')!=reserve_phase:continue
     sid=row['sample_id'];rr=receipts.get(sid)
     if rr is None:
      # Unstarted scheduler slots are not silently resubmitted.
      if any(s['manifest']==str((root/shard['manifest']).resolve()) and i in s['indices'] for s in submissions):continue
      ix.append(i)
     elif not rr.get('qualified') and rr.get('simulation_status')=='infrastructure_failure' and sid in latest and latest[sid]['ordinal_for_sample']==1:ix.append(i)
    if ix:pick=(shard,ix);break
   if pick is not None:break
  if pick is None:
   result['status']='FINITE_DESIGN_EXHAUSTED_WITH_UNQUALIFIED_POINTS';write_json(root/'results/dataset_progress.json',result);return
  shard,indices=pick;remaining=data[stage]['target']-data[stage]['qualified']
  # v1 points already scheduled remain reserved for incorporation; do not replace them.
  if stage=='train':remaining-=max(0,4096-db.execute('select count(*) from labels where id not like "v2_%" and split="train"').fetchone()[0])
  if stage=='train':
   inherited=db.execute('select count(*) from labels where id not like "v2_%" and split="train"').fetchone()[0]
   planned_total=data[stage]['qualified']+max(0,4096-inherited)
   next_boundary=next((n for n in cfg['wave_totals'] if n>planned_total),100000)
   remaining=min(remaining,max(0,next_boundary-planned_total))
  indices=indices[:min(16 if not submissions else cfg['max_slots_per_array'],max(0,remaining))]
  if not indices:return
  # Stage concurrency lives in config; ramp config mutation is logged, gate unaffected scientifically.
  cfg['stages'][stage]['max_concurrent']=concurrency;write_json(BUDGET,cfg)
  cmd=[sys.executable,str(root/'scripts/submit_data_array.py'),'--project',str(root),'--budget',str(BUDGET),'--stage',stage,'--manifest',str(root/shard['manifest']),'--indices',','.join(map(str,indices)),'--submit']
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
  if r.returncode:raise RuntimeError('Bounded array submission failed: '+r.stderr)
  job=r.stdout.strip().split(';')[0]
  # Durable afterany auditor also handles killed workers that cannot execute a callback.
  cmd=['sbatch','--parsable','--account='+cfg['allowed_account'],'--partition='+cfg['allowed_partition'],'--qos='+cfg['allowed_qos'],'--reservation=tkcastrosim1','--cpus-per-task=1','--mem=4G','--time=15','--dependency=afterany:'+job,'--output='+str(RUN/'audit_%j.log'),str(root/'maintenance/v2/audit.sbatch')]
  a=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
  write_json(RUN/'audit_submissions'/(job+'.json'),{'array_job':job,'audit_job':a.stdout.strip(),'exit_code':a.returncode,'stderr':a.stderr,'command':cmd},exclusive=True)
  result.update(status='ARRAY_SUBMITTED',array_job=job,audit_job=a.stdout.strip());write_json(root/'results/dataset_progress.json',result)
  if a.returncode:raise RuntimeError('Array submitted but durable auditor submission failed; resume controller: '+a.stderr)
  print(json.dumps({'array_job':job,'audit_job':a.stdout.strip(),'stage':stage,'indices':indices,'concurrency':concurrency}))

if __name__=='__main__':
 try:controller('--submit' in sys.argv)
 except Exception as e:
  write_json(RUN/'controller_error.json',{'error':repr(e),'as_of_unix':time.time(),'existing_workers_untouched':True});raise
