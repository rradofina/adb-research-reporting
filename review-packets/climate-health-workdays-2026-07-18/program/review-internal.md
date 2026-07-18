# Internal review — Climate-health labor capacity

`attestation_chain: ai-first` · critique pass 2026-07-18

## Decision

**Accept as PP after claim replacement.** The old pressure-cluster claim is not
accepted. The construct-validation result is supported by committed scripts,
aligned data, required sensitivity, and explicit limits.

## Critical checks

| Check | Finding | Resolution |
|---|---|---|
| Construct | PM2.5 and WBGT heat loss are different mechanisms | Replace ranking with validation failure; do not combine them |
| Vintage | Latest-value joins could create artificial disagreement | Use common annual 2018–2020 rows only |
| Units | Lancet sector totals are thousands of hours | Convert ×1,000 in the evidence pipeline and regenerate |
| Outcome | Potential loss could be mistaken for absence | Repeat modelled-potential label in title support, charts, method, and limits |
| Denominator | Total population was used as workers | Repair with employed people aged 15+ and keep old value only as error evidence |
| Ranking ethics | Country order could imply performance | Frame as construct disagreement and planning units, not grades |
| License | Lancet terms are more restrictive than the article license | Record source license and require downstream compliance |

## Remaining limitation

No observed labor outcome is joined. This is a stated stopping condition, not
a hidden omission. It prevents progression beyond PP without a new data object.
