# Direct random-IC 的 MCMC 开发联调

本轮把已训练的五成员 Direct ResMLP 接入原 LF + τ + xHI pipeline，执行有界功能测试。**不启动生产 MCMC，不发布经过验收的 posterior 约束。** 最新回执在[项目网页](https://hainahuang729.github.io/BTemu/#mcmc-development)显示。

## 保持的科学定义

网络只输入 10D 物理参数，输出 32 节点体积平均 global_xHI；random seed 不作为输入。成员先解码，再在物理 xHI 空间平均。τ 完全来自原 tau_from_history / selected native compute_tau；LF 和观测 likelihood 保持原实现。

原来的两套 inference view 不修改：固定 KP=10、MS=2.5，以及 KP=1、MS∈[0.5,2]。保留 ETA_STAR 转换、prior 与 Jacobian 语义。新的 random-IC 开发 view 单独版本化，不把 fixed-IC target 和 random-IC checkpoint 静默混用。

这一步没有新建 KP/MS 联合采样 prior，也没有把训练矩形域当作新的科学 prior。当前在预测 history 上求 likelihood 的近似，尚未证明等价于对 IC 边缘化的 likelihood。

## 检查顺序

1. 软件回归测试：保留原 prior 与坐标；拒绝 native、红移、后处理不一致；覆盖域错误不能冒充 LF 插值失败。
2. 计算节点加载获准 native，核对 checkpoint 和来源 hash。分别测试两套接口的原 prior、共享输入 history 的原 τ/xHI/总 likelihood 一致性；LF 做 A→B→A 状态一致性检查。
3. 复用训练中未参与拟合的 512 条 Validation histories，补算同一参数点的原精确 LF。分别比较 history、τ、xHI、各项 likelihood 与总和；LF 无效时保留 history 并单独计数。
4. 两套视图各运行 32 walkers、10 步 burn-in、100 步留存的短链。初始化和采样 seeds 预先冻结，全部使用现有 emcee 实现；不启用 classifier hard gate。

Validation 曾用于 epoch/model selection，因此这是 development validation，不是封存测试。按该验证样本内最高 exact likelihood 划分 ΔlogL=2/5/10/25 的诊断分组，不能将这些分组称作 posterior credible region。

## 适用域与失败

开发阶段采用仅从 Train 拟合的最近邻几何检查；它不是已经校准的精度适用域。超出检查域时明确报错，不改成零 prior。仅保留原 sampler 明确定义的 LF 网格错误处理；native NaN、来源错误和 emulator 覆盖错误均显式失败。

第一次软件检查捕获了 DomainError 与 LF 错误的区分问题，原作业在调用 native 前被拦截。失败日志和旧实现身份保留，修正后重跑；没有用此次软件测试产生科学性能结论。

## 资源和完成含义

单作业最多 16 CPU、8 GiB、4 小时；不新增完整 history evaluation，不改变当前模拟生产并发。运行期间冻结权重、normalization、分析协议和原 prior。

“短链完成”只代表有有限概率、接受移动且接口正常，**不代表收敛、posterior 重加权有效、IC 边缘化成立或科学部署通过**。后续仍需与开发链支持区域匹配的独立 exact 检验，以及模型冻结后的封存验收。Sealed labels 本轮不生成、不读取。


## 已取得的开发验证结果（2026-10-15）

作业 2216430 的五项软件回归测试通过。实际计算节点加载指定 repaired native；两套原 prior / 参数转换、共享 history 的原后处理与 likelihood 一致性、LF A→B→A 检查全部通过。此项接口检查不等于 emulator 与 exact history 已达到科学误差要求。

512 条已有 random-IC Validation 全部完成 LF 检查；412 条可比较完整 likelihood，100 条发生原 LF 网格域错误，原 history 全部保留。412 条的已保存 exact τ/xHI/likelihood 参考均逐值复现，同一参数点的 LF 在 exact 与 emulator 比较中保持不变。

| 指标（412 条 LF-valid Validation） | q50 | q90 | q95 |
|---|---:|---:|---:|
| trajectory RMSE | 0.002828 | 0.013613 | 0.020573 |
| absolute Δτ | 0.000163 | 0.001595 | 0.003269 |
| absolute ΔxHI(5.9) | 0.002055 | 0.015503 | 0.028358 |
| absolute ΔlogLτ | 0.04271 | 1.66939 | 5.91192 |
| absolute ΔlogLxHI | 0.47998 | 2.74803 | 4.17730 |
| absolute ΔlogL总和 | 0.91641 | 4.55574 | 8.23935 |

分位数按独立参数点计算；参考是每点一个随机 IC realization，所以误差同时包含 emulator 误差和 IC 散布。各项 likelihood 分别保留，不能用总和抵消来掩盖误差。LF-invalid 的 100 条不属于这张完整 likelihood 统计表，但仍属于有效 history 数据。

相对该 Validation 样本内最高 exact likelihood，ΔlogL≤2/5/10/25 分组分别仅有 1/2/5/7 条。数量不足以验证 posterior 支持区域，这些组也不是 posterior 区间。

本次测得单点中位耗时：history 网络约 4.05 ms、原 LF 约 265.53 ms、两次原 τ/xHI 后处理合计约 3.75 ms。不同分项的中位数不能相加当作实测端到端中位数；现有 exact generation 的计时范围不同，暂不宣称端到端加速倍数。

开发短链的实时进度和完成回执由网页自动更新；本表不以短链完成代替科学验收。
