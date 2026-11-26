"""Generate Fig. 6 (PSX-emu 300-pt independent audit), Fig. 7 (t_STAR Plan A RBF patch & 4-way PL diagnostics), and Fig. 8 (ARD-GP lightcone patches & 3-way 8D Stretch+GMM chains)."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator
import numpy as np

from style_prd import (
    AMBER,
    DOUBLE_COL_MM,
    GRID_FAINT,
    INK,
    MM_TO_IN,
    NAVY,
    SLATE,
    SPINE,
    TEAL_SLATE,
    apply_prd_style,
    export_prd_figure,
    format_box_axes,
    panel_header,
)

BASE = Path("/Users/amadeus/Documents/ChatGPT/论文")
OUT_DIR = BASE / "output/btemu_methods_manuscript/figures"
AUDIT_JSON = BASE / "output/vps_progress_20261126/reports/joint_independent_audit_report.json"
STAGE2_JSON = BASE / "output/vps_progress_20261126/tstar_local_correction_20261120/results/b_validation_pslf_report.json"
FOURWAY_JSON = BASE / "output/vps_progress_20261126/fourway_diagnostic_figures/report.json"
ARCHIVE_DIR = BASE / "output/ps_models_and_chains_20261126"
KP10_GMM_JSON = ARCHIVE_DIR / "reports/converged_kp10_gmm_report.json"
BT3_GMM_JSON = ARCHIVE_DIR / "reports/bt_kp3_ms2p0_report.json"
ABLATION_JSON = ARCHIVE_DIR / "reports/tstar_ablation_report.json"


def draw_fig6_psx_independent_audit() -> dict[str, str]:
    """Fig. 6 (168 mm): Split-contamination audit & 300-pt zero-overlap PSX-emu evaluation."""
    audit = json.loads(AUDIT_JSON.read_text())
    a_l10 = audit["audit_A_val64_split"]["emu_joint_l10"]
    a_v1 = audit["audit_A_val64_split"]["psx_emu_v1_8seed"]
    b_l10 = audit["audit_B_independent_300"]["models"]["emu_joint_l10"]
    b_v1 = audit["audit_B_independent_300"]["models"]["psx_emu_v1_8seed"]
    b_ic = audit["audit_B_independent_300"]["noise_floor_2ic_halfdiff"]

    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 79.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1, 2,
        left=0.145, right=0.985, top=0.815, bottom=0.155,
        wspace=0.46,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    # Panel (a): PS rmse_log10 across split val_64 vs independent 300-pt strata
    strata = [
        ("val64 overlap (54)", a_l10["overlap_54"]["ps"]["rmse_log10"], a_v1["overlap_54"]["ps"]["rmse_log10"], None),
        ("val64 disjoint (10)", a_l10["non_overlap_10"]["ps"]["rmse_log10"], a_v1["non_overlap_10"]["ps"]["rmse_log10"], None),
        ("Indep. 300 (all)", b_l10["all_300"]["ps"]["rmse_log10"], b_v1["all_300"]["ps"]["rmse_log10"], b_ic["all_300"]["ps"]["rmse_log10_halfdiff"]),
        ("LF draws (100)", b_l10["by_group"]["LF_draws"]["ps"]["rmse_log10"], b_v1["by_group"]["LF_draws"]["ps"]["rmse_log10"], b_ic["by_group"]["LF_draws"]["ps"]["rmse_log10_halfdiff"]),
        ("Selected active (100)", b_l10["by_group"]["selected_active"]["ps"]["rmse_log10"], b_v1["by_group"]["selected_active"]["ps"]["rmse_log10"], b_ic["by_group"]["selected_active"]["ps"]["rmse_log10_halfdiff"]),
        ("Prior edges 8D (100)", b_l10["by_group"]["prior_edges_8D"]["ps"]["rmse_log10"], b_v1["by_group"]["prior_edges_8D"]["ps"]["rmse_log10"], b_ic["by_group"]["prior_edges_8D"]["ps"]["rmse_log10_halfdiff"]),
    ]

    ax_a.axhspan(-0.5, 1.5, color="#f4f6f8", lw=0, zorder=0.5)
    ax_a.axhline(1.5, color="#cfd6dd", ls="-", lw=0.75, zorder=1.0)
    y_a = np.arange(len(strata), dtype=float)
    for y, (_, v3, v8, vic) in zip(y_a, strata):
        lo = vic if vic is not None else min(v3, v8)
        hi = max(v3, v8)
        ax_a.plot([lo, hi], [y, y], color="#b8c1c8", lw=1.1, zorder=2.0)
        if vic is not None:
            ax_a.plot(vic, y, marker="o", ms=4.3, mfc="white", mec=INK, mew=1.0, ls="none", zorder=3.5)
        ax_a.plot(v3, y, marker="s", ms=4.2, mfc=AMBER, mec="white", mew=0.55, ls="none", zorder=4.0)
        ax_a.plot(v8, y, marker="D", ms=4.2, mfc=NAVY, mec="white", mew=0.55, ls="none", zorder=4.5)

    ax_a.set(
        xlim=(0.015, 0.080),
        ylim=(-0.55, len(strata) - 0.45),
        xticks=[0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        yticks=y_a,
        yticklabels=[s[0] for s in strata],
    )
    ax_a.invert_yaxis()
    ax_a.xaxis.grid(True, color=GRID_FAINT, lw=0.55, zorder=0)
    ax_a.set_xlabel(r"PS $\log_{10}(\Delta^2_{21}+0.01)$ RMSE (dex)", labelpad=3)
    panel_header(ax_a, "(a)", "Split vs. 300-pt audit")
    format_box_axes(ax_a, top_ticks=True, right_ticks=True, minor_x=False, minor_y=False, tick_size=7.2)

    # Panel (b): Multi-metric relative / Planck-normalized errors (%) on Indep. 300
    metrics = [
        (r"PS $>1\,\mathrm{mK}^2$ med", 100 * b_l10["all_300"]["ps"]["gt_1mK2"]["rel_med"], 100 * b_v1["all_300"]["ps"]["gt_1mK2"]["rel_med"], 100 * b_ic["all_300"]["ps"]["gt_1mK2"]["rel_med"]),
        (r"PS $>1\,\mathrm{mK}^2$ $p_{90}$", 100 * b_l10["all_300"]["ps"]["gt_1mK2"]["rel_p90"], 100 * b_v1["all_300"]["ps"]["gt_1mK2"]["rel_p90"], 100 * b_ic["all_300"]["ps"]["gt_1mK2"]["rel_p90"]),
        (r"PS $>10\,\mathrm{mK}^2$ med", 100 * b_l10["all_300"]["ps"]["gt_10mK2"]["rel_med"], 100 * b_v1["all_300"]["ps"]["gt_10mK2"]["rel_med"], 100 * b_ic["all_300"]["ps"]["gt_10mK2"]["rel_med"]),
        (r"PS $>10\,\mathrm{mK}^2$ $p_{90}$", 100 * b_l10["all_300"]["ps"]["gt_10mK2"]["rel_p90"], 100 * b_v1["all_300"]["ps"]["gt_10mK2"]["rel_p90"], 100 * b_ic["all_300"]["ps"]["gt_10mK2"]["rel_p90"]),
        (r"$\tau_e$ RMSE / $\sigma_{\rm Planck}$", 100 * b_l10["all_300"]["tau_e"]["rmse_over_planck_sigma"], 100 * b_v1["all_300"]["tau_e"]["rmse_over_planck_sigma"], 100 * b_ic["all_300"]["tau_e"]["rmse_over_planck_sigma"]),
        (r"$\tau_e$ $p_{90}$ / $\sigma_{\rm Planck}$", 100 * b_l10["all_300"]["tau_e"]["abs_p90_over_planck_sigma"], 100 * b_v1["all_300"]["tau_e"]["abs_p90_over_planck_sigma"], 100 * b_ic["all_300"]["tau_e"]["abs_p90_over_planck_sigma"]),
    ]

    ax_b.axhline(3.5, color="#cfd6dd", ls="-", lw=0.75, zorder=1.0)
    y_b = np.arange(len(metrics), dtype=float)
    for y, (_, v3, v8, vic) in zip(y_b, metrics):
        ax_b.plot([vic, v3], [y, y], color="#b8c1c8", lw=1.1, zorder=2.0)
        ax_b.plot(vic, y, marker="o", ms=4.3, mfc="white", mec=INK, mew=1.0, ls="none", zorder=3.5)
        ax_b.plot(v3, y, marker="s", ms=4.2, mfc=AMBER, mec="white", mew=0.55, ls="none", zorder=4.0)
        ax_b.plot(v8, y, marker="D", ms=4.2, mfc=NAVY, mec="white", mew=0.55, ls="none", zorder=4.5)

    ax_b.set(
        xlim=(0.0, 12.2),
        ylim=(-0.55, len(metrics) - 0.45),
        xticks=[0, 2, 4, 6, 8, 10, 12],
        yticks=y_b,
        yticklabels=[m[0] for m in metrics],
    )
    ax_b.invert_yaxis()
    ax_b.xaxis.grid(True, color=GRID_FAINT, lw=0.55, zorder=0)
    ax_b.set_xlabel("Normalized error on 300 indep. points (%)", labelpad=3)
    panel_header(ax_b, "(b)", r"Joint PS + $\tau_e$ accuracy")
    format_box_axes(ax_b, top_ticks=True, right_ticks=True, minor_x=False, minor_y=False, tick_size=7.2)

    fig.legend(
        handles=[
            Line2D([], [], ls="none", marker="D", ms=4.4, mfc=NAVY, mec="white", mew=0.55, label="PSX-emu v1.0 (8-seed)"),
            Line2D([], [], ls="none", marker="s", ms=4.4, mfc=AMBER, mec="white", mew=0.55, label="emu_joint_l10 (3-seed)"),
            Line2D([], [], ls="none", marker="o", ms=4.4, mfc="white", mec=INK, mew=1.0, label="2-IC half-diff floor"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.56, 0.985),
        ncol=3,
        fontsize=7.6,
        columnspacing=1.5,
        handletextpad=0.35,
    )

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig6_psx_independent_audit",
        alignment_kwargs={"axes": [ax_a, ax_b]},
    )


def draw_fig7_tstar_local_correction() -> dict[str, str]:
    """Fig. 7 (168 mm): Plan A localized RBF residual patch & t_STAR posterior recovery."""
    st2 = json.loads(STAGE2_JSON.read_text())
    fw = json.loads(FOURWAY_JSON.read_text())

    # Exact Stage 1-3 before/after metrics (verified from LOCAL_CORRECTION_B_VALIDATION,
    # b_validation_pslf_report.json, and LOCAL_CORRECTION_A_PLAN_PSLF_VALIDATION_20261121.md)
    # Four groups on x-axis: Truth L2 p90, Held L2 p90, Truth t* L3, Held med t* L3
    # Grouped bars / paired dumbbells for Stage 2 (24pt PS+LF) and Stage 3 (64pt Plan A PS+LF)
    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 79.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1, 2,
        left=0.140, right=0.985, top=0.815, bottom=0.155,
        wspace=0.52,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    # Panel (a): L2 & t_STAR Fisher L3 drop across Stage 1, Stage 2, Stage 3
    rows_a = [
        (r"Stg 1: truth $L_2$", 0.7608, 0.0406),
        (r"Stg 1: held $L_2$", 0.7829, 0.1126),
        (r"Stg 2: held $t_\star\ L_3$", 0.922, 0.225),
        (r"Stg 3: truth $L_2$", 0.7796, 0.0622),
        (r"Stg 3: held $L_2$", 0.7924, 0.0671),
        (r"Stg 3: truth $t_\star\ L_3$", 0.971, 0.106),
        (r"Stg 3: held $t_\star\ L_3$", 0.973, 0.052),
    ]
    ax_a.axvline(0.10, color=TEAL_SLATE, ls=":", lw=1.05, zorder=1.5)
    ax_a.axhspan(2.5, 6.5, color="#f4f6f8", lw=0, zorder=0.5)
    ax_a.axhline(2.5, color="#cfd6dd", ls="-", lw=0.75, zorder=1.0)
    y_a = np.arange(len(rows_a), dtype=float)
    for y, (_, v_bef, v_aft) in zip(y_a, rows_a):
        ax_a.plot([v_aft, v_bef], [y, y], color=SPINE, lw=1.05, zorder=2.5)
        ax_a.plot(v_bef, y, marker="o", ms=4.5, mfc="white", mec=AMBER, mew=1.05, ls="none", zorder=3.8)
        ax_a.plot(v_aft, y, marker="D", ms=4.0, mfc=NAVY, mec="white", mew=0.5, ls="none", zorder=4.4)

    ax_a.set_xscale("log")
    ax_a.set(
        xlim=(0.028, 1.45),
        ylim=(-0.55, len(rows_a) - 0.45),
        yticks=y_a,
        yticklabels=[r[0] for r in rows_a],
    )
    ax_a.invert_yaxis()
    ax_a.xaxis.set_major_locator(FixedLocator([0.03, 0.1, 0.3, 1.0]))
    ax_a.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:g}"))
    ax_a.set_xlabel(r"Normalized residual metric ($L_2$ $p_{90}$ or $L_3$)", labelpad=3)
    panel_header(ax_a, "(a)", "RBF patch residual reduction")
    format_box_axes(ax_a, top_ticks=True, right_ticks=True, minor_x=True, minor_y=False, tick_size=7.2)

    # Panel (b): t_STAR posterior recovery (16-50-84%) vs truth = 0.500
    # 4-way PL quantiles: t_STAR is col 3 for LF (4D) / LF+xHI+tau (6D), and col 5 for 21cm PS (8D) / PS+LF (8D)
    fw_specs = [
        ("PL diag: LF", 3),
        (r"PL diag: LF+$\tau$+$x_{\rm HI}$", 3),
        ("PL diag: 21cm PS", 5),
        ("PL diag: 21cm PS+LF", 5),
    ]
    fw_rows = []
    for (name, tidx), s in zip(fw_specs, fw["sets"]):
        qs = s["quantiles"]
        fw_rows.append((name, float(qs[0][tidx]), float(qs[1][tidx]), float(qs[2][tidx]), SLATE))

    st2_t = st2["mcmc_pslf_against_native_truth"]["params"]["t_STAR"]
    b16, b50, b84 = st2_t["before_q16_50_84"]
    a16, a50, a84 = st2_t["after_q16_50_84"]
    rows_b = fw_rows + [
        ("Stg 2: base PS+LF", b16, b50, b84, AMBER),
        ("Stg 2: RBF PS+LF", a16, a50, a84, TEAL_SLATE),
        ("Stg 3: Plan A PS+LF", 0.1772, 0.4942, 0.8393, NAVY),
    ]

    ax_b.axvline(0.500, color=INK, ls="--", lw=1.0, zorder=2.0)
    ax_b.axhspan(3.5, 6.5, color="#f4f6f8", lw=0, zorder=0.5)
    ax_b.axhline(3.5, color="#cfd6dd", ls="-", lw=0.75, zorder=1.0)
    y_b = np.arange(len(rows_b), dtype=float)
    for y, (_, q16, q50, q84, col) in zip(y_b, rows_b):
        ax_b.plot([q16, q84], [y, y], color=col, lw=1.6, zorder=3.2)
        ax_b.plot(q50, y, marker="D" if col == NAVY else "o", ms=4.4 if col == NAVY else 4.0,
                  mfc=col, mec="white", mew=0.55, ls="none", zorder=4.4)
    # Mark Stage 3 unfrozen baseline bias median (0.6326) openly on row 6 for exact before->after arrow
    ax_b.plot(0.6326, 6.0, marker="s", ms=4.3, mfc="white", mec=AMBER, mew=1.05, ls="none", zorder=4.8)

    ax_b.set(
        xlim=(0.05, 0.98),
        ylim=(-0.55, len(rows_b) - 0.45),
        xticks=[0.1, 0.3, 0.5, 0.7, 0.9],
        yticks=y_b,
        yticklabels=[r[0] for r in rows_b],
    )
    ax_b.invert_yaxis()
    ax_b.set_xlabel(r"Recovered $t_\star$ (median, 68% CI)", labelpad=3)
    panel_header(ax_b, "(b)", r"$t_\star$ truth = $0.500$ recovery")
    format_box_axes(ax_b, top_ticks=True, right_ticks=True, minor_x=False, minor_y=False, tick_size=7.2)

    fig.legend(
        handles=[
            Line2D([], [], ls="none", marker="o", ms=4.4, mfc="white", mec=AMBER, mew=1.05, label="Frozen base (before patch)"),
            Line2D([], [], ls="none", marker="D", ms=4.1, mfc=NAVY, mec="white", mew=0.55, label="After Plan A RBF patch"),
            Line2D([], [], color=TEAL_SLATE, ls=":", lw=1.1, label=r"Target floor ($0.10$)"),
            Line2D([], [], ls="--", color=INK, lw=1.0, label=r"Truth $t_\star=0.500$"),
            Line2D([], [], ls="none", marker="s", ms=4.2, mfc="white", mec=AMBER, mew=1.0, label=r"Stg 3 base med ($0.633$)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.54, 0.990),
        ncol=3,
        fontsize=7.2,
        columnspacing=1.15,
        handletextpad=0.35,
        labelspacing=0.22,
    )

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig7_tstar_local_correction",
        alignment_kwargs={"axes": [ax_a, ax_b]},
    )


def draw_fig8_ard_gp_and_threeway_gmm() -> dict[str, str]:
    """Fig. 8 (168 mm): Four ARD-GP local patches and three-way 8D Stretch+GMM posterior accuracy."""
    kp10 = json.loads(KP10_GMM_JSON.read_text())
    bt3_rep = json.loads(BT3_GMM_JSON.read_text())
    ablation = json.loads(ABLATION_JSON.read_text())

    # Panel (a) metrics from archived JSON reports & README provenance:
    # PL coeval (0.7924 -> 0.0608), PL lightcone (from tstar_ablation_report.json),
    # BT10 lightcone (1.2988 -> 0.0278 held; 1.2005 -> 0.0124 truth),
    # BT3 lightcone (from bt_kp3_ms2p0_report.json).
    pl_lc = ablation["lc_ard_global_fit"]
    bt3_fit = bt3_rep["bt3_fit"]
    rows_a = [
        ("PL (10, 0.968) coeval [held]", 0.7924, 0.0608),
        ("PL (10, 0.968) LC [held]", float(pl_lc["heldout_L2_p90_before"]), float(pl_lc["heldout_L2_p90_after"])),
        ("BT (10, 2.5) LC [held]", 1.2988, 0.0278),
        ("BT (10, 2.5) LC [truth]", 1.2005, 0.0124),
        ("BT (3, 2.0) LC [held]", float(bt3_fit["heldout_16_L2_p90_before"]), float(bt3_fit["heldout_16_L2_p90_after"])),
        ("BT (3, 2.0) LC [truth]", float(bt3_fit["truth_bt3_L2_p90_before"]), float(bt3_fit["truth_bt3_L2_p90_after"])),
    ]

    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 81.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1,
        2,
        figure=fig,
        left=0.195,
        right=0.982,
        top=0.795,
        bottom=0.145,
        wspace=0.40,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    ax_a.axvline(0.10, color=TEAL_SLATE, ls=":", lw=1.05, zorder=1.5)
    ax_a.axhspan(1.5, 5.5, color="#f4f6f8", lw=0, zorder=0.5)
    ax_a.axhline(1.5, color="#cfd6dd", ls="-", lw=0.75, zorder=1.0)
    y_a = np.arange(len(rows_a), dtype=float)
    for y, (_, v_bef, v_aft) in zip(y_a, rows_a):
        ax_a.plot([v_aft, v_bef], [y, y], color=SPINE, lw=1.05, zorder=2.5)
        ax_a.plot(v_bef, y, marker="o", ms=4.4, mfc="white", mec=AMBER, mew=1.05, ls="none", zorder=3.8)
        ax_a.plot(v_aft, y, marker="D", ms=4.0, mfc=NAVY, mec="white", mew=0.5, ls="none", zorder=4.4)

    ax_a.set_xscale("log")
    ax_a.set(
        xlim=(0.008, 6.2),
        ylim=(-0.55, len(rows_a) - 0.45),
        yticks=y_a,
        yticklabels=[r[0] for r in rows_a],
    )
    ax_a.invert_yaxis()
    ax_a.xaxis.set_major_locator(FixedLocator([0.01, 0.1, 1.0]))
    ax_a.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:g}"))
    ax_a.set_xlabel(r"Normalized residual $L_2\ p_{90}$ (64 train / 16 held)", labelpad=3)
    panel_header(ax_a, "(a)", "Matern-5/2 ARD-GP local patches")
    format_box_axes(ax_a, top_ticks=True, right_ticks=True, minor_x=True, minor_y=False, tick_size=7.2)

    # Panel (b): Standardized parameter recovery (q - truth)/halfwidth for the 3 Stretch+GMM chains
    param_specs = [
        ("F_STAR10", r"$f_{\star,10}$"),
        ("ALPHA_STAR", r"$\alpha_\star$"),
        ("F_ESC10", r"$f_{\mathrm{esc},10}$"),
        ("ALPHA_ESC", r"$\alpha_{\mathrm{esc}}$"),
        ("M_TURN", r"$M_{\mathrm{turn}}$"),
        ("t_STAR", r"$t_\star$"),
        ("L_X", r"$L_X$"),
        ("NU_X_THRESH", r"$E_0$"),
    ]
    chains = [
        ("PL (10, 0.968)", kp10["pl_kp10_ms0p968_8seed"]["params"], NAVY, "D", -0.22),
        ("BT (10, 2.5)", kp10["bt_kp10_ms2p5"]["params"], AMBER, "o", 0.0),
        ("BT (3, 2.0)", bt3_rep["bt_kp3_ms2p0"]["params"], TEAL_SLATE, "s", 0.22),
    ]

    ax_b.axvspan(-1.0, 1.0, color="#eef2f6", lw=0, zorder=0.4)
    ax_b.axvline(0.0, color=INK, ls="--", lw=1.0, zorder=1.6)
    y_b = np.arange(len(param_specs), dtype=float)
    for y in y_b[:-1]:
        ax_b.axhline(y + 0.5, color="#e6ebf0", lw=0.6, zorder=0.8)

    for _, pdict, col, mk, dy in chains:
        for idx, (pkey, _) in enumerate(param_specs):
            pv = pdict[pkey]
            truth = float(pv["truth"])
            hw = float(pv["halfwidth"])
            q16, q50, q84 = [float(v) for v in pv["q16_50_84"]]
            z16, z50, z84 = (q16 - truth) / hw, (q50 - truth) / hw, (q84 - truth) / hw
            yc = idx + dy
            ax_b.plot([z16, z84], [yc, yc], color=col, lw=1.25, zorder=3.1)
            ax_b.plot(z50, yc, marker=mk, ms=3.5, mfc=col, mec="white", mew=0.45, ls="none", zorder=4.2)

    ax_b.set(
        xlim=(-1.95, 2.85),
        ylim=(-0.55, len(param_specs) - 0.45),
        xticks=[-1, 0, 1, 2],
        yticks=y_b,
        yticklabels=[lbl for _, lbl in param_specs],
    )
    ax_b.invert_yaxis()
    ax_b.set_xlabel(r"Standardized offset $(q - \theta_{\mathrm{truth}})/\sigma_{68}$", labelpad=3)
    panel_header(ax_b, "(b)", "3-way 8D Stretch+GMM chains (230.4k)")
    format_box_axes(ax_b, top_ticks=True, right_ticks=True, minor_x=False, minor_y=False, tick_size=7.2)

    fig.legend(
        handles=[
            Line2D([], [], ls="none", marker="o", ms=4.3, mfc="white", mec=AMBER, mew=1.05, label="Frozen base (before ARD-GP)"),
            Line2D([], [], ls="none", marker="D", ms=4.0, mfc=NAVY, mec="white", mew=0.55, label="After ARD-GP patch"),
            Line2D([], [], color=TEAL_SLATE, ls=":", lw=1.1, label=r"Target floor ($0.10$)"),
            Line2D([], [], ls="-", marker="D", ms=3.6, color=NAVY, label=r"PL $(10,0.968)$ ($\hat{R}=1.007$)"),
            Line2D([], [], ls="-", marker="o", ms=3.6, color=AMBER, label=r"BT $(10,2.5)$ ($\hat{R}=1.011$)"),
            Line2D([], [], ls="-", marker="s", ms=3.5, color=TEAL_SLATE, label=r"BT $(3,2.0)$ ($\hat{R}=1.005$)"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.54, 0.992),
        ncol=3,
        fontsize=7.0,
        columnspacing=1.05,
        handletextpad=0.35,
        labelspacing=0.22,
    )

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig8_ard_gp_and_threeway_gmm",
        alignment_kwargs={"axes": [ax_a, ax_b]},
    )


def main() -> None:
    apply_prd_style()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    res = {
        "fig6_psx_independent_audit": draw_fig6_psx_independent_audit(),
        "fig7_tstar_local_correction": draw_fig7_tstar_local_correction(),
        "fig8_ard_gp_and_threeway_gmm": draw_fig8_ard_gp_and_threeway_gmm(),
    }
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
