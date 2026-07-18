---
slug: the-first-issue
title: "Vol. I, № 04: The first issue of the Blindspots Lab"
subtitle: "Seven programs finished for the current issue, eight at Screening Result, one at Program Prospectus, one at Prepared Pipeline, and one at Hypothesis. Every gate is AI-attested under Constitution §18. Read with that in mind."
kind: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: []
topics: [governance, methodology, first-issue]
program: meta
maturity: PR
abstract: >
  This is the first issue of The Blindspots Lab. Seven programs cross
  to finished-for-current-issue status under Constitution §18 (AI-First Operating
  Mode). Eight more sit at Screening Result with explicit honest
  narrowings or triage-only screens. One — climate-health-workdays —
  is a Program Prospectus because the PM2.5 layer is computed but the
  heat layer remains an upgrade. One — digital-performance — stays at
  Prepared Pipeline because the Ookla parquet aggregation has not yet
  been run. One — mpi-nighttime-lights — remains at Hypothesis until
  the external track is reconciled. The article introduces the finished
  issue findings, the screening results, the held-back tracks, and what
  readers should know about §18 attested research before they cite it.
doi:
published_at: 2026-04-26
updated_at: 2026-07-07
references: []
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18
---

# What's in the issue

Seven current-issue finished programs, each with a permanent self-hosted
evidence packet at `/program/{slug}/evidence` and a working-paper
article in this hub. The full issue register now has an honest label for
all eighteen topics: seven finished, eight screening-only, one
prospectus, one prepared pipeline, and one hypothesis. All under §18 —
AI-attested rather than human-attested. Read each headline with that
label.

## The seven finished current-issue programs

**Public Service Data Quality.** OpenStreetMap captures 17.1% of the
Philippines clinical-tier health-facility registry and 11.8% of the
Bangladeshi one. Both fall below the 30% fit-for-planning threshold.
The within-country gradient is steep. → [the-osm-vs-registry-gap](/findings/measurement-gap-philippines-bangladesh)

**Remittance Resilience.** Five DMCs — Kyrgyz Republic, Nepal, Tonga,
Vanuatu, Samoa — persistently cluster as remittance-corridor-stress-
exposed. Stable across every ±50% sensitivity row including a
multiplicative-vs-additive aggregation switch. → [/findings/remittance-corridors-vulnerability-cluster](/findings/remittance-corridors-vulnerability-cluster)

**Migration & Displacement.** Five DMCs — India, China, Bangladesh,
Afghanistan, Philippines — hold the top of the emigrant-stock
ranking across raw-stock and net-migrant definitions. Three of the
five concentrate over 50% of emigration in three corridors; two have
diversified destinations. Afghanistan is refugee-driven, flagged
distinctly. → [/findings/emigrant-stock-corridor-concentration](/findings/emigrant-stock-corridor-concentration)

**Disaster Burden.** Two DMCs — China and India — hold the top two
of every alternative burden ranking (events-per-year, total-affected,
damage-USD-adjusted). Top-5 metric-sensitive; metric-robust top-2 is
the headline. Recovery-lag analysis itself deferred to upgrade-pass. → [/findings/disaster-burden-cluster](/findings/disaster-burden-cluster)

**Single-Fuel Grids.** Five DMCs — Brunei, Bhutan, Mongolia, Nepal,
Tajikistan — depend on a single fuel for 80%+ of capacity. Mixed
subtypes: three hydro-dominant, one gas, one coal. Fragility
mechanism differs by subtype; the article does not aggregate them. → [/findings/single-fuel-grid-cluster](/findings/single-fuel-grid-cluster)

**Port-Hinterland Friction — corrected 2026-07-18.** The original
trade-volume × LPI top five failed validation against observed CPPI
vessel-time data: only Indonesia remains in the main direct-measure
top five. The national proxy ranking is retired; the hinterland leg
remains unresolved. → [/findings/port-friction-trade-volume-cluster](/findings/port-friction-trade-volume-cluster)

**Social-Protection Readiness — corrected 2026-07-18.** Only three members of
the inherited named five survive the panel's own value order. Vanuatu and
Tajikistan outrank two named members but were omitted for a missing proxy leg.
All five named economies have documented COVID-19 cash-transfer responses;
zero comparable delivery outcomes are joined. The ranking is retired. →
[/findings/sp-shock-readiness-cluster](/findings/sp-shock-readiness-cluster)

