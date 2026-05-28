---
slug: measurement-gap-philippines-bangladesh
title: The OSM-vs-registry gap in Philippine and Bangladeshi health facilities
subtitle: OpenStreetMap covers 17.1 percent of the Philippine national health-facility registry and 11.8 percent of the Bangladeshi one — both well below the 30 percent fit-for-planning threshold. The current upgrade drills below ADM1 into Philippine city/municipality and Bangladeshi upazila views, keeping source gaps explicit.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [PHL, BGD]
topics: [measurement-gap, public-service-data-quality, OSM, health-facility-registry]
program: public-service-data-quality
maturity: PR
abstract: >
  OpenStreetMap captures 17.1 percent of the Philippine clinical-tier
  national health-facility registry and 11.8 percent of the
  Bangladeshi one — both pilots well below the 30-percent
  fit-for-planning threshold of Macharia and colleagues 2025. The
  gap is steep within the Philippines: a 9.8x best-to-worst gradient
  across 17 administrative regions (63.5 percent in NCR, 6.5 percent
  in BARMM) and a 5.5x gradient between the top and bottom
  rural-share quintiles. The Bangladesh division-level gradient is
  directionally consistent but illustrative only (N=8). No
  administrative unit in either country agrees within 10 percent;
  the pattern survives every parameter in a plus-or-minus 50 percent
  sensitivity suite. The upgrade pass adds a Philippine ADM3 Open
  Buildings denominator, Bangladeshi facility-buffer and road-context
  layers, and an owner-downloaded official Philippines PSA Small Area
  Estimates poverty overlay — keeping 10 source-missing ADM3 rows
  and 8 unresolved BARMM facility records explicit and non-imputed.
  Published under CONSTITUTION.md §18 (AI-First Operating Mode): the
  literature, pre-registration, internal review, and red-team review
  are AI-attested. The article is upgrade-eligible to a human-final
  attestation chain via §18.5.
doi:
published_at: 2026-04-25
updated_at: 2026-05-05
references:
  - maina2019facilities
  - south2021reproducible
  - macharia2025mapping
  - sandefur2015badata
  - markhof2025records
  - herfort2023osm
  - zhao2022datagaps
  - ghalavand2024dataquality
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18 (§9.1 + §9.2)
---

# The question

Project teams that build facility catchments, service-coverage maps,
and travel-time isochrones routinely combine public maps with official
registries. When the two sources disagree — and they do — the
disagreement is typically absorbed into the analysis as if it were
random measurement noise. It is not random. Sandefur and Glassman 2015
[@sandefur2015badata] documented that household-survey counts and
administrative-record counts of African school enrollments diverge in
directions that correlate with reporting incentives, not with
measurement noise. Markhof, Wollburg, and Zezza 2025
[@markhof2025records] documented a 9-percentage-point persistent gap
between phone-survey and administrative COVID-vaccination coverage in
LMICs that survives correction for respondent-selection effects. A
planner who treats the gap as noise will treat coverage problems as
present-but-small when they are present-and-systematic.

The corresponding question for facility lists in the Asia-Pacific has
not been answered with consistent methodology. The African-side
methodological literature is well established — Maina and colleagues
2019 [@maina2019facilities] assembled a 98,745-facility cross-country
spatial database from national master facility lists; South and
colleagues 2021 [@south2021reproducible] compared MOH lists, the
WHO-KEMRI-Wellcome dataset, and OpenStreetMap-derived `healthsites.io`
across Africa, shipping the `afrihealthsites` R tools as a
reproducible reference; Macharia and colleagues 2025
[@macharia2025mapping] called for a renewed cross-country open
facility dataset. No equivalent methodologically rigorous work
exists for ADB developing member economies.

This article reports the first such comparison for two DMCs:
Philippines (Department of Health National Health Facility Registry
v2.0) and Bangladesh (Directorate General of Health Services Facility
Registry). It is finished for the current issue under §18 AI-first
attestation, not a human-final publication claim. The pre-registration
is at `public-service-data-quality/pre-registration.md` in the
repository; the sensitivity suite is at `sensitivity.md`; the
limitations are at `limitations.md`.

