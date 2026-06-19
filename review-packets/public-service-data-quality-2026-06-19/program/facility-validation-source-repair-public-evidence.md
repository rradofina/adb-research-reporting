---
title: "Bangladesh Source-Repair Public Evidence Attachment"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_repair_evidence_attachment_not_human_validation
created: 2026-06-19
---

# Bangladesh Source-Repair Public Evidence Attachment

## Why This Measurement Problem Matters

The public-source decision ledger identified four rows where source repair has
to come before map-absence or same-facility language. These rows are not ready
for closure because the first question is about the coordinate or source record
itself: why does the DGHS row point toward a particular public-map candidate,
and does public evidence explain the location?

## Data Sources and Coverage

This pass uses two generated public-source artifacts:

- `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`

The upstream confirmation packet already recorded public DGHS profile retrieval
and public OSM API retrieval. This step does not fetch new data. It attaches
those public-source links, HTTP statuses, OSM names, tags, and candidate
distances to the four source-repair-first reviewer questions.

## Method

The script applies a source-repair-only scope.

1. Read the 16-row decision ledger.
2. Select rows where `decision_track` is `source_repair_first`.
3. Join each selected row back to the targeted public-source confirmation
   packet by `confirmation_id`.
4. Attach the public DGHS profile URL, DGHS HTTP status, OSM feature URL, OSM
   API status, candidate name, compact OSM tags, candidate distance, and
   retrieval timestamp.
5. Classify source-repair evidence into shared-candidate and long-distance
   coordinate-source checks.
6. Keep every row open.

## Results

| Source-repair scope | Rows |
|---|---:|
| Decision-ledger rows read | 16 |
| Source-repair rows selected | 4 |
| Public evidence attachments | 4 |
| DGHS profiles attached | 4 |
| OSM API records attached | 4 |
| Rows sharing a public-map candidate | 2 |
| Rows with candidate distance of 10 km or more | 2 |
| Rows with candidate distance of 50 km or more | 1 |
| Rows closed by this pass | 0 |
| Rows reclassified by this pass | 0 |

The four source-repair rows split into three evidence classes:

| Evidence class | Rows | Reviewer meaning |
|---|---:|---|
| Shared public-map candidate across multiple DGHS rows | 2 | Two DGHS rows point to the same public OSM candidate; this is a collision check, not a duplicate closure. |
| Strong name but long coordinate-distance conflict | 1 | The candidate name is strong, but the distance is still too large for a map-absence or same-facility label. |
| Strong name but extreme coordinate-distance conflict | 1 | The candidate name is strong, but the coordinate-distance gap is large enough to require source-coordinate review before any row outcome. |

## What The Result Means

The evidence attachment makes the first repair problem visible. For the two
Narayanganj rows, the public evidence shows a shared OSM candidate and requires
a duplicate/source-coordinate question. For Bera and Durgapur, the public OSM
candidate name is strong, but the candidate distance remains a coordinate-source
problem. The operational implication is sequence: source repair comes first,
then any map-completeness or same-facility review.

## What It Does Not Mean

This is not human validation, not ground truth, not a row closure, and not a
same-facility reclassification. The evidence attachment does not prove which
coordinate is correct. It only records what public DGHS and OSM evidence is
already attached to each source-repair question.

## Reproduce the Analysis

```powershell
python public-service-data-quality/scripts/attach-bgd-facility-source-repair-public-evidence.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json`

## Next Statistical Upgrade

Use the attached public evidence to search for official coordinate/source
explanations for the four source-repair rows. A row should be closed or
reclassified only if a public official source explains the intended coordinate,
the duplicate-source issue, or the facility identity. Otherwise it remains open.
