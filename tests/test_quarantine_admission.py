import json,tempfile,unittest
from pathlib import Path
from bt_history.data_control import assert_development_path,write_json
from bt_history.quarantine_admission import effective_receipt,admit_completed
from bt_history.contracts import digest

class QuarantineTests(unittest.TestCase):
 def test_quarantine_path_and_symlink_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);q=p/'quarantine_pending_native';q.mkdir();f=q/'label.json';f.write_text('DO NOT READ');alias=p/'alias.json';alias.symlink_to(f)
   for path in [f,alias]:
    with self.assertRaises(PermissionError):assert_development_path(path,'train')
 def test_mechanical_success_is_not_admitted(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);write_json(p/'configs/data_stage_budgets.json',{'budget_id':'b'})
   write_json(p/'data_runs/b/receipts/a.json',{'qualified':False,'mechanical_qualified':True,'simulation_status':'success'})
   r=effective_receipt(p,{'attempt_id':'a'});self.assertFalse(r['qualified']);self.assertTrue(r['mechanical_qualified'])
 def test_false_native_gate_refuses_admission_before_label_access(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   for name,val in [('configs/data_stage_budgets.json',{'budget_id':'b'}),('contracts/science_contract.json',{}),('contracts/selected_native_contract.json',{'native_sha256':'sha'}),('results/native_qualification.json',{'qualified_for_batch1':False})]:write_json(p/name,val)
   with self.assertRaises(PermissionError):admit_completed(p)
 def test_gate_with_wrong_target_refuses_admission(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)
   for name,val in [('configs/data_stage_budgets.json',{'budget_id':'b'}),('contracts/science_contract.json',{}),('contracts/selected_native_contract.json',{'native_sha256':'sha'}),('results/native_qualification.json',{'qualified_for_batch1':True,'science_contract_hash':'wrong'})]:write_json(p/name,val)
   with self.assertRaises(PermissionError):admit_completed(p)

class MigrationTests(unittest.TestCase):
 def test_orchestration_migration_rejects_scientific_change(self):
  from bt_history.contracts import file_hash
  from bt_history.quarantine_admission import qualified_pipeline_matches
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);science=p/'src/bt_history/label_worker.py';science.parent.mkdir(parents=True);science.write_text('science unchanged')
   control=p/'scripts/advance_batch1.py';control.parent.mkdir();control.write_text('old')
   old={'files':{str(x.relative_to(p)):file_hash(x) for x in [science,control]}}
   oldpath=p/'contracts/original.json';write_json(oldpath,old)
   q={'pipeline_integrity_sha256':file_hash(oldpath)};write_json(p/'results/native_qualification.json',q)
   control.write_text('continue failures');new={'files':{str(x.relative_to(p)):file_hash(x) for x in [science,control]}}
   write_json(p/'contracts/pipeline_integrity.json',new)
   m={'qualification_sha256':file_hash(p/'results/native_qualification.json'),'from_pipeline_sha256':file_hash(oldpath),'to_pipeline_sha256':file_hash(p/'contracts/pipeline_integrity.json'),'original_pipeline_path':'contracts/original.json','changed_files':['scripts/advance_batch1.py']}
   write_json(p/'contracts/orchestration_migration.json',m)
   self.assertTrue(qualified_pipeline_matches(p,q))
   science.write_text('changed physics');self.assertFalse(qualified_pipeline_matches(p,q))
