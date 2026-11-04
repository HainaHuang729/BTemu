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
