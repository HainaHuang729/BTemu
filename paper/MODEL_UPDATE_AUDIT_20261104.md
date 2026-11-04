# November 4 model and fixed-spectrum update audit

Source: BTemu revision `45edd179770899d57ffd9dc1917f91a032be7d3c`. Original results, metric JSON and PS inventory are frozen byte-for-byte under `paper/reproduction/data/model_update_20261104/` in the manuscript project. The source manifest records SHA256 hashes. This audit verifies the exported evidence, not external calculations.

## 1. Old/new validation comparison

The released 512-history NPZ independently gives the earlier five-model-average RMSE median 0.0010076164530363834 and q95 0.006814576402167939. Seed 11 gives median 0.00152412201824959 and q95 0.010080229640065698. Thus the source old-model column's rounded median 0.0010 and q95 0.0101 mix average and individual-seed definitions. The original values are preserved in the frozen source; no improvement ratio is inferred from that column.

The new JSON reports 100000 training histories, a 10000-history development-validation split, five training seeds, RMSE median 0.0008506683514504011 and q95 0.005563643971917824, xHI q90 0.004570504253875837, tau q90 0.00033507794141769416 and dlogL q90 1.177335122574713. These values are included as reported summaries. The evaluated sample membership/count, prediction aggregation, signed-versus-absolute q90 definitions, actual postprocessing and new predictions are missing. The 10000 split size is not independently established as the number evaluated for these statistics. `seconds=47661.272694741376` is 13.2392 hours, rather than the prose's 13.5 hours; no timing or speed claim is added.

## 2. IC4/IC8 PS comparison

The prose reports a full-box versus 12-sub-box estimator difference. Equal box size/resolution/cosmology alone cannot equate window functions, mode weighting or masks. The stated 1.25% median, 13.9% q90 mean-spectrum difference and 1.82%/3.05% realization scatter cannot isolate the effect of increasing IC count. Metric definitions, assignments of the scatter values, matched spectra, estimator code, seeds and bins are unexported. No causal explanation, convergence-with-IC claim or new history-emulator accuracy is inferred. The methods draft records this distinction; PS+LF corner behaviour is excluded from physics results. A small PS residual at the injection does not identify which likelihood/support/mapping term caused the chain behaviour. The older phase60 sealed PS test remains failed in the exported inventory, with 249 complete theta out of 256 planned; its status is separate from the new history model.

## 3. Fixed-spectrum samples

The physics draft transcribes three fixed-spectrum rows and five named galaxy coordinates. Source summaries report 3000 steps and acceptance 0.31--0.38, but no walker count, retention, centre/spread convention, independent convergence/ESS, raw chain, likelihood/prior parity or fixed X-ray receipts. These are reported centres/spreads, not newly computed means, standard deviations or credible intervals. t_STAR is absent. The 7D row's last entry is explicitly MS=2.28+/-1.01 rather than ALPHA_ESC, and is described separately.

At MS=1.5, kp1 versus kp5 changes reported ETA_STAR by -0.629 and ALPHA_STAR by +0.088. The kp1/MS1.5 versus kp10/MS2.5 difference is -0.702/+0.180, with both spectrum coordinates changed. Neither comparison supplies physical kp/MS bounds or isolates observational effects before run parity and sampling are checked. Existing corners and the old exact200 T6 remain tied to their original predictor and samples.

## Verification and remaining evidence

`audit_model_update.py` checks frozen hashes, reproduces old metrics, parses the fixed rows and generates TeX table rows. New summaries are not independently reconstructed. The SSH read attempt reached the login host but was rejected by authentication; no remote file was read and no simulation, training, sampler or controller task was launched.

Priority return package: (1) new evaluation code, member IDs, predictions/truth, normalizer and weight hashes with aggregation and likelihood definitions; (2) all fixed/7D raw chains, parameters/orders, estimator/retention definitions, data/prior/fixed-value receipts and independent diagnostics; (3) paired IC4/IC8 spectra under identical PS estimators/windows/masks and seed policy; (4) matching exact-versus-new-model comparison. Previously frozen numerical tables, equations, figures, citations and chain selections are preserved. Compile/render verification is recorded in `paper/revisions/MODEL_INTEGRATION_CHECKS_20261104.json`.
