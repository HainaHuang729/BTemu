"""Reuse verified recovery-aware development loader without changing production code."""
import json,runpy,sys,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2];run=Path(sys.argv[1]);plan=json.loads((run/'loader_recovery_plan.json').read_text())
for path,sha in plan['implementation_hashes'].items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==sha
sys.argv=[str(root/'maintenance/development_snapshot/compare.py'),str(run)]
runpy.run_path(sys.argv[0],run_name='__main__')
p=json.loads((run/'plan.json').read_text());(run/'complete.json').write_text(json.dumps({'N':p['N'],'validation_n':p['validation_n'],'loader_recovery_plan':'loader_recovery_plan.json','production_accepted':False,'sealed_access':False},indent=2)+'\n')
