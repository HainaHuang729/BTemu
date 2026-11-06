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
