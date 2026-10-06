"""Frozen real-data development training; reuse existing five-seed Direct trainer."""
import sys,json,time,os,importlib.util,traceback
from pathlib import Path
root=Path(sys.argv[1]);run=Path(sys.argv[2]);sys.path.insert(0,str(root/'src'));sys.path.insert(0,str(root/'maintenance'))
from bt_history.data_control import read_json,write_json
from bt_history.contracts import read_contract,file_hash
from bt_history.runtime_qualification import inspect_runtime
from bt_history.history_dataset import load_development,split_groups
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from semantic_audit import component_metadata,summary,endpoint_metrics
plan=read_json(run/'plan.json')
try:
    assert os.environ.get('SLURM_JOB_ID') and int(os.environ.get('SLURM_CPUS_PER_TASK','0'))==1
    assert os.uname().nodename.split('.')[0] in ['chpc-cn%03d'%n for n in range(57,65)]
    for name,sha in plan['implementation_sha256'].items():assert file_hash(root/name)==sha
    assert file_hash(run/'manifest.json')==plan['manifest_sha256']
    assert file_hash(root/'contracts/science_contract.json')==plan['science_contract_file_sha256']
    assert file_hash(run/'training_config.json')==plan['training_config_sha256']
    runtime=inspect_runtime(root);write_json(run/'runtime.json',runtime)
    assert runtime['qualified_for_full_simulation'] # identity audit only; no history generation
    c=read_contract(root/'contracts/science_contract.json');post=OriginalPostprocessingAdapter(c)
    rows,failures=load_development(run/'manifest.json',c,post);assert not failures
    split=split_groups(rows);cfg=read_json(run/'training_config.json')
    assert cfg['seeds']==[11,29,47,71,101] and cfg['architecture']['blocks']==4
    assert sum(v=='train' for v in split.values())>=cfg['minimum_train_groups'] and sum(v=='validation' for v in split.values())>=cfg['minimum_validation_groups']
    audit=summary(c,rows);audit['true_numerical_failure_count']=plan['true_numerical_failure_count'];audit['snapshot_manifest_sha256']=plan['manifest_sha256'];write_json(run/'endpoint_audit.json',audit)
    sidecars=[{'sample_id':r['sample_id'],'split':r['split'],'source_label_sha256':it['sha256'],**component_metadata(c,r)} for r,it in zip(rows,read_json(run/'manifest.json')['files'])]
    (run/'component_metadata.jsonl').write_text(''.join(json.dumps(r,allow_nan=False)+'\n' for r in sidecars))
    write_json(run/'status.json',{'status':'TRAINING_RUNNING','job_id':os.environ['SLURM_JOB_ID'],'training_counts':{st:sum(v==st for v in split.values()) for st in ['train','validation']},'new_exact_simulations':0,'sealed_access':False,'email_sent':False})
    print('Snapshot validated:',json.dumps(audit),flush=True)
    from bt_history import training
    from bt_history.metrics import fidelity
    def reporting(c,rs,predictions,post):
        report=fidelity(c,rs,predictions,post,stratify=False)
        # Frozen explicit view/stratum tags; never infer view from guessed fixed values.
        report['target_regions']={}
        import numpy as np
        pred=np.asarray(predictions)
        for name in ['fixed','continuous_ms','broad','anchors_edges']:
            ids=[i for i,r in enumerate(rs) if name in r.get('inference_view_tags',[]) or r.get('stratum')==name]
            report['target_regions'][name]=endpoint_metrics(c,[rs[i] for i in ids],pred[ids],fidelity(c,[rs[i] for i in ids],pred[ids],post,stratify=False)) if ids else {'status':'missing_validation_coverage'}
        return endpoint_metrics(c,rs,pred,report)
    training.fidelity=reporting
    started=time.time();result=training.train(c,rows,split,cfg,run/'direct_resmlp',post)
    write_json(run/'status.json',{'status':'DEVELOPMENT_TRAINING_COMPLETED','job_id':os.environ['SLURM_JOB_ID'],'seconds':time.time()-started,'members':result['members'],'production_accepted':False,'posterior_passed':False,'sealed_access':False,'email_sent':False,'acceptance_thresholds':'proposed; report errors without granting acceptance'})
    print('Completed all five registered seeds',flush=True)
except Exception as error:
    write_json(run/'status.json',{'status':'DEVELOPMENT_TRAINING_FAILED','error':repr(error),'job_id':os.environ.get('SLURM_JOB_ID'),'sealed_access':False,'email_sent':False});traceback.print_exc();raise
