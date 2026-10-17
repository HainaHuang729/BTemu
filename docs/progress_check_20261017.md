# BTemu 进度检查：2026-10-17

检查时间：2026-10-17T10:51:46.545445+08:00。入库数量来自最新完整波次验收，当前波次产物尚未计入。

| 数据集 | 已合格 | 目标 |
|---|---:|---:|
| train | 20,624 | 100,000 |
| validation | 512 | 10,000 |

相比上次 Train15,890，新增 4,734 条入库数据。
当前数组 2227545：RUNNING=32、PENDING=26，运行仿真分配 512 CPU；上限32并发、每条16 CPU。collector 2227546 已提交，验收后沿用自动续跑链。
累计 attempts=21256，当前 numerical failures=5，未恢复 infrastructure failures=0，基础设施 retries=115。失败参数与原始记录保留。
已核算 40275.16 allocated core-hours；wall time中位数/q90为 417.7/496.9秒；生产目录约 5.74 GiB。资源记账与队列时间不同，旧快照零预留不代表当前无运行任务。

## 16k训练完成

作业2221216：Slurm COMPLETED，退出码0；1 CPU运行41分50秒，约0.697 core-hours。Direct、classifier、PCA+6×80 MLP均完成全部五个seeds。16000 Train含5930条positive；同一批512 Validation含183条positive。

以下统一比较183条exact-positive Validation，先在物理xHI空间取ensemble均值，再调用原后处理。

| 方法 | Train N | Trajectory RMSE q95 | 绝对Δτ q90 | 绝对ΔlogLτ q90 |
|---|---:|---:|---:|---:|
| Direct ResMLP | 10,000 | 0.03791 | 0.003377 | 7.819 |
| PCA+6×80 MLP | 10,000 | 0.36626 | 0.030604 | 101.961 |
| Direct ResMLP | 16,000 | 0.02372 | 0.002568 | 6.690 |
| PCA+6×80 MLP | 16,000 | 0.31423 | 0.029141 | 125.237 |

Direct在全部512条Validation上：RMSE q95=0.01957，绝对Δτ q90=0.001207；绝对ΔlogLτ / ΔlogLxHI / 两者之和的q90为1.333 / 2.595 / 3.916。该组与positive子集分开，未补算新的LF对照。
Classifier仍有3/183个false negatives（1.64%），false positives为3。PCA仍只有logit K=32通过重构筛查，没有证明压缩收益。
增加至16k改善了Direct的history及τ误差。MLP的history误差下降，但τ likelihood尾部误差变大；不能只凭history MSE改善宣称可用于推断。昨日初始化对照是独立10k实验，不混入本轮数据量比较。

## 尚未完成

- 100k Train / 10k Validation继续生产。下一档32k模型训练尚未提交。
- MLP拟合、IC均值/边际化解释、likelihood及posterior验收仍未解决。
- 本次未新增MCMC；classifier硬拒绝未启用；sealed labels保持未生成、未读取。
