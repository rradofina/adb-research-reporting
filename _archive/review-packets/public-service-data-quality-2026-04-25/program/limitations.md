# Limitations — Public Service Data Quality

Status: **AI-drafted from `results.md` and the sensitivity suite.** Owner
reviews and amends before SR → PR review packet is sent.

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

(populated after `review-external.md` closes; objections that the
owner could not resolve are quoted here verbatim with reviewer permission)

### 5.1 *(reviewer name pending)*

> *(objection)*

## 6. Banned framings — explicit non-claims

Per `CONSTITUTION.md` §13.3 and §14:

- This result does **not** rank DMCs.
- This result does **not** describe DMCs as deficient.
- This result does **not** support causal inference from the screening
  signal alone.
- The article does not use any banned word from §14.
