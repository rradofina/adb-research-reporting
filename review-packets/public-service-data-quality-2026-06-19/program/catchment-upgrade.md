---
attestation_chain: ai-first
status: methods_upgrade_ready
program: public-service-data-quality
created: 2026-04-29
---

# Catchment and Open Buildings Upgrade

## Decision

The next PSDQ upgrade should not be another ADM1 table. It should convert the
registry-versus-map gap into a local exposure question:

> Which settlements or building clusters would be affected if a project team
> used public-map facilities instead of the official registry?

The honest path is staged. The readiness audit at
`generated/psdq-catchment-readiness.json` shows that the Philippines cache is
ready for subnational admin-code joins but not facility buffers, because the
44,267 NHFR records have near-complete region/province/city/barangay codes
and no latitude/longitude. Bangladesh is now facility-buffer ready for a
coordinate subset: the current 39,421-record counting endpoint has
district/upazila fields but no coordinates, while the full 789-page richer
public facilities endpoint has 39,419 records, 29,371 records with coordinates
inside Bangladesh bounds, and catchment fields on all records. The records
without coordinates should stay visible as an uncertainty layer and can be
handled through district or upazila denominators.

The first Bangladesh facility-buffer denominator is now computed. Four
Google Open Buildings V3 point shards intersect Bangladesh. The full local
pass processed 148,982,383 catalog rows, retained 37,573,563 building points
inside the Bangladesh ADM0 boundary, and assigned 37,162,607 buildings to a
coordinate-ready DGHS facility within 5 km. At the tile-specific p85
precision threshold, the denominator is 9,110,471 buildings within 1 km,
17,545,636 within 3 km, and 18,475,230 within 5 km.

The first exposure-ranked disagreement pass is also computed. The script
retrieves OSM `amenity=hospital|clinic|doctors` features for Bangladesh,
assigns node or way/relation centers to geoBoundaries ADM3 polygons, and
joins the resulting upazila counts to DGHS active clinical facilities and
the Open Buildings denominator. Current join quality: 3,303 OSM health
features retrieved, 3,302 assigned to ADM3, 3,212 joined to DGHS upazila
rows, and 90 assigned OSM features left unmatched, mostly Dhaka urban thanas
without a clean DGHS upazila counterpart. The current top exposure-ranked
rows are Gazipur Sadar, Narayanganj Sadar, Kushtia Sadar, Pabna Sadar, and
Narsingdi Sadar.

The first road-surface context pass is now computed. The pipeline downloads
the HeiGIT/HDX Bangladesh Road Surface Data GeoPackage, assigns 650,579 road
features to geoBoundaries ADM3 polygons by representative point, and keeps
surface-class coverage explicit. The assigned network has 304,941.2 km of
OSM-length road lines; 51,327.4 km have a paved/unpaved surface class from
the combined OSM/Mapillary/deep-learning field; and 17,739.2 km of that
classified length are unpaved. The joined PSDQ road-context score is only
shown for upazilas with at least 50 km of classified road surface and at
least 10% classified-surface coverage.

The first Philippines admin-denominator pass is now computed. Eight Google
Open Buildings V3 point shards intersect the Philippines boundary. The full
local pass processed 38,122,474 catalog rows, assigned 36,447,136 building
points to PSA/NAMRIA ADM3 city/municipality polygons, and retained
13,538,628 assigned buildings at the tile-specific p85 precision threshold.
The direct NHFR code join is useful but incomplete: `PH` + NHFR
`ctymuncode` matches 35,932 of 44,267 active records. The coded pipeline now
adds a PSA PSGC 10 Digit Code to Correspondence Code resolver and deterministic
code-vintage rules for Manila district-like NHFR codes, Negros Island Region,
Sulu/BARMM, and the Special Geographic Area. The resulting ADM3 match covers
44,010 records (99.42%) and 37,135 of 37,392 clinical-tier records (99.31%).
The remaining 257 records are not imputed because the 2023 boundary code list
and NHFR codes still do not fully align. That mismatch remains part of the
PSDQ source-quality finding.

## Upgrade Ladder

### Tier 0: Current ADM1 Disagreement

This is the current computed result. It is useful as screening evidence, but
it is too coarse for project preparation. It tells us that public maps and
registries disagree, not where settlement exposure is concentrated inside a
province, district, municipality, or facility catchment.

### Tier 1: Admin-Code Building Denominators

Join registry counts and OSM facility counts to the deepest reliable
administrative unit, then aggregate Google Open Buildings inside the same
unit. This is immediately plausible for:

