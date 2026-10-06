import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
from bt_history.data_control import write_json
from bt_history.submission_accounting import submission_charges,confirmed_array_rejection
class Tests(unittest.TestCase):
 def test_manifest_indices_map_to_local_slurm_accounting(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);write_json(root/'s_slurm.json',{'response':'123','submitted':True,'exit_code':0})
   sub={'submission_id':'s','stage':'train','indices':[1000,1001],'slurm_array_indices':[0,1]};b={'stages':{'train':{'cpus':16,'wall_seconds':7200}}}
   class R:stdout='123_0|COMPLETED|90|16\n123_1|RUNNING|10|16\n'
   with patch('bt_history.submission_accounting.subprocess.run',return_value=R()):rows=submission_charges(root,[sub],b)
   self.assertEqual(rows[0]['index'],1000);self.assertEqual(rows[0]['job_id'],'123_0');self.assertEqual(rows[0]['actual_core_hours'],.4);self.assertEqual(rows[1]['reserved_core_hours'],32)
 def test_only_explicit_rejection_releases_reservation(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);sub={'submission_id':'s','stage':'train','indices':[1000]};b={'stages':{'train':{'cpus':16,'wall_seconds':7200}}}
   write_json(root/'s_slurm.json',{'response':'','submitted':False,'exit_code':1,'stderr':'sbatch: error: Batch job submission failed: Invalid job array specification'})
   self.assertTrue(confirmed_array_rejection(root,sub));self.assertEqual(submission_charges(root,[sub],b)[0]['charged_core_hours'],0)
   write_json(root/'s_slurm.json',{'response':'','submitted':False,'exit_code':1,'stderr':'network unknown'})
   self.assertFalse(confirmed_array_rejection(root,sub));self.assertEqual(submission_charges(root,[sub],b)[0]['charged_core_hours'],32)
