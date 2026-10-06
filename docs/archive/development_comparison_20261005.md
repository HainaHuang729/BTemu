# 当前合格数据开发比较（2026-10-05）

用户授权在数据生产继续期间冻结开发快照，开展覆盖审计、Direct ResMLP 和 NNERO-style 比较。此快照不替换 v1/v2 学习曲线、validation 或 sealed 设计。

冻结作业：2177072。结果目录：`artifacts/development_comparison_20261005`。实际训练作业号以该目录 `submission.json` 和 `status.json` 为准；排队不代表训练已开始。

快照从只读 dataset_manifest.sqlite 的单次读取取得已验收 Train 和独立 v2 Validation；文件 checksum、receipt、design、native/IC/config 和原 tau/xHI 后处理由现有 loader 重新验证。所有当时合格标签均保留，包括 classifier-negative、LF-invalid/history-valid 和 endpoint-warning histories。对照只使用原始 32 节点 history。

覆盖输出：coverage.json，包括按 split 的参数范围、过渡区、全零/全一、端点分位数、classifier 比例、LF 状态；这是成功条件下的开发快照，失败抽样分母仍以生产 registry 为准，不能称为完整 prior 无偏性能。

复用现有 Direct ResMLP、classifier 10→30→30→1、6×80 PCA MLP 和训练配置，保留 seeds 11/29/47/71/101。配置为 AdamW、physical history MSE、至多 1000 epochs、early stopping 60、gradient clipping 1。classifier 使用所有训练标签，regressor 使用 exact positive Train；PCA 只在 positive Train 拟合。K=4/8/12/16/20/24/28/32，physical/logit 表示分别验收 history、tau、xHI 与两项 likelihood。无候选通过时仍完成 classifier、记录 regressor 阻塞，不临时放宽阈值。

Direct 在所有 Validation 上评估；与 NNERO regressor 的比较使用相同 exact-positive Validation IDs，记录两者训练样本选择不同。ensemble 在物理空间平均；classifier false-negative/false-positive 单独记录，classifier 不作为 MCMC prior 或预测闸门。

输出训练曲线、checkpoints、PCA basis、normalizer、per-seed metrics 和 comparison_metrics.json。快照另保存 nested 1k/2k/4k/8k IDs，当前只运行全快照的有限比较；不声称这些新子集已训练，也不修改原学习曲线。

资源：快照 1 CPU/8 GiB/15 min，比较 1 CPU/8 GiB/8 h；生产与封存管线保持不变。生产 provider 不切换 decoder，不运行生产 MCMC，不读取 sealed labels，不发送邮件。

## 执行记录

冻结完成：Train 9080、独立 Validation 2048；positive 分别 3302 和 749；LF-invalid/history-valid 分别 1746 和 399，均保留。首次训练作业 2177077 在开始训练前暴露恢复标签没有 design 路径时旧 loader 的 v1 fallback 错误。失败日志完整保留，未修改标签。新增开发专用 resolver 从冻结 train/validation 注册表定位 sample_id，并调用原 validate_label；不扫描 sealed 数据，不改生产实现。修复后训练作业 2177093 已实际运行。
