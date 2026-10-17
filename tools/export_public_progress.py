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
    work["transition"]={"dataset_version":"fixed_ic_v1","new_target":"random_ic_v2","fixed_waves_stopped":True,"fixed_drained":ts.get("drained_running")==0,"fixed_qualified":ts.get("drained_qualified",ts["qualified"]),"cancelled_unstarted_slots":ts["cancelled_pending_slots"],"audit_status":audit.get("status","MANIFEST_FROZEN"),"audit_max_concurrent":json.loads((root/"configs/ic_audit_budget.json").read_text())["max_concurrent"],"audit_receipt_updated_at_hkt":datetime.fromtimestamp(ap.stat().st_mtime,timezone(timedelta(hours=8))).isoformat() if ap.exists() else None,"audit_theta_count":128,"ICs_per_theta":8,"new_evaluations":896,"qualified_fresh":max(audit.get("qualified_fresh",0),partial.get("qualified_fresh",0)),"qualified_fresh_scope":"Qualified worker receipts, checksum/native/seed checked; completed-wave audit status reported separately","complete_IC_families":max(audit.get("complete_families",0),partial.get("complete_families",0)),"partial_scatter_snapshot_at_hkt":partial.get("updated_at_hkt"),"reused_fixed":128,"audit_array_job":(audit.get("submission") or {}).get("array_job"),"random_bulk_started":False,"classifier_cut":0.31,"decision":"AUDIT_NOT_YET_COMPLETE"}
recovery_path=root/"results/ic_audit_scheduler_recovery.json"
if recovery_path.exists() and "transition" in work:
    recovery=json.loads(recovery_path.read_text())
    work["transition"]["scheduler_recovery"]={"controller_job":recovery.get("recovery_controller_job"),"remaining_at_recovery":recovery["remaining_evaluations"],"reason":recovery["cause"],"status":"RESOLVED_COMPLETED" if work["transition"].get("audit_status")=="AUDIT_COMPLETED" else ("WAITING_FOR_RECOVERY_CONTROLLER" if work["transition"].get("audit_array_job")=="2191736" else "RECOVERY_SUBMITTED")}
    if work["transition"]["scheduler_recovery"]["status"]=="WAITING_FOR_RECOVERY_CONTROLLER":
        work["transition"]["audit_status"]="WAITING_FOR_RECOVERY_CONTROLLER"
queue_path=root/"results/ic_audit_queue_status.json"
if queue_path.exists() and work.get("transition",{}).get("audit_status")=="WAITING_FOR_RECOVERY_CONTROLLER":
    work["transition"]["queue_snapshot"]=json.loads(queue_path.read_text())
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
final_audit_path=root/"results/ic_audit_completion_summary.json"
if final_audit_path.exists() and "transition" in work:
    work["transition"]["completed_audit"]=json.loads(final_audit_path.read_text())
explicit_start=root/"results/random_ic_explicit_start.json"
if explicit_start.exists() and "transition" in work:
    work["transition"]["explicit_random_start"]=json.loads(explicit_start.read_text())
random_dev=root/"artifacts/random_ic_development_20261014"
if (random_dev/"intent.json").exists():
    intent=json.loads((random_dev/"intent.json").read_text())
    state=json.loads((random_dev/"status.json").read_text()) if (random_dev/"status.json").exists() else {"status":"SETUP_IN_PROGRESS"}
    rp=json.loads((root/"results/random_ic_dataset_progress.json").read_text())
    trial={"dataset_version":"random_ic_v2","train_count":10000,"validation_planned":512,
        "validation_qualified":min(512,rp["datasets"]["validation"]["qualified"]),
        "seeds":intent["seeds"],"status":state["status"],"state":state,
        "mean_target_qualified":False,"posterior_accepted":False,"sealed_access":False,
        "direct_completed_seeds":sum((random_dev/"direct_resmlp"/("seed_%d_metrics.json"%seed)).exists() for seed in intent["seeds"]),
        "classifier_completed_seeds":sum((random_dev/"nnero_style"/("classifier_seed_%d.json"%seed)).exists() for seed in intent["seeds"]),
        "regressor_completed_seeds":sum((random_dev/"nnero_style"/("regressor_seed_%d.json"%seed)).exists() for seed in intent["seeds"])}
    if (random_dev/"submission.json").exists():
        sub=json.loads((random_dev/"submission.json").read_text())
        trial["validation_array_job"]=sub["validation"]["array_job"]
        trial["training_job"]=sub["training"]["job_id"]
    if (random_dev/"comparison_metrics.json").exists():
        trial["metrics"]=json.loads((random_dev/"comparison_metrics.json").read_text())
    if (random_dev/"validation_admission.json").exists():
        adm=json.loads((random_dev/"validation_admission.json").read_text())
        trial["validation_qualified"]=adm["qualified"]
        trial["validation_unqualified"]=len(adm["unqualified_indices"])
    work["random_development"]=trial
