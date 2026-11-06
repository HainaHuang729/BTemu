# Review setup

Input is the complete physics manuscript v0.21 and the common immutable manuscript/source packet. The author asks whether its main line, physical explanation and conclusion support are clear, and whether defensive or repetitive prose remains. No manuscript edit is requested.

Emphasis briefs fixed before launch

1. R1 foregrounds technical soundness, numerical estimands and support for physical claims.
2. R2 foregrounds the scientific argument, physical significance, originality and the relation between question and completed result.
3. R3 foregrounds readability, physical explanation, repetition, caveats and main-text/appendix hierarchy.

All reviewers cover the five criteria. Each receives only the common packet, criteria and its own emphasis in an isolated context. Reports are finalized and frozen before audit and synthesis. No earlier reports, shared concerns, synthesis hints or prior review ledgers are supplied.


# Reviewer 1

## Review setup

**Input scope** Complete physics manuscript v0.21, including the immutable source packet, numbered text, figures, numerical summaries and released fixed-spectrum and 600-step joint chains.

**Assessment boundary** This assessment addresses the supplied numerical experiment. Native binaries, predictor weights and complete production configurations are external. 

**Shared manuscript claim summary** Spectrum changes separate fixed-galaxy histories; independent galaxy fits can produce similar LFs; fixed-spectrum sample transformations give lower active-halo star formation in one BT case; free-spectrum samples remain broad.

**Visible evidence base** The manuscript and supplied records support checking the reported sample statistics and the distinctions among numerical products. They do not independently establish the executed likelihood and prior of every chain.

## Overall assessment

The narrow descriptive conclusions are largely supported and unusually careful about their limitations. I independently reproduced the three BT-to-PL ratios of marginal median star-formation factors, 0.12277, 0.19477 and 0.30792, from the released chains. The last-half selections give 0.12148, 0.19359 and 0.30653, respectively. Thus the reported contrast is neither an algebraic error nor an obvious consequence of retaining the initial half alone. I also reproduced the joint-chain marginal quantiles quoted in the text. These checks establish finite-sample transformations, not posterior calibration or a physical explanation for the differences.

The main limitation is the scientific endpoint. The article establishes conditional sensitivity and the existence of candidate compatible fits, while explicitly leaving the separation of weak sensitivity and compensation unresolved. The physical insight required for a broad journal is not yet demonstrated.

## Who would be interested in the results, and why

Researchers studying reionization, high-redshift galaxies and small-scale matter spectra would value a controlled measurement of how galaxy freedom obscures spectrum changes. The connection between cosmology and uncertain source prescriptions could interest a wider astrophysics audience if the study determines which observables retain spectral information and why.

## Major strengths

The experiment map makes meaningful distinctions among conditional histories, fitted LF curves and sampled parameter distributions. The star-formation factor follows transparently from the capped galaxy prescription. Its interpretation correctly excludes halo abundance, duty cycle and escape fraction. The atlas figure visibly identifies the boundary-saturated history. Failed LF diagnostics do not negate the existence of the displayed candidate curves, and the text appropriately avoids converting their stored maxima into significance or evidence ratios.

## Major Concerns

### R1-M1

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness and reproducibility  
**Claim pointer** The fixed-spectrum samples select lower active-halo star formation for the specified BT case than PL, and the joint projection describes the status of spectrum inference.  
**Evidence pointer** main_numbered.txt line 29; body_numbered.txt lines 129-169, 191-215 and 247; Table `tab:fixed-100k`; Figure `fig:physics-kpms-current`; data/current8d_analysis.json fields `prior_status` and `diagnostics`; released HDF5 attributes.

**Concern** The transformation is reproducible, but the physical comparability of its inputs remains unverified. The fixed-chain files identify spectrum labels but do not encode their executed priors or likelihood configurations. The joint file has no run attributes. This matters particularly because lines 45 and 169 already identify potentially different prior supports and unestablished common settings. A common coordinate name is insufficient to establish a common target. The small last-half sensitivity cannot repair this provenance gap. Likewise, the older exact comparison uses an unconverged smoke chain and cannot validate the current 100k-model comparison across spectra.

