# Public Service Data Quality

**Status (2026-04-30):** Finished for the current §18 AI-First issue with
two-DMC pilot artifacts (PHL + BGD), Bangladesh facility-buffer / road-context
upgrades, and a Philippines city/municipality Open Buildings denominator.
See `results.md` for the headline finding
across both countries:
- **PHL:** OSM captures 17.1% of NHFR-clinical facilities; rural-urban
  gradient 6.5% (BARMM) → 63.5% (NCR).
- **BGD:** OSM captures 11.8% of DGHS-clinical facilities; gradient
  6.2% (Barisal) → 20.1% (Dhaka).

The first testable claim's pattern (OSM materially under-counts official
registry; gap larger in rural / low-HDI ADM1) is supported in both pilots
independently. Human-final review is still required before any external
submission or peer-reviewed claim beyond the current issue.

## Files in this folder
- `README.md` — this overview
- `REPRODUCE.md` — exact rerun commands, cache map, current source blocker, and verification gates
- `SOURCE-ACTION.md` — PSA SAE workbook acquisition packet and rerun checklist
- `literature.md` — systematic Tier-A/B/C scan, 10 verified references
- `scoring.md` — §3.3 rubric, 24/30 (pending owner sign-off)
- `results.md` — Philippines pilot screening result, ranked ADM1 disagreement
- `upgrade-gap.md` — current blockers and source-gate decisions before human-final or next-country extension
- `pipeline.ts` — TypeScript scaffold (PHL + BGD implemented in scripts/, IND/IDN/NPL TODO)
- `scripts/fetch-nhfr.sh` — pages through DOH NHFR JWT-issued API (PHL)
- `scripts/process-disagreement.py` — single-country PHL processing
- `scripts/process-multi-country.py` — multi-country processing (PHL + BGD); produces summary
- `scripts/audit-catchment-readiness.py` — checks whether cached registry records support ADM2/admin-code or facility-catchment Open Buildings joins
- `scripts/fetch-bgd-public-facilities.py` — polite/resumable fetcher for the richer Bangladesh coordinate-bearing public facilities endpoint
- `scripts/prepare-bgd-open-buildings-manifest.py` — builds the Bangladesh-intersecting Google Open Buildings tile manifest and threshold table
- `scripts/download-bgd-open-buildings-points.py` — resumable downloader for the four Google Open Buildings point shards
- `scripts/compute-bgd-open-buildings-facility-buffers.py` — computes nearest-facility Open Buildings counts at 1/3/5 km using all/p85/p90 confidence modes
- `scripts/build-bgd-exposure-ranked-disagreement.py` — assigns Bangladesh OSM health features to ADM3/upazila polygons and joins OSM, DGHS, and Open Buildings into an exposure-ranked gap screen
- `scripts/build-bgd-road-surface-context.py` — aggregates the HeiGIT/HDX Bangladesh road-surface GeoPackage to upazilas and joins it to the exposure-ranked PSDQ screen
- `scripts/build-bgd-source-disagreement-strata.py` — packages the Bangladesh exposure and road-context outputs into L3 ratio strata, validation residues, and top validation rows for the showcase report
- `scripts/design-bgd-facility-validation-sample.py` — designs the Bangladesh facility-level validation sample and blank coding sheet from the L3 strata and DGHS facility-coordinate extract
- `scripts/code-bgd-facility-validation-sample.py` — codes the Bangladesh validation sample with the cached all-Bangladesh OSM health-feature pull and geoBoundaries ADM3 coordinate checks
- `scripts/review-bgd-facility-validation-flags.py` — converts the flagged Bangladesh coded-screen rows into an AI public-source row-review ledger and workstream summary
- `scripts/resolve-bgd-facility-candidate-rows.py` — separates the candidate-resolution subset of the Bangladesh validation ledger into narrower public-source lanes
- `scripts/check-bgd-facility-candidate-public-sources.py` — scans richer public OSM tags and DGHS public registry fields for the 8 candidate-resolution rows
- `scripts/triage-bgd-facility-coordinate-repairs.py` — separates the 23 Bangladesh coordinate-repair rows by missing, reused, wrong-admin, and boundary-mismatch coordinate signals
- `scripts/triage-bgd-facility-public-map-gaps.py` — separates the 40 Bangladesh public-map-gap rows by duplicate-coordinate, same-upazila name-signal, buffer-sensitivity, zero-OSM-upazila, and no-nearby-OSM lanes
- `scripts/build-bgd-facility-public-map-gap-row-evidence.py` — adds DGHS profile/source notes, OSM inspection links, and keep-open reviewer actions for all 40 public-map-gap rows
- `scripts/inspect-bgd-facility-public-map-targets.py` — builds the targeted public-map inspection packet with candidate OSM feature links and closure/reclassification requirements for the 40 row-evidence records
- `scripts/confirm-bgd-facility-public-map-first-rows.py` — retrieves public DGHS profile pages and public OSM API feature records for the first 12 targeted inspection rows
- `scripts/confirm-bgd-facility-public-map-targeted-rows.py` — retrieves public DGHS profile pages and public OSM API feature records for all 40 targeted inspection rows
- `scripts/build-bgd-facility-public-source-decision-ledger.py` — converts the 40-row public-source confirmation packet into a no-network reviewer decision ledger
- `scripts/attach-bgd-facility-source-repair-public-evidence.py` — attaches public DGHS and OSM evidence to the four source-repair-first decision rows
- `scripts/explain-bgd-facility-source-repair-official-coordinates.py` — retrieves public DGHS profile pages and parses official map coordinates for the four source-repair-first rows
- `scripts/search-bgd-facility-source-repair-public-explanations.py` — searches public DGHS profile tabs, cached DGHS registry records, and official government health portals for source-repair coordinate explanations
- `scripts/followup-bgd-facility-source-repair-correction-records.py` — checks targeted DGHS registry, Health Dashboard, and government health portal pages for correction records on the Durgapur and Narayanganj source-repair rows
- `scripts/build-bgd-facility-source-repair-clarification-packet.py` — builds a no-contact source-owner and human-review question packet for the unresolved Durgapur and Narayanganj source-repair rows
- `scripts/build-bgd-facility-source-repair-registry-vintage-review.py` — joins clarification rows to public profile update timestamps and correction-record status to block premature closure, reclassification, or map-absence language
- `scripts/prepare-phl-open-buildings-manifest.py` — builds the Philippines-intersecting Google Open Buildings tile manifest using the HDX/OCHA PSA/NAMRIA boundary package
- `scripts/download-phl-open-buildings-points.py` — resumable downloader for the eight Philippines-intersecting Google Open Buildings point shards
- `scripts/build-phl-admin3-open-buildings-context.py` — assigns Open Buildings and OSM health features to PSA/NAMRIA ADM3 city/municipality polygons and joins NHFR counts using direct boundary codes plus PSA PSGC correspondence codes
- `scripts/fetch-phl-sae-poverty.py` — attempts the official PSA 2023 city/municipality SAE poverty attachment and caches PSA OpenSTAT 2023 direct poverty estimates
- `scripts/build-phl-admin3-poverty-context.py` — joins source-gated poverty fields to the Philippines ADM3 context without imputing missing city/municipality SAE values
- `catchment-upgrade.md` — method note for the Open Buildings settlement-exposure upgrade
- `.cache/nhfr_p{1..23}.json` — cached PHL NHFR responses (23 pages, 44,267 records)
- `.cache/bgd_dghs_p{1..20}.json` — cached BGD DGHS responses (20 pages, 39,421 records)
- `generated/public-service-data-quality-PHL.{json,csv}` — Philippines output
- `generated/public-service-data-quality-BGD.{json,csv}` — Bangladesh output
- `generated/public-service-data-quality-summary.json` — multi-country summary
- `generated/psdq-catchment-readiness.json` — source-field audit for the catchment upgrade
- `generated/psdq-bgd-open-buildings-tile-manifest.{json,csv}` — four Bangladesh-intersecting Open Buildings V3 point shards and precision thresholds
- `generated/psdq-bgd-open-buildings-facility-buffers.csv` — one row per coordinate-ready DGHS facility with nearest-building counts
- `generated/psdq-bgd-open-buildings-admin-summary.csv` — upazila/district/division rollup of the facility-buffer denominator
- `generated/psdq-bgd-open-buildings-buffer-summary.json` — chart-ready Open Buildings denominator summary
- `generated/psdq-bgd-osm-health-upazila.csv` — OSM health features assigned to geoBoundaries ADM3/upazila polygons
- `generated/psdq-bgd-exposure-ranked-disagreement.csv` — DGHS/OSM/Open Buildings exposure-ranked upazila table
- `generated/psdq-bgd-exposure-ranked-disagreement-summary.json` — chart-ready exposure-gap summary
- `generated/psdq-bgd-road-surface-upazila.csv` — upazila road-surface context from HeiGIT/HDX road data
- `generated/psdq-bgd-road-surface-summary.json` — chart-ready road-surface summary
- `generated/psdq-bgd-exposure-road-context.csv` — exposure-ranked PSDQ table joined to road-surface context
- `generated/psdq-bgd-exposure-road-context-summary.json` — chart-ready service-gap plus road-context summary
- `generated/psdq-bgd-source-disagreement-strata.{json,csv}` — L3 source-disagreement ratio buckets, validation residues, and top rows for the showcase report
- `generated/psdq-bgd-facility-validation-sample.json` — deterministic Bangladesh validation-sample design, public-source stack, and non-claim
- `generated/psdq-bgd-facility-validation-sample-upazilas.csv` — 20 sampled upazila rows across high-gap, zero-OSM, OSM-above-registry, and comparison groups
- `generated/psdq-bgd-facility-validation-sample-facilities.csv` — 76 sampled DGHS facility rows selected for public-source review
- `generated/psdq-bgd-facility-validation-coding-sheet.csv` — blank validation coding sheet with suggested public OSM checks where coordinates are available
- `generated/psdq-bgd-facility-validation-coded-screen.csv` — automated public-source validation screen for the 76 sampled DGHS facility rows
- `generated/psdq-bgd-facility-validation-osm-candidates.csv` — OSM health candidates within 500 meters of sampled DGHS coordinates
- `generated/psdq-bgd-facility-validation-coded-summary.json` — chart-ready validation-code counts, group counts, and source-status metadata
- `generated/psdq-bgd-facility-validation-ai-review.csv` — AI public-source row-review ledger for the 71 flagged coded-screen rows
- `generated/psdq-bgd-facility-validation-ai-review-summary.json` — chart-ready review workstream counts, priority counts, and non-claim metadata
- `generated/psdq-bgd-facility-validation-candidate-resolution.csv` — AI public-source candidate-resolution pass over the 8 row-level candidate cases
- `generated/psdq-bgd-facility-validation-candidate-resolution-summary.json` — chart-ready candidate-resolution lane counts and non-claim metadata
- `generated/psdq-bgd-facility-validation-candidate-public-source-check.csv` — AI public-source scan of richer OSM tags and DGHS public registry fields for the 8 candidate rows
- `generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json` — chart-ready public-source check lanes and non-claim metadata
- `generated/psdq-bgd-facility-validation-coordinate-repair.csv` — AI public-source coordinate-repair triage for the 23 registry-coordinate repair rows
- `generated/psdq-bgd-facility-validation-coordinate-repair-summary.json` — chart-ready coordinate-repair lanes, distance ledger, and non-claim metadata
- `generated/psdq-bgd-facility-validation-public-map-gap.csv` — AI public-source public-map-gap triage for the 40 valid-coordinate map-gap rows
- `generated/psdq-bgd-facility-validation-public-map-gap-summary.json` — chart-ready public-map-gap lanes, upazila queue, and non-claim metadata
- `generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv` — row-level DGHS/OSM public-source evidence notes and keep-open reviewer actions for the 40 map-gap rows
- `generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json` — chart-ready row-evidence tiers, upazila queue, and top evidence-card rows
- `generated/psdq-bgd-facility-validation-public-map-inspection.csv` — targeted public-map inspection packet with prioritized candidate features and evidence-needed fields
- `generated/psdq-bgd-facility-validation-public-map-inspection-summary.json` — chart-ready inspection lanes, focus queue, and top inspection-card rows
- `generated/psdq-bgd-facility-validation-public-source-confirmation.csv` — first-row public-source confirmation ledger with DGHS profile and OSM API retrieval status
- `generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json` — chart-ready confirmation lanes, retrieval counts, and first-row source cards
- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv` — targeted-row public-source confirmation ledger with DGHS profile and OSM API retrieval status for all 40 inspection rows
- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json` — chart-ready targeted-row confirmation lanes, retrieval counts, and upazila confirmation rows
- `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv` — no-network public-source decision ledger for possible same-facility, source-repair, and priority-1 name-conflict rows
- `generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json` — chart-ready decision-track counts, defer counts, and reviewer decision rows
- `generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv` — source-repair public-evidence attachment table for the four source-repair-first decision rows
- `generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json` — chart-ready source-repair attachment counts, evidence classes, and candidate groups
- `generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv` — official DGHS profile coordinate evidence for the four source-repair-first rows
- `generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json` — chart-ready official-coordinate exposure, distance, and keep-open counts
- `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv` — public official-page explanation search for the four source-repair-first coordinates
- `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json` — chart-ready explanation-search counts, same-name conflicts, and keep-open actions
- `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv` — targeted public correction-record follow-up for the Durgapur conflict and shared-coordinate Narayanganj rows
- `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json` — chart-ready correction-record counts, DGHS dashboard confirmations, and keep-open actions
- `generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv` — no-contact clarification questions and human-review prompts for the unresolved Durgapur and Narayanganj rows
- `generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json` — chart-ready clarification-packet counts, issue classes, public links, and non-claim metadata
- `generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv` — profile-update timestamp and review-gate checklist for the unresolved Durgapur and Narayanganj rows
- `generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json` — chart-ready registry-vintage counts, age range, keep-open gates, and non-claim metadata
- `generated/psdq-phl-open-buildings-tile-manifest.{json,csv}` — eight Philippines-intersecting Open Buildings V3 point shards and precision thresholds
- `generated/psdq-phl-admin3-open-buildings-context.csv` — PSA/NAMRIA ADM3 city/municipality table with Open Buildings, PSGC-resolved NHFR, and OSM health counts
- `generated/psdq-phl-admin3-open-buildings-context-summary.json` — chart-ready Philippines ADM3 denominator and code-match summary
- `generated/psdq-phl-admin3-poverty-context.csv` — Philippines ADM3 context joined to official PSA poverty fields where source-gated data are available
- `generated/psdq-phl-admin3-poverty-context-summary.json` — poverty-context source status, join counts, and chart-ready direct-estimate/HUC rows

