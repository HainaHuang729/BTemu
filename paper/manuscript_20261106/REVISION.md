# BTemu main-line revision, November 6, 2026

## Request and revision

The author requested one scientific line, supplementary placement of other material, and removal of repeated defensive explanations.

The default manuscript now asks how LF, optical-depth and neutral-fraction observations restrict the matter-spectrum parameters after marginalizing over galaxy parameters. Its three result groups are current-model history accuracy, one representative PL/BT galaxy comparison, and the KP/MS marginals with uniform-prior references. The abstract and conclusions follow the same order.

The earlier-model validation, current sampling checks, finite exact comparison, initial-condition audit, old chain construction and remaining fixed-spectrum comparisons are appendices. Their numerical records and citation keys are preserved. The former separate physics entry point is retained as `paper/physics_archive_20261106.tex`, using its unchanged physics body. The default `paper/main.tex` and `paper/btemu_methods/main.tex` share the revised BTemu body.

## Before and after

Before, the main text described successive model exports, the 512-history evaluation, finite exact statistics and IC checks as separate result narratives. After, the main text follows the joint-inference question and keeps each qualification at its relevant result. Repeated production counts and upload chronology were removed. One sampling-status paragraph accompanies the current marginal intervals.

## Numerical and source checks

- The 100k accuracy values retain their reported-development status and exact source values.
- The fixed-spectrum representative comparison uses the previously verified finite-log-probability sample selection and unchanged plot.
- Current KP/MS medians and equal-tail intervals agree with the verified `[300:600]` chain selection to displayed precision. No 65k and 100k samples are mixed.
- All eight citation keys in the former methods body are retained. Equation definitions, numerical comparison tables and source figures are retained or moved to the appendices.
- Both manuscript entry points compile. All labels are unique; all references resolve. No undefined references/citations or overfull boxes occur in the final logs. The package nameref/revtex label warning is unchanged.
- Final output has 16 pages. The main text and references occupy pages 1–6; appendices begin on page 7. Rendered pages were inspected as a full contact sheet and the main result pages at higher resolution.

## Remaining evidence

Complete independent-ensemble sampling with the same 100k model and export its actual prior/model configuration. Export the current model's truth/prediction validation arrays and metric definitions. These are the two outstanding empirical tasks; no new sampling was launched during this revision.

## Reproduction receipt

`analysis.json`, `intervals.csv`, `CHECKS.json` and the archived `analyze.py` copy preserve the KP/MS source calculation. The script's original executable location is `BTemu/paper/analysis_kpms_20261106/analyze.py`, as documented in the copied analysis README; its unchanged relative imports are not a standalone Overleaf program. `body_before.tex` and `main_before.tex` preserve the pre-revision methods source.
