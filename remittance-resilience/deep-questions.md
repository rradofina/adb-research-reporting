# Deep questions — Remittance Resilience

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap, not a country ranking. Each
question is meant to be specific enough to be answered, falsifiable, and
tied to a named public dataset — not a generic prompt. Where a question
would dissolve or transform the headline, it says so.

Status update, 2026-06-17: question 1.1 has now been partially answered with
the public World Bank/KNOMAD 2021 bilateral remittance matrix in
`flow-weighting-l3-module.md`. The same five-economy set survives, but order
changes and low matched-flow coverage remain central caveats. This file
remains the broader research agenda, not the current result record.

---

## 0. Where the screen currently stops

The result is: five economies — Kyrgyz Republic, Nepal, Tonga, Vanuatu,
Samoa — sit in the top five of a `dependence (% GDP) × mean corridor cost`
triage product, and that set is stable across ±50% perturbation of the two
cap parameters. That is a **robustness property of a ranking of two public
indicators**. It is not yet a statement about households, about resilience,
or about what anyone should do. Everything below is the distance between
that and a finding.

## 1. Questions that could falsify or hollow out the result

**1.1 — The volume-weighting question (the keystone).** RPW gives every
corridor equal weight; the cluster ranks on a *destination-mean* cost. For
the Kyrgyz Republic the Russia→Kyrgyz corridor — cheap (~2–3%) because of
EAEU banking integration and dense MTO competition — almost certainly
carries the dominant share of actual flow, while the 10.5% mean is pulled
up by thin, low-volume corridors that few people use. **If we reweight each
economy's mean cost by IMF bilateral remittance / DOTS-style flow shares,
does the Kyrgyz Republic stay in the top five at all — and does the whole
cluster reshuffle?** A fragility index built on equal-weighted corridors is
treating a $5M corridor and a $2B corridor as one observation each. This is
the single question most likely to make or break the result, and the data
to answer it is public.

**1.2 — The negative-cost question.** The committed panel contains negative
transfer costs: Tonga's corridor minimum is −3.0%, Nepal's −76%, Pakistan's
−305%, the Philippines' −201%. These are promotional pricing, FX-spread
quirks, and outliers in the RPW quote set. How many of each cluster
economy's observations are negative, sub-1%, or implausibly extreme? **If
the destination mean is sensitive to a handful of promotional or outlier
quotes, is the mean a meaningful central tendency at all — or should the
screen use a volume-weighted median of realized prices?** Re-run the ranking
on a trimmed/median cost and see who moves.

**1.3 — The small-sample question.** Tonga, Vanuatu, and Samoa each rest on
two observed corridors; the Kyrgyz Republic on one. A "mean cost" over one
or two corridors has no sampling distribution worth the name. If the claim
were restricted to economies with ≥10 corridor observations — or if each
mean carried a bootstrap interval — **how many of the five cluster members
survive?** Is the cluster substantially an artifact of *which economies
happen to have thin RPW coverage*, i.e. an observability gap masquerading as
a vulnerability signal?

**1.4 — The redundancy question.** Dependence and cost are reported as
weakly negatively correlated (Pearson −0.22). Among the high-dependence
economies specifically, is cost actually informative, or does almost
everyone cluster at similar cost so that the second axis adds nothing the
first did not? Plot the conditional distribution of cost within the top
dependence decile. If cost carries no independent signal there, the "joint"
screen is re-stating dependence.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — What market structure produces a high corridor cost?** The honest
research object is not "who is expensive" but "what makes a corridor
expensive." Candidate mechanisms differ sharply across the cluster:
correspondent-banking withdrawal and AML de-risking that thinned Pacific
corridors; a small number of licensed MTOs in a tiny market (Tonga, Samoa,
Vanuatu); regulatory and licensing barriers; and corridor volume itself
(fixed costs spread over few transfers). **Which mechanism dominates for the
Pacific three, and which for the Central Asian two?** They are almost
certainly different stories wearing the same index value, and a single
"fragility" number hides that.

**2.2 — Does a high formal cost measure a price no one pays?** KNOMAD
flags informal channels (hawala / hundi / undocumented MTO use) as the
substitute when formal cost is high, concentrated in exactly the GCC→South
Asia and Russia→Central Asia corridors in this set. If high formal cost
*causes* informal substitution, the published cost is the price of a channel
households have already abandoned. **What share of inbound flow to Nepal,
the Kyrgyz Republic, and Pakistan is estimated to move informally — and does
the formal-cost ranking invert once you weight by the channel people
actually use?**

## 3. Questions that would make it decision-grade

