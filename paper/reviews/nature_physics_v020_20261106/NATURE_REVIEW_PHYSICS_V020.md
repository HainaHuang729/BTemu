# Review setup

Input is the full physics manuscript v0.20 and its immutable common source packet. The author requested assessment rather than editing. Focus is scientific line, evidence-supported conclusions, defensive prose and repetition. Three independent contexts receive the same packet, criteria and only their own preassigned emphasis.

Preassigned emphasis, fixed before launch

1. R1 foregrounds technical validity and support for the physical conclusions.
2. R2 foregrounds originality, scientific significance and the causal or inferential main line.
3. R3 foregrounds clarity, physical explanation, defensive language and repetition.

All cover the five criteria. Reports are finalized and frozen before comparison and the separate forensic audit.


# Reviewer 1

## Review setup

**Input scope** Complete physics manuscript v0.20, including its abstract, numbered body, figures, appendices and supplied data records.

**Assessment boundary** This assessment concerns the physics article, not the companion emulator methods contribution. It uses only the immutable packet and common criteria. Later-file metadata establishes availability, not revised v0.20 results.

**Shared manuscript claim summary** Spectrum changes separate fixed-galaxy ionization histories; independently adjusted galaxies yield similar stored LF maxima over part of the grid; joint summaries change star-formation coordinates and escape-fraction spreads. Spectrum identifiability remains unresolved.

**Visible evidence base** Numbered manuscript, LF grid and curves, two fixed-galaxy history sets, T3 summaries and script, newer fixed-spectrum report, finite approximation checks and chain diagnostics.

**Missing materials affecting confidence** Several raw chains, actual inference-prior specifications, complete numerical configurations and independent convergence evidence are unavailable for the comparisons emphasized below.

## Overall assessment

The three-stage scientific line is intelligible and appropriate. The strongest established results are qualitative spectrum sensitivity in the exported histories and the existence of independently fitted LF curves with comparable likelihoods. The observational interpretation is considerably less secure. Explicitly calling moments descriptive avoids a false posterior claim, but does not establish that differences between separately sampled distributions reflect added observations or changed spectra. The manuscript is candid about this limitation. Its central physics question consequently remains an investigation programme rather than a completed inference.

## Who would be interested in the results, and why

Researchers studying reionization, high-redshift galaxies and small-scale cosmology would value a reliable demonstration of which spectral effects galaxy freedom absorbs and which survive joint observations. That distinction could inform the interpretation of future 21-cm measurements and existing galaxy surveys.

## Major strengths

The spectrum definition explicitly includes its fixed-sigma8 normalization and distinguishes the numerical PL reference from removing the analytic break. The separation between star formation and ionizing escape is clearly motivated. Figure 3 supplies an especially useful visual demonstration that distinct fitted spectra can reproduce similar LF shapes. The paper correctly withholds a spectrum constraint from the unconverged free-spectrum chain, excludes an unverified PL history, and declines to interpret the saturated atlas series as a resolved transition.

## Major Concerns

### R1-M1

**Severity** Major  
**Blocking** Yes  
**Axis** Technical soundness, statistical rigor

**Claim pointer** Adding history observations produces the largest decrease in escape-normalization spread; newer fixed-spectrum fitted centres shift with break scale. Both statements enter the abstract and conclusions.

**Evidence pointer** main_numbered.txt line 28; body_numbered.txt lines 48, 168–191, 243–245 and 317–328; data/t3_update_20261103/t3_fig.py; data/model_update_20261104/RESULTS_20261104.md, section 2.

**Concern** The arithmetic summaries support statements about the exported samples, but their physical attribution is not established. Two T3 raw files are absent, their parameter orders are unverified, and the generating script applies labels from the final file to all three arrays without checking equality. Full common configurations and stationarity diagnostics are missing. The newer fixed-spectrum results report acceptance fractions and 3,000 steps, but leave retention, centre definition, spread definition and independent convergence unspecified. The manuscript explains two possible transformed-prior supports without stating which actual inference support was used. This matters especially for broad escape-fraction distributions and for comparisons involving different pipelines.

