# Sensitivity — School Heat Disruption

`attestation_chain: ai-first`. Run 2026-04-26.

The index is **very parameter-sensitive**. Top-5 set composition
shifts dramatically under tmax-floor and tmax-cap perturbations. Only
the top-1 (KHM) is parameter-robust.

| Variant | Top-1 | Top-5 stable? |
|---|---|---|
| Baseline | KHM | (set varies) |
| tmax_floor ±50% | KHM | no |
| tmax_cap ±50% | KHM | no |
| PTR cap ±50% | KHM | partial |

**Common top-1: `[KHM]`.** Honest narrowing.

The high parameter-sensitivity is itself a finding: the index
formula's tmax-ramp is the dominant driver, not the children-share or
PTR component. Future iterations should consider replacing the
linear-ramp with a more empirically grounded heat-impact function
(e.g., Lancet Countdown labor-capacity-loss curve).

## TODO §18.5

- Replace linear tmax ramp with Lancet Countdown-style heat-stress
  function.
- Subnational tasmax (CCKP country-mean is too coarse).
