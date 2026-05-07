# Remittance Resilience Gaps (Program 14)

**Status (2026-04-25):** Finished for the current §18 AI-First issue with a
multi-DMC screening artifact computed. Human-final review is still required
before any external submission or peer-reviewed claim beyond the current
issue.

## Files
- `README.md` — this overview
- `scripts/process-remittance.py` — pulls RPW + WDI, computes fragility index
- `.cache/rpw_dataset_2011_2025_q1.xlsx` — World Bank Remittance Prices
  Worldwide Q1 2025 dataset (49 MB)
- `.cache/wdi_remittance_pct_gdp.json` — WDI BX.TRF.PWKR.DT.GD.ZS 2015–2024
- `generated/remittance-resilience-adb-panel.json` — ADB regional DMC panel
- `generated/remittance-resilience-adb-panel.csv`

## Headline (to be reviewed by owner)

Across the 50 ADB regional DMCs, the 10 most fragile (highest combination
of remittance dependence and inbound transfer cost) are:

| Rank | DMC | Dependence (% GDP) | Mean cost % | Fragility |
|---|---|---|---|---|
| 1 | KGZ — Kyrgyz Republic | 26.58 | 10.54 | 70.3 |
| 2 | WSM — Samoa | 24.01 | 7.96 | 51.0 |
| 3 | TON — Tonga | 42.61 | 7.51 | 50.1 |
| 4 | VUT — Vanuatu | 18.75 | 9.54 | 47.7 |
| 5 | NPL — Nepal | 26.23 | 6.74 | 44.9 |
| 6 | TJK — Tajikistan | 47.89 | 2.95 | 19.7 |
| 7 | PAK — Pakistan | 9.40 | 7.69 | 19.3 |
| 8 | KHM — Cambodia | 6.10 | 10.56 | 17.2 |
| 9 | MMR — Myanmar | 3.40 | 28.16 | 13.6 |
| 10 | BGD — Bangladesh | 6.11 | 6.97 | 11.4 |

Three patterns:
1. **Pacific small islands** (TON, WSM, VUT) carry both high dependence and
   high inbound cost — small destination markets attract few corridors.
2. **Central Asia** (KGZ, TJK) has high dependence; cost is moderate for
   Russia-routes but elevated for non-Russia routes.
3. **Myanmar's 28.16% transfer cost** is exceptional — likely reflects
   FX/sanctions friction.

## Method (summary)

For each ADB DMC, the fragility index is:

```
fragility = min(remittance_pct_gdp / 25, 1) × min(mean_cost_pct / 15, 1) × 100
```

This is a **triage measure**, not a final risk rating. Per Constitution
§6.4, composite indices may not be the headline of any program — the
headline finding is the **distribution and the corridor-level breakdown**,
not the rank.

## Sources

- **RPW Q1 2025** — World Bank Remittance Prices Worldwide. License:
  open with attribution. Retrieved 2026-04-25 from
  `https://remittanceprices.worldbank.org/data-download`. 198,000 rows
  globally; 84,947 with an ADB-DMC destination; 2,963 in the latest
  Q1 2025 period.
- **WDI BX.TRF.PWKR.DT.GD.ZS** — Personal remittances received (% GDP).
  CC BY 4.0. Latest available year per economy (2015–2024 window).

## Reproduce

```bash
# RPW xlsx already cached; rerun if you want fresh:
curl -sS -o remittance-resilience/.cache/rpw_dataset_2011_2025_q1.xlsx \
  "https://remittanceprices.worldbank.org/sites/default/files/rpw_dataset_2011_2025_q1.xlsx"

# WDI cache (also already populated):
curl -sS -o remittance-resilience/.cache/wdi_remittance_pct_gdp.json \
  "https://api.worldbank.org/v2/country/all/indicator/BX.TRF.PWKR.DT.GD.ZS?format=json&per_page=20000&date=2015:2024"

# Compute the panel:
python remittance-resilience/scripts/process-remittance.py
```

## Caveats

1. RPW only covers **monitored corridors**. Many ADB DMCs are partially
   covered (e.g., RPW samples USD-AUD-SGD-NZD-EUR-JPY-CAD-RUB-AED senders;
   intra-regional corridors like Thailand → Lao PDR are under-sampled).
2. Mean cost across observed corridors is biased toward the corridors that
   are *actually monitored* — Pacific corridors with thin samples will
   read with high variance.
3. Dependence (% GDP) measures macro-level reliance but misses
   household-level concentration (one prefecture / district may carry
   most remittance flows; this is invisible at country level).
4. Fragility = dependence × cost is multiplicative; either factor at zero
   yields zero. A DMC with 0% remittance dependence is not "resilient" —
   it just isn't using this channel. The index does not measure overall
   household financial resilience.

Per Constitution §13.3, framing in any output is **"corridor-cost ×
dependence vulnerability"**, not "fragile country."
