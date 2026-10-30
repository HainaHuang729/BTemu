"""T4b: posterior widths from stored chain checkpoints, sigma-level recovery."""
import json
from pathlib import Path

import numpy as np

D = Path("/oss06/data/project/tkcastrosim/HNHuang/project_21cmFast/experiments/bt_matched_recovery/data/paired_pl_bt_mock0_recovery_v1")
OUT = Path("/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/results/paper_materials_20261029")

with np.load(D / "initialization.npz", allow_pickle=True) as z:
    truth = np.asarray(z["truth_theta"], float)
    names = [str(x) for x in z["parameter_names"]]

out = {"source": str(D), "models": {}, "checkpoint_structure": {}}
for model in ("bt", "pl"):
    ck = D / "chains" / model / "ensemble_1" / "checkpoint.npz"
    if not ck.exists():
        out["checkpoint_structure"][model] = "missing"
        continue
    with np.load(ck, allow_pickle=True) as z:
        keys = list(z.files)
        arr = [(k, np.asarray(z[k]).shape, str(np.asarray(z[k]).dtype)) for k in keys]
        out["checkpoint_structure"][model] = arr
        cand = None
        for k in ("chain", "samples", "positions", "theta", "p"):
            if k in z.files and np.asarray(z[k]).ndim >= 2:
                cand = (k, np.asarray(z[k], float))
                break
        if cand is None:
            continue
        key, ch = cand
        flat = ch.reshape(-1, ch.shape[-1])
        if flat.shape[1] != len(names):
            out["models"][model] = {"error": f"{key} width {flat.shape[1]} != {len(names)}", "shape": list(ch.shape)}
            continue
        med = np.median(flat, axis=0)
        sd = flat.std(axis=0)
        out["models"][model] = {
            "key": key, "shape": list(ch.shape), "n_samples": int(len(flat)),
            "median": [float(v) for v in med], "std": [float(v) for v in sd],
            "offset_sigma": [float((med[i] - truth[i]) / sd[i]) if sd[i] > 0 else None for i in range(len(names))],
        }

rows = ["| parameter | truth | BT median ± sd | offset/σ | PL median ± sd | offset/σ |",
        "|---|---:|---:|---:|---:|---:|"]
for i, k in enumerate(names):
    bt = out["models"].get("bt", {})
    pl = out["models"].get("pl", {})
    def fmt(m):
        if not m or "median" not in m:
            return "n/a", "n/a"
        return f"{m['median'][i]:.3f} ± {m['std'][i]:.3f}", f"{m['offset_sigma'][i]:+.2f}"
    b1, b2 = fmt(bt)
    p1, p2 = fmt(pl)
    rows.append(f"| {k} | {truth[i]:.3f} | {b1} | {b2} | {p1} | {p2} |")

(OUT / "metrics/t4b_paired_recovery_sigma.json").write_text(json.dumps(out, indent=2) + "\n")
(OUT / "tables/t4b_paired_recovery_sigma.md").write_text("\n".join(rows) + "\n")
print(json.dumps(out["checkpoint_structure"], indent=1)[:1500])
print("\n".join(rows))
