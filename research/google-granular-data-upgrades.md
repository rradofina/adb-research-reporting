# Google Granular Data Upgrades

`attestation_chain: ai-first`  
Date checked: 2026-04-29

Purpose: identify Google-released or Google-hosted public datasets that can
make the research more granular while staying reproducible, licensed, and
methodologically grounded.

## Short Verdict

Yes, Google has public data that can make this work materially stronger. The
best sources are not Google Places or Google Maps business listings. Those are
useful products, but their terms are not suitable for building a persistent
research database.

The strongest research-safe Google sources are:

1. Google Open Buildings V3 and Open Buildings 2.5D Temporal.
2. AlphaEarth Foundations / Satellite Embedding V1.
3. Dynamic World land-cover probabilities.
4. Groundsource flood-event dataset and the Flood Forecasting API.
5. Google Cloud / BigQuery public datasets where licensing is compatible.
6. Data Commons for harmonized reference statistics, not for the granular
   empirical claim itself.

## Highest-Value Sources

### 1. Google Open Buildings V3

- What it gives: building footprints, centroid Plus Codes, area, and model
  confidence for 1.8 billion building detections across Africa, Latin America,
  the Caribbean, South Asia, and Southeast Asia.
- Unit: building polygon / building centroid.
- Access: Earth Engine `GOOGLE/Research/open-buildings/v3/polygons`; also
  bulk download from Google Research Open Buildings.
- License: CC BY 4.0.
- Best uses here:
  - invisible urbanization;
  - PSDQ facility catchments and facility-per-building denominators;
  - coastal informal-settlement exposure;
  - school/clinic/market catchment denominators;
  - settlement growth around road corridors.
- Caveat: model-detected buildings are not official building permits, household
  counts, or population. Rural materials, contiguous structures, high-rise
  rooftops, and visually confusing terrain need validation.

### 2. Open Buildings 2.5D Temporal

- What it gives: annual building presence, fractional building counts, and
  building heights for 2016-2023 across about 58 million square kilometers.
- Unit: 4-meter effective spatial resolution grid / annual time slice.
- Access: Google Research Open Buildings 2.5D Temporal download.
- License: dual CC BY 4.0 and ODbL.
- Best uses here:
  - invisible urbanization as a real building-growth story instead of a WDI
    urban-growth proxy;
  - poverty visibility by locating settlement growth near high-MPI regions;
  - disaster recovery by observing building-presence change around event
    footprints;
  - school heat by estimating dense built-up context around school locations.
- Caveat: the underlying high-resolution training imagery and annotations are
  not public; use as a derived open dataset, not as an inspectable imagery
  archive.

### 3. AlphaEarth Foundations / Satellite Embedding V1

- What it gives: annual, global, 10-meter, 64-dimensional geospatial
  embeddings summarizing surface conditions from multiple Earth-observation
  streams. Google documents years 2017-2025 in the GCS bucket and 2017-2025
  availability in Earth Engine.
- Unit: 10-meter pixel, 64-dimensional embedding, annual time slice.
- Access: Earth Engine `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`; Google Cloud
  Storage bucket `gs://alphaearth_foundations` is requester-pays.
- License: CC BY 4.0.
- Best uses here:
  - change detection for invisible urbanization and disaster recovery;
  - land-surface classification when local labels are sparse;
  - flood, crop, settlement, and coastal-risk feature generation;
  - validation layer for Dynamic World, GHSL, and building-change results.
- Caveat: embeddings are not directly interpretable physical bands. They are
  excellent features for clustering, classification, regression, and change
  detection, but any headline result needs labels, validation, and plain
  source notes.

### 4. Dynamic World

- What it gives: near-real-time, 10-meter land-use / land-cover probabilities
  from Sentinel-2, produced by Google with National Geographic Society and WRI.
- Unit: 10-meter pixel, land-cover class probabilities.
- Access: Earth Engine `GOOGLE/DYNAMICWORLD/V1`.
- License: CC BY 4.0 with required attribution.
- Best uses here:
  - land-cover context around schools, clinics, roads, and markets;
  - built-up and vegetation change near city edges;
  - flood and coastal exposure context;
  - interpretable baseline before AlphaEarth feature modeling.
- Caveat: it is a land-cover model, not an official land-use registry.

### 5. Groundsource Flood Events

- What it gives: 2.6 million historical flood events derived from news reports
  across more than 150 countries; Google Research frames it as an open global
  dataset for urban flash-flood modeling.
- Unit: event record with time and geography derived from public reports.
- Access: Zenodo DOI `10.5281/zenodo.18647054`; one Parquet file, about
  667 MB in version v1.
