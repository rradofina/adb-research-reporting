# Deep questions — Air-Quality Monitoring Coverage

`attestation_chain: ai-first`

This is an AI-generated research agenda, not a finding. It asks the
questions the observability-gap screen did not. Per `CONSTITUTION.md` §13.3
the framing is a measurement-and-coverage gap, not a country pollution
ranking and not a country shaming. Each question is meant to be specific
enough to be answered, falsifiable, and tied to a named public dataset —
not a generic prompt. Where a question would dissolve or transform the
headline, it says so.

---

## 0. Where the screen currently stops

The result is: five ADB-region economies — Afghanistan (gap 100),
Bangladesh (100), Myanmar (95), Uzbekistan (94), Tajikistan (80) — top a
`(people-per-OpenAQ-PM2.5-monitor) × (PM2.5-exposure-above-WHO-5µg/m³)`
composite over 50 economies, using WDI national-mean PM2.5
(`EN.ATM.PM25.MC.M3`, itself DIMAQ-interpolated per [@shaddick2018data])
and an OpenAQ public-monitor snapshot dated 2026-04-23. The pre-registration
itself calls the top-5 **"stable by construction"**: the formula is
multiplicative over two bounded inputs and the 5 µg/m³ threshold is fixed,
so the §6.6 "sensitivity" is not a perturbation of parameters — it is the
admission that there are no free parameters to perturb. That is a property
of *an arithmetic combination of two public indicators*. It is not yet a
statement about whose air is unmeasured, about exposure, or about what a
monitor would buy that a satellite does not. Everything below is the
distance between that and a finding.

## 1. Questions that could falsify or hollow out the result

**1.1 — The development-confound question (the keystone).** The gap-score is
the product of two things that low-HDI economies tend to have *together*:
high PM2.5 and few public monitors. Afghanistan scores 100 on PM2.5 46.09
µg/m³ and **2** monitors; India scores only 79 on *higher* pollution (48.39
µg/m³) because it has **713** monitors; Korea and Japan, at 25.94 and 12.84
µg/m³, sit at gap 49 and 25 on 765 and 1,131 monitors. Monitor density is
itself a near-monotone function of state fiscal capacity, which is a
near-monotone function of GDP per capita and HDI (the C-4/HEI objection in
`review-external.md` concedes exactly this). **If you regress
log(people-per-monitor) on HDI and log(GDP per capita) and take the
residual, does any economy retain an *independent* monitoring deficit —
i.e. fewer monitors than its income predicts — or does the residual collapse
to noise, leaving the gap-score collinear with development?** If nothing
survives the partial, the headline is a poverty map with a PM2.5 coat of
paint, and it should say so. This is the single question most likely to
make or break the program, and HDI (UNDP) and GDP per capita (WDI) are both
public and already alignable to the 50-economy panel.

**1.2 — The two-different-populations question.** The pre-registered top-5
(AFG, BGD, MMR, UZB, TJK) and the alternative "zero-monitor + above-WHO-
guideline" set (PNG, Timor-Leste, Fiji, Brunei, Vanuatu) share **not one
member**. The first set is large, high-pollution, low-income South/Central
Asia; the second is small, low-pollution (PNG 17.31, Timor 17.41, Brunei
7.60 µg/m³), and includes a high-income economy (Brunei). These are two
unrelated phenomena the program is collapsing into one word. **Which
"observability gap" is the object of study — the under-instrumented
high-burden economy, or the wholly uninstrumented low-burden one — and does
the gap-score formula privilege the first only because PM2.5 enters
multiplicatively and the Pacific's air is relatively clean?** A single index
that ranks Afghanistan and Brunei on the same axis is answering two
questions at once and committing to neither.

**1.3 — The denominator question.** "People-per-monitor" is a raw national
count over a raw national population; it is blind to *where the monitors and
the people are*. Korea's 765 monitors and Japan's 1,131 are not why their
air is well-characterized — coverage of the populated, polluted grid cells
is. Bangladesh's 20 monitors for 173.6M (≈8.7M people per monitor) might
nonetheless cover Dhaka's exposed millions, while India's 713 might cluster
in cities and miss the rural Indo-Gangetic Plain entirely. **If the
denominator were population-weighted exposure — people living in WHO-
exceedance grid cells with no monitor within, say, 25 km — rather than a
national headcount, which DMCs move?** A monitor in an empty desert and a
monitor over ten million exposed people are one observation each under the
current metric.

**1.4 — The monitor-grade question.** The C-1/OpenAQ objection is recorded
and "accepted" but never operationalized: OpenAQ pools regulatory
reference-grade analyzers with low-cost sensors (e.g. PurpleAir-class), and
the panel's raw `pm25_locations` count makes no distinction. Nepal's **75**
and the Kyrgyz Republic's **96** locations — both higher than Bangladesh's
20 — may be dominated by low-cost sensors that cannot serve regulatory
enforcement and drift without calibration. **If the count were restricted to
reference-grade, regulatory-class monitors, how many of the 50 economies
that currently read as "monitored" revert to effectively unmonitored — and
does the apparent adequacy of Nepal or the Kyrgyz Republic survive?** A gap
score built on an undifferentiated location count may be measuring sensor
hobbyism, not regulatory observability.