## Catchment upgrade readiness

Run:

```bash
python public-service-data-quality/scripts/audit-catchment-readiness.py
```

Current audit result:

- **PHL NHFR:** 44,267 records; region, province, city/municipality, and
  barangay codes are essentially complete, but there are no cached facility
  coordinates. Use admin-code Open Buildings denominators first.
- **PHL ADM3 Open Buildings denominator:** eight Google Open Buildings V3
  point shards intersect the Philippines. The full local pass processed
  38,122,474 catalog rows and assigned 36,447,136 building points to
  PSA/NAMRIA ADM3 city/municipality polygons. At the tile-specific p85
  precision threshold, 13,538,628 building points are assigned to ADM3. A
  direct NHFR-to-ADM3 code join matches 35,932 of 44,267 active records;
  a chain of three deterministic resolvers then raises the ADM3 match to
  **44,259 records (99.98%)** and **37,384 of 37,392 clinical-tier records
  (99.98%)**. The 8,327 records resolved after direct matching split into
  5,603 PSGC correspondence-code matches, 2,475 special code-vintage rules
  (Negros Island Region, Manila districts, Sulu, Special Geographic Area),
  and 249 records resolved by a barangay-name lookup against the PSA/NAMRIA
  2023 ADM4 layer for the BARMM Maguindanao split (NHFR uses an older
  PSGC vintage where these barangays were assigned to different parent
  municipalities; the deterministic resolver finds the modern parent
  ADM3 by majority vote of barangay-name matches per ctymuncode — see
  `generated/psdq-phl-nhfr-barmm-ctymun-resolution.json` for the full
  audit trail). The remaining 8 NHFR records are confirmed as a
  source-quality residue and are not imputed. OSM Overpass
  retrieved 6,548 Philippines health features and assigned 6,544 to ADM3.
  The current top exposure-screen rows are Zamboanga City, Davao City,
  Cagayan de Oro City, General Santos City, and Quezon City. This is an
  admin-denominator screen, not a facility catchment or affected-population
  estimate.
