# Review setup

Input scope is the immutable v0.9 packet, with full manuscript, figures and the available source records. The author requests assessment, not a manuscript edit.

Three independent contexts receive only this packet, shared criteria and their own emphasis brief. Reports are frozen before cross-review synthesis and the forensic audit.

Preassigned emphasis

1. R1 foregrounds technical validity and the relation between numerical evidence and conclusions.
2. R2 foregrounds originality, scientific significance and coherence of the scientific argument.
3. R3 foregrounds readability, defensive prose, repetition and the relation between main text and appendices.

All three cover all five criteria and the author's requested focus. No shared concern ledger or review findings are supplied to them.


# Reviewer 1

**Overall assessment**

BTemu addresses a useful question, how much information about a modified matter spectrum survives freedom in galaxy formation. The scientific sequence is clear in the Introduction, but the results currently establish a development-stage surrogate and descriptive chain summaries rather than an observational inference. The manuscript generally recognizes this distinction. Its restraint is a strength, although disclaimers cannot substitute for the missing validation. The abstract's broad sample intervals are supported by the supplied summaries. Their interpretation as weak spectral information remains provisional.

**Who would be interested in the results, and why**

Researchers studying reionization, galaxy formation and small-scale cosmology would be interested in jointly varying spectral and galaxy parameters while retaining an exact luminosity-function calculation. Wider interest would depend on a reliable demonstration of which spectral information these observations retain or lose.

**Major strengths**

The forward prescription, units and fixed normalization are explicit (body lines 15–27). The paper distinguishes the representative-history likelihood from initial-condition marginalization, correlated stored rows from independent information, and older-model checks from current-model performance. Its current marginal intervals and prior-width ratios agree with `current_analysis.json`. The finite exact comparison is appropriately described as finite-chain agreement rather than posterior fidelity (lines 247–261).

## Major Concerns

### R1-M1

**Severity** Major  
**Blocking** Yes  
**Axis** statistical-rigor

**Claim pointer** The free-spectrum calculation addresses how much spectral information remains after galaxy marginalization, and the fixed-spectrum comparison motivates joint treatment.

**Evidence pointer** Body lines 9, 123–154 and 205–207; `current_analysis.json`, fields `prior_status`, `diagnostics` and `primary_selection`; `fixed_kp1_summary.json`, field `sources`.

**Concern** Neither main comparison yet separates a scientific distribution from initialization and sampling effects. The 600-step run has unstable autocorrelation estimates and no independent-ensemble assessment. Its lower k_p sample endpoint changes from 4.101 using all steps to 4.748 using the last 150. The fixed-spectrum figure includes every finite-log-probability row without a chronological discard or corresponding convergence evidence. Moreover, the current 8D file has no run attributes confirming the archived priors. This matters especially because lines 33–47 explain that rectangular eta_star support and transformed native support represent different priors.

**Why it matters** Projecting samples is a valid marginalization operation, but it does not establish that those samples represent the intended posterior. The central scientific question cannot yet be answered by the plotted distributions, even though their descriptive quantiles are correctly reported.

**Resolution test** Export the actual joint prior, support, fixed settings, likelihood and model identity for each main run. Show consistent marginals and tail probabilities across independent ensembles with justified retained ranges and Monte Carlo uncertainty. Test whether the PL/BT shifts and low-k_p change persist. Otherwise retain these results solely as workflow demonstrations and narrow the main scientific claim accordingly.

### R1-M2

**Severity** Major  
**Blocking** Yes  
**Axis** experimental-design

**Claim pointer** The 100,000-history model supplies sufficiently accurate histories for the main inference calculations.

**Evidence pointer** Main line 28; body lines 82–116 and 215–239; `100k_metrics.json`, fields `validation_n`, `dlogL_q90` and `note`.

**Concern** The central current-model accuracy evidence is an aggregate development report. The source does not define whether its likelihood-error q90 of 1.17734 is signed or absolute. Consequently, the small trajectory RMSE cannot establish that likelihood distortion is negligible. Equal weighting over 32 nodes can dilute errors concentrated around reionization or at z=5.9. Earlier-model arrays and a smoke-only exact chain do not validate the current model. Development validation used for learning-rate changes and stopping also does not measure independent generalization.

