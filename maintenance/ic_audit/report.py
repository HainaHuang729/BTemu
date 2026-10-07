"""Family-level IC scatter and finite-IC convergence, original postprocessing."""
import sys,json,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,RUN,rows
from bt_history.data_control import read_json,write_json
from bt_history.contracts import file_hash

def summarize():
 from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
 c=read_json(ROOT/'contracts/science_contract.json');post=OriginalPostprocessingAdapter(c);cut=read_json(ROOT/'contracts/classifier_cut.json')['cut']
 latest={x['sample_id']:x for x in __import__('bt_history.data_control',fromlist=['AttemptLedger']).AttemptLedger(RUN).entries()};families={};failed=[]
 for row in rows():
  if row['reuse_fixed_reference']:
   ref=row['fixed_reference'];path=ROOT/ref['path'];sha=ref['sha256']
  else:
   a=latest.get(row['sample_id'])
   if a is None:continue
   receipt=RUN/'receipts'/(a['attempt_id']+'.json')
   if not receipt.exists():continue
   rec=read_json(receipt)
   if not rec.get('qualified'):failed.append({'sample_id':row['sample_id'],'status':rec['simulation_status']});continue
   path=ROOT/rec['artifact_path'];sha=rec['label_sha256']
  if file_hash(path)!=sha:raise ValueError('Audit/reference checksum changed')
  r=read_json(path)
  if r['native_sha256']!=c['native_sha256'] or r['effective_ic_seed']!=row['requested_ic_seed']:raise ValueError('Audit native/seed mismatch')
  x=np.asarray(r['global_xHI'],float);z=np.asarray(r['redshifts'],float);d=post.evaluate(row['canonical_parameters'],z,x)
  families.setdefault(row['family_id'],[]).append((row,x,d))
 stats=[]
 for fid,items in sorted(families.items()):
  items.sort(key=lambda it:it[0]['realization_index'])
  if len(items)!=8:continue
  x=np.array([it[1] for it in items]);mean=x.mean(0);sigma=x.std(0,ddof=1);values=np.array([[it[2][k] for k in ['tau','xHI_obs','logL_tau','logL_xHI','logL_joint_history']] for it in items]);means=values.mean(0);sigmas=values.std(0,ddof=1)
  p=items[0][0]['canonical_parameters'];md=post.evaluate(p,c['redshift_grid'],mean)
  ll=values[:,-1];logmeanlike=float(np.max(ll)+np.log(np.exp(ll-np.max(ll)).mean()))
  positive=values[:,1]<cut;convergence={}
  # Subsample convergence to the finite 8-IC reference, not a known infinite mean.
  import itertools
  for n in [2,4,8]:
   errs=[];dt=[]
   for ix in itertools.combinations(range(8),n):
    xm=x[list(ix)].mean(0);errs.append(float(np.sqrt(np.mean((xm-mean)**2))))
    dt.append(abs(post.evaluate(p,c['redshift_grid'],xm)['tau']-md['tau']))
   convergence[str(n)]={'history_RMSE_to_8_IC_q90':float(np.quantile(errs,.9)),'tau_abs_to_8_IC_q90':float(np.quantile(dt,.9)),'not_independent_infinite_mean_reference':True}
  stats.append({'family_id':fid,'selection_tag':items[0][0]['stratum'],'source_split':items[0][0]['source_split'],'canonical_parameters':p,'IC_count':8,'trajectory_IC_scatter_RMS':float(np.sqrt(np.mean(sigma**2))),'mean_global_xHI':mean.tolist(),'std_global_xHI':sigma.tolist(),'relative_scatter_where_mean_gt_0p01':[float(s/m) if m>.01 else None for s,m in zip(sigma,mean)],'mean_history_standard_error':(sigma/np.sqrt(8)).tolist(),'fixed_minus_mean_max_abs':float(np.max(abs(x[0]-mean))),'fixed_minus_mean_trajectory_RMSE':float(np.sqrt(np.mean((x[0]-mean)**2))),'mean_tau':float(means[0]),'std_tau':float(sigmas[0]),'fixed_minus_mean_tau':float(values[0,0]-means[0]),'mean_xHI_5p9':float(means[1]),'std_xHI_5p9':float(sigmas[1]),'std_logL_tau':float(sigmas[2]),'std_logL_xHI':float(sigmas[3]),'std_logL_joint_history':float(sigmas[4]),'positive_IC_count':int(positive.sum()),'classification_stable':bool(positive.all() or (~positive).all()),'far_from_cut':bool(abs(means[1]-cut)>.01),'logL_of_mean_history':md['logL_joint_history'],'log_mean_likelihood_over_IC':logmeanlike,'delta_logL_mean_history_vs_IC_marginal':float(md['logL_joint_history']-logmeanlike),'tau_of_mean_history_minus_mean_tau':float(md['tau']-means[0]),'mean_history_convergence':convergence})
 write_json(RUN/'family_statistics.json',{'families':stats,'statistical_unit':'theta family','exact_IC_mean_is_estimated_not_known':True})
 summary={'status':'COMPLETE' if len(stats)==128 else 'PARTIAL','complete_families':len(stats),'planned_families':128,'qualified_fresh_IC_realizations':sum(len(v)-1 for v in families.values()),'reused_fixed_IC_realizations':128,'failed':failed,'classifier_cut':cut,'single_IC_production_decision':'AUDIT_INCOMPLETE' if len(stats)!=128 else 'SCIENTIFIC_THRESHOLD_CONFIRMATION_PENDING','sealed_access':False}
 if stats:
  keys=['trajectory_IC_scatter_RMS','fixed_minus_mean_max_abs','fixed_minus_mean_trajectory_RMSE','std_tau','std_xHI_5p9','std_logL_tau','std_logL_xHI','std_logL_joint_history','delta_logL_mean_history_vs_IC_marginal']
  summary['family_quantiles']={k:{'q50':float(np.quantile([s[k] for s in stats],.5)),'q90':float(np.quantile([s[k] for s in stats],.9)),'q95':float(np.quantile([s[k] for s in stats],.95)),'max_abs':float(np.max(np.abs([s[k] for s in stats])))} for k in keys}
  summary['absolute_IC_scatter_by_redshift_mean']=np.mean([s['std_global_xHI'] for s in stats],0).tolist()
  summary['classifier_unstable_families']=sum(not s['classification_stable'] for s in stats)
  summary['classifier_unstable_far_from_cut']=sum(not s['classification_stable'] and s['far_from_cut'] for s in stats)
  summary['all_realizations_positive_fraction']=sum(s['positive_IC_count'] for s in stats)/(8*len(stats))
  proposal=read_json(ROOT/'contracts/ic_audit_acceptance.json');q=summary['family_quantiles']
  passed=all(q[k]['q90']<=lim for k,lim in proposal['q90_std_threshold_proposals'].items()) and summary['classifier_unstable_far_from_cut']==0
  passed=passed and float(np.quantile([abs(s['delta_logL_mean_history_vs_IC_marginal']) for s in stats],.9))<=proposal['q90_abs_Jensen_logL_difference_proposal']
  summary['proposal_screen_pass']=passed
  if len(stats)==128 and proposal['status']=='CONFIRMED':summary['single_IC_production_decision']='RANDOM_IC_SINGLE_REALIZATION_SUPPORTED' if passed else 'MULTI_IC_AVERAGING_REQUIRED'
  elif len(stats)==128:summary['unconfirmed_proposal_diagnostic']='SINGLE_IC_PROPOSAL_SCREEN_PASS' if passed else 'MULTI_IC_PROPOSAL_SCREEN_FAIL'
 write_json(ROOT/'results/ic_sensitivity_report.json',summary)
 (ROOT/'reports/ic_sensitivity_report.md').write_text('# IC sensitivity audit\n\n```json\n'+json.dumps(summary,indent=2)+'\n```\n\nEach statistic uses the theta family as the sampling unit. Multi-IC means are arithmetic means in physical xHI. LogL(mean history) is compared to log(mean likelihood), because these are not generally equal. LF is unchanged at fixed theta; joint_history refers to tau+xHI, not an independently requalified LF pipeline. Convergence is to the finite eight-IC reference and cannot establish the infinite-IC mean. No sealed labels are used.\n')
 return summary
if __name__=='__main__':print(json.dumps(summarize()))
