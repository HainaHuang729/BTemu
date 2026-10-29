"""Figure for T2b: matched (fixed-astro) BT vs PL reionization histories."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/results/paper_materials_20261029")
data = json.loads((OUT / "tables/t2b_matched_kpms_histories.json").read_text())
res = data["results"]
ref = res["PL reference"]
zr = np.asarray(ref["z"])
xr = np.asarray(ref["xHI"])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
a1.plot(zr, xr, "k-", lw=2, label="PL (KP=MS=0)")
for label, d in res.items():
    if label == "PL reference":
        continue
    a1.plot(d["z"], d["xHI"], "--", lw=1.3, label=label)
a1.set_xlabel("z"); a1.set_ylabel(r"$\bar{x}_{\mathrm{HI}}$")
a1.set_title("matched astrophysics, varying KP/MS", fontsize=9)
a1.legend(fontsize=7); a1.grid(alpha=0.25)

for label, d in res.items():
    if label == "PL reference":
        continue
    dz = np.asarray(d["z"]); dx = np.asarray(d["xHI"]) - np.interp(dz, zr, xr)
    a2.plot(dz, dx, lw=1.3, label=label)
a2.axhline(0, color="k", lw=0.8)
a2.set_xlabel("z"); a2.set_ylabel(r"$\bar{x}_{\mathrm{HI}}^{\rm BT} - \bar{x}_{\mathrm{HI}}^{\rm PL}$")
a2.set_title("difference with respect to the PL reference", fontsize=9)
a2.legend(fontsize=7); a2.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "figures/fig_t2b_matched_kpms.png", dpi=180)
plt.close(fig)

rows = ["| case | KP | MS | xHI(z=8) | xHI(6.5) | xHI(5.9) |", "|---|---:|---:|---:|---:|---:|"]
for label, d in res.items():
    zz = np.asarray(d["z"]); xh = np.asarray(d["xHI"])
    rows.append(f"| {label} | {d['kp']:g} | {d['ms']:g} | {np.interp(8.0, zz, xh):.4f} | "
                f"{np.interp(6.5, zz, xh):.4f} | {np.interp(5.9, zz, xh):.4f} |")
(OUT / "tables/t2b_matched_kpms.md").write_text("\n".join(rows) + "\n")
print("\n".join(rows))
