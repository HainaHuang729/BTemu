#!/bin/bash
set -euo pipefail
P=/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator
source "$P/scripts/environment.sh"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
"$BT_HISTORY_PYTHON" "$P/maintenance/random_ic/design.py"
"$BT_HISTORY_PYTHON" "$P/maintenance/random_ic/freeze.py"
