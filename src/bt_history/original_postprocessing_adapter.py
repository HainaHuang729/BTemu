"""Delegate to frozen original functions; no alternative tau integrator."""
import importlib
import sys
import numpy as np
from .contracts import verify_sources, validate_history, parameters, ContractError, file_hash

class OriginalPostprocessingAdapter:
    def __init__(self, contract, *, verify=True):
        self.contract = contract
        if verify:
            verify_sources(contract)
        sys.path.insert(0, contract['original_project_root'])
        sys.path.insert(0, contract['native_python_root'])
        self.module = importlib.import_module('workflows.MCMC.fixed_btps_posterior.inference.non21_likelihood')

    def context(self, p):
        parameters(self.contract, p)
        cosmo = dict(self.contract['cosmology'])
        cosmo['MS'] = p.get('MS', self.contract['fixed_parameters'].get('MS'))
        if 'KP_h_Mpc' in p:
            cosmo['KP'] = p['KP_h_Mpc'] * cosmo['hlittle']
        return dict(self.contract['simulation_settings']['user_params']), cosmo

    def check_native(self):
        from .runtime import import_native
        native = import_native(self.contract['native_python_root'])
        if file_hash(native.__file__) != self.contract['native_sha256']:
            raise ContractError('Imported native is not the frozen target')

    def evaluate(self, p, z, x, *, compute_tau_fn=None):
        validate_history(self.contract, z, x)
        user, cosmo = self.context(p)
        if compute_tau_fn is None:
            self.check_native()
        convention = self.contract['tau_postprocessing_convention']
        tau = self.module.tau_from_history(z, x, user_params=user, cosmo_params=cosmo,
            compute_tau_fn=compute_tau_fn, **convention['arguments'])
        t = self.contract['likelihood']['planck_tau']
        n = self.contract['likelihood']['neutral_fraction']
        lt = self.module.loglike_split_normal_tau(tau, mean=t['mean'], sigma_upper=t['sigma_upper'], sigma_lower=t['sigma_lower'])
        lx = self.module.loglike_neutral_fraction(z, x, target_redshift=n['redshift'], threshold=n['threshold'], sigma=n['sigma_above_threshold'])
        # Same piecewise-linear interpolant as original neutral-fraction kernel.
        from scipy.interpolate import InterpolatedUnivariateSpline
        obs = float(InterpolatedUnivariateSpline(z, x, k=1)(n['redshift']))
        return {'tau': float(tau), 'xHI_obs': obs, 'logL_tau': float(lt), 'logL_xHI': float(lx), 'logL_joint_history': float(lt + lx)}
