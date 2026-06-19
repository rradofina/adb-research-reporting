# Limitations — Public Service Data Quality

`attestation_chain: ai-first`

Status: **§18 AI-finalized — 2026-04-25.** Updated to incorporate
the unresolved reviewer objections from `review-external.md` §5
under `CONSTITUTION.md` §18.4.

Per `CONSTITUTION.md` §6.5 and §9.3. This file is included verbatim in
the published article's Limitations section. Reviewer objections that
the owner cannot resolve will be appended to §5 below verbatim, with
the reviewer's permission.

---

## 1. What this result cannot establish

- The result does not establish that OSM is wrong. It establishes that
  OSM and the official national registry disagree, and the disagreement
  is systematic by ADM1 rural share. A registry could itself be biased
  upward for donor-reporting reasons (`sandefur2015badata`), in which
  case the gap reflects registry over-statement rather than OSM
  under-statement. Without a third independent source, the direction
  of the gap is not attributable to one side.
- The result does not establish causal mechanisms. It does not separate
  OSM volunteer behavior, registry operating-cost incentives, conflict
  exposure, or licensing-driven over-registration as drivers of the
  observed gap.
- The result does not produce a country-quality ranking. Per Constitution
  §13.3 and §14, the framing is measurement gap, observability gap,
  coverage gap. The two pilot DMCs (PHL, BGD) are not comparable to each
  other on the headline ratio because their registry definitions and
  facility taxonomies differ; the within-country rural-urban gradient is
  the comparable quantity, and the magnitude of that gradient is not the
  basis for ranking.

## 2. Source-side limitations

- **OSM vintage drift.** OSM counts come from the access-services
  pipeline cache, with `osm_timestamp` per row ranging 2026-04-05 to
  2026-04-23. NHFR (PHL) and DGHS (BGD) were fetched 2026-04-25. The
  date misalignment is up to 20 days; OSM is continuously edited. A
  publication-grade rerun aligns retrievals within a single calendar
  week and pins OSM to a Geofabrik or Overture monthly snapshot per
  Constitution §11.
- **Registry completeness assumption.** The OSM/registry ratio assumes
  the registry is closer to ground truth than OSM. This is plausible
  (DOH and DGHS have regulatory authority and licensing implications)
  but not guaranteed (`sandefur2015badata`). A publication-grade rerun
  triangulates against DHIS2 (where deployed) and against
  survey-enumerated facility lists (PSA 2020 census, BBS Health Survey,
  PhilHealth provider directory).
- **Factype mapping is imperfect.** OSM `amenity=hospital|clinic|doctors`
  does not have a 1:1 mapping to NHFR's 44 factypes or DGHS's
  taxonomy. The CLINICAL_FACTYPES set is a defensible best-effort
  bucket; the sensitivity suite shows the headline ratio range is
  14.5%–17.3% across reasonable factype-set choices for PHL.
- **Region 18 = Negros Island Region** was abolished in 2017 but DOH
  still uses regcode 18 in NHFR. Manual mapping of 4 provcodes is
  preserved as a baseline; dropping the manual splits shifts the country
  ratio from 17.1% to 17.9% (`sensitivity-runs.json` row `nir_mapping_dropped`).
- **BGD division-level granularity.** Bangladesh has 8 divisions (the
  upper administrative tier); the comparable PHL granularity is 17
  regions. A fairer cross-country granularity would be ADM2 (PHL
  provinces vs. BGD districts). ADM2 is TODO and is not in the SR → PR
  gate request.

## 3. Method-side limitations

- **Statistical inference is preliminary.** The Mann-Whitney
  rank-sum test on the rural-urban gradient is reported but the small
  N (17 regions in PHL, 8 divisions in BGD) limits power. A
  publication-grade rerun should report bootstrap confidence intervals
  on the gradient, not just a p-value.
- **No HDI control.** The pre-registered claim refers to "low-HDI
  ADM1 units." The current pipeline uses rural-share as a proxy (PSA
  2020 census). Subnational HDI from `globaldatalab.org/shdi` is the
  more direct quantity and is TODO for the publication-grade rerun.
- **Sensitivity to OSM-Overpass query window.** Strict ADM1-polygon
  clip at dilate=0 km is the baseline. A buffer of 1–5 km would
  redistribute facilities across boundaries and shift per-ADM1 counts.
  The dilate-buffer sensitivity row in `sensitivity.md` is TODO and
  requires a live Overpass rerun.

## 4. DMC-coverage limitations

The SR → PR gate request covers PHL and BGD only. India (HMIS) and
Indonesia (SATUSEHAT) pipelines are not yet built. The article and the
`results.md` headline are explicit that the cross-DMC pattern is
documented in two DMCs, not four.

## 5. Reviewer objections quoted verbatim

Per `review-external.md` §5 under `CONSTITUTION.md` §18.4. The
objections below are AI-synthesized from each candidate institution's
published methodological position. **No individual reviewer was
contacted under §18.** This section is upgrade-eligible: when an
actual reviewer returns written comments, the relevant entries are
replaced verbatim with their feedback.

### 5.1 From C-1 (KEMRI–Wellcome / WorldPop network), synthesized

> The afrihealthsites methodology recommends triangulation across at
> least three independent sources — MOH list, WHO-KEMRI dataset, and
> OSM-derived `healthsites.io`. The PSDQ pilot uses two: NHFR/DGHS
> and OSM. Without a third source, the OSM/registry gap is
> directional but not adjudicable.

