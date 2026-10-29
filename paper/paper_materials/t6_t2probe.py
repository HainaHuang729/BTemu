"""T6 matched exact-emulator comparison (5000-step 6D chain) + T2 cache probe for xHI histories."""
import json
from pathlib import Path

import h5py
import numpy as np

BASE = Path("/oss06/data/project/tkcastrosim/HNHuang")
EMU = BASE / "project_bt_history_emulator"
OUT = EMU / "results/paper_materials_20261029"
E = EMU / "artifacts"
EXACT = BASE / "project_mcmc/workflows/MCMC/fixed_btps_posterior/handoffs/fixed_joint6_lx500_20261022/output/chain.h5"

def load(p):
    with h5py.File(p, "r", locking=False) as f:
        return np.asarray(f["chain"][:], float), [x.decode() for x in f["parameter_names"][:]]

def rhat(ch):
    n = ch.shape[0] // 2
    out = []
    for d in range(ch.shape[2]):
        a = np.asarray([ch[:n, :, d].T, ch[n:2 * n, :, d].T])
        W = a.var(axis=2, ddof=1).mean()
        B = n * np.var(a.mean(axis=2), axis=1, ddof=1).mean()
        out.append(np.sqrt(((n - 1) / n * W + B / n) / W))
    return np.array(out)

# ---------- T6 ----------
ex, names = load(EXACT)
parts = [load(E / p)[0] for p in ("posterior_check_emulator_chain_20261027/chain.h5",
                                 "posterior_check_emulator_chain_ext_20261028/chain.h5",
                                 "posterior_check_emulator_chain_ext2_20261029/chain.h5")]
em = np.concatenate(parts)

be = ex[len(ex) // 2:].reshape(-1, ex.shape[2])
bm = em[len(em) // 2:].reshape(-1, em.shape[2])
rows = []
for i, k in enumerate(names):
    m1, s1 = be[:, i].mean(), be[:, i].std()
    m2, s2 = bm[:, i].mean(), bm[:, i].std()
    rows.append({"parameter": k, "exact_mean": float(m1), "exact_std": float(s1),
                 "emulator_mean": float(m2), "emulator_std": float(s2),
                 "shift_sigma": float((m2 - m1) / s1), "width_ratio": float(s2 / s1)})
c1, c2 = np.corrcoef(be.T), np.corrcoef(bm.T)
summary = {"exact_steps": int(ex.shape[0]), "emulator_steps": int(em.shape[0]),
           "exact_Rhat": [float(x) for x in rhat(ex)],
           "emulator_Rhat": [float(x) for x in rhat(em)],
           "parameters": rows,
           "max_abs_shift_sigma": float(max(abs(r["shift_sigma"]) for r in rows)),
           "width_ratio_range": [float(min(r["width_ratio"] for r in rows)),
                                 float(max(r["width_ratio"] for r in rows))],
           "corr_matrix_frobenius_diff": float(np.linalg.norm(c1 - c2)),
           "note": "exact chain 200 steps; emulator 5000 steps (pooled segments, last half used)"}
(OUT / "metrics").mkdir(parents=True, exist_ok=True)
(OUT / "metrics/t6_matched_exact_emulator.json").write_text(json.dumps(summary, indent=2) + "\n")

md = ["| parameter | exact | emulator | shift/sigma | width ratio |", "|---|---:|---:|---:|---:|"]
for r in rows:
    md.append(f"| {r['parameter']} | {r['exact_mean']:.4f} ± {r['exact_std']:.4f} | "
              f"{r['emulator_mean']:.4f} ± {r['emulator_std']:.4f} | {r['shift_sigma']:+.2f} | {r['width_ratio']:.2f} |")
md.append("")
md.append(f"max |shift| = {summary['max_abs_shift_sigma']:.2f} sigma; width ratio range "
          f"{summary['width_ratio_range'][0]:.2f}-{summary['width_ratio_range'][1]:.2f}; "
          f"correlation Frobenius diff = {summary['corr_matrix_frobenius_diff']:.2f}")
(OUT / "tables").mkdir(parents=True, exist_ok=True)
(OUT / "tables" / "t6_matched_exact_emulator.md").write_text("\n".join(md) + "\n")
print("T6 done:", json.dumps({k: summary[k] for k in ("max_abs_shift_sigma", "width_ratio_range", "corr_matrix_frobenius_diff")}))

# ---------- T2 probe ----------
cache = BASE / "project_mcmc/data/21cm_cache"
probe = {"dirs": [], "datasets": []}
for d in sorted(cache.iterdir()):
    if not d.is_dir():
        continue
    files = sorted(d.glob("*.h5"))
    probe["dirs"].append({"name": d.name, "n_h5": len(files), "example": files[0].name if files else None})
    if files and len(probe["datasets"]) < 3:
        with h5py.File(files[0], "r") as h:
            def walk(g, pre="", depth=0):
                for k in list(g.keys())[:8]:
                    item = g[k]
                    probe["datasets"].append({"file": files[0].name, "path": pre + k,
                                              "shape": list(getattr(item, "shape", [])),
                                              "dtype": str(getattr(item, "dtype", ""))})
                    if isinstance(item, h5py.Group) and depth < 1:
                        walk(item, pre + k + "/", depth + 1)
            walk(h)
(OUT / "metrics" / "t2_cache_probe.json").write_text(json.dumps(probe, indent=2) + "\n")
print("T2 probe dirs:", len(probe["dirs"]), "| datasets:", len(probe["datasets"]))