**Why it matters** These comparisons carry the paper's positive observational conclusions. Calling them descriptive does not exclude prior, selection or exploration differences as explanations for their changes.

**Resolution test** Supply the actual prior densities and supports, verify coordinate orders and common configurations, define all retained selections and summaries, and demonstrate stable estimates across independent ensembles and retention windows for the comparisons retained as physical results. Otherwise restrict these statements to unvalidated export summaries and remove their role as headline observational findings. Newer file availability alone does not validate the selections printed in v0.20.

### R1-M2

**Severity** Major  
**Blocking** No  
**Axis** Scientific importance, mechanism evidence

**Claim pointer** The contrast between fixed-galaxy sensitivity and independently fitted LFs connects spectrum changes to compensating galaxy freedom.

**Evidence pointer** body_numbered.txt lines 113–158, 191 and 235–237; LF-grid table at lines 342–355; figures labelled atlas-history, fixed-astro-bt and lf-fits.

**Concern** Similar refitted LF maxima show that the archive contains comparably fitting prescriptions. They do not quantify how much of an initially observable spectral effect was absorbed by galaxy adjustments. Near-PL maxima at large break scales are also compatible with intrinsically weak LF sensitivity there. The fixed-galaxy demonstrations and fitted-LF comparison use different prescriptions and numerical products, and the manuscript supplies no matched before-and-after LF residuals or fitted joint-history predictions. The paper itself identifies the latter as future work.

**Why it matters** The proposed physical insight concerns distinguishability. An existence result for good LF fits is useful, but does not yet reveal the mechanism or extent of compensation.

**Resolution test** For selected identical spectrum points, show fixed-galaxy and refitted LF predictions against a common reference, together with the corresponding galaxy-coordinate changes. Add histories and optical depths from the same joint fits, or explicitly narrow the contribution to sensitivity and fit compatibility without claiming a resolved compensation mechanism.

### R1-M3

**Severity** Major  
**Blocking** No  
**Axis** Technical soundness, approximation validity

**Claim pointer** Representative-history joint calculations support interpreting the reported galaxy-coordinate distributions physically.

**Evidence pointer** body_numbered.txt lines 70–77 and 265–285; data/t7_update_20261031/t7_ic_sensitivity_report.json, family_quantiles and single_IC_production_decision; data/model_update_20261104/RESULTS_20261104.md, sections 1 and 6.

**Concern** The deterministic target is clearly defined, which is good. However, the supplied finite-IC comparison reaches a log-likelihood difference of 1.90797, while the exact comparison uses a smoke-only unconverged chain. The newer fixed-spectrum centres also use a different history model whose matched exact comparison was still pending in the source report. Neither global history RMSE nor finite-chain moment agreement establishes negligible impact on the particular inter-model shifts being interpreted.

**Why it matters** This uncertainty affects the physics evidence chain even though emulator development belongs in another article.

**Resolution test** Evaluate likelihood discrepancies and observable predictions at representative supported points from the relevant fixed-spectrum comparisons, and assess whether corrections materially change their contrasts. Retain the deterministic target explicitly if intended; demonstrate robustness rather than assuming equivalence to IC marginalization.

## Minor Comments

### R1-m1

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Main narrative and uncertainty framing  
**Evidence pointer** body_numbered.txt lines 175, 193–230, 237–245 and appendices at 331–398.

**Issue** Run chronology and repeated qualifications obscure the otherwise clear scientific progression. Necessary statements about failed diagnostics and unresolved identifiability recur alongside detailed archive accounting.

**Required correction** Keep uncertainty labels where numbers or plots might otherwise imply constraints. Consolidate repeated explanation into one status paragraph and one run-definition table; move continuation chronology to the appendix. Preserve the abstract and conclusion limitation.

### R1-m2

**Severity** Minor  
**Axis** Originality  
**Affected element** Introduction  
**Evidence pointer** body_numbered.txt lines 5–9.

**Issue** Park et al. supplies the galaxy and data-combination rationale, but the new physics result relative to that starting point is not stated sharply.

**Required correction** Identify the specific spectral extension and demonstrated scientific increment, keeping unresolved spectrum inference distinct from established results. External priority cannot be assessed from the supplied references alone.

