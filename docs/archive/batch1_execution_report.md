> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 本轮实际执行报告

状态：**PREFLIGHT_FAILED**。Runtime 阻塞已解除，但第一条 preflight 被助手误取消；不能把它解释成 native 的科学验收失败或通过。本轮尚未达到启动训练标签生产的目标。

## 作业

| 阶段 | Job ID | 实际状态 | Allocation | 样本范围 |
|---|---|---|---|---|
| Runtime probe | 2159716 | COMPLETED，import 通过 | 1 CPU，4 s；cn004 | 无完整模拟 |
| Runtime probe | 2159717 | CANCELLED，未运行 | 0 CPU，0 s | 冗余 EPYC 探测 |
| Runtime probe | 2159724 | COMPLETED，runtime ready | 1 CPU，4 s；cn009 | 无完整模拟 |
| Preflight | 2159722_0 | CANCELLED，已计一次尝试 | 16 CPU，38 s；cn009 | normal_original |
| 诊断恢复 probe | 2159730 | COMPLETED，未找到产物 | 1 CPU，0 s（sacct 秒级计数） | 仅查找本次取消作业私有日志 |
| Train batch 1 | — | 未提交 | — | 冻结前 448 条 |

四个轻量作业合计低于授权的六次；没有额外完整模拟。

## 数据

| Dataset | Planned unique points | Attempts | Qualified labels | Failed/quarantined | Remaining |
|---|---:|---:|---:|---:|---:|
| Train batch 1 | 448 | 0 | 0 | 0 | 448 |

Preflight 单独统计：冻结 12 次 evaluation、7 个唯一点；1 次尝试被中断，0 次完成、0 条合格。它不是额外训练数据。旧 45 条记录仍隔离。

## 直接回答

- GLIBC/runtime：在实际 cn004、cn009 上确认 AlmaLinux 9.6 / GLIBC 2.34；现有 Python 环境可用，未替换系统库或 native。
- 两个 runtime probe 实际加载的 native SHA256 均为 `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`。实际 package/.so 路径、动态依赖和 source 指纹见对应 JSON。被中断完整 evaluation 的独立 runtime 文件未恢复，不以 probe 冒充该 worker 的完整 provenance。
- Runtime fingerprint：`6fc2f3625507e495eb6db8c157d59941e8b71a04688da79729b104951fda460c`。
- 原入口/adapter 对照：未完成，未通过。
- PL 极限数值检查：尚未运行，未通过。
- 正式训练标签：未开始，合格数 0。
- 所有本轮作业已终止；后续预检、Train 及依赖作业均未提交。未修改任何既有 MCMC 作业。
- 高 MS 数值稳定性、PL KP 不变性、红移端点覆盖风险仍未解决。
- Sealed labels 仍未生成、未读取；未运行科学模型训练或生产 MCMC。

## 成本与中断

实际分配成本合计 **0.171111 core-hours**：preflight 0.168889，探测 0.002222。所有作业已对账，当前未结清预留 **0**。预检 batch step 的峰值 RSS 为 3,846,736 KiB；由于运行被中断，这不是一次完整模拟的峰值/耗时测量。完整模拟存储、CPU 利用率和科学数值失败率尚不可估计。持久日志与回执字节数见 `results/batch1_execution_status.json`。

调度事故：查询时作业仍 PENDING；对节点和 Requeue 的组合更新返回错误，但节点更新实际已生效。助手随后错误地依据过时状态取消作业，此时它已在 cn009 运行。此次尝试和成本没有删除。诊断恢复作业未找到可验收文件，不能推断标签成功。后续取消应使用 Slurm 条件状态过滤，不能依赖先查询后取消来保证未启动。

## 已落地的授权与保护

历史零预算已归档到 `contracts/authorization_history/20260928_batch1/`。当前阶段预算为 preflight 12/384 core-hours、Train 480 次（最多 32 基础设施重试）/2000 core-hours，仅允许 initial_448 manifest；其他科学阶段仍关闭。

保留原 AttemptLedger 与提交入口，补齐 sacct 确认后的预留释放，待运行/未对账作业保留完整上限；禁用 Slurm 自动 requeue；未知代码错误、超时/OOM 不自动当成可重试基础设施故障；非 sealed worker 日志改为持久存储以保留中断证据。相关 25 项软件测试通过。一次扩大到全部测试的运行在原有 synthetic 训练测试处被系统终止，因此不宣称完整 46 项测试通过。

## 恢复门槛

首条消耗了冻结 12 次尝试中的一次。目前原预算不允许额外补跑，也无法在剩余 11 次中完成全部 12 项验证。已经请求仅将 preflight 尝试上限改为 13、允许补跑被误取消的 normal_original 一次，384 core-hours 与总预算不变；尚未收到该新增授权。不得借用 Train 重试额度、替换样本或忽略中断尝试。

机器记录 `results/native_qualification.json` 的 `qualified_for_batch1=false`，生产门禁保持关闭。当前仅可运行以下只读恢复检查；这不是新的模拟提交：

```bash
source scripts/environment.sh
"$BT_HISTORY_PYTHON" scripts/reconcile_allocation.py --budget-id 20260928_batch1
"$BT_HISTORY_PYTHON" scripts/qualify_native.py --budget-id 20260928_batch1
"$BT_HISTORY_PYTHON" scripts/collect_dataset_status.py
```
