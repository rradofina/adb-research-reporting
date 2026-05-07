# ADB-Facing Paper Package Priorities

Date: 2026-04-29  
Purpose: choose the next topics to turn into ADB/ERDI-style paper packages
using `.claude/skills/adb-erdi-paper-framing.md`.

This is a packaging and prioritization memo, not a new empirical result.
The first package files now live in `research/adb-paper-packages/`. Every
package still needs its evidence spine, figure source notes, and caveat box
checked before it becomes a full draft.

## First Three Packages

### 1. Public-service data quality

Why it should lead: this is already the strongest current result. It has a
clear measurement gap, concrete public-service stakes, and a result that is
hard to dismiss if the facility-level and ADM2 evidence layer is added.

ADB-style problem statement:

Public service planning increasingly depends on mapped facility data, but
public maps and official health-facility registries can diverge sharply at
the units where service coverage is planned and monitored. This brief uses
official health-facility registries, OpenStreetMap, and administrative
boundaries to measure a registry-observability gap for the Philippines and
Bangladesh. The result is a screening layer for data-quality investment and
service-access analytics, not a claim about actual clinical service
availability.

Best output form: ADB Brief plus dataset note.

Granularity story: move from ADM1 count comparison to facility record,
ADM2/province/district, duplicate cluster, and facility catchment.

Immediate chart: registry-versus-public-map coverage gap by facility tier,
with a second small panel showing missingness or match status.

Must add before stronger claim: facility-level matching, ADM2 join, facility
type harmonization, duplicate rules, and a source-note line under every chart.

### 2. Multidimensional poverty and small-area poverty visibility

Why it should be second: it is the best ADB/ERDI strategic topic because it
connects poverty, subnational granularity, data integration, and official
statistics. It is not yet the strongest computed repo result, so it should be
framed as a methods/data-integration package until the nighttime-lights join
and subnational poverty layer are fully committed.

ADB-style problem statement:

Poverty programs are designed for places and households, but comparable
poverty indicators are often published at national or broad subnational
levels. This paper assembles multidimensional poverty, subnational poverty,
population, and nighttime-light data to identify where deprivation remains
poorly observed at project-relevant geography. The output is a small-area
screen for targeting and validation, not an official poverty estimate and not
a substitute for household survey production.

Best output form: Key Indicators-style data story or Data Division methods
note.

Granularity story: subnational MPI unit joined to ADM1/ADM2, population
grid, and VIIRS/Black Marble grid cell.

Immediate chart: subnational MPI deprivation or poverty rate versus
nighttime-light intensity, with population-weighted panels and clear
coverage flags.

Must add before stronger claim: OPHI subnational MPI harmonization, SPID or
national poverty source cross-check, Black Marble/VIIRS zonal statistics,
admin crosswalk, and explicit non-claim language.

### 3. Road quality and poverty access

Why it should be third: it matches the current ADB/Arturo frontier-method
line and the user's granularity narrative. The 2026 road-quality
super-resolution paper shows the right tone: test the advanced method, report
when it does not improve prediction, and focus on what data fusion actually
adds.

ADB-style problem statement:

Road access indicators often measure whether roads exist, but project teams
also need to know whether roads are passable, maintained, and connected to
schools, clinics, markets, and poor settlements. This brief would combine
road networks, poverty and population layers, facility locations, hazard
layers, and road-quality screening data to identify corridors where poor road
condition may weaken access. The output is a maintenance and access-screening
layer, not a replacement for engineering-grade International Roughness Index
surveys.

Best output form: ADB Brief or Data Division guide/toolkit.

Granularity story: road segment, village/settlement, municipality, facility
or market catchment, and poverty-exposed corridor.

Immediate chart: map or ranked corridor panel combining poor-road-quality
screen, population/MPI exposure, and facility or market catchment.

Must add before stronger claim: road-segment validation source, surface or
roughness proxy, poverty and facility overlays, passability/hazard layer,
and a caveat that the result is for prioritization and validation.

## Next Queue

- Flood-market access: strong ADB access story once it moves from country
  flood events to flooded road segments, markets, settlements, and facility
  catchments.
- Air-monitoring: strong environmental justice story once country PM2.5 is
  replaced by gridded exposure and monitor catchments.
- Food-price climate transmission: high policy interest, but it needs
  market-month commodity prices before it can claim transmission.
- Social-protection shock coverage: good operational topic once coverage,
  payment points, delivery speed, and shock footprints are spatially linked.
- School heat disruption: intuitive and important, but it needs school
  geocodes and a defensible heat-learning or heat-attendance function.

## Packaging Rule

Do not lead with "18 topics." Lead with three ADB-grade packages and keep
the rest as a transparent pipeline. The website can still show all topics,
but the research pitch should say:

1. one finished measurement-gap package,
2. one poverty/small-area data-integration package,
3. one frontier road-quality/access package,
4. a queue of granular public-data upgrades.

That is more credible than claiming every topic is equally publication-ready.

## Source Pointers

- ADB/ERDI writing audit: `research/adb-erdi-writing-audit.md`
- Brief metadata and granularity fields: `reporting-site/src/data/briefs.ts`
- Data-source upgrade list: `reporting-site/src/data/sourceUpgrades.ts`
- Arturo/ADB road-quality ML style example: https://www.nature.com/articles/s41598-026-47749-3
- ADB road-quality ML working paper: https://www.adb.org/publications/machine-learning-satellite-imagery-road-quality-monitoring
- ADB guidebook on road-quality ML techniques: https://policycommons.net/artifacts/20142856/guidebook-on-machine-learning-techniques-for-road-quality-monitoring/21043381/
