"""Record user v2 authorization; migrate orchestration fingerprints only."""
import sys,json,copy,shutil,time
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'))
import hashlib,os,tempfile

def read_json(path):return json.loads(Path(path).read_text())
def file_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(dir=path.parent)
 with os.fdopen(fd,'w') as f:f.write(json.dumps(obj,indent=2)+'\n')
 os.replace(tmp,str(path))
archive=root/'contracts/authorization_history'/('20261004_v2_100k_%d'%time.time());archive.mkdir(parents=True)
files=['src/bt_history/data_control.py','src/bt_history/quarantine_admission.py','contracts/pipeline_integrity.json','contracts/orchestration_migration.json','contracts/selected_native_contract.json','configs/budget.json','configs/data_stage_budgets.json','configs/batch2_budget.json']
for f in files:
 dst=archive/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/f,dst)
p=root/'src/bt_history/data_control.py';s=p.read_text()
needle="if design['manifest_sha256'].get(relative)!=file_hash(manifest): raise ContractError('Manifest not frozen or digest changed')"
replacement="""if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if design['manifest_sha256'].get(relative)!=file_hash(manifest): raise ContractError('Manifest not frozen or digest changed')"""
if needle in s:s=s.replace(needle,replacement)
s=s.replace("b.get('dataset_design_sha256')!=file_hash(project/'contracts/dataset_design.json')", "b.get('dataset_design_sha256')!=file_hash(project/b.get('dataset_design_contract','contracts/dataset_design.json'))")
p.write_text(s)
p=root/'src/bt_history/quarantine_admission.py';s=p.read_text();needle="'maintenance/learning_curve_controller.py'}";replacement="'maintenance/learning_curve_controller.py','maintenance/v2/advance.py','maintenance/v2/worker.sbatch','maintenance/v2/audit.sbatch','maintenance/v2/learning.py'}";s=s.replace(needle,replacement);s=s.replace("'maintenance/v2/audit.sbatch'}","'maintenance/v2/audit.sbatch','maintenance/v2/learning.py'}");p.write_text(s)
integrity=read_json(root/'contracts/pipeline_integrity.json')
for f in ['src/bt_history/data_control.py','src/bt_history/quarantine_admission.py','maintenance/v2/advance.py','maintenance/v2/worker.sbatch','maintenance/v2/audit.sbatch','maintenance/v2/learning.py']:integrity['files'][f]=file_hash(root/f)
integrity['approval_reference']='user_explicit_100k_10k_v2_20261004';write_json(root/'contracts/pipeline_integrity.json',integrity)
sha=file_hash(root/'contracts/pipeline_integrity.json');m=read_json(root/'contracts/orchestration_migration.json');m['to_pipeline_sha256']=sha;old=read_json(root/m['original_pipeline_path'])['files'];m['changed_files']=sorted(k for k in set(old)|set(integrity['files']) if old.get(k)!=integrity['files'].get(k));m['v2_approval_reference']='user_explicit_100k_10k_v2_20261004';m['v2_scope']='Independent designs, existing exact worker/QA/native/postprocessing unchanged; sharded bounded orchestration';write_json(root/'contracts/orchestration_migration.json',m)
sel=read_json(root/'contracts/selected_native_contract.json');sel['accepted_training_pipeline_sha256']=list(dict.fromkeys(sel['accepted_training_pipeline_sha256']+[sha]));write_json(root/'contracts/selected_native_contract.json',sel)
for name in ['budget.json','data_stage_budgets.json','batch2_budget.json']:
 p=root/'configs'/name;b=read_json(p);b.update(pipeline_integrity_sha256=sha,selected_native_contract_sha256=file_hash(root/'contracts/selected_native_contract.json'));write_json(p,b)
d=read_json(root/'contracts/dataset_design_v2_100k.json');b=copy.deepcopy(read_json(root/'configs/batch2_budget.json'));b.update(budget_id='dataset_v2_100k',approval_reference='user_explicit_100k_10k_v2_20261004',dataset_design_contract='contracts/dataset_design_v2_100k.json',dataset_design_sha256=file_hash(root/'contracts/dataset_design_v2_100k.json'),max_concurrent_tasks=64,max_array_concurrency=64,max_slots_per_array=512,worker_script='maintenance/v2/worker.sbatch',storage_limit_bytes=500*1024**3,failure_rate_stop=.05,memory_ramp_limit_MiB=12288,target_totals={'train':100000,'validation':10000},wave_totals=[10000,25000,50000,75000,100000])
previous_v2=read_json(root/'configs/v2_100k_budget.json') if (root/'configs/v2_100k_budget.json').exists() else {}
for stage in ['train','validation']:
 spec=b['stages'][stage];spec.pop('allowed_indices',None)
 spec['manifests']=[sh['manifest'] for sh in d['stages'][stage]]
 n=sum(sh['count'] for sh in d['stages'][stage])
 spec.update(max_attempts=n*2,max_retry_attempts=n,max_retries_per_sample=1,max_concurrent=previous_v2.get('stages',{}).get(stage,{}).get('max_concurrent',16),recover_history_on_LF_grid_error=True)
b['max_evaluations']=sum(b['stages'][s]['max_attempts'] for s in ['train','validation']);write_json(root/'configs/v2_100k_budget.json',b)
write_json(root/'contracts/v2_100k_authorization.json',{'authorization':'user_explicit_100k_10k_v2_20261004','scope':b['target_totals'],'sealed_generation_authorized':False,'max_array_concurrency':64,'cpus_per_evaluation':16,'memory_MiB':16384,'wall_seconds':7200,'max_attempts':b['max_evaluations'],'storage_limit_bytes':b['storage_limit_bytes'],'core_hour_cap_removed_by_user':True,'policy_limits_not_performance_prediction':True,'prior_and_physics_unchanged':True,'archive':str(archive.relative_to(root)),'qualification_sha256_unchanged':file_hash(root/'results/native_qualification.json')})
print('Activated v2 orchestration; scientific/native/QA unchanged')
