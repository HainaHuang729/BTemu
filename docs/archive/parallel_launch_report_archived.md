> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# 预检与隔离 Train 并行执行报告

状态：**TRAIN_BATCH1_RUNNING（候选标签生成；尚未科学入库）**。

已按用户新授权启用并行：预检 `2159786_1` 在 cn009；Train 数组 `2159806` 的任务 0、1 在 cn010，均已确认 RUNNING，每任务 16 CPU、2 小时上限。首批仅冻结前两条参数，不重采样。

cn010 的真实 runtime probe 为 `2159793`（第 5 个轻量作业），GLIBC 2.34，native 完整 SHA256 `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`，runtime fingerprint 与 cn009 相同。没有编译、更换 native 或改变原科学配置。

隔离产物即使机械 QA 成功也保持 `qualified=false`。原生成回执不可改写；只有完整 native qualification 通过并经原后处理再次校验，才创建独立 admission 回执并进入训练 loader。隔离路径及其符号链接默认拒绝读取为训练数据。35 项相关软件测试通过，不代表科学精度。

运行中的预检使用其已加载的历史实施版本；该版本已归档，并经显式 allowlist 接受用于 preflight。此次变动只涉及并行、隔离与入库机制；exact adapter、原后处理、label worker 科学调用代码保持相同指纹，没有修改正在运行的 Slurm 作业。

所有 core-hour、attempt 上限保持原授权：preflight 13/384、Train 480（最多 32 次基础设施重试）/2000、总计 2385。预检并发 1，Train 并发 2。目前共 48 CPU，未扩大到并发 8。

实时完成数及已消耗/预留成本见 `results/batch1_execution_status.json`。后续标签首先进入隔离候选池；native 未通过前入库数必须为 0。Sealed labels 未生成、未读取，未启动模型训练或生产 MCMC。
