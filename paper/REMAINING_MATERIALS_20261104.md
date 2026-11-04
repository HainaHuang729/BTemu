# Materials required after the November 4 review

Scope: physics v0.19 and methods v0.7. Existing evidence is listed first so completed exports are not requested again. This is a material and validation inventory, not authorization to launch simulations or sampling.

## P0. Physical spectrum and numerical identity

Available: the exported piecewise matter-spectrum prescription, sigma8 normalization convention, units, cosmological parameters and fixed-astrophysics history summaries.

Return: the frozen native source/build fingerprint and configuration used by each result; arrays of k and the realized input P_lin(k) for the compared settings; normalization records; and an actual MS=ns comparison against the separate PL branch under matching numerical conditions. Include the halo abundance/collapsed-fraction prescription, source efficiency and UV conversion implementation. A primordial-spectrum interpretation additionally needs its explicit definition and mapping to the simulated matter spectrum. The revised drafts use the phenomenological matter-spectrum framing in the meantime.

Addresses R1-M4, R2-M3 and R3-M3. Terminology is corrected in the manuscripts; executable physical-model verification remains open.

## P0. New-chain records and matching inference

Available: archived 6D/8D HDF5 segments and exact200; the T3 joint ext2 segment and reproduced last-half moments; the three new fixed-spectrum summaries; four new 100k-model corner PNGs at revision e250ae0. The PNG titles give 3000 steps and 32 walkers and show t_STAR. They do not replace raw arrays or retained-selection definitions.

Return: raw new kp10/MS2.5, kp1/MS1.5, kp5/MS1.5 and kp10/free-MS7D chains; the two outstanding T3 files for LF-only and LF+tau; parameter order and fixed values for every run; the exact centre/spread or percentile conventions used by each table/figure; retained step ranges; segment/RNG continuation records; likelihood/data/prior identities; weights and normalizer hashes; and actual tau integration settings. Reconcile the executable z=5--35/31-point convention with the metadata z=5--30/25-point entry. Supply the point-by-point observational publication mapping and LF residual-space/asymmetric-error definition.

For the central information result, provide independent-run diagnostics, autocorrelation-aware ESS, selection stability and prior-to-posterior comparisons under matching targets. Reuse existing runs and diagnostics where appropriate before listing additional computation.

Addresses R1-M1, R1-M4, R2-M2 and R3-M1. Current sample arithmetic is preserved; inference qualification remains open.

## P0. Current 100k-model validation and predictor definition

Available: 100k training / 10k development-split report, five training seeds and aggregate error JSON; the earlier predictor's 512-history truth/prediction NPZ and independently reproduced average/seed metrics.

Return: evaluated sample IDs, truth histories and predictions for each new-model seed and the actual deployed aggregate; weights and normalizer hashes; evaluation code; absolute/signed q90 definitions and aggregation axes; optical-depth postprocessing; and actual evaluated membership/count. Preserve the distinction between the 10000-history split size and the number evaluated. A controlled old/new comparison needs both predictors on the same histories with the same aggregation. Supply an independent final-test record separately from development selection; the old PS phase60 test is not a test of the new history emulator.

Addresses R1-M3 and R2-M4. The old comparison's mixed predictor definitions are corrected; new-model reconstruction and independent coverage remain open.

## P0. Inference target and exact comparison

Available: T7 aggregate summaries for 128 existing eight-IC families; generating statistic definitions; signed target-difference quantiles and a maximum absolute difference; the older exact200 smoke chain and finite T6 calculation.

Return: existing family-level histories and likelihoods, IC seeds, same-point deployed predictions and finite-reference uncertainty. Declare the intended representative-history, conditional-mean-history or IC-marginalized likelihood. Report absolute likelihood errors and their location in parameter space. The older exact200 comparison remains attached to its original predictor. A new-model inference check requires a matching predictor/target and an adequately sampled exact reference.

Addresses R1-M2, R2-M4 and R3-M2. No IC scatter is used as a universal emulator-error floor, and signed quantiles are not substituted for absolute-error quantiles.

## P1. Observable predictions from the current joint samples

Available: existing LF-best displays, 23 archived matched BT/PL LF-best pairs and older joint predictive products. These are not all missing.

Return: LF, xHI(z) and tau predictions with IDs tying them to the same retained samples used for the current information comparison. State retained weights and target identities. This connects changes in galaxy/spectrum coordinates to distinguishable observations.

Addresses R1-M1, R2-M2 and R3-M1.

## P1. PS IC comparison and runtime accounting

Available: reported IC4/IC8 summaries and differing PS estimators; the November 4 runtime ledger plus historical timing exports.

Return: paired spectra under the same estimator, windows, k bins, masks and parameter points, with the relevant seed policy and uncertainty. For the abnormal PS+LF chain, provide prior, LF and PS contributions at the injection and sampled corner together with the theta-to-astro mapping and support checks. Reconcile job/timer scopes for 13.2392 h in the 100k JSON versus 13.5 h in the ledger. The phase60 ledger arithmetic is now corrected from 26 to 262.1375 core-h using the unchanged 943695 core-seconds. A complete-likelihood timing must include LF and tau costs; current snippets do not define a matched end-to-end speedup.

Addresses AUD-04, AUD-05 and the scope of the PS comparison. These remain separate from current history-model validation.

## P2. Distinctive scientific result and positioning

Available: a physically motivated BT extension, spectrum-sensitive histories, galaxy fitting freedom and an established-architecture development predictor.

The remaining result is a controlled statement about which spectral changes can be distinguished after galaxy freedom, or a robust limit on that distinguishability. For a separate methods contribution, provide evidence of the distinctive BT-domain capability and verified likelihood/inference accuracy, with prior-work comparisons on matching observables and error definitions. New architecture labels or a larger training set alone do not establish that advance.

Addresses R2-M1 and the shared significance assessment. Novelty and a completed information result remain open, rather than being marked resolved by prose edits.