## Technical failings that need to be addressed before the case is established

R1-M1 blocks the observational interpretation. R1-M2 and R1-M3 materially limit its explanatory reach and robustness.

## Assessment against Nature-style criteria

Originality is plausible in the supplied spectral extension, but priority remains unverified. Scientific importance is potentially substantial; presently the quantitative identifiability result is missing. Interdisciplinary interest is credible through the connection between dark-matter structure and galaxy formation. Technical soundness is strongest for descriptive exports and weakest for observational attribution. Nonspecialist readability benefits from the introduction but suffers from provenance-heavy repetition.

## Recommendation posture

Substantive revision is needed before the positive observational findings support a strong physics case. This is an assessment of evidential readiness, not an editorial decision.


# Reviewer 2

**Input scope** Complete physics working draft v0.20, including appendices, supplied data summaries and figure descriptions in the immutable packet. Line references below refer to `body_numbered.txt` unless specified otherwise.

**Assessment boundary** This assesses the physics argument rather than the separate BTemu methods contribution. External priority, unpublished companion work and missing native records are not independently assessable. Later file availability is not evidence for revised v0.20 results.

**Overall assessment** The manuscript asks a worthwhile question about separating small-scale matter-spectrum changes from uncertain galaxy formation. Its strongest supported result is conditional sensitivity of ionization histories, accompanied by examples of similarly fitting luminosity functions after galaxy adjustment. Its principal weakness is that these examples do not yet answer the stated identifiability question. The authors acknowledge this explicitly, which improves reliability but leaves a physics paper whose concluding result is partly an account of unfinished inference. The summary is appropriately restrained; stronger significance requires a completed observational comparison or a sharper, quantitatively established conditional conclusion.

**Who would be interested in the results, and why** Researchers studying reionization, high-redshift galaxies and small-scale cosmology would value a reliable map of which spectral changes survive galaxy freedom. The broader connection between unseen matter and the first ionizing sources is accessible and potentially important. The present numerical summaries do not yet establish how observations change that connection.

**Major strengths** The three-stage organization separates fixed-galaxy response from fitted-galaxy freedom and joint exploration. The model equations explain why UV light and ionizing escape probe different parameter combinations. The manuscript distinguishes fixed-sigma8 matter spectra from fixed primordial amplitude, identifies the separate numerical PL branch, and avoids treating near-equal stored likelihoods as significance or evidence ratios. It also excludes an unverified PL export and does not attribute mock offsets uniquely to a PL assumption when the nominal BT recovery is itself unstable. These are substantive strengths in claim calibration.

## Major Concerns

### R2-M1

**Severity** Major  
**Blocking** Yes  
**Axis** Scientific importance and originality  
**Claim pointer** The central question is how matter-spectrum changes can be distinguished from galaxy astrophysics, followed through fixed histories, LF fits and joint samples (lines 7–9 and 197).

**Evidence pointer** Lines 158, 191, 228–237 and 243–245. The free-spectrum monitor reaches 1.5125 (line 228); line 230 explicitly leaves weak information versus incomplete exploration unresolved. The introduction identifies the adopted Park prescription and its existing data-combination logic (lines 5–7).

**Concern** The manuscript establishes examples of sensitivity and accommodation, but no completed result about distinguishability. Similar LF maxima at large break scales could reflect little response in the selected observations as well as compensation by galaxy parameters. Broad exploratory spectrum distributions cannot distinguish observational degeneracy from sampling failure. The fixed-spectrum parameter shifts do not supply that missing distinction. Consequently the main physics advance beyond applying an established flexible galaxy prescription to modified spectra remains insufficiently defined. This is not a claim that the work lacks external novelty, which cannot be settled from this packet.

**Why it matters** The astrophysical question motivates the paper's importance. An honest statement that the observational answer remains unknown does not itself establish an important new observational or physical limitation.

**Resolution test** Establish a quantitative result about residual spectral discrimination using verified joint exploration, or narrow the paper to a demonstrated conditional sensitivity result. For the latter route, quantify where the observational predictions change and how much refitting restores agreement. State explicitly what new physical conclusion follows beyond the adopted prescription and what remains a methods or validation deliverable.

