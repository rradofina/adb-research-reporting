# Deepened result — the inert imports-cap parameter

`attestation_chain: ai-first`

This answers the keystone in `deep-questions.md` §1.1 with a real
recomputation. Every number below is produced by
`scripts/deepen-inert-parameter.py` from the committed World Bank LPI (via
WDI) and WDI imports (`NE.IMP.GNFS.CD`) JSON in the program cache — the same
two sources the headline uses — re-read from disk. No new data, no network,
no AI-supplied figures. The friction-exposure index is a triage measure per
CONSTITUTION.md §6.4, not a country-quality ranking; per §13.3 the framing is
an observability gap in the public freight-data layer, not a deficiency of any
economy.

Artifact: `generated/port-hinterland-inert-parameter.json`.

## The question

The headline robustness claim is that the top-5 friction set
`[CHN, IDN, IND, THA, VNM]` is "stable across all ±50% perturbations" of the
index's two parameters — the imports normalizer (50) and the imports cap (2.0)
— per `sensitivity.md` (5/5 top-5 overlap for every variant). The index is
`(5 − LPI_overall) × min(sqrt(imports_B)/50, 2.0)`. The deep question: does the
cap of 2.0 ever actually bind on any economy in the panel — or is one of the
two knobs the robustness test perturbs disconnected from the output, so that
"stable when the cap moves ±50%" is the stability of a parameter that does
nothing?

## What the recomputation shows — the cap is inert

The ceiling `min(·, 2.0)` engages only when `sqrt(imports_B)/50 ≥ 2.0`, i.e.
when imports reach **$10.0 trillion**. No ADB DMC is within a factor of three
of that. The import proxy `sqrt(imports_B)/50` for every rankable economy,
sorted by import volume:

| ISO | Economy | Imports ($B) | Proxy `sqrt(imports_B)/50` | Reaches 2.0 cap? |
|---|---|---:|---:|---|
| CHN | China | 3,106.5 | 1.1147 | no |
| IND | India | 856.7 | 0.5854 | no |
| HKG | Hong Kong SAR | 671.4 | 0.5182 | no |
| VNM | Viet Nam | 339.9 | 0.3687 | no |
| THA | Thailand | 327.0 | 0.3617 | no |
| IDN | Indonesia | 268.5 | 0.3277 | no |
| MYS | Malaysia | 255.6 | 0.3198 | no |
| PHL | Philippines | 178.2 | 0.2670 | no |
| BGD | Bangladesh | 78.0 | 0.1766 | no |
| KAZ | Kazakhstan | 72.5 | 0.1703 | no |
| PAK | Pakistan | 60.5 | 0.1556 | no |
| UZB | Uzbekistan | 42.8 | 0.1308 | no |
| KHM | Cambodia | 28.5 | 0.1068 | no |
| LKA | Sri Lanka | 19.1 | 0.0875 | no |
| GEO | Georgia | 17.8 | 0.0844 | no |
| ARM | Armenia | 15.1 | 0.0777 | no |
| KGZ | Kyrgyzstan | 14.5 | 0.0761 | no |
| NPL | Nepal | 14.2 | 0.0753 | no |
| MNG | Mongolia | 13.5 | 0.0736 | no |
| BRN | Brunei Darussalam | 9.1 | 0.0603 | no |
| AFG | Afghanistan | 8.7 | 0.0590 | no |
| TJK | Tajikistan | 5.9 | 0.0487 | no |
| TKM | Turkmenistan | 5.7 | 0.0479 | no |
| MDV | Maldives | 5.0 | 0.0447 | no |
| BTN | Bhutan | 1.6 | 0.0254 | no |
| SLB | Solomon Islands | 1.0 | 0.0198 | no |

**The maximum proxy in the panel is China's 1.1147 — against a ceiling of
2.0. Zero of 26 rankable economies reach the cap.** The recomputation
reproduces the committed panel's top-5 exactly (`[CHN, IND, IDN, VNM, THA]`,
reproduced == committed), so this is the same index, not a re-specified one.

### The headline's own ±50% cap sweep, dissected

Re-running the cap over the ±50% range `sensitivity.md` reports:

| Cap | Top-5 | Overlap with baseline | Rows the cap truncates |
|---|---|---|---|
| 1.0 | `[CHN, IND, IDN, VNM, THA]` | 5/5 | CHN only |
| 2.0 (baseline) | `[CHN, IND, IDN, VNM, THA]` | 5/5 | none |
| 3.0 | `[CHN, IND, IDN, VNM, THA]` | 5/5 | none |

