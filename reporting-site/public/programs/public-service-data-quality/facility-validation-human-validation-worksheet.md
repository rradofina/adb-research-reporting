---
title: "Bangladesh Facility-Validation Human-Validation Worksheet"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_human_validation_worksheet_not_validation
created: 2026-06-19
---

# Bangladesh Facility-Validation Human-Validation Worksheet

## Why This Measurement Problem Matters

The handoff matrix identifies the PSDQ Bangladesh rows that cannot be resolved
by AI-only public-source review. A human reviewer still needs a consistent
instrument: the same row identifiers, the same public evidence basis, the same
decision vocabulary, and the same minimum evidence rules.

This worksheet provides that instrument. It is not a validation result.

## Data Sources and Coverage

The no-network script reads:

- `generated/psdq-bgd-facility-validation-human-gated-handoff.csv`

It writes a worksheet that keeps every human-review decision field blank while
pre-filling:

- the handoff row and inspection identifiers,
- the facility, district, upazila, and candidate fields,
- the public evidence basis already assembled by the AI loop,
- the review question,
- the minimum acceptable evidence rule,
- the allowed decision values for the row class, and
- the current public-evidence gates, all of which remain false.

## Results

| Worksheet signal | Count |
|---|---:|
| Worksheet rows | 39 |
| Handoff groups | 5 |
| Primary reviewer-role classes | 2 |
| Blank human-validation status rows | 39 |
| Blank proposed-decision rows | 39 |
| Prefilled external contacts made | 0 |
| Prefilled closure-allowed rows | 0 |
| Prefilled reclassification-allowed rows | 0 |
| Prefilled map-absence-allowed rows | 0 |
| Prefilled coordinate-correction-allowed rows | 0 |

The worksheet groups are:

| Handoff group | Rows |
|---|---:|
| Zero-OSM facility-row absence validation | 18 |
| Priority name-conflict alias/location validation | 9 |
| Lower-priority name-conflict alias/location validation | 6 |
| Possible same-facility validation | 3 |
| Source-repair owner clarification | 3 |

The reviewer-role allocation is:

| Primary reviewer role | Rows |
|---|---:|
| Human location reviewer | 36 |
| Source owner or human location reviewer | 3 |

## Interpretation

The worksheet is designed to prevent two mistakes:

1. Treating a visible public-map candidate as a row closure without validating
   identity and location together.
2. Treating upazila-level zero-OSM observability as a facility-level absence
   finding.

The blank decision fields are intentional. A future reviewer can fill them only
after public official evidence, source-owner response, or human location
validation supplies the missing evidence.

## Reproduce

```bash
python public-service-data-quality/scripts/build-bgd-facility-human-validation-worksheet.py
```

Expected outputs:

- `generated/psdq-bgd-facility-validation-human-validation-worksheet.csv`
- `generated/psdq-bgd-facility-validation-human-validation-worksheet-summary.json`

## Non-Claim

This is an AI-first no-contact worksheet for unresolved PSDQ Bangladesh
facility-validation rows. It pre-fills public evidence, review questions, and
decision rules for a future human or source-owner review. It is not external
outreach, not human validation, not ground truth, not a row closure, not a
same-facility reclassification, not a coordinate correction, not a
facility-quality assessment, and not a service-access estimate.
