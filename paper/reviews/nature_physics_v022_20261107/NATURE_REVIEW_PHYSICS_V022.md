# Review setup

Input is the complete physics v0.22 manuscript and the same frozen source packet for three independent reviewers. The author requests assessment of the main line after relocation of the spectrum figure, physical interpretation, evidence and prose. The evidence includes the five fixed-spectrum arrays, the short joint array and the atlas and LF records. Full executed configurations and current validation arrays are outside the packet.

Emphases fixed before launch

1. R1 assesses evidence, statistical scope and physical attribution.
2. R2 assesses the scientific line after figure relocation, originality and significance.
3. R3 assesses readability, physical explanation, repetition and caveat placement.

# Reviewer 1

## Overall assessment

The main text stands on its own with the exploratory spectrum projection in the appendix. Its three main results can be read without assuming a constraint on the spectrum. At one fixed galaxy prescription, the atlas shows that the exported ionization histories separate. Independent LF fits at several spectra attain similar stored likelihoods. A transformation of the released galaxy chains shows a substantially smaller star-formation factor per active halo in one BT sample than in the PL sample. The third result is reproducible from the arrays and has a clear meaning at fixed halo mass. The first two are distinct comparisons and their juxtaposition does not measure the extent to which galaxy properties hide a spectrum change.

The main text accurately recognizes this distinction in its closing section. As a result, the remaining question is scientific as much as editorial. The physics article has yet to demonstrate which changes in the halo population matter for the measured luminosities and reionization history, or how much adjustment of the galaxy prescription is needed to recover those observables. The most compelling version would quantify those effects in a common forward calculation. The paper as supplied is an informative model comparison with a well-defined descriptive source statistic.

This assessment is limited to the numbered v0.22 manuscript, supplied figures, packet source records and six HDF5 arrays, using the supplied Nature criteria. I independently checked the array hashes, dimensions and finite-row counts against the packet records and recomputed the headline star-formation statistic. Executed configurations, native and predictor identities, and validation arrays for the headline inference are unavailable within the packet.

## Who would be interested in the results, and why

Reionization and high-redshift galaxy researchers would use a controlled comparison to identify which galaxy parameters can absorb changes in the dark-matter halo population. Cosmologists interested in power on poorly measured scales would want to know when early galaxies and reionization provide complementary information. Readers working on inverse problems could follow the distinction between a forward-model response and what can be learned when a flexible source model is fitted. That broader interest depends on showing the distinction for the same observable and spectral comparison.

## Major strengths

- The paper distinguishes the fixed-galaxy atlas, LF-only fits, fixed-spectrum galaxy chains, and free-spectrum exploration in the experiment table. The separate axes for absolute histories and PL-relative differences in `fig:atlas-history` make the direct numerical comparison legible.
- The capped transformation in `eq:physics-sfr-factor` is applied to the stored rows. It separates star formation per active halo from halo abundance, the duty cycle and photon escape. Recomputing it on the PL and BT1 arrays yields the stated ratios of marginal medians, 0.123, 0.195 and 0.308. The ratios from the final quarter of stored steps are approximately 0.123, 0.194 and 0.305. That is a useful within-run sensitivity check for this particular summary.
- The manuscript flags the saturation of the extreme atlas history at the upper redshift boundary and keeps the nonstationary free-spectrum projection outside the main argument. These choices make the paper easier to assess.

## Major Concerns

### R1-M1 — The experiments do not isolate the physical source of LF compatibility

**Severity** Major  
**Blocking** Yes  
**Axis** Mechanism and experimental design

**Claim pointer** The abstract and conclusion report conditional history sensitivity and fit compatibility, and frame the unresolved issue as weak direct sensitivity versus galaxy compensation.

**Evidence pointer** Main 0029. Body 0076–0085, 0089–0100, 0104–0123 and 0142–0161. Figures `fig:atlas-history`, `fig:lf-grid` and `fig:lf-fits`. The first comparison holds the galaxy prescription fixed for a history, the second refits four galaxy parameters for LFs, and the star-formation contrast derives from six-coordinate samples with attributed history terms.

**Concern** None of these comparisons supplies the fixed-galaxy LF response at the same spectral contrast for which an LF is refitted. The strongest numerical LF agreement is reported at $k_p=20$–$30\,h\,\mathrm{Mpc}^{-1}$, while the headline active-halo ratio is for $k_p=1\,h\,\mathrm{Mpc}^{-1}$ and $m_s=1.5$. The latter is a different physical regime and adds no estimate of the adjustment needed at the larger break scales. Nor does the packet show the realized change in halo abundance across the masses that contribute to the fitted galaxies. Fixed $\sigma_8$ changes the normalization as well as the shape, so the direction and mass dependence of the population change need to be demonstrated for the actual normalized spectra.

**Why it matters** The archival compatibility claim survives. The main physical question, whether a spectrum change affects observables appreciably before fitting and can be absorbed afterward, remains open. An observable-level answer would supply the scientific advance that connects the three results.

**Resolution test** For a representative small and large break scale, use a verified PL reference and a common solver, realization strategy and galaxy prescription. Evaluate the same LF bins and history summaries under both spectra with the galaxy parameters fixed, then after adjustment under a shared fit definition. Report the changes in observable residuals and the LF and history likelihood contributions separately. Show the change in mass variance or halo abundance over the masses that actually supply the fitted UV galaxies and ionizing emission. If the analysis remains an archive comparison, frame the central result around descriptive sensitivities and explain the more limited advance.

