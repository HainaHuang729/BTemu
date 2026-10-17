# 结果分析与下一步：2026-10-17

## Material Passport

- 模式：validate / plan；当前证据为 random_ic_v2 的 10k、16k 开发实验及既有128×8 IC审计。
- 原始报告和权重不改；本次无新模拟、无新训练、无MCMC、无sealed访问。
- 新增配对统计保存于 results/development_interpretation_20261017.json，输入SHA256、抽样单位与随机种子均保留。
- 下述路线是下一步建议，不能写成新增作业已经提交。

## 当前判断

Direct值得继续增加数据并验证；现有PCA+6×80 MLP主要应先解决训练拟合问题。与此同时，验证覆盖和random-IC推断语义是独立门槛，不能等待100k自动解决。

### 同一组183条positive Validation

| 指标 | Direct 10k | Direct 16k | PCA+MLP 10k | PCA+MLP 16k |
|---|---:|---:|---:|---:|
| Trajectory RMSE q95 | 0.03791 | 0.02372 | 0.36626 | 0.31423 |
| 绝对Δτ q90 | 0.003377 | 0.002568 | 0.030604 | 0.029141 |
| 绝对ΔlogLτ q90 | 7.819 | 6.690 | 101.961 | 125.237 |

Direct的positive子集RMSE q95下降约37%，τ误差下降约24%。但并非所有seed或所有样本都改善，也不能从两个N点外推“多少数据必定达标”。

在完整512条Validation上，Direct RMSE q95为0.02139→0.01957，绝对Δτ q90为0.001707→0.001207。约60.9%的trajectory RMSE下降；positive子集约61.2%下降。以整条theta trajectory进行2000次配对bootstrap，RMSE q95差值（16k−10k）的95% percentile区间：完整集合[-0.01137,0.00049]，positive子集[-0.03897,-0.00214]。这些是对已拟合模型和已用于开发选择的Validation的条件性描述，不是独立最终验收或posterior证明。

### MLP问题定位

10k时真实PCA系数可将原history重构到约1e-6，但神经网络预测误差大得多；K32表示误差不是当前MLP误差的主要来源。五个seed的训练平方误差中92.65%–98.11%集中在错误饱和输出上。只改变输出初始化的独立10k实验将RMSE q95由0.366降到0.305，但仍明显弱于Direct，且错误饱和问题保留。

16k的logit PCA K28已达到history RMSE q95约0.000932，但其绝对ΔlogLτ q95约0.04453，仍未通过预注册0.01的表示筛查；只有K32通过。目前没有证明PCA压缩收益，不能根据结果放宽门槛。

### 验证覆盖仍不足

当前512条random Validation均属broad抽样；两套原inference view和边界没有专门验证点。冻结的10k random Validation设计本身也只有broad点，因此增加broad验证不能替代单独的view/challenge检查。

已有412条LF-valid参考中，距本组最高exact总logL的2/5/10/25范围分别只有1/2/5/7个点。本次将16k模型的原后处理差值与同参数已保存的exact LF对齐：这些小组绝对总logL误差q90约1.011/0.914/0.908/0.856。样本太少，不能称作posterior样本，也不能从全域q90反推高概率区域已经准确。单参数点的LF保持相同，此计算未产生新的LF或history模拟。

### IC与classifier是另一层问题

既有128×8 IC审计中，theta层q90的IC标准差为：τ约0.000135、xHI(5.9)约0.00751、logLτ约0.122、logLxHI约0.945；13个family跨classifier边界，2个不在近cut区间。审计点是代表性/挑战加密开发点，不是无偏prior样本。

mean-history likelihood不等于IC-marginalized likelihood。既有审计中，logL(mean history)与log(mean likelihood over IC)的绝对差q90约0.308。更多随机训练点可能改善均值拟合，却不能自动消除两种推断目标之间的差异。

还有需要实测的选择偏差：每个theta只取一个随机IC，并只用classifier-positive histories拟合regressor时，边界附近对应的是经过允许条件筛选的IC分布；不能自动把其均值称作全部IC的条件均值。已有13个翻转family可用来检查该问题，不需要停止随机IC数据生产或混入fixed-IC训练。

16k classifier仍有3/183 false negatives（1.64%）。不能启用hard gate。模型最终科学精度阈值仍标为PROPOSED_REQUIRES_SCIENTIFIC_CONFIRMATION；IC审计的已确认门槛是另一份协议，不能混为“全部阈值均已确认”。

## 建议的下一步顺序

1. **数据继续，验证提前。** 保持32并发random-IC生产。优先从已冻结的10k Validation设计补足至2048，保留原512作持续learning-curve比较，新增1536单列补充开发验证。两套view和near-cut检查另建独立development challenge协议，不改变现有split或挪用sealed。
2. **Direct做32k嵌套比较。** 同一配置、同一512选择集、全部五个seeds，另报新增验证结果及tau/xHI两项likelihood。32k训练尚未提交；不根据两个N点承诺100k一定足够。
3. **MLP先过拟合诊断，再扩大实验。** 在固定32–128条真实positive Train上做有限过拟合试验，检查系数尺度、初始输出、各层梯度和错误饱和。未能拟合小数据前，不把追加全规模训练当作修复。任何后续变体单独预注册，保留现有Direct和原MLP。
4. **利用已有128×8审计比较模型与IC均值。** 核对theta重合与用途，分别计算模型对单IC、八IC均值、均值不确定度的误差；近cut family比较全IC均值与positive-only均值。八IC是有限参考，不能称作已知真均值，也不能用网络seed散布替代IC散布。
5. **最后做面向推断的开发验收。** 在独立、有足够覆盖的高likelihood开发点检验原LF+tau+xHI及分类false negatives；明确选择mean-history还是IC-marginalized likelihood的近似和误差预算，再进入posterior验证。生产MCMC与sealed test保持独立授权及冻结门槛。

优先资源投入建议：继续Direct learning curve与补充验证；NNERO-style保持有限诊断路线。所选BT native、原tau积分、LF、priors、随机IC设计和全部有效history标签保持原定义。


## 验收门槛与论文比较（2026-10-17补充）

最终模型精度协议仍为 PROPOSED_REQUIRES_SCIENTIFIC_CONFIRMATION；用户确认的是IC审计的保守开发门槛。PCA表示筛查另行预注册。当前Direct16k只有τ平均偏差满足最终提案的对应单项，模型、IC均值和posterior仍未验收。

NNERO论文对log10(Xe)做PCA，使用history与派生τ相对误差项；当前实现为logit(xHI) PCA加物理xHI MSE。量定义、训练方法和误差统计口径均有差异，不能直接比较“通过率”或把当前实验称为完整复现。

[完整门槛、确认状态、论文数据及比较](acceptance_and_nnero_comparison_20261017.md)。
