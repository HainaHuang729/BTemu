"""Freeze implementation hashes; does not authorize a native, budget or job."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.data_control import read_json,write_json
from bt_history.contracts import file_hash
root=Path(__file__).resolve().parents[1];budget=read_json(root/'configs/data_stage_budgets.json')
if budget['authorized']:raise PermissionError('Cannot refreeze an authorized running generation pipeline')
files={str(p.relative_to(root)):file_hash(p) for folder in ['src','scripts'] for p in sorted((root/folder).rglob('*')) if p.is_file() and p.suffix in ['.py','.sh','.sbatch']}
write_json(root/'contracts/pipeline_integrity.json',{'files':files,'approval':False,'scope':'implementation identity only'})
budget['policy_sha256']={p:file_hash(root/p) for p in ['contracts/data_quality_protocol.json','contracts/split_policy.json','contracts/sealed_test_policy.json']}
budget['pipeline_integrity_sha256']=file_hash(root/'contracts/pipeline_integrity.json');write_json(root/'configs/data_stage_budgets.json',budget)