### R2-M2

**Severity** Major  
**Blocking** Yes  
**Axis** Technical soundness and inferential attribution  
**Claim pointer** Adding history observations produces the largest decrease in escape-normalization sample spread, while fixed-spectrum fitted star-formation shifts connect spectrum sensitivity to galaxy freedom (lines 168, 191, 237 and 245).

**Evidence pointer** T3 selection and table at lines 315–328; the source JSON `data/t3_update_20261103/t3_obs_combinations.json`; fixed-spectrum summaries at lines 180–193 and `data/model_update_20261104/RESULTS_20261104.md`, section 2. Lines 48 and 320 identify prior-support dependence and missing configuration/diagnostic records.

**Concern** The numerical spread decrease is faithfully reported, but attributing it to added observational information requires comparable inference targets and adequately explored samples. Two T3 raw chains and their coordinate orders remain unverified, and complete configuration and diagnostic records are absent. The newer fixed-spectrum table reports unspecified centres and spreads, omits the sixth galaxy coordinate and supplies acceptance fractions rather than evidence of stationary exploration. The manuscript correctly calls these descriptive statistics, yet promotes their changes into the abstract and conclusions as the main evidence for its physical interpretation. A descriptive label does not resolve this attribution problem.

**Why it matters** These comparisons provide most of the positive inference result once free-spectrum identifiability is left unresolved. Differences in priors, coordinate assignments or exploration could alter the physical reading without changing the displayed summary arithmetic.

**Resolution test** Verify coordinate orders, likelihood terms, transformed priors, fixed settings and sample selections for every compared run. Supply exploration diagnostics appropriate to independent runs and define the newer summary statistic and coverage. Then demonstrate stability of the stated contrasts. Otherwise retain them as provisional products outside the central conclusions.

### R2-M3

**Severity** Major  
**Blocking** No  
**Axis** Mechanism evidence and scientific interpretation  
**Claim pointer** The fixed-spectrum shifts connect fixed-galaxy history sensitivity to the galaxy freedom seen in LF fits (lines 191 and 235).

**Evidence pointer** Fixed histories at lines 113–133, four-coordinate LF fits at lines 141–158 and 333, six-coordinate newer summaries at lines 180–193, and the proposed same-sample observable predictions at line 237.

**Concern** This connection currently joins different experiments with different galaxy prescriptions, sampled dimensions and numerical products. The controlled within-BT history comparison supports response to changing the input spectrum. It does not demonstrate that the later fitted parameter shifts are the compensating pathway that restores agreement in both LFs and reionization observables. The authors themselves identify the missing observable-space bridge.

**Why it matters** A physically interpretable compensation mechanism would strengthen the contribution beyond a collection of parameter summaries.

**Resolution test** Show LF, neutral-history and optical-depth predictions from matched fitted samples or representative verified fits across the selected spectra. Identify what is restored by adjustment and what residual remains. Preserve the stated fixed-sigma8 scope when interpreting this response.

## Minor Comments

### R2-m1

**Severity** Minor  
**Axis** Readability for nonspecialists  
**Affected element** Repeated qualifications and archive detail  
**Evidence pointer** Lines 147, 154, 202, 209, 228–239 and 375–398.

**Issue** Repeated warnings about stored samples, plot counts and exploratory status interrupt the physics argument. They are necessary qualifications, but the reader repeatedly encounters the same limitation before learning its scientific consequence.

**Required correction** Keep a concise qualification beside each central result and consolidate shared sampling conventions in one referenced location. Use the discussion to explain consequences for the physical conclusion rather than repeat the inventory.

## Assessment and recommendation posture

**Technical failings requiring resolution** R2-M1 and R2-M2 prevent the central inference case from being established. R2-M3 materially weakens its physical interpretation.

**Assessment against Nature-style criteria** Original calculations are presented, but their distinctive scientific conclusion needs sharpening. Outstanding scientific importance and interdisciplinary implications remain potential rather than demonstrated. Technical soundness is stronger for conditional model sensitivity than for inference comparisons. The introductory explanation is accessible, while archive terminology and defensive repetition reduce readability. Substantial revision and a decisive physics result are needed before a strong broad-interest case can be assessed. This is a referee assessment, not an editorial decision.


