# BTemu progress

Qualified data snapshot: 2026-10-07T09:16:30.346034+08:00 (Hong Kong time). Completed-wave receipts, not live Slurm occupancy.

## Completed

- Scientific contract, repaired-native qualification, exact adapter parity and PL-limit checks.
- Dataset v1: 4,096 qualified Train histories and 512 Validation benchmark histories. V1 Train is retained in the v2 total.
- Recoverable isolated data-generation pipeline, per-sample provenance and failure records.
- Development comparison: Direct ResMLP, classifier and PCA + 6×80 MLP; all five initialization seeds; 9,080 Train / 2,048 Validation. This is development evidence, not production acceptance.
- Frozen learning-curve runs completed: 2,048, 4,096, 8,192 Train points, on the same 144-point v1 Validation benchmark.
- PCA representation audit: only logit K=32 passed the current reconstruction screen. No compression benefit has been established.

## In progress

| Dataset | Qualified | Target | Remaining |
|---|---:|---:|---:|
| Train v2 | 18,432 | 100,000 | 81,568 |
| Validation v2 | 4,608 | 10,000 | 5,392 |

- Learning curves: 16,384: DEVELOPMENT_TRAINING_RUNNING
- Configured simulation concurrency cap: 32 × 16 CPUs. This is a cap, not a live occupancy measurement.
- Accounted v2 worker allocation cost: 35,794.48 core-hours; median / q90 wall time: 415.5 / 496.6 seconds.
- Receipted numerical / infrastructure failures: 0 / 0.

## Pending

- Complete 100,000 qualified Train and 10,000 independent Validation histories.
- Complete 32k, 64k and 100k learning curves and final model selection. Different Validation scopes are reported separately.
- Reduce and qualify derived tau and each likelihood error, including tails. Current development models are not accepted for scientific deployment.
- Freeze model and analysis before separately authorized sealed-label generation and evaluation. Sealed labels generated/read: False/False.
- Independent posterior fidelity validation and production MCMC integration; no production emulator MCMC has been started.

## Publication and scope

Public aggregate snapshots are checked hourly. Queue and GitHub Pages deployment delays apply. Only qualified data counts and completed-training receipts enter the completed list; submitted jobs are not counted as completed. Source history labels, checkpoints, native libraries and sealed payloads are excluded. Email notifications remain disabled.

The emulator predicts only the simulator-defined 32-node volume-averaged global_xHI history. Tau uses original history postprocessing; LF keeps its exact provider. Endpoint warnings do not remove valid histories, and classifier-negative histories are retained. The reported PCA result is a completed audit, not evidence that compressed PCA is accepted.

Selected native SHA256: `3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`.

Code exports are cluster-oriented templates with submission disabled by default. Production authorization is managed separately in the independent scientific workspace.
