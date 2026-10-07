"""No simulations: adversarial release and sealed-path denial checks."""
import importlib.util,json,sys
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('random_production_common',P/'maintenance/random_ic/common.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def passing_summary():
 return {'status':'COMPLETE','complete_families':128,'qualified_fresh_IC_realizations':896,'failed':[],'single_IC_production_decision':'RANDOM_IC_SINGLE_REALIZATION_SUPPORTED','confirmed_core_screen_pass':True,'additional_proposed_diagnostic_screen_pass':True}

@pytest.mark.parametrize('field,value',[('status','PARTIAL'),('complete_families',127),('qualified_fresh_IC_realizations',895),('failed',[{'reason':'NaN'}]),('confirmed_core_screen_pass',False),('additional_proposed_diagnostic_screen_pass',False),('single_IC_production_decision','MULTI_IC_AVERAGING_REQUIRED')])
def test_incomplete_failed_or_unqualified_never_releases(field,value):
 s=passing_summary();s[field]=value;assert not m.audit_gate(s,{'status':'CONFIRMED'})[0]

def test_scientific_confirmation_required():
 assert not m.audit_gate(passing_summary(),{'status':'PROPOSED'})[0]
 assert m.audit_gate(passing_summary(),{'status':'CONFIRMED'})[0]

def test_sealed_path_is_denied(tmp_path,monkeypatch):
 import sqlite3
 dbfile=tmp_path/'design.sqlite';db=sqlite3.connect(dbfile);db.execute('CREATE TABLE design(idx INTEGER PRIMARY KEY,payload TEXT)');db.execute('INSERT INTO design VALUES(?,?)',(115120,json.dumps({'split':'sealed_test'})));db.commit();db.close();monkeypatch.setattr(m,'RUN',tmp_path)
 with pytest.raises(PermissionError,match='Sealed'):m.row(115120)
