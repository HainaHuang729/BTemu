# November 4 results viewer

`index.html` is a self-contained offline report in Chinese. It includes fixed-spectrum summary plots, validation statistics, a selectable centre-difference comparison and downloadable SVG/CSV/JSON. The HTML requires no server or external libraries. Source summaries preserve their reported rather than independently reconstructed scope.

Rebuild with Python, NumPy and Matplotlib:

```
python build.py audit.json index.html
```

`audit.json` is copied from the manuscript's frozen November 4 audit. New raw chains/predictions are not inferred from summaries. `checks.json` records browser and export checks; full-page QA screenshots are local under `output/playwright/`.

## English edition and archived corner plots

Use `python build.py audit.json index_en.html --en` for the English desktop edition. The Chinese edition remains `index.html`. Both embed the unchanged 6D, 8D and exact200 PNGs from `assets/`; hashes are recorded in `corner_sources.json`. Buttons select a chain, and clicking a plot opens its original resolution in a scrollable dialog. New 100k-model raw chains remain unexported. No corner plot is inferred from the summary table.
