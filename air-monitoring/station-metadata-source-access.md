# OpenAQ station-metadata source-access pass

`attestation_chain: ai-first`

This pass moves the air-monitoring program from a station-metadata wall to a
source-access record for the 24 economies in the committed upgrade queue. It
does not make the article station-radius ready. It records which OpenAQ PM2.5
station rows can now be inspected for coordinates, owner or provider, and
first-seen metadata, and it leaves monitor-grade and regulator-inventory
claims blocked.

## Why this measurement problem matters

The country-level panel can show that some economies have few public PM2.5
monitor locations relative to population and exposure. It cannot show where
people are outside a station catchment, whether a station is regulatory grade,
or whether an OpenAQ-visible zero means no monitor exists on the ground. The
next decision-grade step is therefore source access: can the station rows be
retrieved, versioned, and inspected before the visualization says anything
about spatial coverage?

## Source added

The script `scripts/fetch-openaq-station-metadata.py` reads
`generated/air-monitoring-metadata-readiness-audit.csv`, selects the 24
non-panel-context upgrade-queue economies, and queries the OpenAQ v3
`locations` endpoint with `parameters_id=2` for PM2.5. OpenAQ documentation
states that locations include station name, coordinates, provider or
responsible organization fields, sensor information, active/mobile flags, and
license/attribution fields. The API requires an OpenAQ API key; the script
uses a locally configured key without printing or committing it.

Public source notes:

- OpenAQ locations resource: https://docs.openaq.org/resources/locations
- OpenAQ examples: https://docs.openaq.org/examples/examples
- OpenAQ quick start and API-key guidance:
  https://docs.openaq.org/using-the-api/quick-start

Raw response caches are written under `.cache/openaq-station-metadata/` and
are ignored by git under the repository cache policy. The durable committed
record is the script plus:

- `generated/air-monitoring-openaq-station-metadata.csv`
- `generated/air-monitoring-openaq-station-metadata-summary.json`

## What the fetch found

Generated at `2026-06-19T06:27:19Z`, the pass queried all 24 target economies
without API errors.

| Gate | Count |
|---|---:|
| Upgrade-queue economies targeted | 24 |
| Economies computed | 24 |
| Economies with OpenAQ PM2.5 station rows | 11 |
| Economies with zero OpenAQ PM2.5 station rows | 13 |
| OpenAQ PM2.5 station rows fetched | 101 |
| Station-coordinate rows | 101 |
| Owner/provider rows | 101 |
| First-seen rows | 93 |
| Coordinate-QC exclusions | 2 |
| Monitor-grade rows | 0 |
| Regulator-inventory rows | 0 |
| Station-radius analysis ready | 0 |

The 11 economies with OpenAQ PM2.5 station rows are Afghanistan, Azerbaijan,
Bangladesh, Georgia, Indonesia, Malaysia, Myanmar, Sri Lanka, Tajikistan,
Turkmenistan, and Uzbekistan. The 13 economies that remain at zero OpenAQ
PM2.5 station rows are Brunei Darussalam, Fiji, Kiribati, Marshall Islands,
Micronesia (Federated States of), Nauru, Palau, Papua New Guinea,
Timor-Leste, Tonga, Tuvalu, Vanuatu, and Samoa.

| ISO | Economy | Panel PM2.5 locations | OpenAQ PM2.5 rows fetched | Coordinate rows | First-seen rows |
|---|---|---:|---:|---:|---:|
| AFG | Afghanistan | 2 | 2 | 2 | 2 |
| BGD | Bangladesh | 20 | 22 | 22 | 20 |
| MMR | Myanmar | 3 | 3 | 3 | 3 |
| UZB | Uzbekistan | 5 | 4 | 4 | 4 |
| TJK | Tajikistan | 5 | 7 | 7 | 7 |
| AZE | Azerbaijan | 1 | 2 | 2 | 2 |
| GEO | Georgia | 2 | 2 | 2 | 2 |
| IDN | Indonesia | 35 | 36 | 36 | 30 |
| LKA | Sri Lanka | 3 | 3 | 3 | 3 |
| MYS | Malaysia | 18 | 18 | 18 | 18 |
| TKM | Turkmenistan | 2 | 2 | 2 | 2 |

## Interpretation

The fetch removes one specific wall: the upgrade queue now has a committed
station-metadata extract for every OpenAQ PM2.5 location returned by the v3
API. That means the next visual can show where the 101 OpenAQ-visible PM2.5
station rows are, and it can show which of the 24 target economies still have
zero OpenAQ PM2.5 rows.

The fetch also surfaces a source-quality issue. Two OpenAQ rows were returned
under the requested country code but had coordinates outside broad
target-country bounds: one row labeled Uzbekistan and one row labeled
Indonesia. The committed station table excludes those rows from the coordinate
map and country counts and records them in the summary JSON under
`excluded_locations`.

It does not remove the policy caution. Owner and provider fields are
provenance fields, not monitor-grade validation. A zero result in OpenAQ is
still OpenAQ-visible zero, not proof that a regulator, embassy, university, or
private provider has no monitor outside OpenAQ. Station-radius analysis remains
uncomputed because it needs a separate catchment method and gridded population
or exposure denominators.

## What this does not mean

- It is not a station-radius or population-catchment estimate.
- It is not a monitor-grade validation.
- It is not a regulatory inventory.
- It is not proof that no monitor exists outside OpenAQ.
- It is not a pollution ranking or health-impact estimate.

## Reproduce

```bash
python air-monitoring/scripts/build-metadata-readiness-audit.py
python air-monitoring/scripts/fetch-openaq-station-metadata.py
```

If `OPENAQ_API_KEY` or `NEXT_PUBLIC_OPENAQ_API_KEY` is not configured, the
script writes an `api_key_required` artifact instead of station rows.
