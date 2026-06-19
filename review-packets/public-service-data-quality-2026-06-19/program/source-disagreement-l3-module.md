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

## Candidate-Resolution Addendum

The first row-level public-source pass is now structured in
`facility-validation-candidate-resolution.md`. The script
`scripts/resolve-bgd-facility-candidate-rows.py` reads the AI review ledger,
the OSM-candidates CSV, and the AI review summary, then separates the 8
candidate-resolution rows into narrower lanes.

All 8 rows remain open:

| Candidate-resolution lane | Rows |
|---|---:|
| Probable same-facility alias or campus | 1 |
| Probable same-site classification conflict | 2 |
| Possible alias requiring name check | 2 |
| Local-script candidate requiring name check | 1 |
| Ambiguous nearby candidate | 1 |
| Weak nearby OSM signal | 1 |

This is not human validation and does not close any row as a confirmed
same-facility match. It makes the next review step more specific: alias/campus
checks, type-conflict checks, possible aliases, a local-script name check, and
weak or ambiguous nearby features.

## Public-Source Check Addendum

The candidate rows are now checked against richer public OSM tags in
`facility-validation-candidate-public-source-check.md`. The script
`scripts/check-bgd-facility-candidate-public-sources.py` reads the
candidate-resolution CSV, the OSM-candidates CSV, the pinned all-Bangladesh
OSM/Overpass health-feature cache, and cached DGHS public DataTables rows.

All 8 rows remain open:

| Public-source check lane | Rows |
|---|---:|
| Strong same-site OSM tag support, still requiring human confirmation | 2 |
| Same-site type or label conflict requiring public label check | 2 |
| Name support with coordinate or function conflict | 2 |
| Nearby features do not support the registry name | 2 |

The richer tags matter. The Ahsania row, for example, is not just a weak
English-string match: the nearby OSM hospital carries `name:en = Ahsania
mission cancer hospital` in the pinned cache. The Aichi row similarly has a
nearby OSM candidate with `name:en = Aichi Medical College Hospital`, but the
candidate is 277.7 meters away, so the row remains a coordinate/function
conflict rather than a closed same-site match.

## Coordinate-Repair Addendum

The registry-coordinate repair rows are now structured in
`facility-validation-coordinate-repair.md`. The script
`scripts/triage-bgd-facility-coordinate-repairs.py` reads the AI review ledger,
the coded-screen CSV, public geoBoundaries ADM3, cached all-Bangladesh OSM
health features, and cached DGHS public DataTables rows.

All 23 coordinate-repair rows remain open:

| Coordinate-repair lane | Rows |
|---|---:|
| Missing registry coordinate | 7 |
| Reused sampled coordinate | 2 |
| Other public ADM3 and near an OSM health feature | 6 |
| Other public ADM3 and no nearby OSM health feature | 5 |
| Outside public ADM3 boundary | 3 |

The distance check is the useful caution. Sixteen rows have usable coordinates
that fall outside the expected sampled upazila. Four of those suspect
coordinates are at least 50 kilometers from the named upazila, and the largest
measured distance is 351.4 kilometers. This means the high-exposure
public-map-gap rows should not be interpreted until the coordinate queue has
been separated from true map-absence candidates.

## Public-Map-Gap Addendum

The valid-coordinate public-map-gap rows are now structured in
`facility-validation-public-map-gap.md`. The script
`scripts/triage-bgd-facility-public-map-gaps.py` reads the AI review ledger,
the coded-screen CSV, the coordinate-repair CSV, exposure-ranked upazila
context, the OSM upazila table, cached all-Bangladesh OSM health features, and
cached DGHS public DataTables rows.

All 40 public-map-gap rows remain open:

| Public-map-gap lane | Rows |
|---|---:|
| Reused valid coordinate | 2 |
| Same-upazila name signal far from coordinate | 2 |
| Same-upazila name signal outside 500 m | 1 |
| Same-upazila OSM 500-1,000 m away | 2 |
| Zero OSM in expected public upazila | 18 |
| Same-upazila OSM present, not at facility | 3 |
| No same-upazila OSM signal within 3 km | 12 |

The triage keeps the interpretation narrow. Thirty rows are priority-1
high-exposure checks, but the output does not close any row as a confirmed OSM
absence. The zero-OSM lane is an upazila-level public-map observability signal.
The same-name and 500m-to-1km lanes are row-level matching problems.

## Public-Map-Gap Row-Evidence Addendum

The row-level public-source evidence is now structured in
`facility-validation-public-map-gap-evidence.md`. The script
`scripts/build-bgd-facility-public-map-gap-row-evidence.py` reads the
public-map-gap triage CSV and summary JSON, then writes a source-evidence note
for every open row. It does not fetch new data, cache full DGHS profile HTML,
or close rows.

All 40 public-map-gap rows now have a DGHS source note, public profile URL,
OSM coordinate-inspection URL, OSM feature or absence note, and keep-open
reviewer action. The row-evidence tiers are:

| Row-evidence tier | Rows |
|---|---:|
| Source repair before row absence | 4 |
| Possible match or buffer review | 3 |
| Row-level public-map absence review | 15 |
| Upazila-level public-map observability review | 18 |

This is the first row-readable evidence layer. It separates source-repair
questions from map-absence candidates, and it keeps zero-OSM expected-upazila
cases out of facility-specific language unless a row-level public source
supports that interpretation.

