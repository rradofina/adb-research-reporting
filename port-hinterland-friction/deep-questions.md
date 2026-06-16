# Deep questions — Port–Hinterland Friction

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the screening result did not. Per `CONSTITUTION.md` §13.3 the
framing is a measurement-and-mechanism gap — where the public data cannot
see freight friction — not a ranking of which economy moves goods badly.
Each question is meant to be specific enough to be answered, falsifiable,
and tied to a named public dataset, not a generic prompt. Where a question
would dissolve or transform the headline, it says so.

---

## 0. Where the screen currently stops

The result is: five ADB DMCs — **China, India, Indonesia, Viet Nam,
Thailand** — hold the top five positions of a
`(5 − LPI_overall) × min(sqrt(imports_B)/50, 2.0)` triage product, and that
set is stable across ±50% perturbation of the two index parameters
(the imports normalizer, 50; the imports cap, 2.0). That is a **robustness
property of a ranking of two public indicators** — a perception survey and
an import total. It is not yet a statement about ports, about hinterlands,
about transit time, or about what a corridor costs to move a container
through. Everything below is the distance between that and a finding.

Two facts about the construction bound everything that follows. First, the
LPI input is a *perception* survey of freight forwarders, not a measured
transit time or cost (`limitations.md`, C-1). Second, the program is named
"port–**hinterland** friction" but every input is a single **national**
number: there is no port, no interior, no port-to-inland corridor anywhere
in the panel. The headline measures national trade scale weighted by a
national logistics-reputation gap. It does not measure friction, and it
contains no hinterland.

## 1. Questions that could falsify or hollow out the result

