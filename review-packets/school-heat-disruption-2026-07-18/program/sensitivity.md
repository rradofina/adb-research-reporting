# Sensitivity audit

`attestation_chain: ai-first`

## Original ±50% runs

| Run | Result |
|---|---|
| Baseline | Cambodia first |
| Temperature floor -50% | Pakistan first; Cambodia second |
| Temperature floor +50% | All-zero tie; non-discriminating |
| Temperature cap -50% | Cambodia first |
| Temperature cap +50% | Cambodia first |
| PTR cap -50% | Cambodia first |
| PTR cap +50% | Cambodia first |

The defensible statement is “Cambodia leads five of six discriminating runs,”
not “Cambodia is first in every perturbation.”

## Outcome-correlation uncertainty

Each construct-validation correlation uses 5,000 deterministic bootstrap
resamples. The six-row heatwave subset produces wide intervals:

- old index: +0.03, interval -1.00 to +1.00;
- child population: +0.94, interval +0.52 to +1.00;
- historical tasmax: +0.03, interval -1.00 to +1.00; and
- pupil-teacher ratio: -0.37, interval -1.00 to +0.81.

The intervals are a warning against generalization. No parameter retuning is
performed after observing UNICEF counts.
