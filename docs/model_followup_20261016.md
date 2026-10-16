# 2026-10-16：MLP 诊断与 16k learning curve

数据生产按已批准的 32 并发继续，单条 16 CPU。当前推进两项独立的开发工作，均不产生新的 exact simulation，不改变标签或生产配置。

## Material Passport

- 阶段：run / reproducibility diagnosis；数据版本 random_ic_v2。
- 证据：冻结开发快照、已保存的五个 MLP checkpoints、Slurm 提交记录与后续验收回执。
- 范围：Train / Validation；sealed labels 未读取。未启动新的 MCMC。

## 10k MLP 权重诊断

作业 2221212，1 CPU、8 GiB、最多 1 小时。读取已有 10k Train / 512 Validation，通过原 loader 重新验证来源与后处理；只分析 classifier-positive 子集。检查每个 seed 的 Train/Validation MSE、逐红移误差、错误饱和输出、饱和单元对平方误差的贡献，以及真实 PCA 系数的完整重构误差。

上一轮五个 seed 的选中 epoch 训练 MSE 约 0.012–0.018，说明拟合不足已存在于训练侧；不能仅凭验证误差判断是数据量不足。该诊断不自动改变 loss、架构或阈值，也不证明某一个因素是唯一原因。

## 16k 嵌套训练

作业 2221216 已提交，依赖当前数据 collector 2221087；独立 1 CPU、8 GiB、最多 8 小时。队列 PENDING 只表示等待。启动时还必须检查确实存在 16,000 条已验收 Train，以及每条标签的 native/target/seed/checksum/原后处理一致性。

- Train 按冻结设计顺序选择前 16,000 条合格数据，前 10,000 条必须与上一轮完全一致。
- Validation 保持同一批 512 条，不重新选择。
- 全部五个 seeds：11、29、47、71、101。
- 复用原 Direct ResMLP、2×30 classifier、positive-only PCA 重构审计与 6×80 MLP；保持同一优化器、训练上限及 early stopping。
- 统计归一化只拟合本轮 Train，PCA 只拟合本轮 Train-positive。

这轮测量增加数据量带来的影响。MLP 诊断与该比较分开保存，不能根据结果删除较差 seed。即使 16k 有改善，也不代表条件均值或 posterior 已验收；单随机 IC 验证误差仍含 IC scatter。

状态及完成后指标由网页自动读取实际回执更新，见首页“模型诊断与下一轮”。

## 已完成的权重诊断

作业 2221212 已完成，分析耗时约 205 秒；读取同一批 3,701 条 Train-positive 和 183 条 Validation-positive。原五成员物理均值的 trajectory RMSE q95：Train 0.32175，Validation 0.36626。真实 PCA 系数重构最大误差约 1e-6（既定 logit endpoint epsilon 的量级）。

“错误饱和”预定义为：预测小于 1e-4 而 exact 大于 0.1，或预测大于 1−1e-4 而 exact 小于 0.9。每个 seed 的训练平方误差有 92.65%–98.11% 位于这些单元；验证对应比例为 75.94%–87.62%。分母分别为该 seed 在本集合全部 32 节点的总平方误差；该数值不是独立样本置信区间。

这些结果支持优先检查优化过程中的饱和，而不是仅增加数据或将问题归咎于 PCA 截断；尚不证明饱和是唯一原因。

## 预注册一次初始化对照

作业 2221253 已提交，1 CPU、8 GiB、最多 2 小时。只将最终 Linear 的初始权重设为 0，并将初始偏置设成 Train-positive 原始 xHI 算术平均的 logit/PCA 投影，让初始完整预测接近该算术平均。原始标签不变；后续仍用原 physical-history MSE、AdamW、early stopping、最多 1000 epochs及全部五个 seeds。

该对照沿用冻结的 10k 数据、512 Validation、既有 normalizer 和 K=32 PCA；隐层 RNG 恢复到原 classifier 训练后相同位置。逐 seed 保存曲线和原后处理指标，不删除较差 seed、不自动继续搜索初始化。它独立于 16k 不改配置的 learning curve，不能把两者混为数据量效应。

对照结果尚未产生时只报告提交/运行状态，完成后由网页自动读取汇总指标。原模型保留，不自动替换任何推理 provider。
