"""One isolated audit evaluation; existing exact adapter and QA, seed-only variant."""
import os,sys,copy,time,resource,shutil,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,policy,rows
from bt_history.data_control import AttemptLedger,write_json,read_json
from bt_history.contracts import file_hash,digest

def main():
 ix=int(os.environ['SLURM_ARRAY_TASK_ID']);os.environ['BT_MANIFEST_INDEX']=str(ix)
 c,a,b,spec=policy(require_runtime=True);row=rows()[ix]
 if row['reuse_fixed_reference']:raise PermissionError('Fixed realization reused by checksum, not resimulated')
 ledger=AttemptLedger(RUN);attempt=ledger.reserve(row,'ic_audit',spec,budget_hash=file_hash(ROOT/'configs/ic_audit_budget.json'),contract_hash=digest(a))
 if attempt is None:
  old=[x for x in ledger.entries() if x['sample_id']==row['sample_id']][-1];rec=read_json(RUN/'receipts'/(old['attempt_id']+'.json'))
  if file_hash(ROOT/rec['artifact_path'])!=rec['label_sha256']:raise ValueError('Qualified artifact damaged')
  return
 dest=RUN/'labels'/row['sample_id']/attempt['attempt_id'];dest.mkdir(parents=True,exist_ok=False)
 scratch=Path(os.environ.get('SLURM_TMPDIR',os.environ.get('TMPDIR','/tmp')))/('bt_ic_audit_'+attempt['attempt_id']+'_'+os.environ['SLURM_JOB_ID']);scratch.mkdir(exist_ok=False)
 started=time.perf_counter();r=dict(row);r.update(attempt_id=attempt['attempt_id'],base_science_contract_hash=digest(c),audit_contract_sha256=file_hash(ROOT/'contracts/ic_audit_v1.json'),dataset_version='IC_AUDIT_V1',native_sha256=c['native_sha256'],source_fingerprint=c['source_and_native_fingerprints'].get('source_fingerprint'),cpu_allocation=spec['cpus'],slurm_job_id=os.environ['SLURM_JOB_ID'])
 try:
  from bt_history.runtime_qualification import inspect_runtime
  from bt_history.exact_history_adapter import ExactHistoryAdapter
  from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
  from bt_history.label_quality import validate_label
  runtime=inspect_runtime(ROOT);write_json(dest/'runtime.json',runtime)
  if not runtime['qualified_for_full_simulation']:raise ImportError('Unapproved runtime/native')
  per=copy.deepcopy(c);per['ic_target']['seed']=row['requested_ic_seed']
  h=ExactHistoryAdapter(per,scratch).predict_history(row['canonical_parameters'])
  if h.diagnostics['effective_ic_seeds']!=[row['requested_ic_seed']]:raise ValueError('Requested/effective IC seed mismatch')
  post=OriginalPostprocessingAdapter(per);d=post.evaluate(row['canonical_parameters'],h.redshifts,h.global_xHI)
  check=post.evaluate(row['canonical_parameters'],h.redshifts,h.global_xHI)
  if d!=check:raise ValueError('Original postprocessing not reproducible')
  sel=read_json(ROOT/'contracts/selected_native_contract.json');r.update(source_fingerprint=sel['source_fingerprint'],physics_table_fingerprint=sel['physics_table_fingerprint'],postprocessing_hash=sel['postprocessing_hash'],config_hash=digest(per),science_contract_hash=digest(per),runtime_fingerprint=runtime['runtime_fingerprint'],adapter_implementation_sha256=file_hash(ROOT/'src/bt_history/exact_history_adapter.py'),postprocessing_implementation_sha256=file_hash(ROOT/'src/bt_history/original_postprocessing_adapter.py'),redshifts=h.redshifts.tolist(),global_xHI=h.global_xHI.tolist(),effective_ic_seed=row['requested_ic_seed'],tau_exact_derived=d['tau'],xHI_at_observation_redshifts={'5.9':d['xHI_obs']},derived=d,history_valid=True,tau_valid=True,xhi_likelihood_valid=True,lf_valid=row['lf_valid'],LF_reference_scope='Unchanged theta fixed-IC reference; LF is not resimulated for the IC audit',joint_likelihood_valid=False,simulation_status='success',exit_code=0)
  qa=validate_label(per,r,row,sel,read_json(ROOT/'contracts/data_quality_protocol.json'),post);r['quality_flags']=qa['quality_flags'];r['mechanical_qa']=qa
  r.update(xHI_zmin=float(h.global_xHI[0]),xHI_zmax=float(h.global_xHI[-1]),classifier_label=int(d['xHI_obs']<read_json(ROOT/'contracts/classifier_cut.json')['cut']))
 except Exception as e:
  from bt_history.label_quality import classify_failure
  r.update(history_valid=False,tau_valid=False,simulation_status=classify_failure(e),failure_reason=repr(e),exit_code=1)
 finally:
  r.update(wall_time=time.perf_counter()-started,peak_memory_MiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
  write_json(dest/'label.json',r);label=read_json(dest/'label.json')
  if label!=r:raise ValueError('Atomic label reload mismatch')
  ledger.finish(attempt,{'sample_id':row['sample_id'],'split':'challenge_development','qualified':r['history_valid'],'simulation_status':r['simulation_status'],'exit_code':r['exit_code'],'artifact_path':str((dest/'label.json').relative_to(ROOT)),'label_sha256':file_hash(dest/'label.json'),'wall_seconds':r['wall_time'],'allocation_core_hours':spec['cpus']*r['wall_time']/3600})
  shutil.rmtree(scratch)
 print(json.dumps({'sample_id':row['sample_id'],'qualified':r['history_valid'],'status':r['simulation_status']}))
 sys.exit(r['exit_code'])
if __name__=='__main__':main()
