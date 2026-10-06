"""Internal, short-lived probe of exported frozen native functions; no IC fields."""
import ctypes,json,sys,faulthandler
faulthandler.enable()
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from bt_history.data_control import read_json,check_execution_gate,verify_design,AttemptLedger
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.runtime_qualification import inspect_runtime
def initialize_power_structs(native,user,cosmo):
    # sigma_z0 -> MtoR reads the separate UsefulFunctions global pointers.
    up,cp=user(),cosmo()
    native.lib.Broadcast_struct_global_PS(up,cp)
    native.lib.Broadcast_struct_global_UF(up,cp)
    return up,cp  # retain the C structs across all ctypes calls

project=Path(sys.argv[1]);budget,manifest,index,attempt_id,ledger_root=sys.argv[2:7];p=json.load(sys.stdin)
c,_,_=check_execution_gate(project,'preflight',budget,manifest)
row=verify_design(project,manifest)[int(index)]
if row['canonical_parameters']!=p or row['split']!='preflight':raise PermissionError('Probe design mismatch')
entries=[a for a in AttemptLedger(ledger_root).entries() if a['attempt_id']==attempt_id and a['sample_id']==row['sample_id']]
if len(entries)!=1 or not (Path(ledger_root)/('claimed_'+attempt_id)).exists():raise PermissionError('Probe has no reserved parent evaluation')
with (Path(ledger_root)/('probe_claimed_'+attempt_id)).open('x') as f:f.write('One probe charged to this reserved preflight allocation')
r=inspect_runtime(project)
if not r['qualified_for_full_simulation']:raise PermissionError('Probe requires confirmed native and approved compute runtime')
post=OriginalPostprocessingAdapter(c);post.check_native();user,cosmo=post.context(p)
import py21cmfast as p21
import py21cmfast.c_21cmfast as native
u=p21.UserParams(user);cp=p21.CosmoParams(cosmo)
_user_c,_cosmo_c=initialize_power_structs(native,u,cp)
lib=ctypes.CDLL(native.__file__)
lib.init_ps.argtypes=[];lib.init_ps.restype=ctypes.c_double
lib.power_in_k.argtypes=[ctypes.c_double];lib.power_in_k.restype=ctypes.c_double
lib.sigma_z0.argtypes=[ctypes.c_double];lib.sigma_z0.restype=ctypes.c_double
lib.free_ps.argtypes=[];lib.free_ps.restype=None
print('probe_phase=init_ps',file=sys.stderr,flush=True)
lib.init_ps()
try:
    k=np.geomspace(1e-3,100,32);mass=np.geomspace(1e8,1e12,8)
    print('probe_phase=power',file=sys.stderr,flush=True)
    power=[lib.power_in_k(float(v)) for v in k]
    print('probe_phase=sigma_z0',file=sys.stderr,flush=True)
    sigma=[lib.sigma_z0(float(v)) for v in mass]
    if not np.isfinite(power+sigma).all():raise FloatingPointError('Nonfinite power/variance')
    print(json.dumps({'k_1_Mpc':k.tolist(),'power_native':power,'mass_Msun':mass.tolist(),'sigma_z0':sigma,'native_sha256':c['native_sha256']}))
finally:lib.free_ps()