# What this paper adds

The contribution is deliberately narrow. It does not claim to audit
health-system quality, service readiness, staffing, medicine stock, or
patient access. It adds three pieces that are useful before any of
those harder claims are attempted:

1. **A registry-to-map reconciliation design for ADB DMCs.** The
   African health-facility-list literature already shows how hard it
   is to keep public facility inventories complete, current, and
   openly licensed [@maina2019facilities; @south2021reproducible;
   @macharia2025mapping]. This paper ports that measurement question
   to two Asia-Pacific registries with public, reproducible code.
2. **A within-country gradient, not a country league table.** The
   comparable signal is whether community-level and rural-facing
   facilities disappear from public maps more often than higher-tier
   facilities. The Philippines carries the stronger inferential weight
   because it has 17 ADM1 units; Bangladesh is kept as a second
   registry design and a directional check.
3. **A falsifiable planning threshold.** The paper uses a 30 percent
   map-to-registry ratio as a fit-for-planning screen and a ±10 percent
   agreement band as the falsification test. Those thresholds are
   explicit, sensitivity-tested, and easy to reject in later work.
4. **A granular audit layer after the headline result.** The upgrade
   pass adds Philippine ADM3 city/municipality denominators, Bangladeshi
   upazila settlement and road context, and a source-gated poverty-status
   layer. These additions do not change the headline ADM1 ratio; they
   make the measurement problem inspectable at the level where a project
   team would start asking follow-up questions.

This is why the paper should be read as a measurement-gap brief. The
policy implication is not "OSM is bad" or "the registry is correct."
The implication is that a planning workflow that silently mixes public
maps and official registries needs a reconciliation step before it is
used for facility catchment, travel-time, or coverage analysis.

# The data

Two registries:

- **Philippines DOH NHFR v2.0**, retrieved 2026-04-25, 44,267 active
  facilities across 23 paginated API responses (committed cache;
  `versions.json` pin).
- **Bangladesh DGHS Facility Registry**, retrieved 2026-04-25, 39,421
  active facilities across 20 paginated responses.

One reference for OSM:

- **OpenStreetMap** via Overpass, `amenity=hospital|clinic|doctors`
  intersected with `geoBoundaries` gbOpen ADM1 polygons. OSM data
  vintage window 2026-04-05 to 2026-04-23.

Three granular context layers were added after the initial two-country
screening result:

- **Google Open Buildings V3** point shards for Bangladesh and the
  Philippines, used as settlement denominators after precision
  thresholding and polygon assignment.
- **HeiGIT / HDX Bangladesh road-surface data**, used only as an
  upazila road-context layer after minimum classified-road coverage
  filters.
- **Philippines PSA poverty sources**, using the owner-downloaded official
  2023 city/municipality SAE Excel plus OpenSTAT direct-estimate rows for
  35 city/HUC units.

The headline metric is the **clinical-tier OSM/registry ratio at
ADM1**: OSM count divided by registry count, where the registry's
"clinical-tier" comprises hospitals, main clinics, primary-care units,
and community-level health stations. Across the Philippines, the
clinical-tier set is 19 of NHFR's 44 facility types; across Bangladesh,
the analog is the DGHS hospitals + clinics + community-clinics + UHC
union.

**Source note.** Counts are registry records and OSM points/polygons
after taxonomy harmonization. They are not unique physical-service
delivery points verified by field audit. This is appropriate for the
paper's question because the object being measured is public
observability and list agreement, not true facility existence.

# The finding

Both pilots fall well below the 30-percent fit-for-planning
threshold Macharia and colleagues 2025 [@macharia2025mapping] propose
for treating a facility list as plan-ready, mapped onto the 14-
dimension health-information-system data-quality taxonomy of
Ghalavand and colleagues 2024 [@ghalavand2024dataquality] this is a
**completeness** gap primarily, not an accuracy or timeliness gap.

