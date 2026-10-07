# IC audit scheduler recovery — 2026-10-07

770 / 896 fresh realizations are qualified; 110 / 128 families have eight ICs, with zero failed simulation receipts. The last submission was rejected because frozen manifest indices reached 1023 while Slurm MaxArraySize is 1001. These 126 evaluations never started and incurred no simulation allocation.

The launcher now uses compact 0..125 array positions mapped to the original frozen manifest indices. Rejected submissions are retained in the submission registry but excluded from simulation-attempt ordinals. Native, theta, seeds, thresholds and resource limits are unchanged. Recovery controller: 2192051. Software regression check: 2192053.

The partial scientific result does not pass the confirmed single-IC screen: q90 sigma_tau=0.0001348, sigma_xHI(5.9)=0.007287, sigma_logL_tau=0.1235 and sigma_logL_xHI=0.8297. Eleven families have classifier flips, all within the declared near-cut band. These are 110-family development statistics, not final acceptance. Full audit completion is still required; random-IC bulk production remains unstarted.
