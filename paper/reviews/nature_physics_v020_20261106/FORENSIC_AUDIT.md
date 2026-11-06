# Forensic consistency audit

The independent reports were finalized and hashed before this audit. No findings were returned to reviewers and no frozen report was edited. Numerical results are recorded in AUDIT_VALUES.json.

## AUD-P01

**Status** passed

**Claim pointer** The T3 sample spread decreases most strongly in the escape-fraction normalization.

**Evidence pointer** packet/body_numbered.txt lines 168 and 317–328; packet/data/t3_update_20261103/t3_obs_combinations.json.

**Check and result** From LF-only to the joint summary, the F_ESC10 population standard deviation changes from 0.866633630 to 0.386434762, a decrease of 0.480198868 or 55.4097%. This is the largest decrease among the six listed coordinates. M_TURN decreases by 8.4480%, t_STAR by 4.5599% and ALPHA_ESC by 12.1028%. ETA_STAR and ALPHA_STAR instead increase in spread by 7.8847% and 5.4382%. The text correctly says that not every spread decreases.

**Impact** The arithmetic claim is supported as a comparison of reported sample statistics. It does not by itself establish the causal attribution to added observations.

**Reviewer overlap** R1-M1, R2-M2, R3-M1.

## AUD-P02

**Status** passed

**Claim pointer** The T3 joint row reproduces the last half of the earlier ext2 segment.

**Evidence pointer** packet/body_numbered.txt lines 175 and 317–328; BTemu/paper/chains/chain6_ext2_2000.h5, matching the source identified in the earlier chain receipt.

**Check and result** The ext2 chain has 2,000 steps, 32 walkers and six named coordinates. Stored steps [1000:2000] produce 32,000 rows. All six mean and population-standard-deviation differences from the T3 joint JSON are below 1e-12. Only this joint row was independently reconstructed in this check. The other two T3 raw files remain unavailable in the review source basis.

**Impact** The joint row's reproduction passes. Complete parity of the three T3 runs remains unresolved.

**Reviewer overlap** R1-M1, R2-M2, R3-M1.

## AUD-P03

**Status** passed

**Claim pointer** Stored LF maxima remain close to PL at larger break scales.

**Evidence pointer** packet/body_numbered.txt lines 141–158 and 342–355; packet/data/21cmtb_evidence_20261029.json, lf_grid and pl_best_log_LF.

**Check and result** The shared PL stored maximum is -13.2610407746. Across slopes, BT minus PL lies between -0.000689868 and 0.074688714 at kp=20, and -0.000138965 and 0.013701615 at kp=30. At kp=1 the stored values decrease monotonically from -11.895258269 to -143.670239485 as MS increases. All 25 grid diagnostic flags are false, as stated in the figure caption.

**Impact** The source contains comparably fitting candidate points. Failed MCMC diagnostics do not erase their existence if the likelihood and predictions are valid. They do prevent assuming the stored maxima are global optima or using their sample distributions as validated posteriors. The near-equality does not discriminate compensation from intrinsically weak sensitivity, or provide a Bayes factor.

**Reviewer overlap** R1-M2, R2-M1, R2-M3, R3-M2.

## AUD-P04

**Status** passed

**Claim pointer** Coeval xHI(8) decreases with MS at kp=10 in the second fixed-galaxy prescription.

**Evidence pointer** packet/body_numbered.txt line 129; packet/data/material_update_20261030/t2b_matched_kpms_histories.json.

**Check and result** At MS=1.5,2,3, exported xHI(8) is 0.786144061, 0.761016665 and 0.651972956, matching the text's 0.7861,0.7610,0.6520. This check verifies the supplied histories, not their native numerical implementation, IC control or uncertainty.

**Impact** The literal conditional sensitivity example is supported. It is not a comparison to the separately unverified PL entry.

**Reviewer overlap** Consistent with the strengths recognized by all three reports.

## AUD-P05

**Status** aggregation_ambiguity

**Claim pointer** The newer 100k-model fixed-spectrum centres shift with the spectrum.

**Evidence pointer** packet/body_numbered.txt lines 180–193; packet/data/model_update_20261104/RESULTS_20261104.md, section 2.

**Check and result** Reported ETA_STAR centre differences are -1.642−(-1.013)=-0.629 between kp1 and kp5 at MS1.5, and -1.642−(-0.940)=-0.702 between kp1/MS1.5 and kp10/MS2.5. The latter also changes MS, which the text states. ALPHA_STAR differences of +0.088 and +0.180 reconcile. The centre estimator and the meaning of ± in the source are unspecified.

**Impact** Arithmetic passes but posterior or uncertainty interpretation is not established.

**Resolution test** Recompute named summaries from the available raw files with explicit selection and diagnostics, rather than treating the old source ± values as known credible intervals.

**Reviewer overlap** R1-M1, R2-M2, R3-M1.

## AUD-P06

**Status** unresolved_input_needed

**Claim pointer** The physical argument separates direct spectral sensitivity from compensating galaxy adjustments.

**Evidence pointer** packet/body_numbered.txt lines 113–158, 191 and 235–239; common source records.

**Check and result** The paper combines atlas plane averages, a second coeval prescription, four-coordinate LF fits, six-coordinate observation summaries and older free-spectrum emulator samples. The manuscript discloses many differences but supplies no single matched before-and-after observable comparison across this sequence. A lack of discrimination may arise from weak direct response, adjustment, prior support or exploration.

**Impact** This is an incomplete physical bridge, not a proved numerical contradiction.

**Reviewer overlap** R1-M2, R2-M1, R2-M3, R3-M2.

## AUD-P07

**Status** provenance_gap

**Claim pointer** Newer fixed-spectrum raw chains are missing.

**Evidence pointer** R3 opening missing-materials list; packet/LATER_AVAILABLE_FILES.json.

**Check and result** The later inventory records readable raw 100k-model PL, kp1/MS1.5, kp5/MS1.5, kp10/MS2.5 and kp10/free-MS files, plus the 600-step joint 8D export. They are not integrated into v0.20. Thus a global statement that newer fixed-spectrum chains have not been delivered is too broad. What remains missing is verified alignment of v0.20's reported summaries with explicit source selections and executed configurations. The two specific T3 LF-only and LF+tau files are a separate absence and are not supplied by these newer chains.

**Impact** This editorial clarification supersedes a broad reading of the frozen R3 availability wording. It does not edit the report or invalidate its target-parity concern. Reanalysis of existing material should precede requests for new runs.

**Reviewer overlap** R1 and R2 explicitly distinguish later availability from validation of v0.20 summaries.

## AUD-P08

**Status** confirmed_internal_error

**Claim pointer** R3-m1 refers to warnings in “figure 6” for the LF grid and “figure 15” for spectrum sampling.

**Evidence pointer** R3-m1; active figure environments and labels in packet/body.tex.

**Check and result** Legacy asset numbers are not the manuscript's printed figure numbers. The LF grid is fig:lf-grid, main Figure 3; the free-spectrum focus is fig:kpms-focus, main Figure 6. The observation-combination figure is main Figure 5. Numbered source and labels supply unambiguous replacements. No manuscript figure-number error is implied.

**Impact** A reviewer cross-reference error, not a scientific error. Use the corrected label map in the synthesis while retaining the frozen report verbatim.

**Reviewer overlap** None. This is an editorial audit correction.
