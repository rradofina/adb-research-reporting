# Pre-registration — {program-title}

Governed by `CONSTITUTION.md` §3.2 and §7. This document is **frozen
before the pipeline runs**. Any change after the pipeline run is treated
as a new pre-registration and the prior result is retracted, not edited.

---

## 1. Claim sentence

The exact sentence this program intends to test. Maximum one sentence.

> *{claim}*

## 2. Falsification condition

The empirical signature that would disprove the claim. Specific enough
that, given the data, the result is unambiguous.

> *{condition}*

## 3. Population in scope

DMCs covered by this pre-registration. List by ISO3.

- {ISO3, ISO3, …}

## 4. Time window

Earliest and latest source observation dates that contribute to the claim.

- Start: YYYY-MM-DD
- End:   YYYY-MM-DD

## 5. Primary metric

The single number, rate, or distribution the claim turns on. Define
precisely; specify units and rounding.

> *{metric}*

## 6. Pre-specified arbitrary numerics

Every numeric choice that would normally be a researcher degree-of-freedom
(threshold, weight, buffer, cutoff, smoothing window). Each must be tested
at ±50% per §6.6 in `sensitivity.md`.

| Parameter | Value | Reason for value | Sensitivity range |
|---|---|---|---|
| {name} | {value} | {reason} | {-50% to +50%} |

## 7. Primary source(s)

BibTeX keys for cited sources. Pinned versions in `/versions.json`.

- {key1, key2, …}

## 8. Decision rule

Given the metric and the sensitivity suite, what counts as a positive
result vs. a negative result? Stated as an unambiguous rule.

> *{rule}*

## 9. Stopping rule

When does data collection or computation stop? Stated as a deterministic
rule (e.g., "all DMCs in scope have at least one observation in the
time window, OR the source has been retried 3 times with exponential
back-off").

> *{rule}*

## 10. Owner attestation

| Field | Value |
|---|---|
| Frozen by | *(name)* |
| Date frozen | YYYY-MM-DD |
| Commit hash | *(hash)* |
| Pipeline run started after this commit | *(yes / no)* |

Any change to §1–§9 after a pipeline run is a retraction. A new
pre-registration replaces this one and the prior result is moved to
`retracted/`.
