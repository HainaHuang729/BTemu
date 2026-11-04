# November 4 results viewer

`index.html` is a self-contained offline report in Chinese. It includes fixed-spectrum summary plots, validation statistics, a selectable centre-difference comparison and downloadable SVG/CSV/JSON. The HTML requires no server or external libraries. Source summaries preserve their reported rather than independently reconstructed scope.

Rebuild with Python, NumPy and Matplotlib:

```
python build.py audit.json index.html
```

`audit.json` is copied from the manuscript's frozen November 4 audit. New raw chains/predictions are not inferred from summaries. `checks.json` records browser and export checks; full-page QA screenshots are local under `output/playwright/`.

## English edition and archived corner plots

Use `python build.py audit.json index_en.html --en` for the English desktop edition. The Chinese edition remains `index.html`. Both embed the unchanged 6D, 8D and exact200 PNGs from `assets/`; hashes are recorded in `corner_sources.json`. Buttons select a chain, and clicking a plot opens its original resolution in a scrollable dialog. New 100k-model raw chains remain unexported. No corner plot is inferred from the summary table.

## Runtime inventory

Both editions now list 25 workflow steps, with unavailable elapsed times explicitly marked. Expandable tables preserve six coeval runs, 15 timed cache cases plus three setup failures, and 87 archived atlas timings. `timing_section.py` renders these records from hash-checked snapshots in `timing_sources/`. The page exports timing JSON. Historical per-call/per-iteration values are not assigned to new 100k-model runs, and mixed or overlapping costs are not summed into an end-to-end duration. New-model source `seconds` converts to 13.2392 h, with per-seed/hardware allocation unverified.

## Concise results view

The default view retains numerical tables, plots and recorded runtimes. Full workflow rows, missing timings and audit notes remain in closed details panels. All embedded data and original corner images are preserved.

The concise runtime table now incorporates the newly exported ledger at revision `4d99ddd`. Both 100k training times (JSON and ledger) remain distinguished. The phase60 core-time value is converted from 943695 core-seconds to 262.1375 core-hours; no headline speedup extrapolations are adopted. The earlier timing inventory is retained under a closed details panel.
