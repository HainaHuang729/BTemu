"""One fresh process per complete evaluation; parent owns budget and encrypted IO."""
import copy
import hashlib
import importlib
import os
from pathlib import Path
import resource
import subprocess
import sys
import json
import time
import numpy as np
from .contracts import digest,file_hash
from .data_control import read_json,write_json,check_execution_gate,verify_design
from .runtime_qualification import inspect_runtime
from .exact_history_adapter import ExactHistoryAdapter
from .original_postprocessing_adapter import OriginalPostprocessingAdapter
from .label_quality import validate_label,classify_failure

def evaluate(project,manifest,index,budget,stage,attempt_id,ledger_root,workspace):
    root=Path(project);work=Path(workspace);row=verify_design(root,manifest)[index]
    c,spec,b=check_execution_gate(root,stage,budget,manifest)
    attempts=[read_json_line for read_json_line in __import__('bt_history.data_control',fromlist=['AttemptLedger']).AttemptLedger(ledger_root).entries() if read_json_line['attempt_id']==attempt_id]
    if len(attempts)!=1 or attempts[0]['sample_id']!=row['sample_id'] or attempts[0]['slurm_job_id']!=os.environ.get('SLURM_JOB_ID'):raise PermissionError('Worker has no matching reserved attempt')
    with (Path(ledger_root)/('claimed_'+attempt_id)).open('x') as f:f.write(str(os.getpid()))
    selected=read_json(root/'contracts/selected_native_contract.json');protocol=read_json(root/'contracts/data_quality_protocol.json')
    record={**row,'attempt_id':attempt_id,'native_sha256':selected['native_sha256'],'source_fingerprint':selected['source_fingerprint'],'physics_table_fingerprint':selected['physics_table_fingerprint'],'config_hash':digest(c),'postprocessing_hash':selected['postprocessing_hash'],'cache_status':'bypass_regenerate_true_write_false','cpu_allocation':spec['cpus'],'pipeline_integrity_sha256':file_hash(root/'contracts/pipeline_integrity.json')}
    started=time.perf_counter();cpu_started=time.process_time();raw={};effective=[]
    try:
        runtime=inspect_runtime(root);write_json(work/'runtime.json',runtime)
        record['runtime_fingerprint']=runtime['runtime_fingerprint']
        if not runtime['qualified_for_full_simulation']:raise ImportError('Native/runtime qualification failed')
        import py21cmfast as p21
        sys.path.insert(0,c['original_project_root'])
        original=importlib.import_module('workflows.MCMC.fixed_btps_posterior.validation.web_fixed_bt_pilot')
        p=row['canonical_parameters']
        if stage=='preflight' and row['stratum'].startswith('PL'):
            probe=subprocess.run([sys.executable,str(root/'scripts/native_power_probe.py'),str(root),str(budget),str(manifest),str(index),attempt_id,str(ledger_root)],input=json.dumps(p),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
            (work/'power_probe_stderr.log').write_text(probe.stderr)
            record['native_power_probe_exit_code']=probe.returncode
            (work/'power_probe_stdout.log').write_text(probe.stdout)
            if probe.returncode!=0:raise RuntimeError('Native power probe process failed: exit_code='+str(probe.returncode)+'; inspect logs; no physical verdict inferred')
            record['native_power_probe']=json.loads(probe.stdout)
        plan=copy.deepcopy(c['original_plan']);plan['models']=[{'KP_h_Mpc':p['KP_h_Mpc'],'MS':p['MS']}]
        # Same original evaluator at a configured BT model, preserving all actual scientific calls.
        ev=original.Evaluator(plan,0,work,spec['cpus']);astro={k:p[k] for k in c['astro_parameter_order']}
        tau_calls=[];effective=[]
        def coeval(**kw):
            if kw['random_seed']!=c['ic_target']['seed']:raise ValueError('Seed changed')
            result=p21.run_coeval(**kw)
            effective.extend(int(v.random_seed) for v in result)
            pairs=sorted((float(v.redshift),float(np.mean(v.xH_box,dtype=np.float64))) for v in result)
            raw['redshifts'],raw['global_xHI']=np.array(pairs).T
            return result
        def tau_capture(**kw):
            tau_calls.append({'redshifts':np.asarray(kw['redshifts']).tolist(),'global_xHI':np.asarray(kw['global_xHI']).tolist()})
            value=p21.compute_tau(**kw);tau_calls[-1]['tau']=float(value);return value
        if row['engine']=='original':
            model_lfs=[];lf_predict=ev.lf.predict
            def capture_lf(*args,**kwargs):
                v=lf_predict(*args,**kwargs);model_lfs.append(v);return v
            ev.lf.predict=capture_lf
            _,_,details=ev.evaluate(original.theta_from_astro(astro,ev.config),run_coeval_fn=coeval,compute_tau_fn=tau_capture)
            z=np.array(details['redshifts']);x=np.array(details['xHI']);tau=details['tau'];obs=details['xHI_z5p9'];ll=details['log_likelihood'];lfs=model_lfs[0]
        else:
            lfs=ev.lf.predict(astro)  # Preserve original LF -> history -> tau call order.
            adapter=ExactHistoryAdapter(c,work/'cache',run_coeval_fn=coeval)
            h=adapter.predict_history(p);z,x=h.redshifts,h.global_xHI
            d=adapter.post.evaluate(p,z,x,compute_tau_fn=tau_capture);tau,obs=d['tau'],d['xHI_obs']
            ll=ev.likelihood.evaluate(model_lfs=lfs,redshifts=z,xhi=x,tau=tau).as_dict()
        if not effective or set(effective)!={c['ic_target']['seed']}:raise ValueError('Effective returned seed differs/missing')
        lf_arrays={str(k)+'_'+str(j):np.asarray(a) for k,v in lfs.items() for j,a in enumerate(v)}
        np.savez(work/'lf_reference.npz',**lf_arrays)
        record['LF_array_fingerprints']={k:{'dtype':str(a.dtype),'shape':list(a.shape),'sha256':hashlib.sha256(a.tobytes()).hexdigest()} for k,a in lf_arrays.items()}
        def lf_list(a):
            return [float(v) if np.isfinite(v) else str(v) for v in np.asarray(a)]
        record.update(redshifts=z.tolist(),global_xHI=x.tolist(),tau_exact_derived=tau,xHI_at_observation_redshifts={'5.9':obs},LF_reference_if_computed={str(k):[lf_list(v[0]),lf_list(v[1])] for k,v in lfs.items()},individual_loglikelihood_references_if_computed=ll,tau_pipeline_calls=tau_calls,effective_ic_seed=effective[0],simulation_status='success',exit_code=0)
        qa=validate_label(c,record,row,selected,protocol,OriginalPostprocessingAdapter(c));record['quality_flags']=qa['quality_flags'];record['mechanical_qa']=qa
        # Compatibility fields allow reuse of the existing history dataset/trainer.
        record.update(physical_parameters=p,ic_seed=record['effective_ic_seed'],exact_tau=tau,exact_xHI_at_observation_redshifts={'5.9':obs},source_native_config_hashes=c['source_and_native_fingerprints'],provenance={'role':'development' if stage!='sealed_test' else 'sealed_test','design':str(manifest),'design_sha256':file_hash(manifest)})
    except Exception as error:
        if effective and len(set(effective))==1:record['effective_ic_seed']=effective[0]
        record.update(simulation_status=classify_failure(error),exit_code=1,failure_reason=repr(error),quality_flags=[])
        if raw:
            x=raw['global_xHI']
            if np.isfinite(x).all() and np.any((x<0)|(x>1)) and np.all((x>=-1e-6)&(x<=1+1e-6)):
                record['quality_flags'].append('tiny_range_excursion_quarantined_raw_unchanged')
            np.savez(work/'raw_failed_history.npz',**raw)
            record['raw_failure_artifact']='raw_failed_history.npz'
    record.update(wall_time=time.perf_counter()-started,process_cpu_seconds=time.process_time()-cpu_started,peak_memory_MiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    write_json(work/'label.json',record)
    receipt={k:record[k] for k in ['sample_id','attempt_id','split','simulation_status','exit_code']}
    receipt['qualified']=record['simulation_status']=='success';receipt['wall_seconds']=record['wall_time'];receipt['allocation_core_hours']=spec['cpus']*record['wall_time']/3600
    write_json(work/'worker_receipt.json',receipt)
    return record['exit_code']
