# 论文提纲与证据映射（2026-10-29，同步核验版）

## 1. 当前章节

| 章节 | 内容 | 证据与状态 |
|---|---|---|
| §1 Introduction | 再电离物理问题和 emulation 需求 | 保留已有文献线索，投稿前补全引用 |
| §2 Model | 八个天体物理参数、k_p/MS 扩展和 coeval 历史 | `contracts/science_contract.json` 及对应原运行配置 |
| §3 Data and likelihood | 34 点 LF、τ、xHI；链的参数身份与先验 | 6 astro 和 6 astro + KP/MS 的 names 可从 HDF5 检查；固定值与 predictor 待配置 |
| §4 BTemu | 10→32 预测、训练设计和绝对误差定义 | 65,536 checkpoint；生产快照 83,756 train / 2,752 validation |
| §5.1 Results | PL 拟合 BT mock 的当前差异 | 原始 summary 与 `figures/fig1_bt_bias.png`；链诊断未全部通过 |
| §5.2 Results | 已发布链的描述性样本统计 | 6-D 5,000 步；8-D 实际 5,568 步；`DRAFT_SNAPSHOT_VALIDATION_20261029.json` |
| §5.3 Results | 旧 exact/emulator 比较 | <0.25σ、0.85–1.09 属旧比较；exact 200 步和 emulator 留样范围待复核 |
| §6 Discussion | IC 散布、似然目标、验证与采样范围 | `docs/ic_audit_completion.md`；保留原验收定义 |
| §7 Conclusions | 匹配当前证据的结论 | 预测误差与描述统计分开，不声明最终联合约束已取得 |

## 2. 结果口径

- **模型精度**：65k milestone 的绝对轨迹 RMSE 中位 0.0010、q95 0.0101；xHI(5.9) q90 0.0079、τ q90 0.00070、历史 logL 误差 q90 2.44。需补原始 metrics 与验证成员。
- **IC 散布**：128 参数族 × 8 IC，族间 q90(std_IC logL_history) = 0.9480653；与 emulator 误差 q90 的定义不同。
- **6-D 样本**：最后半段 2,500 步 × 32 walkers；普通 split monitor 1.0340–1.0535。所有参数收敛未验收。
- **8-D 样本**：6 astro + KP/MS，实际 5,568 步；最后半段 2,784 步 × 32 walkers，普通 split monitor 1.1136–1.5125。
- **学习曲线**：16k→65k 的已报告 logL 误差 q90 为 7.45→2.44，共同验证口径需核对。

## 3. Mock 拟合记录

来源：`experiments/bt_mock_pl_bias/results/final_summary/phase37_bt_mock_pl_bias_summary.json`。保留原报告值：

| case | χ²_min | 中心差 | 宽度比示例 |
|---|---:|---|---|
| pl_control | 42.4 | 0.006–0.06σ | 对照 |
| bt_kp10_ms2 | 150.9 | <0.04σ | ALPHA_ESC 5.6、L_X 9.9、NU_X_THRESH 6.7 |
| bt_kp10_ms3 | 432.2 | ALPHA_STAR 1.94σ、F_STAR10 1.29σ | ALPHA_ESC 5.9、NU_X_THRESH 31.9 |
| bt_kp10_ms4 | 248.7 | F_STAR10 2.03σ、ALPHA_ESC 1.23σ、M_TURN 1.54σ | NU_X_THRESH 14.7 |

该批 `all_combined_chain_gates_passed = false`。这些是当前拟合的描述性数值；需补逐项诊断和有效样本数后评估偏置显著性。

## 4. 待完成

1. 补 frozen metrics、验证成员、mock 原表和 exact 参考链。
2. 核实链段续接、先验、固定 X-ray/BT 参数、predictor 与积分约定。
3. 用匹配配置完成 exact/emulator 比较和充分链诊断。
4. 整理实际再电离历史图，标明 coeval 或 spatial light-cone 的采样定义。
5. 用相同观测量和误差定义开展文献精度比较，再决定是否作精度优劣陈述。
