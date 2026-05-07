# External red-team review — Grid Reliability under Heat

`attestation_chain: ai-first`. §18.4 AI synthesis. Closed 2026-04-26.

**No individual reviewer was contacted.**

## Roster

| ID | Institution | Synthesized from |
|---|---|---|
| C-1 | IEA / Ember | Annual electricity reports |
| C-2 | IRENA | Renewables capacity statistics |
| C-3 | WRI Energy | Power-plant DB methodology paper |
| C-4 | ADB Energy SD | ADB Energy Trends |

## Objections

**C-1 (IEA / Ember).** WRI v1.3.0 (2022) misses 2022–2025 solar.
IEA-Ember has more current capacity; the headline single-fuel
ranking is partly a snapshot artifact.

**C-2 (IRENA).** Hydro-dominance (BTN, NPL, TJK) is renewable.
Calling it "fragility" without specifying drought-vulnerability
mechanism conflates concepts.

**C-3 (WRI).** Plant-level data does not include actual generation;
capacity-share Herfindahl assumes all plants run at rated capacity.
Generation-share Herfindahl would shift figures.

**C-4 (ADB Energy SD).** The program name "grid reliability under
heat" requires heat-sensitive data: temperature-derated generation,
thermal-plant efficiency drop above 35°C, or hydro low-flow during
drought-summer combination. None of this is in the current artifact.

## Responses

All accepted. Article: (a) frames as "structural single-fuel
exposure," not generic fragility; (b) splits hydro/gas/coal subtypes;
(c) flags WRI 2022 vintage limit; (d) §18.5 upgrade-pass: heat-derated
reliability metric.

## §18.4 non-claim

No individual reviewer contacted.