### 5.2 From C-1 (KEMRI–Wellcome / WorldPop network), synthesized

> The Africa-side cross-country databases were built via national
> ministry outreach, not solely public pulls. The ADB DMC analysis
> would benefit from outreach to PHL DOH and BGD DGHS to confirm
> whether the public-pull NHFR / DGHS represents the canonical
> official list.

### 5.3 From C-2 (HeiGIT, Heidelberg), synthesized

> An HDI scatter plotting OSM-health/registry against
> `herfort2023osm` building-completeness percentile would let the
> reader see whether health-facility coverage is materially
> different from underlying OSM coverage in each country.

### 5.4 From C-4 (OPHI, Oxford), synthesized

> Aggregation should occur where capability is delivered. For health
> facility access, that is approximately the catchment-area level
> (ADM2 or sub-ADM2 in PHL). The current ADM1 aggregation is honest
> about its unit-of-analysis but should upgrade to ADM2 in any
> publication-grade rerun.

### 5.5 From C-6 (BIDS, Dhaka), synthesized

> The DGHS public dashboard captures a subset of the canonical DGHS
> DHIS2 instance. The 11.8% headline is OSM-vs-DGHS-public-dashboard,
> not OSM-vs-DGHS-canonical. Outreach to DGHS is required for any
> §18.5 upgrade to claim canonical comparison.

## 6. Banned framings — explicit non-claims

Per `CONSTITUTION.md` §13.3 and §14:

- This result does **not** rank DMCs.
- This result does **not** describe DMCs as deficient.
- This result does **not** support causal inference from the screening
  signal alone.
- The article does not use any banned word from §14.

## 7. 2026-05-07 addendum — limitations on the new artifacts

These items are added in response to the Mode A review iteration on
the 2026-05-05 to 2026-05-07 work (PSA SAE poverty overlay,
choropleth maps, publication ladder, BARMM Maguindanao resolver,
review packet).

### 7.1 BARMM Maguindanao resolver residue

Eight NHFR records remain unresolved at the ADM3 level, all in
ctymuncode `1908807`. Their facility names (clinic / lying-in /
hospital) do not contain a recognizable barangay name, so the
deterministic barangay-name resolver in `scripts/inspect-barmm-codes.py`
cannot vote. One phantom NHFR municipality is therefore undercounted
in the ADM3 view by exactly these 8 records (8 of 8 are clinical-
tier). Resolution requires DOH outreach or a manual gazette cross-
check, both owner-only under §18.5.

### 7.2 BARMM resolver depends on a Philippine-specific regex pattern set

The barangay-name extractor in `scripts/inspect-barmm-codes.py`
matches NHFR facility-name suffixes (`{name} BARANGAY HEALTH STATION`,
`{name} RURAL HEALTH UNIT`, `{name} BIRTHING HOME`, etc.). The set is
tuned to Philippine NHFR conventions; it is documented in the
script's docstring and is treated as a build-time constant. Records
whose facility names follow a different pattern (e.g., commercial
clinics with brand names) will not vote — the per-ctymuncode
majority winner can still resolve them if other records in the same
group have recognizable patterns. The regex set is not exhaustive
and is upgrade-pass scope.

### 7.3 Geometry simplification tolerances are not pre-registered

`scripts/build-choropleth.py` simplifies polygon geometry at 0.005°
(ADM1) and 0.001° (ADM3) tolerances before SVG export. The values
were chosen to keep SVG file sizes publishable (down from 336/357 MB
to 1.0/4.3 MB at full PSA/NAMRIA precision); the visual output is
unchanged at country scale. The tolerances are build-time constants
in the script docstring, not pre-registered methods choices, and are
not currently subject to the ±50% sensitivity suite. Upgrade-pass
scope.

### 7.4 PSA SAE workbook is in-repo cached

The 2023 PSA city/municipal SAE Excel attachment is cached at
`public-service-data-quality/.cache/psa-phl-2023-sae-with-psgc-nohuc.xlsx`
(361 KB). PSA government-site content is public domain unless
otherwise stated; `SOURCE-ACTION.md` documents the verified-public
source page and the manual-download record. The owner-side preference
of PSA institutional reviewers (synthesized from PIDS's published
position) is for derivative outputs to be re-hosted, not the source
workbook itself. Before any external venue submission, the in-repo
binary is replaced with a deterministic-fetch path.

### 7.5 Caveat-loss across publication tiers

The publication ladder (`research/factory.md`) publishes the same
headline ratios at every tier from working paper to social card. The
working paper carries the multi-page Limitations section; the brief
compresses to four bullets; the social card has no caveats in its
280-character body. The mitigation is the back-link rule
(`Caveats:` link to a tier with the full Limitations section
required from every social-tier post) and the §13.3 measurement-gap
framing inline at every tier above the social card. Distribution
risk is not zero.

### 7.6 BGD ADM1 choropleth has N=8

The BGD division-level choropleth shows 8 polygons; this is below
the threshold for any rank-based statistical test. The pattern
direction (Dhaka highest, Sylhet/Barisal lowest) is visible but not
statistically demonstrated. A district-level (ADM2, 64 polygons)
choropleth is the natural upgrade and would parallel the PHL
treatment more closely.
