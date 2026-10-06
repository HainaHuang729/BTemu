"""Finite frozen 1024/2048/4096 comparison; reuses the existing five-seed trainer."""
import json,sys,time,subprocess,shutil
from pathlib import Path

def select_nested_snapshot(source,baseline,target_ids):
    byid={x['sample_id']:x for x in source['files'] if x['split']=='train'}
    if not set(target_ids)<=set(byid):return None
    out=dict(baseline);original=[x for x in baseline['files'] if x['split']=='train'];base_ids={x['sample_id'] for x in original}
    if not base_ids<=set(target_ids):raise ValueError('Non-nested baseline')
    out['files']=original+[byid[sid] for sid in target_ids if sid not in base_ids]+[x for x in baseline['files'] if x['split']=='validation']
    return out

def advance_learning_curve(root):
    root=Path(root);sys.path.insert(0,str(root/'src'))
    from bt_history.data_control import read_json,write_json,locked
    from bt_history.contracts import file_hash
    project=root/'artifacts/learning_curve_fixed_validation_v1';contract_path=project/'design.json'
    if not contract_path.exists():return 'not_registered'
    with locked(project/'controller.lock'):
        design=read_json(contract_path);base=root/design['baseline_run'];baseline=read_json(base/'manifest.json');source=read_json(root/'manifests/qualified_batch2_development.json');baseplan=read_json(base/'plan.json')
        if file_hash(base/'manifest.json')!=design['baseline_manifest_sha256']:raise ValueError('Baseline changed')
        assert file_hash(root/'configs/training.json')==design['training_config_sha256']
        reports=[{'N':1024,'run':str(base.relative_to(root)),'status':'COMPLETED'}];running=False
        for n in [2048,4096]:
            run=project/f'N{n}';submission=run/'submission.json'
            if submission.exists():
                s=read_json(submission);status=read_json(run/'status.json') if (run/'status.json').exists() else {}
                reports.append({'N':n,'run':str(run.relative_to(root)),'job_id':s.get('job_id'),'status':status.get('status','SUBMITTED')});running=running or s.get('exit_code')==0 and status.get('status') not in ['DEVELOPMENT_TRAINING_COMPLETED','DEVELOPMENT_TRAINING_FAILED'];continue
            snapshot=select_nested_snapshot(source,baseline,design['train_sample_ids'][str(n)])
            if snapshot is None or running:reports.append({'N':n,'status':'WAITING_FOR_FROZEN_LABELS' if snapshot is None else 'WAITING_FOR_PRIOR_TRAINING'});continue
            for it in snapshot['files']:
                assert file_hash(root/it['path'])==it['sha256']
                receipt=read_json(root/it['receipt']);assert receipt.get('qualified') and receipt['label_sha256']==it['sha256']
            run.mkdir(exist_ok=False);write_json(run/'manifest.json',snapshot);shutil.copy2(base/'training_config.json',run/'training_config.json');plan=dict(baseplan);plan.update(snapshot_counts={'train':n,'validation':design['validation_count']},manifest_sha256=file_hash(run/'manifest.json'),training_config_sha256=file_hash(run/'training_config.json'),learning_curve_design_sha256=file_hash(contract_path))
            write_json(run/'plan.json',plan);write_json(run/'status.json',{'status':'LEARNING_CURVE_SNAPSHOT_FROZEN','N':n})
            script=run/'train.sbatch';script.write_text('#!/bin/bash\nset -euo pipefail\nsource '+str(root/'scripts/environment.sh')+'\nexport OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1\n"$BT_HISTORY_PYTHON" -u '+str(root/'maintenance/run_development.py')+' '+str(root)+' '+str(run)+'\n\"$BT_HISTORY_PYTHON\" '+str(root/'maintenance/learning_curve_controller.py')+' '+str(root)+'\n')
            cmd=['sbatch','--parsable','--no-requeue','--nodes=1','--ntasks=1','--cpus-per-task=1','--mem=8192M','--time=02:00:00','--partition=chpc','--account=tkcastrosim','--qos=tkcastrosim','--reservation=tkcastrosim1','--job-name=bt_lcurve_N'+str(n),'--output='+str(run/'%j.out'),'--error='+str(run/'%j.err'),str(script)]
            r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout=30);write_json(submission,{'command':cmd,'job_id':r.stdout.strip(),'exit_code':r.returncode,'stderr':r.stderr,'time_unix':time.time()});reports.append({'N':n,'job_id':r.stdout.strip(),'status':'SUBMITTED' if not r.returncode else 'SUBMISSION_FAILED'});running=True
        write_json(project/'status.json',{'milestones':reports,'validation_count':design['validation_count'],'configuration_unchanged':True,'max_additional_training_jobs':2,'max_training_concurrent':1,'new_exact_evaluations':0,'sealed_access':False,'email':False})
        return reports
if __name__=='__main__':print(advance_learning_curve(sys.argv[1]))
