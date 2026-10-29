# 21cmTB 网页材料复核：已有内容与论文用途

日期：2026-10-29。对照物理稿 v0.10、BTemu 方法稿 v0.1。21cmTB 源码版本 09227c79dcf466cdcc30520228a8c25d02287aab。

## 结论与对前次清点的修正

网页材料比前次纳入论文的选定导出更丰富。前次使用了旧 LF 主展示快照、部分 atlas 历史、repaired corner/诊断及 PL 参考；未充分利用较晚 LF 选点的重算模拟、同参数 PL 配对和联合样本的观测量预测。

必须区分：
- 2026-09-18 的 lf_main_comparison：25 个模型的旧展示快照，诊断标记全 false。
- 2026-09-26 静态 posterior/catalog：25 个谱模型的来源记录均标记 diagnostic_gate_passed=true，源运行各为 10000–40000 production steps/ensemble。该来源标记未通过本次检查重新认证。
- 每个谱模型选 5 个真实链位置：最高存储 LF 似然点及覆盖点，共 125 个候选。覆盖点按 maximin 选取，不是带后验概率权重的抽样，不能据它们的包络画可信带。
- catalog 的完成状态来自静态快照，不是当前集群实时状态。

因此“旧展示 LF 网格全未通过”准确；将其扩大为“整个库的 LF 来源均未通过”不准确。新来源也不能在缺少原诊断与完整配置时直接写成已独立认证的收敛后验。

## 实际核查范围

主站抓取接口和浏览器打开失败后，直接读取线上页面对应 JSON 与源码：
- 从 GitHub Pages 下载并保存了 34 个清单、诊断及观测量 JSON。
- 从目录指向的 GitHub raw 下载了 23 个可用 LF-best BT JSON、25 个 PL 对照 JSON，共 48 个源文件。
- 25 个 PL JSON 全部通过目录给出的 SHA256 校验。
- 23 个 BT/PL 配对逐一核对八个 astrophysical 参数、BT run ID、84 个 global 红移节点、32 个横截面历史节点与 32×256×256 切片尺寸。
- 未下载三维体数据或切片二进制，也未重跑任何模拟、拟合或 sampler。

完整来源、URL、SHA256 与复算结果见本地 data/21cmtb_web_audit_20261029/。提交到论文项目的紧凑审计保留数据定位和核查结果，不复制约 30 MB 的可重新下载源 JSON。

## 网站材料地图

| 材料 | 已有内容 | 对论文的用途与边界 |
|---|---|---|
| 原始精确图谱 | 55 个成功 BT 模型、32 个 PL 参考；global signal、LF、32 面历史、五种场 | 参数响应与空间物理背景；不能替代 BTemu 的 coeval 训练标签或数值收敛检查 |
| 较晚 LF 样本目录 | 25 个谱模型、125 个候选；46 个 completed、4 个 under_review、1 个 awaiting_validation、4 个 running、70 个 submitted | 真实联合参数位置和来源版本。状态均属静态快照，46 点也不是一个概率加权后验样本集 |
| LF-best 重算 BT | 25 个最高存储似然点中，23 个 completed；kp1/ms3.25 与 kp1/ms4 标记 under_review、无公开可用 BT JSON | 23 组可用于 LF 校准后的物理预测；两组待审不替换为基准曲线 |
| 同参数 PL 重算 | 25 组，matched_bt_config=true；与各 BT LF-best 点的 astrophysics 对齐 | 23 组可形成已核对的成对比较；历史 native 身份仍全部标记未核实 |
| 旧 LF 网格与单独拟合 PL | 25 组 15000×32×2；PL 30000×32×2；34 点、严格 MUV>-20 | 各谱独立拟合后的最大存储似然比较；旧快照诊断全 false，与较晚来源分开 |
| repaired exact 联合预测 | 固定 kp10/ms2.5、八个 astrophysical 坐标、两组 1000×32，共 64000 行 | 已有 LF、tau、xHI/xi(z) 数值，不是只有 corner 图；仍明确未收敛 |
| LF 样本带 | 从上述 64000 行中等概率选 256 行，128/ensemble，253 次唯一计算；z6/7/8/10 | 点态 16/50/84% 经验分位，不是已认证可信带；不能当 LF-only→joint 的单因素实验 |
| walker 与收敛 | 两个 1000 步 ensemble 的 12 个量；单边后续到 2000 步的诊断和续接核查 | 可展示混合问题、解释诊断；1000、600、200 与续接有共享前缀，不能当独立重复 |
| PL emulator 参考 | 35000×32×2，2240000 行；记录 gate pass、Rhat max=1.04827、ensemble-mean ESS min=4465.3 | 有参考价值；宇宙学、M_TURN 上界及 flags 不同，不能作为匹配的 BT 对照 |
| Park/PL 对照 | 27 点 Park/HST 与34点 PL/HST+Donnan，各自拟合、参数与LF曲线 | 检查模型和数据选择；不能把不同数据集似然差解释为 BT 显著性 |
| Mhalo→UV 参数响应 | 网页有实际 SFR–UV 参考换算和恒星质量比例说明 | 可补方法说明；这是解析注释与控制参数响应，不是 MCMC 相关性或新模拟 |
| exact 缓存对比 | 15 个完成用例；64/128 网格还有24个用例，含耗时、内存、I/O与逐位比较 | 方法/计算验证材料确实已有；部分官方缓存模式存在科学数值差异，不能只选最快时间 |
| 三维 viewer | PL/BT 各85个真实快照，64³公开展示 | 物理展示背景；亮温异常与未认证相位匹配的警示保留，不用于逐体素差分结论 |