### R1-M2 — Stable row summaries do not verify a common inference target

**Severity** Major  
**Blocking** Yes  
**Axis** Statistical scope and reproducibility

**Claim pointer** The abstract and main text compare the PL and BT1 active-halo factors under the adopted prescription and use the difference as the main quantitative source result.

**Evidence pointer** Main 0029. Body 0023, 0045, 0129–0148, 0157, 0231 and 0235–0237. Packet `chains/pl_100k.h5`, `chains/kp1_ms1p5_100k.h5`, `data/prior_table.csv` and `data/SOURCES.json`. The files contain named samples, log probabilities and the fixed-spectrum `kp` and `ms` attributes. The PL array stores zeros for those attributes, which identify neither the executed branch nor the way its history predictor was selected.

**Concern** The transformation and finite-row statistic are supported. The arrays cannot show that the PL and BT1 targets shared the implemented galaxy prior, likelihood terms, fixed coordinates and history calculation. A rectangular prior in $\eta_\star$ would differ from the mapped native prior. The optical-depth adapter and metadata also give different interpolation and redshift settings (body 0237). The all-finite selection includes early excursions. My final-quarter calculation indicates that these excursions have little effect on the reported $S$ contrast, but the last quarter and full chain are from the same interacting ensemble. A stable median in one run does not resolve target parity or independent exploration.

**Why it matters** The reported ratios are reproducible descriptions of these files. Their physical interpretation as a response of the fitted galaxy prescription to a change in the spectrum requires a comparison whose target changes only in the intended way.

**Resolution test** Supply the executed manifests for the exact PL and BT1 files, including prior support in sampled coordinates, the PL branch and predictor routing, fixed X-ray settings, and the effective optical-depth adapter. Demonstrate that common inputs receive the same priors and that the stored likelihood terms can be reproduced. Check stability and Monte Carlo precision for $S$ directly using multiple independent initializations. If executed provenance or independent sampling remains unavailable, retain the calculation as a named array statistic and keep attribution to the spectrum explicitly unresolved.

### R1-M3 — The approximation checks do not cover the headline comparison

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness

**Claim pointer** Body 0065–0072 describes the representative-history calculation and body 0157 identifies its validation as necessary for attribution.

**Evidence pointer** Body 0203–0227 and 0493–0494. Packet `data/t6_recomputed_20261029.json` and `data/t7_update_20261031/t7_ic_sensitivity_report.json`. T6 compares earlier emulator samples and a smoke-only exact run at $k_p=10$, $m_s=2.5$. The earlier 512-history RMSE and the aggregate T7 IC comparisons do not give a validation subset for the headline PL and BT1 samples.

**Concern** A good trajectory RMSE across a validation set does not determine errors in optical depth or the late neutral-fraction likelihood near their observational thresholds. Similarly, the likelihood of a representative mean history and the likelihood averaged over ICs are different targets. The stated T7 maximum absolute gap of 1.908 log-likelihood units is large enough to warrant locating the relevant families before using it as reassurance for PL and BT1.

**Why it matters** A spectrum-dependent likelihood error could alter the relative weight of regions in galaxy parameter space. The existing checks support the older calculations at the level described and leave that potential error unmeasured for the central comparison.

**Resolution test** Benchmark the actual PL and BT1 predictor paths against native calculations at matched high-likelihood points and nearby tails. Report signed errors in $\tau$, $x_{\rm HI}(5.9)$ and their combined log-likelihood contribution, and propagate them into $S$ or show that the changes are too small to alter the scientific conclusion. State whether the target is a representative-history likelihood or an IC-averaged likelihood, with the finite comparison tied to that choice.

### R1-M4 — The fixed-galaxy history response has no measured realization or resolution scale

**Severity** Major  
**Blocking** No  
**Axis** Experimental design

**Claim pointer** The main history figure and interpretation use the atlas as evidence of conditional history sensitivity.

**Evidence pointer** Body 0089–0100, 0268–0278 and 0294–0304. Figures `fig:atlas-history` and `fig:fixed-astro-bt`. Packet `data/21cmtb_evidence_20261029.json`, `histories` and `history_semantics`.

**Concern** The atlas supplies a documented common seed and plane-average differences at common stored redshifts. Executed phase matching and numerical robustness are unverified. The extreme BT series is fully ionized at the highest exported redshift, so the physical transition and optical depth associated with any earlier ionization are unresolved. The second fixed-galaxy export adds a coeval within-BT trend, but uses another prescription and its PL branch is unverified.

**Why it matters** The atlas illustrates sizeable separations, but the experiment does not give a numerical uncertainty for those separations. The smaller shifts and the physical interpretation of the saturated curve are particularly exposed.

**Resolution test** Verify phase pairing and run identity, then repeat one strong and one modest response with independently paired realizations and a grid or volume check. Compare like averages and quote a response alongside its realization scatter. Extend the high-redshift integration and verify initialization for the extreme case if a physical transition or optical depth is to be interpreted. The main comparison can proceed with resolved cases if the boundary-saturated series remains a diagnostic.

## Minor Comments