## Targeted Public-Map Inspection Addendum

The targeted public-map inspection packet is now structured in
`facility-validation-public-map-inspection.md`. The script
`scripts/inspect-bgd-facility-public-map-targets.py` reads the row-evidence
ledger, public ADM3 boundaries, and the pinned all-Bangladesh OSM/Overpass
health-feature cache. It then ranks candidate public-map features and records
what evidence would be needed before a row could be closed or reclassified.

The pass inspects all 40 row-evidence records. It marks 10 named-upazila start
rows, 18 zero-OSM queue rows, 22 rows with same-upazila candidate public-map
feature links, and 6 rows with specific-name signals among candidate features.
All 40 rows remain open; 0 are closed as resolved and 0 are reclassified as
same-facility matches.

The inspection lanes are:

| Inspection lane | Rows |
|---|---:|
| Source repair first | 4 |
| Possible public-map match or buffer case | 3 |
| Facility-specific public-map absence candidate | 15 |
| Upazila public-map observability gap | 18 |

This addendum makes the review queue more actionable without changing the
claim. The evidence still supports a source-disagreement workbench, not a
facility-quality, service-access, or ground-truth result.

## First-Row Public-Source Confirmation Addendum

The first public-source confirmation packet now lives in
`facility-validation-public-source-confirmation.md`. The script
`scripts/confirm-bgd-facility-public-map-first-rows.py` reads the targeted
inspection summary and retrieves public DGHS profile pages plus public OSM API
feature records for the first 12 inspection rows.

The pass checks 12 first-row cases. It retrieves 12 DGHS public profiles and
12 OSM API feature records. All 12 rows show DGHS profile token support, and 2
rows have live OSM candidate-name scores at or above 0.75. All 12 rows remain
open; 0 are closed as resolved and 0 are reclassified as same-facility
matches.

The first 12 rows split into:

| Public-source confirmation lane | Rows |
|---|---:|
| Candidate feature retrieved but name conflict remains | 7 |
| Source-repair public sources retrieved, still open | 2 |
| Zero-OSM context candidate outside upazila, still open | 2 |
| Possible same-facility candidate needing manual location check | 1 |

This confirms that the first DGHS and OSM source links are live, while keeping
the substantive row decision separate from API reachability and name support.

## Targeted-Row Public-Source Confirmation Addendum

The targeted-row public-source confirmation packet now lives in
`facility-validation-public-source-confirmation-targeted-rows.md`. The script
`scripts/confirm-bgd-facility-public-map-targeted-rows.py` reads the 40-row
targeted inspection CSV and retrieves public DGHS profile pages plus public
OSM API feature records for all targeted inspection rows.

The pass checks 40 targeted inspection cases, including all 30 priority-1
rows. It retrieves 40 DGHS public profiles and 40 OSM API feature records. All
40 rows show DGHS profile token support, and 6 rows have live OSM
candidate-name scores at or above 0.75. All 40 rows remain open; 0 are closed
as resolved and 0 are reclassified as same-facility matches.

The 40 rows split into:

| Public-source confirmation lane | Rows |
|---|---:|
| Zero-OSM context candidate outside upazila, still open | 18 |
| Candidate feature retrieved but name conflict remains | 15 |
| Source-repair public sources retrieved, still open | 4 |
| Possible same-facility candidate needing manual location check | 3 |

This confirms that public-source reachability is not the limiting issue for
the targeted queue. The remaining work is source classification: separating
upazila-level observability gaps from row-level name conflicts, source-repair
cases, and possible same-facility public-map candidates.

## Public-Source Decision Ledger Addendum

The public-source decision ledger now lives in
`facility-validation-public-source-decision-ledger.md`. The script
`scripts/build-bgd-facility-public-source-decision-ledger.py` reads the
targeted-row confirmation CSV/JSON and builds the next reviewer queue without
fetching new data.

The ledger selects 16 rows from the 40-row confirmation packet:

| Decision track | Rows |
|---|---:|
| Source repair first | 4 |
| Possible same-facility location review | 3 |
| Priority-1 name-conflict review | 9 |

It defers 18 zero-OSM upazila observability rows and 6 lower-priority
name-conflict spot checks. All 40 targeted rows remain open; 0 are closed as
resolved and 0 are reclassified as same-facility matches.

This makes the review queue narrower and more operational. It does not make
the evidence human-validated, and it does not turn source reachability into a
row outcome.

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
python public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py
python public-service-data-quality/scripts/check-bgd-facility-candidate-public-sources.py
python public-service-data-quality/scripts/triage-bgd-facility-coordinate-repairs.py
python public-service-data-quality/scripts/triage-bgd-facility-public-map-gaps.py
python public-service-data-quality/scripts/build-bgd-facility-public-map-gap-row-evidence.py
python public-service-data-quality/scripts/inspect-bgd-facility-public-map-targets.py
python public-service-data-quality/scripts/confirm-bgd-facility-public-map-first-rows.py
python public-service-data-quality/scripts/confirm-bgd-facility-public-map-targeted-rows.py
python public-service-data-quality/scripts/build-bgd-facility-public-source-decision-ledger.py
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
- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`

## Next Statistical Upgrade

The next upgrade is a decision ledger for the 3 possible same-facility rows,
the 4 source-repair rows, and a small set of high-exposure name-conflict rows.
Close or reclassify a row only if a public source supports the change;
otherwise keep it open with the specific unresolved source question.
