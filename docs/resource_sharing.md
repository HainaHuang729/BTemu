# Resource sharing — 2026-10-08

Current authorized cap: 16 concurrent simulations × 16 CPUs = 256 simulation CPUs. The user clarified that halving concurrency was unnecessary, so the original cap has been restored. The intermediate eight-simulation setting and both budget revisions remain archived by SHA256.

Actual occupancy follows ordinary Slurm scheduling and available allocation; this cap is not a request to occupy all reservation nodes. The scientific thread count, parameter/IC schedules, audit qualification gate and unrelated running jobs are unchanged. Lightweight reporting/controller jobs allocate one CPU separately.
