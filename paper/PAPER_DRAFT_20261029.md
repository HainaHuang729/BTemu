# Blue-tilted primordial power spectra and the 21-cm reionization history: model fits and an emulator for inference

*Draft v0.2, 2026-10-29, HNHuang. Updated against the 15:45 production snapshot and the published chain files.*

## Abstract (draft)

Small-scale primordial power affects the formation of the ionizing sources that drive reionization. We study this dependence with a BT-modified 21cmFAST model that adds a break scale k_p and spectral slope MS to an eight-parameter astrophysical prescription. The inference uses ultraviolet luminosity functions, Planck optical depth, and the McGreer neutral-fraction constraint. We train BTemu, a residual multilayer perceptron, to predict the volume-averaged neutral-fraction history at 32 redshifts. For the reported 65,536-history training milestone, the median absolute trajectory RMSE is 0.0010; the 90th-percentile absolute errors in x_HI(5.9) and optical depth are 0.0079 and 0.00070. PL fits to BT mock catalogues have reported minimum χ² values of 150.9–432.2, compared with 42.4 for the PL control; the mock-fit chains have not passed all configured diagnostics. The published six- and eight-dimensional chain segments contain 5,000 and 5,568 stored steps, respectively. Their descriptive split statistics exceed 1.05 for at least one coordinate in each run. The current chain diagnostics leave the joint parameter constraints unresolved.

## 1. Introduction

- 21-cm observations probe the ionization and thermal state of the IGM.
- Bayesian inference with repeated simulations is computationally expensive. Existing approaches include 21cmGEM and 21cmEMU.
- Here we extend the selected 21cmFAST model across k_p and MS and develop a history emulator for that model.
- We examine the dependence of reionization observables on the spectrum, PL fits to BT mock catalogues, and the agreement between exact and emulated calculations under the sampled configurations.

## 2. Model

- The astrophysical prescription follows Park et al. (2019), with F_STAR10, ALPHA_STAR, F_ESC10, ALPHA_ESC, M_TURN, t_STAR, L_X, and NU_X_THRESH.
- The spectrum extension uses k_p ∈ [1,30] h Mpc⁻¹ and MS ∈ [0.5,4], implemented through the `btps` cosmology with kp_1_mpc = k_p·h. The full design includes slopes below the reference n_s; “blue-tilted” describes its enhanced-slope subset.
- Simulation settings: BOX_LEN = 250 Mpc, HII_DIM = 128, DIM = 512, with spin-temperature fluctuations enabled.
- BTemu predicts 32 volume-averaged coeval neutral fractions: integer redshifts z = 5–35 plus z = 5.9. These are coeval volume averages.

## 3. Data and likelihood

- UV luminosity functions: 34 HST+Donnan points selected with M_UV > −20.
- The history-dependent likelihood combines Planck optical depth and the McGreer neutral-fraction constraint at z = 5.9; the LF term retains its exact provider.
- The six-dimensional history run samples ETA_STAR, t_STAR, ALPHA_STAR, M_TURN, F_ESC10, and ALPHA_ESC. The reported configuration fixes L_X = 40.5 and NU_X_THRESH = 500 eV. Its fixed k_p/MS values require confirmation from the run configuration.
- The published eight-dimensional chain files sample the same six astrophysical coordinates plus KP_h_Mpc and MS. They are distinct from the older eight-astrophysical-parameter, X-ray-free exact calculation described in the original notes.
- The original notes specify uniform priors in the sampling coordinates, with KP ∈ [1,30] and MS ∈ [0.5,4]. The complete inference priors and fixed settings must be matched to the run configurations. The exported chain files record parameter names but do not contain the full prior configuration.

## 4. BTemu

