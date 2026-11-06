# Forensic consistency audit

This editorial audit was performed after all three independent reports were finalized and hashed in REPORT_FREEZE.json. Findings were not returned to the reviewers. Values are recorded in AUDIT_VALUES.json. Manuscript sources and the reviewer reports were not edited.

## AUD-01

**Status** passed

**Claim pointer** Current spectral intervals describe steps 301–600 of the uploaded 600-step 8D chain.

**Evidence pointer** packet/body_numbered.txt lines 139–154; packet/current8d.h5; packet/current_intervals.csv.

**Check and result** The raw array is 600×32×8 and all 19,200 coordinate rows and log probabilities are finite. The [300:600] slice contains 9,600 rows. Its KP q025, median and q975 are 4.419969654, 17.705716030 and 29.071113734. MS values are 0.583505204, 1.813331555 and 3.962328441. They reproduce the manuscript at its displayed precision.

**Impact** Numerical reproduction passes. This does not establish equilibration or the actual prior.

**Reviewer overlap** R1-M1, R2-M2, R3-M1 concern inference status rather than failed arithmetic.

## AUD-02

**Status** passed

**Claim pointer** The sample 95% interval widths are 89.5% and 101.6% of the reference prior 95% interval widths.

**Evidence pointer** packet/body_numbered.txt lines 147–154; packet/prior_table.csv.

**Check and result** Uniform reference KP [1,30] has equal-tail 95% interval [1.725,29.275]. MS [0.5,4] gives [0.5875,3.9125]. Ratios are 100×(29.071113734−4.419969654)/(29.275−1.725)=89.47784% and 100×(3.962328441−0.583505204)/(3.9125−0.5875)=101.61874%. The reported percentages are correctly rounded. These are width comparisons, not measures of all information in the distributions.

**Impact** The manuscript's descriptive statements are consistent. No final exclusion limit follows from these ratios alone.

**Reviewer overlap** R1-M1, R2-M2, R3-M1.

## AUD-03

**Status** passed

**Claim pointer** The representative PL/BT figure retains 95,942 and 95,964 rows.

**Evidence pointer** packet/body_numbered.txt lines 123–127; packet/fixed_kp1_summary.json, sources.

**Check and result** PL stores 3,000×32=96,000 rows and excludes 58, leaving 95,942. BT excludes 36, leaving 95,964. The retained counts reconcile with the frozen figure receipt. The receipt states no chronological discard. This is a receipt consistency check, not a new independent convergence test.

**Impact** Counts pass; a sampling-status qualification remains necessary for the interpretation of shifts.

**Reviewer overlap** R1-M1, R2-M2.

## AUD-04

**Status** aggregation_ambiguity

**Claim pointer** Current-model accuracy supports the likelihood calculation.

**Evidence pointer** packet/body_numbered.txt lines 106–116; packet/100k_metrics.json.

**Check and result** Trajectory median and q95 match the supplied JSON. The current truth/prediction arrays and exact evaluation membership are absent from the packet. The three q90 error fields do not define signed versus absolute aggregation. In particular, 1.17734 cannot be interpreted as an absolute likelihood-error tolerance or evidence of negligible bias.

**Impact** The reported history summary is traceable but current-model likelihood fidelity cannot be established from the aggregate alone.

**Resolution test** Supply metric definitions, executed predictor identity and validation arrays, then measure signed bias and absolute tails in the relevant inference region.

**Reviewer overlap** R1-M2, R2-M3, R3-M1.

## AUD-05

**Status** provenance_gap

**Claim pointer** The archived uniform priors are the prior reference for the current chain.

**Evidence pointer** packet/prior_table.csv; current8d.h5; body lines 47 and 139.

**Check and result** The archived table labels native-coordinate uniform supports. The current HDF5 has no run attributes confirming the actual joint prior, its transformed galaxy support or the deployed predictor. The manuscript explicitly calls the plotted prior a reference, so there is no proved contradiction.

**Impact** The extent to which the observations reshape the actual prior remains unresolved.

**Resolution test** Export executed prior and coordinate support together with the likelihood, fixed settings and model identity.

**Reviewer overlap** R1-M1, R2-M2, R3-M1.

## AUD-06

**Status** confirmed_internal_error

**Claim pointer** The preceding revision's machine-readable check record says the main text contains three tables.

**Evidence pointer** BTemu/paper/manuscript_20261106/MANUSCRIPT_CHECKS.json, main_tables; identical Overleaf reproduction record. packet/body.tex before the appendix command.

**Check and result** Counting active table/table* environments before the appendix gives two tables, the current-model accuracy summary and the spectral interval table. The record says three. The manuscript itself has the correct table numbering.

**Impact** Minor metadata error in the earlier check record. It does not change any scientific result. It is recorded here separately from reviewer consensus; correction can accompany the next authorized revision.

**Reviewer overlap** None identified.

## AUD-07

**Status** unresolved_input_needed

**Claim pointer** The main result answers how much observational information survives galaxy freedom.

**Evidence pointer** packet/body_numbered.txt lines 9, 123–160 and 205–207.

**Check and result** The published quantities reproduce as stored-sample summaries. Independent-ensemble evidence, actual prior support and current likelihood-fidelity evaluation are not supplied. No controlled fixed-versus-free galaxy information comparison is shown. The paper currently supports a preliminary demonstration rather than a completed measurement of information loss.

**Impact** Closing the scientific question needs evidence, not removal of its qualifications.

**Reviewer overlap** R1-M1, R1-M2, R2-M1 through R2-M3, R3-M1 and R3-M2.
