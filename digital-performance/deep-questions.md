# Deep questions — Digital Performance

`attestation_chain: ai-first`

This is an AI-generated research agenda for a program still at Stage 1: the
folder holds committed Ookla Speedtest SQL (`ookla-fixed-2026-q1.sql`,
`ookla-mobile-2026-q1.sql`) but no executed output, and — critically — no
official-coverage side to form a measurement gap against. So these are not
questions that hollow out a result; they are the questions that decide
whether this program is worth building, and in which form. Framing is a
measurement / observability gap per §13.3, not a country ranking.

---

## 0. Where the program currently stands

The pipeline would pull Ookla open data (median fixed and mobile
download/upload by tile), aggregate to each DMC, and flag economies below an
ITU/WHO broadband threshold. That produces a *speed ranking*. The program is
named "digital performance," but a development measurement gap is not about
how fast the connected are — it is about who is *not* connected, where, and
why. The distance between those two is the whole agenda below.

## 1. Questions that decide whether the planned screen measures anything real

**1.1 — The Ookla selection problem (the keystone, and it is severe).** A
Speedtest is run by someone who already owns a capable device, already has a
connection, and usually already suspects a problem worth testing. The median
Ookla speed is therefore conditional on *being a tester* — a population that
systematically excludes the unconnected, the rural, the prepaid-data-rationed,
and the feature-phone user: exactly the people a digital-development gap is
about. **An economy with terrible rural coverage can post a healthy median
Ookla speed precisely because its unconnected rural population never
generates a test.** Before anything else: in each DMC, what fraction of the
population lives in a tile that produced *zero* Ookla samples, and how does
that blank-tile share correlate with rurality and poverty? The silence in the
data may carry more signal than the speeds.

**1.2 — Coverage, performance, adoption, and affordability are four
different gaps — which one is this?** Ookla measures *performance,
conditional on use*. Development cares mostly about *adoption* (who is
online at all) and *affordability* (can a household pay for a usable plan).
A DMC can have fast median speeds and very low adoption. **Is the program
measuring the gap that matters, or the one the data happens to expose?**

**1.3 — There is no measurement gap without an official claim to compare
against.** The repo's whole premise (§13.3) is *measured reality minus
official/claimed coverage*. Operator and regulator coverage maps are
self-reported and widely understood to overstate real availability. **Where
is the official-coverage side?** Without an ITU/regulator coverage figure or
an operator map to difference against, this is a speed ranking, not an
observability gap — and the program's most defensible output is precisely
`claimed coverage − measured presence`.

## 2. Mechanism — what the speed number is and is not

**2.1 — Median of whom, on what device, at what time?** Ookla mixes Wi-Fi
offload, peak vs off-peak, flagship vs budget handsets, and operator
promotional periods. A "mobile" median can be dominated by tests run on
home Wi-Fi. **Does the planned aggregation separate cellular from
Wi-Fi-offloaded mobile tests, and weight by population rather than by test
count (which over-weights heavy testers in dense, well-served tiles)?**

**2.2 — The tile is not a person.** Ookla tiles are ~600 m; a tile's median
speed says nothing about how many people live there or whether they can
afford the service measured. **Joined to WorldPop, do the slow or
zero-sample tiles contain most of a DMC's population, or are they empty
land?** The population behind the gap is the unit, not the tile.

## 3. What would make it decision-grade

**3.1 — The estimand worth reporting.** Not "DMC X median = Y Mbps," but:
*how many people live where measured service falls below a usable threshold
yet official coverage claims service exists* — the population in the
claim-minus-reality gap. That is a number a regulator can be held to.

**3.2 — Affordability is the binding constraint for most of the
unconnected, and Ookla cannot see it.** The Alliance for Affordable Internet
tracks the price of a data basket as a share of income. **For the DMCs that
look "covered," what share of the population faces a usable plan costing
more than the affordability threshold — i.e. is the gap technical or
economic?** A coverage-only or speed-only program will misdiagnose an
affordability problem as solved.

## 4. Frontier

**4.1 — Triangulate the unconnected against independent layers.** Cross
Ookla blank-tiles with Meta/Facebook connectivity estimates, GSMA mobile
coverage maps, ITU adoption series, and population — the agreement and
disagreement across these is the actual observability map. **Where do
independent sources disagree most about who is online, and is that
disagreement itself the finding?**

**4.2 — Does measured digital performance predict any development outcome?**
If the speed/coverage gap correlates with nothing — not firm formalization,
not e-government uptake, not remote-service access — then it is an
infrastructure statistic, not a development one. Name the outcome it should
move.

## 5. The question we are most afraid to ask

**Is measured speed even the right construct for a *development* measurement
gap — or does this program measure the connected and name itself after the
unconnected?** The development question is "who cannot get online, where, and
why," which is an adoption–affordability–coverage question. Ookla answers
"how fast is it for those already online and equipped enough to test." If the
program ships a median-speed ranking, it will have produced a competent
statistic about the people who least need the attention, under a title that
promises the opposite. The honest test before building: can the pipeline
produce the *claim-minus-reality* population gap (§3.1), or only the speed
ranking? If only the latter, the program should either acquire the official
coverage side or be retired with that reason recorded.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 blank-tile silence | Ookla open tiles + WorldPop | yes |
| 1.3 the missing claim side | ITU coverage, regulator/operator coverage maps | partly |
| 2.2 population behind tiles | Ookla tiles + WorldPop / GHS-POP | yes |
| 3.2 affordability | Alliance for Affordable Internet basket prices, ITU | yes |
| 4.1 triangulation | Meta connectivity, GSMA, ITU adoption | partly |

## 7. Keystone

Before executing the committed SQL, settle **1.1**: compute the
zero-sample-tile population share per DMC and its correlation with rurality
and poverty. If the blank-tile share is large and skewed toward the poor,
the median-speed product is measuring the wrong population, and the program
should be rebuilt around *who is missing from the data* (joined to an
official coverage claim, §1.3) rather than how fast the present test-takers
are. That decision should be made before, not after, the pipeline runs.
