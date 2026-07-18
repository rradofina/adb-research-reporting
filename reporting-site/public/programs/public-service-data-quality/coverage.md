# Coverage — Public Service Data Quality

Per-DMC coverage. Status: AI-derived from `generated/`. Refreshed when
the pipeline reruns.

Last refresh: 2026-07-19.

---

## Economies in the original prospectus

Source: `pre-registration.md` §3.

- PHL — Philippines
- BGD — Bangladesh
- IND — India (deferred from the current issue)
- IDN — Indonesia (deferred from the current issue)

## Economies covered by the current result

| ISO3 | DMC | Country ratio (clinical-tier) | Worst ADM1 | Best ADM1 | Source | Retrieval date | Notes |
|---|---|---|---|---|---|---|---|
| PHL | Philippines | 17.1% | BARMM 6.5% | NCR 63.5% | DOH NHFR v2.0 | 2026-04-25 | 44,267 active facilities; 17 ADM1 units; 19-factype clinical-tier set. |
| BGD | Bangladesh | 11.8% | Barisal 6.2% | Dhaka 20.1% | DGHS Facility Registry | 2026-04-25 | 39,421 active facilities; 8 divisions; clinical-tier set derived from DGHS factype taxonomy. |

## Prospectus extensions not included in this result

| ISO3 | DMC | Reason | Plan |
|---|---|---|---|
| IND | India | No current-issue pipeline or frozen comparable registry extract | Requires a separately registered question, source custody, and method freeze. |
| IDN | Indonesia | Comparable SATUSEHAT access requires an owner-provisioned account | Remains an owner-access extension, not an incomplete current-issue row. |

These two economies are explicitly **outside the bounded Philippines–Bangladesh
result**. They require a new source object and claim freeze rather than being
silently added to the current denominator.

## Coverage summary

| Field | Value |
|---|---|
| In scope (this gate) | 2 (PHL + BGD) |
| Covered | 2 |
| Coverage rate | 100% |
| Last refresh | 2026-07-19 |
| Next refresh | only for a registered vintage-replication question or a claim-changing source |

## ADM1 coverage detail

PHL: 17 of 17 ADM1 regions have at least one OSM observation and at
least one NHFR observation. No ADM1 is missing.

BGD: 8 of 8 divisions have at least one OSM observation and at least
one DGHS observation. No division is missing.

The granular modules disclose their own join coverage. The Philippine poverty
context joins an official value for 1,632 of 1,642 city/municipality polygons
and leaves 10 explicit source-missing rows. The Bangladesh upazila module has
572 registry rows, 561 Open Buildings denominators, and 527 rows with joined
OpenStreetMap features. These modules are contextual screens, not additions to
the national facility-count denominator.