- **BGD DGHS DataTables:** 39,421 records; division, district, and upazila
  fields are near-complete, but there are no cached facility coordinates in
  the current counting endpoint.
- **BGD public facilities JSON endpoint:** full 789-page pull cached,
  39,419 records parsed. The chart-ready extract finds 29,371 records
  (74.51%) with coordinates inside Bangladesh bounds and 39,419 records
  (100%) with at least one catchment field. Use the coordinate subset for
  facility-buffer analysis and route non-coordinate records through district
  or upazila denominators.
- **BGD Open Buildings facility buffers:** four Google Open Buildings V3
  point shards intersect Bangladesh. The full pass processed 148,982,383
  catalog rows, screened 37,573,563 building points inside Bangladesh, and
  assigned 37,162,607 of those to a coordinate-ready DGHS facility within
  5 km. At the tile-specific p85 precision threshold, the nearest-facility
  denominator is 9,110,471 buildings within 1 km, 17,545,636 within 3 km,
  and 18,475,230 within 5 km. These are settlement-exposure denominators,
  not people, households, poverty, service demand, or validated catchments.
- **BGD exposure-ranked disagreement:** the new upazila pass retrieved
  3,303 OSM health features from Overpass, assigned 3,302 to geoBoundaries
  ADM3 polygons, and joined 3,212 to DGHS upazila rows after documented
  name canonicalization. The exposure proxy combines the active DGHS clinical
  facility gap with the 3 km p85 Open Buildings denominator. Current top
  rows are Gazipur Sadar, Narayanganj Sadar, Kushtia Sadar, Pabna Sadar,
  and Narsingdi Sadar. The total gap-weighted 3 km p85 denominator is
  15,668,648 buildings. This is a screening index, not a population,
  poverty, service-demand, or verified catchment estimate.
