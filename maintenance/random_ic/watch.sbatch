#!/bin/bash
set -euo pipefail
P=/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator
source "$P/scripts/environment.sh"
export OMP_NUM_THREADS=1
"$BT_HISTORY_PYTHON" "$P/maintenance/random_ic/watch.py"