- Input: ten physical parameters; output: the 32-node volume-averaged x_HI(z) history.
- Architecture: residual MLP, width 256, hidden width 512, four blocks, with five training seeds and physical-x_HI MSE loss.
- At the 2026-10-29 15:45 production snapshot, 83,756 training histories and 2,752 validation histories were admitted, toward targets of 100,000 and 10,000. These production counts are separate from the 65,536-history checkpoint evaluated below.
- For each history, trajectory RMSE is the square root of the mean squared x_HI difference over the 32 redshift nodes. Quantiles are taken across histories. RMSE = 0.0010 is a dimensionless absolute neutral-fraction error.
- Reported accuracy for the 65k model, worst seed: trajectory RMSE median 0.0010 and q95 0.0101; absolute x_HI(5.9) error q90 0.0079; absolute τ error q90 0.00070; history log-likelihood error q90 2.44. These values retain the milestone report’s worst-seed aggregation.
- The reported learning curve gives log-likelihood-error q90 values of 7.45 at 16k and 2.44 at 65k. The validation membership for the two milestones is absent from the current export.

## 5. Results

### 5.1 PL fits to BT mock catalogues

Ten mock cases were fitted with the PL model (`experiments/bt_mock_pl_bias`). The PL control has a reported χ²_min = 42.4 and parameter-centre differences of 0.006–0.06σ. Selected BT cases are listed below. The normalized shifts and width ratios retain the definitions in the original mock-fit summary; their numerical estimates come from chains whose combined diagnostic requirements have not all passed.

| mock | χ²_min | reported parameter-centre difference | largest reported width ratio |
|---|---:|---|---:|
| bt_kp10_ms2 | 150.9 | < 0.04σ | L_X 9.9 |
| bt_kp10_ms3 | 432.2 | ALPHA_STAR 1.94σ, F_STAR10 1.29σ | NU_X_THRESH 31.9 |
| bt_kp10_ms4 | 248.7 | F_STAR10 2.03σ, M_TURN 1.54σ | NU_X_THRESH 14.7 |

[Figure 1](figures/fig1_bt_bias.png) displays the reported shift and width-ratio matrices. The mock-fit summary records `all_combined_chain_gates_passed = false` and supplies an aggregate diagnostic status. The table describes the current fits; their normalized offsets have not been established as bias significance.

### 5.2 Published six- and eight-dimensional chain samples

The available six-dimensional files contain 1,000 + 2,000 + 2,000 stored steps with 32 walkers. The eight-dimensional files contain 2,000 + 3,568 steps with 32 walkers. The extension named `chain8_ext_3399.h5` actually stores 3,568 finite steps, so the total is 5,568, superseding the earlier 5,400-step summary.

We concatenate the segments in the order listed in the source snapshot and retain the last chronological half of each sequence, with all walkers and no thinning. The six-dimensional summary uses 2,500 retained steps, or 80,000 correlated rows; the eight-dimensional summary uses 2,784 steps, or 89,088 correlated rows. Complete duplicated suffix/prefix blocks were checked and none were found. The files lack iteration offsets, RNG state, and complete target settings, so continuation and target identity still require the original run records.

The resulting six-dimensional means and sample standard deviations are:

| Parameter | Sample mean | Sample standard deviation |
|---|---:|---:|
| ETA_STAR | -0.9411 | 0.0435 |
| t_STAR | 0.5163 | 0.2703 |
| ALPHA_STAR | 0.5721 | 0.0823 |
| M_TURN | 8.9676 | 0.4147 |
| F_ESC10 | -1.0837 | 0.3959 |
| ALPHA_ESC | 0.0626 | 0.3617 |

These are descriptive sample moments. The ordinary split variance-ratio statistic, formed by splitting each walker sequence in half, spans 1.0340–1.0535 for the six-dimensional sequence and 1.1136–1.5125 for the eight-dimensional sequence. In the former, t_STAR has the largest value, 1.0535. The walkers form interacting ensembles; this monitor is distinct from independent-chain, rank-normalized/folded R̂, and no ESS assessment is supplied here. Convergence acceptance is not established for either run.

