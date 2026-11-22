"""Publication-grade APS/PRD figure generator for the standalone BTemu methods manuscript."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter, ScalarFormatter
import numpy as np

from style_prd import (
    AMBER,
    DOUBLE_COL_MM,
    EXTRAP_TINT,
    GRID_FAINT,
    INK,
    INNER_SPINE,
    MM_TO_IN,
    NAVY,
    PLANCK_BAND,
    SINGLE_COL_MM,
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

T5B_NPZ = BASE / "overleaf-btemu/paper/reproduction/paper_materials/tables/t5b_validation_predictions.npz"
VAL65K_JSON = BASE / "overleaf-btemu/paper/data/btemu_audit/validation_recomputed_20261029.json"
JOINT_VAL_JSON = BASE / "output/park_figure_examples/joint_sampling_validation.json"
T7_JSON = BASE / "BTemu/paper/paper_materials/metrics/t7_ic_sensitivity_report.json"
M100K_JSON = BASE / "BTemu/paper/paper_materials/metrics/100k_comparison_metrics.json"
A3_JSON = BASE / "output/park_figure_examples/review_blockers_20261121/a3_summary.json"
T6_JSON = BASE / "overleaf-btemu/paper/data/btemu_audit/t6_recomputed_20261029.json"

PS_RESIDUALS_NPZ = BASE / "output/ps_emu_20261108/residual_metrics.npz"
PS_REPORT_JSON = BASE / "output/ps_emu_20261108/report.json"
PS_LEARN_JSON = BASE / "output/ps_emu_20261108/learning_report.json"
PS32_REPORT_JSON = BASE / "output/ps_emu_20261108/fullbox_batch/ps32_training_report.json"
PS32_VAL_NPZ = BASE / "output/ps_emu_20261108/fullbox_batch/ps32_validation_predictions.npz"
CMP_833_NPZ = BASE / "output/ps_emu_20261108/estimator/comparison_833.npz"
CMP_199_NPZ = BASE / "output/ps_emu_20261108/estimator/comparison_199.npz"


def _empirical_cdf(vals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xs = np.sort(vals)
    ys = np.arange(1, len(xs) + 1, dtype=float) / float(len(xs))
    return xs, ys


def draw_fig1_history_accuracy() -> dict[str, str]:
    """Fig. 1: History emulator reconstruction, redshift-resolved residual vs IC scatter, seed ensemble CDF, and 65k->100k scaling."""
    t5b = np.load(T5B_NPZ)
    z = np.asarray(t5b["z"], dtype=float)
    truth = np.asarray(t5b["truth"], dtype=float)
    ens = np.asarray(t5b["ensemble"], dtype=float)
    seeds = np.asarray(t5b["seeds"], dtype=float)

    t7 = json.loads(T7_JSON.read_text())
    ic_z = np.asarray(t7["absolute_IC_scatter_by_redshift_mean"], dtype=float)
    jval = json.loads(JOINT_VAL_JSON.read_text())

    diff = ens - truth
    rmses = np.sqrt(np.mean(diff**2, axis=1))
    order = np.argsort(rmses)
    idx_med = int(order[255])  # one-based rank 256
    idx_q95 = int(order[486])  # one-based rank 487

    # Nested 2x2 GridSpec with independent subplots
    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 108.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        2, 2,
        left=0.075, right=0.980, top=0.945, bottom=0.090,
        wspace=0.29, hspace=0.33,
    )

    # Panel (a): Representative histories (z in [5, 22])
    ax_a = fig.add_subplot(gs[0, 0])
    z_mask = z <= 22.0
    zw = z[z_mask]
    s_min_m = np.min(seeds[:, idx_med, z_mask], axis=0)
    s_max_m = np.max(seeds[:, idx_med, z_mask], axis=0)
    s_min_q = np.min(seeds[:, idx_q95, z_mask], axis=0)
    s_max_q = np.max(seeds[:, idx_q95, z_mask], axis=0)

    ax_a.fill_between(zw, s_min_m, s_max_m, color="#c8dce8", alpha=0.55, zorder=1)
    ax_a.fill_between(zw, s_min_q, s_max_q, color="#f2cfb6", alpha=0.55, zorder=1)
    ax_a.plot(zw, truth[idx_med, z_mask], color=NAVY, lw=1.45, ls="-", label=f"Rank 256 truth (RMSE={rmses[idx_med]:.4f})", zorder=3)
    ax_a.plot(zw, ens[idx_med, z_mask], color=NAVY, lw=1.25, ls=(0, (3.0, 1.5)), label="Rank 256 5-seed avg", zorder=4)
    ax_a.plot(zw, truth[idx_q95, z_mask], color=AMBER, lw=1.45, ls="-", label=f"Rank 487 truth (RMSE={rmses[idx_q95]:.4f})", zorder=3)
    ax_a.plot(zw, ens[idx_q95, z_mask], color=AMBER, lw=1.25, ls=(0, (3.0, 1.5)), label="Rank 487 5-seed avg", zorder=4)

    format_box_axes(ax_a, minor_x=False, minor_y=False)
    ax_a.set_xlim(5.0, 22.0)
    ax_a.set_ylim(-0.03, 1.04)
    ax_a.set_xticks([5, 8, 11, 14, 17, 20])
    ax_a.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax_a.set_xlabel("Redshift $z$")
    ax_a.set_ylabel(r"Neutral fraction $x_{\mathrm{HI}}(z)$")
    panel_header(ax_a, "(a)", "65,536-run 512-val trajectories")
    ax_a.legend(loc="center left", bbox_to_anchor=(0.02, 0.48), fontsize=7.2, handlelength=1.7, labelspacing=0.25, borderaxespad=0.2)

    # Panel (b): Redshift-resolved residual & q90(|err|) vs T7 IC scatter
    ax_b = fig.add_subplot(gs[0, 1])
    q90_z = np.quantile(np.abs(diff), 0.90, axis=0) * 1e3
    ic_z_m = ic_z * 1e3
    ax_b.fill_between(zw, -q90_z[z_mask], q90_z[z_mask], color="#dde8f2", edgecolor="none", label=r"512-val $q_{90}(|\Delta x_{\mathrm{HI}}|)$ band", zorder=1)
    ax_b.plot(zw, ic_z_m[z_mask], color=TEAL_SLATE, lw=1.25, ls="-.", label=r"T7 mean IC scatter $\bar{s}_{\mathrm{IC}}(z)$", zorder=2)
    ax_b.plot(zw, -ic_z_m[z_mask], color=TEAL_SLATE, lw=1.25, ls="-.", zorder=2)
    ax_b.axhline(0.0, color=SPINE, lw=0.7, ls=":", zorder=1.5)
    ax_b.plot(zw, diff[idx_med, z_mask] * 1e3, color=NAVY, lw=1.30, ls="-", label="Rank 256 signed residual", zorder=3)
    ax_b.plot(zw, diff[idx_q95, z_mask] * 1e3, color=AMBER, lw=1.25, ls="-", label="Rank 487 signed residual", zorder=3)

    format_box_axes(ax_b, minor_x=False, minor_y=False)
    ax_b.set_xlim(5.0, 22.0)
    ax_b.set_ylim(-19.5, 22.0)
    ax_b.set_xticks([5, 8, 11, 14, 17, 20])
    ax_b.set_yticks([-15, -10, -5, 0, 5, 10, 15, 20])
    ax_b.set_xlabel("Redshift $z$")
    ax_b.set_ylabel(r"Residual $(\widehat{x}_{\mathrm{HI}}-x_{\mathrm{HI}})\times 10^3$")
    panel_header(ax_b, "(b)", "Residuals vs. T7 IC scatter")
    ax_b.legend(loc="upper left", fontsize=7.2, handlelength=1.6, labelspacing=0.22, borderaxespad=0.30)

    # Panel (c): Trajectory RMSE CDF (5 seeds vs ensemble + 100k dev reference)
    ax_c = fig.add_subplot(gs[1, 0])
    seed_labels = [11, 29, 47, 71, 101]
    for s_i, s_val in enumerate(seed_labels):
        s_rmses = np.sqrt(np.mean((seeds[s_i] - truth) ** 2, axis=1))
        xs, ys = _empirical_cdf(s_rmses)
        lbl = "5 individual seeds" if s_i == 0 else None
        ax_c.plot(xs, ys, color=SLATE, lw=0.85, alpha=0.55, label=lbl, zorder=2)

    xs_e, ys_e = _empirical_cdf(rmses)
    ax_c.plot(xs_e, ys_e, color=NAVY, lw=1.75, label="5-seed ensemble (65k)", zorder=4)
    ax_c.axvline(float(np.median(rmses)), color=NAVY, lw=0.85, ls=":", zorder=3)
    ax_c.axvline(float(np.quantile(rmses, 0.95)), color=NAVY, lw=0.85, ls="--", zorder=3)
    # 100k 10k-dev milestones from 100k_comparison_metrics.json
    m100k = json.loads(M100K_JSON.read_text())
    q50_100k = float(m100k["trajectory_RMSE_median"])
    q95_100k = float(m100k["trajectory_RMSE_q95"])
    ax_c.axvline(q50_100k, color=AMBER, lw=1.05, ls=":", label=rf"100k dev $q_{{50}}$ (${q50_100k:.2e}$)", zorder=3.5)
    ax_c.axvline(q95_100k, color=AMBER, lw=1.05, ls="--", label=rf"100k dev $q_{{95}}$ (${q95_100k:.2e}$)", zorder=3.5)
    ax_c.axhline(0.50, color=GRID_FAINT, lw=0.8, zorder=0.5)
    ax_c.axhline(0.95, color=GRID_FAINT, lw=0.8, zorder=0.5)

    ax_c.set_xscale("log")
    format_box_axes(ax_c, minor_x=True, minor_y=False)
    ax_c.set_xlim(1.5e-4, 6.0e-2)
    ax_c.xaxis.set_major_locator(FixedLocator([1e-3, 1e-2]))
    ax_c.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
    ax_c.xaxis.set_minor_formatter(NullFormatter())
    ax_c.set_ylim(0.0, 1.03)
    ax_c.set_yticks([0.0, 0.25, 0.50, 0.75, 0.95])
    ax_c.set_xlabel("Per-history trajectory RMSE")
    ax_c.set_ylabel("Cumulative fraction (512 val)")
    panel_header(ax_c, "(c)", "Ensembling & sample gain")
    leg_c = ax_c.legend(
        loc="lower right",
        fontsize=7.2,
        handlelength=1.5,
        labelspacing=0.22,
        borderaxespad=0.30,
        frameon=True,
        facecolor="white",
        edgecolor="none",
        framealpha=0.92,
    )
    leg_c.set_zorder(6)

    # Panel (d): Paired 65,536 -> 100,000 error reduction on the same 512 validation points
    ax_d = fig.add_subplot(gs[1, 1])
    m65 = jval["validation"]["65536_matched"]
    m100 = jval["validation"]["100000_matched"]
    metrics = [
        (r"$x_{\mathrm{HI}}(5.9)$ RMSE", m65["xhi_5p9"]["rmse"], m100["xhi_5p9"]["rmse"], "{:.4f}"),
        (r"$x_{\mathrm{HI}}(5.9)$ MAE", m65["xhi_5p9"]["mae"], m100["xhi_5p9"]["mae"], "{:.4f}"),
        (r"$\tau$ RMSE ($\times 10^4$)", m65["tau"]["rmse"] * 1e4, m100["tau"]["rmse"] * 1e4, "{:.2f}"),
        (r"$\tau$ $q_{95}$ ($\times 10^4$)", m65["tau"]["q95_abs"] * 1e4, m100["tau"]["q95_abs"] * 1e4, "{:.2f}"),
        (r"$|\Delta \ell_{\mathrm{hist}}|$ $q_{90}$", m65["joint_history_logL"]["q90_abs"], m100["joint_history_logL"]["q90_abs"], "{:.2f}"),
        (r"$|\Delta \ell_{\mathrm{hist}}|$ $q_{95}$", m65["joint_history_logL"]["q95_abs"], m100["joint_history_logL"]["q95_abs"], "{:.2f}"),
    ]
    y_pos = np.arange(len(metrics))[::-1]
    ratios = [v100 / v65 for _, v65, v100, _ in metrics]

    ax_d.axvline(1.0, color=SPINE, lw=0.85, ls="--", zorder=1)
    for y_i, (lbl, v65, v100, fmt), r in zip(y_pos, metrics, ratios):
        ax_d.plot([r, 1.0], [y_i, y_i], color=TEAL_SLATE, lw=1.7, zorder=2)
        ax_d.scatter([1.0], [y_i], s=22, color="white", edgecolor=SLATE, linewidth=0.95, zorder=3)
        ax_d.scatter([r], [y_i], s=28, color=NAVY, edgecolor=NAVY, linewidth=0.6, zorder=4)
        pct = (r - 1.0) * 100.0
        txt = f"{fmt.format(v65)}→{fmt.format(v100)} ({pct:+.1f}%)"
        ax_d.text(r - 0.015, y_i, txt, ha="right", va="center", fontsize=7.2, color=INK, zorder=5)

    format_box_axes(ax_d, minor_x=False, minor_y=False)
    ax_d.set_xlim(0.06, 1.08)
    ax_d.set_ylim(-0.6, len(metrics) - 0.4)
    ax_d.set_yticks(y_pos)
    ax_d.set_yticklabels([m[0] for m in metrics], fontsize=7.3)
    ax_d.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax_d.set_xlabel("Error ratio (100k / 65,536 on paired 512 val)")
    panel_header(ax_d, "(d)", "Paired 65k → 100k improvement")

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig1_history_accuracy",
        alignment_kwargs={"axes": [ax_a, ax_b, ax_c, ax_d]},
    )


def draw_fig3_ic_and_posterior_val() -> dict[str, str]:
    """Fig. 3: Reconciling prior-box T7 IC/emulator likelihood tails with A3 stratified posterior direct simulations & 4-IC checks."""
    t7 = json.loads(T7_JSON.read_text())["family_quantiles"]
    jval = json.loads(JOINT_VAL_JSON.read_text())["validation"]["100000_matched"]["joint_history_logL"]
    a3 = json.loads(A3_JSON.read_text())

    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 80.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1, 2,
        left=0.220, right=0.985, top=0.900, bottom=0.145,
        wspace=0.41,
    )

    # Panel (a): Likelihood discrepancy budget across prior vs posterior
    ax_a = fig.add_subplot(gs[0, 0])
    fq = t7
    rows = [
        ("T7 IC std $s_{\\mathrm{IC}}(\\ell_{\\mathrm{hist}})$", fq["std_logL_joint_history"]["q50"], fq["std_logL_joint_history"]["q90"], fq["std_logL_joint_history"]["max_abs"], AMBER, "Prior box (128 fam.)"),
        # q90(|delta ell|) = 0.308246 is documented in BTemu/docs/ic_audit_completion.md L29 (T7_JSON only retains signed quantiles)
        ("T7 $|\\delta\\ell|$ mean-hist vs IC-avg", None, 0.308246, fq["delta_logL_mean_history_vs_IC_marginal"]["max_abs"], AMBER, None),
        ("100k prior val $|\\Delta \\ell_{\\mathrm{hist}}|$", jval["mae"], jval["q90_abs"], None, SLATE, None),
        ("A3 joint8d post. ($N=28$)", a3["by_group"]["joint8d"]["lnL_reion"]["mae"], a3["by_group"]["joint8d"]["lnL_reion"]["q90_abs"], a3["by_group"]["joint8d"]["lnL_reion"]["max_abs"], NAVY, "Posterior strata"),
        ("A3 fixed-joint post. ($N=20$)", a3["by_group"]["fixed_joint"]["lnL_reion"]["mae"], a3["by_group"]["fixed_joint"]["lnL_reion"]["q90_abs"], a3["by_group"]["fixed_joint"]["lnL_reion"]["max_abs"], NAVY, None),
        ("A3 fixed-LF+$\\tau$ active $\\ell_\\tau$", a3["by_group"]["fixed_lf_tau"]["lnL_tau"]["mae"], a3["by_group"]["fixed_lf_tau"]["lnL_tau"]["q90_abs"], a3["by_group"]["fixed_lf_tau"]["lnL_tau"]["max_abs"], NAVY, None),
        ("A3 4-IC $|\\ell(\\bar{X}_4)-\\ell_{\\mathrm{avg}}|$ ($N=8$)", None, None, max(abs(p["mean_xhi_minus_ic_avg_like_lnL"]) for p in a3["multi_ic_comparisons"]), TEAL_SLATE, None),
    ]
    y_idx = np.arange(len(rows))[::-1]
    ax_a.axhspan(3.6, 6.6, color=EXTRAP_TINT, zorder=0)
    ax_a.axvline(0.05, color=INNER_SPINE, lw=0.85, ls="--", zorder=1)
    ax_a.axvline(1.0, color=INNER_SPINE, lw=0.85, ls=":", zorder=1)

    for yi, (label, v_med, v_q90, v_max, col, _) in zip(y_idx, rows):
        pts = [v for v in (v_med, v_q90, v_max) if v is not None]
        if len(pts) >= 2:
            ax_a.plot([min(pts), max(pts)], [yi, yi], color=col, lw=1.45, alpha=0.8, zorder=2)
        if v_med is not None:
            ax_a.scatter([v_med], [yi], s=22, color=col, marker="o", zorder=3)
        if v_q90 is not None:
            ax_a.scatter([v_q90], [yi], s=26, color=col, marker="s", zorder=3.5)
        if v_max is not None:
            ax_a.scatter([v_max], [yi], s=28, color="white", edgecolor=col, linewidth=1.0, marker="D", zorder=4)
    # Mark unused xHI term for fixed_lf_tau row cleanly
    ax_a.scatter([a3["by_group"]["fixed_lf_tau"]["lnL_reion"]["max_abs"]], [y_idx[5]], s=24, color=SLATE, linewidth=1.0, marker="x", zorder=3.5)

    ax_a.set_xscale("log")
    format_box_axes(ax_a, minor_x=True, minor_y=False)
    ax_a.set_xlim(2.0e-3, 5.0)
    ax_a.xaxis.set_major_locator(FixedLocator([1e-2, 1e-1, 1e0]))
    ax_a.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
    ax_a.xaxis.set_minor_formatter(NullFormatter())
    ax_a.set_ylim(-0.6, len(rows) - 0.35)
    ax_a.set_yticks(y_idx)
    ax_a.set_yticklabels([r[0] for r in rows], fontsize=7.3)
    ax_a.set_xlabel(r"Log-likelihood offset $|\Delta \ell|$ (log scale)")
    panel_header(ax_a, "(a)", "Prior box vs. posterior support")

    leg_a = [
        Line2D([], [], color=NAVY, marker="o", ls="None", ms=4.0, label="MAE / $q_{50}$"),
        Line2D([], [], color=NAVY, marker="s", ls="None", ms=4.2, label="$q_{90}$"),
        Line2D([], [], color=NAVY, mfc="white", mec=NAVY, marker="D", ls="None", ms=4.2, label="Max"),
        Line2D([], [], color=SLATE, marker="x", ls="None", ms=4.2, label="Unused $x_{\\mathrm{HI}}$ tail"),
    ]
    ax_a.legend(handles=leg_a, loc="upper left", fontsize=7.2, handletextpad=0.30, labelspacing=0.20, borderaxespad=0.30)

    # Panel (b): 8 four-IC posterior points comparing IC spread, mean-history, and 100k BTemu
    ax_b = fig.add_subplot(gs[0, 1])
    pts4 = a3["multi_ic_comparisons"]
    y4 = np.arange(len(pts4))[::-1]
    ax_b.axvspan(-0.05, 0.05, color=PLANCK_BAND, alpha=0.65, zorder=0.5)
    ax_b.axvline(0.0, color=SPINE, lw=0.85, ls="--", zorder=1)

    y_labels = []
    for yi, p in zip(y4, pts4):
        l_avg = float(p["sim_lnL_reion_ic_avg_like"])
        l_ics = np.asarray(p["sim_lnL_reion_ics"], dtype=float) - l_avg
        l_mean = float(p["mean_xhi_minus_ic_avg_like_lnL"])
        l_emu = float(p["emu_minus_ic_avg_like_lnL"])
        ax_b.plot([l_ics.min(), l_ics.max()], [yi, yi], color=SLATE, lw=1.2, alpha=0.6, zorder=2)
        ax_b.scatter(l_ics, np.full_like(l_ics, yi, dtype=float), s=15, color=SLATE, alpha=0.85, zorder=3)
        ax_b.scatter([l_mean], [yi], s=26, color=NAVY, marker="s", zorder=4)
        ax_b.scatter([l_emu], [yi], s=28, color=AMBER, marker="D", zorder=4.5)
        grp = "8D" if p["group"] == "joint8d" else "6D"
        stratum = "bulk" if p["stratum"] == "bulk" else ("<0.06" if p["stratum"] == "threshold_below006" else ">0.06")
        y_labels.append(f"pt {p['point_id']} ({grp}, {stratum})")

    format_box_axes(ax_b, minor_x=False, minor_y=False)
    ax_b.set_xlim(-0.072, 0.072)
    ax_b.set_ylim(-0.6, len(pts4) + 1.85)
    ax_b.set_yticks(y4)
    ax_b.set_yticklabels(y_labels, fontsize=7.2)
    ax_b.set_xticks([-0.05, -0.025, 0.0, 0.025, 0.05])
    ax_b.set_xlabel(r"$\ell - \ell_{\mathrm{IC\text{-}avg}}$ (4-IC posterior realizations)")
    panel_header(ax_b, "(b)", "8 four-IC posterior points")

    leg_b = [
        Line2D([], [], color=SLATE, marker="o", ls="None", ms=3.8, label="4 single ICs"),
        Line2D([], [], color=NAVY, marker="s", ls="None", ms=4.2, label=r"$\ell(\bar{X}_4)$ ($\leq 0.0054$)"),
        Line2D([], [], color=AMBER, marker="D", ls="None", ms=4.2, label=r"100k BTemu ($\leq 0.028$)"),
    ]
    ax_b.legend(handles=leg_b, loc="upper left", fontsize=7.2, handletextpad=0.30, labelspacing=0.18, borderaxespad=0.30, frameon=False)

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig3_ic_and_posterior_val",
        alignment_kwargs={"axes": [ax_a, ax_b]},
    )


def draw_fig2_t6_exact_vs_emu() -> dict[str, str]:
    """Fig. 2: Single-column T6 finite exact-vs-emulator 6D smoke comparison."""
    t6 = json.loads(T6_JSON.read_text())
    params = t6["parameters"]
    label_map = {
        "ETA_STAR": r"$\eta_\star$",
        "t_STAR": r"$t_\star$",
        "ALPHA_STAR": r"$\alpha_\star$",
        "M_TURN": r"$\log_{10}(M_{\mathrm{turn}}/M_\odot)$",
        "F_ESC10": r"$\log_{10} f_{\mathrm{esc},10}$",
        "ALPHA_ESC": r"$\alpha_{\mathrm{esc}}$",
    }

    fig = plt.figure(figsize=(SINGLE_COL_MM * MM_TO_IN, 66.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1, 2,
        left=0.315, right=0.975, top=0.875, bottom=0.165,
        wspace=0.14,
    )
    ax_l = fig.add_subplot(gs[0, 0])
    ax_r = fig.add_subplot(gs[0, 1], sharey=ax_l)

    y_pos = np.arange(len(params))[::-1]
    shifts = [p["shift_sigma"] for p in params]
    ratios = [p["width_ratio"] for p in params]

    ax_l.axvspan(-0.25, 0.25, color=PLANCK_BAND, alpha=0.70, zorder=0.5)
    ax_l.axvline(0.0, color=SPINE, lw=0.8, ls="--", zorder=1)
    for yi, sh in zip(y_pos, shifts):
        ax_l.plot([0.0, sh], [yi, yi], color=NAVY, lw=1.45, zorder=2)
        ax_l.scatter([sh], [yi], s=24, color=NAVY, zorder=3)

    format_box_axes(ax_l, minor_x=False, minor_y=False)
    ax_l.set_xlim(-0.29, 0.31)
    ax_l.set_xticks([-0.2, 0.0, 0.2])
    ax_l.set_ylim(-0.6, len(params) - 0.4)
    ax_l.set_yticks(y_pos)
    ax_l.set_yticklabels([label_map[p["parameter"]] for p in params], fontsize=7.3)
    ax_l.set_xlabel(r"$(\mu_e - \mu_m)/\sigma_m$")
    panel_header(ax_l, "(a)", "Mean shift", title_size=7.6)

    ax_r.axvspan(0.90, 1.10, color=PLANCK_BAND, alpha=0.70, zorder=0.5)
    ax_r.axvline(1.0, color=SPINE, lw=0.8, ls="--", zorder=1)
    for yi, wr in zip(y_pos, ratios):
        ax_r.plot([1.0, wr], [yi, yi], color=AMBER, lw=1.45, zorder=2)
        ax_r.scatter([wr], [yi], s=24, color=AMBER, marker="s", zorder=3)

    format_box_axes(ax_r, minor_x=False, minor_y=False)
    ax_r.tick_params(labelleft=False)
    ax_r.set_xlim(0.84, 1.13)
    ax_r.set_xticks([0.9, 1.0, 1.1])
    ax_r.set_xlabel(r"$s_e / s_m$")
    panel_header(ax_r, "(b)", "Width ratio", title_size=7.6)

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig2_t6_exact_vs_emu",
        alignment_kwargs={"axes": [ax_l, ax_r]},
    )


def draw_fig4_ps_pilot_scaling_and_ic() -> dict[str, str]:
    """Fig. 4: Pilot (z,k) PS log-RMSE vs 4-IC scatter heatmap + sample-size / 1-IC-vs-4-IC / 100k scaling."""
    rm = np.load(PS_RESIDUALS_NPZ)
    z_grid = np.asarray(rm["z"], dtype=float)
    k_grid = np.asarray(rm["k"], dtype=float)
    rmse = np.asarray(rm["rmse"], dtype=float)
    ic_sc = np.asarray(rm["ic_scatter"], dtype=float)
    ratio = rmse / np.maximum(ic_sc, 1e-12)

    rep = json.loads(PS_REPORT_JSON.read_text())
    learn = json.loads(PS_LEARN_JSON.read_text())
    ps32_rep = json.loads(PS32_REPORT_JSON.read_text())

    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 76.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1, 2,
        left=0.075, right=0.975, top=0.895, bottom=0.145,
        wspace=0.33,
    )

    # Panel (a): (z, k) heatmap of rmse + contours of rmse / ic_scatter
    ax_a = fig.add_subplot(gs[0, 0])
    # Build clean cell edges in k and uniform redshift index space (with explicit z tick labels)
    dk = np.diff(k_grid)[0]
    k_edges = np.r_[k_grid[0] - 0.5 * dk, 0.5 * (k_grid[:-1] + k_grid[1:]), k_grid[-1] + 0.5 * dk]
    y_idx = np.arange(len(z_grid), dtype=float)
    y_edges = np.arange(len(z_grid) + 1, dtype=float) - 0.5

    mesh = ax_a.pcolormesh(
        k_edges, y_edges, rmse,
        cmap="Blues",
        norm=Normalize(vmin=0.30, vmax=0.85),
        shading="flat",
        rasterized=True,
    )
    KK, YY = np.meshgrid(k_grid, y_idx)
    cs = ax_a.contour(
        KK, YY, ratio,
        levels=[8.0, 15.0, 30.0, 45.0],
        colors=[AMBER, INK, INK, INK],
        linestyles=["--", "-", "-", "-"],
        linewidths=[1.05, 0.90, 0.90, 0.90],
        zorder=4,
    )
    ax_a.clabel(cs, fmt=r"$%.0f\times$", fontsize=7.2, inline=True, inline_spacing=2.5)

    format_box_axes(ax_a, minor_x=False, minor_y=False)
    ax_a.set_xlim(k_edges[0], k_edges[-1])
    ax_a.set_ylim(-0.5, len(z_grid) - 0.5)
    ax_a.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax_a.set_yticks(y_idx[::2])
    ax_a.set_yticklabels([f"{z_grid[i]:.2f}" for i in range(0, len(z_grid), 2)], fontsize=7.4)
    ax_a.set_xlabel(r"Wavenumber $k$ ($\mathrm{Mpc}^{-1}$)")
    ax_a.set_ylabel(r"Redshift $z$")
    panel_header(ax_a, "(a)", r"Pilot $\mathrm{RMSE}$ vs. $\mathrm{RMSE}/s_{\mathrm{IC}}$")

    # Place colorbar cleanly in the upper-right region (above z~14, away from steep contours)
    ax_a.add_patch(
        plt.Rectangle((0.535, 0.725), 0.445, 0.245, transform=ax_a.transAxes, facecolor="white", edgecolor=INNER_SPINE, linewidth=0.55, alpha=0.96, zorder=4.2)
    )
    cax = ax_a.inset_axes([0.57, 0.865, 0.375, 0.052])
    cbar = fig.colorbar(mesh, cax=cax, orientation="horizontal")
    cbar.set_ticks([0.35, 0.60, 0.85])
    cbar.ax.tick_params(labelsize=6.8, pad=1.2, length=1.8, width=0.5)
    cbar.set_label(r"$\log_{10}$ RMSE (dex)", fontsize=7.2, labelpad=1.5, color=INK)
    cax.set_zorder(5)

    # Panel (b): Sample-size & IC-budget scaling + 100k clean external benchmark
    ax_b = fig.add_subplot(gs[0, 1])
    n_pilot = [learn["half_4ic"]["n_train"], learn["full_4ic"]["n_train"], learn["mixed"]["n_train"]]
    rmse_pilot = [learn["half_4ic"]["log_rmse"], learn["full_4ic"]["log_rmse"], learn["mixed"]["log_rmse"]]
    lowz_pilot = [learn["half_4ic"]["low_z_rmse"], learn["full_4ic"]["low_z_rmse"], learn["mixed"]["low_z_rmse"]]

    ax_b.plot(n_pilot, rmse_pilot, color=NAVY, lw=1.55, marker="o", ms=4.5, label=r"Pilot $9\times 20$ overall (4-IC / mixed)", zorder=4)
    ax_b.plot(n_pilot, lowz_pilot, color=TEAL_SLATE, lw=1.25, ls="--", marker="^", ms=4.2, label=r"Pilot $9\times 20$ low-$z$ ($z\leq 7.97$)", zorder=3.5)
    # 1-IC vs 4-IC comparison at N=534
    ax_b.scatter([534], [rep["one_ic"]["log_rmse"]], s=48, marker="D", facecolor="white", edgecolor=AMBER, linewidth=1.25, label=f"Pilot $N=534$, 1-IC ({rep['one_ic']['log_rmse']:.3f} vs 4-IC {rep['four_ic']['log_rmse']:.3f})", zorder=5)

    # Full-box 32x32 scratch baseline at N=128 (cluster-prototype extrapolations purged)
    ax_b.scatter([ps32_rep["train"]], [ps32_rep["model"]["rmse_dex"]], s=40, marker="s", color=AMBER, edgecolor="white", linewidth=0.6, label=rf"Full-box $32\times 32$ MLP ($N={ps32_rep['train']}$, {ps32_rep['model']['rmse_dex']:.3f} dex)", zorder=4)
    ax_b.scatter([ps32_rep["train"]], [ps32_rep["constant_baseline"]["rmse_dex"]], s=32, marker="x", color=SLATE, linewidth=1.1, label=rf"Full-box constant baseline ({ps32_rep['constant_baseline']['rmse_dex']:.3f} dex)", zorder=3)

    ax_b.set_xscale("log")
    format_box_axes(ax_b, minor_x=True, minor_y=False)
    ax_b.set_xlim(90.0, 3800.0)
    ax_b.set_xticks([100, 300, 1000, 3000])
    ax_b.set_xticklabels([r"$10^2$", r"$3\times 10^2$", r"$10^3$", r"$3\times 10^3$"])
    ax_b.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
    ax_b.xaxis.set_minor_formatter(NullFormatter())
    ax_b.set_ylim(0.15, 1.58)
    ax_b.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
    ax_b.set_xlabel(r"Unique training design points $N_{\mathrm{train}}$")
    ax_b.set_ylabel(r"Power-spectrum $\log_{10}(\Delta^2_{21}+0.01)$ RMSE (dex)")
    panel_header(ax_b, "(b)", "Coverage vs. ICs per point")
    ax_b.legend(loc="upper right", fontsize=7.2, handlelength=1.6, labelspacing=0.22, borderaxespad=0.30)

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig4_ps_pilot_scaling_and_ic",
        alignment_kwargs={"axes": [ax_a, ax_b]},
    )


def draw_fig5_ps_estimator_and_fullbox() -> dict[str, str]:
    """Fig. 5: Subbox-vs-fullbox low-k estimator bias and 32x32 full-box contract validation spectra."""
    c833 = np.load(CMP_833_NPZ)
    c199 = np.load(CMP_199_NPZ)
    k_c = np.asarray(c833["k"], dtype=float)
    z_c = np.asarray(c833["z"], dtype=float)
    mask_k = k_c >= 0.1
    kk = k_c[mask_k]
    r833 = (c833["sub"] / c833["full"])[:, mask_k]
    r199 = (c199["sub"] / c199["full"])[:, mask_k]

    ps32 = np.load(PS32_VAL_NPZ)
    z32 = np.asarray(ps32["z"], dtype=float)
    k32 = np.asarray(ps32["k"], dtype=float)
    pred32 = np.asarray(ps32["pred"], dtype=float)
    truth32 = np.asarray(ps32["truth"], dtype=float)
    vids = np.asarray(ps32["validation_ids"], dtype=int)
    pt_rmse = np.sqrt(np.mean((np.log10(pred32 + 0.01) - np.log10(truth32 + 0.01)) ** 2, axis=(1, 2)))
    med_idx = int(np.argsort(pt_rmse)[len(pt_rmse) // 2])
    vid_med = int(vids[med_idx])

    fig = plt.figure(figsize=(DOUBLE_COL_MM * MM_TO_IN, 76.0 * MM_TO_IN))
    gs = gridspec.GridSpec(
        1, 2,
        left=0.075, right=0.980, top=0.895, bottom=0.145,
        wspace=0.28,
    )

    # Panel (a): Subbox / Fullbox ratio for cases 833 and 199 across z=6.34, 7.10, 7.97
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.axhline(1.0, color=SPINE, lw=0.85, ls=":", zorder=1)
    ls_z = [(0, (1.5, 1.2)), "-.", "-"]
    colors_833 = [TEAL_SLATE, AMBER, NAVY]
    for zi, zv in enumerate(z_c):
        ax_a.plot(kk, r833[zi], color=colors_833[zi], ls=ls_z[zi], lw=1.40, label=f"id=833 ($z={zv:.2f}$)", zorder=3.5)
    # For case 199, show z=6.34 and z=7.97 cleanly in slate so plot stays crisp
    ax_a.plot(kk, r199[0], color=SLATE, ls=(0, (3.0, 1.5)), lw=1.10, alpha=0.85, label=f"id=199 ($z={z_c[0]:.2f}$)", zorder=2.5)
    ax_a.plot(kk, r199[2], color=SLATE, ls="-", lw=1.10, alpha=0.85, label=f"id=199 ($z={z_c[2]:.2f}$)", zorder=2.5)

    ax_a.set_xscale("log")
    format_box_axes(ax_a, minor_x=True, minor_y=False)
    ax_a.set_xlim(0.095, 1.05)
    ax_a.set_ylim(0.88, 1.56)
    ax_a.set_xticks([0.1, 0.2, 0.5, 1.0])
    ax_a.xaxis.set_major_formatter(ScalarFormatter())
    ax_a.set_xlabel(r"Wavenumber $k$ ($\mathrm{Mpc}^{-1}$)")
    ax_a.set_ylabel(r"Estimator ratio $\Delta^2_{\mathrm{sub}} / \Delta^2_{\mathrm{full}}$")
    panel_header(ax_a, "(a)", "12-subbox vs. 250 Mpc full-box")
    ax_a.legend(loc="upper right", fontsize=6.4, handlelength=1.8, labelspacing=0.24, borderaxespad=0.35)

    # Panel (b): 32x32 Full-box contract spectra at median 4-IC validation case (vid=80475)
    ax_b = fig.add_subplot(gs[0, 1])
    z_targets = [(7.0, NAVY), (8.0, AMBER), (10.0, TEAL_SLATE)]
    for zv, col in z_targets:
        zi = int(np.argmin(np.abs(z32 - zv)))
        ax_b.plot(k32, truth32[med_idx, zi], color=col, ls="-", lw=1.45, label=f"$z={z32[zi]:.0f}$ 4-IC truth", zorder=3.5)
        ax_b.plot(k32, pred32[med_idx, zi], color=col, ls=(0, (3.0, 1.5)), lw=1.25, label=f"$z={z32[zi]:.0f}$ $N=128$ baseline", zorder=3)

    ax_b.set_xscale("log")
    ax_b.set_yscale("log")
    format_box_axes(ax_b, minor_x=True, minor_y=True)
    ax_b.set_xlim(0.095, 1.05)
    ax_b.set_ylim(0.45, 220.0)
    ax_b.set_xticks([0.1, 0.2, 0.5, 1.0])
    ax_b.xaxis.set_major_formatter(ScalarFormatter())
    ax_b.yaxis.set_major_locator(FixedLocator([1.0, 10.0, 100.0]))
    ax_b.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
    ax_b.yaxis.set_minor_formatter(NullFormatter())
    ax_b.set_xlabel(r"Wavenumber $k$ ($\mathrm{Mpc}^{-1}$)")
    ax_b.set_ylabel(r"$\Delta^2_{21}(k, z)$ ($\mathrm{mK}^2$)")
    panel_header(ax_b, "(b)", f"Full-box $32\\times 32$ val id={vid_med}")
    ax_b.legend(loc="upper right", ncol=2, columnspacing=0.9, fontsize=6.0, handlelength=1.6, labelspacing=0.24, borderaxespad=0.35)

    return export_prd_figure(
        fig,
        OUT_DIR,
        "fig5_ps_estimator_and_fullbox",
        alignment_kwargs={"axes": [ax_a, ax_b]},
    )


def main() -> None:
    apply_prd_style()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = {
        "fig1_history_accuracy": draw_fig1_history_accuracy(),
        "fig2_t6_exact_vs_emu": draw_fig2_t6_exact_vs_emu(),
        "fig3_ic_and_posterior_val": draw_fig3_ic_and_posterior_val(),
        "fig4_ps_pilot_scaling_and_ic": draw_fig4_ps_pilot_scaling_and_ic(),
        "fig5_ps_estimator_and_fullbox": draw_fig5_ps_estimator_and_fullbox(),
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
