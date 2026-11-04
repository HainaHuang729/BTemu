# Nature-style reassessment of the BT reionization and BTemu working drafts

4 November 2026

# Review setup

**Input scope** Physics working draft v0.17, methods working draft v0.5, the current visible English HTML and the supplied numerical/source exports.

**Assessment boundary** Author-support simulated review using the open-source nature-reviewer skill. No journal submission target was declared. Nature-style criteria are an assessment lens, not an official review or editorial decision. No new exhaustive literature search or new scientific computation is used to establish novelty.

**Shared manuscript claim summary** The drafts present fixed-galaxy spectrum sensitivity, galaxy freedom in LF fits, exploratory joint samples and history-emulator development validation. They do not claim a detection or accepted spectrum constraints.

**Visible evidence base** A frozen 28-file packet, with its SHA256 manifest, supplied identically to three isolated reviewer contexts. It contains manuscript sources, figures, prediction arrays for the older model, new summary JSON, source definitions and the runtime ledger. Previous review reports and hidden HTML audit notes are excluded.

**Missing materials affecting confidence** The packet does not supply raw new fixed-spectrum chains, new-model prediction arrays, deployed weights or full external native receipts. Missing here does not mean nonexistent elsewhere.

**Isolation** Three fork_turns=none reviewer subagents received only the same packet, the installed skill references and their own fixed emphasis brief. R1 foregrounded technical soundness, R2 originality and importance, and R3 interdisciplinary interest and readability. Each report was frozen before any comparison. Report hashes are recorded in review_qa.json. The forensic pass and synthesis followed freezing and were not fed back.

# Reviewer 1

## Overall assessment

The two working drafts document spectrum-sensitive reionization histories, luminosity-function fitting freedom and an emulator-supported exploratory inference programme. They do not claim a detection of a spectral modification. Their strongest established contribution is a carefully qualified numerical record, particularly the distinction between development-validation accuracy, finite-chain agreement and validated inference. The principal scientific question, whether observations retain information about the spectrum after galaxy freedom is included, remains unanswered. The existing demonstrations motivate that question but cannot yet discriminate physical degeneracy from numerical limitations.

My assessment uses only the immutable packet, including the supplied numerical summaries and four inspected PNGs, `fig14_validation`, `fig15_kpms_focus`, `fig16_fixed_astro_bt_histories` and `fig17_obs_combinations`. External native implementations, weights, raw new chains and new prediction arrays are outside this assessment. Their absence here does not imply their absence elsewhere.

## Who would be interested in the results, and why

Reionization modellers, researchers connecting galaxy formation to small-scale matter power, and simulation-based inference practitioners would find the spectrum–galaxy trade-off and the likelihood-target distinction useful. Broader cosmological interest would depend on a validated conclusion about information retained by the observations, or a demonstrably transferable methodological result.

## Major strengths

The work separates changes at fixed galaxy parameters from fits that permit galaxy adjustment. It also preserves the different meanings of atlas plane averages and coeval volume means. The inspected fixed-astrophysics figure visibly supports sensitivity within the displayed BT realizations.

The methods draft treats absolute neutral-fraction error correctly and distinguishes the five-model average from individual networks. The validation figure exposes signed residuals and the full empirical error distribution. Importantly, the text recognizes that small history errors need not control likelihood tails. The explicit separation of a likelihood evaluated at a representative history from an IC-marginalized likelihood is scientifically sound. The draft also avoids interpreting unconverged count histograms as credible regions.

## Major Concerns

### R1-M1

**Severity** Major  
**Blocking** No  
**Axis** technical soundness, statistical-rigor

**Claim pointer** The physics draft uses fixed/free-spectrum samples and observation-combination summaries to explore what reionization observations add after galaxy freedom is included.

**Evidence pointer** Physics sections `observation-combinations`, `fixed-spectrum-100k`, `joint-samples-fixed-free` and `app:current-chains`; Figures `fig:t3-obs-combinations` and `fig:kpms-focus`; Table `tab:fixed-100k`.

**Concern** The sample comparisons have no common demonstrated inferential qualification. The 8D ordinary split statistic reaches 1.5125, and splitting interacting walkers does not supply independent runs. The 100k summaries lack defined retention and centre/spread estimators. Two T3 raw chains and their verified parameter orders are unavailable in this export. Consequently, the reduction in escape-fraction spread and the movement of galaxy centres cannot yet be assigned quantitatively to observations or spectral settings. The manuscript recognizes this, so this concern does not invalidate its literal descriptive claims.

**Why it matters** These comparisons provide the intended bridge from illustrative histories to physical inference. Without qualification, apparent insensitivity to the spectrum could also reflect prior support or incomplete exploration.

