"""Random-IC production gates; reuse approved physics/runtime and accounting."""
import json,sys,sqlite3,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from bt_history.data_control import read_json,write_json,check_execution_gate
from bt_history.contracts import file_hash,digest
RUN=ROOT/'data_runs/random_ic_v2'

def audit_gate(summary,acceptance):
 if acceptance.get('status')!='CONFIRMED':return False,'THRESHOLDS_UNCONFIRMED'
 if summary.get('status')!='COMPLETE' or summary.get('complete_families')!=128:return False,'AUDIT_INCOMPLETE'
 if summary.get('qualified_fresh_IC_realizations')!=896 or summary.get('failed'):return False,'AUDIT_INCOMPLETE_OR_FAILED'
 if summary.get('single_IC_production_decision')!='RANDOM_IC_SINGLE_REALIZATION_SUPPORTED':return False,summary.get('single_IC_production_decision','AUDIT_NOT_QUALIFIED')
 if not summary.get('confirmed_core_screen_pass') or not summary.get('additional_proposed_diagnostic_screen_pass'):return False,'AUDIT_DIAGNOSTIC_REVIEW_REQUIRED'
 return True,'AUDIT_PASSED'

def qualification():
 s=read_json(ROOT/'results/ic_sensitivity_report.json');a=read_json(ROOT/'contracts/ic_audit_acceptance.json');ok,reason=audit_gate(s,a)
 if not ok:raise PermissionError(reason)
 if s.get('acceptance_contract_sha256')!=file_hash(ROOT/'contracts/ic_audit_acceptance.json'):raise ValueError('Audit accepted different criteria')
 q=read_json(ROOT/'results/random_ic_production_qualification.json')
 for name,key in [('results/ic_sensitivity_report.json','audit_report_sha256'),('data_runs/ic_audit_v1/family_statistics.json','family_statistics_sha256'),('contracts/ic_audit_acceptance.json','acceptance_sha256'),('contracts/random_ic_v2_target.json','target_contract_sha256')]:
  if file_hash(ROOT/name)!=q[key]:raise ValueError('Approved audit evidence changed: '+name)
 return q

def policy(require_runtime=False):
 qualification();b=read_json(ROOT/'configs/random_ic_v2_budget.json');d=read_json(ROOT/'contracts/dataset_design_random_ic_v2.json')
 if not b['authorized'] or b['max_attempts']!=230240 or b['max_concurrent']>16:raise PermissionError('Random budget not authorized')
 if file_hash(ROOT/'contracts/dataset_design_random_ic_v2.json')!=b['design_sha256']:raise ValueError('Design changed')
 for f,sha in b['implementation_sha256'].items():
  if file_hash(ROOT/f)!=sha:raise ValueError('Production implementation changed: '+f)
 c,base,_=check_execution_gate(ROOT,'train',ROOT/'configs/v2_100k_budget.json',ROOT/'manifests/v2_100k/train_0000.jsonl',require_runtime=require_runtime)
 if file_hash(ROOT/'contracts/science_contract.json')!=d['base_science_contract_sha256']:raise ValueError('Physics changed')
 if require_runtime and (int(os.environ['SLURM_CPUS_PER_TASK'])!=16 or os.environ.get('SLURM_ARRAY_TASK_ID') is None):raise ValueError('Wrong worker allocation')
 spec=dict(base);spec.update(max_attempts=b['max_attempts'],global_max_attempts=b['max_attempts'],max_retry_attempts=115120,max_retries_per_sample=1,allowed_retry_statuses=['infrastructure_failure'],max_concurrent=b['max_concurrent'],global_max_concurrent=b['max_concurrent'],max_reserved_core_hours=float('inf'),global_max_reserved_core_hours=float('inf'))
 return c,d,b,spec

def connection():
 return sqlite3.connect('file:'+str(RUN/'design.sqlite')+'?mode=ro',uri=True)

def row(index):
 with connection() as db:r=db.execute('SELECT payload FROM design WHERE idx=?',(index,)).fetchone()
 if r is None:raise ValueError('Unknown random design index')
 r=json.loads(r[0])
 if r['split']=='sealed_test':raise PermissionError('Sealed-label generation forbidden')
 d=read_json(ROOT/'contracts/dataset_design_random_ic_v2.json');remaining=index
 for split in ['train','validation','sealed_test']:
  for shard in d['stages'][split]['shards']:
   if remaining<shard['count']:
    path=ROOT/shard['manifest']
    if file_hash(path)!=d['manifest_sha256'][shard['manifest']]:raise ValueError('Frozen assigned manifest changed')
    with path.open() as f:
     for i,line in enumerate(f):
      if i==remaining:
       if json.loads(line)!=r:raise ValueError('Index and frozen manifest disagree')
       return r
   remaining-=shard['count']
 raise ValueError('Frozen manifest index missing')
