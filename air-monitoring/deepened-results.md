# Deepened result — population concentration of the zero-monitor headline, and the development confound

`attestation_chain: ai-first`

This answers the two keystones in `deep-questions.md` — §4.2 (the
zero-monitor population headline) and §1.1 / §5 (the development confound)
— with a real recomputation. Every number below is produced by
`scripts/deepen-concentration-and-hdi.py` from the committed
`generated/air-monitoring-adb-panel.json` (OpenAQ v3 public PM2.5 monitor
metadata + WDI `EN.ATM.PM25.MC.M3` exposure, itself DIMAQ-interpolated per
[@shaddick2018data], + WHO Ambient AQ Database v6.1; snapshot 2026-04-23) —
the same panel the headline uses. The 2026-06-16 repair also fetches public
WDI `NY.GDP.PCAP.CD` (GDP per capita, current US$) through the World Bank API
and caches the response at `.cache/wdi-NY.GDP.PCAP.CD.json`. No AI-supplied
figures. Spearman rho is hand-computed from fractional ranks and
cross-checked against `scipy.stats.spearmanr` where applicable. The gap-score
is a composite triage measure per CONSTITUTION.md §6.4, never a country
pollution ranking; per §13.3 this is a measurement / coverage gap.

Artifact: `generated/air-monitoring-concentration-deepening.{json,csv}`.
Metadata-readiness audit:
`generated/air-monitoring-metadata-readiness-audit-summary.json` and
`generated/air-monitoring-metadata-readiness-audit.csv`.
Station-metadata source-access pass:
`generated/air-monitoring-openaq-station-metadata-summary.json` and
`generated/air-monitoring-openaq-station-metadata.csv`.
Regulator-source discovery and station-source extraction:
`generated/air-monitoring-regulator-source-inventory-summary.json`,
`generated/air-monitoring-regulator-source-inventory.csv`,
`generated/air-monitoring-regulator-station-extraction-summary.json`, and
`generated/air-monitoring-regulator-station-extraction.csv`.
Monitor-grade evidence audit:
`generated/air-monitoring-monitor-grade-evidence-summary.json` and
`generated/air-monitoring-monitor-grade-evidence.csv`.
Official-to-OpenAQ reconciliation audit:
`generated/air-monitoring-official-openaq-reconciliation-summary.json` and
`generated/air-monitoring-official-openaq-reconciliation.csv`.
Official/OpenAQ candidate review worksheet:
`generated/air-monitoring-official-openaq-candidate-review-summary.json` and
`generated/air-monitoring-official-openaq-candidate-review.csv`.
Official/OpenAQ candidate public-evidence audit:
`generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json`
and
`generated/air-monitoring-official-openaq-candidate-public-evidence.csv`.
Official/OpenAQ candidate crosswalk source scan:
`generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json`
and
`generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv`.
Official/OpenAQ candidate public-feed source scan:
`generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json`
and
`generated/air-monitoring-official-openaq-candidate-public-feed-source-scan.csv`.
One-signal review queue:
`generated/air-monitoring-one-signal-review-queue-summary.json` and
`generated/air-monitoring-one-signal-review-queue.csv`.
Monitor-grade source-validation scan:
`generated/air-monitoring-monitor-grade-source-validation-scan-summary.json`
and
`generated/air-monitoring-monitor-grade-source-validation-scan.csv`.
Monitor-grade station-review queue:
`generated/air-monitoring-monitor-grade-station-review-queue-summary.json`
and
`generated/air-monitoring-monitor-grade-station-review-queue.csv`.
Monitor-grade station method-evidence audit:
`generated/air-monitoring-monitor-grade-station-method-evidence-summary.json`
and
`generated/air-monitoring-monitor-grade-station-method-evidence.csv`.

## The two questions

1. **Concentration (§4.2).** The "~14.3M people in zero-public-monitor
   economies" regional headline rests on 13 economies. Is that aggregate
   really one or two economies wearing a regional label — a composite that
   should not lead under §6.4?
2. **Development confound (§1.1 / §5).** The gap-score multiplies two
   things low-income economies tend to have together: high PM2.5 and few
   public monitors. Does an *independent* monitoring deficit survive once
   income (HDI / GDP per capita) is partialled out — or is the score
   collinear with development? This is the question that could dissolve the
   program, and it is settled only by a series this repository does not yet
   hold on disk.

