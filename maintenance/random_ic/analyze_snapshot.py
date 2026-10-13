"""Read-only random-IC development analysis; no discovery of sealed label files."""
import os,sys,json,sqlite3,hashlib,time,csv
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.stats import spearmanr
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from bt_history.transforms import fit_pca,logit
from bt_history.contracts import validate_history,parameters
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
OUT=ROOT/'results/random_ic_analysis_20261013'
Q=[0,.05,.25,.5,.68,.9,.95,1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,x):(OUT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def quant(x):
 a=np.asarray(x,dtype=float);a=a[np.isfinite(a)]
 return dict(zip(['min','q05','q25','q50','q68','q90','q95','max'],np.quantile(a,Q).tolist())) if len(a) else None
def count(x):return int(np.count_nonzero(x))
def figsave(fig,name):
 fig.tight_layout();fig.savefig(OUT/(name+'.png'),dpi=170);fig.savefig(OUT/(name+'.pdf'));plt.close(fig)
def stats(rows):
 x=np.array([r['global_xHI'] for r in rows]);d=np.array([[r['derived'][k] for k in ['tau','xHI_obs','logL_tau','logL_xHI','logL_joint_history']] for r in rows]);positive=d[:,1]<CUT
 return {'n':len(rows),'positive':count(positive),'negative':count(~positive),'positive_fraction':float(positive.mean()),'derived':{k:quant(d[:,i]) for i,k in enumerate(['tau','xHI5p9','logL_tau','logL_xHI','logL_tau_plus_xHI'])},'xHI_z5':quant(x[:,0]),'xHI_z35':quant(x[:,-1]),'all_zero_histories':count(np.all(x==0,axis=1)),'all_one_histories':count(np.all(x==1,axis=1)),'transition_histories':count(np.any((x>.1)&(x<.9),axis=1)),'xHI5_counts':{str(v):count(x[:,0]>v) for v in [.01,.05,.1,.2]},'xHI35_counts_below':{str(v):count(x[:,-1]<v) for v in [.99,.95,.9]},'classifier_near_cut':{str(v):count(abs(d[:,1]-CUT)<=v) for v in [.01,.02,.05]},'xHI_likelihood_penalized':count(d[:,3]<0),'tau_logL_ge_minus12p5':count(d[:,2]>=-12.5),'both_tau_logL_ge_minus12p5_and_classifier_positive':count((d[:,2]>=-12.5)&positive),'nonmonotone_increasing_z_at_1e_minus6':count(np.any(np.diff(x,axis=1)<-1e-6,axis=1)),'flags':dict(Counter(f for r in rows for f in r['quality_flags']))}
started=time.perf_counter();m=read(OUT/'input_manifest.json');c=read(ROOT/'contracts/science_contract.json');CUT=read(ROOT/'contracts/classifier_cut.json')['cut'];order=c['parameter_order'];bounds=np.array([c['prior_support'][k] for k in order]);z=np.array(c['redshift_grid']);rows=[];seen=set();seeds=set();families=set();records=[]
assert m['role']=='development' and m['sealed_labels_read'] is False
for p,k in [('contracts/random_ic_v2_target.json','target_contract_sha256'),('contracts/science_contract.json','science_contract_sha256'),('contracts/dataset_design_random_ic_v2.json','design_sha256')]:assert sha(ROOT/p)==m[k]
db=sqlite3.connect('file:'+str(ROOT/m['parameter_design_db'])+'?mode=ro',uri=True)
for f in m['files']:
 assert f['split'] in ('train','validation')
 path=(ROOT/f['path']).resolve();assert path.is_relative_to((ROOT/'data_runs/random_ic_v2/labels').resolve()) and 'sealed' not in str(path)
 assert sha(path)==f['sha256'];r=read(path);design=read_design=json.loads(db.execute('select payload from design where idx=? and split=?',(f['index'],f['split'])).fetchone()[0])
 assert r['sample_id']==f['sample_id'] and r['split']==f['split'] and r['history_valid'] and r['tau_valid'] and r['mechanical_qa']['qualified']
 assert r['dataset_version']=='random_ic_v2' and r['native_sha256']==c['native_sha256'] and r['target_contract_sha256']==m['target_contract_sha256']
 assert r['canonical_parameters']==design['canonical_parameters'] and r['requested_ic_seed']==r['effective_ic_seed']==design['requested_ic_seed']
 validate_history(c,r['redshifts'],r['global_xHI']);parameters(c,r['canonical_parameters'])
 assert np.isfinite(list(r['derived'].values())).all();assert r['classifier_label']==int(r['derived']['xHI_obs']<CUT)
 assert r['sample_id'] not in seen and r['family_id'] not in families and r['effective_ic_seed'] not in seeds
 seen.add(r['sample_id']);families.add(r['family_id']);seeds.add(r['effective_ic_seed']);rows.append(r)
 records.append({'sample_id':r['sample_id'],'split':r['split'],'stratum':r['stratum'],'xHI5':r['global_xHI'][0],'xHI35':r['global_xHI'][-1],**r['derived'],'positive':r['classifier_label'],'wall_seconds':r['wall_time']})
db.close();print('Verified snapshot',len(rows),flush=True)
x=np.array([r['global_xHI'] for r in rows]);theta=np.array([[r['canonical_parameters'][k] for k in order] for r in rows]);norm=(theta-bounds[:,0])/(bounds[:,1]-bounds[:,0]);tau=np.array([r['derived']['tau'] for r in rows]);obs=np.array([r['derived']['xHI_obs'] for r in rows]);positive=obs<CUT;strata=np.array([r['stratum'] for r in rows]);splits=np.array([r['split'] for r in rows]);wall=np.array([r['wall_time'] for r in rows]);lf=Counter(str(r.get('lf_valid')) for r in rows)
s={'analysis_id':m['analysis_id'],'snapshot_hkt':m['snapshot_hkt'],'manifest_sha256':sha(OUT/'input_manifest.json'),'verification_status':'ANALYZED','n':len(rows),'splits':dict(Counter(splits)),'strata':dict(Counter(strata)),'overview':stats(rows),'by_stratum':{a:stats([r for r in rows if r['stratum']==a]) for a in sorted(set(strata))},'LF_flags':dict(lf),'history_valid':len(rows),'tau_valid':len(rows),'lf_invalid_but_history_valid':sum(r.get('lf_valid') is False for r in rows),'lf_not_computed':sum(r.get('lf_valid') is None for r in rows),'unique_seed_count':len(seeds),'unique_family_count':len(families),'provenance_distinct_values':{k:sorted({r[k] for r in rows}) for k in ['native_sha256','source_fingerprint','physics_table_fingerprint','postprocessing_hash','target_contract_sha256','adapter_implementation_sha256']},'notes':['All primary statistics describe qualified development samples, not the scientific prior or posterior.','All rows have one random realization; IC variance at fixed theta cannot be estimated from them.','LF is not computed; tau+xHI diagnostics are not a joint LF posterior.','PCA is fitted and evaluated in-sample; no independent validation or deployment selection.']}
s['parameter_coverage']={k:{'min':float(theta[:,j].min()),'max':float(theta[:,j].max()),'declared':bounds[j].tolist(),'counts_10_equal_coordinate_bins':np.histogram(theta[:,j],bins=10,range=tuple(bounds[j]))[0].tolist()} for j,k in enumerate(order)}
nearest=cKDTree(norm).query(norm,k=2,workers=1)[0][:,1];s['nearest_theta_distance_normalized_L2']=quant(nearest)
s['correlations']={}
for scope,mask in [('all',np.ones(len(rows),bool)),('broad',strata=='broad'),('positive',positive)]:
 s['correlations'][scope]={k:{name:float(spearmanr(theta[mask,j],v[mask]).statistic) for name,v in [('xHI5p9',obs),('tau',tau)]} for j,k in enumerate(order)}
failures=[]
for f in m['failure_registry']['latest_failures']:
 assert f['split'] in ('train','validation');p=(ROOT/f['artifact_path']).resolve();assert p.is_relative_to((ROOT/'data_runs/random_ic_v2/labels').resolve());assert sha(p)==f['label_sha256'];r=read(p)
 failures.append({k:r.get(k) for k in ['sample_id','canonical_parameters','failure_reason','simulation_status','requested_ic_seed','wall_time']})
s['failures']=failures;s['failure_denominator']={'qualified':len(rows),'failed':len(failures),'attempts':m['production_progress_snapshot']['attempts'],'rate':len(failures)/m['production_progress_snapshot']['attempts']}
s['resources']={'wall_seconds':quant(wall),'peak_memory_MiB':quant([r['peak_memory_MiB'] for r in rows]),'allocated_core_hours_completed_waves':m['production_progress_snapshot']['allocated_core_hours'],'disk_bytes_production_snapshot':m['production_progress_snapshot']['disk_bytes'],'CPU_allocation_values':sorted({r['cpu_allocation'] for r in rows})}
# Redshift crossing diagnostics: exact/bracketed roots, without smoothing or assuming monotonicity.
crossing={}
for level in [.1,.5,.9]:
 roots=[];none=multi=0
 for history in x:
  locations=list(z[history==level])
  for j in range(len(z)-1):
   if (history[j]-level)*(history[j+1]-level)<0:locations.append(float(z[j]+(level-history[j])/(history[j+1]-history[j])*(z[j+1]-z[j])))
  locations=sorted(set(locations))
  if len(locations)==1:roots.append(locations[0])
  elif not locations:none+=1
  else:multi+=1
 crossing[str(level)]={'unique_crossing_count':len(roots),'not_crossed_within_grid':none,'multiple_crossings':multi,'z_unique_crossing':quant(roots)}
s['crossings']=crossing
reversals=np.maximum(0,-np.diff(x,axis=1)).max(axis=1)
s['nonmonotonicity_diagnostic']={'largest_adjacent_decrease_with_increasing_z':quant(reversals),'counts_above':{str(t):count(reversals>t) for t in [1e-6,1e-4,.001,.01]},'raw_histories_preserved':True}
s['classifier_positive_tau_screen_fraction']=s['overview']['both_tau_logL_ge_minus12p5_and_classifier_positive']/s['overview']['positive']
with (OUT/'development_rows.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
# Visual distributions: every ordinate is a descriptive quantile across unique theta, not a confidence band.
fig,axs=plt.subplots(2,3,figsize=(14,8))
for mask,label,color in [(positive,'classifier-positive','#007f86'),(~positive,'classifier-negative','#d26731')]:
 qq=np.quantile(x[mask],[.1,.5,.9],axis=0);axs[0,0].fill_between(z,qq[0],qq[2],alpha=.17,color=color);axs[0,0].plot(z,qq[1],label=label,color=color)
axs[0,0].set(xlabel='z',ylabel='volume-mean xHI',title='Median and 10–90% across Train theta');axs[0,0].legend(fontsize=8)
for ax,v,title in [(axs[0,1],x[:,0],'xHI(z=5)'),(axs[0,2],x[:,-1],'xHI(z=35)'),(axs[1,0],obs,'xHI(5.9)'),(axs[1,1],tau,'Derived tau')]:
 ax.hist(v,bins=30,color='#007f86');ax.set(title=title,ylabel='Qualified Train histories')
axs[1,0].axvline(CUT,color='#d26731',label='classifier cut 0.31');axs[1,0].legend()
axs[1,2].hexbin(obs,tau,gridsize=35,mincnt=1,cmap='viridis');axs[1,2].set(xlabel='xHI(5.9)',ylabel='tau',title='Exact derived values (LF not included)')
fig.suptitle('Random-IC development snapshot: %d Train histories; no Validation'%len(rows));figsave(fig,'history_distributions')
# KP/MS two-dimensional occupancy and conditional class proportions.
e1=np.linspace(1,30,11);e2=np.linspace(.5,4,11);n=np.histogram2d(theta[:,8],theta[:,9],bins=[e1,e2])[0];pos=np.histogram2d(theta[positive,8],theta[positive,9],bins=[e1,e2])[0]
s['KP_MS_grid']={'KP_edges':e1.tolist(),'MS_edges':e2.tolist(),'counts':n.astype(int).tolist(),'positive_counts':pos.astype(int).tolist(),'empty_cells':count(n==0),'min_count':int(n.min()),'max_count':int(n.max())}
fig,axs=plt.subplots(1,2,figsize=(12,4.5))
for ax,v,title,lims in [(axs[0],n,'Count per KP/MS bin',{}),(axs[1],np.divide(pos,n,out=np.full_like(n,np.nan),where=n>0),'Classifier-positive fraction',{'vmin':0,'vmax':1})]:
 im=ax.pcolormesh(e1,e2,v.T,cmap='viridis',**lims);fig.colorbar(im,ax=ax);ax.set(xlabel='KP [h/Mpc]',ylabel='MS',title=title);ax.axhline(.968,color='white',ls='--',lw=1)
fig.suptitle('Mixed 80/10/10 design; these are not posterior constraints');figsave(fig,'kp_ms_coverage')
fig,axs=plt.subplots(2,5,figsize=(16,6))
for j,ax in enumerate(axs.flat):
 ax.hist(theta[:,j],bins=10,range=tuple(bounds[j]),color='#007f86');ax.set(title=order[j])
fig.suptitle('Parameter coverage in frozen stored coordinates (log10 parameters unchanged)');figsave(fig,'parameter_coverage')
fig,axs=plt.subplots(1,2,figsize=(12,4.5))
for name,color in [('all','#007f86'),('broad','#d26731'),('positive','#785ca4')]:
 for ax,v in zip(axs,['xHI5p9','tau']):ax.plot(range(10),[s['correlations'][name][k][v] for k in order],marker='o',label=name,color=color);ax.set_xticks(range(10));ax.set_xticklabels(order,rotation=65,ha='right');ax.set(ylim=(-1,1),ylabel='Spearman rho',title=v);ax.axhline(0,color='gray',lw=.5)
axs[0].legend();fig.suptitle('Exploratory associations; selected positive subset may induce selection effects');figsave(fig,'parameter_associations')
print('Descriptive metrics ready; native postprocessing and PCA diagnostics next',flush=True)
post=OriginalPostprocessingAdapter(c);post.check_native();rng=np.random.default_rng(2026101301);positive_indices=np.flatnonzero(positive & (splits=='train'));fit=x[positive_indices];probe=rng.choice(len(fit),size=min(256,len(fit)),replace=False);actual_indices=positive_indices[probe];reference=np.array([[rows[i]['derived'][k] for k in ['tau','xHI_obs','logL_tau','logL_xHI','logL_joint_history']] for i in actual_indices]);keys=['tau','xHI_obs','logL_tau','logL_xHI','logL_joint_history']
# Check the exact saved references through the same native path; no simulations are run.
maxdiff=np.zeros(5)
for j,i in enumerate(actual_indices):
 d=post.evaluate(rows[i]['canonical_parameters'],z,x[i]);maxdiff=np.maximum(maxdiff,np.abs(np.array([d[k] for k in keys])-reference[j]))
assert np.array_equal(maxdiff,np.zeros(5)),maxdiff
s['postprocessing_replay']={'n':len(actual_indices),'max_absolute_difference':dict(zip(keys,maxdiff.tolist())),'bitwise_equal':True,'source':'original adapter + selected native'}
pca=[]
for space in ['physical','logit']:
 values=fit if space=='physical' else logit(fit,1e-6);mean,basis=fit_pca(values,32,split='train');coeff=(values-mean)@basis.T
 for k in [4,8,12,16,20,24,28,32]:
  raw=mean+coeff[:,:k]@basis[:k];recon=raw if space=='physical' else 1/(1+np.exp(-raw));err=recon-fit;valid=np.all((recon>=0)&(recon<=1)&np.isfinite(recon),axis=1);delta=[]
  for j,i in enumerate(actual_indices):
   ii=probe[j]
   if not valid[ii]:continue
   d=post.evaluate(rows[i]['canonical_parameters'],z,recon[ii]);delta.append(np.array([d[key] for key in keys])-reference[j])
  delta=np.array(delta);rr={'space':space,'K':k,'fit_n':len(fit),'reconstruction_scope':'same Train-positive used to fit; not independent validation','epsilon':1e-6 if space=='logit' else None,'trajectory_RMSE':quant(np.sqrt(np.mean(err**2,axis=1))),'trajectory_max_absolute':quant(np.max(abs(err),axis=1)),'out_of_range_histories':count(~valid),'raw_range':[float(recon.min()),float(recon.max())],'derived_probe_n':len(probe),'derived_valid_n':len(delta),'derived_errors_absolute':{key:quant(abs(delta[:,j])) for j,key in enumerate(keys)} if len(delta) else None};rr['roundoff_diagnostic_only_counts_beyond_tolerance']={str(t):count(np.any((recon < -t)|(recon > 1+t),axis=1)) for t in [1e-12,1e-6]};rr['max_range_excursion']=float(max(0,-recon.min(),recon.max()-1));pca.append(rr)
  print('PCA',space,k,'RMSE q95',rr['trajectory_RMSE']['q95'],'range violations',rr['out_of_range_histories'],'derived',len(delta),flush=True)
s['PCA']=pca;s['PCA_accepted']=False;s['validation_available']=bool(np.any(splits=='validation'));s['no_exact_simulations_run']=True;s['sealed_labels_read']=False;s['analysis_elapsed_seconds']=time.perf_counter()-started;s['analysis_script_sha256']=sha(Path(__file__))
fig,axs=plt.subplots(1,2,figsize=(11,4))
for space,color in [('physical','#d26731'),('logit','#007f86')]:
 pp=[p for p in pca if p['space']==space];axs[0].semilogy([p['K'] for p in pp],[p['trajectory_RMSE']['q95'] for p in pp],marker='o',label=space,color=color);axs[1].plot([p['K'] for p in pp],[p['out_of_range_histories']/p['fit_n'] for p in pp],marker='o',label=space,color=color)
axs[0].set(xlabel='PCA K',ylabel='Trajectory RMSE q95',title='In-sample reconstruction');axs[1].set(xlabel='PCA K',ylabel='Fraction outside [0,1]',title='Unclipped raw reconstruction');axs[0].legend();axs[1].legend();fig.suptitle('Train-positive only; no independent K acceptance');figsave(fig,'pca_representation')
dump('analysis.json',s);dump('status.json',{'status':'ANALYSIS_COMPLETED','job_id':os.environ.get('SLURM_JOB_ID'),'n':len(rows),'elapsed_seconds':time.perf_counter()-started,'sealed_access':False,'new_exact_simulations':0});print('ANALYSIS_COMPLETED',len(rows),flush=True)
