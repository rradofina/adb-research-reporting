# L3 Evidence Module: Bangladesh Registry-Map Source Disagreement

`attestation_chain: ai-first`
Date: 2026-06-19
Goal level: L3 program evidence

## Status

This module packages the Bangladesh source-disagreement showcase into a
program evidence note. It does not change the PSDQ maturity label, and it does
not convert the report into human-final review. The purpose is narrower: make
the validation strata behind `/showcase/psdq-source-disagreement` visible
before the source-disagreement visual is used for any service-access,
catchment, or travel-time interpretation.

## Why This Measurement Problem Matters

Service-access maps often begin by taking facility locations from a public map
or an official registry. If the two sources disagree before travel time is
modeled, the access map inherits a source-quality problem. PSDQ treats that
source disagreement as the object of measurement.

For Bangladesh, the question is not whether OpenStreetMap or the DGHS registry
is the final ground truth. The question is where the two public sources are far
enough apart that an ADB team, health ministry, or statistics office should
validate the facility layer before using it downstream.

## What Existing Data Miss

The national PSDQ panel reports that Bangladesh has 3,298 OSM health features
against 27,992 DGHS clinical-tier registry facilities. That national ratio is
useful, but it is too coarse for validation planning. The operational question
is at the upazila row: where are official registry counts, public-map counts,
Open Buildings denominators, and road-context eligibility available together?

## Data Sources and Coverage

The L3 strata script reads three already-generated public artifacts:

| Input | Local path | Producing script |
|---|---|---|
| Bangladesh exposure-ranked disagreement table | `generated/psdq-bgd-exposure-ranked-disagreement.csv` | `scripts/build-bgd-exposure-ranked-disagreement.py` |
| Bangladesh exposure-ranked summary | `generated/psdq-bgd-exposure-ranked-disagreement-summary.json` | `scripts/build-bgd-exposure-ranked-disagreement.py` |
| Bangladesh exposure plus road-context summary | `generated/psdq-bgd-exposure-road-context-summary.json` | `scripts/build-bgd-road-surface-context.py --skip-download` |

The resulting L3 artifact is
`generated/psdq-bgd-source-disagreement-strata.{json,csv}`.

Current coverage in the generated artifact:

| Coverage check | Result |
|---|---:|
| DGHS registry upazila rows in the CSV | 572 |
| Rows with Open Buildings denominator | 561 |
| Registry rows with joined OSM features | 527 |
| OSM elements retrieved / assigned to boundary | 3,303 / 3,302 |
| OSM features joined to registry rows | 3,212 |
| OSM features not joined to registry rows | 90 |
| Active DGHS clinical facilities | 28,166 |
| Joined OSM health features | 3,212 |
| Registry-minus-OSM clinical gap | 25,262 |
| 3 km p85 Open Buildings denominator | 17,467,160 |
| Under-observed 3 km p85 building proxy | 15,668,648 |
| Rows with road context / surface-score eligibility | 527 / 234 |

## Method

The L3 module performs no new source retrieval. It packages the existing PSDQ
outputs in four steps:

1. Read the exposure-ranked upazila CSV and the two chart-ready JSON summaries.
2. Stratify each registry row by OSM-to-DGHS clinical ratio.
3. Count validation residues: missing Open Buildings denominators, registry
   rows without joined OSM features, zero-OSM rows, rows where OSM equals or
   exceeds the registry count, and road-surface eligibility.
4. Emit a JSON/CSV package that the showcase route can display directly.

## Results

The ratio strata are the core validation check. They show that the report
should be framed as source disagreement, not as a simple "OSM is always lower"
statement.

| Stratum | Rows | Active DGHS clinical | OSM health |
|---|---:|---:|---:|
| No active clinical registry count | 5 | 0 | 0 |
| Registry row has zero OSM health features | 115 | 3,879 | 0 |
| More than zero and below 5% OSM / registry | 197 | 11,135 | 289 |
| 5% to below 10% OSM / registry | 92 | 4,569 | 321 |
| 10% to below 20% OSM / registry | 81 | 4,774 | 682 |
| 20% to below 50% OSM / registry | 44 | 2,744 | 804 |
| 50% to below 100% OSM / registry | 17 | 655 | 398 |
| OSM count equals or exceeds the active registry count | 21 | 410 | 718 |

The validation residue is equally important:

| Validation check | Rows |
|---|---:|
| Missing Open Buildings denominator | 11 |
| Registry row without joined OSM features | 45 |
| Zero OSM health features with active registry count | 115 |
| OSM equals or exceeds active registry count | 21 |
| Positive registry-minus-OSM gap | 551 |
| Eligible for road context | 527 |
| Eligible for road-surface score | 234 |

