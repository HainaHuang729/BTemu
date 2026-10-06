> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 尚未解决的科学域风险

这些风险不是已证明的失效，也不是删除参数点的理由。没有通过 emulator 插值消除风险，没有改变 target 定义。

- **PL 极限。** 本地 mode6 的 power 与 dsigma 分支在 MS=POWER_INDEX=0.968 时代数上消除 KP；sigma8 归一化使用相同 dsigma 积分。HMF 的 sigma_z0/source 路径继承这一输入。浮点运算、全局状态和积分器实际是否逐位 KP 不变，仍需预算内的 native power/variance 与 history 对照。未解释的 KP 依赖将阻止批量生成。
- **场分辨率与 source 不同。** BOX=250 Mpc，DIM=512 的轴向 Nyquist 约 6.434 /Mpc（9.49 h/Mpc）；HII_DIM=128 对应约 1.608 /Mpc（2.37 h/Mpc）。KP 全域对应 0.678–20.34 /Mpc，部分超过显式场的轴向 Nyquist。但 mode6 sigma_z0 在每个质量对应的半径 R 上积分到 350/R，sigma8 归一化上限约 29.6625 /Mpc，并不受上述 FFT 网格截断。不能据此断言高 KP 对 LF/history 无影响。
- **高 MS。** 原源码采用有限、随质量变化的积分范围和 GSL qag。MS 到 4 的收敛、误差状态、overflow 和源表插值可靠性尚未在本域验证。这里没有断言真实积分发散；也没有宣称任何整段参数范围已经数值合格。
- **红移端点。** z=35 时电离比例 >0.01、z=5 时中性比例 >0.01 被预注册为筛查 warning。它们可能提示范围外历史或原低 z 延拓不适用，但不自动将数值有效点变成失败。保留原范围、原数组和标记；阈值是工程筛查，不是新增科学精度判据。
- **输出与内部节点。** 32 个输出节点包含 5.9，并非全部内部 thermal/ionization 步。当前数据复现原 31 节点 tau 后处理，不能据此声称输出分辨率或 z 上界已收敛。
- **缓存/IC。** KP/MS 改变后即使 seed 相同，功率谱幅度和场仍可能变化。当前所有任务 regenerate=True/write=False，跨点缓存关闭；任何未来缓存需另行验证完整依赖键。新进程隔离避免长驻 native 全局状态串点。
- **target 版本。** 当前只有候选 repaired native，用户尚未确认；旧/新版本不混合。若发现影响 target 的 bug，停止此版本，创建新的 native/数据版本并明确重算范围。
