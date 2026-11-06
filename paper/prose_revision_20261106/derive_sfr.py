"""Project existing chain rows through the published galaxy prescription."""
from pathlib import Path
import hashlib,json,csv
import numpy as np
import h5py
B=Path(__file__).resolve().parent;ROOT=B.parents[1]
files={'PL':'pl_100k.h5','BT':'kp1_ms1p5_100k.h5'}
rows=[];sources={}
for model,name in files.items():
 p=ROOT/'paper/paper_materials/chains_20261104'/name
 with h5py.File(p) as f:
  chain=f['chain'][:];mask=np.isfinite(f['log_prob'][:]);names=[x.decode() for x in f['parameter_names'][:]]
 a=chain[mask];assert np.isfinite(a).all()
 eta=a[:,names.index('ETA_STAR')];alpha=a[:,names.index('ALPHA_STAR')];t=a[:,names.index('t_STAR')]
 sources[model]=dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),stored_shape=list(chain.shape),rows=len(a),selection='all finite log_prob rows, identical to the representative PL/BT corner; no additional discard')
 for m in [1e9,1e10,1e11]:
  fstar=10**eta*t*(m/1e10)**alpha
  value=np.minimum(1,fstar)/t
  q=np.quantile(value,[.025,.5,.975])
  rows.append(dict(model=model,halo_mass_Msun=m,q025=float(q[0]),median=float(q[1]),q975=float(q[2]),saturated_fraction=float(np.mean(fstar>=1))))
ratios=[]
for m in [1e9,1e10,1e11]:
 vals={r['model']:r['median'] for r in rows if r['halo_mass_Msun']==m}
 ratios.append(dict(halo_mass_Msun=m,ratio_of_marginal_medians_BT_over_PL=vals['BT']/vals['PL']))
result=dict(definition='S=dotM_star/[M_h H(z) (Omega_b/Omega_m)]=min[1,10^eta_star t_star (M_h/1e10 Msun)^alpha_star]/t_star',uncapped_definition='S=10^eta_star (M_h/1e10 Msun)^alpha_star',units='dimensionless; same fixed mass and redshift in both models',sources=sources,summaries=rows,ratios=ratios,interpretation='single-halo active-galaxy prescription; not halo abundance, duty-cycle-weighted emissivity, or actual LF predictions. Ratios compare marginal medians of different samples, not paired simulations. Finite-chain status is inherited from source comparison.')
(B/'SFR_INTERPRETATION.json').write_text(json.dumps(result,indent=2)+'\n')
with (B/'SFR_INTERPRETATION.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print(json.dumps(ratios,indent=2))
