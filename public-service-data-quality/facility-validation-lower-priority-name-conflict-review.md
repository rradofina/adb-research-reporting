---
title: "Bangladesh Lower-Priority Name-Conflict Spot-Check Packet"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_lower_priority_name_conflict_review_not_validation
created: 2026-06-19
---

# Bangladesh Lower-Priority Name-Conflict Spot-Check Packet

## Why This Measurement Problem Matters

The priority name-conflict review showed that public-map candidates can be
retrieved without resolving a DGHS row. This packet asks whether the same
problem persists outside the high-exposure queue.

It reviews the six lower-priority name-conflict rows that the public-source
decision ledger deferred. These rows are useful as a pressure test: they are
community-clinic rows, the retrieved public-map candidates are differently
named clinics or hospitals, and two candidate features each appear for two
DGHS rows in the same upazila. Candidate reuse is context. It is not a row
resolution.

## Data Sources and Coverage

The no-network script reads two committed inputs:

- `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
- `generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`

The output covers targeted confirmation rows where
`public_source_confirmation_lane` equals
`candidate_feature_retrieved_but_name_conflict_keep_open` and
`priority_scope` is not `priority_1_high_exposure`.

## Method

The review applies six steps:

1. Read the 40-row targeted public-source confirmation packet.
2. Select lower-priority name-conflict rows deferred by the decision ledger.
3. Carry forward DGHS profile retrieval, OSM API retrieval, live candidate
   name, candidate distance, and candidate tags.
4. Group rows by public-map candidate feature to identify reused candidate
   pairs.
5. Classify rows as repeated-candidate context, long-distance single
   candidate context, partial-name unresolved, or different-name unresolved.
6. Block closure, same-facility reclassification, map-absence language, and
   coordinate correction unless public alias/location evidence or human
   validation is available.

## Results

| Lower-priority name-conflict signal | Count |
|---|---:|
| Targeted confirmation rows read | 40 |
| Deferred lower-priority name-conflict rows reviewed | 6 |
| DGHS profiles retrieved | 6 |
| OSM API records retrieved | 6 |
| Unique public-map candidate features | 4 |
| Candidate features reused by multiple rows | 2 |
| Rows sharing reused candidate features | 4 |
| Districts in the spot check | 3 |
| Upazilas in the spot check | 3 |
| Rows with name score at least 0.50 | 1 |
| Rows with name score at least 0.70 | 0 |
| Rows at least 5 km from the candidate | 6 |
| Rows at least 10 km from the candidate | 3 |
| Public alias/location sources found in current artifacts | 0 |
| Facility rows allowed for closure | 0 |
| Rows allowed for same-facility reclassification | 0 |
| Rows allowed for map-absence language | 0 |

The six-row backstop concentrates in three upazilas:

| District | Upazila | Rows | Candidate names | Distance range |
|---|---|---:|---|---:|
| Natore | Gurudaspur | 2 | momotaz clinic / momotaz clinic | 7.8-13.7 km |
| Netrakona | Durgapur | 2 | Broadbank Clinic Quatere / Broadbank Clinic Quatere | 7.8-10.6 km |
| Pabna | Bera | 2 | Nurunnahar Diogonostic Center / Chowdhury Clinic | 8.8-20.9 km |

## Interpretation

The lower-priority spot check strengthens the same caveat as the priority
review. Public-source retrieval is not enough. In this set, all rows have
reachable DGHS and OSM evidence, but none has a public alias or location
source that links the DGHS row to the mapped candidate.

Two repeated candidates are especially important:

- `momotaz clinic` appears for two Gurudaspur community-clinic rows.
- `Broadbank Clinic Quatere` appears for two Durgapur community-clinic rows.

Those repeated candidates are evidence that the public map contains nearby
health features. They are not evidence that the DGHS rows are closed,
duplicated, absent from the map, or represented by the retrieved feature.

## What Would Change the Label

A row can move out of this open name-conflict state only with traceable public
evidence or human validation that resolves identity and location together:

- an official DGHS alias or facility page that names the public-map candidate;
- a public location source linking the DGHS facility to the mapped feature;
- source-owner clarification; or
- human validation that the candidate is the same facility or a separate
  facility.

Until then, the lower-priority rows remain open. They can support a reviewer
queue. They cannot support closure, same-facility reclassification, or
facility-specific map-absence language.

## Reproduce

```bash
python public-service-data-quality/scripts/build-bgd-facility-lower-priority-name-conflict-review.py
```

Expected outputs:

- `generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv`
- `generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json`

## Non-Claim

This is an AI-first no-contact spot-check review packet for PSDQ
lower-priority name-conflict public-map candidates. It reads public DGHS and
OSM retrieval artifacts and translates them into review gates. It is not
external outreach, not human validation, not ground truth, not a row closure,
not a same-facility reclassification, not a coordinate correction, not a
facility-quality assessment, and not a service-access estimate.