**Why it matters** A surrogate can predict histories accurately in aggregate while changing relative likelihoods enough to alter the spectral distributions. Here that possibility is material because the inferred prior-to-sample difference is modest.

**Resolution test** Release current-model predictions and truth arrays with predictor aggregation, selections and error definitions. Evaluate an independently reserved set, including posterior-relevant regions, reporting signed bias, absolute-error tails and likelihood-error dependence on k_p and m_s. Separate realization scatter from surrogate error where possible. Demonstrate that correction or propagation of the measured errors leaves the main distributions stable within reported uncertainty, or explicitly restrict the paper to development performance.

### R1-M3

**Severity** Major  
**Blocking** No  
**Axis** mechanism-evidence

**Claim pointer** The representative predicted history is used to evaluate the observational likelihood.

**Evidence pointer** Body lines 69–76, 82 and 264–297; `earlier_IC_summary.json`, fields `single_IC_production_decision` and `family_quantiles`.

**Concern** Squared-error training on random realizations targets a mean history in an idealized limit, whereas the physical nuisance-variable likelihood averages likelihoods over realizations. The paper correctly states their non-equivalence. Its earlier audit reports q90 realization scatter of 0.948 in history log likelihood and a maximum absolute mean-history versus finite-IC likelihood difference of 1.908. These are warning signals, not evidence that the current spectral marginals are biased by a known amount. Their relevance depends on where affected families lie relative to the likelihood-supported region.

**Why it matters** Longer chains alone resolve sampling error, not a difference in the inferential target. The current explicitly approximate calculation remains interpretable, but its eventual observational interpretation requires this distinction to be quantified.

**Resolution test** At parameter families relevant to the current run, compare the representative-history likelihood with a converged realization-averaged likelihood, including uncertainty from finite realization counts. Measure the effect on spectral inference or define the reported result explicitly as conditional on the representative-history approximation. Explain why the earlier single-realization screen is or is not relevant to this target.

## Minor Comments

### R1-m1

**Severity** Minor  
**Axis** writing-clarity  
**Affected element** Main-line progression and repeated qualifications  
**Evidence pointer** Main line 28; body lines 106, 139, 154, 160, 243–261 and 309–336.

**Issue** Necessary caveats recur while the physical interpretation remains brief. Phrases such as “reproducing the supplied summary”, “uploaded” and “remaining input” emphasize file-transfer history. Multiple earlier-chain descriptions interrupt the distinction between the current scientific result and supporting checks.

**Required correction** State the current evidential boundary once near the main results and retain targeted reminders only where interpretation could change. Consolidate earlier-chain provenance into a compact appendix table. Use the recovered space to explain the galaxy-response direction and distinguish observed sample changes from their proposed physical explanation.

**Technical failings that need to be addressed before the case is established**

R1-M1 and R1-M2 block a reliable joint-inference claim. R1-M3 qualifies its physical interpretation beyond the representative-history approximation.

**Assessment against Nature-style criteria**

Originality lies in this application to a jointly variable phenomenological spectrum; the manuscript acknowledges established history emulation. Scientific importance is plausible but not established by the present preliminary distributions. Interdisciplinary readership could arise from the connection between early galaxies and small-scale cosmology. Technical soundness requires the sampling and current-model validation above. Readability for nonspecialists benefits from the opening motivation but would improve through less provenance-heavy repetition and more physical explanation.

**Recommendation posture**

Promising technical work whose observational inference is not yet established. This assessment is limited to the supplied manuscript and numerical records; external novelty, unreleased arrays and complete production configurations are not independently assessable.


# Reviewer 2

## Overall assessment

The manuscript asks a clear scientific question, namely how much information reionization observations retain about small-scale matter spectra after galaxy uncertainties are marginalized. Its present answer is an exploratory calculation rather than an established scientific result. The text accurately acknowledges this boundary. Nevertheless, descriptive chain summaries and reported development accuracy cannot yet establish either observational information loss or reliable joint inference. The main line is intelligible through the introduction, but the results culminate in prerequisites for a future answer.

