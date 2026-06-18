---
title: "Bangladesh Facility-Validation Coordinate-Repair Triage"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_coordinate_repair_triage_not_human_validation
created: 2026-06-19
---

# Bangladesh Facility-Validation Coordinate-Repair Triage

## Why This Measurement Problem Matters

A source-disagreement map can overstate a public-map gap if the official
registry coordinate is missing, duplicated, or attached to the wrong
administrative unit. Before a facility row is coded as absent from OpenStreetMap
(OSM), the coordinate itself has to be checked.

This triage pass isolates that problem inside the PSDQ Bangladesh validation
sample. It does not ask whether OSM or DGHS is "right." It asks which sampled
DGHS rows cannot yet be used for map matching because the coordinate source
needs repair.

## Data Sources and Coverage

The script uses only public-source artifacts already committed in the PSDQ
package:

- `generated/psdq-bgd-facility-validation-ai-review.csv` - the AI
  public-source review ledger that identified 23 registry-coordinate repair
  rows.
- `generated/psdq-bgd-facility-validation-coded-screen.csv` - the sampled DGHS
  rows used to test exact-coordinate reuse.
- `.cache/geo/geoBoundaries-BGD-ADM3.geojson` - public ADM3/upazila geometry
  used to test whether a coordinate falls inside the named sampled upazila.
- `.cache/bgd_osm_health_features_overpass.json` - cached all-Bangladesh OSM
  health features used to find the nearest public-map health point to the
  suspect coordinate.
- `.cache/bgd_dghs_p*.json` - cached public DGHS DataTables rows used for
  public registry names, type labels, active status, and profile links.

Outputs:

- `generated/psdq-bgd-facility-validation-coordinate-repair.csv`
- `generated/psdq-bgd-facility-validation-coordinate-repair-summary.json`

## Method

The deterministic script
`scripts/triage-bgd-facility-coordinate-repairs.py` runs five checks.

1. Keep only rows that the AI review ledger already placed in the
   `registry_coordinate_repair` bucket.
2. Separate rows with missing or invalid coordinates from rows with a usable
   latitude and longitude.
3. Compare usable coordinates with the public geoBoundaries ADM3/upazila
   polygons and measure the distance back to the named sampled upazila.
4. Check whether the exact sampled coordinate is reused by more than one
   facility row in the 76-row validation sample.
5. For usable but suspect coordinates, find the nearest cached OSM health
   feature and record whether it is within 500 meters.

No row is closed by this pass. The output is a source-repair worklist.

## Results

The coordinate-repair queue contains 23 sampled DGHS rows. Seven rows have no
usable registry coordinate. The remaining 16 rows have a coordinate, but the
coordinate falls outside the expected sampled upazila in the public ADM3
boundary check.

Among the 16 usable-but-suspect coordinates, 13 fall inside another public ADM3
polygon, 3 fall outside the public Bangladesh ADM3 polygons used in this check,
and 6 sit within 500 meters of a cached OSM health feature. Two sampled rows
reuse the same exact coordinate. Four suspect coordinates are at least 50
kilometers from the named sampled upazila; the largest measured distance is
351.4 kilometers.

The repair lanes are:

| Coordinate-repair lane | Rows | What it means |
|---|---:|---|
| Missing registry coordinate | 7 | The row cannot enter map matching until a public coordinate source is found. |
| Reused sampled coordinate | 2 | More than one sampled DGHS row carries the same exact coordinate. |
| Other public upazila, near OSM health feature | 6 | The coordinate is in another ADM3 and near a public-map health point. |
| Other public upazila, no near OSM health feature | 5 | The coordinate is in another ADM3 but not near a cached OSM health point. |
| Outside public ADM3 boundary | 3 | The coordinate is not inside a public Bangladesh ADM3 polygon in this check. |

The distance ledger matters because it prevents a weak interpretation. A row
whose registry coordinate is in another upazila, or hundreds of kilometers from
the named upazila, should not be used to declare an OSM absence at that sampled
facility location.

## What This Does Not Mean

This is not human validation. It does not prove the DGHS registry row is wrong,
does not prove that OSM is correct, and does not estimate health-service
access, demand, quality, staffing, or catchment coverage.

The nearest OSM feature is a source clue only. A nearby OSM hospital or clinic
can indicate that the coordinate is pointing to a public-map health location,
but it does not identify the sampled DGHS facility without a public name,
profile, or campus confirmation.

## Reproduce the Analysis

Run:

```bash
python public-service-data-quality/scripts/triage-bgd-facility-coordinate-repairs.py
```

Then inspect:

```bash
public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair.csv
public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair-summary.json
```

## Next Statistical Upgrade

The next PSDQ loop should use this coordinate-repair ledger before moving to
the 40 public-map-gap rows. Rows with missing coordinates need public DGHS or
official source retrieval. Rows with valid but wrong-admin coordinates need a
row-level source note: whether the coordinate points to another public facility,
a shared campus, a copied placeholder, or an unrepaired registry location. Only
after that repair pass should the high-exposure public-map-gap rows be read as
candidate OSM absence cases.
