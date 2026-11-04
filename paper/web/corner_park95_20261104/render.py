"""Park-inspired single 95% smoothed sample-density regions; preview PNGs."""
from pathlib import Path
import argparse, importlib.util, json
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

B=Path(__file__).resolve().parent
ROOT=B.parents[2]
INK='#3D4C59'
FILL='#8B9BA8'

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

curves=module('contour_refinement',B.parent/'corner_contours_20261104/render.py')

def mass_level(field,target=.95):
    """Highest-density threshold on an equal-area integration grid; include ties."""
    assert np.isfinite(field).all() and field.min()>=0 and field.sum()>0
    values=np.sort(field.ravel())[::-1]
    k=int(np.searchsorted(np.cumsum(values),target*values.sum(),side='left'))
    level=float(values[k]);mass=float(field[field>=level].sum()/field.sum())
    strict=float(field[field>level].sum()/field.sum())
    assert strict<target+1e-12 and mass>=target-1e-12
    return level,{'target_mass':target,'integrated_mass_at_or_above_level':mass,'integrated_mass_strictly_above_level':strict,'threshold':level,'integration_grid_shape':list(field.shape)}

def analytic_check():
    x=np.linspace(-5,5,512);xx,yy=np.meshgrid(x,x);field=np.exp(-.5*(xx*xx+yy*yy))
    level,audit=mass_level(field)
    # An untruncated 2D standard Gaussian has threshold/peak = 1 - mass.
    assert abs(level/field.max()-.05)<.001
    _,flat=mass_level(np.ones((20,20)))
    assert flat['integrated_mass_at_or_above_level']==1.0
    return dict(gaussian_threshold_over_peak=level/field.max(),expected_gaussian_threshold_over_peak=.05,uniform_ties='whole plateau included',passed=True)

def density_grid(h,limx,limy):
    sm=gaussian_filter(h.T,1.1,mode='reflect')
    # Integrate an interpolated density over the complete original plotting range.
    # Cell centres give equal-area quadrature; edges are added only for drawing.
    grid=256
    px=(np.arange(grid)+.5)*32/grid-.5
    xx,yy=np.meshgrid(px,px)
    field=map_coordinates(sm,[yy,xx],order=1,mode='nearest')
    level,audit=mass_level(field)
    assert audit['integrated_mass_at_or_above_level']<=.951
    x=limx[0]+(np.arange(grid)+.5)/grid*(limx[1]-limx[0])
    y=limy[0]+(np.arange(grid)+.5)/grid*(limy[1]-limy[0])
    return np.r_[limx[0],x,limx[1]],np.r_[limy[0],y,limy[1]],np.pad(field,1,mode='edge'),level,audit

def draw(a,labels,spec,limits,readable_ticks,groups=None):
    fig,checks=curves.draw(a,labels,dict(spec,kind='lines'),limits,readable_ticks,groups)
    fig.subplots_adjust(top=.95)
    lim=limits(a);n=a.shape[1];regions=[];summaries=[]
    for i in range(n):
      for j in range(i+1):
        ax=fig.axes[i*n+j]
        for sp in ax.spines.values():sp.set_visible(True);sp.set_color('#77838D');sp.set_linewidth(.55)
        ax.tick_params(direction='in',bottom=True,left=i!=j,length=2,width=.45)
        if i==j:
            lo,median,hi=np.quantile(a[:,i],[.025,.5,.975])
            lower,upper=median-lo,hi-median
            scale=min(v for v in [lower,upper] if v>0)
            decimals=max(0,min(6,1-int(np.floor(np.log10(scale)))))
            fmt=lambda v:f'{v:.{decimals}f}'
            title=rf'${fmt(median)}^{{+{fmt(upper)}}}_{{-{fmt(lower)}}}$'
            ax.set_title(title,fontsize=9.5 if n==6 else 8.8,pad=3,color=INK)
            summaries.append(dict(parameter_index=i,label=labels[i],median=float(median),q025=float(lo),q975=float(hi),lower_offset=float(lower),upper_offset=float(upper),display=title,selection='all retained rows; pooled across historical ensemble groups'))
            for k,line in enumerate(ax.lines):
                color=INK if k==0 else '#376C96';line.set_color(color);line.set_linewidth(1.05)
                ax.fill_between(line.get_xdata(),0,line.get_ydata(),color=FILL if k==0 else color,alpha=.32 if k==0 else .12,lw=0)
        else:
            for coll in list(ax.collections):coll.remove()
            h,_,_=np.histogram2d(a[:,j],a[:,i],bins=32,range=[lim[j],lim[i]])
            assert int(h.sum())==len(a)
            x,y,field,level,audit=density_grid(h,lim[j],lim[i])
            ax.contourf(x,y,field,levels=[level,np.nextafter(field.max(),np.inf)],colors=[FILL],alpha=.45,antialiased=True)
            ax.contour(x,y,field,levels=[level],colors=[INK],linewidths=.85)
            regions.append(dict(x_parameter_index=j,y_parameter_index=i,**audit))
    assert not fig.texts and all(not ax.get_visible() for i in range(n) for ax in fig.axes[i*n+i+1:(i+1)*n])
    checks.pop('contour_levels_peak_relative',None)
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    for i in range(n):
        bb=fig.axes[i*n+i].title.get_window_extent(renderer)
        assert bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height,'Marginal number outside canvas'
    checks.update(region_definition='95% highest-density region of interpolated smoothed stored-sample density',contour_probability_content=.95,regions=regions,marginal_summaries=summaries,marginal_annotation='median with 2.5th–97.5th percentile offsets of retained rows',filled_bands_per_dataset=1,outline_levels_per_dataset=1,fill_alpha=.45,in_figure_information_blocks=0)
    return fig,checks

