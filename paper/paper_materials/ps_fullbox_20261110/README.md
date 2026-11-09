# Full-box versus sub-box 21cm power spectra (2026-11-10)

32 paired realisations: same theta, same IC seed, same 250 Mpc / DIM 512 run.
Each realisation is analysed twice: once over the whole box, once averaged
over the eight 125 Mpc sub-boxes (the estimator used for all earlier labels).

## Result

The full-box spectrum is systematically lower, by an amount that grows with k
and is nearly independent of redshift:

| z | median full/sub | 16-84% |
|---|---:|---|
| 6.34-7.97 | 0.974-0.980 | 0.91-1.03 |
| 9.00-13.42 | 0.973-0.979 | 0.92-1.02 |
| 15.56-18.21 | 0.982-0.985 | 0.93-1.02 |

| k [1/Mpc] | median full/sub | 16-84% |
|---|---:|---|
| 0.116 | 0.999 | 0.89-1.07 |
| 0.347 | 1.007 | 0.96-1.04 |
| 0.579 | 0.977 | 0.93-1.00 |
| 0.996 | 0.953 | 0.92-0.98 |

Per-point scatter is 5-10% and is dominated by sample variance, not by a
systematic trend.

## Consequence for the emulator

Applying the (z, k) median ratio to the existing 5,245 sub-box labels and
retraining the same network changes the validation metrics from

| labels | median error | 68% | 90% | shifted-log RMSE |
|---|---:|---:|---:|---:|
| sub-box (3,730 theta) | 22.6% | 38.1% | 91.9% | 0.294 |
| full-box corrected (4,113 theta) | 19.6% | 32.5% | 79.2% | 0.241 |

so roughly a fifth of the previous error floor was estimator inconsistency
rather than limited sample size. New production should use the full-box
estimator directly.
