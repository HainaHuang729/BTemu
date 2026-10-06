"""Aggregate public attempt receipts only; never open sealed scientific payloads."""
from collections import Counter
from pathlib import Path
from .contracts import digest,file_hash
from .data_control import read_json,write_json,read_design,AttemptLedger,verify_design

DESIGNS={'preflight':'preflight','train':'train_full_design','validation':'validation_design','challenge_development':'challenge_development','sealed_test':'sealed_test_design'}

def collect(project):
    root=Path(project);c=read_json(root/'contracts/science_contract.json');budget=read_json(root/'configs/data_stage_budgets.json')
    ledger=AttemptLedger(root/'data_runs'/budget['budget_id']);attempts=ledger.entries();receipts={};failures=[]
    for a in attempts:
        path=ledger.root/'receipts'/(a['attempt_id']+'.json')
        if path.exists():
            from .quarantine_admission import effective_receipt
            r=effective_receipt(root,a)
            if r.get('qualified'):
                artifact=root/r['artifact_path'];payload=artifact if a['stage']=='sealed_test' else artifact/'label.json'
                expected=r['ciphertext_sha256'] if a['stage']=='sealed_test' else r['label_sha256']
                if not payload.is_file() or file_hash(payload)!=expected:r={**r,'qualified':False,'simulation_status':'schema_provenance_failure','integrity_issue':'missing_or_corrupt_artifact'}
            receipts[a['attempt_id']]=r
            if not r.get('qualified') and not r.get('mechanical_qualified'):failures.append({k:r.get(k) for k in ['sample_id','attempt_id','stage','simulation_status','exit_code','wall_seconds','allocation_core_hours','failure_reason','error','integrity_issue']})
    accounting_path=ledger.root/'allocation_accounting.json'
    accounting={r['attempt_id']:r for r in read_json(accounting_path)['rows'] if r.get('terminal')} if accounting_path.exists() else {}
    table=[];manifest={'schema_version':2,'role':'development','science_contract_hash':digest(c),'dataset_design_sha256':file_hash(root/'contracts/dataset_design.json'),'files':[]}
    for stage,name in DESIGNS.items():
        design=verify_design(root,root/'manifests'/(name+'.jsonl'));ids={r['sample_id'] for r in design};aa=[a for a in attempts if a['stage']==stage]
        rr=[receipts[a['attempt_id']] for a in aa if a['attempt_id'] in receipts]
        good={r['sample_id'] for r in rr if r.get('qualified')};bad={r['sample_id'] for r in rr if not r.get('qualified')}-good
        unknown={a['sample_id'] for a in aa if a['attempt_id'] not in receipts}-good
        if not good<=ids or not bad<=ids:raise ValueError('Ledger contains out-of-design IDs')
        table.append({'dataset':stage,'planned':len(design),'attempted':len(aa),'attempted_unique':len({a['sample_id'] for a in aa}),'qualified':len(good),'quarantined_or_failed':len(bad),'unsettled':len(unknown),'quarantined_pending_native':sum(r.get('mechanical_qualified',False) and not r.get('qualified',False) for r in rr),'submitted':'未提交' if not aa else 'see_attempt_ledger','labels':'未生成' if not good else 'generated','label_access':'Sealed' if stage=='sealed_test' else 'Training' if stage=='train' else 'Development','failure_rate':len({r['sample_id'] for r in rr if not r.get('qualified') and not r.get('mechanical_qualified')})/len({a['sample_id'] for a in aa}) if aa else None,'actual_allocation_core_hours':sum(accounting[x['attempt_id']]['allocation_core_hours'] for x in aa) if all(x['attempt_id'] in accounting for x in aa) else None,'measured_worker_envelope_core_hours':sum(r.get('allocation_core_hours',0) for r in rr),'unsettled_reserved_core_hours':sum(a['reserved_core_hours'] for a in aa if a['attempt_id'] not in receipts)})
        if stage in ['train','validation']:
            # Select latest qualified attempt without counting retries as new samples.
            byid={r['sample_id']:r for r in rr if r.get('qualified')}
            for sid,r in sorted(byid.items()):
                manifest['files'].append({'sample_id':sid,'split':stage,'role':'development','path':r['artifact_path']+'/label.json','sha256':r['label_sha256'],'receipt':str((ledger.root/('admissions' if r.get('admission_status')=='ADMITTED_AFTER_NATIVE_QUALIFICATION' else 'receipts')/(r['attempt_id']+'.json')).relative_to(root))})
    write_json(root/'results/dataset_status.json',{'status':'BLOCKED' if not attempts else 'IN_PROGRESS','table':table,'legacy_quarantined':45,'legacy_transferred_to_train':0,'sealed_labels_read':False,'new_complete_evaluations':len(attempts),'new_qualified_labels':sum(x['qualified'] for x in table),'scientific_training_ready':False})
    (root/'results/failure_registry.jsonl').write_text(''.join(__import__('json').dumps(x)+'\n' for x in failures))
    write_json(root/'manifests/qualified_development.json',manifest)
    return table
