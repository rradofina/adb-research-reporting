# AI Public-Source Review Ledger: Bangladesh PSDQ Facility Flags

`attestation_chain: ai-first`
Date: 2026-06-19
Goal level: L3 AI public-source review ledger
Status: AI public-source row review, not human validation

## Why This Measurement Problem Matters

The automated coded screen flagged 71 of the 76 sampled DGHS facility rows for
additional review. Leaving those rows as one undifferentiated queue would make
the PSDQ source-disagreement package hard to act on. A planner or reviewer
needs to know whether a row is a coordinate-source problem, a missing public
map feature, a name or type conflict, or a nearby OSM feature that does not
match the sampled registry name.

This ledger turns the flagged queue into those workstreams. It is a review
aid, not a validation decision.

## Data Sources and Coverage

The script uses only committed public-source artifacts from the previous PSDQ
facility-validation steps.

| Input | Local path | Role |
|---|---|---|
| Automated coded screen | `generated/psdq-bgd-facility-validation-coded-screen.csv` | Validation code, coordinate status, and best OSM candidate fields |
| OSM candidates | `generated/psdq-bgd-facility-validation-osm-candidates.csv` | Ranked OSM health candidates within 500 meters |
| Coded summary | `generated/psdq-bgd-facility-validation-coded-summary.json` | Public-source metadata and non-claim |

The underlying OSM health-feature cache records
`timestamp_osm_base = 2026-04-29T09:11:39Z`. The ledger reviews only the 71
rows already flagged by the automated screen; the 5 same-facility rows are not
reopened.

## Method

The review script applies a deterministic second pass over the flagged rows:

1. Keep registry-coordinate issues separate from OSM map-absence rows.
2. Treat rows with no OSM health candidate within 500 meters of a usable DGHS
   coordinate as public-map-gap checks, not as proof that the facility is
   absent.
3. Put probable aliases and classification mismatches into a name/type
   resolution queue.
4. Put OSM-only candidates into a separate nearby-OSM-without-registry-match
   queue.
5. Preserve the row-level follow-up question and top OSM candidate evidence in
   the CSV so a human or later public-source review can work row by row.

## Results

| AI review workstream | Rows |
|---|---:|
| `public_map_gap_at_valid_coordinate` | 40 |
| `registry_coordinate_repair` | 23 |
| `candidate_name_or_type_resolution` | 6 |
| `nearby_osm_without_registry_match` | 2 |

| Sample group | Flagged rows | Public-map gap | Coordinate repair | Name/type resolution | Nearby OSM without match |
|---|---:|---:|---:|---:|---:|
| `comparison_mid_ratio` | 19 | 9 | 7 | 3 | 0 |
| `high_exposure_gap` | 18 | 12 | 6 | 0 | 0 |
| `osm_ge_registry` | 14 | 1 | 8 | 3 | 2 |
| `zero_osm_high_proxy` | 20 | 18 | 2 | 0 | 0 |

The next queue is therefore not one task. Eight rows need candidate-level
name/type or nearby-feature resolution first. Thirty high-exposure rows have
usable DGHS coordinates but no OSM health point within 500 meters in the
pinned OSM snapshot. Twenty-three rows need coordinate-source repair before
they can support a map-matching judgment.

## What the Result Means

The Bangladesh source-disagreement report can now show the reader what kind of
source problem sits behind the facility sample. The zero-OSM/high-proxy group
is mostly a public-map-gap inspection task. The OSM-above-registry group is a
more mixed source problem: it includes coordinate repair, name/type resolution,
and nearby OSM features that do not match the sampled DGHS row by name.

This strengthens the PSDQ showcase because the caveat is no longer generic.
The report can say which public-source checks remain and why they matter
before a service-access map uses the facility layer.

## What It Does Not Mean

- This is not human validation.
- The ledger does not prove a facility is present, absent, open, closed,
  correctly classified, or service-ready.
- A missing OSM health feature within 500 meters does not mean a facility does
  not exist.
- A coordinate-source issue does not mean the facility name or registry row is
  wrong.
- The ledger does not measure access, quality, travel time, population,
  households, poverty, demand, or catchments.
- The result does not change the existing PSDQ maturity label or make the
  artifact human-final.

## Reproduce the Ledger

```bash
python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/review-bgd-facility-validation-flags.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review-summary.json`

## Next Statistical Upgrade

The first richer public-source tag scan now lives in
`facility-validation-candidate-public-source-check.md`, and the coordinate
source-repair triage now lives in `facility-validation-coordinate-repair.md`.
The public-map-gap triage now lives in
`facility-validation-public-map-gap.md`. Together these passes narrow the
ledger before any row is read as a candidate OSM absence case. The row-level
public-source evidence ledger now lives in
`facility-validation-public-map-gap-evidence.md`: it records DGHS profile
links, OSM coordinate links, feature or absence notes, and the reason each row
remains open. The next PSDQ loop should run targeted public-map inspection from
that ledger. Keep unresolved rows unresolved unless public evidence supports a
row-level label.
