"""Per-node read-only import/link audit, without generating an IC or history."""
import ctypes
import importlib.metadata
import os
from pathlib import Path
import platform
import subprocess
import sys
from .contracts import digest,file_hash,verify_sources
from .data_control import read_json

def command(argv):
    try:
        r=subprocess.run(argv,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
        return {'exit_code':r.returncode,'output':r.stdout}
    except (OSError,subprocess.TimeoutExpired) as e:return {'exit_code':None,'error':str(e)}

def inspect_runtime(project):
    root=Path(project);c=read_json(root/'contracts/science_contract.json');sel=read_json(root/'contracts/selected_native_contract.json')
    r={'host':platform.node(),'platform':platform.platform(),'python':sys.version,'python_executable':sys.executable,'glibc':platform.libc_ver(),'slurm_job_id':os.environ.get('SLURM_JOB_ID'),'slurm_cpus_per_task':os.environ.get('SLURM_CPUS_PER_TASK'),'is_compute_allocation':bool(os.environ.get('SLURM_JOB_ID')),'native_path':sel['native_path'],'native_sha256':file_hash(sel['native_path']),'source_fingerprint':sel['source_fingerprint'],'science_contract_hash':digest(c),'linked_libraries':command(['ldd',sel['native_path']]),'compiler_available_not_build_provenance':command(['gcc','--version']),'unsigned_long_bytes':ctypes.sizeof(ctypes.c_ulong),'unsigned_long_long_bytes':ctypes.sizeof(ctypes.c_ulonglong),'requested_seed':c['ic_target']['seed'],'full_evaluations':0}
    r['imported_package_path']=None;r['loaded_native_path']=None
    import re
    libraries={path for path in re.findall(r'/[^\s()]+',r['linked_libraries'].get('output','')) if Path(path).is_file()}
    r['dynamic_dependency_sha256']={str(Path(path).resolve()):file_hash(path) for path in sorted(libraries)}
    r['packages']={}
    for name in ['numpy','scipy','cffi','astropy','h5py']:
        try:r['packages'][name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:r['packages'][name]=None
    try:
        verify_sources(c)
        for path,sha in sel.get('physics_table_sha256',{}).items():
            if file_hash(path)!=sha:raise ValueError('Frozen physical table changed: '+path)
        from .runtime import import_native
        native=import_native(c['native_python_root'])
        import py21cmfast as p21
        r['imported_package_path']=str(Path(p21.__file__).resolve());r['loaded_native_path']=str(Path(native.__file__).resolve())
        if file_hash(native.__file__)!=c['native_sha256']:raise ValueError('Loaded wrong native')
        r['loaded_native_sha256']=file_hash(native.__file__)
        r['process_mapped_libraries']=[line.strip() for line in Path('/proc/self/maps').read_text().splitlines() if '.so' in line and any(x in line for x in ['21cmfast','libgsl','libfftw','libgomp','libc.so','libm.so'])]
        user=p21.UserParams(c['simulation_settings']['user_params']);flags=p21.FlagOptions(c['simulation_settings']['flag_options'])
        r['resolved_user_params']=dict(user.self);r['resolved_flag_options']=dict(flags.self)
        r['global_params']={k:v for k,v in p21.global_params.items() if isinstance(v,(str,int,float,bool,type(None)))}
        # ABI representation only, no manual seed modulo and no random-field generation.
        r['initial_conditions_C_signature']=native.ffi.typeof(native.lib.ComputeInitialConditions).cname
        r['cffi_seed_argument']=int(native.ffi.cast('unsigned long long',c['ic_target']['seed']))
        r['effective_returned_seed']=None
        r['import_passed']=True
    except Exception as e:
        r.update(import_passed=False,error=repr(e),effective_returned_seed=None)
    identity={k:r[k] for k in ['python_executable','python','glibc','native_sha256','source_fingerprint','packages','unsigned_long_bytes','unsigned_long_long_bytes','dynamic_dependency_sha256']}
    import re
    identity['ldd']=re.sub(r'\(0x[0-9a-fA-F]+\)', '(address)', r['linked_libraries'].get('output',''))
    r['runtime_fingerprint']=digest(identity)
    r['approved_runtime']=sel.get('compatible_runtime_approved',False) and r['runtime_fingerprint'] in sel.get('allowed_runtime_fingerprints',[])
    r['qualified_for_full_simulation']=r['import_passed'] and r['is_compute_allocation'] and r['unsigned_long_bytes']==8 and r['unsigned_long_long_bytes']==8 and r['approved_runtime'] and sel['confirmed']
    r['status']='RUNTIME_READY' if r['qualified_for_full_simulation'] else 'BLOCKED'
    return r
