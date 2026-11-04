"""Overlay actual PL and BT sample arrays, using the approved Park-style design.

No synthetic data or extraction from raster figures is used. Input discard counts
are explicit; HDF5/NPZ files must carry parameter_names, or use --*-names JSON.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import FixedLocator, FuncFormatter, MaxNLocator

B=Path(__file__).resolve().parent
ROOT=B.parents[2]
PARAMETERS=['ETA_STAR','t_STAR','ALPHA_STAR','M_TURN','F_ESC10','ALPHA_ESC']
LABELS=[r'$\eta_\star$',r'$t_\star$',r'$\alpha_\star$',r'$\log_{10}M_{\rm turn}$',r'$\log_{10}f_{{\rm esc},10}$',r'$\alpha_{\rm esc}$']
PL='#B56B42';BT='#285E7A';FILL='#8B9BA8'
STYLE_NAME='park-overlay-unified-v1'
DASH=(0,(4,2))
STAT_DECIMALS=[3,2,2,2,2,2]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def load(path,discard,names_path=None):
    """Read actual stored samples; never reconstruct a joint distribution from quantiles."""
    names=None
    if path.suffix.lower() in ['.h5','.hdf5']:
        with h5py.File(path,'r') as f:
            key='chain' if 'chain' in f else 'mcmc/chain'
            a=f[key][:]
            if 'parameter_names' in f:names=f['parameter_names'][:]
            elif 'parameter_names' in f.attrs:names=f.attrs['parameter_names']
    elif path.suffix.lower()=='.npz':
        with np.load(path,allow_pickle=False) as f:
            key='samples' if 'samples' in f else 'chain';a=f[key]
            if 'parameter_names' in f:names=f['parameter_names']
    elif path.suffix.lower()=='.csv':
        table=np.genfromtxt(path,delimiter=',',names=True);names=list(table.dtype.names);a=np.column_stack([table[n] for n in names])
    else:raise ValueError('Expected HDF5, NPZ, or named-column CSV samples')
    if names_path is not None:names=json.loads(names_path.read_text())
    if isinstance(names,str):names=json.loads(names)
    if names is None:raise ValueError(f'{path}: parameter_names are required; supply --pl-names/--bt-names JSON')
    names=[n.decode() if isinstance(n,bytes) else str(n) for n in names]
    assert a.ndim in [2,3] and a.shape[-1]==len(names)
    assert 0<=discard<len(a)
    shape=list(a.shape);kept=a[discard:].reshape(-1,a.shape[-1])
    missing=set(PARAMETERS)-set(names)
    if missing:raise ValueError(f'{path}: missing exact coordinates {sorted(missing)}; no automatic F_STAR10/ETA_STAR conversion is assumed')
    a=np.asarray(kept[:,[names.index(p) for p in PARAMETERS]],float)
    assert len(a)>1 and np.isfinite(a).all()
    receipt=dict(file=str(path.resolve()),sha256=sha(path),stored_shape=shape,discard_leading_stored_rows_or_steps=discard,retained_rows=len(a),source_parameters=names,selected_parameters=PARAMETERS,coordinate_transform='none')
    return a,receipt

def number(a,decimals=None):
    lo,m,hi=np.quantile(a,[.025,.5,.975]);lower=m-lo;upper=hi-m
    positive=[x for x in [lower,upper] if x>0]
    dec=decimals if decimals is not None else (max(0,min(6,1-int(np.floor(np.log10(min(positive)))))) if positive else 3)
    fmt=lambda x:f'{x:.{dec}f}'
    return rf'${fmt(m)}^{{+{fmt(upper)}}}_{{-{fmt(lower)}}}$',dict(median=float(m),q025=float(lo),q975=float(hi))

def display_limits(a):
    result=[]
    for col in a.T:
        lo,hi=col.min(),col.max();pad=max((hi-lo)*.025,1e-8);result.append((lo-pad,hi+pad))
    return result

def axis_ticks(lim):
    lo,hi=lim;span=hi-lo
    ticks=MaxNLocator(4,min_n_ticks=3).tick_values(lo,hi)
    ticks=ticks[(ticks>=lo+.08*span)&(ticks<=hi-.08*span)]
    return ticks

def render(pl,bt,out,shared_limits=None,shared_marginal_ymax=None):
    p=B.parent/'corner_park95_20261104/render.py';sp=importlib.util.spec_from_file_location('park95',p);park=importlib.util.module_from_spec(sp);sp.loader.exec_module(park)
    lim=shared_limits if shared_limits is not None else display_limits(np.concatenate([pl,bt]));n=len(PARAMETERS)
    for a in [pl,bt]:assert all(a[:,i].min()>=lo and a[:,i].max()<=hi for i,(lo,hi) in enumerate(lim))
    plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':10,'axes.labelsize':11.5,'xtick.labelsize':9,'ytick.labelsize':9,'text.color':'#344C5E','axes.labelcolor':'#344C5E','xtick.color':'#506577','ytick.color':'#506577','figure.facecolor':'white','axes.facecolor':'white','axes.grid':False})
    fig,axs=plt.subplots(n,n,figsize=(8.25,8.25));fig.subplots_adjust(left=.125,right=.985,bottom=.11,top=.91,wspace=.10,hspace=.10)
    checks={'PL':[],'BT':[]};summaries={'PL':[],'BT':[]}
    for i in range(n):
      for j in range(n):
        ax=axs[i,j]
        if j>i:ax.set_visible(False);continue
        ax.set_xlim(lim[j]);ax.xaxis.set_major_locator(FixedLocator(axis_ticks(lim[j])));ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}'))
        ax.tick_params(direction='in',length=2.1,width=.45,labelbottom=i==n-1,labelleft=j==0 and i!=j,pad=3)
        for spine in ax.spines.values():spine.set_color('#A3ADB6');spine.set_linewidth(.45)
        if i==j:
            for name,a,c,ls,ytext in [('BT',bt,BT,'-',1.27),('PL',pl,PL,DASH,1.08)]:
                h,e=np.histogram(a[:,i],bins=32,range=lim[i],density=True);y=gaussian_filter1d(h,.8,mode='reflect');x=(e[1:]+e[:-1])/2
                ax.plot(x,y,color=c,ls=ls,lw=1.15)
                if name=='BT':ax.fill_between(x,0,y,color=FILL,alpha=.18,lw=0)
                title,stats=number(a[:,i],STAT_DECIMALS[i]);summaries[name].append(dict(parameter=PARAMETERS[i],**stats))
                ax.text(.5,ytext,name+' '+title,transform=ax.transAxes,ha='center',va='bottom',fontsize=8.6,color=c)
            ax.set_yticks([])
            if shared_marginal_ymax is not None:ax.set_ylim(0,shared_marginal_ymax[i])
            else:ax.set_ylim(bottom=0)
        else:
            ax.set_ylim(lim[i]);ax.yaxis.set_major_locator(FixedLocator(axis_ticks(lim[i])));ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}'))
            for name,a,c,ls in [('BT',bt,BT,'-'),('PL',pl,PL,DASH)]:
                h,_,_=np.histogram2d(a[:,j],a[:,i],bins=32,range=[lim[j],lim[i]]);assert int(h.sum())==len(a)
                x,y,field,level,coverage=park.density_grid(h,lim[j],lim[i])
                if name=='BT':ax.contourf(x,y,field,levels=[level,np.nextafter(field.max(),np.inf)],colors=[FILL],alpha=.30)
                ax.contour(x,y,field,levels=[level],colors=[c],linewidths=1.,linestyles=[ls])
                checks[name].append(dict(x_parameter=PARAMETERS[j],y_parameter=PARAMETERS[i],rows=len(a),**coverage))
        if i==n-1:ax.set_xlabel(LABELS[j],labelpad=7)
        if j==0 and i!=j:ax.set_ylabel(LABELS[i],labelpad=7)
    fig.canvas.draw();r=fig.canvas.get_renderer()
    for ax in fig.axes:
        if not ax.get_visible():continue
        for t in [ax.xaxis.label,ax.yaxis.label,*ax.texts,*ax.get_xticklabels(),*ax.get_yticklabels()]:
            if t.get_visible() and t.get_text():
                bb=t.get_window_extent(r);assert bb.x0>=-1 and bb.y0>=-1 and bb.x1<=fig.bbox.width+1 and bb.y1<=fig.bbox.height+1,t.get_text()
    assert not fig.texts
    out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out,dpi=250,facecolor='white');plt.close(fig)
    return dict(common_coordinate_limits=lim,common_marginal_ymax=shared_marginal_ymax,sample_density_coverage=checks,marginal_summaries=summaries,style_name=STYLE_NAME,style={'BT':'blue solid outline with single light-grey fill','PL':'orange dashed outline, no fill','font':'STIXGeneral','figure_inches':[8.25,8.25],'contour_width_pt':1.,'marginal_width_pt':1.15,'axis_width_pt':.45,'fill_alpha_2d':.30,'fill_alpha_1d':.18,'pl_dash_pattern':[4,2],'annotation_order_top_to_bottom':['BT','PL'],'annotation_decimals':STAT_DECIMALS,'shared_across_all_cases':shared_limits is not None},second_data_set_included=True,upper_triangle_information_blocks=0,renderer_sha256=sha(Path(__file__)),park_renderer_sha256=sha(Path(park.__file__)))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['pl','bt']:
        p.add_argument('--'+name,type=Path,required=True);p.add_argument('--'+name+'-discard',type=int,required=True);p.add_argument('--'+name+'-names',type=Path)
    p.add_argument('--output',type=Path,default=ROOT/'output/html/BTemu_corner_PL_BT_Park95_20261104.png');args=p.parse_args()
    pl,rp=load(args.pl,args.pl_discard,args.pl_names);bt,rb=load(args.bt,args.bt_discard,args.bt_names)
    audit=render(pl,bt,args.output);audit['sources']={'PL':rp,'BT':rb};audit['output_sha256']=sha(args.output)
    assert sha(args.pl)==rp['sha256'] and sha(args.bt)==rb['sha256']
    args.output.with_suffix('.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');print(args.output)
