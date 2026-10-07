"""Export aggregate receipts only. No history arrays or sealed paths are read."""
import argparse, json, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--project", required=True)
p.add_argument("--output", default="site/progress.json")
a=p.parse_args()
root=Path(a.project)
d=json.loads((root/"results/dataset_progress.json").read_text())
keys=["updated_at_hkt","version","datasets","numerical_failed","infrastructure_failed","retry_success","v2_attempts_reserved","v2_actual_core_hours_as_accounted","median_wall_seconds","q90_wall_seconds","current_ramp_concurrency","native_sha256","science_contract_hash","sealed_labels_generated","sealed_labels_read","stop_reasons"]
out={k:d.get(k) for k in keys}
for split in out["datasets"].values():
    split.pop("xHI_5p9_histogram_20_equal_bins_0_1",None)
out.update(snapshot_notice="Validated wave summary, not live Slurm state.",production_accepted=False,email_notifications_enabled=False)
Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
curve=json.loads((root/"artifacts/learning_curve_v2_100k/status.json").read_text())
items=[]
for n, item in sorted(curve["milestones"].items(),key=lambda pair:int(pair[0])):
    run=root/item["run"]
    state=item["status"]
    if (run/"complete.json").exists():
        state="COMPLETED"
    elif (run/"status.json").exists():
        state=json.loads((run/"status.json").read_text()).get("status",state)
    receipt=run/("complete.json" if state=="COMPLETED" else "status.json")
    receipt_time=datetime.fromtimestamp(receipt.stat().st_mtime,timezone(timedelta(hours=8))).isoformat() if receipt.exists() else None
    items.append({"N":int(n),"status":state,"job_id":item.get("job_id"),"receipt_updated_at_hkt":receipt_time})
work={"learning_curves":items,"validation_scope":"Frozen v1 144-point benchmark; separate from the 9k comparison on 2048 v2 Validation points.","next_milestone":curve.get("next_milestone"),"comparison_completed":json.loads((root/"artifacts/development_comparison_20261005/status.json").read_text())["status"]=="DEVELOPMENT_COMPARISON_COMPLETED","production_accepted":False,"sealed_labels_generated":d["sealed_labels_generated"],"sealed_labels_read":d["sealed_labels_read"],"publication_policy":"Hourly aggregate checks; only qualified counts and completed training receipts are published. Queue and deployment delays apply."}
transition_path=root/"results/fixed_ic_transition_snapshot.json"
if transition_path.exists():
    ts=json.loads(transition_path.read_text())
    ap=root/"results/ic_audit_progress.json"
    audit=json.loads(ap.read_text()) if ap.exists() else {}
    partial_path=root/"results/ic_audit_partial_scatter.json"
    partial=json.loads(partial_path.read_text()) if partial_path.exists() else {}
    live_path=root/"results/ic_audit_live_receipts.json"
    if live_path.exists():
        live=json.loads(live_path.read_text())
        partial["qualified_fresh"]=max(partial.get("qualified_fresh",0),live.get("qualified_fresh",0))
        partial["complete_families"]=max(partial.get("complete_families",0),live.get("complete_families",0))
        partial["updated_at_hkt"]=live.get("updated_at_hkt",partial.get("updated_at_hkt"))
    work["transition"]={"dataset_version":"fixed_ic_v1","new_target":"random_ic_v2","fixed_waves_stopped":True,"fixed_drained":ts.get("drained_running")==0,"fixed_qualified":ts.get("drained_qualified",ts["qualified"]),"cancelled_unstarted_slots":ts["cancelled_pending_slots"],"audit_status":audit.get("status","MANIFEST_FROZEN"),"audit_max_concurrent":16,"audit_receipt_updated_at_hkt":datetime.fromtimestamp(ap.stat().st_mtime,timezone(timedelta(hours=8))).isoformat() if ap.exists() else None,"audit_theta_count":128,"ICs_per_theta":8,"new_evaluations":896,"qualified_fresh":max(audit.get("qualified_fresh",0),partial.get("qualified_fresh",0)),"qualified_fresh_scope":"Qualified worker receipts, checksum/native/seed checked; completed-wave audit status reported separately","complete_IC_families":max(audit.get("complete_families",0),partial.get("complete_families",0)),"partial_scatter_snapshot_at_hkt":partial.get("updated_at_hkt"),"reused_fixed":128,"audit_array_job":(audit.get("submission") or {}).get("array_job"),"random_bulk_started":False,"classifier_cut":0.31,"decision":"AUDIT_NOT_YET_COMPLETE"}