- Philippines: region, province, city/municipality, and barangay codes in
  NHFR. The first city/municipality pass is done, with PSGC-resolved NHFR
  codes scored and the remaining unresolved code groups held out visibly.
- Bangladesh: division, district, city corporation, upazila, and selected
  local fields in DGHS.

The output becomes a ranked list of places such as: "ADM2 units where the
registry-map gap is large and the Open Buildings denominator is high." This
does not claim true facility catchments; it is a much better prioritization
screen than ADM1 counts.

### Tier 2: Facility Coordinates and Fixed Buffers

For records with valid latitude/longitude, compute building counts inside
standard buffers, for example 1 km, 3 km, and 5 km. The main Bangladesh path
is the full DGHS public facilities JSON endpoint. The Philippines path needs
a geocoded public facility source or a defensible geocoding protocol before
facility buffers can be claimed.

The Bangladesh Tier 2 pass assigns every Open Buildings point inside
Bangladesh to only its nearest coordinate-ready DGHS facility before applying
the radius tests. This avoids double-counting the same building across
overlapping circular buffers. The output is not a real catchment or travel
time surface; it is a settlement denominator that can be joined to
registry-map disagreement, poverty, or road-quality variables in the next
analysis step.

The first join uses a transparent screening proxy:

`buildings_nearest_3km_p85 * max(active_clinical_registry - osm_health, 0) / active_clinical_registry`

This is named `underobserved_buildings_3km_p85_proxy` in the generated CSV.
It should be described as a prioritization index, not as affected people or
true demand.

The chartable measure is:

`buildings_in_buffer * registry_minus_public_map_gap_indicator`

This converts an abstract count mismatch into an immediately legible
settlement-exposure measure.

### Tier 3: Network or Travel-Time Catchments

After Tier 2, replace circular buffers with travel-time catchments using open
roads, road quality, ferry/barrier handling, and terrain where relevant. This
is where the road-quality research track becomes operationally useful, but it
should come after the coordinate and denominator audit.

The current road-surface overlay is a Tier 2.5 context layer. It can tell the
team where registry-map under-observability coincides with a higher
classified-unpaved road share, but it is not yet a travel-time model. To move
to Tier 3, route the same facility points over a network graph, validate road
passability assumptions, handle ferries and water crossings, and test results
against known travel-time or service-area benchmarks.

## Poverty Overlay Gate

Do not treat Open Buildings, road surface, or night-lights as poverty in this
package. A poverty overlay should only be added after a subnational poverty
source is retrieved with unit definitions, vintage, license, and table fields
that can be joined to the same ADM2/ADM3 geography.

The Philippines poverty-context pass now clears the PSA SAE source gate. The
owner manually downloaded the official PSA 2023 city/municipality SAE Excel
attachment from the PSA page, and Codex seeded the canonical cache with
`--sae-xlsx`. The companion join script now uses 1,597 SAE rows plus 35 PSA
OpenSTAT 2023 direct-estimate city/HUC rows. Ten ADM3 rows remain without a
source match and are not imputed.

## Google Data Use

Use Google Open Buildings only as a research-safe settlement denominator, not
as a Google Maps business/facility source. The V3 polygon dataset provides
building footprints inferred from high-resolution imagery, with area,
confidence, and centroid fields under CC-BY-4.0. The 2.5D Temporal dataset
provides annual building presence, fractional building counts, and building
height rasters for 2016-2023, with CC-BY-4.0 or ODbL licensing options.

Recommended use:

- V3 polygons for static 2023 building counts inside admin units or buffers.
- 2.5D Temporal for growth/change claims, such as facilities missing from
  public maps in newly built-up areas.
- Confidence thresholds and sensitivity checks for rural, cloudy, high-rise,
  and dense informal-settlement areas.

Do not use Google Places, Google Maps listings, Routes, or traffic products
as bulk research inputs unless the licensing and terms are explicitly cleared
for the exact use case.

## Figure Plan

1. Exposure-ranked disagreement bars: admin unit or catchment on the y-axis;
   x-axis = registry-map gap; color or size = buildings affected.
2. Small-multiple maps: one panel for registry facilities, one for public-map
   facilities, one for Open Buildings density.
3. Bubble map: bubbles at facility or admin centroids; bubble size =
   buildings in catchment; color = list-agreement ratio.
4. Uncertainty panel: results at low/medium/high Open Buildings confidence
   thresholds and at 1/3/5 km buffers.
5. Upgrade-readiness table: source, deepest unit, coordinate availability,
   building-denominator path, and current blocker.

## Non-Claims

