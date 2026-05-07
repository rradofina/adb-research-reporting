---
attestation_chain: ai-first
package_status: adb_brief_package
topic_status: finished_for_current_issue_under_ai_first
program: public-service-data-quality
created: 2026-04-29
---

# Public-Service Data Quality

## 1. Problem Statement

Public service planning increasingly depends on mapped facility data, but
public maps and official health-facility registries can diverge sharply at
the units where service access is planned and monitored. This package uses
the Philippines Department of Health National Health Facility Registry,
the Bangladesh DGHS Facility Registry, OpenStreetMap, and administrative
boundaries to measure a health-facility registry-observability gap. The
result is a screening layer for data-quality investment and access analytics,
not a claim about actual clinical service availability or health-system
performance.

## Marginal Contribution

This is original as a narrow measurement design, not as a claim that nobody
has compared health-facility lists before. The contribution is a reproducible
Asia-Pacific DMC comparison between official health-facility registries and a
public map source, with PHL and BGD processed through a shared taxonomy,
sensitivity checks, and within-country geography. The global facility-list
literature supplies the method template; this package contributes the DMC
source stack, local gradient, and policy-facing observability-gap framing.

## 2. Key Messages

- OpenStreetMap captures 17.1% of the Philippines clinical-tier registry
  and 11.8% of the Bangladesh clinical-tier registry in the current
  two-DMC pilot.
- The useful comparison is within-country geography, not a country ranking:
  the Philippines ranges from 6.5% in BARMM to 63.5% in NCR; Bangladesh
  ranges from 6.2% in Barisal to 20.1% in Dhaka.
- The gap concentrates in community-level and primary-care facilities, which
  are exactly the facilities most likely to matter for local service access.
- Bangladesh can now move beyond ADM1: the first facility-buffer pass screens
  37.6 million Google Open Buildings points inside Bangladesh and counts
  17.5 million p85-threshold buildings within 3 km of the nearest
  coordinate-ready DGHS facility.
- The next chart is now computed, not only planned: OSM health features are
  assigned to upazilas and joined to DGHS active clinical facilities plus the
  3 km p85 Open Buildings denominator. The current exposure-ranked leaders
  are Gazipur Sadar, Narayanganj Sadar, Kushtia Sadar, Pabna Sadar, and
  Narsingdi Sadar.
- The road-quality context overlay is now computed at upazila level. It
  assigns 650,579 HeiGIT/HDX Bangladesh road-surface features to ADM3
  polygons, keeps unclassified road length visible, and joins the exposure
  screen to classified paved/unpaved road mix for 234 coverage-gated upazila
  rows.
- The Philippines now has a city/municipality denominator screen: 36.4
  million Open Buildings points are assigned to 1,642 PSA/NAMRIA ADM3 units,
  with 13.5 million at the p85 precision threshold. Direct NHFR code matching
  covers 35,932 of 44,267 active records; the PSA PSGC correspondence-code
  resolver raises the ADM3 match to 44,010 records (99.42%) and 37,135 of
  37,392 clinical-tier records (99.31%). The remaining 257 records are
  retained as a code-vintage data-quality finding, not imputed.
- This is already the strongest computed package in the repo, but a human-
  final version needs ADM2 geography, facility-level matching, duplicate
  rules, and a third source for triangulation.

## 3. Evidence Spine

- Current unit: ADM1, covering 17 Philippine regions and 8 Bangladesh
  divisions.
- Target unit: facility record, duplicate cluster, ADM2/province/district,
  facility catchment, and settlement/building denominator.
- Source stack: Philippines DOH NHFR v2.0 active facilities, Bangladesh
  DGHS Facility Registry, OpenStreetMap `amenity=hospital|clinic|doctors`,
  geoBoundaries ADM1, and Google Open Buildings V3 or 2.5D Temporal for
  catchment-scale settlement denominators.
- Retrieval window: DOH and DGHS registry pulls on 2026-04-25; ADM1 OSM
  cache vintage 2026-04-05 to 2026-04-23; new ADM3 Overpass overlays use
  2026-04-29 base timestamps.
- Repository evidence: `public-service-data-quality/results.md`,
  `public-service-data-quality/limitations.md`,
  `public-service-data-quality/sensitivity.md`, and
  `public-service-data-quality/generated/public-service-data-quality-summary.json`.
- Catchment upgrade evidence: `public-service-data-quality/catchment-upgrade.md`
  and `public-service-data-quality/generated/psdq-catchment-readiness.json`.
  Current finding: PHL is admin-code ready but not coordinate ready; BGD has
  a full 789-page coordinate-bearing public-facility pull with 39,419 records,
  29,371 Bangladesh-bounded coordinate records, and catchment fields on all
  records.
