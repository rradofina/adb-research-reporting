# Deep questions — Food Price–Climate Transmission

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the questions
the screening result did not. Per `CONSTITUTION.md` §13.3 the framing is a
measurement-and-attribution gap, not a country ranking and not a causal claim.
Each question is meant to be specific enough to be answered, falsifiable, and
tied to a named public dataset — not a generic prompt. Where a question would
dissolve or transform the headline, it says so. This program is unusual in the
portfolio: its original composite **failed** its own ±50% sensitivity gate
(`NEGATIVE-RESULT.md`), so the questions below are not polishing a robust
result — they are interrogating one that was reformulated to survive.

---

## 0. Where the screen currently stops

The result is: two ADB DMCs — **Lao PDR (CPI 23.1%, ag-imports 4.6% of
merchandise) and Pakistan (12.6%, 4.3%)** — sit in the top-N of *both* a WDI
general-CPI-inflation ranking and a WDI agricultural-imports-share ranking for
every N from 3 to 10; **Bangladesh (10.5%, 6.0%)** joins only from N=5 onward
(the hollow "joins from N=5" marker). That is the headline.

Two facts about how that headline was reached govern everything below. First,
the original `food_price_vulnerability` composite **did not survive ±50%
perturbation** — alternative sub-metric weights produced top-5 sets "with no
overlap" (`NEGATIVE-RESULT.md`), so the composite was abandoned and replaced by
a set-intersection that is invariant to weights *by construction*. The
intersection did not pass the robustness test; it was designed so the test
cannot apply. Second, the program is named **"transmission"** — a causal
climate→price channel — and **no climate variable enters the pipeline at all**.
The two committed indicators are general CPI and a trade ratio. The README
names CHIRPS rainfall, ERA5/TerraClimate heat, WFP subnational prices, FAOSTAT,
and the World Bank Pink Sheet; `reformulated.py` reads none of them. Everything
below is the distance between a weight-proof intersection of two non-climate
indicators and the climate-price-transmission claim on the masthead.

## 1. Questions that could falsify or hollow out the result

**1.1 — The attribution question (the keystone).** Pakistan's 12.6% CPI in
2023 was an exchange-rate event — the rupee lost roughly half its value against
the dollar — not a climate event; this is conceded in `results.md`,
`limitations.md`, and objection C-4 (WB Food Crisis Observatory). General food
CPI moves from at least six largely-separable forces: **FX pass-through** (PAK),
**fuel and freight** (2022 diesel), **war and the wheat market** (Ukraine 2022,
which dominates exactly Bangladesh's and Pakistan's import basket),
**export bans** (India's 2022–23 wheat and 2023 non-basmati rice bans hit
import-dependent neighbors directly), **subsidy and tariff changes**, and
**climate anomaly**. The committed screen — a single year's country-mean CPI —
**cannot separate any of these from any other.** So the sharp question is not
"who has high inflation and high import-dependence," it is: **for LAO, PAK, and
BGD, what share of the 2024 CPI print is even plausibly climate-attributable
once you net out the FX move (IMF IFS / central-bank rate), the Pink Sheet
energy and wheat indices, and the documented export-ban dates?** If, after
those subtractions, Pakistan's climate-attributable food inflation is near
zero, the program has placed in its top-2 a country whose headline number the
program's own name misdescribes. This is the single question most likely to
hollow the result, and every dataset to answer it is public.

**1.2 — "Transmission" with no transmission term.** The word names a mechanism:
a climate shock in period *t* shows up in prices in period *t+k*. The artifact
contains no shock, no *t+k*, and no *k* — it is a cross-sectional rank
intersection in a single vintage. **Is "transmission" defensible at all without
a climate anomaly series (SPEI or CHIRPS) on one side and a price series on the
other, joined with an explicit lag?** Until that join exists, the honest title
is *joint food-price vulnerability* (which is what `review-internal.md` and the
article already fall back to). State plainly whether the program keeps the name
or the name keeps overclaiming.

