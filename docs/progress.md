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

Latest user authorization selects one independent random IC per theta. Controller 2194516 completed; array 2194518 started eight Train simulations on cn061 (128 CPUs at launch). Dependent validation/continuation job 2194519 is submitted. Maximum simulation allocation remains 256 CPUs. Mean-history and posterior fidelity remain unqualified. See [launch record](random_ic_explicit_start.md).
