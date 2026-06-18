# Facility-Validation Coded Screen: Bangladesh PSDQ Source Disagreement

`attestation_chain: ai-first`
Date: 2026-06-19
Goal level: L3 validation coding screen
Status: automated public-source screen, not manual validation

## Why This Measurement Problem Matters

The Bangladesh PSDQ validation sample made the next review task explicit: 76
DGHS facility rows should be checked before a registry-map disagreement is
used in any service-access analysis. This coded screen performs a first
deterministic public-source pass. It asks whether each sampled DGHS row has a
public OSM health feature nearby, whether the DGHS coordinate appears to fall
inside the sampled upazila, and whether the closest OSM candidate has a
plausible name or classification relationship.

The result is a triage screen for manual review. It is not a final facility
validation outcome.

## Data Sources and Coverage

The script reads the committed validation sample and public OSM cache:

| Input | Local path | Role |
|---|---|---|
| Blank coding sheet | `generated/psdq-bgd-facility-validation-coding-sheet.csv` | 76 sampled DGHS facility rows |
| Sample metadata | `generated/psdq-bgd-facility-validation-sample.json` | Sample groups and non-claim |
| OSM health-feature cache | `.cache/bgd_osm_health_features_overpass.json` | All-Bangladesh OSM `amenity=hospital/clinic/doctors` pull |
| geoBoundaries ADM3 | `.cache/geo/geoBoundaries-BGD-ADM3.geojson` | Upazila coordinate plausibility check |

The OSM cache records `timestamp_osm_base = 2026-04-29T09:11:39Z`. The coded
screen covers all 76 sampled DGHS facility rows and writes 86 nearby OSM
candidate rows.

## Method

The automated screen follows four steps:

1. Check whether a sampled DGHS row has a valid coordinate inside Bangladesh.
2. Check whether that coordinate falls inside the expected geoBoundaries
   ADM3/upazila polygon where the upazila geometry is available.
3. Search the cached Bangladesh OSM health features within 500 meters of the
   valid DGHS coordinate.
4. Assign a conservative validation code using name similarity, facility class,
   distance, and sample group.

The code values are the same as the sample-design coding sheet. Rows with
missing or out-of-upazila coordinates are separated from rows that appear to
have no public-map point nearby. This matters because a missing OSM feature
and a questionable registry coordinate call for different source-improvement
actions.

## Coded Screen Results

| Validation code | Rows |
|---|---:|
| `confirmed_same_facility` | 5 |
| `probable_duplicate_or_alias` | 3 |
| `classification_mismatch` | 3 |
| `registry_coordinate_issue` | 23 |
| `missing_public_map_point` | 40 |
| `osm_only_candidate` | 2 |
| `unresolved_public_sources` | 0 |

| Group | Rows | Confirmed | Probable alias | Classification mismatch | Coordinate issue | Missing public-map point | OSM-only candidate |
|---|---:|---:|---:|---:|---:|---:|---:|
| `comparison_mid_ratio` | 20 | 1 | 1 | 2 | 7 | 9 | 0 |
| `high_exposure_gap` | 20 | 2 | 0 | 0 | 6 | 12 | 0 |
| `osm_ge_registry` | 16 | 2 | 2 | 1 | 8 | 1 | 2 |
| `zero_osm_high_proxy` | 20 | 0 | 0 | 0 | 2 | 18 | 0 |

The screen flags 71 of 76 rows for manual review. Thirteen sampled rows have
at least one OSM health candidate within 500 meters. Fifty-three sampled rows
have a valid DGHS coordinate that falls inside the expected upazila boundary.

## What the Result Means

The automated screen sharpens the next manual task. The zero-OSM sample is not
just a national undercount story: 18 of its 20 sampled rows have valid
coordinates inside the sampled upazila but no cached OSM health point within
500 meters. The OSM-above-registry sample behaves differently: it contains
same-facility matches, probable aliases, classification questions,
coordinate issues, and OSM-only candidates. That is why the report should keep
the phrase "source disagreement" rather than collapse the evidence into a
single undercount claim.

## What It Does Not Mean

- This is not a human validation pass.
- The OSM cache is a public-source snapshot, not ground truth.
- A missing public-map point does not prove that a facility is absent.
- A registry-coordinate issue does not prove that the facility name or registry
  row is wrong.
- The screen does not measure service availability, quality, access, travel
  time, population, households, poverty, or catchments.
- The result does not promote PSDQ beyond its existing ai-first PR label and
  does not make the artifact human-final.

## Reproduce the Coded Screen

```bash
python public-service-data-quality/scripts/design-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-coded-screen.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-osm-candidates.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coded-summary.json`

## Next Statistical Upgrade

Use `facility-validation-ai-review.md`,
`facility-validation-candidate-resolution.md`, and
`facility-validation-candidate-public-source-check.md` as the current
worklists. The 8 candidate-resolution rows have been split into four
public-source check lanes; confirm those lanes first, then move to
coordinate-source repair rows and high-exposure public-map-gap checks. Record
reviewer notes row by row and compare any public-source labels with the
automated screen before revising any PSDQ source-disagreement claim.
