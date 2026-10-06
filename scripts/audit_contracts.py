"""Read declared scientific sources only, never discover/open test labels."""
import argparse, importlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from bt_history.contracts import file_hash
ROOT = Path('/oss06/data/project/tkcastrosim/HNHuang/project_mcmc')
BASE = ROOT/'workflows/MCMC/fixed_btps_posterior'
OUT = Path(__file__).resolve().parents[1]

def write(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(x, indent=2, allow_nan=False)+'\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--native', choices=['repaired','audit'], required=True); a=ap.parse_args()
    sys.path.insert(0,str(ROOT))
    native_root = BASE/'deployments/ts_stable_strict_20260928/src' if a.native=='repaired' else ROOT/'software/21cmFAST/src'
    sys.path.insert(0,str(native_root))
    from workflows.MCMC.fixed_btps_posterior.inference.exact_lf_provider import ExactLuminosityFunctionProvider
    from workflows.MCMC.fixed_btps_posterior.inference.configuration import ASTRO_PARAMETER_ORDER
    summaries={}
    for variant, module, plan_name in [('fixed','validation.web_fixed_bt_pilot','joint_grid128_w16t16_20260922_e0.json'),('continuous_ms','sampling.run_ms_joint_ts','ms_joint_ts_w16t16_20260922_e0.json')]:
        mod=importlib.import_module('workflows.MCMC.fixed_btps_posterior.'+module)
        plan_path=BASE/'contracts'/plan_name
        plan=json.loads(plan_path.read_text()); cfg=mod.configuration_for(plan,0)
        lf=ExactLuminosityFunctionProvider('btps',configuration=cfg)
        ev=mod.Evaluator(plan,0,OUT/'results/scratch',16)
        active=list(ASTRO_PARAMETER_ORDER)+(['MS'] if variant=='continuous_ms' else [])
        support={k:list(cfg.prior_bounds(k)) for k in ASTRO_PARAMETER_ORDER}
        if variant=='continuous_ms': support['MS']=plan['ms_prior']
        native_path=next((native_root/'py21cmfast').glob('c_21cmfast*.so'))
        files=[Path(mod.__file__),BASE/'inference/non21_likelihood.py',BASE/'inference/exact_lf_provider.py',BASE/'inference/configuration.py',BASE/'inference/parameterization_v2.py',plan_path,native_path]
        # Freeze source tree, effective defaults, inherited contracts and external observations.
        files += sorted((native_root/'py21cmfast').glob('*.py'))
        files += sorted((native_root/'py21cmfast/src').glob('*.[ch]'))
        parent=cfg.contract_path
        while True:
            files.append(parent)
            document=json.loads(parent.read_text())
            if 'extends_contract' not in document: break
            parent=ROOT/document['extends_contract']['path']
        for row in cfg.non21_likelihood['luminosity_function']['files']:
            for key in ['data','noise']: files.append(ROOT/row[key])
        settings={'user_params':{**lf.user_params,'N_THREADS':16},'flag_options':lf.flag_options,'global_overrides':{'Z_HEAT_MAX':35.0,'EVOLVE_DENSITY_LINEARLY':False},
          'implicit_defaults':'Frozen inputs.py and native/global sources; runtime resolved-default export pending compatible compute host'}
        c={'contract_id':'bt_history_'+variant+'_v1','status':'implementation_frozen_scientific_acceptance_pending','production_authorized':False,
           'active_parameters':active,'fixed_parameters':{'KP_h_Mpc':plan['models'][0]['KP_h_Mpc'],**({'MS':2.5} if variant=='fixed' else {})},
           'parameter_order':active,'astro_parameter_order':list(ASTRO_PARAMETER_ORDER),
           'parameter_units':{k:('eV' if k=='NU_X_THRESH' else 'log10(erg/s per Msun/yr)' if k=='L_X' else 'log10(Msun)' if k=='M_TURN' else 'dimensionless') for k in active},
           'parameter_transforms':{k:('stored_log10_identity' if k in ['F_STAR10','F_ESC10','M_TURN','L_X'] else 'identity') for k in active},
           'sampler_order':list(mod.PARAMETERS),'sampler_mapping':'F_STAR10 = ETA_STAR + log10(t_STAR); preserve original prior density',
           'prior_support':support,'cosmology':lf.cosmo_params,
           'bt_definition':{'POWER_SPECTRUM':6,'formula':'P(k) proportional to k^ns T_EH(k)^2 below KP; k^MS KP^(ns-MS) T_EH(k)^2 above KP; native sigma8 normalization','KP_native_units':'1/Mpc','PL_limit':'MS=POWER_INDEX algebraically removes the break; POWER_SPECTRUM=0 is explicit local PL branch; no numerical parity claim'},
           'redshift_grid':ev.z.tolist(),'global_xHI_definition':'float64 volume mean of coeval xH_box; neutral hydrogen, not mass average or electron fraction',
           'tau_postprocessing_convention':{'function':'original non21_likelihood.tau_from_history -> native compute_tau','arguments':{'z_min':5.,'z_max':35.,'interpolation_points':31},'notes':'original linear spline + original clipping, float32 native input, original helium and low-z convention'},
           'ic_target':{'type':'fixed_ic','seed':plan['initial_condition_seed']},'simulation_settings':settings,
           'likelihood':dict(cfg.non21_likelihood),'original_project_root':str(ROOT),'native_python_root':str(native_root),'native_sha256':file_hash(native_path),
           'source_and_native_fingerprints':{str(p):file_hash(p) for p in files},
           'original_base_contract':str(cfg.contract_path),'original_plan':plan,'native_selection':a.native,
           'conflicts':['Parent base contract describes 84-node ensemble mean; actual TS-on sampler overrides to 32-node fixed IC. Actual sampler wins.', 'Old ExactCoevalIonizationHistoryProvider disables TS and linearizes density; deliberately not reused.', 'Audit native and repaired native must never be pooled. Repaired release metadata stale; regression_gate passed.']}
        write(OUT/'contracts'/variant/'science_contract.json',c)
        summaries[variant]={'path':variant+'/science_contract.json','parameters':active,'native_sha256':c['native_sha256']}
    write(OUT/'contracts/science_contract.json',{'variants':summaries,'shared_checkpoint':False})
if __name__=='__main__':main()
