# BTemu 进度检查：2026-10-18

检查时间：2026-10-18T11:07:12.190492+08:00。数据数量来自已验收完整波次；运行中本波产物未计入。

| Dataset | Qualified | Target |
|---|---:|---:|
| train | 26,256 | 100,000 |
| validation | 512 | 10,000 |

Train相比昨日检查20,624条，新增5,632条。Validation仍512条，尚未扩至2048或10000。
队列检查：数组2234233，32个RUNNING（512 CPU）、64个PENDING；运行节点cn059/cn063。collector2234234等待依赖后验收并继续既有生产链。32并发是上限，实际数量会随波次尾段及调度变化。
当前numerical failures为5条，与昨日相同；未恢复infrastructure failures为0。累计基础设施retry115次。失败记录保留，未重抽参数或修改科学设置。
累计attempts=26888；已核算51131.13 allocated core-hours；wall time median/q90=418.1/496.9秒；生产目录约7.20 GiB。

## 模型状态

最新完成仍为16k Train / 512 Validation、全部五个seeds的开发比较；本次未提交新训练。下一档32k训练尚未提交。
同一183条positive Validation：Direct trajectory RMSE q95=0.02372、绝对Δτ q90=0.002568；PCA+MLP分别为0.31423、0.029141。模型、IC均值/边际化likelihood及posterior尚未验收。
当前数据生产继续，不将已生成样本数当作科学部署精度。

## 门槛及边界

[验收门槛与NNERO论文比较](acceptance_and_nnero_comparison_20261017.md)：模型最终精度仍为待确认提案；IC确认门槛和PCA开发筛查分别记录。
[结果分析与下一步](analysis_and_next_steps_20261017.md)。
Selected repaired native身份与冻结random-IC target继续沿用。当前无生产停止标记；sealed labels未生成、未读取，本次未新增MCMC。
