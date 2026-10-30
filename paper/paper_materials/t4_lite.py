"""T4 (lite): injected truth vs best-fit parameters under BT and PL models."""
import json
from pathlib import Path

import numpy as np

D = Path("/oss06/data/project/tkcastrosim/HNHuang/project_21cmFast/experiments/bt_matched_recovery/data/paired_pl_bt_mock0_recovery_v1")
OUT = Path("/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/results/paper_materials_20261029")

with np.load(D / "initialization.npz", allow_pickle=True) as z:
    truth = np.asarray(z["truth_theta"], float)
    best_pl = np.asarray(z["global_best_pl"], float)
    best_bt = np.asarray(z["global_best_bt"], float)
    lo = np.asarray(z["lower"], float)
    hi = np.asarray(z["upper"], float)
    names = [str(x) for x in z["parameter_names"]]

span = hi - lo
rows = []
for i, k in enumerate(names):
    rows.append({"parameter": k, "truth": float(truth[i]),
                 "bt_best": float(best_bt[i]), "pl_best": float(best_pl[i]),
                 "bt_offset_prior_span": float((best_bt[i] - truth[i]) / span[i]),
                 "pl_offset_prior_span": float((best_pl[i] - truth[i]) / span[i])})

obs = {
    "source": str(D / "initialization.npz"),
    "dimension": len(names),
    "parameters": rows,
    "max_abs_offset_bt_prior_span": float(max(abs(r["bt_offset_prior_span"]) for r in rows)),
    "max_abs_offset_pl_prior_span": float(max(abs(r["pl_offset_prior_span"]) for r in rows)),
    "note": ("Offsets are expressed as a fraction of the prior span; the npz does not carry a "
             "posterior width or sigma, so binomial significance cannot be quoted from this file alone. "
             "The stored chains (chains/{bt,pl}/ensemble_1/checkpoint.npz) would be needed for sigma."),
}
(OUT / "metrics/t4_paired_recovery.json").write_text(json.dumps(obs, indent=2) + "\n")

md = ["| parameter | truth | BT best | offset/span | PL best | offset/span |",
      "|---|---:|---:|---:|---:|---:|"]
for r in rows:
    md.append(f"| {r['parameter']} | {r['truth']:.3f} | {r['bt_best']:.3f} | {r['bt_offset_prior_span']:+.3f} | "
              f"{r['pl_best']:.3f} | {r['pl_offset_prior_span']:+.3f} |")
(OUT / "tables/t4_paired_recovery.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
print("max |offset|/span  BT:", round(obs["max_abs_offset_bt_prior_span"], 4),
      " PL:", round(obs["max_abs_offset_pl_prior_span"], 4))
