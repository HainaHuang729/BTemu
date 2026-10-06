"""Recompute original tau/xHI on explicitly allowed development reports only."""
import argparse,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from bt_history.contracts import read_contract,file_hash,validate_history
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter
from bt_history.training import save_json
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--development-jsonl',required=True);p.add_argument('--expected-sha256',required=True);p.add_argument('--output',required=True);a=p.parse_args()
if file_hash(a.development_jsonl)!=a.expected_sha256:raise ValueError('Explicit development allowlist hash mismatch')
c=read_contract(a.contract);post=OriginalPostprocessingAdapter(c);rows=[]
for line in Path(a.development_jsonl).read_text().splitlines():
    row=json.loads(line)
    if row['provenance']['role']!='development_regression':raise ValueError('Not allowed development role')
    if row['simulation_status']!='ok':continue
    validate_history(c,row['redshifts'],row['global_xHI']);start=time.perf_counter()
    d=post.evaluate(row['physical_parameters'],row['redshifts'],row['global_xHI'])
    dt=d['tau']-row['exact_tau'];dx=d['xHI_obs']-row['exact_xHI_at_observation_redshifts']['5.9']
    rows.append({'sample_id':row['sample_id'],'delta_tau':dt,'delta_xHI_obs':dx,'seconds':time.perf_counter()-start,'passed':abs(dt)<=1e-8 and abs(dx)<=1e-10})
save_json(a.output,{'native_regression_passed':bool(rows) and all(r['passed'] for r in rows),'rows':rows,'source_qualification':'Native parity alone does not establish absent original full-source fingerprints. Records remain quarantined until provenance is qualified.'})
