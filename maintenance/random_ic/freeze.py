"""Bind a conditional finite production budget after offline parameter design."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,read_json,write_json,file_hash
p=ROOT/'contracts/dataset_design_random_ic_v2.json';d=read_json(p)
files=sorted(str(f.relative_to(ROOT)) for f in (ROOT/'maintenance/random_ic').glob('*') if f.suffix in ['.py','.sbatch'])
b={'authorized':False,'conditional_approval_reference':'PUBLIC_TEMPLATE_NO_EXECUTION_AUTHORIZATION','mandatory_audit_gate':'complete 128 theta x8 IC, confirmed thresholds and diagnostic review passed','design_sha256':file_hash(p),'max_attempts':230240,'max_unique_points_including_finite_reserves':115120,'max_retries_per_sample':1,'retry_statuses':['infrastructure_failure'],'max_concurrent':16,'wave_size':128,'cpus_per_simulation':16,'memory_MiB':16384,'wall_seconds':7200,'allowed_node_scope':'chpc-cn[057-064]','core_hour_cap':None,'core_hour_cap_note':'Prior 2000 core-hour cap explicitly removed by user; attempts/resources remain finite and all allocations charged','storage_limit_bytes':100*1024**3,'failure_rate_stop':0.05,'targets':{'train':100000,'validation':10000},'sealed_generation_authorized':False,'implementation_sha256':{f:file_hash(ROOT/f) for f in files}}
f=ROOT/'configs/random_ic_v2_budget.json'
if f.exists():
 if read_json(f)!=b:raise ValueError('Existing conditional production budget differs; no overwrite')
else:write_json(f,b,exclusive=True)
write_json(ROOT/'results/random_ic_design_status.json',{'status':'FROZEN_DESIGN_ONLY','target_unique_theta':d['target_unique_theta'],'finite_reserves':{'train':4096,'validation':1024},'design_sha256':file_hash(p),'budget_sha256':file_hash(f),'random_IC_labels_generated':0,'sealed_labels_generated':False,'selected_native_sha256':d['native_sha256'],'authorization_condition':'Complete IC audit must pass; no simulations submitted by design generation'})
print(json.dumps({'status':'FROZEN_DESIGN_ONLY','targets':d['target_unique_theta']}))
