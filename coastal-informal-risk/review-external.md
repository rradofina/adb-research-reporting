# External red-team review — Coastal Informal Risk

`attestation_chain: ai-first`. §18.4 AI synthesis. Closed 2026-04-26.

**No individual reviewer was contacted under §18.**

## Roster

| ID | Institution | Synthesized from |
|---|---|---|
| C-1 | UN-Habitat Global Urban Observatory | Slum measurement methodology |
| C-2 | CIESIN SEDAC LECZ team | Low-elevation coastal-zone delineation |
| C-3 | World Bank Climate Change Cross-Cutting | Coastal-risk policy framing |
| C-4 | ANU Devpolicy / Pacific small-island risk | Pacific perspective |

## Objections

**C-1 (UN-Habitat).** "Slum" definition varies by country; UN-Habitat
maintains a 5-criterion standard (water, sanitation, durable housing,
sufficient living area, secure tenure). WDI's SP.POP.SLUM.UR.ZS is a
country-reported aggregate and is sparsely available. The 10%
imputation hides this heterogeneity.

**C-2 (CIESIN).** LECZ (Low-Elevation Coastal Zone, ≤10m elevation)
is the standard exposure layer. This artifact uses country-level
coastal-yes/no instead. The §18.5 upgrade-pass should integrate
LECZ population shares.

**C-3 (WB Climate).** Coastal exposure ≠ coastal-informal risk.
Cyclone tracks, sea-level-rise scenarios, and storm-surge modeling
are needed for actionable policy framing. This is structural-
exposure only.

**C-4 (ANU Devpolicy / Pacific).** Pacific small-island states
(KIR, MHL, TUV, MDV) have entire populations in LECZ but small
absolute populations; the log-population term down-weights them.
The headline misses Pacific vulnerability.

## Responses

All accepted. Documented in limitations.md. §18.5 upgrade-pass
priorities: (a) LECZ integration; (b) Pacific small-island
sub-population analysis; (c) cyclone/storm-surge layer.

## §18.4 non-claim

No individual reviewer was contacted.
