# Deep questions — Social Protection Shock Coverage

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap — whether the index observes
shock-payment capacity at all — not a ranking of which countries are
under-protected. Each question is meant to be specific enough to be
answered, falsifiable, and tied to a named public dataset, not a generic
prompt. Where a question would dissolve or transform the headline, it says
so.

---

## 0. Where the screen currently stops

The result is: five ADB DMCs — **Bangladesh, Lao PDR, Myanmar, Pakistan,
Philippines** — persistently hold the top-5 of a
`poverty × (1 − mean(SP-coverage, account-ownership))` triage product, and
that set is stable across ±50% perturbation of the single weight in that
mean (SP weight 0.25 → 0.75 in `pre-registration.md` §6). That is a
**robustness property of a ranking built from three World Bank WDI
indicators of different vintages**: ASPIRE coverage (`per_allsp.cov_pop_tot`,
fielded 2017–2022 across the set), Findex account ownership
(`FX.OWN.TOTL.ZS`, all 2021), and `$3.00/day (2021 PPP)` poverty
(`SI.POV.DDAY`, ranging 2017 for MMR to 2024 for PAK/LAO). It is not yet a
statement about whether an emergency transfer reaches a flood-displaced
household. Everything below is the distance between that and a finding —
and the program's own name, "shock coverage," is the size of that distance.

## 1. Questions that could falsify or hollow out the result

