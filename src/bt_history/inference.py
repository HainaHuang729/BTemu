"""Independent opt-in LF + original tau/xHI path; never starts a sampler."""
import importlib
import json
from pathlib import Path
import time
import torch
from .contracts import digest, file_hash, ContractError
from .history_provider import HistoryProvider
from .transforms import Normalizer
from .resmlp import ReionizationHistoryEmulator
from .original_postprocessing_adapter import OriginalPostprocessingAdapter

class JointEvaluator:
    def __init__(self,c,provider):
        self.c,self.provider=c,provider
        self.post=OriginalPostprocessingAdapter(c)
        mode='sampling.run_ms_joint_ts' if 'MS' in c['active_parameters'] else 'validation.web_fixed_bt_pilot'
        mod=importlib.import_module('workflows.MCMC.fixed_btps_posterior.'+mode)
        cfg=mod.configuration_for(c['original_plan'],0)
        lfmod=importlib.import_module('workflows.MCMC.fixed_btps_posterior.inference.exact_lf_provider')
        self.lf=lfmod.ExactLuminosityFunctionProvider('btps',configuration=cfg)
        self.likelihood=self.post.module.Non21Likelihood(cfg.contract_path)
        self.original=mod; self.config=cfg

    def evaluate(self,p):
        started=time.perf_counter(); history=self.provider.predict_history(p); history_seconds=time.perf_counter()-started
        if history.science_contract_hash!=digest(self.c): raise ContractError('Provider contract mismatch')
        t=time.perf_counter(); derived=self.post.evaluate(p,history.redshifts,history.global_xHI); post_seconds=time.perf_counter()-t
        astro={k:p[k] for k in self.c['astro_parameter_order']}; t=time.perf_counter()
        lfs=self.lf.predict(astro,**({'ms':p['MS']} if 'MS' in p else {})); lf_seconds=time.perf_counter()-t
        components=self.likelihood.evaluate(model_lfs=lfs,redshifts=history.redshifts,xhi=history.global_xHI,tau=derived['tau'])
        return {'components':components.as_dict(),'derived':derived,'timing':{'history_seconds':history_seconds,'tau_xhi_seconds':post_seconds,'LF_seconds':lf_seconds,'end_to_end_seconds':time.perf_counter()-started}}

    def sampler_callback(self,theta):
        prior=self.original.log_prior(theta,self.config)
        if not torch.isfinite(torch.tensor(prior)): return -float('inf')
        p=self.original.astro_from_theta(theta,self.config)
        if 'MS' in self.c['active_parameters']: p['MS']=float(theta[-1])
        # Domain/numerical errors propagate: never silently turn failures into zero prior.
        return prior+self.evaluate(p)['components']['total']

def load_development_provider(c,artifact,coverage):
    root=Path(artifact); m=json.loads((root/'model_manifest.json').read_text()); cfg=json.loads((root/'training_config.json').read_text())
    if m['science_contract_hash']!=digest(c): raise ContractError('Checkpoint contract mismatch')
    for name,key in [('normalizer.json','normalizer_sha256'),('training_config.json','training_config_sha256'),('split.json','split_sha256')]:
        if file_hash(root/name)!=m[key]: raise ContractError('Changed artifact '+name)
    models=[]
    if [r['seed'] for r in m['members']]!=cfg['seeds']: raise ContractError('Missing/reordered seeds')
    for r in m['members']:
        if file_hash(root/r['checkpoint'])!=r['sha256']: raise ContractError('Changed checkpoint')
        model=ReionizationHistoryEmulator(len(c['parameter_order']),len(c['redshift_grid']),**cfg['architecture'])
        model.load_state_dict(torch.load(root/r['checkpoint'],map_location='cpu',weights_only=True)); models.append(model)
    n=Normalizer(**json.loads((root/'normalizer.json').read_text()))
    return HistoryProvider(c,models,n,model_version=m['model_version'],development=True,coverage=coverage)
