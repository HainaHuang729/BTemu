> 2026-10-03 科学定义澄清：[history fidelity target](history_fidelity_target.md)。端点只作 SCIENCE_DOMAIN_WARNING，不使数值有效标签失效；A emulator fidelity、B 原后处理 fidelity、C 物理模型有效性分开判断。下文的历史进度记录不覆盖当前机器验收状态。

# Frozen Train continuation, 2026-09-29

Status at resume: TRAIN_BATCH1_SUBMITTED. Slurm job 2160513, indices 12 and 13 (zero-based), PENDING(Resources). Two tasks, each 16 CPUs, 16 GiB, maximum two hours, maximum concurrency two. New wave reserves 64 core-hours under the unchanged Train 2000 core-hour ceiling.

At resume: 448 planned unique Train points; 12 attempted, 11 admitted, one failed, 436 not yet attempted. Failed broad_rectangle_000011 remains failed because observed LF magnitudes at z=6 lie outside the model grid. No replacement or automatic numerical retry. The old 45 quarantined records remain isolated.

Native qualification remains PREFLIGHT_PASSED with 12 qualified evaluations from 14 attempts. Its original checksum and all existing admissions are preserved. A hash-bound orchestration migration verifies every scientific compute/QA file unchanged. No additional preflight simulation was executed.

Independent Train errors no longer halt later frozen points. Workers invoke advance_batch1.py after generation, which records errors and submits the next two points through the existing budgeted submitter. Successful labels still require original postprocessing validation before admission. Invalid provenance is never admitted. Existing identity, qualification and budget gates remain enforced. When all points have terminal receipts, failures produce TRAIN_BATCH1_PARTIAL with all_planned_attempted=true rather than claiming 448 qualified labels. Hard allocation termination before any durable receipt can still require accounting reconciliation; no unlimited retries are enabled.

Fixed the qualified development manifest to reference admission receipts. All 11 actual receipt links and artifact checksums passed collection. Actual native-backed training-loader verification runs on the compute worker callback; it has not yet been claimed passed in this report. Sixteen focused continuation/admission tests passed. Broader test discovery exited 137; no broad-suite pass is claimed. A status-accounting field typo found during deployment was corrected before the queued workers started, and the real collector then passed.

Last reconciled costs: Train 32.28 core-hours, preflight 34.7733333333, runtime probes 0.0033333333. Total 67.0566666667, plus the new wave reservation of 64. These are snapshots; live accounting is in data_runs/20260928_batch1/submission_accounting.json. Subsequent waves reconcile terminal Slurm accounting and retain conservative reservations for unresolved jobs.

No model training, validation/challenge generation, sealed generation/access, or production MCMC. Failure aggregation: data_runs/20260928_batch1/train_error_summary.json and results/failure_registry.jsonl. Automatic continuation is contained in the submitted generate.sbatch job, not a detached login process. Additional future waves are conditional submissions, not already-submitted job IDs.
