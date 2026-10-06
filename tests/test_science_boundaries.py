import copy,json,tempfile,unittest
from pathlib import Path
import numpy as np
import torch
from bt_history.contracts import read_contract,parameters,validate_history,digest,ContractError,DomainError
from bt_history.transforms import Normalizer,logit,fit_pca
from bt_history.resmlp import ReionizationHistoryEmulator
from bt_history.history_decoders import DirectDecoder,ResidualDecoder
from bt_history.history_provider import HistoryProvider
from bt_history.history_dataset import split_groups,group_id,load_development,validate_row
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.exact_history_adapter import ExactHistoryAdapter
from bt_history.metrics import posterior_reweight,representation_audit
ROOT=Path(__file__).resolve().parents[1]

class ScienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        cls.c=read_contract(ROOT/'contracts/fixed/science_contract.json')
        cls.p={k:sum(v)/2 for k,v in cls.c['prior_support'].items()}
        cls.z=np.array(cls.c['redshift_grid']); cls.x=np.linspace(0,1,len(cls.z))
        cls.post=OriginalPostprocessingAdapter(cls.c)
    def test_grid_not_ps_contract(self):
        self.assertEqual(len(self.z),32);self.assertIn(5.9,self.z);self.assertFalse(np.allclose(np.diff(self.z),np.diff(self.z)[0]))
    def test_strict_history(self):
        for x in [np.full(32,np.nan),np.full(32,1.01),np.zeros(31)]:
            with self.assertRaises(ContractError):validate_history(self.c,self.z,x)
        with self.assertRaises(ContractError):validate_history(self.c,self.z[::-1],self.x[::-1])
        validate_history(self.c,self.z,np.zeros(32));validate_history(self.c,self.z,np.ones(32))
    def test_parameter_domain(self):
        parameters(self.c,self.p)
        with self.assertRaises(DomainError):parameters(self.c,{**self.p,'KP':10})
        with self.assertRaises(DomainError):parameters(self.c,{**self.p,'F_STAR10':np.nan})
    def test_log_coordinates_not_logged_twice(self):
        x=np.stack([list(self.p.values()),list(self.p.values())]);x[1,0]+=.1
        n=Normalizer.fit(x,split='train');self.assertTrue(np.isfinite(n.transform(x)).all());self.assertAlmostEqual(n.mean[0],self.p['F_STAR10']+.05)
        with self.assertRaises(ValueError):Normalizer.fit(x,split='validation')
    def test_pca_train_only_and_full_rank(self):
        x=np.random.default_rng(2).normal(size=(40,32));mean,b=fit_pca(x,32,split='train')
        np.testing.assert_allclose(mean+(x-mean)@b.T@b,x,atol=1e-12)
        with self.assertRaises(ValueError):fit_pca(x,2,split='test')
    def test_no_tau_head_and_physical_training(self):
        m=ReionizationHistoryEmulator(8,32);x=torch.randn(3,8);y=m(x)
        self.assertEqual(y.shape,(3,32));self.assertTrue(((y>=0)&(y<=1)).all())
        self.assertFalse(any('tau' in k for k in m.state_dict()))
        ((y-torch.zeros_like(y))**2).mean().backward();self.assertIsNotNone(m.net[0].weight.grad)
    def test_residual_gates(self):
        with self.assertRaises(ValueError):ResidualDecoder(compatibility_passed=False)
        with self.assertRaises(ValueError):ResidualDecoder(compatibility_passed=True,mean=np.zeros(32),basis=np.eye(32))
        d=ResidualDecoder(compatibility_passed=True);p=torch.full((2,32),.3)
        torch.testing.assert_close(d(torch.zeros_like(p),p),p)
        q=torch.tensor([[0.,1.]]);v=d(torch.zeros_like(q),q);self.assertGreater(v[0,0],0);self.assertLess(v[0,1],1)
    def test_tau_delegate_exact_arguments(self):
        seen={}
        def stub(**kw):seen.update(kw);return .055
        r=self.post.evaluate(self.p,self.z,self.x,compute_tau_fn=stub)
        np.testing.assert_array_equal(seen['redshifts'],np.linspace(5,35,31))
        np.testing.assert_allclose(seen['global_xHI'],np.interp(seen['redshifts'],self.z,self.x))
        self.assertEqual(r['tau'],.055)
    def test_original_likelihood_parity_both_tau_sides_penalty(self):
        t=self.c['likelihood']['planck_tau'];n=self.c['likelihood']['neutral_fraction']
        for tau in [t['mean']-.01,t['mean']+.01]:
            x=np.full(32,.3);r=self.post.evaluate(self.p,self.z,x,compute_tau_fn=lambda **kw:tau)
            expected=self.post.module.loglike_split_normal_tau(tau,mean=t['mean'],sigma_upper=t['sigma_upper'],sigma_lower=t['sigma_lower'])
            self.assertEqual(r['logL_tau'],expected);self.assertLess(r['logL_xHI'],0)
            self.assertAlmostEqual(r['logL_xHI'],-.5*((.3-n['threshold'])/n['sigma_above_threshold'])**2)
    def test_exact_adapter_keeps_physics_and_mean(self):
        seen={}
        from types import SimpleNamespace
        def run(**kw):
            seen.update(kw);return [SimpleNamespace(redshift=z,xH_box=np.array([.1,.3],dtype=np.float32)) for z in kw['redshift']]
        a=ExactHistoryAdapter(self.c,'/tmp/bt_history_test_scratch',run_coeval_fn=run)
        r=a.predict_history(self.p)
        self.assertTrue(seen['flag_options']['USE_TS_FLUCT']);self.assertFalse(seen['EVOLVE_DENSITY_LINEARLY']);self.assertFalse(seen['write']);self.assertTrue(seen['regenerate'])
        np.testing.assert_array_equal(r.global_xHI,np.full(32,np.mean(np.array([.1,.3],np.float32),dtype=np.float64)))
    def test_continuous_ms_context(self):
        c=read_contract(ROOT/'contracts/continuous_ms/science_contract.json');p={k:sum(v)/2 for k,v in c['prior_support'].items()}
        post=OriginalPostprocessingAdapter(c);_,cosmo=post.context(p);self.assertEqual(cosmo['MS'],p['MS']);self.assertEqual(cosmo['KP'],c['cosmology']['hlittle'])
    def test_physical_ensemble_mean(self):
        class Constant(torch.nn.Module):
            def __init__(self,v):super().__init__();self.v=v
            def forward(self,x):return torch.full((len(x),32),self.v)
        n=Normalizer(np.zeros(8),np.ones(8))
        provider=HistoryProvider(self.c,[Constant(.1),Constant(.5)],n,model_version='test',development=True,coverage=lambda p:True)
        np.testing.assert_allclose(provider.predict_history(self.p).global_xHI,.3)
        with self.assertRaises(ValueError):HistoryProvider(self.c,[Constant(.1)],n,model_version='test',coverage=lambda p:True)
    def test_coverage_failure_not_negative_infinity(self):
        provider=HistoryProvider(self.c,[ReionizationHistoryEmulator(8,32)],Normalizer(np.zeros(8),np.ones(8)),model_version='test',development=True,coverage=lambda p:False)
        with self.assertRaises(DomainError):provider.predict_history(self.p)
    def test_group_split_all_ic_together(self):
        rows=[{'sample_id':f'{i}_{seed}','physical_parameters':{'a':i},'ic_seed':seed} for i in range(10) for seed in [1,2]]
        s=split_groups(rows)
        for i in range(10):self.assertEqual(s[f'{i}_1'],s[f'{i}_2'])
    def test_sealed_rejected_before_label_open(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'manifest.json';p.write_text(json.dumps({'role':'sealed','science_contract_hash':digest(self.c),'files':[{'path':'DO_NOT_OPEN'}]}))
            with self.assertRaises(ContractError):load_development(p,self.c,self.post)
    def test_logit_rejects_bad_labels(self):
        with self.assertRaises(ValueError):logit([-1,.2],1e-5)
        self.assertTrue(np.isfinite(logit([0,1],1e-5)).all())
    def test_weight_degeneracy_reported(self):
        r=posterior_reweight([1000,0,0],[0,0,0],[[0,1],[1,2],[2,3]])
        self.assertEqual(r['ESS'],1);self.assertFalse(r['posterior_passed'])

if __name__=='__main__':unittest.main()