**Why it matters** Readers can accept the numerical ratios as summaries of these arrays, but cannot yet attribute the contrast to changing the matter spectrum under otherwise common inference assumptions. This does not invalidate the explicitly bounded descriptive conclusion, hence the nonblocking designation.

**Resolution test** Supply the executed configuration and prior support for PL, BT1 and the joint run, including the coordinate transformation, fixed galaxy coordinates and predictor identity. Demonstrate independent-ensemble stability for the quantities interpreted physically and check relevant exact history-likelihood errors at representative PL and BT samples. Alternatively, retain the ratios strictly as archive summaries and remove any implication that they already establish a data-selected physical response.

### R1-M2

**Severity** Major  
**Blocking** No  
**Axis** Scientific importance and physical explanation  
**Claim pointer** The combined calculations illuminate spectrum sensitivity and galaxy freedom, while compensation remains a possible explanation of fit compatibility.  
**Evidence pointer** body_numbered.txt lines 23, 91-123, 148 and 165-173; Figures `fig:atlas-history` and `fig:lf-fits`; Table `tab:experiment-map`.

**Concern** The central comparisons change both the observable and the experimental construction. The fixed-galaxy evidence concerns ionization histories, whereas the fitted evidence concerns LFs. Neither comparison measures how much of the same observable's initial spectrum response is removed by galaxy adjustment. Moreover, at fixed sigma8 the spectrum normalization changes with shape. An enhanced high-k slope alone therefore does not explain the magnitude or scale dependence of the source response. The present discussion mostly restates the sequence of numerical findings rather than tracing it through halo abundance and source weighting.

**Why it matters** The manuscript correctly acknowledges the missing comparison, so this is not an unsupported claim of demonstrated compensation. It nevertheless leaves the proposed physical question unanswered and materially weakens originality and wider importance.

**Resolution test** For selected spectra, compute the same LF and history observables before and after galaxy adjustment under matched numerical settings. Quantify the response removed and retained. Show the actual normalized spectrum or mass variance and the resulting halo/source weighting over the relevant masses. This would distinguish weak direct sensitivity from compensation.

## Minor Comments

### R1-m1

**Severity** Minor  
**Axis** Readability and statistical reporting  
**Affected element** Current joint-chain status  
**Evidence pointer** body_numbered.txt lines 156-169; Figure `fig:physics-kpms-current`; data/current8d_analysis.json, `diagnostics.last300`.

**Issue** The packet already contains adverse current-run monitoring results, whereas the main text gives a generic preliminary-status warning. The ordinary interacting-walker split ratios for the selected half range approximately from 2.15 to 3.45. They are not independent-chain Rhat estimates, but are more informative than the generic warning.

**Required correction** Report these as descriptive warning diagnostics, with their dependence limitation. Keep the numerical intervals explicitly empirical and explain that 300 retained steps are a convention rather than diagnosed burn-in.

### R1-m2

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Repeated provenance and defensive prose  
**Evidence pointer** body_numbered.txt lines 106, 112, 119, 123, 129, 165-173 and 290-307.

**Issue** Necessary boundaries are repeated alongside editorial bookkeeping. The two references to the same LF status at line 106 and the opening statement about replacing an earlier unspecified report at line 129 interrupt the scientific argument. The T3 appendix also repeats selections and provenance across prose and caption.

**Required correction** Consolidate repeated provenance statements and remove revision-history language. Preserve the boundary-saturation explanation, failed-diagnostic status, active-halo definition and distinction between representative-history and IC-marginalized likelihoods. Those qualifications prevent specific incorrect interpretations and should not be removed as mere defensiveness.

## Technical failings that need to be addressed before the case is established

R1-M1 limits physical attribution of the sample contrast. R1-M2 limits the explanation of galaxy compensation and the broader scientific case. No blocking defect is demonstrated for the manuscript's expressly restricted claims of conditional numerical sensitivity and candidate-fit existence.

## Assessment against Nature-style criteria

**Originality** A potentially useful controlled application, but the distinctive physical conclusion beyond sensitivity and compatibility remains incomplete. **Scientific importance** Relevant to interpreting reionization constraints, with magnitude and consequences still unquantified. **Interdisciplinary readership** Plausible across cosmology and galaxy formation; broader implications require a clearer discriminating result. **Technical soundness** Recomputed summaries are correct, while target comparability and physical inference remain provisional. **Readability for nonspecialists** The main sequence is understandable; the physical mechanism needs more explanation and the provenance material needs compression.