# Reviewer 3

## Review setup

**Input scope** Complete physics manuscript v0.20, including its appendices, numbered sources, supplied figures and frozen data summaries. This assessment concerns the physics article, not the BTemu methods contribution.

**Assessment boundary** I use the immutable packet and its editorial criteria only. Native calculations, absent chains and external run records cannot be independently assessed. Later-file availability does not validate the v0.20 selections.

**Shared manuscript claim summary** Small-scale spectrum changes separate fixed-galaxy ionization histories, while independently adjusted galaxies admit similar stored luminosity-function fits over part of the grid. History observations primarily reduce the reported escape-normalization spread. Surviving information about the spectrum remains unresolved.

**Visible evidence base** The numbered text, atlas histories and LF grid in `21cmtb_evidence_20261029.json`, T3 means and spreads, November 4 fixed-spectrum summaries, approximation summaries and accompanying figures.

**Missing materials affecting confidence** Complete priors and configuration parity, two T3 raw chains and their coordinate records, newer fixed-spectrum chains and diagnostic definitions, and converged independent free-spectrum calculations.

## Overall assessment

The manuscript has a clear physical question and unusually candid limitations. Its strongest supported result is a demonstration of model sensitivity together with the existence of differently configured galaxy fits, rather than an observational determination of the matter spectrum. More seriously, two prominently summarized comparisons remain descriptions of incompletely documented samples. Calling them descriptive is appropriate but does not establish that their differences arise from the intended physical or observational change.

## Who would be interested in the results, and why

Researchers studying reionization, early galaxies and small-scale cosmology would value an explicit demonstration of how galaxy freedom changes the interpretation of matter-spectrum sensitivity. A broader readership could follow the contrast between counting galaxy light and accounting for escaped ionizing photons, provided the paper quantifies that contrast in observables.

## Major strengths

The introductory question is direct. The galaxy equations explain why ultraviolet light and ionization history test different combinations. Fixed-sigma8 normalization, the separate numerical PL branch and the unresolved saturated history are explicitly identified. The LF archive supplies actual fitted examples, not merely an assertion that astrophysics might compensate. The manuscript correctly avoids interpreting exploratory spectrum histograms as constraints.

## Major Concerns

### R3-M1

**Severity** Major  
**Blocking** Yes  
**Axis** Technical soundness and data support

**Claim pointer** Adding history observations gives the largest decrease in the escape-normalization sample spread, and newer fixed-spectrum shifts connect history sensitivity with galaxy freedom. Abstract, main lines 28; body lines 168, 191 and 243-245.

**Evidence pointer** Body lines 180-193, 317-328; `t3_obs_combinations.json`, runs and note; `RESULTS_20261104.md`, section 2.

**Concern** The exported numbers support the stated arithmetic. They do not yet establish a controlled comparison. Two T3 coordinate orders remain unverified, configuration and diagnostic records are absent, and the November 4 centres have unspecified estimands and coverage with one galaxy coordinate omitted. Section 48 explains that different transformed prior supports are possible without identifying the support actually used by each comparison. Acceptance fractions cannot establish stationarity or prior parity.

**Why it matters** These are headline physical interpretations. Without verified coordinate labels and matched inference targets, even the direction attributed to adding observations or changing the break scale is not securely established as that effect.

**Resolution test** Supply a compact comparison record verifying coordinate order, likelihood components, all fixed settings, transformed priors, retained steps and the definition of each centre and spread. Establish reproducibility and sampling stability for the displayed comparisons. Otherwise remove their evidential role in the abstract and conclusions and retain them as provisional numerical reports. This blocks the current observation-information claim, not the narrower fixed-prescription sensitivity demonstration.

### R3-M2

**Severity** Major  
**Blocking** No  
**Axis** Physical explanation and scientific importance

**Claim pointer** Near-PL maxima at larger break scales demonstrate galaxy freedom, with fixed-spectrum shifts connecting this to history sensitivity. Body lines 158, 191 and 235.

**Evidence pointer** Spectrum definition at lines 16-28; galaxy equations at 38-46; LF grid and Table of stored maxima at 141-158 and 342-355; missing same-sample observable predictions acknowledged at 237.