Building counts are not population, households, poverty, or service demand.
They are a settlement-exposure denominator. Facility coordinates are not
automatically validated ground truth. Registry-list disagreement is not the
same as service availability, service readiness, staffing, quality, or
clinical performance. A paper can say where the planning data are likely weak;
it cannot say a community is unserved without travel-time, service-capacity,
and validation evidence.

## Source Note Template

Author calculations using Philippines DOH National Health Facility Registry
v2.0, Bangladesh DGHS Facility Registry, OpenStreetMap, administrative
boundaries, and Google Open Buildings. Registry records retrieved
2026-04-25; ADM1 OSM cache vintage 2026-04-05 to 2026-04-23; new ADM3
Overpass overlays use 2026-04-29 base timestamps. Open Buildings V3 is a
2023 snapshot; Open Buildings Temporal covers 2016-2023. Values are
list-agreement and settlement-exposure measures, not verified
service-availability measures.

## Implementation Checklist

1. Run `scripts/audit-catchment-readiness.py` and review
   `generated/psdq-catchment-readiness.json`. Done for the current cache.
2. Build the Bangladesh Open Buildings tile manifest, download the four point
   shards, and run `scripts/compute-bgd-open-buildings-facility-buffers.py`.
   Done for the 2026-04-29 local pass; chart-ready outputs are in
   `generated/psdq-bgd-open-buildings-*`.
3. Decide the Philippines geocoding path: admin-code denominator first, then
   facility coordinates only if a source or protocol passes review.
4. Add a chart-ready CSV with one row per admin unit or catchment:
   registry count, public-map count, gap, building denominator, uncertainty
   tier, and source timestamps. Done for BGD upazilas in
   `generated/psdq-bgd-exposure-ranked-disagreement.csv`.
5. Join the Bangladesh buffer denominator to the OSM/registry disagreement
   measure and produce the first exposure-ranked figure. Done on the PSDQ
   website.
6. Add the Bangladesh road-surface context overlay from HeiGIT/HDX road data.
   Done in `scripts/build-bgd-road-surface-context.py`, producing
   `generated/psdq-bgd-road-surface-*` and
   `generated/psdq-bgd-exposure-road-context-*`. Next step: poverty overlay
   only after a valid subnational poverty table is source-gated.
7. Build the Philippines admin-code denominator. Done in
   `scripts/build-phl-admin3-open-buildings-context.py`, producing
   `generated/psdq-phl-admin3-open-buildings-context.*`.
8. Add the Philippines poverty-context source-status join. Done
   in `scripts/fetch-phl-sae-poverty.py` and
   `scripts/build-phl-admin3-poverty-context.py`, producing
   `generated/psdq-phl-admin3-poverty-context.*`. The PSA SAE Excel attachment
   was obtained through the owner/manual source path and rerun with
   `--require-sae`.

## Sources

- Google Open Buildings V3 Earth Engine catalog:
  https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons
- Google Open Buildings project page:
  https://sites.research.google/open-buildings/
- Google Open Buildings V3 tile catalog:
  https://openbuildings-public-dot-gweb-research.uw.r.appspot.com/public/tiles.geojson
- Google Open Buildings V3 tile-specific precision thresholds:
  https://storage.googleapis.com/open-buildings-data/v3/score_thresholds_s2_level_4.csv
- Google Open Buildings Temporal V1 Earth Engine catalog:
  https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1
- Google Open Buildings 2.5D Temporal project page:
  https://sites.research.google/gr/open-buildings/temporal/
- geoBoundaries Bangladesh ADM0:
  https://www.geoboundaries.org/api/current/gbOpen/BGD/ADM0
- geoBoundaries Bangladesh ADM3:
  https://www.geoboundaries.org/api/current/gbOpen/BGD/ADM3
- HDX/OCHA Philippines subnational administrative boundaries:
  https://data.humdata.org/dataset/cod-ab-phl
- HDX/OCHA Philippines PSA/NAMRIA GDB used by the local pipeline:
  https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/314cbaea-c7a0-4ce9-a4ea-e5af2a788ac1/download/phl_adm_psa_namria_20231106_gdb.gdb.zip
- OpenStreetMap Overpass API:
  https://overpass-api.de/api/interpreter
- HDX / HeiGIT Bangladesh Road Surface Data:
  https://data.humdata.org/dataset/bangladesh-road-surface-data
- HeiGIT road-surface GeoPackage used by the local pipeline:
  https://downloads.ohsome.org/hdx/mapillary_road_surface/heigit_bgd_roadsurface_lines.gpkg
