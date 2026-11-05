# Reconciliation of the new paper skeleton

Original source: `paper/paper_materials/BTEMU_DRAFT_20261105.md` at revision `27b03de`. The source remains unchanged. The organized working outline and this record separate editorial changes from checked numerical corrections.

| Source claim or number | Evidence available | Placement in the working outline |
| --- | --- | --- |
| BT primordial spectrum interpretation | Existing methods paper defines an input matter spectrum; the explicit primordial mapping remains requested | Use the existing matter-spectrum definition; retain the source interpretation in this record pending its mapping. |
| 100,000 train / 10,000 validation; RMSE 0.00085 / 0.00556 | Aggregate metric JSON is available; actual new evaluation arrays are absent | Report the supplied development summary and list arrays once. |
| 13.5 h per seed | JSON records 47,661.2727 s; the ledger describes five-seed training as 13 h 30 m | Keep both scopes in the timing reconciliation; do not label the JSON time as per-seed. |
| Forward speed-up about 6e6, exact 460 s versus 8e-5 s | Arithmetic is a component comparison; full LF+tau evaluation timing is unexported | Keep the reported component example in the cost section. |
| All fixed-spectrum chains have 3,000 steps | The new kp20 raw shape is 10,000 x 32 x 6 | Use 3,000 for PL/kp1/kp5/kp10/7D and 10,000 for kp20. |
| 8D Rhat up to 1.084 | JSON gives ETA_STAR 1.258, ALPHA_STAR 1.178, M_TURN 1.082, KP 1.084 | Identify KP's entry and the actual maximum separately. |
| Nearly prior-wide KP/MS intervals imply no constraints | The joined chain arrays, selection and diagnostic definition are not exported | Describe the reported samples and complete the information comparison from actual joint arrays. |
| 0.948 IC noise floor makes dlogL<=0.1 unreachable | Existing T7 finite-IC summaries do not establish a universal predictor-error floor | Keep the original numerical claim here; use target-specific error and finite-reference analysis. |
| IC4 to IC8 changes mean by 1.25%, so IC noise is subdominant | The source comparison also changes the PS estimator | Retain the 1.25% report with its estimator scope; omit the unsupported causal conclusion. |
| Validation predictions and 10D PS products are ready/running | Those entries name external paths; local exports contain summary/image/progress records | Distinguish source-reported availability from received arrays. |
| MS<1.5 gives invalid BT models | Progress snapshot reports a producer filter and zero-signal cases | State the production-domain filter without a universal physical validity conclusion. |

The organized outline uses direct scientific prose, places each material requirement once, and keeps the original empirical numbers and external-path inventory in the preserved source. No missing evidence is supplied by changing prose.
