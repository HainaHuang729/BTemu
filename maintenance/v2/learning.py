"""Finite larger learning-curve jobs; immutable data snapshots and one ML job at a time."""
import sys,json,subprocess,sqlite3,time,os
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'))
from bt_history.data_control import read_json,write_json,locked
from bt_history.contracts import file_hash
BASE=root/'artifacts/learning_curve_v2_100k'

def advance():
 BASE.mkdir(parents=True,exist_ok=True)
 with locked(BASE/'controller.lock'):
  status_path=BASE/'status.json';state=read_json(status_path) if status_path.exists() else {'milestones':{},'max_concurrent_training':1,'max_additional_jobs':7,'validation':'same frozen v1 144 benchmark; v2 full validation evaluated separately after qualification','sealed_access':False,'production_accepted':False}
  for row in state['milestones'].values():
   if row['status']=='SUBMITTED':
    r=subprocess.run(['sacct','-j',row['job_id'],'-n','-P','--format=JobID,State'],capture_output=True,text=True,timeout=20)
    if r.returncode:return
    terminal=next((s.split('|')[1].split()[0] for s in r.stdout.splitlines() if s.split('|')[0]==row['job_id']),None)
    if terminal not in ['COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED','NODE_FAIL']:return
    completed=(root/row['run']/'complete.json').exists();row['status']='COMPLETED' if terminal=='COMPLETED' and completed else 'FAILED_REQUIRES_REVIEW'
    if not completed:write_json(status_path,state);return
  db=sqlite3.connect('file:'+str(root/'data_runs/dataset_v2_100k/dataset_manifest.sqlite')+'?mode=ro',uri=True)
  reference=read_json(root/'artifacts/development_history_fidelity_20261003/manifest.json');val=[it for it in reference['files'] if it['split']=='validation']
  for n in [2048,4096,8192,16384,32768,65536,100000]:
   if str(n) in state['milestones']:continue
   plan=read_json(root/'manifests/v2_100k/learning_curves'/('train_%06d.json'%n));items=[];missing=[]
   for sid in plan['sample_ids']:
    r=db.execute('select item from labels where id=? and split="train"',(sid,)).fetchone()
    if not r:missing.append(sid)
    else:items.append(json.loads(r[0]))
   if missing:
    state['next_milestone']={'N':n,'status':'WAITING_FOR_FROZEN_LABELS','missing_count':len(missing)};write_json(status_path,state);return
   reuse=None
   if n<=4096:
    prior=root/'artifacts/learning_curve_fixed_validation_v1'/('N%d'%n)
    status=read_json(prior/'status.json') if (prior/'status.json').exists() else {}
    if status.get('status')!='DEVELOPMENT_TRAINING_COMPLETED':
     state['next_milestone']={'N':n,'status':'WAITING_FOR_EXISTING_DIRECT_BENCHMARK'};write_json(status_path,state);return
    reuse=str(prior.relative_to(root))
   run=BASE/('N_%06d'%n);run.mkdir(exist_ok=False)
   snapshot=run/'snapshot.json';write_json(snapshot,{'role':'development','schema_version':'v2_explicit_snapshot','files':items+val,'parameter_ID_subset_sha256':file_hash(root/'manifests/v2_100k/learning_curves'/('train_%06d.json'%n)),'validation_snapshot_sha256':file_hash(root/'artifacts/development_history_fidelity_20261003/manifest.json'),'split_frozen':True},exclusive=True)
   write_json(run/'plan.json',{'snapshot_sha256':file_hash(snapshot),'training_config_sha256':file_hash(root/'configs/training.json'),'model_implementation_sha256':file_hash(root/'maintenance/v2/models.py'),'baseline_implementation_sha256':file_hash(root/'maintenance/v2/baseline.py'),'driver_sha256':file_hash(root/'maintenance/v2/run_curve.py'),'N':n,'reuse_direct_run':reuse,'validation_n':len(val),'all_five_seeds_retained':True,'production_accepted':False},exclusive=True)
   cmd=['sbatch','--parsable','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--cpus-per-task=1','--mem=8G','--time=480','--output='+str(run/'job_%j.log'),str(root/'maintenance/v2/curve.sbatch'),str(run)]
   r=subprocess.run(cmd,capture_output=True,text=True,timeout=30);write_json(run/'submission.json',{'command':cmd,'job_id':r.stdout.strip(),'exit_code':r.returncode,'stderr':r.stderr})
   if r.returncode:raise RuntimeError('Learning-curve submission failed '+r.stderr)
   state['milestones'][str(n)]={'N':n,'status':'SUBMITTED','job_id':r.stdout.strip().split(';')[0],'run':str(run.relative_to(root))};state.pop('next_milestone',None);write_json(status_path,state);return
if __name__=='__main__':advance()
