# Results — {program-title}

Status: **{screening-result | publication-ready}**. The maturity label is
applied by the human owner per `CONSTITUTION.md` §7. AI must not advance
the label.

Frozen pre-registration: `pre-registration.md` (commit hash {hash}).

---

## 1. Headline finding

A single sentence. No hedges, no narrative. The claim from
`pre-registration.md` §1 with the empirical answer attached.

> *{finding}*

## 2. Headline-supporting tables and figures

Tables and figures referenced from `generated/`. Every cell traces to
either a row in `obs.*` or a script output in `generated/`.

| Number | Caption | Source |
|---|---|---|
| Table 1 | … | `generated/{slug}-table-1.csv` |
| Figure 1 | … | `generated/{slug}-figure-1.svg` |

## 3. Sensitivity

Headline replication ranges from `sensitivity.md` §2. Critical failures
resolved per §6.6.

| Metric | Baseline | Min across sensitivity suite | Max across sensitivity suite |
|---|---|---|---|

## 4. Limitations

Bullet list of what this result cannot establish. Reviewer objections
that the owner could not resolve are quoted verbatim with the reviewer's
permission, per §9.3.

- *{limitation}*

## 5. Comparison to literature

How this result fits the cited literature. BibTeX keys only — no bare URLs.

> Cites: `key1`, `key2`, `key3`.

## 6. Reproduction

A clean clone of this repository at the frozen commit hash reproduces
the headline finding by running:

```bash
{command}
```

Hash check (per `manifest.sha256`):

```bash
{verification command}
```

## 7. Banned-words check

Run on every commit by `scripts/check-banned-words.mjs`. Latest pass:
{date}.

## 8. DMC framing check

Run on every commit by `scripts/check-dmc-framing.mjs`. Latest pass:
{date}.

## 9. Owner attestation

| Field | Value |
|---|---|
| Pre-registration frozen before pipeline run | *(yes / no)* |
| Pipeline reproduces from clean clone | *(yes / no)* |
| Sensitivity suite complete | *(yes / no)* |
| Banned-words check passing | *(yes / no)* |
| DMC-framing check passing | *(yes / no)* |
| Internal review complete | *(yes / no)* |
| External red-team complete | *(yes / no)* |
| Date attested | YYYY-MM-DD |
