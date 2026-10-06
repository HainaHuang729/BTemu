import unittest
from bt_history.contracts import digest
from bt_history.data_control import retry_authorized
class ScopedReplayTests(unittest.TestCase):
 def test_exact_approved_attempt_only(self):
  a={'attempt_id':'preflight_0000003','sample_id':'preflight_PL1_original'};r={'simulation_status':'numerical_failure','reason':'probe initialization'}
  s={'allowed_retry_statuses':['infrastructure_failure'],'retry_sample_allowlist':[a['sample_id']],'explicit_retry_exceptions':[{**a,'receipt_digest':digest(r),'approval_reference':'user_explicit'}]}
  self.assertTrue(retry_authorized(s,a,r))
  self.assertFalse(retry_authorized(s,{**a,'attempt_id':'next'},r))
  self.assertFalse(retry_authorized(s,a,{**r,'reason':'actual numerical failure'}))
  self.assertFalse(retry_authorized({**s,'explicit_retry_exceptions':[]},a,r))
 def test_unknown_numerical_failure_never_auto_retries(self):
  self.assertFalse(retry_authorized({'allowed_retry_statuses':['infrastructure_failure']},{'attempt_id':'x','sample_id':'p'},{'simulation_status':'numerical_failure'}))
