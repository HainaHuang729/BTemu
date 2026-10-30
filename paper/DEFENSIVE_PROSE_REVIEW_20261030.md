# 防御性写作检查与修订

物理稿 v0.13 → v0.14，2026-10-30。方法稿 v0.3 保持原样。

## 检查结论

主要问题是同一限制在摘要、引言、结果、图注和结论反复出现，以及 accepted/qualified 等验收用语盖过物理结果。本次保留影响解释的限定，删除或合并同一上下文中的重复提醒。

## 已修订

- 摘要先报告固定参数历史差异、分别调整星系参数后的 LF 模式及联合样本的宽分布；具体链长/监测数值继续保留在采样结果，不再堆入摘要。
- LF 最大似然的统计性质与失败诊断集中在网格图注；结果段描述谱网格上的实际模式。
- 观测组合比较由连续 must 句改为简短定义；6D→8D 改变谱自由度的区分保留。
- 样本表保留均值/标准差定义及探索性解释；图注保留独立收敛未建立的说明，避免正文逐句重复。
- 五条 coeval 历史的外部配置/IC/native 缺口移到相应附录，原信息保留；未确认 PL 仍排除。
- 讨论先连接固定参数敏感性、星系自由度和联合样本，再集中说明恢复/似然目标。
- 结论缩成两段，避免连续三段以审查清单收尾。

## 代表性修订

原文：`The dependent walkers and the absence of independent accepted convergence prevent interpreting those spreads as qualified physical constraints.`

修订：`Independent convergence has not been established for these interacting-ensemble chains.`

说明：用明确的采样状态替代验收术语；统计解释已经在表注定义。

原文：`Their width must not be interpreted as a measured absence of spectrum information.`

合并后：`The broad sampled distributions remain compatible with both weak observational information about kp and MS and incomplete sampling.`（数学排版以 TeX 为准。）

说明：把反复告诫改为两种尚可容许的解释；仍不把样本宽度直接写成观测约束。

原文：`No optical depths, uncertainty bands or convergence claims are inferred from these curves.`

处理：删除该清单句。图注直接定义五条历史和同节点差值，继续明确说明排除未核验的 PL。

## 保留的科学限制

独立收敛未建立；表中标准差为相关样本的描述性散布；PL 数值身份未核实；atlas 饱和历史的转折/积分边界未解析；paired mock 未完成正确模型恢复验证；代表历史似然与 IC 边缘化的关系未验证。所有数值、公式、引用键、图件和原有样本选择保持不变。
