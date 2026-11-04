"""Reproduce the three actual PL/BT overlays and their standalone offline viewer."""
from pathlib import Path
import argparse, base64, json, subprocess
import numpy as np
import render as renderer

B=Path(__file__).resolve().parent
ROOT=B.parents[2]
CASES=[('kp10_ms2p5_100k','BT: kp=10, ms=2.5'),('kp1_ms1p5_100k','BT: kp=1, ms=1.5'),('kp5_ms1p5_100k','BT: kp=5, ms=1.5')]

def page(manifest):
    entries=[]
    for case in manifest['cases']:
        p=B/'assets'/case['file'];assert renderer.sha(p)==case['sha256']
        audit=(B/'assets'/case['audit']).read_bytes()
        entries.append(dict(case,image='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode(),audit_data='data:application/json;base64,'+base64.b64encode(audit).decode()))
    html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>PL 与 BT · Park 风格叠加</title><style>
*{box-sizing:border-box}body{margin:0;background:#eef1f4;color:#263a49;font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}header{background:white;border-bottom:1px solid #d4dee5;padding:26px 4vw 20px}h1{font-size:27px;font-weight:600;margin:0 0 8px}p{margin:4px 0;color:#5d6b77}.tools{background:#ffffffef;position:sticky;top:0;z-index:2;border-bottom:1px solid #d4dee5;display:flex;gap:20px;align-items:center;padding:13px 4vw}select,button{font:inherit;background:white;border:1px solid #b9c6d0;border-radius:5px;padding:7px 12px;color:#263a49;cursor:pointer}.key{display:flex;align-items:center;gap:8px}.line{display:inline-block;width:32px;border-top:2px solid #285e7a}.line.pl{border-color:#b56b42;border-top-style:dashed}main{max-width:1200px;margin:24px auto;background:white;border:1px solid #d4dee5}#image{display:block;width:100%;height:auto;cursor:zoom-in}.links{display:flex;gap:24px;padding:12px 20px;border-top:1px solid #e7edf1}a{color:#315e80}dialog{width:94vw;height:94vh;max-width:none;border:1px solid #9caebb;padding:15px}dialog::backdrop{background:#17202b99}.scroll{overflow:auto;height:calc(100% - 50px)}dialog img{display:block;max-width:100%;height:auto;margin:auto}
</style><header><h1>PL 与 BT · 95% 样本区域叠加</h1><p>统一配色、线型、刻度与数字精度；对角数字上排为 BT，下排为 PL。右上角留空。</p><p>三张图共用坐标范围、分箱和归一化方法。每组保留全部 96,000 行，轮廓包围各自平滑样本密度的 95%。</p></header><div class="tools"><label for="case">比较</label><select id="case"></select><span class="key"><i class="line"></i>BT：蓝色实线、浅灰填色</span><span class="key"><i class="line pl"></i>PL：橙色虚线</span></div><main><img id="image" alt="PL 与 BT 的六维 corner 图"><div class="links"><a id="png" download>下载 PNG</a><a id="audit" download>数据与计算记录</a></div></main><dialog id="viewer"><button id="close">关闭</button><div class="scroll"><img id="large" alt="PL 与 BT 的 corner 图放大视图"></div></dialog><script>
const cases=ENTRIES,select=document.getElementById('case'),image=document.getElementById('image');cases.forEach((c,i)=>{const o=document.createElement('option');o.value=i;o.textContent='PL vs '+c.label;select.append(o)});function draw(){const c=cases[+select.value];image.src=c.image;document.getElementById('png').href=c.image;document.getElementById('png').download=c.file;document.getElementById('audit').href=c.audit_data;document.getElementById('audit').download=c.audit}select.onchange=draw;image.onclick=()=>{document.getElementById('large').src=image.src;document.getElementById('viewer').showModal()};document.getElementById('close').onclick=()=>document.getElementById('viewer').close();draw();</script></html>'''.replace('ENTRIES',json.dumps(entries,ensure_ascii=False))
    (B/'index.html').write_text(html)
    out=ROOT/'output/html/BTemu_corner_PL_BT_Park95_20261104.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(html);print(out,flush=True)

def main(source,page_only):
    if not page_only:
        pl,rp=renderer.load(source/'pl_100k.h5',0)
        assets=B/'assets';assets.mkdir(exist_ok=True)
        loaded=[(stem,label,*renderer.load(source/(stem+'.h5'),0)) for stem,label in CASES]
        datasets=[pl,*[a for _,_,a,_ in loaded]]
        shared_limits=renderer.display_limits(np.concatenate(datasets))
        shared_ymax=[]
        for i,lim in enumerate(shared_limits):
            peaks=[float(renderer.gaussian_filter1d(np.histogram(a[:,i],bins=32,range=lim,density=True)[0],.8,mode='reflect').max()) for a in datasets]
            shared_ymax.append(max(peaks)*1.06)
        manifest=dict(source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),selection='All 3000 stored steps x 32 walkers for each model; no additional discard or thinning',parameters=renderer.PARAMETERS,style_name=renderer.STYLE_NAME,shared_coordinate_limits=shared_limits,shared_marginal_ymax=shared_ymax,cases=[])
        for stem,label,bt,rb in loaded:
            out=assets/('PL_vs_'+stem+'_Park95.png')
            audit=renderer.render(pl,bt,out,shared_limits=shared_limits,shared_marginal_ymax=shared_ymax);audit.update(sources={'PL':rp,'BT':rb},output_sha256=renderer.sha(out),label=label)
            out.with_suffix('.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
            assert renderer.sha(source/'pl_100k.h5')==rp['sha256'] and renderer.sha(source/(stem+'.h5'))==rb['sha256']
            manifest['cases'].append(dict(file=out.name,label=label,audit=out.with_suffix('.json').name,sha256=renderer.sha(out)))
            print(label,len(pl),len(bt),flush=True)
        (B/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    page(json.loads((B/'manifest.json').read_text()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=ROOT/'paper/paper_materials/chains_20261104');p.add_argument('--page-only',action='store_true');args=p.parse_args();main(args.source.resolve(),args.page_only)
