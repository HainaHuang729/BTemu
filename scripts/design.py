"""Broad prior LHS proposal; refinement must use train/development only."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from scipy.stats import qmc
from bt_history.contracts import read_contract
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--count',type=int,default=128);p.add_argument('--output',required=True);a=p.parse_args()
c=read_contract(a.contract)
if a.count<1:raise ValueError('count must be positive')
u=qmc.LatinHypercube(d=len(c['parameter_order']),seed=20260928).random(a.count)
b=np.array([c['prior_support'][k] for k in c['parameter_order']]);x=qmc.scale(u,b[:,0],b[:,1])
rows=[{'sample_id':f'prior_lhs_{i:06d}','design_stratum':'broad_prior','physical_parameters':dict(zip(c['parameter_order'],v.tolist()))} for i,v in enumerate(x)]
with open(a.output,'x') as f:json.dump(rows,f,indent=2)