This assessment covers the supplied v0.9 manuscript and packet records. I have not independently established priority against the cited literature, reconstructed unavailable validation arrays, or assessed the externally retained production implementation.

## Who would be interested in the results, and why

Reionization researchers and cosmologists testing small-scale structure would value a validated way to distinguish spectral effects from galaxy freedom. Emulator developers would also be interested in the consequences of predicting representative stochastic histories before applying nonlinear likelihoods. Broader interest depends on demonstrating a physical inference that survives these numerical choices.

## Major strengths

The question and modeling scope are explicit in body lines 3–9. Keeping the luminosity-function calculation exact isolates the approximation to the history-dependent terms. The spectrum normalization convention, coordinate transformation and statistical constructions are described unusually carefully. The manuscript separates older and current predictors and correctly avoids treating interacting walkers or an exact smoke chain as independent posterior validation. These distinctions make the remaining evidential gaps identifiable.

## Major Concerns

### R2-M1

**Severity** Major  
**Blocking** No  
**Axis** novelty-significance  
**Claim pointer** Applying history emulation to jointly varying spectrum and galaxy parameters provides the manuscript's scientific advance.  
**Evidence pointer** body lines 7–9, 123, 137–158; Table 2, the preliminary spectral marginal table at lines 146–152.  
**Concern** The manuscript distinguishes its parameterization from established history emulation, but does not demonstrate what new physical understanding follows. A shift in galaxy distributions under two assumed spectra is compatible with the opening premise; broad spectral intervals alone do not identify which galaxy freedoms absorb which spectral effects. There is no controlled comparison quantifying how spectral information changes when those freedoms are fixed or released. The current text therefore establishes an application scope more clearly than an original scientific conclusion.  
**Why it matters** Technical usefulness and outstanding scientific importance are different assessments. The supplied evidence supports a potentially useful tool, while the significance of its scientific application remains underdeveloped.  
**Resolution test** State the precise advance relative to the cited methods and demonstrate one stable physical inference. A matched fixed-versus-free galaxy comparison, supported by the relevant parameter dependencies or observable responses, could establish the proposed loss of spectral information. Alternatively, frame the contribution as a methods demonstration and substantiate its practical advantage with matched accuracy and computational-cost evidence.

### R2-M2

**Severity** Major  
**Blocking** Yes  
**Axis** statistical-rigor  
**Claim pointer** The projected eight-dimensional samples describe how observations restrict the spectral coordinates relative to their priors.  
**Evidence pointer** body lines 137–154 and 205–207; `current_analysis.json`, fields `prior_status`, `primary_selection` and `diagnostics`; body lines 47 and 123–127.  
**Concern** The last-half selection reproduces an existing summary but is not an established equilibration cut. The run spans only about 10–11 descriptive autocorrelation times, and independent ensembles are absent. Moreover, the actual inference prior is unconfirmed. This is consequential because the manuscript explains that rectangular and transformed galaxy supports differ. Even a converged spectral histogram cannot be interpreted against the archived reference without knowing the prior used to marginalize the galaxy coordinates. The PL/BT demonstration also retains all finite rows without chronological discard or comparable stability evidence.  
**Why it matters** Neither the low-kp depletion nor apparent lack of ms restriction can yet be attributed securely to the observations. Calling the values preliminary is appropriate, but does not close the scientific question posed.  
**Resolution test** Export the actual run configuration, including the joint prior and coordinate support. Demonstrate agreement across independently initialized ensembles and stability of the relevant marginal quantiles with uncertainty estimates. Apply equivalent checks to the fixed-spectrum comparison before interpreting its shifts as inferred galaxy responses.

### R2-M3