**Resolution test** Use matched, fully recorded targets and independent ensembles with rank/folded diagnostics and autocorrelation-aware ESS. Show retained-sample stability and prior-to-posterior changes. Evaluate luminosity functions, neutral fractions and optical depths for those same samples. Alternatively, retain these products strictly as an exploratory archive and remove any suggestion that their spread changes measure observational information.

### R1-M2

**Severity** Major  
**Blocking** No  
**Axis** technical soundness, statistical-rigor

**Claim pointer** BTemu provides the representative-history approximation used for exploratory joint inference with random-IC simulation labels.

**Evidence pointer** Methods sections `training-data-and-initial-conditions` and `initial-condition-scatter-and-limits-of-inference`; Table `tab:t7-ic-summary`; Equation `eq:t7-target-difference`; physics section `app:approximation`.

**Concern** The numerical accuracy of the actual inference target is not established. Validation against one realization per parameter point combines approximation error with IC variation. The eight-IC audit compares different targets and does not evaluate the deployed predictor against a resolved conditional mean. Its maximum absolute likelihood-target difference of 1.90797 is large enough to require locating the affected parameter regions, rather than relying on small signed upper quantiles. Neither this value nor the log-likelihood scatter is an emulator-error bound. The draft correctly says so, but offers no quantitative error budget for the inference it illustrates.

**Why it matters** Nonlinearity of the likelihood allows excellent mean-history prediction to coexist with biased likelihood weights. This is distinct from sampler convergence and would persist in a perfectly converged chain.

**Resolution test** Declare whether the intended scientific estimand is a representative-realization, conditional-mean-history or IC-marginalized likelihood. At independently selected relevant parameter points, estimate that target with quantified finite-IC uncertainty and compare the deployed predictions and likelihoods. Map absolute likelihood errors and demonstrate their effect on inference, or restrict conclusions to the declared deterministic approximation without interpreting it as population-level IC marginalization.

### R1-M3

**Severity** Major  
**Blocking** No  
**Axis** technical soundness, reproducibility

**Claim pointer** The 100,000-example model supplies the current development accuracy and the newer fixed-spectrum sample summaries.

**Evidence pointer** Methods section `new-model-validation`, Table `tab:100k-validation` and Data and code availability; `metrics_100k.json`; physics section `fixed-spectrum-100k`; `visible_html_content.txt`, development-validation display.

**Concern** The current model's reported metrics are insufficiently defined for independent scientific interpretation. The JSON supplies three q90 values without their signed/absolute conventions, membership or generating code. A q90 log-likelihood difference of 1.17734 has materially different meanings under signed and absolute definitions. The predictor aggregation is also unspecified. Earlier 512-history results cannot qualify this model, and an unchanged development split cannot supply independent final coverage. These limitations are disclosed but remain central to the current methods result.

**Why it matters** The new model now supports the newest physical comparisons. Its global trajectory quantiles do not establish fidelity near relevant likelihood transitions, spectrum boundaries or the sampled support.

**Resolution test** Release frozen prediction/label pairs, membership, aggregation and evaluation code for the reported statistics. Evaluate the deployed predictor on an independent final set with region-dependent history, optical-depth and absolute likelihood errors. Include relevant tails and the mapping between test coverage and inference support. Do not express improvement over the earlier model without a common evaluation.

### R1-M4

**Severity** Major  
**Blocking** No  
**Axis** technical soundness, reproducibility

**Claim pointer** Changes across spectral settings illustrate the physical response of a selected BT-modified calculation, and the exact/emulator calculations supply a finite comparison of that calculation.

**Evidence pointer** Both drafts, sections `spectrum-modification`, `luminosity-functions-and-reionization-constraints` and `parameter-domain-and-chain-definitions`; physics appendix `app:fixed-astro-update`; methods section `inference-status`.

**Concern** Several essential implementation identities remain unresolved. The native spectrum and normalization have not been checked against the exported contract; the PL limit is algebraic rather than numerically verified. Chain receipts do not establish all fixed parameters, prior support, weights or optical-depth conventions. The adapter and metadata use different optical-depth integration settings. These are not evidence that the exported differences are erroneous, but they prevent independent attribution of an exact/emulator discrepancy, or a cross-run parameter shift, to its intended cause.

**Why it matters** The scientific interpretation requires a common forward model and target. Holding sigma8 fixed also changes normalization with shape, so a slope change alone does not identify a uniquely small-scale amplitude intervention.

