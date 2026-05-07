---
slug: emigrant-stock-corridor-concentration
title: Five DMCs hold the top of UN DESA's emigrant-stock ranking — and the corridor concentration splits the cluster in two
subtitle: India, China, Bangladesh, Afghanistan, Philippines stable across direction-of-definition; three of the five concentrate over half their emigration in three corridors, two diversify.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [IND, CHN, BGD, AFG, PHL]
topics: [migration, emigrant-stock, corridor-concentration]
program: migration-displacement-signals
maturity: PR
abstract: >
  UN DESA International Migrant Stock 2024 reports cumulative foreign-
  born populations by country. Across the 44 ADB regional DMCs published
  in the 2024 vintage, five economies — India, China, Bangladesh,
  Afghanistan, Philippines — sit in the top five of the emigrant-stock
  ranking. The same five hold the top five when ranked by net migrant
  stock (emigrant minus immigrant). A second pattern splits the cluster:
  three of the five (Bangladesh, Afghanistan, Philippines) concentrate
  more than 50 percent of their emigration in their top-3 destination
  corridors; India and China have substantially more diversified
  destination profiles. Afghanistan's 80 percent concentration is
  refugee-driven and not comparable to labor-migration concentration.
  Published under §18 (AI-First).
doi:
published_at: 2026-04-26
updated_at: 2026-04-26
references: []
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
review_external_chain: ai-synthesis under §18.4
review_internal_chain: ai-critique-pass under §18 (§9.1 + §9.2)
---

# The question

International migration corridors are an old subject in development
economics. The standard headlines — "top remittance-receiver," "top
labor-export country" — typically rank flows. UN DESA, by contrast,
publishes **stock** (cumulative foreign-born), updated every five
years (latest: 2024). The structural question this article asks is
different: do the same DMCs hold the top of the emigrant-stock
ranking regardless of direction-of-definition? And is the
corridor-concentration pattern uniform within that set, or does it
split?

# The data

UN DESA International Migrant Stock 2024 (CC BY 3.0 IGO). The 2024
vintage publishes for 44 of the 50 ADB regional DMCs. Six small
economies (NIU, COK, NRU, TUV, KIR, MHL) are not in the publication.
The dataset is bilateral: every country pair has an entry for stock
of country-A-born currently resident in country B.

# The finding

## Set-stability of the top-5 emigrant DMCs

| Rank | ISO3 | DMC | Emigrant stock 2024 |
|---|---|---|---|
| 1 | IND | India | 18,533,845 |
| 2 | CHN | China | 11,701,619 |
| 3 | BGD | Bangladesh | 8,706,947 |
| 4 | AFG | Afghanistan | 7,528,994 |
| 5 | PHL | Philippines | 6,988,383 |

The same five economies hold the top-5 positions when ranked by
**net** migrant stock (emigrant minus immigrant) instead of raw
emigrant stock. Set overlap: 5 of 5.

A separate ranking — **emigrant share of total foreign-born stock**
(emigrant / (emigrant + immigrant)) — produces a different top-5,
dominated by small high-share DMCs. This is a different question
("how emigration-heavy is the country relative to its population
churn") and is not the §1 claim.

## Corridor-concentration split

Top-3 destination share for each top-5 DMC:

| ISO3 | Top-3 destination share | Note |
|---|---|---|
| IND | 45% | diversified labor + skilled corridors |
| CHN | 49% | diversified — US/Canada/Australia + intra-Asia |
| BGD | 65% | concentrated — India + GCC |
| AFG | 80% | refugee-driven — Iran + Pakistan + Pakistan |
| PHL | 55% | concentrated — US + Canada + KSA |

The split is structural: three of the five (BGD, AFG, PHL) concentrate
more than half their emigration in three destinations; the other two
(IND, CHN) do not.

Afghanistan's 80% is refugee-driven and not comparable to the others.
The Iran and Pakistan corridors are post-1979 and post-2021
displaced-population stocks, not labor migration.

# What the data does not say

- **Stock is not flow.** UN DESA measures cumulative foreign-born
  stock. The 18.5M India figure is people of Indian origin currently
  abroad, accumulated over decades, not migrants leaving in 2024.
- **Refugees are folded in.** UN DESA's methodology counts all
  foreign-born regardless of legal status. AFG and (less dramatically)
  MMR are refugee-driven entries; the article does not present them
  as labor-migration patterns.
- **Internal displacement is excluded.** UN DESA measures
  international migration only. Internal displacement (IDPs) requires
  IDMC GRID data; this program does not yet integrate it.
- **Informal corridors are under-reported.** Intra-South-Asia and
  intra-GCC undocumented labor migration is known to be undercounted
  in UN DESA's bilateral matrices.
- **Pacific cumulative diaspora.** TON, WSM, VUT have emigrant stocks
  that include large historical diaspora populations from earlier
  waves; not contemporary labor-mobility flow.

# Attestation chain

Per `CONSTITUTION.md` §18 (AI-First). Pre-registration AI-frozen
2026-04-26. Internal critique-pass and §18.4 AI synthesis (KNOMAD,
UN DESA, IZA migration cluster, KEMRI/WorldPop, ANU Devpolicy, IDMC)
closed. **No individual reviewer was contacted.**

Permanent archive: [/program/migration-displacement-signals/evidence](/program/migration-displacement-signals/evidence).

# Reproduction

```bash
python migration-displacement-signals/scripts/process-migration.py
python migration-displacement-signals/scripts/sensitivity.py
```

— Raymond Adofina · 2026-04-26 · `attestation_chain: ai-first`
