# Internal review — Air Pollution Without Air Monitors

`attestation_chain: ai-first`. §18 critique-pass. Closed 2026-04-27.

## Critique

1. WDI EN.ATM.PM25.MC.M3 is a country-mean. Within-country variance
   is enormous (Indo-Gangetic Plain >>> South India).
2. OpenAQ monitor count varies daily; a snapshot can mis-rank DMCs
   that recently added monitors.
3. The gap-score is a multiplicative composite. Its sensitivity is
   limited because the inputs are bounded (PM2.5 cap ~50 µg/m³,
   monitor count ≥ 0), but the headline could be presented as a
   proxy rather than a measurement.

## Responses

1. Subnational ACAG-V6 is §18.5 upgrade-pass.
2. Snapshot date documented (2026-04-23 retrieval in versions.json).
3. Article frames as observability-gap *signal*, not measurement.
