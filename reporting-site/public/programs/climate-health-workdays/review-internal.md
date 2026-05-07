# Internal review — Climate-Health Workday Loss

`attestation_chain: ai-first`

Reviewer: §18 AI critique-pass.
Date: 2026-04-26.
Status: **closed**.

---

## 1. What was reviewed

`pre-registration.md`, `sensitivity.md`, `sensitivity-runs.json`,
`coverage.md`, `generated/*`, the article.

## 2. Critique-pass — issues raised

### 2.1 The "outdoor labor" proxy is coarse

`agri% + 0.5 × industry%` is a rough proxy. Industry includes both
outdoor (construction, mining) and indoor (manufacturing) work; the
0.5 weight is split-the-difference. Sensitivity at ±50% on this
weight is included; the headline survives.

### 2.2 PM2.5-only ignores heat

The program README anticipates heat exposure as a dimension. The
current pipeline uses PM2.5 alone. The article must not present this
as the full "climate-health workday loss" pressure — it is the
pollution-only subset. Heat is the §18.5 upgrade-pass.

### 2.3 Country-mean PM2.5 hides huge within-country variance

WDI EN.ATM.PM25.MC.M3 is a national mean. India's actual PM2.5
distribution ranges from ~10 µg/m³ in the south to >100 µg/m³ in the
Indo-Gangetic Plain. The country-mean understates exposure for the
populated north and overstates for the south. Subnational analysis
via ACAG-V6 (Dalhousie) or Earth Engine is the upgrade-pass.

### 2.4 The 5/45 PM2.5 ramp is WHO-anchored but not universal

The PM2.5 floor (5) is the WHO 2021 ambient AQ guideline. The cap (45)
is roughly WHO interim target 2 + margin. A reviewer at WHO Air
Quality team might reasonably argue for a different cap (e.g., the
35 µg/m³ interim target 2 itself, or the 25 IT-3). The sensitivity
suite tests ±50% (22.5 and 67.5) and the headline narrows accordingly.

### 2.5 Top-3 is honest but small

A 3-economy claim is narrower than the typical top-5 in screening
articles. The honest answer to "what does the data robustly show?"
is the top-3. Reviewers may request the top-5 with explicit
sensitivity-shift labels rather than the narrowed top-3 — the
article reports both.

## 3. Owner-equivalent responses

3.1: accepted as a known limitation. Documented in `limitations.md`.
3.2: heat-exposure dimension is the §18.5 upgrade-pass; the article
explicitly labels the current index as the PM2.5-only subset.
3.3: subnational PM2.5 is in the upgrade-pass list.
3.4: WHO-team objection synthesized in `review-external.md`.
3.5: article reports both top-3 (claim) and top-5 (with sensitivity
disclosure).

## 4. §18 attestation

| Field | Value |
|---|---|
| Comments addressed | yes |
| Date closed | 2026-04-26 |
| Reviewer chain | §18 AI critique-pass |
| Upgrade-eligible | yes |
