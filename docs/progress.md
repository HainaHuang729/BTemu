# BTemu progress

Qualified data snapshot: 2026-10-07T12:11:29.263444+08:00 (Hong Kong time). Completed-wave receipts, not live Slurm occupancy.

## Completed

- Scientific contract, repaired-native qualification, exact adapter parity and PL-limit checks.
- Dataset v1: 4,096 qualified Train histories and 512 Validation benchmark histories. V1 Train is retained in the v2 total.
- Recoverable isolated data-generation pipeline, per-sample provenance and failure records.
- Development comparison: Direct ResMLP, classifier and PCA + 6×80 MLP; all five initialization seeds; 9,080 Train / 2,048 Validation. This is development evidence, not production acceptance.
- Frozen learning-curve runs completed: 2,048, 4,096, 8,192, 16,384 Train points, on the same 144-point v1 Validation benchmark.
- PCA representation audit: only logit K=32 passed the current reconstruction screen. No compression benefit has been established.

## Scientific-target transition

Fixed-IC production waves have stopped. Existing data retain their original labels and splits under the catalog alias fixed_ic_v1. Random-IC training is separate.

IC_AUDIT_V1: 128 theta families × 8 ICs; reuse 128 qualified fixed references and run 896 fresh realizations. Audit status: AUDIT_COMPLETED. Fresh qualified: 896. Classifier cut is derived from the original likelihood: 0.06 + 5×0.05 = 0.31. No classifier hard gate is enabled.

## Retained fixed-IC data

| Retained baseline | Qualified | Role |
|---|---:|---|
| Fixed-IC Train | 18,654 | Baseline / diagnostics |
| Fixed-IC Validation | 5,120 | Development reference |

- Learning curves: No incomplete submitted milestones in the latest receipt.
- Historical fixed-IC simulation concurrency cap (production stopped): 32 × 16 CPUs. This is a cap, not a live occupancy measurement.
- Accounted v2 worker allocation cost: 37,183.95 core-hours; median / q90 wall time: 415.5 / 496.6 seconds.
- Receipted numerical / infrastructure failures: 0 / 0.

## Pending

- Continue explicitly authorized random-realization production: 100k Train / 10k Validation. Audit scatter failures remain documented for model/inference validation. Fixed-IC totals are retained baselines, not random-IC training data.
- Complete 32k, 64k and 100k learning curves and final model selection. Different Validation scopes are reported separately.
- Reduce and qualify derived tau and each likelihood error, including tails. Current development models are not accepted for scientific deployment.
- Freeze model and analysis before separately authorized sealed-label generation and evaluation. Sealed labels generated/read: False/False.
- Independent posterior fidelity validation and production MCMC integration; no production emulator MCMC has been started.

## Publication and scope

Public aggregate snapshots are checked hourly. Queue and GitHub Pages deployment delays apply. Only qualified data counts and completed-training receipts enter the completed list; submitted jobs are not counted as completed. Source history labels, checkpoints, native libraries and sealed payloads are excluded. Email notifications remain disabled.

The emulator predicts only the simulator-defined 32-node volume-averaged global_xHI history. Tau uses original history postprocessing; LF keeps its exact provider. Endpoint warnings do not remove valid histories, and classifier-negative histories are retained. The reported PCA result is a completed audit, not evidence that compressed PCA is accepted.

Selected native SHA256: `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`.

Code exports are cluster-oriented templates with submission disabled by default. Production authorization is managed separately in the independent scientific workspace.

## Audit-gated random-IC launch

Submitted offline design job: 2190856. Last submitted scientific gate watcher (completed; no successor after gate failure): 2190857. Status: RANDOM_REALIZATION_DEVELOPMENT_PRODUCTION_STARTED. Parameter design frozen: True. The original wait-for-pass rule was superseded by explicit user authorization on 2026-10-10; see the launch update below. First eight evaluations, then waves of up to 128, maximum 16 simulations / 256 CPUs. See [launch record](random_ic_production_launch.md).

## Audit scheduler recovery

Final-wave Slurm array indices exceeded MaxArraySize=1001. Compact task-to-manifest mapping now preserves the original theta/seed schedule. Recovery controller 2192051: RESOLVED_COMPLETED. See [recovery record](ic_audit_scheduler_recovery.md). This historical audit gate was superseded for random-realization data production on 2026-10-10.

## Complete IC audit decision

896/896 new realizations qualified; all 128 families have eight ICs. Zero simulation failures. Cost: 1,694.12 allocated core-hours. **MULTI_IC_AVERAGING_REQUIRED** under the confirmed conservative development gates. At audit completion, random-IC production was withheld. It has since been explicitly authorized and launched, without changing the failed audit decision. Thirteen families change classifier label across ICs, including two outside the near-cut band. The 2/4/8-IC finite-reference comparison does not establish that eight ICs are sufficient. See [complete audit report](ic_audit_completion.md).

