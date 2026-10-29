# paper_materials status — 2026-10-29

T0 (inventory)      : complete — `material_inventory.json`, `run_configuration_table.csv`
T1 (method/params)  : partial — parameter/prior table produced (`tables/parameter_prior_table.csv`); narrative text pending
T2 (BT-PL physics)  : partial — 21cm cache and phase-pair experiments exist, figure not assembled
T3 (obs combos)     : partial — joint chains exist; LF-only reference uses different data vintage
T4 (mock recovery)  : partial — BT-mock-to-PL results exist (gates false); BT-to-BT recovery pending
T5 (independent test): partial — development validation error figure+metrics produced (`figures/fig_t5_dev_validation_errors.png`, `metrics/t5_*.json`); sealed test still missing
T6 (exact-emu)      : partial — 6-D matched comparison done (200 vs 5000 steps), 8-D not converged
T7 (IC conditional) : partial — 128x8 audit exists; conditional-mean comparison not produced
T8 (cost)           : partial — `metrics/t8_cost_table.json` produced (emulator 8e-5 s/sample, exact 416 s/sim)

Missing inputs: 1
- learning_curve_16k: /oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/artifacts/random_ic_development_16k_20261025
