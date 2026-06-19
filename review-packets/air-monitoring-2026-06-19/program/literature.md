# Literature review — Air Pollution Without Air Monitors

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27.

## 1. Search record

Queries (2026-04-27):
1. `OpenAQ public PM2.5 monitor density LMIC`
2. `WHO 2021 ambient air quality guidelines 5 µg/m³`
3. `Shaddick DIMAQ PM2.5 data integration model`
4. `van Donkelaar ACAG-V6 satellite PM2.5 Dalhousie`

Tier-A: *Environmental Science & Technology*, *Journal of the
Royal Statistical Society: Series C*, *The Lancet Planetary Health*.
Tier-B: WHO, HEI, Dalhousie, OpenAQ. Tier-C: WB AQM, IIASA.

## 2. Verified entries

- **`who2021aqg`** — WHO 2021 ambient AQ guidelines. **The 5 µg/m³
  annual mean PM2.5 guideline.**
- **`vandonkelaar2021monthly`** — van Donkelaar et al. (2021).
  ACAG-V6 satellite PM2.5. *EST*. **§18.5 upgrade-pass.**
- **`shaddick2018data`** — Shaddick et al. (2018). DIMAQ
  data-integration model. *JRSS:C*. doi:10.1111/rssc.12227.
  **The model underlying WDI national PM2.5 estimates in
  low-monitor DMCs.**

## 3. Synthesis

1. **WDI national PM2.5 is monitor-interpolated**
   [@shaddick2018data]; in low-monitor DMCs it is effectively
   imputed via DIMAQ.
2. **WHO 2021 [@who2021aqg]** tightened the annual mean guideline
   to 5 µg/m³ and provides interim targets at 35, 25, 15, 10.
3. **ACAG-V6 [@vandonkelaar2021monthly]** provides 1-km gridded
   global PM2.5; the §18.5 upgrade-pass for low-monitor DMCs.

## 4. Gap

No published cross-ADB-region PM2.5 observability-gap ranking
combining OpenAQ monitor density with WHO PM2.5 exposure.

## 5. First testable claim

> Five ADB-region economies — Afghanistan, Bangladesh, Myanmar,
> Uzbekistan, Tajikistan — hold the top-5 PM2.5 observability-gap
> positions, combining high WHO-derived PM2.5 exposure with
> sparse or absent OpenAQ public PM2.5 monitoring.

## 7. §18 attestation

`ai-first`. 2026-04-27.
