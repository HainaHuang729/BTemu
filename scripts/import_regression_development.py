"""Extract only explicit TS regression job reports; retain unvalidated status."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import file_hash,digest,parameters,validate_history
root=Path(__file__).resolve().parents[1];base=Path('/oss06/data/project/tkcastrosim/HNHuang/project_mcmc/workflows/MCMC/fixed_btps_posterior')
contracts={k:json.loads((root/'contracts'/k/'science_contract.json').read_text()) for k in ['fixed','continuous_ms']}
rows={k:[] for k in contracts}; excluded=[]
for i in range(57):
    directory=base/'runs/joint_ts_regression_20260928'/f'job_2158988_{i}'
    mp=directory/'manifest.json';rp=directory/'run_report.json'
    if not mp.exists() or not rp.exists():excluded.append({'case':i,'reason':'missing report'});continue
    m=json.loads(mp.read_text());r=json.loads(rp.read_text());case=m['case'];kind='continuous_ms' if case['runner']=='ms' else 'fixed';c=contracts[kind]
    if m['native_sha256']!=c['native_sha256']:
        excluded.append({'case':i,'reason':'different native','native_sha256':m['native_sha256']});continue
    plan=case['plan']
    if plan['initial_condition_seed']!=c['ic_target']['seed'] or plan['models'][0]['KP_h_Mpc']!=c['fixed_parameters']['KP_h_Mpc'] or plan['simulation']!=c['original_plan']['simulation']:
        excluded.append({'case':i,'reason':'config/IC mismatch'});continue
    provenance={'manifest':str(mp),'manifest_sha256':file_hash(mp),'report':str(rp),'report_sha256':file_hash(rp),'role':'development_regression','original_case':case,'native_postprocessing_rechecked':False}
    if r['status']!='point_succeeded':
        rows[kind].append({'sample_id':f'regression_{i}','simulation_status':'failed','physical_parameters':None,'sampled_theta':case['theta'],'failure_reason':r.get('error'),'provenance':provenance});continue
    d=r['details'];p=d['astrophysical_parameters'].copy()
    if kind=='continuous_ms':p['MS']=case['theta'][-1]
    try:
        parameters(c,p);validate_history(c,d['redshifts'],d['xHI'])
        if d['USE_TS_FLUCT'] is not True:raise ValueError('TS disabled')
    except Exception as e:excluded.append({'case':i,'reason':str(e)});continue
    rows[kind].append({'sample_id':f'regression_{i}','physical_parameters':p,'fixed_parameters':c['fixed_parameters'],'ic_seed':c['ic_target']['seed'],'redshifts':d['redshifts'],'global_xHI':d['xHI'],'exact_tau':d['tau'],'exact_xHI_at_observation_redshifts':{'5.9':d['xHI_z5p9']},'simulation_status':'ok','science_contract_hash':digest(c),'source_native_config_hashes':c['source_and_native_fingerprints'],'provenance':provenance,'source_provenance_qualification':'Native and plan checked; full source hashes not present in source manifest; current fingerprints are candidate target, equivalence not proven','validation_status':'QUARANTINED_NOT_TRAINING_ELIGIBLE'})
summary={'excluded':excluded,'sealed_labels_opened':False,'native_regression':'blocked on execution-host GLIBC; no labels accepted for training'}
for kind,rr in rows.items():
    path=root/'results'/f'{kind}_quarantined_development.jsonl';path.write_text(''.join(json.dumps(r,allow_nan=False)+'\n' for r in rr))
    valid=[r for r in rr if r['simulation_status']=='ok'];summary[kind]={'records':len(rr),'successful':len(valid),'unique_physical_groups':len({digest(r['physical_parameters']) for r in valid}),'training_eligible':0,'path':str(path),'sha256':file_hash(path)}
(root/'results/data_inventory.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='excluded'},indent=2))
