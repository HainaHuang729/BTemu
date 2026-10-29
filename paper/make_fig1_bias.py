import csv, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
SRC=Path("/oss06/data/project/tkcastrosim/HNHuang/project_21cmFast/experiments/bt_mock_pl_bias/results/final_summary/phase37_parameter_bias.csv")
OUT=Path("/storage01/users/s1155206606/.dsh/qq-workspace/paper_fig_bias.png")
rows=list(csv.DictReader(open(SRC)))
mocks=sorted({(r["mock_index"],r["mock_label"]) for r in rows}, key=lambda x:int(x[0]))
params=["F_STAR10","ALPHA_STAR","F_ESC10","ALPHA_ESC","M_TURN","t_STAR","L_X","NU_X_THRESH"]
shift=np.full((len(mocks),len(params)),np.nan); width=np.full_like(shift,np.nan)
for r in rows:
    i=[m[0] for m in mocks].index(r["mock_index"]); j=params.index(r["parameter"])
    shift[i,j]=float(r["shift_from_pl_control_in_combined_sigma"] or 0)
    width[i,j]=float(r["width_ratio_to_pl_control"] or 1)
lab=[m[1] for m in mocks]
fig,(a1,a2)=plt.subplots(1,2,figsize=(13,0.55*len(mocks)+2.2))
im1=a1.imshow(shift,cmap="RdBu_r",vmin=-2.5,vmax=2.5,aspect="auto")
a1.set_title(r"Parameter shift vs PL control [$\sigma$]",fontsize=10)
a1.set_xticks(range(len(params))); a1.set_xticklabels(params,rotation=45,ha="right",fontsize=8)
a1.set_yticks(range(len(lab))); a1.set_yticklabels(lab,fontsize=7)
fig.colorbar(im1,ax=a1,shrink=.8,label=r"$\Delta\theta/\sigma$")
im2=a2.imshow(np.log10(width),cmap="viridis",aspect="auto")
a2.set_title(r"Posterior width ratio [$\log_{10}(\sigma/\sigma_{\rm PL})$]",fontsize=10)
a2.set_xticks(range(len(params))); a2.set_xticklabels(params,rotation=45,ha="right",fontsize=8)
a2.set_yticks(range(len(lab))); a2.set_yticklabels(lab,fontsize=7)
fig.colorbar(im2,ax=a2,shrink=.8,label=r"$\log_{10}(\sigma/\sigma_{\rm PL})$")
fig.suptitle("Fitting BT mocks with a non-BT model: shifts and broadening",fontsize=11)
fig.tight_layout(); fig.savefig(OUT,dpi=200,bbox_inches="tight"); print("saved",OUT,shift.shape)
