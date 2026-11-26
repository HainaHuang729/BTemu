"""Shared Physical Review D (APS) figure style, safety, alignment, and export helpers."""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Iterable, Sequence

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter, NullLocator, StrMethodFormatter
import numpy as np
from scipy.ndimage import gaussian_filter, gaussian_filter1d

SKILL_SCRIPTS_DIR = Path("/Users/amadeus/.gemini/config/plugins/codex-skills/skills/nature-figure/scripts")
if str(SKILL_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS_DIR))
from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402

# Physical widths matching APS Physical Review D two-column layout
SINGLE_COL_MM = 86.0
DOUBLE_COL_MM = 168.0
APPENDIX_COL_MM = 150.0
MM_TO_IN = 1.0 / 25.4

# Typography: uniform normal weight everywhere; bold reserved only for panel letters (a, b, c, ...)
PANEL_LETTER_SIZE = 9.0
LABEL_SIZE = 8.8
LEGEND_SIZE = 8.2
PANEL_TITLE_SIZE = 8.2
TICK_SIZE = 7.8
COMPACT_LABEL_SIZE = 8.2
COMPACT_TICK_SIZE = 7.5
INSET_LABEL_SIZE = 7.8
INSET_TITLE_SIZE = 7.8
INSET_TICK_SIZE = 7.5

# Restrained modern PRD color palette (colorblind-safe & grayscale-distinguishable)
INK = "#1f2730"
SPINE = "#5d6770"
INNER_SPINE = "#cfd6dd"
NAVY = "#164c78"
BAND_68 = "#8fb4d4"
BAND_95 = "#dbe7f2"
AMBER = "#b55d15"
TEAL_SLATE = "#4d7ea8"
SLATE = "#5e6873"
PLANCK_BAND = "#e6ebf0"
EXTRAP_TINT = "#f4f6f8"
GRID_FAINT = "#eaedf0"

# Ordered baseline -> signal -> hero so PL dashed stays visible on top if coinciding with BT(10, 2.5)
SPECTRA_STYLE = (
    (SLATE, "--", 1.30, 4.0, "o"),
    (AMBER, "-.", 1.30, 3.4, "s"),
    (TEAL_SLATE, ":", 1.35, 3.2, "^"),
    (NAVY, "-", 1.45, 3.0, "D"),
)


def apply_prd_style() -> None:
    """Configure Matplotlib for APS/PRD publication output with STIX serif and editable vectors."""
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.unicode_minus": False,
        "font.weight": "normal",
        "axes.labelweight": "normal",
        "axes.titleweight": "normal",
        "font.size": LABEL_SIZE,
        "axes.labelsize": LABEL_SIZE,
        "axes.titlesize": PANEL_TITLE_SIZE,
        "xtick.labelsize": TICK_SIZE,
        "ytick.labelsize": TICK_SIZE,
        "legend.fontsize": LEGEND_SIZE,
        "legend.frameon": False,
        "axes.spines.top": True,
        "axes.spines.right": True,
        "axes.axisbelow": True,
        "axes.edgecolor": SPINE,
        "axes.linewidth": 0.62,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "figure.dpi": 150,
        "savefig.dpi": 600,
        "savefig.bbox": None,
        "savefig.pad_inches": 0.0,
    })


def format_box_axes(
    ax: plt.Axes,
    *,
    top_ticks: bool = True,
    right_ticks: bool = True,
    minor_x: bool = False,
    minor_y: bool = False,
    tick_size: float | None = None,
) -> None:
    """Apply clean closed-box APS axis styling with inward ticks and optional log minor ticks."""
    for spine in ax.spines.values():
        spine.set_color(SPINE)
        spine.set_linewidth(0.62)
    kw: dict[str, Any] = {
        "which": "major",
        "direction": "in",
        "top": top_ticks,
        "right": right_ticks,
        "length": 2.8,
        "width": 0.62,
        "pad": 2.4,
    }
    if tick_size is not None:
        kw["labelsize"] = tick_size
    ax.tick_params(**kw)
    if minor_x:
        if ax.get_xscale() == "log":
            ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
            ax.xaxis.set_minor_formatter(NullFormatter())
        ax.tick_params(
            axis="x", which="minor", direction="in",
            top=top_ticks, bottom=True, length=1.5, width=0.45,
        )
    else:
        ax.xaxis.set_minor_locator(NullLocator())
    if minor_y:
        if ax.get_yscale() == "log":
            ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1))
            ax.yaxis.set_minor_formatter(NullFormatter())
        ax.tick_params(
            axis="y", which="minor", direction="in",
            right=right_ticks, left=True, length=1.5, width=0.45,
        )
    else:
        ax.yaxis.set_minor_locator(NullLocator())