**Resolution test** Freeze executable native identities, parameter transformations, priors and postprocessing with each run. Demonstrate native BT/PL agreement at MS equal to ns, verify spectrum units and normalization, and test optical-depth parity on identical histories. Supply matched IC/configuration records for the fixed-astrophysics comparison. Keep primordial-index interpretations outside the claim until the primordial definition is established.

## Minor Comments

### R1-m1

**Severity** Minor  
**Axis** readability for nonspecialists  
**Affected element** Scientific framing of the spectrum and emulator target  
**Evidence pointer** Physics Introduction and `spectrum-modification`; methods `luminosity-functions-and-reionization-constraints`.

**Issue** MS, BT and the representative-history target require substantial technical reconstruction before a broad reader can state what was changed and what the observations test.

**Required correction** Add a compact explanation connecting input matter power, halo abundance, UV luminosities and ionization history. Define the representative-history approximation in ordinary language alongside its equation and explain the consequence of fixed sigma8.

## Technical failings that need to be addressed before the case is established

No concern is marked blocking for the narrow claim that these are descriptive development and exploratory products. R1-M1 through R1-M4 must be resolved before these products establish an observational identifiability result or qualified emulator-based inference. A detection claim is neither made nor assessed.

## Assessment against Nature-style criteria

Originality is plausible in the selected BT implementation, but the documented prior-emulator comparison does not establish a general technical advance. Scientific importance is prospective because the central information question remains open. Interdisciplinary readership could extend to cosmological inference if a transferable conclusion emerges. Technical soundness supports the bounded descriptive results more strongly than their intended inferential application. Readability benefits from explicit limitations but needs a shorter conceptual account for nonspecialists.

## Recommendation posture

Promising exploratory work, with responsible claim moderation. The supplied evidence does not yet establish an outstanding broad-interest result or a validated inference method. The most useful next version would resolve one scientific question with a fully qualified calculation rather than add further unqualified sample summaries.


# Reviewer 2

## Review setup

**Input scope** Physics working draft v0.17, methods working draft v0.5, visible English results content, and numerical/source exports in the immutable packet.

**Assessment boundary** This review emphasizes originality and scientific importance. It uses only the supplied packet and journal criteria, without external literature verification. Figures `fig6_21cmtb_lf_grid.png`, `fig14_validation.png`, `fig15_kpms_focus.png` and `fig17_obs_combinations.png` were inspected directly. Raw new-model predictions and fixed-spectrum chains are outside the packet, as its scope explicitly states.

**Shared manuscript claim summary** The authors illustrate spectrum sensitivity at fixed galaxy parameters, comparably fitting LF solutions over part of a spectral grid, exploratory joint samples, and development accuracy of a history emulator. They do not claim a detection, qualified spectrum bounds or established posterior fidelity.

## Overall assessment

The scientific question is worthwhile. Reionization can connect galaxy formation to small-scale matter structure, and permitting galaxy freedom is essential to interpreting that connection. The work provides useful exploratory calculations and unusually clear distinctions between numerical products. Its strongest demonstrated contribution is presently a documented investigation and validation record. The outstanding scientific result remains prospective. Neither a robust observational limitation on the spectrum nor a demonstrated non-identifiability result has been established. The careful qualifications make the claims more credible, but do not themselves supply the missing scientific conclusion.

## Who would be interested in the results, and why

Researchers studying reionization, high-redshift galaxy populations and small-scale cosmology would value a reliable account of which spectral changes can be absorbed by galaxy parameters. Simulation and inference researchers would also find the separation of history error, realization scatter and likelihood targets useful. Interest beyond these communities would depend on a completed conclusion about what observations can reveal about matter structure, or a transferable methodological advance demonstrated beyond this selected calculation.

## Major strengths

The fixed-astrophysics and independently fitted LF experiments address different questions and are presented as such. Figure `fig6` makes the sharp contrast between small-break-scale deterioration and near-PL stored maxima at larger scales readily visible. The authors avoid converting those maxima into evidence ratios or exclusion significance.

The released five-model history errors have explicit aggregation and absolute-error definitions. Figure `fig14` shows both a distribution and signed residuals, supporting the stated development-validation interpretation. The manuscript also recognizes that a likelihood evaluated on a mean history differs from a likelihood marginalized over realizations. These are useful foundations for a rigorous final analysis.

## Major Concerns

### R2-M1

