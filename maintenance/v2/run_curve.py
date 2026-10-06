"""Reuse Direct training; compare NNERO-style at one immutable data snapshot."""
import sys,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'src'));sys.path.insert(0,str(root/'maintenance/v2'))
from bt_history.data_control import read_json,write_json
from bt_history.contracts import file_hash
from bt_history.training import train
from baseline import load
run=Path(sys.argv[1]);plan=read_json(run/'plan.json')
for p,h in [('snapshot.json',plan['snapshot_sha256'])]:assert file_hash(run/p)==h
for p,h in [('configs/training.json',plan['training_config_sha256']),('maintenance/v2/models.py',plan['model_implementation_sha256']),('maintenance/v2/baseline.py',plan['baseline_implementation_sha256']),('maintenance/v2/run_curve.py',plan['driver_sha256'])]:assert file_hash(root/p)==h
c,rows,post=load(run/'snapshot.json');cfg=read_json(root/'configs/training.json');split={r['sample_id']:r['split'] for r in rows}
if plan.get('reuse_direct_run'):
 source=root/plan['reuse_direct_run']/'direct_resmlp'
 write_json(run/'direct_baseline_reference.json',{'run':plan['reuse_direct_run'],'ensemble_metrics_sha256':file_hash(source/'ensemble_metrics.json'),'same_train_ID_subset':True,'same_frozen_validation':True,'no_duplicate_direct_training':True})
else:train(c,rows,split,cfg,run/'direct_resmlp',post)
subprocess.run([sys.executable,str(root/'maintenance/v2/baseline.py'),'--snapshot',str(run/'snapshot.json'),'--out',str(run/'nnero_style'),'--train'],check=True)
write_json(run/'complete.json',{'N':plan['N'],'seeds':cfg['seeds'],'validation_n':plan['validation_n'],'production_accepted':False,'sealed_access':False})
