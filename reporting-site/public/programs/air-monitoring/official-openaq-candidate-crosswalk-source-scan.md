# Official/OpenAQ candidate crosswalk source scan

`attestation_chain: ai-first`

This scan reviews the 6 OpenAQ `isMonitor` candidate rows from the
official/OpenAQ candidate public-evidence audit. It asks whether public source
pages support a same-station join, documented co-location, or a separate
nearby-stations decision. The result is not a catchment layer: validated
same-station joins remain zero.

## Why this measurement problem matters

The candidate worksheet had 13 near-plus-name rows. The public-evidence audit
then showed that 6 of those rows were marked `isMonitor` in OpenAQ. Those are
the rows most likely to tempt a premature join. This scan checks them first
against public official and source-owner pages.

## Source added

The script `scripts/scan-official-openaq-candidate-crosswalk-sources.py` reads:

- `source-inputs/candidate-crosswalk-public-source-seed.csv`
- `generated/air-monitoring-official-openaq-candidate-public-evidence.csv`
- `generated/air-monitoring-openaq-station-metadata.csv`

It writes:

- `generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv`
- `generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json`

The seed file names five public source URLs: the Bangladesh Department of
Environment ambient air quality PDF, the SPARTAN Dhaka station page, the
OpenAQ SPARTAN aggregation announcement, the Uzhydromet public monitoring map,
and the World Bank text version of the Tashkent air-quality assessment.

## What the scan found

| Scan result | Rows |
|---|---:|
| Candidate rows before this scan | 13 |
| OpenAQ `isMonitor` candidate rows scanned | 6 |
| Candidate rows not scanned here because OpenAQ was not `isMonitor` | 7 |
| Public source URLs retrieved | 5 |
| Rows with official coordinate evidence | 2 |
| Rows with official address evidence | 6 |
| Rows with OpenAQ coordinate evidence | 6 |
| Rows screened as separate nearby stations | 6 |
| Shared station-ID rows found | 0 |
| Source crosswalk rows found | 0 |
| Documented co-location rows found | 0 |
| Validated same-station joins | 0 |
| Station-radius join-ready rows | 0 |

## Row decisions

| ISO | Candidate rows scanned | Separate nearby-station decisions | Validated joins | Radius-ready rows |
|---|---:|---:|---:|---:|
| BGD | 2 | 2 | 0 | 0 |
| UZB | 4 | 4 | 0 | 0 |

For Bangladesh, the official Department of Environment PDF gives coordinates
for BUET, Dhaka and Nagar Bhaban, DSCC, Dhaka. The SPARTAN public station page
identifies the OpenAQ-side station as BDDU, University of Dhaka, with its own
coordinates. The distances are 0.532 km and 1.156 km, matching the candidate
diagnostic but not proving co-location.

For Uzbekistan, the Uzhydromet public map lists the official POP rows and
addresses. The OpenAQ-side row is StateAir / US Diplomatic Post: Tashkent.
The World Bank Tashkent assessment distinguishes the US Embassy station from
Uzhydromet stations and states that manual Uzhydromet stations do not monitor
PM 2.5. The scan therefore keeps the Uzhydromet POP rows out of the US Embassy
join.

## Interpretation

This is a useful negative result. The most tempting six candidate rows now have
public-source separation evidence. The public surface should show that the
review queue got smaller in one direction: the `isMonitor` candidates are not
validated joins; they are screened as separate nearby stations unless a later
source-owner crosswalk reverses that decision.

The remaining row-level work is the seven not-`isMonitor` public-feed
candidate rows and the broader one-signal candidate queue. Those rows should
not be used in station-radius analysis either.

## What this does not mean

- It does not validate any official/OpenAQ same-station join.
- It does not certify complete monitor-grade status for official stations.
- It does not prove that the public inventories are complete.
- It does not make any row station-radius-ready.
- It does not build a catchment denominator.

## Reproduce

```bash
python air-monitoring/scripts/audit-official-openaq-candidate-public-evidence.py
python air-monitoring/scripts/scan-official-openaq-candidate-crosswalk-sources.py
```

The next upgrade is to scan the seven not-`isMonitor` public-feed candidates
for source-owner documentation, current-status pages, or documented
co-location evidence. If no such evidence exists, they should stay outside the
station-radius denominator.