mcmc_run=root/"artifacts/random_ic_mcmc_development_20261015"
if (mcmc_run/"plan.json").exists():
    st=json.loads((mcmc_run/"status.json").read_text())
    sub=json.loads((mcmc_run/"submission.json").read_text()) if (mcmc_run/"submission.json").exists() else {}
    trial={"status":st["status"],"job_id":sub.get("job_id"),"views":["fixed","continuous_ms"],
        "allocation_CPUs":16,"maximum_wall_hours":4,"new_full_history_evaluations":0,
        "posterior_accepted":False,"sealed_access":False,"original_priors_preserved":True,
        "classifier_hard_gate":False,"validation_planned":512,"chain_reports":[]}
    for key in ["view","completed_steps","total_steps","processed","planned","elapsed_seconds"]:
        if key in st:trial[key]=st[key]
    if (mcmc_run/"interface_parity.json").exists():
        parity=json.loads((mcmc_run/"interface_parity.json").read_text())
        trial["interface_parity_pass"]=parity["status"]=="PASSED"
        trial["LF_A_B_A_pass"]=parity["LF_A_B_A_pass"]
    if (mcmc_run/"validation_likelihood_report.json").exists():
        v=json.loads((mcmc_run/"validation_likelihood_report.json").read_text())
        trial["validation"]={k:v[k] for k in ["planned","processed","LF_valid","LF_invalid_history_retained","original_reference_replay_pass","LF_unchanged_pass","all_LF_valid","reference_likelihood_bands","bands_are_not_posterior_regions","IC_scatter_included","timing_medians"]}
    for name in trial["views"]:
        file=mcmc_run/(name+"_chain_report.json")
        if file.exists():trial["chain_reports"].append(json.loads(file.read_text()))
    work["random_mcmc_development"]=trial
followup={"production_accepted":False,"sealed_access":False}
diagnostic=root/"artifacts/random_ic_mlp_diagnosis_20261016"
if (diagnostic/"status.json").exists():
    ds=json.loads((diagnostic/"status.json").read_text())
    followup["diagnostic"]={k:ds[k] for k in ["status","job_id","seconds","counts"] if k in ds}
    if (diagnostic/"checkpoint_diagnosis.json").exists():
        dd=json.loads((diagnostic/"checkpoint_diagnosis.json").read_text())
        followup["diagnostic"].update(physical_ensemble=dd["physical_ensemble"],exact_projection_max_abs_error=dd["exact_projection_max_abs_error"],
            per_seed_saturation={seed:{split:{k:v[k] for k in ["wrong_saturated_cells","trajectories_with_wrong_saturation","fraction_squared_error_in_wrong_saturated_cells"]} for split,v in by_split.items()} for seed,by_split in dd["per_seed"].items()})
