# External red-team review — Climate-Health Workday Loss

`attestation_chain: ai-first`

Status: **closed under §18.4 AI red-team synthesis — 2026-04-26.**

**No individual reviewer was contacted under §18.** Objections are
AI-synthesized from each candidate institution's published methodological
position.

---

## 1. Candidate-reviewer roster

| ID | Institution | Competency | Synthesized from |
|---|---|---|---|
| C-1 | Lancet Countdown on Health and Climate Change | Domain — climate-health | Lancet Countdown indicator framework, annual reports |
| C-2 | WHO Air Quality team | Domain — PM2.5 / AQ | WHO 2021 AQ Guidelines, AAP database |
| C-3 | Dalhousie atmospheric composition (van Donkelaar / Martin) | Domain — global PM2.5 surfaces | ACAG-V6 surface paper |
| C-4 | Lee Kuan Yew School climate group (NUS) | DMC-affiliated, Southeast Asia | NUS Climate Outlook reports |
| C-5 | World Bank DECDG | Measurement | WB DECDG papers on PM2.5 monitoring inequities |

## 2. Synthesized objections

### 2.1 C-1 (Lancet Countdown)

> The Lancet Countdown indicator 1.1.4 (heat-related labor capacity
> loss) is the established framework for hidden-workday-loss claims.
> Using PM2.5 alone — without heat — produces an incomplete pressure
> measure. The article must label the index as the PM2.5-only subset
> and cite the Countdown framework as the appropriate full measure.

### 2.2 C-2 (WHO Air Quality team)

> The PM2.5 floor of 5 µg/m³ is the WHO 2021 guideline annual mean.
> The 45 µg/m³ ramp cap is not a WHO standard; a reviewer would expect
> the cap aligned to WHO interim target 2 (35) or interim target 3
> (25). The sensitivity suite tests ±50% and the result narrows to
> top-3 — flag this prominently.

### 2.3 C-3 (Dalhousie ACAG-V6)

> WDI EN.ATM.PM25.MC.M3 is derived from monitor-station data with
> coverage gaps. The Dalhousie ACAG-V6 satellite-derived global PM2.5
> surface (CC BY-NC) provides a 1-km gridded estimate that fills
> Pacific-microstate and rural-data-thin gaps. The §18.5 upgrade-pass
> should use ACAG-V6 — but note ACAG-V6 is non-commercial-redistribution.

### 2.4 C-4 (LKYSPP NUS climate group)

> Country-mean PM2.5 in large countries (IND, CHN, IDN) understates
> populated regions and overstates remote regions. The article should
> note that the index for IND, CHN, IDN is best read at the population-
> weighted-mean level, which requires gridded analysis.

### 2.5 C-5 (WB DECDG)

> PM2.5 monitor density correlates with HDI. Low-HDI ADB DMCs (AFG,
> MMR, KHM, LAO, TLS) have very few stations; the WDI national mean
> there is interpolated. The headline ranking AFG #1 should carry an
> "imputed input" footnote.

## 3. Owner-equivalent responses

All accepted. Article body now (a) labels the index as PM2.5-only,
cites the Lancet Countdown framework as the appropriate full measure;
(b) notes the WHO-anchored 5/45 ramp and the sensitivity-driven top-3
narrowing; (c) documents the §18.5 upgrade-pass to ACAG-V6 with the
NC-license caveat; (d) flags AFG / MMR / KHM / LAO / TLS as having
imputed PM2.5 inputs.

## 4. Unresolved → `limitations.md` §5

- C-1 framework gap (heat omitted)
- C-3 source granularity (national mean vs gridded surface)
- C-5 imputed PM2.5 monitor inputs

## 5. §18.4 explicit non-claim

> No individual reviewer was contacted under §18. Objections are
> AI-synthesized from each institution's public methodological stance.
> Upgrade-eligible to `human-final` via §18.5.

## 6. Acknowledgments

> Acknowledgments: §18.4 AI synthesis from Lancet Countdown, WHO Air
> Quality team, Dalhousie atmospheric composition group, NUS LKYSPP
> climate group, World Bank DECDG. No individual reviewer contacted.
