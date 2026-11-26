"""Automated figure QA and provenance manifest generator for BTemu Track B manuscript."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

MANUSCRIPT_DIR = Path("/Users/amadeus/Documents/ChatGPT/论文/output/btemu_methods_manuscript")
FIG_DIR = MANUSCRIPT_DIR / "figures"
QA_DIR = MANUSCRIPT_DIR / "qa"
PDF_AUDIT_SCRIPT = Path("/Users/amadeus/.gemini/config/plugins/codex-skills/skills/nature-figure/scripts/audit_pdf_text.py")

FIG_SPECS = [
    ("fig1_history_accuracy", 1, "BTemu-xHI 65k 512-val reconstruction, residuals vs T7 IC scatter, 5-seed CDF, and paired 65k->100k reduction"),
    ("fig2_t6_exact_vs_emu", 2, "Finite-sample T6 exact-vs-emulator 6D smoke comparison"),
    ("fig3_ic_and_posterior_val", 3, "Prior-box T7 scatter/emulator error vs A3 posterior strata and 8 four-IC posterior points"),
    ("fig4_ps_pilot_scaling_and_ic", 4, "21-cm PS pilot (z,k) log-RMSE vs 4-IC scatter and de-confounded training-budget scaling (1-IC vs 4-IC vs N_train and full-box N=128 baseline)"),
    ("fig5_ps_estimator_and_fullbox", 5, "Subbox-vs-fullbox low-k estimator ratio bias and full-box 32x32 validation baseline spectra"),
    ("fig6_psx_independent_audit", 6, "PSX-emu v1.0 split-contamination vs 300-pt zero-overlap independent PS+xHI+tau audit and 2-IC noise floor"),
    ("fig7_tstar_local_correction", 7, "Localized RBF residual patch L2/L3 reductions across Stages 1-3 and t_STAR posterior recovery vs four-way PL diagnostics"),
    ("fig8_ard_gp_and_threeway_gmm", 8, "Matern-5/2 ARD-GP lightcone/coeval patch residual reductions and three-way 8D Stretch+GMM posterior parameter recovery"),
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    pymupdf_available = importlib.util.find_spec("fitz") is not None

    manifest_items = []
    qa_lines = [
        "# BTemu Track B Figure QA Report",
        "",
        f"- **PyMuPDF (`fitz`) installed locally**: `{pymupdf_available}` (not installed; PDF typography verified via `audit_pdf_text.py` + Matplotlib display bbox checks + Ghostscript 600/160 dpi PNG visual audit)",
        "",
        "| Figure | Alignment (`<=1.5 pt`, strict) | Text BBox Overlaps | Page Clippings | Tick Labels | PDF Min Font (pt) | PDF Status | Overall |",
        "|---|---|---|---|---|---|---|---|",
    ]
    all_pass = True

    for name, fnum, desc in FIG_SPECS:
        pdf_path = FIG_DIR / f"{name}.pdf"
        png_path = FIG_DIR / f"{name}.png"
        align_path = FIG_DIR / f"{name}.alignment.json"
        bbox_path = FIG_DIR / f"{name}.bbox_check.json"

        align_data = json.loads(align_path.read_text())
        bbox_data = json.loads(bbox_path.read_text())

        proc = subprocess.run(
            [sys.executable, str(PDF_AUDIT_SCRIPT), str(pdf_path), "--min-pt", "5.0", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        pdf_json_path = QA_DIR / f"{name}.pdf_audit.json"
        pdf_json_path.write_text(proc.stdout)
        pdf_audit = json.loads(proc.stdout)
        min_pt = float(pdf_audit["minimum_found_pt"])
        below_cnt = int(pdf_audit["below_minimum_count"])
        pdf_status = "PASS" if (proc.returncode == 0 and below_cnt == 0 and min_pt >= 5.0) else "FAIL"

        fig_pass = (
            align_data.get("verdict") == "PASS"
            and bbox_data.get("verdict") == "PASS"
            and bbox_data.get("overlap_count", 1) == 0
            and bbox_data.get("clipping_count", 1) == 0
            and bbox_data.get("tick_label_count", 0) > 0
            and pdf_status == "PASS"
        )
        if not fig_pass:
            all_pass = False

        qa_lines.append(
            f"| `{name}.pdf` | {align_data.get('verdict')} | {bbox_data.get('overlap_count')} | "
            f"{bbox_data.get('clipping_count')} | {bbox_data.get('tick_label_count')} | "
            f"{min_pt:.2f} | {pdf_status} | **{'PASS' if fig_pass else 'FAIL'}** |"
        )
        manifest_items.append({
            "figure_number": fnum,
            "name": name,
            "pdf": f"figures/{name}.pdf",
            "png": f"figures/{name}.png",
            "pdf_sha256": _sha256(pdf_path),
            "png_sha256": _sha256(png_path),
            "description": desc,
            "alignment_verdict": align_data.get("verdict"),
            "bbox_verdict": bbox_data.get("verdict"),
            "min_font_pt": min_pt,
            "pdf_audit_status": pdf_status,
            "qa_pass": fig_pass,
        })

    qa_lines.extend([
        "",
        f"**QA_OVERALL_PASS**: `{all_pass}`",
    ])
    (QA_DIR / "QA_REPORT.md").write_text("\n".join(qa_lines) + "\n")
    (MANUSCRIPT_DIR / "figure_manifest.json").write_text(
        json.dumps({"qa_overall_pass": all_pass, "pymupdf_available": pymupdf_available, "figures": manifest_items}, indent=2) + "\n"
    )
    print(f"QA_OVERALL_PASS={all_pass} (PYMUPDF={pymupdf_available})")
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
