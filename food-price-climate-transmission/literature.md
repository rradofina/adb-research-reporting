# Literature review — Food Price Climate Transmission

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27.

## 1. Search record

Queries (2026-04-27):
1. `Headey Fan IFPRI food price crisis transmission`
2. `WFP HungerMap LIVE food insecurity`
3. `climate-CPI transmission commodity LMIC`
4. `food-CPI subindex WDI alternative`

Tier-A: *American Journal of Agricultural Economics*, *Food Policy*,
*Global Food Security*. Tier-B: IFPRI, WFP, FAO GIEWS, World
Bank Food Crisis Observatory. Tier-C: ADB food-security briefs.

## 2. Verified entries

- **`headey2010foodprices`** — Headey & Fan (2010). Reflections
  on the global food crisis. *IFPRI Research Monograph 165*.
  **Foundational food-price-shock review.**
- **`wfp2024hungermap`** — WFP HungerMap LIVE. **Real-time
  food-insecurity dashboard; alternative source.**

## 3. Synthesis

1. **Joint inflation × import-dependence is a reasonable
   triage proxy** for food-price vulnerability
   [@headey2010foodprices]; the IFPRI review documents
   transmission mechanisms.
2. **Real-time food-insecurity classification (WFP IPC)**
   [@wfp2024hungermap] is the actionable layer; this artifact
   is structural-vulnerability only.
3. **The original composite-index formulation failed the ±50%
   sensitivity gate** (alternative weights produce different
   top-5 sets). Reformulated to set-based joint qualifier.

## 4. Gap

No published cross-ADB-DMC top-N joint-vulnerability set claim
that survives weight-choice perturbation. The set-intersection
formulation is the marginal contribution.

## 5. First testable claim

> Two ADB DMCs — Lao PDR and Pakistan — sit in the top-N of both
> WDI CPI inflation AND ag-imports-share-of-merchandise for every
> N from 3 to 10. Bangladesh joins from N=5.

## 7. §18 attestation

`ai-first`. 2026-04-27. Reformulation; original composite failed
gate (documented in `NEGATIVE-RESULT.md`).
