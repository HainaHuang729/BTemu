"""Figures from an immutable development allowlist. No simulations or label edits."""
import sys,json,hashlib,os,time,zipfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LogNorm
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/random_ic_analysis_20261013';OUT=BASE/'gallery';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(BASE/'input_manifest.json');s=read(BASE/'analysis.json');c=read(ROOT/'contracts/science_contract.json');cut=read(ROOT/'contracts/classifier_cut.json')['cut']
assert s['manifest_sha256']==sha(BASE/'input_manifest.json')
rows=[]
for item in m['files']:
 assert item['split']=='train'
 p=(ROOT/item['path']).resolve();assert p.is_relative_to((ROOT/'data_runs/random_ic_v2/labels').resolve()) and 'sealed' not in str(p)
 assert sha(p)==item['sha256'];r=read(p)
 assert r['history_valid'] and r['dataset_version']=='random_ic_v2' and r['target_contract_sha256']==m['target_contract_sha256'];rows.append(r)
x=np.array([r['global_xHI'] for r in rows]);z=np.array(c['redshift_grid']);obs=np.array([r['derived']['xHI_obs'] for r in rows]);tau=np.array([r['derived']['tau'] for r in rows]);lt=np.array([r['derived']['logL_tau'] for r in rows]);pos=obs<cut;strata=np.array([r['stratum'] for r in rows]);kp=np.array([r['canonical_parameters']['KP_h_Mpc'] for r in rows]);ms=np.array([r['canonical_parameters']['MS'] for r in rows]);N=len(rows)
assert N==s['n']==9094 and pos.sum()==s['overview']['positive']
TEAL='#0b7f83';ORANGE='#c65a31';GOLD='#b89232';INK='#243641';MUTED='#657581'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':13,'axes.labelsize':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#b5bec4','text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,'figure.facecolor':'#fafaf7','axes.facecolor':'#fafaf7','savefig.facecolor':'#fafaf7','pdf.fonttype':42,'axes.grid':True,'grid.alpha':.17,'grid.linewidth':.6})
manifest={'snapshot':m['snapshot_hkt'],'input_manifest_sha256':sha(BASE/'input_manifest.json'),'script_sha256':sha(Path(__file__)),'N':N,'split':'train','source_analysis_sha256':sha(BASE/'analysis.json'),'exact_evaluations':0,'sealed_access':False,'figures':[],'IC_variance_claim':False,'posterior_claim':False}
pdf=PdfPages(OUT/'BT_random_IC_analysis_9094.pdf')
def frame(title,subtitle,figsize=(13,5.5)):
 f=plt.figure(figsize=figsize);f.suptitle(title,x=.07,y=.975,ha='left',fontsize=20,fontweight='bold');f.text(.07,.905,subtitle,color=MUTED,fontsize=10.5);return f
def save(fig,name,caption):
 fig.text(.07,.025,caption,fontsize=9,color=MUTED);fig.savefig(OUT/(name+'.png'),dpi=190);fig.savefig(OUT/(name+'.pdf'));pdf.savefig(fig);plt.close(fig);manifest['figures'].append({'name':name,'caption':caption,'png_sha256':sha(OUT/(name+'.png'))})
