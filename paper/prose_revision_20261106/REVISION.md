# BTemu v0.10 prose and interpretation revision

## Scope

The author requested consolidation of defensive and repetitive explanations, data-supported physical interpretation, a separate evidence list and upload. The three frozen v0.9 reviewer reports remain unchanged. This revision addresses the writing items and adds an algebraic interpretation of existing samples. It does not claim that their evidence-blocking concerns have been resolved.

## Changes

- Combined the main sampling, actual-prior and aggregate-validation boundary into one paragraph beside the spectral results. Kept the abstract's preliminary designation and the exact result selection.
- Removed repeated future-work and missing-array explanations from the conclusion, and replaced upload chronology with stable model and sample definitions.
- Consolidated the earlier-chain descriptions by referring the finite comparison to its single construction/diagnostic appendix. Retained earlier numerical values and citations.
- Defined LF, PL and BT before their first shorthand use and distinguished ten emulator inputs from eight jointly varied coordinates.
- Rounded headline RMSE values to three significant figures while retaining the original source precision in the accuracy table and receipts.
- Replaced a readiness statement with the observed sample result and its physical interpretation.

## Physical interpretation and verification

Combining the existing stellar-mass and star-formation equations with log10(f_star,10)=eta_star+log10(t_star) gives

S(M)=dotM_star/[M H(z)(Omega_b/Omega_m)]=min[1,10^eta_star t_star (M/1e10 Msun)^alpha_star]/t_star.

The new calculation evaluates this expression on every existing finite-log-probability row of the same PL and BT(kp=1,ms=1.5) samples used by Figure 1. It includes the efficiency cap and introduces no new retention cuts. At 1e10 Msun, no retained row is capped and the medians are 0.118501 (PL) and 0.0230803 (BT). BT/PL ratios of marginal medians are 0.122772, 0.194769 and 0.307922 at 1e9, 1e10 and 1e11 Msun. These are separate marginal medians, not paired-run effects or a total emissivity ratio.

The existing equations also determine the extra spectral scale dependence (k/kp)^(ms-ns) above the break. For ms=1.5 and ns=0.968 the exponent is 0.532. Absolute PL/BT power ratios are not inferred from that exponent because normalization and the separately implemented PL branch remain relevant.

## Selected before and after

Before, the result ended with “These shifts show how the selected galaxy distributions change … motivating their joint treatment”. After, Eq. (SFR factor) and a row-wise sample calculation explain that eta_star controls the active-halo star-formation normalization, alpha_star controls its mass dependence, and the selected BT sample reduces it more at low mass.

Before, the conclusion said the free-spectrum calculation “provides the quantities needed to measure” surviving information and repeated planned sampling and missing validation arrays. After, it states the observed broad sample ranges, their low-kp difference from the reference, and the explicitly preliminary representative-history scope.

## Evidence and fidelity

EVIDENCE_GAPS_20261106.md is the separate author-facing evidence list. It distinguishes target-posterior sampling, current-model likelihood validation, conditional IC-target checks, the unmeasured halo-abundance compensation mechanism and controlled information-loss comparisons.

All existing citation keys, original likelihood/spectrum/galaxy equations, main interval values and figure assets are preserved. The added S equation is algebraically derived; S statistics are new calculations on unchanged source arrays. Missing validation metrics were not filled in or reinterpreted. The previously reported main-table count is corrected to two in the new revision's check record; the frozen v0.9 review and source records are preserved.
