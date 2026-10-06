The emulator is a numerical surrogate of the selected BT-modified 21cmFAST forward model. Its purpose is to reproduce the simulator-defined volume-averaged neutral-fraction history over the frozen redshift grid. It does not impose additional completion-of-reionization, monotonicity, or optical-depth constraints beyond those already present in the reference simulation and downstream likelihood pipeline.

Emulator 的目标是忠实代理 selected BT–21cmFAST，而不是修正或重定义再电离历史。只要 exact simulation 输出有效，z=5 仍存在中性氢不构成训练标签无效；τ 完全通过原 history 后处理得到。

A. Emulator fidelity: compare emulated history with the original exact 32-node array. B. Downstream inference fidelity: apply the same original tau/xHI postprocessing and compare delta_tau, delta_xHI(5.9), delta_logL_tau, delta_logL_xHI and their history sum. C. Underlying physical-model validity: a separate scientific study which must never modify A's ground-truth labels.

Endpoint flags are SCIENCE_DOMAIN_WARNING only. Any finite in-range history on the exact frozen grid with valid provenance/IC/native/config and successful original postprocessing is eligible, including xHI(5)=0.2. Full ionization, monotonicity, smoothing or observational adjustment is never imposed. Positive xHI does not prevent compute_tau. LF grid failure may coexist with history_valid=true; such points do not establish LF+tau+xHI joint-likelihood validity.

Changes to redshift range, reference physics or tau convention require a new target/dataset/model version. This clarification adds metadata and reporting only; the original scientific contract hash, labels, split, priors, native and postprocessing remain unchanged.
