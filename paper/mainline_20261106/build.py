# -*- coding: utf-8 -*-
from pathlib import Path
import base64,json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[1]
images=[ROOT/'paper/web/corner_pl_bt_20261104/assets/PL_vs_kp1_ms1p5_100k_Park95.png',ROOT/'paper/analysis_kpms_20261106/kp_ms_marginal_prior.png']
a=json.loads((ROOT/'paper/analysis_kpms_20261106/analysis.json').read_text())
def img(p):return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
metrics=json.loads((ROOT/'paper/paper_materials/metrics/100k_comparison_metrics.json').read_text())
s='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>BTemu · 论文主线</title><link rel="icon" href="data:,"><style>body{margin:0;background:#f4f6f7;color:#293f4e;font:16px/1.75 system-ui}main{width:1060px;margin:50px auto}h1{font-size:34px;line-height:1.45;max-width:950px}h2{font-size:23px}section{padding:28px 32px;background:white;border:1px solid #dce3e7;margin:24px 0}img{width:100%;display:block}table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}td,th{text-align:left;padding:13px 10px;border-bottom:1px solid #e0e6e9}a{color:#285e7a}.eyebrow,.caption{color:#647b88;font-size:14px}.metric{font:32px STIXGeneral,Georgia,serif;color:#285e7a}.summary{max-width:940px}li{margin:10px 0}</style><main><div class="eyebrow">BTEMU · MAIN LINE · 2026-11-06</div><h1>允许星系形成参数变化后，<br>再电离观测能把 kₚ、mₛ 限制到什么范围？</h1><p class="summary">BTemu 预测再电离历史，使物质谱与星系参数能够联合采样。全文依次呈现预测精度、星系参数随谱变化，以及谱参数的边缘后验。</p><section><h2>1 · 预测精度</h2><div class="metric">RMSE 中位数 0.000850668 · q₉₅ 0.00556364</div><p>100k 模型报告的历史误差。正文保留一张精度图与简表，验证数组补齐后复算。</p></section><section><h2>2 · 星系参数随物质谱变化</h2><p>只保留一个代表性对照：PL 与 BT（kₚ=1，mₛ=1.5）。六个星系参数的分布用于说明联合推断的必要性。</p><img alt="PL and BT representative six parameter comparison" src="IMAGE1"><p class="caption">同一 100k 模型的有限链比较。PL 为橙色虚线，BT 为蓝色实线。其余固定谱对照归入补充材料。</p></section><section><h2>3 · kₚ、mₛ 的边缘分布</h2><img alt="KP MS marginal distributions and uniform prior reference" src="IMAGE2"><table><tr><th>参数</th><th>中位数</th><th>95% 等尾区间</th><th>参考均匀先验</th></tr>ROWS</table><p>mₛ 的范围接近参考先验；kₚ 的变化主要在低值端。当前数值来自 600 步联合链的后 300 步，属于初步样本统计。最终区间由长链与独立运行检验确定。</p><p class="caption">蓝色边缘分布，橙色先验。先验来自归档参数表；本次实际配置随完整采样补齐。</p></section><section><h2>接下来只做两件事</h2><ol><li>完成同一 100k 模型的 8D 联合推断：延长现有链，增加三组独立初值运行。</li><li>补齐同一模型的验证数组，复算历史与似然相关误差。</li></ol><p>其他固定参数链、旧模型、exact 短链、T7、耗时与采样诊断保留在补充材料和复现归档。</p><p><a href="MAINLINEDATA" download="MAINLINE.md">下载主线提纲</a> · <a href="BTemu_kpms_posterior_20261106.html">采样细节与任务</a></p></section></main></html>'''
rows=''
for r in a['intervals']:
 if r['selection']=='last300':
  name='kₚ / h Mpc⁻¹' if r['parameter']=='KP_h_Mpc' else 'mₛ'
  rows+=f'<tr><td>{name}</td><td>{r["median"]:.3f}</td><td>[{r["q025"]:.3f}, {r["q975"]:.3f}]</td><td>[{r["prior_low"]}, {r["prior_high"]}]</td></tr>'
s=s.replace('IMAGE1',img(images[0])).replace('IMAGE2',img(images[1])).replace('ROWS',rows).replace('MAINLINEDATA','data:text/plain;base64,'+base64.b64encode((ROOT/'paper/MAINLINE.md').read_bytes()).decode())
(B/'index.html').write_text(s.replace('href="BTemu_kpms_posterior_20261106.html"','href="../analysis_kpms_20261106/index.html"'))
out=ROOT/'output/html/BTemu_mainline_20261106.html';out.write_text(s)
(B/'SELECTION.json').write_text(json.dumps(dict(selected_images=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in images],source_files_preserved=True,manuscript_tex_changed=False,primary_model='100k',result_groups=3,core_tasks=2),indent=2)+'\n')
print(out)