- Bangladesh Open Buildings denominator evidence:
  `public-service-data-quality/generated/psdq-bgd-open-buildings-buffer-summary.json`,
  `psdq-bgd-open-buildings-facility-buffers.csv`, and
  `psdq-bgd-open-buildings-admin-summary.csv`. Current finding: four
  Open Buildings V3 point shards intersect Bangladesh; 148,982,383 catalog
  rows were processed, 37,573,563 points were retained inside Bangladesh,
  and 37,162,607 were assigned to a coordinate-ready DGHS facility within
  5 km. At p85 precision, the nearest-facility denominator is 9,110,471
  buildings within 1 km, 17,545,636 within 3 km, and 18,475,230 within
  5 km.
- Bangladesh exposure-ranked disagreement evidence:
  `public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json`,
  `psdq-bgd-exposure-ranked-disagreement.csv`, and
  `psdq-bgd-osm-health-upazila.csv`. Current finding: 3,303 OSM health
  features were retrieved from Overpass; 3,302 were assigned to ADM3; 3,212
  joined to DGHS upazila rows; and the total gap-weighted 3 km p85
  denominator is 15,668,648 buildings.
- Bangladesh road-surface context evidence:
  `public-service-data-quality/generated/psdq-bgd-road-surface-summary.json`,
  `psdq-bgd-road-surface-upazila.csv`,
  `psdq-bgd-exposure-road-context-summary.json`, and
  `psdq-bgd-exposure-road-context.csv`. Current finding: 304,941.2 km of
  assigned OSM-length road lines, 51,327.4 km with a paved/unpaved surface
  class, and a classified unpaved share of 34.6%. The service-gap plus
  road-context chart only scores rows with at least 50 km classified road
  length and at least 10% classified-surface coverage.
- Philippines ADM3 denominator evidence:
  `public-service-data-quality/generated/psdq-phl-admin3-open-buildings-context-summary.json`,
  `psdq-phl-admin3-open-buildings-context.csv`, and
  `psdq-phl-open-buildings-tile-manifest.json`. Current finding: eight
  Philippines-intersecting Open Buildings shards were processed; 36,447,136
  building points were assigned to PSA/NAMRIA ADM3 polygons; 13,538,628
  assigned buildings pass the p85 precision threshold; 6,544 OSM health
  features were assigned to ADM3; and the direct-code NHFR join plus PSA PSGC
  correspondence-code resolver matches 44,010 of 44,267 active records. The
  top exposure-screen rows are Zamboanga City, Davao City, Cagayan de Oro
  City, General Santos City, and Quezon City. The remaining unresolved code
  groups remain visible and excluded from publication-grade city scoring.
- Claim status: finished for the current issue under ai-first attestation;
  upgrade-eligible to human-final after actual external review and owner
  re-attestation.

## 4. Proposed Section Outline

1. Why facility-list agreement matters for planning
2. Data sources and taxonomy harmonization
3. Registry-versus-map coverage by country and administrative unit
4. Where the gap is largest and why the direction is not fully adjudicable
5. Sensitivity tests and falsification checks
6. What an ADM2 and facility-level upgrade would add
7. Policy use for ADB sector teams, ministries, and national statistics
   systems

## 5. Figure and Table Plan

1. Registry-versus-OSM coverage by country and facility tier.
   - Chart type: grouped bar chart.
   - Source note: Author calculations using DOH NHFR v2.0, DGHS Facility
     Registry, OpenStreetMap, and geoBoundaries; registries retrieved
     2026-04-25; OSM vintage 2026-04-05 to 2026-04-23. Unit = facility
     records aggregated to ADM1. Values are list-agreement measures, not
     verified service-availability measures.
2. ADM1 coverage-gradient panel.
   - Chart type: ranked dot plot or horizontal bar chart by ADM1.
   - Source note: Same as above. Notes must state that Bangladesh has only
     8 divisions and is therefore illustrative for gradient comparison.
3. Upgrade-readiness table.
   - Columns: data source, deepest reliable unit, coordinate-pair coverage,
     Open Buildings denominator path, current blocker, and next action.
4. Bangladesh settlement-exposure chart from the computed facility buffers.
   - Chart type: p85 radius-sensitivity bars plus ranked upazila bars.
   - Source note: Same as above, plus Google Open Buildings V3 point CSVs,
     Google tile-specific precision thresholds, and geoBoundaries Bangladesh
     ADM0; local denominator pass generated 2026-04-29. State clearly that
     buildings are settlement-exposure denominators, not people, households,
     poverty, verified catchments, or service demand.
5. Bangladesh coordinate-readiness panel.
   - Chart type: metric cards plus ranked upazila coordinate-coverage bars.
   - Source note: DGHS public facilities JSON endpoint; full 789-page cache
     retrieved 2026-04-29; coordinates screened only against Bangladesh
     bounds.