## Philippines

![Philippines choropleth: OSM-to-NHFR clinical-tier ratio per ADM1 region. NCR shows the highest ratio (about 0.6); BARMM and the rural Mindanao regions show the lowest (about 0.07).](/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm1.svg)

OSM captures **17.1 percent** of the Philippines clinical-tier
registry country-wide. Across the 17 ADM1 regions, the ratio ranges
from **6.5 percent (BARMM)** to **63.5 percent (NCR)** — a 9.8x
ratio between the worst- and best-mapped regions, and a 5.5x ratio
between the top and bottom quintile means. Every region (17 of 17) is
outside the pre-registered ±10 percent agreement band. The
"within-X-percent" falsification condition does not trigger at ±5,
±10, or ±15 percent.

The principal-tier ratio (the narrower hospitals + main clinics
comparison) is 72.8 percent, much closer to agreement. The bulk of
the gap is in community-level facilities — Barangay Health Stations,
Rural Health Units, dialysis clinics — which OSM volunteers map less
consistently than larger institutions. A leave-one-out check dropping
BARMM yields a country ratio of 17.4 percent and a top/bottom
quintile gradient of 4.8x: the headline pattern is not a
BARMM-only phenomenon.

The BARMM result is co-produced. Both registry coverage and OSM
volunteer mapping are constrained in conflict-affected regions —
the gap there is not attributable to either side alone.

## Bangladesh

![Bangladesh choropleth: OSM-to-DGHS clinical-tier ratio per ADM1 division. Dhaka (centre) shows the highest ratio (about 0.20); Sylhet and Barisal show the lowest (about 0.06 to 0.08).](/programs/public-service-data-quality/generated/charts/psdq-choropleth-bgd-adm1.svg)

OSM captures **11.8 percent** of the Bangladesh clinical-tier
registry. The principal-tier ratio (CC-excluded: hospitals + main
clinics) is 41 percent — the bulk of the headline gap is the
community-clinic tier, which OSM volunteers do not typically map.
Across the 8 divisions, the clinical-tier ratio ranges from
**6.2 percent (Barisal)** to **20.1 percent (Dhaka)**. The
Bangladesh gradient is illustrative (N=8 divisions; below the
threshold for any rank-based test to be informative); the
Philippine 17-region pattern carries the inferential weight.

The 11.8 percent headline is OSM-vs-DGHS-public-dashboard. The
DGHS-DHIS2 backend may carry a more complete inventory; outreach
to DGHS is required to claim a comparison against the canonical
DGHS list.

# What the granular upgrade adds

The original article could establish that the registry-map gap exists
at ADM1. It could not show where a reader should inspect the problem
inside a region or division. The current evidence package adds three
local-readiness layers while keeping the same non-claim discipline.

## Philippines ADM3 and poverty-source status

![Philippines ADM3 choropleth: official 2023 poverty incidence at city/municipality level from PSA Small Area Estimates plus PSA OpenSTAT direct estimates. Highest poverty concentrations in BARMM, the Cordillera, and parts of Eastern Visayas. Ten polygons stay gray, marking source-missing rows that were not imputed.](/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm3-poverty.svg)

The Philippine pipeline now assigns Google Open Buildings points to
1,642 PSA/NAMRIA ADM3 city/municipality polygons. It processes
38,122,474 catalog rows, assigns 36,447,136 building points to ADM3,
and keeps 13,538,628 p85-threshold building points for the chart-ready
denominator. The NHFR code join now resolves 44,259 of 44,267 active
facility records to ADM3 (99.98 percent), and 37,384 of 37,392
clinical-tier records (99.98 percent). The chain of resolvers is direct
code matching, PSA PSGC correspondence-code matching, deterministic
code-vintage rules, and a barangay-name lookup against PSA/NAMRIA 2023
ADM4 polygons that resolves the BARMM Maguindanao split (where NHFR
uses an older PSGC vintage for several cities/municipalities; the
modern parent ADM3 is found by majority vote of barangay-name matches
per NHFR ctymuncode). The remaining 8 NHFR records — all in a single
ctymuncode whose facility names do not contain a recognizable barangay
name — are left explicitly unresolved as a source-quality residue and
are not imputed.

