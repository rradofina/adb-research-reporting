# Coverage — Migration and displacement signals

`attestation_chain: ai-first`

Last refresh: 2026-07-18.

## Analysis population

The committed program panel contains **44 economies** encoded in
`scripts/process-migration.py`. This is the program's analysis roster, not a
claim that 44 is the current authoritative count of all ADB developing
members. Public copy refers to the exact program panel and named economies.

## Source coverage

| Evidence layer | Rows available | Use in this issue | Important exclusion |
|---|---:|---|---|
| UN DESA International Migrant Stock 2024 | 44/44 program economies | Absolute origin stock and bilateral destinations | Cumulative stock, not annual flow |
| WDI `SP.POP.TOTL`, 2024 | 41/44 | Resident-population denominator | No WDI value for Taipei,China, Cook Islands, or Niue |
| UNHCR 2024 origin-asylum query | 44/44 origins queried | Forced-displacement crosswalk | 41 origins have at least one positive forced-abroad row |
| UNHCR forced-displacement majority test | 44 origins assessed | Distinguish Afghanistan from the population-share top five | Does not classify labor, family, student, or temporary migration |

The population-share ranking withholds three economies rather than assigning
a fabricated denominator. Cook Islands and Niue are small Pacific economies,
so their absence may matter for the upper tail; the paper does not assume the
observed top-five set would remain unchanged if authoritative denominators
were added.

## Primary comparison

| Measure | Top five |
|---|---|
| Absolute emigrant stock | India, China, Bangladesh, Afghanistan, Philippines |
| Emigrant stock ÷ resident population | Samoa, Tonga, Armenia, Nauru, Fiji |

The two sets have zero overlap. Afghanistan is share rank 6 and is retained
as the forced-displacement comparison because UNHCR forced-displacement stock
equals 81.7% of its UN DESA emigrant stock.

## Temporal alignment

- UN DESA stock vintage: 2024.
- WDI population denominator: mid-year 2024, live query refreshed 2026-07-18.
- UNHCR forced-displacement stock: end-year 2024, API refreshed 2026-07-18.

The common reference year improves interpretability but does not make the
constructs identical. UN DESA stock accumulates over multiple years; WDI is a
resident-population snapshot; UNHCR reports defined protection categories at
year end.

## Coverage conclusion

The evidence is sufficient for a denominator and construct audit. It is not
sufficient for a current migration-flow, labor-migration, or internal-
displacement paper.
