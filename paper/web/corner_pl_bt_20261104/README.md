# PL and BT overlay: actual uploaded 100k-model chains

Open index.html for the standalone offline viewer. The default compares pl_100k.h5 and kp10_ms2p5_100k.h5. The selector also offers fixed kp1/ms1.5 and kp5/ms1.5 BT cases, each paired with the same PL data. Each plot contains exactly two model distributions.

All four HDF5 files have 3,000 steps, 32 walkers and six identically ordered named coordinates. Their kp/ms attributes were checked against the labels. All 96,000 stored rows per model are used, with no additional discard or thinning; no burn-in receipt is present in these files. Coordinates are not transformed. The common display range is the union of both sets, with the existing 2.5% padding rule.

BT uses a solid blue outline and one translucent grey filled band; PL uses an orange dashed outline without fill. Each density is normalized independently. Histograms use 32 bins, Gaussian display smoothing sigma 1.1 bins in 2D and 0.8 in 1D. The 95% highest-density threshold is found by sorted integration over a 256-by-256 equal-area grid. All 90 model/panel regions passed mass checks (0.950000025–0.950072980). Marginal annotations show each model median and 2.5th–97.5th percentile offsets. The upper triangle is empty. The source archives and accepted manuscripts are unchanged.

Rebuild with `/usr/bin/python3 build.py`; use `--page-only` to rebuild the viewer from verified existing images. `render.py --help` documents the two-file entry point. Audits record source/output hashes, selected rows, common limits, parameter summaries and each contour mass. The renderer passed an identical-array integration check using actual BT rows; that internal check is not a PL result and is not published.
