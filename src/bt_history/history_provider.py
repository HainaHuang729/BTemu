import numpy as np
import torch
from .contracts import parameters, digest, DomainError, validate_history
from .exact_history_adapter import History

class HistoryProvider:
    def __init__(self, contract, models, normalizer, *, model_version, accepted=False, development=False, coverage=None, exact_fallback=None, journal=None):
        if not accepted and not development:
            raise ValueError('Unaccepted model cannot be deployed')
        if not models:
            raise ValueError('Empty ensemble')
        if accepted and len(models) != 5:
            raise ValueError('Production requires all five registered seeds')
        if coverage is None:
            raise ValueError('Explicit validated coverage predicate required')
        self.c, self.models, self.norm = contract, [m.eval() for m in models], normalizer
        self.version, self.coverage = model_version, coverage
        self.fallback, self.journal = exact_fallback, journal
        if exact_fallback is not None and journal is None:
            raise ValueError('Exact fallback requires a persistent event journal')

    def predict_history(self, parameter_dict):
        x = parameters(self.c, parameter_dict)  # invalid scientific prior never converted to -inf
        try:
            if not self.coverage(parameter_dict):
                raise DomainError('Outside validated training coverage')
            tensor = torch.as_tensor(self.norm.transform(x)[None], dtype=torch.float32)
            with torch.no_grad():
                members = np.stack([m(tensor).cpu().numpy()[0] for m in self.models])
            for member in members:
                validate_history(self.c, self.c['redshift_grid'], member)
            mean = members.mean(axis=0, dtype=np.float64)  # physical-space mean
            return History(np.asarray(self.c['redshift_grid']), mean, self.version, digest(self.c), True,
                {'member_std': members.std(0).tolist(), 'uncertainty_calibrated': False, 'ic_variance': False})
        except (DomainError, FloatingPointError, ValueError) as error:
            if self.fallback is None:
                raise
            self.journal({'event':'exact_fallback','reason':str(error),'parameters':dict(parameter_dict)})
            return self.fallback.predict_history(parameter_dict)

class BoundHistoryProvider:
    """Expose the shared 10D emulator through either original inference view."""
    def __init__(self, shared, view_contract):
        self.shared, self.c = shared, view_contract
        keys=['redshift_grid','ic_target','native_sha256','simulation_settings','astro_parameter_order']
        if any(shared.c[k]!=view_contract[k] for k in keys):
            raise ValueError('Inference view incompatible with shared emulator')
        for k in ['OMm','OMb','hlittle','SIGMA_8','POWER_INDEX']:
            if shared.c['cosmology'][k]!=view_contract['cosmology'][k]:
                raise ValueError('Inference view cosmology mismatch')
    def predict_history(self, parameter_dict):
        parameters(self.c,parameter_dict)
        p={**parameter_dict,**self.c['fixed_parameters']}
        history=self.shared.predict_history(p)
        return History(history.redshifts,history.global_xHI,history.model_version,digest(self.c),history.in_domain,
            {**history.diagnostics,'shared_science_contract_hash':history.science_contract_hash})
