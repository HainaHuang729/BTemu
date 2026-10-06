> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Architecture decision

Implementation candidate: shared ten-input Direct ResMLP, width 256, four pre-norm residual blocks with 256→512→256 SiLU, residual scale 0.5, final LayerNorm and 32-logit head. Linear weights use Xavier uniform initialization; biases zero. Inputs use train-only standardization with no second log transform. Parameters are the canonical eight followed by KP_h_Mpc and MS. All fixed cosmology and simulation settings remain in the contract.

One registered hyperparameter setting and five seeds (11,29,47,71,101) are specified. Physical-space history MSE selects checkpoints; original derived tau and likelihood remain deterministic validation. AdamW, scheduling, early stopping, clipping and finite maximum epochs are in configs/training.json. No architecture competition, auxiliary tau supervision or IC-variance interpretation of ensemble spread.

Direct is the executable candidate because PL compatibility fails and PCA is unqualified. It is not yet a selected scientifically validated deployment model. The same future qualified histories can be reused if residual/PCA gates are later met. Shared KP/MS coverage does not authorize changing either original sampler prior.
