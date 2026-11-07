# Post-review forensic consistency audit

This audit follows the report hashes in REPORT_FREEZE.json. The checks use the frozen packet. AUDIT_VALUES.json contains the numerical outputs.

## A01. Fixed-spectrum samples and active-halo factors

**Status** Passed.

**Evidence** Body 129–148, Table II, the five HDF5 files and FIXED_CHAIN_SUMMARIES.csv.

All 30 coordinate summaries reproduce at stored precision. The finite-log-probability masks retain 95,942, 95,964, 95,904, 95,949 and 319,997 rows. Applying the capped prescription to each PL and BT1 row gives BT-to-PL ratios of marginal medians 0.122772, 0.194769 and 0.307922 at 10^9, 10^10 and 10^11 solar masses. Using only the last half gives 0.121477, 0.193588 and 0.306534. This check concerns sensitivity to the retained range within the supplied ensembles. Executed target parity and between-run stability require separate verification.

## A02. Observable evidence and the fitted LF regimes

**Status** Passed for the numerical descriptions. Unresolved input needed for the physical mechanism.

**Evidence** Body 91–123 and 153–161, Figures 1–3, data/21cmtb_evidence_20261029.json.

At the common atlas node z=8.171374 the PL and BT(kp=10, ms=2.5) neutral fractions are 0.754172 and 0.467216. The maximum stored LF score differences at kp=20 span −0.000689868 to 0.074688714. At kp=30 they span −0.000138965 to 0.013701615. These reproduce the manuscript to its printed precision. The grid is the source for the large-break result. The example curves display kp=1,3,10. A matched fixed-galaxy versus refitted LF or history contrast would be needed to quantify compensation. The common-redshift atlas comparison describes exported plane averages. Its realization and resolution sensitivity remain unmeasured.

## A03. Appendix placement and diagnostic wording

**Status** Passed for placement and arithmetic.

**Evidence** Appendix A, Figure S1 on page 10, Table III and current8d_analysis.json.

The ideal marginal equation, 9,600 retained rows, quantiles and 95% sample contour are presented in the appendix. The current 600-step source reproduces medians 17.705716 and 1.813332 and equal-tail sample intervals [4.419970,29.071114] and [0.583505,3.962328]. Ordinary interacting-walker split monitors over the retained half span 2.145102–3.446218, with 2.323164 and 2.218052 for the spectrum coordinates. Caption 185 can carry a short pointer to this warning and the unconfirmed prior when Figure S1 is read separately.

## A04. Interpretation and provenance

**Status** Provenance gap.

**Evidence** Body 45, 82, 129–157 and 229–237 and the fixed-spectrum chain headers.

Sample names, labels and hashes identify the arrays. The supplied records leave the actual common prior in sampled coordinates, PL branch, fixed parameters, likelihood terms and predictor routing unverified. The pivot-factor calculation and retention-window comparison cannot distinguish a spectrum intervention from a change in inference settings. There is no arithmetic contradiction in the checked headline results.
