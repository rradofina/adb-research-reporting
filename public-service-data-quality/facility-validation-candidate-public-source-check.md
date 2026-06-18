# Public-Source Check: Bangladesh PSDQ Candidate Rows

`attestation_chain: ai-first`
Date: 2026-06-19
Goal level: L3 public-source confirmation scan
Status: AI public-source candidate check, not human validation

## Why This Measurement Problem Matters

The candidate-resolution pass narrowed the PSDQ facility review to 8 rows, but
the previous artifact still relied mainly on the ranked candidate table. That
table used the primary OSM `name` tag, distance, and facility class. It did
not fully use public tags such as `name:en`, `name:bn`, address, operator,
website, emergency, and healthcare fields.

This check reads those richer public-source fields. The purpose is not to
close rows. It is to tell a reviewer which candidate rows have public OSM tag
support, which rows are same-site label or type conflicts, and which rows
still lack public OSM name support.

## Data Sources and Coverage

The script uses only committed public-source artifacts and local public-source
caches.

| Input | Local path | Role |
|---|---|---|
| Candidate-resolution CSV | `generated/psdq-bgd-facility-validation-candidate-resolution.csv` | The 8-row worklist |
| OSM candidates | `generated/psdq-bgd-facility-validation-osm-candidates.csv` | Ranked OSM health candidates within 500 meters |
| OSM Overpass cache | `.cache/bgd_osm_health_features_overpass.json` | Full OSM tags for Bangladesh health features |
| DGHS DataTables cache | `.cache/bgd_dghs_p*.json` | Public DGHS name, Bangla name, active status, and public/private status |

The OSM cache records `timestamp_osm_base = 2026-04-29T09:11:39Z`. The
script does not fetch new data. All 8 rows remain open after the scan.

## Method

The source-check script applies a deterministic evidence scan:

1. Join the 8 candidate-resolution rows to all OSM health candidates within
   500 meters.
2. Load the full OSM tags for each candidate from the pinned Overpass cache.
3. Load the cached public DGHS registry row for each sampled facility.
4. Compare DGHS English and Bangla names against OSM `name`, `name:en`,
   `name:bn`, `official_name`, `alt_name`, `short_name`, `operator`, and
   `brand` fields.
5. Separate rows into four public-source lanes while keeping every row open.

## Results

| Public-source check lane | Rows |
|---|---:|
| `strong_same_site_osm_tag_support_requires_human_confirmation` | 2 |
| `same_site_type_or_label_conflict_requires_public_label_check` | 2 |
| `name_support_but_coordinate_or_function_conflict` | 2 |
| `nearby_features_do_not_support_registry_name` | 2 |

Five of the 8 rows have specific OSM name-tag support somewhere in the
candidate set. Three of those have the best public-name candidate within 50
meters. This is useful source evidence, but it is not a same-facility
closure.

The two strongest same-site tag-support rows are:

| DGHS row | OSM support | Distance |
|---|---|---:|
| ASGAR ALI MEDICAL COLLEGE & HOSPITAL LIMITED | OSM `name = Asgar Ali Hospital` | 12.6 m |
| Ahsania Mission Cancer and General Hospital | OSM `name:en = Ahsania mission cancer hospital` | 18.9 m |

Two rows are same-site label or type conflicts: Chattogram Chest Disease
Clinic sits near an OSM `General Hospital` feature, and Gurudashpur Upazila
Health Complex sits near an OSM `Gurudaspur General Hospital` feature. These
rows need public label review before the map-matching code changes.

Two rows have name support but unresolved coordinate or function conflict:
Aichi Medical College & Hospital has an OSM `name:en` candidate 277.7 meters
away, and Al-Helal Specialized Hospital Limited (Blood Bank) has an OSM
`Al-Helal Hospital` candidate 434.5 meters away. These are not close enough
to treat as same-site without another public source.

Two rows still lack public OSM name support in the cached candidates: Alhera
Nagar General Hospital & Diagnostic Center and Al-Arafah Islami Bank
Foundation Kidney Dialysis Center.

## What the Result Means

The PSDQ source-disagreement package now has a more credible next worklist.
Instead of asking a reviewer to inspect 71 flagged rows or even 8 generic
candidate rows, the evidence points to four different tasks: confirm
same-site tag support, resolve same-site type labels, inspect coordinate or
function conflicts, and keep weak nearby features unresolved unless another
public source supports the registry name.

This strengthens the showcase because the caveat is no longer generic. The
reader can see how public-source disagreement changes from a broad chart into
a row-level source QA sequence.

## What It Does Not Mean

- This is not human validation.
- No row is closed as a confirmed same-facility match.
- OSM `name:en` or `name:bn` support does not prove current operation,
  ownership, service readiness, or facility quality.
- A nearby OSM health feature without name support does not prove the DGHS row
  is wrong.
- The result does not measure access, travel time, population, households,
  poverty, service demand, quality, or catchments.
- The result does not change the existing PSDQ maturity label or make the
  artifact human-final.

## Reproduce the Check

```bash
python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/review-bgd-facility-validation-flags.py
python public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py
python public-service-data-quality/scripts/check-bgd-facility-candidate-public-sources.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json`

## Next Statistical Upgrade

The next source-repair step now lives in
`facility-validation-coordinate-repair.md`. It keeps the same caution: no row
is closed by AI-only evidence. The follow-on public-map-gap triage now lives in
`facility-validation-public-map-gap.md`, and it keeps all 40 map-gap rows open.
The row-level public-source evidence ledger now lives in
`facility-validation-public-map-gap-evidence.md`; it keeps all 40 rows open and
records DGHS and OSM inspection links. The next loop should perform targeted
public-map inspection before changing any source-disagreement claim.
