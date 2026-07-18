# Sensitivity — {program-title}

Governed by `CONSTITUTION.md` §6.6. Every arbitrary numeric in
`pre-registration.md` §6 is tested at ±50%. The program does not
advance past Screening Result without a complete sensitivity table.

Status: **{not run | in progress | complete}**

---

## 1. Test matrix

| Parameter | Pre-registered value | Test at -50% | Test at +50% | Result delta vs. baseline | Decision-rule preserved? |
|---|---|---|---|---|---|
| {name} | {v} | {0.5v} | {1.5v} | {delta} | {yes / no} |

A row that flips the decision rule (changes the answer to the claim) is a
**critical sensitivity failure**. The claim cannot advance to
Publication-ready until either (a) the parameter is removed from the
pipeline, (b) the parameter is replaced with a non-arbitrary
specification, or (c) the claim is restricted to the parameter range
where the decision rule survives.

---

## 2. Replication ranges

For each metric, the range of plausible values across the sensitivity
suite. Reported in the publication's results table per §10.

| Metric | Baseline | Min across sensitivity suite | Max across sensitivity suite |
|---|---|---|---|

---

## 3. Robustness checks beyond ±50%

Additional checks that go beyond the §6.6 minimum:

- {leave-one-out by DMC}
- {alternative source cross-validation}
- {time-window subsampling}
- {seed sensitivity for any randomized component}

---

## 4. Owner attestation

| Field | Value |
|---|---|
| Sensitivity suite run | *(yes / no)* |
| Date run | YYYY-MM-DD |
| Critical failures resolved | *(yes / no — if no, list)* |
| Commit hash | *(hash)* |
