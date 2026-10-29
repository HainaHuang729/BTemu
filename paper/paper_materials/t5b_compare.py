"""BTemu vs exact 21cmFAST on held-out validation samples (T5b comparison figure)."""
import json, sys
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator")
OUT = ROOT / "results/paper_materials_20261029"
ART = ROOT / "artifacts/random_ic_development_65536_20261026"
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "maintenance/random_ic_development")]

from bt_history.contracts import parameters
from bt_history.transforms import Normalizer
from bt_history.resmlp import ReionizationHistoryEmulator
from loader import load

cfg = json.loads((ROOT / "configs/training.json").read_text())
c, rows, post = load(ART / "snapshot.json")
split = json.loads((ART / "direct_resmlp/split.json").read_text())
val = [r for r in rows if split[r["sample_id"]] == "validation"]
x = np.array([parameters(c, r["physical_parameters"]) for r in val])
y = np.array([r["global_xHI"] for r in val], dtype=np.float64)
_nd = json.loads((ART / "direct_resmlp/normalizer.json").read_text())
norm = Normalizer(_nd["mean"], _nd["scale"])

nets = []
for s in cfg["seeds"]:
    n = ReionizationHistoryEmulator(10, 32, **cfg["architecture"])
    n.load_state_dict(torch.load(ART / f"direct_resmlp/seed_{s}.pt", map_location="cpu"))
    n.eval(); nets.append(n)
tx = torch.tensor(norm.transform(x), dtype=torch.float32)
with torch.no_grad():
    preds = np.stack([n(tx).numpy() for n in nets]).astype(np.float64)
ens = preds.mean(0)
res = ens - y
rmse = np.sqrt((res ** 2).mean(axis=1))
z = np.unique(np.r_[np.linspace(5.0, 35.0, 31), 5.9])

np.savez_compressed(OUT / "tables" / "t5b_validation_predictions.npz",
                    z=z, truth=y, ensemble=ens, seeds=preds, sample_ids=np.array([r["sample_id"] for r in val]))

pick = [int(np.argmin(rmse)), int(np.percentile(rmse, 50) and np.argsort(rmse)[len(rmse) // 2]),
        int(np.argsort(rmse)[-1]), int(np.argsort(rmse)[-3])]
fig = plt.figure(figsize=(12, 7.5))
gs = fig.add_gridspec(2, 4, height_ratios=[1.25, 1])
for i, idx in enumerate(pick[:3]):
    ax = fig.add_subplot(gs[0, i])
    ax.plot(z, y[idx], "k-", lw=1.4, label="21cmFAST")
    ax.plot(z, ens[idx], "C1--", lw=1.4, label="BTemu (5-seed mean)")
    ax.fill_between(z, preds[:, idx].min(0), preds[:, idx].max(0), color="C1", alpha=0.15)
    ax.set_title(f"sample {idx}: RMSE={rmse[idx]:.4f}", fontsize=9)
    ax.set_xlabel("z"); ax.set_ylabel(r"$x_{\mathrm{HI}}$")
    if i == 0:
        ax.legend(fontsize=7)
ax = fig.add_subplot(gs[0, 3])
ax.hist(rmse, bins=30, color="C0", alpha=0.8)
ax.axvline(np.median(rmse), color="k", ls="--", label=f"median={np.median(rmse):.4f}")
ax.set_xlabel("per-sample trajectory RMSE"); ax.set_ylabel("count"); ax.legend(fontsize=7)
ax.set_title("validation RMSE distribution", fontsize=9)

ax = fig.add_subplot(gs[1, :2])
for i in range(len(val)):
    ax.plot(y[i], np.abs(res[i]), ".", ms=1, alpha=0.25, color="C0")
ax.set_xlabel(r"true $x_{\mathrm{HI}}$"); ax.set_ylabel(r"$|x_{\mathrm{HI}}^{\rm pred}-x_{\mathrm{HI}}^{\rm true}|$")
ax.set_yscale("log"); ax.set_title("error vs neutral fraction", fontsize=9)

ax = fig.add_subplot(gs[1, 2:])
med = np.median(np.abs(res), axis=0)
p95 = np.percentile(np.abs(res), 95, axis=0)
ax.plot(z, med, label="median |err|")
ax.plot(z, p95, label="95% |err|")
ax.set_xlabel("z"); ax.set_ylabel("absolute error"); ax.set_yscale("log")
ax.legend(fontsize=7); ax.set_title("error by redshift", fontsize=9)
fig.suptitle("BTemu vs exact 21cmFAST on 512 held-out random-IC validation samples", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "figures" / "fig_t5b_btemu_vs_21cmfast.png", dpi=180)
plt.close(fig)

summary = {
    "n_samples": int(len(val)),
    "trajectory_RMSE_median": float(np.median(rmse)),
    "trajectory_RMSE_mean": float(rmse.mean()),
    "trajectory_RMSE_q95": float(np.percentile(rmse, 95)),
    "trajectory_RMSE_max": float(rmse.max()),
    "max_abs_error_per_sample_q95": float(np.percentile(np.abs(res).max(axis=1), 95)),
    "per_z_median_abs_error_max": float(med.max()),
    "per_z_median_abs_error_at_z": float(z[int(np.argmax(med))]),
    "ensemble_vs_single_seed_median_rmse": {
        "ensemble": float(np.median(rmse)),
        **{f"seed_{s}": float(np.median(np.sqrt(((preds[i] - y) ** 2).mean(axis=1))))
           for i, s in enumerate(cfg["seeds"])},
    },
}
(OUT / "metrics" / "t5b_btemu_vs_21cmfast.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2), flush=True)
