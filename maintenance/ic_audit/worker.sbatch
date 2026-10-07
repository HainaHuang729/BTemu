#!/bin/bash
set -euo pipefail
P=/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator
source "$P/scripts/environment.sh"
"$BT_HISTORY_PYTHON" "$P/maintenance/ic_audit/worker.py"
