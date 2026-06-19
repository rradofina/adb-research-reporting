# Candidate-Resolution Pass: Bangladesh PSDQ Facility Flags

`attestation_chain: ai-first`
Date: 2026-06-19
Goal level: L3 candidate-resolution pass
Status: AI public-source candidate resolution, not human validation

## Why This Measurement Problem Matters

The AI review ledger found 8 rows where a nearby OSM health feature exists
but the public-source evidence is not strong enough to close the row. These
are the rows most likely to confuse a reader: some may be aliases or shared
campuses, some may be classification conflicts, and some may be nearby but
unrelated facilities.

This pass turns those 8 rows into narrower review lanes. It does not confirm
that any facility is present, absent, duplicated, correctly classified, or
service-ready.

## Data Sources and Coverage

The script uses only committed public-source artifacts from the PSDQ
facility-validation workflow.

| Input | Local path | Role |
|---|---|---|
| AI review ledger | `generated/psdq-bgd-facility-validation-ai-review.csv` | Source of the 8 candidate-resolution rows |
| OSM candidates | `generated/psdq-bgd-facility-validation-osm-candidates.csv` | Ranked OSM health candidates within 500 meters |
| AI review summary | `generated/psdq-bgd-facility-validation-ai-review-summary.json` | Scope, public-source metadata, and non-claim |

The underlying OSM health-feature cache records
`timestamp_osm_base = 2026-04-29T09:11:39Z`. The pass reviews only the 8
rows queued by the AI review ledger. All 8 remain open after this pass.

## Method

The resolution script applies deterministic public-source rules:

1. Mark a probable alias/campus lane only when the best OSM candidate is very
   close, category-compatible, and has a high combined score.
2. Mark a same-site classification-conflict lane when the best candidate is
   within 75 meters but DGHS and OSM facility categories differ.
3. Mark a possible-alias lane when the best candidate has name signal but
   distance or registry category prevents stronger coding.
4. Mark a local-script name-gap lane when an OSM health candidate in
   non-Latin script is spatially close but the automated string match is weak.
5. Keep weak or mixed evidence in ambiguous or weak-nearby lanes.

No row is closed as a confirmed same-facility match.

## Results

| Candidate-resolution lane | Rows |
|---|---:|
| `probable_same_facility_alias_or_campus` | 1 |
| `probable_same_site_classification_conflict` | 2 |
| `possible_alias_requires_name_check` | 2 |
| `local_script_candidate_requires_name_check` | 1 |
| `ambiguous_nearby_candidate` | 1 |
| `weak_nearby_osm_signal` | 1 |

| Sample group | Rows | Alias/campus | Same-site type conflict | Possible alias | Local-script name gap | Ambiguous | Weak nearby |
|---|---:|---:|---:|---:|---:|---:|---:|
| `comparison_mid_ratio` | 3 | 0 | 1 | 1 | 0 | 1 | 0 |
| `osm_ge_registry` | 5 | 1 | 1 | 1 | 1 | 0 | 1 |

The strongest row-level signal is Asgar Ali Medical College & Hospital
Limited, where the OSM candidate "Asgar Ali Hospital" is 12.6 meters away
with the highest combined candidate score in this queue. The pass still keeps
the row open because public-source name confirmation is needed before the
same-facility label is treated as resolved.

The most instructive weak-string case is Ahsania Mission Cancer and General
Hospital. The best-scoring candidate is not a good name match, but another
nearby OSM hospital candidate appears in non-Latin script within 18.9 meters.
That is a source-resolution problem, not evidence that the sampled row is
unmapped.

## What the Result Means

This improves the PSDQ source-disagreement package because the first row-level
question is now specific. A reviewer does not need to start with all 71 flagged
rows. The candidate queue is split into alias/campus checks, type-conflict
checks, possible aliases, a local-script name check, and weak or ambiguous
nearby features.

The next publication use is still conservative: show this as a source-QA
ladder before any access-map or service-coverage result.

## What It Does Not Mean

- This is not human validation.
- The pass does not confirm any same-facility row.
- A probable alias/campus lane does not prove that the DGHS row and OSM
  feature are the same institution.
- A local-script candidate does not prove a translation or equivalence.
- A weak nearby OSM signal does not mean the registry row is wrong.
- The result does not measure access, quality, travel time, population,
  households, poverty, demand, or catchments.
- The result does not change the existing PSDQ maturity label or make the
  artifact human-final.

## Reproduce the Pass

```bash
python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py
python public-service-data-quality/scripts/review-bgd-facility-validation-flags.py
python public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py
```

Outputs:

- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution.csv`
- `public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`

## Next Statistical Upgrade

The first richer public-source tag scan now lives in
`facility-validation-candidate-public-source-check.md`. Use that source-check
artifact as the immediate row-level worklist. Confirm same-site OSM tag
support, same-site type/label conflicts, coordinate/function conflicts, and
weak nearby features against public DGHS, OSM, or other official public pages
before changing any source-disagreement claim. The coordinate-source repair
triage now lives in `facility-validation-coordinate-repair.md`, and the
public-map-gap triage now lives in
`facility-validation-public-map-gap.md`. The row-level public-source evidence
ledger for the open public-map-gap rows now lives in
`facility-validation-public-map-gap-evidence.md`, and the targeted public-map
inspection packet now lives in
`facility-validation-public-map-inspection.md`. The next upgrade is
public-source/manual confirmation of the first inspection rows before changing
any row-level or source-disagreement claim.