**Concern** Similar optimized LF values can reflect either compensation by galaxy parameters or little change in the matter spectrum over the halo masses probed by those observations. The manuscript supplies no mass-scale or observable bridge that distinguishes these explanations at large break scales. Fixed-galaxy histories use different sampling geometries and prescriptions from the LF and joint products. Their juxtaposition motivates compensation but does not quantify its role.

**Why it matters** This distinction determines whether the physics result is an astrophysical degeneracy or simply limited sensitivity to the selected scales.

**Resolution test** Show, for representative matched configurations, the spectrum or halo-source change over the relevant masses and the LF or emissivity response before and after galaxy adjustment. Explain the direction of the eta-star shift through the supplied star-formation equations. Until such evidence exists, describe similar LF fits as compatible with both explanations.

### R3-M3

**Severity** Major  
**Blocking** No  
**Axis** Readability for nonspecialists

**Claim pointer** The paper answers its physical question through three calculations. Body lines 7-9.

**Evidence pointer** Body lines 166-230 introduce T3, a 100,000-example model, a seven-coordinate run and older six/eight-coordinate samples in succession; appendices at 331-398 and 400-478 retain further historical products.

**Concern** The results sequence is organized partly by delivery date and archive identity. Readers must reconstruct which products share a physical target before interpreting the results. Training size becomes a subsection title ahead of the physical question. 

**Why it matters** This obscures the evidence chain and physical contribution.

**Resolution test** Organize the main results around fixed-galaxy sensitivity, fitted-galaxy response and added-observation information. Give one compact experiment map identifying fixed and varied quantities, data, predictor and inferential status. Move chronological reconciliation and auxiliary recovery inventories into a clearly separated provenance supplement.

## Minor Comments

### R3-m1

**Severity** Minor  
**Axis** Writing clarity  
**Affected element** Repeated explanation and defensive language  
**Evidence pointer** Body lines 3, 7 and 9; 109 and 113; 235-245.

**Issue** The fixed-versus-adjusted contrast is repeatedly announced and then repeated almost unchanged in interpretation and conclusions.

**Required correction** Merge lines 109 and 113. Keep one introductory roadmap. Make the interpretation explain the physical direction and limitations, leaving the conclusion to state the principal result once. Retain the necessary warnings about failed LF diagnostics in figure 6 and exploratory spectrum sampling in figure 15. Those warnings prevent misinterpretation and should not be removed as stylistic repetition.

### R3-m2

**Severity** Minor  
**Axis** Readability and figure interpretation  
**Affected element** Public-facing terminology  
**Evidence pointer** Main line 28; body lines 26, 32-36, 166 and 180-193; figure 17.

**Issue** The abstract's “newer fixed-spectrum summaries” and “reported centre” describe provenance rather than a physical result. MS, ETA_STAR and T3 coexist with mathematical names.

**Required correction** Use physical symbols consistently in prose and reserve storage identifiers for the reproducibility table. Define eta-star immediately as the logarithm of star-formation efficiency per timescale. Explain each comparison by its physical intervention before naming its source product.

## Technical failings that need to be addressed before the case is established

R3-M1 requires verified comparison targets and interpretable sampling summaries. R3-M2 requires separating weak direct sensitivity from compensating galaxy changes. Broad free-spectrum histograms cannot settle identifiability, as the manuscript itself recognizes.

## Assessment against Nature-style criteria

**Originality** The spectrum variation within a flexible galaxy prescription offers a potentially useful contribution. Priority beyond the supplied comparison to Park et al. is not established here.

**Scientific importance** The question matters, but the present result remains predominantly sensitivity and preliminary fitting evidence.

**Interdisciplinary readership** The light-versus-escaped-photon distinction is accessible and valuable. Its quantitative implications need clearer presentation.

**Technical soundness** Stored data support several literal descriptions, with substantial unresolved inference and provenance limits.

**Readability for nonspecialists** The opening is effective; subsequent archive chronology and identifiers interrupt the physical argument.

## Recommendation posture