That upgrade turns the Philippines result from a regional summary into
a city/municipality inspection table. The top ADM3 rows by the current
gap-building screen include Zamboanga City, Davao City, Cagayan de Oro
City, General Santos City, and Quezon City. The measure is a screening
proxy: registry-map gap share multiplied by p85 Open Buildings counts.
It is not affected population, demand, welfare loss, or a validated
facility catchment.

The poverty layer is deliberately source-gated. The official PSA 2023
city/municipality Small Area Estimates Excel attachment is the preferred
source. Scripted fetches hit a PSA/Cloudflare browser challenge, so the
owner manually downloaded the listed workbook from the PSA page and Codex
seeded the deterministic cache. The generated poverty-context file now
joins 1,597 SAE rows and 35 official OpenSTAT direct-estimate city/HUC
rows, leaving 10 ADM3 rows without a poverty source match. No poverty
value is imputed from buildings, roads, OSM, or registry gaps.

## Bangladesh upazila settlement and road context

The Bangladesh upgrade starts from the richer coordinate-bearing DGHS
public-facilities endpoint. The cached pull parses 39,419 records and
finds 29,371 records with coordinates inside Bangladesh bounds. Google
Open Buildings points are then assigned to coordinate-ready facilities
within 1 km, 3 km, and 5 km buffers, with p85 and p90 confidence
thresholds kept separate. At the p85 threshold, 17,545,636 building
points sit within 3 km of a coordinate-ready DGHS facility.

A separate upazila pass assigns 3,302 OSM health features to
geoBoundaries ADM3 polygons and joins 3,212 of those features to DGHS
upazila rows after documented name canonicalization. The exposure proxy
combines the active clinical facility gap with the 3 km p85 Open
Buildings denominator. Current top rows include Gazipur Sadar,
Narayanganj Sadar, Kushtia Sadar, Pabna Sadar, and Narsingdi Sadar.

The road layer adds context, not access measurement. It assigns 650,579
HeiGIT / HDX Bangladesh road features to upazilas by representative
point. Of 304,941.2 km assigned OSM-length road lines, 51,327.4 km have
a paved/unpaved surface class. The joined service-gap screen keeps only
upazila rows with at least 50 km classified road length and at least 10
percent classified-surface coverage. The resulting road-context score
is still a triage quantity, not travel time, poverty exposure, or a
service-access model.

The main value of this upgrade is not a new headline number. It is
traceability. A reader can now move from the ADM1 claim to the exact
generated CSVs, source-status JSON, and public UI panels that show what
is complete, what remains source-missing, and which values are not imputed.

# The sensitivity suite

The pre-registration freezes five arbitrary numerics. Every one was
tested at ±50 percent in both DMCs.

For the Philippines, the country clinical-tier ratio ranges 14.5
percent to 17.9 percent across the suite; the top-quintile to
bottom-quintile gradient ranges 4.0x to 7.0x; the within-band
falsification count remains 0 of 17 ADM1 units at every threshold
tested (±5 percent, ±10 percent, ±15 percent).

For Bangladesh, the country clinical-tier ratio ranges 11.6 percent
to 11.8 percent across the suite (a 0.2 percentage-point span across
all keyword-set perturbations — exceptionally stable); the gradient
ranges 2.18x to 3.21x at the 20-percent and 10-percent quintile sizes
respectively; the within-band falsification count remains 0 of 8
divisions at every threshold tested.

No row in the suite flips the §8 decision rule in either DMC. The
headline pattern survives every parameter perturbation tried.

