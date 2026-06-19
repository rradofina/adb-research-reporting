---
title: "Bangladesh Priority Name-Conflict Review Packet"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_priority_name_conflict_review_not_validation
created: 2026-06-19
---

# Bangladesh Priority Name-Conflict Review Packet

## Why This Measurement Problem Matters

The public-map inspection queue still contains rows where an OSM health
feature is visible, but its name does not resolve the DGHS registry row. These
cases matter because a nearby mapped hospital can make a facility appear
observable when the evidence is only nearby context.

This packet isolates the priority-1 name-conflict rows. It asks whether the
retrieved public-map candidate is an alias, a same-campus facility, a separate
facility, or only a nearby point that should not close the DGHS row.

## Data Sources and Coverage

The no-network script reads two committed inputs:

- `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`

The output covers the 9 decision-ledger rows marked
`high_exposure_name_conflict_review`. All 9 rows have retrieved DGHS public
profiles and retrieved public OSM API feature records.

## Method

The review applies five steps:

1. Select decision-ledger rows whose decision track is priority-1
   name-conflict review.
2. Join each row to the targeted public-source confirmation record by
   `confirmation_id`.
3. Carry forward DGHS retrieval, OSM retrieval, candidate name score,
   candidate distance, OSM tags, and the original closure gate.
4. Classify the candidate by name-score band, distance band, and whether the
   candidate name contains a district or upazila place name.
5. Block closure, same-facility reclassification, and map-absence language
   unless public alias/location evidence or human validation resolves the name
   conflict.

## Results

| Priority name-conflict review signal | Count |
|---|---:|
| Decision-ledger rows read | 16 |
| Priority-1 name-conflict rows reviewed | 9 |
| DGHS profiles retrieved | 9 |
| OSM API records retrieved | 9 |
| Rows with candidate name score at least 0.70 | 1 |
| Rows with candidate distance 5 km or more | 6 |
| Rows with candidate distance 10 km or more | 1 |
| Rows where candidate contains an admin place name | 4 |
| Public alias/location sources found in current artifacts | 0 |
| Rows allowed for closure | 0 |
| Rows allowed for same-facility reclassification | 0 |
| Rows allowed for map-absence language | 0 |

The row-level score and distance range is wide:

| DGHS row | Public OSM candidate | Name score | Distance |
|---|---|---:|---:|
| Pabna 250 bed General Hospital | Pabna Mental Hospital | 0.7451 | 2.9 km |
| Babur Bagan Community Clinic, Pabna Sadar | ASEAB Health Clinic | 0.4068 | 3.3 km |
| Gazipur District Hospital | Kahinur Multicare Hospital | 0.6667 | 4.5 km |
| Alirtek Community Clinic, Narayanganj Sadar | Narayanganj General Hospital | 0.5000 | 6.1 km |
| Balrampur Community Clinic, Pabna Sadar | ASEAB Health Clinic | 0.3860 | 6.7 km |
| Char Bayragadi Community Clinic, Narayanganj Sadar | Narayanganj General Hospital | 0.3636 | 8.9 km |
| Argariya Community Clinic, Gazipur Sadar | Galaxy Hospital (pvt) Ltd. Monipur, Hospital | 0.4304 | 9.5 km |
| Astanagar Community Clinic, Kushtia Sadar | Islamic University Medical Centre | 0.3562 | 9.8 km |
| Amdia Union Health Sub Center | Narsingdi Sadar Hospital | 0.3019 | 10.7 km |

The practical result is that the public map has useful context, but the
current artifacts do not contain a public alias or location source that would
close any row.

## What The Result Means

The packet separates visibility from resolution. A nearby public-map candidate
is useful for a reviewer because it points to what should be checked next. It
does not, by itself, show that the DGHS row is mapped, absent, duplicated, or
same-facility. The high-exposure rows therefore remain as public-source
questions, not outcomes.

For the showcase, this protects the source-disagreement result from a common
shortcut: treating any nearby public hospital as evidence that the official
row is represented. The packet requires public alias evidence, a public
location source, or human validation before changing a row label.

## What It Does Not Mean

This is not external outreach, not human validation, not ground truth, not a
row closure, not a same-facility reclassification, not a coordinate correction,
not a facility-quality assessment, and not a service-access estimate.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/build-bgd-facility-priority-name-conflict-review.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-priority-name-conflict-review.csv`
- `generated/psdq-bgd-facility-validation-priority-name-conflict-review-summary.json`

## Next Statistical Upgrade

The next AI-doable step is to keep this review gate visible in the public
surface and reviewer packet. The substantive upgrade remains a public alias or
location source, source-owner clarification, or human validation that can
resolve each name conflict without treating nearby mapped hospitals as direct
evidence.