## 最值得优先纳入物理论文的新增材料

### A. LF 校准后的 BT/PL 历史与 global signal

现有基准参数图谱只说明固定 astrophysics 的谱敏感性。较晚目录允许在实际 LF 选出的星系参数处，检查更贴近拟合结果的再电离预测。

23 组可用配对有 84 个 global 历史节点及 32 个横截面历史节点。这两种历史定义应分别保存；不能将 lightcone global/plane mean 称为 BTemu coeval volume mean。

这里的 PL 使用 BT LF-best 的同一组 astrophysics，不是重新优化过的 PL。与“各谱单独拟合”的旧 LF 网格是两种不同对照。

历史 native hash 未核实，因此只能写成已导出匹配设置的比较，不能宣称已排除实现差异或已认证相位匹配。源记录的 tau 字段可引用但不混成 BTemu native tau 的重算结果。

### B. 联合参数样本必须连接观测量预测

repaired1000 已有：
- 64000 行的 tau 和 xHI(z=5.9)。
- 32 红移节点的历史经验分位与最高联合似然样本。
- 256 个选中样本的 LF 点态分位。
- 一组真实最高联合似然向量、对应 tau=0.05405481159687042、joint logL=-12.917762185911394。

直接从已核对源 hash 的 pooled_samples.csv 复算，全64000行的 q16/median/q84：
- tau：0.0504844934 / 0.0569027793 / 0.0632998571。
- xHI(5.9)：0 / 0 / 0.0291655100。

这些是未收敛样本的经验分位，不是可信区间。该历史 exact8 也不是当前 BTemu six-astro+kp/MS8：不能把这套预测贴在另一条八维 corner 上。

### C. 补齐较晚 LF 来源的诊断链条

catalog 中25个模型组的 source gate 均为 true，来源、summary hash 和 diagnostics hash 均有记录。这明显比“没有后续材料”更进一步。

但目前公开的是选点与重算结果，不是每组完整的较晚原链与原诊断。下一步应按记录中的具体 job/source_run、summary_sha256 和 diagnostics_sha256 找回它们，而不是先要求25组重跑。

## 对缺失材料清单的修正

| 原需求 | 复核后的准确表述 |
|---|---|
| 物理历史对比仍需补 | 已有基准图谱及23组可核对的LF-best BT/PL配对；先整理现有数据，保留native/温度审核限制 |
| 观测量预测缺失 | 历史 exact8 的LF经验带、tau和32节点历史已有；缺的是目标统一、适用的独立诊断和可接受的推断 |
| LF来源全部未收敛 | 仅旧展示快照全false；较晚25组来源记录true，仍需原诊断与配置追溯 |
| 原始成本材料缺失 | exact/cache在多模式多网格的计时与一致性已有；仍缺实际部署BTemu完整likelihood的共同条件计时 |
| 观测数据来源全缺 | 网站44点显示集来源已有说明；实际34点likelihood仍需逐点对应核对 |
| 可把目录选点当后验带 | 不可。maximin覆盖点无后验概率权重，只能展示所选真实模型 |
| 还需等待更多corner才有物理论文材料 | 不准确。优先把现有LF拟合、联合样本、历史及观测量预测接成同一条可追溯的物理论证 |

独立最终测试、BTemu训练权重/normalizer、当前6D/8D完整配置、真正匹配且独立收敛的exact参考、正确模型mock恢复、IC目标验证等需求，并未由这些不同用途的网页材料自动解决。

## 推荐的物理论文主线

固定 astrophysics 的谱效应 → LF 拟合允许的星系参数 → 这些参数下的再电离/亮温预测 → 联合 likelihood 的参数分布和观测量预测 → 独立诊断与物理解释。

BTemu 的架构与训练仍归方法稿。物理稿的下一步应优先整合已有预测和较晚LF来源，按具体缺口补证据，避免把已完成材料重新列为全缺。

## 网页入口

- 主站与“LF posterior joint samples”模式：https://hainahuang729.github.io/21cmTB/
- 较晚 LF 选点目录：https://hainahuang729.github.io/21cmTB/web_data/posterior/catalog.json
- 同参数 PL 配对目录：https://hainahuang729.github.io/21cmTB/web_data/pl_lf_predictions/index.json
- repaired exact 联合预测、最佳向量与轨迹：https://hainahuang729.github.io/21cmTB/joint-repaired.html
- PL emulator 参考：https://hainahuang729.github.io/21cmTB/pl-emu-reference.html
- exact/cache 比较：https://hainahuang729.github.io/21cmTB/mcmc-cache.html
- Mhalo–UV 响应：https://hainahuang729.github.io/21cmTB/lf-mass-response.html
