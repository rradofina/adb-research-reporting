# Gate request — SR → PR — Public Service Data Quality

Per `CONSTITUTION.md` §7.3 and §9. AI prepared this artifact and
requests review. The owner applies the maturity label.

Program: `public-service-data-quality`
Owner: Raymond Adofina
Date submitted: *(pending owner — AI cannot submit)*

---

## Required artifacts checklist (§7.3)

| Artifact | Path | Status |
|---|---|---|
| Systematic literature review (Tier-A/B/C, owner-attested) | `public-service-data-quality/literature.md` | **complete (AI-drafted, 10 verified entries)** — owner line-by-line attestation pending |
| Pre-registration frozen before pipeline run | `public-service-data-quality/pre-registration.md` | **drafted** — owner freeze pending in §10 commit-message attestation |
| Sensitivity at ±50% on every arbitrary numeric | `public-service-data-quality/sensitivity.md`, `sensitivity-runs.json` | **PHL complete, no critical failures.** BGD sensitivity TODO |
| Internal review complete | `public-service-data-quality/review-internal.md` | **template open** — supervisor review not yet started |
| External red-team review complete (≥ 2 reviewers) | `public-service-data-quality/review-external.md` | **template open, roster empty** — owner recruits |
| Limitations section (verbatim reviewer objections) | `public-service-data-quality/limitations.md` | **drafted** — reviewer objections to be appended after `review-external.md` closes |
| coverage.md with reasons for non-coverage | `public-service-data-quality/coverage.md` | **complete** — 2 / 4 DMCs covered; IND + IDN explicitly out of scope |
| Banned-words check passing | `scripts/check-banned-words.mjs` | **passing** at 2026-04-25 |
| DMC-framing check passing | `scripts/check-dmc-framing.mjs` | **passing** at 2026-04-25 |
| Citations check passing (no bare URLs) | `scripts/check-citations.mjs` | **passing** at 2026-04-25 |
| Composite-headline guard | `scripts/check-composite-headline.mjs` | **passing** at 2026-04-25 |
| Manifest hash check | `scripts/verify-manifest.mjs` | **2 mismatches + 1 missing** — manifest needs re-pinning before gate; PHL pipeline output drift |
| Zenodo deposition (DOI minted) | `research/zenodo/public-service-data-quality.json` | **metadata template prepared; DOI not yet reserved** — owner reserves |

## Reviewer record

| Reviewer | Affiliation | Competency | DMC focus | COI | Acceptance | Closed |
|---|---|---|---|---|---|---|
| *(pending)* | *(institution)* | M / D / S | *(region)* | *(none / disclosed)* | *(YYYY-MM-DD)* | *(YYYY-MM-DD)* |
| *(pending)* | *(institution)* | M / D / S | *(region)* | *(none / disclosed)* | *(YYYY-MM-DD)* | *(YYYY-MM-DD)* |

`red-team.md` §minimum-roster-size requires 2 measurement, 2 domain,
1 DMC-affiliated reviewer per program. The roster is currently empty;
the program may not advance until `red-team.md` is populated and the
reviewers above are recruited and have accepted with COI disclosures.

## WIP attestation

| Field | Value |
|---|---|
| Current PR count (before this promotion) | 0 |
| WIP cap (§8.1) | 1 |
| Programs to retire / move down | n/a (cap not yet reached) |

## What is blocked on the owner

The gate cannot close until the owner:

1. Reads every cited entry in `literature.md` line-by-line and attests
   in the commit message.
2. Freezes `pre-registration.md` §10 with a commit-message attestation
   (a hash before any pipeline rerun).
3. Re-runs the manifest pin (`manifest.sha256`) to clear the 2
   mismatches + 1 missing on PHL outputs (currently real drift after
   the most recent pipeline run).
4. Runs the BGD sensitivity suite at ±50% (mirror of `scripts/sensitivity.py`
   for Bangladesh; appends to `sensitivity.md` §1).
5. Recruits 2+ external reviewers from `red-team.md`'s targeted
   institutions (PIDS, BIDS, OPHI, HeiGIT, Macharia / Snow network),
   sends each the evidence packet built from the artifacts above,
   collects their written comments.
6. Files supervisor's internal review (`review-internal.md`) and
   responds in writing.
7. Reserves a Zenodo DOI from `research/zenodo/public-service-data-quality.json`
   metadata; commits the DOI back to `pre-registration.md` and the
   article frontmatter.
8. Updates `CONSTITUTION.md` §15 Program Register and
   `research/wip-register.md` to mark Program 13 as Publication-Ready
   in the same commit.

## Owner promotion attestation

> "I, the program owner, have closed both internal and external review,
> committed every reviewer comment verbatim alongside my written
> response, moved every unresolved objection into `limitations.md`,
> deposited a replication archive on Zenodo, and attest that this
> program is ready to advance to Publication-Ready. The WIP cap is
> respected at the date below."

Signed: *(pending)*
Date:   *(pending)*
Commit: *(pending)*
DOI:    *(pending)*
