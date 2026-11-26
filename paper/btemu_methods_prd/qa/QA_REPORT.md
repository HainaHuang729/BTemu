# BTemu Track B Figure QA Report

- **PyMuPDF (`fitz`) installed locally**: `False` (not installed; PDF typography verified via `audit_pdf_text.py` + Matplotlib display bbox checks + Ghostscript 600/160 dpi PNG visual audit)

| Figure | Alignment (`<=1.5 pt`, strict) | Text BBox Overlaps | Page Clippings | Tick Labels | PDF Min Font (pt) | PDF Status | Overall |
|---|---|---|---|---|---|---|---|
| `fig1_history_accuracy.pdf` | PASS | 0 | 0 | 43 | 5.04 | PASS | **PASS** |
| `fig2_t6_exact_vs_emu.pdf` | PASS | 0 | 0 | 12 | 5.11 | PASS | **PASS** |
| `fig3_ic_and_posterior_val.pdf` | PASS | 0 | 0 | 23 | 5.04 | PASS | **PASS** |
| `fig4_ps_pilot_scaling_and_ic.pdf` | PASS | 0 | 0 | 21 | 5.04 | PASS | **PASS** |
| `fig5_ps_estimator_and_fullbox.pdf` | PASS | 0 | 0 | 20 | 5.46 | PASS | **PASS** |
| `fig6_psx_independent_audit.pdf` | PASS | 0 | 0 | 25 | 5.04 | PASS | **PASS** |
| `fig7_tstar_local_correction.pdf` | PASS | 0 | 0 | 23 | 5.04 | PASS | **PASS** |
| `fig8_ard_gp_and_threeway_gmm.pdf` | PASS | 0 | 0 | 21 | 5.04 | PASS | **PASS** |

**QA_OVERALL_PASS**: `True`