- **R1-m1** Readability. Main 0029 and body 0142–0161 repeat the three-mass result while the abstract gives no intuitive scale for the change. Define the star-formation factor as the rate per unit halo mass after removing the common cosmological factors and lead with the roughly fivefold reduction at the pivot for these samples. Give the mass dependence where the equation and table are available.
- **R1-m2** Figures and claim scope. Body 0109–0123 and `fig:lf-fits` show curves for $k_p=1$, 3 and 10, whereas the clearest near-PL claim in the prose concerns $k_p=20$ and 30. Include one of those candidate curves or explicitly direct readers to the grid as the evidence for the large-break comparison. Keep the LF claim at the level of archived candidate fits to the 34 selected bins. Failed sampling diagnostics do not erase the demonstrated existence of those points, and the stored maxima do not establish the ordering of optimized likelihoods. Round the PL value in the prose to the precision needed for the reported comparisons.
- **R1-m3** Physical explanation. Body 0135–0139 and 0153–0155. The escape normalization also varies materially in the samples, including between PL and the large-break BT case where the star-formation medians are similar. Acknowledge this when discussing the separation between UV light and escaped ionizing radiation. The source-factor comparison alone cannot summarize the escaping emissivity of a population.
- **R1-m4** Appendix hierarchy. Body 0175–0187 and 0381–0418. Keeping `fig:physics-kpms-current` in the appendix is appropriate. Put the current run's failed diagnostics and unconfirmed prior in its caption, where readers encounter the prior overlay and 95% contour. Cross-reference the earlier sample once and drop either the duplicate older $k_p$–MS panel or its standalone expanded view unless it illustrates an additional point.
- **R1-m5** Prose. Body 0089–0100, 0153–0161 and 0276–0298. Give the positive result and its observable first, with each major limitation placed at the result it qualifies. Consolidate repeated atlas definitions and repeated calls for the next comparison.
- **R1-m6** Reproducibility. In `data/recompute.py`, the input paths follow the source repository layout and the script writes new outputs. Provide a read-only verification command or a documented input and output path for use with the packet layout.

## Technical failings to address before the case is established

R1-M1 and R1-M2 are the immediate barriers to a physical attribution. R1-M3 specifies the relevant validation for that attribution. R1-M4 delimits how far the present fixed-galaxy atlas can support quantitative physical claims.

## Assessment against Nature-style criteria

- **Originality** The supplied introduction identifies the galaxy prescription and simulation framework as adopted. The contribution specific to this article is the comparison across a broken-spectrum model and the translation of fitted coordinates into an active-halo quantity. The packet supports that distinction but leaves priority over prior small-scale-spectrum studies unassessable. The introduction should say which physical question this calculation answers beyond the companion emulator development.
- **Scientific importance** Quantifying whether flexible galaxy properties absorb a direct spectral signal would matter for the interpretation of early-galaxy data. The current experiments demonstrate related sensitivities and compatible candidate fits while leaving that quantitative attribution open.
- **Interdisciplinary readership** The competing effects of halo supply and galaxy output give the paper a question that can travel beyond reionization modelling. A matched observable comparison would make the implication legible to those readers.
- **Technical soundness** The main finite-row arithmetic is sound. The comparison of physical and statistical targets is incomplete, and the free-spectrum run warrants its exploratory label.
- **Readability for nonspecialists** The experiment map and the split between direct histories and refitted LFs help the paper stand on its own. The source explanation would be clearer if it led from halo abundance to UV and ionizing output, introducing each fitted factor as it enters that chain.

## Recommendation posture

Substantive revision before the manuscript makes a strong physics case under the supplied criteria. Retain the appendix placement of the exploratory spectrum projection and the explicit distinction between the three comparisons. The central evidence needed is a controlled observable comparison supported by verified inference targets for the headline source shift.

# Reviewer 2

## Overall assessment

The main text stands on its own after moving the exploratory spectrum projections to the appendix. Its sequence is intelligible: change the spectrum at fixed galaxy parameters, refit the UV luminosity function (LF) independently for each spectrum, and translate a separate set of galaxy samples into star formation at fixed halo mass. The manuscript appropriately limits the free-spectrum distributions to an exploration record. The remaining scientific gap is between this sequence of examples and a result that identifies how galaxy freedom changes the observable response to the matter spectrum.

The packet supports three descriptive findings. The exported fixed-galaxy histories separate in particular cases, the LF archive contains curves with nearly equal stored likelihoods at large break wavenumbers, and two specified arrays give substantially different empirical active-halo star-formation factors. The abstract and conclusion broadly respect those bounds. A controlled attribution of the third finding and a joint explanation of the three findings require additional evidence. I assessed the numbered manuscript, packet figures, frozen records and supplied arrays using the local editorial criteria. The complete executed configurations, predictor validation arrays and independent novelty assessment are outside the available evidence.

## Who would be interested, and why

Reionization modelers and observers of early galaxies would be interested in whether UV galaxy counts can conceal changes in the population of halos that produce them, and in whether the ionization history can expose such changes. Cosmologists working on small-scale initial fluctuations would benefit from knowing which combinations of reionization and galaxy observables retain a spectral response after galaxies are allowed to adjust. The present work maps where to ask these questions in one prescription.

## Major strengths