**Severity** Major  
**Blocking** Yes  
**Axis** mechanism-evidence  
**Claim pointer** Accurate representative histories enable the likelihood calculation used for joint spectrum–galaxy inference.  
**Evidence pointer** body lines 69–74, 82–106, Table 1 at lines 108–117, and lines 266–297; `100k_metrics.json`.  
**Concern** The current model has aggregate development statistics, with no supplied arrays to establish error signs, likelihood tails or dependence on the inference region. Its reported likelihood-error q90 is 1.17734, with an unspecified signed/absolute convention. A small trajectory RMSE therefore does not establish likelihood accuracy. Separately, predicting a representative history and evaluating its likelihood differs from marginalizing the likelihood over initial conditions. The earlier audit explicitly demonstrates this distinction and reports maximum absolute target difference 1.90797. Its signed upper quantiles cannot establish a small absolute discrepancy. These are two distinct error sources, neither resolved for the current inference.  
**Why it matters** Improving interpolation accuracy alone may leave the likelihood target changed. Consequently, successful sampling would still not establish the intended observational interpretation.  
**Resolution test** Define whether the scientific target is explicitly a representative-history likelihood or an initial-condition-marginalized likelihood. Reconstruct current-model signed and absolute observable and likelihood residuals on independent validation points, including inference-relevant regions. Quantify the effect of both emulator error and target choice on the spectral conclusions, or restrict the claim to the stated representative-history model.

## Minor Comments

### R2-m1

**Severity** Minor  
**Axis** writing-clarity  
**Affected element** Repeated qualification and archival narrative  
**Evidence pointer** main line 28; body lines 106, 139, 154, 160, 239, 243 and 309.  
**Issue** Necessary cautions recur at nearly every transition, while phrases such as “uploaded”, “remaining input” and “newly exported” make the paper read as a project-status record. In particular, “provides the quantities needed to measure” at line 158 leaves the scientific conclusion deferred.  
**Required correction** Retain the abstract qualification, consolidate the main limitations into one clear paragraph, and use stable dataset/model identifiers elsewhere. Separate reproducibility history from the argument. Preserve all substantive limitations while reducing repeated explanations.

### R2-m2

**Severity** Minor  
**Axis** writing-clarity  
**Affected element** Physical meaning of the spectral parameterization  
**Evidence pointer** body lines 15–27 and 123.  
**Issue** The mathematical prescription is clear, but nonspecialists are not shown how the selected PL/BT spectra differ over the scales relevant to galaxy formation. Fixed sigma8 normalization also changes the amplitude, complicating an intuitive reading of “blue-tilted”.  
**Required correction** Add a compact spectrum-ratio illustration or equivalent quantitative explanation, including the separate PL branch, and connect those differences to the galaxy response under study.

## Technical failings that need to be addressed before the case is established

R2-M2 and R2-M3 prevent the present sample distributions from establishing the intended observational inference.

## Assessment against Nature-style criteria

Originality is plausible at the application level but insufficiently distinguished scientifically. Scientific importance remains prospective. Interdisciplinary readership could arise from understanding cosmology–galaxy degeneracies, which is not yet demonstrated decisively. Technical soundness benefits from transparent reporting but remains limited by sampling, prior provenance and likelihood validation. Readability for nonspecialists is reasonable at the question-setting stage and weaker in the spectrum interpretation and archival appendices.

## Recommendation posture

Promising methods development, with the central inference and broad-interest scientific case currently unestablished from the supplied evidence.


# Reviewer 3

## Overall assessment

The scientific line is recognizable. Galaxy formation and small-scale matter power affect the same reionization observables, so their parameters should be explored jointly. BTemu supplies histories for that exploration while retaining the exact luminosity-function calculation. The manuscript is unusually careful about distinguishing stored sample distributions from established posterior constraints. Its actual achievement is presently a computational demonstration with preliminary distributions. It has not yet answered its motivating question about the surviving observational information on the spectrum.

This assessment covers the supplied v0.9 manuscript and packet records, particularly `main_numbered.txt`, `body_numbered.txt`, `100k_metrics.json`, `current_analysis.json`, and `prior_table.csv`. Current-model validation arrays and complete production configurations are unavailable within this packet. Their absence limits verification without establishing that the reported calculations are erroneous.

## Who would be interested in the results, and why

Reionization and early-galaxy researchers would be interested in testing how astrophysical flexibility changes small-scale-spectrum inference. Researchers using simulation emulators would also value a demonstrated connection between history error and inference accuracy. Interest beyond these communities depends on explaining the physical consequence of the joint calculation, which is still less developed than its numerical provenance.

