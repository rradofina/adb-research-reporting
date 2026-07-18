# Coverage — Access services

`attestation_chain: ai-first`. Updated 2026-07-18.

## Analytic coverage

| Layer | Coverage | Comparable use in this paper |
|---|---:|---|
| Legacy OSM/population pilot | 8 DMCs, 104 ADM1 units | Source-validation queue only |
| Philippines official clinical registry join | 17 of 17 regions | Main denominator and rank falsification |
| Bangladesh official facility registry join | 8 of 8 divisions | Supporting registry check |
| Cambodia 2010 public-facility inventory | 24 of 25 access-panel provinces joined | Source-disagreement and vintage test only |
| Other pilot DMCs | 6 economies without a comparable registry correction in the committed module | No corrected cross-economy rank |

The pilot economies are PHL, BGD, PAK, NPL, LKA, KHM, LAO, and TLS. The
current paper does not generalize to the other ADB DMCs.

## Source and version ledger

| Object | Geography / time | Role | Binding limitation |
|---|---|---|---|
| OSM health amenities | 8-DMC ADM1 extraction, timestamped 2026 | Open-map point denominator | Mapping effort and tagging vary spatially |
| geoBoundaries gbOpen | ADM1 boundary release recorded in manifest | Spatial join | Boundary vintages can differ from registries |
| PSA 2020 and WorldPop 2024 population | PHL census; other pilot ADM1 population | Numerator | Population vintages differ across economies |
| Philippine DOH NHFR v2.0 | Clinical registry retrieved 2026 | Main comparison denominator | Registry taxonomy is narrower than all possible OSM health tags |
| Bangladesh DGHS Facility Registry | Registry retrieved 2026 | Supporting comparison denominator | Same taxonomy/currency caveat |
| Cambodia HDX/MoH/OCHA public facilities | 2010 inventory, package retrieved 2026 | Source-disagreement audit | Sixteen-year vintage gap; public-provider scope only |

## Missingness is part of the result

Only 2 of 8 pilot economies have a comparable registry correction in the
committed cross-economy module. Missing corrections are not zero facilities.
They identify where a common access rank cannot be supported from the present
data architecture.