# 1. Cross-parameter history distributions; bands explicitly not IC uncertainty.
f=frame('01  |  Reionization history diversity','Frozen random-IC Train snapshot: 9,094 histories. Original 32-node arrays; no smoothing.')
gs=f.add_gridspec(1,3,left=.07,right=.98,bottom=.17,top=.80,wspace=.24)
masks=[obs<cut-.02,abs(obs-cut)<=.02,obs>cut+.02];names=['xHI(5.9) < 0.29','0.29 ≤ xHI(5.9) ≤ 0.33','xHI(5.9) > 0.33'];colors=[TEAL,GOLD,ORANGE];rng=np.random.default_rng(2026101401);selected={}
for j,(mask,name,color) in enumerate(zip(masks,names,colors)):
 ax=f.add_subplot(gs[j]);ids=np.flatnonzero(mask);draw=rng.choice(ids,min(18,len(ids)),replace=False);selected[name]=[rows[i]['sample_id'] for i in draw]
 for i in draw:ax.plot(z,x[i],lw=.6,alpha=.22,color=color)
 q=np.quantile(x[mask],[.1,.5,.9],axis=0);ax.fill_between(z,q[0],q[2],color=color,alpha=.14,label='10–90% across theta');ax.plot(z,q[1],color=color,lw=2.6,label='Median across theta');ax.axvline(5.9,color=MUTED,ls=':',lw=1);ax.set(xlim=(35,5),ylim=(-.02,1.02),xlabel='Redshift z  (early → late)',title=f'{name}\nN = {len(ids):,}')
 if j==0:ax.set_ylabel('Volume-mean neutral fraction');ax.legend(loc='lower left',fontsize=8,frameon=False)
 ax.set_xticks([35,25,15,5])
save(f,'01_history_atlas','Thin lines: 18 reproducibly sampled exact histories/panel. Bands describe different theta, not IC scatter at fixed theta.')
# 2. Classifier distribution and visible sparse boundary; axis breaks avoided.
f=frame('02  |  Classifier balance and the boundary','Cut = xHI(5.9) < 0.31, from the frozen original likelihood. Negative histories remain in the dataset.')
gs=f.add_gridspec(1,2,left=.07,right=.97,bottom=.25,top=.80,wspace=.20,width_ratios=[1.25,1]);a=f.add_subplot(gs[0]);b=f.add_subplot(gs[1]);edges=np.linspace(0,1,41)
a.hist([obs[pos],obs[~pos]],bins=edges,stacked=True,color=[TEAL,ORANGE],label=[f'Positive: {pos.sum():,} ({pos.mean():.1%})',f'Negative: {(~pos).sum():,} ({(~pos).mean():.1%})']);a.set(yscale='log',xlabel='xHI(5.9)',ylabel='Histories per bin (log scale)',xlim=(0,1));a.axvline(cut,color=INK,ls='--',lw=1.4);a.legend(frameon=False,loc='upper center',fontsize=9)
zoom=(obs>=cut-.1)&(obs<=cut+.1);b.hist(obs[zoom],bins=np.linspace(cut-.1,cut+.1,21),color='#92aab1',edgecolor='white');b.axvspan(cut-.01,cut+.01,color=GOLD,alpha=.23);b.axvline(cut,color=INK,ls='--',lw=1.4);b.set(xlim=(cut-.1,cut+.1),xlabel='xHI(5.9): boundary zoom',ylabel='Histories per 0.01-wide bin',title=f'Only {np.sum(abs(obs-cut)<=.01)} histories within ±0.01')
f.text(.07,.105,f'{np.sum(pos & (lt>=-12.5)):,} / {pos.sum():,} positives also have logL_tau ≥ −12.5. This excludes LF and is not posterior acceptance.',fontsize=11,color=INK)
save(f,'02_classifier_boundary','Counts are from the mixed training design, not the scientific prior. Cut remains unchanged; no classifier hard gate enabled.')
# 3. Broad stratum only: reduce visual artifacts from inference-view enrichment.
broad=strata=='broad';xe=np.linspace(1,30,11);ye=np.linspace(.5,4,11);n=np.histogram2d(kp[broad],ms[broad],bins=[xe,ye])[0];positive=np.histogram2d(kp[broad & pos],ms[broad & pos],bins=[xe,ye])[0];frac=np.divide(positive,n,out=np.full_like(n,np.nan),where=n>0);med=np.full((10,10),np.nan)
for i in range(10):
 for j in range(10):
  mask=broad&(kp>=xe[i])&(kp<(xe[i+1]) if i<9 else kp<=xe[i+1])&(ms>=ye[j])&(ms<(ye[j+1]) if j<9 else ms<=ye[j+1])
  if mask.any():med[i,j]=np.median(tau[mask])