**Severity** Major  
**Blocking** No  
**Axis** Originality and scientific importance  
**Claim pointer** The physics Introduction proposes extending the Park galaxy-inference framework to variable small-scale spectra; the methods Introduction documents BTemu for the selected BT calculation.  
**Evidence pointer** Physics sections `introduction` and `conclusions`; methods sections `introduction`, `network-and-training-objective` and `conclusions`; supplied bibliography entries Park2019, Breitman2024 and Breitman2026.  
**Concern** The packet identifies an application distinction, adding spectrum coordinates to an adopted galaxy prescription, but does not establish what scientific insight this extension delivers beyond sensitivity and compensating parameter freedom. The methods draft explicitly says that emulation and inferred-distribution comparisons are established approaches. Its residual MLP and five-model average are described clearly, but no new algorithmic principle or demonstrated capability unavailable in the cited framework is established. This is not evidence that the work lacks originality. It means the originality case is currently limited to a selected physical extension and its development record.  
**Why it matters** A useful extension can support a specialist contribution without establishing outstanding scientific importance or a technical advance with significant impact across a research community. The current evidence does not yet distinguish those levels.  
**Resolution test** State the specific previously unresolved scientific question answered by the completed analysis and distinguish it from the supplied prior-work descriptions. Demonstrate the answer with a controlled result. If the intended contribution is instead a technical resource, substantiate its distinctive capability and reusable impact under matching error and observable definitions. No claim of being first should exceed the documented literature basis.

### R2-M2

**Severity** Major  
**Blocking** Yes  
**Axis** Scientific importance and technical soundness  
**Claim pointer** The physics central question is whether observations retain information about the break scale and slope after galaxy parameters vary; the observation-combination summaries suggest where history constraints add information.  
**Evidence pointer** Physics sections `introduction`, `observation-combinations`, `joint-samples-fixed-free`, `app:t3-selection` and `app:current-chains`; Figures `fig:kpms-focus` and `fig:t3-obs-combinations`; Tables `tab:chain-moments` and `tab:t3-obs-combinations`.  
**Concern** The central information question remains unanswered. The broad spectrum display is correctly labelled exploratory, and the eight-dimensional monitoring statistic reaches 1.5125. The T3 narrowing is shown at one attributed fixed spectrum, while two raw chain records and shared configurations remain unverified. It therefore cannot yet establish which observations break spectrum-galaxy degeneracies. Broad finite-chain distributions cannot distinguish weak information from incomplete sampling, and fixed-spectrum escape-fraction narrowing does not resolve that ambiguity.  
**Why it matters** This is the main route from a model exploration to a scientifically consequential conclusion. The concern does not challenge the faithful description of finite samples or demand a detection. A robust negative conclusion about identifiability could also be important, but it requires qualified inference.  
**Resolution test** Supply matching priors, parameter orders, fixed settings and likelihood identities, then obtain independent converged ensembles and effective sample sizes for the relevant observation combinations with spectrum freedom. Compare the resulting spectrum distributions with their priors and show LF, neutral-fraction and optical-depth predictions from the same retained samples. This should decide whether the observations meaningfully distinguish spectra within the adopted galaxy model.

### R2-M3

**Severity** Major  
**Blocking** Yes  
**Axis** Technical soundness and physical interpretation  
**Claim pointer** The physics title frames the subject as primordial spectra, while the model defines a modified input linear matter spectrum normalized at fixed sigma8.  
**Evidence pointer** Physics title in `physics_main.tex`; both drafts' sections `spectrum-modification` and `astrophysical-parameters`; physics section `app:fixed-astro-update`.  
**Concern** The physical meaning of the spectral extension is not fully anchored to an executable model. The text explicitly leaves the primordial-spectrum definition, native normalization test, PL-limit equivalence and external BT implementation unverified. Fixing sigma8 changes the normalization as shape changes, so the observed response cannot simply be interpreted as a change confined to high wavenumber at fixed primordial amplitude. The later coeval export also lacks the realized configuration needed to verify its spectrum settings.  
**Why it matters** The originality and cosmological importance depend on what physical family is actually being explored. Descriptive curve separation is credible as an exported result, but its interpretation as primordial-spectrum physics requires this link.  
**Resolution test** Provide the frozen native spectrum and halo-source implementation, verify units and normalization, test the no-break limit against the PL branch, and display actual input-spectrum ratios under the adopted convention. Either derive the corresponding primordial definition or consistently restrict the scientific framing to the verified matter-spectrum prescription.