- **BGD road-surface context:** the road overlay assigns 650,579 HeiGIT/HDX
  Bangladesh road features to geoBoundaries ADM3 polygons by representative
  point. The assigned network has 304,941.2 km of OSM-length road lines;
  51,327.4 km have a paved/unpaved surface class from the combined
  OSM/Mapillary/deep-learning surface field. Of the classified length,
  33,588.2 km are paved and 17,739.2 km are unpaved. The joined
  service-gap screen scores 234 upazila rows after requiring at least 50 km
  classified road length and at least 10% classified-surface coverage. The
  score is a triage context layer, not a travel-time, poverty, or road-access
  estimate.
- **BGD source-disagreement L3 strata:** the no-network packaging pass reads
  the exposure-ranked table and road-context summary, then writes
  `generated/psdq-bgd-source-disagreement-strata.{json,csv}`. The current
  artifact covers 572 DGHS registry upazila rows; 561 have an Open Buildings
  denominator; 115 active-registry rows have zero OSM health features; 21 rows
  have OSM counts equal to or above the active registry count; 234 rows meet
  the road-surface scoring threshold. This is a source-validation ledger for
  `/showcase/psdq-source-disagreement`, not an access or quality result.
- **BGD facility-validation sample design:** the no-network sample pass reads
  the L3 strata, exposure-ranked table, and DGHS facility-coordinate extract.
  It writes `generated/psdq-bgd-facility-validation-sample.json`, two sample
  CSVs, and a blank coding sheet with 20 sampled upazila rows and 76 DGHS
  facility rows. Of the sampled facility rows, 69 are coordinate-ready. This
  is a public-source validation workplan, not a validation result.
