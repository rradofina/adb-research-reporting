# Prospective design freeze

`attestation_chain: ai-first` · Prospective extension record · 2026-07-19

This design was frozen after the nine-indicator L2 hook sprint and a review of
the WDI catalogue, WDI monitoring framework, and ADB *Basic Statistics 2026*,
but before downloading or inspecting observations for the 18 additional
indicators. The nine-indicator pilot is disclosed prior information; the
expanded 9/18/27 design is prospective.

## Decision question

Does a source-relative freshness clock identify materially different review
cells than a calendar-age clock in a cross-domain WDI matrix for ADB developing
member economies?

## Unit, population, and snapshot

- Unit: one economy × indicator cell.
- Population: the repository's established 42-economy WDI-compatible ADB
  developing-member roster used in the L2 sprint.
- Snapshot: values published through reference year 2025 in API responses
  retrieved on the first accepted L3 run in 2026.
- No value is carried forward, backfilled, interpolated, or imputed.
- Missing means no non-null value through 2025 in the retrieved WDI series.

## Frozen indicator sets

The first code in each row forms the 9-indicator lower set. The first two form
the 18-indicator baseline. All three form the 27-indicator upper set.

| Domain | Core code | Baseline addition | Upper-set addition |
|---|---|---|---|
| Demography | `SP.POP.TOTL` | `SP.DYN.LE00.IN` | `SP.DYN.TFRT.IN` |
| Poverty and inequality | `SI.POV.DDAY` | `SI.POV.NAHC` | `SI.POV.GINI` |
| Health | `SH.XPD.CHEX.GD.ZS` | `SH.DYN.MORT` | `SH.STA.MMRT` |
| Education | `SE.PRM.ENRR` | `SE.SEC.ENRR` | `SE.ADT.LITR.ZS` |
| Labor and social conditions | `SL.UEM.TOTL.ZS` | `SL.TLF.CACT.ZS` | `SL.EMP.VULN.ZS` |
| Infrastructure and digital access | `EG.ELC.ACCS.ZS` | `IT.NET.USER.ZS` | `IT.CEL.SETS.P2` |
| Environment and climate | `EN.ATM.PM25.MC.M3` | `AG.LND.FRST.ZS` | `EN.ATM.CO2E.PC` |
| Economy and structure | `NY.GDP.MKTP.KD.ZG` | `NV.AGR.TOTL.ZS` | `FP.CPI.TOTL.ZG` |
| External and public finance | `BX.TRF.PWKR.DT.GD.ZS` | `NE.TRD.GNFS.ZS` | `GC.DOD.TOTL.GD.ZS` |

Codes remain in their frozen set even if sparse. A code that returns no valid
API object is reported as a source failure and cannot be silently replaced.

## Estimands

For observed economy *i*, indicator *j*, snapshot year 2026:

- `latest_year(i,j)` = latest non-null reference year through 2025.
- `global_frontier(j)` = latest non-null reference year through 2025 across
  all WDI economies in the same response.
- `calendar_age(i,j)` = `2026 - latest_year(i,j)`.
- `production_age(j)` = `2026 - global_frontier(j)`.
- `relative_lag(i,j)` = `global_frontier(j) - latest_year(i,j)`.

By construction:

`calendar_age(i,j) = production_age(j) + relative_lag(i,j)`

At threshold *k*:

- absolute review: `calendar_age >= k`;
- relative review: `relative_lag >= k`;
- production-cycle-only review: absolute review is true and relative review is
  false;
- classification disagreement: the absolute and relative review flags differ.

Missing cells are reported separately and excluded from observed-cell shares.

## Primary estimand and decision rule

The primary estimand is the share of observed baseline cells whose absolute
and relative review flags disagree at `k = 3` years.

- If the share is at least 10%, the decomposition earns continued analysis.
- If it is below 10%, the primary claim fails.
- A passing baseline is not sufficient if both the 9- and 27-indicator runs
  fall below 10%.

The 10% rule is an interpretability threshold, not an estimate of harm.

## Secondary estimands

- Share of absolute-review cells that are production-cycle-only.
- Relative-review and missing shares by policy domain.
- Median and interquartile calendar age, production age, and relative lag.
- Agreement under a DMC-only indicator frontier instead of the global WDI
  frontier.
- Coverage pattern for Pacific small-island economies versus the rest of the
  roster, reported as grouped distributions rather than country ranks.

## Sensitivity

1. Indicator-set size: 9 (−50%), 18 (baseline), and 27 (+50%).
2. Review threshold: 1.5 years (−50%), 3 years, and 4.5 years (+50%). Integer
   year data imply effective cutoffs of 2, 3, and 5 years; both the literal and
   effective rules will be printed.
3. Frontier: global WDI frontier versus ADB-DMC frontier.
4. Reference cap: 2025 baseline and a 2024 cap that removes the newest year
   before recomputing every frontier and latest cell.
5. Leave-one-domain-out: nine runs to test whether one domain creates the
   headline.

No sensitivity result may replace the primary specification as the headline.

## Source and provenance rules

- Cache one raw response per code plus ADB *Basic Statistics 2026* CSV and
  dataset metadata when licensing permits.
- Record URL, retrieval timestamp, response bytes, SHA-256, API metadata update
  date, and whether live retrieval or cache fallback was used.
- Preserve indicator source notes and source organizations.
- Every generated row records its retrieval timestamp and response hash.

## Non-claims

The matrix does not rate an economy, national statistical office, indicator
quality, or policy performance. It cannot distinguish producer delay, national
reporting delay, modeling cadence, revisions, non-applicability, or aggregator
ingestion without independent source tracing. Missing is not stale; old is not
wrong; relative-to-frontier is not on-time against a formal release standard.

## Falsification and stopping rules

- Retract the primary claim if disagreement is below 10% in the baseline and
  both set-size sensitivities.
- Publish indicator-selection instability instead if the baseline passes but
  the lower and upper sets point in opposite directions around the threshold.
- Stop before article production if more than half of the baseline codes fail
  retrieval or fewer than half of possible baseline cells are observed.
- Reshape to a source-coverage result if missingness, rather than clock
  disagreement, is the only stable pattern.
- Do not take a third pass at a failed source. A new pass must name a previously
  unchecked object that could change the claim.

## AI-first freeze

| Field | Value |
|---|---|
| Frozen by | §18 AI-first under `CONSTITUTION.md` §18.1 |
| Date frozen | 2026-07-19, before the first expanded L3 pipeline run |
| Prior information | Nine-indicator L2 sprint completed 2026-06-19 and disclosed above |
| Freeze commit | The commit containing this file; resolve with `git log -- public-data-freshness/pre-registration.md` |
| First testable claim | At least 10% of observed baseline cells change review status under the source-relative clock. |
| Falsification condition | Below 10% in baseline and both set-size sensitivity runs, or failure of the minimum retrieval/coverage rules. |
| Attestation chain | `ai-first` |

Later results may report whether these rules passed, but may not rewrite them
without preserving this version as superseded.
