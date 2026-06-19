# Official station-source extraction pass

`attestation_chain: ai-first`

This pass turns the regulator-source inventory into station-level evidence.
It extracts public official station tables or portal rows where available,
keeps name-only, count-only, and plan-only sources separate, and compares
official coordinate rows with OpenAQ station coordinates as a screening
diagnostic. It does not validate monitor grade or compute station-radius
population coverage.

## Why this measurement problem matters

The air-monitoring article now has two different maps of visibility. OpenAQ
shows where public PM2.5 feeds are visible through an open data aggregator.
Regulators and official portals may show a different station network. A
monitoring-gap claim cannot treat those as the same object.

The policy problem is therefore not only whether an economy has OpenAQ rows.
It is whether a reader can see the official station network, its pollutant
coverage, and enough station metadata to compare it with the open aggregator
view.

## Source added

The script `scripts/extract-regulator-station-evidence.py` reads:

- `generated/air-monitoring-regulator-source-inventory.csv`
- `generated/air-monitoring-openaq-station-metadata.csv`

It then retrieves public official sources for the nine official inventory,
portal, or plan candidates and writes:

- `generated/air-monitoring-regulator-station-extraction.csv`
- `generated/air-monitoring-regulator-station-extraction-summary.json`

The script intentionally excludes public API contact fields and keeps only the
station evidence needed for the research claim: station identifiers, station
names or areas, coordinates where public, pollutant signals, source URLs, and
OpenAQ comparison diagnostics.

## What the extraction found

Generated at `2026-06-19T07:14:55Z`, the pass retrieved all nine targeted
official sources.

| Gate | Count |
|---|---:|
| Official sources targeted | 9 |
| Countries with official station-coordinate rows | 5 |
| Official station-coordinate rows | 230 |
| Official station name-only rows | 6 |
| Official count-only rows | 1 |
| Official plan-count-only rows | 2 |
| Official rows with PM2.5 signal | 183 |
| Official coordinate rows within 5 km of an OpenAQ row | 22 |
| Official coordinate rows not within 5 km of an OpenAQ row | 208 |
| Monitor-grade rows | 0 |

The extraction makes a sharper reader-facing point: official sources can
expose many station coordinates that are not visible as nearby OpenAQ PM2.5
locations. The nearest-distance result is only a screening diagnostic, not a
validated same-station match.

## Country-level evidence

| ISO | Evidence level | Official rows | Coordinate rows | PM2.5-signal rows | OpenAQ rows | Within 5 km of OpenAQ |
|---|---|---:|---:|---:|---:|---:|
| BGD | station coordinates | 31 | 31 | 31 | 22 | 5 |
| UZB | station coordinates | 93 | 93 | 40 | 4 | 10 |
| GEO | station coordinates | 16 | 16 | 16 | 2 | 0 |
| IDN | station coordinates | 22 | 22 | 22 | 36 | 2 |
| MYS | station coordinates | 68 | 68 | 67 | 18 | 5 |
| LKA | station names only | 5 | 0 | 5 | 3 | 0 |
| TJK | station names only | 1 | 0 | 1 | 7 | 0 |
| BRN | count only | 1 | 0 | 1 | 0 | 0 |
| MMR | plan count only | 2 | 0 | 0 | 3 | 0 |

Bangladesh is the cleanest table extraction: the Department of Environment
PDF lists 31 monitoring sites, 16 CAMS and 15 C-CAMS, with coordinates and
PM2.5 among the monitored pollutants. Malaysia, Uzbekistan, Georgia, and
Indonesia expose station coordinates through public portal or API structures.
Sri Lanka and Tajikistan provide named official monitoring evidence without
coordinates in this pass. Brunei provides a public official count statement.
Myanmar remains a project-plan source, not active-station validation.

## Interpretation

This is the first pass that makes official station evidence visible beside
OpenAQ station evidence. It shifts the research question away from a generic
country monitor count and toward source reconciliation:

- Where official coordinate rows exist, OpenAQ is not the whole regulator map.
- Where official sources provide only names or counts, the source helps the
audit but still cannot support station-radius or catchment claims.
- Where the source is a project plan, it cannot be treated as active monitor
coverage.
- No targeted source in this pass provides a complete monitor-grade
classification, so reference-grade or regulatory-grade language remains
blocked.

## What this does not mean

- It is not a validated official-to-OpenAQ station join.
- A row within 5 km of OpenAQ is only a proximity candidate.
- A row not within 5 km of OpenAQ is not proof that OpenAQ is wrong.
- It is not monitor-grade or reference-grade validation.
- It is not proof that zero-OpenAQ economies have no monitor.
- It is not station-radius population coverage.

## Reproduce

```bash
python air-monitoring/scripts/fetch-openaq-station-metadata.py
python air-monitoring/scripts/build-regulator-source-inventory.py
python air-monitoring/scripts/extract-regulator-station-evidence.py
```

The next statistical upgrade is to validate station-grade metadata where
public sources distinguish regulatory/reference monitors from low-cost or
other feeds, then add a declared catchment method and gridded denominators.
