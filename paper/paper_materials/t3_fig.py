"""T3 figure: how each observation tightens the posterior (LF -> +tau -> +xHI)."""
import json
from pathlib import Path

import h5py
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EMU = Path("/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator")
OUT = EMU / "results/paper_materials_20261029"
E = EMU / "artifacts"
runs = [("LF only", f"{E}/obs_combo_lf_20261101/chain.h5", "tab:red"),
        ("LF + tau", f"{E}/obs_combo_lf_tau_20261101/chain.h5", "tab:orange"),
        ("LF + tau + xHI", f"{E}/posterior_check_emulator_chain_ext2_20261029/chain.h5", "tab:blue")]

data = []
for name, path, colour in runs:
    with h5py.File(path, "r", locking=False) as f:
        ch = np.asarray(f["chain"][:], float)
        names = [x.decode() for x in f["parameter_names"][:]]
    b = ch[len(ch) // 2:].reshape(-1, ch.shape[2])
    data.append((name, colour, b.mean(0), b.std(0), names))

fig, axes = plt.subplots(1, len(names), figsize=(3.0 * len(names), 3.4), sharey=False)
for ax, i, k in zip(axes, range(len(names)), names):
    for j, (name, colour, mean, sd, _) in enumerate(data):
        ax.errorbar(j, mean[i], yerr=sd[i], fmt="o", color=colour, capsize=4, ms=5)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([d[0] for d in data], rotation=35, ha="right", fontsize=7)
    ax.set_title(k, fontsize=9)
    ax.grid(alpha=0.25)
fig.suptitle("Posterior tightening as observations are added (fixed KP=10, MS=2.5)", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "figures/fig_t3_obs_combinations.png", dpi=180)
plt.close(fig)

rows = ["| parameter | LF only | LF + tau | LF + tau + xHI |", "|---|---:|---:|---:|"]
for i, k in enumerate(names):
    rows.append(f"| {k} | {data[0][2][i]:+.3f} ± {data[0][3][i]:.3f} | {data[1][2][i]:+.3f} ± {data[1][3][i]:.3f} "
                f"| {data[2][2][i]:+.3f} ± {data[2][3][i]:.3f} |")
(OUT / "tables/t3_obs_combinations.md").write_text("\n".join(rows) + "\n")
(OUT / "metrics/t3_obs_combinations.json").write_text(json.dumps({
    "runs": [{"name": d[0], "mean": dict(zip(names, d[2].tolist())), "std": dict(zip(names, d[3].tolist()))}
             for d in data],
    "note": "emulator chains, 1500-2000 steps, fixed KP=10 MS=2.5, random prior starts, last half used",
}, indent=2) + "\n")
print("\n".join(rows))