## Major strengths

The introduction states the degeneracy clearly, and the separation of exact luminosity functions from emulated history terms is explicit. The manuscript defines absolute trajectory RMSE rather than leaving its units ambiguous. It reports prior equal-tail intervals alongside sample intervals, avoids treating interacting walkers as independent ensembles, and does not pool samples from different emulator versions. The distinction between a mean-history likelihood and a likelihood averaged over initial conditions is scientifically important. These qualifications should survive revision.

## Major Concerns

### R3-M1

**Severity** Major  
**Blocking** Yes  
**Axis** technical soundness, claim moderation  
**Claim pointer** BTemu enables spectral information to be assessed after marginalizing over galaxy parameters.  
**Evidence pointer** Body lines 69–76, 106–116, 139–160, 205–207 and 284–297; `100k_metrics.json`; `current_analysis.json`.

**Concern** The inference chain remains unvalidated at several decisive links. The current history evaluation is an aggregate development report. Its reported log-likelihood-error quantile is 1.17734, but its signed or absolute convention is unspecified. Thus the small trajectory RMSE alone does not establish accuracy where the likelihood is informative. The representative-history target also differs mathematically from averaging likelihoods over realizations. Finally, the short current chain has no independent-ensemble convergence evidence, and its actual prior configuration remains unconfirmed. The manuscript acknowledges these points accurately, but acknowledging them does not establish the observational inference.

**Why it matters** The reported interval widths are valid descriptions of selected stored rows. They cannot yet distinguish weak observational information from sampling, prior-support, or surrogate effects. This blocks the observational interpretation of the central question, rather than invalidating the descriptive statistics themselves.

**Resolution test** Reconstruct current-model observable and absolute likelihood errors, including the relevant likelihood region; establish or bound the effect of the representative-history approximation; document the executed prior support; and demonstrate stable spectral summaries across independently initialized ensembles. Otherwise explicitly frame the completed scientific result as a limited computational demonstration and leave the information-content question unanswered.

### R3-M2

**Severity** Major  
**Blocking** No  
**Axis** readability for nonspecialists, scientific importance  
**Claim pointer** The PL/BT comparison motivates joint galaxy-spectrum treatment and the spectral marginals measure the information surviving it.  
**Evidence pointer** Body lines 3–9, 25–27, 123–127 and 154–160.

**Concern** The argument moves from a clear physical motivation to parameter-distribution changes without explaining their physical meaning. The shifts in eta-star and alpha-star are given numerically, but the reader is not told what galaxy population or ionizing-source change they represent. Nor is it explained which observation should distinguish the break from a galaxy adjustment. The fixed-sigma-eight normalization and the separately implemented PL reference further make a simple “more small-scale power” interpretation nontrivial. The conclusions mostly restate that joint exploration is possible.

**Why it matters** A nonspecialist can follow the computation without understanding what has been learned about reionization. This weakens the significance case even if the numerical validation succeeds.

**Resolution test** Add a compact physical account linking a specified spectrum change to galaxy abundance, compensating galaxy parameters and the observables. Use representative histories or luminosity functions if available, and distinguish demonstrated behavior from a proposed explanation. State the scientific takeaway at the level supported by those comparisons.

## Minor Comments

### R3-m1

**Severity** Minor  
**Axis** writing clarity  
**Affected element** Main-text hierarchy and repeated caveats  
**Evidence pointer** Main line 28; body lines 106, 139, 154 and 160; appendix lines 205–207 and 239–243.

**Issue** Necessary uncertainty is repeated across the abstract, accuracy section, spectral-results paragraph and conclusion. In particular, missing current validation arrays recur at body lines 106 and 160, while sampling limitations recur at 139, 154 and 160. The appendix then adds extensive earlier-version bookkeeping. None of these statements is individually improper, but the repeated status reporting occupies space that could explain the scientific result.

**Required correction** Keep the abstract's preliminary designation, one explicit current-model limitations paragraph and the conclusion's consequent boundary. Consolidate diagnostic details in the appendix. Retain distinctions between current and earlier models, while shortening historical corrections such as line 239 unless needed to interpret a displayed result. Preserve the warning that the lower endpoint is not an exclusion limit.

