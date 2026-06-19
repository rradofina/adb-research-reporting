# Deepened result — fuel concentration on generation, not capacity

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 with a real
recomputation. Every number below is produced by
`scripts/deepen-generation.py` from the committed WRI Global Power Plant
Database v1.3.0 (CC BY 4.0) in the program cache — the same source the
headline uses. No new data, no network, no AI-supplied figures. The
fuel-Herfindahl is a triage measure per CONSTITUTION.md §6.4, not a
reliability ranking.

Artifact: `generated/grid-generation-deepening.{json,csv}`.

## The question

The headline single-fuel cluster {BTN, BRN, NPL, MNG, TJK} is computed on
installed **capacity**, which assumes every plant runs at its nameplate.
The deep question: does the concentration survive when recomputed on what
each grid actually **generates** — or is a grid that looks single-fuel in
capacity actually diverse in dispatch (e.g. dry-season thermal backup
behind a dominant hydro fleet)?

## What the recomputation shows

The cluster **membership is stable** — the same five economies top both
rankings — but the ordering shifts and, more importantly, the
concentration *rises* on generation for almost every grid in the set:

| ISO | Herfindahl (capacity) | Herfindahl (generation) | Δ | Top fuel | Gen. coverage |
|---|---|---|---|---|---|
| BTN | 1.0000 | 1.0000 | 0.000 | Hydro | 100% |
| BRN | 1.0000 | 1.0000 | 0.000 | Gas | 100% |
| NPL | 0.9032 | 0.9403 | +0.037 | Hydro | 100% |
| MNG | 0.7971 | 0.9191 | +0.122 | Coal | 100% |
| TJK | 0.7962 | **1.0000** | **+0.204** | Hydro | 88% |
| KAZ | 0.7389 | 0.8277 | +0.089 | Coal | 100% |
| KGZ | 0.6758 | 0.8063 | +0.131 | Hydro | 99% |
| AFG | 0.6539 | 0.9146 | +0.261 | Hydro | 86% |
| BGD | 0.5959 | 0.7425 | +0.147 | Gas | 100% |

Capacity top-5: **BTN, BRN, NPL, MNG, TJK**. Generation top-5: **BTN, BRN,
TJK, NPL, MNG** (TJK rises from 5th to 3rd). Of every DMC with adequate
generation coverage, only Georgia (−0.053) and Myanmar (−0.007) become
*less* concentrated on generation; every other grid becomes *more* so.

## The finding — and it inverts the question's own guess

The deep question hypothesized that generation might **dilute** the
capacity story: dry-season thermal backup behind a hydro fleet would show
up as real fuel diversity in dispatch. The data says the opposite for the
annual figure. The secondary capacity that makes these grids look
diversified is **barely dispatched** — so what each grid actually runs on
is *more* single-fuel than what it is built with.

Tajikistan is the clean case. On capacity it is 0.80 (a large hydro fleet
plus the Dushanbe and Yavan thermal units); on 2017 generation it is a
perfect **1.0000** — the Nurek-led hydro fleet does essentially all the
generating, and the thermal units sit as idle backup that contribute
almost nothing to annual output. The "diversification" those thermal
plants imply is a capacity artifact.

So the headline's underlying concern — single-fuel exposure — is not only
real but, measured on the right variable, *stronger* than the capacity
screen reported. The screen had the right worry and the wrong variable.

## What this does and does not settle

- **Settles:** capacity over-states diversity; the corrected single-fuel
  signal is sharper, and TJK/AFG/MNG/KGZ/BGD are materially more
  concentrated in generation than the capacity panel showed.
- **Does not settle (the next frontier):** this is an *annual* 2017
  figure. The dry-season thermal dispatch the question imagined would show
  up in a **seasonal** generation split, which the annual estimate
  averages away — so the seasonal question is still open and is now the
  sharper one (a winter-only generation mix for TJK/KGZ/AFG would test
  whether the idle thermal units fire when the rivers run low).
- **Honestly bounded:** Turkmenistan (34% generation coverage) and Lao PDR
  (62%) fall below the 80% coverage floor and are withheld from the
  generation ranking rather than reported on thin data. Generation is
  WRI's reported 2017 value where available, else its modeled 2017
  estimate; the database is a 2022-vintage snapshot, so post-2022 solar is
  absent (the same limitation the capacity headline carries).

## Public reliability-proxy source check

The next source question is whether the generation-concentration screen can be
linked to a public reliability proxy before the report uses reliability
language. `scripts/audit-public-reliability-proxies.py` queries 15 World Bank
indicator endpoints: firm outage exposure and value-loss indicators,
Enterprise Survey legacy outage measures, Doing Business electricity
reliability indicators, and B-READY utility-service scores.

The result is a source-readiness object, not a reliability estimate. The audit
finds 38 ADB DMCs with at least one public reliability proxy, 22 DMCs with
both a generation-concentration result and at least one proxy, and 8 DMCs with
high generation concentration (`H >= 0.8`) plus at least one proxy. The proxy
vintages span 2009-2025. Three cataloged outage-duration or outage-count
endpoints return no usable ADB-DMC observations through the World Bank API in
this pull, which is recorded as a negative source result rather than hidden.

The bridge is useful because it narrows the next real research task: the
public data stack can crosswalk generation concentration against firm-reported
outage exposure and institutional electricity-service indicators, but it still
does not observe reserve margins, dispatch by season, outage event records, or
heat-stress curtailment. The report can therefore show a reliability-proxy
source wall, not a reliability ranking.

Artifacts:

- `generated/grid-generation-reliability-source-audit.json`
- `generated/grid-public-reliability-proxy-readiness.json`
- `generated/grid-public-reliability-proxy-readiness-country.csv`
- `generated/grid-public-reliability-proxy-readiness-indicators.csv`

## Reproduce

```bash
python grid-reliability-heat/scripts/deepen-generation.py
python grid-reliability-heat/scripts/audit-public-reliability-proxies.py
```
