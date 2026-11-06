> Historical November 5 outline. The current author-facing main line is `paper/MAINLINE.md`; this file is retained as a dated record.

# BTemu: a history emulator for BT-modified reionization calculations

Working outline reconciled with the November 5 exports. The original upstream skeleton remains in `paper/paper_materials/BTEMU_DRAFT_20261105.md`; the existing methods manuscript supplies the definitions, bibliography and earlier validation. This outline organizes the added evidence rather than replacing that manuscript.

## Abstract

Small-scale matter spectra and galaxy astrophysics both affect the reionization history. BTemu approximates 32-node neutral-fraction histories from ten input coordinates, including the spectrum parameters KP and MS. The current development report describes 100,000 training histories and a 10,000-history validation split, with trajectory-RMSE median 0.000850668 and q95 0.00556364. Uploaded PL and fixed-spectrum BT chains permit direct comparison of six galaxy coordinates, including a new 10,000-step kp20/MS2.5 calculation. These comparisons connect changes in the input spectrum to the galaxy parameters selected by the same reported class of observations. The complete free-spectrum sampling and independent validation define the remaining tests of this application.

## 1. Introduction

Open with the ambiguity between small-scale matter spectra and galaxy astrophysics in reionization calculations. Explain why repeated history calculations are needed to vary both sets of coordinates. Position BTemu through its BT-domain observables and validation, using the existing methods-paper references. The paper's main result should be the accuracy and computational use of the history approximation over this domain.

## 2. Simulations and training data

Use the matter-spectrum definition and normalization already documented in the methods manuscript. List the reported 250 Mpc box, DIM=512, HII_DIM=128 and 32 redshift nodes. Separate the training coordinate F_STAR10 from the inference coordinate ETA_STAR, with the actual conversion. Describe the 100,000/10,000 split, IC policy and the membership of the evaluated validation set. Keep the current history target distinct from the spatial fields needed for a power spectrum.

## 3. Emulator architecture

Describe the existing ResMLP, ten inputs, 32 outputs, five training seeds, normalization and output transformation. Identify the deployed prediction aggregate and its weights. Architecture and training-set size are method definitions; the BT-domain accuracy is the empirical result.

## 4. Training and validation

Present trajectory errors first, then errors in xHI(5.9), optical depth and the history likelihood. The supplied q90 summaries are 0.00457050, 0.000335078 and 1.17734, respectively. Their signed/absolute convention and evaluation membership belong beside the completed validation calculation. The new accuracy PNG can guide figure layout; reconstruct its redshift errors and residual histogram when truth/prediction arrays are exported. Keep the earlier 512-history average/seed calculation separate from the new aggregate report.

## 5. Computational cost

Separate simulation, data generation, training, prediction and complete-likelihood costs. Preserve the source ledger's 416 s median realization time and its separately reported 460 s versus 8e-5 s forward-component example. The approximate 6e6 component ratio is not a measured end-to-end MCMC speed-up. The metric JSON records 47,661.2727 s (13.2392 h); the ledger's 13.5 h and per-seed allocation require their timing scopes. Present the receipts and scopes in one table.

## 6. Applications to galaxy and spectrum parameters

### 6.1. Fixed-spectrum PL/BT comparisons

Use the uploaded PL and kp1/MS1.5, kp5/MS1.5, kp10/MS2.5 and kp20/MS2.5 arrays. The first four calculations contain 3,000 steps and 32 walkers each; kp20 contains 10,000 steps and 32 walkers. Exclude only the supplied rows with nonfinite log probability in the current material comparison, and state any later chronological retention rule separately. Plot each PL/BT pair with the common Park-style coordinates and independent 95% sample-density regions. Give both models' marginal summaries. Use `CHAIN_SUMMARIES_20261105.csv` for recomputed quantities; retain the original reported table as a separate source record.

### 6.2. Free-spectrum sampling

The new JSON describes 16,018 steps and 32 walkers, reporting KP=15.74 with standard deviation 8.118 and MS=2.037 with standard deviation 0.962. Its reported Rhat values include ETA_STAR=1.258, ALPHA_STAR=1.178, M_TURN=1.082 and KP=1.084. Thus 1.084 is the KP entry, while the maximum is 1.258. Use the complete joined arrays, retention rule and diagnostic definition to reproduce the figure before drawing a prior-to-posterior information conclusion. A broad displayed histogram and an incomplete sampling diagnostic do not establish a physical lack of constraints.

## 7. Discussion

Relate history errors to the likelihood quantity used in inference. The existing T7 material describes finite-IC variation and does not establish a universal 0.948 log-likelihood noise floor or the impossibility of achieving an error below 0.1. Likewise, the reported 1.25% IC4/IC8 difference changes the PS estimator and cannot identify IC noise as subdominant by itself. Keep these interpretation points together rather than repeating them throughout the results.

The November 5 PS10D snapshot is a separate production update. It reports 60 NPZ files, approximately 150–200 parameter points, and filtering to KP>=1 and MS>=1.5. These are producer selections and progress counts, not an independently tested emulator or a verified physical validity boundary. The snapshot's 7 batches, approximately 450 cores and 2,000-point queue target are historical job-status reports. Particle radial profiles belong to the nonlinear-structure manuscript.

## 8. Conclusions

Summarize the verified history approximation and the fixed-spectrum sample comparisons. State the independent validation and complete free-spectrum inference tests once, as the next empirical results needed for the same scientific question.

## Appendices and material placement

1. Simulation, spectrum and coordinate definitions.
2. Training/evaluation membership, metric definitions and predictor identity.
3. Uploaded-chain inventory, finite-log-probability selection and numerical summaries.
4. Sampling diagnostics with their exact definitions and selection ranges.
5. Timing receipts and computational scope.

The PS likelihood and 10-D PS emulator remain separate decisions; neither is assumed in the current history-likelihood application. The source inventory's external `artifacts/` paths are tracked as material to export until the corresponding files are available locally.
