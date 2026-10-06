# BTemu project progress

Snapshot: 2026-10-06T09:25:28.900094+08:00 (Hong Kong). This records qualified labels at the last completed wave; it is not a live queue display.

| Dataset | Qualified | Target |
|---|---:|---:|
| Train including retained v1 Train | 13824 | 100000 |
| Validation v2 | 3072 | 10000 |
| Validation v1 benchmark | 512 | 512 |

V1 Train 4096/4096 is complete. V2 receipted attempts: 12800; numerical failures: 0; infrastructure failures: 0. Current configured production concurrency limit: 32 simulations ×16 allocated CPUs. V2 accounted worker cost: 24160.04 core-hours; this excludes v1/preflight/metadata/ML allocations.

The frozen 9080 Train/2048 independent Validation development comparison completed all five seeds in approximately 40 minutes. Classifier accuracy 97.41%, false-negative rate 3.60%. Direct ensemble all-Validation history RMSE q95=0.02466, absolute tau error q90=0.001472. On identical exact-positive Validation IDs, Direct RMSE q95=0.04477 versus NNERO-style PCA+MLP 0.34278. These positive-subset results must not be compared with all-Validation results as though they used the same sample distribution.

Only logit PCA K=32 passed the preregistered development reconstruction screens. No compression benefit is established. Likelihood error tails remain too large to claim scientific inference readiness. Classifier is diagnostic and is not a hard prior gate. All negative histories are retained.

Sealed v1/v2 parameter designs remain frozen. No sealed labels were generated or accessed, and no production emulator MCMC was launched. Endpoint ionization flags are warnings; original histories are not clipped, smoothed, or forced to complete reionization. Tau is computed only through the original history postprocessing and selected native compute_tau. LF remains the original exact forward.

This is a public code/report export. Simulator binaries, native tables, raw labels, encrypted payloads, checkpoints, production attempt logs and credentials remain outside Git. Historical reports under docs/archive reflect their original stage; use this progress report and site JSON for current status. Public budget templates are disabled and do not grant cluster execution authorization.

## Reproduction and deployment

Install Python >=3.10 package dependencies with `pip install -e .`. Run cheap software checks with `PYTHONPATH=src python -m unittest discover -s tests -p test_compact_array.py`. The original native/postprocessing environment and approved data contracts are required for science-facing tests and training. The selected native hash is recorded in contracts/science_contract.json; a version string alone is not sufficient.

V1 parameter-only manifests are included. Large v2 manifests and data receipts must be restored from the frozen private workspace or recreated and hash-verified with maintenance/v2/generate_design.py; the registry records the expected manifest identities. Cluster-specific absolute paths in the exported implementation identify the audited deployment and need explicit environment adaptation for another deployment. Never update a source/native identity silently.

## Web progress

The static dashboard is in site/. GitHub Actions deploys only that directory after GitHub Pages is configured to use GitHub Actions. Refresh the public snapshot with tools/export_public_progress.py using the private project root, review the diff, and commit/push the aggregate JSON. The page displays the snapshot timestamp explicitly and does not automatically access the cluster.
