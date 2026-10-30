# 新材料核查与论文采用记录：2026-10-30

来源：BTemu `dcd013159f913db0e4e37800f084bca3a9730a5c`，较前次 `3919aef` 新增 5 次提交。BTemu 已快进拉取；原有本地修改保留。21cmTB `09227c7` 与 Overleaf 原 `49519e0` 均无额外远端更新。

## 核查结论及采用范围

| 材料 | 核查结果 | 论文处理 |
|---|---|---|
| T2b 五条 BT 历史 | 共享同一导出的 8 个天体物理参数；32 个相同红移节点；所有值有限且在 [0,1]；原表插值/舍入与 JSON 一致 | 物理稿新增五条 BT 历史图、同节点的 BT 内部差值与固定参数表 |
| T2b 的“PL reference” | `kp=ms=0` 只是列表标签；该分支沿用外部 `configuration_for(plan,0)`，仍初始化 `ExactLuminosityFunctionProvider("btps",...)` 并调用 `cosmo_params_for(None)`。未显式固定独立 PL 分支。未取得底层代码，不能断定一定是错误的 BT 曲线 | 排除该系列，删除其作为新增 BT–PL 差值分母的用途；原始 JSON/脚本逐字保留 |
| T4 初始化 best 点 | 表与 JSON 一致，来自 `initialization.npz` 的 `global_best_bt/pl`；尚未证实是最终链的最大似然点 | 附录采用“stored initialization best points”，不称为最终最大似然估计 |
| T4b 链摘要 | 每模型 `8000×32×8`，脚本只读 `ensemble_1`，展平全部 256,000 行；未丢弃初始阶段；`std` 为 ddof=0。表与 JSON、(median−truth)/s 的算术一致 | 附录列真值、best、median 和样本标准差；明确不是可信区间、标准误或高斯显著性 |
| 生产数量 | 状态快照时间为 2026-10-30 08:33:26 UTC+8；train=85,020，validation=3,888 | 方法稿更新生产快照；65,536 模型与 512 条开发验证结果保持原定义 |

两个模型的恢复摘要都不能视为已合格的恢复结果。BT 的最大描述性 |median−truth|/s 为 2.7527868，PL 为 3.9971104；这不是对应显著性的宣称，也不能据此给出 PL 特有偏差或模型优劣。T4b 的八维都是天体物理参数，不能混同于“六个天体物理参数 + kp/MS”八维链。

## 已有文件与仍需补齐的证据

新文件只有导出 JSON、表格、PNG 和摘要脚本，没有 paired mock 的原始 checkpoint 或 initialization 文件。完整来源字节、SHA256、数值检查与图件摘要在 Overleaf 的 `paper/reproduction/data/material_update_20261030/`；可运行 `paper/reproduction/audit_material_update.py` 重现表格算术和 BT-only 新图。

为解决 PL 身份，需要回传：

1. `project_mcmc/workflows/MCMC/fixed_btps_posterior/handoffs/fixed_joint6_lx500_20261022/run.py` 和 `plan.json`；
2. 对应 `inference/exact_lf_provider.py` 及配置构造源码；
3. 本次六例实际 POWER_SPECTRUM、KP、MS、归一化、native、seed、网格与 flags 的运行记录；显式数值 PL 对照结果。

为资格化 mock 恢复，需要回传：

1. `paired_pl_bt_mock0_recovery_v1/initialization.npz` 和 `chains/{bt,pl}/ensemble_1/checkpoint.npz`；
2. 注入数据/噪声、likelihood、先验、固定谱、IC 和 native 身份；
3. 独立重复运行、初始阶段/稳态检查、适用收敛与 ESS、保留区间敏感性及实际恢复区间。

本次尝试通过已有 cuhk SSH 别名读取原文件，连接 chpc-login01.itsc.cuhk.edu.hk:22 超时，没有读取到集群文件。连接的 GitHub 21cm、SmallScalePPS-21cm、code 仓库树未找到对应源路径（仅说明未找到这些路径，不能排除其他命名）。未启动任何模拟、训练或采样；不凭摘要重建虚假的收敛统计。

## 正文调整

物理稿 v0.12：固定谱敏感性增加可用的 BT-only 对照；讨论/结论区分“恢复摘要已提供”与“正确模型恢复已验证”；附录保留完整配对表和统计限制。

原句：`A correct-model BT-to-BT recovery test has not been released ...`

修订：`The later paired export adds nominal BT recovery summaries, but has not qualified correct-model recovery: its raw chain rows, appropriate retained selection and independent diagnostics are still absent.`

中文说明：新的 BT 拟合摘要确实已经提供；目前缺的是能验证恢复质量的原始链、选样和独立诊断，不能继续写成材料完全不存在。

方法稿 v0.3：仅更新生产进度及其来源；原预测数组、开发验证指标、6D/8D/exact200 图、T6 统计和既有科学方程均不改变。