## Random-realization production launch

Latest user authorization selects one independent random IC per theta. Controller 2194516 completed; array 2194518 started eight Train simulations on cn061 (128 CPUs at launch). Dependent validation/continuation job 2194519 is submitted. At that launch the simulation cap was 256 CPUs; subsequent resource changes are recorded below. Mean-history and posterior fidelity remain unqualified. See [launch record](random_ic_explicit_start.md).

## Frozen random-IC data analysis

9,094 qualified Train histories analyzed (separate from live production counts): 3,372 classifier-positive, 5,722 negative; 24 within 0.01 of the cut. Positive-only logit PCA K=28 achieved in-sample trajectory RMSE q95 0.00134; independent Validation and K qualification remain pending. [Analysis report and plots](random_ic_data_analysis_20261013.md).

## Random-IC first development training

Status: DEVELOPMENT_COMPARISON_COMPLETED. Frozen 10,000 qualified random-IC Train histories; first 512 independent frozen Validation points brought forward, admitted 512. Five initialization seeds: 11, 29, 47, 71, 101. Direct ResMLP, 2×30 classifier, and positive-only PCA audit / 6×80 MLP reuse the existing training protocol. Seed is not a feature; fixed-IC labels are not mixed.

Validation array: 2208787; dependent training job: 2208789. Completed seeds (Direct / classifier / regressor): 5 / 5 / 5. Errors against independent single-IC labels include IC scatter. This is development validation, not conditional-mean or posterior acceptance. [Run protocol](random_ic_development_20261014.md).

## Direct random-IC MCMC interface development

Status: DEVELOPMENT_INTERFACE_VALIDATION_AND_SHORT_CHAINS_COMPLETED. Development job: 2216430; 16 CPUs, four-hour hard limit. Reuses 512 existing independent Validation histories, adding original exact LF and downstream comparisons; no new full-history simulations. Two functional short chains preserve the original fixed-view and continuous-MS priors. Classifier hard gate disabled; no posterior acceptance or production MCMC. Completed functional chains: 2/2. [Protocol and interpretation](random_ic_mcmc_development_20261015.md).

512 Validation LF checks completed: 412 LF-valid, 100 LF-domain failures with history retained. Original exact references reproduce and LF is unchanged. On the LF-valid subset, absolute total log-likelihood error q90 = 4.55574. These are development errors against random realizations, not posterior acceptance.

## Slurm metadata timeout recovery (2026-10-16)

A worker stopped before native evaluation because its Slurm allocation metadata query exceeded 20 seconds. The allocation was preserved and classified as infrastructure failure; native/scientific contracts were rechecked. Seven software regression tests passed. Recovery job: 2221082; resumed data array: 2221086; dependent collector: 2221087. Existing numerical failures are retained. No new model training or MCMC was submitted. [Incident and recovery scope](runtime_metadata_recovery_20261016.md).

## Concurrency update (2026-10-16)

User authorized 32 simultaneous data simulations, each with 16 CPUs: maximum 512 simulation CPUs. Applied to array 2221086 and future waves; live scheduler verification observed 32 running tasks. Physics, seeds, samples, per-simulation resources, and other jobs are unchanged. [Resource change record](concurrency_32_20261016.md).

## Model diagnosis and 16k learning curve (2026-10-16)

Checkpoint diagnosis: CHECKPOINT_DIAGNOSIS_COMPLETED; job 2221212. Nested 16k comparison: DEVELOPMENT_COMPARISON_COMPLETED; job 2221216. Same 512 Validation and five seeds, unchanged training protocol. Completed Direct / classifier / regressor seeds: 5 / 5 / 5. No new MCMC. [Development follow-up](model_followup_20261016.md).

Initialization-only MLP ablation: INITIALIZATION_TRIAL_COMPLETED; job 2221253; completed seeds 5/5. Same frozen 10k data, PCA, six hidden layers and physical history loss. Old results retained; this is one registered diagnostic experiment, not production model replacement.

## Acceptance criteria and NNERO comparison

Final model accuracy thresholds remain proposals requiring scientific confirmation. Confirmed IC audit gates and preregistered PCA representation screens are separate. Current logit(xHI) PCA / physical-history MSE differs from the paper log10(Xe) / relative history plus derived-tau training. [Threshold status and paper comparison](acceptance_and_nnero_comparison_20261017.md).

## Latest training update: 26,000 Train

Status: DEVELOPMENT_COMPARISON_COMPLETED; job 2234346. Same 512 Validation, unchanged configurations and five seeds. Completed Direct / classifier / regressor seeds: 5 / 5 / 5. This intermediate update retains the original 32k milestone. [26k protocol](training_update_26k_20261018.md).