## Part (a) — the 14.3M is a Papua-New-Guinea-and-Timor-Leste figure

Recomputed from the panel: **13** zero-public-monitor economies with a
population, summing to **14,343,130** people. The population share is not
spread across the 13 — it is dominated by two economies.

| ISO | Economy | Population | Share of zero-monitor pop | Cumulative | PM2.5 (µg/m³) |
|---|---|---:|---:|---:|---:|
| PNG | Papua New Guinea | 10,576,502 | **73.7%** | 73.7% | 17.3 |
| TLS | Timor-Leste | 1,400,638 | **9.8%** | **83.5%** | 17.4 |
| FJI | Fiji | 928,784 | 6.5% | 90.0% | 12.4 |
| BRN | Brunei Darussalam | 462,721 | 3.2% | 93.2% | 7.6 |
| VUT | Vanuatu | 327,777 | 2.3% | 95.5% | 14.1 |
| WSM | Samoa | 218,019 | 1.5% | 97.0% | 12.6 |
| KIR | Kiribati | 134,518 | 0.9% | 98.0% | 11.3 |
| FSM | Micronesia, Fed. Sts. | 113,160 | 0.8% | 98.8% | 12.1 |
| TON | Tonga | 104,175 | 0.7% | 99.5% | 12.5 |
| MHL | Marshall Islands | 37,548 | 0.3% | 99.8% | 10.7 |
| PLW | Palau | 17,695 | 0.1% | 99.9% | 7.3 |
| NRU | Nauru | 11,947 | 0.1% | 100.0% | 6.1 |
| TUV | Tuvalu | 9,646 | 0.1% | 100.0% | 5.9 |

**PNG alone is 73.7% of the headline; PNG + Timor-Leste together are
83.5%.** The remaining eleven — all Pacific micro-states plus high-income
Brunei — are 16.5% combined, and the bottom seven are under 1% each. A
regional total that is 84% two economies is a composite headline in the
§6.4 sense and must not lead: the honest and more actionable statement
names Papua New Guinea and Timor-Leste directly. The §4.2 hypothesis
(≈84% two economies, PNG ≈74%) is confirmed to the figure.

This also exposes that the zero-monitor set answers a *different* question
from the pre-registered top-5 (Afghanistan, Bangladesh, Myanmar,
Uzbekistan, Tajikistan): the top-5 are large, high-exposure, low-income
South/Central Asia (PM2.5 32–46 µg/m³), whereas the zero-monitor set is
small and relatively clean (PM2.5 5.9–17.4 µg/m³, all but PNG/TLS/VUT below
13). The two are not one phenomenon, and the 14.3M aggregate should not be
read as a high-exposure-coverage story — it is a small-island plus
Melanesia coverage story, concentrated in two economies.

## Part (b) — GDP per capita explains much of the monitor-density pattern

The 2026-06-16 repair closes the earlier on-disk data wall for one
development proxy by fetching WDI `NY.GDP.PCAP.CD`. The partial is still
descriptive, not causal, and it covers only economies with at least one
public PM2.5 monitor because `people-per-monitor` is undefined when the
monitor count is zero.

| Spearman rho (descriptive only) | rho | n |
|---|---:|---:|
| gap-score vs PM2.5 exposure | +0.578 | 46 |
| gap-score vs log10(population) | +0.302 | 46 |
| gap-score vs log10(people-per-monitor) — economies with >=1 monitor | **+0.688** | 33 |
| log10(people-per-monitor) vs PM2.5 exposure — economies with >=1 monitor | +0.225 | 33 |
| log10(people-per-monitor) vs log10(GDP per capita) — economies with >=1 monitor | **-0.417** | 33 |
| gap-score vs log10(GDP per capita) — economies with >=1 monitor | **-0.623** | 33 |
| PM2.5 exposure vs log10(GDP per capita) — economies with >=1 monitor | **-0.648** | 33 |

The GDP partial fits:

```text
log10(people per monitor) = 8.7232 - 0.7611 × log10(GDP per capita)
```

The largest positive residuals — more people per monitor than GDP per
capita would predict among monitored economies — are:

| ISO | Economy | Residual | People per monitor | GDP pc, current US$ |
|---|---|---:|---:|---:|
| AZE | Azerbaijan | +1.225 | 10,202,830 | 7,284 |
| IDN | Indonesia | +0.996 | 8,099,655 | 4,925 |
| LKA | Sri Lanka | +0.922 | 7,305,333 | 4,516 |
| MMR | Myanmar | +0.921 | 18,166,697 | 1,359 |
| BGD | Bangladesh | +0.814 | 8,678,118 | 2,593 |

