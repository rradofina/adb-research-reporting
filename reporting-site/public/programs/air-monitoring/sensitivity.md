# Sensitivity -- Air-monitoring public QA observability

`attestation_chain: ai-first`. Updated 2026-07-07.

This note replaces the old monitor-density sensitivity as the active headline
check. The current claim is not a composite monitor-density score; it is a
documented public-evidence absence generated from
`air-monitoring/scripts/build-evidence-ledger.py`.

## Active claim

Public evidence in the audited packet does not close the station-level QA gates
needed for a station-radius air-monitoring coverage claim.

The generated ledger records 64 summary rows and 214 supporting files. The
claim-enabling counters remain zero for validated same-station rows, BMKG
station-specific inspection logs, BMKG station-specific calibration
certificates, BMKG calibration-status rows, complete monitor-grade rows,
station-radius-ready economies, and allowed coverage-claim rows.

## Sensitivity logic

The result is not sensitive to the 0.5 km, 4 km, or 50 km station-radius bands,
because the current claim stops before any radius coverage estimate is allowed.
Changing the radius changes future denominator geometry; it does not create a
station-level calibration certificate, inspection log, same-station crosswalk,
or complete monitor-grade row.

The result is not sensitive to the GHSL/ACAG denominator route either. The
coverage gate records 831 denominator join rows, but denominator rows are
explicitly non-claim evidence until station identity and monitor-grade gates
close.

The result is sensitive to source-discovery false negatives. A newly public
station-level certificate, inspection log, calibration-status row, official
same-station crosswalk, or public method-grade ledger would update the ledger
and could overturn the absence finding for the affected economy or station.

## Source-expansion test

A further pass is justified only if it names a previously unchecked source and
why it plausibly differs from the searched routes. Generic re-searching is not
a sensitivity check. A valid expansion source would be one of:

- an official station-level calibration-certificate or inspection-log registry;
- an official station-code crosswalk linking regulator rows and OpenAQ rows;
- a public audit or QA ledger with station identifiers and current calibration
  status;
- a regulator API endpoint not represented in the current summary set.

## Retired background result

The April 2026 gap-score result remains a background screening artifact only.
It combined people per monitor with PM2.5-above-guideline context. It is no
longer the active air-monitoring claim because the later public-source audit
showed that station identity and monitor-grade evidence gates do not close.
