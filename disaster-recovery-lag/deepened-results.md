# Deepened result — does the top-2 survive its own falsification condition?

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.3 (and §3.2) with a real
recomputation. Every disaster number below is produced by
`scripts/deepen-metric-falsification.py` by re-aggregating the committed
EM-DAT country-profiles workbook in the program cache
(`.cache/emdat_country_profiles.xlsx`, CRED/UCLouvain, vintage 2026-04-24) —
the same source the headline uses — and is asserted equal to the committed
panel before any ranking is reported. The per-capita denominator is World Bank
WDI `SP.POP.TOTL` read from an on-disk sibling-program cache
(`climate-health-workdays/.cache/wdi_pop.json`, lastupdated 2026-04-08); that
join is labeled wherever it appears and carries a wall-note below. No new data,
no network, no AI-supplied figures. Per `CONSTITUTION.md` §6.4 these rankings
are triage, not a fragility ranking; per §13.3 the object is a
measurement/observability gap, not a country-quality ranking.

Artifact: `generated/disaster-recovery-lag-metric-falsification.{json,csv}`.

Source-readiness artifact:
`generated/disaster-recovery-lag-recovery-source-readiness.{json,csv}` plus
`generated/disaster-recovery-lag-recovery-source-readiness-events.csv`.

## The question

`results.md`, `sensitivity.md`, and `pre-registration.md` §2 claim the
disaster-burden top-2 set is `[CHN, IND]` and that it is "metric-robust"
across three metrics — events-per-year, total-affected, total-damage-USD-adj —
and they pre-register an explicit kill-condition:

> Retract if the top-2 set composition changes by ≥ 1 entry under any
> alternative metric.

The committed sensitivity matrix tested only those three metrics. It omitted
the single most-cited disaster-impact measure — **total deaths** — and the
per-capita view (**events per million population**) that `limitations.md`
already concedes "shifts the picture toward Pacific vulnerability." The deep
question: does the headline survive its own pre-registration once those two
metrics are admitted?

## What the recomputation shows

The recompute reproduces the committed panel exactly (all 38 DMCs match on
events, deaths, and affected; EM-DAT rows = 6,499, in-filter = 1,767), so the
table below shares the headline's numbers rather than competing with them.

Top-5 under each metric (the committed three, then the two omitted):

