# External red-team review — Remittance Resilience

`attestation_chain: ai-first`

Status: **closed under §18.4 AI red-team synthesis — 2026-04-26.**

Per `CONSTITUTION.md` §9.3, §18.1, and §18.4. **No individual reviewer
was contacted under §18.** Objections below are AI-synthesized from
each candidate institution's published methodological position.

---

## 1. Candidate-reviewer roster

| ID | Institution | Competency | DMC focus | Synthesized from |
|---|---|---|---|---|
| C-1 | KNOMAD (World Bank Global Knowledge Partnership on Migration and Development) | Domain — remittances, migration | Global LMIC | KNOMAD Migration and Development Brief series, RPW methodological papers |
| C-2 | World Bank Payment Systems Development Group | Domain — remittance corridor pricing | Global LMIC | RPW dataset documentation, GENRC methodology |
| C-3 | IZA migration cluster | Measurement — household remittance distribution | Global | IZA discussion-paper series on remittances |
| C-4 | Pacific Community (SPC) Statistics for Development Division | DMC-affiliated, Pacific | Pacific small-island states | SPC Pacific economy snapshots, NSO-coordinated household-survey programs |
| C-5 | Nepal Rastra Bank Research Department | DMC-affiliated, NPL | NPL | NRB working-paper series on remittance flows |
| C-6 | OSCE Academy in Bishkek | DMC-affiliated, KGZ | Central Asia | OSCE Academy working papers on Russia-corridor labor migration |

## 2. What was reviewed

The full set of program artifacts at `public-service-data-quality/`-
equivalent paths under `remittance-resilience/`, including
`pre-registration.md`, `sensitivity.md`, `sensitivity-runs.json`,
`coverage.md`, `generated/remittance-resilience-adb-panel.{json,csv}`,
`review-internal.md`, the article at
`articles/remittance-corridors-vulnerability-cluster.md`, and
`limitations.md`.

## 3. Synthesized objections

### 3.1 From C-1 (KNOMAD), synthesized

> **Objection 3.1.1.** RPW measures the cost of *publicly-quoted*
> corridors. In high-volume corridors with significant informal
> remittance use (e.g., GCC → South Asia, Russia → Central Asia
> hawala / hundi), the publicly-quoted cost may be a poor proxy for
> what households actually pay. KNOMAD has repeatedly flagged the
> formal-vs-informal corridor share as a confounder. The article
> should report the WB Migration and Development Brief estimate of
> informal-share for each top-5 DMC if available.

> **Objection 3.1.2.** Personal remittances received as percent of
> GDP (WDI) and the fragility framing do not capture the
> *resilience* dimension that the program name implies. Resilience
> includes counter-cyclicality (do remittances rise during local
> shocks?), which is well-documented in KNOMAD work but not measured
> here. The article's framing should be precise: this measures
> exposure to corridor-cost shocks, not resilience.

### 3.2 From C-2 (World Bank Payment Systems), synthesized

> **Objection 3.2.1.** RPW publishes corridor cost as the inbound
> total cost from a sending country to a destination country. The
> destination-aggregated mean (used here) loses information about
> which sending corridors are most expensive. For policy use, the
> per-source-corridor breakdown is more actionable. The article
> should publish the corridor table (`expensive_corridors_top50` in
> the JSON) prominently, not just the destination ranking.

> **Objection 3.2.2.** The 5% cost benchmark from SDG 10.c.1 is the
> standard reference. The article should map each top-5 DMC's mean
> cost to the SDG benchmark explicitly: KGZ 10.5% (2.1× SDG), TON
> 7.5% (1.5× SDG), etc.

### 3.3 From C-3 (IZA migration cluster), synthesized

> **Objection 3.3.1.** Within-country distribution of remittance
> receipt is highly concentrated. IZA work has documented that
> the top decile of households receiving remittances accounts for
> 50–70% of total remittance income in many LMICs. Country-level
> WDI dependence is therefore not a household-vulnerability measure;
> the article must distinguish.

### 3.4 From C-4 (SPC, Pacific), synthesized

> **Objection 3.4.1.** Pacific micro-states have very few RPW
> corridors (Tonga's RPW corridor count is around 5–8; Vanuatu
> similar). The mean cost across so few corridors has wide
> sampling uncertainty. The article should report a confidence
> interval on the mean cost or restrict the top-5 claim to DMCs
> with at least 10 corridor observations.

> **Objection 3.4.2.** Tonga and Samoa receive the bulk of their
> remittances from a small set of sources (US, NZ, AU). The
> "destination" framing of RPW masks the source-corridor
> concentration: 80%+ of TON inbound flows from a small number of
> source markets, so cost in those specific corridors matters far
> more than the destination-mean. The article should report
> source-corridor-specific cost for the Pacific top-5.

### 3.5 From C-5 (NRB, Nepal), synthesized

> **Objection 3.5.1.** Nepal's GCC corridors (Saudi Arabia, UAE,
> Qatar) are the dominant inbound flow. NRB tracks corridor cost
> for these specifically and publishes them in its quarterly
> bulletin. The RPW figure of 6.74% mean cost for Nepal is
> consistent with NRB's GCC-corridor estimates but masks the higher-
> cost Malaysia and Korea corridors. The article should reference
> NRB's bulletin as the local-data anchor.

