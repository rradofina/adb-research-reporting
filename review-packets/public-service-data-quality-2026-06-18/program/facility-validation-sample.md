# Facility-Validation Sample Design: Bangladesh PSDQ Source Disagreement

`attestation_chain: ai-first`
Date: 2026-06-19
Goal level: L3 validation-sample design
Status: sample design, not validation result

## Why This Measurement Problem Matters

The Bangladesh PSDQ source-disagreement module shows where the DGHS public
facility registry and OpenStreetMap health features diverge at the upazila
row. That is useful for a first screen, but an operations team cannot treat a
count gap as a validated facility-location result. The next question is
smaller and more practical: which public registry rows should be checked first,
and what exactly should a reviewer code when the public sources disagree?

This note turns the L3 strata into a facility-level validation sample. It does
not decide whether any facility is present, absent, duplicated, or correctly
classified.

## What Existing Data Miss

The L3 source-disagreement artifact identifies high-gap rows, zero-OSM rows,
and counterexamples where OSM counts equal or exceed the DGHS clinical
registry count. Those strata are still upazila-level. They do not say whether
the source gap comes from duplicate facility names, registry vintage,
classification differences, missing public-map points, coordinate uncertainty,
or unresolved public evidence.

The sample design bridges that gap by selecting DGHS facility rows for a
coding sheet before any manual public-source lookup is performed.

## Data Sources and Coverage

The no-network script reads only committed PSDQ artifacts:

| Input | Local path | Role |
|---|---|---|
| Exposure-ranked source-disagreement table | `generated/psdq-bgd-exposure-ranked-disagreement.csv` | Upazila registry-map disagreement and Open Buildings exposure proxy |
| L3 ratio strata | `generated/psdq-bgd-source-disagreement-strata.json` | Validation groups and residue counts |
| DGHS facility-coordinate extract | `generated/psdq-bgd-facility-coordinate-extract.csv` | Public DGHS facility names, types, flags, and coordinates |

The generated sample contains 20 upazila rows, 76 DGHS facility rows, and 69
coordinate-ready facility rows. The coding sheet has 76 rows, one per sampled
DGHS facility row.

## Method

The sample is deterministic and uses four groups:

1. Select five high-exposure-gap upazila rows from the top exposure-proxy
   list.
2. Select five zero-OSM, high-proxy rows where the registry has active
   clinical facilities but the joined OSM health count is zero.
3. Select five counterexample rows where OSM health counts equal or exceed the
   active DGHS clinical registry count.
4. Select five non-extreme comparison rows from the middle of eligible
   positive-ratio rows.

Within each sampled upazila, the script selects up to four active clinical
DGHS facility rows. It prefers coordinate-ready and principal-tier rows while
retaining community-level rows where available. A per-division cap is used
first for diversity, then the script backfills only if a group cannot reach
the target count.

## Sample Design

| Group | Upazila rows | Facility rows | Coordinate-ready facility rows |
|---|---:|---:|---:|
| `high_exposure_gap` | 5 | 20 | 20 |
| `zero_osm_high_proxy` | 5 | 20 | 20 |
| `osm_ge_registry` | 5 | 16 | 11 |
| `comparison_mid_ratio` | 5 | 20 | 18 |

| Group | Sampled upazilas |
|---|---|
| `high_exposure_gap` | Gazipur Sadar, Gazipur; Narayanganj Sadar, Narayanganj; Kushtia Sadar, Kushtia; Pabna Sadar, Pabna; Narsingdi Sadar, Narsingdi |
| `zero_osm_high_proxy` | Sonargaon, Narayanganj; Sharsha, Jashore; Araihazar, Narayanganj; Pirganj, Thakurgaon; Parbatipur, Dinajpur |
| `osm_ge_registry` | Ramna, Dhaka; Gendaria, Dhaka; Kotwali, Chattogram; Kafrul, Dhaka; Patenga, Chattogram |
| `comparison_mid_ratio` | Durgapur, Netrakona; Bera, Pabna; Demra, Dhaka; Panchagarh Sadar, Panchagarh; Gurudaspur, Natore |

The `osm_ge_registry` group has 16 facility rows because several sampled
counterexample upazilas have fewer than four active clinical DGHS rows in the
facility extract. The shortfall is retained rather than padded from another
group.

## Coding Sheet

The coding sheet leaves validation outcomes blank by design. A reviewer should
use public evidence only and code each row with one of these values:

| Code | Meaning |
|---|---|
| `confirmed_same_facility` | A public OSM feature and the DGHS row appear to describe the same facility. |
| `probable_duplicate_or_alias` | Names differ but public evidence suggests duplicate naming or aliasing. |
| `classification_mismatch` | The DGHS row and OSM feature use materially different facility classifications. |
| `registry_coordinate_issue` | DGHS coordinates are missing, implausible, or too uncertain for local OSM matching. |
| `missing_public_map_point` | DGHS row is public and coordinate-ready, but no plausible OSM health feature is found nearby. |
| `osm_only_candidate` | OSM feature appears plausible but no corresponding DGHS row is identified in the sampled registry rows. |
| `unresolved_public_sources` | Public evidence is insufficient to assign one of the above codes. |

The public validation source stack is DGHS public facility rows and OSM
Overpass health-feature lookups. The generated coding sheet includes a
coordinate-nearby Overpass query hint where a DGHS latitude and longitude are
available. Google Open Buildings remains settlement-exposure context only; it
is not a facility validation source.

## What the Result Means

This is a validation workplan for the PSDQ source-disagreement report. It
makes the next reviewer task explicit: check a bounded set of DGHS rows against
public-map evidence, record the reason for disagreement, and separate registry
and OSM source issues before the same facility layer is used in service-access
or catchment analysis.

## What It Does Not Mean

- The sample does not validate any facility.
- The coding sheet has no match outcomes yet.
- The sample is not a population, household, service-demand, quality,
  travel-time, or access estimate.
- Open Buildings denominators are not used to confirm facility existence.
- The result does not promote PSDQ beyond its existing ai-first PR label and
  does not make the artifact human-final.

## Reproduce the Sample Design

```bash
python public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py
python public-service-data-quality/scripts/build-bgd-road-surface-context.py --skip-download
python public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py
python public-service-data-quality/scripts/design-bgd-facility-validation-sample.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-sample.json`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-sample-upazilas.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-sample-facilities.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-coding-sheet.csv`

## Next Statistical Upgrade

The automated public-source coding screen is now documented in
`facility-validation-coded-screen.md`. The next upgrade is manual public-source
review of the rows flagged for manual review, followed by a comparison between
manual labels and the automated screen before any PSDQ source-disagreement
claim is revised.
