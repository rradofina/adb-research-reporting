---
title: "Bangladesh Facility-Validation Human-Gated Handoff Matrix"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_human_gated_handoff_not_validation
created: 2026-06-19
---

# Bangladesh Facility-Validation Human-Gated Handoff Matrix

## Why This Measurement Problem Matters

The PSDQ Bangladesh review has enough public evidence to say where the
registry-map disagreement is concentrated. It does not have enough evidence to
close every facility row. This matrix makes that boundary explicit.

It consolidates the rows that remain human- or source-owner-gated after the
AI-only public-source loop: source-repair clarifications, possible
same-facility candidates, priority and lower-priority name conflicts, and
zero-OSM facility-row absence decisions. It is a reviewer queue. It is not a
validation result.

## Data Sources and Coverage

The no-network script reads five committed inputs:

- `generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv`
- `generated/psdq-bgd-facility-validation-possible-same-facility-review.csv`
- `generated/psdq-bgd-facility-validation-priority-name-conflict-review.csv`
- `generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv`
- `generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json`

The output covers every row where the current public evidence says "keep
open" because an owner clarification, public alias/location source, or human
validation is still required.

## Results

| Human-gated handoff signal | Count |
|---|---:|
| Handoff rows | 39 |
| Handoff groups | 5 |
| Upazilas with handoff rows | 15 |
| Human- or owner-action required rows | 39 |
| External contacts made | 0 |
| Facility rows allowed for closure | 0 |
| Same-facility reclassifications allowed | 0 |
| Map-absence uses allowed | 0 |
| Coordinate corrections allowed | 0 |

The handoff groups are:

| Handoff group | Rows |
|---|---:|
| Source-repair owner clarification | 3 |
| Possible same-facility validation | 3 |
| Priority name-conflict alias/location validation | 9 |
| Lower-priority name-conflict alias/location validation | 6 |
| Zero-OSM facility-row absence validation | 18 |

The largest current wall is the zero-OSM facility-row absence gate. Upazila
context can explain why the public map is sparse. It cannot close a specific
DGHS facility row.

## Interpretation

This matrix is the current "do not overclaim" surface for the PSDQ Bangladesh
module:

- Source-repair rows need owner clarification or human review before
  coordinate-source questions are treated as resolved.
- Possible same-facility rows need identity and location validated together.
- Name-conflict rows need public alias/location evidence or human validation
  before a candidate feature can become a same-facility or map-absence label.
- Zero-OSM rows need facility-level evidence before an upazila-level
  observability signal becomes a row-level absence statement.

All 39 rows remain open. The matrix closes 0 rows, reclassifies 0 rows, makes
0 coordinate corrections, and makes 0 external contacts.

## Reproduce

```bash
python public-service-data-quality/scripts/build-bgd-facility-human-gated-handoff.py
```

Expected outputs:

- `generated/psdq-bgd-facility-validation-human-gated-handoff.csv`
- `generated/psdq-bgd-facility-validation-human-gated-handoff-summary.json`

## Non-Claim

This is an AI-first no-contact handoff matrix for unresolved PSDQ Bangladesh
facility-validation rows. It consolidates public evidence and states the owner
or human-validation gate. It is not external outreach, not human validation,
not ground truth, not a row closure, not a same-facility reclassification, not
a coordinate correction, not a facility-quality assessment, and not a
service-access estimate.
