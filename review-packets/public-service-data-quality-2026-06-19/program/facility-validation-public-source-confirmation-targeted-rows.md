---
title: "Bangladesh Targeted-Row Public-Source Confirmation"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_confirmation_targeted_rows_not_human_validation
created: 2026-06-19
---

# Bangladesh Targeted-Row Public-Source Confirmation

## Why This Measurement Problem Matters

The first public-source confirmation pass showed that the initial inspection
rows were not blocked by dead source links. A reviewer still needs to know
whether that pattern holds across the full targeted inspection packet. This
pass extends the check from the first 12 rows to all 40 targeted inspection
rows, preserving the same rule: public-source reachability is evidence for
review, not a row-level validation decision.

## Data Sources and Coverage

The pass starts from
`generated/psdq-bgd-facility-validation-public-map-inspection.csv`, the
40-row targeted public-map inspection ledger. For each row, it retrieves:

- the public DGHS facility profile URL recorded in the inspection packet; and
- the public OSM API record for the prioritized candidate feature.

The retrieval time is recorded in
`generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`.

## Method

The script performs five steps.

1. Read all 40 targeted inspection rows.
2. Fetch each DGHS profile URL and record the HTTP status, final URL, profile
   token support, and profile-id signal.
3. Convert each prioritized OSM feature URL into the public OSM API endpoint,
   retrieve its tags, and recompute a live name-support score against the DGHS
   row name.
4. Assign each row to a confirmation lane: name conflict, possible same
   facility requiring manual location check, source repair, or zero-OSM
   observability context.
5. Keep every row open unless a later public-source/manual review supports a
   closure or reclassification.

## Results

| Check | Count |
|---|---:|
| Targeted inspection rows checked | 40 |
| Priority-1 rows checked | 30 |
| DGHS profiles retrieved | 40 |
| OSM candidate API records retrieved | 40 |
| Rows with DGHS profile token support | 40 |
| Rows with candidate name score at least 0.75 | 6 |
| Rows closed by this pass | 0 |
| Rows reclassified by this pass | 0 |

The 40 rows split into four confirmation lanes:

- 18 zero-OSM context rows remain upazila-level public-map observability cases.
- 15 candidate features were retrieved but still show name conflict or weak
  support.
- 4 source-repair rows have public sources reachable, but duplicate-coordinate
  or coordinate-source questions still come first.
- 3 possible same-facility candidates need manual location or official-source
  confirmation before reclassification.

## What The Result Means

The confirmation pass strengthens the source audit. The full targeted queue is
now covered by live public-source retrieval records, so the next reviewer can
work from documented DGHS and OSM responses rather than from source links
alone. The lane split also shows why row closure remains cautious: most rows
are not missing-source problems; they are classification, matching, or
observability questions.

## What It Does Not Mean

This is not human validation, not ground truth, not a facility-quality
assessment, and not a service-access estimate. A DGHS profile response and an
OSM API tag response are public-source evidence, not a field audit. The rows
remain open until a public map feature, DGHS source correction, or other public
official source supports a row-level decision.

## Reproduce the Analysis

```powershell
python public-service-data-quality/scripts/confirm-bgd-facility-public-map-targeted-rows.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`

## Next Statistical Upgrade

Use the targeted-row confirmation packet to build a decision ledger for the
rows with plausible same-facility signals and for the source-repair rows. Keep
zero-OSM upazila cases separate from facility-specific absence candidates, and
close or reclassify a row only when public evidence supports the change.
