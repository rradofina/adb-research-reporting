---
title: "Bangladesh Zero-OSM Upazila Observability Review Packet"
program: public-service-data-quality
attestation_chain: ai-first
status: ai_zero_osm_upazila_observability_review_not_validation
created: 2026-06-19
---

# Bangladesh Zero-OSM Upazila Observability Review Packet

## Why This Measurement Problem Matters

A source-disagreement map can mislead if a zero in the public-map layer is
read as facility absence. In the Bangladesh PSDQ module, some upazilas have
active DGHS clinical registry rows but no joined OSM health features. That is
a source-observability signal. It is not enough to decide whether any specific
facility is unmapped, duplicated, wrongly located, or absent from the public
map.

This packet keeps that distinction visible. It turns the zero-OSM lane into an
upazila-level review queue and blocks row-level closure unless facility-level
public evidence or human validation is available.

## Data Sources and Coverage

The no-network script reads four committed inputs:

- `generated/psdq-bgd-exposure-ranked-disagreement.csv`
- `generated/psdq-bgd-exposure-ranked-disagreement-summary.json`
- `generated/psdq-bgd-facility-validation-public-map-inspection.csv`
- `generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`

The output covers upazilas where `active_clinical_facilities` is greater than
0 and `osm_health` equals 0. It then joins the targeted public-map inspection
queue to identify rows already deferred as upazila observability context.

## Method

The review applies six steps:

1. Read the exposure-ranked source-disagreement table.
2. Select upazilas with active DGHS clinical registry rows and zero joined OSM
   health features.
3. Carry forward active registry counts, coordinate-ready counts, Open
   Buildings p85 context, OSM boundary-match status, and denominator status.
4. Join the targeted public-map inspection queue by `join_key` where the lane
   is `upazila_public_map_observability_gap`.
5. Classify zero-OSM upazilas into boundary-join residue, missing denominator,
   high registry-count, high building-proxy, or general observability-context
   classes.
6. Allow upazila-level observability language while blocking facility-row
   closure, facility absence language, coordinate correction, and
   reclassification.

## Results

| Zero-OSM observability signal | Count |
|---|---:|
| Exposure rows read | 572 |
| Active-registry upazilas with zero OSM health features | 115 |
| Active clinical registry rows in those upazilas | 3,879 |
| Share of exposure rows in the zero-OSM class | 20.1% |
| Share of active clinical registry rows in the zero-OSM class | 13.8% |
| Zero-OSM upazilas with Open Buildings denominator | 108 |
| Zero-OSM upazilas with OSM boundary match | 75 |
| 3 km p85 under-observed building proxy in zero-OSM upazilas | 2,334,152 |
| Targeted inspection rows in the zero-OSM lane | 18 |
| Targeted zero-OSM upazilas | 5 |
| Facility rows allowed for closure | 0 |
| Facility rows allowed for absence language | 0 |
| Coordinate corrections allowed | 0 |

The review separates the 115-upazila context from the 18 targeted inspection
rows:

| Division | Zero-OSM upazilas | Active clinical rows | Targeted inspection rows |
|---|---:|---:|---:|
| Chattogram | 32 | 940 | 0 |
| Dhaka | 27 | 804 | 8 |
| Rangpur | 14 | 610 | 6 |
| Rajshahi | 11 | 457 | 0 |
| Barishal | 10 | 301 | 0 |
| Sylhet | 8 | 144 | 0 |
| Khulna | 7 | 326 | 4 |
| Mymensingh | 6 | 297 | 0 |

The class split is also important:

| Review class | Rows |
|---|---:|
| Boundary-join residue review first | 40 |
| High building-proxy zero-OSM context | 5 |
| High registry-count zero-OSM context | 8 |
| General zero-OSM observability context | 62 |

The five targeted upazilas are Sonargaon, Sharsha, Araihazar, Pirganj, and
Parbatipur. They should stay in the reviewer queue, but the packet does not
convert their upazila-level OSM zero into row-level closure evidence.

## What The Result Means

The result supports a source-quality statement: there are upazilas where the
official registry records active clinical facilities but the pinned public-map
health-feature layer has no joined health features. That is useful for
prioritizing source checks, validation samples, and public-map completeness
reviews.

For a reader, the operational value is that the map gap is no longer a single
undifferentiated red cell. The packet shows where the issue is broad upazila
observability, where boundary joins need review first, and where targeted
facility rows must stay open until a facility-level source resolves them.

## What It Does Not Mean

This is not facility-level absence evidence, not external outreach, not human
validation, not ground truth, not a row closure, not a coordinate correction,
not a facility-quality assessment, and not a service-access estimate.

## Reproduce The Analysis

Run:

```bash
python public-service-data-quality/scripts/build-bgd-facility-zero-osm-upazila-observability-review.py
```

Outputs:

- `generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review.csv`
- `generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json`

## Next Statistical Upgrade

The next upgrade is a refreshed public-map extraction plus targeted
facility-level public evidence inside the zero-OSM upazilas. Until then, the
correct reader-facing language is upazila observability context, not facility
absence.
