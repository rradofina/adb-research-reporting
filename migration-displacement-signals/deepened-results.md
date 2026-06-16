# Deepened result — emigrant stock as a share of population, not an absolute count

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 (and the §5 "question
we are most afraid to ask") with a real recomputation. Every number below is
produced by `scripts/deepen-per-population.py` from data already on disk: the
numerator is the committed program panel's `emigrant_stock_2024` (UN DESA
International Migrant Stock 2024, CC BY 3.0 IGO); the denominator is World
Bank WDI `SP.POP.TOTL` (Population, total) mid-year 2024, CC BY 4.0. No new
data, no network, no AI-supplied figures. Per CONSTITUTION.md §13.3 this is a
measurement/observability framing — what the stock matrix can and cannot
resolve about migration *intensity* — not a ranking of which DMC migrates
"too much."

Artifact: `generated/migration-per-population-deepening.{json,csv}`.

**Denominator wall-note.** WDI `SP.POP.TOTL` is not committed inside this
program's own `.cache/`. The script reads the same indicator from a sibling
program's on-disk cache (`school-heat-disruption/.cache/wdi_pop.json`, World
Bank API vintage `lastupdated 2026-04-08`). This is on-disk public data
re-read locally; there is no network call. Mirroring the pull into this
program's `.cache/` is a future tidy-up, not a number change.

## The question

The headline ranks *absolute* emigrant stock, and its top five — India,
China, Bangladesh, Afghanistan, Philippines — are five of the most populous
economies in scope. The deep question: is that a migration-intensity
finding, or mostly a population ranking that dissolves once each DMC's
emigrant stock is divided by its own population? India's 18.5M is 1.3% of its
people; Tonga's 53k is over half its resident nation. If absolute stock is
largely a population proxy, the top-5 "finding" is partly a finding about who
is big, and the per-capita cut is the real object.

## What the recomputation shows — absolute vs. share, side by side

The headline top-5 **does not survive on the share measure at all** — the
overlap between the two top-5 sets is **zero**. The same five economies that
top the absolute ranking sit between rank 6 and rank 39 once normalized:

| Absolute rank | DMC | Emigrant stock | % of population | Share rank |
|---|---|---:|---:|---:|
| 1 | India | 18,533,845 | 1.28% | #36 |
| 2 | China | 11,701,619 | 0.83% | #39 |
| 3 | Bangladesh | 8,706,947 | 5.02% | #25 |
| 4 | Afghanistan | 7,528,994 | 17.65% | #6 |
| 5 | Philippines | 6,988,383 | 6.03% | #23 |

The share ranking is an entirely different set of economies — small Pacific
and Caucasus states whose absolute counts are tiny:

| Share rank | DMC | Emigrant stock | Population (2024) | % of population | Absolute rank |
|---|---|---:|---:|---:|---:|
| 1 | Samoa | 119,313 | 218,019 | 54.73% | #27 |
| 2 | Tonga | 53,237 | 104,175 | 51.10% | #30 |
| 3 | Armenia | 637,604 | 3,033,500 | 21.02% | #20 |
| 4 | Nauru | 2,484 | 11,947 | 20.79% | #39 |
| 5 | Fiji | 181,025 | 928,784 | 19.49% | #25 |
| 6 | Afghanistan | 7,528,994 | 42,647,492 | 17.65% | #4 |
| 7 | Hong Kong SAR | 1,240,250 | 7,524,100 | 16.48% | #15 |

