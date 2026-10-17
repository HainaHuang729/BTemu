# 当前验收门槛与NNERO论文比较（2026-10-17）

本记录区分模型精度提案、PCA表示开发筛查、已确认IC审计门槛和论文实测性能。记录这些数值不等于确认或修改科学阈值。

## 模型最终验收：仍为待确认提案

来源：contracts/acceptance_protocol.json，状态 PROPOSED_REQUIRES_SCIENTIFIC_CONFIRMATION。
以下现值来自16k Direct的全部512条Validation，ensemble成员先在物理xHI空间平均，再运行原后处理。q90/q95以整条theta history为抽样单位。

| 指标 | 当前提案上限 | 16k Direct现值 |
|---|---:|---:|
| trajectory RMSE q95 | 0.01 | 0.01957 |
| trajectory最大绝对误差 q95 | 0.03 | 0.07014 |
| 绝对Δτ q90 | 0.001 | 0.001207 |
| τ误差平均值的绝对值 | 0.0002 | 0.0000195 |
| 绝对ΔxHI(5.9) q90 | 0.01 | 0.01363 |
| 绝对ΔlogLτ q90 | 0.1 | 1.333 |
| 绝对ΔlogLxHI q90 | 0.1 | 2.595 |
| 绝对ΔlogL(tau+xHI) q90 | 0.1 | 3.916 |

只有τ平均偏差满足上述单项提案；最终还需要分组覆盖及独立exact posterior位置、宽度、相关性和支持重叠验证。配置中的reweighting ESS fraction≥0.5也是提案，不是已经完成的验收。

## PCA表示：独立的预注册开发筛查

当前 maintenance/v2/baseline.py 要求真实投影系数重构后的：

- history RMSE q95 < 0.001；
- 绝对Δτ q95 < 0.0001；
- 绝对ΔxHI(5.9) q95 < 0.001；
- τ与xHI两项绝对ΔlogL q95分别 < 0.01；
- 全部重构history数值有效且在物理范围内。

这是本项目的开发表示筛查，不是NNERO论文原标准。目前只有logit K=32通过，没有证明32节点history的压缩收益。不能把该筛查、最终模型门槛或训练loss混为一项。

## IC审计：用户已确认的保守开发门槛

来源：contracts/ic_audit_acceptance.json及2026-10-07的明确确认记录。

- theta层q90(std_tau) ≤ 0.0002；
- theta层q90(std_xHI(5.9)) ≤ 0.002；
- theta层q90(std_logL_tau / std_logL_xHI / std_logL_joint_history)，每项 ≤ 0.02；
- 远离cut的family不得因IC变化而翻转classifier标签。

history IC scatter RMS≤0.002、mean-history与IC-marginalized logL绝对差≤0.02属于另外预注册的诊断提案，不在用户明确确认的数值字段列表中。已确认的IC门槛不能据此扩写成“全部模型最终精度阈值均已确认”。

该审计用于判断随机realization的散布与推断近似，不是网络预测误差。原审计失败决定保留；后续单随机IC开发生产来自另外的用户授权，不构成均值或posterior验收通过。

## NNERO原论文：数据规模与报告性能

| 项目 | NNERO论文 | 本项目16k实验 |
|---|---:|---:|
| Classifier Train | 101,921 | 16,000 |
| Classifier Validation / Test | 各12,740 | Validation512；sealed未开启 |
| Regressor正类Train | 34,913 | 5,930 |
| Regressor正类Validation / Test | 各4,364 | Validation183；sealed未开启 |
| History节点 / PCA系数 | 50 / 约30 | 32 / 32 |
| Classifier accuracy | 独立Test98.4% | 开发Validation98.83% |

论文共127,401次模拟，随机IC；τ相对误差均值0.11%、标准差1.13%；各红移history相对误差的1σ范围约低于10%。它们不能直接等同于本项目绝对误差的q90/q95，也没有给出我们这套全域ΔlogL q90≤0.1验收标准。来源：[论文§III](https://arxiv.org/html/2503.11261v1#S3)。

## 当前实现与论文方法的差异

论文目标Xe与本项目体积平均global_xHI定义不同，不能直接作1−xHI等同替换。论文对log10(Xe)做PCA，训练目标包含history和派生τ的相对误差项；目前BT实现使用logit(xHI) PCA和重构后物理xHI MSE。来源：[论文§II.1与§III.3](https://arxiv.org/html/2503.11261v1#S3.SS3)。

因此，目前是NNERO-style架构与流程对照，尚不是其完整训练方法复现。下一步应核对表示、loss和量定义的差异，再在冻结的BT xHI target下适配。若研究derived-tau loss，仍须验证其与原后处理一致，不新增独立tau head。

最终精度提案需结合推断相关区域正式审查并确认；不根据当前结果临时放宽，也不能将未满足本项目提案称作未达到论文标准。本次只补充说明，没有更改任何contract、模型、标签或运行作业。
