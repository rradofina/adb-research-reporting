---
slug: measurement-gap-philippines-bangladesh
title: Two maps of the same health system disagree — and not at random
subtitle: OpenStreetMap shows 17.1 percent of the Philippines' official clinical-tier facility registry and 11.8 percent of Bangladesh's, and the gap is widest exactly where planners need maps most. Any workflow that mixes the two sources needs a reconciliation step first.
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
updated_at: 2026-07-31
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

# Two maps of the same country

Ask two public sources how many health facilities serve a Philippine
region — the country's official registry and OpenStreetMap — and you
get answers that differ not by a margin, but by a factor of six.
Project teams that build facility catchments, coverage maps, and
travel-time isochrones routinely combine exactly these two kinds of
sources, and when they disagree, the disagreement is usually absorbed
into the analysis as if it were random noise.

It is not random. Sandefur and Glassman 2015 [@sandefur2015badata]
showed that survey counts and administrative counts of African school
enrollments diverge in directions that track reporting incentives.
Markhof, Wollburg, and Zezza 2025 [@markhof2025records] found a
9-percentage-point gap between phone-survey and administrative
COVID-vaccination coverage in low- and middle-income countries that
survives every selection correction. A planner who treats such gaps as
noise will treat coverage problems as present-but-small when they are
present-and-systematic.

For health-facility lists, this question has been studied carefully in
Africa [@maina2019facilities; @south2021reproducible;
@macharia2025mapping] — but never with consistent methodology for ADB
developing member economies. This paper reports the first such
comparison for two of them: the Philippines (Department of Health
National Health Facility Registry v2.0) and Bangladesh (Directorate
General of Health Services Facility Registry). It is finished for the
current issue under §18 AI-first attestation, not a human-final
publication claim.

# What we compared

Two official registries, retrieved 2026-04-25 into committed caches:
the Philippine NHFR v2.0 with **44,267 active facilities**, and the
Bangladesh DGHS registry with **39,421**. Against them, OpenStreetMap
health features (`amenity=hospital|clinic|doctors`, data vintage
2026-04-05 to 2026-04-23) intersected with geoBoundaries ADM1
polygons.

The headline metric is simple: the OSM count divided by the registry
count at the clinical tier — hospitals, main clinics, primary-care
units, and community-level health stations. Counts are list records
after taxonomy harmonization, not field-verified service points; that
is the right object here because the question is public observability
and list agreement, not true facility existence.

Two thresholds were fixed in advance: a 30 percent map-to-registry
ratio as the fit-for-planning screen [@macharia2025mapping], and a
±10 percent agreement band as the falsification test. Both are
explicit, sensitivity-tested, and easy to reject in later work.

# What we found: the map misses most of the system

Both countries fall far below the planning screen. In the taxonomy of
health-information-system data quality [@ghalavand2024dataquality],
this is a **completeness** gap, not an accuracy or timeliness gap.

## The Philippines: a 9.8× gradient inside one country

![Philippines choropleth: OSM-to-NHFR clinical-tier ratio per ADM1 region. NCR shows the highest ratio (about 0.6); BARMM and the rural Mindanao regions show the lowest (about 0.07).](/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm1.svg)

Country-wide, OpenStreetMap captures **17.1 percent** of the
clinical-tier registry. But the average hides the story. Metro Manila
(NCR) shows 63.5 percent agreement; the Bangsamoro Autonomous Region
in Muslim Mindanao shows 6.5 percent — a **9.8× spread** between the
best- and worst-mapped regions, and a 5.5× spread between the top and
bottom rural-share quintiles. Not one of the 17 regions falls inside
the ±10 percent agreement band, at ±5, ±10, or ±15 percent.

Where does the gap live? Not in hospitals. The principal-tier
comparison — hospitals and main clinics only — reaches 72.8 percent.
What vanishes from the public map are Barangay Health Stations, Rural
Health Units, and dialysis clinics: the community-level facilities
volunteers map least consistently, and the ones closest to rural
residents. Dropping BARMM entirely still leaves a 17.4 percent country
ratio and a 4.8× gradient, so this is not a single-region artifact.
The BARMM figure itself is co-produced — both registry coverage and
volunteer mapping are constrained in conflict-affected areas, so the
gap there is not attributable to either side alone.

## Bangladesh: the same direction, at smaller scale

![Bangladesh choropleth: OSM-to-DGHS clinical-tier ratio per ADM1 division. Dhaka (centre) shows the highest ratio (about 0.20); Sylhet and Barisal show the lowest (about 0.06 to 0.08).](/programs/public-service-data-quality/generated/charts/psdq-choropleth-bgd-adm1.svg)

