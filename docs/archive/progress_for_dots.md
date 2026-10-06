# BT 10D xHI Emulator 进度（dots 监控入口）

更新时间：2026-10-06T10:12:25.119696+08:00。此文档为刷新时的快照，生产侧汇总距刷新 12805 秒。

当前阶段：`DATA_BATCH_COMPLETED`。正式数据仍在生产；首轮模型完成开发训练，但尚未达到科学部署要求。

| Dataset | Planned | Qualified | Remaining unqualified | Batch2 failed |
|---|---:|---:|---:|---:|
| train | 4096 | 4096 | 0 | 0 |
| validation | 512 | 512 | 0 | 0 |

Train 合格数包含首批 448 条已验收 history；Batch2 attempts/failed 不包含首批历史重试记录。剩余未合格不等于尚未提交。

## 当前队列

最近提交作业：`None`。仅列最近一波的即时队列状态；空表不代表完成，需查 receipts 与 sacct。

| Job | Slurm state | Node | CPU | Reason |
|---|---|---|---:|---|
| — | 当前队列无该作业；终态待核对 | — | — | — |

资源：仅使用 tkcastrosim1 / chpc-cn[057-064]，最多 8 个完整 evaluations 并发，单任务最多 16 CPU、16 GiB、2 小时。总 core-hour 上限已由用户取消；尝试次数和单任务限制仍有效。

Batch2 汇总记账：已计入 8024.996 core-hours，预留 32.000 core-hours。此数不含首批 448、preflight、模型训练，且以生产侧记账时间为准。

## 科学对象和验收边界

- 10D 输入；fixed-IC requested seed 725213656658；32 节点体积平均 global_xHI。
- Selected native SHA256：`3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`。既有 native/adapter/PL 极限预检已通过。
- τ 完全由原 history 后处理派生；LF 保留原精确 forward。
- z=5 中性残余和 z=35 早期电离属于 SCIENCE_DOMAIN_WARNING，不删标签、不强制完全电离。
- LF-invalid 但 history-valid 的标签仍可用于 history 训练；不宣称该点 joint likelihood 有效。
- 45 条旧隔离记录未转入训练。封存测试未开启；监控器不读取封存文件或标签。不启动生产 MCMC。

## 开发训练

首轮使用固定 1024 Train / 144 Validation、5 个初始化 seeds，已完成。Ensemble trajectory RMSE q95=0.18746；|Δτ| q90=0.02316，当前不足以用于科学推断。

训练误差下降但验证改善不足。验证误差与最近训练点距离相关系数约 0.095，尚不能确定主要原因。

| Train N | 状态 |
|---:|---|
| 1024 | COMPLETED |
| 2048 | DEVELOPMENT_TRAINING_COMPLETED |
| 4096 | DEVELOPMENT_TRAINING_COMPLETED |

2048/4096 达到冻结样本要求后由现有 controller 自动提交；固定首轮 144 Validation、同一配置和全部 5 seeds。上述 WAITING 状态表示尚未提交训练作业。

## Endpoint 与组件有效性（开发数据）

| Split | History-valid | LF-invalid/history-valid | xHI(5) q50 / q95 | xHI(35) q50 / min |
|---|---:|---:|---|---|
| train | 4096 | 778 | 0.603179 / 0.995951 | 0.999795 / 0.000000 |
| validation | 512 | 91 | 0.526476 / 0.996235 | 0.999795 / 0.000000 |

真实 numerical failure count（开发侧 QA 汇总）：0。更多分位数和阈值计数见 results/endpoint_domain_audit.json。

## dots 刷新与告警规则

固定入口：`docs/progress_for_dots.md`；机器入口：`results/dots_progress.json`。生产状态源由现有流水线更新；本快照由下列命令刷新。dots 可每 10–15 分钟调用，不需要完整模拟环境：

```bash
python3 /oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/maintenance/write_progress_for_dots.py
```

刷新命令只读取开发状态、汇总 metadata 和 Slurm 队列，原子写入两个监控文件；不提交或取消作业，不读 sealed labels，不改科学契约或生产代码。未新建定时任务；dots 需调用上述命令获得新快照。

- source_age_seconds > 7200：检查是否超时、等待调度或汇总失败；不要仅凭时间自动取消。
- PENDING 仅表示等待；RUNNING 才表示执行中。最近作业不在队列时检查 sacct 和验收回执。
- 数量不增长且无运行/等待作业：检查 continuation_status、失败 registry 与 controller 错误文件。
- 偶发独立失败按既有协议记录后继续其他点；系统性 native/config/provenance 错误应人工核查。
- Endpoint warnings 与 LF-domain failures 不触发删除 history。不得自动改 seed、native、分辨率、priors 或 split。

本次告警：
- 生产汇总超过 2 小时未刷新；检查队列和 worker 日志，不自动取消作业。

关键证据路径：

- `data_runs/20261001_batch2/continuation_status.json`、`failure_registry.json`、`submissions.jsonl`
- `results/native_qualification.json`、`results/endpoint_domain_audit.json`
- `artifacts/learning_curve_fixed_validation_v1/status.json`
- `artifacts/development_history_fidelity_20261003/diagnostics/trajectory_diagnostics.json`

下一步：继续冻结 Train4096 / Validation512 生产；依次完成 2048 与 4096 learning curve；之后检查 history、派生 τ/xHI 和各项 likelihood fidelity。最终封存验收仍需单独授权。

## Dataset v2 100k（独立生产）

v2快照更新时间：2026-10-06T09:25:28.900094+08:00。更多实时字段见 results/dataset_progress.json；执行记录见 docs/dataset_v2_100k_production.md。

Train：13824/100000（已包含截至该快照的合格v1 Train）；独立 Validation v2：3072/10000。旧Validation512继续保留v1 benchmark。

v2 RUNNING=0，PENDING=0；当前ramp=32，配置上限=32。

v2 true numerical failures=0；stop reasons=[]。sealed v2只有独立参数设计，未生成/读取labels。
