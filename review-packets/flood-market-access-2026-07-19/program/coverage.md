# Coverage — Sylhet observed-flood route pilot

`attestation_chain: ai-first`

## Spatial frame

- UNOSAT analysis footprint: 324.1 km²
- Downloaded satellite-detected flood geometry: 144.5 km²
- Event image time: 26 June 2024, 11:45 UTC
- Field validation: not completed by the source at publication

## Population funnel

| Gate | Modeled population | Share of previous gate |
|---|---:|---:|
| Inside analysis footprint | 872,293 | — |
| Within 1 km of core graph | 869,817 | 99.72% |
| Baseline route to mapped market | 838,224 | 96.37% |
| Post-cut route to mapped market | 492,505 | 58.76% |

![Coverage funnel](generated/charts/flood-sylhet-coverage-funnel.png)

WorldPop is a 2020 unconstrained modeled surface. The population totals are
weights, not an event-day census, and do not incorporate 2020–2024 growth or
flood displacement.

## Graph coverage

| Graph | Nodes | Edges | Base-buffer cut length |
|---|---:|---:|---:|
| Core | 38,365 | 39,562 | 341.3 km |
| Broad | 44,953 | 46,304 | 460.6 km |

Only segments fully inside the UNOSAT footprint are eligible. This prevents
routes from using roads outside the observed flood-analysis area as unassessed
bypasses. It also truncates real trips that may legitimately leave and re-enter
the footprint, so the boundary remains an analytical constraint.

## Destination coverage

| Gate | Objects |
|---|---:|
| Historical OSM marketplace objects in query box | 17 |
| Inside UNOSAT footprint | 11 |
| Deduplicated at 100 m | 8 |
| Snapped to core graph | 8 |
| Representative point outside buffered flood water | 8 |

There is no independent registry of all operating markets in the footprint.
The eight destinations are therefore an observed map inventory, not a complete
service census.