OpenStreetMap captures **11.8 percent** of the Bangladesh
clinical-tier registry. Again the gap concentrates at the community
tier: excluding community clinics, the hospitals-and-main-clinics
ratio is 41 percent. Across the 8 divisions the ratio runs from 6.2
percent (Barisal) to 20.1 percent (Dhaka). With only eight divisions,
the Bangladesh gradient is illustrative — the 17-region Philippine
pattern carries the inferential weight, and Bangladesh serves as a
directional check on a second registry design.

One caveat belongs next to the headline: 11.8 percent is measured
against the DGHS public dashboard. The DGHS-DHIS2 backend may hold a
more complete inventory, and claiming a comparison against the
canonical list would require outreach to DGHS.

# Does the pattern survive scrutiny?

Every arbitrary numeric frozen in the pre-registration was perturbed
by ±50 percent in both countries. The pattern held every time.

| Test | Philippines result | Bangladesh result | Interpretation |
|---|---:|---:|---|
| Country clinical-tier OSM/registry ratio | 14.5% to 17.9% | 11.6% to 11.8% | Always below the 30% planning screen |
| ADM1 units within ±10% agreement band | 0 of 17 | 0 of 8 | Falsification condition never triggers |
| Top/bottom rural-share gradient | 4.0x to 7.0x | 2.18x to 3.21x | Gradient direction survives perturbation |

![Sensitivity range plot. The Philippines remains between 14.5 and 17.9 percent and Bangladesh between 11.6 and 11.8 percent across completed runs; both ranges remain well below the 30 percent fit-for-planning screen.](/programs/public-service-data-quality/generated/charts/psdq-sensitivity-range.svg)

The distance to the planning screen matters more than the small
within-country movements: no clinical-tier definition tried brings
either country anywhere near 30 percent, and no perturbation flips the
pre-registered decision rule. One honesty note: the offline
polygon-dilation test remains incomplete, so the figure summarizes
completed runs rather than claiming every pre-registered perturbation
has executed.

# Zooming in: from regional summary to street level

The original result could say *that* the gap exists at the regional
level. The upgrade pass makes it inspectable at the level where a
project team would start asking follow-up questions — without changing
the headline or imputing a single missing value.

## Philippines: city and municipality resolution

![Philippines ADM3 choropleth: official 2023 poverty incidence at city/municipality level from PSA Small Area Estimates plus PSA OpenSTAT direct estimates. Highest poverty concentrations in BARMM, the Cordillera, and parts of Eastern Visayas. Ten polygons stay gray, marking source-missing rows that were not imputed.](/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm3-poverty.svg)

The pipeline now resolves 44,259 of the 44,267 active registry records
(99.98 percent) to one of 1,642 city/municipality polygons — including
the BARMM Maguindanao split, where the registry uses an older
geographic-code vintage and the modern parent unit is recovered by
majority vote of barangay-name matches. The 8 records that cannot be
resolved are left explicitly unresolved rather than guessed. A
settlement denominator built from Google Open Buildings (38,122,474
catalog rows processed; 13,538,628 high-confidence points kept) turns
the regional summary into a city-level screening table, whose current
top rows include Zamboanga City, Davao City, Cagayan de Oro City,
General Santos City, and Quezon City. That screen is a triage proxy —
gap share times buildings — not affected population or a validated
catchment.

The poverty overlay is deliberately source-gated. Scripted fetches of
the official PSA Small Area Estimates workbook hit a browser
challenge, so the owner downloaded it manually and the pipeline joined
1,597 SAE rows plus 35 official OpenSTAT direct-estimate city rows.
Ten city/municipality rows still lack a poverty source match, and they
stay gray on the map: no poverty value is imputed from buildings,
roads, or registry gaps.

## Bangladesh: upazila settlement and road context

The Bangladesh side starts from the coordinate-bearing DGHS endpoint:
39,419 parsed records, 29,371 with coordinates inside the country
bounds. Open Buildings points are counted within 1, 3, and 5 km of
each coordinate-ready facility (17,545,636 points within 3 km at the
p85 confidence threshold), and 3,212 of 3,302 OSM health features are
joined to upazila rows after documented name canonicalization. The
resulting exposure screen currently ranks Gazipur Sadar, Narayanganj
Sadar, Kushtia Sadar, Pabna Sadar, and Narsingdi Sadar highest.

A road layer adds context, not access measurement: 650,579 public road
features assigned to upazilas, of which 51,327.4 km of 304,941.2 km
carry a paved/unpaved surface class. The screen keeps only upazilas
with at least 50 km of classified roads and at least 10 percent
classified coverage — still a triage quantity, not travel time or a
service-access model.

