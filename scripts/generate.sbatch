#!/bin/bash
# Resources, bounded array and concurrency are supplied by submit_data_array.sh.
set -uo pipefail
BT_DATA_PROJECT=$1
BT_DATA_MANIFEST=$2
BT_DATA_BUDGET=$3
BT_DATA_STAGE=$4
source "$BT_DATA_PROJECT/scripts/environment.sh"
umask 077
"$BT_HISTORY_PYTHON" "$BT_DATA_PROJECT/scripts/generate_history_label.py" --project "$BT_DATA_PROJECT" --manifest "$BT_DATA_MANIFEST" --budget "$BT_DATA_BUDGET" --stage "$BT_DATA_STAGE" --index "${SLURM_ARRAY_TASK_ID:?Explicit bounded array required}"

BT_WORKER_EXIT=$?
# Continuation costs are inside this allocation; no detached login-node worker.
"$BT_HISTORY_PYTHON" "$BT_DATA_PROJECT/scripts/advance_batch1.py" --project "$BT_DATA_PROJECT" --budget "$BT_DATA_BUDGET" --worker-exit "$BT_WORKER_EXIT"
BT_ADVANCE_EXIT=$?
if [ "$BT_WORKER_EXIT" -ne 0 ]; then exit "$BT_WORKER_EXIT"; fi
exit "$BT_ADVANCE_EXIT"