### R2-M4

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness and methodological significance  
**Claim pointer** The history approximation supplies the numerical interface for joint exploration, with development accuracy documented separately.  
**Evidence pointer** Methods sections `reported-history-accuracy`, `new-model-validation`, `inference-status`, `initial-condition-scatter-and-limits-of-inference` and `validation-plan`; Tables `tab:100k-validation`, `tab:t6` and `tab:t7-ic-summary`.  
**Concern** Small development trajectory errors have not been connected to reliable scientific inference for the deployed predictor. The 100k statistics lack exported prediction membership and aggregation, the exact reference is a 200-step smoke chain, and the IC audit finds a maximum mean-history versus finite-marginalized log-likelihood difference of 1.90797. These facts do not establish that IC effects invalidate the representative target. They leave its accuracy and scientific adequacy unqualified.  
**Why it matters** Without this connection, the methods work establishes development performance rather than a validated inference capability, limiting both deployment and its significance claim.  
**Resolution test** Freeze the deployed weights and target, evaluate independent histories with likelihood-sensitive tail diagnostics, quantify conditional-mean reference uncertainty, and demonstrate matching converged exact versus emulator inference. An IC-marginalized target should be tested explicitly if intended. The criteria should refer to changes in the scientific conclusions rather than trajectory RMSE alone.

## Minor Comments

### R2-m1

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Spectrum terminology and coordinate labels  
**Evidence pointer** Physics Abstract, section `spectrum-modification`, and Figure `fig:kpms-focus`.  
**Issue** The narrative uses MS, while the figure uses an index-style label. A nonspecialist can easily read this as the primordial spectral index despite the later distinction.  
**Required correction** Use one visible name for the modified-spectrum slope and briefly explain the break scale and fixed-normalization convention when first introduced.

## Technical failings that need to be addressed before the case is established

R2-M2 and R2-M3 block the central physical interpretation. R2-M4 additionally limits qualification of inference performed through the emulator. The currently supported descriptive results remain useful.

## Assessment against Nature-style criteria

**Originality** A plausible application extension is visible, but a distinct scientific conclusion and independent methodological advance are not yet demonstrated.

**Scientific importance** The underlying question matters. The present exploratory answer does not establish outstanding importance.

**Interdisciplinary readership** The potential connection between early galaxies and matter structure is broad; the current results chiefly serve the immediate modelling community.

**Technical soundness** Development statistics and finite samples are carefully scoped. The physical implementation and qualified information comparison remain incomplete.

**Readability for nonspecialists** The logical progression is good, but repeated archive distinctions and coordinate names obscure the central result. A short physical overview would help once that result is settled.

## Recommendation posture

Promising exploratory work requiring substantial scientific completion. The packet supports a useful specialist investigation and development report; a strong Nature-style case remains unestablished. This is an assessment of the supplied evidence, not an editorial decision.


# Reviewer 3

## Overall assessment

The physics draft asks an important question. Can observations of the ionized early Universe distinguish changes in the small-scale matter spectrum once uncertain galaxy properties can adjust? The supplied material establishes illustrative spectrum sensitivity at fixed astrophysics, similar stored luminosity-function maxima over part of a spectral grid, and exploratory sample distributions. The methods draft documents useful development-validation results. Neither manuscript claims a detection, and the explicit separation of descriptive samples from accepted constraints is a substantial strength.

The present package nevertheless reads principally as a carefully documented development state. Its central observational question remains unresolved, and the connection from the displayed parameter shifts to a general physical conclusion is incomplete. I would support further development, but a strong interdisciplinary scientific case is not established by the available results.

## Assessment boundary

This assessment uses only the immutable packet, including the two manuscript sources, visible HTML text, numerical summaries and supplied source exports. I inspected the supplied PNGs for the fixed-astrophysics coeval histories, LF grid, focused spectrum distribution and observation-combination comparison. No external literature verification was performed. Several other manuscript figures, full new chains, new-model prediction arrays and external native implementation records are outside the supplied evidence. Their absence does not establish that they do not exist.

## Who would be interested in the results, and why

Reionization researchers and galaxy-formation modellers would be interested in how source efficiencies compensate for altered halo populations. Cosmologists concerned with the small-scale matter spectrum would care if the analysis could show which observations retain information independent of those source assumptions. Researchers using simulation surrogates would find the distinction between a representative prediction and an initial-condition-marginalized likelihood useful. At present, this last point is a diagnostic lesson rather than a demonstrated general correction or transferable inference method.

## Major strengths

The physics introduction gives a direct motivation for joint inference rather than comparing spectra at one galaxy prescription. The spectrum equation, stored-coordinate definitions and prior-transformation discussion expose assumptions that materially affect interpretation. The T3 comparison usefully distinguishes the role of non-ionizing galaxy light from that of ionizing escape.

The figure captions are unusually explicit about failed diagnostics, retained rows and the meaning of error bars. The inspected LF grid makes both large discrepancies and near-reference differences visible. The focused spectrum plot prominently labels its exploratory status. The methods draft also correctly separates individual-network errors, the five-model average and the later model's separate evaluation. These choices make the limitations inspectable rather than hiding them behind apparently precise summaries.

## Major Concerns

### R3-M1

