"""Resolve development recovery labels through frozen split registries, never sealed."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'src'))
from bt_history.data_control import read_json,assert_development_path,verify_design
from bt_history.contracts import file_hash
from bt_history.label_quality import validate_label
from bt_history.original_postprocessing_adapter import OriginalPostprocessingAdapter

def load(snapshot):
 c=read_json(ROOT/'contracts/science_contract.json');sel=read_json(ROOT/'contracts/selected_native_contract.json');post=OriginalPostprocessingAdapter(c);protocol=read_json(ROOT/'contracts/data_quality_protocol.json');m=read_json(snapshot)
 if m['role']!='development':raise PermissionError('Only explicit development snapshots')
 wanted={x['sample_id']:x for x in m['files']}
 if len(wanted)!=len(m['files']) or any(x['split'] not in ['train','validation'] for x in m['files']):raise PermissionError('Duplicate or unauthorized split')
 registry={};v2=read_json(ROOT/'contracts/dataset_design_v2_100k.json')
 manifests=[ROOT/'manifests/train_full_design.jsonl',ROOT/'manifests/validation_design.jsonl']
 for split in ['train','validation']:manifests.extend(ROOT/shard['manifest'] for shard in v2['stages'][split])
 for path in manifests:
  # Cheap ID inspection then frozen manifest SHA verification for relevant shards.
  import json
  ids={json.loads(s)['sample_id'] for s in path.read_text().splitlines() if s}
  if not ids.intersection(wanted):continue
  for d in verify_design(ROOT,path):
   if d['sample_id'] in wanted:
    if d['sample_id'] in registry:raise ValueError('Duplicate design identity')
    registry[d['sample_id']]=d
 if set(registry)!=set(wanted):raise ValueError('Missing frozen development design')
 rows=[];seen=set();families={}
 for it in m['files']:
  path=ROOT/it['path'];assert_development_path(path,it['split'])
  if file_hash(path)!=it['sha256']:raise ValueError('Changed label')
  r=read_json(path);rp=read_json(ROOT/it['receipt']);design=registry[it['sample_id']]
  if not rp.get('qualified') or rp['label_sha256']!=it['sha256'] or design['split']!=it['split']:raise ValueError('Receipt/split mismatch')
  if r['pipeline_integrity_sha256'] not in sel['accepted_training_pipeline_sha256'] or r['runtime_fingerprint'] not in sel['allowed_runtime_fingerprints']:raise ValueError('Unaccepted execution provenance')
  validate_label(c,r,design,sel,protocol,post)
  physical=tuple(sorted(r['physical_parameters'].items()))
  if physical in seen:raise ValueError('Duplicate physical parameters')
  seen.add(physical);f=r['family_id']
  if f in families and families[f]!=r['split']:raise ValueError('Family split leakage')
  families[f]=r['split']
  rows.append({k:r[k] for k in ['sample_id','split','family_id','physical_parameters','redshifts','global_xHI','exact_tau','exact_xHI_at_observation_redshifts','quality_flags']} | {k:r[k] for k in ['original_end_to_end_success','LF_reference_status','stratum','inference_view_tags','fixed_parameters','ic_seed','science_contract_hash','source_native_config_hashes','provenance'] if k in r})
 return c,rows,post
