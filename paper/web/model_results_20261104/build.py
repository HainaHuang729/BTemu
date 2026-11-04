"""Build a self-contained, offline report from the audited November 4 summaries.
Usage: python build.py [audit.json] [output.html]
"""
from pathlib import Path
import sys,json,io,re,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else B/'audit.json'
output=Path(sys.argv[2]) if len(sys.argv)>2 else B/'index.html'
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
html=(B/'template.html').read_text().replace('@@FIXED_SVG@@',fixed_svg).replace('@@VALIDATION_SVG@@',validation_svg).replace('@@METRIC_ROWS@@',metric_rows).replace('@@FIXED_ROWS@@',fixed_rows).replace('@@DATA@@',json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
output.parent.mkdir(parents=True,exist_ok=True);output.write_text(html)
print(json.dumps({'output':str(output),'bytes':output.stat().st_size,'audit_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}))
