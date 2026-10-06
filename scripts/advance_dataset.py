"""Continue explicitly authorized frozen slices through the existing bounded submitter."""
import argparse,json,sys,subprocess,time,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.data_control import read_json,write_json,locked,AttemptLedger,verify_design,retry_authorized,core_hour_limit
from bt_history.contracts import file_hash
from bt_history.submission_accounting import submission_charges,confirmed_array_rejection
from bt_history.quarantine_admission import qualified_pipeline_matches

def main(root,budget):
 root=Path(root);b=read_json(budget);run=root/'data_runs'/b['budget_id']
 with locked(run/'advance.lock'):
  q=read_json(root/'results/native_qualification.json')
  if not q.get('qualified_for_batch1') or not qualified_pipeline_matches(root,q):raise PermissionError('Scientific qualification required')
  ledger=AttemptLedger(run);attempts=ledger.entries();latest={a['sample_id']:a for a in attempts};receipts={}
  for sid,a in latest.items():
   f=run/'receipts'/(a['attempt_id']+'.json')
   if f.exists():receipts[sid]=read_json(f)
  path=run/'submissions.jsonl';subs=[json.loads(x) for x in path.read_text().splitlines()] if path.exists() else [];charges=submission_charges(run,subs,b)
  write_json(run/'submission_accounting.json',{'rows':charges,'as_of_unix':time.time()})
  active_subs=[s for s in subs if not confirmed_array_rejection(run,s)]
  accounting=[]
  for a in attempts:
   ss=[s for s in active_subs if s['stage']==a['stage'] and int(a.get('manifest_index',a['slurm_array_task_id'])) in s['indices']]
   idx=a['ordinal_for_sample']-1
   ch=next((c for c in charges if idx<len(ss) and c['submission_id']==ss[idx]['submission_id'] and c['index']==int(a.get('manifest_index',a['slurm_array_task_id']))),None)
   if ch:accounting.append({'attempt_id':a['attempt_id'],'terminal':ch['terminal'],'allocation_core_hours':ch['actual_core_hours']})
  write_json(run/'allocation_accounting.json',{'rows':accounting})
  designs={st:verify_design(root,root/b['stages'][st]['manifests'][0]) for st in ['train','validation']}
  table={};failures=[]
  manifest=read_json(root/'manifests/qualified_history_recovered_v1.json')
  for st in ['train','validation']:
   wanted=[designs[st][i] for i in b['stages'][st]['allowed_indices']];good=0;bad=0;tried=0
   for row in wanted:
    sid=row['sample_id'];rr=receipts.get(sid);tried+=sid in latest
    if not rr:continue
    if rr.get('qualified'):
     path=root/rr['artifact_path']/'label.json'
     if file_hash(path)!=rr['label_sha256']:raise ValueError('Qualified artifact changed')
     good+=1;manifest['files'].append({'sample_id':sid,'split':st,'role':'development','path':str(path.relative_to(root)),'sha256':rr['label_sha256'],'receipt':str((run/'receipts'/(rr['attempt_id']+'.json')).relative_to(root))})
    else:bad+=1;failures.append(rr)
   table[st]={'planned':len(wanted),'attempted_unique':tried,'attempts':sum(a['stage']==st for a in attempts),'qualified':good,'failed':bad,'unattempted':len(wanted)-tried}
  write_json(root/'manifests/qualified_batch2_development.json',manifest);write_json(run/'failure_registry.json',{'rows':failures})
  # Endpoint metadata is diagnostic; its warning flags never remove labels.
  try:
   sys.path.insert(0,str(root/'maintenance'))
   from semantic_audit import write_endpoint_sidecars
   write_endpoint_sidecars(root,root/'manifests/qualified_batch2_development.json',true_numerical_failure_count=sum(rr.get('simulation_status')=='numerical_failure' for rr in receipts.values()))
  except Exception as error:write_json(root/'results/endpoint_audit_error.json',{'error':repr(error),'labels_unchanged':True})
  # Finite preregistered training milestones do not delay or stop label production.
  try:
   sys.path.insert(0,str(root/'maintenance'))
   from learning_curve_controller import advance_learning_curve
   advance_learning_curve(root)
  except Exception as error:write_json(root/'results/learning_curve_controller_error.json',{'error':repr(error),'data_generation_continues':True})
  all_done=all(all(designs[st][i]['sample_id'] in receipts for i in b['stages'][st]['allowed_indices']) for st in designs)
  state={'budget_id':b['budget_id'],'table':table,'as_of_unix':time.time(),'all_planned_attempted':all_done,'charged_core_hours':sum(c['charged_core_hours'] for c in charges),'reserved_core_hours':sum(c['reserved_core_hours'] for c in charges),'email_sent':False,'sealed_access':False}
  def save(status,**kw):write_json(run/'continuation_status.json',{**state,'status':status,**kw})
  if (run/'STOP_AUTOMATION').exists():save('STOPPED_EXPLICITLY');return
  # Only start a new wave when every submitted slot has published a receipt.
  for s in active_subs:
   for ix in s['indices']:
    sid=designs[s['stage']][ix]['sample_id'];submitted=sum(ss['stage']==s['stage'] and ix in ss['indices'] for ss in active_subs);done=sum(a['sample_id']==sid and (run/'receipts'/(a['attempt_id']+'.json')).exists() for a in attempts)
    if done<submitted:save('DATA_BATCH_RUNNING');return
  candidates={}
  for st in designs:
   spec=b['stages'][st];retry_used=sum(a['stage']==st and a['ordinal_for_sample']>1 for a in attempts);ixs=[]
   for ix in spec['allowed_indices']:
    sid=designs[st][ix]['sample_id'];rr=receipts.get(sid)
    if rr is None:ixs.append(ix)
    elif not rr.get('qualified') and retry_used<spec['max_retry_attempts'] and latest[sid]['ordinal_for_sample']<=spec['max_retries_per_sample'] and retry_authorized(spec,latest[sid],rr):ixs.append(ix);retry_used+=1
   candidates[st]=ixs
  if not any(candidates.values()):
   from bt_history.history_dataset import load_development
   from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
   c=read_json(root/'contracts/science_contract.json');rows,_=load_development(root/'manifests/qualified_batch2_development.json',c,OriginalPostprocessingAdapter(c));save('DATA_BATCH_COMPLETED' if not failures else 'DATA_BATCH_PARTIAL',loader_passed=True,total_loaded=len(rows));return
  # Alternate stages so independent validation is produced early.
  preferred='validation' if not subs or subs[-1]['stage']=='train' else 'train'
  st=preferred if candidates[preferred] else next(st for st in candidates if candidates[st])
  # Queue/run reservations plus actual costs share one cap; reduce wave near exhaustion.
  available=core_hour_limit(b)-sum(c['charged_core_hours'] for c in charges);per=b['stages'][st]['cpus']*b['stages'][st]['wall_seconds']/3600
  count=min(b['max_concurrent_tasks'],(b['max_concurrent_tasks'] if available==float('inf') else int(max(0,available)//per)),len(candidates[st]))
  if count==0:save('BUDGET_EXHAUSTED');return
  indices=candidates[st][:count];cmd=[sys.executable,str(root/'scripts/submit_data_array.py'),'--project',str(root),'--budget',str(budget),'--stage',st,'--manifest',str(root/b['stages'][st]['manifests'][0]),'--indices',','.join(map(str,indices)),'--submit']
  deps=sorted({c['job_id'] for c in charges if not c['terminal'] and c.get('job_id')})
  if deps:cmd+=['--dependency','afterany:'+':'.join(deps)]
  result=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
  if result.returncode:save('BUDGET_OR_SUBMISSION_STOP',error=result.stderr);raise RuntimeError(result.stderr)
  save('DATA_BATCH_SUBMITTED',submitted_job=result.stdout.strip(),stage=st,indices=indices);print(result.stdout.strip())
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--budget',required=True);a=ap.parse_args();main(a.project,a.budget)