| Test | Philippines result | Bangladesh result | Interpretation |
|---|---:|---:|---|
| Country clinical-tier OSM/registry ratio | 14.5% to 17.9% | 11.6% to 11.8% | Always below the 30% planning screen |
| ADM1 units within ±10% agreement band | 0 of 17 | 0 of 8 | Falsification condition never triggers |
| Top/bottom rural-share gradient | 4.0x to 7.0x | 2.18x to 3.21x | Gradient direction survives perturbation |

The table is intentionally compact: it shows the three checks a reader
needs before deciding whether the headline is robust or just a product
of arbitrary thresholds.

# What this result cannot establish

The full list is in `limitations.md`. The most important non-claims:

- The result does not establish that OSM is "wrong" relative to a
  ground truth. It establishes that OSM and the registry disagree
  systematically. The dominant mechanism is likely OSM under-mapping
  rather than registry over-reporting: Markhof, Wollburg, and Zezza
  2025 [@markhof2025records] documented residual administrative-record
  gaps of 9 percentage points in LMIC vaccination data, an order of
  magnitude smaller than the gap reported here. But the registry-OSM
  gap is itself partly an HDI-correlated artifact —
  Herfort and colleagues 2023 [@herfort2023osm] document that OSM
  building completeness in East Asia & Pacific averages 20 percent
  globally, so the "OSM under-counts" reading must be paired with
  the complementary "OSM coverage tracks development indicators."
- The result does not establish causal mechanisms for the gradient.
  Volunteer behavior, registry operating-cost incentives, conflict
  exposure, and licensing-driven over-registration could all
  contribute.
- The result does not produce a country-quality ranking. The
  Philippines and Bangladesh registry definitions and facility
  taxonomies differ; the within-country gradient is the comparable
  quantity, not the headline ratio across countries.
- The result is two-source. South and colleagues 2021
  [@south2021reproducible] establish that triangulation across at
  least three independent sources (MOH list, WHO-KEMRI dataset, OSM-
  derived `healthsites.io`) is the methodological standard. Adding
  `healthsites.io` and DHIS2 (where deployed) as the third leg is
  the §18.5 upgrade-pass step before any human-final attestation.
- The result does not yet cover India or Indonesia. The
  pre-registration scopes this gate to PHL + BGD only. India (HMIS)
  and Indonesia (SATUSEHAT) pipelines remain TODO until their public or
  owner-provisioned facility-registry paths pass the source gate.
- The headline aggregation unit remains ADM1: PHL regions and BGD
  divisions. The upgrade pass now adds PHL ADM3 and BGD upazila context,
  but those lower-level screens are still inspection layers. They are
  not validated catchment, travel-time, or welfare estimates.

# What would make this human-final

A human-final version should not simply polish this draft. It should
raise the evidentiary standard in four places:

| Upgrade | Why it matters |
|---|---|
| Add a third facility source such as healthsites.io, DHIS2 where public, or another national list | South and colleagues 2021 treat triangulation as the stronger design, not a two-list comparison [@south2021reproducible]. |
| Convert the new PHL ADM3 and BGD upazila screens into validated local analysis | Facility-access decisions are local; the current local screens are source-gated context layers, not field-validated catchments. |
| Hand-check a stratified sample of matched and unmatched facilities | The current design measures list disagreement; it does not validate whether the listed facility exists and provides clinical services. |
| Review the 10 remaining Philippines ADM3 poverty-source gaps and decide whether a separate official source resolves them | The PSA SAE workbook is now joined, but a small set of source-missing rows remains explicit and non-imputed. |
| Replace AI-synthesized review with actual named readers | That is the difference between a current-issue AI-first paper and a human-final submission. |

# Attestation chain

This article is published under `CONSTITUTION.md` §18 (AI-First
Operating Mode), ACTIVE since 2026-04-25. Specifically:

- **Literature review** (`literature.md`): AI-finalized under §18.1.
- **Pre-registration** (`pre-registration.md`): AI-frozen 2026-04-25
  under §18.1. Attestation chain `ai-first`.
- **Sensitivity suite** (`sensitivity.md`, `sensitivity-runs.json`):
  deterministic computation, non-suspendable. Run for both PHL and
  BGD.