- License: CC BY 4.0.
- Best uses here:
  - flood-market access;
  - disaster-recovery lag;
  - urban flash-flood observability gaps;
  - validating where official disaster inventories miss smaller urban events.
- Caveat: media-derived events carry language, reporting, urban, and severity
  bias. Google reports 60% exact location/timing accuracy and 82% practical
  usefulness in manual review. Treat it as an event-observability layer, not
  as an official disaster inventory.

### 6. Google Flood Forecasting API

- What it gives: real-time riverine flood forecasts and access to related
  historical datasets, including inundation history and Google Runoff
  Reanalysis & Reforecast.
- Unit: forecast point / riverine forecast / historical runoff or inundation
  layer.
- Access: public, no charge, but requires waitlist approval, API key, and a
  Google Cloud project.
- License: CC BY 4.0 for exposed data.
- Best uses here:
  - near-real-time flood warning context;
  - flood-market access validation;
  - disaster early-warning data story.
- Caveat: API access is gated by approval. For reproducible papers, cache
  approved outputs and pin retrieval timestamps.

## Useful but Not the Main Claim

### Data Commons

Data Commons is a normalized knowledge graph across public statistical sources.
Use it for reference statistics, entity alignment, and quick metadata checks.
Do not use it as the original granular empirical layer unless the underlying
source and vintage are pinned.

### BigQuery Public Datasets

BigQuery public datasets are useful for M-Lab, mobility-adjacent logs where
available, and large-scale public-data joins. Google pays for storage and the
user pays for query processing beyond the free tier. Treat BigQuery as an
access layer, not automatically as a license clearance.

## Do Not Use for Persistent Research Datasets

Do not build research claims from bulk-stored Google Places, Google Maps
business listings, Routes, traffic, or similar Maps Platform content. Google's
Places policy says Places API content cannot be prefetched, cached, or stored
beyond allowed exceptions, with `place_id` treated separately. For persistent
research databases, use OpenStreetMap, Overture, healthsites.io, official
registries, or open Google Research datasets instead.

## Next-Level but Grounded Research Moves

### Move 1: Poverty Visibility + Buildings + Lights

Join OPHI/UNDP subnational MPI, Google Open Buildings 2.5D Temporal, NASA
Black Marble or VIIRS, WorldPop/GHSL, and AlphaEarth change features. The
paper asks where settlement growth and luminosity diverge from MPI deprivation.
It does not replace poverty statistics.

### Move 2: Facility Data Quality at Catchment Scale

Extend PSDQ from ADM1 counts to facility-level and ADM2 geography, then add
Open Buildings as a settlement denominator. The better question becomes:
"Where does the public-map registry gap matter for people and buildings in a
facility catchment?"

### Move 3: Road Quality + Poverty Access

Combine ADB road-quality screening, Overture/OSM/GRIP roads, Google Open
Buildings settlement growth, WorldPop/GHSL, facility and market locations,
Groundsource flood-event history, and hazard layers. The unit should be a road
segment or catchment, not a country.

### Move 4: Flood-Market Access

Use Groundsource, Global Flood Database, JRC Global Surface Water, Overture
roads, markets, facilities, WorldPop, and Open Buildings to identify flooded
road and market catchments. This is stronger than the current country-level
flood-rural proxy.

### Move 5: Invisible Urbanization

Use Open Buildings 2.5D Temporal, Dynamic World, GHSL, and AlphaEarth to
measure settlement-edge expansion directly. This would replace the current WDI
urban-growth-from-rural-base proxy with a real spatial growth measure.

## Recommended Priority

1. Add Open Buildings V3 / 2.5D Temporal to PSDQ, invisible urbanization, and
   small-area poverty.
2. Add Groundsource to flood-market access and disaster-recovery lag.
3. Use Dynamic World as the interpretable land-cover baseline.
4. Use AlphaEarth only after a validation design is written, because embeddings
   are powerful but easy to overclaim.

## Source Pointers

- Google Open Buildings V3 Earth Engine catalog: https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons
- Google Open Buildings 2.5D Temporal: https://sites.research.google/gr/open-buildings/temporal/
- AlphaEarth / Satellite Embedding V1: https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
- AlphaEarth GCS README: https://developers.google.com/earth-engine/guides/aef_on_gcs_readme
- Dynamic World: https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1
- Groundsource dataset: https://doi.org/10.5281/zenodo.18647054
- Google Flood Forecasting API: https://developers.google.com/flood-forecasting
- Data Commons docs: https://docs.datacommons.org/what_is.html
- BigQuery public datasets: https://docs.cloud.google.com/bigquery/public-data
- Google Places API policy: https://developers.google.com/maps/documentation/places/web-service/policies
