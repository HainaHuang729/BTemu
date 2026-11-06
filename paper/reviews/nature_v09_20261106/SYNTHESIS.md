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
