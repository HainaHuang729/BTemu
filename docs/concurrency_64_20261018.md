# 2026-10-18：数据仿真上限提高到64并发

用户在原32并发基础上明确要求再增加32。本次将当前数组2236501和未来random_ic_v2 Train/Validation波次上限提高为64，单条16 CPU，最多1024 simulation CPUs。

每条仍为16 GiB、最多2小时；节点范围cn057–064。128任务的wave大小不变。科学target、selected repaired native、IC seeds、参数设计、split、priors和全部attempt/storage/failure限制保持原定义。该授权仅调整数据生产资源，不授权新MCMC或sealed访问。

## 实际生效证据

- 8项资源授权回归检查通过，包括64允许、旧32授权兼容、65拒绝、错误授权/设计/CPU/内存/时限/节点拒绝。
- 完整执行门槛重新通过：64并发、每条16 CPU，native SHA256仍为3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2。
- 当前Slurm数组有效ArrayTaskThrottle=64。命令对部分已结束/运行成员返回错误，因此依据实际throttle和实时队列核实，不单凭命令退出码判断。
- 当次检查58条RUNNING、928 CPU；本波待启动任务已全部启动。未来完整波次允许最多64条同时运行，实际数仍服从scheduler。
- 当次节点空闲352 CPU；若其他作业不变且BTemu达到64条，预计仍留256 CPU。空闲量会随其他调度变化。
- 原运行仿真未取消，其他项目作业未改动。只在切换配置时临时限制待启动任务，确认全部旧worker通过启动门槛后再原子更新，避免身份检查竞态。

原32并发授权及预算/source快照保留。完整内部证据位于results/concurrency_revision_20261018_64；公开报告仅含资源与状态摘要。
