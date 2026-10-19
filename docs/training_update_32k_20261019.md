# 32k开发训练更新（2026-10-19）

已验收random-IC Train达到34,574条，满足原定32k学习曲线档位。复用原训练器提交32,000条Train、同一512条Validation、全部五个seeds（11/29/47/71/101）的比较。

作业2243610已提交，实际Slurm检查为RUNNING。分配1 CPU、8 GiB、最多8小时；先复核冻结数据、原后处理和来源，之后训练。作业RUNNING不等于梯度训练已开始。

原26k成员是本轮32k的完全相同前缀，Validation成员不变；冻结记录在artifacts/random_ic_development_32k_20261019。数据归一化仅拟合本轮Train，PCA仅拟合Train-positive。Direct、classifier、PCA+6×80 MLP沿用同一训练配置与physical-history loss，旧结果保留。本轮没有改变tau积分、LF、priors、native或随机IC设计。

昨晚失败点random_v2_train_029433已在相同seed下重试成功并验收入库，未恢复infrastructure failures恢复为0。当前数值失败6条，其中新增random_v2_train_030259，保持原失败记录。数据仍按64并发上限分波生成，波次尾段实际运行数会下降，collector完成后继续下一波。

本轮不读取sealed、不启动新MCMC；模型最终精度提案与IC审计门槛保持原定义。32k完成后才能新增对应学习曲线点，不能预填精度。
