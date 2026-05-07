# Pre-registration — Migration & Displacement Signals

`attestation_chain: ai-first`

Status: **§18 AI-first frozen — 2026-04-26.**

---

## 1. Claim sentence

> Five ADB DMCs — India, China, Bangladesh, Afghanistan, Philippines —
> persistently rank in the top five emigrant-stock economies in UN DESA
> 2024, regardless of whether ranked by raw emigrant stock or by net
> migrant stock (emigrant minus immigrant). Three of the five —
> Bangladesh, Afghanistan, Philippines — concentrate over 50 percent
> of their emigration in their top-3 destination corridors; India and
> China have more diversified destination profiles.

The two-part claim is intentional: a **set-stability** finding for
the top-5 economies, plus a **corridor-concentration split** within
that set. Per Constitution §6.4 no composite-index headline; the
headline is two structural facts about the data, not a ranking.

## 2. Falsification condition

The claim is retracted if either:
- (a) The top-5 emigrant-stock set changes by more than 1 entry under
  alternative direction-of-migration definitions (raw stock, net
  stock, emigrant share of total stock).
- (b) Any of BGD, AFG, PHL has a top-3 destination share **below** 50%,
  or any of IND, CHN has a top-3 destination share **above** 50%.

## 3. Population in scope

50 ADB regional DMCs. UN DESA 2024 publishes for 44 of them; 6 are
not in the publication (some Pacific microstates).

## 4. Time window

UN DESA International Migrant Stock 2024 (vintage 2024). Earlier
vintages (2020, 2015) used as historical-stability check.

## 5. Primary metrics

- **Emigrant stock** — total persons born in DMC, currently resident
  abroad, 2024.
- **Net migrant stock** — immigrant stock minus emigrant stock, 2024.
- **Top-N destination concentration** — share of emigrant stock
  captured by the top-N destination corridors (N ∈ {2, 3, 5}).

## 6. Pre-specified arbitrary numerics

| Parameter | Value | Reason | Sensitivity range |
|---|---|---|---|
| Top-N for set claim | 5 | Convention | 3 to 8 (sets shift somewhat) |
| Top-N for corridor concentration | 3 | Standard policy framing | 2 to 5 |
| Concentration threshold | 50% | Halfway-mark heuristic | 25% to 75% |

## 7. Primary sources

UN DESA International Migrant Stock 2024 (CC BY 3.0 IGO). Pinned in
`versions.json`.

## 8. Decision rule

- **Positive**: top-5 set stable across emigrant-stock vs net-migrant
  ranking, AND the BGD/AFG/PHL > 50% and IND/CHN ≤ 50% pattern holds.
- **Mixed**: one or the other but not both.
- **Negative**: neither.

Per `sensitivity-runs.json`: top-5 set is identical across raw and net
definitions (5/5 overlap). Corridor concentrations: BGD 65%, AFG 80%,
PHL 55% (all > 50%); IND 45%, CHN 49% (both ≤ 50%). **Positive.**

## 9. Stopping rule

Stops when each in-scope DMC has UN DESA 2024 data or is documented
as not-published.

## 10. Attestation (§18)

| Field | Value |
|---|---|
| Frozen by | §18 AI-first under §18.1 |
| Date | 2026-04-26 |
| Attestation chain | `ai-first` |
| §18.5 upgrade-eligible | yes |
