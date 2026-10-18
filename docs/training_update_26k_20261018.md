# 26k训练更新（2026-10-18）

用户要求更新训练。本轮使用已验收random_ic_v2数据的前26,000条Train，原16,000条完全保留为前缀，同一512条Validation、同一训练配置与全部五个seeds（11/29/47/71/101）。这是新增中间比较，不改原32k milestone。

Slurm作业2234346已经提交，实际队列检查为RUNNING，位于cn060。分配1 CPU、8 GiB、最多8小时；先复核来源、checksum、IC、native和原后处理，之后启动训练。不能把作业RUNNING直接当成梯度训练已经开始。

复用原Direct ResMLP、2×30 classifier、train-positive PCA审计和6×80 MLP。继续使用physical xHI MSE；未新增tau head或loss，不混入fixed-IC标签。旧10k/16k及初始化对照checkpoint均保留，不替换推理provider。本轮保持原配置以测量增加数据的效果，不称作完整NNERO训练方法复现。

冻结记录：artifacts/random_ic_development_26k_20261018/intent.json、frozen_membership.json。实际snapshot须与冻结成员一致；结果与各seed曲线保存在同一独立目录。生产32并发仿真继续。未开启sealed或新增MCMC。

网页“模型诊断与下一轮”展示最新26k状态与各模型已完成seed数；尚未生成指标时不填入旧模型结果。