## Recommendation posture

Substantive revision is warranted before treating this as an established physics inference. The descriptive results are credible within their stated definitions. A matched observable comparison and verified common inference targets would determine whether they support a stronger scientific contribution.

## Risk / unsupported claims

Posterior exclusion, calibrated compensation, stable mock recovery and equivalence to IC-marginalized inference are not established by the packet. The manuscript generally states these boundaries faithfully.


# Reviewer 2

**Input scope** Complete physics manuscript v0.21, numbered source, supplied figures, frozen summaries and six raw chain files in `packet/chains/`. This assessment emphasizes the scientific line, physical significance and originality. External priority and unpublished companion validation are not independently assessable.

**Overall assessment** The manuscript establishes a useful bounded result. Changing the spectrum at fixed galaxy parameters separates exported ionization histories, and independently adjusted galaxy prescriptions can accompany compatible LF curves. The conversion from sampled galaxy coordinates to active-halo star formation is the clearest physical result. However, the evidence does not yet determine whether observational compatibility arises from intrinsically weak spectral sensitivity or compensating galaxy freedom. The authors acknowledge this accurately. The remaining challenge is to make the completed physical advance, rather than the inventory of numerical products, carry the article.

**Who would be interested in the results, and why** Reionization researchers, galaxy-formation modellers and cosmologists studying small-scale structure would value a quantitative demonstration of how assumed matter spectra change inferred source properties. More broadly, this is an example of the difficulty of recovering fundamental physics through uncertain luminous tracers. The latter implication becomes compelling only when the direct and adjustable responses are compared consistently.

**Major strengths** The manuscript distinguishes fixed-galaxy interventions, LF fitting and marginalized sampling. It avoids interpreting likelihood maxima as significance and does not claim spectral exclusion. The displayed star-formation factor at body lines 142-148 translates abstract coordinates into a mass-dependent physical quantity. The distinction between active-halo star formation and total emissivity is particularly helpful. Raw samples and explicit selection definitions permit scrutiny beyond rounded tables.

## Major Concerns

### R2-M1

**Severity** Major  
**Blocking** No  
**Axis** Originality and scientific importance  
**Claim pointer** Introduction, body lines 3-7, and physical interpretation, lines 165-173, present the interplay between spectral response and galaxy freedom as the scientific subject.  
**Evidence pointer** Body lines 91-123, 148 and 165. Fixed-galaxy histories, large-break LF compatibility and the strongest small-break galaxy shift are separate comparisons.

**Concern** The article demonstrates three facts but does not establish their quantitative relationship. In particular, comparable LF fits at large break scales may reflect weak direct LF response, whereas the striking star-formation reduction is demonstrated at a small break scale. These do not by themselves measure compensation. The explicit acknowledgement at line 165 prevents an overclaim, but also leaves the main interpretive question open. The introduction distinguishes the adopted prescription from Park et al.'s experiment without explaining which completed result changes the physical understanding supplied by that prescription.

**Why it matters** A descriptive coexistence of sensitivity and fit compatibility supports a narrower advance than an identified physical degeneracy. Outstanding importance and originality are therefore not yet demonstrated by the manuscript's own argument. This does not invalidate the conditional calculations.

**Resolution test** Identify one completed quantitative physical conclusion as the principal advance and distinguish it from the adopted framework. If compensation remains the intended result, compare the same LF and history observables before and after galaxy adjustment under matched numerical definitions. Otherwise organize the article around the bounded conditional result and explain its specific consequence. No claim of external priority can be verified from this packet alone.

### R2-M2

**Severity** Major  
**Blocking** Yes  
**Axis** Technical soundness and conclusion support  
**Claim pointer** Abstract, main line 29, and conclusion, body line 173, attribute lower active-halo star formation to the selected BT case relative to PL.  
**Evidence pointer** Body lines 45, 132-148, 169 and 215; `chains/pl_100k.h5`, `chains/kp1_ms1p5_100k.h5`, and `data/SOURCES.json`.

