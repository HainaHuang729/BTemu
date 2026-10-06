# BT-xHI Dataset v2：100k 扩展执行记录

2026-10-04，用户明确授权 100,000 qualified Train、10,000 independent Validation、5,000 sealed 参数设计。本轮不生成或读取 sealed labels，不启动生产 MCMC。

科学对象维持 selected repaired native `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`、fixed IC requested seed 725213656658、原分辨率/TS/热与重组计算、32 节点体积平均 global_xHI。τ 经原 tau_from_history / compute_tau 派生。原科学计算与 label QA 源码未改；v2 迁移仅扩展冻结设计注册、预算和调度，验收文件本身未改。

## 数据和分区

- v1 Train4096 的合格 histories 全部计入 100k，未生成部分仍由 v1 流水线生产；不会重复模拟或用旧 45 条 quarantine 替代。
- v1 Validation512、sealed design1024 原样保留为 v1 benchmark，不纳入新 Train，也不覆盖。
- v2 新 Train primary 95,904 点，另冻结 4,096 个有限 reserve candidates；v2 Validation primary10,000、reserve1,024；sealed 独立参数设计5,000。
- reserves 只用于原 primary 已尝试后的有限补充，原失败分母、坐标和所有 attempts/receipts 始终保留。有限设计用尽仍不足时报告不足，不无限重抽。
- 采用独立 scrambled Sobol 随机流：Train2026100401、Validation2026100402、sealed2026100403。生成 base2 点集后使用声明的 prefix；Train 约80% broad、10% 两个 inference views、10%边界映射。最终分层/截断结果不称为严格平衡 Sobol net。
- 参数定义为现有存储坐标，不重复 log10。与全部 v1 参数设计做精确和归一化12位舍入去重；各 family 保持 train/validation 分离。
- 冻结契约 `contracts/dataset_design_v2_100k.json`，分片 `manifests/v2_100k/`，每片最多512条。原 v1 契约不覆盖。

## 实际调度

离线设计 job2167012 完成；激活/入库检查 job2167025 完成并真实提交首批。

- 首批 exact Train array：2167026，16条，初始并发16，cn061–062。
- afterany 机械验收/续跑：2167027，等待首批结束；上游失败也会进入汇总，不只依赖 afterok。
- 16→32→64 ramp：前16条检查通过后32并发；v2累计512 attempts且无系统错误时最多64。参数配置 `configs/v2_100k_budget.json` 的 max_array_concurrency=64；原 v1 8并发保持。
- 每条16 CPU、16GiB、2小时，CPU/物理线程保持原契约。仅 tkcastrosim / tkcastrosim1 / cn057–064，Slurm 负责实际分配。058–060现有重要作业不修改。
- 每个 array 至多512slots，遵守 MaxArraySize=1001；不是提交100k独立作业。受限 submitter 原样复用，每个 sample 独立产物、原子回执；独立 controller 每片验收后提交下一片。
- attempts 上限有限，infrastructure failure 每点最多重试一次；timeout/OOM/numerical/provenance 不自动重试。现有 user core-hour cap removal 继续有效。v2 存储硬限500GiB，超过即停止追加；此限是运行保护，不是实际容量预测。
- STOP_AUTOMATION 可阻止追加，不取消已在运行的正常模拟。native/config错误、系统性失败或无效数组会保留产物并要求核查。

## 吞吐证据

`results/v2_throughput_reference.json` 来自 repaired native 的2088条真实 qualified receipts：median420.879秒，q90 498.209秒；抽样83条最高peak RSS7878.6MiB；sample产物median328380字节。

据此，64并发满负载的中位数容量约547 histories/hour，约13.1k/day；每1000 core-hours约535 histories。这里是容量估算，不是实测64并发吞吐；queue、广域边界成本、验收及失败都会改变实际速度。总生产约需数十万 core-hours，不能承诺特定完成日期。每日/每片以实际新合格数更新。

## 数据内容与 classifier