**1.1 — The inert-parameter question (the keystone).** The headline's
robustness claim rests on perturbing two parameters ±50%, and the
`sensitivity.md` table reports 5/5 top-5 overlap for every one. But the
imports cap of 2.0 never binds: `min(sqrt(imports_B)/50, 2.0)` reaches 2.0
only at imports above **$10 trillion**, and the largest economy in the
panel, China, sits at $3.11 trillion → a proxy of **1.114**, nowhere near
the ceiling. Even at the lower perturbation (cap = 1.0, binding above
$2.5T) only China is truncated, and only from 1.114 to 1.0 — it stays #1 by
a margin (1.45 vs India's 0.94). **So one of the two knobs the sensitivity
test perturbs is disconnected from the output across almost its entire
tested range.** The "stable across all ±50% perturbations" headline is
partly the stability of a parameter that does nothing. Re-run the
sensitivity over parameters that actually move the index — the LPI-gap
exponent, the choice of imports vs imports/GDP, the cardinal-vs-rank
treatment of LPI — and ask whether 5/5 survives. This is the single
question most likely to deflate the robustness claim, and it needs only the
committed script.

**1.2 — The size-is-friction question.** The index is dominated by the
volume term, not the friction term. Afghanistan has the worst logistics
perception in the panel (LPI 1.9, gap 3.1) and ranks near the bottom at
0.18; China has a *mid-pack* perception (LPI 3.70, gap 1.30) and tops the
list at 1.45, purely on $3.11T of imports. The economy the index calls
most "friction-exposed" is the one with the most trade and roughly
average logistics. **Strip the volume term and rank on the LPI gap alone:
does any of {CHN, IND, IDN, VNM, THA} stay in the top five?** If the
ranking is volume wearing a friction label — the "size = friction
tautology" already flagged in `limitations.md` — then the headline is a
GDP-of-trade ranking, and UN Comtrade reproduces it directly without ever
invoking logistics.

**1.3 — The cardinal-LPI question.** The gap term `(5 − LPI)` treats LPI as
a cardinal, linear, ratio scale: it assumes the distance from 3.7 to 3.0
(China → Indonesia) means the same quantity of "friction" as the distance
from 2.6 to 1.9 (Bangladesh → Afghanistan), and that a one-point LPI move is
twice a half-point move. LPI is an aggregate of Likert-scale survey
responses; the World Bank publishes it with confidence intervals precisely
because the cardinal interpretation is fragile [@wb2023lpi]. **If `(5 − LPI)`
is replaced by the LPI rank, or by the published lower/upper-bound score,
does the top five reshuffle?** A friction index built on subtracting a
perception score from 5 is doing cardinal arithmetic on an ordinal-ish
instrument.

**1.4 — The vintage-mismatch question.** The panel multiplies 2023 imports
by LPI scores of two different vintages: most of the top five carry
LPI 2022, but Pakistan, Nepal, Brunei, Turkmenistan, Maldives, and Myanmar
carry **LPI 2018** (per `lpi_overall_year` in the panel). A 2018 logistics
perception is being multiplied by a 2023 import total. For the economies on
the 2018 score, **does the friction reading move if the missing 2023 LPI is
imputed, or if every row is forced to a common year?** The fix is to pull
the full LPI panel (2007–2023) and align vintages; until then the index
mixes a pre-pandemic perception with a post-pandemic trade volume for a
subset of the sample.

## 2. Questions about the mechanism — *why* the gap exists

**2.1 — Does perception agree with measured friction?** The whole index
rests on LPI, and LPI is what freight forwarders *say*, not what trucks and
ships *do* (`literature.md` §3, fact 1; C-1). The question that decides
whether the screen tracks anything real: **does measured transit friction
agree with the perception score?** Three public-or-licensable instruments
can adjudicate it. AIS vessel-tracking and port-call data
(UNCTAD's port-call statistics; commercial feeds such as MarineTraffic)
give measured port time-in-port and turnaround. OpenStreetMap road networks
routed through OSRM give modelled port-to-interior travel time without any
survey. The World Bank Doing Business *trading-across-borders* archive gives
documented hours and dollars to clear a border export/import. **For the top
five, do any of these correlate with LPI 3.0–3.7 — or does China's 3.70
sit alongside measured port times that tell a different story?** If
perception and measurement diverge, the index is measuring reputation, and
the divergence *is* the observability gap this program should be about.

**2.2 — Friction for whom?** A single national LPI fuses incommensurable
freight realities. Kazakhstan (LPI 2.7, index 0.39, rank 11) and Uzbekistan
(LPI 2.6, index 0.31, rank 12) are **landlocked**: their binding friction is
transit-country dependence and border-crossing delay across third
sovereigns, not a domestic port (`sensitivity.md` §18.5 TODO; C-3). China is
a coastal manufacturing hub whose friction, if any, is congestion and
inland distribution. These are different physical processes — one is a
border/transit problem, the other a throughput/distribution problem —
collapsed into one LPI value and then one index column. **Should the
landlocked DMCs (KAZ, UZB, plus AFG, BTN, NPL, TJK, KGZ, TKM, MNG, LAO) be
modelled with transit-time and border-delay data and never merged into a
coastal-port index at all?** A single "friction" number that means
"border crossings" for Uzbekistan and "container terminals" for China is two
mechanisms wearing one score.

## 3. Questions that would make it decision-grade

**3.1 — The counterfactual estimand.** Replace the unitless "friction 1.45"
with a number an ADB transport team can act on: *for a representative
container moving from the main gateway port to the largest interior
consumption center, how many days and how many dollars does friction add,
and what would closing it save per year?* Concretely, route the corridor in
OSRM over the OpenStreetMap network for measured distance and time, attach
border-dwell from the Doing Business trading-across-borders archive, and
scale by Comtrade containerized volume on that lane. That converts a
ranking into a days-and-dollars-per-corridor figure with a lever (which
segment — port, road, or border — to fix) attached. The index as it stands
has no unit; this gives it one.

**3.2 — Who bears the friction, and on which goods?** A national import
total treats a $1,000 electronics consignment and a truckload of perishable
produce as the same dollar of "trade." But friction is not linear in cargo:
a day of port or border delay is near-costless for durable manufactures and
ruinous for perishables, pharmaceuticals, and just-in-time inputs. Comtrade
gives the commodity composition of each economy's imports. **What share of
each top-five economy's trade is time-sensitive, and does the friction
that matters — perishable spoilage, demurrage, stock-out — fall on a narrow
band of goods invisible in the aggregate import total?** This decides
whether the friction is a macro trade-cost issue or a concentrated
loss borne by specific perishable and time-critical supply chains.

**3.3 — The dynamics the static screen omits.** The index is a single
cross-section: 2022/2018 LPI × 2023 imports. Friction is a process that
moves — Viet Nam's port investment, India's Sagarmala corridor build-out,
border-digitization reforms. **For the top five, has measured friction
(port turnaround from AIS, border hours from successive Doing Business
vintages, LPI across 2014–2023) been falling, flat, or rising?** An economy
whose ports are getting faster is in a different policy situation from one
stuck, and a one-year snapshot of a perception score cannot tell convergence
from stagnation — yet that distinction is what a transport-investment
decision turns on.

## 4. Frontier questions

**4.1 — Where is the hinterland? (sub-national).** The program's name
promises an interior corridor and the data contains none — this is the
deepest crack, not a footnote. A national LPI of 3.70 for China averages over
the deep-water gateway at Shanghai/Shenzhen and the interior provinces a
thousand kilometres from any port; India's 3.40 averages over JNPT and a
landlocked state in the Gangetic plain. **Build the missing layer: take the
principal container ports (gateway nodes), route to the largest interior
city/economic centers over the OpenStreetMap road and rail network via OSRM,
and compute a port-to-hinterland travel-time and -cost surface per corridor.**
That is the object the program is named for. Until it exists, every sentence
with the word "hinterland" in it describes data that is not in the panel, and
the honest title of the current artifact is "national trade-scale ×
logistics-perception gap."

**4.2 — Independent-outcome validation.** Name the independent outcome this
index would have to predict and check whether it does. Candidates, each with
a public source: realized bilateral trade cost (the ESCAP–World Bank
trade-cost database / OECD ITF figures, C-4); measured port time-in-port
(UNCTAD port-call statistics); border clearance hours (Doing Business
trading-across-borders archive); shipment-level dwell from container-tracking
or GPS truck telematics where licensable. **Does `(5 − LPI) × imports`
predict any of these out of sample — or does it predict only itself?** If
flagging China #1 tells you nothing about China's measured port turnaround or
its bilateral trade cost relative to Viet Nam's, the index is a triage label
and should keep that name (§6.4).

**4.3 — The coverage gap is the Pacific, and it is total.** Seven of fifty
DMCs are unrankable for lack of LPI or imports, and they are
overwhelmingly Pacific or transit economies: Tonga, Vanuatu, Samoa, the
Marshall Islands, Micronesia, Nauru, Palau, Kiribati, Timor-Leste, and the
Cook Islands carry **no LPI score at all**, while Fiji, Lao PDR, Papua New
Guinea, and Myanmar have an LPI but no usable 2023 imports figure (panel
`null` rows). For small-island economies, port friction — a single
under-served berth, one weekly feeder call, transshipment dependence on a
hub like Suva or Singapore — is plausibly the *most* binding logistics
constraint in the entire region, and it is exactly the set the index cannot
see. **Is the friction screen structurally blind to the economies where
port friction bites hardest, because LPI's freight-forwarder survey frame
never sampled them?** That is an observability gap, not an absence of
friction, and it should be stated as the headline limitation, not a
coverage footnote.

## 5. The question we are most afraid to ask

**Does the index measure port–hinterland friction at all, or did we build a
trade-volume ranking and name it after a corridor we never observed?** The
top five — CHN, IND, IDN, VNM, THA — is, to three significant figures, the
ranking of ADB-DMC import volume; the LPI gap only modulates the order at
the margin (it is what nudges Thailand at 0.54 below Indonesia at 0.66
despite Thailand's higher LPI). If you showed the ranking to a port
authority in Jakarta or a freight forwarder hauling from Shanghai to
Chengdu and asked "does this describe your friction?", would they recognize
it — or is it an index of *who imports the most*, dressed as an index of
*how hard it is to move goods inland*? The honest test is §4.2: name the
measured friction outcome it must predict and check out of sample. If it
predicts only import scale, the program has a name its data cannot earn,
and the fix is either to rename the artifact to what it measures or to build
the corridor layer (§4.1) that would let it measure what its name claims.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 inert parameter | committed `process-logistics.py` re-run over live parameters | yes |
| 1.2 size-vs-friction | same panel, drop volume term | yes |
| 1.4 vintage | full World Bank LPI panel 2007–2023 | yes |
| 2.1 perception vs measured | UNCTAD port-call / AIS (MarineTraffic), OSM+OSRM travel time, Doing Business trading-across-borders archive | mostly |
| 3.1 days-and-dollars | OpenStreetMap + OSRM, Doing Business border-dwell, UN Comtrade volume | mostly |
| 3.2 commodity incidence | UN Comtrade by HS commodity | yes |
| 3.3 dynamics | LPI 2014–2023 panel; successive Doing Business vintages; AIS turnaround | mostly |
| 4.1 sub-national hinterland | OpenStreetMap road/rail network + OSRM routing from gateway ports | yes |
| 4.2 outcome validation | ESCAP–World Bank trade-cost database / OECD ITF; UNCTAD port-call | yes |

Most of the keystone work is blocked only by *not having reached for the
data*, not by access: §1.1, §1.2, §1.4, §3.2, and §4.1 sit in the §18.5
"upgrade-pass" pile — the deep-research backlog — and need no credentials.
AIS/container-tracking and GPS truck telematics (§2.1, §3.3) are the
genuinely gated inputs (commercial licensing), which is why C-2's AIS
upgrade is staged, not done.

## 7. Keystone

Answer **1.1 (the inert parameter)** first, then **4.1 (build the
hinterland layer)**. 1.1 is nearly free — it re-runs the committed script —
and it tells us whether the headline's "robust across ±50%" claim is real
robustness or the stability of a knob (the $10T import cap) that the data
never reaches. 4.1 is the question the program's name has been writing a
cheque against since it was created: until a port-to-interior travel-time
surface exists from OpenStreetMap and OSRM, there is no hinterland in
"port–hinterland friction," and every other refinement is decorating a
national trade-volume ranking. Settle whether the robustness is real, then
go build the corridor the title promises.