curve16=root/"artifacts/random_ic_development_16k_20261016"
if (curve16/"status.json").exists():
    cs=json.loads((curve16/"status.json").read_text())
    ci=json.loads((curve16/"intent.json").read_text())
    sub=json.loads((curve16/"submission.json").read_text())
    trial={"N":ci["N"],"validation_n":ci["validation_n"],"status":cs["status"],"job_id":sub["job_id"],"seeds":ci["seeds"],"allocated_CPUs":1,
           "direct_completed_seeds":sum((curve16/"direct_resmlp"/("seed_%d_metrics.json"%s)).exists() for s in ci["seeds"]),
           "classifier_completed_seeds":sum((curve16/"nnero_style"/("classifier_seed_%d.json"%s)).exists() for s in ci["seeds"]),
           "regressor_completed_seeds":sum((curve16/"nnero_style"/("regressor_seed_%d.json"%s)).exists() for s in ci["seeds"])}
    if (curve16/"comparison_metrics.json").exists():
        cm=json.loads((curve16/"comparison_metrics.json").read_text())
        trial["metrics"]={"classifier_ensemble":cm["classifier_ensemble"],"exact_positive_validation_count":cm["exact_positive_validation_count"]}
        for key in ["direct_ensemble_all_validation","direct_ensemble_positive_validation","nnero_ensemble_positive_validation"]:
            value=cm.get(key,{})
            trial["metrics"][key]={k:value[k] for k in ["status","n_trajectories","trajectory_RMSE_quantiles","derived_absolute_quantiles"] if k in value}
    followup["learning_curve_16k"]=trial
initialization=root/"artifacts/random_ic_mlp_initialization_20261016"
if (initialization/"status.json").exists():
    it=json.loads((initialization/"status.json").read_text())
    followup["initialization_trial"]={k:it[k] for k in ["status","job_id","completed_seeds","seconds"] if k in it}
    if (initialization/"comparison_metrics.json").exists():
        im=json.loads((initialization/"comparison_metrics.json").read_text())
        followup["initialization_trial"]["metrics"]={key:{k:im[key][k] for k in ["n_trajectories","trajectory_RMSE_quantiles","derived_absolute_quantiles"]} for key in ["initialization_trial","original_MLP","direct_reference"]}
work["random_model_followup"]=followup
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
    report+="\n## Audit-gated random-IC launch\n\nSubmitted offline design job: "+r["design_job"]+". Submitted scientific gate watcher: "+r["gate_job"]+". Status: "+r["status"]+". Parameter design frozen: "+str(r["design_frozen"])+". Complete 128×8 audit must pass before any random-IC production array is submitted. First eight evaluations, then waves of up to 128, maximum "+str(work["transition"]["audit_max_concurrent"])+" simulations / "+str(16*work["transition"]["audit_max_concurrent"])+" CPUs. See [launch record](random_ic_production_launch.md).\n"
if work.get("transition",{}).get("scheduler_recovery"):
    rec=work["transition"]["scheduler_recovery"]
    report+="\n## Audit scheduler recovery\n\nFinal-wave Slurm array indices exceeded MaxArraySize=1001. Compact task-to-manifest mapping now preserves the original theta/seed schedule. Recovery controller "+str(rec["controller_job"])+": "+rec["status"]+". See [recovery record](ic_audit_scheduler_recovery.md). No random-IC bulk simulation is released before the full audit passes.\n"
if work.get("transition",{}).get("queue_snapshot"):
    q=work["transition"]["queue_snapshot"]
    report+="\n## Queue snapshot\n\nChecked "+q["checked_at_hkt"]+". Audit uses zero CPUs; all 2048 reservation CPUs are allocated to existing jobs. Recovery job "+q["recovery_controller_job"]+" is PENDING. Slurm estimated start "+q["scheduler_estimated_start_hkt"]+" is provisional. See [queue status](ic_audit_queue_status.md).\n"
