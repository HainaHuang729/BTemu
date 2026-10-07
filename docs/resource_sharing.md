# Resource sharing — 2026-10-08

User requested capacity for other users. Audit and conditional random-IC production now allow at most eight simulations concurrently: 8 × 16 = 128 simulation CPUs. The 16-thread scientific/IC convention is unchanged. Lightweight scheduler/reporting jobs each allocate one CPU separately.

No audit simulation is currently running. Six other running jobs under the same account user allocate 1536 CPUs across other projects. Reducing this emulator cap does not release those existing allocations; their running state was not modified. No claim is made that this change immediately creates idle nodes.

Previous budget files were archived by SHA256. Pending recovery controller 2192051 reads the new cap when it starts; no simulation arrays need live throttling at present. The complete IC audit remains a prerequisite for random-IC production.