- **BGD facility-validation coded screen:** the no-network coding pass reads
  the validation sheet, the cached all-Bangladesh OSM health-feature pull, and
  geoBoundaries ADM3. It writes `generated/psdq-bgd-facility-validation-coded-screen.csv`,
  `generated/psdq-bgd-facility-validation-osm-candidates.csv`, and
  `generated/psdq-bgd-facility-validation-coded-summary.json`. The automated
  screen codes 76 sampled DGHS rows: 40 missing public-map points, 23 registry
  coordinate issues, 5 confirmed same-facility matches, 3 probable aliases, 3
  classification mismatches, and 2 OSM-only candidates. This is not a human
  validation pass.
- **BGD AI public-source review ledger:** the no-network review pass reads the
  coded screen, the OSM candidate table, and the coded-summary metadata. It
  writes `generated/psdq-bgd-facility-validation-ai-review.csv` and
  `generated/psdq-bgd-facility-validation-ai-review-summary.json`. The ledger
  keeps all 71 flagged rows open while separating them into 40 public-map-gap
  checks, 23 coordinate-source repairs, 6 name/type resolution rows, and 2
  nearby-OSM-without-registry-match rows. This is AI public-source row review,
  not human validation.
- **BGD candidate-resolution pass:** the no-network candidate pass reads the
  AI review ledger, OSM candidate table, and AI review summary. It writes
  `generated/psdq-bgd-facility-validation-candidate-resolution.csv` and
  `generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`.
  The pass keeps all 8 queued rows open while separating them into 1 probable
  alias/campus lane, 2 same-site classification-conflict lanes, 2 possible
  aliases, 1 local-script name gap, 1 ambiguous nearby candidate, and 1 weak
  nearby OSM signal. This is AI public-source candidate resolution, not human
  validation.
