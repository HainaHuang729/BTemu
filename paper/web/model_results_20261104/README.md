# November 4 results viewer

`index.html` is a self-contained offline report in Chinese. It includes fixed-spectrum summary plots, validation statistics, a selectable centre-difference comparison and downloadable SVG/CSV/JSON. The HTML requires no server or external libraries. Source summaries preserve their reported rather than independently reconstructed scope.

Rebuild with Python, NumPy and Matplotlib:

```
python build.py audit.json index.html
```

`audit.json` is copied from the manuscript's frozen November 4 audit. New raw chains/predictions are not inferred from summaries. `checks.json` records browser and export checks; full-page QA screenshots are local under `output/playwright/`.
