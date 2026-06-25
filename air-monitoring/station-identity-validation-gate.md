# Station-identity validation gate

`attestation_chain: ai-first`

Generated: 2026-06-25T15:22:01Z

## What this adds

This derivative gate consolidates the official/OpenAQ station-identity evidence into one release decision. It reads the candidate review worksheet, the two public source scans, and the one-signal queue, then asks whether any row has enough public evidence to be treated as the same station.

It currently blocks the identity join. The evidence package has useful proximity, name, provider, and source-context signals, but it still has no shared station ID, source-owner crosswalk, current-status crosswalk, or documented co-location row.

## Mechanical rule

A same-station identity row is validated only when public evidence gives a shared station ID, source-owner crosswalk, current-status crosswalk, documented co-location, or an existing validated same-station flag. Proximity or name overlap alone is insufficient.

## Summary counts

| Measure | Count |
|---|---:|
| identity candidate rows checked | 44 |
| countries with identity candidates | 4 |
| near plus name candidate rows before source screen | 13 |
| source screened near plus name rows | 13 |
| source screened is monitor rows | 6 |
| source screened public feed rows | 7 |
| one signal identity rows | 31 |
| near only identity rows | 9 |
| name overlap not near identity rows | 22 |
| shared station id rows | 0 |
| source owner crosswalk rows | 0 |
| current status crosswalk rows | 0 |
| documented colocation rows | 0 |
| validated same station rows | 0 |
| station radius identity ready rows | 0 |

## Evidence gates

| Gate | Rows | Status |
|---|---:|---|
| Near-plus-name candidates source-screened | 13 | computed |
| Shared station ID evidence | 0 | blocked |
| Source-owner crosswalk evidence | 0 | blocked |
| Current-status crosswalk evidence | 0 | blocked |
| Documented co-location evidence | 0 | blocked |
| Validated same-station rows | 0 | blocked |
| Station-radius identity-ready rows | 0 | blocked |

## Country queue

| Economy | Candidate rows | Source-screened | One-signal | Validated | Radius-ready |
|---|---:|---:|---:|---:|---:|
| Uzbekistan (`UZB`) | 18 | 5 | 13 | 0 | 0 |
| Malaysia (`MYS`) | 16 | 3 | 13 | 0 | 0 |
| Bangladesh (`BGD`) | 7 | 4 | 3 | 0 | 0 |
| Indonesia (`IDN`) | 3 | 1 | 2 | 0 | 0 |

## Non-claim

This gate validates only station identity evidence. It does not certify monitor grade, does not estimate station-radius coverage, does not create people-served or exposure estimates, and does not turn nearby public-feed rows into official stations.
