"""Read released chains; define explicit summaries without new sampling."""
from pathlib import Path
import numpy as np,h5py,json,csv,hashlib
B=Path(__file__).resolve().parent;R=B.parents[1]
cases=[('PL','pl_100k.h5',None,None),('BT1','kp1_ms1p5_100k.h5',1,1.5),('BT5','kp5_ms1p5_100k.h5',5,1.5),('BT10','kp10_ms2p5_100k.h5',10,2.5),('BT20','kp20_ms2p5_10000.h5',20,2.5)]
rows=[];sources=[]
for label,name,kp,ms in cases:
 p=R/'paper/paper_materials/chains_20261104'/name
 with h5py.File(p) as f:a=f['chain'][:];lp=f['log_prob'][:];names=[x.decode() for x in f['parameter_names'][:]]
 assert np.isfinite(a).all();mask=np.isfinite(lp);x=a[mask]
 sources.append(dict(label=label,kp=kp,ms=ms,path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),shape=list(a.shape),retained_rows=len(x),excluded_nonfinite_log_prob=int((~mask).sum()),selection='all finite-log-probability rows; no chronological discard or thinning'))
 for i,n in enumerate(names):
  q=np.quantile(x[:,i],[.025,.16,.5,.84,.975]);rows.append(dict(model=label,parameter=n,mean=float(x[:,i].mean()),std_ddof0=float(x[:,i].std()),q025=float(q[0]),q16=float(q[1]),median=float(q[2]),q84=float(q[3]),q975=float(q[4])))
with (B/'FIXED_CHAIN_SUMMARIES.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(B/'SOURCES.json').write_text(json.dumps(sources,indent=2)+'\n')
head=r'''\begin{table*}[t]\centering\small
\caption{Recomputed medians of the six galaxy coordinates at fixed spectrum, using the 100,000-history BTemu model. All rows with finite log probability are retained. These are finite-chain sample medians; counts and summary definitions are given in Appendix~\ref{app:recomputed-fixed}. $k_p$ is in $h\,\mathrm{Mpc}^{-1}$.}\label{tab:fixed-100k}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrrr}\toprule
Model / $k_p$ & $m_s$ & $\eta_\star$ & $t_\star$ & $\alpha_\star$ & $\log_{10}(M_{\rm turn}/M_\odot)$ & $\log_{10} f_{{\rm esc},10}$ & $\alpha_{\rm esc}$\\\midrule
'''
for label,name,kp,ms in cases:
 vals={r['parameter']:r['median'] for r in rows if r['model']==label};cell='PL' if kp is None else str(kp)
 head+=cell+' & '+('--' if ms is None else str(ms))+' & '+' & '.join(f'{vals[k]:.4f}' for k in ['ETA_STAR','t_STAR','ALPHA_STAR','M_TURN','F_ESC10','ALPHA_ESC'])+r'\\'+'\n'
head+=r'\bottomrule\end{tabular*}\end{table*}'+'\n'
(B/'fixed_medians.tex').write_text(head)
print(head)
