# Official/OpenAQ candidate review worksheet

`attestation_chain: ai-first`

This worksheet turns the strongest official/OpenAQ reconciliation lane into a
review queue. It starts from rows where the official station-source extraction
found both signals: the nearest OpenAQ PM2.5 row is within 5 kilometers, and
the station-name comparison found an overlap signal. It does not validate the
rows as same-station joins.

## Why this measurement problem matters

The reconciliation audit found 13 near-plus-name candidate rows. Those are the
rows a reader would naturally want to use first in a catchment or station-radius
map. That would be premature. A proximity signal and a name-overlap signal make
a row worth reviewing, but they do not prove that the official record and the
OpenAQ record are the same station.

## Source added

The script `scripts/build-official-openaq-candidate-review.py` reads:

- `generated/air-monitoring-official-openaq-reconciliation.csv`
- `generated/air-monitoring-regulator-station-extraction.csv`

It writes:

- `generated/air-monitoring-official-openaq-candidate-review.csv`
- `generated/air-monitoring-official-openaq-candidate-review-summary.json`

The worksheet filters only `near_and_name_overlap_candidate` rows. It carries
forward source name, agency, source URL, station ID, station name, nearest
OpenAQ location, distance, review question, allowed decisions, and the minimum
evidence needed before a row can be closed.

## What the worksheet found

The worksheet covers 13 candidate rows across 4 economies. The exact run
timestamp is recorded in the generated JSON.

| Review status | Rows |
|---|---:|
| Near-plus-name candidate rows in the worksheet | 13 |
| Economies with candidate rows | 4 |
| Rows with station-ID crosswalk evidence | 0 |
| Rows with public current-status confirmation | 0 |
| Validated same-station joins | 0 |
| Separate nearby-station decisions | 0 |
| Insufficient-public-evidence rows still open | 13 |
| Station-radius join-ready rows | 0 |

## Country-level review queue

| ISO | Candidate rows | Unique OpenAQ candidate IDs | Minimum distance, km | Maximum distance, km | Validated joins | Radius-ready rows |
|---|---:|---:|---:|---:|---:|---:|
| BGD | 4 | 3 | 0.532 | 1.850 | 0 | 0 |
| IDN | 1 | 1 | 2.372 | 2.372 | 0 | 0 |
| MYS | 3 | 3 | 1.367 | 4.502 | 0 | 0 |
| UZB | 5 | 2 | 2.064 | 4.750 | 0 | 0 |

## Minimum evidence for closing a row

A row can become a validated same-station join only with one of the following:

- a shared station ID;
- an official/OpenAQ source crosswalk;
- source-owner or current-status documentation naming both records;
- public evidence of documented co-location.

Allowed decisions are `validated_same_station`,
`separate_nearby_stations`, `insufficient_public_evidence_keep_open`, and
`superseded_or_inactive`. The current worksheet assigns none of those closure
decisions. Every row remains `not_yet_validated`.

## Interpretation

The review queue is strongest in Uzbekistan and Bangladesh by row count, but
that does not make those rows validated. Bangladesh includes candidate matches
near Dhaka source rows and OpenAQ locations. Uzbekistan includes several
Tashkent source rows that point to a small number of nearby OpenAQ locations.
Those patterns are useful for review prioritization, but they also show why a
simple distance join can collapse multiple official rows onto the same OpenAQ
row.

The public article should therefore keep official and OpenAQ station layers
separate. The next source step is row-level station-crosswalk evidence, not a
station-radius population denominator.

## What this does not mean

- It does not validate any official-to-OpenAQ same-station join.
- It does not prove that a nearby OpenAQ row is regulatory, current, or
  co-located with the official station row.
- It does not prove official inventories or OpenAQ inventories are complete.
- It does not classify monitor grade.
- It does not make any candidate row ready for station-radius population
  coverage.

## Reproduce

```bash
python air-monitoring/scripts/reconcile-official-openaq-stations.py
python air-monitoring/scripts/build-official-openaq-candidate-review.py
```

The next upgrade is to review the 13 candidate rows against public station IDs,
source-owner documentation, current-status pages, or documented co-location
evidence. If no public evidence closes a row, it should stay open rather than
be treated as a station crosswalk.
