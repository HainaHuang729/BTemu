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