**Concern** The headline ratios are reproducible descriptive summaries, but the executed prior and likelihood parity needed to interpret their difference as a spectrum-dependent galaxy response remain unestablished. The raw fixed-spectrum files identify coordinates and spectrum labels, but do not document the full executed inference target. The manuscript itself says common settings and executed priors remain to be established. This is consequential because the text explains that changing to a rectangular prior in efficiency per timescale changes the allowed galaxy population.

**Why it matters** The lower-star-formation result carries most of the article's distinct physical content. A difference between samples drawn under unidentified targets cannot establish a controlled physical comparison. This concern blocks that interpretation, rather than the arithmetic or the existence of the samples. As a limited positive check, separately flattening finite-log-probability rows in each chronological quarter gives pivot-factor medians about 0.1180-0.1189 for PL and 0.0228-0.0234 for BT. Thus the difference is not merely an obvious early-step artifact, although this is not independent convergence evidence.

**Resolution test** Recover the executed priors, likelihood definitions, fixed coordinates, numerical PL branch and predictor identity for both runs, and show they differ only in the intended spectrum intervention. Establish stability adequate for the claimed population comparison. Alternatively restrict the headline to a descriptive contrast between these particular archived samples and remove its attribution to a controlled galaxy response.

### R2-M3

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness and physical interpretation  
**Claim pointer** Body lines 152-160 describe the projected 600-step sample alongside archived uniform-prior densities.  
**Evidence pointer** Figure 4; `data/current8d_analysis.json`, fields `prior_status`, `primary_selection` and `diagnostics.last300`; body line 169.

**Concern** The visible comparison suggests modest suppression of low break scales after galaxy marginalization, but the prior is only an archived reference and the retained interval is not diagnosed burn-in. The supplied diagnostic record gives ordinary interacting-walker split ratios about 2.15-3.45 for the retained sample, with every length-to-autocorrelation heuristic failing. These monitors are not independent-chain diagnostics, but their values make the current broadness scientifically indeterminate. The general caveat in the discussion does not convey this evidence as directly as the figure conveys a 95% region.

**Why it matters** Broad sampling cannot yet answer whether the observations contain little spectral information. The authors correctly avoid exclusion limits; the same restraint should govern the implied prior-to-sample comparison.

**Resolution test** Report the current chain's diagnostics beside Figure 4 and distinguish sampled coverage from a demonstrated marginalized distribution. Verify the executed prior before interpreting departures from it. Retaining the figure as an explicitly noninferential exploration record would also resolve this concern without additional sampling.

## Minor Comments

### R2-m1

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Results and discussion transitions  
**Evidence pointer** Body lines 106, 112, 119, 123, 165, 169 and 173.  
**Issue** Repeated statements of archive status, diagnostic failure and limited interpretation interrupt the physical narrative. Line 129 also describes replacement of an earlier report, which requires version history to understand.  
**Required correction** Consolidate numerical-status qualifications in the experiment map and relevant captions, retain the necessary conclusion-level limitation, and describe the current calculation directly. Preserve all substantive caveats.

### R2-m2

**Severity** Minor  
**Axis** Physical interpretation and readability  
**Affected element** Spectrum prescription  
**Evidence pointer** Body lines 13-25 and 148.  
**Issue** Readers are given break wavenumbers and halo masses without a bridge explaining which source population each break can affect. Fixed normalization also changes the amplitude outside the modified branch.  
**Required correction** Explain this scale relationship and normalization consequence in plain language, while avoiding an unmeasured claim about the actual halo-abundance response.

**Technical failings that need to be addressed before the case is established** R2-M2 is necessary for a controlled physical interpretation of the headline galaxy shift. R2-M3 limits spectral inference; R2-M1 limits the demonstrated significance.

**Assessment against Nature-style criteria** Originality is incompletely distinguished within the supplied context. Scientific importance is plausible but rests on an unresolved physical separation. Interdisciplinary interest lies in uncertain-tracer inference. Technical soundness is strongest for descriptive calculations and weakest for target parity. Nonspecialist readability benefits from the source prescription but suffers from archival detail and repeated qualifications.

**Recommendation posture** Substantive revision. The current bounded conclusions are mostly candid; the strongest physical comparison needs a verified inference basis and a clearer statement of what has actually been learned. Final journal suitability is an editorial judgment.


