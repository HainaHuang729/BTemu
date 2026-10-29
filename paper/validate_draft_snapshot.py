"""Read published chain segments and report descriptive statistics; no sampling."""
import hashlib
import json
from pathlib import Path

import h5py
import numpy as np

ROOT = Path(__file__).resolve().parent
CASES = {
    '6d': ['chain6_1000.h5', 'chain6_ext_2000.h5', 'chain6_ext2_2000.h5'],
    '8d': ['chain8_2000.h5', 'chain8_ext_3399.h5'],
}


def describe(files):
    segments, sources, names = [], [], None
    for filename in files:
        path = ROOT / 'chains' / filename
        with h5py.File(path, 'r') as f:
            order = [s.decode() for s in f['parameter_names'][:]]
            if names is None:
                names = order
            assert names == order
            chain = f['chain'][:]
            assert chain.shape[1:] == (32, len(names))
            assert f['log_prob'].shape == chain.shape[:2]
            assert np.isfinite(chain).all() and np.isfinite(f['log_prob'][:]).all()
            sources.append({'file': 'chains/' + filename, 'shape': list(chain.shape),
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                            'attributes': {k: str(v) for k, v in f.attrs.items()}})
            segments.append(chain)
    # Reject exact repeated suffix/prefix blocks; per-walker rejections remain.
    for left, right in zip(segments, segments[1:]):
        for index in np.flatnonzero(np.all(left == right[0], axis=(1, 2))):
            overlap = len(left) - index
            assert overlap > len(right) or not np.array_equal(left[index:], right[:overlap])
    chain = np.concatenate(segments)
    half = len(chain) // 2
    retained = chain[half:].reshape(-1, len(names))
    split = np.concatenate([chain[:half], chain[-half:]], axis=1)
    within = split.var(axis=0, ddof=1).mean(axis=0)
    between = half * split.mean(axis=0).var(axis=0, ddof=1)
    statistic = np.sqrt(((half - 1) / half * within + between / half) / within)
    return {
        'source_files': sources, 'parameter_order': names,
        'total_stored_steps': len(chain), 'walkers': 32,
        'summary_selection': 'last chronological half; all walkers; no thinning',
        'retained_steps': len(chain) - half, 'retained_correlated_rows': len(retained),
        'ordinary_split_statistic_range': [float(statistic.min()), float(statistic.max())],
        'parameters': {name: {'mean': float(retained[:, i].mean()),
                              'sample_sd_ddof1': float(retained[:, i].std(ddof=1)),
                              'ordinary_split_statistic': float(statistic[i])}
                       for i, name in enumerate(names)},
    }


if __name__ == '__main__':
    result = {'cases': {name: describe(files) for name, files in CASES.items()},
              'statistic_definition': 'Ordinary split variance ratio over interacting ensemble walkers; descriptive, not independent-chain rank-normalized/folded R-hat or ESS.',
              'continuation_order': 'Order follows the published snapshot and filenames. HDF5 files lack iteration offsets, RNG state and complete target settings; continuity and target identity remain to be checked against run receipts.',
              'data_counts': {'source': 'RESULTS_20261029.md, original 15:45 production snapshot',
                              'train_admitted': 83756, 'validation_admitted': 2752},
              'ic_scatter': {'source': '../docs/ic_audit_completion.md',
                             'statistic': 'Across-parameter q90 of within-parameter IC sample standard deviation in history log likelihood',
                             'value': 0.9480653, 'parameter_families': 128,
                             'realizations_per_family': 8}}
    target = ROOT / 'DRAFT_SNAPSHOT_VALIDATION_20261029.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    for key, case in result['cases'].items():
        print(key, case['total_stored_steps'], case['ordinary_split_statistic_range'])
