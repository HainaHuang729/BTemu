# Park-inspired 95% sample-density corner preview

Single light-grey fill and one dark outline per data set, boxed compact lower triangle, smoothed diagonal marginals, and an empty upper triangle. Five archived corner cases are provided. No second data set has been added and accepted manuscript assets are unchanged. Open index.html locally.

For each pair, all retained rows enter the original 32-by-32 count histogram over unchanged coordinate limits. A Gaussian filter of sigma 1.1 bins with reflected boundaries smooths the histogram. Bilinear interpolation onto 256-by-256 equal-area cell centres defines the density integration grid over the full display domain. Grid densities are sorted from highest to lowest, and the threshold is the first whose cumulative mass reaches 0.95; tied densities are included. The drawn band uses that single threshold. Plot-domain edge nodes use nearest edge values. Diagonal density smoothing is sigma 0.8 bins. The historical diagonal ensemble groups remain separate.

This is a 95% region of the smoothed stored-sample density. No posterior convergence or calibrated coverage is inferred from its presentation. It replaces the previous design-only 10%-of-peak threshold. The method was checked against a 2D standard Gaussian (expected threshold/peak 0.05), and a uniform plateau tie case. Input hashes, all 122 pairwise grid-mass checks and output hashes are recorded in manifest.json. Region masses range from 0.950000036 to 0.950018555.

Style reference: Park et al. (2019), Figure 4: https://arxiv.org/html/1809.08995v2#S6.F4 .
