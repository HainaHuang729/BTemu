# 首轮 random-IC 开发训练

冻结现有 10,000 条已入库 random_ic_v2 Train；提前生成原独立 Validation 设计中的前 512 条。不更改任何参数坐标、随机种子或 split，不混入 fixed-IC labels。

复用现有 Direct ResMLP、10→30→30→1 classifier，以及 positive-only PCA + 6×80 MLP。五个初始化 seeds 为 11、29、47、71、101，沿用冻结 optimizer、epoch 上限和 early stopping。Normalizer 只拟合 Train；PCA 只拟合 exact-positive Train。

PCA 的 K=4/8/12/16/20/24/28/32 在独立 positive Validation 上检查 history、原 τ、xHI(5.9) 和两项 likelihood 重构误差。筛查失败时保留 Direct/classifier 结果，不放宽门槛强行启用压缩。

Validation 的原抽样分母始终为 512。任何失败均保留，不重采样。训练需至少 256 条合格 Validation、两类各至少 25 条，并通过生产来源和质量检查。这些是执行下限，不是精度保证。

本轮比较 history MAE/RMSE、trajectory 分位数、原后处理的 τ/xHI/likelihood 误差，以及 classifier false negatives。Classifier 概率阈值 0.5 仅作开发诊断，不启用生产 hard gate。结果针对独立单次 random-IC realization，包含 IC scatter，不能解释为已验证的条件均值或 posterior 精度。

模拟并发仍最多 16×16=256 CPU；模型训练另用 1 CPU、8 GiB、最多 8 小时。验证数据由现有 worker 和 collector 验收入库后，依赖训练作业检查实际回执再开始。

10 月 14 日生产日志发现共享 home 临时目录配额耗尽，造成 2 个目录创建失败及 112 个连带并发保护启动失败，均发生在相应 exact evaluation 开始前。原错误、Slurm 成本和原自动分类保留；节点本地 `/tmp` 写入探测通过后，仅修改临时目录与启动异常收据处理，按原基础设施重试规则恢复。此前 2 个真实 NaN 数值失败保留且不自动重试。

最新状态与结果由[项目首页](https://hainahuang729.github.io/BTemu/#random-development)和[进度文档](progress.md)按回执更新。提交与等待调度不算训练完成。Sealed labels 未生成、未读取；不启动生产 MCMC。

## 首轮实测结果（2026-10-14 完成）

10,000 条 random-IC Train、512/512 条独立 Validation，三类模型全部完成 5 个 seeds；模型训练与比较耗时 1,806.9 秒（约 30 分钟，另计标签验收）。不是 fixed-IC 旧模型结果。

下面两行在相同的 183 条 exact-positive Validation 上比较；分位数单位是一整条 history。

| 模型 | History RMSE q50 | History RMSE q95 | 绝对 τ 误差 q90 | 绝对 logL_tau 误差 q90 |
|---|---:|---:|---:|---:|
| Direct ResMLP | 0.00748 | 0.03791 | 0.00338 | 7.819 |
| PCA + 6×80 MLP | 0.02996 | 0.36626 | 0.03060 | 101.961 |

Direct 在全部 512 条 Validation 上的 trajectory RMSE q50/q95 为 0.00290/0.02139，绝对 τ 误差 q90 为 0.00171。不同验证范围不可混为同一比较。

Classifier ensemble accuracy 为 99.02%，但误拒绝了 3/183 条允许区样本（FN rate 1.64%），另有 2 个 false positives。尚不足以证明生产 hard gate 不影响 posterior。

Positive-only PCA 仍只有 logit K=32 通过现有重构筛查，没有确认压缩收益。本轮 PCA+MLP 的拟合误差显著大于 Direct；完成训练不等于拟合或科学验收通过，尚需检查训练稳定性与 decoder。

Direct 的 likelihood 误差尾部也明显偏大，当前两种模型均未通过科学部署验收。验证针对独立单次随机 IC，包含 IC scatter；不能将全部误差归因于网络，也不能据此声称已经学到经过验证的 IC 条件均值。

LF 未在本轮模型验证中重新计算；上述 likelihood 指标仅涵盖原 τ 与 xHI 后处理。Sealed labels 仍未生成、未读取，未启动生产 emulator MCMC。
