"""Offline scientific contract tests; no native calls or simulation fixtures."""
import json,sys,unittest,tempfile,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'maintenance/ic_audit'))
from common import policy,rows
from bt_history.data_control import AttemptLedger
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter

@unittest.skipUnless(json.loads((ROOT/'configs/ic_audit_budget.json').read_text()).get('authorized',False),'Approved production-workspace audit gate required; public submission template is disabled')
class ICAuditTests(unittest.TestCase):
 def test_original_likelihood_cut_and_equality(self):
  c,a,b,s=policy(False);post=OriginalPostprocessingAdapter(c);cut=json.loads((ROOT/'contracts/classifier_cut.json').read_text())
  z=np.array(c['redshift_grid']);x=np.full(len(z),cut['cut'])
  self.assertAlmostEqual(post.module.loglike_neutral_fraction(z,x,target_redshift=5.9,threshold=.06,sigma=.05),-12.5)
  self.assertEqual(post.module.loglike_neutral_fraction(z,np.zeros_like(x)),0.)
  self.assertEqual(int(float(x[0])<cut['cut']),0)
 def test_frozen_families_and_independent_seeds(self):
  r=rows();fresh=[x for x in r if not x['reuse_fixed_reference']]
  self.assertEqual(len(r),1024);self.assertEqual(len(fresh),896)
  self.assertEqual(len({x['requested_ic_seed'] for x in fresh}),896)
  self.assertEqual(len({x['requested_ic_seed']&0xffffffff for x in fresh}|{725213656658&0xffffffff}),897)
  self.assertTrue(all(1<=x['requested_ic_seed']<2**31 for x in fresh))
  for f in {x['family_id'] for x in r}:
   group=[x for x in r if x['family_id']==f]
   self.assertEqual(len(group),8);self.assertEqual(sum(x['reuse_fixed_reference'] for x in group),1)
   self.assertEqual(len({json.dumps(x['canonical_parameters'],sort_keys=True) for x in group}),1)
   self.assertEqual(len({x['source_split'] for x in group}),1)
   self.assertTrue(all(x['split']=='challenge_development' for x in group))
 def test_audit_ledger_does_not_retry_numerical_failures(self):
  c,a,b,s=policy(False);r=rows()[1]
  with tempfile.TemporaryDirectory() as tmp:
   ledger=AttemptLedger(tmp);at=ledger.reserve(r,'ic_audit',s,budget_hash='test',contract_hash='test')
   ledger.finish(at,{'simulation_status':'numerical_failure','qualified':False})
   with self.assertRaises(PermissionError):ledger.reserve(r,'ic_audit',s,budget_hash='test',contract_hash='test')
 def test_one_infrastructure_retry_then_stop(self):
  c,a,b,s=policy(False);r=rows()[1]
  with tempfile.TemporaryDirectory() as tmp:
   ledger=AttemptLedger(tmp)
   for _ in range(2):
    at=ledger.reserve(r,'ic_audit',s,budget_hash='test',contract_hash='test');ledger.finish(at,{'simulation_status':'infrastructure_failure','qualified':False})
   with self.assertRaises(PermissionError):ledger.reserve(r,'ic_audit',s,budget_hash='test',contract_hash='test')
if __name__=='__main__':unittest.main()
