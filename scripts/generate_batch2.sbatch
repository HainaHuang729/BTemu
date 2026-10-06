#!/bin/bash
set -uo pipefail
BT_DATA_PROJECT=$1
BT_DATA_MANIFEST=$2
BT_DATA_BUDGET=$3
BT_DATA_STAGE=$4
source "$BT_DATA_PROJECT/scripts/environment.sh"
umask 077
if [ -n "${5:-}" ]; then
  IFS=',' read -r -a BT_BATCH_INDICES <<< "$5"
  export BT_MANIFEST_INDEX="${BT_BATCH_INDICES[${SLURM_ARRAY_TASK_ID:?}]:?Missing index mapping}"
else
  export BT_MANIFEST_INDEX="${SLURM_ARRAY_TASK_ID:?}"
fi
"$BT_HISTORY_PYTHON" "$BT_DATA_PROJECT/scripts/generate_history_label.py" --project "$BT_DATA_PROJECT" --manifest "$BT_DATA_MANIFEST" --budget "$BT_DATA_BUDGET" --stage "$BT_DATA_STAGE" --index "$BT_MANIFEST_INDEX"
BT_WORKER_EXIT=$?
"$BT_HISTORY_PYTHON" "$BT_DATA_PROJECT/scripts/advance_dataset.py" --project "$BT_DATA_PROJECT" --budget "$BT_DATA_BUDGET"
BT_ADVANCE_EXIT=$?
if [ "$BT_ADVANCE_EXIT" -ne 0 ]; then exit "$BT_ADVANCE_EXIT"; fi
exit "$BT_WORKER_EXIT"
