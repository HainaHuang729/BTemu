> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 当前执行状态

用户已授权仅补跑 PL1，尝试上限为 14；384/2000/2385 core-hours 上限均保持不变。PL1 补跑作业 2159847_2 已运行，修复后的真实 power/sigma 探针成功返回；完整 history 和 KP 不变性验收仍未完成。

前两条 Train 作业 2159806 已成功生成，单条 QA 通过；两条都保持隔离，正式入库 0。下一波冻结索引 2、3 已由真实 Slurm 作业 2159850_2、2159850_3 在 cn010 运行。预检与候选 Train 按现有受预算控制器并行推进，无需进一步确认。

各阶段仍按原失败分类处理；本次 PL1 特例绑定唯一历史 attempt 与完整回执 digest，不开放一般数值失败重试。历史取消和探针错误均保留、计费。

只有完整 native qualification 通过、候选标签经原后处理再验收后才创建 admission 回执。隔离候选不能用于训练。模型训练、sealed labels、生产 MCMC 均未启动。

查询 results/batch1_execution_status.json 与 data_runs/20260928_batch1 的 Slurm/receipt/continuation 记录。不要重提尚在运行的样本，也不要把尚未提交的未来波次当作已提交。
