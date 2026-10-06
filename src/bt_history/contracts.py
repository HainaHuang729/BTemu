"""Immutable scientific identity, prior support and source checks."""
import hashlib
import json
from pathlib import Path
import numpy as np

class ContractError(ValueError):
    pass

class DomainError(ValueError):
    pass

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()

def read_contract(path):
    c = json.loads(Path(path).read_text())
    if len(c['parameter_order']) != len(set(c['parameter_order'])):
        raise ContractError('Duplicate parameters')
    z = np.asarray(c['redshift_grid'])
    if not np.isfinite(z).all() or not (np.diff(z) > 0).all():
        raise ContractError('Redshifts must be finite and strictly increasing')
    return c

def parameters(c, values):
    if set(values) != set(c['parameter_order']):
        raise DomainError('Expected exactly ' + str(c['parameter_order']))
    x = np.array([values[k] for k in c['parameter_order']], dtype=float)
    bounds = np.array([c['prior_support'][k] for k in c['parameter_order']])
    if not np.isfinite(x).all() or np.any(x < bounds[:, 0]) or np.any(x > bounds[:, 1]):
        raise DomainError('Outside finite scientific prior support')
    return x

def verify_sources(c):
    for path, expected in c['source_and_native_fingerprints'].items():
        if file_hash(path) != expected:
            raise ContractError('Changed source/native: ' + path)

def validate_history(c, z, x):
    z, x = np.asarray(z, float), np.asarray(x, float)
    expected = np.asarray(c['redshift_grid'])
    if z.shape != expected.shape or not np.array_equal(z, expected):
        raise ContractError('History grid differs, contains duplicates or missing nodes')
    if x.shape != z.shape or not np.isfinite(x).all() or np.any((x < 0) | (x > 1)):
        raise ContractError('Invalid history; labels are never clipped or imputed')
    return x
