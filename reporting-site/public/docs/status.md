# Current research status — operating board

**Principle.** This file is the **board, not the file**. Its job is to point
to the active flagship and to define how a session opens, runs, and closes.
Per-program detail — last completed, next focused work, current blockers,
program-specific runbooks — lives in `{program}/STATUS.md` or in the
program's `README.md`. If you find PSDQ-specific narrative here, move it.

Last updated: 2026-06-20.

## Current focus

| Field | Value |
|---|---|
| Active flagship | `air-monitoring` (L3 candidate; prototype surface at `/showcase/air-monitoring-observability`; concentration/GDP-confound deepening, metadata-readiness audit, OpenAQ station-metadata source-access pass, station map, regulator-source wall, official station-source extraction, official-to-OpenAQ reconciliation audit, candidate station-crosswalk review worksheet, candidate public-evidence audit, candidate crosswalk source scan, candidate public-feed source scan, one-signal review queue, monitor-grade evidence ladder, monitor-grade source-validation wall, monitor-grade station-review wall, exact station method-evidence wall, Uzbekistan current/method wall, Uzbekistan method-policy wall, Uzbekistan station-specific source wall, Uzbekistan status/certification wall, Uzbekistan blocker wall, Indonesia/Georgia method-context wall, station-code status/method wall, station-grade decision ledger, station-method classification audit, BMKG operation/maintenance source scan, and Georgia report-verification source scan exist; station-radius, validated station-crosswalk, and complete monitor-grade claims remain blocked until station-level method/current-status sources, crosswalk evidence, and catchment denominators are added) |
| Per-program board | `air-monitoring/STATUS.md` |
| Operating mode | §18 ACTIVE (AI-First) |
| Default review mode | Mode A (AI-only); see `research/factory.md` |
| Previous flagship | `public-service-data-quality` (PR; evidence ladder closed in commit `8913943`; AI-doable work is back at the owner-only source-owner contact or human-validation wall) |

The active flagship is the only program that may be advanced this session.
Rotation reason recorded in the operational notes below. Programs in the
queue are listed in `research/wip-register.md` and `CONSTITUTION.md` §15.
Do not silently switch programs; rotation requires recording the reason
here before switching.

## Next-up queue

