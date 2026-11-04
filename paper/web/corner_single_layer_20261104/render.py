"""One translucent filled region and one outline per data set, for later overlay."""
from pathlib import Path
import argparse, importlib.util, json
import numpy as np
from scipy.ndimage import gaussian_filter

B=Path(__file__).resolve().parent
ROOT=B.parents[2]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

curves=module('contour_refinement',B.parent/'corner_contours_20261104/render.py')

def draw(a,labels,spec,limits,readable_ticks,groups=None):
    fig,checks=curves.draw(a,labels,dict(spec,kind='lines'),limits,readable_ticks,groups)
    lim=limits(a);n=a.shape[1]
    for i in range(n):
      for j in range(i+1):
        ax=fig.axes[i*n+j]
        if i==j:
            for line in ax.lines:
                ax.fill_between(line.get_xdata(),0,line.get_ydata(),color=line.get_color(),alpha=.12,lw=0)
        else:
            for coll in list(ax.collections):coll.remove()
            h,xe,ye=np.histogram2d(a[:,j],a[:,i],bins=32,range=[lim[j],lim[i]])
            assert int(h.sum())==len(a)
            sm=gaussian_filter(h.T,1.1,mode='reflect');sm/=sm.max()
            xc=(xe[:-1]+xe[1:])/2;yc=(ye[:-1]+ye[1:])/2
            ax.contourf(xc,yc,sm,levels=[.10,1.00001],colors=[curves.INK],alpha=.18,antialiased=True)
            ax.contour(xc,yc,sm,levels=[.10],colors=[curves.INK],linewidths=.9)
    checks.update(contour_levels_peak_relative=[.10],filled_regions_per_dataset=1,outline_levels_per_dataset=1,fill_alpha=.18,marginal_fill_alpha=.12)
    return fig,checks

def main(source,atlas):
    base=module('corner_structures',B.parent/'corner_structures_20261104/render.py');base.B=B;base.draw=draw
    base.DESIGNS=[dict(kind='single',name='单层填色轮廓',en='Single-layer filled contour',desc='每组数据只保留一层半透明填色和一条外轮廓；边缘分布用轻填色曲线，为另一组数据预留叠加空间。')]
    original_sha=base.sha;base.sha=lambda p:original_sha(Path(__file__) if Path(p).resolve()==Path(base.__file__).resolve() else p)
    old=ROOT/'output/html/BTemu_five_designs_20261104.html';prior=old.read_bytes() if old.exists() else None
    try:
        base.main(source,atlas);html=old.read_text()
    finally:
        if prior is not None:old.write_bytes(prior)
    html=html.replace('Corner 图 · 五个设计方向','Corner 图 · 单层填色')
    html=html.replace('同一份原始样本、同一蓝色系，比较五种布局和密度表达；图内仅保留坐标与数据。','每组数据一层半透明填色＋一条外轮廓，为第二组数据留出叠加空间。')
    html=html.replace('轮廓为面板峰值密度的等值线，平滑宽度为 0.9 个分箱；散点最多显示 4,500 个等距选取的存储行，轮廓使用全部留样。六边形计数使用全部样本。','外轮廓沿用面板峰值密度的 10% 等值线；二维平滑宽度 1.1 个分箱，填色透明度 18%。')
    html=html.replace('</style>','article header,#compare,#one,#single{display:none!important}.grid{grid-template-columns:1fr;max-width:1200px;margin:auto}</style>')
    out=ROOT/'output/html/BTemu_corner_single_layer_20261104.html';out.write_text(html);(B/'index.html').write_text(html.replace('figure_directions_20261104/','assets/'))
    m=json.loads((B/'manifest.json').read_text());m['direction']='single-layer filled contour for future data overlay';m['second_dataset_added']=False;m['dependencies_sha256']={str(p.relative_to(ROOT)):original_sha(p) for p in [Path(curves.__file__),Path(base.__file__)]};(B/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(out,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--atlas',type=Path,required=True);args=p.parse_args();main(args.source.resolve(),args.atlas.resolve())