def main(source,atlas):
    validation=analytic_check()
    base=module('corner_structures',B.parent/'corner_structures_20261104/render.py');base.B=B;base.draw=draw
    base.DESIGNS=[dict(kind='park95',name='Park 风格 · 95% 样本区域',en='Park-style 95% sample-density region',desc='单层浅灰填色与一条深灰外轮廓；阈值由密度积分得到，保留紧凑下三角与对角边缘分布。')]
    original_sha=base.sha;base.sha=lambda p:original_sha(Path(__file__) if Path(p).resolve()==Path(base.__file__).resolve() else p)
    old=ROOT/'output/html/BTemu_five_designs_20261104.html';prior=old.read_bytes() if old.exists() else None
    try:
        base.main(source,atlas);html=old.read_text()
    finally:
        if prior is not None:old.write_bytes(prior)
    html=html.replace('Corner 图 · 五个设计方向','Corner 图 · Park 风格 95% 样本区域')
    html=html.replace('同一份原始样本、同一蓝色系，比较五种布局和密度表达；图内仅保留坐标与数据。','单层浅灰填色＋一条 95% 样本密度轮廓。紧凑下三角布局，右上角留空。')
    html=html.replace('轮廓为面板峰值密度的等值线，平滑宽度为 0.9 个分箱；散点最多显示 4,500 个等距选取的存储行，轮廓使用全部留样。六边形计数使用全部样本。','二维轮廓包围平滑样本密度的 95%。对角线上方数字为全部留样的中位数及 2.5%–97.5% 分位区间，以不对称上下偏差表示。')
    html=html.replace('</style>','article header,#compare,#one,#single{display:none!important}.grid{grid-template-columns:1fr;max-width:1200px;margin:auto}</style>')
    out=ROOT/'output/html/BTemu_corner_Park95_20261104.html';out.write_text(html);(B/'index.html').write_text(html.replace('figure_directions_20261104/','assets/'))
    m=json.loads((B/'manifest.json').read_text());m.pop('contours_are_peak_density_levels_not_credible_regions',None)
    m.update(direction='Park-style single 95% stored-sample density region',second_dataset_added=False,analytic_validation=validation,reference='https://arxiv.org/html/1809.08995v2#S6.F4',dependencies_sha256={str(p.relative_to(ROOT)):original_sha(p) for p in [Path(curves.__file__),Path(base.__file__)]})
    (B/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
    from PIL import Image,ImageDraw,ImageFont
    sheet=Image.new('RGB',(1800,940),'#edf1f4');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23)
    folder=B/'assets'/m['designs'][0]['id']
    for k,(name,title) in enumerate(base.FIGURES[:2]):
        im=Image.open(folder/(name+'.png')).convert('RGB');im.thumbnail((885,885));sheet.paste(im,(k*900+(900-im.width)//2,48));d.text((k*900+18,12),title+' | 95% sample-density region',font=font,fill=INK)
    sheet.save(ROOT/'output/html/BTemu_corner_Park95_preview_20261104.png');print(out,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--atlas',type=Path,required=True);args=p.parse_args();main(args.source.resolve(),args.atlas.resolve())