**Severity** Major  
**Blocking** Yes  
**Axis** Scientific importance and technical soundness  
**Claim pointer** The physics manuscript's central question is whether observations retain information about the spectral break and slope after galaxy parameters vary.  
**Evidence pointer** Physics sections `introduction`, `observation-combinations`, `joint-samples-fixed-free` and `initial-condition-scatter-and-limits-of-inference`; figures `fig:t3-obs-combinations` and `fig:kpms-focus`.

**Concern** The evidence does not yet answer that question even in a qualified quantitative form. T3 varies observations at an attributed fixed spectrum. The free-spectrum sample adds spectral freedom but has ordinary split monitoring values up to 1.5125 and no independent convergence. The manuscript explicitly allows both weak information and incomplete sampling as explanations for its broad distribution. In addition, luminosity functions and histories predicted from the current joint samples are proposed rather than shown. The available comparisons therefore cannot establish where observational degeneracy survives or where a particular observation breaks it.

**Why it matters** This is the missing result that separates a broadly interesting physical conclusion from motivation for a future calculation. The honest exploratory language prevents overclaiming, but does not supply the result needed to establish the central scientific case.

**Resolution test** Provide a matched, independently converged comparison with fixed and free spectrum, documented priors and effective sample sizes, together with predicted LF, neutral-fraction and optical-depth distributions from those same retained samples. Show the change from prior to data-informed distributions. A demonstrated lack of useful information would also answer the question if numerical uncertainty is controlled. Otherwise retain the work's narrower development scope and explicitly leave the central question unanswered.

### R3-M2

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness  
**Claim pointer** A deterministic emulator history supplies the history-dependent likelihood for the exploratory joint calculations.  
**Evidence pointer** Both drafts, section `luminosity-functions-and-reionization-constraints`; methods sections `network-and-training-objective`, `initial-condition-scatter-and-limits-of-inference` and `validation-plan`, especially equation `eq:t7-target-difference` and table `tab:t7-ic-summary`.

**Concern** The scientific meaning of the deterministic target remains insufficiently qualified for physical interpretation. Labels are individual random realizations, while a squared-error predictor may approximate a conditional mean. The supplied audit measures a maximum absolute difference of 1.90797 between the likelihood of an eight-realization mean and the finite-IC averaged likelihood, but does not evaluate the deployed predictor at those families with reference uncertainty. Its location relative to the parameter region actually used by inference is also not established. Development RMSE alone cannot determine the corresponding distortion of observational information.

**Why it matters** A nonspecialist could reasonably read the improved trajectory error as evidence that the physical inference is becoming accurate. The manuscript itself explains why those are different questions. That distinction needs a result tied to the intended likelihood, not only a general warning.

**Resolution test** Freeze the intended target and deployed predictor identity, evaluate its likelihood errors against a sufficiently resolved repeated-IC reference, and report their parameter dependence in regions relevant to inference. Demonstrate whether the approximation changes the observable distributions or inferred information. A representative-history target can remain legitimate if its conditional scope and sensitivity are established.

### R3-M3

**Severity** Major  
**Blocking** No  
**Axis** Interdisciplinary readership and readability for nonspecialists  
**Claim pointer** The physics paper presents an exploratory connection between blue-tilted primordial power spectra and reionization inference.  
**Evidence pointer** Physics title and abstract in `physics_main.tex`; physics sections `spectrum-modification`, `physical-model-and-simulations` and `initial-condition-scatter-and-limits-of-inference`.

**Concern** The title names primordial power spectra, whereas the body explicitly defines a modified linear matter spectrum with a transfer function and fixed sigma-eight normalization, and retains an author note requiring the exact primordial definition and native normalization test. This is more than terminology for the intended broad readership. Readers cannot yet identify which underlying primordial change the explored coordinates represent, and the text warns that even relative amplitude cannot be inferred from slope alone.

**Why it matters** The cosmological significance depends on what physical hypothesis is varied. A title invoking primordial physics makes a connection that the current model contract deliberately leaves unverified.

**Resolution test** Verify and document the mapping to the primordial spectrum, normalization and numerical PL limit before retaining that framing. Alternatively frame the title and summary around phenomenological small-scale matter-spectrum modifications, with a concise explanation of the fixed-normalization choice and the physical scope it permits.

## Minor Comments

### R3-m1

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Physics abstract and opening narrative  
**Evidence pointer** `physics_main.tex` abstract and physics `introduction`.

**Issue** LF, PL and BT enter the summary without consistently providing an accessible first-use description. The reader is also given several inference coordinates before a simple account of what each observation measures.

**Required correction** Define the abbreviations and add a short plain-language account of galaxy counts, integrated scattering optical depth and late neutral fraction. State what would constitute an answer to the central question.

