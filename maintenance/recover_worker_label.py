"""Keep successful history when the unchanged optional LF reference rejects its grid."""
import sys,shutil,json
from pathlib import Path
import numpy as np
root=Path(sys.argv[1]);work=Path(sys.argv[2]);manifest=Path(sys.argv[3]);index=int(sys.argv[4]);sys.path.insert(0,str(root/'src'));sys.path.insert(0,str(root/'maintenance'))
from bt_history.data_control import read_json,write_json,verify_design
from bt_history.contracts import file_hash
from bt_history.runtime_qualification import inspect_runtime
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.label_quality import validate_label
from recover_history_v1 import recover_record
old=read_json(work/'label.json')
if old.get('simulation_status')!='schema_provenance_failure' or not old.get('failure_reason','').startswith("ValueError('Observed LF magnitudes at z=") or 'outside the model grid' not in old.get('failure_reason',''):sys.exit(3)
raw=work/'raw_failed_history.npz'
if not raw.is_file():sys.exit(3)
c=read_json(root/'contracts/science_contract.json');selected=read_json(root/'contracts/selected_native_contract.json');protocol=read_json(root/'contracts/data_quality_protocol.json');design=verify_design(root,manifest)[index]
runtime=inspect_runtime(root)
if not runtime['qualified_for_full_simulation'] or runtime['runtime_fingerprint']!=old['runtime_fingerprint']:raise RuntimeError('Recovery runtime mismatch')
source={'original_label_sha256':file_hash(work/'label.json'),'original_worker_receipt_sha256':file_hash(work/'worker_receipt.json'),'raw_history_sha256':file_hash(raw),'original_label_artifact':'original_failed_label.json','original_receipt_artifact':'original_failed_worker_receipt.json','raw_history_artifact':'raw_failed_history.npz','recovery_implementation_sha256':file_hash(__file__),'mode':'same_allocation_original_LF_error_preserved'}
with np.load(raw,allow_pickle=False) as arrays:z=arrays['redshifts'].copy();x=arrays['global_xHI'].copy()
post=OriginalPostprocessingAdapter(c);row=recover_record(c,old,z,x,post,source);qa=validate_label(c,row,design,selected,protocol,post);row.update(mechanical_qa=qa,quality_flags=qa['quality_flags'])
shutil.copy2(work/'label.json',work/'original_failed_label.json');shutil.copy2(work/'worker_receipt.json',work/'original_failed_worker_receipt.json')
write_json(work/'label.json',row);receipt=read_json(work/'worker_receipt.json');receipt.update(qualified=True,simulation_status='success',exit_code=0,history_only_revalidated=True,original_LF_failure=old['failure_reason'],raw_history_sha256=source['raw_history_sha256']);write_json(work/'worker_receipt.json',receipt)
print('History passed unchanged QA; original LF grid failure retained')
