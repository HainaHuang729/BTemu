import sys,unittest,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'maintenance'))
from semantic_audit import component_metadata,summary,endpoint_metrics
class Tests(unittest.TestCase):
 def fixture(self):
  c={'redshift_grid':[5.,5.9,35.],'likelihood':{'neutral_fraction':{'redshift':5.9}}};r={'redshifts':[5.,5.9,35.],'global_xHI':[.2,.3,.8],'exact_tau':.07,'exact_xHI_at_observation_redshifts':{'5.9':.3},'split':'train'};return c,r
 def test_neutral_endpoints_do_not_invalidate(self):
  c,r=self.fixture();m=component_metadata(c,r);self.assertTrue(m['history_valid']);self.assertTrue(m['tau_valid']);self.assertTrue(m['zmin_neutral_warning']);self.assertTrue(m['zmax_ionized_warning']);self.assertEqual(r['global_xHI'],[.2,.3,.8])
 def test_lf_failure_preserves_history(self):
  c,r=self.fixture();r['original_end_to_end_success']=False;m=component_metadata(c,r);self.assertTrue(m['history_valid']);self.assertFalse(m['lf_valid']);self.assertFalse(m['joint_likelihood_valid'])
 def test_true_invalid_history_rejected(self):
  c,r=self.fixture();r['global_xHI'][0]=np.nan
  with self.assertRaises(ValueError):component_metadata(c,r)
 def test_endpoint_quantile_and_accuracy_reports(self):
  c,r=self.fixture();s=summary(c,[r]);self.assertEqual(s['by_split']['train']['xHI_zmin']['q50'],.2);m=endpoint_metrics(c,[r],np.array([r['global_xHI']]),{});self.assertEqual(m['endpoint_accuracy']['5.0']['RMSE'],0)
unittest.main()
