> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 10D 数据建设计划与当前状态

Material Passport：academic-research-suite / experiment-agent；离线实现与软件验证。没有完整 native evaluation 或封存标签读取。

共享输入、fixed IC 和 32 节点输出沿用 science_contract.json。训练分布是各分层独立 LHS 批次与预定义 anchors 的混合；不是两套 MCMC 的新 prior，也不称为一张整体 LHS。F_STAR10、F_ESC10、M_TURN、L_X 保持现有 log10 坐标，KP 使用 h/Mpc 后乘 h=0.678 传入 native。原 ETA_STAR 转换不变。

| Dataset | Planned | Attempted | Qualified | Quarantined/Failed | Label access |
|---|---:|---:|---:|---:|---|
| Preflight | 12 evaluations（7 个不同参数点） | 0 | 0 | 0 | Development |
| Train | 4096 | 0 | 0 | 0 | Training |
| Validation | 512 | 0 | 0 | 0 | Development |
| Challenge development | 24 | 0 | 0 | 0 | Development |
| Sealed final test | 1024 | 0 | 0 | 0 | Sealed |

全部**未提交、未生成**。旧 45 条隔离记录另计，合法转入 Train 为 0。0 次尝试不能报告为 0% 失败率；失败率和实际完整 evaluation 成本均未测量。以上 preflight 单位是完整 evaluation，包含原入口/adapter 对照及重复，不把它们当作独立训练样本。

## 分区与版本

| Stratum | Train | Validation | Sealed test |
|---|---:|---:|---:|
| Broad 10D | 3072 | 256 | 512 |
| Fixed view | 384 | 128 | 256 |
| Continuous MS view | 384 | 128 | 256 |
| PL anchors / KP-MS edges | 256 | 0 | 0 |

旧 448 点保持原 JSON、sample IDs、坐标和各批设计 seed，全部进入 Train，且是 train_full_design 的前 448 条。补点构成独立 LHS 批次。256 anchors/edges 包含旧 64 edges、32 个天体物理 family × 3 个 PL-KP 点、96 个新 edges。同一个 PL family 不跨集合。训练共有 4096 不同物理点；其中 PL 扫描 family 相关性必须保留。

train、validation、test 使用不同设计随机流。主 manifest 与 SHA256 已冻结。检查完全重复、归一化坐标 12 位舍入重复、family 交叉、旧开发参数重合；未发现 train/validation/test 泄漏。最近邻距离只作参数几何报告，不用于事后清空 test 周围训练点。

preflight 初版及设计契约保存在 contracts/design_revisions。随后开发侧修订 preflight_penalty_v1a：用旧隔离记录 regression_0 的参数重算一个已知惩罚点，替换冗余 adapter repeat。原入口 repeat 保留，仍为 12 次。此操作只借用参数定位开发挑战，未认可或转入旧标签；Train/Validation/Test manifest 字节保持不变。`generate_design.py` 对现有修订冻结只核验，不覆写。新目录重现顺序是 generate_design.py 后 amend_preflight_penalty.py。

## 阶段、预算与执行

现有 configs/budget.json 未被改成授权。新的 configs/data_stage_budgets.json 同样 authorized=false、max_evaluations=0，各阶段 cap=0、重试=0、并发=0。阶段配额是计划，不是预算。preflight 提案为最多 12 次、每任务 16 CPUs、16 GiB、2 小时硬上限、并发 1；最坏分配上限 384 core-hours，不是预计耗时。必须经确认后方可执行。

所有提交和 worker 均核验完整 native 身份、批准的 runtime fingerprint、冻结科学/数据/QA/实现 hash、非零阶段与总预算、Slurm account/partition/核数/内存/时间上限。非 preflight 还要求原入口 parity、真实 PL power/variance 与 history KP 不变性通过。所有 expensive history 均使用一个新进程；PL cheap probes 另用短进程避免改变 history 进程的全局状态，其成本包含在该 preflight allocation。

`submit_data_array.sh` 默认仅打印命令；必须加 --submit 才可能调用 sbatch，且零预算仍拒绝。已保存的命令含待确认 account/partition，不可直接提交。提交登记和 worker 尝试分别加锁；失联或状态未定的登记不自动重发。每条记录独立保存，成功后恢复跳过；基础设施重试必须有剩余预算，参数、seed、native、物理配置不变。数值失败和 schema 失败默认不自动重试、不重抽点。所有 attempted 与 retry 成本保留。

## 单一管线

现有 ExactHistoryAdapter 和 OriginalPostprocessingAdapter 被复用；模型和 decoder 未重写。generate_labels.py 是新统一入口 generate_history_label.py 的兼容转发，不再维护另一套自由设计生成逻辑。

每条记录保存设计/family/split、canonical 参数、适用的原 sampler 坐标、requested/effective IC seed、native/source/物理表/config/后处理/runtime/管线指纹、32 个原精度 history、派生参考量、LF/likelihood references、attempt、成本和状态。默认不保存三维 cubes。LF 若含非有限的无效 bins，会保留原数组 NPZ 与数组字节 hash，JSON 明示非有限标记；不将它们当 xHI 零标签。

机械 QA 不对 xHI 做归一化、平滑或 clip。超出 [0,1] 的小偏差也隔离原值；数值失败的紧凑 raw history 单独保存。端点风险仅加 science warning，不删除有效点。生成后的 JSON、独立 checksum 和 receipt 必须完整，才可加入 qualified_development manifest。

load_development 的 v2 路径核验 frozen sample IDs/splits、receipt 和 checksum；split_groups 对有冻结 split 的记录不再随机拆分。训练和 validation 标签只能通过显式 manifest 读取，无 dataset glob。

## 封存与成本

当前只有 Sealed test 参数设计，没有标签。未来生成需要独立授权、科学模型/分析冻结、外部保管私钥的公钥，以及批准的 worker/key-custody 隔离。worker 将标签、原始日志及中间紧凑文件一并公钥加密，只发布有限回执。开发 loader 在读取前拒绝 sealed split、sealed 路径、符号链接指向的 sealed 路径和密文扩展名。本轮不提供解封入口。

目录权限不能阻止同 UID 的全部访问，所以不将 mode 0700 夸大成完整隔离；外部密钥与批准的执行隔离仍是硬门槛。原 test 分母固定 1024；没有自动备选点。未来任何备选设计必须单列、不能抹去原失败分母。

预算使用 allocation 核数。receipt 中的 worker envelope 成本不是完整 scheduler 会计；reconcile_allocation.py 只读取本管线记录的 sacct 信息，实际 allocation core-hours 以终态 ElapsedRaw × AllocCPUS 计算。缺失 accounting 时明确 unknown，并保留全部 reserved 上限，不能用成功样本均值掩盖失败成本。
