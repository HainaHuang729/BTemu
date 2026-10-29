# Draft corrections and result synchronization

Date: 2026-10-29. Starting tracked revision: `f8053a0`.

## Scope

Updated `PAPER_DRAFT_20261029.md`, `RESULTS_20261029.md`, `PLAN_20261029.md`,
`PRD_20261029.md`, and `OUTLINE_MAPPING_20261029.md`. Existing independent
working-manuscript and figure files in this checkout were left untouched.

## Corrections

| Passage or result | Problem | Final treatment |
|---|---|---|
| Abstract and discussion | Absolute history RMSE 0.0010 was written as a relative 0.10% error. | Define the trajectory RMSE and report the dimensionless absolute value. |
| Discussion and result snapshot | Realization scatter was used to declare an error threshold unreachable and argue for different acceptance criteria. | Report the actual statistic: across-family q90 of the within-family IC sample standard deviation of history log likelihood, 0.9480653. Keep the original acceptance requirements; no new lower bound is inferred. |
| Discussion and result snapshot | Comparability or superiority to another emulator was claimed using unmatched error definitions and observables. | Remove the performance ranking and “our acceptance is stricter” argument. Retain the measured errors and their scope. |
| Mock fits | “Cannot be absorbed” and definitive bias claims exceeded the evidence from chains with failed configured diagnostics. | Retain reported fit/sample statistics and the failed aggregate diagnostic status; use a neutral section title. |
| Exact/emulator comparison | A centre difference below 0.25σ was presented as posterior fidelity; the exact reference has only 200 steps. | Attribute the offset and width ratios to the older comparison, separate from the newly combined chain. State the unresolved reference/configuration/diagnostic requirements. |
| Eight-dimensional chain identity | Six astrophysical coordinates plus KP/MS were confused with an eight-astrophysical-parameter, X-ray-free exact calculation. | Use parameter names from HDF5 for the current chain; preserve the older exact-run reports separately. |
| Convergence | The six-dimensional sequence was called converged despite a reported value above 1.05. | Recompute the ordinary split monitor and describe its definition and limitations. No all-parameter convergence acceptance is claimed. |
| Chain length | The eight-dimensional extension filename and summary implied 5,400 total steps. | Read array shapes: 2,000 + 3,568 = 5,568 stored steps. |
| Sample summary | Rounded six-dimensional moments in the source snapshot did not match its stated last-half selection. | Recompute all moments from the last 2,500 of 5,000 steps, all 32 walkers, without thinning. Retain source hashes and selection details. |
| Data scale | Admitted label counts were conflated with checkpoint training size; counts were stale. | Keep 65,536 as the reported model training milestone and separately date the production counts, 83,756 training and 2,752 validation histories at 15:45. |
| Original §5.2 and planning documents | A matter-power-spectrum figure and low-redshift sim/HMcode reports were labelled as 21-cm results. | Remove that result section and its science/figure-plan references from the five edited documents. The existing unused image is retained as a legacy asset, preserving other working files. |

## Evidence and reproducibility

- `validate_draft_snapshot.py` reads the published HDF5 segments, checks parameter
  order, shapes, finite chains and log probabilities, and exact repeated
  suffix/prefix blocks. It writes `DRAFT_SNAPSHOT_VALIDATION_20261029.json`.
- Six-dimensional total: 5,000 stored steps; retained last half: 2,500 steps and
  80,000 correlated rows. Ordinary split statistic: 1.0340356133–1.0534691575.
- Eight-dimensional total: 5,568 stored steps; retained last half: 2,784 steps
  and 89,088 correlated rows. Ordinary split statistic:
  1.1135829013–1.5125408061.
- The monitor splits interacting ensemble walkers; it is distinct from
  independent-chain rank-normalized/folded R-hat. No new ESS or convergence
  certification is inferred.
- File ordering follows the published snapshot and filenames. Complete target
  settings, iteration offsets and RNG state remain absent from the HDF5 export.
- IC-scatter definitions and values are verified against
  `docs/ic_audit_completion.md` and `maintenance/ic_audit/report.py`.
- Accuracy, learning-curve endpoints, mock-fit values and the older exact-chain
  offsets remain attributed to their source reports. Missing external artifacts
  have not been invented or replaced with new measurements.

## Validation

The numerical refresh is deterministic under the stated chain selection.
Published chain file digests were checked against the tracked source blobs;
the raw simulation and chain arrays are unchanged. Relative Markdown links in
the five edited documents resolve. The mixed spectrum reports and the
unmatched performance/threshold assertions are absent from those documents.
`git diff --check` passes.

This revision is Markdown; no TeX compilation is applicable. No simulation,
training, new inference run, figure regeneration, commit or push was performed.
