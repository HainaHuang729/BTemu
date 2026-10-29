"""T2: volume-averaged xHI(z) for PL and BT cache realizations (chunked means)."""
import json
from pathlib import Path

import h5py
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path("/oss06/data/project/tkcastrosim/HNHuang")
CACHE = BASE / "project_mcmc/data/21cm_cache"
OUT = BASE / "project_bt_history_emulator/results/paper_materials_20261029"
(OUT / "figures").mkdir(parents=True, exist_ok=True)
(OUT / "tables").mkdir(parents=True, exist_ok=True)

targets = []
for d in sorted(CACHE.iterdir()):
    if not d.is_dir():
        continue
    files = sorted(d.glob("*.h5"))
    if not files:
        continue
    targets.append((d.name, files[0]))

curves = {}
meta = {}
for name, f in targets:
    try:
        with h5py.File(f, "r") as h:
            z = np.asarray(h["node_redshifts"][:], float)
            ds = h["global_quantities/xH_box"]
            means = []
            for i in range(ds.shape[0]):
                block = ds[i]
                means.append(float(np.asarray(block, dtype=np.float32).mean()))
            ap = {}
            try:
                for k, v in h["astro_params"].attrs.items():
                    ap[k] = float(v) if np.isscalar(v) else str(v)
            except Exception:
                pass
        curves[name] = {"redshifts": z.tolist(), "xHI": means}
        meta[name] = {"file": f.name, "astro": ap, "shape": list(ds.shape)}
        print("read", name, f.name, "nodes:", len(z), flush=True)
    except Exception as exc:
        print("skip", name, type(exc).__name__, str(exc)[:120], flush=True)

(OUT / "tables" / "t2_xhi_histories.json").write_text(json.dumps({"curves": curves, "meta": meta}, indent=2) + "\n")

fig, ax = plt.subplots(figsize=(6.4, 4.2))
for name, c in curves.items():
    z = np.asarray(c["redshifts"]); y = np.asarray(c["xHI"])
    style = "-" if "0.0_MS_0.0" in name or "PL" in name else "--"
    ax.plot(z, y, style, lw=1.4, label=f"{name} ({meta[name]['file'][:22]}…)")
ax.set_xlabel("z"); ax.set_ylabel(r"$\bar{x}_{\mathrm{HI}}$")
ax.set_title("Volume-averaged neutral fraction from 21cmFAST cache", fontsize=10)
ax.legend(fontsize=6, loc="upper left"); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig(OUT / "figures" / "fig_t2_xhi_histories.png", dpi=180)
plt.close(fig)
print("done:", list(curves))
