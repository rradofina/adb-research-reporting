# External red-team review — Flood Market Access

`attestation_chain: ai-first`. §18.4 AI synthesis. Closed 2026-04-26.

**No individual reviewer was contacted.**

## Roster

| ID | Institution | Synthesized from |
|---|---|---|
| C-1 | CRED EM-DAT | Threshold limitations |
| C-2 | GLOFAS / ECMWF | Modeled flood-extent methodology |
| C-3 | World Bank Rural Roads | Market-access proxy frameworks |
| C-4 | ANU Devpolicy / Pacific flood vulnerability | Per-capita exposure |

## Objections

**C-1 (CRED).** EM-DAT counts events meeting thresholds. Small
recurrent floods are under-counted. Article should note that
"flood frequency" means "qualifying-event frequency," not all flooding.

**C-2 (GLOFAS).** Modeled flood-extent (GLOFAS, FATHOM) provides
exposure layers; observed events alone undercount. §18.5 upgrade-pass.

**C-3 (WB Rural Roads).** "Market access" requires road density and
all-weather road share. WDI doesn't expose these consistently. The
current artifact uses rural-share as a coarse proxy.

**C-4 (Pacific).** Per-capita affected populations in single Pacific
flood events (e.g., 2009 PNG, 2016 FJI) exceed any large-country
share but are absorbed by the absolute-frequency metric.

## Responses

All accepted. Documented in limitations.md. §18.5 upgrade-pass:
(a) GLOFAS modeled-extent integration; (b) all-weather road density
from WB rural-roads + OSM; (c) per-capita affected as alternative
metric.

## §18.4 non-claim

No individual reviewer was contacted.
