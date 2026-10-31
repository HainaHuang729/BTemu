# T7 — IC conditional mean and likelihood target (from the 128×8 audit)

Source: `results/ic_sensitivity_report.json` (status COMPLETE; 128 families, 896 fresh IC realizations + 128 reused fixed-IC; classifier cut 0.31; sealed data untouched).

## Dispersion of the single-IC target

| quantity | q50 | q90 | q95 | max |
|---|---:|---:|---:|---:|
| trajectory IC scatter RMS | 0.000288 | 0.00313 | 0.00371 | 0.00516 |
| std tau | 2.86e-5 | 1.35e-4 | 1.90e-4 | 2.74e-4 |
| std xHI(5.9) | 1.25e-4 | 7.51e-3 | 1.37e-2 | 2.20e-2 |
| std logL_tau | 0.0035 | 0.122 | 0.194 | 0.326 |
| std logL_xHI | 0.028 | 0.945 | 1.425 | 2.182 |
| std logL_joint_history | 0.077 | **0.948** | 1.438 | 2.210 |

## Single IC versus the finite-IC mean

| quantity | q50 | q90 | q95 | max |
|---|---:|---:|---:|---:|
| max abs difference (fixed IC vs 8-IC mean) | 0.00075 | 0.0134 | 0.0172 | 0.0278 |
| trajectory RMSE (fixed IC vs mean) | 0.00019 | 0.00288 | 0.00364 | 0.00700 |
| Δ logL(mean history) − logL(IC marginal) | −0.0025 | 1.2e-7 | 6.0e-7 | 1.908 |

## Reading

- The single-IC label noise floor is **0.948** in ΔlogL_joint (q90), which is why the 0.1 acceptance threshold used earlier is unreachable with one IC per parameter point.
- The 8-IC mean differs from a single realization by 0.013 in xHI (q90 max-abs) and by 0.0029 in trajectory RMSE — consistent with the IC scatter above, i.e. the mean is a distinct, smoother target.
- `ΔlogL(mean history) − logL(IC marginal)` is essentially zero in the bulk (q90 ≈ 1e-7) but reaches 1.9 in the tail: for those families the mean-history likelihood and the IC-marginal likelihood differ measurably, so the two targets are not interchangeable everywhere.
- Consequence for the paper: report the emulator target explicitly as the **finite-IC mean** (or per-realization), and quote accuracy against that target; do not compare emulator errors to single-realization scatter.

## Caveat

Only 8 realizations per family; the mean itself carries an uncertainty of order scatter/√8, so the mean-vs-single numbers are indicative rather than converged. The 128 families were used during method development, so they are not an independent validation set.
