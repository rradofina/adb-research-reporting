# Gate request — Prepared Pipeline → Screening Result

Per `CONSTITUTION.md` §7.2. AI may prepare this artifact and request
review. The owner applies the maturity label. WIP cap (§8.1) must not
be exceeded after this promotion: max 3 SR programs at any time.

Program: `{slug}`
Owner: {name}
Date submitted: YYYY-MM-DD

---

## Required artifacts checklist (§7.2)

| Artifact | Path | Commit hash | Status |
|---|---|---|---|
| Pipeline runs from clean clone | `{slug}/scripts/` | | *(verified / pending)* |
| Evidence packet (generated/) | `{slug}/generated/` | | *(complete / pending)* |
| Cache committed | `{slug}/.cache/` | | *(verified / pending)* |
| manifest.sha256 entry for every cache file | `manifest.sha256` | | *(verified / pending)* |
| versions.json entry per upstream source | `versions.json` | | *(verified / pending)* |
| coverage.md auto-generated | `{slug}/coverage.md` | | *(complete / pending)* |
| Per-row retrieval timestamps | `generated/*` | | *(verified / pending)* |

## Reproduction proof

```bash
# Run from a fresh clone with no API keys; all values reproduce exactly.
git clean -fdx
{install}
{run}
{verify}
```

Output of the verify step must be **PASS** for every row.

## WIP attestation

| Field | Value |
|---|---|
| Current SR count (before this promotion) | N |
| WIP cap (§8.1) | 3 |
| Programs to retire / move down to free a slot, if at cap | {list or "n/a"} |

## Owner promotion attestation

> "I, the program owner, have run the pipeline from a clean clone, verified
> every cache hash, and attest that this program is ready to advance to
> Screening Result. The WIP cap is respected at the date below."

Signed: {name}
Date:   YYYY-MM-DD
Commit: {hash}
