# BTemu paper draft skeleton (following the 21cmEMUv3 structure)

Reference structure: arXiv 2606.00219 (21cmEMUv3) — Abstract; 1 Introduction; 2 Simulations and training data; 3 Emulator architecture; 4 Training and validation; 5 Performance; 6 Applications; 7 Discussion; 8 Conclusions; appendices (data tables, convergence, resolution).

## Abstract (target content)
- BT (blue-tilted) primordial power spectrum changes the small-scale matter distribution and therefore reionization timing and morphology.
- We train BTemu: 10-D → 32-node volume-averaged xHI(z) history, 100,000 training + 10,000 validation independent-IC runs.
- Accuracy: trajectory RMSE median 0.00085, q95 0.00556; xHI(5.9) q90 0.0046; tau q90 0.00034; dlogL q90 1.18.
- Forward-model speed-up ~6e6 over exact 21cmFAST at 250 Mpc/512^3.
- Applications: posterior on (KP, MS) marginalised over astrophysics; kp=1 vs kp=10 vs PL comparison.

## 1 Introduction
- Physics motivation: BT spectra from inflation/axion-like models; effect on small-scale power and structure formation.
- Observational status: UV LF, Planck tau, McGreer xHI; 21cm PS upper limits.
- Why an emulator: exact chains cost ~460 s per evaluation; sampling needs 1e5–1e6 evaluations.
- Existing emulators (21cmEMUv1-v3) and what is new here: BT tilt as a free parameter pair (KP, MS).

## 2 Simulations and training data
- 21cmFAST v3 configuration: 250 Mpc, DIM 512, HII_DIM 128, z 6–35, 16 threads, 416 s median per run.
- Design: Sobol 10-D over F_STAR10, ALPHA_STAR, F_ESC10, ALPHA_ESC, M_TURN, t_STAR, L_X, NU_X_THRESH, KP_h_Mpc, MS (120,120 points: 100,000 train / 10,000 validation).
- One unique IC per point (random_ic_v2) → labels in sqlite.
- Cost ledger: 100k+10k runs ≈ 200,000 core-hours, ~30 GB labels.
- Target definition: volume-averaged xHI at 32 nodes in z.

## 3 Emulator architecture
- ResMLP, 10 inputs → 32 outputs, 5 seeds, normaliser from training set.
- Per-seed training: 8 cores, 13.5 h for 100k points.

## 4 Training and validation
- Train/validation split, loss (MSE on normalised trajectories), seeds.
- Metrics table: RMSE median/q95, xHI q90, tau q90, dlogL q90 (65k vs 100k comparison).
- Noise floor discussion: single-IC label noise std_logL q90 ≈ 0.948, so dlogL ≤ 0.1 is unreachable; multi-IC averaging required.

## 5 Performance
- Accuracy vs redshift and xHI fraction.
- Cost and speed-up (exact 460 s vs emulator 8e-5 s).
- Where it fails: extreme tau, late reionization.

## 6 Applications
- MCMC at fixed (KP, MS): kp1, kp5, kp10, kp20 chains with the 100k model (3000 steps each, 16 processes).
- 8-D chain (KP, MS free): R-hat up to 1.084 on KP; kp/ms 95% credible intervals nearly span the prior → LF+tau+xHI alone do not constrain the tilt.
- PL vs BT overlay under the same constraint (contours only): shifts of 0.7 in ETA_STAR and 0.18 in ALPHA_STAR between kp1 and kp10.
- Physical interpretation of the pivot dependence.

## 7 Discussion
- Limitation: no 21cm PS term in the inference (PS emulator is fixed to KP=1, MS=1.5 and failed its sealed test with 6.1% improvement vs the required 10%).
- 8-IC pilot: 4→8 IC changes the mean target by only 1.25%, so IC noise is not the dominant error.
- Model capacity vs data volume.

## 8 Conclusions

## Appendices
- A: simulation configuration and design table.
- B: convergence diagnostics (R-hat, integrated autocorrelation).
- C: timing and cost ledger (TIMING_20261104.md).
- D: residual systematics (resolution, box size).

# Data the draft needs (inventory)

| item | path | status |
|---|---|---|
| 100k training labels | `artifacts/random_ic_development_100000_20261103/comparison_metrics.json` | ready |
| validation predictions | same dir, `validation_predictions.npz` | ready |
| 65k baseline metrics | `artifacts/random_ic_development_65536_20261026` | ready |
| design points | `data_runs/random_ic_v2/design.sqlite` | ready |
| 4-D fixed chains | `artifacts/kpms_scan_*_100k_20261031/chain.h5` | ready |
| 8-D chain | `artifacts/joint_kpms8_emulator_chain_*` | ready (R-hat 1.084) |
| PL chain | `artifacts/kpms_scan_pl_100k_20261031` | ready |
| corner plots | `results/corners_20261104/` | ready |
| PS sealed-test outcome | `results/phase60_*_evaluation.json` | ready |
| 8-IC pilot | `artifacts/ps_ic8_*` + `results/ps_ic8_diagnostic_20261103` | ready |
| timing ledger | `paper/paper_materials/TIMING_20261104.md` | ready |
| 21cmPS mock (fixed X-ray) | `artifacts/ps_mock_lx405nu500_20261104` | ready |
| PS+LF chain (5000 steps) | `results/joint_ps_lf_mock405_long_20261104` | running |
| 10-D PS pilot | `artifacts/ps10d_pilot_ms15_20261105` | running |

## Gaps to close before submission
1. An authorised PS likelihood (or a statement that PS is excluded and why).
2. A converged 8-D chain (KP R-hat ≤ 1.05) or an explicit statement that KP/MS are unconstrained.
3. Figure set: trajectory accuracy, xHI(z) examples, corner plots, PL vs BT overlay, cost table.
4. A decision on whether the 10-D PS emulator replaces the fixed-KP/MS one.
