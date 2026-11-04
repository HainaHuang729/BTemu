"""Render recorded runtimes with explicit units and evidence boundaries."""
from pathlib import Path
import json,hashlib,html
B=Path(__file__).resolve().parent;D=B/'timing_sources'
def render(en=False):
 manifest=json.loads((D/'manifest.json').read_text())
 for n,record in manifest.items():assert hashlib.sha256((D/n).read_bytes()).hexdigest()==record['sha256']
 t=json.loads((D/'t8_cost_table.json').read_text());m=json.loads((D/'100k_comparison_metrics.json').read_text());hist=json.loads((D/'t2b_matched_kpms_histories.json').read_text())['results'];atlas=json.loads((D/'atlas_index.json').read_text());cache=json.loads((D/'cache_comparison.json').read_text())
 def tr(zh,eng):return eng if en else zh
 def fmt(seconds):
  if seconds is None:return tr('未记录','Not recorded')
  if seconds<.001:return f'{seconds*1e6:.3f} μs'
  if seconds<1:return f'{seconds*1000:.6f} ms'
  return f'{seconds:,.3f} s / {seconds/60:,.3f} min'+(f' / {seconds/3600:,.4f} h' if seconds>=3600 else '')
 rows=[];payload=[]
 def row(zh,eng,seconds,scope_zh,scope_en,source):
  label=tr(zh,eng);scope=tr(scope_zh,scope_en)
  rows.append('<tr>'+''.join(f'<td>{html.escape(str(v))}</td>' for v in [label,fmt(seconds),scope,source])+'</tr>')
  payload.append({'stage':eng,'seconds':seconds,'scope':scope_en,'source':source})
 missing=tr('无实际计时；不从步数或单例外推总时长','No elapsed record; no total extrapolated from counts or single-run timings')
 def absent(zh,enlabel,scope=''):
  row(zh,enlabel,None,scope or missing,scope or missing,'—')
 absent('参数设计与训练数据生成','Parameter design and training-data generation')
 absent('数据筛选、入库与预处理','Selection, admission and preprocessing')
 absent('旧 65k 模型训练','Earlier 65k-model training')
 row('新 100k 模型：报告运行耗时','100k model: reported run elapsed',m['seconds'],'JSON seconds 字段；约 13.2392 h。未定义逐 seed、训练/验证分摊和硬件配置；不是 GPU-hours。','JSON seconds field: 13.2392 h. Per-seed allocation, training/validation split and hardware are unspecified; not GPU-hours.','100k_comparison_metrics.json')
 absent('新模型逐 seed 训练','100k training by individual seed')
 absent('512 条旧模型指标复算','Reconstruction of the 512-history older-model metrics')
 absent('10k 开发验证、tau 与似然指标评估','10k development validation, optical-depth and likelihood evaluation')
 absent('T7 128×8 历史 IC 审计','T7 128×8 history IC audit')
 row('历史模拟器预测：32 节点','Historical predictor call: 32 history nodes',t['emulator_mean_prediction_seconds_per_sample_32_nodes'],'T8 报告 / 每样本；字段名 mean_prediction。来源注明模拟器计时为 4 threads、batch=1。','T8 report / sample; source field mean_prediction. Emulator timing note: 4 threads, batch=1.','t8_cost_table.json')
 row('历史五模型平均预测','Historical five-model prediction',t['emulator_ensemble_of_5_seconds_per_sample'],'T8 报告 / 每样本；不包含已证实的完整 LF+tau+xHI 似然成本。','T8 report / sample; not a verified complete LF+tau+xHI likelihood cost.','t8_cost_table.json')
 row('历史 exact 21cmFAST 单例','Historical exact 21cmFAST realization',t['exact_21cmfast_wall_seconds_median'],'T8 报告的单例 wall-time 中位数；生产台账原始计时未在此复算。','T8 reported median realization wall time; original production-ledger timing is not reconstructed here.','t8_cost_table.json')
 absent('LF provider 与 tau 后处理单独计时','Separate exact LF and optical-depth postprocessing')
 for label,key in [('Exact','exact_chain_seconds_per_iteration'),('Emulator 6D','emulator_chain_seconds_per_iteration_6d'),('Emulator 8D','emulator_chain_seconds_per_iteration_8d')]:
  row('历史 '+label+' 链每迭代',label+' historical chain iteration',t[key],'T8 历史报告 / iteration；不是每 walker、每 likelihood 调用或新 100k 链计时。','T8 historical report / iteration; not per walker, likelihood call or new 100k-model chain.','t8_cost_table.json')
 for label in ['kp10 / ms2.5','kp1 / ms1.5','kp5 / ms1.5','kp10 / free MS (7D)']:
  row('新模型链：'+label,'100k-model chain: '+label,None,'报告 3,000 步、16 processes；没有总耗时或每步计时。','Reported 3,000 steps and 16 processes; no elapsed or per-step timing.','RESULTS_20261104.md')
 absent('历史 corner 链总耗时（6D / 8D / exact200）','Total elapsed for archived corner chains (6D / 8D / exact200)')
 absent('T3 观测组合运行（LF / LF+tau / LF+tau+xHI）','T3 observation-combination runs (LF / LF+tau / LF+tau+xHI)')
 absent('完整 LF+tau+xHI 单次似然','Complete LF+tau+xHI likelihood call')
 absent('PS 训练、phase60 封存测试、IC8 pilot','PS training, phase60 sealed test and IC8 pilot')
 absent('PS+LF 联合采样','PS+LF joint sampling')
 absent('图表生成、论文编译与 HTML 整理','Figure generation, manuscript compilation and HTML assembly')
 headers=tr(['步骤','耗时','计量口径与范围','来源'],['Step','Recorded duration','Unit and scope','Source'])
 def table(headers,body):return '<div class="table-wrap timing-table"><table><thead><tr>'+''.join('<th>'+v+'</th>' for v in headers)+'</tr></thead><tbody>'+body+'</tbody></table></div>'
 full_workflow=table(headers,''.join(rows))
 compact=[]
 for item in payload:
  if item['seconds'] is None:continue
  # Original row labels are already localized; retain them from the rendered row.
  original=rows[payload.index(item)]
  label=original.split('<td>')[1].split('</td>')[0]
  unit=tr('每迭代（历史）','per iteration (historical)') if 'iteration' in item['stage'] else tr('每样本（历史）','per sample (historical)') if 'predict' in item['stage'].lower() else tr('单例中位数（历史）','median realization (historical)') if 'realization' in item['stage'] else tr('报告运行总时长','reported run elapsed')
  compact.append('<tr><td>'+label+'</td><td>'+fmt(item['seconds'])+'</td><td>'+unit+'</td></tr>')
 summary=table(tr(['步骤','耗时','口径'],['Step','Duration','Unit']),''.join(compact))
 hr=[]
 for label,r in hist.items():
  text=tr('16 threads；32 节点 coeval；计时含配置、模拟及 xH_box 均值提取。','16 threads; 32-node coeval calculation, including configuration, simulation and xH_box mean extraction.')
  if label=='PL reference':text+=tr(' 来源所称 PL 的身份未确认；只记录计时。',' Source-labelled PL identity is unverified; timing only.')
  hr.append('<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in [label,fmt(r['seconds']),text])+'</tr>')
 historytable=table(tr(['固定天体物理运行','单次记录耗时','范围'],['Fixed-astrophysics run','Recorded elapsed','Scope']),''.join(hr))
 # Keep each cache case, including numerically discrepant modes.
 cr=[]
 for mode in cache['modes']:
  for case in mode.get('cases',[]):
   if 'seconds' not in case:continue
   cr.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [mode['id'],case.get('point',''),case.get('index',''),fmt(case['seconds']),case.get('science_status',case.get('status',''))])+'</tr>')
 cachetable=table(tr(['缓存模式','点','序号','记录耗时','数值一致性状态'],['Cache mode','Point','Index','Recorded elapsed','Numerical-agreement status']),''.join(cr))
 ar=[];atlasrecords=[]
 for group in ['inventory','pl_inventory']:
  for r in atlas.get(group,[]):
   sec=r.get('summary',{}).get('elapsed_seconds')
   if sec is None:continue
   atlasrecords.append({'group':group,'run_id':r.get('run_id',r.get('pl_id')),'seconds':sec})
   ar.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [group,r.get('run_id',r.get('pl_id')),fmt(sec)])+'</tr>')
 atlastable=table(tr(['历史类别','运行标识','报告耗时'],['Archive group','Run ID','Reported elapsed']),''.join(ar))
 data={'workflow':payload,'coeval_histories':hist,'cache_comparison':cache,'atlas_timings':atlasrecords,'source_manifest':manifest,'scope':'Mixed historical/new reported timings and per-call/per-iteration units; no end-to-end sum or speedup inferred'}
 # Avoid embedding full history arrays in the timing download.
 data['coeval_histories']=[{'label':k,'seconds':v['seconds']} for k,v in hist.items()]
 title=tr('各步骤耗时与运行记录','Runtime by step and available run records')
 intro=tr('按实际记录列出整个工作流。新模型耗时、历史单例与每迭代计时分别标注；缺失项目保留为空，不从步数估算。','The workflow is listed with the timing records currently available. New-model elapsed time, historical per-realization costs and per-iteration costs are labelled separately. Missing durations are not inferred from step counts.')
 warning=tr('各项存在不同硬件、样本数、并行度和计时范围，部分记录互相重叠，不能相加得到项目总耗时。T8 的网络预测不等于完整似然，历史每步时间也不能套用到新 100k 链。','These records have different hardware, sample counts, parallelism and timing scopes, with possible overlap. They cannot be summed into an end-to-end project duration. T8 network prediction is not the complete likelihood, and historical iteration costs are not assigned to new 100k-model chains.')
 trainingnote=tr('100k 源 JSON 为 47,661.272695 s = 13.2392 h；早期摘要的 13.5 h 与该字段不同。页面采用 JSON 数值，暂不解释为五个 seed 总 GPU 成本。','The 100k source JSON gives 47,661.272695 s = 13.2392 h, differing from the earlier prose value of 13.5 h. The page uses the JSON value without interpreting it as the total GPU cost of five seeds.')
 atlasnote=tr('21cmTB 历史 atlas 的配置为 BOX_LEN=250 Mpc、DIM=768、HII_DIM=256、16 threads，区别于当前 DIM=512/HII_DIM=128。该表不用于估计新模型训练数据成本。','The historical 21cmTB atlas uses BOX_LEN=250 Mpc, DIM=768, HII_DIM=256 and 16 threads, distinct from the current DIM=512/HII_DIM=128 setup. It is not used to estimate the new training-data cost.')
 result=f'<section id="timing"><div class="section-head"><h2>'+tr('耗时','Runtime')+'</h2><div class="actions"><button id="timing-json">'+tr('下载耗时 JSON','Download timing JSON')+'</button></div></div>'+summary
 result+='<p class="small">'+tr('仅列有计时的步骤；各项采用其原始计量口径。','Recorded durations, with their original timing units.')+'</p>'
 result+='<details><summary>'+tr('完整工作流（含未记录项目）','Full workflow, including unrecorded durations')+'</summary>'+full_workflow+'<p class="small">'+warning+'</p><p class="small">'+trainingnote+'</p></details>'
 for name,note,body in [(tr('逐次 coeval 历史计算（6 条记录）','Individual coeval history calculations (6 records)'),tr('其中五条 BT 用于论文；来源标注的 PL 身份仍待核实。','Five BT cases enter the manuscript; the source-labelled PL identity remains unverified.'),historytable),(tr('Exact / cache（15 条计时与 3 条失败记录）','Exact/cache comparison (15 timed cases and 3 failed cases)'),tr('保留数值不一致的模式，不以最快运行宣称加速。','Numerically discrepant modes are retained; the fastest entry is not treated as a valid speedup.'),cachetable),(tr(f'历史 21cmTB atlas（{len(ar)} 条计时）',f'Historical 21cmTB atlas ({len(ar)} timing records)'),atlasnote,atlastable)]:
  result+=f'<details><summary>{name}</summary><p class="small">{note}</p>{body}</details>'
 result+='</section><script type="application/json" id="timing-data">'+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+'</script>'
 return result
