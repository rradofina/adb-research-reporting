---
title: "Bangladesh First-Row Public-Source Confirmation"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_confirmation_not_human_validation
created: 2026-06-19
---

# Bangladesh First-Row Public-Source Confirmation

## Why This Measurement Problem Matters

The targeted public-map inspection packet made the PSDQ queue more specific,
but a reviewer still needs to know whether the public source links actually
open and what they say. This pass checks the first inspection rows against two
public source families: the DGHS public profile page and the OSM API record for
the prioritized candidate feature.

## Data Sources and Coverage

The pass starts from
`generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`.
For the first 12 inspection-card rows, it retrieves:

- the public DGHS facility profile URL recorded in the inspection packet; and
- the public OSM API record for the prioritized candidate feature.

The retrieval time is recorded in
`generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json`.

## Method

The script performs four steps.

1. Read the first 12 targeted inspection rows.
2. Fetch each DGHS profile URL and record the HTTP status, final URL, profile
   token support, and profile-id signal.
3. Convert each OSM feature URL into the public OSM API endpoint, retrieve its
   tags, and recompute a live name-support score against the DGHS row name.
4. Keep every row open unless a later public-source/manual review supports a
   closure or reclassification.

## Results

| Check | Count |
|---|---:|
| First inspection rows checked | 12 |
| DGHS profiles retrieved | 12 |
| OSM candidate API records retrieved | 12 |
| Rows with DGHS profile token support | 12 |
| Rows with candidate name score at least 0.75 | 2 |
| Rows closed by this pass | 0 |
| Rows reclassified by this pass | 0 |

The first 12 rows split into four confirmation lanes:

- 7 candidate features were retrieved but still show name conflict or weak
  support.
- 2 source-repair rows have public sources reachable, but duplicate-coordinate
  or coordinate-source questions still come first.
- 2 zero-OSM upazila rows remain observability cases, because the nearest
  public-map candidate is context rather than row-level evidence.
- 1 possible same-facility candidate still needs manual location or
  official-source confirmation before reclassification.

## What The Result Means

The confirmation pass strengthens the reviewer workflow. It shows that the
first DGHS and OSM public links are reachable and that the row queue is not
blocked by dead public URLs. It also prevents overclaiming: reachable public
sources do not automatically make a candidate the same facility.

## What It Does Not Mean

This is not human validation, not ground truth, not a facility-quality
assessment, and not a service-access estimate. A DGHS profile response and an
OSM API tag response are public-source evidence, not a field audit. The rows
remain open until a public map feature, DGHS source correction, or other public
official source supports a row-level decision.

## Reproduce the Analysis

```powershell
python public-service-data-quality/scripts/confirm-bgd-facility-public-map-first-rows.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json`

## Next Statistical Upgrade

The next confirmation packet extends this check to all 40 targeted inspection
rows in `facility-validation-public-source-confirmation-targeted-rows.md`.
Keep the same standard: separate source-repair rows, possible same-facility
candidates, weak candidate links, and zero-OSM observability cases. A row
should be closed or reclassified only when public evidence supports the
change.