**1.3 — The lag the annual data erases.** A drought does not hit the CPI the
month it starts; it propagates through the harvest calendar — a failed monsoon
shows up in cereal prices one-to-two seasons later, and an import-dependent
country imports the price after that. IFPRI's transmission literature
([@headey2010foodprices]) and objection C-3 both say this needs **sub-annual,
commodity-level** data. The committed panel is **annual country-mean CPI** —
its time resolution is exactly the dimension on which transmission lives, and it
has none of it. **At what lag does a SPEI/CHIRPS drought anomaly co-move with
WFP monthly market prices for LAO rice or PAK wheat — one quarter, two, four —
and is that lag even estimable from annual data?** (It is not.) This is why the
sub-annual upgrade-pass in `sensitivity.md` is not a nicety; it is the
difference between the program's name and its content.

**1.4 — Lao PDR's 23.1% is a currency story too.** The anchor of the stable
pair is the single highest CPI print in the panel — but Lao PDR ran a kip
collapse and a debt-distress episode through 2022–24, with IMF and World Bank
country notes attributing the inflation largely to currency depreciation and
imported fuel, not domestic crop failure. The original panel's own
`food_production_index` for Lao PDR is **114.8** (2014–16 = 100) — food
*output* was rising. **If both members of the invariant top-2 (LAO 23.1%, PAK
12.6%) have FX-driven headline CPI and rising domestic food production, what
exactly is the "food-price" signal the intersection is detecting** — and does
"climate transmission" survive when its two anchors are currency events sitting
on top of growing harvests?

**1.5 — The redundancy / who-is-really-doing-the-work question.** Lao PDR ranks
**1st on CPI but 2nd on imports**; Pakistan 2nd and 3rd; Bangladesh **1st on
imports but only 4th on CPI**. The set survives because three countries happen
to sit high on both lists at once — but is the second axis adding information,
or are the same few high-inflation economies also the few that import a lot of
agriculture because both correlate with being a small, open, distressed economy?
Plot ag-import-share against CPI across the 36 DMCs with both values. If the
intersection is just selecting "small open economies with macro distress," the
"food-price" and "climate" labels are decoration on a generic
macro-vulnerability rank.

## 2. Questions about the measurement gap — *why* the signal is unobservable

**2.1 — Which CPI? Headline vs food vs farmgate measure different things.** The
pipeline uses WDI `FP.CPI.TOTL.ZG` — **all-items headline CPI**. Objection C-1
(FAO GIEWS) and `review-internal.md` both flag that a **food-CPI subindex** is
the targeted series, and it exists in national statistical-office releases and
in FAO's FPMA / food-price-index products. These three layers can move in
opposite directions: headline CPI can spike on fuel while food CPI is flat;
food CPI can rise on imported wheat while **farmgate** prices *fall* because
producers are squeezed. **For LAO, PAK, and BGD, how far does the food-CPI
subindex diverge from the headline CPI the screen actually used — and does the
joint qualifier survive when the correct (food) series replaces the
convenient (headline) one?** The screen is currently measuring the wrong price
because the wrong price was the one in WDI.

**2.2 — Domestic vs imported food price, the distinction the import ratio
implies but never uses.** The whole rationale for the ag-imports axis is that
import-dependent countries import world price shocks. But the CPI axis is a
*single domestic* number that blends domestically-produced staples (insulated
by local harvests, export bans, and producer subsidies) with imported staples
(exposed to Pink Sheet world prices and FX). A climate-*transmission* claim
lives entirely in the **imported** component for an import-dependent country
and in the **domestic** component for a self-sufficient one. **Can the screen
decompose any cluster member's food CPI into a domestic and an imported tradable
component (FAO FBS import shares × Pink Sheet world prices vs FAOSTAT producer
prices)** — and if it cannot, on what basis does pairing one undifferentiated
CPI with an import ratio say anything about transmission rather than coincidence?

## 3. Questions that would make it decision-grade

