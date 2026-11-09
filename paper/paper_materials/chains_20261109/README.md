# 8-D joint chain, 50k steps, log10(kp) + 64 walkers (2026-11-09)

Setup: 100k-point BTemu emulator; LF + Planck tau + McGreer xHI likelihood;
6 astrophysical parameters + kp + ms free; kp sampled in log10(kp);
64 walkers, 4 chains (one continuation of the 100k chain plus three
independent prior draws), 20k + 30k = 50,000 steps each.

## Convergence

| chain | steps | max R-hat | R-hat(kp) | R-hat(ms) | tau(kp) | ESS(kp) |
|---|---:|---:|---:|---:|---:|---:|
| ext | 50000 | 1.048 | 1.036 | 1.022 | 1808 | 1769 |
| indep1 | 50000 | 1.049 | 1.047 | 1.021 | 1922 | 1665 |
| indep2 | 50000 | 1.046 | 1.046 | 1.029 | 1781 | 1796 |
| indep3 | 50000 | 1.038 | 1.038 | 1.023 | 1742 | 1836 |

All chains satisfy R-hat <= 1.05 after 50,000 steps.

## Marginalised constraints (6.4 million samples, six astrophysical parameters marginalised)

| parameter | median | 68% | 95% | uniform prior |
|---|---:|---|---|---|
| kp / h Mpc^-1 | 4.8 | [1.8, 11.7] | [1.11, 27.33] | [1, 30] |
| ms | 1.70 | [1.09, 2.63] | [0.665, 3.764] | [0.5, 4] |

kp and ms remain essentially unconstrained by LF + tau + xHI; the 95% intervals
span most of the prior. A 21-cm power-spectrum term is required to constrain them.

The chain files store log10(kp) in column 7; apply 10** before interpreting it.