Substantial revision is warranted before presenting the observation comparisons as established physical information. The narrower sensitivity results provide a credible foundation, but do not yet demonstrate how much matter-spectrum information survives galaxy freedom.


# Cross-review synthesis (post-review; not shown to reviewers)

## Overall assessment

The physics manuscript has a recognizable and useful main line. It asks whether changes in the small-scale matter spectrum can be distinguished from galaxy astrophysics, and follows fixed-galaxy histories, fitted luminosity functions and joint samples. The first two stages already contain interpretable numerical results. The central inferential and compensation conclusions remain incomplete.

Its strongest current claim is conditional sensitivity plus fit compatibility. It is not yet a measured loss of cosmological information or a reliable spectrum constraint. The manuscript largely respects that distinction, but some positive observation-combination statements are more prominent than their source verification warrants.

## Consensus strengths

All three reports identify a clear physical question, useful galaxy equations and well-calibrated treatment of exploratory spectrum samples. They recognize fixed-sigma8 normalization and the numerical PL distinction as important. Actual LF candidate curves demonstrate compatibility for some spectra. Excluding the unverified PL coeval curve and treating the saturated atlas history separately are appropriate source-based choices.

## Consensus blocking concerns

**S1. Headline inference comparisons lack verified common targets and stable sample interpretation.** R1-M1, R2-M2 and R3-M1 independently identify this issue and all mark it blocking for the positive observation-information interpretation.

The T3 escape-normalization spread changes from 0.867 to 0.562 to 0.386, but two source chains and their coordinate orders remain unverified. Executed priors, fixed settings and diagnostics are not established across the comparison. The 100k fixed-spectrum table has undefined centres/± spreads and omits t_star. These are valid records of reported numbers; they are not yet controlled evidence attributing changes to observations or spectrum alone.

A repair begins with configurations, raw coordinate verification and explicit selection, using material already delivered where available. It does not require assuming that every comparison must be rerun.

## Other consensus major concerns

**S2. Similar refitted LFs do not distinguish compensation from weak direct sensitivity.** R1-M2, R2-M1/R2-M3 and R3-M2 independently raise this gap. At larger kp, a good fit may arise because galaxy adjustments absorb a spectrum change or because the observations scarcely respond to that part of the spectrum. Comparing different fixed histories and independently fitted products does not quantify their separate roles.

The needed bridge is an observable comparison before and after galaxy adjustment under matched spectra, prescriptions and numerical definitions. LF, xHI and tau predictions from those same selected fits would show what adjustment restores and what residual survives. A directly supported alternative is to narrow the paper to conditional history sensitivity and LF compatibility.

S2 is not unanimously marked blocking. R2 makes the incomplete central answer a blocking significance concern; R1 and R3 treat the compensation mechanism as a nonblocking major limitation on a narrower paper. This distinction is retained.

**S3. Physical interpretation is weakened by chronology and product mixing.** R3-M3 gives this Major, Blocking No status. Related readability concerns appear as Minor in R1-m1 and R2-m1. Sections move through T3, training size, a 7D product and old 6D/8D samples, so the reader must reconstruct which change is physical and which is a change of calculation. A single experiment map would help more than repeated caveats.

## Where emphasis differs across reviewers

R1 separately raises approximation fidelity as a nonblocking major concern (R1-M3). It asks whether the representative-history approximation and changed predictor affect the specific physical comparisons. This should be addressed by the methods validation relevant to those runs, rather than expanded into a second emulator-development paper.

R2 gives greatest weight to a completed identifiability result and a precise scientific increment relative to adopting the Park prescription. R3 emphasizes the missing mass-scale/observable explanation and the narrative burden of archive chronology. None independently establishes external priority or a final editorial decision.

## Defensive writing and repeated explanation

The issue is repetition of source status, rather than excessive caution in every sentence. Preserve the uncertainty where it affects a plot or claim, and recover space for physical explanation.

