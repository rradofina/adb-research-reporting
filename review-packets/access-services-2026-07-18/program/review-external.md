# External red-team review — Access to Services

`attestation_chain: ai-first`. §18.4 AI synthesis. Closed 2026-04-27.

**No individual reviewer was contacted.**

## Roster

| ID | Institution | Synthesized from |
|---|---|---|
| C-1 | KEMRI–Wellcome / WorldPop | Travel-time isochrone work |
| C-2 | Macharia / Snow / Okiro network | Health-facility access measurement |
| C-3 | HeiGIT (Heidelberg) | OSM data quality |
| C-4 | UN-Habitat | Service-access indicators |

## Objections

**C-1 (KEMRI/WorldPop).** Facility-count is a poor proxy for access.
Travel-time isochrones (mode-of-transport-aware, terrain-aware,
network-distance) is the standard. afri-healthsites and accessmod
are the toolchains.

**C-2 (Macharia/Snow).** PSDQ has shown OSM under-counts the official
registry by 80%+ in PHL and BGD. Using OSM amenity counts as the
service-availability layer here therefore inherits that
under-count. Triangulation with national health-facility registries
is the §18.5 upgrade.

**C-3 (HeiGIT).** OSM completeness varies dramatically by country
and by ADM1. The access_stress_index already includes an
osm_completeness_risk_score component, but the score is itself
a proxy.

**C-4 (UN-Habitat).** Service access has multiple dimensions
(health, education, market). Aggregating all into a single score
loses sectoral specificity.

## Responses

All accepted. §18.5 upgrade-pass: (a) travel-time isochrones via
ORS or Google Maps; (b) NHFR/DGHS triangulation (already done in
PSDQ for PHL/BGD); (c) sectoral disaggregation.

## §18.4 non-claim

No individual reviewer was contacted.

## 2026-07-18 red-team synthesis addendum

The completed source tests resolve the central objection by changing the
claim, not by defending the proxy.

- **Travel-time measurement position:** accepted. The paper now states that
  population per point is not access and places travel-time modeling in the
  upgrade gap [@macharia2017travel].
- **Facility-master-list position:** accepted. Current, geocoded,
  provider-scoped and versioned facility sources are treated as necessary
  infrastructure, not an optional robustness check [@south2021reproducible;
  @macharia2025mapping].
- **OSM data-quality position:** accepted and tested. The Philippine
  completeness ratio is associated with the apparent load, and official
  registry substitution reorders 16 of 17 ranks [@herfort2023osm].
- **Multidimensional-access position:** accepted. Education and market points
  are removed from the research claim rather than blended into a headline
  composite.

Remaining red-team objection: even an official registry does not measure
availability, capacity, quality, or use. The paper accepts this and stops at
denominator falsification. No individual reviewer was contacted; all positions
remain AI synthesis under §18.4.
