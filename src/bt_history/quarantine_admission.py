"""Immutable generation receipts; a separate native-gated admission receipt."""
import shutil
from pathlib import Path
from .contracts import digest,file_hash
from .data_control import read_json,write_json,verify_design,AttemptLedger,locked

def effective_receipt(project,attempt):
    root=Path(project);b=read_json(root/'configs/data_stage_budgets.json');run=root/'data_runs'/b['budget_id']
    raw=run/'receipts'/(attempt['attempt_id']+'.json');r=read_json(raw)
    admission=run/'admissions'/(attempt['attempt_id']+'.json')
    if admission.exists():
        a=read_json(admission)
        if a['generation_receipt_sha256']!=file_hash(raw):raise ValueError('Original generation receipt changed')
        q=read_json(root/'results/native_qualification.json')
        if not q.get('qualified_for_batch1') or file_hash(root/'results/native_qualification.json')!=a['native_qualification_sha256']:raise PermissionError('Admission qualification changed')
        return a
    return r

def qualified_pipeline_matches(root,q):
    """Bind a reviewed orchestration-only migration to the original qualification."""
    root=Path(root);current=read_json(root/'contracts/pipeline_integrity.json')
    if q.get('pipeline_integrity_sha256')==file_hash(root/'contracts/pipeline_integrity.json'):return True
    path=root/'contracts/orchestration_migration.json'
    if not path.exists():return False
    m=read_json(path)
    if m['qualification_sha256']!=file_hash(root/'results/native_qualification.json') or m['from_pipeline_sha256']!=q.get('pipeline_integrity_sha256') or m['to_pipeline_sha256']!=file_hash(root/'contracts/pipeline_integrity.json'):return False
    old_path=root/m['original_pipeline_path']
    if file_hash(old_path)!=m['from_pipeline_sha256']:return False
    old=read_json(old_path)['files'];new=current['files']
    allowed={'scripts/advance_batch1.py','src/bt_history/data_status.py','src/bt_history/quarantine_admission.py','scripts/submit_data_array.py','configs/batch1_execution.json','notifications/completion_email.py','src/bt_history/data_control.py','src/bt_history/data_runner.py','scripts/generate_batch2.sbatch','scripts/advance_dataset.py','maintenance/recover_worker_label.py','maintenance/recover_history_v1.py','src/bt_history/submission_accounting.py','maintenance/semantic_audit.py','maintenance/learning_curve_controller.py','maintenance/v2/advance.py','maintenance/v2/worker.sbatch','maintenance/v2/audit.sbatch','maintenance/v2/learning.py'}
    changed={k for k in set(old)|set(new) if old.get(k)!=new.get(k)}
    if changed!=set(m['changed_files']) or not changed<=allowed:return False
    return all((root/k).is_file() and file_hash(root/k)==v for k,v in new.items())

def admit_completed(project):
    root=Path(project);b=read_json(root/'configs/data_stage_budgets.json');run=root/'data_runs'/b['budget_id']
    qpath=root/'results/native_qualification.json';q=read_json(qpath)
    c=read_json(root/'contracts/science_contract.json');selected=read_json(root/'contracts/selected_native_contract.json')
    if not q.get('qualified_for_batch1') or q.get('science_contract_hash')!=digest(c) or q.get('native_sha256')!=selected['native_sha256'] or not qualified_pipeline_matches(root,q):raise PermissionError('Native scientific qualification required before admission')
    from .label_quality import validate_label
    from .original_postprocessing_adapter import OriginalPostprocessingAdapter
    post=OriginalPostprocessingAdapter(c);design={r['sample_id']:r for r in verify_design(root,root/'manifests/train_initial_448.jsonl')};admitted=[]
    with locked(run/'admission.lock'):
        for attempt in AttemptLedger(run).entries():
            if attempt['stage']!='train':continue
            rp=run/'receipts'/(attempt['attempt_id']+'.json');ap=run/'admissions'/(attempt['attempt_id']+'.json')
            if not rp.exists():continue
            if ap.exists():effective_receipt(root,attempt);continue
            receipt=read_json(rp)
            if not receipt.get('mechanical_qualified'):continue
            src=root/receipt['artifact_path'];path=src/'label.json'
            if 'quarantine_pending_native' not in src.parts or file_hash(path)!=receipt['label_sha256']:raise ValueError('Quarantine artifact identity mismatch')
            row=read_json(path)
            if row['pipeline_integrity_sha256'] not in selected.get('accepted_training_pipeline_sha256',[file_hash(root/'contracts/pipeline_integrity.json')]) or row['runtime_fingerprint'] not in selected['allowed_runtime_fingerprints']:raise ValueError('Unqualified generation implementation/runtime')
            qa=validate_label(c,row,design[row['sample_id']],selected,read_json(root/'contracts/data_quality_protocol.json'),post)
            dest=run/'labels'/row['sample_id']/attempt['attempt_id'];dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():shutil.copytree(src,dest)
            if file_hash(dest/'label.json')!=receipt['label_sha256']:raise ValueError('Admission copy changed raw history')
            write_json(ap,{**receipt,'qualified':True,'admission_status':'ADMITTED_AFTER_NATIVE_QUALIFICATION','artifact_path':str(dest.relative_to(root)),'generation_receipt_sha256':file_hash(rp),'native_qualification_sha256':file_hash(qpath),'original_postprocessing_rechecked':True,'qa':qa},exclusive=True)
            admitted.append(row['sample_id'])
    return admitted
