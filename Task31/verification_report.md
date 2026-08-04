# Task 31 citation verification report

`attestation_chain: ai-first`

Verification run (UTC): 2026-08-04T17:26:43+00:00
Verifier: `verify_citations.py` against Crossref REST API.

This gate checks **citation identity** — that each DOI resolves to a real
work whose journal, year, and first author match the evidence register. It
does **not** confirm that the quoted estimate appears in the source; rows
marked `NEEDS_LOCATOR` still require a page/table locator.

## Evidence register (52 records)

| Status | Count | Meaning |
|---|---|---|
| VERIFIED | 25 | DOI resolves; journal, year, first author all match |
| MISMATCH | 0 | DOI resolves but recorded metadata disagrees |
| UNRESOLVED | 0 | DOI does not resolve — treat as unsupported |
| NEEDS_LOCATOR | 30 | No DOI; URL serves; locator still required |
| URL_FAIL | 0 | No DOI and URL did not serve |

## Reference list (55 entries)

| Status | Count |
|---|---|
| RESOLVED | 25 |
| UNRESOLVED | 0 |
| NO_DOI | 32 |

## Records requiring action

None.

## Interpretation

A `VERIFIED` row means the publication exists and is correctly identified.
It does not mean the estimate was independently reproduced. Under the
review provenance rule, a headline number is citable only once its row is
`VERIFIED` **and** carries a page or table locator.
