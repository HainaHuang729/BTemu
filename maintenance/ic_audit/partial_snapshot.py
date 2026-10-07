"""Read qualified development receipts for provisional scatter; no native calls."""
import json,sys,datetime
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from bt_history.data_control import read_json,write_json,AttemptLedger
from bt_history.contracts import file_hash
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
RUN=ROOT/'data_runs/ic_audit_v1'
c=read_json(ROOT/'contracts/science_contract.json');module=OriginalPostprocessingAdapter(c).module;cut=read_json(ROOT/'contracts/classifier_cut.json')['cut'];schedule=[json.loads(x) for x in (ROOT/'manifests/ic_audit_v1.jsonl').read_text().splitlines()]
latest={r['sample_id']:r for r in AttemptLedger(RUN).entries()};families={};qualified=0;failures=[]
for row in schedule:
 if row['reuse_fixed_reference']:item=row['fixed_reference'];path=ROOT/item['path'];checksum=item['sha256']
 else:
  at=latest.get(row['sample_id'])
  if at is None:continue
  rp=RUN/'receipts'/(at['attempt_id']+'.json')
  if not rp.exists():continue
  rec=read_json(rp)
  if not rec.get('qualified'):failures.append(rec['simulation_status']);continue
  path=ROOT/rec['artifact_path'];checksum=rec['label_sha256'];qualified+=1
 if file_hash(path)!=checksum:raise ValueError('Qualified audit/reference checksum mismatch')
 r=read_json(path)
 if r['native_sha256']!=c['native_sha256'] or r['effective_ic_seed']!=row['requested_ic_seed']:raise ValueError('Seed/native identity mismatch')
 t=c['likelihood']['planck_tau'];n=c['likelihood']['neutral_fraction'];tau=r['tau_exact_derived'];xhi=r['xHI_at_observation_redshifts']['5.9'];lt=module.loglike_split_normal_tau(tau,mean=t['mean'],sigma_upper=t['sigma_upper'],sigma_lower=t['sigma_lower']);lx=module.loglike_neutral_fraction(r['redshifts'],r['global_xHI'],target_redshift=n['redshift'],threshold=n['threshold'],sigma=n['sigma_above_threshold'])
 families.setdefault(row['family_id'],[]).append((row['realization_index'],r['global_xHI'],[tau,xhi,lt,lx,lt+lx]))
complete=[]
for fid,items in families.items():
 if len(items)!=8:continue
 items.sort();x=np.array([s[1] for s in items]);d=np.array([s[2] for s in items]);positive=d[:,1]<cut
 complete.append({'family_id':fid,'IC_count':8,'history_IC_scatter_RMS':float(np.sqrt(np.mean(x.std(0,ddof=1)**2))),'max_history_std':float(x.std(0,ddof=1).max()),'max_fixed_minus_mean_history':float(abs(x[0]-x.mean(0)).max()),'mean_tau':float(d[:,0].mean()),'std_tau':float(d[:,0].std(ddof=1)),'mean_xHI_5p9':float(d[:,1].mean()),'std_xHI_5p9':float(d[:,1].std(ddof=1)),'std_logL_tau':float(d[:,2].std(ddof=1)),'std_logL_xHI':float(d[:,3].std(ddof=1)),'std_logL_joint_history':float(d[:,4].std(ddof=1)),'positive_IC_count':int(positive.sum()),'classification_stable':bool(positive.all() or (~positive).all())})
result={'updated_at_hkt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'status':'PROVISIONAL_DEVELOPMENT_SCATTER','qualified_fresh':qualified,'complete_families':len(complete),'planned_families':128,'family_statistics':complete,'failed_statuses':failures,'single_IC_decision':'NOT_EVALUATED_UNTIL_FULL_AUDIT','not_full_domain_or_posterior_validation':True,'tau_values_from_original_native_postprocessing':'saved exact-derived references; no substitute integration','sealed_access':False}
write_json(ROOT/'results/ic_audit_partial_scatter.json',result);print(json.dumps(result))