- **Internal review** (`review-internal.md`): AI critique-pass under
  §9.1 and §9.2 of the Constitution as suspended by §18.1.
- **External red-team review** (`review-external.md`): AI synthesis
  under §18.4 from the published methodological positions of named
  candidate institutions (KEMRI–Wellcome / WorldPop network, HeiGIT,
  World Bank DECDG / SPI, OPHI, PIDS, BIDS). **No individual
  reviewer was contacted.** The objections in §3 of
  `review-external.md` are AI-synthesized, not actual reviewer
  feedback.
- **Permanent archive (§10.3)**: the self-hosted evidence packet at
  [/program/public-service-data-quality/evidence](/program/public-service-data-quality/evidence)
  renders every gate artifact and is the citation handle for this
  work. Optional Zenodo DOI deposition remains available for venues
  that require an external DOI; not used here.
- **Maturity label**: finished for the current issue (internal PR code)
  under §18 AI-first attestation.

# What an upgrade-pass looks like

A subsequent §18.5 upgrade-pass converts the `ai-first` chain to
`mixed` or `human-final` by:

1. The owner reading each cited paper line-by-line and re-attesting
   `literature.md` with a human-signed commit message.
2. The owner re-freezing `pre-registration.md` §10 with their name.
3. Recruiting at least two named external reviewers from the
   institutions listed in `review-external.md` §1, sending the packet
   at `review-packets/public-service-data-quality-2026-04-25/`,
   collecting written feedback, and replacing `review-external.md`
   §3 verbatim with their actual comments.
4. Forwarding the packet to the named supervisor (Arturo Martinez Jr)
   for actual internal review, replacing `review-internal.md` §2
   verbatim with their comments.
5. Re-issuing the article and the dated archive at
   [/program/public-service-data-quality/evidence](/program/public-service-data-quality/evidence)
   with frontmatter updated to `attestation_chain: human-final` (or
   `mixed`) and a new commit SHA.

# Reproduction

A clean clone of the repository at the frozen commit hash reproduces
the headline ratios and current upgrade artifacts by following
`public-service-data-quality/REPRODUCE.md`. The minimal headline-ratio
commands are:

```bash
bash public-service-data-quality/scripts/fetch-nhfr.sh
python public-service-data-quality/scripts/process-multi-country.py
python public-service-data-quality/scripts/sensitivity.py
```

The committed cache means no API key or live network call is required.
The hash check is `node scripts/verify-manifest.mjs`. The Bangladesh
DGHS pull is committed in `.cache/bgd_dghs_p{1..20}.json`; the
Philippine NHFR pull is in `.cache/nhfr_p{1..23}.json`.

The current poverty-source-status overlay is reproduced with:

```bash
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py --sae-xlsx "public-service-data-quality/.cache/2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx"
python public-service-data-quality/scripts/build-phl-admin3-poverty-context.py --require-sae
```

The expected status with the owner-downloaded official PSA SAE Excel is
`sae_city_municipal_join`.

# Acknowledgments

Per `review-external.md` §7 under `CONSTITUTION.md` §18.4:

> This article's red-team review was performed under §18.4 (AI-First
> Operating Mode) by AI synthesis against the published methodological
> positions of KEMRI–Wellcome / WorldPop network, HeiGIT, World Bank
> DECDG / SPI, OPHI Oxford, PIDS Manila, and BIDS Dhaka. No individual
> reviewer is named because none was contacted under §18. The article
> is upgrade-eligible to a human-final attestation chain via §18.5.

# Citations

The full citation list is in `references.bib` at the repository root.
Keys cited above:
`maina2019facilities`, `south2021reproducible`, `macharia2025mapping`,
`sandefur2015badata`, `markhof2025records`, `herfort2023osm`,
`zhao2022datagaps`, `ghalavand2024dataquality`.

— Raymond Adofina · 2026-04-25 · `attestation_chain: ai-first`