def format_corner_axes(ax: plt.Axes, row: int, col: int, n: int) -> None:
    """Style corner-plot axes with solid outer borders and quiet inner hairlines."""
    outer_x = row == n - 1
    outer_y = col == 0
    is_diag = row == col
    ax.tick_params(
        axis="x", which="major", bottom=True, top=False,
        labelbottom=outer_x, direction="in", length=2.0, width=0.58, pad=2.0,
        labelsize=COMPACT_TICK_SIZE,
    )
    ax.tick_params(
        axis="y", which="major", left=not is_diag, right=False,
        labelleft=outer_y and not is_diag, direction="in", length=2.0, width=0.58, pad=2.0,
        labelsize=COMPACT_TICK_SIZE,
    )
    ax.xaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_minor_locator(NullLocator())
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(SPINE if outer_x else INNER_SPINE)
    ax.spines["bottom"].set_linewidth(0.60 if outer_x else 0.45)
    if is_diag:
        ax.spines["left"].set_visible(False)
    else:
        ax.spines["left"].set_visible(True)
        ax.spines["left"].set_color(SPINE if outer_y else INNER_SPINE)
        ax.spines["left"].set_linewidth(0.60 if outer_y else 0.45)


def panel_header(ax: plt.Axes, letter: str, title: str = "", pad: float = 3.5, title_size: float | None = None) -> None:
    """Set bold lowercase panel letter on left and normal-weight context title on right."""
    ax.set_title(letter, loc="left", fontweight="bold", pad=pad, fontsize=PANEL_LETTER_SIZE, color=INK)
    if title:
        ax.set_title(
            title,
            loc="right",
            fontweight="normal",
            pad=pad,
            fontsize=title_size or PANEL_TITLE_SIZE,
            color=INK,
        )


def interp_monotone(x_eval: np.ndarray, xp: np.ndarray, fp: np.ndarray) -> np.ndarray:
    """Interpolate strictly increasing xp -> fp after asserting monotonicity."""
    xp_arr = np.asarray(xp, dtype=float)
    fp_arr = np.asarray(fp, dtype=float)
    if xp_arr.ndim != 1 or fp_arr.ndim != 1 or len(xp_arr) != len(fp_arr):
        raise ValueError("xp and fp must be 1D arrays of equal length")
    if not np.all(np.diff(xp_arr) > 0):
        raise ValueError("xp must be strictly increasing for np.interp")
    return np.interp(x_eval, xp_arr, fp_arr)


