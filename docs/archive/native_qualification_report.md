> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Gate 0：native/runtime 状态

**BLOCKED；没有进行真实完整 evaluation。**

候选修复 native 完整 SHA256：

`3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`

位置：project_mcmc/workflows/MCMC/fixed_btps_posterior/deployments/ts_stable_strict_20260928/src/py21cmfast/c_21cmfast.cpython-310-x86_64-linux-gnu.so。

旧审计 native：

`80b30c5c5c4bb32949db8664e852054c43a73e7ac6ac397f57925ea0f89bad9c`

selected_native_contract.json 保存完整绝对路径、source fingerprint、物理表 hashes、科学配置和后处理 hash，但 confirmed=false。旧发布的 regression_gate 不是本次数据 adapter 的 native qualification，也不是用户对新数据目标的确认。

已在当前 chpc-loginb 登录节点做无模拟的链接/import 检查：系统 GLIBC 2.28；候选动态库依赖 GLIBC_2.29，因此 import 失败。实际成功导入 package/加载 native 路径为空，不能把候选路径伪称为已加载路径。没有替换 GLIBC、native 或进行重编译。详见 results/runtime_qualification.json，含 ldd、依赖文件 hashes、解释器、包版本、可用编译器和 ABI 字长。可用 gcc 版本不是该 .so 的实际 build provenance。

真实运行仍须在每个计算节点上执行同一检查；批准一个 fingerprint 不等于绕过逐节点 import/链接验证。核数固定 16，源 IC RNG 按线程分配 seeds，不能任意调整线程数后声称数值/IC 完全相同。

seed 源码证据：outputs.py 把原 Python 整数传入 native；21cmFAST.h 声明 unsigned long long；GenerateICs.c 将其交给 gsl_rng_set 并生成/打乱每线程 seeds。725213656658 在 64 位 unsigned long long 内。运行契约要求 unsigned long 和 unsigned long long 均为 8 字节。输出对象的 effective seed 尚未实测；worker 将逐节点核对并保存。GSL 内部 RNG 初始化属于冻结实现，未手动取模，也不把不同 model initialization/design seed 当作 IC。

preflight 12 次包含：基准 original/adapter、original repeat；PL KP=1 original/adapter、KP=10/30 adapter；continuous view original/adapter；KP=1/MS=4 强修改 original/adapter；已知受 xHI 惩罚的开发参数重算。只在 selected native 下比较全部节点、tau 输入/输出、观测插值、LF 原数组字节和各 likelihood。首选逐位相等；不通过时先看 original repeat，不事后放宽 tolerance。

PL probe 在隔离子进程导出 native power_in_k 和 sigma_z0，覆盖统一 k/mass 网格。此脚本尚未在可加载的 native 上实测，符号可用性与积分行为也属于 preflight 验收。当前 results/pl_limit_checks.json 仅记录静态代数预期，不宣称 native KP 不变性通过。
