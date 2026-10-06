# BTemu

A 10D numerical surrogate of the selected BT-modified 21cmFAST forward model: physical parameters → 32-node **volume-averaged global_xHI history**.

**Current status:** exact-data production is active; development models have been trained, but scientific deployment and posterior fidelity have not been accepted.

- [Project progress and measured validation](docs/progress.md)
- [Progress dashboard](https://hainahuang729.github.io/BTemu/)
- [Scientific contract](contracts/science_contract.json)
- [Development comparison procedure](docs/archive/development_comparison_20261005.md)

Eight astrophysical coordinates plus KP_h_Mpc∈[1,30] and MS∈[0.5,4]. Fixed IC requested/effective seed 725213656658; PL limit MS=0.968. Original log10 parameter coordinates are preserved.

The emulator learns the simulator's exact history, including residual neutral hydrogen at z=5. It imposes no additional monotonicity, smoothing, completion-of-reionization or observational adjustment. Tau is derived by original tau_from_history/native compute_tau; LF uses the original exact provider. There is no learned tau head.

Production target: 100000 qualified Train histories and 10000 independent Validation histories. V1 benchmarks are retained. Sealed designs remain isolated. NNERO-style classifier and PCA+MLP are development comparisons; no WDM physics is substituted for BT and no classifier-negative label is deleted.

## Repository contents

src/bt_history contains exact adapters, provenance/QA, transforms, ResMLP, decoders, history provider, metrics and training. maintenance/v2 contains bounded resumable wave production and NNERO-style experiments. maintenance/development_snapshot contains a recovery-aware loader and a frozen-data comparison. contracts and configs record the target and protocols. tests verify software behavior. site contains the aggregate progress dashboard.

Raw labels, native binaries, production receipts, training weights and sealed payloads are external. Public budgets are disabled reference templates. This export does not authorize simulations or provide a portable native build. See docs/progress.md for reproduction boundaries and current measurements; docs/archive preserves historical stage reports.