At the bottom of the share ranking sit precisely the large-population
economies the headline elevates: China at 0.83% of population (share-rank
#39, from absolute-rank #2) and India at 1.28% (share-rank #36, from
absolute-rank #1).

Absolute top-5: **IND, CHN, BGD, AFG, PHL**. Share top-5: **WSM, TON, ARM,
NRU, FJI**. Dropped on share: **all five** of IND, CHN, BGD, AFG, PHL.
Entered on share: WSM, TON, ARM, NRU, FJI.

## The finding — the absolute headline is largely a population ranking

Re-ranking on intensity rather than count collapses the absolute top-5
completely. Four of the five headline economies (India 1.28%, China 0.83%,
Bangladesh 5.02%, Philippines 6.03%) are at or below the panel's median share
despite topping the absolute list, because they are big, not because an
unusually large fraction of their people are abroad. The economies where
emigration is structurally largest *relative to the resident population* —
Samoa (54.7%), Tonga (51.1%), Armenia, Nauru, Fiji — are nowhere near the
absolute top-5. The absolute screen is, to first order, an index of
population size crossed with which economies keep diaspora registers, not a
measure of migration intensity.

**Afghanistan is the one partial exception, and it is the wrong kind.** It is
the single DMC that is high on *both* measures — absolute-rank #4 and
share-rank #6 (17.65% of population). But Afghanistan's 7.5M is overwhelmingly
displaced people in Iran and Pakistan, not labor migrants (see the
stock-not-flow and refugee caveats below). So the one economy whose absolute
prominence partly survives normalization survives it for a displacement
reason the metric cannot, on its own, name — which sharpens rather than
rescues the headline.

## What this does and does not settle

- **Settles:** the absolute top-5 emigrant-stock ranking is not a
  migration-intensity ranking. On emigrant stock as a share of origin
  population the set {IND, CHN, BGD, AFG, PHL} has zero members in the top
  five; it is replaced by a small-island/Caucasus ordering led by Samoa
  (54.7%) and Tonga (51.1%). The per-capita cut, not the absolute rank, is
  the object that carries a structural signal. This confirms the §1.1
  conjecture and the §5 fear directly.
- **Does not settle — stock is not a flow.** Both the numerator and the
  reordered ranking are cumulative foreign-born *stock* accumulated over
  decades, not 2024 departures. Samoa's 54.7% is a multi-generational
  diaspora (New Zealand, Australia, the US), not a current outflow rate. A
  high-share economy with a frozen diaspora and one with an active corridor
  look identical here. Separating them needs a flow series (UN DESA
  inter-vintage differencing, or national deployment registers) and is
  deferred.
- **Does not settle — refugee vs. labor conflation persists under
  normalization.** Dividing by population does nothing to separate displaced
  people from workers. Afghanistan's 17.65% share is mostly the Iran/Pakistan
  displacement footprint; Samoa's 54.7% is labor-and-family migration. The
  share metric calls both "emigrant intensity." Netting out UNHCR
  refugee/asylum stock and IOM DTM displacement is the next pass and is
  blocked only on reaching for those datasets.
- **The Afghanistan displacement caveat specifically.** Afghanistan is the
  only economy whose absolute prominence partly persists on the share
  measure. Reading that as "high labor-migration intensity" would be wrong:
  it is a humanitarian caseload expressed as a fraction of population, and it
  is the clearest case where the construct's refugee/labor merge changes the
  policy meaning of the number.
- **Honestly bounded — withheld for missing denominator.** Three DMCs have no
  `SP.POP.TOTL` value in the WDI cache and are withheld from the share
  ranking rather than placed on a fabricated denominator: Taiwan (TWN,
  emigrant stock 832,507), Cook Islands (COK, 20,288), and Niue (NIU, 4,955).
  WDI does not report population for these economies. Cook Islands and Niue
  are themselves small high-emigration Pacific states, so their absence
  *understates* how thoroughly the share ranking is dominated by small
  islands — the withheld set would, if anything, reinforce the finding, not
  reverse it.
- **Honestly bounded — denominator vintage.** Population is mid-year 2024
  WDI, matched to the UN DESA 2024 stock vintage; no DMC required the
  documented 2023 fallback. The reordering has only been tested on one
  vintage of each input; vintage stability (UN DESA 2015/2020) remains the
  separate §1.5 question.

## Reproduce

```bash
python migration-displacement-signals/scripts/deepen-per-population.py
```
