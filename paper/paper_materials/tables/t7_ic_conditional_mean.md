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
| Δ logL(mean history) − logL(IC marginal) | −0.0025 | 1.1e-7 | 6.0e-7 | 1.908 |

## Reading (definition audit, 2026-10-31)

- The 0.948 value is the across-family q90 of within-family sample standard deviations of history log likelihood (ddof=1). It is not a universal lower bound on emulator prediction error relative to a conditional mean. The corresponding confirmed IC-scatter gate is 0.02; no emulator-error impossibility at 0.1 follows from this statistic.
- Fixed-realization versus eight-IC-mean differences describe a finite, overlapping reference comparison. They are not errors of the deployed emulator.
- The delta-logL q50/q90/q95 entries are SIGNED quantiles. Their small upper values do not establish that most absolute differences are small. The maximum absolute difference is 1.907966527. The earlier completion note separately reports q90(abs(delta))=0.308246; raw family rows are required to reproduce that number, and it cannot be recovered from these signed quantiles.
- The production records use one random realization per parameter point. Retain per-realization development validation and the representative-history inference target. The audit's eight-IC mean is a separate finite reference; conditional-mean prediction accuracy and IC-marginalized likelihood fidelity remain to be tested with matched predictions.
- Summary availability and definition checks are complete. Scientific target validation remains partial. See [the audit and required raw inputs](../../T7_AUDIT_20261031.md).

## Caveat

Only 8 realizations per family; the mean itself carries an uncertainty of order scatter/√8, so the mean-vs-single numbers are indicative rather than converged. The 128 families were used during method development, so they are not an independent validation set.
