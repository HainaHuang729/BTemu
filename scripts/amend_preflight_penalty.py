"""Development-only amendment; preserve train/validation/sealed manifests byte-for-byte."""
import json,sys,copy,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import digest,file_hash
from bt_history.data_control import read_json,read_design,write_json
root=Path(__file__).resolve().parents[1];d=read_json(root/'contracts/dataset_design.json');pf=root/'manifests/preflight.jsonl';rows=read_design(pf)
old=next(r for r in rows if r['stratum']=='normal_adapter_repeat')
used=[json.loads(x) for x in (root/'results/fixed_quarantined_development.jsonl').read_text().splitlines()]
candidate=next(r for r in used if r.get('simulation_status')=='ok' and r['exact_xHI_at_observation_redshifts']['5.9']>.06)
v=read_json(root/'contracts/fixed/science_contract.json');p={**candidate['physical_parameters'],**v['fixed_parameters']}
new=copy.deepcopy(old);new.update(sample_id='preflight_known_penalized_adapter',family_id='theta_'+digest(p),stratum='known_penalized_adapter',canonical_parameters=p,physical_parameters=p,origin='development_penalty_amendment_from_quarantined_parameters_only',original_sampler_coordinates_if_applicable={'ETA_STAR':p['F_STAR10']-math.log10(p['t_STAR']),**{k:p[k] for k in ['t_STAR','ALPHA_STAR','M_TURN','F_ESC10','ALPHA_ESC','L_X','NU_X_THRESH']}})
archive=root/'contracts/design_revisions';archive.mkdir(exist_ok=True)
write_json(archive/'dataset_design_initial_v1.json',d,exclusive=True)
(archive/'preflight_initial_v1.jsonl').write_bytes(pf.read_bytes())
rows[-1]=new;pf.write_text(''.join(json.dumps(r,sort_keys=True)+'\n' for r in rows))
d['manifest_sha256']['manifests/preflight.jsonl']=file_hash(pf)
d['development_amendment']={'id':'preflight_penalty_v1a','reason':'Five already-accessible quarantined development records have penalized xHI; replace redundant adapter-repeat with one explicit penalty replay. Original-repeat retained. No old label is transferred.','source_sample_id':candidate['sample_id'],'changed_only':'preflight manifest','evaluation_count':12,'train_validation_test_unchanged':True}
d['counts']['preflight'].pop('normal_adapter_repeat');d['counts']['preflight']['known_penalized_adapter']=1
repeats=d['duplicate_audit']['intentional_preflight_repeats'];d['duplicate_audit']['intentional_preflight_repeats']=[pair for pair in repeats if old['sample_id'] not in pair]
d['duplicate_audit']['old_development_parameter_overlaps'].append(new['sample_id'])
write_json(root/'contracts/dataset_design.json',d)
for file in ['contracts/split_policy.json','configs/data_stage_budgets.json']:
 b=read_json(root/file)
 if file.startswith('configs'):b['dataset_design_sha256']=file_hash(root/'contracts/dataset_design.json')
 else:b['design_sha256']=file_hash(root/'contracts/dataset_design.json')
 write_json(root/file,b)