# Reviewer 3

## Review setup

**Input scope** Complete physics manuscript v0.21, its immutable source packet, numbered text, supplied figures and numerical records.

**Assessment boundary** This assessment concerns the physics article and its visible evidence, not the companion methods manuscript. Executed production configurations and the external native implementation cannot be independently assessed here. All line references below refer to `body_numbered.txt` unless explicitly identified as `main_numbered.txt`.

**Shared manuscript claim summary** Fixed-galaxy histories respond to changes in the spectrum; independently fitted LF curves can remain compatible; selected galaxy samples give lower active-halo star formation for one BT case; preliminary joint samples remain broad.

**Visible evidence base** The spectrum and galaxy equations, matched atlas histories, LF fits, fixed-spectrum summaries, `SFR_INTERPRETATION.json`, `current8d_analysis.json`, and the current spectrum-marginal figure.

**Missing materials affecting confidence** Verified executed priors and shared run settings, independent convergence evidence, and current likelihood-error validation are explicitly unresolved at lines 0169 and 0179.

## Overall assessment

The argument has a clear and scientifically legitimate core. Its strongest explanatory passage is the conversion of sampled coordinates into an active-halo star-formation factor at lines 0142-0148. The conclusion at line 0173 is substantially supported when read literally as a description of supplied numerical products. It does not establish compensation, a robust spectral constraint, or a measured change in total emissivity, and the manuscript generally respects those boundaries.

The remaining problem is the distance between this restricted descriptive result and a physical inference about the spectrum-galaxy interplay. Numerical comparisons are unusually carefully qualified, but their limitations sometimes receive more explanatory attention than the physics that makes them interesting. The article needs clearer evidential hierarchy and a more direct account of what its numerical response teaches us.

## Who would be interested in the results, and why

Researchers studying reionization, early galaxies and small-scale structure would be interested because an altered source population and altered galaxy efficiency can affect overlapping observables. The broader appeal is an inference problem shared across astrophysics, namely distinguishing a change in the underlying population from a change in how individual objects emit radiation. That appeal depends on explaining the population-to-observable connection concretely.

## Major strengths

The introduction identifies the two sources of freedom without assuming that one explains the other. Table I explicitly separates physical interventions from numerical products. The LF discussion treats stored maxima as examples of compatible curves rather than model-selection evidence. The star-formation calculation preserves the efficiency cap, evaluates the samples themselves, and correctly distinguishes ratios of marginal medians from paired ratios. Its reported values agree with the supplied interpretation record. Moving historical recovery exercises and exploratory distributions into appendices also protects the current main result from unsupported claims.

## Major Concerns

### R3-M1

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness and claim moderation

**Claim pointer** The fixed-spectrum distributions are presented as a galaxy response, and the joint projection is introduced through the spectral posterior marginal at lines 0125-0156. These results feed the physical interpretation and conclusion at lines 0165-0173.

**Evidence pointer** Lines 0045, 0132, 0156-0160, 0169 and 0215. `current8d_analysis.json` explicitly records unverified executed priors, no diagnosed burn-in, and poor ordinary interacting-walker split monitors. For the selected last 300 steps, the reported spectrum-coordinate ratios are approximately 2.32 and 2.22; these are monitors, not independent-chain convergence estimates.

**Concern** The descriptive calculations are credible, but comparability and sampling stability are not established sufficiently to interpret their shifts as stable model-conditioned galaxy inference. All finite-probability rows are used in the fixed-spectrum comparison without chronological discard. The manuscript itself explains that alternative coordinate-prior supports differ. Likewise, projecting stored rows is mechanically correct but estimates the intended posterior only if those rows adequately sample the stated target. Calling the distributions preliminary is necessary, but the current figure and posterior equation still invite a stronger reading than the available diagnostics support.

**Why it matters** This materially limits the physical interpretation and reproducibility, especially the apparent low-break-scale depletion. It does not block the narrower case that these stored samples differ and these candidate LF curves exist.

**Resolution test** Document the executed targets and prior supports for the compared products, demonstrate retention and independent-run stability for any inference retained as physical evidence, and assess the relevant approximation error. Alternatively, explicitly introduce the current plots as empirical sample projections before the posterior equation and restrict the physical conclusions to those descriptive products. A broad sample range alone must not become evidence of intrinsically weak observational information.

