> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 本轮数据建设回报

结论：**离线设计、分区冻结、生成/验收/恢复/封存管线已补齐；真实模拟 BLOCKED，尚不具备正式科学训练条件。** 本轮没有重选模型、训练 tau head、启用 residual/PCA 或启动生产 MCMC。

1. **选定 native**：尚未获用户确认。候选完整 SHA256 为 `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`，source/物理表/config/后处理指纹已保存；真实原入口与 adapter 验收尚未运行。
2. **GLIBC/runtime**：未解决。当前登录节点 GLIBC 2.28，native 要求 GLIBC_2.29；无批准的兼容计算 runtime。未改系统、生产环境或 .so。
3. **PL 极限**：源码确认 MS=0.968 消除折断的代数条件，归一化和 HMF 路径已审计。已准备 KP=1/10/30 的隔离 native power/variance probes 及完整 history 对照，尚未执行、未宣称通过。
4. **10D 风险**：高 MS 积分/数值稳定性、超出场网格但仍影响 HMF 的 KP、z=35 早期电离与 z=5 中性延拓均未合格。只报告风险、不删域、不更改物理开关。
5. **448 点**：原设计文件和版本完整保留，全部是 Train 第一批候选，未分配到 validation/test。其坐标/sample ID 与 full train 前 448 条一致。
6. **计划/完成**：Train 4096/0、Validation 512/0、Sealed test 1024/0。另有 12 次 preflight（7 个不同参数点）和 24 challenge 点，均未提交、未生成。
7. **两套 view**：已分别覆盖。fixed KP10/MS2.5：Train/Val/Test 配额 384/128/256；continuous KP1/MS∈[0.5,2]：384/128/256。真正 active/fixed 与原 sampler 坐标从现有契约核对，科学 prior 没有修改。
8. **旧 45 条**：仍全部隔离，转入 Train 为 0。已知惩罚点只借用其开发参数位置安排新 preflight，不认可旧标签。初版 preflight 与开发修订留档，Train/Val/Test 不受修改。
9. **统一获批准 target**：没有任何新标签，因此不能声称已有获批准同源训练集。未来 worker 强制核对候选被确认后的 target/native/source/table/config/runtime/QA/实现 identity；旧 native 标签不混入。
10. **失败/资源**：完整 evaluation 尝试为 0，实际新模拟 core-hours 为 0，失败率、wall/RSS/CPU 利用/临时存储均未测量。12 次 preflight 的 16CPU×2h 硬上限提案对应最多 384 core-hours，不是成本预测。仅 history/redshift float64 数组为每条 512 bytes；元数据、LF、日志和加密开销另计。当前没有新标签存储。
11. **Sealed**：参数设计已冻结，标签未生成、未读。未来生成与解封分别授权；外部公钥、私钥隔离、模型/分析冻结是生成门槛。开发 loader 默认拒绝 sealed，公开回执不含曲线、tau、likelihood 或误差。本轮没有解封入口，也没有读取任何旧 sealed 数据。
12. **训练条件**：尚未满足。还缺 native 确认、获批准兼容节点/runtime、非零 preflight 与后续阶段预算、真实路径/PL 验收，以及足量合格 Train/Validation 标签。无需重写现有 Direct ResMLP；新的 loader 使用固定 split，不再事后随机拆分。

| Dataset | Planned | Attempted | Qualified | Quarantined/Failed | Label access |
|---|---:|---:|---:|---:|---|
| Preflight | 12 evaluations | 0 | 0 | 0 | Development |
| Train | 4096 | 0 | 0 | 0 | Training |
| Validation | 512 | 0 | 0 | 0 | Development |
| Challenge development | 24 | 0 | 0 | 0 | Development |
| Sealed final test | 1024 | 0 | 0 | 0 | Sealed |

所有新分区均**未提交、未生成**。旧 45 条 quarantine 单列，不计入新分区完成数。

软件验收覆盖：原 21 项测试，加分区、旧 448 保真、family 泄漏、sealed/symlink 拒绝、零预算拒绝、attempt/concurrency/core-hour/retry 限制、成功恢复、seed 不取模、原值保留与端点 warning 等新测试。科学 native 测量不能由这些测试替代，详见 results/data_pipeline_tests.txt。

原始科学源码/native/观测 fingerprints 已再次核对，不因本轮实施改写。提交脚本默认 dry-run；configs/budget.json 与新阶段预算均维持未授权和 0 attempts。
