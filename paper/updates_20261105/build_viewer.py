"""Build a compact offline material review, keeping source figures distinct."""
from pathlib import Path
import base64,html,json

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
def embed(p):return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
def download(p,label):
    mime='text/csv' if p.suffix=='.csv' else 'text/plain'
    data='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
    return f'<a href="{data}" download="{p.name}">{html.escape(label)}</a>'

def main():
    audit=json.loads((B/'MATERIAL_AUDIT_20261105.json').read_text())
    order=['pl_100k.h5','kp1_ms1p5_100k.h5','kp5_ms1p5_100k.h5','kp10_ms2p5_100k.h5','kp20_ms2p5_10000.h5','kp10_msfree7d_100k.h5']
    labels=['PL','BT kp1 / MS1.5','BT kp5 / MS1.5','BT kp10 / MS2.5','BT kp20 / MS2.5','BT kp10 / free MS (7D)']
    rows=[]
    for name,label in zip(order,labels):
        c=audit['chains'][name];s=c['summary'];rows.append(f'<tr><td>{label}</td><td>{c["shape"][0]:,} × {c["shape"][1]}</td><td>{c["rows"]:,}</td><td>{c["excluded_nonfinite_log_prob"]}</td><td>{s["ETA_STAR"]["median"]:.4f}</td><td>{s["ALPHA_STAR"]["median"]:.4f}</td></tr>')
    rhat=''.join(f'<tr><td>{name}</td><td>{value:.3f}</td><td>{"> 1.05" if value>1.05 else "≤ 1.05"}</td></tr>' for name,value in audit['reported_joined8']['rhat'].items())
    p=ROOT/'paper/web/corner_pl_bt_20261104/assets/PL_vs_kp20_ms2p5_10000_Park95.png'
    mainplot=embed(p)
    accuracy=embed(ROOT/'paper/paper_materials/figures_20261105/accuracy_and_marginals.png')
    joined=embed(ROOT/'paper/paper_materials/corners_20261104/corner_joint_kpms8_joined.png')
    profiles=embed(ROOT/'paper/paper_materials/particle_profiles_20261105/radial_profiles_particles_paperstyle.png')
    links=''.join(download(B/name,label) for name,label in [('BTEMU_WORKING_OUTLINE_20261105.md','整理后的英文骨架'),('REMAINING_MATERIALS_20261105.md','待补材料（按优先级）'),('CLAIM_RECONCILIATION_20261105.md','论断核对记录'),('CHAIN_SUMMARIES_20261105.csv','完整参数统计 CSV'),('MATERIAL_AUDIT_20261105.json','来源与核查 JSON')])
    text='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><link rel="icon" href="data:,"><title>BTemu 新材料 · 2026-11-05</title><style>
