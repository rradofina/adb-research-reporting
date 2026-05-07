# Gate request — Screening Result → Publication-Ready

Per `CONSTITUTION.md` §7.3 and §9. The most stringent gate. AI may
prepare this artifact and request review; the owner applies the
maturity label. WIP cap (§8.1): max 1 PR program at any time.

Program: `{slug}`
Owner: {name}
Date submitted: YYYY-MM-DD

---

## Required artifacts checklist (§7.3)

| Artifact | Path | Commit hash | Status |
|---|---|---|---|
| Systematic literature review (Tier-A/B/C, owner-attested) | `{slug}/literature.md` | | *(complete / pending)* |
| Pre-registration frozen before pipeline run | `{slug}/pre-registration.md` | | *(verified / pending)* |
| Sensitivity at ±50 percent on every arbitrary numeric | `{slug}/sensitivity.md` | | *(complete / pending)* |
| Internal review complete | `{slug}/review-internal.md` | | *(closed / pending)* |
| External red-team review complete (≥ 2 reviewers) | `{slug}/review-external.md` | | *(closed / pending)* |
| Limitations section (verbatim reviewer objections) | `{slug}/limitations.md` | | *(complete / pending)* |
| coverage.md with reasons for non-coverage | `{slug}/coverage.md` | | *(complete / pending)* |
| Banned-words check passing | `scripts/check-banned-words.mjs` | | *(passing / failing)* |
| DMC-framing check passing | `scripts/check-dmc-framing.mjs` | | *(passing / failing)* |
| Citations check passing (no bare URLs) | `scripts/check-citations.mjs` | | *(passing / failing)* |
| Manifest hash check passing | `scripts/verify-manifest.mjs` | | *(passing / failing)* |
| Zenodo deposition (DOI minted) | `research/zenodo/{slug}.json` | | *(complete / pending)* |

## Reviewer record

| Reviewer | Affiliation | Competency | DMC focus | COI | Acceptance | Closed |
|---|---|---|---|---|---|---|
| {name} | {inst} | M / D / S | {region} | none / disclosed | YYYY-MM-DD | YYYY-MM-DD |

Per `red-team.md`, the program may not advance until the roster
minimum is met (2 measurement, 2 domain, 1 DMC-affiliated for the
program's pilot economies).

## WIP attestation

| Field | Value |
|---|---|
| Current PR count (before this promotion) | N |
| WIP cap (§8.1) | 1 |
| Program to retire / move down to free a slot, if at cap | {slug or "n/a"} |

## Owner promotion attestation

> "I, the program owner, have closed both internal and external review,
> committed every reviewer comment verbatim alongside my written response,
> moved every unresolved objection into `limitations.md`, deposited a
> replication archive on Zenodo, and attest that this program is ready
> to advance to Publication-Ready. The WIP cap is respected at the date
> below."

Signed: {name}
Date:   YYYY-MM-DD
Commit: {hash}
DOI:    {doi}
