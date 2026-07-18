# Design record — Sylhet observed-flood route pilot

`attestation_chain: ai-first` · Recorded 2026-07-19

This file occupies the factory's pre-registration slot, but it is **not a
prospective registration**. Source qualification and exploratory computation
preceded this record. It freezes the published construct, sensitivity grid,
claim limits, and decision rules so later presentation work cannot improve the
story by silently changing the model.

## Question

Within the 26 June 2024 UNOSAT analysis footprint in Sylhet, how much modeled
population loses a road-network route to an OpenStreetMap-mapped marketplace if
every road segment intersecting satellite-detected flood water is treated as
unavailable?

## Unit and population

- Origin unit: positive WorldPop 2020 raster cell inside the UNOSAT footprint.
- Destination unit: historical OSM `amenity=marketplace` object inside the same
  footprint, deduplicated spatially and snapped to the road graph.
- Network unit: historical OSM road segment whose full geometry lies inside the
  UNOSAT footprint.
- Headline denominator: modeled population within the road-snap threshold that
  has a baseline route to at least one mapped marketplace.

## Base specification

| Choice | Base | Required sensitivity |
|---|---:|---:|
| Road set | Core motorized road classes | Broad set adds `service` and `track` |
| Flood buffer around detected water | 20 m | 10 m, 30 m |
| Population-to-road snap limit | 1,000 m | 500 m, 1,500 m |
| Market-object deduplication radius | 100 m | 50 m, 150 m |

The full Cartesian grid contains 54 variants. All arbitrary numeric choices are
tested at ±50%, as required by the Constitution.

## Outcomes

Primary:

1. population with a baseline route but no post-cut route;
2. that population as a share of baseline-accessible population.

Diagnostics:

- population coverage at the road-snap gate;
- graph nodes, edges, and intersecting-edge length;
- queried, footprint-filtered, deduplicated, and snapped market counts;
- road-set comparison;
- travel-time summaries among the surviving connected population.

## Decision rules

- **Advance the routed-access construct** if all 54 variants produce positive
  disconnection and the road-set alternative does not reverse the finding.
- **Narrow to a source-boundary result** if the estimate is driven by one
  arbitrary numeric setting or by destinations outside the observed footprint.
- **Retire the access label** if no road, market, flood, and population join can
  be computed from traceable public objects.
- Never convert modeled disconnection into observed closure, behavior, income,
  food security, or welfare loss.

## Known structural assumptions

Every water-intersecting segment is removed. Flood depth, vehicle class,
bridge elevation, road surface, drainage, one-way restrictions, congestion,
boats, temporary crossings, market operating status, and household destination
choice are not observed. The analysis therefore tests a route construct under a
transparent counterfactual; it does not reconstruct actual travel on 26 June.

## Publication decision

The construct advances as a **PP construct-validation pilot**. The base result
is 345,718 modeled people disconnected, or 41.24% of baseline-accessible
population. The 54-variant range is 38.92%–43.45%. The next maturity step
requires passability and destination validation, not more polish on the same
model.
