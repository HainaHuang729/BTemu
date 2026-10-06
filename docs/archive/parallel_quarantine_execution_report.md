> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 并行执行与 PL 探针失败回报

最新状态：**PREFLIGHT_FAILED；已经启动的两条 Train 继续生成并保持隔离，停止追加。**

- 原入口作业 2159756 与 adapter 作业 2159786 均成功；32 节点、tau 输入/输出、观测 xHI、LF 与各项 likelihood 的逐值一致性全部通过，见 results/normal_pair_parity.json。
- 自动启动的 PL1 原入口预检作业 2159815 在功率谱探针阶段失败，尚未调用完整 history。原记录保留，尝试与成本照计。
- 探针只设置 PS 全局参数，漏设 UF 全局参数；源码 sigma_z0 → MtoR 会读取 UF 指针。已修复初始化并增加故障信号、阶段与退出码日志；10 项相关软件回归通过。旧探针没有保存子进程终止信号，因此不伪造具体信号值。尚未真实 native 复测，不能据此称 PL 已通过，也没有证据确认 PL 物理失败。
- 两条 Train：2159806_0、2159806_1，cn010，每条 16 CPU/最多 2 小时，来自冻结第 0、1 行。产物只进入隔离候选池；在完整预检通过前，正式入库必须为 0。
- 这两条运行中的标签 worker 不执行 PL 探针，其科学调用未修改。该实施版本列入明确的候选 admission allowlist，后续仍须经目标与原后处理复验；没有修改运行中作业或 native。
- 当前没有追加后续 Train。原 max_attempts=13 已包含之前误取消的补跑，未授权额外 PL 代码错误重试。已请求仅补跑 PL1，将上限调至 14，384 core-hours/总预算不变；尚未收到。

实时作业、计费及隔离数见 results/batch1_execution_status.json。Sealed labels 仍未生成、未读取，未启动训练权重或生产 MCMC。
