# L2 Hook Sprint: Nepal Market-Climate Price Join

`attestation_chain: ai-first`
Date: 2026-06-16
Goal level: L2 hook sprint

## Decision

Promote this as a new program prospectus candidate.

The hook is not a public finding yet. It is a topic-creation result: WFP
market-month food prices can be joined to local point climate data in a way
that asks a sharper question than a national CPI screen. The first visual
shows price anomalies and previous-month precipitation anomalies side by side
for the same markets and months.

## Question Tested

Do local rice-price anomalies line up with previous-month local precipitation
anomalies, or does the market-month data point to a broader/non-climate price
process that national CPI would hide?

## Public Data Object

The sprint uses Nepal as a one-DMC source test.

- WFP Nepal food-price and market CSV resources from HDX.
- NASA POWER monthly point API values at WFP market coordinates.
- One commodity for sprint control: `Rice (coarse)`, retail `KG`, actual
  price observations.

The method builds a market-month table for 2019-2025 prices, uses 2018-2025
NASA POWER data so January 2019 can receive a previous-month climate lag, and
keeps the climate variable local to each market coordinate.

## Generated Artifacts

| Artifact | Path |
|---|---|
| Script | `research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py` |
| CSV | `research/topic-sprints/generated/nepal-market-climate-prices-sprint.csv` |
| JSON | `research/topic-sprints/generated/nepal-market-climate-prices-sprint.json` |
| Rough chart | `research/topic-sprints/generated/charts/nepal-market-climate-prices-heatmap.png` and `.svg` |

Reproduce:

```powershell
python research/topic-sprints/scripts/sprint-nepal-market-climate-prices.py
```

## Data Sanity Checks

The script retained 2,011 WFP price rows for the selected commodity, price
type, flag, unit, and 2019-2025 period. Those rows covered 36 markets before
selection. The sprint selected 12 markets with sufficient monthly coverage,
creating 1,008 market-month cells; 937 cells have both a price anomaly and a
lagged precipitation anomaly.

NASA POWER metadata in the generated JSON records `PRECTOTCORR` in `mm/day`
and `T2M` in `C`. The chart uses only the lagged precipitation z-score, but
the table stores temperature z-scores for later falsifier design.

The first dry-price-spike screen flags 26 market-months where the rice price
anomaly is at least 20% and previous-month precipitation is at or below a
z-score of -1. This is a screen, not an event attribution. The same output
also shows why the topic needs controls: Kathmandu and Phidim have large 2024
price anomalies that do not line up with dry previous-month precipitation,
while Bhairahawa's April 2025 price anomaly does line up with a dry lagged
precipitation month.

## Visual QA

The heatmap rendered as a nonblank PNG and SVG. The top panel shows rice price
anomalies relative to each market's calendar-month median. The bottom panel
shows previous-month NASA POWER precipitation anomaly at the same market
coordinates. Gray price cells mark missing WFP price rows. White squares mark
the dry-price-spike screen.

What the chart makes visible:

- Price anomalies become broad and synchronized across many markets in
  2023-2025, while precipitation anomalies remain spatially and temporally
  uneven.
- Some high-price months have a local dry-precipitation lag, but others do
  not. That creates a falsifiable research question instead of a climate
  narrative.
- A national CPI view would not show which market-months have local climate
  alignment and which look more like broader market, import, currency, or
  supply-chain pressure.

## What This Does Not Mean

This is not a causal estimate of climate impacts on food prices. NASA POWER is
modeled point climate data, not a market rain-gauge observation. WFP market
coverage is uneven and has missing monthly cells. The sprint uses one
commodity and does not control for roads, storage, imports, exchange rates,
policy interventions, or national inflation.

This is also not a country ranking. It is a source-alignment test showing that
a market-month price/climate join is feasible and worth a program prospectus.

## Prospectus If Promoted

Working title:

**When Food Prices Spike, Is the Weather Local?**

First program question:

Which market-level food-price spikes in DMCs line up with local climate
anomalies, and which appear more consistent with broader market or macro
pressures that national CPI cannot separate?

First L3 tasks:

1. Pre-register commodity inclusion rules and expand beyond one rice series.
2. Compare NASA POWER precipitation with CHIRPS or another public rainfall
   source for the same market coordinates.
3. Add exchange-rate, import-price, fuel-price, and market-access falsifiers.
4. Test event windows against public drought/flood bulletins where available.
5. Build a publication visual that lets readers compare price anomaly,
   climate anomaly, and non-climate controls by market and month.
