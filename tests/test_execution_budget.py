import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from bt_history.data_control import AttemptLedger,write_json
from bt_history.label_quality import classify_failure
from bt_history.submission_accounting import submission_charges

class ExecutionTests(unittest.TestCase):
 def test_timeout_not_retryable_under_authorized_policy(self):
  with tempfile.TemporaryDirectory() as d:
   l=AttemptLedger(d);s={'max_attempts':12,'max_concurrent':1,'cpus':16,'wall_seconds':7200,'max_reserved_core_hours':384,'max_retries_per_sample':1,'max_retry_attempts':1,'allowed_retry_statuses':['infrastructure_failure']};r={'sample_id':'a','family_id':'a'}
   a=l.reserve(r,'preflight',s,budget_hash='x',contract_hash='x');l.finish(a,{'simulation_status':'timeout'})
   with self.assertRaises(PermissionError):l.reserve(r,'preflight',s,budget_hash='x',contract_hash='x')
 def test_releases_only_terminal_accounting(self):
  with tempfile.TemporaryDirectory() as d:
   l=AttemptLedger(d);a={'attempt_id':'a','reserved_core_hours':32}
   self.assertEqual(l.charged_core_hours([a]),32)
   write_json(Path(d)/'allocation_accounting.json',{'rows':[{'attempt_id':'a','terminal':False,'allocation_core_hours':1}]});self.assertEqual(l.charged_core_hours([a]),32)
   write_json(Path(d)/'allocation_accounting.json',{'rows':[{'attempt_id':'a','terminal':True,'allocation_core_hours':1}]});self.assertEqual(l.charged_core_hours([a]),1)
 def test_queued_and_unresolved_cost_full_reservation(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);write_json(root/'s_slurm.json',{'response':'100'})
   sub=[{'submission_id':'s','stage':'train','indices':[0,1,2]}];b={'stages':{'train':{'cpus':16,'wall_seconds':7200}}}
   class R:stdout='100_0|COMPLETED|3600|16\n100_1|RUNNING|300|16\n'
   with patch('bt_history.submission_accounting.subprocess.run',return_value=R()):r=submission_charges(root,sub,b)
   self.assertEqual([v['charged_core_hours'] for v in r],[16,32,32])
 def test_unknown_code_errors_not_automatic_infrastructure_retries(self):
  self.assertEqual(classify_failure(KeyError('missing_config')),'schema_provenance_failure')
  self.assertEqual(classify_failure(FileNotFoundError('path')),'schema_provenance_failure')

class ReplayScopeTests(unittest.TestCase):
 def test_one_named_preflight_retry_only(self):
  with tempfile.TemporaryDirectory() as d:
   l=AttemptLedger(d);s={'max_attempts':13,'max_concurrent':1,'cpus':16,'wall_seconds':7200,'max_reserved_core_hours':384,'max_retries_per_sample':1,'max_retry_attempts':1,'allowed_retry_statuses':['infrastructure_failure'],'retry_sample_allowlist':['preflight_normal_original']}
   bad={'sample_id':'preflight_other','family_id':'f'}
   a=l.reserve(bad,'preflight',s,budget_hash='x',contract_hash='x');l.finish(a,{'simulation_status':'infrastructure_failure'})
   with self.assertRaises(PermissionError):l.reserve(bad,'preflight',s,budget_hash='x',contract_hash='x')
   good={'sample_id':'preflight_normal_original','family_id':'g'}
   a=l.reserve(good,'preflight',s,budget_hash='x',contract_hash='x');l.finish(a,{'simulation_status':'infrastructure_failure'})
   replay=l.reserve(good,'preflight',s,budget_hash='x',contract_hash='x');self.assertEqual(replay['ordinal_for_sample'],2)
   l.finish(replay,{'simulation_status':'infrastructure_failure'})
   with self.assertRaises(PermissionError):l.reserve(good,'preflight',s,budget_hash='x',contract_hash='x')
