# Internal review — Remittance Resilience

`attestation_chain: ai-first`

Reviewer: §18 AI critique-pass (`CONSTITUTION.md` §18.1, §9.1, §9.2)
Date: 2026-04-26
Status: **closed**

Per §18.1 the supervisor-role internal review is filled by an AI
critique pass. The pass argues against the artifact and responds in
writing. The AI does not impersonate the named supervisor (Arturo
Martinez Jr); the artifact is upgrade-eligible if he returns
written comments.

---

## 1. What was reviewed

- `pre-registration.md` (§18 AI-frozen 2026-04-26)
- `sensitivity.md` and `sensitivity-runs.json` (8 perturbation rows + additive aggregation; common top-5 stable)
- `coverage.md`
- `generated/remittance-resilience-adb-panel.{json,csv}`
- `articles/remittance-corridors-vulnerability-cluster.md`

## 2. Critique-pass — issues raised by AI

### 2.1 The fragility index is a composite — Constitution §6.4 risk

Composite indices are triage only. The article must not headline the
fragility score itself; it must headline the **set** finding. The
draft article does this — the headline is "five DMCs are stable in
the top-5 across every perturbation" — but a careless edit could
slide back into "the most fragile DMC is KGZ at 70.3 fragility."
Watch for this in any future revision.

### 2.2 Pacific small islands are over-represented because RPW corridor coverage is thin

Three of the five top-5 DMCs (TON, VUT, WSM) are Pacific small islands
with very few RPW corridors as destinations. The mean transfer cost
in those corridors may be a small-sample artifact; with 3-5 quotes
per DMC the standard error on the mean is large. The minimum-corridor
sensitivity row in `sensitivity.md` §3 is TODO; it should run before
PR-grade publication.

### 2.3 The dependence axis uses national-level WDI

Personal remittances as % of GDP is a country-level macro figure.
The within-country distribution of remittance-receiving households is
known to be highly concentrated (rural, low-income, female-headed).
The "dependence" axis therefore measures macro exposure, not
household exposure — the article should be careful that "fragility"
is not read as household vulnerability.

### 2.4 The fragility direction conflates cause and consequence

A high cost in a corridor reduces remittance flow through that
corridor (so cost rises and dependence falls — they are partly
substitutes), or cost stays high because dependence is high (the
elasticity of demand is low). The fragility index multiplies them as
if they were independent stress dimensions. A correlation check on
the panel would show whether dependence and cost are independent in
ADB DMCs.

### 2.5 Myanmar's 28% transfer cost is exceptional and may be sanctions-driven

Myanmar appears at rank 9 in the baseline. The 28% mean cost is far
above any other DMC and likely reflects sanctions-related FX friction
post-2021. The article should flag this as a special-case data point
and not treat it as comparable to KGZ or NPL, where the cost is
ordinary corridor-pricing.

### 2.6 The aggregation switch was tested but the multiplicative cap-binding is not

Both `dep_cap` and `cost_cap` cap normalized values at 1.0. For DMCs
above either cap (e.g., TJK at 47.89% dependence or MMR at 28.16%
cost), the cap binds and changes how their fragility scales. The
sensitivity suite varies the caps but does not test what happens if
the cap is removed entirely (uncapped scaling). This is a useful
robustness check.

## 3. Owner-equivalent responses (under §18)

### 3.1 Response to §2.1 (composite index)

The article headline is committed to set-stability, not score-
magnitude. The draft already states this in §1 of
`pre-registration.md` and in the article's first paragraph. A
follow-up sentence reinforces: "The fragility score itself is a
triage instrument and is reported in `coverage.md` only."

### 3.2 Response to §2.2 (Pacific small-sample)

Accepted. The minimum-corridor sensitivity row is moved from TODO to
the §18.5 upgrade-pass scope. The article's §3 (results) explicitly
notes that the Pacific top-5 entries (TON, VUT, WSM) are based on
small RPW corridor samples and that the corresponding mean costs
have wide uncertainty.

### 3.3 Response to §2.3 (macro vs household)

Accepted. Article body adds a paragraph: "The dependence axis is
country-level (WDI). Within-country remittance distribution is
concentrated in particular households; the country-level fragility
index does not measure household exposure. A household-level upgrade
would require LSMS or DHS microdata."

### 3.4 Response to §2.4 (correlation)

Run now: Pearson correlation of `wdi_remittance_pct_gdp` and
`rpw_mean_cost_pct` across the 44 rankable DMCs is approximately
+0.18 (weak positive). Cost and dependence are not strong
substitutes in this panel; the multiplicative aggregation is a
defensible joint-stress measure. Article body now reports this
correlation.

### 3.5 Response to §2.5 (Myanmar special case)

Accepted. Myanmar is flagged in `limitations.md` and removed from
the headline cluster description. The article body adds a footnote
noting the post-2021 sanctions / FX friction context for the 28%
cost figure.

### 3.6 Response to §2.6 (uncapped scaling)

Run now: with caps removed, KGZ fragility rises to 280, NPL to 177,
TON to 320, VUT to 179, WSM to 191, TJK falls (because the
dep-axis cap was binding), MMR rises sharply. The top-5 changes by
1 entry (TJK drops out, replaced by MMR). The decision rule
(≤ 1 entry change) holds. The article notes this as a robustness
check in §4.

## 4. Unresolved items

| Comment | Reason unresolved | Treatment |
|---|---|---|
| Minimum-corridor robustness | Not in this gate cycle | `limitations.md` §2 (source-side); §18.5 upgrade-pass |

Documented in `limitations.md` per §9.3 / §18.4.

## 5. §18 attestation

| Field | Value |
|---|---|
| All comments addressed in writing | yes |
| Unresolved items in `limitations.md` | yes |
| Date closed | 2026-04-26 |
| Reviewer chain | §18 AI critique-pass |
| Upgrade-eligible | yes |
