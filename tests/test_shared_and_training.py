import json,tempfile,unittest
from pathlib import Path
import numpy as np
import torch
from bt_history.contracts import read_contract,parameters,DomainError,digest
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.history_provider import HistoryProvider,BoundHistoryProvider
from bt_history.resmlp import ReionizationHistoryEmulator
from bt_history.transforms import Normalizer
from bt_history.training import train
from bt_history.inference import load_development_provider
from bt_history.metrics import trajectory_bootstrap,acceptance_gates
ROOT=Path(__file__).resolve().parents[1]

class SharedTests(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1);self.c=read_contract(ROOT/'contracts/science_contract.json')
        self.p={k:sum(v)/2 for k,v in self.c['prior_support'].items()}
    def test_shared_10d_units_and_ranges(self):
        self.assertEqual(len(self.c['parameter_order']),10)
        self.assertEqual(self.c['prior_support']['KP_h_Mpc'],[1,30]);self.assertEqual(self.c['prior_support']['MS'],[.5,4])
        post=OriginalPostprocessingAdapter(self.c);_,cosmo=post.context(self.p)
        self.assertAlmostEqual(cosmo['KP'],self.p['KP_h_Mpc']*cosmo['hlittle'])
        with self.assertRaises(DomainError):parameters(self.c,{**self.p,'KP_h_Mpc':31})
    def test_original_views_bind_to_one_model(self):
        shared=HistoryProvider(self.c,[ReionizationHistoryEmulator(10,32)],Normalizer(np.zeros(10),np.ones(10)),model_version='test',development=True,coverage=lambda p:True)
        for name in ['fixed','continuous_ms']:
            c=read_contract(ROOT/'contracts'/name/'science_contract.json');p={k:sum(v)/2 for k,v in c['prior_support'].items()}
            bound=BoundHistoryProvider(shared,c);h=bound.predict_history(p)
            self.assertEqual(h.science_contract_hash,digest(c));self.assertEqual(h.global_xHI.shape,(32,))
    def test_bootstrap_unit(self):
        r=trajectory_bootstrap([1,1,2,2,3,3],['a','a','b','b','c','c'],resamples=20)
        self.assertEqual(r['resampling_unit'],'physical-parameter group')
    def test_five_seed_training_checkpoint_roundtrip_synthetic_only(self):
        c=self.c;rng=np.random.default_rng(2);rows=[]
        class FakePost:
            def evaluate(self,p,z,x):
                # Software fixture only: this is explicitly NOT the physical tau pipeline.
                v=float(np.mean(x));return {'tau':v,'xHI_obs':float(x[0]),'logL_tau':-v*v,'logL_xHI':-float(x[0])**2,'logL_joint_history':-v*v-float(x[0])**2}
        for i in range(16):
            p={k:float(rng.uniform(*v)) for k,v in c['prior_support'].items()}
            rows.append({'sample_id':str(i),'physical_parameters':p,'global_xHI':np.linspace(.1,.9,32).tolist()})
        split={str(i):'train' if i<12 else 'validation' for i in range(16)}
        cfg=json.loads((ROOT/'configs/training.json').read_text());cfg.update(epochs=2,minimum_train_groups=10,minimum_validation_groups=4,batch_size=4)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'synthetic';m=train(c,rows,split,cfg,root,FakePost())
            self.assertEqual(len(m['members']),5);self.assertFalse(m['production_accepted'])
            provider=load_development_provider(c,root,lambda p:True);h=provider.predict_history(rows[0]['physical_parameters'])
            self.assertEqual(h.global_xHI.shape,(32,))
            (root/'normalizer.json').write_text('{}')
            with self.assertRaises(ValueError):load_development_provider(c,root,lambda p:True)

if __name__=='__main__':unittest.main()
