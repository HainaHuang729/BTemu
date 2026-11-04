"""Build a self-contained, offline report from the audited November 4 summaries.
Usage: python build.py [audit.json] [output.html]
"""
from pathlib import Path
import sys,json,io,re,hashlib,base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else B/'audit.json'
output=Path(sys.argv[2]) if len(sys.argv)>2 else B/'index.html'
en='--en' in sys.argv
a=json.loads(source.read_text())
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'axes.labelcolor':'#242424','text.color':'#242424','svg.fonttype':'path','savefig.facecolor':'white'})
colors=['#315c83','#aa5145','#a38943'];labels=[r'$\eta_\star$',r'$\alpha_\star$',r'$\log_{10}(M_{\rm turn}/M_\odot)$',r'$\log_{10}f_{{\rm esc},10}$',r'$\alpha_{\rm esc}$']
def svg(fig,name):
 buf=io.StringIO();fig.savefig(buf,format='svg',bbox_inches='tight');plt.close(fig)
 s=buf.getvalue();s=s[s.index('<svg'):];s=re.sub(r'<svg\s','<svg role="img" aria-label="'+name+'" ',s,count=1)
 return s
fig,axes=plt.subplots(1,5,figsize=(13.5,3.1),sharey=True)
for j,ax in enumerate(axes):
 for i,row in enumerate(a['fixed_summaries']):
  value,spread=row['reported_centers_spreads'][j]
  ax.errorbar(value,2-i,xerr=spread,fmt='o',ms=5,capsize=4,lw=1.5,color=colors[i])
 ax.set_title(labels[j],pad=16,fontsize=13);ax.set_ylim(-.6,2.6);ax.set_yticks([2,1,0]);ax.set_yticklabels(['$k_p=10,\ m_s=2.5$','$k_p=1,\ m_s=1.5$','$k_p=5,\ m_s=1.5$']);ax.grid(axis='x',color='#e2e7ed',lw=.6);ax.tick_params(axis='y',length=0,pad=10);ax.tick_params(axis='x',labelsize=10);ax.locator_params(axis='x',nbins=4)
fig.subplots_adjust(wspace=.4,left=.11,right=.99,bottom=.2,top=.79)
fixed_svg=svg(fig,'固定谱链的五个参数，点为报告中心，横线为未定义覆盖率的报告散布')
fig,axes=plt.subplots(1,2,figsize=(10.8,3.1))
old=a['previous_recomputed'];new=a['new_metrics']
for ax,key,title in zip(axes,['median','q95'],['Trajectory RMSE: median','Trajectory RMSE: 95th percentile']):
 vals=[old['five_model_average'][key],old['seed11'][key],new['trajectory_RMSE_'+('median' if key=='median' else 'q95')]]
 for i,(v,c) in enumerate(zip(vals,['#315c83','#8c97a3','#aa5145'])):
  ax.plot(v,2-i,'o',color=c,ms=6);ax.annotate(f'{v:.6f}',(v,2-i),xytext=(9,0),textcoords='offset points',va='center',fontsize=11)
 ax.axhline(.5,color='#9ba9b5',ls='--',lw=.8);ax.set_yticks([2,1,0]);ax.set_yticklabels(['65k five-model average','65k seed 11','100k reported predictor']);ax.set_title(title,loc='left',pad=14,fontsize=13);ax.set_ylim(-.65,2.6);ax.set_xlim(0,max(vals)*1.45);ax.tick_params(axis='y',length=0);ax.grid(axis='x',color='#e2e7ed',lw=.6);ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0),useMathText=True)
