# Remaining material after the November 5 exports

## Delivered and checked

- PL, kp1/MS1.5, kp5/MS1.5, kp10/MS2.5 and kp10/free-MS7D raw HDF5 files are available. Each has 3,000 steps and 32 walkers.
- The added kp20/MS2.5 file has 10,000 steps and 32 walkers. Shapes, parameter names, spectrum attributes, coordinate finiteness, log-probability masks and source hashes have been checked. Recomputed summaries and removal counts are supplied alongside this list.
- The 16,018-step 8D diagnostic JSON and its corner PNG are available as reported results. Its largest Rhat entry is ETA_STAR=1.258, not KP=1.084.
- The accuracy/marginals PNG, paper skeleton and PS10D progress snapshot have been received. Their source bytes and hashes are preserved.

## P0: complete joint sampling and inference identity

Export the actual 16,018-step eight-dimensional chain, segment order/offsets, parameter names, retention selection, and diagnostic code/definition. The currently uploaded six-coordinate and free-MS seven-coordinate files do not contain that eight-coordinate calculation. Supply independent-run diagnostics and autocorrelation-aware ESS, together with likelihood, priors, fixed parameters, IC policy, weights and normalization identities. The two outstanding T3 LF-only and LF+tau files are still separate missing material.

## P0: current model validation arrays

Export evaluated sample IDs, redshift nodes, truth histories, each seed's predictions and the deployed aggregate, plus the calculation used for the new accuracy PNG. Identify the residual q95=0.0032 statistic shown in the image and keep it separate from trajectory-RMSE q95=0.00556364. Record the signed/absolute definitions and axes of each q90, and the independent final-test membership.

## P0: physical model and matched target

Supply the native/build and run fingerprints, realized k/P(k) arrays, normalization and PL-reference comparison already requested in the November 4 inventory. Retain the distinction between a phenomenological input matter spectrum and a primordial-spectrum interpretation. Return the existing finite-IC family arrays and predictions needed to compare the intended history/likelihood target with the new predictor and a matching exact reference.

## P1: observable predictions and timings

Return LF, xHI(z) and tau predictions tied to the same current retained rows. Supply complete-likelihood timing scopes and resolve the 13.2392 h JSON record versus the 13.5 h ledger description, including whether times cover a seed or all seeds. Existing forward-component timing ratios do not provide this scope.

## P1: PS material, if retained in scope

The supplied `ps_lf_joint.h5` is 2,108 bytes and cannot be opened by the current HDF5 reader (bad object header version). Provide a readable complete export with parameter/likelihood contributions and the source configuration before using its samples. The PS10D progress snapshot needs its NPZ files, theta membership, ICs, estimator/window/bin definitions and validation results to support a completed PS result. The MS>=1.5 production filter is not by itself a tested physical validity boundary. The earlier phase60 result and IC4/IC8 estimator mismatch remain separate issues.

## Other manuscript

The particle-profile PNG and associated progress belong to the nonlinear-structure manuscript. Export profile radii, densities, counts, centring definitions and mass units there; they are not evidence for the BTemu history emulator.
