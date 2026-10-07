# Website update policy

The public dashboard separates completed work, current work and pending scientific acceptance. It exports aggregate development receipts only; no history labels, checkpoints, native libraries or sealed payloads are published.

A bounded publisher checks qualified data and training completion receipts every hour, up to 720 checks. Each check requests one CPU, 1 GiB memory and a two-minute limit on an allowed project node. Queuing and GitHub Pages deployment can delay visibility. Completed training is identified by completion receipts, not submission or Slurm exit alone.

The dataset timestamp is the latest completed-wave validation snapshot. Training timestamps are the corresponding status/completion receipt modification times. A cap of 32 simulations is configuration information, not live CPU occupancy. An incomplete job is never shown as completed.

The publisher uses an exclusive lock, checks for unrelated repository changes, commits only `site/progress.json`, `site/work_status.json` and `docs/progress.md`, and pushes to the existing GitHub Pages repository. Publication failure does not stop or modify scientific production. Errors and the next job ID are recorded independently in the scientific workspace's `maintenance/public_progress/state.json`. No email is sent.

Public source configuration templates retain submission disabled. Scientific authorizations and simulation scheduling are separate from website publishing.
