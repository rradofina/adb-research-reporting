# Internal review — Coastal Informal Risk

`attestation_chain: ai-first`. §18 critique-pass. Closed 2026-04-26.

## Critique

1. WDI EN.POP.SLUM.UR.ZS has very few entries for ADB DMCs (only ~7
   of 31 coastal). The 10% imputation is a placeholder; the headline
   is robust to ±50% on imputation but a real slum-share series is
   the upgrade-pass.
2. "Coastal" is a binary flag. Coastal-zone *exposure* (LECZ) is
   the better measure; this artifact uses country-level coastal-yes/no
   only.
3. Population inflates the index for large countries. The headline
   reflects scale, not specifically coastal-informal vulnerability.

## Responses

1. Documented in limitations.md.
2. LECZ via CIESIN SEDAC is the §18.5 upgrade-pass.
3. The headline is honest: this is a population-scaled index. Per-capita
   variant deferred to upgrade-pass.
