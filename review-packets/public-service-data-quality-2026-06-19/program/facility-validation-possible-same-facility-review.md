---
title: "Bangladesh Possible Same-Facility Review Packet"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_possible_same_facility_review_not_validation
created: 2026-06-19
---

# Bangladesh Possible Same-Facility Review Packet

## Why This Measurement Problem Matters

Some public-map candidates look close enough in name to tempt a row-level
decision. For a registry-map audit, that is not enough. A mapped hospital with
a similar or even identical name can still be a separate facility, a different
campus, or a public feature that does not resolve the official registry row.

This packet isolates the possible same-facility cases so they can be reviewed
on identity and location together. It keeps them out of both the source-repair
queue and the map-absence claim until a stronger evidence gate is satisfied.

## Data Sources and Coverage

The no-network script reads two committed inputs:

- `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`

The output covers the 3 decision-ledger rows marked
`possible_same_facility_location_review`. All 3 rows have retrieved DGHS public
profiles and retrieved public OSM API feature records.

## Method

The review applies five steps:

1. Select decision-ledger rows whose decision track is possible same-facility
   location review.
2. Join each row to the targeted public-source confirmation record by
   `confirmation_id`.
3. Carry forward DGHS profile retrieval, OSM API retrieval, candidate name
   score, candidate distance, and the original decision question.
4. Classify name support and distance bands as review context, not as
   outcome labels.
5. Block closure, same-facility reclassification, and map-absence language
   unless public evidence or human validation supports identity and location
   together.

## Results

| Possible same-facility review signal | Count |
|---|---:|
| Decision-ledger rows read | 16 |
| Possible same-facility rows reviewed | 3 |
| DGHS profiles retrieved | 3 |
| OSM API records retrieved | 3 |
| Rows with name score at least 0.95 | 1 |
| Rows with candidate distance 2 km or more | 3 |
| External contacts made by AI | 0 |
| Rows allowed for closure | 0 |
| Rows allowed for same-facility reclassification | 0 |
| Rows allowed for map-absence language | 0 |

The row-level review queue is:

| DGHS row | Public OSM candidate | Name score | Distance |
|---|---|---:|---:|
| KPJ SPECIALIZED HOSPITAL & NURSING COLLEGE | Tajmahal Hospital and Diagnostic, Hospital | 0.4691 | 3.2 km |
| Aichi Medical College & Hospital Ltd. | Aichi Medical College Hospital | 1.0000 | 2.3 km |
| Chattogram 250 bed General Hospital | Chittagong Medical College Hospital | 0.6000 | 3.3 km |

The important result is the constraint: even the Aichi row, with a name score
of 1.0000, remains open because the public evidence does not yet establish
identity and location together.

## What The Result Means

The packet turns a tempting automated match into a reviewer-ready question.
It shows which rows deserve manual or source-owner attention first, while
protecting the report from overstating map evidence. The same public evidence
can support different next steps: one row may eventually become a same-facility
reclassification, another may become a map-absence case, and another may remain
unresolved. This pass does not choose among those outcomes.

For the showcase, the practical rule is direct: possible same-facility rows
should stay visible as decision gates, not be counted as closed matches or
confirmed public-map absences.

## What It Does Not Mean

This is not external outreach, not human validation, not ground truth, not a
row closure, not a same-facility reclassification, not a coordinate correction,
not a facility-quality assessment, and not a service-access estimate.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/build-bgd-facility-possible-same-facility-review.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-possible-same-facility-review.csv`
- `generated/psdq-bgd-facility-validation-possible-same-facility-review-summary.json`

## Next Statistical Upgrade

The next AI-doable step is to keep this review gate visible in the public
surface and reviewer packet. The substantive upgrade remains source-owner
clarification or human location validation that can decide whether each
candidate is the same facility, a separate facility, or an invalid candidate.