## 2. Questions about the mechanism — *why* the gap exists, and whether it is a deficit at all

**2.1 — What does a ground monitor do that satellite AOD cannot?** The
program's own §18.5 upgrade-pass is ACAG-V6 satellite-derived PM2.5
([@vandonkelaar2021monthly]) — which already provides 1-km gridded PM2.5
estimates for *every* economy in the panel, including the 13 with zero
public monitors. If a published surface-PM2.5 field covers Afghanistan and
PNG alike, **in what concrete sense is there a deficit?** The defensible
answer is the set of functions a ground reference monitor performs that a
satellite column cannot: (a) legally admissible regulatory enforcement
against an air-quality standard; (b) real-time, hourly public health alerts
and AQI dissemination; (c) PM2.5 *speciation* (sulfate, nitrate, organic
carbon, black carbon) that enables source attribution; (d) calibration
ground-truth for the satellite product itself. **Which of these four
functions is the program actually claiming is missing — and is the gap a
deficit in *measurement* or a deficit in *regulatory and public-health
infrastructure* that measurement is only a proxy for?** Until that is named,
"observability gap" is doing equivocal work.

**2.2 — Is the satellite even measuring breathing-height PM2.5?** AOD (MODIS
/ MAIAC, Sentinel-5P) is a *column-integrated* optical property of the whole
atmosphere; surface PM2.5 is a mass concentration at ~1.5 m. The AOD→surface
conversion depends on the vertical aerosol profile, hygroscopic growth, and
boundary-layer height, and its error is *largest* in exactly the conditions
that dominate the top-5: high dust loading (Afghanistan, Uzbekistan,
Tajikistan, Turkmenistan), elevated smoke layers from biomass burning
(Myanmar), and the monsoon humidity of the Indo-Gangetic Plain. **For the
five headline economies, what is the documented AOD-to-surface-PM2.5
conversion error — and is the satellite "coverage" that supposedly makes the
gap moot actually trustworthy at breathing height precisely where the gap is
worst?** This cuts both ways: it weakens "AOD covers everyone" *and* it
weakens the WDI/DIMAQ exposure numbers in the same low-monitor economies,
since both lean on the satellite where ground data is thin.

## 3. Questions that would make it decision-grade

**3.1 — Does the gap predict any health or regulatory outcome?** A monitoring
gap matters only if unmeasured air is differentially *harmful* or
differentially *un-acted-upon*. Two public outcome series can test this.
First, IHME GBD gives the ambient-PM2.5-attributable death and DALY burden
per economy — **is the gap-score correlated with attributable burden after
removing PM2.5 level, or does the monitoring deficit add nothing once you
already know the pollution?** Second, the existence of a national ambient
air-quality standard and a public AQI (a coding exercise from public
regulatory records) — **do high-gap economies systematically lack
enforceable standards, which is the actual policy lever?** If the gap
predicts neither incremental burden nor regulatory absence, it is a triage
label, not a finding.

**3.2 — The avoided-imputation estimand.** Replace the unitless "gap 100"
with something an ADB country team or a statistics office can act on: *how
many people live in WHO-exceedance grid cells whose national PM2.5 figure is
currently DIMAQ-imputed rather than monitor-observed?* WDI's exposure number
for a 2-monitor economy like Afghanistan is, per [@shaddick2018data],
substantially a model output; the deliverable is the count of exposed people
whose official exposure statistic is unverifiable from the ground. That
converts a ranking into a "population whose air quality is asserted, not
measured" figure — a measurement-gap quantity in the §13.3 sense, with a
concrete remedy (sited reference monitors) attached.

**3.3 — Who actually bears the unmeasured exposure within a country?** The
gap-score is a national scalar, but the limitations file concedes WDI is a
country mean while within-country variance is "enormous (Indo-Gangetic Plain
>>> South India)." A national gap of 79 for India can hide a fully-monitored,
moderately-polluted south and an under-monitored, severely-polluted north.
**Using ACAG-V6 gridded PM2.5 crossed with WorldPop population and OpenAQ
monitor coordinates, which *sub-national* populations sit in the worst
exposure-per-monitor cells — and do they overlap across the South Asian
top-5 into a contiguous Indo-Gangetic observability gap that the national
ranking dissolves?** That is the unit a health ministry would act on, and it
is invisible at the national mean.

## 4. Frontier questions

