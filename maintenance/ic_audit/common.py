"""Supplemental IC audit gate reusing frozen native/runtime/resource safeguards."""
import os,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from bt_history.data_control import read_json,write_json,check_execution_gate
from bt_history.contracts import file_hash,digest
RUN=ROOT/'data_runs/ic_audit_v1'

def policy(require_runtime=False):
 b=read_json(ROOT/'configs/ic_audit_budget.json');a=read_json(ROOT/'contracts/ic_audit_v1.json')
 if not b['authorized'] or b['max_new_evaluations']!=896 or b['max_attempts']>1024:raise PermissionError('Audit budget missing or expanded')
 if file_hash(ROOT/'contracts/ic_audit_v1.json')!=b['audit_contract_sha256']:raise ValueError('Audit contract changed')
 if file_hash(ROOT/a['manifest'])!=a['manifest_sha256'] or file_hash(RUN/'families.json')!=a['families_sha256']:raise ValueError('Frozen IC schedule/families changed')
 for f,sha in b['implementation_sha256'].items():
  if file_hash(ROOT/f)!=sha:raise ValueError('Audit implementation changed: '+f)
 if file_hash(ROOT/'contracts/science_contract.json')!=a['base_science_contract_sha256']:raise ValueError('Base scientific target changed')
 # Reuse the existing gate to enforce exact native identity, existing approved runtime,
 # fixed physics, frozen pipeline and compute allocation. This does not reserve a
 # fixed-IC Train attempt; only the separate finite audit ledger below is charged.
 c,base,_=check_execution_gate(ROOT,'train',ROOT/'configs/v2_100k_budget.json',ROOT/'manifests/v2_100k/train_0000.jsonl',require_runtime=require_runtime)
 if require_runtime:
  if int(os.environ['SLURM_CPUS_PER_TASK'])!=b['cpus']:raise ValueError('Audit CPU mismatch')
  if os.environ.get('SLURM_ARRAY_TASK_ID') is None:raise ValueError('Audit worker must be a frozen array task')
 spec=dict(base);spec.update(max_attempts=b['max_attempts'],global_max_attempts=b['max_attempts'],max_retry_attempts=b['max_infrastructure_retries'],max_retries_per_sample=1,allowed_retry_statuses=['infrastructure_failure'],max_concurrent=b['max_concurrent'],global_max_concurrent=b['max_concurrent'],max_reserved_core_hours=b['max_core_hours'],global_max_reserved_core_hours=b['max_core_hours'])
 return c,a,b,spec

def rows():
 a=read_json(ROOT/'contracts/ic_audit_v1.json');return [json.loads(x) for x in (ROOT/a['manifest']).read_text().splitlines()]
