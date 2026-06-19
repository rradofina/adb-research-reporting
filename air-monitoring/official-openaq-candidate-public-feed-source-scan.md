# Official/OpenAQ candidate public-feed source scan

`attestation_chain: ai-first`

This scan reviews the 7 official/OpenAQ candidate rows where OpenAQ metadata is
present but `isMonitor` is false. It asks whether public official sources,
OpenAQ metadata, or source-owner context support a same-station join,
documented co-location, or current-status crosswalk. The result is not a
catchment layer: validated same-station joins remain zero.

## Why this measurement problem matters

The previous source scan handled the 6 OpenAQ `isMonitor` candidate rows. The
remaining 7 rows are a different risk: they are nearby public feeds from
AirGradient, Clarity, Kopernik, Smart Air Bangladesh, or individual owners.
They can make a station map look fuller, but they cannot be collapsed into an
official station record without public evidence naming both records.

## Source added

The script `scripts/scan-official-openaq-candidate-public-feed-sources.py`
reads:

- `source-inputs/candidate-public-feed-source-seed.csv`
- `generated/air-monitoring-official-openaq-candidate-public-evidence.csv`
- `generated/air-monitoring-regulator-station-extraction.csv`
- `generated/air-monitoring-openaq-station-metadata.csv`

It writes:

- `generated/air-monitoring-official-openaq-candidate-public-feed-source-scan.csv`
- `generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json`

The seed file names 10 public source URLs: four official source families for
Bangladesh, Indonesia, Malaysia, and Uzbekistan; one official Malaysia feature
API; and five provider-context pages for AirGradient, OpenAQ/AirGradient,
Clarity, Smart Air Bangladesh, and Kopernik.

## What the scan found

| Scan result | Rows |
|---|---:|
| Candidate rows before this scan | 13 |
| Public-feed candidate rows scanned | 7 |
| `isMonitor` candidate rows not scanned here | 6 |
| Public source URLs retrieved | 10 |
| Rows with official coordinate evidence | 7 |
| Rows with OpenAQ coordinate evidence | 7 |
| Rows with public-feed owner/provider metadata | 7 |
| OpenAQ rows not marked `isMonitor` | 7 |
| Rows with provider-context pages retrieved | 7 |
| Same OpenAQ location reused within this scan | 2 |
| Official agency owner/provider matches | 0 |
| Shared station-ID rows found | 0 |
| Source-owner crosswalk rows found | 0 |
| Current-status crosswalk rows found | 0 |
| Documented co-location rows found | 0 |
| Validated same-station joins | 0 |
| Station-radius join-ready rows | 0 |
| Rows screened as public-feed nearby and not join-ready | 7 |

## Row decisions

| ISO | Candidate rows scanned | Public-feed nearby, not join-ready | Validated joins | Radius-ready rows |
|---|---:|---:|---:|---:|
| BGD | 2 | 2 | 0 | 0 |
| IDN | 1 | 1 | 0 | 0 |
| MYS | 3 | 3 | 0 | 0 |
| UZB | 1 | 1 | 0 | 0 |

The two Bangladesh rows are official CAMS stations near the same Smart Air
Bangladesh / AirGradient OpenAQ public-feed location. Because one OpenAQ row is
nearest to two different official station IDs, a one-to-one station join would
require source-owner evidence naming the official records; none was found.

The Indonesia row places the BMKG Talang Betutu Palembang source row 2.372
kilometers from an OpenAQ location named SD Muhammadiyah 18 Palembang. The row
has Kopernik / AirGradient metadata in OpenAQ, not BMKG owner/provider
metadata, and no public crosswalk was found.

The three Malaysia rows are official MyEQMS/APIMS stations near AirGradient or
Clarity public-feed locations. The public evidence keeps Indera Mahkota
Kuantan, Petaling Jaya, and Cheras separate from Indera Mahkota 8, Taman Tun
Dr. Ismail, and Bukit Bintang unless a later source-owner page names both
records.

The Uzbekistan row keeps Uzhydromet POP #23 separate from the AirGradient
Sputnik-4 OpenAQ row. The public source context does not document co-location
or a station crosswalk.

## Interpretation

This closes the second half of the 13-row near-plus-name queue for now. The
candidate queue is still useful, but no row is a station-radius input. The
`isMonitor` rows and the not-`isMonitor` public-feed rows both remain outside
validated official/OpenAQ station joins.

The next row-level validation work is no longer these 13 near-plus-name rows.
It is the broader one-signal queue: near-only, name-only-not-near, and
monitor-grade one-signal official rows that still need public documentation.

## What this does not mean

- It does not validate any official/OpenAQ same-station join.
- It does not classify public-feed sensors as regulatory monitors.
- It does not certify complete monitor-grade status for official stations.
- It does not prove that the public inventories are complete.
- It does not make any row station-radius-ready.
- It does not build a catchment denominator.

## Reproduce

```bash
python air-monitoring/scripts/audit-official-openaq-candidate-public-evidence.py
python air-monitoring/scripts/scan-official-openaq-candidate-crosswalk-sources.py
python air-monitoring/scripts/scan-official-openaq-candidate-public-feed-sources.py
```

The next upgrade is to review the broader one-signal candidate queue and deepen
non-Bangladesh monitor-grade documentation before any station-radius or
catchment analysis is attempted.
