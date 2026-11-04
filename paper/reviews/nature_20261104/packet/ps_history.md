# PS emulator programme: history, phases and diagnostics (2026-11-03)

Scope: `project_21cmFast/experiments/bt_matched_recovery` plus the standalone PS experiments under `project_21cmFast/experiments`. Inventory generated from the live contracts/design/data/results trees (`results/ps_phase_inventory_20261103/`).

## 1. Phase map (43 contract entries, phases 39–63)

| range | purpose | state |
|---|---|---|
| 39–41 | 180-cell view, grid head | predeclared → training contracts |
| 42–44 | fixed KP=1 / MS=1.5 views, combined view | frozen, executable |
| 45–48 | likelihood scope, two-part likelihood, variance floor, chunk-hurdle | frozen contracts |
| 49–51 | fixed-mock recovery, out-of-fold UQ, targeted transition generation (1,000) | executed |
| 52, 52b–52g | direct BT combined view and sub-experiments, xHI auxiliary | generated |
| 53–56b | LSTM2D and mean-recovery attempts | phase56b failed development gates |
| 57–60 | 4-IC mean training set (7,804 θ), phase59 model, phase60 independent sealed test | **phase60 failed** |
| 61–63 | tail diagnosis, 10-D training-asset audit | scripts + audit |

Standalone experiments that predate / sit beside the phase numbering: `bt_mock_pl_bias`, `btkp1_25_phase_inverted`, `btkp10_25_phase_inverted`, `pl25_phase_inverted`, `pl_exact0048`, `phase_pair_highz_2026-10-07`, `kp10_lowz_2026-10-13`, `hmcode_reed07_*`, `mah_halo_errorbars`.

## 2. Six exploration directions

1. **PS representation and architecture** — 180-cell 2D PS (20 k × 9 z); grid head, residual head, PCA+ridge, LSTM2D (row = redshift, column = k), chunk-hurdle. LSTM2D won decisively (q90 linear error 11.4% vs 1654% for PCA+ridge).
2. **IC noise and multi-realization averaging** — single realization → unique IC → 4-IC mean (phase58, 7,804 θ) → 8-IC mean (phase55b, 494 θ); phase54b is a 256×4 pilot. The 4-IC mean improved the curve q90 by 22.9% over the legacy baseline, but the sealed test still failed.
3. **Likelihood and statistics** — two-part likelihood (positive and zero power treated separately), variance-floor sensitivity, chunk-hurdle comparison, shifted-log transform log10(P+0.01). The shifted-log transform suppresses the low-power cells' relative-error blow-up (q90 ≈ 4.19%).
4. **Recovery and mock tests** — fixed-mock recovery (phase49), targeted transition sampling (phase51), 128-theta recovery (phase55b), exploratory mock MCMC. PS alone does not constrain eight astrophysical parameters: the exploratory MCMC shifted ALPHA_ESC by 3.7σ.
5. **Sealed-test discipline** — phase60: 256 independent θ × 4 IC, opened once. Result: **not passed** (relative improvement over baseline only 6.1% vs the required 10%), while test/development ratios of 0.97–1.07 show no overfitting.
6. **Numerics and diagnostics (21cmFAST side)** — resolution check (PL25), HMF diagnostic, IC normalisation/velocity, HMcode comparisons, phase-inverted pairs, early growth, independent small box, k-space component diagnostics. Resolution and box-size systematics of 5–20% are independent of the emulator.

Phase 63 was a 10-D (including kp/ms) training-asset audit, i.e. the programme had already started moving toward the current 10-D BT dataset.

## 3. Headline numbers to remember

| item | value |
|---|---|
| phase59 development q90 (linear / shifted-log / curve) | 11.4% / 3.90% / 0.088 |
| phase53 legacy baseline q90 | 14.2% / 5.27% / 0.115 |
| PCA+ridge baseline q90 | 1654% / 104% / 1.32 |
| phase60 sealed test q90 | 11.0% / 4.19% / 0.094 (improvement 6.1%) |
| independent check (4 fresh 21cmFAST runs, our emulator) | median 4.0%, 68% 7.9%, 90% 24% |

## 4. Open questions

- Is the remaining error dominated by target IC noise (4 ICs) or by model capacity? The 8-IC pilot on 105 θ is designed to answer this.
- Can PS-alone inference be trusted, or must PS enter jointly with LF + τ + xHI? Current evidence favours joint.
- Does the improvement gate (10% over baseline) need redesign, given that precision gates already pass?
