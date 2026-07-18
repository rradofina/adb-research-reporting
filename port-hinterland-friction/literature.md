# Literature review — Port-Hinterland Friction

`attestation_chain: ai-first`. §18 AI-finalized 2026-04-27; construct-validation correction 2026-07-18.

## 1. Search record

Queries (2026-04-26):
1. `World Bank Logistics Performance Index 2023 methodology`
2. `UNCTAD Review of Maritime Transport 2024 ADB region`
3. `port hinterland landlocked transit-country dependence`
4. `bilateral trade cost OECD ITF`

Tier-A: *World Bank Economic Review*, *Journal of Transport Geography*,
*Maritime Economics & Logistics*. Tier-B: WB Connecting to Compete
biennial reports, UNCTAD RMT, OECD International Transport Forum,
ADBI Trade & Logistics. Tier-C: ADB regional transport briefs.

## 2. Verified entries

- **`wb2023lpi`** — World Bank LPI 2023 report (Connecting to
  Compete). **Primary perception-based survey of logistics
  performance. Cited with the explicit perception-vs-measured
  caveat.**
- **`unctad2024rmt`** — UNCTAD Review of Maritime Transport 2024.
  **§18.5 upgrade-pass source for direct port-throughput and
  vessel-tracking measurement.**
- **`worldbank2025cppi`** — World Bank CPPI standardized 2020–2025
  annex and methodology. **Observed port-level vessel-time object used
  to test the inherited national proxy.**
- **`worldbank2026lpi2`** — World Bank LPI 2.0 methodology. **Names the
  2023–2024 shipment indicators needed for the port-to-inland upgrade;
  the underlying file is not yet joined.**

## 3. Synthesis

Three evidence boundaries:

1. **LPI is perception-based, not measured.** Surveys logistics
   experts on country-level perceptions [@wb2023lpi]. Container
   throughput and vessel tracking would be more direct
   [@unctad2024rmt].
2. **CPPI measures observed port time, not hinterland performance.**
   Its standardized port series can test the port-time interpretation
   of the inherited national screen [@worldbank2025cppi].
3. **The inherited screen fails that test.** Only one economy overlaps
   between its top five and the main CPPI-disadvantage top five; across
   20 reasonable specifications the overlap is zero to two.

## 4. Gap

The remaining gap is port-to-inland shipment time. LPI 2.0 documents
the required corridor object [@worldbank2026lpi2], but the official
underlying file is not yet available to this workflow. CPPI cannot be
extended beyond the port gate by interpretation alone.

## 5. Risk of redundancy

The rejected national proxy should not be revived by changing its
weights. The contribution at this stage is a documented construct
failure and a precise data requirement for the second gate.

## 6. First testable claim

> A national imports × LPI ranking does not preserve its ordering when
> tested against observed CPPI port time and therefore cannot support a
> port-hinterland friction headline.

## 7. §18 attestation

`ai-first`. 2026-04-27.