| Metric | #1 | #2 | #3 | #4 | #5 | Top-2 vs `[CHN, IND]` |
|---|---|---|---|---|---|---|
| Events / year (committed) | CHN 25.58 | **IDN 15.69** | IND 15.54 | PHL 14.85 | VNM 7.69 | **CHANGED** (IDN edges IND) |
| Total affected (committed) | CHN 1,771,174,061 | IND 1,146,651,046 | PHL 247,376,088 | BGD 181,508,696 | PAK 102,890,514 | holds |
| Total damage USD-adj (committed) | CHN 715,643,381,558 | IND 162,630,948,683 | THA 69,165,431,042 | PAK 55,559,165,731 | IDN 33,904,319,326 | holds |
| **Total deaths (deepening)** | **IDN 189,700** | **MMR 144,754** | CHN 115,612 | IND 90,743 | PAK 89,835 | **CHANGED** (CHN→#3, IND→#4) |
| **Events / million pop (deepening, WDI join)** | **TUV 414.680** | **MHL 213.061** | TON 115.191 | FSM 79.533 | VUT 79.322 | **CHANGED** (full Pacific inversion) |

Events-per-million uses 2024 WDI population (e.g. CHN 1,408,975,000; IND
1,450,935,791; IDN 283,487,931; TUV 9,646). On that axis CHN falls to 0.472
and IND to 0.278 events per million — both far below every Pacific micro-state.

## The finding — the program's own kill-condition fires

**The pre-registered falsification condition fires under three of the five
metrics.** The top-2 set is `[CHN, IND]` only on **total affected** and **total
damage** — and those are exactly the two axes the program's own critique flags
as inflated by EM-DAT double-counting of "affected" person-events and by
reporting-capacity bias in large, well-administered states. The moment a
metric is used that those two confounds do **not** inflate, the set breaks:

- **By total deaths, the top-2 is `[IDN, MMR]`** — Indonesia (189,700) and
  Myanmar (144,754, Cyclone Nargis 2008). China drops to #3 (115,612) and
  **India falls from #2 to #4** (90,743). `deep-questions.md` §1.3 *guessed*
  the deaths top-2 would be Indonesia + China; the data shows the inversion is
  larger than the agenda saw — Myanmar's single Nargis record outranks China's
  26-year total.
- **By events-per-year, the top-2 is `[CHN, IDN]`** — India is not in it at
  all; Indonesia (15.69) edges India (15.54). This was already visible in the
  committed CSV and contradicts the "metric-robust `[CHN, IND]`" claim on the
  program's own panel.
- **By events-per-million, the top-2 is `[TUV, MHL]`** — Tuvalu and the
  Marshall Islands, with the entire top-5 being Pacific micro-states. This is
  the per-capita inversion `limitations.md` anticipated, now quantified: a
  large DMC's absolute burden and a household's per-capita exposure are
  opposite rankings.

So the honest restatement is the narrow one the keystone already proposed:
**China leads ADB DMCs in recorded disaster burden 2000–2025 on the absolute
count/affected/damage axes; the #2 position is metric-dependent, and on a
deaths or per-capita axis the set is not `[CHN, IND]` at all.** The "metric-
robust top-2" headline does not survive its own pre-registration once deaths
and per-capita are admitted, and should be retired in favor of that wording.

## What this does and does not settle

- **Settles:** the pre-registered kill-condition is met. The top-2 `[CHN, IND]`
  is robust only on affected and damage, fragile on event-frequency, and
  inverted on deaths and per-capita. The claim must narrow to "China is #1 on
  absolute burden; #2 is metric-dependent."
- **Reframes, does not resolve, the affected axis:** that `[CHN, IND]` holds
  on *affected* is weak evidence, because `total_affected` sums person-events
  across 26 years (China's 1.77 B exceeds its ~1.41 B population), so it
  rewards exactly the large, repeatedly-hit, high-reporting economies — an
  **observability gap** (who records) entangled with the exposure signal, not a
  clean impact measure.
- **Bounds from EM-DAT's inclusion threshold:** EM-DAT records an event only at
  ≥10 deaths **or** ≥100 affected **or** a declared emergency/international
  appeal. Sub-threshold and slow-onset stress (atoll saltwater intrusion, king
  tides) never enter, so the Pacific per-million figures are a floor, and the
  large-state counts partly reflect denser reporting machinery rather than more
  hazard. None of the five metrics measures **recovery** — the program's named
  object — which would require post-event indicator-recovery curves joined to
  event timestamps (still unbuilt; see `deep-questions.md` §1.1 / §4.1).
- **Wall-note on the per-capita metric (per-capita was *not* fully blocked, but
  is qualified):** population is **not** in EM-DAT and **not** in this program's
  committed panel — there is no population in this program's own data lineage.
  Rather than write a population number by hand (forbidden) or omit the
  per-capita view the limitations already flag, the denominator is read from an
  on-disk WDI `SP.POP.TOTL` cache committed under a sibling program
  (`climate-health-workdays/.cache/wdi_pop.json`). It is therefore a
  **cross-program join**, and a **2024 single-year** denominator applied to a
  **2000–2025** event count. The per-million ranking is sound enough to
  demonstrate the inversion (the gaps are orders of magnitude) but is **not** a
  calibrated rate; a faithful per-capita metric would use a window-matched
  population series pinned in this program's own `versions.json`. The deaths
  metric carries no such caveat — it is computed entirely from this program's
  own EM-DAT cache.

## Source-readiness check for a true recovery-lag metric

The metric-falsification result does not answer the program's title question.
To move toward recovery lag, the pipeline now checks the source bridge that
would be needed before any post-event recovery curve can be estimated.

`scripts/audit-recovery-source-readiness.py` reads three public-source lanes:

1. The committed EM-DAT country-profiles workbook already used by the program.
2. The GDIS 1960-2018 disaster-location CSV, downloaded through the PRIO mirror
   and cross-checked against NASA CMR/SEDAC metadata pinned in `versions.json`.
3. NASA CMR metadata for Black Marble VNP46A3 monthly nighttime lights.

The result is a readiness object, not a recovery estimate:

| Source gate | What the audit finds | Publication consequence |
|---|---|---|
| Current EM-DAT cache | 1,767 ADB-DMC rows in the 2000-2025 filter, but no disaster identifier, month/day, latitude, longitude, or location field | It can support country burden screens, not event recovery curves |
| GDIS event geography | 39,953 location rows, 9,924 GDIS ids, and 9,018 `disasterno` values for 1960-2018 | It supplies a public event-geography queue through 2018 |
| Black Marble VNP46A3 | NASA CMR reports version 2 with monthly coverage starting 2012-01-01 | The feasible public pilot window is 2012-2018 |
| GDIS x Black Marble overlap | 2,881 ADB-DMC location rows, 609 unique GDIS ids, and 565 unique `disasterno` values in 27 economies | The next step is an event-level join and radiance extraction, not a headline |

The strongest immediate queue is not a country leaderboard. It is a set of
event-geography rows that can be reviewed before a satellite extraction is
attempted. The top overlap by unique `disasterno` values is China (214), India
(113), Philippines (51), Afghanistan (39), Pakistan (38), and Indonesia (33).
The top event-location rows are mostly multi-province Philippine storms and
South Asian floods, which are better candidates for a public pilot than a
single national burden rank.

The blocker is now specific. The current EM-DAT cache is aggregate
country-year-disaster-type data. A recovery-lag metric still needs either an
event-level EM-DAT table with `disasterno` and dates, or a documented public
event-date source that can join to GDIS `disasterno`, plus Black Marble
extraction over GDIS footprints or a declared affected-area proxy. Until that
exists, the honest report title remains metric falsification and source
readiness, not recovery lag.

## Reproduce

```bash
python disaster-recovery-lag/scripts/deepen-metric-falsification.py
python disaster-recovery-lag/scripts/audit-recovery-source-readiness.py
```
