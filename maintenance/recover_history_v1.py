"""Revalidate saved histories only. No LF definition changes, no simulations."""
import sys,json,os,time,resource
from pathlib import Path
import numpy as np

def recover_record(c,old,z,x,post,source):
    from bt_history.contracts import validate_history
    validate_history(c,z,x)
    d=post.evaluate(old['canonical_parameters'],z,x)
    row=dict(old)
    row.update(redshifts=z.tolist(),global_xHI=x.tolist(),tau_exact_derived=d['tau'],xHI_at_observation_redshifts={'5.9':d['xHI_obs']},exact_tau=d['tau'],exact_xHI_at_observation_redshifts={'5.9':d['xHI_obs']},ic_seed=old['effective_ic_seed'],simulation_status='success',exit_code=0,physical_parameters=old['canonical_parameters'],source_native_config_hashes=c['source_and_native_fingerprints'],history_recovery=source,original_end_to_end_success=False,LF_reference_status='FAILED_ORIGINAL_GRID_COVERAGE_NOT_RECOVERED',individual_loglikelihood_references_if_computed=None,history_loglikelihood_references={'tau':d['logL_tau'],'xHI':d['logL_xHI'],'joint_history':d['logL_joint_history']},provenance={'role':'development','original_failure_retained':True,'recovery_source':source})
    row['original_failure_reason']=row.pop('failure_reason');row.pop('raw_failure_artifact',None)
    return row

def main(project):
    root=Path(project);sys.path.insert(0,str(root/'src'))
    from bt_history.contracts import file_hash,digest
    from bt_history.data_control import read_json,write_json,verify_design
    from bt_history.runtime_qualification import inspect_runtime
    from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
    from bt_history.label_quality import validate_label
    from bt_history.history_dataset import load_development
    base=root/'data_runs/20260928_batch1';out=base/'history_recovery_v1';plan=read_json(out/'plan.json');started=time.time()
    assert os.environ.get('SLURM_JOB_ID') and int(os.environ.get('SLURM_CPUS_PER_TASK','0'))==16
    assert os.uname().nodename.split('.')[0] in ['chpc-cn%03d'%n for n in range(57,65)]
    assert file_hash(__file__)==plan['implementation_sha256']
    runtime=inspect_runtime(root);write_json(out/'runtime.json',runtime)
    if not runtime['qualified_for_full_simulation']:raise RuntimeError('Selected native/runtime mismatch; no recovery performed')
    c=read_json(root/'contracts/science_contract.json');sel=read_json(root/'contracts/selected_native_contract.json');protocol=read_json(root/'contracts/data_quality_protocol.json');qpath=root/'results/native_qualification.json'
    assert file_hash(qpath)==plan['native_qualification_sha256'] and read_json(qpath)['qualified_for_batch1']
    for name,sha in plan['contract_sha256'].items():assert file_hash(root/name)==sha
    designs={r['sample_id']:r for r in verify_design(root,root/'manifests/train_initial_448.jsonl')};post=OriginalPostprocessingAdapter(c)
    manifest=read_json(root/'manifests/qualified_development.json')
    assert file_hash(root/'manifests/qualified_development.json')==plan['original_manifest_sha256']
    records=[];failures=[]
    for item in plan['candidates']:
        try:
            for key in ['original_label','original_receipt','raw_history']:
                assert file_hash(root/item[key])==item[key+'_sha256'],key+' changed'
            old=read_json(root/item['original_label']);receipt=read_json(root/item['original_receipt']);sid=old['sample_id']
            assert receipt['label_sha256']==item['original_label_sha256'] and not receipt['qualified']
            assert old['failure_reason'].startswith("ValueError('Observed LF magnitudes at z=") and 'outside the model grid' in old['failure_reason']
            assert old['pipeline_integrity_sha256'] in sel['accepted_training_pipeline_sha256']
            assert old['runtime_fingerprint'] in sel['allowed_runtime_fingerprints']
            assert old['effective_ic_seed']==old['requested_ic_seed']==c['ic_target']['seed']
            with np.load(root/item['raw_history'],allow_pickle=False) as data:z=data['redshifts'].copy();x=data['global_xHI'].copy()
            source={**item,'recovery_job_id':os.environ['SLURM_JOB_ID'],'runtime_fingerprint':runtime['runtime_fingerprint'],'implementation_sha256':plan['implementation_sha256'],'raw_checksum_limitation':'raw NPZ first hashed at recovery audit; original generation receipt binds failure metadata but did not hash raw NPZ'}
            row=recover_record(c,old,z,x,post,source)
            row['mechanical_qa']=validate_label(c,row,designs[sid],sel,protocol,post);row['quality_flags']=row['mechanical_qa']['quality_flags']
            dest=out/'labels'/sid;dest.mkdir(parents=True,exist_ok=True)
            write_json(dest/'label.json',row,exclusive=True)
            sha=file_hash(dest/'label.json');rp=out/'admissions'/(old['attempt_id']+'.json')
            write_json(rp,{'sample_id':sid,'attempt_id':old['attempt_id'],'qualified':True,'label_sha256':sha,'native_qualification_sha256':file_hash(qpath),'admission_scope':'HISTORY_ONLY_REVALIDATED; original LF failure retained','recovery_source':source},exclusive=True)
            manifest['files'].append({'sample_id':sid,'split':'train','role':'development','path':str((dest/'label.json').relative_to(root)),'sha256':sha,'receipt':str(rp.relative_to(root))})
            records.append(sid)
        except Exception as error:failures.append({'sample_id':item['sample_id'],'error':repr(error)})
    manifest['recovery_scope']='history-only; LF grid failures retained separately; no joint likelihood success claim'
    mp=root/'manifests/qualified_history_recovered_v1.json';write_json(mp,manifest)
    rows,_=load_development(mp,c,post)
    result={'status':'RECOVERY_VALIDATED' if not failures else 'RECOVERY_PARTIAL','candidate_count':len(plan['candidates']),'recovered_history_labels':len(records),'qualified_history_total':len(rows),'original_joint_pipeline_failures_retained':len(plan['candidates']),'recovery_failures':failures,'loader_passed':True,'new_complete_simulations':0,'scientific_training_started':False,'sealed_access':False,'email_sent':False,'job_id':os.environ['SLURM_JOB_ID'],'wall_seconds':time.time()-started,'peak_RSS_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'manifest':str(mp),'history_only_recovery_not_LF_fix':True}
    write_json(out/'result.json',result);write_json(root/'results/history_recovery_v1.json',result);print(json.dumps(result))
if __name__=='__main__':main(sys.argv[1])