- The experiment map separates fixed-galaxy, LF-only and joint-history sample products. The main text states the distinction between plane-averaged atlas histories and coeval volume averages and flags the saturated history at the redshift boundary.
- The LF section uses candidate fits as evidence of compatibility. Positive differences in stored likelihood are clearly separated from model preference. The full grid and magnified near-PL differences serve different purposes.
- The active-halo calculation applies the efficiency cap to individual rows and labels the resulting contrast as a ratio of marginal medians. The packet arrays reproduce the pivot-scale contrast and allow a simple check across chronological blocks.

## Major concerns

### R2-M1 — The main comparisons leave the physical explanation unresolved

- **Severity** Major
- **Blocking** Yes
- **Axis** Scientific importance and technical soundness
- **Claim pointer** The main text connects fixed-galaxy history response, refitted LF compatibility and altered source prescriptions as its account of spectrum sensitivity and galaxy freedom. See body lines 0003–0007, 0123 and 0153–0161.
- **Evidence pointer** `tab:experiment-map`, `fig:atlas-history`, `fig:lf-grid` and `tab:fixed-100k` (body lines 0077–0084, 0089–0100, 0104–0123 and 0129–0148). The main fixed-galaxy history, the large-break LF compatibility result and the small-break sample contrast use different comparisons. The later coeval export lacks a verified PL branch (0276–0304).
- **Concern** The response of the LF at fixed galaxies is unmeasured by the displayed comparison, and the response of the history after LF refitting is likewise missing. Near-equal refitted LF likelihoods at large break wavenumber could arise with negligible baseline LF response. The prominent active-halo contrast comes from the small-break case under an attributed joint likelihood. It cannot explain the large-break LF result. A lower rate for an active halo also leaves open the change in population-weighted UV luminosity and escaped ionizing emissivity.
- **Why it matters** The three bounded archive findings can stand individually. They leave unanswered the paper's motivating question about how the spectrum response survives galaxy adjustment, and the unresolved question limits the scientific significance of the current main line.
- **Resolution test** At minimum, compare PL and one large-break near-equality case, plus a small-break contrast if it remains the headline example. For each pair use the same cosmology, normalization convention, solver, numerical settings, observations and parameter support. Show LF and history predictions with galaxies fixed and after applying a common fitting criterion, with likelihood contributions separated. Benchmark changes against numerical and realization variation. If a physical compensation mechanism is claimed, show normalized spectral or halo-variance ratios and halo abundance across the contributing mass range, then show how duty, star formation and escape weight that abundance. The outcome should identify at least one regime with a measurable baseline response that refitting suppresses, or one where the baseline response is already weak.

### R2-M2 — The empirical source contrast lacks a validated matched inference target

- **Severity** Major
- **Blocking** Yes
- **Axis** Technical soundness
- **Claim pointer** The abstract foregrounds the three active-halo ratios and the conclusion presents distinct source prescriptions across the fixed-spectrum samples (main line 0029, body lines 0129–0148 and 0157–0161).
- **Evidence pointer** `chains/pl_100k.h5`, `chains/kp1_ms1p5_100k.h5`, `data/SFR_INTERPRETATION.csv`, `data/SOURCES.json`, body lines 0045, 0082, 0205–0227, 0231–0237 and 0341–0345. The two files contain samples, log probabilities, names and spectrum attributes, with no executed prior or likelihood configuration. `data/t7_update_20261031/t7_ic_sensitivity_report.json` records a multi-IC production decision and failed screens.
- **Concern** I recovered the pivot medians 0.11850 (PL) and 0.02308 (BT) with the stated finite-log-probability cut. Dividing each 3,000-step file into four successive 750-step blocks yields pivot median ratios of approximately 0.197, 0.195, 0.193 and 0.194. This makes a simple chronological-cut explanation unlikely within these files. It does not verify that the executed PL and BT likelihoods and priors are comparable. In particular the log escape normalization differs by almost one dex between the PL and every listed BT sample, including the case where the pivot star-formation factor is close to PL. The PL timescale also differs systematically from the BT cases. These are checks on the run contract, with their cause unresolved. The exact smoke comparison uses an earlier model at a different spectrum. Its moment agreement and development-set trajectory errors do not establish likelihood accuracy for these two targets. The T7 source reports sensitivity to IC treatment, while the text quotes a finite discrepancy without giving its production decision.
- **Why it matters** The empirical ratio is reproducible. Its attribution to a change in spectrum under a common inference model, and its interpretation as a galaxy adjustment supported by the data, remain central and unverified.
- **Resolution test** Identify the executed PL and BT run contracts with executable versions, normalization, parameter ordering, transformed prior support, observation selection, optical-depth integration, likelihood component definitions and predictor identity. Resolve the 5–35 versus 5–30 optical-depth settings for these runs. Compare exact and emulated LF and history likelihood components over representative high-support regions of both samples, and quantify sensitivity of the source contrast to the chosen IC target. Demonstrate stability with independent runs. If the aim is solely to describe the arrays, clearly limit the headline and conclusion to an empirical example and avoid interpreting the inferred shifts as a controlled spectrum effect.

### R2-M3 — The new result needs to be distinguished from its methodological and archival precedents

