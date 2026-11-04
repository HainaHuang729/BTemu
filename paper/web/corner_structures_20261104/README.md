# Five structural corner designs

All five use the same original samples, display limits and blue palette. No in-figure titles, information blocks, colourbars or legends are added. Each covers 6D, 8D, exact 200-step, and both historical 21cmTB corners.

- f2fe0d4b1f54: 紧凑填色轮廓 / Compact filled contours
- bbcc67d4da73: 分隔六边形计数 / Separated hexbin panels
- 0acf7625a23a: 上三角像素密度 / Upper-triangle density
- fa3d1551efd9: 完整双侧矩阵 / Full dual-view matrix
- 8f7a063e8330: 散点与线框轮廓 / Scatter and contour lines

Filled contours use peak-relative levels 0.08, 0.25, 0.50 and 0.75. Line contours use 0.15, 0.40 and 0.75. These are isodensity levels, not probability-content contours. Smoothing uses a Gaussian filter with sigma 0.9 bins on the original 32-by-32 count grid. Hexbin uses gridsize 24 and all rows. Scatter displays at most 4,500 deterministically spaced stored rows; contours use all retained rows. Histograms use all rows and 32 bins. Historical diagonal histograms retain the two ensemble groups (blue 0, ochre 1).

The manifest records fresh SHA-256 design IDs, source hashes, output hashes, row counts, smoothing, and count checks. All inputs were hash-checked after rendering; label extents passed for every output. Accepted paper figures are unchanged. Open index.html for the offline comparison.
