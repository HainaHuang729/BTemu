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
