# Literature review — Climate-Health Workday Loss

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27.

## 1. Search record

Queries (2026-04-26):
1. `Lancet Countdown labor capacity loss heat indicator`
2. `WHO PM2.5 ambient air quality guidelines 2021`
3. `Park Behrer Goodman heat learning PNAS`
4. `van Donkelaar ACAG-V6 satellite PM2.5 1km`
5. `outdoor labor exposure climate productivity LMIC`

Tier-A: *The Lancet*, *Nature Climate Change*, *Environmental
Research Letters*, *American Economic Journal: Economic Policy*.
Tier-B: WHO publications, IIASA, Health Effects Institute (HEI).
Tier-C: WB CCKP technical notes, ADB climate-and-health briefs.

## 2. Verified entries

- **`romanello2024lancet`** — Romanello et al. (2024). The 2024
  Lancet Countdown report. *The Lancet* 404(10465):1847–1896.
  doi:10.1016/S0140-6736(24)01822-1. **Indicator 1.1.4
  (heat-related labor capacity loss) is the established framework
  for hidden-workday-loss claims.**
- **`who2021aqg`** — WHO 2021 ambient AQ guidelines. **The
  5 µg/m³ annual mean PM2.5 guideline used as the floor.**
- **`park2020heat`** — Park, Behrer, Goodman (2020). Heat and
  learning. *AEJ: Economic Policy* 12(2):306–339.
  doi:10.1257/pol.20180612. **Empirical thresholds at 27–32°C;
  cited in the related school-heat program as evidence the linear
  ramp is the wrong functional form.**
- **`vandonkelaar2021monthly`** — van Donkelaar et al. (2021).
  ACAG-V6 satellite-derived 1-km gridded PM2.5. *EST*
  55(22):15287–15300. **The §18.5 upgrade-pass for subnational
  exposure.**

## 3. Synthesis

Three established facts:

1. **Heat reduces outdoor labor productivity.** The Lancet
   Countdown framework [@romanello2024lancet] quantifies this at
   the country-population level annually.
2. **PM2.5 exposure causes premature mortality and labor-capacity
   loss.** WHO 2021 [@who2021aqg] tightened the annual mean
   guideline to 5 µg/m³.
3. **Country-mean PM2.5 conceals dramatic within-country
   variance.** ACAG-V6 [@vandonkelaar2021monthly] documents this
   globally at 1-km resolution.
4. **Heat-learning thresholds are non-linear.** Park et al. 2020
   [@park2020heat] show effects emerging around 27°C, not 25°C.

## 4. Gap

No published cross-ADB-DMC PM2.5-only outdoor-labor pressure index
with sensitivity-tested rank stability. The Lancet Countdown
publishes country-level indicators but not the joint-with-outdoor-
labor product across the ADB regional roster specifically.

## 5. Risk of redundancy

Lancet Countdown 1.1.4 supersedes any composite PM2.5-only index
for actionable policy. This program's value is in the set-stability
claim (top-3 robust across ±50%), not in the index itself.

## 6. First testable claim

> Three ADB DMCs — Afghanistan, India, Bangladesh — persistently
> rank in the top three of the workday-loss pressure index, across
> every ±50% perturbation of three arbitrary parameters.

## 7. §18 attestation

Same structure as remittance literature.md §7. AI-first,
upgrade-eligible.
