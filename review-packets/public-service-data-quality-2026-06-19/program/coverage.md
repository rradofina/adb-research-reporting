# Coverage — Public Service Data Quality

Per-DMC coverage. Status: AI-derived from `generated/`. Refreshed when
the pipeline reruns.

Last refresh: 2026-04-25.

---

## DMCs in pre-registration scope

Source: `pre-registration.md` §3.

- PHL — Philippines
- BGD — Bangladesh
- IND — India (TODO)
- IDN — Indonesia (TODO)

## DMCs covered (this gate request)

| ISO3 | DMC | Country ratio (clinical-tier) | Worst ADM1 | Best ADM1 | Source | Retrieval date | Notes |
|---|---|---|---|---|---|---|---|
| PHL | Philippines | 17.1% | BARMM 6.5% | NCR 63.5% | DOH NHFR v2.0 | 2026-04-25 | 44,267 active facilities; 17 ADM1 units; 19-factype clinical-tier set. |
| BGD | Bangladesh | 11.8% | Barisal 6.2% | Dhaka 20.1% | DGHS Facility Registry | 2026-04-25 | 39,421 active facilities; 8 divisions; clinical-tier set derived from DGHS factype taxonomy. |

## DMCs not yet covered

| ISO3 | DMC | Reason | Plan |
|---|---|---|---|
| IND | India | HMIS pipeline not yet implemented; data available at `data.gov.in` (A-grade) | Add `scripts/fetch-hmis.py` + `scripts/process-disagreement-ind.py` in a follow-up commit. |
| IDN | Indonesia | SATUSEHAT registration is B-grade (light registration required); manual review of dashboard structure pending | Add `scripts/fetch-satusehat.py` after dashboard parsing is scoped. |

These two DMCs are explicitly **out of scope for the pending SR → PR
gate request**. A separate gate request will be filed when their
pipelines are complete.

## Coverage summary

| Field | Value |
|---|---|
| In scope (this gate) | 2 (PHL + BGD) |
| Covered | 2 |
| Coverage rate | 100% |
| Last refresh | 2026-04-25 |
| Next refresh | when OSM cache is re-pinned to Geofabrik/Overture |

## ADM1 coverage detail

PHL: 17 of 17 ADM1 regions have at least one OSM observation and at
least one NHFR observation. No ADM1 is missing.

BGD: 8 of 8 divisions have at least one OSM observation and at least
one DGHS observation. No division is missing.