- **BGD candidate public-source check:** the no-network source check reads the
  candidate-resolution CSV, OSM candidate table, cached all-Bangladesh OSM
  tags, and cached DGHS DataTables rows. It writes
  `generated/psdq-bgd-facility-validation-candidate-public-source-check.csv`
  and
  `generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json`.
  The check keeps all 8 rows open while separating them into 2 strong same-site
  OSM tag-support rows, 2 same-site type/label conflicts, 2 name-support rows
  with coordinate/function conflicts, and 2 nearby-feature rows without
  registry-name support. This is AI public-source evidence scanning, not human
  validation.
- **BGD coordinate-repair triage:** the no-network coordinate pass reads the AI
  review ledger, coded-screen CSV, public geoBoundaries ADM3, cached
  all-Bangladesh OSM health features, and cached DGHS DataTables rows. It
  writes `generated/psdq-bgd-facility-validation-coordinate-repair.csv` and
  `generated/psdq-bgd-facility-validation-coordinate-repair-summary.json`.
  The triage keeps all 23 coordinate-repair rows open: 7 rows have no usable
  coordinate, 2 reuse an exact sampled coordinate, 6 sit in another public ADM3
  and within 500 meters of an OSM health feature, 5 sit in another public ADM3
  without a nearby OSM health feature, and 3 fall outside the public ADM3
  polygons used here. This is source-repair triage, not human validation.
- **BGD public-map-gap triage:** the no-network map-gap pass reads the AI
  review ledger, coded-screen CSV, coordinate-repair CSV, exposure-ranked
  table, OSM upazila table, cached all-Bangladesh OSM health features, and
  cached DGHS public rows. It writes
  `generated/psdq-bgd-facility-validation-public-map-gap.csv` and
  `generated/psdq-bgd-facility-validation-public-map-gap-summary.json`. The
  triage keeps all 40 public-map-gap rows open: 30 are priority-1
  high-exposure rows, 18 sit in zero-OSM expected upazilas, 2 reuse a valid
  sampled coordinate, 2 have a far same-upazila name signal, 1 has a
  same-upazila name signal outside 500 meters, 2 are 500m-to-1km
  buffer-sensitive, 3 have OSM present in the upazila but not at the sampled
  facility, and 12 have no same-upazila OSM health signal within 3 kilometers.
  This is public-source triage, not human validation or proof that a facility
  is absent from OSM.
- **BGD public-map-gap row evidence:** the no-network row-evidence pass reads
  the public-map-gap triage CSV/JSON and writes
  `generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv` and
  `generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`.
  It gives all 40 open rows a DGHS source note, public profile URL, OSM
  coordinate-inspection URL, OSM feature or absence note, and keep-open
  reviewer action. The evidence tiers are 4 source-repair-first rows, 3
  possible match or buffer-review rows, 15 row-level public-map absence-review
  rows, and 18 upazila-level public-map observability rows. This is row-level
  source evidence, not row closure or human validation.
- **BGD targeted public-map inspection:** the no-network inspection pass reads
  the row-evidence CSV/JSON, the pinned all-Bangladesh OSM health-feature
  cache, and public ADM3 boundaries. It writes
  `generated/psdq-bgd-facility-validation-public-map-inspection.csv` and
  `generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`.
  It inspects all 40 row-evidence records while marking 10 named-upazila start
  rows and 18 zero-OSM queue rows. It provides same-upazila candidate feature
  links for 22 rows, identifies 6 specific-name signals among candidate
  features, and keeps all 40 rows open. This is targeted public-map
  inspection, not human validation or row closure.
- **BGD first-row public-source confirmation:** the live public-source
  confirmation pass reads the targeted inspection summary and retrieves public
  DGHS profile pages plus public OSM API feature records for the first 12
  inspection rows. It retrieves 12 DGHS profiles and 12 OSM API records,
  records 2 candidate rows with live OSM name score at least 0.75, and keeps
  all 12 rows open. This is public-source confirmation, not human validation
  or row closure.
