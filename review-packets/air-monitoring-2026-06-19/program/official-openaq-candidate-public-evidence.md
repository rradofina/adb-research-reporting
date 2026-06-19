# Official/OpenAQ candidate public-evidence audit

`attestation_chain: ai-first`

This audit attaches public OpenAQ owner, provider, `isMonitor`, and vintage
metadata to the 13 official/OpenAQ candidate review rows. It is an evidence
attachment, not a decision ledger. It asks what the public OpenAQ metadata
supports before any candidate row is treated as a station crosswalk.

## Why this measurement problem matters

The previous worksheet made the 13 near-plus-name candidate rows reviewable.
The next risk is that a reader may treat a nearby OpenAQ row as if it were the
same official station because it is near and has a partial name signal. Public
OpenAQ metadata can sharpen that review. It can show whether the OpenAQ row has
an owner/provider, whether OpenAQ marks it as `isMonitor`, and whether a
first-seen or last-seen timestamp exists. None of those fields is a station
crosswalk by itself.

## Source added

The script `scripts/audit-official-openaq-candidate-public-evidence.py` reads:

- `generated/air-monitoring-official-openaq-candidate-review.csv`
- `generated/air-monitoring-openaq-station-metadata.csv`

It writes:

- `generated/air-monitoring-official-openaq-candidate-public-evidence.csv`
- `generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json`

The audit checks whether the OpenAQ candidate row has owner/provider metadata,
an `isMonitor` flag, first-seen and last-seen timestamps, exact station-ID
overlap, exact official-agency text in the OpenAQ owner/provider fields, or an
explicit crosswalk signal in the committed public artifacts.

## What the audit found

The audit covers all 13 near-plus-name candidate rows across 4 economies and 9
unique OpenAQ candidate location IDs.

| Public evidence field | Rows |
|---|---:|
| Candidate rows audited | 13 |
| OpenAQ owner/provider metadata present | 13 |
| OpenAQ `isMonitor` true | 6 |
| OpenAQ not marked `isMonitor` | 7 |
| OpenAQ first-seen timestamp present | 11 |
| OpenAQ last-seen timestamp present | 11 |
| Exact station-ID overlap found | 0 |
| Official agency exactly found in OpenAQ owner/provider | 0 |
| Explicit public crosswalk evidence found | 0 |
| Validated same-station joins | 0 |
| Station-radius join-ready rows | 0 |

## Evidence lanes

| Lane | Rows | Interpretation |
|---|---:|---|
| OpenAQ monitor metadata, no crosswalk | 6 | OpenAQ marks the nearby row as `isMonitor`, but no station-ID or agency crosswalk exists in the committed artifacts. |
| OpenAQ non-monitor or sensor metadata, no crosswalk | 7 | OpenAQ metadata is present, but the row is not marked `isMonitor` and has no crosswalk signal. |

## Country-level evidence

| ISO | Candidate rows | `isMonitor` true | Not marked `isMonitor` | Owner/provider rows | First-seen rows | Crosswalk-like signal rows | Validated joins |
|---|---:|---:|---:|---:|---:|---:|---:|
| BGD | 4 | 2 | 2 | 4 | 2 | 0 | 0 |
| IDN | 1 | 0 | 1 | 1 | 1 | 0 | 0 |
| MYS | 3 | 0 | 3 | 3 | 3 | 0 | 0 |
| UZB | 5 | 4 | 1 | 5 | 5 | 0 | 0 |

## Interpretation

This pass makes the candidate queue more useful and less ambiguous. Some rows
point to OpenAQ locations with `isMonitor` set to true, including SPARTAN or
StateAir-linked rows. Other rows point to OpenAQ locations attributed to
AirGradient, Clarity, Kopernik, or an individual owner/provider and are not
marked `isMonitor`. That split is useful for source review, but it does not
close any official/OpenAQ same-station decision.

The most important result is still the zero: no candidate row has exact
station-ID overlap, an exact official-agency match in OpenAQ owner/provider
metadata, or an explicit public crosswalk in the committed artifacts. The
station-radius denominator remains blocked.

## What this does not mean

- It does not validate any official/OpenAQ same-station join.
- It does not certify that an OpenAQ `isMonitor` row is regulatory-grade.
- It does not prove that a non-`isMonitor` OpenAQ row is unimportant or
  unusable.
- It does not classify official monitor grade.
- It does not make any row station-radius-ready.

## Reproduce

```bash
python air-monitoring/scripts/build-official-openaq-candidate-review.py
python air-monitoring/scripts/audit-official-openaq-candidate-public-evidence.py
```

The next upgrade is still row-level public station-crosswalk evidence: station
IDs, source-owner documentation, current-status pages, or documented
co-location evidence that names both the official row and the OpenAQ row.
