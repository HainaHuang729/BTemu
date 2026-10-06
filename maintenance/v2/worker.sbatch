#!/bin/bash
set -uo pipefail
P=$1
source "$P/scripts/environment.sh"
umask 077
IFS=',' read -r -a BT_V2_INDICES <<< "$5"
export BT_MANIFEST_INDEX="${BT_V2_INDICES[${SLURM_ARRAY_TASK_ID:?}]:?}"
"$BT_HISTORY_PYTHON" "$P/scripts/generate_history_label.py" --project "$P" --manifest "$2" --budget "$3" --stage "$4" --index "$BT_MANIFEST_INDEX"
