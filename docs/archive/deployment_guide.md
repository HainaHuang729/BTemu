> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Deployment guide

No production-ready weights exist. Default artifact manifest says NO_TRAINED_ACCEPTED_MODEL. Never use synthetic-test checkpoints for science. No production MCMC was started or changed.

From this independent directory:

```bash
source scripts/environment.sh
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
"$BT_HISTORY_PYTHON" -m unittest discover -s tests -v
```

The shell setup does not alter HOME or the original environment. The native import adapter redirects only 21cmFAST's user cache config lookup to an absent temporary file so imports cannot rewrite production configuration. It does not modify physics code. A compatible compute host with the frozen native's GLIBC requirement is required for real compute_tau and simulations.

Contracts/science_contract.json defines the shared 10D model. Contracts/fixed and continuous_ms define original inference views. To use one future accepted shared model, instantiate a HistoryProvider and wrap it in BoundHistoryProvider with the desired view. JointEvaluator(view_contract, bound_provider) calls original LF, original tau_from_history and original likelihood. Its sampler_callback uses the original parameter conversion and prior, but does not start a sampler. An independent script/config must explicitly select it. ExactHistoryAdapter remains available; no original provider is replaced.

Domain check requires exact parameter names, native parameter units, finite values, full configured ranges and an explicit validated coverage predicate. A rectangular prior check alone is insufficient validated coverage. KP input units are h/Mpc. Failure and out-of-coverage exceptions propagate, never silently become prior=-infinity. Optional exact fallback requires a persistent event journal. Model members decode separately; tau is calculated from the physical ensemble mean. Member std is diagnostic, never added to observation errors.

Data generation is explicit and budget-gated:

1. Confirm target native and scientific precision proposals; obtain a compatible execution host.
2. Review configs/proposed_448_point_design.json and configs/budget.json. No budget is authorized yet. Tie any approved budget to the exact design file SHA256 and scientific contract hash.
3. Submit scripts/generate.sbatch only with explicit array bounds and BT_HISTORY_* variables. Every invocation reserves one row exclusively, generates a full TS-on coeval history and original tau, and saves success or failure. No raw cubes are retained. Failure records preserve parameters/reason. Broad failures and their strata must be diagnosed before coverage claims.
4. Construct an explicit development manifest listing immutable JSONL files and SHA256 hashes. Required shape: role=development, science_contract_hash, files=[{path,sha256,role:development}]. Only source-qualified successful records enter training; quarantined records are rejected. Full postprocessing parity is checked on load.
5. Run scripts/development.py validate, then representation if relevant, then train with explicit --contract, --manifest and a fresh --output. Train and validation are grouped by complete physical parameters. scripts/learning_curve.py uses nested train subsets and fixed validation. No test is opened.
6. Prepare a freeze with scripts/final_acceptance.py. It hashes all artifacts and the protocol, and explicitly refuses sealed-test reads this round. Record an authorization before extending/running the sealed-label evaluation. The model must remain frozen during subsequent MCMC.
7. Independent exact posterior comparisons can be summarized by scripts/posterior_check.py. ESS and support overlap are mandatory; its output never declares posterior acceptance solely from importance weights.

No code path creates a learned tau. No PL or PCA artifact is required for the direct model. Native regression and end-to-end LF timing scripts are provided separately; their results must accompany scientific acceptance.

## Dataset pipeline amendment

For the new frozen dataset use `scripts/generate_design.py`, `configs/data_stage_budgets.json` and `scripts/submit_data_array.sh`. The original 448 proposal is preserved, but old `generate_labels.py` now delegates to the single new guarded generator. Do not use the earlier free-form design command to assign validation or test after generation. `load_development` accepts the generated v2 qualified manifest and honors frozen splits. See `docs/data_generation_plan.md`; the earlier manual manifest and retrospective split instructions above apply only to historical software fixtures, not this dataset.
