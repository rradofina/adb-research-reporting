# WIP register

Governed by `CONSTITUTION.md` §8.1 — work-in-progress cap. Updated on
every gate promotion or demotion.

| Cap | Limit | Current count |
|---|---|---|
| Publication-Ready (PR) | 1 | 0 |
| Screening Result (SR) | 3 | 0 |

A program with all SR-tier artifacts drafted but awaiting owner attestation is **not yet at SR**. Maturity advances on the owner's commit-message attestation, not on AI-drafted file presence.

A promotion request that would push either count over its cap is
rejected at the gate.

Last updated: 2026-04-25.

---

## Programs by maturity

### Publication-Ready

*(none)*

### Screening Result

*(none)*

### Prepared Pipeline (with SR artifacts drafted, awaiting owner attestation)

- **public-service-data-quality** — PHL + BGD pilots computed
  (17.1% / 11.8% clinical-tier OSM/registry ratio); literature.md (10
  Tier-A/B/C entries), scoring.md (24/30), pre-registration.md,
  sensitivity.md (PHL +/-50% pass, BGD TODO), coverage.md, results.md,
  review-internal.md (open), review-external.md (open, roster empty),
  limitations.md, articles/measurement-gap-philippines-bangladesh.md
  drafted. **Blocked on:** owner literature-review attestation, owner
  pre-registration freeze, BGD sensitivity rerun, manifest pin refresh,
  red-team roster, Zenodo DOI reservation. See `public-service-data-quality/SR-to-PR.md`.

### Prepared Pipeline (other)

*(see `CONSTITUTION.md` §15 program register; cross-check on every
promotion)*

### Hypothesis

*(see `CONSTITUTION.md` §15 program register; cross-check on every
promotion)*

### Retired

*(none)*

---

## Promotion log

| Date | Program | Transition | Commit | Notes |
|---|---|---|---|---|

---

## How this file is kept honest

`scripts/check-wip.mjs` reads this file and `CONSTITUTION.md` §15 and
exits non-zero if the counts diverge or if the cap is exceeded. CI runs
this on every PR.
