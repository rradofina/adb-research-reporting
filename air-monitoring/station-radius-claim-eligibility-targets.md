# Station-radius claim-eligibility targets

`attestation_chain: ai-first`

Generated: 2026-07-01T12:59:08Z

## What this adds

This no-network matrix answers the next loop question: what exact public document would convert a blocked row into a claim-eligible row?

The answer is not another map. The package already has denominator geometry. It needs public row-level documents that close identity, grade, verification, or endpoint-status gates.

## Required document primitives

- official/OpenAQ station identity bridge
- target-station inspection log
- target-station PM2.5 calibration certificate or calibration-status record
- explicit station-grade record
- verified report/export or station-code status table
- official endpoint correction/status record

## Target matrix

| Target | Blocked rows | Missing public document | Would unlock |
|---|---:|---|---|
| same-station identity | 44 | A shared station ID, source-owner crosswalk, current-status crosswalk, or documented co-location record linking the official row to the OpenAQ row. | Station-radius identity-ready rows; it would not by itself unlock monitor-grade or coverage claims. |
| complete station-grade evidence | 22 | A target-station inspection log, PM2.5 calibration certificate/status record, or explicit station-grade record. | A complete monitor-grade candidate row after the strict BMKG closure rule; identity gates would still need to pass before radius claims. |
| verified report or station-code closure | 16 | A verified report/export surface without the not-verified caution, or a station-code method/status document that closes verification for the exact target station codes. | Georgia report-verification closure candidates; it would not by itself solve OpenAQ identity or grade completeness. |
| endpoint consistency and station-status closure | 3 | A public official correction, status, or grade record resolving the stale-detail, sentinel PM2.5, or API/detail/regional-table mismatch for the exact station ID. | Uzbekistan blocker-row resolution candidates; it would not by itself create complete monitor-grade or radius readiness. |
| coverage-claim permission | 11 | The upstream identity and complete-grade documents above; denominator geometry alone cannot become a station-radius coverage claim. | Permission to discuss station-radius coverage for a row/economy only if all upstream gates also pass. |

## Why this matters

The current package is already strong enough to show the measurement blind spot: public station visibility, official station lists, source-specific method context, and denominator geometry do not automatically support station-radius coverage language. This target matrix turns the remaining gap into auditable document primitives rather than a vague request for better data.

## Non-claim

This target matrix identifies public-document prerequisites for future station-radius claim eligibility. It does not validate same-station joins, does not certify monitor grade, does not estimate people served, and does not allow station-radius coverage language.
