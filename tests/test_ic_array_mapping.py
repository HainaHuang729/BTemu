import sys,json,importlib.util
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'maintenance/ic_audit'));sys.path.insert(0,str(P/'src'))
from worker import manifest_index
from advance import allocated_charges
from bt_history.contracts import file_hash

def test_compact_position_preserves_high_manifest_index(tmp_path,monkeypatch):
 f=tmp_path/'map.json';f.write_text(json.dumps({'indices':[881,1001,1023]}));monkeypatch.setenv('BT_IC_AUDIT_MAP',str(f));monkeypatch.setenv('BT_IC_AUDIT_MAP_SHA',file_hash(f));monkeypatch.setenv('SLURM_ARRAY_TASK_ID','2');assert manifest_index()==1023
 f.write_text(json.dumps({'indices':[881,1001,1022]}))
 with pytest.raises(ValueError,match='checksum'):manifest_index()

def test_legacy_task_mapping(monkeypatch):
 monkeypatch.delenv('BT_IC_AUDIT_MAP',raising=False);monkeypatch.setenv('SLURM_ARRAY_TASK_ID','879');assert manifest_index()==879

def test_rejection_does_not_consume_first_attempt_ordinal():
 rejected={'index':1023,'state':'SUBMISSION_REJECTED','actual_core_hours':0};real={'index':1023,'state':'COMPLETED','actual_core_hours':1.5}
 assert allocated_charges([rejected,real])==[real]
