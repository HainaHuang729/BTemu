"""Analyze the already-budgeted original/adapter preflight, never generate histories."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from bt_history.contracts import digest,file_hash
from bt_history.data_control import read_json,read_design,write_json,AttemptLedger,assert_development_path,retry_authorized
p=argparse.ArgumentParser();p.add_argument('--project',default=str(Path(__file__).resolve().parents[1]));p.add_argument('--budget-id',required=True);a=p.parse_args();root=Path(a.project)
c=read_json(root/'contracts/science_contract.json');ledger=AttemptLedger(root/'data_runs'/a.budget_id);records={};errors=[]
attempt_history=[v for v in ledger.entries() if v['stage']=='preflight']
latest={v['sample_id']:v for v in attempt_history}
historical_failures=[]
retry_spec=read_json(root/'configs/data_stage_budgets.json')['stages']['preflight']
for attempt in attempt_history:
    if latest[attempt['sample_id']]['attempt_id']!=attempt['attempt_id']:
        old=read_json(ledger.root/'receipts'/(attempt['attempt_id']+'.json'))
        historical_failures.append(old)
        if not retry_authorized(retry_spec,attempt,old):errors.append('unapproved superseded failure '+attempt['attempt_id'])
        continue
    rp=ledger.root/'receipts'/(attempt['attempt_id']+'.json')
    if not rp.exists():errors.append('unsettled '+attempt['sample_id']);continue
    r=read_json(rp)
    if not r.get('qualified'):errors.append('unqualified '+attempt['sample_id']);continue
    path=root/r['artifact_path']/'label.json';assert_development_path(path,'preflight')
    if file_hash(path)!=r['label_sha256']:raise ValueError('Preflight checksum changed')
    record=read_json(path)
    if record['config_hash']!=digest(c) or record['native_sha256']!=c['native_sha256']:raise ValueError('Preflight target mismatch')
    selection=read_json(root/'contracts/selected_native_contract.json')
    allowed=selection.get('accepted_preflight_pipeline_sha256',[file_hash(root/'contracts/pipeline_integrity.json')])
    if record.get('pipeline_integrity_sha256') not in allowed:raise ValueError('Unapproved preflight implementation version')
    records[record['sample_id'].removeprefix('preflight_')]=record
keys=['redshifts','global_xHI','tau_exact_derived','xHI_at_observation_redshifts','tau_pipeline_calls','LF_reference_if_computed','LF_array_fingerprints','individual_loglikelihood_references_if_computed','effective_ic_seed']
pairs=[('normal_original','normal_adapter'),('PL1_original','PL1_adapter'),('continuous_original','continuous_adapter'),('strong_original','strong_adapter'),('normal_original','normal_original_repeat')]
comparisons=[]
for x,y in pairs:
    checks={k:records[x].get(k)==records[y].get(k) for k in keys} if x in records and y in records else {'complete':False}
    comparisons.append({'pair':[x,y],'bitwise_checks':checks,'passed':all(checks.values())})
pl=[]
for other in ['PL10_adapter','PL30_adapter']:
    checks={k:records['PL1_adapter'].get(k)==records[other].get(k) for k in keys} if 'PL1_adapter' in records and other in records else {'complete':False}
    pl.append({'pair':['PL1_adapter',other],'checks':checks,'passed':all(checks.values())})
power=[]
for other in ['PL10_adapter','PL30_adapter']:
    ok='PL1_adapter' in records and other in records and 'native_power_probe' in records['PL1_adapter'] and records['PL1_adapter']['native_power_probe']==records[other].get('native_power_probe')
    power.append({'pair':['PL1_adapter',other],'passed':bool(ok)})
common={'science_contract_hash':digest(c),'dataset_design_sha256':file_hash(root/'contracts/dataset_design.json'),'native_sha256':c['native_sha256'],'attempted_complete_evaluations':len([x for x in ledger.entries() if x['stage']=='preflight']),'qualified_records':len(records),'historical_failed_attempts':historical_failures,'errors':errors,'threshold':'bitwise, no post-hoc relaxation'}
penalty_present=any(v<0 for k,v in records.get('known_penalized_adapter',{}).get('individual_loglikelihood_references_if_computed',{}).items() if 'xhi' in k.lower())
common['known_penalty_replay_penalized']=penalty_present
passed=penalty_present and len(records)==12 and not errors and all(x['passed'] for x in comparisons+pl+power)
write_json(root/'results/native_parity.json',{**common,'status':'PASSED' if passed else 'BLOCKED','passed':passed,'comparisons':comparisons,'note':'If original repeats differ, diagnose baseline variability first; do not widen tolerances.'})
write_json(root/'results/pl_limit_checks.json',{**common,'status':'PASSED' if passed else 'BLOCKED','PL_limit_MS':.968,'native_history_passed':len(records)==12 and all(x['passed'] for x in pl),'native_power_variance_passed':all(x['passed'] for x in power),'history_checks':pl,'power_variance_checks':power})
print('PASSED' if passed else 'BLOCKED')
selected=read_json(root/'contracts/selected_native_contract.json')
runtime_path=root/'results/runtime_qualification.json'
qualification={
 'status':'PREFLIGHT_PASSED' if passed else 'PREFLIGHT_FAILED',
 'selected_native_identity':{'native_sha256':selected['native_sha256'],'native_path':selected['native_path'],'source_fingerprint':selected['source_fingerprint'],'physics_table_fingerprint':selected['physics_table_fingerprint']},
 'runtime_identity':read_json(runtime_path) if runtime_path.exists() else None,
 'native_sha256':c['native_sha256'],'science_contract_hash':digest(c),
 'pipeline_integrity_sha256':file_hash(root/'contracts/pipeline_integrity.json'),
 'adapter_parity_pass':all(v['passed'] for v in comparisons),
 'pl_limit_check_pass':all(v['passed'] for v in pl+power),
 'data_schema_pass':len(records)==12 and not errors,
 'unresolved_issues':errors+([] if len(records)==12 else ['Incomplete frozen preflight; no train authorization released']),
 'qualified_for_batch1':bool(passed),'attempted_complete_evaluations':common['attempted_complete_evaluations'],
 'qualified_preflight_records':len(records),'production_inference_authorized':False,
}
write_json(root/'results/native_qualification.json',qualification)
