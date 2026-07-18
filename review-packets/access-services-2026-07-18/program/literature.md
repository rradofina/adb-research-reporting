# Literature review — Access services

`attestation_chain: ai-first`. Updated and source-verified 2026-07-18.

## Research traditions

### 1. Geographic access is a travel-time problem

Health-facility access studies commonly combine geolocated facilities,
population, transport networks, terrain, travel-mode assumptions, and modeled
travel time. Macharia et al. demonstrate catchment allocation from travel time
and facility choice rather than a simple population-to-point ratio
[@macharia2017travel]. The implication for this program is direct: facility
load can be a screening statistic, but it is not a geographic access measure.

### 2. Facility master lists are statistical infrastructure

Reproducible facility-data work depends on current, geocoded, documented
source lists and transparent reconciliation across ministries, research
datasets, and open mapping [@south2021reproducible]. More recent work treats
comprehensive and openly usable health-facility databases as core public-data
infrastructure, while emphasizing provider coverage, temporal currency,
services, capacity, and stable identifiers [@macharia2025mapping]. A point
count without those properties is not an interchangeable denominator.

### 3. OSM coverage is uneven

Large-scale assessments of OSM show substantial geographic inequalities in
coverage and warn analysts to assess bias before drawing comparisons from the
map [@herfort2023osm]. This is not a generic footnote here. It is the mechanism
tested by the Philippine registry join: regional OSM capture varies from 6.45%
to 63.53%, and the resulting load ranks change when the denominator changes.

### 4. Boundaries and crosswalks are part of measurement

Open ADM1 boundaries make reproducible spatial joins possible
[@geoboundaries2024], but administrative changes can still break longitudinal
comparisons. The unmatched Cambodia row, Tbong Khmum, is not a missing health
system; it is a boundary-vintage problem because the 2010 facility source
predates the province.

## What this paper adds

The contribution is not another access index. It is a falsification test for
an inherited open-map screen:

1. verify that the apparent Philippine worst-region statistic is exactly the
   population divided by the OSM point count;
2. replace that denominator with the official clinical registry at the same
   subnational level;
3. measure rank movement and the association between OSM capture and apparent
   load;
4. expose where comparable registry joins are unavailable; and
5. use Cambodia to show why a second public source can reveal disagreement
   without providing current validation.

The result supports a narrower and more useful research object: a
map-observability and source-validation queue that precedes travel-time access
analysis.

## Evidence gap

The upgrade path is not a larger composite or more economies on the same OSM
denominator. It is a versioned, provider-scoped facility crosswalk followed by
travel-time, capability, and utilization layers. Until those objects exist,
service-access and welfare language remains outside the evidence.