- **Severity** Major
- **Blocking** No
- **Axis** Originality and interdisciplinary readership
- **Claim pointer** The introduction presents a BT modification of the Park galaxy framework and assigns the emulator to a companion methods article (body lines 0005–0007).
- **Evidence pointer** Body lines 0013–0025, 0087–0148, 0159–0167 and 0268–0274, with the references to Park2019, Breitman2024 and Breitman2026. The supplied references and brief introduction do not establish the precedence of the specific fixed-normalization physical comparison.
- **Concern** The reader can identify which ingredients were adopted, but the new scientific inference relative to earlier studies of the halo population and flexible source models is unclear. The status of the atlas results as prior public displays or new analyses for this manuscript also deserves clarification. The local packet does not establish external priority or duplication.
- **Why it matters** The paper's broader-interest case depends on a demonstrable physical finding, such as a measurable change in the sensitivity of an observable after refitting galaxies. A list of descriptive outputs at different settings leaves that advance difficult to judge.
- **Resolution test** State which analysis and result are new in this article, which outputs come from the atlas, and which validation belongs to the companion paper. Compare the physical conclusion with the closest relevant prior studies using like-for-like claims and explain the consequence for interpreting early galaxy or reionization data.

## Minor comments

- **R2-m1 | Minor | Readability.** The history discussion repeats the saturated-case warning in the caption and text (body 0096 and 0100), while the text gives five high-precision stored optical depths. Lead with one resolved comparison and its physical meaning. Keep the boundary warning near the plotted series and place the exhaustive optical-depth list in a table or supplement. Define the PL reference at first use and make the ordering of cosmic time on the redshift axis explicit for readers outside reionization.
- **R2-m2 | Minor | Figures.** `fig:lf-fits` shows PL and BT cases at break wavenumbers 1, 3 and 10, whereas the main near-equality claim concerns 20–30 (body 0116–0123). Include a representative curve from the stated regime or explicitly describe the plotted curves as distinct illustrative cases, with `fig:lf-grid` providing the evidence for the 20–30 claim. Clarify in the caption that asymmetric bars are plotted as supplied while the likelihood uses symmetrized errors (0055 and 0119).
- **R2-m3 | Minor | Readability and redundancy.** Body lines 0181–0187 adequately explain the status of the relocated spectrum projection. The earlier spectrum focus and corner plot repeat the same two-dimensional count panel by design (0385–0391 and 0436–0444), and the monitoring ranges recur at 0416 and 0444. Keep one plot per diagnostic purpose and one place for detailed chain caveats. Use the space in the main text to translate one result into what changes for the observable, with run chronology in the provenance record.
- **R2-m4 | Minor | Reporting.** The PL stored LF maximum is quoted to 15 decimal places (0106), while the main conclusion concerns differences of order hundredths or smaller. Round the main text to a precision appropriate to the comparison and retain full values in the frozen source record.

## Technical failings to resolve before the physical case is established

R2-M1 requires the crossed fixed and refitted comparison on common observables and matched configurations. R2-M2 requires the executed inference contract, likelihood-level validation and evidence that the interpreted sample contrast survives independent runs. The supplied appendix checks document why these issues remain open.

## Assessment against Nature-style criteria

- **Originality.** The exact configuration and sample reanalysis are identifiable. The physical advance relative to the closest work remains insufficiently distinguished.
- **Scientific importance.** The problem matters because early galaxy counts and reionization history could constrain the same unseen halo population in different ways. The manuscript establishes conditional examples, with the discriminating physical result still missing.
- **Interdisciplinary readership.** The prospect of separating primordial-spectrum effects from galaxy formation would reach across cosmology, galaxy formation and high-redshift observations. The current results stop at the level of this model and archive.
- **Technical soundness.** The finite-array calculation and archive descriptions support bounded statements. The controlled physical attribution and the matched inference target require the checks above.
- **Readability for nonspecialists.** The experiment map and figure relocation help materially. A more direct account of what each observable measures, which intervention produced each comparison, and where the answer changes would make the main line easier to follow.

## Recommendation posture

Substantial revision before the physical case can be assessed at the stated level of scientific importance. The figure relocation is appropriate and the current main text can support a narrower numerical account. A journal-level judgment should rest on the result of the matched physical comparison and the credibility of the sample-based interpretation.

# Reviewer 3

## Overall assessment

The main argument stands without the free-spectrum figure. The reader can see that several exported histories differ at fixed galaxy settings, that separately fitted ultraviolet luminosity functions can look very similar for different spectra, and that the released galaxy samples yield different star-formation rates per active halo. The placement of the free-spectrum plot in Appendix A keeps a poorly explored sample projection from becoming the visual answer to a question the paper cannot yet settle. I would retain that placement.

The strongest potential physical result is a separation between what happens when the halo population changes and what can be absorbed by the galaxies assigned to it. The current draft establishes those pieces at different levels of evidence and with different numerical products. A reader can reconstruct those distinctions from the experiment map, but the paper still asks the reader to assemble the physical argument. The result is a well-qualified inventory of conditional calculations with one clear quantitative source-level contrast.

**Assessment boundary.** I used the supplied v0.22 numbered TeX, figures, source summaries and six HDF5 files under `packet/chains/`. I checked the relevant raw chain summaries by direct read. The executed likelihood and prior configurations, realized initial conditions, emulator weights and underlying validation arrays were unavailable. The packet contains a bibliography and the supplied editorial criteria. It does not establish publication history or allow an exhaustive prior-art comparison.

## Who would be interested and why

Reionization and high-redshift galaxy researchers would be interested in how assumptions about the matter spectrum alter the inferred relation between halo mass and ultraviolet output. Small-scale cosmologists and researchers using galaxy populations to test matter models would be interested in which observables retain sensitivity after the galaxy prescription can vary. Readers in those groups need to see which comparison tests the spectrum directly and which admits a galaxy adjustment.