acceptance_path=root/"contracts/ic_audit_acceptance.json"
if acceptance_path.exists() and "transition" in work:
    acceptance=json.loads(acceptance_path.read_text())
    work["transition"]["development_gate_status"]=acceptance["status"]
    work["transition"]["posterior_accepted"]=False
launch_path=root/"results/random_ic_launch_execution.json"
if launch_path.exists():
    launch=json.loads(launch_path.read_text())
    activation_path=root/"results/random_ic_activation_status.json"
    activation=json.loads(activation_path.read_text()) if activation_path.exists() else {}
    random_progress_path=root/"results/random_ic_dataset_progress.json"
    rp=json.loads(random_progress_path.read_text()) if random_progress_path.exists() else {}
    design_status_path=root/"results/random_ic_design_status.json"
    work["random_launch"]={"design_job":launch["design_job"]["job_id"],"gate_job":activation.get("next_watch",{}).get("job_id",launch["audit_gate_job"]["job_id"]),"initial_gate_job":launch["audit_gate_job"]["job_id"],"status":activation.get("status","WAITING_FOR_COMPLETE_AUDIT"),"design_frozen":design_status_path.exists(),"targets":{"train":100000,"validation":10000,"sealed_design":5000},"production":rp,"sealed_labels_generated":False,"sealed_labels_read":False}
    if "transition" in work:
        work["transition"]["random_bulk_started"]=activation.get("random_IC_production_started",False)
        work["transition"]["decision"]=activation.get("audit_decision",work["transition"]["decision"])
