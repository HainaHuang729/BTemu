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