### R3-m2

**Severity** Minor  
**Axis** writing clarity  
**Affected element** Terminology and numerical presentation  
**Evidence pointer** Main line 28; body lines 5–9, 25–31 and 106–116.

**Issue** LF and PL/BT arrive before plain-language definitions, and the abstract leads with eight galaxy/heating coordinates before distinguishing the six actually varied. Seven significant digits for development RMSE distract from both its scale and its verification boundary.

**Required correction** Expand luminosity function at first use, introduce the spectrum labels in physical language, and distinguish emulator inputs from inference variables in one sentence. Round headline accuracy values appropriately while retaining full precision in source records.

## Technical failings that need to be addressed before the case is established

R3-M1 identifies the missing validation and sampling links required for observational interpretation. R3-M2 concerns the explanatory and significance case.

## Assessment against Nature-style criteria

**Originality** The application to jointly varying phenomenological spectrum and galaxy parameters is identifiable. The packet does not establish novelty beyond that application relative to the cited broader emulator work.

**Scientific importance** A useful methodological direction is evident; an observational advance is preliminary.

**Interdisciplinary readership** The degeneracy problem is broadly understandable, but the demonstrated physical consequence needs development.

**Technical soundness** Definitions and limitations are careful. Current likelihood fidelity, target approximation, prior provenance and sampling remain insufficiently established for constraints.

**Readability for nonspecialists** The opening is effective. Parameter-heavy results, unexplained abbreviations and recurring implementation-status qualifications interrupt the main argument.

## Recommendation posture

Promising computational work requiring substantive validation before observational interpretation. The restraint of the present claims is a strength, but it should be accompanied by a clearer statement of the completed scientific result.


# Cross-review synthesis (post-review; not shown to reviewers)

## Overall assessment

The scientific line is clear. The paper asks how reionization observations restrict small-scale matter-spectrum parameters after galaxy marginalization, and follows an intelligible sequence from history accuracy to galaxy comparison to spectral sample marginals. Its conclusion is mostly calibrated to the available evidence. However, the motivating observational question is not yet answered. The current completed result is a preliminary computational demonstration.

The chief problem is a gap between the question and the completed evidence, rather than widespread overstatement. Additional disclaimers cannot close that gap, and removing all qualifications would make the present intervals easier to overinterpret.

## Consensus strengths

All three reviewers recognize a useful question, explicit model and likelihood definitions, separation of older and current predictors, and restraint about the short joint chain. The numerical marginal summaries and the prior-reference comparison are useful and reproducible at the stored-sample level. The manuscript correctly distinguishes the representative-history target from averaging likelihoods over realizations.

## Consensus blocking concerns

| Synthesis key | Concern | Independent reports | Consequence |
|---|---|---|---|
| S1 | The current samples and actual prior are not established as the intended posterior | R1-M1, R2-M2, R3-M1 | Stable independent sampling and executed prior/model configuration are needed before observational bounds |
| S2 | Current-model history accuracy has not established likelihood fidelity | R1-M2, R2-M3, R3-M1 | Release current validation arrays, define signed/absolute errors and assess their effect in inference-relevant regions |

These concerns block a reliable observational-constraint claim, not reproduction of the finite sample quantiles. They do not imply that the source numbers are erroneous.

## Other consensus major concerns

The physical interpretation is thinner than the numerical provenance. The PL/BT shifts show changes in selected galaxy distributions, but do not by themselves measure which galaxy freedoms absorb which spectral effects or how much information is lost by marginalization (R2-M1, R3-M2; related discussion in R1-m1). A controlled comparison would be needed if information loss is promoted to the main physical result.

The representative-history likelihood is a defined approximation, not automatically the likelihood marginalized over initial conditions (R1-M3, R2-M3, R3-M1). The reviewers differ in blocking status. R1 marks this nonblocking for an explicitly conditional representative-history claim; R2 treats it as part of the obstacle to the intended physical inference, while R3 groups it with the central validation gap. The synthesis therefore does not label this a unanimously separate blocking concern. The required evidence depends on the claimed inferential target.

