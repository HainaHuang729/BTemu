"""Five structural corner designs from unchanged archived chains; PNG previews only."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, secrets, shutil, sys
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, PowerNorm
from matplotlib.ticker import FixedLocator, FuncFormatter
from scipy.ndimage import gaussian_filter

B=Path(__file__).resolve().parent
ROOT=B.parents[2]
OUT=ROOT/'output/html'
COLOR='#285E7A'
CMAP=LinearSegmentedColormap.from_list('same_blue',['#ffffff','#e6eef3','#acc7d6','#608fa8','#254e6a'])
DESIGNS=[
 dict(kind='filled',name='紧凑填色轮廓',en='Compact filled contours',desc='下三角紧贴排列；平滑计数密度分四层填色，细轮廓强调峰形，边缘直方图实心填充。'),
 dict(kind='hex',name='分隔六边形计数',en='Separated hexbin panels',desc='下三角留出宽间隔，以六边形单元展示原始样本计数；边缘分布用分立柱形。'),
 dict(kind='upper',name='上三角像素密度',en='Upper-triangle density',desc='翻转至上三角，参数标签移到顶部和右侧；保留未经平滑的 32×32 像素计数，边缘分布为阶梯线。'),
 dict(kind='matrix',name='完整双侧矩阵',en='Full dual-view matrix',desc='展开完整矩阵：下三角为原始计数图，上三角为平滑等密度线；对角线保留边缘直方图。'),
 dict(kind='scatter',name='散点与线框轮廓',en='Scatter and contour lines',desc='下三角用稀疏散点显示样本结构，叠加三条平滑等密度线；直方图仅保留轮廓，面板去边框。'),
]
FIGURES=[('fig11_btemu_corner6_5000','6D corner'),('fig12_btemu_corner8_5568','8D corner'),('fig13_exact_corner6_200','Exact 200-step corner'),('fig8_21cmtb_corner_fixed8','21cmTB 8D corner'),('fig9_21cmtb_corner_free9','21cmTB 9D corner')]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def draw(a,labels,spec,limits,readable_ticks,groups=None):
    n=a.shape[1];kind=spec['kind'];upper=kind=='upper';full=kind=='matrix'
    plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':10,'axes.labelsize':12,'xtick.labelsize':9,'ytick.labelsize':9,'text.color':'#253847','axes.labelcolor':'#253847','xtick.color':'#506577','ytick.color':'#506577','axes.linewidth':.55,'figure.facecolor':'white','axes.facecolor':'white'})
    lim=limits(a);size={6:7.5,8:9.0,9:9.8}[n]
    fig,axs=plt.subplots(n,n,figsize=(size,size))
    gap={'filled':.025,'hex':.34,'upper':.08,'matrix':.07,'scatter':.16}[kind]
    fig.subplots_adjust(left=.035 if upper else .12,right=.80 if upper else .985,bottom=.025 if upper else .105,top=.875 if upper else .985,wspace=gap,hspace=gap)
    counts=[];scatter_counts=[]
    for i in range(n):
      for j in range(n):
        ax=axs[i,j]
        if (upper and j<i) or (not upper and not full and j>i):ax.set_visible(False);continue
        ax.set_xlim(lim[j]);ax.xaxis.set_major_locator(FixedLocator(readable_ticks(lim[j])));ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'))
        ax.tick_params(length=2,width=.5,pad=3)
        if i==j:
            sets=[(np.ones(len(a),bool),COLOR,'-')] if groups is None else [(groups==g,c,ls) for g,c,ls in [(0,COLOR,'-'),(1,'#A96549','--')]]
            for mask,c,ls in sets:
                ax.hist(a[mask,i],bins=32,range=lim[i],density=True,histtype='bar' if kind=='hex' else ('stepfilled' if kind in ['filled','matrix'] else 'step'),color=c,alpha=.65 if kind=='hex' else (.28 if kind in ['filled','matrix'] else 1),rwidth=.80 if kind=='hex' else 1,lw=1.3,ls=ls)
            ax.set_yticks([])
        else:
            ax.set_ylim(lim[i]);ax.yaxis.set_major_locator(FixedLocator(readable_ticks(lim[i])));ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'))
            h,xe,ye=np.histogram2d(a[:,j],a[:,i],bins=32,range=[lim[j],lim[i]])
            assert int(h.sum())==len(a);counts.append(int(h.sum()))
            xc=(xe[1:]+xe[:-1])/2;yc=(ye[1:]+ye[:-1])/2
            sm=gaussian_filter(h.T,.9,mode='reflect');sm/=sm.max()
            if kind=='hex':
                coll=ax.hexbin(a[:,j],a[:,i],gridsize=24,extent=(*lim[j],*lim[i]),mincnt=1,cmap=CMAP,norm=PowerNorm(.5),linewidths=.12,edgecolors='white',rasterized=True)
                assert int(coll.get_array().sum())==len(a)
            elif kind=='filled':
                levels=[.08,.25,.50,.75,1.00001]
                ax.contourf(xc,yc,sm,levels=levels,cmap=CMAP,vmin=-.1,vmax=1,antialiased=True)
                ax.contour(xc,yc,sm,levels=levels[:-1],colors=COLOR,linewidths=.45,alpha=.7)
            elif kind=='scatter':
                indices=np.linspace(0,len(a)-1,min(len(a),4500),dtype=int)
                ax.scatter(a[indices,j],a[indices,i],s=.9,c=COLOR,alpha=.14,edgecolors='none',rasterized=True)
                scatter_counts.append(len(indices))
                ax.contour(xc,yc,sm,levels=[.15,.40,.75],colors=COLOR,linewidths=[.6,.85,1.1])
            elif kind=='matrix' and j>i:
                ax.contour(xc,yc,sm,levels=[.15,.40,.75],colors=COLOR,linewidths=[.55,.85,1.2])
            else:ax.pcolormesh(xe,ye,h.T,cmap=CMAP,norm=PowerNorm(.5,vmin=0,vmax=h.max()),rasterized=True,shading='flat')
        for side,sp in ax.spines.items():
            sp.set_color('#ACBAC4');sp.set_linewidth(.5)
            sp.set_visible(kind=='hex' or (kind!='scatter' and side in ['bottom','left'] and i!=j))
        if upper:
            ax.xaxis.tick_top();ax.xaxis.set_label_position('top');ax.yaxis.tick_right();ax.yaxis.set_label_position('right')
            ax.tick_params(labeltop=i==0,labelbottom=False,labelright=j==n-1 and i!=j,labelleft=False)
            if i==0:ax.set_xlabel(labels[j],labelpad=7)
            if j==n-1 and i!=j:
                ax.set_ylabel(labels[i],rotation=0,ha='left',va='center',fontsize=10.7)
                ax.yaxis.set_label_coords(1.35,.5)
        else:
            ax.tick_params(labelbottom=i==n-1,labelleft=j==0 and i!=j)
            if i==n-1:ax.set_xlabel(labels[j],labelpad=7)
            if j==0 and i!=j:ax.set_ylabel(labels[i],labelpad=7)
        if kind=='scatter' and i!=j:ax.tick_params(length=0)
    assert len(fig.texts)==0,'No upper-triangle information blocks'
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    for ax in fig.axes:
        if not ax.get_visible():continue
        for t in [ax.xaxis.label,ax.yaxis.label,*ax.get_xticklabels(),*ax.get_yticklabels()]:
            if t.get_visible() and t.get_text():
                bb=t.get_window_extent(renderer)
                assert bb.x0>=-1 and bb.y0>=-1 and bb.x1<=fig.bbox.width+1 and bb.y1<=fig.bbox.height+1,(kind,t.get_text())
    return fig,{'rows':len(a),'all_pair_histogram_counts':counts,'scatter_display_rows_per_pair':scatter_counts,'bins':32,'smoothing_sigma_bins':.9 if kind in ['filled','matrix','scatter'] else 0,'contour_level_definition':'fractions of panel peak smoothed bin count, not credible probability content' if kind in ['filled','matrix','scatter'] else None,'hex_gridsize':24 if kind=='hex' else None,'figure_information_blocks':0}

def main(source,atlas):
    sys.path.insert(0,str(source));from render_new_chain_corners import read_case,CASES
    from plot_design import limits,readable_ticks,SHORT_LABELS
    inputs={str(p):sha(p) for p in (source/'chains').glob('*.h5')}
    cases=[]
    for key,name in [('6d',FIGURES[0][0]),('8d',FIGURES[1][0])]:
        a,meta=read_case(CASES[key]);labels=SHORT_LABELS[:6]+([r'$k_p$',r'$m_s$'] if key=='8d' else [])
        cases.append((name,a,labels,None))
    with h5py.File(source/'chains/chain6_exact_200.h5','r') as f:a=f['chain'][:].reshape(-1,6)
    assert a.shape==(6400,6);cases.append((FIGURES[2][0],a,SHORT_LABELS[:6],None))
    idx=json.loads((atlas/'web_data/joint_repaired1000/index.json').read_text())
    for branch,filename,name in [('fixed','pooled_samples.csv',FIGURES[3][0]),('free_ms','free_ms_samples.csv',FIGURES[4][0])]:
        p=atlas/'web_data/joint_repaired1000'/filename;assert sha(p)==idx['files_sha256'][filename];inputs[str(p)]=sha(p)
        rows=np.genfromtxt(p,delimiter=',',names=True);params=idx[branch]['parameters'];a=np.column_stack([rows[p] for p in params]);assert len(a)==idx[branch]['sample_count'];cases.append((name,a,SHORT_LABELS[:len(params)],rows['ensemble']))
    specs=[]
    for d in DESIGNS:
        spec=dict(d,nonce=secrets.token_hex(16),renderer_sha256=sha(Path(__file__)))
        spec['hash']=hashlib.sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False).encode()).hexdigest();spec['id']=spec['hash'][:12];spec['outputs']={};spec['checks']={}
        folder=B/'assets'/spec['id'];folder.mkdir(parents=True,exist_ok=True)
        for name,a,labels,groups in cases:
            fig,checks=draw(a,labels,spec,limits,readable_ticks,groups)
            p=folder/(name+'.png');fig.savefig(p,dpi=220,facecolor='white');plt.close(fig)
            spec['outputs'][name]=sha(p);spec['checks'][name]=checks
        target=OUT/'figure_directions_20261104'/spec['id'];shutil.copytree(folder,target,dirs_exist_ok=True)
        specs.append(spec);print(spec['id'],spec['name'],'5 corners rendered',flush=True)
    assert all(sha(Path(p))==h for p,h in inputs.items())
    manifest={'source_inputs_sha256':inputs,'same_original_samples':True,'same_palette_for_all_designs':True,'no_figure_information_blocks':True,'contours_are_peak_density_levels_not_credible_regions':True,'designs':specs}
    (B/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    path=B.parent/'figure_directions_20261104/build.py';sp=importlib.util.spec_from_file_location('gallery',path);gallery=importlib.util.module_from_spec(sp);sp.loader.exec_module(gallery);gallery.B=B;gallery.FIGURES=FIGURES
    p=gallery.page(specs)
    html=p.read_text().replace('以同一份 6D 链为例比较五套 corner 设计。可切换 8D、exact 200 步和 21cmTB；留样与分箱一致。','同一份原始样本、同一蓝色系，比较五种布局和密度表达；图内仅保留坐标与数据。').replace('点击放大</small>','点击放大</small>')
    html=html.replace('</header>\n<div class="tools">','<p style="font-size:13px">轮廓为面板峰值密度的等值线，平滑宽度为 0.9 个分箱；散点最多显示 4,500 个等距选取的存储行，轮廓使用全部留样。六边形计数使用全部样本。</p></header>\n<div class="tools">',1)
    p.write_text(html);(B/'index.html').write_text(html.replace('figure_directions_20261104/','assets/'))
    print(p,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--atlas',type=Path,required=True);args=parser.parse_args();main(args.source.resolve(),args.atlas.resolve())