- **BGD targeted-row public-source confirmation:** the live public-source
  confirmation pass reads the 40-row targeted inspection CSV and retrieves
  public DGHS profile pages plus public OSM API feature records for all 40
  inspection rows. It retrieves 40 DGHS profiles and 40 OSM API records,
  covers all 30 priority-1 rows, records 6 candidate rows with live OSM name
  score at least 0.75, and keeps all 40 rows open. Confirmation lanes are 18
  zero-OSM context rows, 15 retrieved-candidate name-conflict rows, 4
  source-repair rows, and 3 possible same-facility rows requiring manual
  location or official-source confirmation. This is public-source
  confirmation, not human validation or row closure.
- **BGD public-source decision ledger:** the no-network decision pass reads
  the targeted-row confirmation CSV/JSON and selects 16 reviewer decision
  rows: 4 source-repair rows, 3 possible same-facility rows, and 9 priority-1
  name-conflict rows. It defers 18 zero-OSM upazila observability rows and 6
  lower-priority name-conflict spot checks. It keeps all 40 targeted rows open
  with 0 AI closures and 0 AI reclassifications. This is a public-source
  reviewer queue, not human validation or a row outcome table.
- **BGD source-repair public evidence:** the no-network attachment pass reads
  the decision ledger and targeted-row confirmation CSV, then attaches public
  DGHS profile and OSM API evidence to the 4 source-repair-first rows. All 4
  rows have public evidence attached; 2 rows share one public-map candidate; 2
  rows have candidate distances of at least 10 kilometers; and 1 row has a
  candidate distance of at least 50 kilometers. It keeps all 4 rows open with
  0 AI closures and 0 AI reclassifications. This is source evidence
  attachment, not human validation or source repair completion.
- **BGD source-repair official-coordinate evidence:** the live public-source
  pass retrieves the 4 public DGHS profile pages, parses the embedded official
  map coordinate, and compares it with the pinned OSM candidate coordinate. All
  4 profiles expose coordinates that match the inspection CSV; 2 rows share one
  official profile coordinate; 2 rows are at least 10 kilometers from the named
  OSM candidate; 1 row is at least 50 kilometers from the named OSM candidate;
  and 0 explicit coordinate-source explanations are exposed. It keeps all 4
  rows open with 0 AI closures and 0 AI reclassifications.
- **BGD source-repair public-explanation evidence:** the live public-source
  search checks the 4 source-repair rows against 8 DGHS profile tabs, cached
  DGHS registry records, and 6 official portal URLs. It retrieves 5 portal
  pages and finds 0 explicit coordinate-source or coordinate-correction
  explanations. It sharpens the queue: 2 Narayanganj rows share one official
  coordinate, 1 Netrakona Durgapur row has a same-name Rajshahi DGHS registry
  sibling whose coordinate is 747.0 meters away, and 0 rows are closed or
  reclassified.
- **BGD source-repair correction-record follow-up:** the live targeted
  follow-up reads the public-explanation evidence, selects the 3 unresolved
  shared-coordinate or same-name cross-district rows, and checks public DGHS
  registry pages, DGHS Health Dashboard pages, and public government health
  portals for correction records or coordinate-source notes. It checks and
  retrieves 20 official sources, finds 0 public correction or coordinate-source
  records, confirms target DGHS dashboard codes for all 3 rows, confirms the
  linked Rajshahi Durgapur dashboard code for the Durgapur conflict, and closes
  or reclassifies 0 rows.
- **BGD source-repair clarification packet:** the no-network packet reads the
  correction-record follow-up and creates 3 source-owner or human-review
  questions: 2 shared-coordinate Narayanganj questions and 1 same-name
  cross-district Durgapur question. It makes 0 external contacts, closes 0
  rows, reclassifies 0 rows, and keeps all three rows out of map-absence or
  same-facility language until source-owner clarification or human validation.
- **BGD source-repair registry-vintage review:** the no-network review joins
  the clarification packet to public DGHS profile timestamps and the
  correction-record follow-up. All 3 unresolved rows have profile update
  timestamps that were 1 to 12 days old at public-explanation retrieval, but
  0 public correction or coordinate-source records were found. The review
  allows 0 closures, 0 same-facility reclassifications, and 0 map-absence uses.