## Major strengths

- The experiment map makes clear that the fixed-galaxy histories, four-coordinate LF fits and six-coordinate joint samples answer different questions. The LF figures show individual achievable curves and the archived likelihood values on an expanded scale where needed.
- The conversion from fitted coordinates to an active-halo star-formation factor is physically interpretable. The capped formula evaluated row by row gives BT-to-PL median ratios of 0.12277, 0.19477 and 0.30792 at the three stated masses. Using the first and second halves separately with the same finite-log-probability rule gives ratios of about (0.124, 0.196, 0.310) and (0.121, 0.194, 0.307), respectively. This limited sensitivity check supports the descriptive result. It tests chronological selection only.
- The latest free-spectrum sample selection is documented. The last 300 steps reproduce the reported medians and equal-tail ranges, and the adjacent warning explains why these empirical ranges cannot answer whether the observations are informative.

## Major Concerns

### R3-M1 — Show the two physical explanations on the same observable

- **Severity** Major
- **Blocking** No
- **Axis** Mechanism evidence and scientific importance
- **Claim pointer** `main_numbered.txt:29` and `body_numbered.txt:123,153–161`. Near-equal stored LF fits are compatible with weak direct LF sensitivity, galaxy adjustment or both.
- **Evidence pointer** `tab:experiment-map`, `fig:atlas-history`, `fig:lf-grid`, `fig:lf-fits`, and `data/21cmtb_evidence_20261029.json`. The history atlas changes the spectrum at one fixed galaxy prescription. The LF archive changes galaxy parameters separately for each spectrum. The largest active-halo contrast comes from the six-coordinate joint samples for PL and the strong small-break case.
- **Concern and why it matters** The evidence establishes the existence of comparable candidate LFs. It gives no direct LF response at the same galaxy point for the spectra that fit similarly. A reduced active-halo star-formation factor at the small break also gives no measurement of how much of an LF change was absorbed by refitting at a large break. This is a limitation of the physical significance of the present result, and the draft already acknowledges it.
- **Resolution test** In one numerical setup, show the same binned LFs and history observables for a PL galaxy point evaluated with PL, that same galaxy point evaluated with BT, and the BT point after adjustment to the same objective. Include one small-break case and one near-PL candidate from the large-break grid. Plot the change before and after adjustment against the observational errors or the relevant likelihood scale. Show the corresponding change in halo abundance or mass variance across the masses contributing to those bins if attributing the response to halo supply. A large fixed-galaxy observable shift followed by recovery after adjustment would provide evidence for compensation. A small fixed-galaxy shift would support weak direct sensitivity at that comparison point. The current compatibility statement can stand independently.

### R3-M2 — Establish the provenance of the headline fixed-spectrum comparison

- **Severity** Major
- **Blocking** Yes, for interpreting the headline galaxy contrast as a response to changing the spectrum in a common joint inference
- **Axis** Experimental design and reproducibility
- **Claim pointer** `main_numbered.txt:29` and `body_numbered.txt:127–148,155–161`. The abstract and conclusion foreground the PL versus small-break BT contrast under the adopted prescription.
- **Evidence pointer** `chains/pl_100k.h5`, `chains/kp1_ms1p5_100k.h5`, `chains/kp20_ms2p5_10000.h5`, `data/SOURCES.json`, and `body_numbered.txt:67–74,132–139,157,163–167,205–227,229–237`. The HDF5 files supply the coordinate order, spectrum tags and finite-row summaries, with no executed target manifest. The PL file carries `kp=0, ms=0`, which is a file tag. The paper itself describes the PL implementation as a distinct numerical branch.
- **Concern and why it matters** The row-wise calculation is reproducible, and its magnitude persists across the two chronological halves. Neither check identifies which settings produced the contrast. The six-coordinate samples are attributed to a shared likelihood, but the executed prior, numerical branch parity and likelihood components are unavailable. The source-level result also need not move as a unit. For example, the large-break BT file has a pivot star-formation factor close to PL (0.11921 versus 0.11850), but its median log escape normalization is about −1.079 versus −0.229 for PL. That difference merits a provenance check before assigning either coordinate shift to the spectrum. The exact smoke comparison and pooled history RMSE do not establish target parity for the headline runs. The T7 record also reports an absolute difference of up to 1.91 between a mean-history log likelihood and its finite-IC counterpart, so small trajectory errors alone provide no bound at the likelihood scale.
- **Resolution test** Supply per-run executed settings and demonstrate common priors in the actual sampled coordinates, identical LF point selection and likelihood conventions, and matched numerical settings apart from the spectral intervention. An implementation check should recover PL observables when the BT exponent equals the native tilt, within a documented tolerance. Show sampling stability across independent starts and validate history likelihood errors for PL and the small-break BT case on representative high-weight samples. State explicitly whether the target conditions on a representative history or marginalizes over initial conditions. With the present files, the result can instead stand as a comparison of two labelled exports with a shared algebraic source prescription. The abstract and conclusion should then make that the status of the numerical contrast and give priority to the export-level results.

### R3-M3 — Put the physical comparison before the archive description