The eight-dimensional parameter names are ETA_STAR, t_STAR, ALPHA_STAR, M_TURN, F_ESC10, ALPHA_ESC, KP_h_Mpc, and MS. The eight-dimensional files contain no emulator-identification attributes. Their predictor and fixed X-ray settings require the run receipt before these samples can be compared quantitatively with the six-dimensional emulator run.

### 5.3 Earlier exact/emulator comparison

The earlier six-parameter comparison reports centre differences below 0.25σ and width ratios of 0.85–1.09 against a 200-step exact chain. The original draft describes a 1,000-step emulator comparison, while the availability notes also identify a 2,000-step extension. Those offsets belong to the earlier comparison and have not been recomputed for the current 5,000-step sequence. The exact reference chain, retained intervals, predictor, priors, and diagnostics are required to determine posterior agreement.

The earlier notes also report an X-ray-free, eight-astrophysical-parameter exact run with L_X ≈ 40.0, NU_X_THRESH ≈ 762, and astrophysical centre differences of 0.02σ. That exact run is separate from the published six-astrophysical-plus-KP/MS chain. Its reported values are retained in the result record, pending the corresponding chain artifact and configuration.

## 6. Discussion and limitations

- The completed IC sensitivity test contains 128 parameter families with eight initial-condition realizations per family. The across-family q90 of the within-family sample standard deviation of the history log likelihood is 0.9480653. This statistic measures realization scatter. It is distinct from the q90 emulator prediction error of 2.44 and does not supply a universal lower bound on emulator error.
- In that sensitivity test, the q90 absolute difference between log likelihood evaluated at the finite-IC mean history and the logarithm of the finite-IC mean likelihood is 0.308246. Mean-history accuracy and initial-condition-marginalized inference therefore require separate validation.
- The accuracy measurements apply to 32-node neutral-fraction histories, derived optical depth, and the corresponding history likelihood over the reported validation sample.
- The current KP/MS chain does not satisfy a convergence acceptance. The earlier report gives a sampling acceptance fraction of 0.24; the current export supplies no corresponding effective-sample-size assessment.
- The initial-condition seed is not an emulator input. Validation against individual random-IC histories includes realization scatter as well as prediction error; validation of a mean-history target needs repeated-IC reference calculations.

## 7. Conclusions

BTemu predicts volume-averaged neutral-fraction histories for the selected spectrum and astrophysical model. At the reported 65,536-history milestone, the median absolute trajectory RMSE is 0.0010, with q90 absolute errors of 0.0079 in x_HI(5.9) and 0.00070 in τ. PL fits to BT mocks show differences in fitted distributions and fit quality in the available samples. The published six- and eight-dimensional sequences now contain 5,000 and 5,568 stored steps, respectively; their diagnostics and the exact-reference comparison do not yet establish converged joint constraints. Further inference comparisons require matched configurations and adequate effective sample sizes.

## Data and code availability

- Emulator package: `project_bt_history_emulator` (`bt-history-emulator` 0.1.0); exported implementation in this repository.
- Reported accuracy checkpoint: `artifacts/random_ic_development_65536_20261026` (external milestone artifact). Frozen metrics, validation membership, and seed-level reports are needed to reproduce its aggregate errors.
- Published chain segments: `chains/chain6_1000.h5`, `chains/chain6_ext_2000.h5`, `chains/chain6_ext2_2000.h5`, `chains/chain8_2000.h5`, and `chains/chain8_ext_3399.h5`.
- Recompute the descriptive chain statistics with `python paper/validate_draft_snapshot.py` from the repository root. Shapes, parameter order, file digests, retained intervals, and statistic definitions are recorded in [DRAFT_SNAPSHOT_VALIDATION_20261029.json](DRAFT_SNAPSHOT_VALIDATION_20261029.json).
- Exact six-dimensional reference: `handoffs/fixed_joint6_lx500_20261022/output/chain.h5` (external, 200-step comparison).
- BT mock fits: `experiments/bt_mock_pl_bias/results/final_summary` (external numerical summary).
- Completed IC sensitivity definition and values: [ic_audit_completion.md](../docs/ic_audit_completion.md).