原标签不修改，正负类别都保存。基于已验收的原插值值：classifier_label=int(xHI_5p9 <0.31)，同时保存连续xHI_5p9、原logL_xHI、derived_tau、history/lf/tau组件有效性。0.31只是本轮开发 classifier 定义，不修改科学 prior 或 likelihood。

索引：`data_runs/dataset_v2_100k/dataset_manifest.sqlite`，包含参数、原label与receipt路径/checksum、native/source/config/seed、Slurm/attempt、资源、quality flags及完整32节点history；`classifier_metadata/` 为逐样本sidecar。worker不并发写巨大中央JSON，SQLite仅受单一controller锁写入。原始失败回执保留；failure_registry为当前状态汇总。

## 模型和 learning curve

8个 nested 参数ID子集已冻结：1024→2048→4096→8192→16384→32768→65536→100000，见 manifests/v2_100k/learning_curves。完整family不跨subset；缺失失败标签不能静默替换。已有 Direct ResMLP 的2048/4096 controller保持；2048/4096 NNERO comparison 自动复用已完成的 Direct benchmark；8192→100000 各规模分别触发 Direct 与 NNERO comparison，最多7个额外有限训练作业、一次仅1个。数据不足时不提交。固定144条验证用于同协议learning curve，完整v2验证10k保持独立评估。不能声称未提交规模已经执行。

新增 NNERO-style classifier10→30→30→1（ReLU）和6×80 hidden PCA MLP，保留5 seeds、有限训练配置和physical xHI MSE。PCA K=4,8,12,16,20,24,28,32，只fit对应Train positive。分别审计 raw physical PCA 与预注册epsilon=1e-6的logit PCA；epsilon影响单独记录，原标签不变。选择只依据history、tau、xHI(5.9)和两项likelihood表示误差；不能仅看explained variance。物理PCA非法重构不clip，不通过则禁止该decoder。

`maintenance/v2/baseline.py` 为可重复入口，首轮实际开发 job2167058，使用现有冻结1024 Train/144 Validation，先PCA audit，再符合development screen才训练regressor；classifier保留所有正负样本。此screen不是科学部署验收，最终likelihood/posterior门槛仍独立。软件检查 job2167057已通过；不等于科学精度。

这是对BT volume-mean xHI target的NNERO-style架构适配。原NNERO论文的目标是free-electron history，不能将其性能或WDM物理直接搬到BT；本实现也不搬用其tau loss或积分器。[NNERO 原论文](https://arxiv.org/html/2503.11261v1)

## dots 和恢复

v2监控入口：`results/dataset_progress.json`、`results/dataset_progress.md`。v1原入口docs/progress_for_dots.md和results/dots_progress.json保留。JSON带时间、attempts、qualified、失败、classifier比例/直方图、资源及system stop原因；array间自动刷新。

手动只读状态汇总（需兼容项目Python；仅读开发labels，仍核对checksum，不读sealed）：

```bash
source /oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/scripts/environment.sh
"$BT_HISTORY_PYTHON" /oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/maintenance/v2/advance.py
```

核查无未决提交/系统错误后，断点续跑用同一命令加 `--submit`。它复用有限授权预算与已验收skip机制。不要重新运行activate.py：该脚本用于身份迁移，不是日常resume。

封存5k只是参数设计，原sealed policy和key isolation仍生效；本轮没有创建sealed labels或解封事件。


## 首批实测追加

首批16/16已合格，首个shard剩余496条自动提交2167059（32并发），依赖验收2167060已提交；检查通过将升64。此时100k尚未完成，Validation v2尚未开始；v1 Validation512已完成。

1k NNERO-style开发已完成（2167058）：classifier五seed validation accuracy 0.90278–0.94444，false negatives 3–6/144。logit PCA只有K32通过该轮表示筛查，没有压缩收益；raw physical PCA连满rank也有浮点端点范围问题，不clip通过。候选不获得部署授权。2k Direct已完成2167094，NNERO同数据comparison2167134已提交。

初次1k NNERO开发记录有snapshot/config但未在启动时完整冻结实现文件hash，属开发原型；不能追溯声称已完整模型冻结。后续learning-curve作业明确保存driver/models/baseline/config/snapshot SHA256，防止实现漂移。