**1.1 — The dropped-leg question (the keystone).** The headline top-5 is
**not** the descending order of the gap value. The committed panel's actual
ranking by `shock_payment_readiness_gap` is PAK 18.0, **VUT 13.6**, MMR 7.1,
LAO 5.7, **TJK 3.7**, PHL 2.8, BGD 2.7. Vanuatu (the #2 value) and
Tajikistan (the #5 value) outrank Philippines and Bangladesh — yet they are
absent from the named five. The reason is in `process-sp.py` line 58:
`mean_readiness = (sp_v + acc_v)/2 if (s and a) else (sp_v if s else acc_v)`.
Vanuatu has **no Findex account figure** (`findex_account_pct: null`) so its
"readiness" is SP-coverage alone (30.4%); Tajikistan has **no ASPIRE SP
coverage** (`sp_coverage_pct: null`) so its readiness is account-ownership
alone (39.5%). **Each is scored on one leg of a two-legged index, and the
headline silently restricts the top-5 to countries with both legs present.**
So is the published five a "vulnerability cluster," or a list of *which DMCs
happen to have both indicators reported in the same WDI extract*? Re-run the
ranking imputing the missing leg (e.g. regional mean, or carry the present
leg at a documented penalty) and see whether VUT and TJK displace PHL and
BGD. This is the single question most likely to make or break the result,
and the data to answer it is already cached.

**1.2 — The Lao single-indicator question.** Lao PDR enters the top-5 with
an ASPIRE SP coverage of **2.16%** (2018) — the lowest non-null value in the
entire 43-economy panel, an order of magnitude below the next (Bhutan 8.97%,
Myanmar 13.97%). Its readiness mean is therefore dominated almost entirely
by its 37.3% Findex account figure; the SP term contributes essentially
nothing but a near-1.0 multiplier. **Is 2.16% a real coverage estimate, or
an ASPIRE harmonization artifact** (a single small survey-based program
captured, the rest of Lao social assistance invisible to the household-survey
instrument ASPIRE harmonizes)? If 2.16% is a coverage *measurement* failure
rather than a coverage *level*, Lao's rank is an observability gap wearing a
vulnerability label, and it should be flagged as not-rankable, not ranked #4.

**1.3 — The vintage-collision question.** The index averages a 2021 Findex
account number, a 2017–2022 SP coverage number, and a poverty headcount from
anywhere in 2017–2024 — then multiplies them as if they described one moment.
Myanmar is the extreme case: poverty 10.3% from **2017** (pre-COVID,
pre-coup), SP coverage 13.97% from **2017**, account ownership 47.79% from a
**2021** Findex fielded in the year of the February coup and the banking-system
freeze that followed. **Does MMR's rank survive if all three terms are forced
to the same year, or to a post-2021 vintage?** More generally: the WDI loader
(`load_wdi`, lines 38–40) takes the *most recent available year per indicator
per country* — so the cross-country comparison silently mixes years. Compute
the index on a fixed common year and report how many of the five move.

**1.4 — The redundancy question.** The index is poverty × (1 − readiness),
and across the panel poverty and readiness are almost certainly strongly
negatively correlated (rich DMCs — THA, MYS, KAZ, MNG — sit at poverty 0.0
*and* readiness ~0.9, pinning their gap to 0.0). If, conditional on the
poverty being non-trivial, readiness barely varies, then the second factor
adds nothing and the index is re-stating the `$3.00/day (2021 PPP)` poverty headcount with
extra steps. Pakistan illustrates the worry from the other side: its gap of
18.0 is roughly four times Vanuatu's (13.6) and is driven overwhelmingly by
its 23% poverty headcount, the panel's highest by a wide margin. **Plot the
gap against poverty alone for the rankable set: if the rank-order is
near-identical, the readiness layer is decoration and the program is a
poverty ranking.** Re-running the ±50% weight perturbation cannot detect
this, because that perturbation only moves SP-vs-account inside readiness — it
never tests readiness-vs-poverty.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — What does "account ownership" mechanically do in a shock?** The
honest research object is not "who has accounts" but "what makes a transfer
arrive after a flood." An account in `FX.OWN.TOTL.ZS` is a *stock* — a person
who, when surveyed in 2021, reported any account at a bank or mobile-money
provider. A shock transfer requires a *flow rail*: a payee record linked to a
live account, a funded program, and a cash-out point reachable within days.
**Can a dormant account receive an emergency G2P transfer 72 hours after a
cyclone?** Findex itself reports an "active use" cut (any deposit/withdrawal
in the past 12 months) and a "used account to receive a government transfer"
cut, both far below headline ownership in South Asia. The program uses the
headline. **What fraction of the top-5's accounts are dormant, and does the
ranking invert when readiness is built from active-use rather than
ownership?** This is the C-3 (IPA/J-PAL) objection in `review-external.md`,
accepted but never operationalized.

**2.2 — ASPIRE measures whether programs exist, not whether they surge.**
`per_allsp.cov_pop_tot` pools pensions, social assistance, and labor-market
programs into one "% of population covered" number (the C-1 WB SPJ objection).
A contributory pension paid to retirees is counted identically to a flexible
cash-transfer roster that can be topped up in a disaster — but only the second
is shock-responsive. Bangladesh's 55.6% and the Philippines' 43.0% almost
certainly bundle large non-shock components (old-age allowance; 4Ps
conditional schooling transfers that are *not* designed to scale on a flood).
**What share of each top-5 economy's ASPIRE coverage is shock-responsive in
the sense the program's name claims** — i.e. has a documented vertical/horizontal
expansion mechanism (e.g. Pakistan's BISP/Ehsaas emergency cash, the
Philippines' AICS/listahanan-triggered top-ups)? The right denominator is
adaptive-social-protection capacity, not all-SP coverage, and the two can
rank countries in opposite orders.

**2.3 — Why is Pakistan's account ownership 21% when its SP coverage is
22%?** Pakistan is the only top-5 economy where both readiness legs are
roughly equal and both are low (`findex_account_pct` 20.98, `sp_coverage_pct`
22.09). Yet BISP/Ehsaas disbursed emergency cash to ~15 million households
during COVID and the 2022 floods *through* a payment architecture (biometric
ID, agent network, mobile wallets). **If Pakistan's delivery rails demonstrably
fired at scale during the 2022 floods, why does the financial-inclusion stock
(21% accounts) score it as the least shock-ready in the panel?** Either the
account number badly understates the rail that actually exists (because BISP
pays through ID-linked instruments Findex's account question misses), or the
account number is the right unit and BISP's reach was shallower than reported.
Both cannot be true; resolving it tells us whether account ownership is the
correct measurand at all.

## 3. Questions that would make it decision-grade

**3.1 — State the estimand the name promises.** "Shock coverage" implies a
conditional probability: *given that an eligible poor household is hit by a
covariate shock, what is the probability it receives a government transfer
within N days?* The committed index estimates none of its terms — it is
`poverty-share × (1 − a static inclusion average)`. Replace the unitless
18.0 / 13.6 / 7.1 with that probability, or its closest public proxy: from
Findex's "received a government transfer into an account in the past year"
item and EM-DAT's record of which of these economies had a major flood or
cyclone in the Findex reference year, estimate the *realized* transfer-receipt
rate among the bottom-40% in shock-affected economies. That converts a ranking
into a quantity a country team can argue about.

**3.2 — Who actually bears the readiness gap — and where?** A national
coverage mean hides the only thing that matters in a shock: whether the
*poorest and most exposed* are on the roster. Pakistan's BISP penetrates parts
of Sindh and Punjab strongly while leaving Balochistan thin (the C-2 UNDP
objection, accepted, never measured). **Does the readiness gap fall hardest on
the sub-national units that are also flood/cyclone-exposed?** This needs a
join the repository can already attempt: national ASPIRE/Findex against
sub-national poverty (DHS/MICS wealth strata) and against this repo's own
flood-market-access and disaster-recovery-lag exposure layers. A household one
SP-roster gap and one cyclone away from no transfer is the real unit of
concern, and it is invisible at the 23%/22%/21% national triple.

**3.3 — The dynamics the word "shock" requires but the screen never
measures.** "Shock coverage" is inherently temporal — coverage *at the moment
of and in the weeks after* a covariate event. The index is a single static
cross-section. **Did SP coverage and G2P receipt actually rise in these five
when they were hit?** Bangladesh after Cyclone Amphan (2020) / the 2022 floods;
the Philippines after Typhoon Rai/Odette (Dec 2021) and Typhoon Haiyan
historically; Pakistan after the 2022 floods (EM-DAT dates all five economies'
major events). The static screen cannot distinguish a system that *scaled* in
a disaster from one that was merely large beforehand — yet that distinction is
the entire content of the word "shock."

## 4. Frontier questions

**4.1 — Validate against a transfer that actually fired.** The sharpest test
is external: take a documented G2P shock response with measured household-level
receipt — Pakistan's BISP COVID Emergency Cash (Ehsaas, 2020) or the 2022 flood
cash, both studied; or GiveDirectly / J-PAL G2P-disbursement evaluations in the
region — and ask whether the economies the index calls "least ready" are in
fact the ones where receipt was slowest, thinnest, or most ID-excluded. If the
index cannot retrodict a shock response we already have receipt data for, it is
not measuring readiness. The `banerjee2015multifaceted` graduation RCT in
`literature.md` establishes that small-scale transfer effectiveness is well
documented; the open question is *delivery at population scale during a
covariate shock*, which is a different object entirely.

**4.2 — The Pacific blind spot.** Of the economies most exposed to cyclones
and sea-level shocks, the panel cannot rank most of them: Samoa, Solomon
Islands, Papua New Guinea, Timor-Leste, Tuvalu, Nauru, Palau, Micronesia, Cook
Islands all have `shock_payment_readiness_gap: null`; Tonga and Fiji have a
poverty figure but no SP or account data; Vanuatu and Kiribati and the Marshall
Islands have SP coverage but **no Findex account number at all**. So the index
is structurally blind to the sub-region where climate shocks are most acute and
where remittance-financed informal insurance (this repo's remittance-resilience
program) substitutes for state SP. **Is the "top-5 readiness gap" really a
ranking of large-population Asian DMCs that survived the both-legs-present
filter, while the genuinely highest-exposure Pacific economies were dropped for
missing a Findex survey?** That is an observability gap that points the index
away from the places it most claims to serve.

**4.3 — Has readiness moved since the 2021 high-water mark?** Findex 2021 was
fielded mid-pandemic, when emergency G2P pushes spiked account opening — PMJDY
in India, GCash uptake in the Philippines (named in `review-internal.md`).
Account ownership in 2021 is therefore a *peak*, not a steady state: a portion
of those accounts were opened to receive one COVID transfer and may have gone
dormant since. **For the top-5, is the 2021 account figure a durable rail or a
pandemic spike that has partly deflated?** Only the Findex 2025 wave (TODO in
`sensitivity.md`) against the 2021 and 2017 panels can separate a structural
gain from a transient one — and if much of PHL's and BGD's readiness was
pandemic-opened dormant accounts, their already-low ranks understate the gap.

## 5. The question we are most afraid to ask

**Is `poverty × (1 − inclusion)` measuring shock-payment readiness at all, or
is it an index of which three WDI series happened to be co-populated for a
country?** The program is named "shock coverage" and measures a static
financial-inclusion *stock* plus an all-SP coverage *stock* — never the
delivery rails that fire in a shock, never a transfer that arrived, never a
date relative to a disaster. The dropped-leg artifact in §1.1 is the tell: two
of the highest-gap economies (Vanuatu, Tajikistan) are excluded from the
headline purely because one survey was missing, and an entire sub-region (the
Pacific, §4.2) is unrankable for the same reason. If you put this index in
front of the Pakistan BISP delivery team or a flood-displaced household in
Sindh and asked "does this 18.0 describe whether your emergency cash arrives?",
would they recognize it? The honest test: name the independent outcome this
index must predict — realized G2P transfer-receipt rate among the bottom-40%
in a documented EM-DAT shock — and check whether it does. If it cannot
retrodict the Pakistan 2022 flood response or the COVID Ehsaas disbursement,
it is a data-availability triage label, and it should keep that name and lose
the word "shock."

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 dropped leg | Same cached WDI panel + an imputation rule for the missing leg | yes (cached) |
| 1.2 Lao 2.16% | ASPIRE program-level decomposition (which programs feed `cov_pop_tot`) | yes |
| 1.3 vintage collision | WDI all-years series; re-run on a fixed common year | yes (cached) |
| 2.1 active use | Findex 2021 active-use + "received govt transfer to account" indicators | yes |
| 2.2 shock-responsive share | ASPIRE program-type split; national adaptive-SP / G2P program inventories | mostly |
| 3.1 estimand | Findex govt-transfer-receipt item × EM-DAT shock-year flag | yes |
| 3.2 sub-national | DHS/MICS wealth strata + this repo's flood/disaster exposure layers | mostly |
| 3.3 / 4.1 dynamics | EM-DAT event dates + national CCT admin caseload time series; BISP/Ehsaas, 4Ps studies, GiveDirectly/J-PAL G2P evaluations | mostly |
| 4.3 vintage | Findex 2025 wave vs 2021 and 2017 panels | on release |

Most of the keystone work (§1.1, §1.3) is blocked only by *not having reached
for an imputation/common-year re-run on data already cached*, not by access —
it sits in the §18.5 "upgrade-pass" pile. The genuinely external dependencies
are administrative CCT caseload series and the unreleased Findex 2025 wave.

## 7. Keystone

Answer **1.1 (the dropped-leg artifact)** first. It is the cheapest possible
test — the panel is already cached and the fix is one imputation rule in
`process-sp.py` — and it is the question that could either dissolve the
headline (if Vanuatu and Tajikistan displace Philippines and Bangladesh once
their missing leg is imputed, the "stable top-5" is an artifact of the
both-legs-present filter, not of vulnerability) or sharpen it (if the five
survive honest imputation, the claim is suddenly far stronger than "three WDI
series multiplied where all three happened to be reported"). Everything else
— active use, shock-responsive share, sub-national incidence, dynamics — is
worth more once we know the named five are not an accident of survey coverage.