Ordering by Mode-A readiness (cheapest path to "ai-first finished for
current issue" under the publication ladder + review loop). The owner
overrides priority by editing this list.

1. **`air-monitoring`** — *current active flagship; L3 candidate*. The
   existing deepening proves the zero-monitor population headline is
   concentrated in Papua New Guinea and Timor-Leste and that monitor-density
   patterns are strongly confounded with GDP per capita among monitored
   economies. The metadata-readiness audit made the station-level wall
   explicit; the OpenAQ station-metadata source pass and public station panel
   now supply 101 coordinate rows for 11 upgrade-queue economies, record 2
   coordinate-QC exclusions, and keep 13 economies at OpenAQ-visible zero. The
   regulator-source discovery pass identifies 9 official inventory or
   air-quality portal candidates, 6 official station-count claim rows, and 0
   monitor-grade classification rows, now surfaced in a public source wall.
   The official station-source extraction retrieves the 9 targeted official
   sources, normalizes 230 official station-coordinate rows across 5
   economies, keeps 6 station name-only rows, 1 count-only row, and 2
   plan-count-only rows separate, and finds 22 coordinate rows within 5
   kilometers of an OpenAQ PM2.5 row as a screening diagnostic. The
   official-to-OpenAQ reconciliation audit covers the 230 official coordinate
   rows and 82 OpenAQ coordinate rows in the same five economies, classifying
   13 near-plus-name candidate rows, 9 near-only candidate rows, 22
   name-only-not-near candidate rows, 186 official coordinate rows without
   either candidate signal, and 0 validated same-station joins. The candidate
   review worksheet then turns the 13 near-plus-name rows into row-level
   reviewer questions across 4 economies, while recording 0 station-ID
   crosswalk rows, 0 current-status confirmation rows, 0 validated
   same-station joins, and 0 station-radius-ready rows. The candidate
   public-evidence audit attaches OpenAQ owner/provider and `isMonitor`
   metadata to those 13 rows, finding 13 owner/provider rows, 6 OpenAQ
   `isMonitor` true rows, 7 not-`isMonitor` rows, 0 exact station-ID overlaps,
   0 exact agency owner/provider matches, 0 explicit crosswalk rows, 0
   validated same-station joins, and 0 station-radius-ready rows. The candidate
   crosswalk source scan then retrieves five public source URLs and screens all
   6 OpenAQ `isMonitor` candidate rows as separate nearby stations while
   keeping validated joins and radius-ready rows at 0. The candidate
   public-feed source scan retrieves 10 public source URLs and screens all 7
   not-`isMonitor` candidate rows as public-feed nearby rows that are not
   join-ready, again keeping validated joins and radius-ready rows at 0. The
   one-signal review queue then combines 9 near-only official/OpenAQ rows, 22
   name-only-not-near rows, and 138 automatic or official-portal
   monitor-grade provenance-only rows into 169 review items across 149 unique
   official station keys and 8 economies, while keeping validated
   same-station joins, complete monitor-grade classifications, and
   station-radius-ready rows at 0. The
   monitor-grade evidence audit covers 239 official-source rows and finds 31
   source-specific method-standard signal rows in Bangladesh, 138 automatic or
   official-portal signal-only rows, 3 sensor-under-test rows, 2 plan-only
   rows, 65 rows with no public grade language, and 0 complete monitor-grade
   classification rows. The monitor-grade source-validation scan then
   retrieves 14 public source URLs across 7 non-Bangladesh economies, covers
   all 138 provenance-only queue rows, finds 7 source rows with method,
   equipment, standard, or method context, 6 official/automatic context-only
   source rows, 1 caution source row, and still 0 complete grade or
   station-radius-ready rows. The station-review queue then assigns those 138
   provenance-only station rows to row-level review lanes: 66 method-context
   rows needing station confirmation, 2 caution-blocked rows, 70
   official-context-only rows, and still 0 current-status confirmed,
   station-method classified, complete grade, or station-radius-ready rows.
   The station method-evidence audit then joins the 66 method-context rows to
   exact official extraction rows, finds 66 exact rows with PM2.5 signal and
   coordinates, separates 28 exact-row instrument hints from 38 exact PM2.5
   portal/API rows, flags 37 positive raw live PM2.5 values plus 29 negative,
   sentinel, or missing raw-value rows, and still keeps current-status
   confirmed, station-method classified, complete grade, and
   station-radius-ready rows at 0. The Uzbekistan station current/method scan
   then finds all 28 target instrument-hint station IDs in the public API with
   HORIBA markers, but only 5 reading dates within 30 days, 22 older than 365
   days, 13 negative or sentinel raw PM2.5 values, and still 0 explicit
   current-status confirmed, complete grade, or station-radius-ready rows. The
   Uzbekistan method-policy source scan retrieves 4 public source-policy rows
   with method/equipment and cadence/status context, but 0 sources name a target
   station ID from the 28-row queue. The Uzbekistan station-specific source
   evidence scan then retrieves the official Uzhydromet map, 14 official
   regional station-table pages, 28 station-detail pages, and one official
   gov.uz ecology note; parses 93 station rows; matches all 28 target rows to
   official regional table rows; finds 28 official station-detail URLs whose
   numeric path matches the internal target station ID, 26 detail measurements
   within 30 days, 22 Horiba table-context rows, 6 `Updating data` rows, 2
   official event-note station matches, and 1 negative sentinel detail PM2.5
   value. The Uzbekistan status/certification source scan then retrieves 7
   public source URLs, finds 6 source rows with method/equipment context, 7
   with operating or online context, 3 with source-level standards or
   reference-grade context, 1 with maintenance/training context, 2 additional
   exact station event mentions, 4 weaker context candidate rows, 2 stale
   station-detail follow-up rows, and 1 sentinel PM2.5 follow-up row; and still
   keeps current-status confirmation, station-method classification, complete
   monitor-grade classification, and station-radius readiness at 0. The
   Uzbekistan blocker-row follow-up then retrieves 2 official regional table
   pages and 3 exact official detail pages for station IDs 107, 728, and 737,
   finds 2 stale detail rows whose regional rows say `Updating data`, 1 recent
   `Sergili` detail row with PM2.5 equal to `-9999`, and 0 public
   blocker-resolution rows; current-status, station-method, complete-grade, and
   station-radius-ready counts remain 0. The Indonesia/Georgia row-method
   source scan then retrieves 29 of 29 seeded or expanded public source URLs
   for the 38 exact PM2.5 portal/API rows, finds 22 Indonesia BMKG same-page
   method-context candidates and 9 Georgia station-alias context candidates,
   and still keeps current-status confirmed, station-method classified,
   complete monitor-grade, and station-radius-ready rows at 0. The
   station-code status/method scan then covers 41 unresolved rows, improving
   Georgia to 16 exact `air.gov.ge` station-code API rows with PM2.5
   equipment/substance rows and 15 operating-description context rows, while
   keeping 1 Georgia test-mode row, 22 Indonesia BMKG payload rows, and 3
   Uzbekistan blockers visible; station method-table, calibration/status,
   current-status confirmed, complete-grade, and station-radius-ready counts
   remain 0. The station-grade decision ledger then joins all 66 exact
   method-context rows into row-level decision lanes, records 66 exact source
   trails, 50 method-context rows, and 16 raw-value or blocker caution rows,
   while keeping current-status, station-method, complete-grade, and
   station-radius-ready counts at 0. The station-method classification audit
   then retrieves 4 BMKG and air.gov.ge method/catalog sources, classifies 22
   Indonesia/BMKG rows as BAM, records 37 recent measurement-visibility rows,
   keeps Georgia at source-level catalog context with live-data verification
   caution and Uzbekistan at instrument-hint or blocker context, and keeps
   current-status, calibration/status, complete-grade, and station-radius-ready
   counts at 0. The BMKG operation/maintenance source scan then retrieves 4
   public BMKG context sources and 22 exact station-detail pages, records
   daily-inspection SOP, maintenance/check, calibration-procedure, BAM
   calibration service/tariff, and regional BAM-1020 model context for all 22
   BMKG rows, and still keeps station-specific inspection logs,
   station-specific calibration certificates, current-status confirmed,
   calibration-status, complete-grade, and station-radius-ready counts at 0.
   The Georgia report-verification source scan then retrieves the official May
   2026 `air.gov.ge` monthly report route, AQI method note, and monitoring
   network catalog, finds all 16 target station codes and PM2.5 report rows,
   records 16 not-verified report-label rows, and keeps verified-report
   closure, station-method classification, current-status confirmed,
   complete-grade, and station-radius-ready counts at 0. Next AI-doable loop is
   station-specific inspection/calibration/status and official grade-basis
   evidence for the 22 BMKG rows, a verified report export or exact
   method/status table for Georgia, plus exact station method/status/certification
   tables for Uzbekistan, before any station-radius or catchment claim.
2. **`remittance-resilience`** — L3 flow-weighting repair closed under Mode A
   in commit `225d4d2`. Repaired baseline top five are KGZ, WSM, TON, NPL,
   and VUT; the public KNOMAD flow-weighting L3 module keeps the same
   five-economy set but changes order to KGZ, NPL, VUT, WSM, TON.
   Human-final remains §18.5 owner-led.
3. **`access-services`** — 8-DMC climate-adjusted access pilot done;
   top-4 narrowing {BGD, KHM, LAO, PAK} stable. Travel-time isochrones
   are §18.5 owner-gated, so AI-doable depth is bounded — clean Mode A
   finish.
4. **`migration-displacement-signals`** — top-5 emigrant-stock cluster
   {IND, CHN, BGD, AFG, PHL} stable across alternative definitions;
   article exists at
   `articles/emigrant-stock-corridor-concentration.md`; same gap as
   remittance-resilience.
5. **`climate-health-workdays`** — top-3 set {AFG, IND, BGD} stable; PM
   2.5-cap sensitivity flagged top-5 → top-3 honest narrowing.
6. **`disaster-recovery-lag`** — metric-falsification deepening shows the
   original {CHN, IND} top-two is not robust: it holds for affected and
   damage, but changes under events/year, deaths, and events per million.
   It still lacks an actual recovery-lag metric.
7. **`grid-reliability-heat`** — top-5 single-fuel set {BTN, BRN, MNG,
   NPL, TJK} stable.
8. **`port-hinterland-friction`** — top-5 trade-volume cluster {CHN,
   IND, IDN, THA, VNM} stable.
9. **`social-protection-shock-coverage`** — top-5 {BGD, LAO, MMR, PAK,
   PHL} stable.
10. **`water-stress-crop-diversification`** — top-4 narrowing {AFG, AZE,
   PAK, TKM}; UZB perturbation-sensitive — narrower headline.
11. **`school-heat-disruption`** — honest narrowing to top-1 (KHM only);
    top-5 fails ±50% gate. Smallest-claim flagship candidate.
12. **`food-price-climate-transmission`** — sensitivity-gate failure on
    composite; index needs reformulation before ladder build.
13. **`flood-market-access`** — top-4 {AFG, CHN, IDN, IND} stable; GLOFAS
    modeled-extent is §18.5 owner-gated.
14. **`public-service-data-quality`** — PR ai-first package remains strong,
    but the next substantive upgrade is owner-only source-owner contact or
    human location validation for source-repair, same-facility,
    priority/lower-priority name-conflict, and facility-level zero-OSM rows.
15. **`invisible-urbanization`** — settlement growth vs admin urban
    boundaries; pipeline ready.
16. **`coastal-informal-risk`** — informal coastal settlements vs
    storm-surge exposure; pipeline ready.
17. **`digital-performance`** — broadband coverage vs official
    connectivity claims; folder mostly empty (Stage 1 framing needed).
18. **`mpi-nighttime-lights`** — Program 0, co-authored with Arturo; H
    stage; owner-led not AI-led (different review path).

Promotions and demotions are recorded in `research/wip-register.md`. The
queue position above is a planning order, not a maturity label.

## Stage labels

Generic across programs. Use these in chat updates and handoffs.

| Stage | Meaning | Output |
|---|---|---|
| 0. Idea queue | New possible topic, not yet judged | Short idea note |
| 1. Research framing | Question, contribution, audience, literature map | `literature.md`, problem statement |
| 2. Source discovery | Public datasets, licenses, API paths, coverage | source plan, cache plan |
| 3. Pipeline implementation | Fetch/process scripts and generated artifacts | `scripts/`, `.cache/`, `generated/` |
| 4. Results and sensitivity | Main result plus robustness checks | `results.md`, `sensitivity.md` |
| 5. Critique and limits | Red-team review, non-claims, failure modes | `limitations.md`, reviews |
| 6. Publication surface | Article, charts, home hooks, evidence page | `articles/`, `reporting-site/` |
| 7. Review loop and handoff | Review mode chosen + iterated to exit condition | `review-internal.md`, `review-external.md`, updated `{program}/STATUS.md` |
| 8. Blocked or owner-only | Needs owner account, reviewer, or non-AI attestation | explicit blocker in the per-program file |

## Where status, register, backlog, process live

| File | Role |
|---|---|
| `research/STATUS.md` (this file) | The board: active flagship + session protocol |
| `{program}/STATUS.md` | Per-program last-completed / next-work / blockers |
| `research/wip-register.md` | Maturity register (which program at which label) |
| `CONSTITUTION.md` §15 | Program register of record |
| `research/TODO-NEXT-SESSION.md` | Backlog of useful future work (cross-program) |
| `research/hook-bank.md` | Data-first shortlist for non-generic topic hooks |
| `research/factory.md` | Process manual: program loop, publication ladder, review loop |
| `CLAUDE.md` | Operating rules for AI assistants |

If these files disagree, fix the per-program file first for immediate
focus, then propagate to the register or this board only if the underlying
status truly changed.

## Session protocol

**Principle.** A session is a unit of accountable work, not a stream of
edits. It opens by stating what is being done, runs by doing it, and closes
by leaving the board in a state the next session can read.

**At session open:**
1. Read this file, the active flagship's `{program}/STATUS.md`, `CLAUDE.md`,
   and `research/factory.md`.
2. State the active flagship, current stage, and next output in plain language.
3. Continue the next focused work in the per-program board, unless the
   owner redirects.

**During session:**
1. Name the kind of work being done (framing, source, pipeline, results,
   critique, publication, review-loop, handoff).
2. Do not silently switch programs. If a switch is justified, record the
   reason in this file before making it.
3. Run end-of-task hygiene per `CLAUDE.md` after substantive changes
   (gates, build if site changed, browser-check if public surface changed,
   per-program STATUS update).

**At session close:**
1. Update the active flagship's `{program}/STATUS.md`: last completed, next
   focused work, blockers, verification actually run.
2. Update this file only if the active flagship, operating mode, or default
   review mode changed.
3. Update `research/wip-register.md` only if a maturity label changed.

## Current operational notes

- **2026-06-20 (food-price food-import source repair):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/food-price-coverage-trap` from a coverage-only audit into a
  raw-ag-import versus true food-import source wall. Added
  `food-price-climate-transmission/scripts/audit-food-import-source-readiness.py`,
  cache regeneration notes under
  `food-price-climate-transmission/.cache/README.md`, generated
  `food-price-coverage-food-import-audit.json`,
  `food-price-food-import-source-readiness.json`,
  `food-price-food-import-rerank.csv`, and
  `food-price-food-import-source-readiness-sources.csv`, and registered
  `food_price_food_import_source_readiness_public_metadata` in
  `versions.json`. The audit documents that the old import leg is WDI
  agricultural raw materials, not food imports; the true WDI food-import leg
  expands CPI x import eligibility from 34 to 36 roster rows under the same
  cached CPI leg, with Micronesia and Vanuatu entering eligibility; the old
  LAO+PAK common set across N becomes empty; and HDX exposes one WFP Global
  Food Prices CSV resource of 225.8 MB that is not joined. The analysis-ready
  food-price exposure wall remains false: no market-month price panel,
  commodity basket, local climate shock, exchange-rate/fuel decomposition, or
  household food-expenditure denominator is computed. Verification in this
  pass reran the food-price scripts, synced public artifacts, built the
  reporting site, ran the deterministic gates and showcase verifier, and
  browser-checked desktop plus 390px mobile with no page errors, failed
  requests, or page-level horizontal overflow.
- **2026-06-20 (climate-health labor denominator and heat-source wall):** In
  the owner-directed 20-report showcase loop, upgraded
  `/showcase/climate-health-measurement-repair` from a cap-saturation-only
  audit into a cap, observed-denominator, and heat-source readiness wall.
  Added
  `climate-health-workdays/scripts/audit-labor-heat-source-readiness.py`,
  cache regeneration notes under `climate-health-workdays/.cache/README.md`,
  generated `climate-health-workdays-denominator-source-audit.json`,
  `climate-health-labor-heat-source-readiness.json`, observed-denominator and
  source-readiness CSV companions, and registered
  `climate_health_labor_heat_source_readiness_public_metadata` in
  `versions.json`. The audit fetches public WDI employment-to-population 15+,
  total population, and ages 0-14 share, joins observed denominator fields for
  34/34 rankable DMCs, cuts India from 798.6M total-population outdoor
  exposure to 320.67M observed employed-15+ outdoor workers, cuts Afghanistan
  from 26.0M to 4.82M, and verifies 34/34 baseline plus 34/34 future CCKP
  national tasmax rows. It keeps `analysis_ready_heat_workday_loss: false`: no
  gridded heat or WBGT layer, worker-location surface, sectoral work-hours
  schedule, observed lost-workday outcome, or causal heat-health estimate is
  produced. Verification in this pass reran the climate-health scripts, synced
  public artifacts, built the reporting site, ran the deterministic gates and
  showcase verifier, and browser-checked desktop plus 390px mobile with no page
  errors, failed requests, or page-level horizontal overflow. Screenshots:
  `reporting-site/qa/showcase-climate-labor-source-desktop.png` and
  `reporting-site/qa/showcase-climate-labor-source-mobile.png`.
- **2026-06-20 (flood access source-readiness wall):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/flood-component-decomposition` from a rank-flip-only audit into a
  decomposition plus public access source-readiness wall. Added
  `flood-market-access/scripts/audit-access-source-readiness.py`, cache
  regeneration notes under `flood-market-access/.cache/README.md`, generated
  `flood-decomposition-access-source-audit.json`,
  `flood-access-source-readiness.json`, and source/link CSV companions, and
  registered `flood_access_source_readiness_public_metadata` in
  `versions.json`. The audit verifies 109 Geofabrik `.osm.pbf` links including
  65 latest extract links, one HDX/WFP food-prices CSV resource whose sampled
  header has no coordinate fields, 5,221 WorldPop dataset rows including 861
  panel rows across all 41 flood-panel economies, and public Global Flood
  Database / NASA flood-product metadata including 913 GFD Earth Engine events
  for 2000-2018. It keeps `analysis_ready_network_join: false`: no road
  extract is downloaded, no market points are geocoded, no population raster is
  downloaded, no observed flood footprint is exported, no road edges are cut,
  no travel time is routed, and no population-weighted access-loss estimate is
  produced. Verification in this pass reran the flood scripts, synced public
  artifacts, built the reporting site, ran the deterministic gates and
  showcase verifier, and browser-checked desktop plus 390px mobile with no page
  errors, failed requests, or page-level horizontal overflow. Screenshots:
  `reporting-site/qa/showcase-flood-access-source-desktop.png` and
  `reporting-site/qa/showcase-flood-access-source-mobile.png`.
- **2026-06-20 (coastal spatial source-readiness wall):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/coastal-population-denominator` from a no-population rank bridge
  into a denominator audit plus public spatial source-readiness wall. Added
  `coastal-informal-risk/scripts/audit-coastal-spatial-source-readiness.py`,
  cache regeneration notes under `coastal-informal-risk/.cache/README.md`,
  generated `coastal-denominator-spatial-source-audit.json`,
  `coastal-spatial-source-readiness.json`, and source/link CSV companions, and
  registered `coastal_spatial_source_readiness_public_metadata` in
  `versions.json`. The audit verifies 2 GHSL/JRC `GHS_BUILT_S` link
  candidates, NASADEM concept `C2763264762-LPCLOUD` with 9 sample HTTPS data
  links in CMR metadata, and 820 WRI Aqueduct coastal-hazard links including
  410 GeoTIFF links. It keeps `analysis_ready_overlay: false`: no rasters are
  downloaded, no return period is selected, no low-elevation band is derived,
  no settlement/elevation/surge overlay is computed, and no exposed-population
  estimate is produced. Verification in this pass reran the coastal scripts,
  synced public artifacts, built the reporting site, ran the deterministic
  gates and showcase verifier, and browser-checked desktop plus 390px mobile
  with no page errors, failed requests, or page-level horizontal overflow.
  Screenshots:
  `reporting-site/qa/showcase-coastal-spatial-source-desktop.png` and
  `reporting-site/qa/showcase-coastal-spatial-source-mobile.png`.
- **2026-06-20 (grid reliability proxy source-wall audit):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/grid-generation-mismatch` from a capacity-versus-generation
  bridge into a generation-concentration plus public reliability-proxy
  source-readiness report. Added
  `grid-reliability-heat/scripts/audit-public-reliability-proxies.py`, cache
  regeneration notes under `grid-reliability-heat/.cache/README.md`, generated
  `grid-generation-reliability-source-audit.json`,
  `grid-public-reliability-proxy-readiness.json`, and country/indicator CSV
  companions, and registered `world_bank_wdi_grid_reliability_proxies` in
  `versions.json`. The audit queries 15 World Bank firm-outage, Enterprise
  Survey legacy, Doing Business, and B-READY utility-service indicators. It
  finds 38 DMCs with at least one public reliability proxy, 22 DMCs with both
  generation concentration and a proxy, and 8 high-generation-concentration
  rows with a proxy; proxy vintages span 2009-2025, and 3 queried
  outage-count or outage-duration endpoints have zero usable ADB-DMC rows in
  this pull. This is a source-readiness wall, not outage-event,
  reserve-margin, dispatch, or heat-stress evidence. Verification in this
  pass reran the grid scripts, synced public artifacts, built the reporting
  site, and browser-checked desktop plus 375px mobile with zero console
  errors, zero network errors, and zero page-level horizontal overflow.
  Screenshots:
  `reporting-site/qa/showcase-grid-reliability-proxy-desktop.png`,
  `reporting-site/qa/showcase-grid-reliability-proxy-desktop-visual.png`,
  `reporting-site/qa/showcase-grid-reliability-proxy-mobile.png`, and
  `reporting-site/qa/showcase-grid-reliability-proxy-mobile-visual.png`.
- **2026-06-20 (migration corridor-type forced-displacement audit):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/migration-denominator-switch` from a denominator-switch rank
  bridge into a UN DESA/WDI migration-stock report with a public UNHCR
  forced-displacement corridor-type falsifier. Added
  `migration-displacement-signals/scripts/audit-corridor-type-forced-displacement.py`,
  cache regeneration notes under
  `migration-displacement-signals/.cache/README.md`, generated
  `migration-denominator-corridor-type-audit.json`,
  `migration-corridor-type-forced-displacement.json`, and country/corridor CSV
  companions, and registered `unhcr_refugee_data_finder_population_api` in
  `versions.json`. The audit queries 44 UN DESA/WDI panel origins against the
  UNHCR Refugee Data Finder population API for 2024 origin-asylum rows, finds
  41 origins with at least one forced-displacement-abroad row, 7 origins with a
  substantial forced-displacement component, and 1 forced-displacement-majority
  origin. Afghanistan is the exception: UNHCR forced-displacement-abroad stock
  is 6,151,318 people, or 81.7% of its UN DESA emigrant stock; the share top
  five has 0/5 forced-displacement-majority rows. This is a corridor-type
  falsifier and source-readiness layer, not a labor, family, student,
  temporary-work, welfare, or fragility classification. Verification in this
  pass reran the migration scripts, synced public artifacts, built the
  reporting site, and browser-checked desktop plus 375px mobile with zero
  console errors, zero network errors, and zero page-level horizontal
  overflow. Screenshots:
  `reporting-site/qa/showcase-migration-corridor-type-desktop.png`,
  `reporting-site/qa/showcase-migration-corridor-type-desktop-visual.png`,
  `reporting-site/qa/showcase-migration-corridor-type-mobile.png`, and
  `reporting-site/qa/showcase-migration-corridor-type-mobile-visual.png`.
- **2026-06-20 (MPI/nighttime-lights source-readiness wall):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/mpi-nightlight-blindspot` from an MPI-only blindness
  decomposition into a public CMR source-readiness wall for the owner-gated
  NTL side. Added
  `mpi-nighttime-lights/scripts/audit-ntl-source-readiness.py`, cache
  regeneration notes under `mpi-nighttime-lights/.cache/README.md`, generated
  `mpi-nightlight-blindspot-source-audit.json`,
  `mpi-nightlight-source-readiness.json`, and collection/granule-link CSV
  companions, and registered `nasa_black_marble_mpi_ntl_cmr` in
  `versions.json`. The audit queries NASA CMR for VNP46A3 and VNP46A4,
  finds 4 collection rows, 2 current v2 collection candidates
  (`C3860061042-LAADS` monthly and `C3860065683-LAADS` yearly), CMR current
  collection coverage starting on 2012-01-01, 2 sample granules checked, and
  2/2 sample granules with HTTPS data links. It explicitly keeps
  `analysis_ready_raster_join` false: no radiance raster was downloaded, no
  Earthdata or Earth Engine authentication was attempted, no population-
  weighted zonal statistic or subnational MPI crosswalk was computed, no gas-
  flare mask was applied, and no NTL x MPI model was estimated. Verification
  in this pass reran the MPI decomposition and CMR source-readiness scripts,
  synced public artifacts, built the reporting site, and browser-checked
  desktop plus 375px mobile with zero console errors, zero network errors, and
  zero page-level horizontal overflow. Screenshots:
  `reporting-site/qa/showcase-mpi-ntl-source-desktop.png`,
  `reporting-site/qa/showcase-mpi-ntl-source-desktop-visual.png`,
  `reporting-site/qa/showcase-mpi-ntl-source-mobile.png`, and
  `reporting-site/qa/showcase-mpi-ntl-source-mobile-visual.png`.
- **2026-06-20 (disaster metric-falsification source-readiness audit):** In
  the owner-directed 20-report showcase loop, upgraded
  `/showcase/disaster-metric-falsification` from a metric-switch route into a
  metric-falsification plus recovery-source-readiness report. Added
  `disaster-recovery-lag/scripts/audit-recovery-source-readiness.py`, cache
  regeneration notes under `disaster-recovery-lag/.cache/README.md`, generated
  `disaster-recovery-lag-recovery-source-readiness.{json,csv}` and the event
  queue CSV, registered `gdis_geocoded_disasters_1960_2018` and
  `nasa_black_marble_vnp46a3_cmr` in `versions.json`, and surfaced the source
  bridge in `deepened-results.md`, the showcase registry, downloads, and a new
  recovery-readiness visual wall. The audit confirms the current EM-DAT
  country-profiles cache has 1,767 ADB-DMC rows in the 2000-2025 filter but
  lacks disaster identifier, month/day, latitude, longitude, and location
  fields, so it supports burden screens but not recovery curves. GDIS supplies
  39,953 location rows, 9,924 GDIS ids, and 9,018 `disasterno` values for
  1960-2018; NASA CMR identifies Black Marble VNP46A3 version 2 with coverage
  starting 2012-01-01. The resulting ADB-DMC 2012-2018 overlap has 2,881
  location rows, 609 unique GDIS ids, 565 unique `disasterno` values, and 27
  economies with overlap; top `disasterno` counts are CHN 214, IND 113, PHL
  51, AFG 39, PAK 38, and IDN 33. This is a public event-geography queue and a
  source-readiness object, not a recovery-lag estimate. Verification in this
  pass: `process-disaster.py`, `deepen-metric-falsification.py`, the new audit
  script, public evidence/reference/doc sync, production `npm run build`, and
  Chrome CDP desktop/mobile screenshot QA all passed; final deterministic
  gates are run in the same handoff pass. Active flagship remains unchanged
  because this is an owner-directed showcase-loop override, not a silent
  flagship rotation.
- **2026-06-20 (access map-completeness Cambodia source audit):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/access-map-completeness` from a no-registry Cambodia warning to a
  testable public-source row. Added
  `access-services/scripts/audit-cambodia-health-facility-source.py`, cache
  regeneration notes under `access-services/.cache/README.md`, generated
  `access-cambodia-health-facility-source-audit.{json,csv}` plus the raw-name
  summary CSV, registered `hdx_cambodia_health_facility_2010` in
  `versions.json`, and surfaced the evidence in the access deepening note,
  showcase registry, downloads, correction-wall visual, and a new Cambodia
  source ledger. The script retrieves the public HDX Cambodia Health
  Facilities package API and `health_facility.zip`, records ZIP SHA-256
  `f4e97c595ba7a20698cf8cefb4b71a76a5eb38d45badf9dcfdf48cde12dd3506`,
  counts only 2010 government health centers, health posts, and referral
  hospitals, and keeps operational-district points as context only. Current
  results: 24/25 Cambodia ADM1 access rows join to the 2010 source; 1,121
  public-source facilities are counted; 21/24 joined rows re-rank; Oddar
  Meanchey changes from 4 OSM health points and 319,413 people per point to
  17 public-source facilities and 75,156 people per facility (4.25x load
  difference); Phnom Penh remains a scope/vintage warning because OSM has 227
  health points versus 22 facilities in the 2010 public inventory. This is a
  partial source-scope audit, not a complete current all-provider registry,
  service-capacity measure, travel-time result, maturity promotion, or
  human-final upgrade. Remaining access blockers: Pakistan and Lao still need
  comparable registry/source joins; Cambodia still needs boundary-year,
  national-hospital, current-provider, and catchment/friction checks before it
  can support an access claim. Verification: `py_compile`, the Cambodia audit
  script, and `deepen-osm-completeness.py` reran; `npm run build` passed with
  the existing chunk-size warning; repository gates
  `check-banned-words`, `check-dmc-framing`, `check-citations`,
  `check-composite-headline`, `check-wip`, `verify-showcase-bench`, and
  `check-versions` passed; Chrome CDP QA passed at 1365x900 and 375x820 with
  no page-level overflow, no blocking console errors, no network failures,
  three hero stats, four Cambodia source cards, and the `KHM 75,156 HDX
  partial` correction-wall label. QA record:
  `reporting-site/qa/showcase-access-cambodia-browser-check.json`;
  screenshots: `showcase-access-cambodia-desktop.png`,
  `showcase-access-cambodia-source-desktop.png`,
  `showcase-access-cambodia-cluster-desktop.png`,
  `showcase-access-cambodia-mobile.png`,
  `showcase-access-cambodia-source-mobile.png`, and
  `showcase-access-cambodia-cluster-mobile.png`.
- **2026-06-20 (remittance flow-weighting confidence ledger):** In the
  owner-directed 20-report showcase loop, upgraded
  `/showcase/remittance-flow-weighting` with a generated evidence-confidence
  ledger rather than a prose-only caveat. The L3 module now emits row-level
  confidence classes, a top-five confidence rail, coverage-absence rows, and
  source-vintage counts from
  `remittance-resilience/scripts/sprint-flow-weighted-cost.py`. Current
  generated counts: 21 rankable economies, 5/5 repaired baseline top-five
  economies still in the flow-weighted top five, 1 flow-weighted top-five row
  below 25% matched-flow coverage, 2 flow-weighted top-five rows with one
  matched RPW corridor, and 15 DMCs with KNOMAD inbound flow but no
  latest-period RPW quote coverage. This is a reader-facing evidence and UI
  repair only, not a maturity promotion. Verification: remittance script rerun,
  `npm run build` passed with the existing chunk-size warning, Chrome CDP QA
  passed at 1365x900 and 375x820 with no page-level horizontal overflow, no
  console errors, no network failures, 5 confidence cards, 14 ledger rows, 6
  absence rows, and hero values `140/142`, `5/5`, `1`. QA record:
  `reporting-site/qa/showcase-remittance-confidence-browser-check.json`;
  screenshots:
  `reporting-site/qa/showcase-remittance-confidence-desktop.png`,
  `reporting-site/qa/showcase-remittance-confidence-ledger-desktop.png`,
  `reporting-site/qa/showcase-remittance-confidence-mobile.png`, and
  `reporting-site/qa/showcase-remittance-confidence-ledger-mobile.png`.
- **2026-06-19 (home report-bench readiness map):** Added a compact
  20-slot readiness map to the first viewport of `/`, using the shared
  showcase registry and explicit stage colors for L2 prototype, L3 candidate,
  evidence audit, and owner-gated reports. This keeps the front page from
  reading like a generic topic gallery and makes the portfolio shape visible
  before the report cards. This is a UI/UX and navigation repair only, not a
  maturity promotion. Browser QA checked desktop and mobile home viewports:
  2/2 passes, 20 map tiles, 4 legend entries, 20 report cards, 4 distinct
  stage colors, no horizontal overflow, and no console/network/runtime errors.
  QA record: `reporting-site/qa/home-showcase-report-map-browser-check.json`;
  screenshots: `reporting-site/qa/home-showcase-report-map-desktop.png` and
  `reporting-site/qa/home-showcase-report-map-mobile.png`.
- **2026-06-19 (shared evidence-audit showcase route refactor):**
  Refactored the shared `/showcase/:reportSlug` route used by reports 9-20
  so each artifact-driven report now renders a four-part evidence spine
  (decision problem, measurement doubt, test added, publication gate) and a
  four-part claim ladder (allowed finding, non-claim, falsifier, next
  upgrade). This is a reader-facing UI/UX repair only, not a maturity
  promotion. Browser QA checked all 12 shared audit routes across desktop and
  mobile viewports, with 24/24 passes, no horizontal overflow, no console
  errors, no network failures, and no missing source/caveat sections. QA
  record:
  `reporting-site/qa/showcase-evidence-audit-shared-route-browser-check.json`;
  screenshots:
  `reporting-site/qa/showcase-evidence-audit-migration-desktop-spine.png`,
  `reporting-site/qa/showcase-evidence-audit-migration-mobile-spine.png`,
  `reporting-site/qa/showcase-evidence-audit-food-desktop-visual.png`,
  `reporting-site/qa/showcase-evidence-audit-food-mobile-visual.png`,
  `reporting-site/qa/showcase-evidence-audit-water-desktop-claim.png`, and
  `reporting-site/qa/showcase-evidence-audit-school-mobile-claim.png`.
- **2026-06-19 (air-monitoring monitor-grade station method-evidence audit):**
  Added
  `air-monitoring/scripts/audit-monitor-grade-station-method-evidence.py`,
  generated
  `air-monitoring/generated/air-monitoring-monitor-grade-station-method-evidence.csv`
  and
  `air-monitoring/generated/air-monitoring-monitor-grade-station-method-evidence-summary.json`,
  and wrote `air-monitoring/monitor-grade-station-method-evidence.md`. The
  no-network audit reads the station-review queue plus the official
  station-source extraction, reviews the 66 method-context station rows, finds
  66 exact official station rows with PM2.5 signal and coordinates, separates
  28 exact-row instrument hints from 38 exact PM2.5 portal/API rows, flags 37
  positive raw live PM2.5 values plus 12 negative raw values, 1 sentinel, and
  16 missing raw values, and keeps current-status confirmed rows,
  station-method classified rows, complete monitor-grade classifications, and
  station-radius grade-assumption-ready rows at 0. The public route now renders
  a monitor-grade station method-evidence wall. Chrome CDP QA passed at
  1440x1100 and 390x1000 with 6 stat cards, 3 lane cards, 3 country cards, 3
  source-group cards, 12 sample station row cards, 8 evidence gates, 3 download
  links, no page or section horizontal
  overflow, no text overflow, and no page errors beyond existing React Router
  future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-grade-method-desktop.png`,
  `reporting-site/qa/showcase-air-grade-method-mobile.png`, and
  `reporting-site/qa/showcase-air-grade-method-mobile-rows.png`.
- **2026-06-19 (air-monitoring Uzbekistan station current/method scan):**
  Added
  `air-monitoring/scripts/scan-uzbekistan-station-current-method-evidence.py`,
  generated
  `air-monitoring/generated/air-monitoring-uzbekistan-station-current-method-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-uzbekistan-station-current-method-scan-summary.json`,
  and wrote `air-monitoring/uzbekistan-station-current-method-scan.md`. The
  networked scan fetches the public Uzhydromet maps API and joins the 28
  Uzbekistan exact-row instrument-hint rows by station ID. It finds all 28
  target station IDs in the API and all 28 with station-level HORIBA markers,
  but only 5 API reading dates within 30 days, 1 between 31 and 90 days, and 22
  older than 365 days. It also records 15 positive raw PM2.5 values, 12
  negative raw values, 1 sentinel value, and still 0 explicit current-status
  confirmed rows, complete monitor-grade rows, or station-radius-ready rows. The
  public route now renders a Uzbekistan current/method panel. Chrome headless
  QA at 1440x1100 and 390x1000 confirmed 6 stat cards, 3 age cards, 12 sample
  station row cards, 9 evidence gates, 3 download links, the 22 stale-date and
  5 within-30-day counts, no page or section horizontal overflow, no text
  overflow, and no page errors beyond existing React Router future-flag
  warnings. Screenshots:
  `reporting-site/qa/showcase-air-uzb-current-desktop.png`,
  `reporting-site/qa/showcase-air-uzb-current-mobile.png`, and
  `reporting-site/qa/showcase-air-uzb-current-mobile-rows.png`. Next work is
  station-owner/regulator documentation for Uzbekistan reading-date policy, station status,
  calibration/certification, and method applicability, then the 38 Indonesia and
  Georgia portal/API rows.
- **2026-06-19 (air-monitoring Uzbekistan method-policy source scan):** Added
  `air-monitoring/source-inputs/uzbekistan-method-policy-source-seed.csv`,
  `air-monitoring/scripts/scan-uzbekistan-method-policy-sources.py`, generated
  `air-monitoring/generated/air-monitoring-uzbekistan-method-policy-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-uzbekistan-method-policy-source-scan-summary.json`,
  and wrote `air-monitoring/uzbekistan-method-policy-source-scan.md`. The scan
  checks 5 public official or technical sources and retrieves 4. It finds 4
  source rows with method/equipment context and 4 with reading-cadence or status
  context, but 0 source rows naming a target station ID from the 28-row queue.
  It keeps current-status confirmed rows, complete monitor-grade rows, and
  station-radius-ready rows at 0. Next work is a stricter station-ID or
  station-specific equipment/status source search for Uzbekistan before any
  grade or catchment promotion. Chrome/Playwright QA at 1440x1100 and 390x1000
  confirmed the home report card, evidence note, and data-tab CSV/JSON are
  visible, with no console errors and no horizontal overflow beyond existing
  React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-method-policy-home-desktop.png`,
  `reporting-site/qa/showcase-method-policy-home-mobile.png`,
  `reporting-site/qa/showcase-air-method-policy-evidence-desktop.png`,
  `reporting-site/qa/showcase-air-method-policy-evidence-mobile.png`,
  `reporting-site/qa/showcase-air-method-policy-data-desktop.png`, and
  `reporting-site/qa/showcase-air-method-policy-data-mobile.png`.
- **2026-06-19 (air-monitoring Uzbekistan station-specific source evidence):**
  Added
  `air-monitoring/source-inputs/uzbekistan-station-specific-source-seed.csv`,
  `air-monitoring/scripts/scan-uzbekistan-station-specific-source-evidence.py`,
  generated
  `air-monitoring/generated/air-monitoring-uzbekistan-station-specific-source-evidence.csv`
  and
  `air-monitoring/generated/air-monitoring-uzbekistan-station-specific-source-evidence-summary.json`,
  and wrote `air-monitoring/uzbekistan-station-specific-source-evidence.md`.
  The scan retrieves the official Uzhydromet map, 14 official regional
  station-table pages, 28 station-detail pages, and one official gov.uz ecology
  note; parses 93 station rows; matches all 28 target Uzbekistan rows to
  official regional table rows; finds 28 station-detail URLs whose numeric path
  matches the internal target station ID, 26 detail measurements within 30 days,
  22 Horiba table-context rows, 6 `Updating data` rows, 2 official event-note
  station matches, and 1 negative sentinel detail PM2.5 value. It keeps
  current-status confirmed rows, complete monitor-grade classification rows,
  and station-radius-ready rows at 0. Chrome CDP QA at 1440x1100 and 390x1000
  confirmed the home report card, evidence-tab note link, and data-tab CSV/JSON
  links are visible, with no page-level horizontal overflow and no
  console/runtime errors. Screenshots:
  `reporting-site/qa/showcase-station-specific-home-desktop.png`,
  `reporting-site/qa/showcase-station-specific-home-mobile.png`,
  `reporting-site/qa/showcase-air-station-specific-evidence-desktop.png`,
  `reporting-site/qa/showcase-air-station-specific-evidence-mobile.png`,
  `reporting-site/qa/showcase-air-station-specific-data-desktop.png`, and
  `reporting-site/qa/showcase-air-station-specific-data-mobile.png`.
- **2026-06-19 (air-monitoring Uzbekistan status/certification source scan):**
  Added
  `air-monitoring/source-inputs/uzbekistan-status-certification-source-seed.csv`,
  `air-monitoring/scripts/scan-uzbekistan-status-certification-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-uzbekistan-status-certification-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-uzbekistan-status-certification-source-scan-summary.json`,
  and wrote
  `air-monitoring/uzbekistan-status-certification-source-scan.md`. The scan
  retrieves 7 public source URLs after the Uzbekistan station-ID gate and finds
  6 source rows with method/equipment context, 7 with operating or online
  context, 3 with source-level standards or reference-grade context, 1 with
  maintenance/training context, 2 additional exact station event mentions, 2
  Tashkent Uzhydromet reference-grade context candidate rows, 1 Almazar
  district commissioning context candidate, 1 Karakalpakstan/Aral Sea regional
  24/7 network context candidate, 2 stale station-detail follow-up rows, and 1
  sentinel PM2.5 follow-up row. It still records 0 current-status confirmed
  rows, 0 station-method classified rows, 0 complete monitor-grade rows, and 0
  station-radius-ready rows. Public surface QA now checks the home card, the
  topic Evidence/Data tabs, and the `/showcase/air-monitoring-observability`
  wall with Chrome CDP at desktop and mobile widths, writing
  `reporting-site/qa/showcase-air-status-certification-desktop.png` and
  `reporting-site/qa/showcase-air-status-certification-mobile.png`; no
  horizontal overflow or route-level browser errors were observed beyond
  dev-server notices.
- **2026-06-19 (air-monitoring Uzbekistan blocker-row follow-up):** Added
  `air-monitoring/source-inputs/uzbekistan-blocker-row-followup-targets.csv`,
  `air-monitoring/scripts/scan-uzbekistan-blocker-row-followup.py`, generated
  `air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup.csv`
  and
  `air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json`,
  and wrote `air-monitoring/uzbekistan-blocker-row-followup.md`. The follow-up
  retrieves 2 official regional table pages and 3 exact official station-detail
  pages for station IDs 107, 728, and 737, finds all 3 matching region rows, 2
  stale detail rows with regional `Updating data`, 1 recent `Sergili` row whose
  PM2.5 value remains `-9999`, and 0 public blocker-resolution rows. It keeps
  current-status confirmed, station-method classified, complete monitor-grade,
  and station-radius-ready rows at 0 and adds a public 3-row blocker wall.
  Chrome CDP QA confirms the home card, topic Evidence/Data tabs, and
  desktop/mobile route panel, writing
  `reporting-site/qa/showcase-air-blocker-followup-desktop.png` and
  `reporting-site/qa/showcase-air-blocker-followup-mobile.png`.
- **2026-06-19 (air-monitoring Indonesia/Georgia row-method source scan):**
  Added
  `air-monitoring/source-inputs/indonesia-georgia-row-method-source-seed.csv`,
  `air-monitoring/scripts/scan-indonesia-georgia-row-method-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan-summary.json`,
  and wrote `air-monitoring/indonesia-georgia-row-method-source-scan.md`. The
  scan covers the 38 exact PM2.5 portal/API rows left by the station
  method-evidence audit, retrieves 29 of 29 seeded or expanded public source
  URLs, finds 22 Indonesia BMKG same-page method-context candidates and 9
  Georgia station-alias context candidates, but still records 0 current-status
  confirmed rows, 0 station-method classified rows, 0 complete monitor-grade
  rows, and 0 station-radius-ready rows. The public route now renders an
  Indonesia/Georgia method-context wall.
- **2026-06-19 (air-monitoring station-code status/method source scan):**
  Added
  `air-monitoring/source-inputs/station-code-status-method-source-seed.csv`,
  `air-monitoring/scripts/scan-station-code-status-method-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-station-code-status-method-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-station-code-status-method-source-scan-summary.json`,
  and wrote `air-monitoring/station-code-status-method-source-scan.md`. The
  scan covers 41 unresolved exact station-code or station-ID rows: 16 Georgia
  `air.gov.ge` station-code API rows, 22 Indonesia BMKG PM2.5 portal payload
  rows, and 3 Uzbekistan blocker rows carried forward from the exact blocker
  follow-up. It finds 41 exact station code or ID rows, 16 Georgia PM2.5
  equipment rows, 15 Georgia operating-description context rows, 1 Georgia
  test-mode row, 22 Indonesia BMKG station-code payload rows, and 3 unresolved
  Uzbekistan blockers, while keeping station method-table, calibration/status,
  current-status confirmed, station-method classified, complete monitor-grade,
  and station-radius-ready rows at 0. The public route now renders a
  station-code status/method wall.
- **2026-06-19 (air-monitoring station-grade decision ledger):** Added
  `air-monitoring/scripts/build-station-grade-decision-ledger.py`, generated
  `air-monitoring/generated/air-monitoring-station-grade-decision-ledger.csv`
  and
  `air-monitoring/generated/air-monitoring-station-grade-decision-ledger-summary.json`,
  and wrote `air-monitoring/station-grade-decision-ledger.md`. The no-network
  ledger joins the 66 exact station method-evidence rows to the committed
  Uzbekistan, Indonesia/Georgia, and station-code follow-up scans, records 66
  exact official row/source-trail rows, 66 PM2.5 row/equipment rows, 50
  method-context rows, 66 operating/current-context rows, 16 raw-value or
  blocker caution rows, and keeps station method-table rows,
  calibration/status rows, current-status confirmed rows, station-method
  classified rows, complete monitor-grade rows, and station-radius-ready rows
  at 0. The public route now renders a station-grade decision ledger panel.
- **2026-06-19 (air-monitoring station-method classification audit):** Added
  `air-monitoring/scripts/build-station-method-classification-audit.py`,
  generated
  `air-monitoring/generated/air-monitoring-station-method-classification-audit.csv`
  and
  `air-monitoring/generated/air-monitoring-station-method-classification-audit-summary.json`,
  and wrote `air-monitoring/station-method-classification-audit.md`. The
  networked audit reads the station-grade decision ledger plus the
  Indonesia/Georgia and station-code scans, retrieves 4 BMKG and air.gov.ge
  method/catalog sources, classifies 22 Indonesia/BMKG rows as
  `Beta Attenuation Monitoring (BAM)`, records 37 rows with recent PM2.5
  measurement visibility, keeps 16 Georgia rows at source-level catalog
  context with live-data verification caution, keeps 28 Uzbekistan rows as
  instrument-hint or blocker context, records 16 raw-value or blocker caution
  rows, and keeps current-status confirmed rows, row-level calibration/status
  rows, complete monitor-grade rows, and station-radius-ready rows at 0. The
  public route now renders a station-method classification panel.
  Agent-browser QA passed at 1440x1100 and 390x1000 with 6 stat cards, 3
  decision lanes, 3 country cards, 16 sample row cards, 9 gate cards, 3
  download links, no page or section horizontal overflow, no overflowing mobile
  children, no console output, and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-method-classification-desktop.png` and
  `reporting-site/qa/showcase-air-method-classification-mobile.png`.
- **2026-06-19 (air-monitoring BMKG operation/maintenance source scan):**
  Added `air-monitoring/scripts/scan-bmkg-operation-maintenance-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-bmkg-operation-maintenance-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-bmkg-operation-maintenance-source-scan-summary.json`,
  and wrote `air-monitoring/bmkg-operation-maintenance-source-scan.md`. The
  networked scan reads the 22 Indonesia/BMKG rows already method-classified as
  BAM, retrieves 4 public BMKG context sources and 22 exact station-detail
  pages, records 22 recent exact station-detail pages, 22 daily-inspection SOP
  context rows, 22 maintenance/check context rows, 22 calibration-procedure
  context rows, 22 BAM calibration service/tariff context rows, and 22 regional
  BAM-1020 model-context rows, while keeping station-specific inspection logs,
  station-specific calibration certificates, current-status confirmed,
  calibration-status, complete monitor-grade, and station-radius-ready rows at
  0. The public route now renders a BMKG operation/maintenance panel.
  Agent-browser QA passed at 1440x1100 and 390x1000 with 6 stat cards, 1
  decision lane, 12 sample row cards, 9 gate cards, 3 download links, no page
  or section horizontal overflow, no overflowing mobile children, no console
  output, and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-bmkg-operation-desktop.png` and
  `reporting-site/qa/showcase-air-bmkg-operation-mobile.png`.
- **2026-06-19 (air-monitoring Georgia report-verification source scan):**
  Added `air-monitoring/scripts/scan-georgia-report-verification-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-georgia-report-verification-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-georgia-report-verification-source-scan-summary.json`,
  and wrote `air-monitoring/georgia-report-verification-source-scan.md`. The
  networked scan reads the 16 Georgia rows from the station-method
  classification audit, retrieves the official May 2026 `air.gov.ge` monthly
  report route for all 16 target station codes plus the AQI method note and
  monitoring-network catalog, finds 16 station-code rows, 16 PM2.5 report rows,
  16 report-page `Not Verified Data` caution rows, 16 AQI-note live-data
  verification caution rows, and 16 source-level network-instrument context
  rows, while keeping verified-report closure, station-method classification,
  current-status confirmed, complete monitor-grade, and station-radius-ready
  rows at 0. The public route now renders a Georgia report-verification panel.
  Agent-browser QA passed at 1440x1100 and 390x1000 with 6 stat cards, 1
  decision lane, 16 sample row cards, 9 gate cards, 3 download links, no page
  or section horizontal overflow, no overflowing mobile children, no console
  output, and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-georgia-report-desktop.png` and
  `reporting-site/qa/showcase-air-georgia-report-mobile.png`.
- **2026-06-19 (air-monitoring monitor-grade station-review queue):** Added
  `air-monitoring/scripts/build-monitor-grade-station-review-queue.py`,
  generated
  `air-monitoring/generated/air-monitoring-monitor-grade-station-review-queue.csv`
  and
  `air-monitoring/generated/air-monitoring-monitor-grade-station-review-queue-summary.json`,
  and wrote `air-monitoring/monitor-grade-station-review-queue.md`. The
  no-network queue reads the one-signal queue plus the monitor-grade
  source-validation scan, then assigns all 138 provenance-only station rows to
  row-level review lanes: 66 method-context rows needing station confirmation,
  2 caution-blocked rows, and 70 official-context-only rows. It keeps
  current-status confirmed rows, station-method classified rows, complete
  monitor-grade classifications, and station-radius grade-assumption-ready rows
  at 0. The public route now renders a monitor-grade station-review wall.
  Chrome CDP QA passed at 1440x1100 and 390x1000 with 5 stat cards, 3 lane
  cards, 7 country cards, 7 source-group cards, 12 sample station row cards, 5
  evidence gates, 3 download links, no page or section horizontal overflow, no
  text overflow, and no page errors beyond existing React Router future-flag
  warnings. Screenshots:
  `reporting-site/qa/showcase-air-grade-station-desktop.png`,
  `reporting-site/qa/showcase-air-grade-station-mobile.png`, and
  `reporting-site/qa/showcase-air-grade-station-mobile-rows.png`. Next work is
  station-level method/current-status evidence for the 66 method-context rows.
- **2026-06-19 (air-monitoring monitor-grade source-validation scan):** Added
  `air-monitoring/source-inputs/monitor-grade-source-validation-seed.csv`,
  `air-monitoring/scripts/scan-monitor-grade-source-validation.py`, generated
  `air-monitoring/generated/air-monitoring-monitor-grade-source-validation-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-monitor-grade-source-validation-scan-summary.json`,
  and wrote `air-monitoring/monitor-grade-source-validation-scan.md`. The scan
  retrieves all 14 seeded public URLs across 7 economies and covers all 138
  monitor-grade provenance-only rows from the one-signal review queue. It finds
  2 method/equipment context source rows, 5 standard/method context source
  rows, 6 official/automatic context-only source rows, 1 caution source row, 0
  complete monitor-grade classification rows, and 0 station-radius
  grade-assumption-ready rows. The public route now renders a monitor-grade
  source-validation wall. Chrome CDP QA passed at 1440x1100 and 390x1000 with
  5 stat cards, 7 country cards, 14 source cards, 5 evidence gates, 3 download
  links, no page or section horizontal overflow, no text overflow, and no page
  errors beyond existing React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-air-grade-source-desktop.png`,
  `reporting-site/qa/showcase-air-grade-source-mobile.png`, and
  `reporting-site/qa/showcase-air-grade-source-mobile-sources.png`. Next work
  is station-level current-status/method review for the rows with public
  method context, not station-radius coverage.
- **2026-06-19 (air-monitoring one-signal review queue):** Added
  `air-monitoring/scripts/build-one-signal-review-queue.py`, generated
  `air-monitoring/generated/air-monitoring-one-signal-review-queue.csv` and
  `air-monitoring/generated/air-monitoring-one-signal-review-queue-summary.json`,
  and wrote `air-monitoring/one-signal-review-queue.md`. The queue excludes
  the 13 near-plus-name candidates already source-screened, then combines 9
  near-only official/OpenAQ rows, 22 name-only-not-near rows, and 138
  automatic or official-portal monitor-grade provenance-only rows. It records
  169 review items across 149 unique official station keys and 8 economies,
  with 0 validated same-station joins, 0 complete monitor-grade
  classifications, and 0 station-radius-ready rows. The public route now
  renders the one-signal review wall. Chrome CDP QA passed at 1440x1100 and
  390x1000 with 5 stat cards, 3 lane cards, 8 country cards, 15 row cards, 8
  source cards, 5 evidence gates, 3 download links, no page or section
  horizontal overflow, no text overflow, and no page errors. Screenshots:
  `reporting-site/qa/showcase-air-one-signal-desktop.png`,
  `reporting-site/qa/showcase-air-one-signal-mobile.png`, and
  `reporting-site/qa/showcase-air-one-signal-mobile-rows.png`. Next work is
  source-owner crosswalk, current-status, documented co-location, or
  station-owner/regulator method documentation for this queue.
- **2026-06-19 (air-monitoring candidate public-feed source scan):** Added
  `air-monitoring/source-inputs/candidate-public-feed-source-seed.csv`,
  `air-monitoring/scripts/scan-official-openaq-candidate-public-feed-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json`,
  and wrote
  `air-monitoring/official-openaq-candidate-public-feed-source-scan.md`. The
  scan targets the 7 candidate rows not marked `isMonitor` in OpenAQ, retrieves
  all 10 seeded public source URLs, records 7 official-coordinate rows, 7
  OpenAQ-coordinate rows, 7 public-feed owner/provider rows, and 2 rows where
  the same OpenAQ public-feed location is reused across multiple official
  candidates. It screens all 7 rows as public-feed nearby rows that are not
  join-ready and keeps official agency owner/provider matches, shared station
  IDs, source-owner crosswalks, current-status crosswalks, documented
  co-location rows, validated same-station joins, and station-radius-ready rows
  at 0. The next row-level source-review queue is the broader one-signal set:
  near-only, name-only-not-near, and monitor-grade one-signal official rows.
  The public route now renders the candidate public-feed source-scan panel.
  Chrome CDP QA passed at 1440x1100 and 390x1000 with 5 public-feed stat
  cards, 4 country cards, 7 row cards, 10 source cards, 3 download links, no
  page or section horizontal overflow, no text overflow, and no console/page
  errors. Screenshots:
  `reporting-site/qa/showcase-air-public-feed-source-scan-desktop.png`,
  `reporting-site/qa/showcase-air-public-feed-source-scan-mobile.png`, and
  `reporting-site/qa/showcase-air-public-feed-source-scan-mobile-sources.png`.
- **2026-06-19 (air-monitoring candidate crosswalk source scan):** Added
  `air-monitoring/source-inputs/candidate-crosswalk-public-source-seed.csv`,
  `air-monitoring/scripts/scan-official-openaq-candidate-crosswalk-sources.py`,
  generated
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv`
  and
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json`,
  and wrote
  `air-monitoring/official-openaq-candidate-crosswalk-source-scan.md`. The
  scan targets the 6 OpenAQ `isMonitor` candidate rows, retrieves all 5 seeded
  public source URLs, finds official coordinate evidence for the 2 Bangladesh
  SPARTAN-adjacent rows and Uzhydromet public-map address evidence for the 4
  Uzbekistan StateAir-adjacent rows, screens all 6 as
  `separate_nearby_stations`, and keeps shared station-ID rows,
  source-crosswalk rows, documented co-location rows, validated same-station
  joins, and station-radius-ready rows at 0. The follow-on public-feed scan
  handles the 7 not-`isMonitor` rows separately.
  The public route now renders the candidate crosswalk source-scan panel.
  Chrome CDP QA passed at 1440x1100 and 390x1000 with 5 source-scan stat
  cards, 2 country cards, 6 row cards, 5 source cards, 3 download links, no
  page or section horizontal overflow, no text overflow, and no console/page
  errors. Screenshots:
  `reporting-site/qa/showcase-air-crosswalk-source-scan-desktop.png`,
  `reporting-site/qa/showcase-air-crosswalk-source-scan-mobile.png`, and
  `reporting-site/qa/showcase-air-crosswalk-source-scan-mobile-sources.png`.
- **2026-06-19 (air-monitoring candidate public-evidence audit):** Added
  `air-monitoring/scripts/audit-official-openaq-candidate-public-evidence.py`,
  generated
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-public-evidence.csv`
  and
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json`,
  and wrote
  `air-monitoring/official-openaq-candidate-public-evidence.md`. The audit
  attaches OpenAQ owner/provider, `isMonitor`, sensor-count, and first/last-seen
  metadata to all 13 candidate worksheet rows across 4 economies and 9 unique
  OpenAQ location IDs. It records 13 rows with owner/provider metadata, 6
  OpenAQ `isMonitor` true rows, 7 rows not marked `isMonitor`, 11 first-seen
  rows, 11 last-seen rows, 0 exact station-ID overlaps, 0 exact official-agency
  owner/provider matches, 0 explicit crosswalk rows, 0 validated same-station
  joins, and 0 station-radius-ready rows. This makes the candidate queue
  easier to inspect but does not validate any station crosswalk or monitor-grade
  claim. The public route now renders the candidate public-evidence panel.
  Chrome CDP QA passed at 1440x1100 and 390x1000 with 5 public-evidence stat
  cards, 2 evidence-lane cards, 4 country cards, 6 row cards, 5 evidence gates,
  3 download links, no page or section horizontal overflow, and no console/page
  errors. Screenshots:
  `reporting-site/qa/showcase-air-openaq-candidate-evidence-desktop.png`,
  `reporting-site/qa/showcase-air-openaq-candidate-evidence-mobile.png`, and
  `reporting-site/qa/showcase-air-openaq-candidate-evidence-mobile-gates.png`.
- **2026-06-19 (air-monitoring candidate station-crosswalk worksheet):**
  Added `air-monitoring/scripts/build-official-openaq-candidate-review.py`,
  generated
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-review.csv`
  and
  `air-monitoring/generated/air-monitoring-official-openaq-candidate-review-summary.json`,
  and wrote `air-monitoring/official-openaq-candidate-review.md`. The
  worksheet reads the official/OpenAQ reconciliation audit and the official
  station-source extraction, filters only the 13 near-plus-name candidate rows
  across 4 economies, and adds row-level review questions, allowed decisions,
  source metadata, and minimum validation evidence. It records 0 station-ID
  crosswalk rows, 0 public current-status confirmation rows, 0 validated
  same-station joins, and 0 station-radius-ready rows. This narrows the next
  review queue but does not validate any station crosswalk or catchment claim.
  The public route now renders the candidate-review worksheet panel. Chrome CDP
  QA passed at 1440x1100 and 390x1000 with 4 stat cards, 4 review-flow cards,
  4 country cards, 6 row cards, 5 evidence gates, 3 download links, no page or
  section horizontal overflow, and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-openaq-candidate-desktop.png`,
  `reporting-site/qa/showcase-air-openaq-candidate-mobile.png`, and
  `reporting-site/qa/showcase-air-openaq-candidate-mobile-gates.png`.
- **2026-06-19 (air-monitoring official-to-OpenAQ reconciliation audit):**
  Added `air-monitoring/scripts/reconcile-official-openaq-stations.py`,
  generated
  `air-monitoring/generated/air-monitoring-official-openaq-reconciliation.csv`
  and
  `air-monitoring/generated/air-monitoring-official-openaq-reconciliation-summary.json`,
  and wrote `air-monitoring/official-openaq-reconciliation.md`. The audit uses
  the official station-source extraction's nearest-OpenAQ within-5-kilometer
  diagnostic and name-overlap signal rather than inventing a new fuzzy-match
  threshold. It covers 230 official coordinate rows and 82 OpenAQ coordinate
  rows in the same five economies, then classifies 13 near-plus-name candidate
  rows, 9 near-only candidate rows, 22 name-only-not-near candidate rows, 186
  official coordinate rows without either candidate signal, 69 OpenAQ rows not
  used as a near candidate, and 0 validated same-station joins. The public
  route now renders an official/OpenAQ reconciliation ladder; station-radius
  claims remain blocked until candidate rows become documented crosswalk rows.
  Browser QA passed at 1440x1100 and 390x1000 with 5 stat cards, 4 lane cards,
  5 country cards, 6 evidence gates, 3 download links, no page or section
  horizontal overflow, and no console/page errors.
- **2026-06-19 (air-monitoring monitor-grade evidence audit):** Added
  `air-monitoring/scripts/audit-monitor-grade-evidence.py`, generated
  `air-monitoring/generated/air-monitoring-monitor-grade-evidence.csv` and
  `air-monitoring/generated/air-monitoring-monitor-grade-evidence-summary.json`,
  and wrote `air-monitoring/monitor-grade-evidence.md`. The audit reads all
  239 official-source rows from the official station-source extraction pass,
  verifies Bangladesh method-standard language and Sri Lanka sensor-under-test
  language, and separates method-standard evidence from weaker automatic or
  official-portal provenance. It records 31 source-specific method-standard
  signal rows in Bangladesh, 138 automatic or official-portal signal-only
  rows, 3 sensor-under-test rows, 2 plan-only rows, 65 rows with no public
  grade language found, and 0 complete monitor-grade classification rows. The
  public showcase now renders a monitor-grade evidence ladder and keeps the
  station-radius/catchment claim blocked until complete grade classification
  and gridded denominators exist. Verification passed: audit script rerun,
  `py_compile`, evidence/doc/reference sync, production build, six deterministic
  gates, source-output contact/token scan with no matches, and Chrome CDP
  desktop/mobile QA with 5 stat cards, 5 ladder cards, 9 country cards, 6
  evidence gates, 3 downloads, no horizontal overflow, and no console/page
  errors.
- **2026-06-19 (air-monitoring metadata-readiness wall):** Added
  `air-monitoring/scripts/build-metadata-readiness-audit.py`, generated
  `air-monitoring/generated/air-monitoring-metadata-readiness-audit.csv` and
  `air-monitoring/generated/air-monitoring-metadata-readiness-audit-summary.json`,
  wrote `air-monitoring/metadata-readiness-audit.md`, and added
  `air-monitoring/STATUS.md`. The no-network audit reads the committed
  country panel and concentration/GDP-confound deepening. It records 50
  country-panel rows, 13 zero-public-monitor above-guideline economies, 33
  monitored economies with GDP residuals, 5 baseline gap-score top-five rows,
  10 positive GDP-residual queue rows, and 24 unique upgrade-queue rows. It
  finds 0 station-level cache files, 0 station-coordinate rows, 0 monitor-grade
  rows, 0 first-seen/vintage rows, 0 regulatory-inventory rows, and marks
  station-radius analysis as not ready. The public showcase now renders the
  metadata-readiness wall with 7 gate cards, 4 summary cards, 10 queue cards,
  and audit note/JSON/CSV downloads. Verification passed: audit script rerun,
  script `py_compile`, evidence/reference sync, production site build, six
  deterministic gates plus `git diff --check`, and Chrome CDP desktop/mobile
  QA at 1440x1100 and 390x900 with no page or metadata-section horizontal
  overflow, no page errors, and only existing React Router future-flag
  warnings. Screenshots:
  `reporting-site/qa/showcase-air-metadata-readiness-desktop.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-desktop-cards.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-mobile.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-mobile-cards.png`,
  `reporting-site/qa/showcase-air-metadata-readiness-mobile-gates.png`, and
  `reporting-site/qa/showcase-air-metadata-readiness-mobile-queue.png`.
  Next AI-doable work is station-level source collection, not station-radius
  claims.
- **2026-06-19 (air-monitoring OpenAQ station-metadata source access):**
  Added `air-monitoring/scripts/fetch-openaq-station-metadata.py`,
  generated
  `air-monitoring/generated/air-monitoring-openaq-station-metadata.csv` and
  `air-monitoring/generated/air-monitoring-openaq-station-metadata-summary.json`,
  wrote `air-monitoring/station-metadata-source-access.md`, and added
  `air-monitoring/.cache/README.md`. The script reads the committed
  metadata-readiness upgrade queue, queries the OpenAQ v3 `locations`
  endpoint with `parameters_id=2` for the 24 non-panel-context economies, and
  uses a configured local API key without printing or committing it. The pass
  computed all 24 target economies with 0 API errors, 11 economies with OpenAQ
  PM2.5 station rows, 13 economies with zero OpenAQ PM2.5 station rows, 101
  OpenAQ PM2.5 station rows, 101 coordinate rows, 101 owner/provider rows, 93
  first-seen rows, 2 coordinate-QC exclusions, 0 monitor-grade rows, 0
  regulator-inventory rows, and station-radius analysis still not ready. Raw
  API responses are cached under
  `.cache/openaq-station-metadata/` and intentionally git-ignored; committed
  reproducibility is the script plus generated CSV/JSON retrieval records.
  The public route now renders the station-source panel with 5 station stat
  cards, 101 map dots, 11 country rows, 13 zero-OpenAQ chips, 7 evidence gate
  cards, note/JSON/CSV downloads, and the 2 coordinate-QC exclusions. Browser
  QA at 1440x1100 and 390x900 found no page, section, or map horizontal
  overflow, no out-of-bounds SVG station dots, and no console/page errors.
  Screenshots:
  `reporting-site/qa/showcase-air-station-metadata-desktop.png`,
  `reporting-site/qa/showcase-air-station-metadata-desktop-map.png`,
  `reporting-site/qa/showcase-air-station-metadata-mobile.png`, and
  `reporting-site/qa/showcase-air-station-metadata-mobile-map.png`. Next loop
  is to collect regulator inventories and monitor-grade sources before any
  no-monitor-on-ground or catchment-coverage claim.
- **2026-06-19 (air-monitoring regulator-source discovery):** Added
  `air-monitoring/source-inputs/regulator-source-inventory-seed.csv`,
  `air-monitoring/scripts/build-regulator-source-inventory.py`,
  generated
  `air-monitoring/generated/air-monitoring-regulator-source-inventory.csv` and
  `air-monitoring/generated/air-monitoring-regulator-source-inventory-summary.json`,
  and wrote `air-monitoring/regulator-source-inventory.md`. The pass covers
  24 upgrade-queue economies, identifies 11 official regulator or portal
  source candidates, 9 official station-inventory or air-quality portal
  candidates, 6 official station-count claim rows, 0 monitor-grade
  classification rows, and 11 targeted-search gaps. Among the 13 zero-OpenAQ
  economies, it finds 1 official inventory or portal candidate, 2 official
  regulator pages with no station inventory found, 1 development-partner
  monitoring reference, and 9 targeted-search gaps. The public showcase route
  now renders the regulator-source wall; Chrome CDP QA at 1440x1100 and
  390x900 confirmed 5 stat cards, 4 zero-grid cells, 4 source groups, 24
  country rows, 5 evidence gates, 3 download links, no page or section
  horizontal overflow, and no console/page errors. Screenshots:
  `reporting-site/qa/showcase-air-regulator-source-desktop.png` and
  `reporting-site/qa/showcase-air-regulator-source-mobile.png`. This is source
  discovery, not regulator validation, not monitor-grade validation, not proof
  of no monitor outside OpenAQ, and not station-radius population coverage.
  Next loop is station-table or portal extraction from official source
  candidates.
- **2026-06-19 (rotation to air-monitoring):** Rotated the active flagship
  from `public-service-data-quality` to `air-monitoring` after PSDQ received
  the 10-stage evidence ladder in commit `8913943` and returned to the
  owner-only source-owner contact or human-validation wall. The next
  AI-doable showcase loop is air-monitoring observability: first make the
  station-level metadata wall explicit, then fetch and version station
  coordinates, monitor grade/owner, station vintage, and regulator inventories
  before any station-radius or catchment claim. No PSDQ maturity label
  changed.
- **2026-06-19 (PSDQ evidence ladder):** Added
  `public-service-data-quality/scripts/build-bgd-facility-evidence-ladder.py`,
  generated
  `psdq-bgd-facility-validation-evidence-ladder.csv` and
  `psdq-bgd-facility-validation-evidence-ladder-summary.json`, and wrote
  `public-service-data-quality/facility-validation-evidence-ladder.md`. The
  no-network ladder reads 10 committed PSDQ Bangladesh facility-validation
  summary artifacts and emits 10 stages from source-disagreement strata to the
  AI closure audit. It records 76 sampled facility rows, 40 targeted
  public-source rows, 39 human-gated handoff rows, 39 AI closure-audit rows,
  0 rows actionable without human or source-owner evidence, 39 keep-open-only
  terminal rows, and 39 human- or source-owner wall rows. This is a
  reader-navigation artifact, not a statistical funnel, source-owner response,
  human validation, ground truth, coordinate correction, row closure,
  same-facility reclassification, map-absence validation, maturity promotion,
  or a human-final upgrade. Verification passed: ladder script rerun, script
  `py_compile`, evidence/reference sync, production site build, six
  deterministic gates plus `git diff --check`, review packet and zip rebuild,
  and Chrome CDP desktop/mobile QA at 1440x1100 and 390x900 with 10 ladder
  stage cards, 4 summary cards, evidence-ladder note/JSON/CSV links visible,
  no page-level or ladder-section horizontal overflow, no page errors, and
  only existing React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-psdq-evidence-ladder-desktop.png`,
  `reporting-site/qa/showcase-psdq-evidence-ladder-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-evidence-ladder-mobile.png`, and
  `reporting-site/qa/showcase-psdq-evidence-ladder-mobile-cards.png`.
- **2026-06-19 (PSDQ AI closure audit):** Added
  `public-service-data-quality/scripts/build-bgd-facility-ai-closure-audit.py`,
  generated
  `psdq-bgd-facility-validation-ai-closure-audit.csv` and
  `psdq-bgd-facility-validation-ai-closure-audit-summary.json`, and wrote
  `public-service-data-quality/facility-validation-ai-closure-audit.md`. The
  no-network audit reads the 39-row human-validation worksheet, then checks
  whether current public evidence and blank human-review fields permit AI
  closure, same-facility reclassification, map-absence language, or coordinate
  correction without source-owner or human-validation evidence. It audits 39
  rows across 5 handoff groups and 15 upazilas; records 39 human- or
  source-owner wall rows; 0 external contacts; 0 AI closure rows; 0 AI
  same-facility reclassification rows; 0 AI map-absence language rows; 0 AI
  coordinate-correction rows; 0 rows actionable without human or source-owner
  evidence; and 39 keep-open-only rows. This is a no-contact decision gate,
  not source-owner response, human validation, ground truth, coordinate
  correction, row closure, same-facility reclassification, map-absence
  validation, maturity promotion, or a human-final upgrade. Verification
  passed: handoff/worksheet/audit chain rerun, audit script `py_compile`,
  evidence/reference sync, production site build, six deterministic gates plus `git diff --check`, review packet and zip rebuild, and Chrome CDP
  desktop/mobile QA at 1440x1100 and 390x900 with 6 gate cards, 4 wall cards,
  10 upazila cards, 12 row cards, audit note and CSV links visible, no
  page-level or section-level horizontal overflow, no page errors, and only
  existing React Router development warnings. Screenshots:
  `reporting-site/qa/showcase-psdq-ai-closure-audit-desktop.png`,
  `reporting-site/qa/showcase-psdq-ai-closure-audit-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-ai-closure-audit-mobile.png`, and
  `reporting-site/qa/showcase-psdq-ai-closure-audit-mobile-cards.png`.
- **2026-06-19 (PSDQ human-validation worksheet):** Added
  `public-service-data-quality/scripts/build-bgd-facility-human-validation-worksheet.py`,
  generated
  `psdq-bgd-facility-validation-human-validation-worksheet.csv` and
  `psdq-bgd-facility-validation-human-validation-worksheet-summary.json`, and
  wrote
  `public-service-data-quality/facility-validation-human-validation-worksheet.md`.
  The no-network review reads the 39-row human-gated handoff CSV, then
  pre-fills public evidence, review questions, minimum acceptable evidence
  rules, allowed decision values, and current public evidence gates. It leaves
  39 human-validation status fields and 39 proposed decision fields blank and
  carries forward 0 external contacts, 0 prefilled closure rows, 0 prefilled
  reclassification rows, 0 prefilled map-absence rows, and 0 prefilled
  coordinate-correction rows. This is a no-contact review instrument, not
  source-owner response, human validation, ground truth, coordinate correction,
  row closure, same-facility reclassification, map-absence validation, maturity
  promotion, or a human-final upgrade. Verification passed: worksheet script
  rerun, script `py_compile`, evidence/reference sync, production site build,
  six deterministic gates plus `git diff --check`, review packet and zip
  rebuild, and agent-browser desktop/mobile QA at 1440x1100 and 390x900 with
  worksheet note/CSV links visible, no page-level or card-level horizontal
  overflow, no page errors, and only existing Vite / React Router development
  warnings.
  Screenshots:
  `reporting-site/qa/showcase-psdq-human-validation-worksheet-links-desktop.png`
  and
  `reporting-site/qa/showcase-psdq-human-validation-worksheet-links-mobile.png`.
- **2026-06-19 (PSDQ human-gated handoff matrix):** Added
  `public-service-data-quality/scripts/build-bgd-facility-human-gated-handoff.py`,
  generated `psdq-bgd-facility-validation-human-gated-handoff.csv` and
  `psdq-bgd-facility-validation-human-gated-handoff-summary.json`, and wrote
  `public-service-data-quality/facility-validation-human-gated-handoff.md`.
  The no-network review reads the source-repair clarification packet,
  possible same-facility review, priority and lower-priority name-conflict
  reviews, and zero-OSM observability summary, then consolidates 39 open rows
  across 5 groups and 15 upazilas: 3 source-repair clarifications, 3 possible
  same-facility rows, 9 priority name-conflict rows, 6 lower-priority
  name-conflict rows, and 18 zero-OSM facility-row absence gates. It records
  39 rows requiring human or source-owner action and allows 0 closures, 0
  same-facility reclassifications, 0 map-absence uses, 0 coordinate
  corrections, and 0 external contacts. This is a no-contact reviewer queue,
  not source-owner response, human validation, ground truth, coordinate
  correction, row closure, same-facility reclassification, map-absence
  validation, maturity promotion, or a human-final upgrade. Verification
  passed: handoff script rerun, script `py_compile`, evidence/reference sync,
  production site build, six deterministic gates plus `git diff --check`,
  review packet and zip rebuild, and agent-browser desktop/mobile QA at
  1440x1100 and 390x900 with 5 group cards, 10 upazila cards, 12 handoff row
  cards, no page-level or card-level horizontal overflow, no page errors, no
  console messages, Durgapur, `0 closed`, and `0 map absence uses` visible.
  Screenshots:
  `reporting-site/qa/showcase-psdq-human-gated-handoff-desktop.png`,
  `reporting-site/qa/showcase-psdq-human-gated-handoff-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-human-gated-handoff-mobile.png`, and
  `reporting-site/qa/showcase-psdq-human-gated-handoff-mobile-cards.png`.
- **2026-06-19 (PSDQ lower-priority name-conflict spot check):** Added
  `public-service-data-quality/scripts/build-bgd-facility-lower-priority-name-conflict-review.py`,
  generated
  `psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv`
  and
  `psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-lower-priority-name-conflict-review.md`.
  The no-network review reads the targeted public-source confirmation CSV and
  decision-ledger summary for the 6 lower-priority name-conflict public-map
  candidates deferred by the decision ledger. All 6 rows have DGHS profiles
  and OSM API records retrieved; 4 rows share reused public-map candidate
  features; all 6 candidates are at least 5 kilometers from the inspection
  point; 3 candidates are at least 10 kilometers away; 1 candidate name score
  is at least 0.50; 0 candidate name scores are at least 0.70; and the current
  artifacts contain 0 public alias/location sources. It allows 0 closures, 0
  same-facility reclassifications, 0 map-absence uses, 0 row
  reclassifications, and 0 external contacts. This is a no-contact spot-check
  evidence gate, not source-owner response, human validation, ground truth,
  coordinate correction, row closure, same-facility reclassification,
  map-absence validation, maturity promotion, or a human-final upgrade.
  Verification passed: lower-priority name-conflict script rerun, script
  `py_compile`, evidence sync, production site build, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with 6 row cards, 4
  candidate-cluster cards, no page-level or card-level horizontal overflow, no
  page errors, `momotaz clinic`, `Broadbank Clinic Quatere`, `0 alias source`,
  and `0 map absence uses` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-mobile-cards.png`.
- **2026-06-19 (PSDQ zero-OSM upazila observability review):** Added
  `public-service-data-quality/scripts/build-bgd-facility-zero-osm-upazila-observability-review.py`,
  generated
  `psdq-bgd-facility-validation-zero-osm-upazila-observability-review.csv`
  and
  `psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-zero-osm-upazila-observability-review.md`.
  The no-network review reads the exposure-ranked disagreement table,
  exposure summary, targeted public-map inspection queue, and
  decision-ledger summary to separate 115 active-registry upazilas with 0
  joined OSM health features from row-level facility absence claims. The
  packet covers 3,879 active DGHS clinical rows and 2,334,152 p85 buildings in
  the 3 km under-observed proxy, links 18 deferred inspection rows across 5
  targeted upazilas, and allows 0 facility closures, 0 facility-level absence
  uses, 0 coordinate corrections, 0 row reclassifications, and 0 external
  contacts. This is upazila-level source observability context, not
  source-owner response, human validation, ground truth, facility-level
  absence evidence, coordinate correction, row closure, same-facility
  reclassification, maturity promotion, or a human-final upgrade.
  Verification passed: zero-OSM script rerun, program-script `py_compile`,
  evidence/reference/docs sync, production site build, six deterministic gates
  plus `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with 8 division cards, 10
  top-upazila cards, 8 targeted-strip cards, no page-level or card-level
  horizontal overflow, no page errors, Sonargaon, Chattogram, `0 closed`, and
  `0 facility absence uses` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-zero-osm-observability-desktop.png`,
  `reporting-site/qa/showcase-psdq-zero-osm-observability-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-zero-osm-observability-mobile.png`, and
  `reporting-site/qa/showcase-psdq-zero-osm-observability-mobile-cards.png`.
- **2026-06-19 (PSDQ priority name-conflict review):** Added
  `public-service-data-quality/scripts/build-bgd-facility-priority-name-conflict-review.py`,
  generated
  `psdq-bgd-facility-validation-priority-name-conflict-review.csv`
  and
  `psdq-bgd-facility-validation-priority-name-conflict-review-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-priority-name-conflict-review.md`.
  The no-network review reads the public-source decision ledger and
  targeted-row confirmation CSV for the 9 priority-1 name-conflict public-map
  candidates. All 9 rows have DGHS profiles and OSM API records retrieved; 1
  row has candidate name score at least 0.70; 6 candidates are at least 5
  kilometers from the inspection point; 1 candidate is at least 10 kilometers
  from the inspection point; 4 candidate names contain an admin place name; and
  the current artifacts contain 0 public alias/location sources. It allows 0
  closures, 0 same-facility reclassifications, and 0 map-absence uses. This is
  a no-contact evidence gate, not source-owner response, human validation,
  ground truth, coordinate correction, row closure, same-facility
  reclassification, maturity promotion, or a human-final upgrade. Verification
  passed: priority name-conflict script rerun, program-script `py_compile`,
  evidence/reference/docs sync, production site build, six deterministic gates
  plus `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with 9 rendered cards, no
  page-level or card-level horizontal overflow, no page errors, no console
  messages, Pabna, Narsingdi, `0 alias source`, and `0 closed` visible.
  Screenshots:
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-mobile-cards.png`.
- **2026-06-19 (PSDQ possible same-facility review):** Added
  `public-service-data-quality/scripts/build-bgd-facility-possible-same-facility-review.py`,
  generated
  `psdq-bgd-facility-validation-possible-same-facility-review.csv`
  and
  `psdq-bgd-facility-validation-possible-same-facility-review-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-possible-same-facility-review.md`.
  The no-network review reads the public-source decision ledger and
  targeted-row confirmation CSV for the 3 possible same-facility public-map
  candidates. All 3 rows have DGHS profiles and OSM API records retrieved; 1
  row has name score at least 0.95; all 3 candidates are at least 2 kilometers
  from the inspection point; and 0 rows are allowed for closure, same-facility
  reclassification, or map-absence language. This is a no-contact evidence
  gate, not source-owner response, human validation, ground truth, coordinate
  correction, row closure, same-facility reclassification, maturity promotion,
  or a human-final upgrade. Verification passed: possible same-facility script
  rerun, program-script `py_compile`, evidence/reference/docs sync, production
  site build, six deterministic gates plus `git diff --check`, review packet
  and zip rebuild, and agent-browser desktop/mobile QA at 1440x1100 and
  390x900 with 3 rendered cards, no page-level or card-level horizontal
  overflow, no page errors, no console messages, KPJ, Aichi, Chattogram, and
  `0 closed` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-mobile-cards.png`.
- **2026-06-19 (PSDQ source-repair registry-vintage review):** Added
  `public-service-data-quality/scripts/build-bgd-facility-source-repair-registry-vintage-review.py`,
  generated
  `psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv`
  and
  `psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-source-repair-registry-vintage-review.md`.
  The no-network review reads the clarification packet, public-explanation
  evidence CSV, and correction-record follow-up CSV for the same 3 unresolved
  rows. All 3 rows have DGHS profile update timestamps; those timestamps were 1
  to 12 days old at public-explanation retrieval; 0 public correction or
  coordinate-source records were found; and 0 rows are allowed for closure,
  same-facility reclassification, or map-absence language. This is a no-contact
  registry-vintage review packet, not source-owner response, human validation,
  ground truth, coordinate correction, row closure, same-facility
  reclassification, maturity promotion, or a human-final upgrade. Verification
  passed: registry-vintage script rerun, program-script `py_compile`,
  evidence/reference sync, production site build, six deterministic gates plus
  `git diff --check`, and agent-browser desktop/mobile QA at 1440x1100 and
  390x900 with 3 rendered cards, no page-level horizontal overflow, no page
  errors, Durgapur and linked code `10000470` visible, the 1-12 day age range
  visible, and only existing Vite / React Router development warnings.
  Screenshots:
  `reporting-site/qa/showcase-psdq-registry-vintage-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-registry-vintage-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-registry-vintage-review-mobile.png`, and
  `reporting-site/qa/showcase-psdq-registry-vintage-review-mobile-cards.png`.
- **2026-06-19 (PSDQ source-repair clarification packet):** Added
  `public-service-data-quality/scripts/build-bgd-facility-source-repair-clarification-packet.py`,
  generated
  `psdq-bgd-facility-validation-source-repair-clarification-packet.csv`
  and
  `psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-source-repair-clarification-packet.md`.
  The no-network packet reads the source-repair correction-record follow-up CSV,
  targets the 2 shared-coordinate Narayanganj rows plus the Durgapur same-name
  cross-district conflict, and creates 3 source-owner or human-review
  questions. It records 0 external contacts, carries forward 0 public
  correction or coordinate-source records found, closes 0 rows, and
  reclassifies 0 rows. This is a no-contact clarification packet, not
  source-owner response, human validation, ground truth, coordinate correction,
  row closure, same-facility reclassification, maturity promotion, or a
  human-final upgrade. Verification passed: clarification script rerun,
  program-script `py_compile`, evidence/reference sync, production site build,
  six deterministic gates plus `git diff --check`, review packet and zip
  rebuild, and agent-browser desktop/mobile QA at 1440x1100 and 390x900 with 3
  rendered cards, no page-level horizontal overflow, no page errors, Durgapur
  and linked code `10000470` visible, and only existing React Router
  development warnings. Screenshots:
  `reporting-site/qa/showcase-psdq-clarification-packet-desktop.png`,
  `reporting-site/qa/showcase-psdq-clarification-packet-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-clarification-packet-mobile.png`, and
  `reporting-site/qa/showcase-psdq-clarification-packet-mobile-cards.png`.
- **2026-06-19 (PSDQ source-repair correction-record follow-up):** Added
  `public-service-data-quality/scripts/followup-bgd-facility-source-repair-correction-records.py`,
  generated
  `psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`
  and
  `psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-source-repair-correction-record-followup.md`.
  The live public-source follow-up reads the source-repair public-explanation
  evidence CSV, selects the two shared-coordinate Narayanganj records and the
  Durgapur same-name cross-district conflict, and checks public DGHS registry
  pages, DGHS Health Dashboard pages, and public government health portals for
  correction records or coordinate-source notes. It checks 20 public official
  sources and retrieves all 20; finds 0 public correction or coordinate-source
  records; confirms the DGHS dashboard target code for all 3 targeted rows;
  confirms the linked Rajshahi Durgapur dashboard code for the Durgapur
  conflict; and closes or reclassifies 0 rows. This is public correction-record
  follow-up, not human validation, ground truth, coordinate correction, row
  closure, same-facility reclassification, maturity promotion, or a human-final
  upgrade. Verification passed: correction-record script rerun, program-script
  `py_compile`, evidence/reference sync, production site build, six
  deterministic gates plus `git diff --check`, review packet and zip rebuild,
  and agent-browser desktop/mobile QA at 1440x1100 and 390x900 with no
  page-level horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-correction-followup-desktop.png`,
  `reporting-site/qa/showcase-psdq-correction-followup-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-correction-followup-mobile.png`, and
  `reporting-site/qa/showcase-psdq-correction-followup-mobile-cards.png`.
- **2026-06-19 (PSDQ source-repair public-explanation evidence):** Added
  `public-service-data-quality/scripts/search-bgd-facility-source-repair-public-explanations.py`,
  generated
  `psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`
  and
  `psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-source-repair-public-explanation-evidence.md`.
  The live public-source pass reads the four-row official-coordinate evidence
  CSV, joins cached DGHS public registry records, checks live DGHS profile
  tabs, and fetches linked public government health portals where available.
  It checks 4 source-repair rows, 8 live DGHS profile tabs, and 6 official
  portal URLs; retrieves 5 official portal pages; finds 0 explicit public
  coordinate-source or coordinate-correction explanations; records 2 rows
  sharing one official profile coordinate; records 1 row with a same-name
  cross-district DGHS registry sibling; and records 1 row where that
  same-name other-district coordinate is within 2 kilometers. The Netrakona
  Durgapur row is 747.0 meters from the separate Rajshahi Durgapur official
  record. All 4 source-repair rows remain open with 0 AI closures and 0 AI
  reclassifications. This is public-source explanation evidence, not human
  validation, a coordinate correction, row closure, a maturity promotion, or a
  human-final upgrade. Verification passed: public-explanation script rerun,
  program-script `py_compile`, production site build, six deterministic gates
  plus `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-explanation-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-explanation-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-public-explanation-mobile.png`, and
  `reporting-site/qa/showcase-psdq-public-explanation-mobile-cards.png`.
  Next PSDQ loop is targeted correction-record follow-up for the Durgapur
  conflict and the shared-coordinate Narayanganj records.
- **2026-06-19 (PSDQ source-repair official-coordinate evidence):** Added
  `public-service-data-quality/scripts/explain-bgd-facility-source-repair-official-coordinates.py`,
  generated
  `psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv`
  and
  `psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-source-repair-official-coordinate-evidence.md`.
  The live public-source pass reads the four-row source-repair evidence
  attachment, joins the targeted public-map inspection CSV, retrieves the 4
  public DGHS profile pages, parses the embedded official map coordinate, and
  compares it with the pinned OSM candidate coordinate. All 4 profiles were
  retrieved; all 4 expose official profile coordinates; all 4 coordinates
  match the inspection CSV; 2 rows share one official profile coordinate; 2
  rows are at least 10 kilometers from the named OSM candidate; 1 row is at
  least 50 kilometers from the named OSM candidate; and 0 explicit
  coordinate-source explanations are exposed. All 4 source-repair rows remain
  open with 0 AI closures and 0 AI reclassifications. This is public-source
  coordinate evidence, not human validation, a coordinate correction, row
  closure, a maturity promotion, or a human-final upgrade. Verification
  passed: official-coordinate script rerun, new script `py_compile`,
  program-script `py_compile`, production site build, six deterministic gates
  plus `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-mobile-cards.png`.
  Next PSDQ loop is the public-explanation evidence pass recorded above.
- **2026-06-19 (PSDQ source-repair public evidence):** Added
  `public-service-data-quality/scripts/attach-bgd-facility-source-repair-public-evidence.py`,
  generated
  `psdq-bgd-facility-validation-source-repair-public-evidence.csv` and
  `psdq-bgd-facility-validation-source-repair-public-evidence-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-source-repair-public-evidence.md`.
  The no-network pass reads the public-source decision ledger and targeted-row
  confirmation CSV, then attaches public DGHS profile and OSM API evidence to
  the 4 source-repair-first rows. All 4 have public evidence attached; 2 rows
  share one public-map candidate; 2 rows have candidate distance of at least
  10 kilometers; and 1 row has candidate distance of at least 50 kilometers.
  All 4 source-repair rows remain open with 0 AI closures and 0 AI
  reclassifications. This is public-source evidence attachment, not human
  validation, source repair completion, row closure, a maturity promotion, or
  a human-final upgrade. Verification passed: source-repair evidence script
  rerun, new script `py_compile`, program-script `py_compile`, production
  site build, six deterministic gates plus `git diff --check`, review packet
  and zip rebuild, and agent-browser desktop/mobile QA at 1440x1100 and
  390x900 with no page-level horizontal overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-source-repair-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-source-repair-evidence-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-source-repair-evidence-mobile.png`, and
  `reporting-site/qa/showcase-psdq-source-repair-evidence-mobile-cards.png`.
  Next PSDQ loop is the official-coordinate evidence pass recorded above.
- **2026-06-19 (PSDQ public-source decision ledger):** Added
  `public-service-data-quality/scripts/build-bgd-facility-public-source-decision-ledger.py`,
  generated
  `psdq-bgd-facility-validation-public-source-decision-ledger.csv` and
  `psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-public-source-decision-ledger.md`.
  The no-network pass reads the 40-row targeted public-source confirmation
  CSV/summary and selects 16 reviewer decision rows: 4 source-repair rows, 3
  possible same-facility rows, and 9 priority-1 name-conflict rows. It defers
  18 zero-OSM upazila observability rows and 6 lower-priority name-conflict
  spot checks. All 40 targeted rows remain open with 0 AI closures and 0 AI
  reclassifications. This is a public-source reviewer queue, not human
  validation, a row closure, a maturity promotion, or a human-final upgrade.
  Verification passed: decision-ledger script rerun, program-script
  `py_compile`, production site build, six deterministic gates plus
  `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-desktop-chart.png`,
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-mobile-list.png`.
  Next PSDQ loop is attaching official public evidence to the 16
  decision-ledger rows, starting with source-repair rows because
  coordinate/source repair changes the interpretation of map absence.
- **2026-06-19 (PSDQ targeted-row public-source confirmation):** Added
  `public-service-data-quality/scripts/confirm-bgd-facility-public-map-targeted-rows.py`,
  generated
  `psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
  and
  `psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-public-source-confirmation-targeted-rows.md`.
  The live public-source pass reads the 40-row targeted public-map inspection
  CSV and retrieves public DGHS profile pages plus public OSM API feature
  records for every targeted inspection row. It retrieves 40 DGHS profiles and
  40 OSM API records, covers all 30 priority-1 rows, records DGHS profile
  token support for all 40 rows, records 6 rows with live OSM candidate-name
  scores at or above 0.75, and keeps all 40 rows open with 0 AI closures and
  0 AI reclassifications. Confirmation lanes: 18 zero-OSM context candidates
  outside the upazila, 15 candidate features retrieved but name conflict
  remains, 4 source-repair public sources retrieved, and 3 possible
  same-facility candidates needing manual location check. This is
  public-source confirmation, not human validation, a maturity promotion, a
  row closure, or a human-final upgrade. Verification passed: targeted-row
  confirmation script rerun, program-script `py_compile`, production site
  build, six deterministic gates plus `git diff --check`, review packet and
  zip rebuild, and agent-browser desktop/mobile QA at 1440x1100 and 390x900
  with no page-level horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-desktop.png`,
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-desktop-chart.png`,
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-mobile-list.png`.
  Next PSDQ loop is a decision ledger for the 3 possible same-facility rows,
  the 4 source-repair rows, and selected high-exposure name-conflict rows.
- **2026-06-19 (PSDQ first-row public-source confirmation):** Added
  `public-service-data-quality/scripts/confirm-bgd-facility-public-map-first-rows.py`,
  generated
  `psdq-bgd-facility-validation-public-source-confirmation.csv` and
  `psdq-bgd-facility-validation-public-source-confirmation-summary.json`, and
  wrote
  `public-service-data-quality/facility-validation-public-source-confirmation.md`.
  The live public-source pass reads the targeted inspection summary and
  retrieves public DGHS profile pages plus public OSM API feature records for
  the first 12 inspection rows. It retrieves 12 DGHS profiles and 12 OSM API
  records, records DGHS profile token support for all 12 rows, records 2 rows
  with live OSM candidate-name score at or above 0.75, and keeps all 12 rows
  open with 0 AI closures and 0 AI reclassifications. This is public-source
  confirmation, not human validation, a maturity promotion, or a human-final
  upgrade. Verification passed: confirmation script rerun, new script
  `py_compile`, program-script `py_compile`, production site build, six
  deterministic gates plus `git diff --check`, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-confirmation-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-source-confirmation-desktop-chart.png`,
  `reporting-site/qa/showcase-psdq-public-source-confirmation-mobile.png`, and
  `reporting-site/qa/showcase-psdq-public-source-confirmation-mobile-list.png`.
  Next PSDQ loop is continuing public-source/manual confirmation beyond the
  first 12 rows.
- **2026-06-19 (PSDQ targeted public-map inspection):** Added
  `public-service-data-quality/scripts/inspect-bgd-facility-public-map-targets.py`,
  generated
  `psdq-bgd-facility-validation-public-map-inspection.csv` and
  `psdq-bgd-facility-validation-public-map-inspection-summary.json`, and wrote
  `public-service-data-quality/facility-validation-public-map-inspection.md`.
  The no-network pass reads the row-evidence ledger plus pinned
  all-Bangladesh OSM/Overpass and public boundary caches. It inspects all 40
  open public-map-gap rows, covers all 30 priority-1 rows, creates a 10-row
  named-upazila start queue and an 18-row zero-OSM upazila queue, records 22
  same-upazila candidate public-map links and 6 specific-name signals, and
  keeps all 40 rows open with 0 AI closures and 0 AI reclassifications. This
  is targeted public-map inspection, not human validation, a maturity
  promotion, or a human-final upgrade. Verification passed: inspection script
  rerun, new script `py_compile`, program-script `py_compile`, production site
  build, six deterministic gates plus `git diff --check`, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-map-inspection-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-map-inspection-mobile.png`, and
  `reporting-site/qa/showcase-psdq-public-map-inspection-mobile-queue.png`.
  This queue is now followed by the first-row public-source confirmation note
  above.
- **2026-06-19 (PSDQ public-map-gap row evidence):** Added
  `public-service-data-quality/scripts/build-bgd-facility-public-map-gap-row-evidence.py`,
  generated `psdq-bgd-facility-validation-public-map-gap-evidence.csv` and
  `psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`, and
  wrote
  `public-service-data-quality/facility-validation-public-map-gap-evidence.md`.
  The no-network pass reads the public-map-gap triage CSV/summary and gives all
  40 open rows a DGHS source note, public profile URL, OSM coordinate-inspection
  URL, OSM feature or absence note, and keep-open reviewer action. It covers
  all 30 priority-1 high-exposure rows. Evidence tiers: 4 source-repair-first
  rows, 3 possible match or buffer-review rows, 15 row-level public-map
  absence-review rows, and 18 upazila-level public-map observability rows. All
  40 rows remain open. This is row-level public-source evidence, not human
  validation, a maturity promotion, or a human-final upgrade. Verification
  passed: row-evidence script rerun, program-script `py_compile`, production
  site build, six deterministic gates, `git diff --check`, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. The mobile row-evidence chart now renders as a
  compact upazila list instead of a cropped wide SVG. Screenshots:
  `reporting-site/qa/showcase-psdq-row-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-row-evidence-mobile.png`, and
  `reporting-site/qa/showcase-psdq-row-evidence-mobile-chart.png`. This queue
  is now followed by the targeted public-map inspection note above.
- **2026-06-19 (PSDQ public-map-gap triage):** Added
  `public-service-data-quality/scripts/triage-bgd-facility-public-map-gaps.py`,
  generated `psdq-bgd-facility-validation-public-map-gap.csv` and
  `psdq-bgd-facility-validation-public-map-gap-summary.json`, and wrote
  `public-service-data-quality/facility-validation-public-map-gap.md`. The
  no-network triage reads the AI review ledger, coded-screen CSV,
  coordinate-repair CSV, exposure-ranked table, OSM upazila table, cached
  all-Bangladesh OSM health features, and cached DGHS public DataTables rows.
  It keeps all 40 public-map-gap rows open: 30 priority-1 high-exposure rows,
  18 zero-OSM expected-upazila rows, 2 reused valid-coordinate rows, 2 far
  same-upazila name-signal rows, 1 same-upazila name signal outside 500
  meters, 2 buffer-sensitive 500m-to-1km rows, 3
  OSM-present-not-at-facility rows, and 12
  no-same-upazila-OSM-signal-within-3km rows. The showcase route
  `/showcase/psdq-source-disagreement` now fetches the public-map-gap summary
  JSON, shows the public-map-gap panel and upazila queue, and links the new
  note/downloads. README, REPRODUCE, hook bank, quality audit,
  sync/review-packet inclusion, source-disagreement L3 note, showcase
  registry, and per-program status were updated. This is public-source triage,
  not human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script rerun, new script `py_compile`,
  program-script `py_compile`, production site build, six deterministic gates,
  and agent-browser desktop/mobile QA at 1365px and 375px with no page-level
  horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-map-gap-desktop.png` and
  `reporting-site/qa/showcase-psdq-public-map-gap-mobile.png`. Next PSDQ loop
  is row-level public DGHS/OSM/source evidence for the highest-exposure open
  public-map-gap rows.
- **2026-06-19 (PSDQ coordinate-repair triage):** Added
  `public-service-data-quality/scripts/triage-bgd-facility-coordinate-repairs.py`,
  generated `psdq-bgd-facility-validation-coordinate-repair.csv` and
  `psdq-bgd-facility-validation-coordinate-repair-summary.json`, and wrote
  `public-service-data-quality/facility-validation-coordinate-repair.md`. The
  no-network triage reads the AI review ledger, coded-screen CSV, public
  geoBoundaries ADM3, cached all-Bangladesh OSM health features, and cached
  DGHS public DataTables rows. It keeps all 23 coordinate-repair rows open:
  7 missing coordinates, 2 reused sampled coordinates, 6 other-ADM3
  coordinates near an OSM health feature, 5 other-ADM3 coordinates without a
  nearby OSM health feature, and 3 outside the public ADM3 polygons used here.
  Sixteen usable suspect coordinates fall outside the expected sampled upazila;
  4 are at least 50 kilometers away and the largest measured distance is 351.4
  kilometers. The showcase route `/showcase/psdq-source-disagreement` now
  fetches the coordinate-repair summary JSON, shows a coordinate-repair panel
  and distance ledger, and links the new note/downloads. README, REPRODUCE,
  hook bank, quality audit, sync/review-packet inclusion, source-disagreement
  L3 note, showcase registry, and per-program status were updated. This is
  source-repair triage, not human validation, a maturity promotion, or a
  human-final upgrade. Verification passed: new script `py_compile`,
  production site build, six deterministic gates, and agent-browser
  desktop/mobile QA at 1365px and 375px with no page-level horizontal overflow
  and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coordinate-repair-desktop.png` and
  `reporting-site/qa/showcase-psdq-coordinate-repair-mobile.png`. This queue
  is now superseded by the public-map-gap triage in the operational note above.
- **2026-06-19 (PSDQ candidate public-source tag scan):** Added
  `public-service-data-quality/scripts/check-bgd-facility-candidate-public-sources.py`,
  generated `psdq-bgd-facility-validation-candidate-public-source-check.csv`
  and
  `psdq-bgd-facility-validation-candidate-public-source-check-summary.json`,
  and wrote
  `public-service-data-quality/facility-validation-candidate-public-source-check.md`.
  The scan reads the candidate-resolution CSV, OSM-candidates CSV, pinned
  all-Bangladesh OSM tags, and cached DGHS public DataTables rows. It keeps
  all 8 candidate rows open while separating them into 2 strong same-site OSM
  tag-support rows, 2 same-site type/label conflicts, 2 name-support rows with
  coordinate/function conflicts, and 2 nearby-feature rows without registry-name
  support. The showcase route `/showcase/psdq-source-disagreement` now fetches
  the source-check summary JSON, shows a public-source tag-support panel/chart,
  and links the new note and downloads. README, REPRODUCE, hook bank, quality
  audit, sync/review-packet inclusion, source-disagreement L3 note, and
  per-program status were updated. This is AI public-source evidence scanning,
  not human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, and agent-browser desktop/mobile QA at
  1365px and 375px with no page-level horizontal overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-check-desktop.png` and
  `reporting-site/qa/showcase-psdq-public-source-check-mobile.png`. This
  source-check queue is now followed by the coordinate-repair and
  public-map-gap triage notes above.
- **2026-06-19 (PSDQ candidate-resolution pass):** Added
  `public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py`,
  generated `psdq-bgd-facility-validation-candidate-resolution.csv` and
  `psdq-bgd-facility-validation-candidate-resolution-summary.json`, and wrote
  `public-service-data-quality/facility-validation-candidate-resolution.md`.
  The pass reads the AI review ledger, OSM-candidates CSV, and AI review
  summary, keeps all 8 candidate-resolution rows open, and separates them into
  1 probable alias/campus lane, 2 same-site classification-conflict lanes, 2
  possible aliases, 1 local-script name gap, 1 ambiguous nearby candidate, and
  1 weak nearby OSM signal. The showcase route
  `/showcase/psdq-source-disagreement` now fetches the candidate-resolution
  summary JSON, shows the lane grid/chart, and links the new note and
  downloads. README, REPRODUCE, hook bank, quality audit,
  sync/review-packet inclusion, source-disagreement L3 note, and per-program
  status were updated. This is AI public-source candidate resolution, not
  human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, review-packet rebuild, and agent-browser
  desktop/mobile QA at 1365px and 375px with no page-level horizontal overflow
  and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-candidate-resolution-desktop.png` and
  `reporting-site/qa/showcase-psdq-candidate-resolution-mobile.png`. Rebuilt
  `review-packets/public-service-data-quality-2026-06-18/` plus zip. This
  candidate-resolution queue is now superseded by the richer public-source tag
  scan in the operational note above.
- **2026-06-19 (PSDQ AI public-source review ledger):** Added
  `public-service-data-quality/scripts/review-bgd-facility-validation-flags.py`,
  generated `psdq-bgd-facility-validation-ai-review.csv` and
  `psdq-bgd-facility-validation-ai-review-summary.json`, and wrote
  `public-service-data-quality/facility-validation-ai-review.md`. The ledger
  keeps all 71 flagged sampled DGHS rows open while separating the queue into
  40 public-map-gap checks, 23 coordinate-source repairs, 6 name/type
  resolution rows, and 2 nearby-OSM-without-registry-match rows. The showcase
  route `/showcase/psdq-source-disagreement` now fetches the AI review summary
  JSON, shows an AI public-source review workstream panel/chart, and links the
  new note and downloads. README, REPRODUCE, hook bank, quality audit,
  sync/review-packet inclusion, and per-program status were updated. Rebuilt
  `review-packets/public-service-data-quality-2026-06-18/` plus zip.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, and agent-browser desktop/mobile QA
  with no page-level horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-ai-review-desktop.png` and
  `reporting-site/qa/showcase-psdq-ai-review-mobile.png`. This is AI
  public-source row review, not human validation, a maturity promotion, or a
  human-final upgrade. This queue is now superseded by the candidate-resolution
  pass; next PSDQ loop is public-source confirmation inside those lanes.
- **2026-06-19 (PSDQ automated facility-validation coded screen):** Added
  `public-service-data-quality/scripts/code-bgd-facility-validation-sample.py`,
  generated the coded-screen CSV, OSM-candidates CSV, and coded-summary JSON,
  and wrote `public-service-data-quality/facility-validation-coded-screen.md`.
  The automated screen uses the cached all-Bangladesh OSM health-feature pull
  and geoBoundaries ADM3 to classify the 76 sampled DGHS rows: 40 missing
  public-map points, 23 registry coordinate issues, 5 confirmed same-facility
  matches, 3 probable aliases, 3 classification mismatches, and 2 OSM-only
  candidates. The showcase route `/showcase/psdq-source-disagreement` now
  fetches the coded-summary JSON, shows a grouped coded-screen chart, and
  links the coded-screen downloads. README, REPRODUCE, hook bank, quality
  audit, sync/review-packet inclusion, and per-program status were updated.
  Browser QA passed at 1365px desktop and 375px mobile with no page-level
  horizontal overflow or page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coded-screen-desktop.png` and
  `reporting-site/qa/showcase-psdq-coded-screen-mobile.png`. This is
  automated public-source triage, not manual validation, a maturity promotion,
  or human-final upgrade. The follow-on AI public-source review ledger was
  completed in the next operational note.
- **2026-06-19 (PSDQ facility-validation sample design):** Added
  `public-service-data-quality/scripts/design-bgd-facility-validation-sample.py`,
  generated the Bangladesh validation-sample JSON, sampled-upazila CSV,
  sampled-facility CSV, and blank coding sheet, and wrote
  `public-service-data-quality/facility-validation-sample.md`. The design
  covers 20 upazilas and 76 DGHS facility rows, with 69 coordinate-ready rows.
  The showcase route `/showcase/psdq-source-disagreement` now fetches the
  sample JSON, shows a validation-sample panel, and links the blank coding
  sheet. README, REPRODUCE, hook bank, quality audit, sync/review-packet
  inclusion, and per-program status were updated. Verification passed:
  validation-sample script and `py_compile`, `npm run build`, six gates, and
  agent-browser desktop/mobile QA with no page-level horizontal overflow or
  page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-validation-sample-desktop.png` and
  `reporting-site/qa/showcase-psdq-validation-sample-mobile.png`. This is a
  sample design, not validation outcomes, a maturity promotion, or human-final
  upgrade. The follow-on automated coded screen was completed in the next
  operational note.
- **2026-06-19 (PSDQ source-disagreement L3 module):** Added
  `public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py`,
  generated `psdq-bgd-source-disagreement-strata.{json,csv}`, and wrote
  `public-service-data-quality/source-disagreement-l3-module.md`. The
  showcase route `/showcase/psdq-source-disagreement` now reads the L3 strata
  JSON, shows ratio buckets and validation residues before the interactive
  workbench, and links the L3 note plus strata downloads. Registry copy,
  hook bank, sync/review-packet inclusion, README, REPRODUCE, and
  per-program status were updated. Rebuilt
  `review-packets/public-service-data-quality-2026-06-18/` plus zip
  (UTC-dated by script). Verification passed: strata script, `npm run build`,
  six gates, and agent-browser desktop/mobile QA with no page-level horizontal
  overflow or page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-l3-desktop.png` and
  `reporting-site/qa/showcase-psdq-l3-mobile.png`. This is an L3 evidence
  module for report #4, not a maturity promotion or human-final upgrade. The
  follow-on validation-sample design was completed in the next operational
  note.
- **2026-06-19 (rotation to PSDQ source-disagreement deepening):** After
  commit `225d4d2` closed the remittance L3 flow-weighting repair, the active
  flagship rotated to `public-service-data-quality` because
  `research/showcase-quality-audit.md` now lists PSDQ source disagreement as
  the next L3 candidate. The work is a focused evidence/public-surface
  deepening of the existing PR program, not a maturity promotion.
- **2026-06-17 (remittance flow-weighting L3 re-close):** Current active
  flagship repair was formalized instead of leaving the showcase report as an
  L2 sprint. Added `remittance-resilience/flow-weighting-l3-module.md` and
  `pre-registration.md` §12 with a 90% corridor-match gate, interpretation
  rule, non-claims, and no maturity promotion. Updated the flow-weighting
  script/generated JSON to `goal_level: L3 sensitivity module`, recording the
  repaired program baseline order (`KGZ`, `WSM`, `TON`, `NPL`, `VUT`), the
  matched-corridor quote order (`KGZ`, `WSM`, `TON`, `VUT`, `NPL`), and the
  flow-weighted order (`KGZ`, `NPL`, `VUT`, `WSM`, `TON`) after matching
  140/142 latest-period RPW corridors to public KNOMAD bilateral-flow
  estimates. Updated results, sensitivity, coverage, limitations, review
  addenda, article, showcase registry, and route copy; rebuilt
  `review-packets/remittance-resilience-2026-06-18/` plus zip. This is an L3
  repair/governance improvement for report #5, not publication-ready or
  human-final status. Closeout verification completed 2026-06-19: production
  site build passed, six gates passed, targeted post-sync contradiction search
  found only historical correction notes, and Chrome/CDP QA on
  `/showcase/remittance-flow-weighting` passed at 1365px and 375px with no
  page-level horizontal overflow. Screenshots:
  `reporting-site/qa/showcase-remittance-l3-desktop.png` and
  `reporting-site/qa/showcase-remittance-l3-mobile.png`.
- **2026-06-17 (showcase readiness ladder):** Added explicit report-readiness
  metadata for all 20 showcase reports in
  `reporting-site/src/data/showcaseReports.ts`: L2 prototype, L3 candidate,
  evidence audit, and owner-gated. The homepage now separates
  screenshot-checked routes from the five L3 candidates, adds one stage chip
  per report card, and shows the next upgrade alongside the visual,
  operational use, falsifier, evidence path, and source stack. `/showcase`
  and dynamic audit route queues now display both surface status and readiness
  stage. New portfolio audit artifact:
  `research/showcase-quality-audit.md`, with stage definitions, current
  distribution, report-by-report publication gaps, and the next deepening
  order. Browser QA saved `home-readiness-desktop.png`,
  `home-readiness-mobile.png`, `showcase-queue-readiness-desktop.png`,
  `showcase-queue-readiness-mobile.png`, and
  `showcase-20-readiness-mobile.png`; checks confirmed 20 home cards, 120
  home fact rows, 20 stage chips, 20 queue rows, readiness labels visible,
  expected audit stats on report #20, and zero page-level horizontal overflow
  at desktop and mobile widths. This is a readiness-governance improvement,
  not a maturity promotion. Follow-up implementation audit found that the
  readiness ladder was global on the homepage and queue, and complete on
  dynamic audit pages 9-20, but not yet visible inside the older static report
  pages 1-8. Added `ShowcaseQualityPanel` and wired it into all eight static
  routes so every report surface now shows current QA stage, operational use,
  falsifier, publication gap, next upgrade, evidence path, and source stack.
  Focused mobile browser QA on `/showcase/remittance-flow-weighting` confirmed
  the shared panel, next-upgrade text, and zero horizontal overflow; build and
  source audit cover the remaining static routes. Screenshot saved:
  `showcase-remittance-readiness-panel-mobile.png`.
- **2026-06-17 (showcase depth-standard pass):** Added bench-level
  `operationalUse`, `falsifier`, and `limitation` metadata for all 20
  showcase reports in `reporting-site/src/data/showcaseReports.ts`. The
  homepage now shows five report-depth rows per card: visual, operational
  use, falsifier, evidence path, and source stack. The dynamic artifact-audit
  route adds operational use and falsifier readouts and carries the limitation
  into the caveat list. Focused browser QA saved
  `home-depth-desktop.png`, `home-depth-mobile.png`, and
  `showcase-20-school-depth-mobile.png`; checks confirmed 20 cards, 100 home
  fact rows, expected audit stats, and zero horizontal overflow at 1440px and
  375px. `npm run build` passed, and the six gates
  (`check-citations`, `check-composite-headline`, `check-wip`,
  `check-dmc-framing`, `check-banned-words`, `check-versions`) passed. This
  improves report-depth coverage but does not close the full showcase goal:
  selected reports still need L3 evidence strengthening and more bespoke
  narrative/visual polishing before publication-ready status.
- **2026-06-17 (20-report showcase batch completed):** Owner directed the
  showcase loop not to stop at reports 9-12, so the report bench was expanded
  to 20 public-data surfaces. `reporting-site/src/data/showcaseReports.ts`
  now registers all 20 reports; reports 9-20 use a new artifact-driven
  route, `reporting-site/src/pages/ShowcaseEvidenceAudit.tsx`, mounted at
  `/showcase/:reportSlug`. The new report set covers grid generation
  concentration, migration denominator switching, MPI/night-light blind
  spots, coastal population-denominator effects, flood index decomposition,
  climate-health cap saturation, food-price coverage traps, social-protection
  dropped legs, water-stress denominator artifacts, invisible-urbanization
  tautology, port inert parameters, and school-heat sensitivity auditing.
  Each new route fetches only its committed public JSON artifact from
  `reporting-site/public/programs/.../generated/` and renders an audit-specific
  visual type: rank bridge, blind/visible stack, coverage funnel, sensitivity
  lane, parameter wall, tautology lane, or component card. Homepage and
  `/showcase` copy now read from the shared registry and present the full
  20-report queue. QA saved desktop and mobile screenshots for home plus all
  new report routes under `reporting-site/qa/` using the `*-20.png` suffix.
  CDP checks confirmed 20 home report cards; for every route 9-20, 3 hero
  stats, expected visual rows, 20 queue rows, no JSON load errors, and no
  page-level horizontal overflow at desktop. A mobile queue auto-placement
  overflow was caught and fixed; the mobile rerun confirmed width `375/375`
  and overflow count 0 for home and all report routes 9-20. `npm run build`
  passed after the fix. These 20 surfaces are still showcase/evidence-audit
  outputs, not maturity-label promotions or publication-ready claims. Next
  loop should critique which 2-3 reports deserve L3 strengthening first,
  rather than adding a 21st surface by default.
- **2026-06-17 (front-page report bench + disaster metric-falsification
  showcase):** Homepage refactored from the older topic-thumbnail gallery
  into a report-first ADB/ERDI showcase bench. New shared report registry
  `reporting-site/src/data/showcaseReports.ts` drives both `/` and the
  `/showcase` queue so the 10-20 report goal does not drift across pages.
  The first viewport now shows the active report queue and target state; the
  older 18-program hero gallery remains below as the evidence archive rather
  than the lead surface. Eighth showcase prototype added and verified at
  `/showcase/disaster-metric-falsification`, reading
  `disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.{json,csv}`.
  Generated evidence shows 1,767 EM-DAT rows in the 2000-2025 DMC filter; the
  pre-registered top-two kill condition fires for 3 of 5 metrics. Original
  CHN+IND holds for affected and damage, but changes to CHN+IDN for
  events/year, IDN+MMR for deaths, and TUV+MHL for events per million. The
  report now uses a mobile-native ranked bar list so narrow viewports do not
  crop chart values. Browser QA saved final home screenshots
  `home-report-refactor-desktop-final.png` and
  `home-report-refactor-mobile-final.png`, plus disaster screenshots
  `showcase-disaster-desktop-verified.png`,
  `showcase-disaster-mobile-verified.png`, and
  `showcase-disaster-mobile-chart-final.png` under `reporting-site/qa/`.
  Checks confirmed 8 report cards, 18 program cards, expected disaster hero
  stats `3/5` and `1,767`, five mobile metric bars, no page-level horizontal
  overflow at 375px, and no browser errors beyond known Vite/React Router
  development warnings. `npm run build`, the five gates, and
  `check-versions` passed. This counts as the eighth verified showcase
  prototype and a publication-surface refactor, not a maturity promotion. The
  next-loop guidance in this note is superseded by the 20-report batch note
  above; current next work is critique and L3 strengthening before adding more
  surfaces.
- **2026-06-16 (access map-completeness showcase prototype):** Seventh
  ADB/ERDI showcase report prototype added at
  `/showcase/access-map-completeness`, reading
  `access-services/generated/access-osm-completeness-deepening.json`,
  `access-services/generated/access-osm-completeness-deepening-phl.csv`, and
  `access-services/generated/access-services-adb-panel.json`. The
  access-services deepening script was rerun on 2026-06-16 and confirms the
  identity check that PSDQ's ARMM population divided by OSM health points
  reproduces the access panel's ARMM people-per-facility value exactly. For
  the Philippines, 16 of 17 ADM1 regions change rank once the denominator
  switches from OSM health points to the official clinical registry; ARMM
  moves from 68,678 people per OSM facility to 4,427 people per registry
  facility, while NCR becomes the highest registry-denominator load. The
  Philippine rank correlation between OSM capture and OSM people-per-facility
  is -0.8105; the log-log R2 is 0.5372. Bangladesh shows the same sign more
  weakly in the available 8-division check. The showcase surface uses a
  desktop rank-flip chart, a completeness scatter with fitted log-log guide,
  a correction-wall chart for the 8-economy cluster, and a mobile-specific
  rank-shift summary after screenshot QA showed the full slope chart cropped
  too much on a narrow viewport. Browser QA saved desktop/mobile first-view
  and evidence-view screenshots under `reporting-site/qa/`; checks confirmed
  expected title, `16/17` and `-0.81` hero stats, 17 rank lines, 34 rank dots,
  17 scatter points, one fitted line, 8 correction-wall bars, 2 corrected
  dots, active mode toggles, no page-level horizontal overflow, and no fresh
  browser errors beyond existing Vite/React Router development warnings.
  `npm run build`, the five gates, and `check-versions` passed before status
  handoff. This counts as the seventh verified showcase prototype, not a
  maturity promotion. The next `access-services` loop is official-registry
  expansion for PAK/KHM/LAO/NPL/LKA/TLS and a public travel-time/friction
  denominator before any access-ranking claim.
- **2026-06-16 (air-monitoring observability showcase prototype):** Sixth
  ADB/ERDI showcase report prototype added at
  `/showcase/air-monitoring-observability`, reading
  `air-monitoring/generated/air-monitoring-concentration-deepening.json` and
  `air-monitoring/generated/air-monitoring-adb-panel.json`. The deepening
  script now fetches/caches public World Bank WDI GDP per capita and replaces
  the earlier false "network blocked" wall with a descriptive GDP-adjusted
  monitor-density check. Current generated evidence shows 13 ADB-region
  economies above the WHO PM2.5 guideline with no visible public PM2.5 monitor
  in the OpenAQ panel; 83.5% of that zero-monitor population is in Papua New
  Guinea and Timor-Leste. The GDP partial frame covers 33 monitored economies,
  with Azerbaijan, Indonesia, Sri Lanka, Myanmar, and Bangladesh showing the
  largest positive monitor-density residuals relative to GDP per capita.
  Browser QA saved desktop and mobile first-view/evidence-view screenshots
  under `reporting-site/qa/`; checks confirmed the expected title, 13
  zero-monitor bars, 33 residual points, 46 exposure-panel points, active mode
  toggles, one fitted GDP line, no browser errors, no page-level horizontal
  overflow, and mobile SVG sizing repaired after visual inspection. `npm run build`,
  the five gates, and `check-versions` passed. This counts as the
  sixth verified showcase prototype, not a maturity promotion. The next
  `air-monitoring` loop should move from national observability screening to
  station catchments with gridded population/PM2.5 and regulatory-inventory
  validation before any stronger monitoring-gap claim.
- **2026-06-16 (remittance flow-weighting showcase prototype):** Fifth
  ADB/ERDI showcase report prototype added at
  `/showcase/remittance-flow-weighting`, reading
  `remittance-resilience/generated/remittance-flow-weighting-sprint.{json,csv}`,
  `remittance-resilience/generated/remittance-median-deepening.{json,csv}`,
  and `remittance-resilience/sensitivity-runs.json`. The remittance repair
  pass fixed the RPW cost-normalization defect, regenerated the main panel,
  sensitivity runs, median-cost deepening, fragility chart, thumbnail, and
  synced site evidence. The repaired baseline top five are `KGZ`, `WSM`,
  `TON`, `NPL`, `VUT`; the common full-suite sensitivity core is `KGZ`,
  `TON`, `VUT`, `WSM`; the maximum top-five entry change is 1 because `PAK`
  replaces `NPL` when the dependence cap is halved. The flow-weighting sprint
  matches 140 of 142 latest-period ADB-DMC-bound RPW corridors to public
  World Bank/KNOMAD 2021 bilateral-flow estimates; flow weighting keeps the
  same five-economy set but changes order to `KGZ`, `NPL`, `VUT`, `WSM`,
  `TON`, with low matched-flow coverage flagged for `KGZ`, `TJK`, `ARM`, and
  `AFG`. Browser QA saved desktop/mobile first-view and evidence-view
  screenshots under `reporting-site/qa/`; checks confirmed the expected
  title, 22 scatter points, 13 side-panel bars, 40 sensitivity cells, working
  mode toggles, no error overlay, no page-level horizontal overflow, mobile
  chart overflow contained inside chart scrollers, and no browser errors
  beyond existing Vite/React Router development warnings. `npm run build`,
  the five gates, and `check-versions` passed. This counts as the fifth
  verified showcase prototype, not a maturity promotion. The active
  remittance program still needs a formal flow-weighting L3 decision and
  rebuilt review packet before it can be re-closed as finished for the
  current issue.
- **2026-06-16 (PSDQ showcase visual uplift):** Fourth ADB/ERDI showcase
  prototype added at `/showcase/psdq-source-disagreement`, reading committed
  PSDQ artifacts
  `public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.{csv,json}`
  and `public-service-data-quality-summary.json`. The first viewport frames
  the non-generic question "When the Map and Registry Disagree" and shows DGHS
  clinical-registry counts versus OSM health features for the top exposure
  rows. The interactive evidence view is a registry-vs-OSM disagreement
  workbench: 16 ranked upazila rows, an OSM-visible registry-share strip,
  DGHS/OSM counts, an Open Buildings 3 km p85 under-observed-building proxy,
  division filter, focus selector, and metric toggle for exposure proxy, gap
  share, and lowest OSM/registry ratio. Browser QA saved
  `showcase-psdq-desktop.png`, `showcase-psdq-desktop-visual.png`,
  `showcase-psdq-mobile.png`, and `showcase-psdq-mobile-visual.png` under
  `reporting-site/qa/`; checks confirmed the expected title, 16 SVG rows,
  sprint-derived hero stats, working metric toggle, no page-level horizontal
  overflow, mobile chart overflow contained inside the chart scroller, and
  zero page errors. Console output contained only existing Vite/React Router
  development warnings. This is a source-QA visual uplift for a finished PSDQ
  issue, not a facility-access claim, service-quality claim, ground-truth
  judgment, or maturity promotion. Next showcase loop should either repair
  remittance flow-weighting for a showcase-safe corridor report or start the
  next evidence-first topic sprint from `research/hook-bank.md`.
- **2026-06-16 (shock-payment showcase prototype):** Third ADB/ERDI
  showcase prototype added at `/showcase/shock-payment-rails`, reading the
  synced shock-payment rails sprint JSON and rendering an evidence-led report
  on disaster exposure versus observable payment-use rails. The first viewport
  now shows account ownership versus electronic payment use for high-exposure
  rows, rather than a generic dashboard card. The interactive evidence view
  renders a disaster-frequency by electronic-payment-use scatter with 26
  plotted rows plus a concept-gap bar panel for account-minus-payment-use and
  ASPIRE-coverage-minus-government-payment-account-use gaps. Browser QA saved
  screenshots under `reporting-site/qa/` for desktop/mobile first view and
  desktop/mobile visual view; checks confirmed the expected title, one scatter,
  one gap chart, 26 plotted points, 12 bars, sprint-derived hero stats, working
  gap toggle and economy selector, no framework overlay, no page-level
  horizontal overflow, mobile chart overflow contained inside chart scrollers,
  and zero page errors. Console output contained only existing Vite/React
  Router development warnings. This is still a prototype report and program
  prospectus candidate, not a readiness index, public claim, or maturity
  promotion. Next showcase loop is remittance parser/flow-weight repair before
  a showcase-safe remittance report, or PSDQ source-disagreement visual uplift.
- **2026-06-16 (data-freshness showcase prototype):** Second ADB/ERDI
  showcase prototype added at `/showcase/data-freshness`, reading the synced
  WDI data-freshness sprint JSON and rendering an interactive 42-DMC by
  9-indicator source-vintage matrix from the generated artifact. The report
  frame follows the ADB/ERDI pattern: planning problem, hidden data-vintage
  gap, World Bank WDI source upgrade, plain-English relative-lag method,
  visual result, non-claim box, operational use, and reproduce links. Browser
  QA saved screenshots under `reporting-site/qa/` for desktop/mobile first
  view and desktop/mobile matrix view; checks confirmed the expected title,
  one matrix with 378 cells, sprint-derived hero stats, focus-control update,
  no framework overlay, no page-level horizontal overflow, mobile matrix
  overflow contained inside the chart scroller, and zero page errors. Console
  output contained only existing Vite/React Router development warnings. This
  is still a prototype report and program prospectus candidate, not a public
  claim or maturity promotion. Next showcase loop is either shock-payment
  rails report design or L3 packaging of one of the two prototypes.
- **2026-06-16 (ADB/ERDI showcase goal opened):** Owner started a new
  persistent goal to build a 10-20 report ADB/ERDI-aligned research showcase,
  with emotionally compelling but institutionally credible evidence surfaces.
  This explicitly broadens the session from remittance-only repair to a
  goal-directed showcase batch while preserving honest maturity labels.
  `research/factory.md` now has a "Showcase report loop" requiring evidence
  first, ADB/ERDI narrative shape, interactivity only when it clarifies
  evidence, screenshot QA, and no maturity promotion from visual polish alone.
  `research/hook-bank.md` now has an ADB/ERDI showcase queue for the first
  five candidates. First prototype surface added at `/showcase` in
  `reporting-site/`, reading the synced Nepal market-climate sprint JSON and
  rendering a native interactive market-month heatmap. New sync script
  `scripts/sync-topic-sprints.mjs` publishes topic-sprint generated files and
  sprint notes into `reporting-site/public/topic-sprints/`. Browser QA saved
  screenshots under `reporting-site/qa/` and checked desktop/mobile render,
  heatmap render, no framework overlay, no page-level horizontal overflow, and
  working animation control. This is a showcase prototype, not a public claim
  or maturity promotion; next loop is L3 packaging for the Nepal report or
  design of the next showcase surface.
- **2026-06-16 (market-climate new-topic sprint):** Third new-topic L2
  sprint completed under `research/topic-sprints/`. New script
  `research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py`
  fetches WFP Nepal food-price and market CSV resources from HDX, pulls NASA
  POWER monthly point data at selected market coordinates, and writes
  `research/topic-sprints/generated/nepal-market-climate-prices-sprint.csv`,
  `research/topic-sprints/generated/nepal-market-climate-prices-sprint.json`,
  and a visually checked aligned heatmap at
  `research/topic-sprints/generated/charts/nepal-market-climate-prices-heatmap.png`.
  The generated artifact records 2,011 retained WFP rice price rows, 36
  markets before selection, 12 selected markets, 1,008 market-month cells,
  937 rows with both price anomaly and lagged precipitation anomaly, and 26
  dry-price-spike screen cells. Decision: promote "market-level climate price
  transmission" to a program prospectus candidate, not to a causal climate
  claim. This closes the current top-three new-topic L2 sprint batch; next
  action is to choose one promoted prospectus for L3 program packaging or
  start a new L1 shortlist batch.
- **2026-06-16 (shock-payment new-topic sprint):** Second new-topic L2
  sprint completed under `research/topic-sprints/`. New script
  `research/topic-sprints/scripts/sprint-shock-payment-rails.py` joins the
  existing ASPIRE/Findex/WDI social-protection panel, the EM-DAT/HDX disaster
  exposure panel, and fresh World Bank API payment-use indicators. It writes
  `research/topic-sprints/generated/shock-payment-rails-sprint.csv`,
  `research/topic-sprints/generated/shock-payment-rails-sprint.json`, and a
  visually checked two-panel chart at
  `research/topic-sprints/generated/charts/shock-payment-rails-scatter.png`.
  The generated artifact records 42 DMC rows, 38 rows with disaster-event
  frequency, 27 rows with digital-payment-use data, 21 rows with
  government-payment account-use data, and 26 plotted rows. Decision: promote
  "shock-payment rails after disasters" to a program prospectus candidate,
  not to a public claim or readiness index. The next strongest new-topic
  sprint was market-level climate price transmission.
- **2026-06-16 (new-topic creation loop):** Owner clarified that `/goal
  research` means refactoring topic creation and generating stronger **new**
  data-first research topics, not only repairing remittance or other existing
  programs. `research/factory.md` now has a "New-topic creation mode" that
  separates repair hooks from new topics and stores exploratory scripts under
  `research/topic-sprints/` until a hook earns a full program package.
  `research/hook-bank.md` now has a separate new-topic shortlist with public
  datasets, first visuals, non-generic questions, source caveats, AI roles,
  kill/defer conditions, and a new-topic L2 sprint queue. First new-topic L2
  sprint completed: `research/topic-sprints/scripts/sprint-wdi-data-freshness.py`
  pulls selected World Bank WDI series, writes a 42 DMC by 9 indicator
  freshness matrix, and renders
  `research/topic-sprints/generated/charts/wdi-data-freshness-heatmap.png`.
  The generated artifact records 378 cells, 19 missing cells, and 13 cells
  three or more years behind the indicator's own latest public reference
  year. Visual QA and source sanity are recorded in
  `research/topic-sprints/wdi-data-freshness-sprint.md`. Decision: promote
  "public data freshness blind spots" to a program prospectus candidate, not
  to a public claim or maturity label. The goal remains active because more
  top new-topic candidates still need L2 sprints.
- **2026-06-16 (later):** `/goal research` completed its first L1 -> L2
  loop. `research/hook-bank.md` is now a ranked data-first hook bank with 15
  candidates, subjective triage scores, public data objects, first-visual
  plans, non-generic questions, AI roles, and kill/defer conditions. Top
  three L2 candidates are remittance flow weighting, PSDQ district/catchment
  validation, and a road-quality/access pilot. The first L2 sprint was run on
  remittance flow weighting:
  `remittance-resilience/scripts/sprint-flow-weighted-cost.py` joined RPW Q1
  2025 corridor prices to the World Bank/KNOMAD 2021 bilateral remittance
  matrix and WDI remittance-dependence values, wrote CSV/JSON plus a PNG/SVG
  rough visual, and recorded visual/source sanity in
  `remittance-resilience/l2-flow-weighting-sprint.md`. Decision: promote the
  hook into the remittance-resilience L3 repair pass, not into a public claim
  or maturity promotion. The active flagship remains `remittance-resilience`;
  next work is parser repair, regenerated evidence, formal flow-weighting
  integration, publication re-sync, gates, build, and browser check.
- **2026-06-16:** `/goal` sharpened from a generic research-factory reminder
  into an operating bar for non-generic flagship work: one evidence spine,
  program-native visuals, visible caveats, traceable artifacts, and a
  concrete current repair bar for `remittance-resilience`. `research/factory.md`
  now starts with a **data-first hook triage** before the standard loop:
  find the public data object, build the rough visual first, ask what it makes
  visible, reverse-design the research frame from that object, and ditch/defer
  weak hooks that only produce generic rankings or topic summaries. A nested
  goal stack now governs `/goal` and `research/factory.md`: L0 lab, L1 research
  discovery, L2 hook sprint, L3 program package, L4 publication surface, L5
  human-final upgrade. The active flagship remains `remittance-resilience`,
  but the next session should not polish the old Mode A ladder as if complete.
  It should start with the
  May 2026 deepening finding: fix the RPW negative-cost normalization defect
  in `process-remittance.py`, regenerate the panel/sensitivity/median-cost
  artifacts and charts, then attempt the public bilateral-flow weighting
  keystone or record the exact data wall. `research/hook-bank.md` added as
  the `/goal research` output: a data-first candidate list ranked by public
  data object, first visual, non-generic question, AI assist, and kill/defer
  condition. `remittance-resilience/STATUS.md` now carries the active
  repair/deepening plan.
- **2026-05-29 (later, deepening pass — all 18):** Owner-directed real
  deepening across the whole portfolio ("aren't we outputting real data,
  charts, narratives, analysis? add that to the goal — full suite on all").
  After the deep-questions pass, each program now also has a `deepen-*.py`
  script, a generated artifact, and a `deepened-results.md` narrative.
  **Binding rule honored:** every number is computed by a committed script
  from data **already on disk** — the program `.cache/` raw public sources
  (the committed fetch scripts had populated them; outbound network is
  blocked this session) and committed `generated/` panels. No AI-supplied
  figures; owner-gated/uncached keystones are named as walls, not faked.
  Real findings (each traces to its artifact): **grid** — fuel concentration
  is *higher* on generation than capacity (TJK 0.80→1.00; idle thermal
  backup), the screen had the right worry and wrong variable; **migration**
  — re-ranking by share-of-population collapses the entire absolute top-5
  (CHN #2→#39), it was a population ranking; **disaster** — the
  pre-registered kill-condition *fires*: by deaths the top-2 is IDN+MMR, IND
  falls #2→#4; **social-protection** — VUT/TJK enter the top-5 and PHL/BGD
  drop once dropped legs are imputed (completeness artifact);
  **port-hinterland** — the imports-cap parameter is inert (max proxy 1.11 vs
  2.0), half the ±50% pass is hollow; **food-price** — "LAO+PAK stable" is a
  coverage artifact and the import axis is raw materials not food;
  **remittance** — the cluster *survives* a robust median cost (good news),
  but a real normalization bug in `process-remittance.py` (`raw*100 if
  raw<=1`) manufactures the −305% quotes; **access** — the access ranking is
  the inverse of OSM mapping completeness (ρ=−0.81); **invisible-urban** —
  the ±50% sweep is a rank-preserving tautology (Spearman 1.0, 0 inversions);
  **school-heat** — "KHM #1 across every perturbation" is false (loses one
  run, one is all-zeros); **coastal** — dropping population reorders the
  top-5; **climate-health** — at the flagged cap the index collapses to an
  outdoor-labor ranking, and "exposed workers" was ×total-pop not labor
  force; **PSDQ** — principal-tier OSM exceeds the registry (Central Luzon
  117%), so the gap is largely the unmapped-BHS denominator; **water-stress**
  — the top-4 saturate the water term, ordered by yield×rural;
  **air-monitoring** — 83.5% of the "14.3M unmonitored" is PNG+Timor-Leste;
  **mpi-nighttime-lights** (owner-led, not advanced) — 28/30 economies hold a
  majority of MPI in health+education, bounding the eventual NTL axis to
  ~14–31%. Named walls (owner action to close): IMF bilateral remittance
  matrix; FAO AQUASTAT TRWR + FAOSTAT crop areas; WDI employment-to-pop and
  HDI/GDP-per-capita level series; DHS/MICS microdata (PSDQ validation);
  GHSL/DEM/surge + GLOFAS/Sentinel-1 rasters (coastal, flood,
  invisible-urban); Earth Engine OAuth + VIIRS Black Marble (MPI); the
  ~2.6 GB Ookla pull (digital-performance — runnable stub committed, refuses
  to invent). Several deepenings produce real grounds to **revise headlines**
  (disaster, school-heat, port, the size/completeness-artifact clusters); the
  subagents correctly did *not* silently rewrite `results.md`/`pre-
  registration.md` — headline retraction and maturity demotion are left for
  owner review. 5 gates pass; active flagship unchanged; no maturity label
  moved.
- **2026-05-29 (later, deep-questions pass):** Owner-directed deep
  research-questions pass across the whole portfolio ("write all the
  remaining research deeply, ask all questions, no holds barred"). Wrote a
  `{program}/deep-questions.md` for all 18 programs (~42k words) plus a
  portfolio synthesis at `research/deep-questions.md`. These are
  AI-generated research **agendas, not findings** — each asks the specific,
  falsifiable, data-grounded questions the screening result never asked
  (sections: falsifiers/keystone, mechanism, decision-grade estimand,
  frontier, the existential question, data-needs table, keystone). The
  synthesis names seven recurring structural patterns: national-unit vs
  sub-national phenomenon; cluster = data-availability; hollow ±50%
  robustness; title-vs-construct gap; no independent-outcome validation; no
  mechanism; size/reporting as signal. Verified cracks worth acting on:
  `port-hinterland-friction`'s imports-cap parameter is inert (never binds
  below ~$10T imports; largest is $3.11T), so its ±50% pass is partly
  hollow; `disaster-recovery-lag`'s pre-registered kill-condition is
  *already met* (by the deaths metric the top-2 is IDN+CHN, not CHN+IND);
  `school-heat-disruption`'s "KHM #1 across every perturbation" is
  contradicted by its own `sensitivity-runs.json` (one run zeros all 32
  economies; KHM is #2 in another); `water-stress` and `flood-market-access`
  indices contain no diversification / no road-market-flood term despite
  their names; `access-services` likely ranks OSM completeness, contradicting
  sibling `public-service-data-quality` on data already in the repo. No
  empirical claims were made or changed; no maturity labels moved.
  Verification: 5 gates pass (banned-words 454 files, dmc-framing 459);
  `npm run build` clean. Suggested next step (owner): pick one program and
  answer its keystone — most are blocked only by reaching for public data
  already named in the file.
- **2026-05-29 (later):** Native-chart rendering layer added
  (owner-requested proof of concept; "beautiful charts natively…
  maps charts etc"). Program heroes can now render as interactive
  in-browser SVG instead of a static matplotlib PNG, reading the SAME
  committed `generated/*.json` a reviewer downloads on the Data tab — so
  the visual is *more* auditable than a raster, not less. Scope:
  - New deterministic basemap builder `scripts/build-webmap.mjs` →
    committed `reporting-site/public/geo/asia-pacific.geojson` (152 KB;
    Asia+Oceania, Pacific-centered at lon0=125, simplified from the
    vendored Natural Earth 50m) + `asia-pacific-centroids.json`. A
    geometry transform of a public-domain source; introduces no numbers.
  - New primitives in `reporting-site/src/lib/charts/` + components in
    `reporting-site/src/components/charts/` (`ChoroplethMap`, `Scatter`,
    `RankedBar`, `ChartFrame`, tooltip, responsive hook). Themed to the
    rebrand's ADB tokens; `attestation_chain` rendered as real text
    (§18.2) rather than burned into pixels.
  - Showcase at `/native-charts` renders the remittance map + scatter +
    ranked bar from `remittance-resilience-adb-panel.json`, with a toggle
    to compare against the current PNG. Cluster derived from the committed
    panel (top-5 by the triage composite — selection only, never
    headlined, §6.4); headline number + TJK exclusion annotation derived
    from data, not hard-coded.
  - `Topic.tsx` shows the native map as the remittance hero in-context;
    every other program still renders its PNG (slug-guarded), and the
    native hero falls back to the PNG while data loads or on any error —
    no regression for the other 15 programs.
  - Verification: `npm run build` clean; browser-checked 1280 desktop +
    375 mobile, zero console errors, zero horizontal overflow (fixed a
    mobile SVG-overflow bug — charts now scale to their container); five
    gates pass. Publication-surface capability, not a per-program
    advancement; active flagship unchanged. Per-program roll-out happens
    as each program reaches publication stage.
- **2026-05-29:** ADB visual-identity rebrand of `reporting-site`
  (owner-requested; "make the styling and feel like ADB"). Refactored
  the design **primitives** only — every page reads from these via
  semantic classes + CSS vars, so the token layer was the single
  leverage point and no per-page rewrite was needed. Ground-truthed the
  palette/type from the live adb.org computed styles (not guessed):
  white surfaces, near-black text `#212529`, ADB web blue `#007DB8` as
  the one signature accent, ADB green `#5A8227` / gold `#FBB00E`
  secondaries, navy `#002569`. Type switched from the editorial serif
  stack (Fraunces + Source Serif 4) to **Source Sans 3** — the closest
  free substitute for ADB's proprietary Ideal Sans — with ADB's exact
  system-ui fallback; JetBrains Mono kept for data/attestation stamps.
  - Token NAMES kept stable (`--crimson` now holds ADB blue, `--sage`
    green, `--ochre` gold) so the re-skin propagated to all ~40 pages
    + `ui.tsx` without a risky rename.
  - Files: `index.html` (fonts, theme-color), `tailwind.config.js`
    (palette + font stacks), `src/index.css` (`:root` tokens, body +
    heading fonts, display/kicker/lede classes, heatmap → blue scale,
    article bodies serif→sans, drop-caps + justified text retired),
    `public/favicon.svg` (ADB-blue "A" mark), `Layout.tsx` (blue top
    rule, brand mark, blue active-nav), `Home.tsx` (category kicker).
  - Verification: 5 gates pass; `npm run build` 3.56s; browser-checked
    at 1280 desktop + 375 mobile, zero console errors, zero horizontal
    overflow.
  - **Known follow-up (not done here):** the 16 hero thumbnail PNGs are
    still rendered in the old warm palette by the Python pipeline
    (`scripts/thumbnail_lib.py` + per-program `build-thumbnail.py`);
    they now sit inside ADB-blue/white chrome. Full consistency needs
    an ADB-palette pass on the matplotlib stack + a 16-thumbnail
    re-render + `sync-evidence`. Active flagship unchanged.

- **2026-05-20 (later):** Second honesty loop, owner-prompted (loop
  loop loop). Read every program's `limitations.md` and audited each
  thumbnail against its program's own admitted caveats. Eleven more
  fixes shipped:
  - **migration** — Afghanistan's 7.5 M is overwhelmingly refugees
    and post-2021 displaced (per IZA C-3); subtitle now discloses
    "Cumulative STOCK, not annual flow. Afghanistan's 7.5 M is
    overwhelmingly refugees and post-2021 displaced — read as
    structural-pressure, not labor migration."
  - **food-price** — Pakistan's 2023 CPI was FX-driven, not
    climate-driven (per WB Food Crisis Observatory C-4). Subtitle
    now discloses the FX driver and says "the joint exposure here
    is not a climate-transmission claim." Also: Bangladesh
    downgraded to hollow ring marker labeled "(joins from N=5)"
    since the stable claim is LAO+PAK only across N=3..10.
  - **grid-reliability** — Title "Six grids RUN on a single fuel"
    implied generation; WRI is installed capacity. Reframed to
    "Six grids: single-fuel CAPACITY concentration" with explicit
    "Capacity ≠ generation; 2022–2025 solar buildouts not in this
    vintage" disclosure.
  - **water-stress** — TKM's 1,868 % is Amu Darya inflow against
    internal-only renewable denominator, not over-pumping (per
    limitations.md and IWMI C-2). Subtitle now says "Values above
    100 % are not over-pumping per se — the denominator excludes
    transboundary river inflows."
  - **climate-health** — WDI PM2.5 is national mean and conceals
    within-country variance (IND/CHN/IDN labeled ‡); AFG/MMR/KHM/
    LAO/TLS values are monitor-interpolated (labeled †). Inline
    legend explains the markers.
  - **social-protection** — Findex 2021 conducted during pandemic
    elevated account ownership figures; subtitle now discloses
    pandemic-vintage caveat and "Ownership ≠ active use."
  - **invisible-urbanization** — Signal co-produced by real urban
    growth AND delayed statistical reclassification of rural
    settlements (per UN-Habitat C-3); subtitle discloses the two
    are not separable here.
  - **air-monitoring** — Gap-score is HDI-correlated, not
    independent (per HEI C-4); subtitle adds "low-HDI DMCs tend to
    have both more pollution AND fewer monitors."
  - **port-hinterland** — LPI is perception-based survey not
    measured (per LPI team C-1); landlocked DMCs (KAZ, UZB in the
    top-15) are structurally different. Subtitle discloses both.
  - **remittance** — TON/VUT/WSM each have 5–8 RPW corridors only
    with wide sampling uncertainty (per Pacific Community C-4);
    subtitle disclosed alongside the existing TJK exclusion note.
  - Verification re-run: 5 gates pass, `npm run build` 2.89s,
    sync-evidence clean.

- **2026-05-20:** Visual-first refactor honesty pass. Owner pushed
  back on whether the headline numbers were accurate (not just
  whether they traced to a script — whether they meant what the
  visual implied). Self-audit surfaced 10 data-honesty issues across
  the 16 thumbnails. Each was rewritten and re-rendered:
  - **PSDQ** — unified the BGD vs PHL choropleth color scale to a
    shared 0–0.7 (previously per-panel scales made a dark BGD region
    visually equate to a 4× darker PHL region).
  - **remittance-resilience** — TJK (48% remittance/GDP, largest in
    the panel) was silently dropped from the cluster for sparse RPW
    coverage. Now shown on the map with hatched fill and an explicit
    "excluded — only 1 corridor / 1 firm in RPW" annotation.
  - **migration-displacement-signals** — title said "Six corridors
    carry 56M" but visual was 7 origins / 64.7M. Realigned to the
    program's stable 5-origin cluster (IND, CHN, BGD, AFG, PHL),
    53M total; surfaced top-9-destination coverage (91%).
  - **disaster-recovery-lag** — "1.77B affected in China" was
    greater than China's population because EM-DAT counts the same
    person across multiple events. Reframed primary axis as recorded
    disasters per year; total_affected shown as "person-events (may
    double-count)" secondary label.
  - **port-hinterland-friction** — bar of imports ÷ LPI made China
    (mid-pack LPI 3.70) look like the worst-logistics country.
    Replaced with a two-axis bubble scatter: LPI on X, imports on Y
    (log scale). China high-volume / mid-LPI; Bangladesh/Pakistan
    low-volume / low-LPI now clearly distinct.
  - **coastal-informal-risk** — headline mixed China's 1.4B
    population with a color scale of slum %. Single-axis now: 58%
    Myanmar slum-share of urban as headline (consistent with
    color encoding).
  - **air-monitoring** — "14.3M people, 13 economies" sounded
    distributed but PNG + Timor-Leste = 84% of the population. Now
    explicitly surfaced in the subtitle.
  - **access-services** — Oddar Meanchey's 319k people/facility is
    OSM-tag coverage, not actual facility count. Relabeled
    everywhere as "OSM-tagged health amenity" with explicit PSDQ
    cross-reference that OSM under-counts the official registry by
    5–10×.
  - **food-price-climate-transmission** — subtitle said "upper-
    right corner" but data was upper-LEFT (high CPI, moderate
    ag-imports). Rewrote to "clear both axes" framing matching the
    geometry.
  - **climate-health-workdays** — "799 M outdoor workers in India"
    was `outdoor_labor_share × total_population` (counts children
    and retirees). Headline reframed as "55% of India's employment
    is outdoor" with explicit note that the panel multiplies by
    total population, not labor force.
  - Verification re-run: 5 gates pass, `npm run build` 3.19s,
    browser-check 1280 desktop + 375 mobile, zero console errors,
    no horizontal overflow.
- **2026-05-19:** Visual-first refactor shipped end-to-end. Sixteen
  programs (every program with committed panel data) now render a
  1600×900 hero thumbnail PNG+SVG with a sidecar JSON; each thumbnail
  reads only committed `generated/*.csv|json` inputs and burns the
  `attestation_chain: ai-first` line into the image so a screenshot
  retains the labeling. Two programs (`digital-performance`,
  `mpi-nighttime-lights`) render honest placeholder cards.
  - New spec at `research/visual-first-refactor.md` extends the
    factory.md visualization rule with a hero-visual contract.
  - New shared helper at `scripts/thumbnail_lib.py` (figure setup,
    editorial typography, world basemap loader, attestation footer,
    sidecar writer).
  - New `opensrc/` directory with Natural Earth 110m + 50m country
    boundaries (public domain) and `REFERENCES.md` pinning the
    matplotlib + geopandas + pycirclize stack.
  - New per-program scripts: `{program}/scripts/build-thumbnail.py` for
    each of the 16 programs.
  - `scripts/sync-evidence.mjs` extended to publish a `hero` block in
    each `manifest.json` and an aggregated `public/programs/heroes.json`
    so the home page does one fetch.
  - `reporting-site/src/pages/Home.tsx` rewrote as a 16:9 thumbnail
    grid (1 col mobile / 2 col tablet / 3 col desktop), with maturity
    + attestation chips overlaid and a styled placeholder for
    programs without a hero.
  - `reporting-site/src/pages/Topic.tsx` adds a hero header above the
    tab strip with the same image shown on the home grid.
  - Composite-demotion editorial pass on `programs.ts`: six summaries
    (climate-health-workdays, port-hinterland-friction,
    remittance-resilience, school-heat-disruption,
    social-protection-shock-coverage, water-stress-crop-diversification)
    rewritten to lead with a single visceral non-composite number per §6.4.
  - Verification: 5 gates pass (banned-words, dmc-framing, citations,
    composite-headline, wip); `cd reporting-site && npm run build`
    succeeds in 2.37s; browser-checked at 1280×900 desktop and 375×800
    mobile with zero console errors and zero horizontal overflow.
  - Active flagship unchanged (`remittance-resilience`); this is a
    cross-program publication-surface refactor not a per-program
    advancement.
- **2026-05-12:** ADB/ERDI-style polish pass on PSDQ public surfaces under
  the new `/goal` skill's flagship bar. Three live-surface edits to the
  PSDQ article (subtitle, abstract, opening of "# The question") +
  governance alignment in `CLAUDE.md` (hard-walls table: "with Arturo" →
  "by an owner-designated reviewer"). Viewport-verified at 1280px desktop
  and 375px mobile, zero console errors, zero horizontal overflow. Five
  gates pass; `npm run build` succeeds in 2.75s. One edit was reverted
  for honesty: an h1 rewrite on `reporting-site/src/pages/ProgramPSDQ.tsx`
  turned out to be in orphan code (component is not routed; `Topic.tsx`
  serves `/<slug>`). `ProgramPSDQ.tsx` is dead code in the tree — either
  wire it back via the router or delete; out of scope for the polish pass.
  PSDQ remains **ai-first finished for current issue** under the same
  attestation chain. **Next flagship pick is pending owner direction**;
  candidates in the PP queue in `research/wip-register.md`; my read is
  remittance-resilience for Mode-A readiness (top-5 corridor cluster
  already stable across ±50%; article draft exists; gap to PSDQ-grade is
  the full publication ladder + Mode A review loop).
- **2026-05-12:** Goal-skill de-specialized.
  `.claude/skills/goal.md` "Current Flagship" section no longer names
  PSDQ; replaced with a STATUS.md-pointer pattern so the goal doesn't go
  stale on flagship rotation. PSDQ-specific guardrails (e.g., "PSA
  poverty overlay is a context layer") moved to PSDQ's README/STATUS
  where program-specific guardrails belong.
- **2026-05-07:** Per-program loop instituted (publication ladder + three
  review modes). 9 programs demoted PR/SR → PP under §16. PSDQ remains
  active flagship. STATUS.md slimmed to a principle-driven board (this
  refactor); PSDQ-specific narrative migrated to
  `public-service-data-quality/STATUS.md`.
- **2026-05-07:** PSDQ completed the full Mode A loop: publication ladder
  built (brief + blog + social + slide deck via Quarto), choropleth
  visualizations added (PHL ADM1, BGD ADM1, PHL ADM3 poverty), 257
  unresolved BARMM Maguindanao NHFR records resolved by deterministic
  barangay-name lookup (residue 8), reviewer packet rebuilt (6.1 MB),
  Mode A self-review + critique-pass + AI second-opinion code review
  iteration closed. PSDQ is **ai-first finished for current issue**.
  Next program from the queue can now enter the loop.
- **2026-05-07:** GitHub-prep cleanup. Repository root now has a
  reader-facing `README.md`, `LICENSE` (MIT for code), and
  `LICENSE-CONTENT` (CC BY 4.0 for research artifacts). `.gitignore`
  rewritten to exclude per-program `.cache/` directories (~8 GB total,
  reproducible from public sources via committed fetch scripts) while
  keeping each cache's `README.md` (regen instructions) committed.
  The 2026-04-25 review packet moved to `_archive/review-packets/`
  (the 2026-05-07 packet stays in `review-packets/` as the current
  one). `luminosity-gap/README.md` now opens with a "legacy" note
  pointing readers to the active `reporting-site/` instead. The repo
  is ready for `git init && git push`.

## Handoff prompt

Use this when starting a fresh session:

```text
Read research/STATUS.md, then the active flagship's {program}/STATUS.md
named in the board. Then read CLAUDE.md and research/factory.md.
Continue the active flagship's next focused work. State the active
program, stage, next output, and verification plan before editing files.
```