Two readings follow:

- The original gap-score is strongly entangled with development capacity:
  the gap-score has rho -0.623 with GDP per capita among monitored economies,
  and PM2.5 exposure itself has rho -0.648 with GDP per capita. A national
  gap-score cannot be read as a pure monitoring-policy failure.
- The residual view still leaves a policy-relevant observability question:
  several monitored economies have more people per public monitor than their
  GDP per capita would predict. This is a prioritization cue for monitor
  metadata validation, not a causal claim.

Zero-monitor economies are not in the residual regression. They remain a
separate category: no public PM2.5 monitor is visible in OpenAQ in the
2026-04-23 snapshot, regardless of GDP per capita.

## What this does and does not settle

- **Settles (Part a):** the 14.3M zero-monitor headline is 83.5% two
  economies (PNG 73.7%, Timor-Leste 9.8%). It is a §6.4 composite and
  should be restated as a Papua-New-Guinea-and-Timor-Leste figure, not a
  13-economy regional total. The zero-monitor set is also a low-exposure
  population, distinct from the high-exposure top-5.
- **Partly settles (Part b):** the GDP-per-capita partial is now runnable
  from a public WDI fetch and confirms that development capacity is a major
  confound. It does not settle HDI-adjusted observability, sensor grade,
  subnational monitor catchments, or zero-monitor residuals.
- **New metadata gate:** the metadata-readiness audit covers 50 country-panel
  rows and 24 upgrade-queue rows, but finds 0 station-level cache files, 0
  station-coordinate rows, 0 monitor-grade rows, 0 first-seen/vintage rows, and
  0 regulatory-inventory rows in the committed artifacts. Station-radius,
  monitor-grade, station-vintage, and regulatory-inventory claims are therefore
  not ready.
- **New source-access result:** the OpenAQ station-metadata fetch covers all
  24 upgrade-queue economies and returns 101 OpenAQ PM2.5 station rows, 101
  station-coordinate rows, 101 owner/provider rows, and 93 first-seen rows
  after excluding 2 rows whose coordinates fell outside broad target-country
  bounds. It still returns 0 monitor-grade rows, 0 regulator-inventory rows,
  and 0 station-radius coverage rows. Thirteen economies in the queue remain
  at zero OpenAQ PM2.5 rows, which is still an OpenAQ-visible zero rather than
  proof of no monitor on the ground.
- **New regulator-source discovery:** the public-source search layer covers
  all 24 upgrade-queue economies and identifies 9 official station-inventory
  or air-quality portal candidates, 6 official station-count claim rows, 0
  monitor-grade classification rows, and 11 targeted-search gaps. Among the 13
  zero-OpenAQ economies, 1 now has an official inventory or portal candidate,
  2 have official regulator pages with no station inventory found, 1 has a
  development-partner monitoring reference, and 9 remain targeted-search gaps.
  This is a source queue for validation, not validation itself.
- **New official station-source extraction:** the extraction pass retrieves
  the 9 targeted official inventory, portal, or plan sources and normalizes
  230 official station-coordinate rows across 5 economies, 6 station
  name-only rows, 1 count-only row, and 2 plan-count-only rows. Only 22 of the
  230 coordinate rows fall within 5 kilometers of an OpenAQ PM2.5 row as a
  screening diagnostic. The strongest new claim is therefore source
  reconciliation, not station coverage: OpenAQ visibility is not the same
  object as the public regulator map. Complete monitor-grade classification
  rows remain 0 and station-radius coverage remains not computed.
- **New official-to-OpenAQ reconciliation audit:** the audit cross-tabulates
  the 230 official coordinate rows against the existing nearest-OpenAQ
  within-5-kilometer diagnostic and the extraction pass's name-overlap signal.
  It finds 13 near-plus-name candidate rows, 9 near-only candidate rows, 22
  name-only-not-near candidate rows, 186 official coordinate rows without
  either candidate signal, 82 OpenAQ coordinate rows in the same five
  official-coordinate economies, 69 OpenAQ rows not used as a near candidate,
  and 0 validated same-station joins. The source story is now a candidate
  reconciliation queue, not a merged station crosswalk.
