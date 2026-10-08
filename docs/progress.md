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

IC_AUDIT_V1: 128 theta families × 8 ICs; reuse 128 qualified fixed references and run 896 fresh realizations. Audit status: WAITING_FOR_RECOVERY_CONTROLLER. Fresh qualified: 770. Classifier cut is derived from the original likelihood: 0.06 + 5×0.05 = 0.31. No classifier hard gate is enabled.

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

- Complete IC sensitivity audit and qualify one-random-IC versus multi-IC averaging before formal random_ic_v2 production (100k Train / 10k Validation). Fixed-IC totals are retained baselines, not random-IC training data.
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

Submitted offline design job: 2190856. Submitted scientific gate watcher: 2192048. Status: WAITING_FOR_COMPLETE_AUDIT. Parameter design frozen: True. Complete 128×8 audit must pass before any random-IC production array is submitted. First eight evaluations, then waves of up to 128, maximum 16 simulations / 256 CPUs. See [launch record](random_ic_production_launch.md).

## Audit scheduler recovery

Final-wave Slurm array indices exceeded MaxArraySize=1001. Compact task-to-manifest mapping now preserves the original theta/seed schedule. Recovery controller 2192051: WAITING_FOR_RECOVERY_CONTROLLER. See [recovery record](ic_audit_scheduler_recovery.md). No random-IC bulk simulation is released before the full audit passes.

## Queue snapshot

Checked 2026-10-08T11:32:23.844063+08:00. Audit uses zero CPUs; all 2048 reservation CPUs are allocated to existing jobs. Recovery job 2192051 is PENDING. Slurm estimated start 2026-10-10T11:20:00+08:00 is provisional. See [queue status](ic_audit_queue_status.md).