## Where emphasis differs across reviewers

R1 concentrates on the statistical and likelihood links and gives a distinct nonblocking concern about initial conditions. R2 places greater weight on a demonstrated advance beyond applying an established emulator approach to a new parameter domain. R3 emphasizes that nonspecialists need a physical account of the galaxy shifts and less numerical bookkeeping. These differences were preserved without rewriting the independent reports.

## Defensive prose and repetition

All three reviewers identify the same cluster of redundancy (R1-m1, R2-m1, R3-m1).

| Location in body_numbered.txt | Assessment | Editorial direction |
|---|---|---|
| 106 and 160 | Missing current validation arrays are repeated | Give the evidence boundary once in the accuracy section and refer to its consequence in the conclusion |
| 139, 154 and 160 | Sampling qualification repeats at successive transitions | Keep one explicit status paragraph by the spectral results and technical diagnostics in the appendix |
| 123, 139, 239, 243 and 309 | “uploaded”, “reproducing the supplied summary”, “original cross-model comparison”, “current” and “newly exported” foreground delivery history | Use stable model identities and a compact provenance table |
| 158 | “provides the quantities needed to measure” states readiness rather than a completed scientific result | State precisely what the present distribution comparison establishes |
| 243 and 309–327 | Earlier-chain construction and diagnostic explanation recur in two appendix sections | Consolidate the earlier-chain definition and diagnostic record |

The words “preliminary” and the warning that the current lower endpoint is not a final exclusion limit carry scientific meaning. Keep that boundary. The RMSE-versus-likelihood distinction, the executed-prior issue, and the representative-history-versus-IC target distinction also remain necessary. These are not removable merely because they sound cautious.

## Forensic consistency findings

The post-review audit independently recomputed the current chain counts, quantiles and prior-width ratios. All main marginal values reproduce to their displayed precision. The PL/BT source-receipt counts also reconcile. No main-result arithmetic contradiction was found in these checks.

The current-model q90 metric convention remains an aggregation ambiguity, and the actual prior remains a provenance gap (AUD-04 and AUD-05). These are not confirmed numerical errors.

A separate confirmed metadata error was found in the previous MANUSCRIPT_CHECKS.json record, which says three main-text tables although there are two (AUD-06). The manuscript numbering itself is correct. This audit finding is not reviewer consensus and has no effect on the scientific intervals.

## Minor-revision checklist

- Consolidate recurring missing-data and sampling explanations without deleting their scientific boundary (R1-m1, R2-m1, R3-m1).
- Replace upload chronology with stable model and selection definitions (same IDs).
- Explain how a specified spectral change connects to the selected galaxy parameters and observables; do not infer a mechanism from a parameter shift alone (R2-m2, R3-M2).
- Define LF and spectrum labels before shorthand use, and distinguish ten emulator inputs from the eight inference coordinates in one sentence (R3-m2).
- Use sensible rounded headline RMSE values while preserving source precision in numerical records (R3-m2).

## Broad-interest / significance readout

The packet supports field-local interest in a history emulator for joint spectrum–galaxy calculations. Outstanding scientific importance and a completed broadly interesting physical inference are not established. The reviewers do not claim an editorial decision or independently verify external priority against the cited papers.

## Most important issues to resolve

The current main line is worth keeping. To support its observational conclusion, complete stable sampling under the executed prior and demonstrate current-model likelihood fidelity. To strengthen the scientific explanation, show what the galaxy freedom changes physically. The paper should not replace either evidence task with a longer limitations section.

# Risk / unsupported claims

- The current KP lower sample endpoint must not be promoted to a robust exclusion limit.
- Broad MS samples do not yet establish an observational absence of constraints under a verified actual prior.
- A shift in fixed-spectrum galaxy samples alone does not quantify loss of spectral information.
- Small trajectory RMSE does not establish small likelihood bias.
- The earlier validation arrays and exact smoke chain do not validate the current predictor's posterior inference.
- No unconditional physical interpretation follows from a representative-history likelihood without defining or testing the IC target.
- Originality beyond the documented application and general significance remain unestablished from the supplied local packet.