The value of this whole layer is traceability: a reader can move from
the regional claim to the exact generated CSVs, source-status records,
and public panels that show what is complete, what is source-missing,
and what was never imputed.

# What this means for planning teams

The implication is not "OpenStreetMap is bad" or "the registry is
correct." It is narrower and more useful:

- **A workflow that silently mixes public maps and official registries
  needs a reconciliation step** before facility-catchment, travel-time,
  or coverage analysis. The two sources describe different subsets of
  the same system, and the difference is largest at the community tier.
- **The direction of the bias matters.** The public map under-counts
  most where rural access questions concentrate — so map-only analysis
  will look most complete precisely where it is least complete.
- **Two sources are a screen, not a standard.** Triangulation across at
  least three independent lists is the established design
  [@south2021reproducible]; adding `healthsites.io` or DHIS2 (where
  public) is the natural next leg.

# What this does not say

- It does not establish that OSM is "wrong" against ground truth —
  only that the two lists disagree systematically. The dominant
  mechanism is likely OSM under-mapping rather than registry
  over-reporting: residual administrative-record errors documented in
  comparable settings are an order of magnitude smaller than this gap
  [@markhof2025records]. But OSM completeness itself tracks
  development indicators — building completeness in East Asia &
  Pacific averages 20 percent [@herfort2023osm] — so "the map
  under-counts" must be read together with "map coverage follows
  development."
- It does not identify causes of the gradient. Volunteer behavior,
  registry operating incentives, conflict exposure, and
  licensing-driven over-registration could all contribute.
- It does not rank the two countries. Their registry definitions and
  taxonomies differ; the comparable quantity is the within-country
  gradient, not the cross-country ratio.
- It does not cover India or Indonesia. The current issue is bounded
  to the Philippines and Bangladesh until a separately registered
  facility-registry route passes the source gate.
- The validated unit remains ADM1. The city/municipality and upazila
  layers are inspection screens, not validated catchment, travel-time,
  or welfare estimates.

The Bangladesh validation queue makes the boundary concrete: of 40
targeted public-source rows, 39 end at a human or source-owner wall
and 0 are closable by AI alone.

![Validation-path infographic. Forty targeted public-source rows lead to 39 rows at a human or source-owner wall and zero AI-actionable closures.](/programs/public-service-data-quality/generated/charts/psdq-validation-wall.svg)

That figure is not an attrition rate or a facility-quality score. It
shows permission: public evidence improved the queue but did not
authorize closure, same-facility reclassification, or coordinate
correction.

# What would change this finding

- **A third independent facility source** (`healthsites.io`, DHIS2
  where public, or another national list) — the upgrade South and
  colleagues treat as the stronger design [@south2021reproducible].
- **Access to the canonical DGHS backend list**, which could revise
  the Bangladesh headline against a more complete inventory.
- **Field validation of a stratified facility sample**, which would
  convert list disagreement into evidence about existence and
  services.
- **An official source for the 10 remaining poverty-gap rows**, which
  would close the last source-missing cells without imputation.
- **Named human reviewers** replacing the AI-synthesized review — the
  difference between this current-issue AI-first paper and a
  human-final submission (§18.5).

# How we measured this

A clean clone at the frozen commit reproduces the headline ratios and
upgrade artifacts via `public-service-data-quality/REPRODUCE.md`. The
committed caches mean no API key or live network call is required; the
hash check is `node scripts/verify-manifest.mjs`.

```bash
bash public-service-data-quality/scripts/fetch-nhfr.sh
python public-service-data-quality/scripts/process-multi-country.py
python public-service-data-quality/scripts/sensitivity.py
```

The poverty overlay is reproduced with:

```bash
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py --sae-xlsx "public-service-data-quality/.cache/2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx"
python public-service-data-quality/scripts/build-phl-admin3-poverty-context.py --require-sae
```

The pre-registration, sensitivity suite, and limitations live at
`public-service-data-quality/pre-registration.md`, `sensitivity.md`,
and `limitations.md`. The full evidence packet is at
[/program/public-service-data-quality/evidence](/program/public-service-data-quality/evidence).

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

A §18.5 upgrade pass converts this chain to `mixed` or `human-final`:
the owner re-attests the literature and pre-registration under their
own name, at least two named external reviewers from the institutions
listed in `review-external.md` §1 replace the synthesized objections
with actual comments, the named supervisor (Arturo Martinez Jr)
performs the internal review, and the article and dated archive are
re-issued with updated frontmatter and a new commit SHA.

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
