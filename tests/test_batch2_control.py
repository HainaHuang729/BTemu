import unittest,tempfile,json,sys,importlib.util
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from bt_history.data_control import write_json,AttemptLedger
s=importlib.util.spec_from_file_location('batch2',ROOT/'scripts/advance_dataset.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_first_wave_validation_only_and_eight(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);b={'budget_id':'test','max_total_core_hours':2000,'max_concurrent_tasks':8,'stages':{st:{'manifests':['manifests/'+st+'.jsonl'],'allowed_indices':list(range(10)),'max_retry_attempts':16,'max_retries_per_sample':1,'cpus':16,'wall_seconds':7200} for st in ['train','validation']}}
   write_json(p/'b.json',b);write_json(p/'results/native_qualification.json',{'qualified_for_batch1':True});write_json(p/'manifests/qualified_history_recovered_v1.json',{'files':[]})
   def design(root,path):return [{'sample_id':Path(path).stem+str(i)} for i in range(10)]
   class Result:returncode=0;stdout='12345';stderr=''
   with patch.object(m,'qualified_pipeline_matches',return_value=True),patch.object(m,'verify_design',side_effect=design),patch.object(m.subprocess,'run',return_value=Result()) as submit:
    m.main(p,p/'b.json')
   cmd=submit.call_args[0][0];self.assertEqual(cmd[cmd.index('--stage')+1],'validation');self.assertEqual(cmd[cmd.index('--indices')+1],'0,1,2,3,4,5,6,7')
 def test_shared_cap_cannot_be_doubled_across_stages(self):
  with tempfile.TemporaryDirectory() as d:
   ledger=AttemptLedger(d);a={'attempt_id':'train0','sample_id':'t','stage':'train','reserved_core_hours':32}
   (Path(d)/'attempts.jsonl').write_text(json.dumps(a)+'\n');write_json(Path(d)/'receipts/train0.json',{'qualified':True})
   spec={'cpus':16,'wall_seconds':7200,'max_attempts':100,'global_max_attempts':100,'max_concurrent':8,'global_max_concurrent':8,'max_reserved_core_hours':2000,'global_max_reserved_core_hours':32,'max_retry_attempts':16}
   with self.assertRaisesRegex(PermissionError,'Shared allocation'):ledger.reserve({'sample_id':'v','family_id':'v'},'validation',spec,budget_hash='b',contract_hash='c')
if __name__=='__main__':unittest.main()