if work.get("transition",{}).get("completed_audit"):
    final=work["transition"]["completed_audit"]
    report=report.replace("- Complete IC sensitivity audit and qualify one-random-IC versus multi-IC averaging before formal random_ic_v2 production (100k Train / 10k Validation).", "- IC audit completed and failed the single-realization gate. Qualify a multi-IC target and inference protocol before formal random_ic_v2 production (100k Train / 10k Validation).")
    report=report.replace("Submitted scientific gate watcher:", "Last submitted scientific gate watcher (completed; no successor after gate failure):")
    report+="\n## Complete IC audit decision\n\n896/896 new realizations qualified; all 128 families have eight ICs. Zero simulation failures. Cost: 1,694.12 allocated core-hours. **MULTI_IC_AVERAGING_REQUIRED** under the confirmed conservative development gates. Single-realization random-IC production was not submitted. Thirteen families change classifier label across ICs, including two outside the near-cut band. The 2/4/8-IC finite-reference comparison does not establish that eight ICs are sufficient. See [complete audit report](ic_audit_completion.md).\n"
if work.get("transition",{}).get("explicit_random_start"):
    report=report.replace("- IC audit completed and failed the single-realization gate. Qualify a multi-IC target and inference protocol before formal random_ic_v2 production (100k Train / 10k Validation).", "- Continue explicitly authorized random-realization production: 100k Train / 10k Validation. Audit scatter failures remain documented for model/inference validation.")
    report=report.replace("Complete 128×8 audit must pass before any random-IC production array is submitted.", "The original wait-for-pass rule was superseded by explicit user authorization on 2026-10-10; see the launch update below.")
    report=report.replace("No random-IC bulk simulation is released before the full audit passes.", "This historical audit gate was superseded for random-realization data production on 2026-10-10.")
    report=report.replace("Single-realization random-IC production was not submitted.", "At audit completion, random-IC production was withheld. It has since been explicitly authorized and launched, without changing the failed audit decision.")
    report+="\n## Random-realization production launch\n\nLatest user authorization selects one independent random IC per theta. Controller 2194516 completed; array 2194518 started eight Train simulations on cn061 (128 CPUs at launch). Dependent validation/continuation job 2194519 is submitted. At that launch the simulation cap was 256 CPUs; subsequent resource changes are recorded below. Mean-history and posterior fidelity remain unqualified. See [launch record](random_ic_explicit_start.md).\n"
if (root/"results/random_ic_analysis_20261013/analysis.json").exists():
    report+="\n## Frozen random-IC data analysis\n\n9,094 qualified Train histories analyzed (separate from live production counts): 3,372 classifier-positive, 5,722 negative; 24 within 0.01 of the cut. Positive-only logit PCA K=28 achieved in-sample trajectory RMSE q95 0.00134; independent Validation and K qualification remain pending. [Analysis report and plots](random_ic_data_analysis_20261013.md).\n"
if work.get("random_development"):
    trial=work["random_development"]
    report+="\n## Random-IC first development training\n\nStatus: "+trial["status"]+". Frozen 10,000 qualified random-IC Train histories; first 512 independent frozen Validation points brought forward, admitted "+str(trial["validation_qualified"])+". Five initialization seeds: 11, 29, 47, 71, 101. Direct ResMLP, 2×30 classifier, and positive-only PCA audit / 6×80 MLP reuse the existing training protocol. Seed is not a feature; fixed-IC labels are not mixed.\n\nValidation array: "+str(trial.get("validation_array_job","not yet submitted"))+"; dependent training job: "+str(trial.get("training_job","not yet submitted"))+". Completed seeds (Direct / classifier / regressor): "+str(trial["direct_completed_seeds"])+" / "+str(trial["classifier_completed_seeds"])+" / "+str(trial["regressor_completed_seeds"])+". Errors against independent single-IC labels include IC scatter. This is development validation, not conditional-mean or posterior acceptance. [Run protocol](random_ic_development_20261014.md).\n"
if work.get("random_mcmc_development"):
    trial=work["random_mcmc_development"]
    report+="\n## Direct random-IC MCMC interface development\n\nStatus: "+trial["status"]+". Development job: "+str(trial.get("job_id"))+"; 16 CPUs, four-hour hard limit. Reuses 512 existing independent Validation histories, adding original exact LF and downstream comparisons; no new full-history simulations. Two functional short chains preserve the original fixed-view and continuous-MS priors. Classifier hard gate disabled; no posterior acceptance or production MCMC. Completed functional chains: "+str(len(trial["chain_reports"]))+"/2. [Protocol and interpretation](random_ic_mcmc_development_20261015.md).\n"
