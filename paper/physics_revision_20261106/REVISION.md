# Physics manuscript v0.21 revision

## Request

Revise the 21cmTB physics manuscript after its independent v0.20 review. Improve its physical line, use available raw samples, consolidate defensive writing and distinguish established results from missing evidence. The methods manuscript and its default entry point remain unchanged.

## Main changes

The argument now separates conditional spectrum sensitivity, the existence of compatible LF candidate fits, and the galaxy prescription selected by fixed-spectrum samples. A compact experiment map states the fixed/varied coordinates, observables, numerical products and interpretation. No matched compensation or observational-information result is inferred from juxtaposing different experiments.

Five fixed-spectrum six-coordinate files, including PL and kp20, are recomputed with the established finite-log-probability selection. The table now gives explicit medians for all six coordinates, including t_star. Full source precision, means, population standard deviations and marginal quantiles are recorded in FIXED_CHAIN_SUMMARIES.csv. The old undefined centre±spread table remains in the frozen v0.20 source record.

The main text interprets eta_star and alpha_star through the existing capped galaxy equations. The new dimensionless SFR factor describes an active halo at fixed mass and redshift. Its BT/PL ratios compare separate marginal medians; they are not paired simulation effects, emissivity ratios or measurements of halo-abundance compensation. The numerical derivation matches the unchanged source arrays already analyzed for the methods revision.

The current 100k-model 600-step spectrum sample marginals replace the old 5,568-step figure in the main text. The older figures and moment tables remain in the earlier-chain appendix. Neither predictor's samples are combined with another predictor's samples.

The T3 comparison is removed from the abstract and conclusions and consolidated in the appendix with its raw-file and coordinate limitations. Its checked summary arithmetic is retained. The second fixed-galaxy coeval product is supplementary, with the unverified PL entry still excluded.

## Defensive prose and repetition

The consecutive fixed-galaxy setup statements were merged. Main results use physical interventions rather than upload dates or training-size section titles. Shared inference limits appear once in the interpretation section. Figure-specific qualifications remain beside the affected plots. Historical source chronology stays in the provenance record and frozen pre-revision source. The discussion explains the completed result and the unresolved compensation alternative rather than repeating the result roadmap.

## Selected before and after

Before, the fixed-spectrum section used undefined reported centres and omitted t_star. After, the table identifies recomputed medians, includes all six coordinates, and points to counts and quantile definitions.

Before, the physical conclusion promoted the T3 spread contraction despite unverified common targets. After, the conclusion centers on conditional sensitivity, LF compatibility and the sample-implied active-halo SFR response. T3 is a supporting appendix record.

Before, successive sections combined distinct numerical products as a compensation narrative. After, the experiment map and interpretation distinguish weak direct sensitivity from compensation, pending matched observable predictions.

## Review status

The writing items and undefined fixed-summary estimand are addressed. Common executed priors, independent sampling, likelihood fidelity and the matched physical bridge remain open where required by the intended claim. EVIDENCE_GAPS.md records them separately. No source array, original equation, figure asset, historical reviewer report or citation key is modified. Old tables replaced or moved are preserved in body_v020.tex and the source receipts.

## Entry points

paper/physics_main.tex is the active independent physics entry point, version v0.21. paper/physics_archive_20261106.tex now explicitly points to the frozen v0.20 body so that its old version label remains faithful. The project default paper/main.tex continues to be BTemu v0.10.

recompute.py is archived here as a source receipt. Its executable repository location is BTemu/paper/physics_revision_20261106/recompute.py, where its relative raw-data paths resolve. The manuscript source package is independently compilable without running that analysis.
