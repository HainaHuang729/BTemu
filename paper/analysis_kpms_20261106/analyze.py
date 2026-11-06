"""Analyze uploaded samples only; no sampler or simulator is invoked."""
from pathlib import Path
import csv, hashlib, json, importlib.util
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
SOURCE=ROOT/'paper/paper_materials/chains_20261106/joint_kpms8_100k_600steps.h5'
P=ROOT/'paper/paper_materials/tables/parameter_prior_table.csv'
spec=importlib.util.spec_from_file_location('park',ROOT/'paper/web/corner_park95_20261104/render.py')
park=importlib.util.module_from_spec(spec);spec.loader.exec_module(park)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
with h5py.File(SOURCE) as f:
    a=f['chain'][:];lp=f['log_prob'][:];names=[x.decode() for x in f['parameter_names'][:]]
assert a.shape==(600,32,8) and lp.shape==(600,32) and np.isfinite(a).all() and np.isfinite(lp).all()
prior_rows={r['parameter']:r for r in csv.DictReader(P.open())}
keys=['KP_h_Mpc','MS'];ix=[names.index(k) for k in keys]
ranges=[(float(prior_rows[k]['prior_low']),float(prior_rows[k]['prior_high'])) for k in keys]
assert all(np.all((a[:,:,i]>=lo)&(a[:,:,i]<=hi)) for i,(lo,hi) in zip(ix,ranges))
# Upstream README numbers reproduce a 300-step chronological discard. This is a
# reproducible preview convention, not a demonstrated equilibration time.
selections=[('all_600',0,600),('discard150',150,600),('last300',300,600),('last150',450,600),('first300',0,300)]
rows=[]
for label,start,stop in selections:
    flat=a[start:stop].reshape(-1,8)
    for k,i,(lo,hi) in zip(keys,ix,ranges):
        qs=np.quantile(flat[:,i],[.025,.16,.5,.84,.975]);pq=np.array([lo+.025*(hi-lo),lo+.975*(hi-lo)])
        rows.append(dict(selection=label,start_step_zero_based=start,stop_step_exclusive=stop,rows=len(flat),parameter=k,q025=float(qs[0]),q16=float(qs[1]),median=float(qs[2]),q84=float(qs[3]),q975=float(qs[4]),prior_low=lo,prior_high=hi,prior_q025=float(pq[0]),prior_q975=float(pq[1]),width95_over_prior_support=float((qs[4]-qs[0])/(hi-lo)),width95_over_prior_equal_tail95=float((qs[4]-qs[0])/(pq[1]-pq[0]))))
with (B/'intervals.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
# Descriptive autocorrelation across time, averaging per-walker ACFs. Walkers
# interact; neither the variance ratio nor pooled ESS below is independent-run evidence.
def diagnostic(x):
    n=len(x);half=n//2;s=np.concatenate([x[:half],x[-half:]],axis=1)
    W=np.var(s,axis=0,ddof=1).mean(0);V=half*np.var(s.mean(0),axis=0,ddof=1)
    ratio=np.sqrt(((half-1)*W+V)/half/W)
    out={}
    for j,k in enumerate(names):
        v=x[:,:,j]-x[:,:,j].mean(axis=0);fft=np.fft.rfft(v,n=2**int(np.ceil(np.log2(2*n))),axis=0)
        ac=np.fft.irfft(fft*np.conjugate(fft),axis=0)[:n];ac=(ac/ac[0]).mean(axis=1)
        taus=2*np.cumsum(ac)-1;inds=np.where(np.arange(n)>=5*taus)[0];window=int(inds[0]) if len(inds) else n-1
        tau=float(taus[window]);reliable=bool(tau>0 and n>=50*tau and len(inds)>0)
        out[k]=dict(ordinary_interacting_walker_split_ratio=float(ratio[j]),acf_window=window,iat_steps_descriptive=tau,length_over_iat=float(n/tau) if tau>0 else None,pooled_ess_heuristic=float(x.shape[0]*x.shape[1]/tau) if tau>0 else None,passes_length_50tau_heuristic=reliable)
    return out
D={label:diagnostic(a[start:stop]) for label,start,stop in [('all600',0,600),('last300',300,600)]}
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,'axes.linewidth':.65,'xtick.direction':'in','ytick.direction':'in','savefig.facecolor':'white'})
BLUE='#285E7A';ORANGE='#B56B42';GREY='#8B9BA8';INK='#344753'
x=a[300:,:,ix].reshape(-1,2)
fig,axs=plt.subplots(2,2,figsize=(8.5,7.6),gridspec_kw={'hspace':.09,'wspace':.10})
axs[0,1].set_visible(False)
for j,(lo,hi) in enumerate(ranges):
    ax=axs[j,j];hist,edges=np.histogram(x[:,j],bins=32,range=(lo,hi),density=True)
    ax.stairs(hist,edges,color=BLUE,lw=1.3,fill=True,alpha=.18);ax.stairs(hist,edges,color=BLUE,lw=1.2)
    ax.hlines(1/(hi-lo),lo,hi,color=ORANGE,lw=1.2,linestyles=(0,(4,2)))
    q=np.quantile(x[:,j],[.025,.5,.975]);ax.axvline(q[0],color=BLUE,lw=.65,ls=':');ax.axvline(q[2],color=BLUE,lw=.65,ls=':')
    ax.set_title(rf'${q[1]:.2f}^{{+{q[2]-q[1]:.2f}}}_{{-{q[1]-q[0]:.2f}}}$',color=BLUE,pad=7)
    ax.set_xlim(lo,hi);ax.set_ylim(bottom=0);ax.set_ylabel('Density');ax.tick_params(labelsize=10)