- **Severity** Major
- **Blocking** No
- **Axis** Readability for nonspecialists and interdisciplinary readership
- **Claim pointer** `main_numbered.txt:24–29` and `body_numbered.txt:3–7,76–100,104–129,142–161`. The paper compares a change to the source population with a change to the amount of radiation assigned to each halo.
- **Evidence pointer** `fig:atlas-history`, `fig:lf-grid`, `tab:fixed-100k`, and `eq:physics-sfr-factor`.
- **Concern and why it matters** The first history result presents all five optical depths to six or seven digits and spends much of the paragraph on the export that was already ionized at its upper boundary. A much easier entry point is the contrast between resolved histories at a common redshift. At the atlas node near redshift 8.17, the neutral fraction is 0.754 in PL, 0.467 at the break scale 10 with slope 2.5, and zero at break scale 1 with slope 1.5. The LF section then changes the question to what the data can accommodate after independent galaxy fits. The reader only gets the clearest account of how source abundance, active fraction, stellar output and photon escape connect these sections at lines 153–155. The abstract's phrase “released six-coordinate samples” likewise identifies the archive before explaining the quantity or its bearing on the question. These choices make the study feel more dependent on its appendices than it is.
- **Resolution test** Give the reader a short physical map near the start. Explain that moving the break changes which wavelengths receive the new slope, that fixed normalization can rescale the spectrum, and that UV counts depend jointly on halo abundance, the active fraction and luminosity per active halo. Lead the history section with one resolved fixed-galaxy contrast, then explain that independent LF refits let galaxy properties change. Present the source-factor result in physical terms, preferably with the two sets of empirical quantiles versus halo mass already supported by `data/SFR_INTERPRETATION.csv`. A reader who skips the appendices should still be able to name the intervention, the observable and the supported inference for each result. The exploratory free-spectrum figure can stay in the appendix.

## Minor Comments

### R3-m1 — Consolidate repeated qualifications at the point of interpretation

- **Axis** Writing clarity
- **Affected element and evidence pointer** `body_numbered.txt:7,72,76–85,155–167,177–187,276–303,383–444`.
- **Issue and correction** The main text repeatedly sends readers to supporting records and restates the need for a matched comparison. The earlier-chain appendix gives the same split-monitor ranges at lines 416 and 444, and the fixed-astrophysics appendix spreads the caveat about the unverified PL branch across two subsections and a caption. Give the matched-comparison limitation once in the main interpretation and end the conclusion with the physical result supported by the paper. Consolidate each appendix's provenance discussion. Retain qualifications that change how results can be read where the results appear. These include the atlas plane-versus-volume distinction, the unresolved high-redshift boundary, failed LF sampling diagnostics, the finite-row interpretation of the galaxy medians, the distinction between likelihood of a representative history and averaging likelihoods, and the unconfirmed prior behind the free-spectrum reference lines.

### R3-m2 — Make the free-spectrum caption interpretable in isolation

- **Axis** Figures and tables
- **Affected element and evidence pointer** `body_numbered.txt:177–187`, `fig:physics-kpms-current`, `figures/btemu/fig_physics_kpms_100k.png`.
- **Issue and correction** The plotted offsets, filled 95% region and prior lines resemble a posterior constraint on a quick read. The warning comes after the caption. Identify the region and offsets as descriptive summaries of an unequilibrated or unvalidated selection in the caption itself, and label the orange curves as reference densities with unverified executed priors. Change the surrounding comparison of the sampled and reference ranges to an explicitly descriptive comparison of their occupied spans.

### R3-m3 — Round for interpretation and align nomenclature

- **Axis** Writing clarity
- **Affected element and evidence pointer** `body_numbered.txt:23–31,91–112,123,148`.
- **Issue and correction** The main text alternates among BT, “blue-tilted,” `MS` and (m_s), and the LF section gives the PL maximum to fifteen significant digits. Use physical notation in the prose, with stored field names in Methods or the provenance tables. Define “PL” as the reference with no break in plain language before relying on the abbreviation. Round likelihood and optical-depth examples to precision commensurate with their interpretation and leave full values in the source records. State that the quoted ratios compare empirical medians of active-halo factors at the same mass. They do not include changes in halo abundance, duty cycle or escape.

## Technical failings to address before the physical case is established

The existing evidence supports a contrast among exported histories, the existence of LF curves with similar fit scores and a reproducible descriptive difference between released sample sets. The inference that changing the spectrum in a common joint calculation produces the headline difference requires the checks in R3-M2. The comparative test in R3-M1 would turn the present observation of compatibility into a result about why compatibility occurs. The exact sampling target and the initial-condition dependence of the relevant runs remain unverified from the packet.

## Assessment against the supplied Nature-style criteria

- **Originality.** The contribution apparent in the packet is the study of a broken matter spectrum with the flexible Park galaxy prescription, including a mass-dependent comparison of the source factors in released samples. The introduction names the inherited model but gives little context about what specific physics result extends earlier small-scale-spectrum work. The packet supports a distinction from the cited Park setup. Priority in the wider literature is unassessed.
- **Scientific importance.** A demonstrated distinction between limited observable sensitivity and compensating galaxy changes would affect interpretation of high-redshift data. The present calculations make the question concrete and establish conditional examples. They leave its physical resolution open.
- **Interdisciplinary readership.** The connection between structure formation, galaxy light and the timing of reionization could reach several astronomy communities. Leading with fixed-galaxy versus refitted observables would make the paper accessible beyond users of these codes.
- **Technical soundness.** The tabulated headline sample statistics reproduce and the figures preserve important distinctions among experiments. Inference validity and matched-run attribution require provenance and targeted validation. The exceptional early-ionized atlas history should continue to be reported as boundary limited.
- **Readability for nonspecialists.** The appendix placement of the exploratory spectrum projection helps. The main text needs a clearer sequence of physical questions and fewer repeated archive qualifications, with each necessary caveat adjacent to the claim it limits.

