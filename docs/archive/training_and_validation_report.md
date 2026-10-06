> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Implementation and validation report

Material Passport: academic-research-suite / experiment-agent, inline; verification status SOFTWARE_TESTED_SCIENCE_PENDING; 2026-09-28.

1. **Prediction:** only full volume-mean global_xHI(z), 32 nodes from the current TS-on entry point. No tau, LF, PS, temperature or electron-fraction head exists.
2. **Tau:** delegates to original tau_from_history with z_min=5, z_max=35, 31 interpolation nodes, then frozen native compute_tau. Original interpolation/clipping/helium semantics remain untouched. Unit tests check delegation and interpolation using a labelled stub; real selected-native parity is not yet run.
3. **Inputs:** canonical order F_STAR10 [-3,0], ALPHA_STAR [-0.5,1], F_ESC10 [-3,0], ALPHA_ESC [-1,0.5], M_TURN [8,11], t_STAR [0.01,1], L_X [38,42], NU_X_THRESH [100,1500] eV, KP_h_Mpc [1,30], MS [0.5,4]. Log10 coordinates remain stored log10 coordinates. Underlying sampler ETA_STAR conversion and priors are preserved. User confirmed PL no-break MS=0.968. Coverage is a design domain, not yet a validated predictive domain.
4. **IC:** fixed-IC target, seed 725213656658. No ensemble-mean or IC-variance claim. Model-seed ensemble averages decoded physical histories.
5. **PL:** incompatible cosmology, photon conservation, minimum redshift and M_TURN domain. Residual disabled; no measured benefit. Local standard-PL forward versus PL EMU comparison is not run because compatibility already fails and no extra exact simulations are budgeted.
6. **PCA:** train-only fitter, exact-projection reconstruction/likelihood evaluator and gates implemented. Scientific reconstruction has not been run or passed; direct output remains uncompressed.
7. **Decoder:** Direct sigmoid is the implementation candidate. No scientific model-selection verdict or production weights yet. Conditional residual/PCA code is tested but intentionally not activated.
8. **Acceptance:** software tests pass. History, derived quantities, real likelihood approximation and posterior acceptance all remain NOT PASSED / NOT EXECUTED. Thresholds are explicit proposals awaiting scientific confirmation; they are not relaxed based on outcomes. Exact original Python split-normal and neutral-fraction kernels are used in unit regression tests, including both sides of tau mean and an xHI-penalized history.
9. **Measured work:** actual merged configurations, sources and native hashes read; existing profiling/cache reports reused; 57 explicitly enumerated development regression reports inventoried, 45 matching-native successful records extracted (32 fixed-view, 13 continuous-MS-view), remaining native/config mismatches excluded. All 45 remain quarantined because original complete source fingerprints and native postprocessing qualification are incomplete. No training data were fabricated, clipped or imputed. Software tests include five registered seeds trained for two epochs on a synthetic fixture solely to validate optimization/checkpoint/reload code; temporary fixture checkpoints are deleted. Scientific training, learning curves, coverage qualification, independent posterior checks and sealed final test are unperformed.
10. **Speed:** no measured scientific emulator end-to-end acceleration. Existing audit exact median 673.29 s is from five local old-native points, not the expanded domain. The old LF ~0.377 s and tau pipeline ~0.000847 s remain historical audit numbers, not a new emulator benchmark. scripts/benchmark_joint.py measures the complete preserved LF + tau + likelihood path once qualified weights exist.

## Data and resources

One proposed 448-label initial design: 256 broad 10D LHS, 64 fixed-view points, 64 continuous-MS-view points, and 16 on each of four KP/MS edges. It does not certify full coverage; LF-guided, transition, constraint-boundary and numerical-failure refinement require development evidence and a separately bounded extension. Original priors do not change. Learning-curve runner uses nested 1k/2k/4k/8k subsets when enough qualified labels exist.

At old local cost, 448 labels would be approximately 1,341 core-hours (16 cores/label), excluding failures, queue time and tails. Extreme KP/MS and astrophysical corners are unmeasured and may cost more or fail. This is a budget estimate only. No jobs submitted; configs/budget.json has authorized=false, max_evaluations=0.

## Remaining scientific decisions / blockers

- Candidate target is strict repaired native 3211a662…, while old audit native is 80b30c5c…. User confirmation of native choice is still pending. No mixed-native training is allowed.
- Current execution host lacks required GLIBC_2.29. Use a compatible pre-existing compute runtime; do not overwrite the original library or silently recompile.
- Qualify development-source provenance and recalculate original tau/xHI references; obtain broad-domain labels under a concrete approved budget.
- Confirm precision proposals, then train all five seeds, compare finite candidates, validate penalized xHI regions and each original inference view separately, and perform independent exact posterior validation.
- Freeze all artifacts and analysis before separately authorized sealed-test evaluation. No current artifact is authorized for scientific inference.
