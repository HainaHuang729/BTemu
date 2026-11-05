# Unified PL and BT overlays, updated November 5

Four source comparisons are included: PL versus BT kp1/MS1.5, kp5/MS1.5, kp10/MS2.5 and the added kp20/MS2.5 chain. The default remains kp10. Rebuild with `/usr/bin/python3 build.py`. Open index.html for the offline viewer.

All available steps are read, with zero extra chronological discard or thinning. Rows with nonfinite log probability are excluded. The source counts and excluded rows are recorded in each audit: PL 95,942/96,000 retained; kp1 95,964; kp5 95,904; kp10 95,949; kp20 319,997/320,000. This finite-log-probability selection supersedes the November 4 design previews that included all stored rows. Source arrays are unchanged.

Every comparison uses identical coordinate limits, 32-bin grids and marginal vertical scales. The PL contour is numerically identical in all four figures. BT is blue solid with one translucent grey fill; PL is orange dashed. Both get one independently integrated 95% smoothed sample-density outline. Diagonal labels give medians and 95% quantile offsets, BT above PL. The upper triangle is empty.

Gaussian display smoothing remains sigma 1.1 bins in 2D and 0.8 in 1D, with 256-by-256 integration. MATERIAL_UPDATE_CHECKS_20261105.json records all 120 model/panel checks and the link to the new chain audit. UNIFIED_STYLE_CHECKS_20261104.json is the historical three-case, all-stored-row design record.
