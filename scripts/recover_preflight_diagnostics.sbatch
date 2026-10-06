#!/bin/bash
set -euo pipefail
source /oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/scripts/environment.sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
"$BT_HISTORY_PYTHON" - <<'RECOVERY'
import json,os,shutil
from pathlib import Path
root=Path('/oss06/data/project/tkcastrosim/HNHuang/project_bt_history_emulator/data_runs/20260928_batch1')
out=root/'cancelled_attempt_diagnostics';out.mkdir(exist_ok=True)
found=[]
for p in Path('/tmp').glob('bt_label_*/payload/runtime.json'):
 try:
  if p.stat().st_uid!=os.getuid():continue
  r=json.loads(p.read_text())
  if r.get('slurm_job_id')!='2159722':continue
  target=out/p.parent.parent.name;target.mkdir(exist_ok=True)
  for x in p.parent.iterdir():
   if x.is_file() and x.suffix in ['.json','.log']:shutil.copy2(x,target/x.name)
  found.append({'workspace':str(p.parent),'runtime_fingerprint':r['runtime_fingerprint'],'import_passed':r['import_passed'],'files':[x.name for x in target.iterdir()]})
 except (PermissionError,FileNotFoundError):continue
(out/'recovery.json').write_text(json.dumps({'recovery_job_id':os.environ['SLURM_JOB_ID'],'source_job':'2159722','full_evaluations':0,'found':found},indent=2))
print(json.dumps(found))
RECOVERY
