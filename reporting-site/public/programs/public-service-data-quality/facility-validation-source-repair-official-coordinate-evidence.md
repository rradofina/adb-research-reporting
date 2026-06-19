---
title: "Bangladesh Source-Repair Official Coordinate Evidence"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_repair_official_coordinate_evidence_not_human_validation
created: 2026-06-19
---

# Bangladesh Source-Repair Official Coordinate Evidence

## Why This Measurement Problem Matters

The source-repair queue asks a narrower question than map completeness: what
does the official public source currently say about the coordinate? A mapped
hospital with a strong name match can still be the wrong row-level conclusion if
the official registry coordinate is reused, distant, or unexplained.

## Data Sources and Coverage

This pass uses three public-source inputs:

- `generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv`
- `generated/psdq-bgd-facility-validation-public-map-inspection.csv`
- `.cache/bgd_osm_health_features_overpass.json`

For each of the four source-repair rows, the script retrieves the public DGHS
profile page and parses the embedded Google Maps iframe coordinate. It then
compares that official public profile coordinate with the pinned OSM candidate
coordinate from the all-Bangladesh health-feature cache.

## Method

1. Read the four-row source-repair public-evidence attachment.
2. Join each row to the targeted public-map inspection CSV by `inspection_id`.
3. Retrieve each public DGHS profile URL.
4. Parse the official profile map coordinate from the embedded map iframe.
5. Compare the parsed official coordinate with the inspection coordinate and
   the pinned OSM candidate coordinate.
6. Record whether the public profile contains an explicit coordinate-source
   explanation.
7. Keep every row open.

## Results

| Official-coordinate evidence scope | Rows |
|---|---:|
| Source-repair rows checked | 4 |
| DGHS public profiles retrieved | 4 |
| Official profile coordinates exposed | 4 |
| Profile coordinates matching the inspection CSV coordinates | 4 |
| Rows sharing an official profile coordinate | 2 |
| Rows where official coordinate is 10 km or more from named OSM candidate | 2 |
| Rows where official coordinate is 50 km or more from named OSM candidate | 1 |
| Explicit coordinate-source explanations found | 0 |
| Rows closed by this pass | 0 |
| Rows reclassified by this pass | 0 |

The evidence classes are:

| Evidence class | Rows | Reviewer meaning |
|---|---:|---|
| Official profile coordinate shared by multiple DGHS rows | 2 | The two Narayanganj profiles publish the same official map coordinate and point toward the same named OSM candidate; this is a coordinate-collision question, not a duplicate closure. |
| Official profile coordinate long distance from named OSM candidate | 1 | The DGHS profile exposes a coordinate, but the named OSM candidate remains at least 10 km away. |
| Official profile coordinate extreme distance from named OSM candidate | 1 | The DGHS profile exposes a coordinate, but the named OSM candidate remains more than 50 km away. |

## What The Result Means

The official DGHS profile pages make the coordinate problem observable. The
inspection CSV did not invent these coordinates: the same coordinates are
currently exposed in the public DGHS profile pages. For the source-repair queue,
that changes the next review question from "is there a public coordinate?" to
"why does the official public profile expose this coordinate?"

## What It Does Not Mean

This is not human validation, not ground truth, not a row closure, and not a
same-facility reclassification. The pass found official profile coordinates,
but it found zero explicit coordinate-source explanation fields. A row should
remain open until a public official source explains the coordinate, a correction
record, or the facility identity.

## Reproduce the Analysis

```powershell
python public-service-data-quality/scripts/explain-bgd-facility-source-repair-official-coordinates.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json`

## Next Statistical Upgrade

Search for public official correction records, registry change logs, or facility
pages that explain why the exposed DGHS profile coordinate is shared or distant.
Without that source, these rows should stay in the source-repair queue.
