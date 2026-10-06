> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# PL1 补跑与并行 Train 状态

截至 2026-09-28 23:20 HKT，状态 **TRAIN_BATCH1_RUNNING（隔离候选）**。

| 阶段 | Job ID | 状态 | Allocation |
|---|---|---|---|
| PL1 补跑 | 2159847_2 | RUNNING，cn009 | 16 CPU，最多 2 小时 |
| Train 第 0、1 条 | 2159806_0、2159806_1 | 已完成，QA 成功，隔离 | 各 16 CPU |
| Train 第 2、3 条 | 2159850_2、2159850_3 | RUNNING，cn010 | 各 16 CPU，最多 2 小时 |

修复后的真实 native 功率谱/方差探针返回成功，输出证据保存在 results/pl1_repaired_probe_output.json；完整 PL history 和 KP=1/10/30 不变性仍待验收，不能称整个 preflight 已通过。

Train 计划 448，已尝试 4；机械合格且隔离 2；正式入库 0；失败 0。Preflight 累计 5 次尝试，其中两个历史失败保留、两条正常点通过、PL1 补跑正在运行。

已结算 10.958889 core-hours；三个未结清作业保守预留合计 96 core-hours（包含其已运行部分，不应重复相加计费）。attempt 上限改为 14，所有 core-hour 上限不变。此次特例只匹配 preflight_0000003 的精确回执，不允许其他数值失败自动重试。17 项相关软件回归通过。

后续已由运行 worker 内的真实受预算推进逻辑负责；目前只有表中作业实际提交，不预先声称其余波次已提交。Sealed labels 未生成、未读取，未启动模型训练或生产 MCMC。