6. Top-upazila exposure table.
   - Current exposure-ranked leaders: Gazipur Sadar, Narayanganj Sadar,
     Kushtia Sadar, Pabna Sadar, and Narsingdi Sadar.
   - Purpose: show reviewers that the pipeline produces project-preparation
     units, not only national or ADM1 summaries.
7. Bangladesh road-context triage panel.
   - Chart type: classified paved/unpaved stacked bar, top upazilas by
     classified unpaved road length, and service-gap rows with road-surface
     context.
   - Source note: Same as the exposure chart, plus HeiGIT/HDX Bangladesh Road
     Surface Data from OSM, Mapillary imagery, and deep-learning surface
     classification; local road overlay generated 2026-04-29. State that the
     score is a prioritization screen, not travel time, poverty, road
     passability, or a service-access effect.
8. Philippines ADM3 denominator and code-match panel.
   - Chart type: metric cards, ranked city/municipality exposure bars, ranked
     remaining unresolved NHFR code groups, and largest p85 building
     denominators.
   - Source note: DOH NHFR cached active-facility endpoint, OpenStreetMap
     Overpass, PSA PSGC correspondence tables, HDX/OCHA Philippines
     PSA/NAMRIA administrative boundaries, and Google Open Buildings V3 point
     CSVs and tile-specific precision thresholds. State that remaining
     unresolved NHFR city codes are excluded from ADM3 scoring.

## 6. Caveat / Non-Claim Box

This package does not establish that OpenStreetMap is wrong or that the
official registry is complete. It establishes systematic disagreement between
two public planning data sources. It does not rank countries, does not measure
service readiness, does not infer staffing or medicine availability, and does
not establish causal mechanisms for the rural-urban gradient. A publication-
grade version needs a third facility source, ADM2 geography, and stratified
manual validation.

## 7. Policy-Use Paragraph

ADB health, governance, urban, and data teams can use this package to identify
where project preparation should not rely on public maps alone. Ministries of
Health and national statistics offices can use the same logic to prioritize
health-facility master-list cleanup, geocoding, duplicate removal, and public
sharing. The operational value is strongest at ADM2 or facility-catchment
level, where mismatched lists can change travel-time access, settlement or
building exposure, service-load, and investment-prioritization results.

## 8. References and Source Notes to Add

- World Health Organization. n.d. Geolocated Health Facilities Data
  initiative. https://www.who.int/data/GIS/GHFD
- Maina, Joseph, et al. 2019. "A spatial database of health facilities
  managed by the public health sector in sub Saharan Africa." Scientific
  Data 6:134. https://www.nature.com/articles/s41597-019-0142-2
- South, Andy, et al. 2021. "A reproducible picture of open access health
  facility data in Africa and R tools to support improvement." Wellcome Open
  Research 5:157. https://wellcomeopenresearch.org/articles/5-157
- Herfort, Benjamin, et al. 2023. "A spatio-temporal analysis investigating
  completeness and inequalities of global urban building data in
  OpenStreetMap." Nature Communications 14:3985.
  https://www.nature.com/articles/s41467-023-39698-6
- Repository source: `articles/measurement-gap-philippines-bangladesh.md`.
- Google Open Buildings V3. https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons
- Google Open Buildings project and V3 tile catalog:
  https://sites.research.google/open-buildings/ and
  https://openbuildings-public-dot-gweb-research.uw.r.appspot.com/public/tiles.geojson
- Google Open Buildings V3 precision thresholds:
  https://storage.googleapis.com/open-buildings-data/v3/score_thresholds_s2_level_4.csv
- geoBoundaries Bangladesh ADM0 API:
  https://www.geoboundaries.org/api/current/gbOpen/BGD/ADM0
- geoBoundaries Bangladesh ADM3 API:
  https://www.geoboundaries.org/api/current/gbOpen/BGD/ADM3
- HDX/OCHA Philippines subnational administrative boundaries:
  https://data.humdata.org/dataset/cod-ab-phl
- HDX/OCHA Philippines PSA/NAMRIA GDB used locally:
  https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/314cbaea-c7a0-4ce9-a4ea-e5af2a788ac1/download/phl_adm_psa_namria_20231106_gdb.gdb.zip
- OpenStreetMap Overpass API:
  https://overpass-api.de/api/interpreter
- HDX / HeiGIT Bangladesh Road Surface Data:
  https://data.humdata.org/dataset/bangladesh-road-surface-data
- HeiGIT Bangladesh road-surface GeoPackage:
  https://downloads.ohsome.org/hdx/mapillary_road_surface/heigit_bgd_roadsurface_lines.gpkg
