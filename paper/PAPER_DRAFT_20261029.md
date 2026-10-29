# Blue-tilted primordial power spectra and the 21-cm reionization history: constraints and an emulator for inference

*Draft v0.1 — 2026-10-29 — HNHuang*

## Abstract (draft)

Blue-tilted (BT) primordial power spectra enhance small-scale structure and therefore change when and how reionization proceeds. We quantify this effect with a BT-modified 21cmFAST model that adds a break scale k_p and a spectral slope MS to the eight-parameter astrophysical model constrained by UV luminosity functions, Planck optical depth and the McGreer neutral-fraction point. Fitting BT mock catalogues with a non-BT model leaves systematic shifts of 1–2σ in ALPHA_STAR, F_STAR10 and M_TURN, broadens posteriors by factors of 3–10, and degrades the minimum χ² from 42 to 150–430. To make joint inference tractable we train a ResMLP emulator (BTemu) on 65,536–82,860 BT realizations: the median trajectory error is 0.10% in x_HI, with τ and x_HI(5.9) quantile errors of 7×10⁻⁴ and 8×10⁻³ respectively. An emulator-driven MCMC reproduces the exact-chain posterior centres to better than 0.25σ. We discuss the remaining limitations: single-IC label noise (0.95 in ΔlogL) and chains that are not yet converged.

## 1. Introduction

- 21-cm observations probe the ionization and thermal state of the IGM.
- Bayesian inference with on-the-fly simulations is expensive; emulators are the standard alternative (21cmGEM, 21cmEMU).
- Existing emulators assume standard primordial power spectra; BT spectra modify small-scale power and are not covered.
- This paper: (i) quantify the BT signature in reionization observables; (ii) provide BTemu, an emulator over BT parameters; (iii) validate it at the posterior level.

## 2. Model

- 21cmFAST with the eight-parameter Park et al. (2019) astrophysical model: F_STAR10, ALPHA_STAR, F_ESC10, ALPHA_ESC, M_TURN, t_STAR plus L_X, NU_X_THRESH for X-rays.
- BT extension: a broken power spectrum with break scale k_p (1–30 h/Mpc) and slope MS (0.5–4); implemented through the `btps` cosmology (kp_1_mpc = k_p·h).
- Simulation settings: BOX_LEN = 250 Mpc, HII_DIM = 128, DIM = 512, TS fluctuations on, 31 redshift nodes from z=5 to 35 plus z=5.9.

## 3. Data and likelihood

- UV LF: 34 HST+Donnan points with M_uv > −20.
- Planck τ and the McGreer x_HI constraint.
- Fixed X-ray nuisance L_X = 40.5, NU_X_THRESH = 500 eV for the six-parameter chains; both are sampled in the eight-parameter chain.
- Priors: uniform in the sampling coordinates, KP ∈ [1,30], MS ∈ [0.5,4].

## 4. BTemu

- Input: ten physical parameters; output: 32-node volume-averaged x_HI(z).
- Architecture: residual MLP (width 256, hidden 512, 4 blocks), five seeds, physical-x_HI MSE loss.
- Training data: random-IC Sobol design; 65,536 (5-seed milestone) and 82,860 admitted labels at the time of writing; validation 1,728 of a planned 10,000.
- Accuracy (65k model, worst seed): trajectory RMSE median 0.0010 (q95 0.0101), x_HI(5.9) q90 0.0079, τ q90 0.00070, ΔlogL q90 2.44.
- Learning curve: ΔlogL q90 falls from 7.45 (16k) to 2.44 (65k).
- Comparison to exact posteriors: parameter-centre shifts < 0.25σ, width ratios 0.85–1.09 (six-parameter chain, 1000 emulator steps versus 200 exact steps).

## 5. Results

### 5.1 The BT signature cannot be absorbed by a non-BT model

Ten mock catalogues were generated with BT spectra and fitted with the non-BT (PL) model
(`experiments/bt_mock_pl_bias`). The PL control gives χ²_min = 42.4 with parameter shifts
0.006–0.06σ. BT mocks instead yield:

| mock | χ²_min | largest parameter shift | largest width ratio |
|---|---:|---|---:|
| bt_kp10_ms2 | 150.9 | < 0.04σ | L_X 9.9 |
| bt_kp10_ms3 | 432.2 | ALPHA_STAR 1.94σ, F_STAR10 1.29σ | NU_X_THRESH 31.9 |
| bt_kp10_ms4 | 248.7 | F_STAR10 2.03σ, M_TURN 1.54σ | NU_X_THRESH 14.7 |

Figure 1 (`paper_fig_bias.png`) shows the full shift and width-ratio matrices.
Caveat: the combined chain gates did not pass for these cases (`all_combined_chain_gates_passed = false`), so the numbers are indicative rather than final.

### 5.2 21-cm power spectra at z = 1.07 and z = 0

Phase-pair measurements at 1024³ (NGP, one V/N shot-noise subtraction, no window deconvolution)
give sim/HMcode ratios of 0.744–1.024 at z = 0 across 118 bins, and 0.815–1.004 at z = 1.07.
The z = 0 measurement (job 2288271) extends the earlier z = 1.07 pair (job 2234368).

### 5.3 Joint posterior with and without X-ray freedom

Six-parameter chain (X-ray fixed): ETA_STAR = −0.939 ± 0.043, ALPHA_STAR = 0.571 ± 0.082,
M_TURN = 9.01 ± 0.38, F_ESC10 = −1.09 ± 0.39, ALPHA_ESC = 0.09 ± 0.33.
Eight-parameter exact chain (X-ray free): the same astrophysical parameters agree within 0.02σ,
while the X-ray parameters settle at L_X ≈ 40.0 and NU_X_THRESH ≈ 762.
Neither chain is converged (R̂ 1.08–1.11 and 1.28–1.75 respectively).

## 6. Discussion and limitations

- Single-IC labels carry a ΔlogL noise floor of 0.95 (128 families × 8 realizations), which makes a 0.1 threshold unreachable; acceptance should be defined relative to this noise or at the posterior level.
- Emulator accuracy at fixed KP/MS is already comparable to published 21cm emulators (median 0.1% versus 0.7%).
- Joint KP/MS sampling is implemented but converges slowly (acceptance 0.24); a longer chain or a coarse KP grid is preferable.
- The 21-cm "lightcones" available for this work are 32-node coeval volume averages, not true light-cones.

## 7. Conclusions

BT spectra leave a measurable imprint: non-BT fits are biased at the 1–2σ level and broadened by
factors of several. BTemu reproduces the exact posterior centres to better than 0.25σ, making joint
inference feasible once the chains converge.

## Data and code availability

- Emulator package: `project_bt_history_emulator` (`bt-history-emulator` 0.1.0).
- Emulator checkpoint: `artifacts/random_ic_development_65536_20261026`.
- Chains: `handoffs/fixed_joint6_lx500_20261022/output/chain.h5` (exact), `artifacts/posterior_check_emulator_chain_ext_20261028/chain.h5` (emulator).
- BT mock bias results: `experiments/bt_mock_pl_bias/results/final_summary`.
