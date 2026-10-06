#!/bin/bash
# Default prints a reviewable command. --submit is explicit and still budget-gated.
set -euo pipefail
BT_DATA_PROJECT=$(cd -- "$(dirname -- "$0")/.." && pwd)
source "$BT_DATA_PROJECT/scripts/environment.sh"
exec "$BT_HISTORY_PYTHON" "$BT_DATA_PROJECT/scripts/submit_data_array.py" "$@"
