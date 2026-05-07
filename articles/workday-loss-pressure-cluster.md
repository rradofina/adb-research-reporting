---
slug: workday-loss-pressure-cluster
title: Three DMCs persistently top the workday-loss pressure cluster
subtitle: Afghanistan, India, Bangladesh hold the top three positions across every parameter perturbation; the fourth and fifth shift.
kind: working-paper
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: [AFG, IND, BGD, PAK, TJK]
topics: [climate-health, PM2.5, outdoor-labor]
program: climate-health-workdays
maturity: PR
abstract: >
  The workday-loss pressure index combines outdoor-labor share
  (agriculture + half-weighted industry employment) with PM2.5 exposure
  pressure. Across 34 rankable ADB DMCs, three economies — Afghanistan,
  India, Bangladesh — sit in the top three of the ranking and remain
  there in every row of a ±50 percent sensitivity suite on the index's
  three arbitrary parameters. The fourth and fifth positions shift
  with PM2.5-cap perturbations; the headline is committed to the stable
  top three. The index is PM2.5-only; heat exposure (the Lancet
  Countdown's labor-capacity-loss framework) is the §18.5 upgrade-pass.
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

Where are heat and air-pollution exposure likely reducing effective
workdays before those losses appear in employment or GDP statistics?
The Lancet Countdown framework's indicator 1.1.4 (heat-related labor
capacity loss) is the established framing for hidden-workday-loss
claims. This article reports a PM2.5-only first cut at the question
across 44 ADB developing member economies.

# The data

- WDI SL.AGR.EMPL.ZS — agriculture employment share (% of total)
- WDI SL.IND.EMPL.ZS — industry employment share (% of total)
- WDI EN.ATM.PM25.MC.M3 — annual mean PM2.5 exposure (µg/m³)
- WDI SP.URB.TOTL.IN.ZS — urban population share
- WDI SP.POP.TOTL — total population

The pressure index is

```
outdoor_labor_share = (agri% + 0.5 × industry%) / 100
pm25_pressure       = clamp((pm25 - 5) / 45, 0, 1)
index               = outdoor_labor_share × pm25_pressure × 100
```

The 5 µg/m³ floor is the WHO 2021 ambient AQ guideline annual mean.
The 45 µg/m³ cap is the WHO interim target 2 (35) plus margin. The
0.5 industry weight reflects mixed indoor/outdoor industry exposure.

# The finding

Three ADB DMCs — **Afghanistan (55.7), India (53.1), Bangladesh
(44.6)** — sit in the top three of the index. The set is identical
across every row of the sensitivity suite at ±50% on each of the three
arbitrary parameters.

The fourth and fifth positions in the top five are typically Pakistan
(41.5) and Tajikistan (37.6) at baseline, but the PM2.5-cap-minus50
perturbation (cap = 22.5) shifts both — moving Nepal and Myanmar into
the top five. The pre-registered decision rule (≤ 1 entry change in
top-5) fails under that single perturbation. The headline therefore
narrows to the stable **top three**.

# What the data does not say

- The index is **PM2.5-only**. The proper "climate-health workday
  loss" measure includes heat. The Lancet Countdown framework's
  labor-capacity-loss indicator is heat-driven and is the upgrade-pass.
- The PM2.5 input is the **country mean**. India, China, Indonesia
  have dramatic within-country variance; the Indo-Gangetic Plain is
  far above the national mean and southern India far below. ACAG-V6
  satellite-derived 1-km gridded PM2.5 (Dalhousie atmospheric
  composition group, CC BY-NC) is the upgrade-pass for subnational
  resolution, with a non-commercial-redistribution caveat.
- Several low-monitor-density DMCs (AFG, MMR, KHM, LAO, TLS) have
  imputed PM2.5 inputs. AFG #1 carries this caveat.
- The result does not measure actual workday loss. It measures a
  proxy for exposure pressure on outdoor labor.

# Attestation chain

Per `CONSTITUTION.md` §18 (AI-First). Pre-registration AI-frozen
2026-04-26. Internal review (§18 critique-pass) and external red-team
review (§18.4 AI synthesis from Lancet Countdown, WHO Air Quality
team, Dalhousie atmospheric composition group, NUS LKYSPP climate
group, World Bank DECDG) closed. **No individual reviewer was
contacted.**

Permanent archive: [/program/climate-health-workdays/evidence](/program/climate-health-workdays/evidence).

# Reproduction

```bash
python climate-health-workdays/scripts/process-climate-health.py
python climate-health-workdays/scripts/sensitivity.py
```

— Raymond Adofina · 2026-04-26 · `attestation_chain: ai-first`