def plot_lf_obs_with_ul(
    ax: plt.Axes,
    muv: np.ndarray,
    phi: np.ndarray,
    sig_minus: np.ndarray,
    sig_plus: np.ndarray,
    *,
    log_y: bool = True,
    ms: float = 2.9,
    ul_dex: float = 0.42,
    capsize: float = 1.25,
    lw: float = 0.62,
    mew: float = 0.68,
) -> int:
    """Plot UV LF measurements with crisp downward arrows where phi - sigma_minus <= 0."""
    muv = np.asarray(muv, dtype=float)
    phi = np.asarray(phi, dtype=float)
    sig_minus = np.asarray(sig_minus, dtype=float)
    sig_plus = np.asarray(sig_plus, dtype=float)
    if not np.all(phi > 0):
        raise ValueError("Observed phi must be strictly positive")

    pos_mask = (phi - sig_minus) > 0.0
    ul_mask = ~pos_mask

    if np.any(pos_mask):
        if log_y:
            y_pos = phi[pos_mask]
            yerr_pos = [sig_minus[pos_mask], sig_plus[pos_mask]]
        else:
            y_pos = np.log10(phi[pos_mask])
            yerr_pos = [
                y_pos - np.log10(phi[pos_mask] - sig_minus[pos_mask]),
                np.log10(phi[pos_mask] + sig_plus[pos_mask]) - y_pos,
            ]
        ax.errorbar(
            muv[pos_mask],
            y_pos,
            yerr=yerr_pos,
            fmt="o",
            ms=ms,
            mfc="white",
            mec=INK,
            mew=mew,
            ecolor=SLATE,
            elinewidth=lw,
            capsize=capsize,
            zorder=5,
        )

    if np.any(ul_mask):
        for m_val, p_val, sp_val in zip(muv[ul_mask], phi[ul_mask], sig_plus[ul_mask]):
            if log_y:
                y_c = p_val
                hi_err = sp_val
                y_end = p_val * (10.0 ** (-ul_dex))
            else:
                y_c = np.log10(p_val)
                hi_err = np.log10(p_val + sp_val) - y_c
                y_end = y_c - ul_dex
            ax.errorbar(
                [m_val],
                [y_c],
                yerr=[[0.0], [hi_err]],
                fmt="o",
                ms=ms,
                mfc="white",
                mec=INK,
                mew=mew,
                ecolor=SLATE,
                elinewidth=lw,
                capsize=capsize,
                zorder=5,
            )
            ax.annotate(
                "",
                xy=(m_val, y_end),
                xytext=(m_val, y_c),
                arrowprops={
                    "arrowstyle": "-|>,head_length=0.25,head_width=0.14",
                    "color": SLATE,
                    "lw": lw,
                    "shrinkA": max(1.5, ms * 0.52),
                    "shrinkB": 0.0,
                },
                zorder=4.8,
            )
    return int(np.sum(ul_mask))


def hpd_levels_2d(
    x: np.ndarray,
    y: np.ndarray,
    bounds_x: tuple[float, float],
    bounds_y: tuple[float, float],
    *,
    bins: int = 28,
    sigma: float = 1.25,
    weights: np.ndarray | None = None,
    probs: Sequence[float] = (0.68, 0.95),
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[float]]:
    """Compute smoothed 2D histogram grid and HPD contour levels for 68% and 95% probability mass."""
    hist_raw, xe, ye = np.histogram2d(x, y, bins=bins, range=[bounds_x, bounds_y], weights=weights)
    hist_smooth = gaussian_filter(hist_raw, sigma=sigma, mode="reflect")
    ordered = np.sort(hist_smooth.ravel())[::-1]
    cumsum = np.cumsum(ordered)
    total = float(cumsum[-1])
    if total <= 0:
        raise ValueError("2D histogram total mass must be positive")
    # Order probabilities high->low mass (e.g., 0.95 -> 0.68) so contour levels ascend
    levels = []
    for p in sorted(probs, reverse=True):
        idx = int(np.searchsorted(cumsum, p * total))
        idx = min(idx, len(ordered) - 1)
        levels.append(float(ordered[idx]))
    # Guarantee strictly ascending thresholds when histogram has flat plateaus
    for k in range(1, len(levels)):
        if levels[k] <= levels[k - 1]:
            levels[k] = levels[k - 1] * (1.0 + 1e-6) + 1e-12
    xc = np.r_[xe[0], 0.5 * (xe[:-1] + xe[1:]), xe[-1]]
    yc = np.r_[ye[0], 0.5 * (ye[:-1] + ye[1:]), ye[-1]]
    density = np.pad(hist_smooth, 1, mode="edge").T
    return xc, yc, density, levels


