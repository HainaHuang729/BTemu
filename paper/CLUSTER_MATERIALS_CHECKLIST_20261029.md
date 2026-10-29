# BTemu 论文补充材料：供集群读取的工作清单

日期：2026-10-29，Asia/Hong_Kong。

## 1. 任务目标与读取顺序

围绕 BT 修正的再电离模型补齐论文证据。优先复用已完成的模拟、预测和链；先核实已有产物，再安排缺少的计算。本文档给出后续集群工作的目标，本次上传不代表已经启动新的计算。

先读取：

1. [当前初稿](PAPER_DRAFT_20261029.md)。
2. [结果说明](RESULTS_20261029.md)。
3. [修订与核验记录](EDITORIAL_UPDATE_20261029.md)。
4. [链文件核验 JSON](DRAFT_SNAPSHOT_VALIDATION_20261029.json) 及脚本 `validate_draft_snapshot.py`。
5. 本清单，再读取对应实验的原始配置、合约和冻结产物。

当前上传入口是 `PAPER_DRAFT_20261029.md`。其他工作稿和历史规划可能对应不同材料组合；引用其结果前核对版本。源代码目录、checkpoint、数据划分、likelihood、先验、native 构建及 IC 规则均以对应计算的实际配置为准。

## 2. 文献依据及使用方式

