> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Representation audit

Direct decoder is sigmoid of all 32 logits, with no PCA, no monotonicity or smoothing constraint, and no tau head. Every member is decoded before ensemble averaging in physical xHI.

Conditional logit-residual decoder and train-only SVD/PCA functions are implemented and tested. Residual construction fails unless compatibility is explicitly passed; PCA additionally requires reconstruction acceptance. Both are disabled for this dataset. The PL incompatibilities already prevent the main residual candidate from proceeding.

scripts/development.py representation computes clipping-only and exact-projection reconstruction errors in physical history, observed xHI, original derived tau, and separate original likelihood components for every eligible K. It fits only train and measures on development validation. Proposed representation budget is 20% of each total error budget. Explained variance alone is never a gate. Endpoint epsilon is 1e-5 and clipping effects are separately measured.

No scientific PCA reconstruction experiment has been run: there is no qualified train/validation dataset and the selected native cannot load on this execution host. No compression benefit or passed reconstruction gate is claimed. Synthetic full-rank reconstruction and endpoint tests are software evidence only.
