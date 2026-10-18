# 2026-10-18：并发记账启动失败与恢复

23:30检查发现生产已在29,455条Train处停止。原数组2237777_100（实际worker2237879、cn060）在22:20以PermissionError: Approved concurrency exhausted退出。退出点位于ledger.reserve，尚未提交attempt reservation、加载native或生成history；已分配16 CPU运行31秒。

这是明确的模拟前名额拒绝。名额/回执可见性时序造成短暂满额是待排查假设，不能仅凭日志断言共享文件系统故障。控制器将“终态allocation但没有attempt/receipt”保守标为系统性来源/runtime/schema告警；本次未发现科学target或已有标签身份变更。

## 有限修复与证据

- 只对完整匹配的Approved concurrency exhausted错误增加有限等待：最多12次原ledger.reserve查询，间隔5秒；每次仍执行原上限检查。没有提高或绕过64并发，也不重试其他PermissionError、native身份错误或数值失败。
- 新增容量等待7项软件测试及原启动回归7项测试均通过。原exact adapter、原后处理、科学/IC/native/design契约指纹保持一致。
- 通过终态Slurm和归档日志补记原启动失败为infrastructure_failure，evaluation_started=false。原31秒×16 CPU=0.137778 core-hours保留；Slurm计费本来已包含这条allocation，补ledger不重复添加同一allocation成本。
- 相同冻结sample random_v2_train_029433、requested IC seed 2018107277按既有一次基础设施重试规则重跑。没有替换参数、改seed或改模拟设置；5条原数值失败保留。
- 恢复作业2237980完成登记，原控制器正常解除停止标记并提交数组2237981与collector2237982。首次恢复核查64条RUNNING、1024 CPU，另64条PENDING。
- 此时Train29,455、Validation512；新增重试标签尚未验收入库。该基础设施失败在下一完整波次汇总前仍显示1条，不能提前写成重试成功。

内部证据：results/reservation_recovery_20261018，包含原source/budget/log快照、变更身份、测试、Slurm记录和reconciliation。公开内容仅为事件及资源汇总，没有原科学标签或内部worker代码。

## 模型与科学状态

26k Direct/classifier/PCA+MLP全部五个seeds已完成；32k训练尚未提交。新data-generation并发上限仍64，每条16 CPU、16 GiB、2小时。未增加MCMC、未开启sealed、未更改最终科学验收提案。恢复数据生产不等于emulator已通过推断验收。
