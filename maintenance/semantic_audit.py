"""Sidecar endpoint/component semantics; never mutate exact history labels."""
import numpy as np

def component_metadata(c,row):
    z=np.asarray(row['redshifts'],float);x=np.asarray(row['global_xHI'],float)
    if not np.array_equal(z,np.asarray(c['redshift_grid'])) or x.shape!=z.shape or not np.isfinite(x).all() or np.any((x<0)|(x>1)):raise ValueError('Invalid exact history; never repair')
    lf_ok=not (row.get('original_end_to_end_success') is False or row.get('LF_reference_status')=='FAILED_ORIGINAL_GRID_COVERAGE_NOT_RECOVERED')
    tau_ok=np.isfinite(float(row['exact_tau']));obs=str(c['likelihood']['neutral_fraction']['redshift']);xhi_ok=np.isfinite(float(row['exact_xHI_at_observation_redshifts'][obs]))
    return {'xHI_zmin':float(x[0]),'xHI_zmax':float(x[-1]),'min_xHI':float(x.min()),'max_xHI':float(x.max()),'zmin_neutral_warning':bool(x[0]>.01),'zmax_ionized_warning':bool(1-x[-1]>.01),'endpoint_classification':'SCIENCE_DOMAIN_WARNING' if x[0]>.01 or 1-x[-1]>.01 else 'NONE','endpoint_changes_label_validity':False,'history_valid':True,'tau_postprocessing_valid':bool(tau_ok),'tau_valid':bool(tau_ok),'xhi_likelihood_valid':bool(xhi_ok),'lf_valid':lf_ok,'joint_likelihood_valid':bool(tau_ok and xhi_ok and lf_ok)}

def summary(c,rows):
    output={'source':'development labels only','quantile_unit':'whole physical-parameter trajectory','sealed_access':False,'ground_truth_modified':False,'by_split':{}}
    for split in ['train','validation']:
        selected=[r for r in rows if r['split']==split];met=[component_metadata(c,r) for r in selected]
        if not met:output['by_split'][split]={'count':0};continue
        low=np.array([m['xHI_zmin'] for m in met]);high=np.array([m['xHI_zmax'] for m in met]);qs=[.5,.68,.9,.95];names=['q50','q68','q90','q95']
        output['by_split'][split]={'count':len(met),'history_valid_count':sum(m['history_valid'] for m in met),'LF_invalid_but_history_valid_count':sum(not m['lf_valid'] for m in met),'tau_valid_count':sum(m['tau_valid'] for m in met),'joint_likelihood_valid_count':sum(m['joint_likelihood_valid'] for m in met),'xHI_zmin':{'redshift':float(c['redshift_grid'][0]),**dict(zip(names,map(float,np.quantile(low,qs)))),'max':float(low.max())},'xHI_zmax':{'redshift':float(c['redshift_grid'][-1]),**dict(zip(names,map(float,np.quantile(high,qs)))),'min':float(high.min())},'zmin_neutral_counts':{str(t):int((low>t).sum()) for t in [.01,.05,.1,.2]},'zmax_ionized_warning_count':int((high<.99).sum())}
    return output

def endpoint_metrics(c,rows,predictions,report):
    exact=np.asarray([r['global_xHI'] for r in rows],float);pred=np.asarray(predictions,float);err=pred-exact;z=np.asarray(c['redshift_grid'],float)
    report['scientific_questions']={'A':'emulator vs selected exact history fidelity','B':'same original history postprocessing and likelihood fidelity','C':'underlying physical-model validity is a separate study, never modifies labels'}
    report['endpoint_accuracy']={}
    for redshift in [5.,5.9,35.]:
        ix=int(np.flatnonzero(z==redshift)[0]);e=err[:,ix]
        report['endpoint_accuracy'][str(redshift)]={'MAE':float(np.abs(e).mean()),'RMSE':float(np.sqrt((e**2).mean())),'max_absolute_error':float(np.abs(e).max()),'absolute_error_q50_q90_q95':dict(zip(['q50','q90','q95'],map(float,np.quantile(np.abs(e),[.5,.9,.95]))))}
    report['component_validity_counts']={'history_valid':len(rows),'LF_invalid_but_history_valid':sum(not component_metadata(c,r)['lf_valid'] for r in rows)}
    report['joint_likelihood_scope']='logL_joint_history is tau+xHI only; LF grid failures remain unresolved and cannot certify LF+tau+xHI at those points'
    report['endpoint_constraints']='none beyond selected reference; neither full ionization nor monotonicity imposed'
    return report

def write_endpoint_sidecars(root,manifest,*,true_numerical_failure_count=0):
    """Audit only explicit qualified train/validation files; no label modifications."""
    import json,hashlib
    from pathlib import Path
    from bt_history.data_control import read_json,write_json,assert_development_path
    from bt_history.contracts import file_hash
    root=Path(root);c=read_json(root/'contracts/science_contract.json');m=read_json(manifest)
    if m.get('role')!='development':raise PermissionError('Only development audit allowed')
    rows=[];sidecars=[]
    for it in m['files']:
        if it.get('split') not in ['train','validation']:raise PermissionError('Sealed or unknown split forbidden')
        path=root/it['path'];assert_development_path(path,it['split'])
        if file_hash(path)!=it['sha256']:raise ValueError('Label checksum changed')
        row=read_json(path);meta=component_metadata(c,row);sidecars.append({'sample_id':row['sample_id'],'split':it['split'],'source_label_sha256':it['sha256'],**meta});rows.append({k:row[k] for k in ['split','redshifts','global_xHI','exact_tau','exact_xHI_at_observation_redshifts'] }|{k:row[k] for k in ['original_end_to_end_success','LF_reference_status'] if k in row})
    report=summary(c,rows);report.update(true_numerical_failure_count=true_numerical_failure_count,manifest_sha256=file_hash(manifest),component_metadata_path='results/component_validity_metadata.jsonl')
    dest=root/'results/component_validity_metadata.jsonl';tmp=dest.with_suffix('.tmp');tmp.write_text(''.join(json.dumps(s,allow_nan=False)+'\n' for s in sidecars));tmp.replace(dest)
    write_json(root/'results/endpoint_domain_audit.json',report)
    return report
