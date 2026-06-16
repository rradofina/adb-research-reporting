# Deepened result — the dropped-leg artifact: value-ranked order vs the headline five

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 (and §7) with a real
recomputation. Every number below is produced by
`scripts/deepen-include-partial.py` from the committed World Bank WDI cache —
ASPIRE social-protection coverage (`per_allsp.cov_pop_tot`), Global Findex 2021
account ownership (`FX.OWN.TOTL.ZS` [@wb2022findex]), and the `$2.15/day`
poverty headcount (`SI.POV.DDAY`), all CC BY 4.0 — re-read from the program
cache. It is the same source, the same loader (most-recent year per indicator
per economy), and the same one-legged-average formula the headline pipeline
`process-sp.py` uses. No new data, no network, no AI-supplied figures
(network was blocked; values are re-read from the committed cache identical to
the headline source). The readiness-gap is a triage measure per
CONSTITUTION.md §6.4, not a country quality ranking; per §13.3 the object here
is whether the index *observes* shock-payment capacity at all — a
measurement / observability gap, not a statement that any economy is
under-protected.

Artifact: `generated/social-protection-dropped-leg.{json,csv}`.

## The question

The headline names five DMCs — **Bangladesh, Lao PDR, Myanmar, Pakistan,
Philippines** — as the stable "top-5 shock-payment-readiness gap"
(`pre-registration.md` §1; `literature.md` §6). But that named set is **not**
the descending order of the `shock_payment_readiness_gap` value. `process-sp.py`
line 58 one-legged-averages economies that are missing a component:

```python
mean_readiness = (sp_v + acc_v) / 2 if (s and a) else (sp_v if s else acc_v)
```

An economy with only ASPIRE SP coverage (Vanuatu, no Findex account) is scored
on SP alone; an economy with only Findex account ownership (Tajikistan, no
ASPIRE coverage) is scored on account alone. The gap is still computed and the
economy still appears in the committed panel — but the published cluster of
five is silently restricted to economies that have **both** WDI legs populated.
So is the published five a "vulnerability cluster," or a list of *which DMCs
happen to have both indicators reported in the same WDI extract*? The keystone
test: recompute the full value-ranked order, and check explicitly whether
Vanuatu (~13.6) and Tajikistan (~3.7) rank above Philippines (~2.8) and
Bangladesh (~2.7) yet are excluded from the named five.

## What the recomputation shows

The top of the true value-ranked order, with the leg each economy actually has
and whether it is in the headline five (`<==`):

| Value rank | ISO | Economy | Gap | Legs present | Poverty % | SP cov % | Findex acct % | In headline five |
|---:|---|---|---:|---|---:|---:|---:|:---:|
| 1 | PAK | Pakistan | 18.0 | both | 23.0 | 22.1 | 21.0 | `<==` |
| 2 | **VUT** | **Vanuatu** | **13.6** | **sp-only** | 19.5 | 30.4 | — | excluded |
| 3 | MMR | Myanmar | 7.1 | both | 10.3 | 14.0 | 47.8 | `<==` |
| 4 | LAO | Lao PDR | 5.7 | both | 7.1 | 2.2 | 37.3 | `<==` |
| 5 | **TJK** | **Tajikistan** | **3.7** | **acc-only** | 6.1 | — | 39.5 | excluded |
| 6 | PHL | Philippines | 2.8 | both | 5.3 | 43.0 | 51.4 | `<==` |
| 7 | BGD | Bangladesh | 2.7 | both | 5.9 | 55.6 | 52.8 | `<==` |
| 8 | IDN | Indonesia | 2.2 | both | 5.4 | 65.1 | 51.8 | excluded |
| 9 | UZB | Uzbekistan | 1.8 | both | 2.7 | 25.5 | 44.1 | excluded |
| 10 | GEO | Georgia | 1.3 | both | 4.2 | 66.0 | 70.5 | excluded |

The keystone comparison is unambiguous, and reproduces the figures in
`deep-questions.md` §1.1 to the decimal:

- **VUT (13.6) > PHL (2.8): true.** VUT (13.6) > BGD (2.7): true.
- **TJK (3.7) > PHL (2.8): true.** TJK (3.7) > BGD (2.7): true.

