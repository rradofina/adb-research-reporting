# Figure plan — Climate-health labor capacity

`attestation_chain: ai-first`

Last updated: 2026-07-18.

| Figure | Reader question | Committed input | Visual role | Removal rule | Required caveat |
|---|---|---|---|---|---|
| Research hero | Do the two 2020 top threes agree? | `generated/climate-health-construct-validation.json` | Paired lists with 0/3 overlap | Remove if years or common sample differ | Heat side is modelled potential loss |
| Rank disagreement | Where do the 34 economies move? | `generated/climate-health-proxy-heat-comparison.csv` | Slopegraph with headline reversals | Remove if labels or rank direction are unclear | Rank is not policy performance |
| Parameter sensitivity | Does proxy tuning restore agreement? | `sensitivity-runs.json` | 3 × 7 overlap heatmap | Remove if ±50% choices are not shown | One-at-a-time sensitivity |
| 2024 heat profile | Which covered rows have high per-worker estimates? | `generated/climate-health-heat-workloss-panel.csv` | Ranked bars | Remove if interpreted as observed absence | Annual potential hours per employed person |
| Rate versus scale | How do per-worker intensity and aggregate burden differ? | same panel | Bubble scatter with log total axis | Remove if bubble area or log scale is hidden | Outdoor-worker count is modelled |
| Worker denominator repair | How large was the total-population error? | panel plus denominator audit | Ratio bars around parity | Remove if Lancet is presented as a census | Comparison benchmark is modelled |
| Sector composition | Why does the direct construct differ? | heat panel sector fields | Stacked shares | Remove if sectors are treated as observed schedules | National sector shares applied in grids |
| Source coverage | Which validation layers remain open? | construct-validation summary | Coverage bars | Remove if 0 is read as nonexistence | 0 means not joined in this package |

Every figure names the unit, vintage, source, limitation, and
`attestation_chain: ai-first`. No decorative chart is retained.