## Minor Comments

### R3-m1

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Physical bridge from spectrum to sources  
**Claim pointer** Spectrum changes affect the source population and ionization history.  
**Evidence pointer** Lines 0003, 0013-0025, 0043, 0091-0100 and 0148.

**Issue** The reader is given the spectrum equation and later the star-formation interpretation, but little connective explanation of which halo population should respond and why earlier ionization is physically expected. Fixed sigma-eight renormalization and the distinct numerical PL reference make an unqualified “more small-scale power” explanation insufficient.

**Required correction** Add a compact explanation connecting the altered spectrum, halo abundance, galaxy luminosity and ionizing emissivity. State which links are model expectations and which are actually demonstrated. A numerical halo-abundance claim would require evidence; an accurate qualitative account need not become another experiment.

### R3-m2

**Severity** Minor  
**Axis** Writing clarity  
**Affected element** Repetition and administrative prose  
**Claim pointer** Main-text explanations of provenance and inferential scope.  
**Evidence pointer** Lines 0106, 0129, 0165, 0169 and 0173; `main_numbered.txt` lines 0029 and 0032.

**Issue** Line 0106 points to the numerical LF table twice within one paragraph. Line 0129 leads with what the table “replaces”, which describes revision history rather than physics. The sensitivity/compatibility/matched-comparison sequence recurs in the abstract, line 0165 and the conclusion, while line 0169 adds another status inventory. The working-draft notice is also administrative.

**Required correction** Remove the duplicated table pointer and revision-history opening. Let the abstract state the result, the discussion explain its physical meaning, and the conclusion state the resulting knowledge and single decisive remaining test. Preserve the failed-diagnostic qualification in the LF caption, the unresolved high-redshift boundary in the history caption, and the active-halo versus total-emissivity distinction. Those qualifications change scientific interpretation and are not removable defensive language.

### R3-m3

**Severity** Minor  
**Axis** Main-text and appendix hierarchy  
**Affected element** Peripheral source-reconciliation details  
**Claim pointer** Implementation discrepancies and supporting historical observation combinations.  
**Evidence pointer** Lines 0074, 0084, 0167, 0304-0307 and 0474-0475.

**Issue** The adapter-versus-metadata discrepancy at line 0074 interrupts the observational model. Line 0167 brings the unavailable-chain T3 comparison back into the main discussion after correctly assigning it supporting status. Both increase the apparent number of scientific threads without strengthening the central conclusion.

**Required correction** Keep the actual optical-depth integration prescription in the main text and collect the metadata discrepancy with provenance. Retain the physical explanation of complementary observables at line 0167, but place the T3 status discussion entirely with its appendix evidence.

## Technical failings that need to be addressed before the case is established

R3-M1 limits any stable posterior or galaxy-response interpretation. No additional blocking defect is identified for the explicitly conditional, descriptive conclusion.

## Assessment against Nature-style criteria

**Originality** The combined numerical comparison appears original within the packet, but its distinction from the adopted Park framework is mainly the altered spectrum and assembled comparisons. Priority cannot be independently verified here.

**Scientific importance** The inference question is important. Outstanding significance is not yet demonstrated by conditional sensitivity and compatible fits alone.

**Interdisciplinary readership** Potentially broad astrophysical interest, provided the source-population explanation becomes more concrete.

**Technical soundness** Descriptive calculations are supported; target parity, sampling stability and spectral discrimination remain unresolved.

**Readability for nonspecialists** The main sequence is understandable. Physical explanation should replace administrative detail, rather than removing scientifically necessary qualifications.

## Recommendation posture

Substantive clarification and targeted validation would strengthen the article. The present evidence supports a bounded physics demonstration, with wider inferential significance still conditional.

## Risk / unsupported claims

The packet does not establish quantified galaxy compensation, calibrated exclusion limits, or a change in halo-integrated ionizing emissivity. These should remain outside the conclusions unless supported by additional evidence.


# Cross-review synthesis (post-review; not shown to reviewers)

## Overall assessment