Vanuatu is the **#2 gap value in the entire panel** and Tajikistan is the **#5**;
the two lowest-ranked named members, Philippines (#6) and Bangladesh (#7),
sit *below* both. The two economies that out-rank the lowest headline member
(BGD, gap 2.7, value-rank 7) and are nonetheless excluded are exactly the two
that are missing a leg: Vanuatu has no Findex account figure and is scored on
SP coverage alone (30.4%); Tajikistan has no ASPIRE coverage and is scored on
account ownership alone (39.5%). **Every economy excluded from the named five
that out-ranks a named member is excluded purely for missing a WDI leg.**

## The finding — the cluster is partly a completeness artifact

The headline five is **not** the five highest readiness-gap values. By the
panel's own metric the five highest are PAK, VUT, MMR, LAO, TJK — and two of
those (Vanuatu, Tajikistan) are dropped from the published cluster solely
because one of the two readiness surveys was not reported for them in the WDI
extract. The named five is therefore, in part, *the five highest-gap economies
that survived the both-legs-present filter* — a ranking of which DMCs had
**both** WDI indicators co-populated, layered on top of the vulnerability
signal.

The robustness variant settles which way it cuts. Imputing the missing leg at
the rankable-set (both-legs) mean — SP coverage 52.53%, Findex account 62.69%,
a documented imputation, not a headline — and re-ranking:

| | Imputed top-5 | Headline five |
|---|---|---|
| Members | PAK, **VUT**, MMR, LAO, **TJK** | BGD, LAO, MMR, PAK, PHL |
| Enter under imputation | **VUT, TJK** | — |
| Drop from headline five | — | **BGD, PHL** |

Under an honest imputation of the missing leg, **Vanuatu and Tajikistan
displace Philippines and Bangladesh** from the top five. The imputation even
*lowers* VUT's and TJK's gaps (VUT 13.6→10.4 because a 62.7% imputed account
leg is far above its 30.4% SP leg; TJK 3.7→3.3) — yet they still enter, because
PHL and BGD were only marginally inside the cluster to begin with. The
"stable top-5" the pre-registration certified across a ±50% weight
perturbation is stable only *because* that perturbation moves the SP-vs-account
weight inside readiness and never tests the both-legs filter (`sensitivity.md`;
`pre-registration.md` §6). The filter, not the perturbation, is doing the work
of fixing the membership at the tail.

## What this does and does not settle

- **Settles:** the named five is not the descending order of the readiness-gap
  value; two higher-gap economies (VUT #2, TJK #5) are excluded purely for a
  missing WDI leg; and under a transparent mean-imputation of that leg the
  bottom two named members (PHL, BGD) are displaced by VUT and TJK. The
  "cluster" is, at its tail, partly a ranking of WDI co-population, not of
  vulnerability.
- **Does not settle (and the imputation cannot fix):** whether a single
  imputed mean is the *right* missing-leg value. A regional mean, a present-leg
  carry at a penalty, or a model-based fill would each move VUT/TJK by
  different amounts. The point is not that the imputed numbers are correct —
  it is that the headline five is *not robust* to the existence of the missing
  legs, so the five cannot be reported as a stable vulnerability set without
  also reporting the economies the filter silently removed.
- **Bounds — the Findex-2021 pandemic vintage.** Every account leg here is the
  2021 Findex wave [@wb2022findex], fielded mid-pandemic when emergency G2P
  pushes spiked account opening; account ownership in 2021 is a high-water
  mark, not a steady state (`literature.md` §3; C-4 in `review-external.md`).
  This cuts two ways for the artifact: (a) the both-legs economies' readiness
  is, if anything, *overstated* (so their gaps understate the true gap), and
  (b) the imputed account leg for Tajikistan (39.5%) and for Vanuatu's fill
  (62.69%) inherits the same upward pandemic bias. The dropped-leg conclusion
  does not depend on the vintage — it is a statement about *which economies the
  filter keeps* — but any forward use of the gap values themselves should wait
  on the Findex 2025 wave (a standing TODO in `sensitivity.md`).
- **Out of scope here:** Lao's 2.16% single-indicator question (§1.2), the
  fixed-common-year vintage-collision re-run (§1.3), and the
  poverty-vs-readiness redundancy plot (§1.4) are separate recomputations on
  the same cache; this pass answers only the keystone (§1.1 / §7).

## Reproduce

```bash
python social-protection-shock-coverage/scripts/deepen-include-partial.py
```
