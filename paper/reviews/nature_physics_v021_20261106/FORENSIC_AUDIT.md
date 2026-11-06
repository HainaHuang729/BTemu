# Forensic consistency audit

This audit was performed after all three reports were finalized and hashed. No findings were returned to reviewers and no frozen report was edited. AUDIT_VALUES.json contains the calculations. Manuscript and raw source files remain unchanged.

## AUD-21-01

**Status** passed

**Claim pointer** Table tab:fixed-100k contains explicitly recomputed six-coordinate medians for five fixed-spectrum choices.

**Evidence pointer** packet/body_numbered.txt lines 129–140; data/FIXED_CHAIN_SUMMARIES.csv; data/SOURCES.json; chains/.

**Check and result** Recomputed the mean, population standard deviation and five quantiles for all 30 coordinate/model combinations using the stated finite-log-probability mask. Maximum discrepancy with the source CSV was zero at the stored precision. Source hashes match. Retained row counts are 95,942 (PL), 95,964 (BT1), 95,904 (BT5), 95,949 (BT10) and 319,997 (BT20). Exclusions are 58, 36, 96, 51 and 3 from the stated 3,000×32 or 10,000×32 arrays.

**Impact** The former unspecified-estimand issue is resolved for these displayed medians. Convergence and common executed priors/likelihoods are separate checks.

**Reviewer overlap** Consistent with the strengths in all reports and the target-parity concerns R1-M1, R2-M2 and R3-M1.

## AUD-21-02

**Status** passed

**Claim pointer** The sample-implied active-halo SFR factors have BT/PL marginal-median ratios 0.123,0.195,0.308 at 1e9,1e10,1e11 Msun.

**Evidence pointer** Main abstract; body lines 142–148 and 173; chains/pl_100k.h5 and kp1_ms1p5_100k.h5; data/SFR_INTERPRETATION.json.

**Check and result** Substituting the existing stellar-mass relation and eta_star transformation gives S=min[1,10^eta_star t_star (M/1e10)^alpha_star]/t_star. Row-wise evaluation with the cap yields ratios 0.122772464,0.194768896,0.307921592. At 1e10 Msun the PL and BT medians are 0.118501182 and 0.023080344. No retained row in either model reaches the cap at that mass.

**Impact** The reported algebra and numerical transformation pass. This is a per-active-halo quantity. Halo abundances, duty cycle and escape fraction are not included, so the ratios do not measure total emissivity or establish a compensation mechanism.

**Reviewer overlap** All three recognize this as a supported interpretation within the specified prescription.

## AUD-21-03

**Status** passed

**Claim pointer** The active-halo contrast is not obviously created by retaining initial stored rows.

**Evidence pointer** R1 overall assessment and R2-M2; the same fixed-spectrum arrays.

**Check and result** Retaining only the chronological last half, with the same finite-log-probability mask, gives BT/PL ratios 0.121476671,0.193588001,0.306533537. These retain the same direction and are close to the all-row values.

**Impact** This is a useful selection-sensitivity check. Agreement of two overlapping summaries does not establish independent convergence or executed-target parity.

**Reviewer overlap** R1-M1 and R2-M2.

## AUD-21-04

**Status** passed

**Claim pointer** Current spectral sample medians and 95% intervals describe the last 300 of 600 stored joint steps.

**Evidence pointer** Body lines 152–160; chains/joint_kpms8_100k_600steps.h5; data/current8d_analysis.json.

**Check and result** The array has 600×32×8 coordinates and 19,200 finite log-probability rows. The retained slice has 9,600 rows. KP q025/median/q975 is 4.419969654/17.705716030/29.071113734. MS is 0.583505204/1.813331555/3.962328441. Values reproduce the manuscript's rounding.

**Impact** The empirical intervals reproduce. Their probability construction does not establish that the retained rows represent the intended posterior.

**Reviewer overlap** R1-m1, R2-M3 and R3-M1.

## AUD-21-05

**Status** passed

**Claim pointer** The source contains adverse current-run monitors that are not quantitatively presented with the main spectral figure.

**Evidence pointer** Body lines 156–169; data/current8d_analysis.json, diagnostics.last300; current joint raw array.

**Check and result** Independently recomputed the ordinary variance-ratio split monitor across interacting walkers for the retained 300 steps, splitting them into two 150-step halves. The eight values span 2.145101544 to 3.446218014; KP is 2.323163530 and MS is 2.218052176. They match the stored diagnostic record. These are not independent-chain, rank-normalized Rhat estimates, and they must not be presented as such.

**Impact** The source diagnostics are a concrete warning against inferring weak observational information from broad sample distributions. The manuscript acknowledges unresolved stability, so this is not a demonstrated arithmetic contradiction. Its reporting is too generic relative to the available diagnostic evidence. Showing the values or placing the spectral display in an exploratory appendix would improve interpretation without adding repeated disclaimers.

**Reviewer overlap** R1-m1, R2-M3 and R3-M1.

## AUD-21-06

**Status** provenance_gap

**Claim pointer** Fixed-spectrum differences can be interpreted as a galaxy response to a controlled spectrum intervention.

**Evidence pointer** Body lines 45,129–173; fixed HDF5 attributes; current joint HDF5 attributes; data/SOURCES.json.

**Check and result** Raw files establish coordinates, source bytes and selections. The joint file has no attributes. The packet does not establish the executed prior support, full likelihood, numerical branch and complete common configuration of the principal PL/BT comparison. In particular, eta_star/t_star support can differ from a transformed native-coordinate support.

**Impact** The numerical difference is well defined. Attribution to the spectrum under otherwise common inference assumptions remains unverified. This is not evidence that the assumptions actually differ.

**Resolution test** Export and reconcile the actual run identities, targets, priors, fixed settings and predictor definitions, then establish stability for the quantities interpreted physically.

**Reviewer overlap** R1-M1, R2-M2, R3-M1. Blocking status differs across reports.

## AUD-21-07

**Status** unresolved_input_needed

**Claim pointer** The collection of results explains how galaxy freedom accommodates spectral changes.

**Evidence pointer** Table tab:experiment-map and body lines 91–173.

**Check and result** The fixed-history response, large-break LF compatibility and strongest small-break SFR contrast remain different experiments and scale regimes. A matched before/after LF and history comparison is absent. The paper explicitly recognizes compensation and weak direct sensitivity as alternatives.

**Impact** A narrow conditional interpretation is supported. A quantified compensation or information-loss mechanism is not established. The uncertainty is not repaired by an additional disclaimer.

**Reviewer overlap** R1-M2, R2-M1 and R3-m1, with different severity emphasis.