## The remaining Screening-Result screens

**Water-Crop Pressure — corrected 2026-07-18.** The published set is the raw
top four in only two of seven runs. Direct available-water stress retains two
published members; direct FAOSTAT crop concentration retains none; and all five
crop-HHI leaders lack water-stress rows. The country ranking is retired. →
[/findings/water-crop-pressure-cluster](/findings/water-crop-pressure-cluster)

**School Heat Disruption.** Top-1 narrowing — only Cambodia is
parameter-stable. The top-5 fails the ±50% sensitivity gate. The
brief documents the parameter-sensitivity itself as the diagnostic;
the index's linear-tmax ramp is the wrong functional form per Lancet
Countdown indicator 1.1.5. → [/findings/school-heat-honest-narrowing](/findings/school-heat-honest-narrowing)

**Food-Price Climate Transmission.** Composite-index result dropped.
The usable screen is a joint qualifier: Lao PDR and Pakistan sit in
the top-N of both CPI inflation and agriculture-import exposure for
every N from 3 to 10; Bangladesh joins from N=5. Annual macro data are
too coarse for a climate-to-price transmission claim. →
[/findings/food-price-joint-qualifier](/findings/food-price-joint-qualifier)

**Access to Services.** An 8-DMC ADM1 pilot finds a stable top-4
access-stress set: Bangladesh, Cambodia, Lao PDR, and Pakistan.
Facility-count stress is not travel-time access; road-network
isochrones remain the policy-grade measure. →
[/findings/access-stress-pilot-cluster](/findings/access-stress-pilot-cluster)

**Air-Monitoring Observability.** A generated evidence ledger indexes
64 public-source summary rows and 214 supporting files, but the
claim-enabling QA counters remain zero for validated same-station
rows, station-level BMKG inspection logs/certificates/status rows,
complete monitor-grade rows, station-radius-ready economies, and
allowed coverage-claim rows. This is an evidence-gap result, not a
monitor-coverage estimate. → [/findings/pm25-observability-gap-cluster](/findings/pm25-observability-gap-cluster)

**Invisible Urbanization.** Papua New Guinea, Solomon Islands,
Afghanistan, Lao PDR, and Bangladesh hold the top urban-growth-from-
rural-base signal. The result is a proxy because official urban
definitions differ across economies. →
[/findings/invisible-urbanization-cluster](/findings/invisible-urbanization-cluster)

**Coastal Informal Risk.** Pakistan, Philippines, China, Bangladesh,
and Myanmar hold the top urban-informal-pressure positions. WDI slum
data are sparse, and the coastal flag is not yet a low-elevation
coastal-zone exposure measure. → [/findings/coastal-informal-cluster](/findings/coastal-informal-cluster)

**Flood-Market Access.** India, China, Indonesia, and Afghanistan hold
the stable top-4 flood-rural-exposure set. The current measure is
flood exposure plus rural population, not road-network disruption or
market isolation. → [/findings/flood-market-access-cluster](/findings/flood-market-access-cluster)

## The one Program Prospectus

**Climate-Health Workdays.** Three DMCs — Afghanistan, India,
Bangladesh — top the PM2.5 workday-pressure screen across every
parameter row. Top-5 narrowed honestly because the PM2.5-cap parameter
shifts the 4th and 5th positions. It is a Program Prospectus, not a
finished issue paper: the PM2.5 layer is computed, but the heat layer
and true workday-loss interpretation remain upgrade-pass work. →
[/findings/workday-loss-pressure-cluster](/findings/workday-loss-pressure-cluster)

## The one Prepared-Pipeline hold-back

**Digital Performance.** Stays at Prepared Pipeline. The Ookla Q1 2026
manifest and DuckDB SQL are committed for Philippines and Bangladesh
pilots, but the parquet aggregation has not been run. No speed,
latency, or coverage claim should appear until those files are fetched
and aggregated.

## The one Hypothesis hold-back

