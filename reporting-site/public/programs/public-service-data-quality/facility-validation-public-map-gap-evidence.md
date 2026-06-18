---
title: "Bangladesh Facility-Validation Public-Map-Gap Row Evidence"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_public_source_public_map_gap_row_evidence_not_human_validation
created: 2026-06-19
---

# Bangladesh Facility-Validation Public-Map-Gap Row Evidence

## Why This Measurement Problem Matters

The public-map-gap triage showed that 40 sampled DGHS rows have valid registry
coordinates but no OSM health feature inside the original 500 meter screen.
That is still too broad for a reviewer. A row can be high priority because it
sits in a dense, under-observed upazila, but the next action depends on the
source trail: whether the DGHS profile exists, whether the coordinate is reused,
whether a same-upazila OSM feature is nearby, and whether the issue is a row
match problem or an upazila-level public-map observability gap.

This pass turns the 40 open rows into row-level public-source evidence notes.
It gives the reviewer a source URL, a map inspection URL, an OSM evidence
summary, and a keep-open decision for every row.

## Data Sources and Coverage

The row-evidence script uses only committed public-source artifacts:

- `generated/psdq-bgd-facility-validation-public-map-gap.csv` - the 40-row
  public-map-gap triage ledger.
- `generated/psdq-bgd-facility-validation-public-map-gap-summary.json` - the
  public-map-gap lane counts and upazila queue.
- Cached DGHS public DataTables rows referenced by the triage ledger, including
  public profile URL, facility name, type, active status, and public/private
  field.
- The pinned all-Bangladesh OSM/Overpass health-feature cache already joined in
  the triage ledger.

The script does not cache full DGHS profile HTML. The public profile URLs are
recorded, but the committed evidence keeps only structured source metadata that
is already in the public DGHS table cache.

Outputs:

- `generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv`
- `generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`

## Method

The deterministic script
`scripts/build-bgd-facility-public-map-gap-row-evidence.py` runs four steps.

1. Read the 40 open public-map-gap rows and rank them with priority-1
   high-exposure rows first, then by the Open Buildings under-observed proxy.
2. Attach a DGHS source note from the public registry cache: public profile
   URL, facility name, type, status field, active status, and cache file.
3. Attach an OSM source note from the pinned OSM health-feature cache: registry
   coordinate inspection URL, nearest same-upazila OSM health feature, best
   same-upazila name signal, or zero-OSM expected-upazila note.
4. Keep every row open and assign the next reviewer action: source repair
   first, possible match or buffer review, row-level public-map absence review,
   or upazila-level public-map observability review.

## Results

The script writes row-level evidence for all 40 open public-map-gap rows. It
covers all 30 priority-1 high-exposure rows and all 10 spot-check rows. Every
row has a DGHS public profile URL and an OSM coordinate-inspection URL. Twenty
two rows have a same-upazila OSM health-feature URL in the pinned cache.

The row-evidence tiers are:

| Row-evidence tier | Rows | Reader action |
|---|---:|---|
| Source repair before row absence | 4 | Resolve duplicate coordinates or far same-name signals before using the row as facility-specific evidence. |
| Possible match or buffer review | 3 | Inspect the linked OSM feature and DGHS coordinate together; the row could change under a wider buffer or alias rule. |
| Row-level public-map absence review | 15 | Same-upazila OSM features exist, but not at the sampled DGHS coordinate; inspect before treating as facility-specific absence. |
| Upazila-level public-map observability review | 18 | The expected upazila has no joined OSM health feature in the pinned health-feature cache. |

The first review queue is no longer generic. Gazipur Sadar leads the evidence
rank because it has 197 active clinical DGHS facilities, 58 joined OSM health
features, and the highest Open Buildings under-observed proxy in this queue.
Its first three rows split across one buffer-sensitive case and two row-level
absence candidates, so they should not be summarized as a single kind of
map-gap row. Narayanganj Sadar follows with four high-priority rows, but two
hospital rows reuse the same DGHS coordinate and therefore require source repair
before any facility-specific map-absence interpretation.

The evidence also clarifies the zero-OSM cases. Sonargaon, Sharsha, Araihazar,
Pirganj, and Parbatipur are not row closures. They are upazila-level public-map
observability cases in this pinned OSM health-feature query; another public map
tag family or a manually inspected OSM feature could still change a specific
row.

## What This Does Not Mean

This is not human validation. It does not prove that a DGHS facility is missing
from OSM, does not prove that an OSM feature is the same facility, and does not
estimate health-service access, facility quality, staffing, demand, or
catchment coverage.

The correct interpretation is narrower: the 40-row queue now has row-level
public-source evidence sufficient to tell a reviewer what to inspect next.
All 40 rows remain open.

## Reproduce the Analysis

Run:

```bash
python public-service-data-quality/scripts/build-bgd-facility-public-map-gap-row-evidence.py
```

Then inspect:

```bash
public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv
public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json
```

## Next Statistical Upgrade

The next PSDQ loop should use the row-evidence ledger for targeted public-map
inspection. Start with the priority-1 rows in Gazipur Sadar, Narayanganj
Sadar, Pabna Sadar, and the zero-OSM upazila queue. Close a row only if a
public source supports the closure. Otherwise keep the row open and record the
specific unresolved source question.
