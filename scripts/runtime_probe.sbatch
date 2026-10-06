#!/bin/bash
set -uo pipefail
BT_PROJECT=/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator
source "$BT_PROJECT/scripts/environment.sh"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
umask 077
hostname
getconf GNU_LIBC_VERSION
cat /etc/os-release
"$BT_HISTORY_PYTHON" "$BT_PROJECT/scripts/check_runtime.py" --output "$BT_PROJECT/data_runs/20260928_batch1/runtime_probes/${SLURM_JOB_ID}.json"
