> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 单点补跑执行报告

状态：**PREFLIGHT_RUNNING**。用户确认的唯一补跑已启动。

- 实际作业 `2159756_0`，cn009，16 CPU，2 小时硬上限；同一 `preflight_normal_original` 参数点和 fixed IC，没有重采样。
- 该 worker 自身记录 native SHA256 `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`；runtime fingerprint `6fc2f3625507e495eb6db8c157d59941e8b71a04688da79729b104951fda460c`；seed C 表示 `725213656658`，runtime 门禁通过。
- 历史取消作业保留。预检最多 13 次尝试，其中唯一允许重试的是 normal_original；仍须获得冻结的 12 项有效预检结果。
- core-hours 上限：preflight 384、Train 2000、总计 2385。其他阶段未授权。
- 26 项预算/数据测试及 4 项推进门禁测试通过；这些不是科学性能验收。
- 已提交的 worker 内包含真实分波提交逻辑。下一条预检只在前条 QA 成功后提交；全部预检和机器科学 qualification 通过后自动进入 Train。afterany 只用于防止分配重叠，不能替代科学门禁。
- Train 尚未提交，合格数 0/448；sealed labels 未生成、未读取。
- 当前运行快照及成本见 `results/batch1_execution_status.json`，真实后续 job IDs 见 `data_runs/20260928_batch1/submissions.jsonl`。本报告不把条件性未来提交写成已经提交。

历史事故报告保留于 `docs/batch1_execution_report.md`；其“等待补跑授权”结论已由本报告取代。
