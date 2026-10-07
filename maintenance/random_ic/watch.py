"""Bounded scheduler watcher: complete scientific audit, then activate production."""
import sys,json,subprocess,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,read_json,write_json,file_hash,audit_gate
from bt_history.data_control import locked

def schedule():
 cmd=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1','--cpus-per-task=1','--mem=4G','--time=10','--begin=now+10minutes','--account=tkcastrosim','--partition=chpc','--qos=tkcastrosim','--reservation=tkcastrosim1','--nodelist=chpc-cn[057-064]','--job-name=bt_random_audit_gate','--output='+str(RUN/'gate_%j.log'),str(ROOT/'maintenance/random_ic/watch.sbatch')]
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
 if r.returncode:raise RuntimeError('Gate watcher submission failed: '+r.stderr)
 return {'job_id':r.stdout.strip().split(';')[0],'command':cmd}

def main():
 with locked(RUN/'gate_watch.lock'):
  path=ROOT/'results/random_ic_activation_status.json';state=read_json(path) if path.exists() else {'checks':0,'max_checks':432,'user_authorization':'Start large scale after full IC audit passes; user explicitly chose wait for audit 2026-10-07','random_IC_production_started':False}
  state['checks']+=1;state['updated_at_unix']=time.time()
  summary=read_json(ROOT/'results/ic_sensitivity_report.json');acceptance=read_json(ROOT/'contracts/ic_audit_acceptance.json');ok,reason=audit_gate(summary,acceptance)
  state['audit_complete_families']=summary.get('complete_families',0);state['audit_decision']=reason
  if ok:
   families=read_json(ROOT/'data_runs/ic_audit_v1/family_statistics.json')['families']
   if len(families)!=128 or any(f['IC_count']!=8 for f in families):raise ValueError('Full 128x8 evidence missing')
   qualification={'qualified':True,'scope':'one independent random IC per theta for development production only, not posterior validation','audit_report_sha256':file_hash(ROOT/'results/ic_sensitivity_report.json'),'family_statistics_sha256':file_hash(ROOT/'data_runs/ic_audit_v1/family_statistics.json'),'acceptance_sha256':file_hash(ROOT/'contracts/ic_audit_acceptance.json'),'authorized_at_unix':time.time(),'sealed_labels_generation_authorized':False}
   q=ROOT/'results/random_ic_production_qualification.json'
   if not q.exists():write_json(q,qualification,exclusive=True)
   from advance import main as advance
   advance();state['status']='PRODUCTION_ACTIVATED';state['random_IC_production_started']=True
  elif summary.get('status')=='COMPLETE':
   state['status']='AUDIT_NOT_PASSED_PRODUCTION_NOT_SUBMITTED';state['next_action']='Evaluate finite 2/4/8-IC mean convergence and define multi-IC target; do not waive thresholds.'
  elif state['checks']>=state['max_checks']:state['status']='BOUNDED_WATCH_LIMIT_REACHED_NO_PRODUCTION'
  else:
   state['status']='WAITING_FOR_COMPLETE_AUDIT';state['next_watch']=schedule()
  write_json(path,state);print(json.dumps(state))
if __name__=='__main__':main()