Across the entire perturbation the cap touches exactly **one** row, and only
at the low end: at cap = 1.0 China's proxy is clipped from 1.1147 to 1.000 —
and China still leads by a wide margin (its index falls only from 1.45 to
1.30, against India's 0.94). At the baseline and the high end the cap touches
nothing at all. The "5/5 overlap when the cap moves ±50%" line in
`sensitivity.md` is therefore, for two of its three points, the stability of a
parameter that never engages.

### A cap that actually binds barely moves the ranking

To show the cap *cannot* change the output even when it is made to bite, the
script lowers the divisor from 50 to 25 (doubling every proxy), so China's
proxy becomes 2.2294 and the 2.0 ceiling finally engages:

- The cap now truncates China (2.2294 → 2.0), removing 0.30 from its index
  (uncapped 2.9 → capped 2.6).
- Top-5 with the binding cap: `[CHN, IND, IDN, VNM, THA]` — **5/5 overlap**
  with baseline. China still ranks #1.

So even a cap engineered to bind within the observed range leaves the top-5
unchanged: the ceiling sits so far above the gap between China and the rest
that clipping the leader cannot reshuffle the set. The perturbed cap cannot
change the output across any tested or constructed range.

## The finding — the ±50% pass is partly hollow

One of the two parameters the robustness test perturbs is **disconnected from
the output**. The imports cap is reached by no economy in the panel (max proxy
1.1147 vs ceiling 2.0), so reporting "5/5 top-5 overlap when the cap is
perturbed ±50%" credits the headline with a robustness it has not earned: it
is the trivial stability of an inert knob. The genuine robustness in
`sensitivity.md` comes only from the *other* parameter, the imports normalizer
(50). Half of the two-parameter ±50% pass is hollow.

The result also sharpens the "size = friction" concern already flagged in
`limitations.md`. The friction top-5 is close to — but **not** identical to —
the raw import-volume order:

| Rank | By friction | By raw imports |
|---|---|---|
| 1 | CHN | CHN |
| 2 | IND | IND |
| 3 | IDN | **HKG** |
| 4 | VNM | VNM |
| 5 | THA | THA |

The only difference is **Hong Kong SAR**: third by import volume ($671.4B) but
absent from the friction top-5, because its LPI of 4.0 gives it the smallest
gap term in the panel (1.0), which demotes it below Indonesia (LPI 3.0, gap
2.0). So the LPI gap does exactly one piece of real work in the ranking — it
removes the one high-volume economy whose logistics perception is strong — and
otherwise the friction order is the import-volume order. The index is
volume-dominated with a single-economy correction, not a logistics ranking.

## What this does and does not settle

- **Settles:** the imports cap (2.0) is inert across the observed range (0/26
  economies reach it; max proxy 1.1147). The "stable across ±50% perturbation
  of the two parameters" headline rests, for the cap, on a knob the data never
  reaches; a cap forced to bind still leaves the top-5 at 5/5. The remaining
  robustness is carried by the normalizer alone.
- **Does not settle (the sharper question now exposed):** robustness of the
  parameters that *do* move the index. §1.1 names three — the LPI-gap exponent,
  imports vs imports/GDP, and cardinal-vs-rank treatment of LPI (§1.3). This
  pass tested the cap; whether 5/5 survives a perturbation of those live levers
  is the open question and is now the one worth running next.
- **Honestly bounded — LPI is perception, not measurement:** the gap term
  `(5 − LPI_overall)` is built on a freight-forwarder *perception* survey
  (`limitations.md`, C-1), not a measured transit time or cost. Demoting Hong
  Kong on a perceived LPI of 4.0 is demoting it on reputation, not on observed
  port turnaround. The inert-cap finding does not rescue the index from this;
  it only shows the cap was never part of the story.
- **Honestly bounded — mixed vintages:** the proxy multiplies 2023 imports by
  LPI scores of two vintages. Most of the top-5 carry LPI 2022, but the panel
  also mixes LPI-2018 economies (Pakistan, Nepal, Brunei, Turkmenistan,
  Maldives, Myanmar) with 2023 imports (§1.4). None of those 2018-vintage rows
  is in the top-5, so the inert-cap result is unaffected by the vintage
  mismatch — but the underlying index still pairs a pre-pandemic perception
  with a post-pandemic trade volume for part of the sample.
- **Coverage:** the 26 rankable economies exclude the Pacific and several
  transit DMCs that carry no LPI or no 2023 imports (§4.3) — an observability
  gap in the public freight-data layer, restated here, not a property of those
  economies.

## 2026-06-20 source-readiness upgrade

`scripts/audit-port-source-readiness.py` keeps the inert-cap result above, then
checks the public source object needed to move beyond the imports/LPI proxy. It
writes:

- `generated/port-hinterland-source-audit.json`
- `generated/port-hinterland-source-readiness.json`
- `generated/port-hinterland-source-readiness-sources.csv`
- `generated/port-hinterland-public-logistics-signals.csv`

The audit queries public World Bank WDI metadata and latest values for 11
indicators: imports, LPI overall and five LPI components, container port
traffic, rail freight, road freight, and air freight. The generated source wall
finds 11/11 WDI metadata records reachable, 16/26 rankable rows with container
port traffic, 26/26 rankable rows with at least one public freight proxy, and
5/5 baseline top-five rows with at least one public freight proxy. The container
port traffic top five in the source wall are CHN, MYS, VNM, IND, and HKG.

This is still not a port-to-hinterland friction estimate. The generated source
wall records `analysis_ready_direct_port_performance: false`,
`analysis_ready_hinterland_travel_time: false`, and
`analysis_ready_od_network_join: false`. No port-level dwell time, turnaround
time, berth productivity, port-call delay table, port-to-inland origin-
destination network, route-impedance surface, corridor travel-time surface,
customs release-time series, trucking-cost series, rail service series, or
inland-terminal performance series is joined. Container throughput and freight
ton-kilometers are source-readiness proxies, not the headline evidence object.

## Reproduce

```bash
python port-hinterland-friction/scripts/deepen-inert-parameter.py
python port-hinterland-friction/scripts/audit-port-source-readiness.py
```
