---
title: "Bangladesh Facility-Validation Public-Map-Gap Triage"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_public_map_gap_triage_not_human_validation
created: 2026-06-19
---

# Bangladesh Facility-Validation Public-Map-Gap Triage

## Why This Measurement Problem Matters

A registry-map disagreement is operationally useful only if a reader can tell
which rows are plausible public-map absences and which rows are still source
repair problems. A missing OSM health feature near a DGHS coordinate can mean a
real map coverage gap. It can also mean the coordinate is duplicated, the OSM
feature is just outside the matching buffer, the same facility is mapped under a
nearby name, or the upazila has no joined OSM health feature at all.

This pass turns the 40 sampled public-map-gap rows into a reviewer queue. It
does not decide whether OSM or DGHS is correct. It shows which rows are ready
for high-exposure public-source inspection and which rows need a narrower
coordinate, name, or matching-radius check first.

## Data Sources and Coverage

The script uses only public-source artifacts already committed in the PSDQ
package:

- `generated/psdq-bgd-facility-validation-ai-review.csv` - the AI
  public-source review ledger that identified 40 public-map-gap rows at valid
  registry coordinates.
- `generated/psdq-bgd-facility-validation-coded-screen.csv` - the 76 sampled
  DGHS rows used to test exact-coordinate reuse.
- `generated/psdq-bgd-facility-validation-coordinate-repair.csv` - the
  coordinate-source repair ledger, used to warn when a public-map-gap row sits
  in an upazila that also has coordinate-source failures.
- `generated/psdq-bgd-exposure-ranked-disagreement.csv` - the upazila-level
  registry, OSM, and Open Buildings context.
- `generated/psdq-bgd-osm-health-upazila.csv` - OSM health features assigned
  to public geoBoundaries ADM3/upazila units.
- `.cache/bgd_osm_health_features_overpass.json` - cached all-Bangladesh OSM
  health features used for nearest-neighbor and same-upazila name-signal
  checks.
- `.cache/bgd_dghs_p*.json` - cached public DGHS DataTables rows used for
  public registry names, type labels, active status, and profile links.

Outputs:

- `generated/psdq-bgd-facility-validation-public-map-gap.csv`
- `generated/psdq-bgd-facility-validation-public-map-gap-summary.json`

## Method

The deterministic script
`scripts/triage-bgd-facility-public-map-gaps.py` runs six checks.

1. Keep only rows that the AI review ledger placed in the
   `public_map_gap_at_valid_coordinate` bucket.
2. Confirm that these rows still have usable registry coordinates inside the
   expected sampled upazila.
3. Check whether the exact sampled coordinate is reused by another row in the
   76-row validation sample.
4. Join upazila-level context: active clinical DGHS facilities, joined OSM
   health features, registry-minus-OSM count, registry gap share, and the Open
   Buildings under-observed proxy.
5. Reassign cached OSM health features to geoBoundaries ADM3 units and check
   nearest same-upazila OSM distance, nearest all-Bangladesh OSM distance, and
   same-upazila name support outside the original 500 meter screen.
6. Keep every row open and assign a reviewer lane rather than a final row code.

## Results

The public-map-gap queue contains 40 sampled DGHS rows. Thirty are priority-1
high-exposure checks. All 40 have valid coordinates inside the expected sampled
upazila in the coded screen, but the triage still keeps all 40 open.

The reviewer lanes are:

| Public-map-gap lane | Rows | What it means |
|---|---:|---|
| Reused valid coordinate | 2 | The row has a valid coordinate, but another sampled row uses the same coordinate. |
| Same-upazila name signal far from coordinate | 2 | A same-upazila OSM feature has strong name support but is more than 10 km from the registry coordinate. |
| Same-upazila name signal outside 500 m | 1 | A same-upazila OSM feature outside the original buffer has specific name support. |
| Same-upazila OSM 500-1,000 m away | 2 | The row is sensitive to the 500 m matching radius. |
| Zero OSM in expected public upazila | 18 | The expected upazila has no joined OSM health feature in the pinned cache. |
| No same-upazila OSM signal within 3 km | 12 | The upazila has OSM health features, but none are near this sampled coordinate. |
| Same-upazila OSM present, not at facility | 3 | The upazila has nearby public-map health features, but not a row-level match. |

The queue is concentrated in a few places. Narayanganj Sadar, Sonargaon,
Sharsha, and Araihazar each contribute four sampled public-map-gap rows.
Sonargaon, Sharsha, Araihazar, Thakurgaon Pirganj, and Dinajpur Parbatipur are
zero-OSM expected-upazila cases in this check. Gazipur Sadar remains high
exposure but needs caution because the same upazila also has a coordinate-repair
flag.

The triage also shows why a single missing-map label would be too blunt. Two
Narayanganj hospital rows reuse the same valid coordinate. Two rows have a
same-upazila OSM name signal more than 10 kilometers away from the registry
coordinate. Two rows have an OSM health feature between 500 meters and 1
kilometer away. These rows need row-level public-source review before they can
support a facility-specific public-map absence interpretation.

## What This Does Not Mean

This is not human validation. It does not prove that a DGHS row is absent from
OSM, does not prove that a same-name OSM feature is the same facility, and does
not estimate health-service access, quality, staffing, demand, or catchment
coverage.

The zero-OSM upazila lane is a public-map observability signal, not a statement
that facilities do not exist. The same-upazila name-signal lanes are review
clues, not row closures. All 40 rows remain open.

## Reproduce the Analysis

Run:

```bash
python public-service-data-quality/scripts/triage-bgd-facility-public-map-gaps.py
```

Then inspect:

```bash
public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap.csv
public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-summary.json
```

## Next Statistical Upgrade

The row-level public-source evidence pass is now documented in
`facility-validation-public-map-gap-evidence.md`. The next PSDQ loop should
use that evidence ledger for targeted public-map inspection: close or
reclassify a row only if a public source supports the change; otherwise keep
the row open with the specific unresolved source question.