### R3-m2

**Severity** Minor  
**Axis** Figures and tables  
**Affected element** Spectrum and observation-combination displays  
**Evidence pointer** Inspected `fig15_kpms_focus.png`, `fig17_obs_combinations.png` and their physics captions.

**Issue** The plots use the symbol `m_s` while the text calls the coordinate MS. The otherwise clear T3 display relies on Greek coordinate symbols whose physical meanings require consulting the model section.

**Required correction** Explicitly identify `m_s` with MS and add brief physical labels to the T3 panels or caption. Preserve the clear distinction between sample spreads and uncertainty intervals.

## Technical failings that need to be addressed before the case is established

R3-M1 blocks an observational answer to the manuscript's central question. R3-M2 requires qualification before that answer can be interpreted through the history approximation. R3-M3 governs the physical scope of the cosmological framing.

## Assessment against Nature-style criteria

**Originality** The supplied comparison with Park et al. identifies the added spectrum freedom. A distinct general methodological advance over established emulation is not demonstrated.

**Scientific importance** The question is consequential, but outstanding importance cannot be assigned to an unresolved inference outcome.

**Interdisciplinary readership** The connection among structure formation, galaxy sources and reionization has broad potential. A stable observable consequence or robust information limit would make that connection concrete.

**Technical soundness** The descriptive presentation is appropriately cautious. Convergence, target qualification and implementation provenance prevent stronger interpretation.

**Readability for nonspecialists** The initial motivation is clear and the inspected displays are legible. Primordial-versus-matter framing, abbreviations and the accumulation of run-specific detail obscure the scientific result.

## Recommendation posture

Promising exploratory research with a useful transparent methods record. The broad-interest case remains underdeveloped until the observational question is answered with a qualified numerical target. This assessment does not imply that the authors have claimed a detection or decide journal suitability.


# Cross-review synthesis (post-review; not shown to reviewers)

## Consensus strengths

All three independently generated reports find a coherent physical motivation and useful descriptive evidence. Holding galaxy parameters fixed shows spectrum sensitivity, while allowing galaxy parameters to adjust reveals fitting freedom. The older 512-history validation separates individual networks from their arithmetic average, and the manuscripts distinguish finite-chain displays from qualified inference. The distinction between a representative-history likelihood and IC marginalization is useful and correctly recognized.

## Consensus blocking concerns

### SYN-01

The central observational information question remains unanswered. R2-M2 and R3-M1 independently mark this as blocking the central physical case. R1-M1 raises the same underlying inference issue but explicitly does not call it blocking for the narrower descriptive scope. This difference is retained.

The data establish illustrative sensitivity and changes in reported sample summaries. They do not yet separate weak observational information from incomplete sampling or prior support when the spectrum is free. Matching target definitions, independent sampling and observable predictions from the same retained samples are needed to establish that scientific answer. A reliable negative result about identifiability could be a valid outcome. A detection is not required or claimed.

## Other consensus major concerns

### SYN-02

Physical spectrum identity and the primordial framing need alignment. R1-M4, R2-M3 and R3-M3 independently raise native implementation, normalization or physical-family concerns. R2 calls its framing concern blocking; R1 and R3 do not. It is therefore a consensus major concern with mixed blocking judgments, not a consensus blocking finding.

The title invokes primordial power spectra while the supplied formula defines a modified input linear matter spectrum under fixed sigma8. The manuscript itself leaves the primordial mapping and native no-break equivalence unresolved. A verified primordial definition or a narrower matter-spectrum framing would make the physical hypothesis explicit.

### SYN-03

Likelihood-target accuracy is separate from trajectory prediction accuracy. R1-M2, R2-M4 and R3-M2 independently identify this issue. None treats the stated finite-IC likelihood difference as an emulator-error lower bound. The needed comparison concerns the deployed predictor and declared inference target in relevant parameter regions, with finite-reference uncertainty. Better global development RMSE alone cannot qualify observational inference.

### SYN-04

The new model lacks independently reconstructible evaluation definitions. R1-M3 and R2-M4 independently raise the issue. The new JSON contains useful reported development statistics, but evaluated membership, prediction aggregation and signed versus absolute q90 definitions are absent from this packet. The older arrays verify an earlier predictor. This does not demonstrate a numerical error in the new values, and does not support a matched improvement percentage.

## Where emphasis differs across reviewers

R1 deliberately evaluates the literal descriptive claims and marks no concern blocking within that narrow scope. R2 and R3 evaluate completion of the central physical question and mark the missing identifiability answer blocking for that case. These are different assessment scopes, not disagreement about the presence of a detection claim.