*{box-sizing:border-box}body{margin:0;background:#f2f4f6;color:#263b4c;font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1380px;margin:0 auto;background:white;padding:36px 48px 60px}h1{font-size:30px;margin:0 0 8px}h2{font-size:22px;margin:36px 0 12px;padding-top:20px;border-top:1px solid #d9e1e7}h3{font-size:17px;margin-bottom:8px}p{max-width:85ch;margin:8px 0;color:#536675}nav{display:flex;gap:25px;margin:22px 0}a{color:#315f80}table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}th,td{padding:9px 13px;border-bottom:1px solid #e1e7ec;text-align:left}th{background:#f0f4f7;font-weight:600}td:not(:first-child){white-space:nowrap}.twocol{display:grid;grid-template-columns:1.35fr 1fr;gap:32px}.key{background:#edf4f7;border-left:3px solid #315f80;padding:12px 18px;max-width:none}figure{margin:20px 0;background:white}figure img{width:100%;height:auto;display:block;cursor:zoom-in}figcaption{font-size:13px;color:#667785;margin:9px 0}.downloads{display:flex;flex-wrap:wrap;gap:14px 25px;padding:16px 0}details{border-bottom:1px solid #d9e1e7;padding:12px 0}summary{cursor:pointer;font-weight:600}code{font-size:13px}dialog{width:95vw;height:95vh;max-width:none;border:1px solid #a9b7c2;padding:15px}dialog::backdrop{background:#17202b99}.scroll{overflow:auto;height:calc(100% - 50px)}dialog img{max-width:100%;height:auto;display:block;margin:auto}button{font:inherit;padding:6px 15px;border:1px solid #b4c2cc;background:white;border-radius:4px;cursor:pointer}
</style><main><h1>BTemu 新材料整理</h1><p>2026-11-05 · BTemu 27b03de：8 个新增文件。21cmTB 09227c7：无新提交。</p><nav><a href="#samples">样本核查</a><a href="#kp20">新 kp20 对照</a><a href="#joint">8D 诊断</a><a href="#figures">新增原图</a><a href="#paper">论文与待补材料</a></nav>
<p class="key"><strong>本次可用：</strong>kp20/MS2.5 的 10,000 步原始链、重算样本统计、PL/BT 四组统一对照。<strong>本次修正：</strong>8D JSON 的最大 Rhat 是 1.258；少量初始零概率行已从统计与重绘中剔除。</p>
<section id="samples"><h2>原始链与实际留样</h2><table><thead><tr><th>计算</th><th>步数 × walkers</th><th>有限 log_prob 行数</th><th>排除行数</th><th>ETA_STAR 中位数</th><th>ALPHA_STAR 中位数</th></tr></thead><tbody>ROWS</tbody></table><p>统计使用全部有限 log_prob 行，未额外推定 burn-in。原始 HDF5 保持不变。PL、固定谱和自由 MS 的 6 个可读源文件均已记录哈希。</p></section>
<section id="kp20"><h2>新增：PL 对 BT kp20 / MS2.5</h2><p>BT 蓝色实线与单层灰色填色；PL 橙色虚线。两组分别积分至 95% 样本密度区域，对角数字为中位数及 95% 分位区间。右上角留空。</p><p><a href="BTemu_corner_PL_BT_Park95_20261104.html">打开四组切换图集：kp1、kp5、kp10、kp20</a></p><figure><img src="MAINPLOT" alt="PL 与 kp20 BT 的统一 Park 风格叠加"><figcaption>kp20：320,000 行中保留 319,997 行；PL：96,000 行中保留 95,942 行。四张对照共用坐标和一维纵向尺度。</figcaption></figure></section>
<section id="joint"><h2>拼接 8D 链：报告值与实际问题</h2><div class="twocol"><div><p>源 JSON 报告 16,018 步 × 32 walkers。论文骨架把 KP 的 1.084 写成了全参数最高值；实际最高为 ETA_STAR=1.258，另有 ALPHA_STAR=1.178、M_TURN=1.082。</p><p>拼接原始链与诊断定义尚未导出。本次将数值列为来源报告，不据宽分布直接写成“谱参数没有约束”。</p></div><table><thead><tr><th>参数</th><th>报告 Rhat</th><th>与 1.05 对照</th></tr></thead><tbody>RHAT</tbody></table></div></section>
<section id="figures"><h2>新增来源图</h2><details><summary>模型准确率与 KP/MS 边缘分布</summary><figure><img src="ACCURACY" alt="上游准确率与边缘分布原图"><figcaption>上游 PNG；truth/prediction 数组和评估成员待导出。图内残差 q95=0.0032 的定义尚未附，不能直接与 trajectory RMSE q95=0.00556364 对照。</figcaption></figure></details><details><summary>16,018 步联合链 corner 原图</summary><figure><img src="JOINED" alt="上游联合链 corner 原图"><figcaption>与报告诊断一起归档；原始联合样本尚未收到，因此本页保留来源图。</figcaption></figure></details></section>
<section id="paper"><h2>论文主线与材料入口</h2><p><strong>问题：</strong>小尺度物质谱与星系参数都影响再电离历史。<strong>动机：</strong>联合变化需要重复计算历史。<strong>方法：</strong>BTemu 近似 32 节点历史，并核对历史、派生似然和采样。<strong>结果：</strong>100k 开发验证摘要及上传的固定谱样本比较。<strong>结论：</strong>把历史近似的准确性与自由谱信息检验分开完成。</p><div class="downloads">LINKS</div><table><thead><tr><th>优先级</th><th>下一份关键材料</th></tr></thead><tbody><tr><td>P0</td><td>16,018 步 8D 原始链、留样和诊断定义；完整模型/likelihood 身份</td></tr><tr><td>P0</td><td>100k 模型逐样本 truth / predictions / IDs，指标和聚合定义</td></tr><tr><td>P0</td><td>输入谱与 native 记录；同目标的 exact 对照与已有 IC family 数组</td></tr><tr><td>P1</td><td>当前样本的 LF、xHI、tau 预测和计时 scope；可读 PS+LF 文件</td></tr></tbody></table></section>
<section><h2>分开归档的进展</h2><p>PS10D 来源快照报告 60 个 NPZ、约 150–200 个参数点，并限制 KP≥1、MS≥1.5。生产进度与已验证的历史模型结果分开记录。上传的 2,108 字节 PS+LF HDF5 当前无法读取，需完整导出。</p><details><summary>粒子径向剖面：结构形成论文材料</summary><p>按结构形成论文归档；当前仅收到来源图，重画需半径、密度、粒子数、中心和单位定义。</p><figure><img src="PROFILES" alt="结构形成论文的粒子径向剖面来源图"></figure></details></section></main><dialog id="viewer"><button id="close">关闭</button><div class="scroll"><img id="large" alt="材料图放大"></div></dialog><script>document.querySelectorAll('figure img').forEach(im=>im.onclick=()=>{document.getElementById('large').src=im.src;document.getElementById('viewer').showModal()});document.getElementById('close').onclick=()=>document.getElementById('viewer').close();</script></html>'''
    for key,value in {'ROWS':''.join(rows),'RHAT':rhat,'MAINPLOT':mainplot,'ACCURACY':accuracy,'JOINED':joined,'PROFILES':profiles,'LINKS':links}.items():text=text.replace(key,value)
    (B/'index.html').write_text(text.replace('href="BTemu_corner_PL_BT_Park95_20261104.html"','href="../web/corner_pl_bt_20261104/index.html"'))
    out=ROOT/'output/html/BTemu_updates_20261105.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text);print(out)

if __name__=='__main__':main()
