# Main-line editorial assessment

## Scope

A focused editorial selection requested by the author, using the nature-reviewer assessment axes and academic-humanizer prose rules. This is not a set of independent or mutually blind referee reports. The requested output is a single main line, rather than the skill's default three-report package.

## Decision

Organize the current BTemu paper around joint inference of the small-scale matter-spectrum parameters and galaxy astrophysics. Establish the history emulator's accuracy first, explain the fixed-spectrum galaxy comparison second, and present marginalized spectrum distributions third. The publishable contribution must rest on accuracy and inference over the BT domain; adopting a familiar architecture or plotting a corner does not establish originality.

## Evidence selection

| Claim pointer | Evidence pointer | Decision |
|---|---|---|
| The current model reports small history errors | paper/paper_materials/metrics/100k_comparison_metrics.json | Preserve source model identity and metric definitions; obtain 100k truth/prediction arrays before a reproduced accuracy claim |
| Galaxy parameter distributions depend on the assumed spectrum | paper/web/corner_pl_bt_20261104/assets/PL_vs_kp1_ms1p5_100k_Park95.json and PNG | Keep one illustrative PL/BT comparison; do not equate a shift alone with a quantified degeneracy |
| The current free-spectrum sample distributions are broad | paper/analysis_kpms_20261106/analysis.json and intervals.csv | Keep only the 100k-model preview and prior reference in the main-line viewer |
| The 95% sample interval is a final observational exclusion limit | Same analysis.json, primary_selection and diagnostics | Not established. Keep the preliminary status once beside the interval; complete independent sampling |
| Emulator and exact posterior agreement is established | paper/btemu_methods/body.tex, finite 200-step comparison (Overleaf source) | Move this finite check to supplementary material; do not promote it to full posterior validation |

## Significance and readership

The question concerns how galaxy freedom affects inference on small-scale matter spectra. It is relevant to reionization and small-scale cosmology readers. The present record supports a focused methods-and-application study; a claim of outstanding general significance or demonstrated physical novelty is not established by the supplied results.

## Consistency audit

- Passed. The selected 100k chain has 600×32×8 coordinates and 19,200 finite-log-probability rows. The [300:600] slice contains 9,600 rows.
- Passed. Main-line interval medians and endpoints are read from the verified intervals.csv/analysis.json; rounding changes display precision only.
- Provenance gap. The current HDF5 does not identify the actual prior configuration. The uniform reference is explicitly attributed to the archived prior table.
- Unresolved input needed. Current 100k validation arrays and independent sampling are needed before the final accuracy-and-inference claim.
- Passed. No 65k and 100k samples are pooled. Supplementary 512-history validation is not presented as a 100k-model test.
- Passed. The new entry point selects two available result images. Planned methods/accuracy figures are identified as a manuscript plan, not completed artifacts.

## Edit record

Reduced date-based organization to one scientific question and three result groups. Consolidated sampling and validation work into two core tasks. Kept raw files, citations, equations and numerical source records intact. No manuscript TeX, existing results, historical reviewer reports or simulation outputs were changed. Historical pages remain accessible as archives; the main-line entry point replaces them for routine reading.