### 3.6 From C-6 (OSCE Academy, KGZ), synthesized

> **Objection 3.6.1.** Russia-Kyrgyz corridor cost is anomalously
> low (~2-3%) due to MTO competition and the cross-border banking
> integration through the Eurasian Economic Union. The 10.5% mean
> cost for KGZ in this artifact is dragged up by non-Russia
> corridors that account for a small share of actual flow. The
> article should weight by corridor-volume, not equal-weight
> across corridors, for the Central Asian DMCs.

## 4. Owner-equivalent responses (under §18)

### 4.1 Response to C-1.1 (formal-vs-informal share)

Accepted. Article body adds a paragraph noting that RPW measures
publicly-quoted corridor cost, and that informal corridors (hawala /
hundi / undocumented MTO use) are common in GCC → South Asia and
Russia → Central Asia. The fragility figure is therefore an upper
bound on what households actually pay through informal channels.

### 4.2 Response to C-1.2 (resilience vs exposure framing)

Accepted. The program is renamed conceptually: the article now
frames the screen as "exposure to corridor-cost stress" not
"resilience." Counter-cyclicality (the actual resilience question)
is flagged as a separate program (out of scope for this gate).

### 4.3 Response to C-2.1 (corridor breakdown)

Accepted. The article's results section now includes the corridor
table from `generated/remittance-resilience-adb-panel.json`'s
`expensive_corridors_top50` field as a key exhibit, not the
destination-ranked table.

### 4.4 Response to C-2.2 (SDG 10.c.1 benchmark)

Accepted. Article body maps each top-5 DMC's mean cost to the SDG
10.c.1 benchmark (5%): KGZ 10.5% (2.1× SDG), WSM 7.96% (1.6×),
TON 7.51% (1.5×), VUT 9.54% (1.9×), NPL 6.74% (1.3×).

### 4.5 Response to C-3.1 (household concentration)

Accepted. Article body adds the paragraph from `review-internal.md`
§3.3 reading: "Personal remittances as percent of GDP is a country-
level macro figure. Within-country remittance receipt is
concentrated in particular households (LSMS / DHS microdata
required for household-level estimates). The country-level
fragility index does not measure household exposure."

### 4.6 Response to C-4.1 (Pacific small-sample)

Accepted. Article body adds the corridor counts per top-5 DMC and
flags Pacific entries as "small-sample mean cost; wide confidence
interval." The §18.5 upgrade-pass restricts the top-5 to DMCs with
≥ 10 corridor observations.

### 4.7 Response to C-4.2 (source-corridor concentration)

Accepted. Article body now reports the top-3 source corridors per
Pacific DMC (TON, VUT, WSM) with their per-corridor cost, alongside
the destination-mean.

### 4.8 Response to C-5.1 (NRB bulletin)

Accepted. The article cites the NRB Quarterly Economic Bulletin as
the local-data anchor for Nepal corridor pricing.

### 4.9 Response to C-6.1 (volume-weighted KGZ)

Accepted as a known limitation. The RPW dataset does not include
corridor-volume; volume-weighting would require IMF-DOTS-style
corridor-flow data. This is documented in `limitations.md` §3 and
is part of the §18.5 upgrade-pass.

## 5. Unresolved items (move to `limitations.md` §5 verbatim)

| Source | Objection | Treatment |
|---|---|---|
| C-2.1 | Per-source-corridor breakdown should be the headline | Article restructured to lead with corridor table |
| C-4.1 | Pacific small-sample mean-cost uncertainty | §18.5 upgrade-pass: restrict to DMCs with ≥ 10 corridor observations |
| C-6.1 | Volume-weighted corridor cost (rather than equal-weight) | §18.5 upgrade-pass: requires IMF-DOTS or central-bank corridor-flow data |
| C-3.1 | Household-level distribution of remittance receipt | §18.5 upgrade-pass: requires LSMS / DHS microdata |

## 6. §18.4 explicit non-claim

> No individual reviewer was contacted under §18. The objections in
> §3 above are AI-synthesized from each candidate institution's
> public methodological stance, not actual reviewer feedback. The
> artifact is upgrade-eligible: when an actual reviewer from any
> listed institution returns written comments, this section is
> replaced verbatim with their feedback and the article is re-
> deposited with a new DOI version.

## 7. Acknowledgments

> Acknowledgments: This article's red-team review was performed
> under `CONSTITUTION.md` §18.4 (AI-First Operating Mode) by AI
> synthesis against the published methodological positions of
> KNOMAD, World Bank Payment Systems Development Group, IZA
> migration cluster, Pacific Community Statistics for Development
> Division, Nepal Rastra Bank Research Department, and OSCE Academy
> in Bishkek. No individual reviewer is named because none was
> contacted under §18. The article is upgrade-eligible to a
> human-final attestation chain via §18.5.

## 8. §18 attestation

| Field | Value |
|---|---|
| Synthesis pass complete | yes (2026-04-26) |
| Each candidate institution covered | yes (6 candidates) |
| Each objection responded to | yes |
| Unresolved objections in `limitations.md` §5 | yes |
| §18.4 explicit non-claim recorded | yes (§6) |
| Upgrade-eligible | yes |
| Date closed | 2026-04-26 |
| Reviewer chain | §18 AI synthesis under §18.4 |