- **New official/OpenAQ candidate review worksheet:** the worksheet filters
  the strongest reconciliation lane into 13 near-plus-name candidate rows
  across 4 economies, then adds source metadata, row-level review questions,
  allowed decisions, and minimum validation evidence. It records 0 station-ID
  crosswalk rows, 0 public current-status confirmation rows, 0 validated
  same-station joins, and 0 station-radius-ready rows. The source story is now
  more actionable for review, but still not a station crosswalk.
- **New candidate public-evidence audit:** the audit attaches OpenAQ
  owner/provider, `isMonitor`, sensor-count, and first/last-seen metadata to
  the 13 candidate worksheet rows. It finds 13 rows with OpenAQ owner/provider
  metadata, 6 OpenAQ `isMonitor` true rows, 7 rows not marked `isMonitor`, 11
  first-seen rows, 11 last-seen rows, 0 exact station-ID overlaps, 0 exact
  official-agency owner/provider matches, 0 explicit crosswalk rows, 0
  validated same-station joins, and 0 station-radius-ready rows. The source
  story is now sharper, but the crosswalk still remains empty.
- **New candidate crosswalk source scan:** the scan fetches five public source
  URLs and reviews the 6 OpenAQ `isMonitor` candidate rows first. It screens
  all 6 rows as separate nearby stations: the 2 Bangladesh SPARTAN-adjacent
  rows have distinct official Department of Environment and SPARTAN source
  coordinates, and the 4 Uzbekistan rows are Uzhydromet POP rows near the
  StateAir / US Diplomatic Post: Tashkent OpenAQ row. It still records 0
  shared station-ID rows, 0 source-crosswalk rows, 0 documented co-location
  rows, 0 validated same-station joins, and 0 station-radius-ready rows.
- **New candidate public-feed source scan:** the scan fetches 10 public source
  URLs and reviews the 7 candidate rows not marked `isMonitor` in OpenAQ. It
  retrieves official coordinate evidence and provider-context pages, then
  screens all 7 rows as public-feed nearby rows that are not join-ready. It
  records 7 rows with official coordinate evidence, 7 with OpenAQ coordinate
  evidence, 7 with public-feed owner/provider metadata, 0 official-agency
  owner/provider matches, 0 source-owner crosswalk rows, 0 documented
  co-location rows, 0 validated same-station joins, and 0 station-radius-ready
  rows.
- **New one-signal review queue:** after the 13 near-plus-name candidates are
  source-screened, the queue combines the weaker unresolved lanes: 9 near-only
  official/OpenAQ rows, 22 name-only-not-near rows, and 138 automatic or
  official-portal monitor-grade provenance-only rows. It covers 169 review
  items across 149 unique official station keys and 8 economies, while keeping
  validated same-station joins, complete monitor-grade classifications, and
  station-radius-ready rows at 0.
- **New monitor-grade evidence audit:** the audit covers all 239
  official-source rows from the station-extraction pass. It finds 31
  source-specific method-standard signal rows in Bangladesh, 138 automatic or
  official-portal signal-only rows, 3 sensor-under-test rows, 2 plan-only rows,
  and 65 rows with no public grade language found. It still finds 0 complete
  monitor-grade classification rows. The source story is now more precise, but
  the catchment story is still blocked.
- **New monitor-grade source-validation scan:** the scan retrieves 14 seeded
  public source URLs across 7 non-Bangladesh economies and covers all 138
  monitor-grade provenance-only rows from the one-signal queue. It finds 2
  method/equipment context source rows, 5 standard/method context source rows,
  6 official/automatic context-only source rows, and 1 caution source row. It
  still finds 0 complete monitor-grade classification rows and 0
  station-radius grade-assumption-ready rows. The method context is useful for
  the next station-level review, but it is not current grade certification.
- **New monitor-grade station-review queue:** the no-network queue projects
  the source-validation scan back onto all 138 provenance-only station rows. It
  assigns 66 rows to method-context review where station-level confirmation is
  missing, 2 rows to caution-blocked status, and 70 rows to official-context
  only. It still records 0 current-status confirmed rows, 0 station-method
  classified rows, 0 complete monitor-grade classification rows, and 0
  station-radius grade-assumption-ready rows.