R2-M1 foregrounds originality. The supplied material supports an application extension to a selected BT calculation, but does not establish a new algorithmic principle or completed broad scientific conclusion. This does not prove the work is merely a copy of a cited emulator. That stronger statement would require a separate literature comparison under matching physical models, observables and tasks.

R3 emphasizes the accessibility cost of primordial-versus-matter terminology, abbreviations and run-specific detail. These concerns do not justify adding repeated caveats to the main results page. Brief physical labels and a coherent evidence-to-conclusion sequence are more useful, with provenance retained separately.

## Forensic consistency findings

The independent editorial pass ran only after all three reports were frozen. It did not supply material to reviewers or alter their reports.

| Audit ID | Classification | Result |
| --- | --- | --- |
| AUD-01 | passed | Recomputed older five-model-average RMSE median 0.001007616453 and q95 0.006814576402. Seed 11 q95 is 0.010080229640. The manuscript already distinguishes these. |
| AUD-02 | aggregation_ambiguity | New-model evaluated membership, aggregation and q90 conventions are not specified by its summary JSON. |
| AUD-03 | passed | Fixed-MS kp1 minus kp5 centre differences are -0.629 in ETA_STAR and +0.088 in ALPHA_STAR. Changing kp1/MS1.5 to kp10/MS2.5 gives -0.702 and +0.180 under the stated subtraction. |
| AUD-04 | confirmed_internal_error | Source phase60 ledger equates 26 core-hours to 943695 core-seconds. Division by 3600 gives 262.1375 core-hours. The visible HTML already uses the correct 262.14 value. This is a source-ledger error, not a newly found manuscript error. |
| AUD-05 | unresolved_input_needed | Training JSON gives 47661.272695 seconds or 13.2392 hours, while the ledger gives 13.5 hours. The difference is 938.727305 seconds; timing scope or job receipts are needed to reconcile it. |
| AUD-06 | passed | The stated selections give 80000 archived 6D rows, 89088 archived 8D rows, 6400 full exact200 rows, 3200 exact T6 rows and 32000 T3 ext2 rows. Distinct selections are not a count contradiction. |
| AUD-07 | provenance_gap | Native spectrum identity, normalization, postprocessing parity and complete run identities remain outside the supplied verification. |
| AUD-08 | not_assessable | Aggregate T7 summaries cannot reconstruct family-level absolute likelihood errors or validate the new deployed predictor. |

AUD-04 and AUD-05 are editorial audit findings, not reviewer consensus. The signed/absolute issue is a definition gap, not proof that a reported q90 is wrong. No new training, simulation or sampling was performed for this assessment.

## Minor revision checklist

- Explain the physical chain from input matter power to halo abundance, UV galaxy counts and ionization history in a compact introduction. Preserve the distinction between galaxy counts, integrated optical depth and the late neutral fraction. R1-m1 and R3-m1.
- Identify the plotted m_s with the stored MS coordinate at first use. R2-m1 and R3-m2.
- Define LF, PL and BT at first relevant use and give short physical labels for the T3 coordinates. R3-m1 and R3-m2.

## Broad-interest / significance readout

The connection between early galaxies and small-scale matter structure has a plausible audience beyond emulator developers. The present packet shows why the question matters more clearly than it establishes its answer. The Nature-style scientific-importance and interdisciplinary-interest criteria are therefore not established by these working drafts. This is a bounded simulated assessment, not a journal decision.

The strongest potential physical contribution is a controlled result about which spectral changes remain distinguishable after galaxy freedom, or a quantitatively established loss of that information. The strongest potential methods contribution would connect the selected BT prediction capability to verified likelihood accuracy and reproducible inference. Increasing training data or using an established architecture is not by itself that result.

## Most important issues to resolve before a strong Nature-style case is established

The decisive gap is a completed physical answer under a declared, verified numerical target. Native spectrum meaning, matched inference configurations and likelihood-target validation determine how such an answer can be interpreted. The validation and sample summaries already available are useful evidence toward that goal; repeating their limitations in more paragraphs does not complete it.

# Risk / unsupported claims

The packet does not establish a BT detection or exclusion, reliable kp/MS bounds, a validated lack of observational information, posterior fidelity from exact200, a universal IC error floor, a matched new-model improvement percentage, or complete-likelihood speedup. The working manuscripts generally avoid making these claims. Their absence should not be misrepresented as an error in a claim that was never made.

No exhaustive independent literature review was performed. Originality is assessed against the distinctions documented in the supplied manuscripts and bibliography. Private native source, deployed weights and raw new chains were not supplied in the frozen packet; no conclusion is made about whether they exist elsewhere.
