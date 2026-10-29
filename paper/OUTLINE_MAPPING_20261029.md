# 论文提纲映射（Park 2019 结构 → 本论文，2026-10-29）

作者：HNHuang。范围：仅 21cmFAST 与 BTemu，不含 SWIFT/物质功率谱材料。

## 1 节映射与素材位置

| Park 2019 章节 | 本论文对应 | 已有素材（路径） | 状态 |
|---|---|---|---|
| §2 天体物理模型（8 参数、质量依赖、非均匀复合） | §2 BT 修正模型：在 8 参数基础上增加 KP、MS 两个 BT 维度 | 模型定义见 `project_mcmc/.../contracts/fixed_btps_joint_muv20_v1.json`；参数先验见 `project_bt_history_emulator/contracts/science_contract.json` | 文字可直接写 |
| §3 观测约束（LF、τ、xHI） | §3 同（HST+Donnan 34 点 Muv>-20、Planck τ、McGreer xHI） | 数据与选择规则在 `fixed_btps_joint_muv20_v1.json`；似然实现 `inference/non21_likelihood.py` | 已有 |
| §4 推断方法（21cmMC） | §4 两条线：exact 21cmFAST MCMC + BTemu 代理 MCMC | exact 链 `handoffs/fixed_joint6_lx500_20261022/output/chain.h5`（200 步）；emulator 链 `artifacts/posterior_check_emulator_chain_ext_20261028/chain.h5`（2000 步）；8 维链 `artifacts/joint_kpms8_emulator_chain_20261028/chain.h5` | 链在跑/已跑，收敛待补 |
| §5.1 LF 单独约束 | §5.1 LF 对 BT 参数的约束 | `experiments/bt_matched_recovery`、`experiments/bt_mock_pl_bias/results` | 需整理成图表 |
| §5.2 加入 τ、xHI | §5.2 联合约束与 BT 参数偏移 | 6 维/8 维链的后验均值与宽度（已有数值） | 数值已有，图未出 |
| §5.3 仪器预报（HERA） | §5.3 21cm PS 层面的 BT 可探测性 | PS25 流水线：`article_figure_check_2026-07-08/ps25_paper_format_job2289693`（含 kp10 z=0） | 图已有，需按论文版式重排 |
| §6 结论 | §6 结论与限制 | — | 待写 |

## 2 本论文新增的两块（Park 2019 没有）

| 板块 | 素材 | 状态 |
|---|---|---|
| A. 21cm PS 的 BT 依赖（z=1.07、z=0，sim/HMcode） | `phase_supplement_kp10_0048_job2234368`、`phase_supplement_kp10_0056_job2288271`；比值 0.744–1.024（z=0） | 数据完整，可直接出图 |
| B. BTemu 精度与后验一致性 | 精度：`artifacts/random_ic_development_65536_20261026/comparison_metrics.json`；一致性：`results/multi_ic_plan_20261027/POSTERIOR_RESULT_20261028.md` | 精度表已有；链长待补 |

## 3 可直接引用的结果数字（来自冻结产物）

- 65k emulator：轨迹 RMSE 中位 **0.0010**、q95 0.0101；xHI(5.9) q90 **0.0079**；τ q90 **0.00070**；ΔlogL q90 2.44。
- 单 IC 噪声底：ΔlogL q90 **0.948**（`results/ic_sensitivity_report.json`）。
- 后验对比（6 维）：中心偏移 **< 0.25σ**，宽度比 0.85–1.09。
- kp10 z=0 PS：sim/HM **0.744–1.024**，118 bins，1024³ NGP。
- 学习曲线：16k→65k 的 ΔlogL q90 = 7.45 → 2.44。

## 4 缺口（写进 §6 限制或先补）

1. 8 维 KP/MS 链收敛（当前 R̂ 1.28–1.75）。
2. validation 1,728/10,000；若要报“100k 训练”必须补齐或改写为“83k”。
3. LF 单独约束那组图（`bt_mock_pl_bias/results`）还没整理。
4. 21cm 光锥是 32 节点 coeval 汇总，不是真正光锥，需在方法里说明。

## 5 下一步（按顺序）

1. 把 §5.1 的 LF 结果整理成一张图 + 一张表（读 `bt_mock_pl_bias/results`）。
2. 用现有链出 §5.2 的后验图（6 维，标注未收敛）。
3. 把 PS25 图按论文版式重排，作为 §5.3 主图。
4. 写 §2–§4 的方法文字（可直接引用契约与已发表公式）。
5. 等收敛后补 §5.2 的正式后验与 §6 结论。


## 6 已找到的关键结果（BT mock 用 PL 模型拟合的偏置）

来源：`experiments/bt_mock_pl_bias/results/final_summary/phase37_bt_mock_pl_bias_summary.json`（10 个 mock case）

- `pl_control`：χ²_min = 42.4，各参数偏移 0.006–0.06σ（自洽对照）。
- `bt_kp10_ms2`：χ²_min = **150.9**，宽度比（相对 PL 对照）ALPHA_ESC 5.6、L_X 9.9、NU_X_THRESH 6.7，参数偏移仍小（<0.04σ）。
- `bt_kp10_ms3`：χ²_min = **432.2**，ALPHA_STAR 偏移 **1.94σ**、F_STAR10 **1.29σ**，宽度比 ALPHA_ESC 5.9、NU_X_THRESH 31.9。
- `bt_kp10_ms4`：χ²_min = **248.7**，F_STAR10 偏移 **2.03σ**、ALPHA_ESC 1.23σ、M_TURN 1.54σ。

**结论方向（可写进 §5.1）**：用非 BT 模型去拟合 BT mock，χ² 显著变差、后验明显变宽，且当 ms 偏离 1.5–2 时部分参数（ALPHA_STAR、F_STAR10、M_TURN、ALPHA_ESC）出现 1–2σ 系统偏移——这是“BT 信号不能被 PL 模型吸收”的直接证据。

**限制**：该批 case 的 `all_combined_chain_gates_passed = False`，因此这些数字只能作为方向性结果，正文需注明链诊断未全部通过。
