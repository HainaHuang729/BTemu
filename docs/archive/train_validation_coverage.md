> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 参数覆盖（没有标签性能）

Train 4096、Validation 512、Sealed test 1024 的参数设计已冻结。分层分别为 broad 3072/256/512、fixed view 384/128/256、continuous-MS view 384/128/256、train-only anchors/edges 256/0/0。

view 来自实际契约：fixed 为 KP=10/MS=2.5，8 个活跃天体物理自由度；continuous 为 KP=1、MS∈[0.5,2]，9 个活跃自由度。共享域 KP∈[1,30]、MS∈[0.5,4] 不改变这些 priors。观测相关 likelihood 仍为原 LF + split-normal tau + neutral fraction。

输入几何和 per-parameter extrema、各 view tags 计数、独立随机流、参数到 Train 的归一化最近邻距离见 results/development_coverage.json 和 contracts/dataset_design.json。Sealed test 此处仅用参数坐标，不读取标签。抽样 mix 因刻意加密而不代表原科学 prior 下无偏的平均误差。

已有 448 候选全部在 Train。尚无 qualified 新标签，故 xHI 多样性、全零/全一占比、过渡区域、tau 分布、xHI 惩罚覆盖、端点风险频率与新域失败率均**未测量**。旧 45 条记录继续隔离，不因已保存 tau 或先前回归成功而自动变成训练标签。

已知旧开发惩罚点的参数仅用于 preflight，旧标签仍不进入 Train。future refinement 只能扩展 Train 并创建版本，不根据 validation 表现重选 validation，更不读 sealed labels 选点。PL-KP family 按整组管理；全体相同 IC seed 不构成一个数据 family。
