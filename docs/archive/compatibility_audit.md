> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Compatibility audit

Material Passport: academic-research-suite / experiment-agent; local source audit and software verification; no sealed labels accessed.

The user approved one shared ten-input emulator: canonical eight astrophysical inputs, KP_h_Mpc in [1,30], MS in [0.5,4]. Its output is the 32-node volume mean of xH_box. Existing inference views remain fixed KP10/MS2.5 (8 sampled coordinates) and KP1/MS in [0.5,2] (9). The sampler's ETA_STAR is converted using the original function; M_TURN prior is [8,11], inherited from the actual merged configuration, not the old [8,10] base document.

Sources are immutable external files under project_mcmc. Contracts fingerprint the actual samplers, parameterization, LF provider, original likelihood, inherited scientific contracts, observations and native/source files. The uniform 31-node tau grid is distinct from the history grid, which additionally contains 5.9.

Conflicts resolved by actual TS-on sampler semantics:

- Old parent documentation says 84 nodes and ensemble mean. Current entry points use 32 nodes and fixed seed 725213656658.
- Old exact_coeval_history_provider disables TS and enables linear density, and clips labels. It is unsuitable for this task; the new adapter reproduces the TS-on sampler's coeval call and float64 volume mean.
- Fixed-view KP is 10 h/Mpc; continuous-MS-view KP is 1 h/Mpc. KP is converted to native 1/Mpc by multiplying hlittle=0.678.
- Original audit native SHA256 starts 80b30c5c; staged strict TS repair starts 3211a662. Regression gate reports passed (57 successful); release.json still says STAGED_PENDING_REGRESSION. Native selection remains a recorded pending user decision; candidate contracts currently pin repaired native and cannot mix original labels.
- Current execution host cannot import repaired native: GLIBC_2.29 missing. No replacement library, recompilation or alternative tau integral was used.

Local ps.c POWER_SPECTRUM=6 uses k^ns below KP and k^MS KP^(ns-MS) above KP, with ns=0.968 and Eisenstein-Hu transfer function. User confirmed the strict no-break limit is MS=0.968. POWER_SPECTRUM=0 is the explicit standard PL branch. Numerical equivalence of the two branches remains unmeasured here.

Existing PL EMU probe (runs/pl_emu_probe_20260928/job_2159467/run_report.json) reports SIGMA_8=.82, h=.6774, OMm=.3075, OMb=.0486, ns=.97; target is .815, .678, .308, .0484, .968. PL flags include PHOTON_CONS=True; local default is False. Its minimum redshift is 5.90059, which does not cover z=5 or even exact 5.9. PL M_TURN limit 10 does not cover target upper limit 11. IC-target equivalence is not established; PL additionally exposes X_RAY_SPEC_INDEX. Baseline compatibility FAILS. No extrapolation, baseline inference, PL ground-truth substitution or residual benefit claim is made.

Existing optimization evidence was read, not rerun. The 20260920 cache harness uses keys only by function/redshift, safe only inside its deliberately fixed configuration; it is not a general complete-dependency cache. Its cache_fields comparison reports tiny nonzero history differences and local warm speedup about 1.072. This does not qualify a cache across KP/MS. The new exact adapter uses regenerate=True/write=False and does not reuse any fields across parameters. No full-chain profiling was repeated.