The physical line is understandable and the manuscript's restricted conclusions are mostly supported. Conditional history sensitivity, existence of compatible LF candidate curves and sample-implied active-halo SFR factors form a coherent descriptive study. The quantitative SFR interpretation is the clearest bridge from coordinates to physics.

The remaining distinction is between a reproducible description of these arrays and a controlled physical inference about galaxy response to the spectrum. The first is largely established. The second still depends on common executed targets, sampling stability and the matched observable comparison that separates compensation from weak sensitivity. The source does not establish an observational spectrum constraint.

## Consensus strengths

All three reports recognize the physical intervention map, separation of numerical products, explicit median definitions and restrained interpretation of LF maxima. All find the SFR-factor interpretation useful and correctly bounded to active halos. The main result is no longer an unspecified table of reported centres and spreads.

The post-review audit reproduces the full fixed-spectrum summary table, SFR ratios and selected joint quantiles. An all-row versus last-half check leaves the SFR contrast close to its reported magnitude. These checks strengthen the descriptive result without validating the inference target.

## Consensus blocking concerns

No concern is unanimously designated Blocking Yes for the explicitly narrow descriptive claims. R1 and R3 identify no blocking defect for conditional numerical sensitivity and candidate-fit existence. R2-M2 marks executed-target parity blocking for the stronger physical attribution of the headline galaxy shift. This difference in claim boundary is substantive and is preserved.

The common target-parity concern is shared by R1-M1, R2-M2 and R3-M1, but the synthesis does not turn it into a three-report blocking consensus. If the abstract is intended to claim a controlled, data-selected BT-versus-PL response, R2's evidence requirement applies. If it is restricted to the particular finite archive samples, the claim must remain explicitly at that level.

## Other consensus major concerns

**S1. Common executed inference targets remain unverified.** R1-M1, R2-M2 and R3-M1 agree that file hashes, named coordinates and correct transformations cannot establish actual prior, likelihood, predictor and fixed-setting parity. The prior-coordinate issue is particularly relevant. Small retention-window sensitivity helps but does not close this gap.

**S2. The strongest physical explanation stops before compensation is measured.** R1-M2 and R2-M1 are nonblocking Major concerns on this point. R3-m1 makes the related qualitative physical-bridge issue Minor. Large-break LF compatibility and a small-break SFR shift do not determine what happens to the same observable before and after galaxy adjustment. The paper accurately acknowledges that alternative weak-sensitivity explanation, but its distinctive scientific increment remains modest until a matched comparison or a sharper bounded result carries the argument.

**S3. The current free-spectrum figure is more inferentially suggestive than its diagnostics justify.** R2-M3 and R3-M1 address this as Major, with R1-m1 a reporting comment. The selected-half monitors span about 2.15–3.45. These are ordinary interacting-walker diagnostics, not independent-chain Rhat, yet they are an important warning. A generic preliminary label does not convey this as clearly as the 95% region conveys apparent posterior structure. Quantitative status beside the display or relocation to an exploratory appendix are both possible resolutions. Stable sampling would be required for observational interpretation.

## Where emphasis differs across reviewers

R1 emphasizes literal reproducibility and finds that the stated descriptive claim can survive the missing target information. R2 treats the physical attribution of the headline sample contrast more strictly and makes target parity blocking for that interpretation. R3 emphasizes explanatory hierarchy, a qualitative spectrum-to-source bridge and removal of administrative prose.

R1 independently checked all-row and last-half SFR ratios. R2 also reports a chronological-quarter check at the pivot. These are separate descriptive robustness checks, not an independent-ensemble convergence result.

## Main line and physical explanation

The main line is clear, but the discussion could give more physical explanation and less summary repetition. The factor S establishes how eta_star and alpha_star determine active-halo star formation at a specified mass. It does not measure the number of halos, the active fraction, escaped photon weighting or integrated emissivity. This distinction is scientifically useful and should remain.

The remaining explanatory bridge is the actual normalized matter spectrum and its effect on the halo population relevant to the LF selection. A qualitative account can explain the model expectation, with fixed-sigma8 normalization stated accurately. A numerical halo-abundance or compensation claim would need the corresponding evidence. Avoid turning this request for explanation into an unsupported mechanism assertion.

## Repetition and defensive wording

