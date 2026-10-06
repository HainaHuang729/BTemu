"""Finite initial coverage design, no simulations and no change to sampler prior."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from scipy.stats import qmc
from bt_history.contracts import read_contract
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--output',required=True);p.add_argument('--broad',type=int,default=256);p.add_argument('--per-view',type=int,default=64);p.add_argument('--per-edge',type=int,default=16);a=p.parse_args()
c=read_contract(a.contract);order=c['parameter_order'];b=np.array([c['prior_support'][k] for k in order]);rows=[]
def add(n,seed,stratum,fixed):
    if n<1:raise ValueError('Positive design count required')
    x=qmc.scale(qmc.LatinHypercube(d=len(order),seed=seed).random(n),b[:,0],b[:,1])
    for v in x:
        values=dict(zip(order,v.tolist()));values.update(fixed)
        if stratum=='continuous_ms_view':values['MS']=.5+(values['MS']-.5)/3.5*1.5
        rows.append({'sample_id':f'{stratum}_{len(rows):06d}','design_stratum':stratum,'physical_parameters':values})
add(a.broad,20260928,'broad_rectangle',{})
add(a.per_view,20260929,'fixed_view',{'KP_h_Mpc':10.,'MS':2.5})
add(a.per_view,20260930,'continuous_ms_view',{'KP_h_Mpc':1.})
for i,fixed in enumerate([{'KP_h_Mpc':1.},{'KP_h_Mpc':30.},{'MS':.5},{'MS':4.}]):add(a.per_edge,20261001+i,'BT_boundary_'+str(i),fixed)
with open(a.output,'x') as f:json.dump(rows,f,indent=2)
