# 26k训练完成与进度更新：2026-10-18

检查时间：2026-10-18T14:21:58.287354+08:00
作业2234346为Slurm COMPLETED，退出码0。1 CPU、总分配时间1小时53分43秒。Direct、classifier、PCA+MLP全部完成五个seeds，原10k/16k模型保留。

## 全部512条Validation：Direct

| 指标 | 16k | 26k |
|---|---:|---:|
| History RMSE q95 | 0.01957 | 0.01161 |
| 绝对Δτ q90 | 0.001207 | 0.000795 |
| 绝对ΔxHI(5.9) q90 | 0.013632 | 0.007786 |
| 绝对ΔlogLτ q90 | 1.333029 | 0.614686 |
| 绝对ΔlogLxHI q90 | 2.594868 | 1.366372 |
| 绝对ΔlogL(tau+xHI) q90 | 3.915908 | 2.238166 |

τ与xHI(5.9)的q90单项满足当前模型精度提案；history RMSE q95仍高于0.01提案，likelihood误差也仍高于0.1提案。提案未正式确认，整体未获得科学部署验收。

## 相同183条positive Validation

| 模型 | RMSE q95 | 绝对Δτ q90 |
|---|---:|---:|
| Direct | 0.01630 | 0.001911 |
| PCA+6×80 MLP | 0.30756 | 0.031531 |

不能将positive子集与全部512条指标混合。Classifier accuracy=99.21875%，FN=3/183、FP=1，仍未启用hard gate。MLP的τ尾部误差没有随样本量稳定改善。

## 数据生产

本次最新波次快照：Train 27024/100000，Validation 512/10000。numerical failures=5，未恢复infrastructure failures=0。32并发生产继续；训练已结束，不再占用其1 CPU。

学习曲线已补入10k、16k、26k三个完成点；[读图说明](random_ic_learning_curves_20261018.md)。原τ积分、LF和priors保持不变；本次无新MCMC，sealed未开启。
