"""Matched BT-PL comparison: fixed astrophysical parameters, vary (KP, MS) only."""
import json, sys, time
from dataclasses import replace
from pathlib import Path

import numpy as np
import h5py

MC = Path("/oss06/data/project/tkcastrosim/HNHuang/project_mcmc")
HAND = MC / "workflows/MCMC/fixed_btps_posterior/handoffs/fixed_joint6_lx500_20261022"
OUT = Path("/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/results/paper_materials_20261029")
sys.path[:0] = [str(MC)]

import importlib.util
spec = importlib.util.spec_from_file_location("fixed6_run", HAND / "run.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

plan = json.loads((HAND / "plan.json").read_text())
base = run.configuration_for(plan, 0)

with h5py.File(HAND / "output/chain.h5", "r", locking=False) as f:
    ch = np.asarray(f["chain"][:], float)
theta = np.median(ch[len(ch) // 2:].reshape(-1, ch.shape[2]), axis=0)
astro = run.astro_from_theta(theta, base)
print("fixed astro:", json.dumps({k: float(v) for k, v in astro.items()}), flush=True)

COMBOS = [(0.0, 0.0, "PL reference"),
          (1.0, 1.5, "BT kp1 ms1.5"),
          (1.0, 2.0, "BT kp1 ms2.0"),
          (10.0, 1.5, "BT kp10 ms1.5"),
          (10.0, 2.0, "BT kp10 ms2.0"),
          (10.0, 3.0, "BT kp10 ms3.0")]

z = np.unique(np.r_[np.linspace(5.0, 35.0, 31), 5.9])
results = {}
from py21cmfast import run_coeval
from workflows.MCMC.fixed_btps_posterior.inference.exact_lf_provider import ExactLuminosityFunctionProvider

for kp, ms, label in COMBOS:
    t0 = time.perf_counter()
    cfg = run.configuration_for(plan, 0)
    if kp > 0 or ms > 0:
        btps = replace(cfg.cosmologies["btps"], kp_h_mpc=float(kp),
                       kp_1_mpc=float(kp) * cfg.cosmologies["btps"].background["hlittle"], ms=float(ms))
        cfg = replace(cfg, cosmologies={**cfg.cosmologies, "btps": btps})
    cfg = replace(cfg, production_authorized=False, cosmological_priors={"MS": (0.5, 4.0)})
    lf = ExactLuminosityFunctionProvider("btps", configuration=cfg)
    user = {**lf.user_params, "N_THREADS": 16}
    cosmo = lf.cosmo_params_for(ms if (kp > 0 or ms > 0) else None)
    flags = {**lf.flag_options, "USE_TS_FLUCT": True}
    coevals = run_coeval(redshift=z.tolist(), user_params=user, cosmo_params=cosmo,
                         astro_params=astro, flag_options=flags,
                         random_seed=plan["initial_condition_seed"],
                         direc=f"/tmp/matched_{label.replace(' ', '_')}", write=False, regenerate=True,
                         cleanup=True, Z_HEAT_MAX=35.0, EVOLVE_DENSITY_LINEARLY=False)
    pairs = sorted((float(c.redshift), float(np.mean(c.xH_box, dtype=np.float64))) for c in coevals)
    zz, xh = np.asarray(pairs, float).T
    results[label] = {"kp": kp, "ms": ms, "z": zz.tolist(), "xHI": xh.tolist(),
                      "seconds": time.perf_counter() - t0}
    print(f"{label}: xHI(z=8)={np.interp(8.0, zz, xh):.4f} xHI(5.9)={np.interp(5.9, zz, xh):.4f} "
          f"({results[label]['seconds']:.0f}s)", flush=True)
    del coevals

(OUT / "tables").mkdir(parents=True, exist_ok=True)
(OUT / "tables" / "t2b_matched_kpms_histories.json").write_text(
    json.dumps({"astro": {k: float(v) for k, v in astro.items()}, "results": results}, indent=2) + "\n")
print("written", OUT / "tables/t2b_matched_kpms_histories.json")
