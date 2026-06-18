---
title: "Bangladesh Facility-Validation Targeted Public-Map Inspection"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_map_targeted_inspection_not_human_validation
created: 2026-06-19
---

# Bangladesh Facility-Validation Targeted Public-Map Inspection

## Why This Measurement Problem Matters

The PSDQ Bangladesh workbench is useful only if it keeps source disagreement
separate from service-access claims. A sampled DGHS facility can appear missing
from the public map for several reasons: the registry coordinate may be reused,
the public-map feature may sit just outside the original buffer, the same
upazila may have other mapped health features but not this facility, or the
whole upazila may be weakly represented in the pinned public-map cache.

This inspection pass turns the 40 row-evidence records into a tighter reviewer
queue. It does not ask whether a facility exists on the ground. It asks what
public source a reviewer should open first and what evidence would be required
before any row is closed or reclassified.

## Data Sources and Coverage

The unit is the sampled DGHS public-map-gap row from the Bangladesh
facility-validation sample. The pass uses four committed public-source
artifacts:

- `generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv`
- `generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`
- `.cache/bgd_osm_health_features_overpass.json`
- `.cache/geo/geoBoundaries-BGD-ADM3.geojson`

The script loads all 40 row-evidence records, the pinned all-Bangladesh
OSM/Overpass health-feature cache, and public ADM3 boundaries. It gives every
row public-map candidate links where the cache can provide them, while keeping
the DGHS public profile link and coordinate-inspection link from the previous
row-evidence pass.

## Method

The inspection pack is built in five steps.

1. Read the row-evidence ledger and preserve the existing evidence tier for
   each sampled DGHS row.
2. Join the pinned OSM/Overpass health features to public ADM3 boundaries, so
   each feature can be compared with the expected upazila.
3. Mark the first inspection lanes: Gazipur Sadar, Narayanganj Sadar, Pabna
   Sadar, and zero-OSM upazilas.
4. Rank candidate OSM features by same-upazila name support and distance. For
   zero-OSM upazilas, keep the nearest national-cache features as context, not
   as same-upazila candidates.
5. Assign an inspection decision that keeps every row open unless public
   evidence can support a future closure or reclassification.

Name support is used only for triage. It is not a same-facility decision.

## Results

| Inspection scope | Rows |
|---|---:|
| Rows inspected | 40 |
| Priority-1 rows inspected | 30 |
| Named-upazila start rows | 10 |
| Zero-OSM upazila queue rows | 18 |
| Rows with same-upazila candidate public-map feature links | 22 |
| Rows with specific-name signals among candidate features | 6 |
| Rows kept open | 40 |
| Rows closed as resolved | 0 |

| Inspection lane | Rows | What it means for review |
|---|---:|---|
| Source repair first | 4 | Duplicate coordinates or far same-name signals must be resolved before absence language is used. |
| Possible public-map match or buffer case | 3 | A public-map feature may be relevant outside the original rule and needs confirmation. |
| Facility-specific public-map absence candidate | 15 | Same-upazila OSM exists, but not at the sampled DGHS coordinate in the pinned cache. |
| Upazila public-map observability gap | 18 | The expected upazila has no joined OSM health feature in the pinned cache, so the row should not be read as a facility-specific absence finding. |

The pass makes the next review sequence more concrete. Narayanganj Sadar
starts with source repair because two sampled hospital rows reuse the same
DGHS coordinate and have nearby public-map name signals. Gazipur Sadar and
Pabna Sadar supply facility-specific absence candidates where the expected
upazila has mapped health features, but not at the sampled coordinate. The
zero-OSM queue remains an upazila-level observability problem rather than a
row-level finding.

## What The Result Means

The inspection packet improves the PSDQ workbench by reducing the temptation to
turn a map gap into a claim. It shows which rows are source-repair questions,
which rows need alias or buffer review, and which rows should be interpreted at
the upazila-observability level until stronger public evidence is available.

For operations and statistical users, this matters because a registry-map
source-disagreement dashboard can otherwise push attention toward the wrong
unit: a facility row when the actual issue is a reused coordinate, or a whole
upazila when the public map has no health features joined at all.

## What It Does Not Mean

This pass is not human validation. It does not prove that a DGHS facility is
present, absent, open, closed, correctly classified, or correctly located. It
does not measure service access, facility quality, or demand. It also does not
close any of the 40 rows. Every row remains open for public-source or human
review.

## Reproduce the Analysis

Run:

```bash
python public-service-data-quality/scripts/inspect-bgd-facility-public-map-targets.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`

The script is no-network by design. It reads committed public-source caches and
the previous row-evidence ledger.

## Next Statistical Upgrade

The next upgrade is public-source/manual confirmation of the first inspection
rows.
Start with the Narayanganj Sadar source-repair rows, then Gazipur Sadar and
Pabna Sadar facility-specific candidates, then the zero-OSM upazila queue. A
row should be closed or reclassified only when a public map feature, DGHS
source correction, or other public official source supports the change.
