> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 当前并行执行

用户已明确授权预检与 Train 同时运行，Train 产物先隔离。预算没有增加。

- 预检在 cn009 逐条执行；Train 在实际探测通过的 cn010 上每波 2 条，从冻结 first_448 的前两条开始。
- Train 在 `quarantine_pending_native/` 保存，原生成回执 `qualified=false`；不进入训练 manifest，loader 拒绝隔离路径与符号链接。
- 全部预检通过且 `qualified_for_batch1=true` 后，复核 checksum、参数、target/implementation/runtime、原 tau/xHI；保持原生成回执不变，另写 `admissions/` 回执，复制紧凑原值至已验收目录，再检查训练 loader。
- 前 8 条先做机械 QA、原后处理复验和隔离拒绝检查；可在尚未科学入库的条件下继续候选生产。实际训练使用仍必须等待 native gate 和 admission。
- 预检失败时停止追加 Train，已经生成的候选保持隔离；不自动修改物理或增加预算。
- 已提交的 Slurm worker 包含后续受预算约束的推进。未提交的 job 不当成已提交；硬故障导致回调未执行时，对账后从同一入口恢复。

当前 job IDs、入库数与成本以 `results/batch1_execution_status.json` 及 Slurm 为准。完整 4096、Validation、Challenge、sealed labels、模型训练与生产 MCMC 未启动。