Path(a.output).with_name("work_status.json").write_text(json.dumps(work,ensure_ascii=False,indent=2)+"\n")
completed=", ".join(f'{x["N"]:,}' for x in items if x["status"]=="COMPLETED")
active=", ".join(f'{x["N"]:,}: {x["status"]}' for x in items if x["status"]!="COMPLETED")
report=f"""# BTemu progress

Qualified data snapshot: {d['updated_at_hkt']} (Hong Kong time). Completed-wave receipts, not live Slurm occupancy.

## Completed

- Scientific contract, repaired-native qualification, exact adapter parity and PL-limit checks.
- Dataset v1: 4,096 qualified Train histories and 512 Validation benchmark histories. V1 Train is retained in the v2 total.
- Recoverable isolated data-generation pipeline, per-sample provenance and failure records.
- Development comparison: Direct ResMLP, classifier and PCA + 6×80 MLP; all five initialization seeds; 9,080 Train / 2,048 Validation. This is development evidence, not production acceptance.
- Frozen learning-curve runs completed: {completed} Train points, on the same 144-point v1 Validation benchmark.
- PCA representation audit: only logit K=32 passed the current reconstruction screen. No compression benefit has been established.

## In progress

| Dataset | Qualified | Target | Remaining |
|---|---:|---:|---:|
| Train v2 | {d['datasets']['train']['qualified']:,} | 100,000 | {100000-d['datasets']['train']['qualified']:,} |
| Validation v2 | {d['datasets']['validation']['qualified']:,} | 10,000 | {10000-d['datasets']['validation']['qualified']:,} |

- Learning curves: {active or 'No incomplete submitted milestones in the latest receipt.'}
- Configured simulation concurrency cap: {d['current_ramp_concurrency']} × 16 CPUs. This is a cap, not a live occupancy measurement.
- Accounted v2 worker allocation cost: {d['v2_actual_core_hours_as_accounted']:,.2f} core-hours; median / q90 wall time: {d['median_wall_seconds']:.1f} / {d['q90_wall_seconds']:.1f} seconds.
- Receipted numerical / infrastructure failures: {d['numerical_failed']} / {d['infrastructure_failed']}.

## Pending

- Complete 100,000 qualified Train and 10,000 independent Validation histories.
- Complete 32k, 64k and 100k learning curves and final model selection. Different Validation scopes are reported separately.
- Reduce and qualify derived tau and each likelihood error, including tails. Current development models are not accepted for scientific deployment.
- Freeze model and analysis before separately authorized sealed-label generation and evaluation. Sealed labels generated/read: {d['sealed_labels_generated']}/{d['sealed_labels_read']}.
- Independent posterior fidelity validation and production MCMC integration; no production emulator MCMC has been started.

## Publication and scope

Public aggregate snapshots are checked hourly. Queue and GitHub Pages deployment delays apply. Only qualified data counts and completed-training receipts enter the completed list; submitted jobs are not counted as completed. Source history labels, checkpoints, native libraries and sealed payloads are excluded. Email notifications remain disabled.

The emulator predicts only the simulator-defined 32-node volume-averaged global_xHI history. Tau uses original history postprocessing; LF keeps its exact provider. Endpoint warnings do not remove valid histories, and classifier-negative histories are retained. The reported PCA result is a completed audit, not evidence that compressed PCA is accepted.

Selected native SHA256: `{d['native_sha256']}`.

Code exports are cluster-oriented templates with submission disabled by default. Production authorization is managed separately in the independent scientific workspace.
"""
if work.get("transition"):
    t=work["transition"]
    report=report.replace("## In progress", "## Scientific-target transition\n\nFixed-IC production waves have stopped. Existing data retain their original labels and splits under the catalog alias fixed_ic_v1. Random-IC training is separate.\n\nIC_AUDIT_V1: 128 theta families × 8 ICs; reuse 128 qualified fixed references and run 896 fresh realizations. Audit status: "+t["audit_status"]+". Fresh qualified: "+str(t["qualified_fresh"])+". Classifier cut is derived from the original likelihood: 0.06 + 5×0.05 = 0.31. No classifier hard gate is enabled.\n\n## Retained fixed-IC data")
    report=report.replace("- Configured simulation concurrency cap:","- Historical fixed-IC simulation concurrency cap (production stopped):")
    report=report.replace("- Complete 100,000 qualified Train and 10,000 independent Validation histories.","- Complete IC sensitivity audit and qualify one-random-IC versus multi-IC averaging before formal random_ic_v2 production (100k Train / 10k Validation). Fixed-IC totals are retained baselines, not random-IC training data.")
    report=re.sub(r"\| Dataset \| Qualified \| Target \| Remaining \|.*?\n\n- Learning curves:", "| Retained baseline | Qualified | Role |\n|---|---:|---|\n| Fixed-IC Train | "+format(d["datasets"]["train"]["qualified"],",")+" | Baseline / diagnostics |\n| Fixed-IC Validation | "+format(d["datasets"]["validation"]["qualified"],",")+" | Development reference |\n\n- Learning curves:", report, flags=re.S)
if work.get("random_launch"):
    r=work["random_launch"]
    report+="\n## Audit-gated random-IC launch\n\nSubmitted offline design job: "+r["design_job"]+". Submitted scientific gate watcher: "+r["gate_job"]+". Status: "+r["status"]+". Parameter design frozen: "+str(r["design_frozen"])+". Complete 128×8 audit must pass before any random-IC production array is submitted. First eight evaluations, then waves of up to 128, maximum 16 simulations / 256 CPUs. See [launch record](random_ic_production_launch.md).\n"
Path("docs/progress.md").write_text(report)