f=frame('03  |  KP / MS structure in the broad sample',f'Broad stratum only: {broad.sum():,} histories; 10 × 10 bins, {int(n.min())}–{int(n.max())} histories/bin. Other astrophysical parameters vary.')
gs=f.add_gridspec(1,2,left=.07,right=.95,bottom=.18,top=.80,wspace=.30)
for j,(values,title,cm,kw) in enumerate([(frac,'Classifier-positive fraction','viridis',{'vmin':0,'vmax':1}),(med,'Median derived tau (log color scale)','magma',{'norm':LogNorm(vmin=np.nanmin(med),vmax=np.nanmax(med))})]):
 ax=f.add_subplot(gs[j]);im=ax.pcolormesh(xe,ye,values.T,cmap=cm,**kw);f.colorbar(im,ax=ax,pad=.025);ax.axhline(.968,color='white',ls='--',lw=1);ax.text(29.5,1.02,'PL: MS=0.968',ha='right',color='white',fontsize=8);ax.set(xlabel='KP [h/Mpc]',ylabel='MS',title=title);ax.grid(False)
save(f,'03_bt_parameter_map','Descriptive associations in the broad design. These maps are neither BT-only causal effects nor KP/MS posterior constraints.')
manifest['broad_bin_count_range']=[int(n.min()),int(n.max())]
# 4. Reuse saved reconstruction metrics, without refitting or alternate tau integration.
pp=[p for p in s['PCA'] if p['space']=='logit'];K=np.array([p['K'] for p in pp]);rmse=np.array([p['trajectory_RMSE']['q95'] for p in pp]);maxerr=np.array([p['trajectory_max_absolute']['q95'] for p in pp]);f=frame('04  |  How much PCA compression is plausible?','Logit PCA fitted to 3,372 Train-positive histories. Exact coefficients; these are in-sample reconstruction errors, not NN errors.')
gs=f.add_gridspec(1,2,left=.08,right=.96,bottom=.25,top=.80,wspace=.25);a=f.add_subplot(gs[0]);b=f.add_subplot(gs[1]);a.semilogy(K,rmse,'o-',color=TEAL,label='Trajectory RMSE q95');a.semilogy(K,maxerr,'s--',color=ORANGE,label='Trajectory max |error| q95');a.set(xlabel='Number of PCA components K',ylabel='Physical xHI reconstruction error');a.legend(frameon=False,fontsize=9,loc='lower left');a.annotate('K=28: RMSE 0.00134',xy=(28,rmse[K==28][0]),xytext=(15,.00012),arrowprops={'arrowstyle':'->','color':INK},fontsize=9)
for key,label,color in [('logL_tau','|Δ logL_tau|',TEAL),('logL_xHI','|Δ logL_xHI|',ORANGE),('logL_joint_history','|Δ logL_(tau+xHI)|','#785ca4')]:
 vals=[p['derived_errors_absolute'][key]['q90'] for p in pp];b.semilogy(K,vals,'o-',color=color,label=label)
b.set(xlabel='Number of PCA components K',ylabel='Absolute likelihood error q90');b.legend(frameon=False,fontsize=9,loc='upper right')
for ax in [a,b]:ax.set_xticks([4,8,12,16,20,24,28,32])
f.text(.08,.105,'K=28 reduces 32 coefficients to 28 (12.5%). Independent Validation is still required before choosing a decoder.',fontsize=10.5)
save(f,'04_pca_tradeoff','History errors: all 3,372 positives. Likelihood errors: the same fixed 256-point subset, using original postprocessing; epsilon=1e−6.')
pdf.close();manifest['selection_record_private']='gallery_selection.json';(BASE/'gallery_selection.json').write_text(json.dumps(selected,indent=2)+'\n');manifest['job_id']=os.environ.get('SLURM_JOB_ID');(OUT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT/'BT_random_IC_figures_9094.zip','w',zipfile.ZIP_DEFLATED) as a:
 for p in sorted(OUT.iterdir()):
  if p.suffix in ('.png','.pdf') or p.name=='figure_manifest.json':a.write(p,p.name)
print('FIGURES_COMPLETED',N,len(manifest['figures']),OUT,flush=True)
