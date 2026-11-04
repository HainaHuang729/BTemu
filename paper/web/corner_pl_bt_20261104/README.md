# Unified PL and BT corner overlays

Open index.html for the offline viewer; the default is PL versus BT kp10/ms2.5. Select kp1/ms1.5 or kp5/ms1.5 for the other comparisons. Every plot contains exactly two distributions. Rebuild with `/usr/bin/python3 build.py`; `--page-only` rebuilds only the viewer from verified images.

The style is park-overlay-unified-v1: STIX type, thin grey boxes, blue solid BT curves with one light grey density fill, orange dashed PL curves, common line weights, and no upper-triangle information blocks. Numerical annotation order is BT above PL, with the same decimal precision per coordinate across models and cases.

All three cases now use one common coordinate range and 32-bin grid, obtained from the union of PL and all three BT arrays with 2.5% padding. Their diagonal marginal density vertical scales are also shared. The same PL density therefore has exactly the same numerical region and display scale in all three plots. This grid replaces the earlier pair-specific ranges. No retained row or quantile summary changed.

Each chain contributes all 3,000 stored steps and 32 walkers (96,000 rows), with no additional discard or thinning; the source files do not specify burn-in selection. Named coordinates are unchanged and kp/ms attributes were checked against plot labels. Densities are normalized separately. Display smoothing is Gaussian sigma 1.1 bins in 2D and 0.8 in 1D. Each single 95% density region is determined by sorted integration on a 256-by-256 equal-area grid. All 90 model/panel checks passed (masses 0.950000250–0.950037083). Diagonal summaries are medians with offsets to the 2.5th and 97.5th percentiles.

Source/output hashes, common ranges, marginal scales, row counts, quantiles and each contour integral are in the per-figure audit JSON files. UNIFIED_STYLE_CHECKS_20261104.json records preservation and display checks. Accepted manuscript assets are unchanged.
