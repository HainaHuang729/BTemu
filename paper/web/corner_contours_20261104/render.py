"""Refine the selected contour direction; unchanged archived samples, PNG previews."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, gaussian_filter1d
from matplotlib.ticker import FixedLocator, FuncFormatter

B=Path(__file__).resolve().parent
ROOT=B.parents[2]
INK='#285E7A'
BLUE=['#f0f5f8','#d5e4ec','#9cbccc','#598ba5']

def draw(a,labels,spec,limits,readable_ticks,groups=None):
    n=a.shape[1];kind=spec['kind'];lim=limits(a)
    plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':10,'axes.labelsize':12,'xtick.labelsize':9,'ytick.labelsize':9,'text.color':'#253847','axes.labelcolor':'#253847','xtick.color':'#506577','ytick.color':'#506577','figure.facecolor':'white','axes.facecolor':'white'})
    size={6:7.5,8:9.,9:9.8}[n];fig,axs=plt.subplots(n,n,figsize=(size,size))
    fig.subplots_adjust(left=.12,right=.985,bottom=.105,top=.985,wspace=.065,hspace=.065)
    counts=[]
    for i in range(n):
      for j in range(n):
        ax=axs[i,j]
        if j>i:ax.set_visible(False);continue
        ax.set_xlim(lim[j]);ax.xaxis.set_major_locator(FixedLocator(readable_ticks(lim[j])));ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'))
        ax.tick_params(length=2,width=.45,pad=3)
        if i==j:
            sets=[(np.ones(len(a),bool),INK,'-')] if groups is None else [(groups==g,c,ls) for g,c,ls in [(0,INK,'-'),(1,'#A96549','--')]]
            for mask,c,ls in sets:
                h,e=np.histogram(a[mask,i],bins=32,range=lim[i],density=True)
                y=gaussian_filter1d(h,.8,mode='reflect');x=(e[1:]+e[:-1])/2
                ax.plot(x,y,color=c,lw=1.1,ls=ls)
                if kind!='lines':ax.fill_between(x,0,y,color=c,alpha=.10 if kind=='wash' else .18,lw=0)
            ax.set_yticks([]);ax.set_ylim(bottom=0)
        else:
            ax.set_ylim(lim[i]);ax.yaxis.set_major_locator(FixedLocator(readable_ticks(lim[i])));ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'))
            h,xe,ye=np.histogram2d(a[:,j],a[:,i],bins=32,range=[lim[j],lim[i]])
            assert int(h.sum())==len(a);counts.append(int(h.sum()))
            sm=gaussian_filter(h.T,1.1,mode='reflect');sm/=sm.max()
            xc=(xe[1:]+xe[:-1])/2;yc=(ye[1:]+ye[:-1])/2
            if kind=='wash':
                ax.contourf(xc,yc,sm,levels=[.10,1.00001],colors=['#e7f0f5'],antialiased=True)
            elif kind=='bands':
                ax.contourf(xc,yc,sm,levels=[.10,.32,.60,.82,1.00001],colors=BLUE,antialiased=True)
            ax.contour(xc,yc,sm,levels=[.10,.32,.60,.82] if kind=='bands' else [.10,.35,.70],colors=INK,linewidths=[.45,.55,.65,.75] if kind=='bands' else [.55,.8,1.05],alpha=.65 if kind=='bands' else .95)
        for side,sp in ax.spines.items():
            sp.set_visible(i!=j and side in ['bottom','left']);sp.set_linewidth(.45);sp.set_color('#B4C0C9')
        # Only the perimeter carries ticks; panel boundaries stay quiet.
        ax.tick_params(bottom=i==n-1,left=j==0 and i!=j,labelbottom=i==n-1,labelleft=j==0 and i!=j)
        if i==n-1:ax.set_xlabel(labels[j],labelpad=7)
        if j==0 and i!=j:ax.set_ylabel(labels[i],labelpad=7)
    assert len(fig.texts)==0
    fig.canvas.draw();r=fig.canvas.get_renderer()
    for ax in fig.axes:
        if not ax.get_visible():continue
        for t in [ax.xaxis.label,ax.yaxis.label,*ax.get_xticklabels(),*ax.get_yticklabels()]:
            if t.get_visible() and t.get_text():
                bb=t.get_window_extent(r);assert bb.x0>=-1 and bb.y0>=-1 and bb.x1<=fig.bbox.width+1 and bb.y1<=fig.bbox.height+1,(kind,t.get_text())
    return fig,dict(rows=len(a),all_pair_histogram_counts=counts,bins=32,smoothing_sigma_bins_2d=1.1,smoothing_sigma_bins_1d=.8,contour_levels_peak_relative=[.10,.32,.60,.82] if kind=='bands' else [.10,.35,.70],figure_information_blocks=0)

def main(source,atlas):
    path=B.parent/'corner_structures_20261104/render.py'
    s=importlib.util.spec_from_file_location('structures',path);base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
    base.B=B;base.draw=draw
    base.DESIGNS=[dict(kind='lines',name='纯线轮廓',en='Contour lines',desc='三条等密度线，线重由外向内递增；边缘分布也只保留平滑曲线。'),dict(kind='wash',name='浅填色轮廓 · 推荐',en='Contours with a light wash',desc='浅色统一铺底，三条轮廓保持清晰；边缘曲线轻填色，层次与留白更均衡。'),dict(kind='bands',name='分层填色轮廓',en='Layered contour bands',desc='四层递进填色突出密度核心；细线区分层次，适合需要更强密度对比的版本。')]
    original_sha=base.sha
    base.sha=lambda p: original_sha(Path(__file__) if Path(p).resolve()==path.resolve() else p)
    old_page=ROOT/'output/html/BTemu_five_designs_20261104.html';old_bytes=old_page.read_bytes() if old_page.exists() else None
    try:
        base.main(source,atlas)
        html=old_page.read_text()
    finally:
        if old_bytes is not None:old_page.write_bytes(old_bytes)
    html=html.replace('Corner 图 · 五个设计方向','Corner 图 · 轮廓细化').replace('五套对照','三套对照')
    html=html.replace('同一份原始样本、同一蓝色系，比较五种布局和密度表达；图内仅保留坐标与数据。','沿轮廓方向细化：纯线、浅填色、分层填色。三套使用同一份原始样本、同一紧凑下三角布局。')
    html=html.replace('轮廓为面板峰值密度的等值线，平滑宽度为 0.9 个分箱；散点最多显示 4,500 个等距选取的存储行，轮廓使用全部留样。六边形计数使用全部样本。','全部留样参与计数；二维与一维平滑宽度分别为 1.1 和 0.8 个分箱。轮廓表示相对面板峰值的密度等值线，方法说明均置于图外。')
    out=ROOT/'output/html/BTemu_corner_contours_20261104.html';out.write_text(html);(B/'index.html').write_text(html.replace('figure_directions_20261104/','assets/'))
    manifest=json.loads((B/'manifest.json').read_text());manifest['direction']='contour refinement';manifest['recommended_kind']='wash';(B/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    from PIL import Image,ImageDraw,ImageFont
    sheet=Image.new('RGB',(1800,650),'#eaf0f4');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
    for i,spec in enumerate(manifest['designs']):
        im=Image.open(B/'assets'/spec['id']/'fig11_btemu_corner6_5000.png').convert('RGB');im.thumbnail((590,590));sheet.paste(im,(i*600+(600-im.width)//2,50));d.text((i*600+14,14),spec['en'],font=font,fill='#263b4d')
    sheet.save(ROOT/'output/html/BTemu_corner_contours_preview_20261104.png');print(out,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--atlas',type=Path,required=True);args=p.parse_args();main(args.source.resolve(),args.atlas.resolve())
