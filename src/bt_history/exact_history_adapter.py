"""Unmodified TS-on coeval path; no cross-parameter field cache."""
from dataclasses import dataclass
import numpy as np
from .contracts import parameters, validate_history, digest
from .original_postprocessing_adapter import OriginalPostprocessingAdapter

@dataclass
class History:
    redshifts: np.ndarray
    global_xHI: np.ndarray
    model_version: str
    science_contract_hash: str
    in_domain: bool
    diagnostics: dict

class ExactHistoryAdapter:
    def __init__(self, contract, scratch, *, run_coeval_fn=None, verify=True):
        self.c, self.scratch, self.run = contract, str(scratch), run_coeval_fn
        self.post = OriginalPostprocessingAdapter(contract, verify=verify)

    def predict_history(self, parameter_dict):
        parameters(self.c, parameter_dict)
        user, cosmo = self.post.context(parameter_dict)
        run = self.run
        if run is None:
            self.post.check_native()
            from py21cmfast import run_coeval
            run = run_coeval
        astro = {k: parameter_dict[k] for k in self.c['astro_parameter_order']}
        coevals = run(redshift=self.c['redshift_grid'], user_params=user, cosmo_params=cosmo,
            astro_params=astro, flag_options=self.c['simulation_settings']['flag_options'],
            random_seed=self.c['ic_target']['seed'], direc=self.scratch,
            write=False, regenerate=True, cleanup=True,
            **self.c['simulation_settings']['global_overrides'])
        pairs = sorted((float(v.redshift), float(np.mean(v.xH_box, dtype=np.float64))) for v in coevals)
        z, x = np.asarray(pairs).T
        validate_history(self.c, z, x)
        return History(z, x, 'exact', digest(self.c), True, {'ic_seed': self.c['ic_target']['seed'], 'requested_ic_seed': self.c['ic_target']['seed'], 'effective_ic_seeds': sorted({int(v.random_seed) for v in coevals if getattr(v, 'random_seed', None) is not None})})
