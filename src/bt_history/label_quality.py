"""Mechanical QA; retain unmodified values and distinguish warnings from failures."""
import json
from pathlib import Path
import numpy as np
from .contracts import parameters,validate_history,digest,file_hash,ContractError
from .data_control import read_json,assert_development_path

class QualityError(ContractError):pass

def validate_label(c,row,design,selected,protocol,post):
    for key in ['sample_id','family_id','split','stratum','design_version','design_seed','canonical_parameters']:
        if row.get(key)!=design.get(key):raise QualityError('Frozen design mismatch: '+key)
    parameters(c,row['canonical_parameters'])
    if row['native_sha256']!=selected['native_sha256'] or row['source_fingerprint']!=selected['source_fingerprint'] or row['config_hash']!=digest(c) or row['postprocessing_hash']!=selected['postprocessing_hash']:raise QualityError('Provenance mismatch')
    if row.get('physics_table_fingerprint')!=selected.get('physics_table_fingerprint'):raise QualityError('Physical table identity mismatch')
    seed=c['ic_target']['seed']
    if row['requested_ic_seed']!=seed or row['effective_ic_seed']!=seed:raise QualityError('Requested/effective seed mismatch or missing')
    if row['simulation_status']!='success':raise QualityError('Not a successful simulation')
    x=np.asarray(row['global_xHI'],float);z=np.asarray(row['redshifts'],float)
    if x.shape!=z.shape or not np.isfinite(x).all():raise QualityError('Nonfinite or incomplete label')
    if np.any((x<0)|(x>1)):
        tol=protocol['range']['tiny_excursion_tolerance']
        raise QualityError('tiny_range_excursion_quarantine' if np.all((x>=-tol)&(x<=1+tol)) else 'numerical_range_failure')
    validate_history(c,z,x)
    d=post.evaluate(row['canonical_parameters'],z,x)
    q=protocol['saved_derived_parity']
    if not np.isfinite(row['tau_exact_derived']) or abs(d['tau']-row['tau_exact_derived'])>q['tau_absolute_tolerance']:raise QualityError('Saved tau cannot be reproduced')
    obs=str(c['likelihood']['neutral_fraction']['redshift'])
    if not np.isfinite(row['xHI_at_observation_redshifts'][obs]) or abs(d['xHI_obs']-row['xHI_at_observation_redshifts'][obs])>q['observed_xHI_absolute_tolerance']:raise QualityError('Saved xHI interpolation cannot be reproduced')
    flags=[];e=protocol['endpoint_warnings']
    if 1-x[-1]>e['z35_ionized_fraction_gt']:flags.append('z35_already_ionized')
    if x[0]>e['z5_neutral_fraction_gt']:flags.append('z5_neutral_low_z_extension_conflict')
    return {'qualified':True,'quality_flags':flags,'status':'science_domain_warning' if flags else 'success'}

def classify_failure(error):
    text=str(error).lower()
    if isinstance(error,(ImportError,ModuleNotFoundError)) or any(x in text for x in ['glibc','cannot open shared object','native load']):return 'runtime_native_load_failure'
    if isinstance(error,MemoryError) or 'out of memory' in text:return 'out_of_memory'
    if isinstance(error,TimeoutError):return 'timeout'
    if type(error).__module__.startswith('py21cmfast'):return 'numerical_failure'
    if isinstance(error,QualityError):return 'schema_provenance_failure'
    if isinstance(error,ContractError) and 'Invalid history' in str(error):return 'numerical_failure'
    if isinstance(error,ContractError):return 'schema_provenance_failure'
    if isinstance(error,OSError):
        import errno
        if error.errno in {errno.EIO,errno.ESTALE,errno.ETIMEDOUT,errno.EAGAIN}:return 'infrastructure_failure'
        return 'schema_provenance_failure'
    if isinstance(error,FloatingPointError) or any(x in text for x in ['nan','infinity','gsl','integration','nonfinite','range']):return 'numerical_failure'
    return 'schema_provenance_failure'

def validate_development_file(project,path,manifest,sample_id,checksum):
    from .data_control import verify_design
    from .original_postprocessing_adapter import OriginalPostprocessingAdapter
    root=Path(project);design=next(r for r in verify_design(root,manifest) if r['sample_id']==sample_id)
    assert_development_path(path,design['split'])
    if file_hash(path)!=checksum:raise QualityError('Checksum mismatch')
    c=read_json(root/'contracts/science_contract.json');r=read_json(path)
    return validate_label(c,r,design,read_json(root/'contracts/selected_native_contract.json'),read_json(root/'contracts/data_quality_protocol.json'),OriginalPostprocessingAdapter(c))