axs[0,0].tick_params(labelbottom=False)
h,_,_=np.histogram2d(x[:,0],x[:,1],bins=32,range=ranges)
gx,gy,field,lev,region=park.density_grid(h,*ranges)
ax=axs[1,0];ax.contourf(gx,gy,field,levels=[lev,np.nextafter(field.max(),np.inf)],colors=[GREY],alpha=.30)
ax.contour(gx,gy,field,levels=[lev],colors=[BLUE],linewidths=1.1)
ax.set_xlim(*ranges[0]);ax.set_ylim(*ranges[1]);ax.set_xlabel(r'$k_p\ [h\,\mathrm{Mpc}^{-1}]$');ax.set_ylabel(r'$m_s$')
axs[1,1].set_xlabel(r'$m_s$');axs[1,1].set_ylabel('')
fig.subplots_adjust(left=.10,right=.97,bottom=.10,top=.94)
fig.savefig(B/'kp_ms_marginal_prior.png',dpi=220);plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(10,5.8),gridspec_kw={'width_ratios':[2,1]},constrained_layout=True)
for j,k in enumerate(keys):
    for w in range(32):axs[j,0].plot(np.arange(1,601),a[:,w,ix[j]],color=BLUE,alpha=.15,lw=.45)
    axs[j,0].plot(np.arange(1,601),np.median(a[:,:,ix[j]],axis=1),color=INK,lw=.9)
    axs[j,0].axvline(300.5,color=ORANGE,ls='--',lw=.9);axs[j,0].set_ylabel(r'$k_p$' if j==0 else r'$m_s$');axs[j,0].set_ylim(*ranges[j])
    for label,st,en,col,style in [('First 300',0,300,ORANGE,'--'),('Last 300',300,600,BLUE,'-')]:
        h,e=np.histogram(a[st:en,:,ix[j]],bins=24,range=ranges[j],density=True);axs[j,1].stairs(h,e,color=col,linestyle=style,lw=1.1,label=label)
    axs[j,1].set_xlim(*ranges[j]);axs[j,1].set_ylabel('Density')
axs[0,1].legend(frameon=False,fontsize=9);axs[1,0].set_xlabel('Stored step');axs[1,1].set_xlabel(r'$m_s$');axs[1,1].set_ylabel('');axs[0,1].set_xlabel(r'$k_p$')
fig.savefig(B/'kp_ms_stability.png',dpi=180);plt.close(fig)
result=dict(source_revision='801a12f',source_file=str(SOURCE.relative_to(ROOT)),sha256=sha(SOURCE),shape=list(a.shape),parameter_names=names,finite_log_prob_rows=int(lp.size),excluded_rows=0,model='100k (upstream README identity; HDF5 has no attributes)',prior_source=str(P.relative_to(ROOT)),prior_sha256=sha(P),prior_status='Uniform reference from archived prior table. Current HDF5 has no prior/likelihood/run attributes; confirm current run uses this table.',primary_selection='steps 301–600 (zero-based [300:600]), 9600 samples. Matches upstream 100k README rounded intervals; not a diagnosed burn-in.',marginalization='Project unweighted MCMC samples onto KP_h_Mpc and MS; integrate out six astrophysical coordinates.',interval_definition='1D equal-tail 2.5–97.5 percentiles; 2D 95% highest smoothed sample-density region. Separate constructions.',intervals=rows,region=region,diagnostics=D,diagnostic_method='Ordinary split variance ratio across interacting walkers; averaged per-walker FFT ACF with window M>=5*tau. Pooled ESS is heuristic and ignores cross-walker dependence. No independent-run Rhat/ESS available.',combine_models=False,old_16018_step_chain_available=False)
(B/'analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
assert sha(SOURCE)==result['sha256']
print(json.dumps({'last300':[r for r in rows if r['selection']=='last300'],'diagnostics':D['all600']},indent=2))