if work.get("random_mcmc_development",{}).get("validation"):
    v=work["random_mcmc_development"]["validation"]
    report+="\n512 Validation LF checks completed: "+str(v["LF_valid"])+" LF-valid, "+str(v["LF_invalid_history_retained"])+" LF-domain failures with history retained. Original exact references reproduce and LF is unchanged. On the LF-valid subset, absolute total log-likelihood error q90 = "+format(v["all_LF_valid"]["absolute_total_logL_q50_q90_q95"][1],".5f")+". These are development errors against random realizations, not posterior acceptance.\n"
metadata_recovery=root/"results/runtime_metadata_recovery_20261016/execution.json"
if metadata_recovery.exists():
    recovery=json.loads(metadata_recovery.read_text())
    report+="\n## Slurm metadata timeout recovery (2026-10-16)\n\nA worker stopped before native evaluation because its Slurm allocation metadata query exceeded 20 seconds. The allocation was preserved and classified as infrastructure failure; native/scientific contracts were rechecked. Seven software regression tests passed. Recovery job: "+str(recovery["recovery_job_id"])+"; resumed data array: "+str(recovery.get("array_job_id","not yet submitted"))+"; dependent collector: "+str(recovery.get("collector_job_id","not yet submitted"))+". Existing numerical failures are retained. No new model training or MCMC was submitted. [Incident and recovery scope](runtime_metadata_recovery_20261016.md).\n"
concurrency_revision=root/"results/concurrency_revision_20261016_32/execution.json"
if concurrency_revision.exists():
    change=json.loads(concurrency_revision.read_text())
    if change.get("status")=="APPLIED_TO_CURRENT_ARRAY_AND_FUTURE_WAVES":
        report+="\n## Concurrency update (2026-10-16)\n\nUser authorized 32 simultaneous data simulations, each with 16 CPUs: maximum 512 simulation CPUs. Applied to array 2221086 and future waves; live scheduler verification observed 32 running tasks. Physics, seeds, samples, per-simulation resources, and other jobs are unchanged. [Resource change record](concurrency_32_20261016.md).\n"
if work.get("random_model_followup"):
    f=work["random_model_followup"]
    diag=f.get("diagnostic",{})
    lc=f.get("learning_curve_16k",{})
    report+="\n## Model diagnosis and 16k learning curve (2026-10-16)\n\nCheckpoint diagnosis: "+str(diag.get("status","not started"))+"; job "+str(diag.get("job_id","not submitted"))+". Nested 16k comparison: "+str(lc.get("status","not started"))+"; job "+str(lc.get("job_id","not submitted"))+". Same 512 Validation and five seeds, unchanged training protocol. Completed Direct / classifier / regressor seeds: "+str(lc.get("direct_completed_seeds",0))+" / "+str(lc.get("classifier_completed_seeds",0))+" / "+str(lc.get("regressor_completed_seeds",0))+". No new MCMC. [Development follow-up](model_followup_20261016.md).\n"
if work.get("random_model_followup",{}).get("initialization_trial"):
    it=work["random_model_followup"]["initialization_trial"]
    report+="\nInitialization-only MLP ablation: "+it["status"]+"; job "+str(it["job_id"])+"; completed seeds "+str(it.get("completed_seeds",0))+"/5. Same frozen 10k data, PCA, six hidden layers and physical history loss. Old results retained; this is one registered diagnostic experiment, not production model replacement.\n"
if (root/"docs/acceptance_and_nnero_comparison_20261017.md").exists():
    report+="\n## Acceptance criteria and NNERO comparison\n\nFinal model accuracy thresholds remain proposals requiring scientific confirmation. Confirmed IC audit gates and preregistered PCA representation screens are separate. Current logit(xHI) PCA / physical-history MSE differs from the paper log10(Xe) / relative history plus derived-tau training. [Threshold status and paper comparison](acceptance_and_nnero_comparison_20261017.md).\n"
Path("docs/progress.md").write_text(report)