**3.1 — The counterfactual estimand.** Replace the unitless "fragility 70.3"
with a number a finance ministry or an ADB country team can act on: *if SDG
10.c.1's 3% target were met on each cluster economy's actual corridors, how
many dollars per year stay with receiving households?* Roughly,
`dependence%GDP × GDP × (current cost − 3%) × formal share`. That converts a
ranking into an avoided-cost figure with a policy lever attached.

**3.2 — Who actually bears the cost?** Country %GDP is a macro ratio; IZA
work finds the top decile of receiving households captures 50–70% of
remittance income. Two opposite welfare stories are consistent with the same
country number. Because RPW cost is dominated by *fixed* fees, the per-unit
cost is worst for the smallest, most frequent transfers — the poorest
senders. **Does the cost burden fall hardest on low-value senders, and is
the cluster's "fragility" therefore regressive within the country?** That is
the question that decides whether this is a poverty issue or a
balance-of-payments issue.

**3.3 — The resilience the name promises but the screen never measures.**
"Resilience" implies dynamics: do inflows *rise* when the receiving economy
is hit (consumption-smoothing insurance), or *fall* when the sending economy
is hit (imported shock)? Did Tongan inflows spike after the 2022 eruption
and cyclones; did Nepal's after the 2015 earthquake? **Are these five
economies remittance-*insured* or remittance-*exposed* — and is it the same
answer for all five?** The static screen cannot tell counter-cyclical
insurance from co-movement risk, yet that distinction is the whole point of
the word "resilience."

## 4. Frontier questions

**4.1 — Single-sender concentration is the sharper fragility.** The Kyrgyz
Republic and Tajikistan are extraordinarily exposed to one sending economy
(Russia); the Pacific three to a handful (Australia, New Zealand, the US).
Compute a Herfindahl index of each economy's inflows by source corridor
(the migration-displacement-signals program holds the bilateral stocks
needed for this). **Who is one sending-economy shock — a ruble collapse, a
recession in the Gulf, an AML-driven corridor closure — away from a
remittance cliff?** That is a more defensible "fragility" than dependence ×
cost, and it reuses data already in this repository.

**4.2 — Sub-national dependence.** Remittance dependence is concentrated in
specific origin communities — Nepal's hill districts, particular provinces,
not the capital. Which sub-national units carry the dependence, and do they
overlap with the places that are also climate- or disaster-exposed (a
cross-program join with disaster-recovery-lag and flood-market-access)? A
household one remittance-corridor shock and one cyclone away from collapse is
the real unit of concern, and it is invisible at the national mean.

**4.3 — Has the cost been stuck for a decade?** RPW is a 2011–2025 panel,
but the screen uses a single Q1 2025 snapshot. For each cluster corridor,
has cost trended toward 3% or stalled above 5% for ten years? An economy
converging is in a different policy situation from one that is structurally
stuck, and only the time series can tell them apart.

## 5. The question we are most afraid to ask

**Is `dependence × cost` measuring anything real, or is it a quantity we
constructed because both numbers happened to be public?** If you put the
fragility index in front of the Nepal Rastra Bank research desk or a Tongan
remittance-receiving household and asked "does this product describe your
risk?", would they recognize it — or is it an index of *data availability*
wearing the costume of an index of *vulnerability*? The honest test: name
the independent outcome this index would have to predict — household
consumption volatility, poverty transitions during a corridor shock,
take-up of informal channels — and check whether it does. If it predicts
nothing out of sample, it is a triage label, and it should keep that name.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 volume-weight | IMF bilateral remittance matrix / DOTS, or central-bank corridor flow | yes |
| 1.2 negative costs | RPW full quote-level set (already cached) | yes |
| 2.2 informal share | KNOMAD Migration & Development Brief estimates | yes |
| 3.1 counterfactual | RPW + WDI GDP (already in panel) | yes |
| 3.2 incidence | LSMS / DHS household microdata | mostly |
| 3.3 resilience | RPW/WDI time series + disaster dates (EM-DAT) | yes |
| 4.1 sender Herfindahl | bilateral migration stocks (this repo's migration program) | yes |

Most of the keystone work is blocked only by *not having reached for the
data*, not by access — it sits in the §18.5 "upgrade-pass" pile, which is
really the deep-research backlog.

## 7. Keystone

Answer **1.1 (volume-weighting)** first. It is cheap — the IMF bilateral
data is public — and it is the question that could either dissolve the
cluster (if equal-weighting was doing the work) or vindicate it (if the
cluster survives flow-weighting, the finding is suddenly far stronger than
"two public indicators multiplied"). Everything else is worth more once that
one is settled.