**MPI × Nighttime Lights.** Remains a Hypothesis in this repository.
OPHI MPI 2024 parsing is present, but the nighttime-lights ingestion,
zonal statistics, and coauthored external track are not reconciled here.
No MPI-light interpretation should be folded into this issue until that
lineage is brought back into the repo or explicitly retired.

## What §18 means for any reader

Every program in this issue carries `attestation_chain: ai-first`.
That label means:

- **Literature reviews** are AI-finalized rather than human-finalized.
  The owner has not line-by-line read every cited paper.
- **Pre-registrations** are AI-frozen. The freeze commits to a
  falsifiable claim before the next pipeline run, but the freezer is
  the AI under §18.1, not the human owner.
- **Internal review** is an AI critique-pass that argues against the
  artifact and responds in writing. It is not the supervisor's
  review.
- **External red-team review** is an AI synthesis from named
  candidate institutions' published methodological positions —
  KEMRI–Wellcome / WorldPop, HeiGIT, OPHI, KNOMAD, IZA, Lancet
  Countdown, IEA / Ember, World Bank teams (LPI, DECDG, SPJ, GFDRR,
  Findex), UNDP HDR, IRENA, WRI Aqueduct, IWMI, FAO AQUASTAT, OSCE
  Bishkek, ANU Devpolicy, Pacific Community, Nepal Rastra Bank, IDMC,
  UNICEF EAPRO, ADBI, UNCTAD, OECD ITF, CRED, UNDRR, NUS LKYSPP,
  IPA / J-PAL. **No individual reviewer at any of these institutions
  was contacted under §18.** The objections are AI-synthesized from
  each institution's public methodological stance; the responses are
  AI-written.
- **Maturity labels** under §18 are AI-applied. The PR label is
  honest *under §18*; it would not survive the pre-§18 gates without
  upgrade-pass work.

A reader who wants `human-final` work can look at the §18.5 upgrade-
pass scope in each program's `review-external.md` §5 — it lists
exactly what conversion would require.

## What stayed under non-suspendable rules

§18 does not suspend everything. The following gates apply equally
under §18:

- **Public data only** — every input traces to a public source.
- **Auditable end-to-end** — `manifest.sha256` pins every cache file;
  `versions.json` pins every external version.
- **Sensitivity at ±50%** — every program's sensitivity suite passed
  or honestly narrowed where a sensitivity suite exists. Screening
  programs are labeled SR precisely because their outputs are triage,
  not policy-grade findings.
- **Reproducibility from clean clone** — every pipeline runs from
  cache without API keys.
- **Ethics in full** — no individual identifiability; framings are
  measurement gap, not country deficiency.
- **Taste heuristics in full** — banned words checked, no composite-
  index headline, no causal language from screening signals.

## Four §16 amendments shipped this issue

This issue has four Constitutional amendments. They are public:

1. **§18 — AI-First Operating Mode** added 2026-04-25. The
   foundation of every "ai-first" attestation in this issue.
2. **§10.3 + §10.4 + §18.1 amendment** 2026-04-26. Replaces
   mandatory Zenodo DOI with a self-hosted permanent archive at
   the reporting-site domain. The Vercel-hosted site you are
   reading is the archive.
3. **§8.1 amendment** 2026-04-26. Suspends the WIP cap (1 PR + 3
   SR) under §18 ACTIVE. The cap was designed for human-attestation
   pacing; under AI-attestation the rationale doesn't apply. Caps
   automatically reactivate when §18 is reverted.
4. **§6.7 stopping-rule amendment** 2026-07-07. Makes claim reshaping
   mandatory after repeated zero-result evidence passes and treats a
   documented public-evidence absence as a first-class result where the
   lab is measuring observability gaps.

## What is not in this issue

One program remains at Hypothesis in this repository:
mpi-nighttime-lights. The track is live only as a reconciled external
paper path until the nighttime-lights code and data lineage are brought
back into this repo.

PSDQ extension to India and Indonesia: deferred to a future issue.
Both pipelines need new data sources fetched (HMIS via data.gov.in;
SATUSEHAT requires registration).

Sub-national disaggregation for most finished programs: many current
issue claims still operate at country level. ADM1 / ADM2 deferred to
per-program upgrade-passes unless the program's evidence packet already
states a lower valid unit.

— Raymond Adofina · 2026-07-07 · `attestation_chain: ai-first`