- **Poverty overlay status:** Philippines now has an official poverty-context
  artifact using the owner-manually downloaded PSA 2023 city/municipality SAE
  Excel plus PSA OpenSTAT 2023 direct estimates for HUC/direct-estimate rows.
  The deterministic fetcher still records that PSA static-file URLs return
  Cloudflare's managed browser challenge from this environment, so the manual
  download is documented in `SOURCE-ACTION.md`. The current join covers 1,632
  of 1,642 ADM3 rows: 1,597 from the SAE workbook and 35 from OpenSTAT direct
  estimates. The remaining 10 rows stay explicitly source-missing. No poverty
  value is imputed from buildings, roads, OSM, or registry gaps. Bangladesh
  poverty remains out of the main result until a current, unit-compatible table
  is source-gated.

Re-run the Open Buildings denominator:

```bash
python public-service-data-quality/scripts/prepare-bgd-open-buildings-manifest.py
python public-service-data-quality/scripts/download-bgd-open-buildings-points.py
python public-service-data-quality/scripts/compute-bgd-open-buildings-facility-buffers.py --chunk-size 500000 --workers 4
python public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py
python public-service-data-quality/scripts/build-bgd-road-surface-context.py --skip-download
python public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py
python public-service-data-quality/scripts/design-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/review-bgd-facility-validation-flags.py
python public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py
python public-service-data-quality/scripts/check-bgd-facility-candidate-public-sources.py
python public-service-data-quality/scripts/triage-bgd-facility-coordinate-repairs.py
python public-service-data-quality/scripts/triage-bgd-facility-public-map-gaps.py
python public-service-data-quality/scripts/build-bgd-facility-public-map-gap-row-evidence.py
python public-service-data-quality/scripts/inspect-bgd-facility-public-map-targets.py
python public-service-data-quality/scripts/confirm-bgd-facility-public-map-first-rows.py
python public-service-data-quality/scripts/confirm-bgd-facility-public-map-targeted-rows.py
python public-service-data-quality/scripts/build-bgd-facility-public-source-decision-ledger.py
python public-service-data-quality/scripts/attach-bgd-facility-source-repair-public-evidence.py
python public-service-data-quality/scripts/explain-bgd-facility-source-repair-official-coordinates.py
python public-service-data-quality/scripts/search-bgd-facility-source-repair-public-explanations.py
python public-service-data-quality/scripts/followup-bgd-facility-source-repair-correction-records.py
python public-service-data-quality/scripts/build-bgd-facility-source-repair-clarification-packet.py
python public-service-data-quality/scripts/build-bgd-facility-source-repair-registry-vintage-review.py
python public-service-data-quality/scripts/prepare-phl-open-buildings-manifest.py
python public-service-data-quality/scripts/download-phl-open-buildings-points.py
python public-service-data-quality/scripts/build-phl-admin3-open-buildings-context.py --chunk-size 500000 --workers 4
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py
python public-service-data-quality/scripts/build-phl-admin3-poverty-context.py
```

To refresh the Philippines NHFR/PSGC/OSM join without reprocessing the
38.1 million Open Buildings rows, reuse the existing ADM3 building columns:

```bash
python public-service-data-quality/scripts/build-phl-admin3-open-buildings-context.py --reuse-existing-buildings --skip-osm-fetch
```

## Original hypothesis text follows


## Research Question

Where do public maps and administrative data disagree enough that development
planning may be operating with a weak picture of service availability?

## Why This Is Unconventional

Instead of only measuring development gaps, this track measures measurement
gaps: where the data infrastructure itself is likely distorting decisions.

## Available Data

- OpenStreetMap schools, clinics, roads, markets, and public offices
- Official statistical agency facility lists where public
- HDX datasets and country open-data portals
- geoBoundaries administrative geometries
- WorldPop population grids
- Existing generated access-services artifacts in this repo

## First Pipeline

1. Compare OSM service counts with any official facility list available for a
   pilot economy.
2. Compute population per observed facility in both sources.
3. Flag places where planning conclusions change depending on data source.

## Outputs

- `generated/public-service-data-quality-pilots.csv`
- Source-disagreement table
- Audit checklist for data-source confidence

## Reproducibility Notes

Record every source timestamp. Public maps change frequently, so stale extracts
must not be silently reused.
