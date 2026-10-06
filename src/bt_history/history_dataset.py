"""Explicit allowlist reads, strict provenance and grouped development splitting."""
import json
from pathlib import Path
import numpy as np
from .contracts import digest, file_hash, parameters, validate_history, ContractError

REQUIRED = {'sample_id','physical_parameters','fixed_parameters','ic_seed','redshifts','global_xHI','exact_tau','exact_xHI_at_observation_redshifts','simulation_status','science_contract_hash','source_native_config_hashes','provenance'}

def group_id(row):
    return row.get('family_id', digest(row['physical_parameters']))

def validate_row(row, c, post):
    if not REQUIRED <= row.keys():
        raise ContractError('Missing record fields: ' + str(REQUIRED-row.keys()))
    if row.get('validation_status') == 'QUARANTINED_NOT_TRAINING_ELIGIBLE':
        raise ContractError('Quarantined provenance is not training eligible')
    if row['simulation_status'] != 'ok':
        raise ContractError('Failed simulation is not a valid label')
    parameters(c, row['physical_parameters'])
    validate_history(c, row['redshifts'], row['global_xHI'])
    if row['science_contract_hash'] != digest(c) or row['fixed_parameters'] != c['fixed_parameters']:
        raise ContractError('Scientific configuration mismatch')
    if row['ic_seed'] != c['ic_target']['seed'] or row['source_native_config_hashes'] != c['source_and_native_fingerprints']:
        raise ContractError('IC/source/native mismatch')
    derived = post.evaluate(row['physical_parameters'], row['redshifts'], row['global_xHI'])
    if not np.isclose(row['exact_tau'], derived['tau'], rtol=0, atol=1e-8):
        raise ContractError('Saved tau mismatch')
    obs = str(c['likelihood']['neutral_fraction']['redshift'])
    if not np.isclose(row['exact_xHI_at_observation_redshifts'][obs], derived['xHI_obs'], rtol=0, atol=1e-10):
        raise ContractError('Saved observational interpolation mismatch')
    return derived

def load_development(manifest_path, c, post):
    # Reject sealed role BEFORE opening any label file. No directory discovery.
    m = json.loads(Path(manifest_path).read_text())
    if m.get('schema_version') == 2:
        return load_frozen_development(manifest_path,c,post)
    if m['role'] != 'development' or m['science_contract_hash'] != digest(c):
        raise ContractError('Only matching development manifests are accepted')
    rows, failures, ids = [], [], set()
    for item in m['files']:
        if item['role'] != 'development':
            raise ContractError('Sealed/mixed file in development manifest')
        path = Path(item['path'])
        from .data_control import assert_development_path
        assert_development_path(path,item['role'])
        if file_hash(path) != item['sha256']:
            raise ContractError('Label file digest mismatch')
        for line in path.read_text().splitlines():
            row = json.loads(line)
            if row['sample_id'] in ids:
                raise ContractError('Duplicate sample ID')
            ids.add(row['sample_id'])
            if row['simulation_status'] != 'ok':
                failures.append(row)
            else:
                validate_row(row, c, post)
                rows.append(row)
    return rows, failures

def split_groups(rows, seed=20260928):
    if any('split' in r for r in rows):
        if not all(r.get('split') in ['train','validation'] for r in rows):
            raise ContractError('Only frozen train/validation rows may enter training')
        families={}
        for r in rows:
            g=group_id(r)
            if g in families and families[g]!=r['split']:
                raise ContractError('Frozen family crosses splits')
            families[g]=r['split']
        return {r['sample_id']:r['split'] for r in rows}
    groups = sorted(set(group_id(r) for r in rows))
    if len(groups) < 5:
        raise ContractError('Need at least five independent parameter groups for a development split')
    np.random.default_rng(seed).shuffle(groups)
    nv = max(1, int(np.ceil(.2 * len(groups))))
    val = set(groups[:nv])
    return {r['sample_id']: ('validation' if group_id(r) in val else 'train') for r in rows}

def nested_ids(rows, split, sizes, seed=20260929):
    groups = sorted({group_id(r) for r in rows if split[r['sample_id']] == 'train'})
    np.random.default_rng(seed).shuffle(groups)
    return {str(n): [r['sample_id'] for r in rows if group_id(r) in set(groups[:n]) and split[r['sample_id']] == 'train'] for n in sizes if n <= len(groups)}

def load_frozen_development(manifest_path,c,post):
    from .data_control import read_json,verify_design,assert_development_path
    from .label_quality import validate_label
    root=Path(__file__).resolve().parents[2]
    m=read_json(manifest_path)
    if m['role']!='development' or m['science_contract_hash']!=digest(c) or m['dataset_design_sha256']!=file_hash(root/'contracts/dataset_design.json'):raise ContractError('Frozen loader contract mismatch')
    designs={}
    for name in ['train_full_design','validation_design']:
        designs.update({r['sample_id']:r for r in verify_design(root,root/'manifests'/(name+'.jsonl'))})
    selected=read_json(root/'contracts/selected_native_contract.json');protocol=read_json(root/'contracts/data_quality_protocol.json');rows=[];seen=set()
    for item in m['files']:
        if item['sample_id'] not in designs or item['sample_id'] in seen:raise ContractError('Unapproved or duplicate sample ID')
        design=designs[item['sample_id']]
        if item['split']!=design['split'] or item['split'] not in ['train','validation']:raise ContractError('Frozen split mismatch')
        path=root/item['path'];assert_development_path(path,item['split'])
        if not path.resolve().is_relative_to((root/'data_runs').resolve()):raise ContractError('Label outside approved generated store')
        rp=root/item['receipt'];assert_development_path(rp,item['split']);receipt=read_json(rp)
        if receipt.get('native_qualification_sha256'):
            qpath=root/'results/native_qualification.json'
            if file_hash(qpath)!=receipt['native_qualification_sha256'] or not read_json(qpath).get('qualified_for_batch1'):raise ContractError('Admission native qualification invalid')
        if not receipt.get('qualified') or receipt['sample_id']!=item['sample_id'] or receipt['label_sha256']!=item['sha256']:raise ContractError('Unqualified receipt')
        if file_hash(path)!=item['sha256']:raise ContractError('Label digest mismatch')
        r=read_json(path);validate_label(c,r,design,selected,protocol,post);seen.add(item['sample_id']);rows.append(r)
    return rows,[]