| Source location in body_numbered.txt | Problem | Editorial direction |
|---|---|---|
| 109 and 113 | The fixed-galaxy setup is announced twice consecutively | Merge into one opening |
| 3, 7, 9 and 235–245 | The fixed-versus-adjusted contrast is repeatedly restated | Keep the question and roadmap once; use interpretation for the direction and scope of the physical result |
| 166–230 | T3, “larger history model”, 7D and old 6D/8D products organize results by release history | Organize by physical intervention and give one compact experiment map |
| 175, 193–209 and 331–398 | Source selections, model chronology and run definitions recur | Consolidate into one provenance/selection table and appendices |
| Figure captions and 228–245 | Exploratory status is repeatedly explained | Retain a concise warning by the relevant display and a single interpretation boundary |
| Abstract “newer fixed-spectrum summaries” and “reported centre” | Administrative status obscures physical meaning | Use a defined statistic and a physical explanation after its source is verified |

Retain the failed-grid-diagnostic qualification beside fig:lf-grid (main Figure 3), the exploratory label beside fig:kpms-focus (main Figure 6), and the distinction between a stored maximum and statistical evidence. Retain the unverified PL and saturated-history boundaries. Removing them would overstate the available result.

## Forensic consistency findings

The independent post-review audit supports the literal arithmetic behind the main descriptions.

- F_ESC10 has the largest reported T3 spread decrease, 55.41% from LF-only to the joint summary. This percentage describes sample standard deviations, not a validated gain in information.
- The T3 joint row reproduces from the archived ext2 chain to below 1e-12 in all six means and population standard deviations. The other two T3 rows remain unreproduced from raw samples here.
- The large-kp LF stored maxima are close to the PL value. All 25 diagnostic flags remain false. Candidate-fit existence and posterior convergence are different questions.
- The second fixed-prescription xHI(8) values reproduce, as do the reported fixed-spectrum centre differences.

No contradiction was found in these checked main numerical statements. The unresolved issues are estimands, target parity, convergence and the physical bridge between experiments.

Two editorial qualifications apply to the frozen reports. Newer 100k fixed-spectrum raw chains are already available, although v0.20 does not integrate them; their selection and configuration still need reconciliation. R3's legacy figure-number references should be read using the corrected labels above. FORENSIC_AUDIT.md records both clarifications without changing the reports.

## Minor-revision checklist

- State the specific physical increment relative to the adopted Park model and data rationale (R1-m2).
- Consolidate repeated setup, status and chronology passages (R1-m1, R2-m1, R3-m1).
- Use physical symbols in the narrative and storage identifiers in the reproducibility record; define eta_star as log star-formation efficiency per timescale (R3-m2).
- Explain the observed star-formation-parameter direction using the stated galaxy equations, while reserving unmeasured halo-abundance compensation for evidence rather than assertion (R3-M2, R3-m2).
- Recompute the old 100k summaries from existing raw files before treating their undefined ± notation as an interval or requesting replacement chains (audit clarification).

## Broad-interest / significance readout

The connection between small-scale structure, galaxy light and escaped ionizing photons has potential interest beyond the immediate numerical application. The present evidence supports a useful field-specific sensitivity and fitting study. A demonstrated physical discrimination result would strengthen its significance. The source packet does not establish outstanding importance, external novelty or editorial suitability for Nature as a settled conclusion.

## Most important issues to resolve

Keep the physics paper centered on spectrum sensitivity and galaxy response. First verify the comparison targets and replace old undefined sample summaries with reproducible statistics from available files. Then build the matched observable bridge that distinguishes compensation from weak direct sensitivity. Sampling and approximation validation should enter only to the extent needed for the physical claims, with detailed methods supplied by the companion BTemu article.

# Risk / unsupported claims

- Near-PL stored LF maxima do not establish cosmological indistinguishability, a Bayes factor or a quantified compensation mechanism.
- T3 sample-spread reduction cannot yet be read as a validated gain from adding observations without target and sampling parity.
- The old free-spectrum chain does not distinguish broad true posteriors from incomplete exploration.
- Fixed-sigma8 matter-spectrum changes should not be interpreted as fixed-amplitude primordial changes.
- Neither nominal PL labels nor seed labels replace actual branch and realization verification.
- A physical model-specific bias cannot be isolated by the paired mock summaries when nominal BT recovery is itself unstable.
- Missing materials must be distinguished from newer raw files already delivered. Later data are not silently treated as v0.20 evidence.
