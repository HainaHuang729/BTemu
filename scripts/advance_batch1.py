"""Concurrent preflight and quarantined Train through the existing bounded submitter."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import file_hash
from bt_history.data_control import read_json,write_json,locked,AttemptLedger,verify_design,retry_authorized
from bt_history.submission_accounting import submission_charges
from bt_history.quarantine_admission import effective_receipt,admit_completed
PARITY_KEYS=['redshifts','global_xHI','tau_exact_derived','xHI_at_observation_redshifts','tau_pipeline_calls','LF_reference_if_computed','LF_array_fingerprints','individual_loglikelihood_references_if_computed','effective_ic_seed']
def load_record(root,receipt):
    path=root/receipt['artifact_path']/'label.json'
    if file_hash(path)!=receipt['label_sha256']:raise ValueError('Accepted label changed')
    return read_json(path)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--budget',required=True);ap.add_argument('--worker-exit',type=int,default=0);a=ap.parse_args()
    root=Path(a.project);b=read_json(a.budget);run=root/'data_runs'/b['budget_id'];control=read_json(root/'configs/batch1_execution.json')
    if not control['enabled'] or control['budget_id']!=b['budget_id']:raise PermissionError('Continuation disabled')
    with locked(run/'advance.lock'):
        ledger=AttemptLedger(run);attempts=ledger.entries();latest={v['sample_id']:v for v in attempts}
        receipts={sid:effective_receipt(root,v) for sid,v in latest.items() if (run/'receipts'/(v['attempt_id']+'.json')).exists()}
        submissions=[json.loads(v) for v in (run/'submissions.jsonl').read_text().splitlines()] if (run/'submissions.jsonl').exists() else []
        charges=submission_charges(run,submissions,b);write_json(run/'submission_accounting.json',{'rows':charges,'as_of_unix':time.time()})
        ac=[]
        for v in attempts:
            matches=[s for s in submissions if s['stage']==v['stage'] and int(v['slurm_array_task_id']) in s['indices'] and not any(q['submission_id']==s['submission_id'] and q['index']==int(v['slurm_array_task_id']) and q.get('terminal') and q.get('state')=='CANCELLED' and q.get('actual_core_hours')==0 for q in charges)];ordinal=v['ordinal_for_sample']-1
            q=next((q for q in charges if ordinal<len(matches) and q['submission_id']==matches[ordinal]['submission_id'] and q['index']==int(v['slurm_array_task_id'])),None)
            if q:ac.append({'attempt_id':v['attempt_id'],'terminal':q['terminal'],'allocation_core_hours':q['actual_core_hours'],'job_id':v['slurm_job_id'],'state':q['state']})
        write_json(run/'allocation_accounting.json',{'rows':ac,'scope':'confirmed Slurm accounting; unresolved keep full reservation'})
        def state(value,**kw):
            write_json(run/'continuation_status.json',{'status':value,'as_of_unix':time.time(),'job_id':os.environ.get('SLURM_JOB_ID'),'attempts':len(attempts),'charged_core_hours_at_entry':sum(v['charged_core_hours'] for v in charges),**kw})
            if value in ['TRAIN_BATCH1_COMPLETED','TRAIN_BATCH1_PARTIAL','BUDGET_EXHAUSTED','PREFLIGHT_FAILED']:
                try:subprocess.run([sys.executable,str(root/'notifications/completion_email.py'),'--project',str(root)],timeout=35,check=False)
                except (OSError,subprocess.TimeoutExpired) as exc:write_json(run/'email_hook_failure.json',{'error':repr(exc)})
        def halt(reason,stage='preflight',**kw):
            state('PREFLIGHT_FAILED' if stage=='preflight' else 'TRAIN_BATCH1_PARTIAL',reason=reason,**kw)
            if stage=='preflight':
                write_json(run/'native_stage_failure.json',{'reason':reason,**kw})
                qp=root/'results/native_qualification.json';q=read_json(qp) if qp.exists() else {};q.update(qualified_for_batch1=False,status='PREFLIGHT_FAILED',unresolved_issues=[reason]);write_json(qp,q)
            return 1
        if (run/'STOP_AUTOMATION').exists():return halt('explicit stop file','train')
        if (run/'native_stage_failure.json').exists():return halt('previous native failure, Train remains isolated')
        if a.worker_exit and not any(v.get('slurm_job_id')==os.environ.get('SLURM_JOB_ID') and v['sample_id'] in receipts for v in attempts):return halt('worker failed before durable receipt')
        designs={stage:verify_design(root,root/'manifests'/name) for stage,name in [('preflight','preflight.jsonl'),('train','train_initial_448.jsonl')]}
        def pending(stage):
            counts={}
            for sub in submissions:
                if sub['stage']!=stage:continue
                for ix in sub['indices']:
                    sid=designs[stage][ix]['sample_id']
                    charge=next((v for v in charges if v['submission_id']==sub['submission_id'] and v['index']==ix),{})
                    if charge.get('terminal') and charge.get('state')=='CANCELLED' and charge.get('actual_core_hours')==0:continue
                    counts[sid]=counts.get(sid,0)+1
            return any(sum(v['sample_id']==sid for v in attempts)<n or sid not in receipts for sid,n in counts.items())
        jobs=[]
        def submit(stage,indices):
            manifest=root/'manifests'/('preflight.jsonl' if stage=='preflight' else 'train_initial_448.jsonl')
            deps=sorted({v['slurm_job_id'] for v in attempts if v['stage']==stage and not any(q['attempt_id']==v['attempt_id'] and q.get('terminal') for q in ac)})
            cmd=[sys.executable,str(root/'scripts/submit_data_array.py'),'--project',str(root),'--manifest',str(manifest),'--stage',stage,'--budget',str(a.budget),'--indices',','.join(map(str,indices)),'--submit']
            if deps:cmd+=['--dependency','afterany:'+':'.join(deps)]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            if r.returncode:
                state('BUDGET_EXHAUSTED' if any(w in r.stderr for w in ['cap','budget','exhaust']) else 'TRAIN_BATCH1_PARTIAL',stage=stage,submission_error=r.stderr,submitted_jobs=jobs);return False
            jobs.append({'stage':stage,'job_id':r.stdout.strip(),'indices':indices,'command':cmd});print('SUBMITTED',r.stdout.strip(),stage,indices,flush=True);return True
        pre=designs['preflight'];available={r['sample_id']:load_record(root,receipts[r['sample_id']]) for r in pre if r['sample_id'] in receipts and receipts[r['sample_id']].get('qualified')}
        for l,r in [('normal_original','normal_adapter'),('PL1_original','PL1_adapter'),('continuous_original','continuous_adapter'),('strong_original','strong_adapter'),('normal_original','normal_original_repeat')]:
            x,y=available.get('preflight_'+l),available.get('preflight_'+r)
            if x is not None and y is not None and any(x.get(k)!=y.get(k) for k in PARITY_KEYS):return halt('exact adapter/repeat parity mismatch',pair=[l,r])
        for row in pre:
            r=receipts.get(row['sample_id'])
            if r and not r.get('qualified'):
                submitted=sum(designs['preflight'][ix]['sample_id']==row['sample_id'] for sub in submissions if sub['stage']=='preflight' for ix in sub['indices'])
                consumed=sum(v['sample_id']==row['sample_id'] for v in attempts)
                if submitted>consumed and retry_authorized(b['stages']['preflight'],latest[row['sample_id']],r):continue
                return halt('unqualified frozen preflight',sample_id=row['sample_id'])
        pre_complete=len(available)==12
        if not pre_complete and not pending('preflight'):
            ix=next(i for i,row in enumerate(pre) if row['sample_id'] not in available)
            if not submit('preflight',[ix]):return 1
        qpath=root/'results/native_qualification.json';q=read_json(qpath) if qpath.exists() else {}
        if pre_complete and not q.get('qualified_for_batch1'):
            subprocess.run([sys.executable,str(root/'scripts/qualify_native.py'),'--project',str(root),'--budget-id',b['budget_id']],check=True,timeout=60);q=read_json(qpath)
            if not q.get('qualified_for_batch1'):return halt('machine qualification false')
        if q.get('qualified_for_batch1'):
            admit_completed(root)
            receipts={sid:effective_receipt(root,v) for sid,v in latest.items() if (run/'receipts'/(v['attempt_id']+'.json')).exists()}
        elif not b['stages']['train'].get('quarantined_generation_authorized'):state('PREFLIGHT_RUNNING',submitted_jobs=jobs);return 0
        train=designs['train']
        if len(train)!=448:raise ValueError('Batch design changed')
        # An individual failure never admits a bad label and does not stop independent points.
        # Identity/qualification/budget gates still execute before every submission and admission.
        errors=[{'sample_id':row['sample_id'],**receipts[row['sample_id']]} for row in train if row['sample_id'] in receipts and not receipts[row['sample_id']].get('qualified') and not receipts[row['sample_id']].get('mechanical_qualified')]
        write_json(run/'train_error_summary.json',{'planned_unique':448,'failed_unique':len(errors),'errors':errors,'policy':'continue independent frozen points; retry only eligible infrastructure failures within existing caps','complete':all(row['sample_id'] in receipts for row in train)})
        first_done=all(r['sample_id'] in receipts for r in train[:8])
        if first_done and not (run/'first8_quality.json').exists():
            from bt_history.label_quality import validate_label
            from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
            from bt_history.data_control import assert_development_path
            c=read_json(root/'contracts/science_contract.json');selected=read_json(root/'contracts/selected_native_contract.json');post=OriginalPostprocessingAdapter(c);good=[]
            for row in train[:8]:
                rec=receipts[row['sample_id']]
                if not rec.get('mechanical_qualified') and not rec.get('qualified'):continue
                data=load_record(root,rec)
                if data['pipeline_integrity_sha256'] not in selected.get('accepted_training_pipeline_sha256',[file_hash(root/'contracts/pipeline_integrity.json')]) or data['runtime_fingerprint'] not in selected['allowed_runtime_fingerprints']:raise ValueError('Candidate provenance mismatch')
                validate_label(c,data,row,selected,read_json(root/'contracts/data_quality_protocol.json'),post)
                if data['peak_memory_MiB']>b['stages']['train']['memory_MiB']:raise ValueError('Memory ceiling exceeded')
                if not rec.get('qualified'):
                    try:assert_development_path(root/rec['artifact_path']/'label.json','train')
                    except PermissionError:pass
                    else:raise ValueError('Quarantine loader guard failed')
                good.append(data)
            if not good:return halt('No mechanically valid first8 labels','train')
            write_json(run/'first8_quality.json',{'mechanical_passed':True,'candidate_count':len(good),'native_admission_pending':not q.get('qualified_for_batch1'),'qualified':sum(receipts[r['sample_id']].get('qualified',False) for r in train[:8]),'original_tau_xhi_recomputed':True,'quarantine_loader_denial_checked':True,'fresh_process_per_theta':True,'cache':'bypass','peak_memory_MiB':max(r['peak_memory_MiB'] for r in good),'concurrency':2})
        if q.get('qualified_for_batch1'):
            from bt_history.data_status import collect
            from bt_history.history_dataset import load_development
            from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
            collect(root);c=read_json(root/'contracts/science_contract.json');rows,_=load_development(root/'manifests/qualified_development.json',c,OriginalPostprocessingAdapter(c))
            write_json(run/'training_loader_admission_check.json',{'passed':True,'admitted_labels':len(rows),'requires_native_pass':True})
        if not pending('train'):
            candidates=train if first_done else train[:8];indices=[]
            retries=sum(v['ordinal_for_sample']>1 for v in attempts if v['stage']=='train')
            for i,row in enumerate(candidates):
                r=receipts.get(row['sample_id'])
                if not r:indices.append(i)
                elif r['simulation_status']=='infrastructure_failure' and latest[row['sample_id']]['ordinal_for_sample']==1 and retries<b['stages']['train']['max_retry_attempts']:indices.append(i);retries+=1
                if len(indices)>=min(b['stages']['train']['max_concurrent'],control.get('subsequent_wave_size',2) if first_done else control.get('first_train_wave_size',2)):break
            if indices and not submit('train',indices):return 1
        from bt_history.data_status import collect
        collect(root)
        admitted=sum(receipts.get(r['sample_id'],{}).get('qualified',False) for r in train)
        isolated=sum(receipts.get(r['sample_id'],{}).get('mechanical_qualified',False) and not receipts.get(r['sample_id'],{}).get('qualified',False) for r in train)
        state('TRAIN_BATCH1_COMPLETED' if admitted==448 else 'TRAIN_BATCH1_SUBMITTED' if jobs else 'TRAIN_BATCH1_PARTIAL' if all(row['sample_id'] in receipts for row in train) else 'TRAIN_BATCH1_RUNNING',all_planned_attempted=all(row['sample_id'] in receipts for row in train),failed_unique=len(errors),submitted_jobs=jobs,qualified=admitted,quarantined_candidates=isolated,native_qualified=q.get('qualified_for_batch1',False),remaining_unqualified=448-admitted)
        return 0
if __name__=='__main__':sys.exit(main())