fig.subplots_adjust(wspace=.9,left=.2,right=.98,bottom=.22,top=.79)
validation_svg=svg(fig,'旧模型平均与单seed复算值，以及评估口径尚未对齐的新模型报告值')
metrics=[('轨迹 RMSE 中位数','trajectory_RMSE_median'),('轨迹 RMSE q95','trajectory_RMSE_q95'),('xHI(5.9) 误差：报告 q90','xHI_q90'),('τ 误差：报告 q90','tau_q90'),('ΔlogL_joint：报告 q90','dlogL_q90')]
metric_rows=''.join(f'<tr><th scope="row">{label}</th><td>{new[k]:.9g}</td><td>{"轨迹绝对误差" if "RMSE" in k else "绝对值／符号与后处理定义待补"}</td></tr>' for label,k in metrics)
fixed_rows=''.join('<tr><th scope="row"><span class="dot" style="background:'+colors[i]+'"></span>'+f'kp={row["kp"]}, ms={row["ms"]}'+ '</th>'+''.join(f'<td>{v:.3f} ± {s:.3f}</td>' for v,s in row['reported_centers_spreads'])+'</tr>' for i,row in enumerate(a['fixed_summaries']))
payload={'rows':a['fixed_summaries'],'labels':['η★','α★','log₁₀(Mturn/M☉)','log₁₀ fesc,10','αesc'],'audit':a}
html=(B/('template_en.html' if en else 'template.html')).read_text().replace('@@FIXED_SVG@@',fixed_svg).replace('@@VALIDATION_SVG@@',validation_svg).replace('@@METRIC_ROWS@@',metric_rows).replace('@@FIXED_ROWS@@',fixed_rows).replace('@@DATA@@',json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
if en:
 translations={'固定谱链的五个参数，点为报告中心，横线为未定义覆盖率的报告散布':'Five fixed-spectrum coordinates: reported centres and spreads with unspecified coverage','旧模型平均与单seed复算值，以及评估口径尚未对齐的新模型报告值':'Recomputed older-model average and seed-11 errors, with new reported values under an unmatched evaluation','轨迹 RMSE 中位数':'Trajectory RMSE: median','轨迹 RMSE q95':'Trajectory RMSE: q95','xHI(5.9) 误差：报告 q90':'xHI(5.9) error: reported q90','τ 误差：报告 q90':'Optical-depth error: reported q90','ΔlogL_joint：报告 q90':'Joint log-likelihood difference: reported q90','轨迹绝对误差':'Absolute history error','绝对值／符号与后处理定义待补':'Signed/absolute convention and postprocessing pending'}
 for old,new in translations.items():html=html.replace(old,new)
corner_files=['fig11_btemu_corner6_5000.png','fig12_btemu_corner8_5568.png','fig13_exact_corner6_200.png']
corner_titles=['6D emulator: fixed spectrum','8D emulator: free kp and MS','Exact 6D: 200-step smoke chain'] if en else ['6D 模拟器：固定谱','8D 模拟器：自由 kp 和 MS','Exact 6D：200 步测试链']
corner_captions=[
 'Earlier-model archive: 5,000 stored steps × 32 walkers; last-half steps [2500,5000), 80,000 correlated rows. Six galaxy coordinates at source-attributed kp=10 h Mpc⁻¹, MS=2.5. Ordinary split monitor: 1.0340–1.0535.',
 'Earlier-model archive: 5,568 stored steps × 32 walkers; last-half steps [2784,5568), 89,088 correlated rows. Six galaxy coordinates plus kp and MS. Ordinary split monitor: 1.1136–1.5125.',
 'Exact archive: all 200 stored steps × 32 walkers, 6,400 rows. Fixed kp=10 h Mpc⁻¹, MS=2.5. Source status: smoke-only, unconverged. The earlier T6 moment comparison instead retains its final 100 steps.'
 ] if en else [
 '旧模型归档：5,000 步 × 32 walkers，保留后半段 [2500,5000)，共 80,000 行相关样本。六个星系坐标；来源标注固定 kp=10 h Mpc⁻¹、MS=2.5。普通 split 监测范围：1.0340–1.0535。',
 '旧模型归档：5,568 步 × 32 walkers，保留后半段 [2784,5568)，共 89,088 行相关样本。六个星系坐标加 kp、MS。普通 split 监测范围：1.1136–1.5125。',
 'Exact 归档：保留全部 200 步 × 32 walkers，共 6,400 行。固定 kp=10 h Mpc⁻¹、MS=2.5；来源明确为 smoke-only、未收敛。此前 T6 矩比较采用其最后 100 步。']
heading='Archived corner plots' if en else '已归档的 corner 图'
note='These plots retain the earlier chain selections. Raw chains for the new 100k-model fixed-spectrum runs are not exported, so these are not corner plots of those new runs. Binned densities are descriptive, with no smoothing or credible contours. Independent convergence is not established by splitting interacting walkers.' if en else '图中保留旧链的原始留样。新十万样本模型固定谱运行尚未导出原始链，因此这些并非新运行的 corner 图。分箱密度仅作描述，无平滑或可信轮廓；拆分相互作用的 walkers 不构成独立收敛验证。'
tabs=''.join(f'<button role="tab" data-corner="corner-{i}" aria-controls="corner-{i}" aria-selected="{str(i==0).lower()}">{title}</button>' for i,title in enumerate(corner_titles))
panels=[]
for i,(filename,title,caption) in enumerate(zip(corner_files,corner_titles,corner_captions)):
 path=B/'assets'/filename
 raw=path.read_bytes();url='data:image/png;base64,'+base64.b64encode(raw).decode()
 panels.append(f'<figure class="corner-panel" id="corner-{i}" role="tabpanel"'+(' hidden' if i else '')+f'><h3>{title}</h3><a href="{url}" target="_blank" rel="noopener" aria-label="{title}"><img src="{url}" alt="{title}" loading="lazy"></a><figcaption class="caption">{caption}</figcaption></figure>')
hint='Select a chain above. Click the image to open it at full resolution.' if en else '上方切换链；点击图片可打开原始分辨率。'
html=html.replace('@@CORNERS@@',f'<section id="corners"><h2>{heading}</h2><p class="lead">{note}</p><div class="corner-tabs" role="tablist" aria-label="Corner plots">{tabs}</div>'+''.join(panels)+f'<p class="small">{hint}</p></section>')
close_label='Close full-resolution image' if en else '关闭原图'
html=html.replace('</body>',f'<dialog id="corner-dialog" style="width:96vw;max-width:96vw;height:94vh;border:1px solid #a9b8c8;border-radius:8px;padding:16px"><button onclick="document.getElementById(&quot;corner-dialog&quot;).close()">{close_label}</button><div style="overflow:auto;height:calc(100% - 55px);margin-top:10px"><img id="corner-full-image" alt="" style="max-width:none;width:auto;height:auto"></div></dialog></body>')
output.parent.mkdir(parents=True,exist_ok=True);output.write_text('\n'.join(line.rstrip() for line in html.splitlines())+'\n')
print(json.dumps({'output':str(output),'bytes':output.stat().st_size,'audit_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}))
