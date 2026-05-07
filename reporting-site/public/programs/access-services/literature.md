# Literature review — Access to Services

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27.

## 1. Search record

Queries (2026-04-27):
1. `Macharia travel-time isochrone health-facility access`
2. `OpenRouteService AccessMod LMIC service-access`
3. `KEMRI WorldPop facility-access raster`
4. `UN-Habitat access-to-services SDG indicator`

Tier-A: *Lancet Global Health*, *Population Health Metrics*,
*BMJ Global Health*. Tier-B: KEMRI–Wellcome, WorldPop, HeiGIT.
Tier-C: WHO Public Health Mapping bulletins.

## 2. Verified entries

- **`macharia2017travel`** — Macharia et al. (2017). Travel-time-
  isochrone allocation methodology. *Malaria Journal* 16.
  doi:10.1186/s12936-017-2009-3. **Methodology baseline for
  the §18.5 upgrade-pass.**
- **`south2021reproducible`** — South et al. (2021).
  afri-healthsites toolchain. **Methodology template.**
- **`herfort2023osm`** — Herfort et al. (2023). OSM completeness
  inequalities; relevant for the OSM-coverage caveat.
- **`geoboundaries2024`** — geoBoundaries gbOpen ADM1 polygons.

## 3. Synthesis

1. **Travel-time isochrones are the standard access measure**
   [@macharia2017travel] — facility count is a coarse proxy.
2. **OSM amenity counts under-count official registries** (PSDQ
   finding for PHL/BGD); the access-stress signal inherits the
   under-count.
3. **Reproducible-data toolchains exist** [@south2021reproducible]
   for cross-country health-facility comparison.

## 4. Gap

No published 8-DMC-pilot pop-weighted access-stress ranking with
aggregation-stability testing. The top-4 set finding is the
marginal contribution within the pilot scope.

## 5. First testable claim

> Among the 8 ADB DMCs in the pilot, four — Bangladesh, Cambodia,
> Lao PDR, Pakistan — persistently hold the top-4 country-level
> access-stress positions across alternative country aggregations.

## 7. §18 attestation

`ai-first`. 2026-04-27. Pilot scope; 8/50 DMCs.
