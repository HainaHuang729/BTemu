"""Frozen designs, atomic artifacts, finite attempts and deny-by-default seals."""
import contextlib
import fcntl
import json
import os
from pathlib import Path
import tempfile
import time
from .contracts import digest, file_hash, ContractError

RETRYABLE = {'infrastructure_failure', 'timeout', 'out_of_memory', 'runtime_native_load_failure'}
STAGES = ('preflight', 'train', 'validation', 'challenge_development', 'sealed_test')

def read_json(path):
    return json.loads(Path(path).read_text())

def write_json(path, value, *, exclusive=False):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(value,indent=2,allow_nan=False)+'\n'
    if exclusive:
        with path.open('x') as f: f.write(data); f.flush(); os.fsync(f.fileno())
        return
    fd,name=tempfile.mkstemp(prefix='.'+path.name,dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f: f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name): os.unlink(name)

def read_design(path):
    rows=[json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    if len({r['sample_id'] for r in rows})!=len(rows): raise ContractError('Duplicate sample IDs')
    return rows

def verify_design(project, manifest):
    project=Path(project); manifest=Path(manifest).resolve()
    design=read_json(project/'contracts/dataset_design.json')
    try: relative=str(manifest.relative_to(project.resolve()))
    except ValueError: raise ContractError('Manifest outside frozen project')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if relative not in design['manifest_sha256']:
        registry=project/'contracts/dataset_design_v2_100k.json'
        if not registry.exists():raise ContractError('Manifest not frozen')
        design=read_json(registry)
        if design.get('preserved_v1_design_sha256')!=file_hash(project/'contracts/dataset_design.json'):raise ContractError('v2 preserved v1 identity mismatch')
        if design.get('science_contract_hash')!=digest(read_json(project/'contracts/science_contract.json')):raise ContractError('v2 target mismatch')
    if design['manifest_sha256'].get(relative)!=file_hash(manifest): raise ContractError('Manifest not frozen or digest changed')
    return read_design(manifest)

def assert_development_path(path, role):
    # Sealed payload and logs are encrypted, never accepted by any development loader.
    if role not in {'train','validation','preflight','challenge_development','development'}: raise PermissionError('Sealed labels cannot be opened here')
    p=Path(path).resolve()
    if any('quarantine' in part.lower() for part in p.parts):raise PermissionError('Quarantined label location forbidden in development loader')
    if any('sealed' in part.lower() for part in p.parts) or p.suffix in {'.gpg','.age'}: raise PermissionError('Sealed location forbidden in development loader')

def core_hour_limit(budget,stage=None):
    value=budget['stages'][stage]['max_reserved_core_hours'] if stage else budget.get('max_total_core_hours',float('inf'))
    if value is None:
        if budget.get('core_hour_limit_removed') is not True or not budget.get('core_hour_limit_removal_approval'):raise PermissionError('Removing core-hour cap requires explicit authorization')
        return float('inf')
    if value<0:raise PermissionError('Negative core-hour cap')
    return value

def check_execution_gate(project, stage, budget, manifest, *, require_runtime=True):
    project=Path(project); c=read_json(project/'contracts/science_contract.json')
    selected=read_json(project/'contracts/selected_native_contract.json')
    if selected.get('confirmed') is not True or selected.get('approval_reference') is None: raise PermissionError('Selected full native hash not confirmed')
    if selected['native_sha256']!=c['native_sha256'] or file_hash(selected['native_path'])!=c['native_sha256']: raise ContractError('Native identity changed')
    if not selected.get('compatible_runtime_approved') or not selected.get('runtime_approval_reference') or not selected.get('allowed_runtime_fingerprints'):
        raise PermissionError('Compatible isolated runtime not approved')
    b=read_json(budget); s=dict(b.get('stages',{}).get(stage,{}))
    if b.get('max_evaluations',0)<=0:raise PermissionError('Global attempt budget is zero')
    s['max_reserved_core_hours']=core_hour_limit(b,stage);s['global_max_reserved_core_hours']=core_hour_limit(b);s['global_max_attempts']=b['max_evaluations'];s['global_max_concurrent']=b.get('max_concurrent_tasks',0)
    if not b.get('authorized') or not b.get('approval_reference') or not s.get('authorized') or s.get('max_attempts',0)<=0: raise PermissionError('No nonzero approved stage budget')
    if b.get('science_contract_hash')!=digest(c) or b.get('dataset_design_sha256')!=file_hash(project/b.get('dataset_design_contract','contracts/dataset_design.json')): raise ContractError('Budget not bound to frozen contracts')
    if b.get('selected_native_contract_sha256')!=file_hash(project/'contracts/selected_native_contract.json'): raise ContractError('Budget native selection changed')
    for name,sha in b.get('policy_sha256',{}).items():
        if file_hash(project/name)!=sha:raise ContractError('Approved QA/split/seal policy changed')
    if set(b.get('policy_sha256',{}))!={'contracts/data_quality_protocol.json','contracts/split_policy.json','contracts/sealed_test_policy.json'}:raise ContractError('Budget lacks frozen data policies')
    integrity=read_json(project/'contracts/pipeline_integrity.json')
    if b.get('pipeline_integrity_sha256')!=file_hash(project/'contracts/pipeline_integrity.json'):raise ContractError('Pipeline is not budget-frozen')
    for name,sha in integrity['files'].items():
        if file_hash(project/name)!=sha:raise ContractError('Generation/QA pipeline changed')
    verify_design(project,manifest)
    relative=str(Path(manifest).resolve().relative_to(project.resolve()))
    if relative not in s['manifests']: raise ContractError('Manifest not approved for this stage')
    if not b.get('allowed_partition') or not b.get('allowed_account'): raise PermissionError('Approved Slurm partition/account missing')
    if require_runtime:
        env=os.environ
        if s.get('allowed_node_scope')=='chpc-cn[057-064]' and os.uname().nodename.split('.')[0] not in ['chpc-cn%03d'%n for n in range(57,65)]:raise PermissionError('Worker outside approved nodes')
        if not env.get('SLURM_JOB_ID') or int(env.get('SLURM_CPUS_PER_TASK','0'))!=s['cpus']: raise PermissionError('Require exact approved Slurm CPU allocation')
        if env.get('SLURM_JOB_PARTITION')!=b['allowed_partition'] or env.get('SLURM_JOB_ACCOUNT')!=b['allowed_account']: raise PermissionError('Slurm account/partition differs from approval')
        import subprocess,re
        job=subprocess.run(['scontrol','show','job','-o',env['SLURM_JOB_ID']],check=True,capture_output=True,text=True,timeout=20).stdout
        found=re.search(r'(?:^| )TimeLimit=([^ ]+)',job)
        if not found:raise PermissionError('Cannot verify Slurm wall-time allocation')
        value=found.group(1);days,clock=(value.split('-',1) if '-' in value else ('0',value));parts=[int(v) for v in clock.split(':')]
        if len(parts)!=3:raise PermissionError('Unrecognized Slurm time limit')
        allocated_seconds=int(days)*86400+parts[0]*3600+parts[1]*60+parts[2]
        if allocated_seconds>s['wall_seconds']:raise PermissionError('Slurm wall allocation exceeds budget')
        if s['cpus']!=c['simulation_settings']['user_params']['N_THREADS']: raise ContractError('Changing threads changes frozen numerical/IC convention')
        if int(env.get('SLURM_MEM_PER_NODE','0'))!=s['memory_MiB']: raise PermissionError('Memory allocation differs from budget')
    speculative=stage=='train' and s.get('quarantined_generation_authorized') is True and bool(b.get('parallel_quarantine_approval_reference'))
    if speculative and (project/'data_runs'/b['budget_id']/'native_stage_failure.json').exists():raise PermissionError('Native preflight failed; no more speculative generation')
    if stage!='preflight' and not speculative:
        qualification=read_json(project/'results/native_qualification.json')
        if not qualification.get('qualified_for_batch1') or qualification.get('science_contract_hash')!=digest(c) or qualification.get('native_sha256')!=c['native_sha256']:raise PermissionError('Machine native qualification does not permit production')
        from .quarantine_admission import qualified_pipeline_matches
        if not qualified_pipeline_matches(project,qualification):raise ContractError('Qualified generation implementation changed')
        gate=read_json(project/'results/native_parity.json')
        if not gate.get('passed') or gate.get('science_contract_hash')!=digest(c): raise PermissionError('Real native preflight has not passed')
        if gate.get('dataset_design_sha256')!=file_hash(project/'contracts/dataset_design.json'): raise ContractError('Native gate design mismatch')
        pl=read_json(project/'results/pl_limit_checks.json')
        if not pl.get('native_power_variance_passed') or not pl.get('native_history_passed') or pl.get('science_contract_hash')!=digest(c): raise PermissionError('PL KP-invariance gate incomplete')
    if stage=='sealed_test':
        policy=read_json(project/'contracts/sealed_test_policy.json')
        if not policy.get('generation_authorized') or not policy.get('generation_approval_reference'): raise PermissionError('Sealed generation not separately authorized')
        freeze=read_json(project/policy['model_freeze_record'])
        if freeze.get('status')!='MODEL_AND_ANALYSIS_FROZEN' or freeze.get('science_contract_hash')!=digest(c): raise PermissionError('Scientific model/analysis freeze missing')
        for name,sha in freeze['files'].items():
            if file_hash(project/name)!=sha: raise ContractError('Frozen artifact changed')
        if not policy.get('public_key_fingerprint') or not policy.get('public_key_file'): raise PermissionError('External sealing public key missing')
    return c,s,b

def retry_authorized(spec,attempt,receipt):
    if 'retry_sample_allowlist' in spec and attempt['sample_id'] not in spec['retry_sample_allowlist']:return False
    if receipt['simulation_status'] in set(spec.get('allowed_retry_statuses',RETRYABLE)):return True
    return any(e.get('attempt_id')==attempt['attempt_id'] and e.get('sample_id')==attempt['sample_id'] and e.get('receipt_digest')==digest(receipt) and e.get('approval_reference') for e in spec.get('explicit_retry_exceptions',[]))

@contextlib.contextmanager
def locked(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)

class AttemptLedger:
    """A reserved attempt is never refunded; crash/timeout/retry costs remain visible."""
    def __init__(self,root): self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
    def entries(self):
        p=self.root/'attempts.jsonl'
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
    def charged_core_hours(self, entries=None):
        entries=self.entries() if entries is None else entries
        path=self.root/'allocation_accounting.json'
        rows=read_json(path).get('rows',[]) if path.exists() else []
        settled={r['attempt_id']:r for r in rows if r.get('terminal') and r.get('allocation_core_hours') is not None}
        return sum(settled[a['attempt_id']]['allocation_core_hours'] if a['attempt_id'] in settled else a['reserved_core_hours'] for a in entries)
    def reserve(self,row,stage,spec,*,budget_hash,contract_hash):
        with locked(self.root/'budget.lock'):
            all_rows=self.entries(); stage_rows=[x for x in all_rows if x['stage']==stage]
            previous=[x for x in all_rows if x['sample_id']==row['sample_id']]
            if previous:
                if 'retry_sample_allowlist' in spec and row['sample_id'] not in spec['retry_sample_allowlist']:raise PermissionError('Sample retry not explicitly authorized')
                receipt=self.root/'receipts'/(previous[-1]['attempt_id']+'.json')
                if not receipt.exists(): raise RuntimeError('Previous attempt unsettled; reconcile allocation before retry')
                r=read_json(receipt)
                if r['simulation_status']=='success': return None
                if not retry_authorized(spec,previous[-1],r) or len(previous)>spec['max_retries_per_sample']: raise PermissionError('Retry policy exhausted or nonretryable failure')
            running=[x for x in all_rows if not (self.root/'receipts'/(x['attempt_id']+'.json')).exists()]
            if len(all_rows)>=spec.get('global_max_attempts',spec['max_attempts']):raise PermissionError('Global attempt budget exhausted')
            if len(running)>=spec.get('global_max_concurrent',spec.get('max_concurrent',0)) or sum(x['stage']==stage for x in running)>=spec.get('max_concurrent',0):raise PermissionError('Approved concurrency exhausted')
            if len(stage_rows)>=spec['max_attempts']:raise PermissionError('Attempt budget exhausted')
            reservation=spec['cpus']*spec['wall_seconds']/3600
            if self.charged_core_hours(all_rows)+reservation>spec.get('global_max_reserved_core_hours',float('inf')):raise PermissionError('Shared allocation core-hour cap exhausted')
            if self.charged_core_hours(stage_rows)+reservation>spec['max_reserved_core_hours']+1e-12: raise PermissionError('Allocation core-hour cap exhausted')
            if len(stage_rows)-len({x['sample_id'] for x in stage_rows})+(1 if previous else 0)>spec['max_retry_attempts']: raise PermissionError('Stage retry allowance exhausted')
            a={'attempt_id':f'{stage}_{len(stage_rows):07d}','sample_id':row['sample_id'],'family_id':row['family_id'],'stage':stage,'ordinal_for_sample':len(previous)+1,'reserved_core_hours':reservation,'cpus':spec['cpus'],'wall_seconds_limit':spec['wall_seconds'],'budget_sha256':budget_hash,'science_contract_hash':contract_hash,'reserved_unix':time.time(),'slurm_job_id':os.environ.get('SLURM_JOB_ID'),'slurm_array_task_id':os.environ.get('SLURM_ARRAY_TASK_ID'),'manifest_index':int(os.environ.get('BT_MANIFEST_INDEX',os.environ.get('SLURM_ARRAY_TASK_ID','-1')))}
            with (self.root/'attempts.jsonl').open('a') as f:f.write(json.dumps(a)+'\n');f.flush();os.fsync(f.fileno())
            return a
    def finish(self,attempt,receipt):
        write_json(self.root/'receipts'/(attempt['attempt_id']+'.json'),{**attempt,**receipt},exclusive=True)
