# Deepened result — the index is a size-and-disaster-count ranking, not a market-access measure

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 and the question of §5
("is this index measuring flood-driven market isolation at all, or did we
multiply three numbers because they were the three that were public?") with a
real recomputation. Every number below is produced by
`scripts/deepen-decompose.py` from the committed program panel
`generated/flood-market-access-adb-panel.json` — re-read from disk, the same
source the headline uses. That panel is built from the EM-DAT 2000-2025 flood
subset (CRED, UCLouvain), WDI rural share (SP.RUR.TOTL.ZS), and WDI population
(SP.POP.TOTL). No new data, no network, no AI-supplied figures. Per
CONSTITUTION.md §6.4 the index is a triage measure, not a risk ranking; the
DMC framing (§13.3) is a measurement / observability gap — the index measures
what was public, not flood-driven market isolation.

Artifact: `generated/flood-decompose-deepening.{json,csv}`.

## The question

The headline `flood_market_access_index` is
`(rural_pct/100) × annual_flood_events × log10(population)`. The deep question:
none of its three factors is a road, a market, a travel time, or a flood
footprint, and two of the three are dominated by country size. Is the top-4
{IND, IDN, CHN, AFG} a market-access signal, or a ranking of large, populous
economies with many reported disasters wearing the name of a market-access
index? The decisive test is whether the top-4 survives once the size terms are
stripped out.

## What the decomposition shows

The headline index reproduces from the panel's own columns to within rounding
(max absolute error **0.03**, because `annual_flood_events` is stored at two
decimals), and the top-4 is exactly {IND, IDN, CHN, AFG}.

| ISO | rural % | population | EM-DAT flood events (2000–2025) | annual_flood_events | index (committed) | index (reproduced) | rural × floods (no size term) | index per million people |
|---|---|---|---|---|---|---|---|---|
| IND | 64.6 | 1,450,935,791 | 205 | 8.2 | 48.55 | 48.53 | 5.2972 | 0.033447 |
| IDN | 41.2 | 283,487,931 | 215 | 8.6 | 29.98 | 29.95 | 3.5432 | 0.105648 |
| CHN | 34.1 | 1,408,975,000 | 225 | 9.0 | 28.08 | 28.08 | 3.0690 | 0.019929 |
| AFG | 74.3 | 42,647,492 | 92 | 3.68 | 20.86 | 20.86 | 2.7342 | 0.489126 |
| PAK | 60.8 | 251,269,164 | 89 | 3.56 | 18.19 | 18.18 | 2.1645 | 0.072353 |

(Reproduced index and the two decomposed columns are computed by the script;
full 41-economy table in the CSV.)

**Stripping the explicit size term changes nothing.** Recomputed as
`rural_share × annual_flood_events` — dropping `log10(population)` entirely —
the top-4 is still **{IND, IDN, CHN, AFG}**, in the same order. The Spearman
rank correlation between the headline and the no-log-pop variant is **0.9974**.
This is the opposite of the keystone's first guess: removing the log-population
multiplier does *not* dissolve the big-country ranking.

**The reason is that the size dominance lives in the flood term, not the
log-pop term.** `annual_flood_events` is the raw EM-DAT qualifying-event count
divided by 25, and that count is itself a country-size variable: the five
highest are CHN (225), IDN (215), IND (205), PHL (109), AFG (92) — four of the
five largest DMCs. The index's correlation with the raw flood count is
**r = 0.94**; with `log10(population)`, **r = 0.71**; with rural share, only
**r = 0.15**. So the index tracks disaster-event count almost perfectly and
rural share almost not at all. Removing one of two collinear size channels
(log-pop) leaves the other (event count) carrying the ranking.

**Per-capita normalization is what actually breaks the big-country ranking.**
Dividing the headline index by population (per million people), the top-4
becomes **{MHL, FSM, KIR, VUT}** — Marshall Islands, Micronesia, Kiribati,
Vanuatu — and the four headline economies {IND, IDN, CHN, AFG} all drop out.
The Spearman correlation between the headline and the per-capita variant
collapses to **0.13**. A single flood event in a Pacific micro-state weighs on
a far larger *share* of its population than any of China's 225 events, exactly
as `deep-questions.md` §1.4 anticipated. The index measures national totals, so
it ranks the economies with the largest national totals.

**The flood term carries no extent, depth, or duration, and its zeros are
reporting zeros.** The term is a count of EM-DAT events meeting the inclusion
threshold (≥10 deaths or ≥100 affected). Seven economies score index **0.0**
purely because EM-DAT logged zero qualifying events, regardless of real
flood-access exposure:

| ISO | economy | rural % | EM-DAT flood events | index |
|---|---|---|---|---|
| TON | Tonga | 78.8 | 0 | 0.0 |
| TKM | Turkmenistan | 52.9 | 0 | 0.0 |
| TUV | Tuvalu | 35.3 | 0 | 0.0 |
| BRN | Brunei Darussalam | 25.1 | 0 | 0.0 |
| PLW | Palau | 20.8 | 0 | 0.0 |
| HKG | Hong Kong, China | 0.0 | 0 | 0.0 |
| NRU | Nauru | 0.0 | 0 | 0.0 |

Tonga is 78.8% rural and scores 0.0 — not because it does not flood, but
because no flood crossed EM-DAT's reporting threshold in 2000–2025. A
threshold-free observed layer (Sentinel-1 SAR, JRC Global Surface Water
seasonality) would not score these economies 0. The screen reports where
disasters are *recorded*, which below the threshold is silent.

## The finding

The `flood_market_access_index` is, on its own committed numbers, a ranking of
national disaster-event count (r = 0.94) and population — it contains no road,
no market, no travel time, and no flood footprint, and rural share, the only
"access"-adjacent term, explains almost none of the ordering (r = 0.15); strip
the size out per-capita and the top-4 {IND, IDN, CHN, AFG} is wholly replaced
by Pacific micro-states, so the index measures country size and
disaster-reporting density, not flood-driven market isolation.

## What this does and does not settle

- **Settles:** the top-4 is a size-and-event-count artifact. The explicit
  `log10(population)` term is not even the main size channel — the raw EM-DAT
  count is — so the index is *doubly* a size ranking. Rural share, the only
  term gesturing at "access," is nearly orthogonal to the result (r = 0.15).
  The zeros are EM-DAT reporting-threshold zeros, not flood-free economies.
- **Does not settle (and cannot, on this data):** whether anyone actually loses
  access to any market. That requires the object the README promised and the
  screen never built — a road graph, market points, routed travel time, and an
  observed inundation footprint — none of which is in the panel.
- **Honestly bounded:** the per-capita variant here is the *headline index per
  capita*, not a flood-affected-population rate; the panel does not carry the
  EM-DAT affected field, so the cleaner size-normalization (affected / total)
  in `deep-questions.md` §1.4 is still owed and is not computed here. The point
  the per-capita variant makes — that the ranking is size-driven — holds
  regardless.

## The data wall for the real object

The frontier object the program name claims is **population-weighted travel
time from rural settlements to the market they actually use, recomputed with
road segments cut where they cross an observed flood footprint.** The new
source-readiness script makes that wall concrete instead of speculative:
`scripts/audit-access-source-readiness.py` queries public source metadata and
emits `generated/flood-decomposition-access-source-audit.json`,
`generated/flood-access-source-readiness-sources.csv`, and a link companion.

The audit confirms that the four source families are visible but not yet
joined:

| Layer needed for a true access claim | Public-source status from the audit | Still missing |
|---|---|---|
| Road and bridge network | Geofabrik exposes 109 `.osm.pbf` links across Asia and Oceania, including 65 latest extract links | No extract downloaded, no routable graph, no bridge/edge table |
| Market locations | HDX/WFP resolves one Global Food Prices Database CSV resource, about 225.8 MB; the sampled header has market/admin/commodity/month/price fields | No full CSV pull, no coordinate fields visible in the sampled header, no market geocoding or service catchment |
| Population weights | WorldPop returns 5,221 population dataset rows; 861 rows cover all 41 economies in the flood panel; latest listed year is 2020 | No raster download, settlement weighting, or zonal statistic |
| Observed flood footprint | The Global Flood Database Earth Engine catalog exposes `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`, parses as 913 events for 2000-2018, and the NASA NRT flood-products page exposes MODIS/VIIRS flood products | No event raster, Sentinel-1/MODIS/SAR mask, or flood-edge overlay downloaded/exported |

The analysis-ready flags remain false: no road graph is built, no market points
are joined, no WorldPop grid is downloaded, no observed flood footprint is
downloaded, no road edges are cut, no travel time is routed, and no
population-weighted access-loss estimate is produced. Until those layers are
actually joined, the index should keep the name "triage label," not
"market-access measure."

## Reproduce

```bash
python flood-market-access/scripts/deepen-decompose.py
python flood-market-access/scripts/audit-access-source-readiness.py
```