**3.1 — A counterfactual estimand instead of a membership flag.** Replace
"LAO and PAK are in the joint top-N" with a number a finance ministry or an ADB
country team can act on: *for a defined climate anomaly (e.g. a 1-in-10 drought,
SPEI < −1.5 over the main cropping season), how many percentage points does a
country's food CPI rise at the estimated lag, scaled by its import-dependence?*
Roughly, `estimated transmission elasticity × anomaly magnitude × tradable food
share`. That converts a binary set-membership into a stress-test figure with a
climate trigger and a price magnitude attached — which is what the name promised
in the first place.

**3.2 — Who eats the price, and does the macro number describe them?** A
country-mean food-CPI rise is a population average; the welfare incidence is not.
Food is a far larger share of the consumption basket for the bottom quintile
(commonly 50–60% in LAO/PAK/BGD per national HIES/HBS), so the *same* CPI move
is a small annoyance at the top and a calorie cut at the bottom. **Does the food
price-stress fall hardest on the poorest households (LSMS / national HIES Engel
shares), and is the cluster's "vulnerability" therefore a poverty-and-nutrition
question rather than a balance-of-payments one?** That distinction decides which
ADB instrument is even relevant.

**3.3 — The food-security outcome the screen never touches.** Objection C-2
(WFP HungerMap) and `[@wfp2024hungermap]` make the point that **joint
vulnerability ≠ a food crisis** — the actionable layer is the IPC/CH acute
food-insecurity classification and WFP's "insufficient food consumption"
nowcast. **For LAO, PAK, and BGD, does the joint-qualifier ranking line up with
the IPC phase or the share of population with insufficient food consumption — or
do high-CPI-high-import countries and high-acute-hunger countries turn out to be
largely different lists?** If the structural screen and the realized-outcome map
disagree, the screen is measuring exposure-on-paper, not hunger.

## 4. Frontier questions

**4.1 — The export-ban channel is sharper than the import ratio.** Import-share
is a slow structural stock; the violent food-price shocks of 2022–23 came from
**policy** — India's wheat-export ban (May 2022) and non-basmati-rice ban
(July 2023), Indonesia's palm-oil restriction (2022), and the Black Sea grain
disruption. These are datable events (FAO FPMA policy tracker, WTO
notifications) and they hit *exactly* the South-Asian import-dependent cluster.
**Which is the better predictor of a cluster member's food-CPI spike — its
standing ag-import ratio, or its bilateral exposure to a specific exporter's
ban?** A trade-policy-shock exposure index, built from FAOSTAT bilateral food
trade, may be a more defensible "transmission" object than either committed
axis — and it would correctly attribute 2023 to policy, not climate.

**4.2 — Subnational prices: the national mean is hiding the transmission.** The
program's own README and objection C-3 point at **WFP subnational market
prices** — and the research premise (in the README) is literally that "national
inflation hides regional pressure." Climate transmission is inherently local: a
drought in one province moves that province's market, invisibly to the national
CPI. **In a single cluster country with WFP market coverage (Pakistan and Lao
PDR both have it), do drought-anomaly grid cells (CHIRPS/SPEI) line up with the
specific markets whose prices rose** — the within-country test the
cross-country rank can never be? This is the program as originally conceived;
the national-mean panel is a retreat from it.

**4.3 — Has the gap been there for a decade, or is 2024 an FX year?** The
screen is a single 2024 vintage (and Bangladesh's import share is from **2018**
— a six-year-stale denominator paired with a 2024 CPI; see 5.1). WDI CPI runs
back decades. **Across 2010–2024, are LAO/PAK/BGD *persistently* in the joint
top-N, or did they enter it only in the 2022–24 macro-distress-and-FX window?**
A structurally exposed country is a different policy object from one that merely
had a bad currency year — and only the time series separates them. If the pair
is stable across N but unstable across *years*, the "every N from 3 to 10"
robustness is robustness on the wrong axis.

## 5. The question we are most afraid to ask