- **Park et al. (2019)**：[全文](https://arxiv.org/html/1809.08995v2)，[摘要及版本](https://arxiv.org/abs/1809.08995)。重点参考 §2–3 的物理模型、Table 1 的参数/先验、§6 和 Figure 4 的分数据组合约束及观测量预测。借鉴其展示科学问题的方式；本项目的数据选择、宇宙学与参数范围应按实际实现单独列明。
- **21cmEMUv3**：[全文](https://arxiv.org/html/2606.00219v1)，[摘要及版本](https://arxiv.org/abs/2606.00219)。重点参考 §4、Table 2、Figures 2–3、Appendix A 的测试与误差展示，以及 Appendix B 的采样器和有效样本数比较。其重复 IC 均值测试针对功率谱；不能直接当作本项目 xHI 历史的既有验证。

这两篇文章的输出、物理模型和实验设置与 BTemu 不同。无需为模仿其架构而新增 diffusion、LSTM、七输出模型或 HERA/SKA 预报。

**比较指标时的重要细节：**21cmEMUv3 式 (11) 使用 `|y_true-y_pred| / max(|y_true|, y_floor) × 100`，中性氢比例的 floor 为 1。应复算同一观测量、同一聚合方式的指标；不能把 BTemu 的“逐 history RMSE 的中位数”直接与其逐点误差统计比较，也不能用功率谱误差代表 xHI 误差。该文 Appendix B 确实报告有效样本数和采样器比较；不能写成“对方没有采样诊断，所以我们的验收更严格”。嵌套采样的加权 ESS 与 MCMC 自相关 ESS 应分别按其定义报告。

## 3. 本地已核实的起点

| 项目 | 当前证据 | 集群侧需做的事 |
|---|---|---|
| 模型精度 | 原报告 65,536-history checkpoint：绝对轨迹 RMSE median 0.0010、q95 0.0101；绝对 xHI(5.9) q90 0.0079；绝对 τ q90 0.00070；history logL 误差 q90 2.44 | 找回 frozen metrics、验证成员、逐样本预测和 seed 汇总定义 |
| 数据生产 | 10 月 29 日 15:45 快照：train 83,756，validation 2,752 | 查询实际最新清单，注明时间；不要把生产数量当作该 checkpoint 的训练或测试数量 |
| 6 维链 | 5,000 × 32；最后 2,500 步有 80,000 个相关样本行；普通 split monitor 1.0340–1.0535 | 找原运行配置、独立重复及 ESS；不能标为所有参数已收敛 |
| 8 维链 | 6 astro + KP/MS，实际 5,568 × 32；最后 2,784 步有 89,088 行；普通 split monitor 1.1136–1.5125 | 核实 predictor、固定 X-ray 值、先验、续接和完整诊断 |
| 旧 exact 比较 | exact 200 步；旧报告中心差 <0.25σ、宽度比 0.85–1.09 | 找回确切比较样本；不能归给当前 5,000 步链 |
| IC 审计 | 128 参数族 × 8 IC；跨参数族 q90(std_IC logL_history)=0.9480653 | 使用原始重复 IC 结果分析均值预测及似然差异 |
| Mock 拟合 | 原表 χ²、中心差、宽度比仍可用作当前样本描述；整体验收标记 false | 找原始 CSV/JSON 和逐项诊断，检查 BT→BT 的恢复结果 |

核验脚本只读取链并计算描述统计，不启动 sampler：

```sh
python paper/validate_draft_snapshot.py
```

当前普通 split monitor 将相互作用的 walkers 分半，是描述性监测量。它不能代替独立链的 rank-normalized/folded R-hat 或有效样本数。

## 4. 任务与预期产物

### T0，第一优先：已有产物清点和配置对齐

检索以下原始位置及其最新对应目录：

- `project_bt_history_emulator/artifacts/random_ic_development_65536_20261026`。
- `project_bt_history_emulator/data_runs/random_ic_v2`。
- `handoffs/fixed_joint6_lx500_20261022/output/chain.h5`。
- `artifacts/posterior_check_emulator_chain_ext_20261028/chain.h5`。
- `artifacts/joint_kpms8_emulator_chain_20261028/chain.h5`。
- `experiments/bt_mock_pl_bias/results/final_summary`。
- `results/multi_ic_plan_20261027/POSTERIOR_RESULT_20261028.md`。
- 已完成的 IC 审计、学习曲线、训练回执和验证预测。

这些是已有记录中的定位线索，不保证每个集群工作目录都能直接使用相同相对路径。找不到的材料标记 missing，并记录已搜索的位置。

为每个拟纳入论文的计算保存：参数顺序、固定值、先验、采样坐标变换、native/checkpoint 摘要、观测数据及选择、τ 积分约定、IC 规则、步数/续接/留样区间、验证成员和指标定义。特别核实 ETA_STAR 与 F_STAR10 的变换及先验密度，以及“8 astro”与“6 astro + KP/MS”的身份。

产物：`material_inventory.json`、`run_configuration_table.csv`、缺失项列表。

### T1，必补：方法与参数表

从实际实现整理：

- 恒星形成、逃逸率、duty cycle、SFR→UV LF 的方程和参数意义。
- BT 修改的具体谱定义、k 单位、转折连续性、归一化，以及如何传入 halo abundance/collapsed fraction 计算。
- 参考谱的实现及其数值一致性检查；不要仅凭 MS=n_s 的代数极限宣称两条代码路径完全等价。
- emulator 的设计范围与每组推断的实际先验分别列出。
- LF 数据来源/红移/选择/误差处理、τ likelihood、xHI 单边约束及 τ 的积分范围与 helium 处理。

产物：方法补充 Markdown、参数/先验表、likelihood 定义和配置指纹。通常先用已有代码及运行记录补齐，不需要新模拟。

### T2，必补：固定天体物理参数的 BT–PL 物理图

在相同天体物理参数下比较 PL 与若干 k_p/MS 组合，展示 xHI(z)、相对 PL 的变化和 τ；可增加再电离中点或持续时间等派生量，但须明确计算定义、插值和有效红移范围。

已有 21cmTB 导出可用于物理展示，先检查其对应的历史/LF 图及脚本。其 256/768 网格与 plane-mean/light-cone 历史不能直接替代 BTemu 128/512 coeval 体积平均值的精度检验。需要配对解释时核实 IC 和归一化设置。

产物：物理历史图、源数值表、参数和历史定义说明。若已有数据不能形成匹配对照，再列出最少缺失的模拟。

### T3，必补：观测组合及后验预测

在同一组模型、先验、固定设置和观测选择下，比较 LF-only、LF+τ、LF+τ+xHI。展示加入每项观测后的参数变化和信息来源，并显式叠加 k_p/MS 先验。

从相应样本计算 LF 与观测点的对比、xHI(z) 和 τ 的预测分布。区分最佳拟合曲线、当前样本分布和通过诊断后的后验预测区间。

已有 LF-only 网格、联合链、Park 复现和近似 PL 参考可能使用不同数据点、宇宙学、固定参数或 native。先对齐 T0；不直接将它们叠加成“只增加了观测”的实验。

产物：数据组合约束图、观测量预测图、各项 likelihood/参数汇总表。需要新跑的组合单独列出。

### T4，必补：BT mock 的 matched recovery

先查已有 matched-recovery 实验。至少覆盖：PL mock→PL、BT mock→BT、同一 BT mock→PL。统一注入值、误差/噪声、likelihood、采样先验和诊断口径。

确认正确 BT 模型能恢复注入参数，再解释错用 PL 时的偏移。保留所有 mock，包括没有明显中心偏移的案例；报告中心差所用 σ 的定义、宽度比的参考分母，以及逐项链诊断。

产物：mock 恢复表、参数恢复/拟合图和诊断。完成前保留当前描述性结果，不将归一化偏移写成已确证的显著性。

### T5，必补：独立测试与误差图

先冻结待评估 checkpoint、normalizer、后处理和评价规则，按现有数据划分规则建立最终独立测试。early stopping 或模型选择用过的 validation 要与最终测试区分。

需要输出：

1. 一组真实/预测 xHI histories 及逐红移残差。
2. 全测试集逐红移的误差中位数、68%/95%分位区间，注明它们是误差分布区间。
3. 轨迹 RMSE、xHI(5.9)、τ、history logL 误差的分布与定义。
4. k_p/MS、转折阶段及先验边缘的误差分布和样本覆盖；单维分箱不等于已验证所有十维组合。
5. 五个训练 seeds 分别的指标；若推断使用 ensemble，另报真实部署预测的指标，注明先在物理空间平均还是其他组合。

已有开发集图可先整理，但不改名成独立最终测试。生产标签规模与本次测试样本数分别报告。若新增模拟，规模由覆盖和目标误差统计的不确定度决定，不照搬另一篇论文的样本数。

产物：冻结测试清单、逐样本预测/误差表、accuracy figure、指标 JSON。

### T6，必补：匹配的 exact–emulator 推断比较

确认 exact 与 emulator 使用相同观测、先验、固定参数、IC/预测目标和 τ/LF 实现。补齐参考采样，使用原实验的诊断要求评估；相关样本行数不能当作独立有效样本数。

比较完整分布、参数中心和宽度、相关结构及观测量预测。给出留样区间、独立重复/采样稳定性、有效样本数和计算成本。旧 <0.25σ 数字仅属于旧比较，除非按当前样本重新计算。

先完成固定谱的匹配比较，再完成带 k_p/MS 的关键验证。若中心接近但宽度或尾部不同，应如实展示。

产物：matched posterior/predictive comparison、诊断表和配置清单。

### T7，建议补：IC 条件均值与似然目标

先复用已有 128×8 开发审计，将同一参数的单 IC 历史、有限 IC 均值、均值估计不确定度与冻结 emulator 输出叠加。开发族参与过方法选择时，独立验证需另外区分。

分别测量预测误差和 IC 散布，评估八次实现的均值精度；不把与自身八次均值的零残差当成收敛证明。分清 `log L(mean history)` 和 `log(mean L over IC)`，保留当前 0.308246 差异定义。

0.9480653 是散布的分位统计，不是普适误差下限，不据此改写既定验收阈值。重复次数以均值误差证据决定，无需照搬 21cmEMUv3 的功率谱重复次数。

产物：IC 对比图、均值不确定度与似然差异表、对应目标定义。

### T8，建议补：真实成本和模型对照

在明确硬件、线程数和 batch size 下，分别测量 history prediction、τ 后处理、exact LF、完整 likelihood 及整次推断的成本。区分冷启动、稳态单点、批量预测、训练成本和摊销收益。

已有 Direct/PCA+MLP 对照和学习曲线优先复用，核对共同 validation、positive 子集与 ensemble 定义。若比较 LSTM 或其他方法，使用同一输出、训练/测试样本和误差定义。当前 416 s 模拟时间本身不等于端到端加速比。

产物：运行时间表、同口径模型/学习曲线图。

## 5. 推荐执行顺序与回传

1. **先清点及补写**：T0、T1，复用已有 T2、T3 图和学习曲线。
2. **再补最关键证据**：T4、T5、T6；配置不匹配时先解决匹配问题。
3. **再扩展**：T7、T8；按主结论需要决定额外计算。

最小主图集合：物理历史对比、观测组合与预测、独立测试误差、matched exact–emulator 比较。Mock 恢复与诊断可按论文篇幅放主文或附录。

建议在项目结果目录保存一个带日期的 `paper_materials` 目录，至少包含：

```text
material_inventory.json
run_configuration_table.csv
status.md
figures/                 # PNG + PDF，附源数据及脚本
tables/                  # 数值表，不只提供图片
metrics/                 # 指标、定义、样本/留样范围
manifests/               # 数据/native/checkpoint/config 的版本与摘要
```

`status.md` 对 T0–T8 逐项填写 complete / partial / missing、产物位置和剩余问题。没有完成的任务直接列出缺口；不从已有图的像素反推数值，不混入另一篇非线性结构论文的物质功率谱，不把历史快照写成实时状态。

本清单不替代当前生产资源配置和实验合约，不要求为展示效果改变标签、删样本、改变先验或放宽诊断标准。
