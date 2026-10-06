"""Export whitelisted aggregate progress only; no labels or sealed paths."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--output",default="site/progress.json");a=p.parse_args()
d=json.loads((Path(a.project)/"results/dataset_progress.json").read_text())
keys=['updated_at_hkt', 'version', 'datasets', 'numerical_failed', 'infrastructure_failed', 'retry_success', 'v2_attempts_reserved', 'v2_actual_core_hours_as_accounted', 'median_wall_seconds', 'q90_wall_seconds', 'current_ramp_concurrency', 'native_sha256', 'science_contract_hash', 'sealed_labels_generated', 'sealed_labels_read', 'stop_reasons']
out={k:d.get(k) for k in keys}
for split in out["datasets"].values():split.pop("xHI_5p9_histogram_20_equal_bins_0_1",None)
out.update(snapshot_notice="Validated wave summary, not live Slurm state.",production_accepted=False,email_notifications_enabled=False)
Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
