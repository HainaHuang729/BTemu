# 物理论文主线：与 Park (2019) 的映射

日期：2026-10-30。适用稿件：物理稿 v0.13；BTemu 方法稿仍为 v0.3。本次为论证结构与文字修订，未改变观测数据、数值表、图件或样本选择。

## 中心问题

允许星系物理参数变化后，再电离观测是否仍包含可辨认的小尺度谱信息？

Park et al. (2019) 的相关对照在 §6.1–6.3、Figure 4 和 Table 2：https://arxiv.org/html/1809.08995v2 。它通过分别和联合使用 LF、模拟 21-cm 观测，讨论星系参数信息及退化，并同时展示预测的 LF 和再电离历史。我们的当前似然包含 LF、tau 和 z=5.9 中性比例约束，没有 21-cm 功率谱项；与该文 §6.1.1 的观测类型更接近。观测点、tau 版本、先验、数值设置仍有区别，不把该文参数精度套用到本项目。

## 当前正文的证据链

| 正文环节 | 要回答的问题 | 现有材料 | 解释边界 |
|---|---|---|---|
| I 引言 | 为什么谱与星系物理需要联合分析？ | Park 星系处方 + 本项目谱自由度 | 独立科学问题是谱与星系参数的可辨识性 |
| II 模型与观测 | 实际比较了什么？ | 八参数处方；当前六个星系参数或六个加kp/MS；LF/tau/xHI | 两个 X-ray 参数固定；设计域不等于推断先验 |
| III 固定星系参数的谱敏感性 | 改变谱是否影响历史？ | atlas 历史；五条 BT coeval 历史及内部差值 | 两种历史几何不同；异常边界保留；新增未验证 PL 排除 |
| IV 星系自由度与 LF 拟合 | 调整星系参数后，谱之间的 LF 差异还剩多少？ | 固定谱网格、分别拟合后的 LF 曲线 | 存储最大似然不是 profile-likelihood 置信限；旧网格诊断仍失败 |
| V 观测信息与谱可辨识性 | 再电离约束增加什么信息？自由谱后剩什么？ | 观测组合的必要定义；当前6D/8D样本及谱放大图 | 匹配的数据组合比较尚未完成；当前宽分布不能区分弱观测信息与采样不足 |
| VI 解释与验证 | 参数结果能否连接到观测量，是否可信？ | 已有预测材料清点、恢复摘要、近似检查 | 同链 LF/xHI/tau 预测仍须身份与诊断对应；不能混用历史档案 |
| VII 结论 | 当前证据链走到哪里？ | 固定参数敏感性及探索性联合样本 | 不宣称 BT 探测、谱排除或 PL 特有偏差 |

## 必须保留的两个区分

1. 改变观测组合：在相同模型、参数、先验、fixed settings、IC 和数值实现下，比较 LF-only、LF+tau、LF+tau+xHI。该比较才可识别新增观测的信息。若增加数据引起张力或模型不适配，不能预设区间一定缩小。
2. 改变模型自由度：固定谱六维与自由谱八维用于考察增加kp/MS后的联合分布；不是数据增加实验。现有四维 LF 档案与六/八维联合链不能直接拼成单因素数据组合序列。

## 图与表各自承担的任务

- atlas 与新 coeval 图：说明固定星系参数下的谱敏感性，不作为后验预测。
- LF 网格、LF 曲线：说明允许星系参数调整后的存储拟合模式；不赋予未合格拟合可信带。
- kp/MS 放大图与全角图：展示自由谱的实际样本；宽分布暂不等同于可靠的弱约束结论。
- 配对恢复表：附录中的数值可靠性检查，尚不能量化模型错设偏差。
- BTemu 训练与开发验证：方法稿；物理稿仅保留解释推断所需的方法与近似核查。

## 正文示例修订

原句：`The joint calculation asks whether the information in the luminosity functions and reionization constraints persists when the spectrum and galaxy parameters vary together.`

新增的限定：`In particular, the 6D-to-8D change adds spectrum freedom; it does not add an observation.`

中文说明：把“放开谱”与“加入新数据”分开，防止用不同维度结果误称数据改善约束。

原句：`These views of the eight-dimensional sample supply a joint exploration rather than an established measurement of kp or MS.`

修订：`The broad spectrum distributions are compatible with weak information about kp and MS, but incomplete priors and unqualified stationarity prevent separating observational degeneracy from sampling effects.`（公式排版以 TeX 为准。）

中文说明：说明图的实际形态，并保留弱观测信息与采样不足的区分。

## 下一步证据

先资格化配置、采样和正确模型恢复；再以同一参数化完成数据组合对照，最后由同一保留样本给出 LF、xHI(z)、tau 的预测比较。已有历史预测材料应优先核对其目标与身份，无需将其重新记为全部不存在。具体待补文件仍见优先材料清单和本日新材料审查。