The top exposure-proxy row remains Gazipur Sadar, where the generated table
records 197 DGHS clinical facilities, 58 OSM health features, and 172,755
under-observed 3 km p85 building proxy. The top zero-OSM validation row is
Sonargaon, with 79 active DGHS clinical facilities and 70,633 under-observed
3 km p85 building proxy.

## What the Result Means

The L3 module gives the showcase a defensible validation spine. A reader can
see whether the map-registry disagreement is being shown in rows with enough
supporting context, and can see the rows that resist a simple undercount
story. The operational use is validation prioritization: select facility rows,
source names, and upazilas for follow-up before using the facility layer in a
travel-time, catchment, or access map.

## Facility-Validation Sample Addendum

The next source-QA step is now packaged as a deterministic sample design in
`facility-validation-sample.md`. The script
`scripts/design-bgd-facility-validation-sample.py` reads the L3 strata, the
exposure-ranked disagreement table, and the DGHS facility-coordinate extract.
It writes a 20-upazila validation sample and a 76-row coding sheet. Of the 76
sampled DGHS facility rows, 69 are coordinate-ready.

The sample is split across four groups:

| Group | Upazila rows | Facility rows | Coordinate-ready facility rows |
|---|---:|---:|---:|
| High exposure gap | 5 | 20 | 20 |
| Zero OSM, high proxy | 5 | 20 | 20 |
| OSM equals or exceeds registry | 5 | 16 | 11 |
| Mid-ratio comparison | 5 | 20 | 18 |

This addendum is a sample design, not a validation result. The coding-sheet
outcome fields were intentionally blank at the sample-design stage. The
follow-on coded screen and AI review ledger now separate the flagged rows into
duplicate/name questions, classification mismatch, registry-coordinate
uncertainty, missing public-map points, nearby OSM features without a registry
name match, and unresolved public-source evidence.

## Automated Coded-Screen Addendum

The first public-source coding screen is now packaged in
`facility-validation-coded-screen.md`. The script
`scripts/code-bgd-facility-validation-sample.py` reads the 76-row coding sheet,
filters the cached all-Bangladesh OSM health-feature pull within 500 meters of
sampled DGHS coordinates, and checks coordinate plausibility against
geoBoundaries ADM3.

The automated screen is not a manual validation pass. It codes the 76 sampled
DGHS rows as follows:

| Validation code | Rows |
|---|---:|
| Confirmed same facility | 5 |
| Probable duplicate or alias | 3 |
| Classification mismatch | 3 |
| Registry coordinate issue | 23 |
| Missing public-map point | 40 |
| OSM-only candidate | 2 |
| Unresolved public sources | 0 |

The group pattern is the useful caution. In the zero-OSM sample, 18 of 20
sampled rows are valid-coordinate DGHS rows with no cached OSM health feature
within 500 meters. In the OSM-equals-or-exceeds-registry group, the automated
screen finds a mixed pattern of confirmed matches, aliases, classification
questions, coordinate issues, missing public-map points, and OSM-only
candidates. That pattern supports source-QA language and argues against a
single universal undercount claim.

## AI Review-Ledger Addendum

The flagged rows are now structured in `facility-validation-ai-review.md`. The
script `scripts/review-bgd-facility-validation-flags.py` reads the coded-screen
CSV, OSM-candidates CSV, and coded-summary JSON, then writes a row-level
AI/public-source review ledger.

The ledger keeps all 71 flagged rows open while separating them into:

| AI review workstream | Rows |
|---|---:|
| Public-map gap at valid coordinate | 40 |
| Registry coordinate repair | 23 |
| Name/type resolution | 6 |
| Nearby OSM without registry-name match | 2 |

This is not human validation. It is the row-level worklist for the next public
source review.

## What It Does Not Mean

- This is not a population estimate, household count, poverty estimate,
  service-demand measure, facility-quality measure, or travel-time result.
- Open Buildings denominators are settlement-exposure context, not validated
  catchments.
- Road-surface context is a triage layer. It is not road access, poverty, or a
  service-delivery effect.
- OSM counts exceeding the registry in 21 rows means the public report must
  say "source disagreement" rather than "OSM undercount" as a universal rule.
- This does not promote PSDQ beyond its existing ai-first PR label and does
  not make the artifact human-final.

## Reproduce the Analysis

```bash
python public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py
python public-service-data-quality/scripts/build-bgd-road-surface-context.py --skip-download
python public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py
python public-service-data-quality/scripts/design-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/review-bgd-facility-validation-flags.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.json`
- `public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-sample.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-sample-upazilas.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-sample-facilities.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coding-sheet.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coded-screen.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-osm-candidates.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coded-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review-summary.json`

## Next Statistical Upgrade

The next upgrade is row-level public-source resolution from the AI review
ledger. Start with the 8 candidate-resolution rows, then coordinate-source
repair, then the high-exposure public-map-gap checks. Until that review exists,
the correct publication use is source QA before service-access mapping, not a
statement about facility availability, service quality, or validated
catchments.
