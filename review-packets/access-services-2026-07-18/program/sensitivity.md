# Sensitivity — Access services

`attestation_chain: ai-first`. Updated 2026-07-18.

The original country-aggregation switch kept the same top-four OSM screen.
That result no longer carries the public claim because it perturbs the
aggregation while leaving the disputed OSM denominator unchanged.

## Claim-reshape decision sensitivity

The post-hoc decision rule retires access-ranking language if the share of
subnational ranks changed by a comparable public facility source reaches a
materiality threshold. Because the 50% threshold is arbitrary, the dossier
also tests minus 50% (25%) and plus 50% (75%).

| Comparison | Ranks changed | Share | >=25% | >=50% | >=75% | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Philippines, current official registry | 16/17 | 94.1% | Yes | Yes | Yes | Retire access rank |
| Bangladesh, current official registry | 6/8 | 75.0% | Yes | Yes | Yes | Retire access rank |
| Cambodia, 2010 public inventory | 21/24 | 87.5% | Yes | Yes | Yes | Source disagreement only |

The Philippine decision survives the full +/-50% threshold suite. Bangladesh
meets the upper threshold exactly. Cambodia also clears every numeric threshold
but cannot validate current completeness because the comparison source is from
2010 and excludes provider categories that OSM may contain.

The machine-readable result is
`generated/access-figure-dossier-summary.json`.