def check_text_overlaps(fig: plt.Figure, *, pad_pt: float = -0.3) -> dict[str, Any]:
    """Measure rendered display bboxes of all visible texts and detect overlaps or page clipping."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig_bbox = fig.bbox
    dpi_scale = 72.0 / fig.dpi  # display px -> pt

    items: list[dict[str, Any]] = []
    tick_label_count = 0
    tick_obj_ids: set[int] = set()
    texts = list(fig.texts)
    for leg in fig.legends:
        texts.extend(leg.get_texts())
    for ax in fig.axes:
        if not ax.get_visible():
            continue
        texts.extend([ax.title, ax._left_title, ax._right_title])
        if ax.axison:
            texts.extend([ax.xaxis.label, ax.yaxis.label])
            for lbl in ax.get_xticklabels() + ax.get_yticklabels():
                if lbl.get_visible():
                    texts.append(lbl)
                    tick_obj_ids.add(id(lbl))
        texts.extend(ax.texts)
        leg = ax.get_legend()
        if leg is not None and leg.get_visible():
            texts.extend(leg.get_texts())

    seen_ids: set[int] = set()
    for t in texts:
        if id(t) in seen_ids or not t.get_visible():
            continue
        seen_ids.add(id(t))
        s = t.get_text().strip()
        if not s:
            continue
        bb = t.get_window_extent(renderer=renderer)
        if bb.width <= 0 or bb.height <= 0:
            continue
        if id(t) in tick_obj_ids:
            tick_label_count += 1
        items.append({
            "text": s,
            "x0": float(bb.x0),
            "y0": float(bb.y0),
            "x1": float(bb.x1),
            "y1": float(bb.y1),
        })

    overlaps = []
    tol_px = pad_pt / dpi_scale  # negative allows tiny touching, positive requires clearance
    for i in range(len(items)):
        a = items[i]
        for j in range(i + 1, len(items)):
            b = items[j]
            ix = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
            iy = min(a["y1"], b["y1"]) - max(a["y0"], b["y0"])
            if ix > -tol_px and iy > -tol_px:
                overlaps.append({
                    "a": a["text"],
                    "b": b["text"],
                    "overlap_x_pt": round(ix * dpi_scale, 2),
                    "overlap_y_pt": round(iy * dpi_scale, 2),
                })

    clippings = []
    margin_px = 0.5 / dpi_scale
    for a in items:
        if (
            a["x0"] < fig_bbox.x0 - margin_px
            or a["y0"] < fig_bbox.y0 - margin_px
            or a["x1"] > fig_bbox.x1 + margin_px
            or a["y1"] > fig_bbox.y1 + margin_px
        ):
            clippings.append({
                "text": a["text"],
                "bbox_pt": [round(v * dpi_scale, 2) for v in (a["x0"], a["y0"], a["x1"], a["y1"])],
                "page_pt": [round(fig_bbox.width * dpi_scale, 2), round(fig_bbox.height * dpi_scale, 2)],
            })

    return {
        "text_count": len(items),
        "tick_label_count": tick_label_count,
        "overlap_count": len(overlaps),
        "clipping_count": len(clippings),
        "overlaps": overlaps,
        "clippings": clippings,
        "verdict": "PASS" if (not overlaps and not clippings) else "FAIL",
    }


def export_prd_figure(
    fig: plt.Figure,
    out_dir: Path,
    name: str,
    *,
    alignment_kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run render-time panel alignment and text-bbox checks, then export PDF, SVG, and 600 dpi PNG."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / name
    align_kw = dict(alignment_kwargs or {})
    align_report = require_matplotlib_panel_alignment(
        fig,
        json_out=stem.with_suffix(".alignment.json"),
        overlay_svg=stem.with_suffix(".alignment.svg"),
        tolerance_pt=1.5,
        gutter_tolerance_pt=1.5,
        strict=True,
        **align_kw,
    )
    bbox_report = check_text_overlaps(fig)
    stem.with_suffix(".bbox_check.json").write_text(json.dumps(bbox_report, indent=2) + "\n")

    fig.savefig(stem.with_suffix(".pdf"), bbox_inches=None)
    fig.savefig(stem.with_suffix(".svg"), bbox_inches=None)
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches=None)
    plt.close(fig)
    return {"alignment": align_report["verdict"], "bbox": bbox_report["verdict"]}


def legend_line(
    label: str,
    color: str,
    ls: str = "-",
    lw: float = 1.4,
    marker: str | None = None,
    mfc: str | None = None,
    mec: str | None = None,
    mew: float | None = None,
) -> Line2D:
    """Create a legend line handle."""
    kw: dict[str, Any] = {"label": label, "color": color, "ls": ls, "lw": lw}
    if marker:
        kw.update({"marker": marker, "markersize": 3.4})
        if mfc is not None:
            kw["markerfacecolor"] = mfc
        if mec is not None:
            kw["markeredgecolor"] = mec
        if mew is not None:
            kw["markeredgewidth"] = mew
    return Line2D([], [], **kw)


def legend_band(label: str, color: str, edge: str | None = None) -> Patch:
    """Create a legend patch handle for credible intervals."""
    return Patch(facecolor=color, edgecolor=edge or "none", linewidth=0.55 if edge else 0.0, label=label)