- **New monitor-grade station method-evidence audit:** the no-network audit
  filters the station-review queue to the 66 method-context rows and joins
  each one back to an exact official extraction row by economy, source name,
  and station ID. It finds 66 exact official rows with PM2.5 signal and
  coordinates, including 28 exact-row instrument hints in Uzbekistan and 38
  official PM2.5 portal/API rows in Indonesia and Georgia. It also flags 37
  positive raw live PM2.5 values, 12 negative raw values, 1 sentinel, and 16
  missing raw values, so raw live fields cannot be treated as clean
  current-status evidence. It still records 0 current-status confirmed rows, 0
  station-method classified rows, 0 complete monitor-grade classification rows,
  and 0 station-radius grade-assumption-ready rows.
- **New Uzbekistan station current/method scan:** the networked scan re-checks
  the 28 Uzbekistan exact-row instrument-hint rows against the public
  Uzhydromet maps API by station ID. It finds all 28 target station IDs in the
  API and all 28 with station-level HORIBA markers, but only 5 API reading
  dates within 30 days, 1 between 31 and 90 days, and 22 older than 365 days.
  It also records 15 positive raw PM2.5 values, 12 negative raw values, and 1
  sentinel value. The result strengthens station-presence and instrument-marker
  evidence, but it keeps current-status confirmation, complete monitor-grade
  classification, and station-radius readiness at 0.
- **New Uzbekistan method-policy source scan:** the seeded source scan retrieves
  4 of 5 public official or technical sources and finds source-level method,
  equipment, reading-cadence, or status context in all 4 retrieved sources.
  However, none of the retrieved sources names a target station ID from the
  28-row Uzbekistan queue. The result explains why source-policy context is
  useful for interpretation but still not station-level closure.

## Bounds

- **Composite caution (§6.4).** The gap-score is a multiplicative triage
  combination of two bounded public indicators; its top-5 is "stable by
  construction" because there are no free parameters to perturb. Part (b)'s
  correlations show the monitoring-density term carries more of the score
  than exposure, reinforcing that the composite should not headline a
  pollution claim.
- **AOD column vs breathing height.** The §18.5 upgrade-path leans on
  ACAG-V6 satellite-derived PM2.5 [@vandonkelaar2021monthly] to "cover" the
  zero-monitor economies. Satellite aerosol optical depth is a
  *column-integrated* optical property of the whole atmospheric column; the
  exposure quantity is a mass concentration at breathing height (~1.5 m).
  The column-to-surface conversion depends on the vertical aerosol profile,
  hygroscopic growth, and boundary-layer height, and its error is largest
  under high dust loading and elevated smoke layers — conditions that
  characterize the high-exposure top-5, not the relatively clean
  zero-monitor Pacific. So satellite "coverage" of the 13 zero-monitor
  economies is most trustworthy exactly where exposure is lowest (the
  Pacific), and least trustworthy where exposure is highest (the dust-belt
  top-5) — which weakens both the claim that the satellite makes the gap
  moot and, symmetrically, the WDI/DIMAQ exposure figures that lean on the
  satellite where monitors are thin [@shaddick2018data].
- **Snapshot.** The monitor count is a single 2026-04-23 OpenAQ snapshot;
  the share arithmetic in Part (a) uses panel population and is unaffected,
  but a zero count is a point-in-time observation, not a decade-long
  attestation of absence.
- **Monitor grade.** OpenAQ pools reference-grade analyzers with low-cost
  sensors; the panel's location count makes no distinction, so a non-zero
  count is an upper bound on regulatory-grade observability. This does not
  affect Part (a)'s zero-monitor set (zero is zero regardless of grade).

## Reproduce

```bash
python air-monitoring/scripts/deepen-concentration-and-hdi.py
python air-monitoring/scripts/build-metadata-readiness-audit.py
python air-monitoring/scripts/fetch-openaq-station-metadata.py
python air-monitoring/scripts/build-regulator-source-inventory.py
python air-monitoring/scripts/extract-regulator-station-evidence.py
python air-monitoring/scripts/reconcile-official-openaq-stations.py
python air-monitoring/scripts/build-official-openaq-candidate-review.py
python air-monitoring/scripts/audit-official-openaq-candidate-public-evidence.py
python air-monitoring/scripts/scan-official-openaq-candidate-crosswalk-sources.py
python air-monitoring/scripts/scan-official-openaq-candidate-public-feed-sources.py
python air-monitoring/scripts/audit-monitor-grade-evidence.py
python air-monitoring/scripts/scan-monitor-grade-source-validation.py
python air-monitoring/scripts/build-monitor-grade-station-review-queue.py
python air-monitoring/scripts/audit-monitor-grade-station-method-evidence.py
```