## Recommendation posture

Substantial revision. The paper can present a credible conditional numerical result now. A stronger Nature-style case would use a matched comparison to identify the physical origin of LF compatibility and secure the interpretation of the headline source-level contrast.

# Cross-review synthesis (post-review, not shown to reviewers)

## Consensus strengths

All three reviews find that the main text stands with the free-spectrum projection in Appendix A. The experiment map distinguishes fixed-galaxy histories, LF candidate fits and the six-coordinate galaxy samples. The capped active-halo calculation gives the sample contrast a precise physical meaning. The history and LF displays remain interpretable when the scientific qualifications are retained.

## Consensus blocking concerns

**S1. Executed target parity for a controlled PL/BT interpretation.** R1-M2, R2-M2 and R3-M2 mark this as blocking for attributing the headline galaxy contrast to the spectral intervention. The finite-row calculation reproduces. The actual priors, LF and history likelihood components, fixed coordinates and predictor routing still need to be reconciled across runs. The companion validation needs to address likelihood errors for the relevant PL and BT samples. The narrower description of the released arrays survives.

**S2. The matched observable comparison.** R1-M1 and R2-M1 designate it blocking for the stronger scientific case. R3-M1 identifies the same gap with Blocking No for the stated compatibility result. Fixed-galaxy history changes and separately refitted LFs address different observables. The strongest SFR contrast is at kp=1, while the closest stored LF scores occur at kp=20–30. A common comparison of LF bins and history outputs before and after galaxy adjustment would measure how much response the adjustment removes. The reports differ on what level of contribution requires that result.

## Other concerns and differences in emphasis

R1-M3 and R1-M4 separately emphasize likelihood fidelity and the realization/resolution scale of the atlas response. R2-M3 emphasizes novelty and the distinction from the atlas and companion methods work. R3-M3 emphasizes presenting the observable contrast before the archive and run details. The local evidence establishes no external priority. The manuscript defines an input linear matter spectrum at fixed sigma8, and that scope should also govern the interpretation of the broader significance.

## Forensic findings

The fixed-spectrum summaries, active-halo ratios and free-spectrum empirical intervals reproduce. Restricting the SFR calculation to the last half gives ratios of 0.1215, 0.1936 and 0.3065, close to the stated 0.123, 0.195 and 0.308. Independent sampling precision and parity of the executed PL/BT inference targets remain unverified. The displayed LF examples and the strongest large-break score result concern different cases. The grid supplies the evidence for the latter. The checked arithmetic gives no contradiction. See FORENSIC_AUDIT.md for pointers and exact outputs.

## Remaining repetition and defensive prose

| Body location | Assessment | Review action |
|---|---|---|
| 91, 96, 100 | Stored-node description and upper-boundary warning recur | Lead with a resolved common-redshift contrast and keep the saturation qualification adjacent to the affected series |
| 106, 112, 119, 123 | Fit setup and status recur. The PL stored score is quoted to fifteen decimal places | Put the common selection and diagnostic status once beside the grid. Use the figure caption to explain its display and preserve the exact value in the source record |
| 129, 132 | Selection provenance and appendix pointers repeat | State the selection once in the table caption |
| 148, 153–161 | The SFR trend and the need for a matched comparison are stated more than once | Reserve the results for numbers, the interpretation for the link from halo abundance to luminosity and escape, and the conclusion for the bounded result |
| 177–187 | The figure caption is weaker than the adjacent sampling warning | Identify the contours as empirical selected-row densities and refer to the monitoring table and archived prior status |
| 385–444 | The older spectrum focus repeats the corner panel and its monitoring range | Keep one display for that diagnostic purpose and one definition of its monitoring range |

These points combine R1-m1–m5, R2-m1–m4 and R3-m1–m3. The failed LF sampling diagnostics, saturated high-redshift curve, plane-versus-volume distinction and prior/likelihood provenance limits materially affect interpretation. Keep each qualification near the relevant claim. The shorter text can carry one numerical example in physical language. At the pivot mass, the empirical BT factor is about one fifth of PL, and the table and equation can carry the mass dependence.

## Broad-interest assessment

The connection between the abundance of early halos and the radiation assigned to each galaxy is legible across cosmology and galaxy formation. At present the paper supports a conditional numerical result and a reproducible source-level contrast. Its stronger significance depends on explaining which observables retain a spectrum response after the galaxy prescription can adjust.

# Risk / unsupported claims

- Quantitative compensation and weak direct LF sensitivity remain unresolved alternatives.
- The active-halo factor gives no direct estimate of a change in halo abundance or total ionizing emissivity.
- The archived candidate fit scores cannot establish optimized likelihood ordering, statistical significance or model preference.
- The short free-spectrum projection supplies no observational constraint under a verified executed prior.
- This review assesses the supplied manuscript and local evidence. External precedence, complete execution settings and predictive validation are partly outside scope.
