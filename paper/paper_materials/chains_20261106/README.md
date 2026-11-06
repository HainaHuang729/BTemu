# MCMC chains (2026-11-06)

All chains use the 100k-point BTemu emulator unless stated otherwise;
32 walkers, 3000 steps, fixed KP/MS unless the name says otherwise.

| file | configuration |
|---|---|
| `kp10_ms2p5_100k.h5` | KP=10, MS=2.5 |
| `kp1_ms1p5_100k.h5` | KP=1, MS=1.5 |
| `kp5_ms1p5_100k.h5` | KP=5, MS=1.5 |
| `kp10_msfree7d_100k.h5` | KP=10, MS free (7-D) |
| `pl_100k.h5` | standard power spectrum (POWER_SPECTRUM=0) |
| `joint_kpms8_100k_600steps.h5` | KP and MS free (8-D), 600 steps |

## Marginalised credible intervals (integrating out the six astrophysical parameters)

| chain | KP median | KP 68% | KP 95% | MS median | MS 68% | MS 95% |
|---|---|---|---|---|---|---|
| 65k model, 16018 steps | 15.74 | [6.34, 25.57] | [3.26, 29.36] | 2.04 | [1.05, 3.26] | [0.59, 3.88] |
| 100k model, 600 steps | 17.71 | [8.39, 24.95] | [4.42, 29.07] | 1.81 | [0.99, 3.38] | [0.58, 3.96] |
| combined, 16618 steps | 15.96 | [6.46, 25.62] | [3.28, 29.36] | 2.03 | [1.04, 3.27] | [0.59, 3.89] |

KP and MS remain essentially unconstrained by LF + Planck tau + McGreer xHI:
the 95% intervals span almost the full prior. A 21-cm power-spectrum term is
required to constrain them.
