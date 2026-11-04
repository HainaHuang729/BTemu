"""Five independently identified designs, rendered from the archived original arrays.

Usage: /usr/bin/python3 build.py --source /path/to/overleaf-btemu/paper/reproduction --atlas /path/to/21cmTB
Only preview PNGs are authored. Accepted manuscript assets are never overwritten.
"""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, os, secrets, shutil, subprocess, sys

B = Path(__file__).resolve().parent
ROOT = B.parents[2]
OUT = ROOT / 'output/html'
WORK = ROOT / 'tmp/figure_directions_20261104'
SCHEMES = [
 dict(name='经典黑白', en='Monochrome journal', palette=['#161616','#343434','#777777','#999999','#575757'], density=['#ffffff','#f2f2f2','#cecece','#999999','#5c5c5c','#181818'], font='STIXGeneral', math='stix', frame='box', width=1.25, fill=.08, spacing=.14, key=.60, grid=False, desc='黑白印刷取向；完整细边框、衬线字体，以灰阶与线型建立层次。'),
 dict(name='冷色精密', en='Teal precision', palette=['#173343','#007B83','#526DA0','#748B49','#308B71'], density=['#ffffff','#eaf5f4','#bee1dc','#74bcb5','#318b8b','#14545e'], font='DejaVu Sans', math='dejavusans', frame='open', width=1.55, fill=.16, spacing=.085, key=.60, grid=True, desc='青绿密度、无衬线字体、开放坐标轴；紧凑排列与轻横向导线。'),
 dict(name='蓝橙对照', en='Blue–orange contrast', palette=['#253649','#2465A2','#D4762A','#9D822D','#258B86'], density=['#ffffff','#edf3fa','#bcd2ed','#739fce','#3b70ac','#183f72'], font='DejaVu Sans', math='dejavusans', frame='bracket', width=1.85, fill=.12, spacing=.20, key=.59, grid=False, desc='蓝色主体、橙色比较项；更宽面板间距，较强线重和更醒目的点标记。'),
 dict(name='紫色层次', en='Plum editorial', palette=['#302A41','#72558C','#B15D70','#A6843D','#438783'], density=['#ffffff','#f4eff7','#ddcde8','#b395cb','#8865a5','#50336e'], font='STIXGeneral', math='stix', frame='open', width=1.65, fill=.24, spacing=.13, key=.60, grid=False, desc='紫色连续密度与莓红比较项；加重边缘分布、衬线排版与柔和轴线。'),
 dict(name='极简线稿', en='Minimal technical', palette=['#202B37','#285777','#9C5348','#8C7839','#4B7971'], density=['#ffffff','#f6f8fa','#e2e8ef','#aebfce','#718da7','#355774'], font='DejaVu Sans', math='dejavusans', frame='bottom', width=1.05, fill=0.0, spacing=.16, key=.60, grid=True, desc='淡密度与无填充边缘直方图；细线、短刻度、点状导线，突出数据结构。'),
]
SCRIPTS = ['render_new_chain_corners.py','render_exact200_corner.py','render_paper_figures.py','review_revision.py','audit_material_update.py','audit_t3_update.py']
FIGURES = [
 ('fig11_btemu_corner6_5000','6D corner'),
 ('fig12_btemu_corner8_5568','8D corner'),
 ('fig13_exact_corner6_200','Exact 200-step corner'),
 ('fig8_21cmtb_corner_fixed8','21cmTB 8D corner'),
 ('fig9_21cmtb_corner_free9','21cmTB 9D corner'),
 ('fig15_kpms_focus','谱参数 / Spectrum focus'),
 ('fig17_obs_combinations','观测组合 / Observation combinations'),
 ('fig16_fixed_astro_bt_histories','固定星系参数历史 / Fixed-galaxy histories'),
 ('fig5_21cmtb_histories','历史对照 / Atlas histories'),
 ('fig6_21cmtb_lf_grid','LF 网格 / LF grid'),
 ('fig7_21cmtb_lf_fits','LF 拟合 / LF fits'),
 ('fig14_validation','模型验证 / Model validation'),
 ('fig10_21cmtb_diagnostics','链诊断 / Chain diagnostics'),
]

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare(source, scheme):
    spec = dict(scheme, nonce=secrets.token_hex(16), source_style='academic-v3', preview_only=True)
    h = hashlib.sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    spec['hash'] = h; spec['id'] = h[:12]
    work = WORK/spec['id']; work.mkdir(parents=True)
    for p in source.glob('*.py'): shutil.copy2(p, work/p.name)
    for name in ['data','paper_materials']: shutil.copytree(source/name, work/name)
    (work/'chains').symlink_to(source/'chains', target_is_directory=True)
    (work/'SOURCE_REVISION.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip())
    old=['#243447','#315E8B','#BE624F','#AA843B','#278579']
    for p in work.glob('*.py'):
        s=p.read_text()
        for before,after in zip(old,spec['palette']): s=s.replace(before,after)
        p.write_text(s)
    p=work/'plot_design.py'; s=p.read_text()
    s=s.replace("['#ffffff','#edf3f6','#bdd2de','#6c9cad','#356b89','#203e63']", repr(spec['density']))
    s=s.replace("for ext in ['png','pdf']:", "for ext in ['png']:")
    s=s.replace('wspace=.105,hspace=.105',f"wspace={spec['spacing']},hspace={spec['spacing']}")
    s=s.replace('alpha=.13',f"alpha={spec['fill']}").replace('alpha=.10',f"alpha={spec['fill']}")
    s=s.replace('x=.60',f"x={spec['key']}")
    p.write_text(s)
    p=work/'figure_style.py'
    s=p.read_text().replace("'font.family':'STIXGeneral'",f"'font.family':{spec['font']!r}").replace("'mathtext.fontset':'stix'",f"'mathtext.fontset':{spec['math']!r}")
    # A second styling pass changes artists only, after the common layout renderer.
    s += '\n\n_original_polish = polish\n'
    s += 'def polish(fig):\n _original_polish(fig)\n'
    s += f' for ax in fig.axes:\n  if not ax.get_visible(): continue\n  ax.tick_params(which="major",width=.6,pad=3)\n  for line in ax.lines:\n   if line.get_linewidth()>1: line.set_linewidth({spec["width"]})\n'
    if spec['frame']=='box':
        s+='  if ax.axison and len(ax.get_yticks())>0:\n   for sp in ax.spines.values(): sp.set_visible(True); sp.set_color("#B4B4B4"); sp.set_linewidth(.55)\n'
    elif spec['frame']=='bracket':
        s+='  ax.spines["bottom"].set_color("#506479"); ax.spines["left"].set_color("#506479")\n  for line in ax.lines:\n   if line.get_marker() not in ["None", "", None]: line.set_markersize(line.get_markersize()*1.15)\n'
    elif spec['frame']=='bottom':
        s+='  ax.spines["left"].set_visible(False)\n  ax.tick_params(axis="y",length=0)\n'
    if spec['grid']:
        s+='  if ax.axison and len(ax.get_yticks())>0:\n   ax.grid(axis="y",color="#DCE3E8",linewidth=.45,linestyle=":"); ax.set_axisbelow(True)\n'
    p.write_text(s)
    (work/'design.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
    return spec,work

def render(task,atlas):
    spec,work=task
    env=dict(os.environ,MPLBACKEND='Agg',PYTHONDONTWRITEBYTECODE='1')
    with (work/'render.log').open('w') as log:
        for script in SCRIPTS:
            cmd=['/usr/bin/python3',str(work/script)]
            if script=='render_paper_figures.py':cmd.append(str(atlas))
            p=subprocess.run(cmd,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
            if p.returncode:raise RuntimeError(f'{spec["id"]}: {script} failed; see {work}/render.log')
    target=OUT/'figure_directions_20261104'/spec['id'];target.mkdir(parents=True,exist_ok=True)
    for name,_ in FIGURES: shutil.copy2(work/'figures'/(name+'.png'),target/(name+'.png'))
    shutil.copytree(target,B/'assets'/spec['id'],dirs_exist_ok=True)
    spec['outputs']={name:digest(target/(name+'.png')) for name,_ in FIGURES}
    # Identical statistics and histogram membership across the variants.
    stats={}
    for f in ['new_chain_audit_20261029.json','exact200_corner_audit_20261029.json','validation_recomputed_20261029.json']:
        d=json.loads((work/'data'/f).read_text())
        def strip(v):
            if isinstance(v,dict):return {k:strip(x) for k,x in v.items() if k not in ['outputs_sha256','figure_outputs_sha256','figure_style']}
            if isinstance(v,list):return [strip(x) for x in v]
            return v
        stats[f]=strip(d)
    spec['statistics_sha256']=hashlib.sha256(json.dumps(stats,sort_keys=True).encode()).hexdigest()
    print(f'{spec["id"]} {spec["name"]}: 13 original figures rendered',flush=True)
    return spec

def page(specs):
    options=''.join(f'<option value="{n}">{t}</option>' for n,t in FIGURES)
    data=json.dumps(specs,ensure_ascii=False)
    html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>原图 · 五个设计方向</title><style>
*{box-sizing:border-box}body{margin:0;background:#eef1f4;color:#23313e;font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}header{padding:30px 4vw 20px;background:white;border-bottom:1px solid #d8e0e6}h1{margin:0;font-size:27px;font-weight:600}p{margin:7px 0;color:#586675}.tools{position:sticky;top:0;z-index:2;background:#ffffffed;padding:15px 4vw;display:flex;align-items:center;gap:12px;border-bottom:1px solid #d8e0e6;backdrop-filter:blur(12px)}select,button{font:inherit;border:1px solid #b8c4ce;border-radius:5px;padding:8px 13px;background:white;color:#263a4c;cursor:pointer}button[aria-pressed=true]{background:#263a4c;color:white}.grid{padding:24px 4vw;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;align-items:start}.grid.single{grid-template-columns:1fr;max-width:1400px;margin:auto}article{background:white;border:1px solid #d8e0e6}article header{padding:17px 21px}h2{font-size:20px;margin:0}code{font:13px ui-monospace,monospace;color:#657586}article p{font-size:13px;min-height:40px}img{display:block;width:100%;height:auto}.image{border:0;padding:0;background:white;border-radius:0;width:100%;cursor:zoom-in}footer{display:flex;justify-content:space-between;padding:10px 21px;border-top:1px solid #edf0f3}a{color:#315e80}dialog{border:1px solid #a6b3be;padding:15px;width:94vw;max-width:none;height:94vh}dialog::backdrop{background:#17202b99}dialog img{width:auto;max-width:100%;margin:auto}.scroll{height:calc(100% - 55px);overflow:auto}small{color:#697988}#single{display:none}
</style><header><h1>原图 · 五个设计方向</h1><p>选择同一张原图，对照五套设计。每套覆盖 13 张图；数据、留样、分箱及统计摘要一致。</p></header>
<div class="tools"><label for="figure">原图</label><select id="figure">OPTIONS</select><button id="compare" aria-pressed="true">五套对照</button><button id="one" aria-pressed="false">单套大图</button><select id="single"></select><small>点击原图可放大</small></div><main class="grid" id="grid"></main><dialog id="zoom"><button id="close">关闭</button><div class="scroll"><img id="large" alt=""></div></dialog><script>
const designs=DATA;const figure=document.getElementById('figure'),grid=document.getElementById('grid'),single=document.getElementById('single');let solo=false;
designs.forEach(d=>{const o=document.createElement('option');o.value=d.id;o.textContent=d.name+' · '+d.id;single.append(o)});
function draw(){grid.classList.toggle('single',solo);grid.replaceChildren();designs.filter(d=>!solo||d.id===single.value).forEach(d=>{const a=document.createElement('article'),url='figure_directions_20261104/'+d.id+'/'+figure.value+'.png';a.innerHTML='<header><h2>'+d.name+'</h2><code>'+d.id+'</code><p>'+d.desc+'</p></header><button class="image" aria-label="放大 '+d.name+'"><img loading="lazy" src="'+url+'" alt="'+d.name+' '+figure.selectedOptions[0].textContent+'"></button><footer><span>'+d.en+'</span><a href="'+url+'" download>下载原图 PNG</a></footer>';a.querySelector('button').onclick=()=>{document.getElementById('large').src=url;document.getElementById('zoom').showModal()};grid.append(a)})}
figure.onchange=single.onchange=draw;document.getElementById('compare').onclick=()=>{solo=false;mode()};document.getElementById('one').onclick=()=>{solo=true;mode()};function mode(){single.style.display=solo?'inline-block':'none';document.getElementById('compare').setAttribute('aria-pressed',!solo);document.getElementById('one').setAttribute('aria-pressed',solo);draw()}document.getElementById('close').onclick=()=>document.getElementById('zoom').close();draw();</script></html>'''.replace('OPTIONS',options).replace('DATA',data)
    OUT.mkdir(parents=True,exist_ok=True)
    html=html.replace('原图 · 五个设计方向','Corner 图 · 五个设计方向')
    html=html.replace('选择同一张原图，对照五套设计。每套覆盖 13 张图；数据、留样、分箱及统计摘要一致。','以同一份 6D 链为例比较五套 corner 设计。可切换 8D、exact 200 步和 21cmTB；留样与分箱一致。')
    html=html.replace('<label for="figure">原图</label>','<label for="figure">Corner / 原图</label>')
    html=html.replace('<small>点击原图可放大</small>', '<button data-quick="fig11_btemu_corner6_5000">6D</button><button data-quick="fig12_btemu_corner8_5568">8D</button><button data-quick="fig13_exact_corner6_200">Exact 200</button><small>点击放大</small>')
    html=html.replace('figure.onchange=single.onchange=draw;', 'document.querySelectorAll("[data-quick]").forEach(b=>b.onclick=()=>{figure.value=b.dataset.quick;draw()});figure.onchange=single.onchange=draw;')
    dest=OUT/'BTemu_five_designs_20261104.html';dest.write_text(html)
    (B/'index.html').write_text(html.replace('figure_directions_20261104/','assets/'))
    return dest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--atlas',type=Path,required=True);args=parser.parse_args()
    source=args.source.resolve();atlas=args.atlas.resolve()
    inputs={str(p.relative_to(source)):digest(p) for folder in ['chains','data','paper_materials'] for p in (source/folder).rglob('*') if p.is_file()}
    tasks=[prepare(source,s) for s in SCHEMES]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: specs=list(pool.map(lambda task:render(task,atlas),tasks))
    assert len({s['statistics_sha256'] for s in specs})==1,'Variant statistics differ'
    assert all(digest(source/p)==sha for p,sha in inputs.items()),'Canonical inputs changed'
    manifest={'source':str(source),'canonical_input_sha256':inputs,'statistics_identical_across_all_five':True,'figures':FIGURES,'designs':specs}
    (B/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(page(specs),flush=True)