**5.1 — Is the "stable pair" a fact about food prices, or a fact about who has
two numbers?** The intersection only ranks the **36 of 50 DMCs that have both
WDI indicators in the same window**, and the gaps fall precisely where the
signal would. **Tajikistan has the 4th-highest ag-import share in the entire
panel (4.12%) — above Pakistan — but its CPI is missing, so it is excluded.
Vanuatu has the 3rd-highest CPI (11.18%) but its ag-import share is missing, so
it too is excluded.** Either could plausibly sit in the joint top-N if observed.
Bangladesh — the one that only "joins from N=5" — earns its import rank from a
**2018** figure paired with 2024 CPI. So the headline "LAO + PAK stable across
N" may be less a finding about food-price vulnerability than an artifact of
*which countries happen to have both indicators, in compatible vintages, right
now.* The honest test: re-run the intersection imputing plausible values for
Tajikistan's CPI and Vanuatu's import share (or restricting to a common vintage
year), and see whether the "stable pair" is still a pair. If it reshuffles, the
robustness across N was never the binding constraint — coverage was.

**5.2 — Did the reformulation find a signal or hide the failure?** The composite
failed ±50% because the underlying axes genuinely disagree about who is
vulnerable; the intersection is "invariant to weight choice by construction"
(`results.md`) — but invariance-by-construction is not robustness, it is
immunity to the test. **If the two axes are unstable enough that no weighted
composite of them survives ±50%, on what grounds do we trust that their
intersection is a real cluster rather than the one operation that mechanically
cannot wobble?** Name the independent outcome the joint qualifier would have to
predict — IPC phase, WFP insufficient-consumption share, or a measured
food-CPI spike at a climate lag (questions 3.3, 1.3) — and check whether it
predicts it out of sample. If it predicts nothing, the intersection is a
triage label that survived its gate by sidestepping it, and it should keep that
name and lose the word "transmission."

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 attribution | IMF IFS exchange rates + WB Pink Sheet (energy, wheat) + FAO FPMA export-ban dates | yes |
| 1.3 lag structure | CHIRPS/SPEI anomalies + WFP monthly market prices, joined at lag | yes |
| 1.4 LAO currency | IMF/WB Lao country notes + FAOSTAT food-production index | yes |
| 2.1 which CPI | FAO food price index / FPMA + national-SO food-CPI subindex | yes |
| 2.2 domestic vs imported | FAO Food Balance Sheets + Pink Sheet + FAOSTAT producer prices | yes |
| 3.2 incidence | LSMS / national HIES-HBS Engel shares | mostly |
| 3.3 hunger outcome | WFP HungerMap / IPC-CH classification | yes |
| 4.1 export-ban exposure | FAOSTAT bilateral food trade + WTO/FPMA policy tracker | yes |
| 4.2 subnational | WFP subnational prices + CHIRPS/SPEI grids (PAK, LAO) | yes |
| 5.1 coverage artifact | WDI (impute TJK CPI, VUT import share; common-vintage re-run) | yes |

Most of the keystone work is blocked only by *not having reached for the climate
and price data the README already names* — not by access. It sits in the §18.5
"upgrade-pass" pile, which for this program is unusually large because the
program currently carries a transmission claim with no transmission data.

## 7. Keystone

Answer **1.1 (attribution)** first, and do it before anything is promoted. The
program's two anchors — Lao PDR and Pakistan — both have headline CPI prints
that public sources attribute mainly to **currency collapse**, and the program
is named for **climate** transmission. Until the FX, fuel, war-wheat, and
export-ban components are netted out (all public: IMF IFS, Pink Sheet, FAO FPMA)
and a climate-attributable residual is shown to be non-trivial, the result is at
risk of placing in its top-2 two countries whose food inflation the program's
own name misdescribes. If the residual is real, the program finally earns the
word "transmission" and the sub-annual/subnational work in §1.3 and §4.2 becomes
worth doing; if it is near zero, the honest move is to rename to *joint
food-price vulnerability* and retire the causal claim. Everything else —
coverage (5.1), lag (1.3), incidence (3.2) — is worth more once attribution is
settled.
