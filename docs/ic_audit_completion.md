# IC audit completed — single-realization production not qualified

Snapshot: 2026-10-10T21:24:17.439404+08:00.

All 896 new evaluations qualified; with 128 reused fixed-IC references, all 128 theta families contain eight ICs. No failed simulations. Allocated simulation cost: 1,694.12 core-hours. Array-index recovery completed; the full software regression suite passed 16 checks.

The pre-registered decision is **MULTI_IC_AVERAGING_REQUIRED**. This is a failed conservative development screen for single-realization production, not a proof that a deterministic network cannot learn a conditional mean. Random-IC 100k/10k production remains unsubmitted.

| Metric: theta-level q90 of IC standard deviation | Measured | Confirmed limit | Outcome |
|---|---:|---:|---|
| std_tau | 0.000135128 | 0.0002 | PASS |
| std_xHI_5p9 | 0.007510504 | 0.002 | FAIL |
| std_logL_tau | 0.1220787 | 0.02 | FAIL |
| std_logL_xHI | 0.9451677 | 0.02 | FAIL |
| std_logL_joint_history | 0.9480653 | 0.02 | FAIL |

Classifier labels flip across ICs in 13/128 families, including two with |mean xHI(5.9) - 0.31| > 0.01. Thus the far-from-cut stability condition also fails.

## Existing finite-IC convergence evidence

| ICs in subset mean | History RMSE to 8-IC reference | Absolute tau difference to 8-IC reference |
|---|---:|---:|
| 2 | 0.00275295 | 0.0001298276 |
| 4 | 0.001723407 | 7.896394e-05 |
| 8 | 0 | 0 |

Each value is the across-theta q90 of the within-theta q90 across all n-of-8 subsets, using saved original-native postprocessing results. These subsets overlap their reference. The n=8 zero is an identity and does not qualify eight ICs as an accurate ensemble mean.

The q90 absolute difference between logL(mean history) and log(mean likelihood over IC) is 0.308246. Mean-history inference and IC-marginalized likelihood therefore require separate validation. Joint_history refers to tau+xHI with LF fixed at the same theta, not a newly qualified LF pipeline.

Next: assess mean-history uncertainty, near-cut classification and inference-relevant likelihood behavior before freezing a multi-IC target and revised production budget. Do not relax the confirmed gates after seeing results. Existing fixed-IC labels remain useful and retain their splits. Sealed labels remain ungenerated and unread; no production MCMC.
