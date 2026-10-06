#!/bin/bash
set -euo pipefail
P=/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator
source "$P/scripts/environment.sh"
export OMP_NUM_THREADS=1
"$BT_HISTORY_PYTHON" "$P/maintenance/v2/baseline.py" --snapshot "$P/artifacts/development_history_fidelity_20261003/manifest.json" --out "$P/artifacts/nnero_style_development_1024_v2" --train