**4.1 — Population-weighted exposure beats raw monitor count as the headline.**
The current metric multiplies people-per-monitor by an above-guideline flag;
it never weights the *exposed* population. The sharper construct: for each
economy, integrate ACAG-V6 PM2.5 over WorldPop to get population-weighted
mean exposure, then divide by reference-grade monitor count to get
*exposure-density per monitor*. **Does that reorder the 50 — pushing, say,
Indonesia (PM2.5 17.88, 35 monitors over 283M) or Pakistan (43.0, 383
monitors over 251M) up, and pulling the clean-air Pacific micro-states down
out of the conversation entirely?** This reuses two datasets the program
already names (ACAG-V6, and WorldPop is a one-line add) and would replace a
headcount ratio with an exposure-burden ratio.

**4.2 — The 14.3M figure is a PNG-and-Timor artifact.** The "~14.3M people in
zero-public-monitor economies" headline rests on 13 economies, but **PNG
(10.58M) and Timor-Leste (1.40M) alone are 12.0M of it — 83.5%, with PNG
alone at 73.7%.** The other eleven are Pacific micro-states (Tuvalu 9,646;
Nauru 11,947; Palau 17,695) plus high-income Brunei. **Is the zero-monitor
population story really a Melanesian story — two specific economies — wearing
a 13-economy regional headline, and would naming PNG and Timor-Leste
directly be both more honest and more actionable than the aggregate?** A
regional total that is 84% two countries is a composite headline in the
§6.4 sense and should not lead.

**4.3 — Has coverage moved, or is the snapshot a freeze-frame?** The monitor
count is a single 2026-04-23 OpenAQ snapshot, and the internal review flags
that the count "varies daily" and a snapshot "can mis-rank DMCs that recently
added monitors." OpenAQ exposes location first-seen timestamps. **For the
top-5, when did each public monitor come online — is Afghanistan's count of 2
a stable decade-long deficit, or a 2026 artifact of a network that is being
stood up or torn down (conflict-driven monitor loss is plausible there)?** An
economy building monitoring capacity is in a different policy situation from
one that has none, and only the time series of `pm25_locations` can tell them
apart.

## 5. The question we are most afraid to ask

**Is the gap-score measuring an observability deficit, or is it just
GDP-per-capita inverted and multiplied by dust?** The pre-registration admits
the metric is "stable by construction"; the literature concedes WDI exposure
is itself satellite-derived where monitors are absent; the external review
concedes monitor density tracks HDI. Stack those three and the uncomfortable
possibility is that the program multiplied a development indicator (monitor
count ≈ state capacity) by a partly-redundant pollution indicator (which
*also* tracks development) and recovered a development ranking — one whose
top-5 a satellite product already images at 1 km. The honest test is 1.1's
partial-out-HDI residual *plus* 3.1's out-of-sample outcome: name the thing
this index must predict that GDP per capita does not — incremental
attributable burden, regulatory absence, or unverifiable official statistics
— and check whether it does. If the residual is noise and the index predicts
nothing GDP per capita doesn't, it is an index of *development wearing the
costume of an index of measurement*, and it should keep the humbler name.

## 6. What answering these would take

| Question | Data it needs | Public? |
|---|---|---|
| 1.1 HDI partial-out (keystone) | UNDP HDI + WDI GDP per capita, joined to the 50-economy panel | yes |
| 1.3 / 4.1 pop-weighted exposure | ACAG-V6 gridded PM2.5 × WorldPop × OpenAQ coordinates | yes |
| 1.4 monitor grade | OpenAQ sensor metadata (reference vs low-cost flag) | yes |
| 2.2 AOD→surface error | MODIS/MAIAC + Sentinel-5P + ACAG-V6 validation tables | yes |
| 3.1 outcome prediction | IHME GBD ambient-PM2.5 burden; coded national AQ-standard registry | yes |
| 3.2 avoided-imputation | WDI/DIMAQ provenance + ACAG-V6 + WorldPop | yes |
| 3.3 / 4.2 sub-national | ACAG-V6 × WorldPop × monitor coordinates | yes |
| 4.3 monitor vintage | OpenAQ location first-seen timestamps | yes |

Every keystone input is public and most are already named in
`literature.md` (ACAG-V6) or trivially joinable (HDI, WorldPop, GBD). The
work is blocked by *not having reached for the data*, not by access — it
sits in the §18.5 upgrade-pass pile, which is the deep-research backlog.

## 7. Keystone

Answer **1.1 (partial out HDI / GDP per capita)** first. It is cheap — UNDP
HDI and WDI GDP per capita are public and already alignable to the existing
panel — and it is the question that could either dissolve the program (if the
monitoring deficit vanishes once development is controlled, the gap-score was
a per-capita-income proxy all along) or vindicate it (if a residual
monitoring deficit survives the partial, the finding sharpens from "two
public indicators multiplied" to "economies under-instrumented *relative to
their income* and over-exposed"). Everything else — pop-weighting,
monitor-grade, outcome prediction — is worth more once that one is settled.
