---
title: "Bangladesh Facility-Validation AI Closure Audit"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_closure_audit_human_or_source_owner_wall
created: 2026-06-19
---

# Bangladesh Facility-Validation AI Closure Audit

## Why This Measurement Problem Matters

The human-validation worksheet is useful only if the reader can see which
decisions remain open and why. This audit asks the narrow AI-side question:
after the public-source review, handoff matrix, and blank human-validation
worksheet, can AI close, reclassify, correct, or use map-absence language for
any unresolved Bangladesh facility row?

The answer in the current artifact is no. The audit is a decision gate, not a
validation result.

## Data Sources and Coverage

The no-network script reads:

- `generated/psdq-bgd-facility-validation-human-validation-worksheet.csv`

It audits every worksheet row for:

- blank human-validation status,
- blank proposed decision,
- blank source-owner contact fields,
- blank public-evidence and human-location validation references,
- prefilled current-public-evidence gates for closure, reclassification,
  map-absence language, and coordinate correction.

## Results

| AI closure-audit signal | Count |
|---|---:|
| Audit rows | 39 |
| Handoff groups | 5 |
| Upazilas with audit rows | 15 |
| Human- or source-owner wall rows | 39 |
| External contacts made | 0 |
| Blank human-validation status rows | 39 |
| Blank proposed-decision rows | 39 |
| AI closure possible now | 0 |
| AI same-facility reclassification possible now | 0 |
| AI map-absence language possible now | 0 |
| AI coordinate correction possible now | 0 |
| AI actionable without human or source owner now | 0 |
| Keep-open only rows | 39 |

The audit-wall categories are:

| Wall category | Rows |
|---|---:|
| Facility-level absence validation | 18 |
| Public alias/location or human validation | 15 |
| Identity and location validation | 3 |
| Source-owner or human location validation | 3 |

## Interpretation

The audit makes the current stopping point explicit. The AI loop can organize
the evidence, identify row-specific blockers, and prepare a reviewer
worksheet. It cannot replace source-owner clarification or human location
validation.

The practical language for the current public surface is therefore
keep-open-only: do not close the row, do not reclassify the candidate as the
same facility, do not treat an upazila-level zero-OSM signal as a facility
absence finding, and do not correct coordinates from current public evidence.

## Reproduce

```bash
python public-service-data-quality/scripts/build-bgd-facility-ai-closure-audit.py
```

Expected outputs:

- `generated/psdq-bgd-facility-validation-ai-closure-audit.csv`
- `generated/psdq-bgd-facility-validation-ai-closure-audit-summary.json`

## Non-Claim

This is an AI-first no-contact closure audit for unresolved PSDQ Bangladesh
facility-validation rows. It audits whether the current public evidence and
blank human-review fields permit closure, reclassification, map-absence
language, or coordinate correction. It is not external outreach, not human
validation, not ground truth, not a row closure, not a same-facility
reclassification, not a coordinate correction, not a facility-quality
assessment, and not a service-access estimate.