| Location in body_numbered.txt | Remaining issue | Recommended treatment |
|---|---|---|
| 106 | The same LF numerical table is referenced twice in one paragraph | Keep one reference |
| 129 | “replaces the earlier unspecified centre-and-spread report” describes revision history | State the current statistic and calculation directly |
| 74 | Optical-depth adapter versus metadata discrepancy interrupts the physical likelihood definition | Keep the executed prescription in the main text; move discrepancy details to provenance |
| 167 | T3's unavailable-source status is brought back into the main discussion | Keep the complementary-observable explanation; leave supporting T3 status with its appendix |
| 165 and 173, plus abstract | The sensitivity/compatibility/matched-comparison sequence is repeatedly restated | Use the abstract for the result, discussion for physical meaning, and conclusion for the one completed takeaway and decisive next test |
| 290–307 | T3 selections and source limitations repeat across prose and caption | Consolidate in one local provenance statement |
| 169 | A generic inventory of unresolved inference issues accompanies a more confident-looking main figure | Report the concrete diagnostic status or change the figure's role, instead of adding repeated generic caution |

The failed LF diagnostic gate, unresolved high-redshift saturated history, active-halo definition, and representative-history/IC-target distinction prevent specific scientific misreadings. They are necessary qualifications. They should not be deleted under a blanket instruction to remove defensive writing.

## Forensic consistency findings

The audit was run only after all reports were frozen.

- All 30 fixed-spectrum coordinate/model summaries reproduce, including the missing-in-earlier-record t_star coordinate and every source CSV quantile.
- The SFR ratios reproduce as 0.122772,0.194769,0.307922. The last-half values are 0.121477,0.193588,0.306534. The substantive descriptive contrast persists in that check.
- Current KP/MS medians and equal-tail endpoints reproduce to printed precision from 9,600 selected rows.
- The selected-half ordinary split monitors reproduce as 2.1451–3.4462, including KP 2.3232 and MS 2.2181. They must not be relabeled independent-chain Rhat.
- The joint file's missing executed-target attributes and the unresolved common-prior provenance remain a gap, not proof of a wrong prior.

No main-result arithmetic contradiction was found in these checks. FORENSIC_AUDIT.md separates passed calculations, provenance gaps and missing physical comparisons. It is not a fourth reviewer or a source of retroactively edited reviewer consensus.

## Minor-revision checklist

- Remove the duplicate LF table pointer and table-replacement history (R1-m2, R2-m1, R3-m2).
- Move the optical-depth metadata discrepancy to provenance (R3-m3).
- Keep T3's pending-source discussion in its appendix (R3-m3).
- Add a concise qualitative spectrum-to-halo-to-source explanation, separating expectations from measured quantities (R2-m2, R3-m1).
- Reduce repeated result-roadmap text without deleting model definitions or result-relevant qualifications (R1-m2, R2-m1, R3-m2).
- Present the current-run warning quantitatively or give the free-spectrum figure an exploratory supplementary role (R1-m1; related R2-M3 and R3-M1).

## Broad-interest / significance readout

The bounded study is useful for reionization, galaxy formation and small-scale cosmology. Its significance is clearest as a demonstration of model-conditioned source-property changes. An outstanding physical inference or a measured compensation mechanism is not established. The packet does not independently establish external priority, and no report claims an editorial decision.

## Most important issues to resolve

Keep the current intervention-based main line and the SFR interpretation. Make the headline's inference scope unambiguous, recover the executed PL/BT targets, and choose whether the short free-spectrum sample belongs in the main physical result. For a stronger compensation claim, the decisive evidence is a matched before-and-after observable comparison. Repeated disclaimers cannot replace it.

# Risk / unsupported claims

- Reproduced marginal-median ratios do not by themselves establish a controlled posterior response to the spectrum.
- Active-halo SFR factors are not halo-integrated emissivity ratios.
- Large-break LF compatibility and small-break SFR shifts do not quantify the same compensation process.
- A 95% empirical sample region and a broad MS histogram do not establish weak observational information under the actual prior.
- Current ordinary walker monitors must not be presented as independent-chain Rhat estimates.
- Native spectrum normalization, actual executed targets, relevant likelihood fidelity and external novelty remain only partly assessable.
