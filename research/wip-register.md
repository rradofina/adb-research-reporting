# WIP register

Governed by `CONSTITUTION.md` §8.1 — work-in-progress cap. Updated on
every gate promotion or demotion.

**Operating mode:** `CONSTITUTION.md` §18 (AI-First Operating Mode) is
**ACTIVE** as of 2026-04-25. Revised 2026-04-26: the §10.3 permanent
archive is now self-hosted at the reporting-site domain
(`/program/{slug}/evidence`) and AI mints it deterministically. Optional
Zenodo deposition remains available for external venues but is not
required. Every artifact carries `attestation_chain: ai-first` per §18.2.

| Cap | Limit (pre-§18 default) | Limit (§18 ACTIVE — current) | Current count |
|---|---|---|---|
| Publication-Ready (PR) | 1 | suspended | 1 |
| Screening Result (SR) | 3 | suspended | 0 |

§8.1 amended 2026-04-26: WIP caps suspended under §18 ACTIVE. Caps
reactivate when §18 is reverted.

§15 amended 2026-05-07: 9 programs previously labeled SR were demoted
back to PP. The SR label had been earned under §18 by a single
composite-index screening + ±50% sensitivity, which the new program-
loop standard (publication ladder + owner-review loop in
`research/factory.md`) treats as starting material rather than as a
ratified screening result. Artifacts are preserved, not deleted.
Re-promotion requires the program loop to be run end-to-end.

A promotion request that would push either count over its cap is
rejected at the gate.

Last updated: 2026-05-07.

---

## Programs by maturity

### Publication-Ready

- **public-service-data-quality** — PHL + BGD pilots computed
  (17.1% / 11.8% clinical-tier OSM/registry ratio). All gate artifacts
  AI-attested under §18 ACTIVE: literature.md (10 Tier-A/B/C entries,
  AI-finalized), scoring.md (24/30), pre-registration.md (§18 frozen
  2026-04-25), sensitivity.md (PHL + BGD ±50% complete, no critical
  failures), coverage.md, results.md, review-internal.md (§9.1+§9.2 AI
  critique-pass closed), review-external.md (§18.4 AI synthesis closed
  with 6 candidate-institution objections + responses), limitations.md
  (5 unresolved synthesized objections quoted verbatim),
  articles/measurement-gap-philippines-bangladesh.md (final).
  Permanent archive at `/program/public-service-data-quality/evidence`.
  Attestation chain `ai-first`.

### Screening Result

*(none currently; 9 programs demoted to PP on 2026-05-07 — see promotion log)*

### Prepared Pipeline

The 9 programs below were demoted from SR to PP on 2026-05-07 because the
SR label was earned under §18 by a single composite-index screening plus
±50% sensitivity only. Under the new program loop standard
(`research/factory.md` publication ladder + owner-review loop), that depth
counts as starting material, not a ratified screening result. Artifacts
are preserved. Re-promotion requires the new program loop to be run
end-to-end.

- **remittance-resilience** — 44 ADB DMCs ranked; top-5 set {KGZ, NPL,
  TON, VUT, WSM} stable across every ±50% perturbation including
  multiplicative→additive aggregation switch. Article:
  `articles/remittance-corridors-vulnerability-cluster.md`.
- **climate-health-workdays** — 34 rankable ADB DMCs; top-3 set
  {AFG, IND, BGD} stable across every ±50% perturbation. Article:
  `articles/workday-loss-pressure-cluster.md`.
- **migration-displacement-signals** — 44 ADB DMCs; top-5 set {IND,
  CHN, BGD, AFG, PHL} stable across emigrant-stock and net-migrant
  definitions. Article: `articles/emigrant-stock-corridor-concentration.md`.
- **disaster-recovery-lag** — the inherited CHN–IND burden headline is
  retired: three of five metrics replace at least one member. A 108-orbit
  Typhoon Haiyan pilot yields zero of seven GDIS centroids with one recovery
  month across 54 variants. Article: `articles/disaster-burden-cluster.md`.
- **grid-reliability-heat** — current issue closed: the capacity-to-generation
  top five remains {BTN, BRN, NPL, MNG, TJK}, but the aligned heat-reliability
  evidence splits direction and does not support a regional vulnerability
  ranking. Article: `articles/single-fuel-grid-cluster.md`.
- **port-hinterland-friction** — inherited national top five rejected:
  only IDN overlaps with the main observed CPPI-disadvantage top five,
  and overlap remains 0–2 across 20 specifications. The port-to-inland
  leg awaits the official LPI 2.0 shipment file. Article:
  `articles/port-friction-trade-volume-cluster.md`.
- **social-protection-shock-coverage** — 43 ADB DMCs; top-5 set
  {BGD, LAO, MMR, PAK, PHL} stable. Article:
  `articles/sp-shock-readiness-cluster.md`.
- **water-stress-crop-diversification** — top-4 narrowing {AFG, AZE,
  PAK, TKM}; UZB shifts under yield perturbations. Article:
  `articles/water-crop-pressure-cluster.md`.
- **school-heat-disruption** — honest narrowing to top-1 (KHM only)
  because top-5 fails sensitivity gate. Article:
  `articles/school-heat-honest-narrowing.md`.

### Prepared Pipeline (other)

*(see `CONSTITUTION.md` §15 program register; cross-check on every
promotion)*

### Hypothesis

*(see `CONSTITUTION.md` §15 program register; cross-check on every
promotion)*

### Retired

*(none)*

---

## Promotion log

| Date | Program | Transition | Commit | Attestation | Notes |
|---|---|---|---|---|---|
| 2026-04-25 | public-service-data-quality | H → PP | (initial) | ai-first | Pipeline complete and reproducible |
| 2026-04-25 | public-service-data-quality | PP → SR | (initial) | ai-first | PHL + BGD screening artifacts computed |
| 2026-04-25 | public-service-data-quality | SR → PR-pending-DOI under §18 | (this commit) | ai-first | All gate artifacts AI-attested under §18; Zenodo DOI was the only remaining step (owner-only per §18.1) |
| 2026-04-26 | remittance-resilience | H → PP → SR under §18 | (this commit) | ai-first | Top-5 set stable across ±50% sensitivity suite + aggregation-operator switch; SR cap now 1/3 |
| 2026-04-26 | (constitution) | §10.3 Zenodo → self-hosted archive | (this commit) | n/a | §16 amendment: permanent archive moved from Zenodo DOI to self-hosted evidence-packet route at /program/{slug}/evidence; Zenodo deposition retained as optional |
| 2026-04-26 | public-service-data-quality | PR-pending-DOI → PR under §18 (self-hosted) | (this commit) | ai-first | Permanent archive at /program/public-service-data-quality/evidence; PR cap now 1/1 |
| 2026-04-26 | climate-health-workdays | H → PP → SR under §18 | (this commit) | ai-first | Top-3 set {AFG, IND, BGD} stable across all ±50% rows; top-5 narrowed to top-3 due to pm25_cap sensitivity |
| 2026-04-26 | migration-displacement-signals | H → PP → SR under §18 | (this commit) | ai-first | Top-5 set {IND, CHN, BGD, AFG, PHL} stable across direction-of-definition; SR cap now 3/3 |
| 2026-04-26 | (constitution) | §8.1 caps suspended under §18 | (this commit) | n/a | "Full ham" pace authorized; caps reactivate when §18 reverted |
| 2026-04-26 | disaster-recovery-lag | H → SR under §18 | (this commit) | ai-first | top-2 stable across burden metrics |
| 2026-04-26 | grid-reliability-heat | H → SR under §18 | (this commit) | ai-first | top-5 single-fuel set stable |
| 2026-04-26 | port-hinterland-friction | H → SR under §18 | (this commit) | ai-first | top-5 stable across ±50% |
| 2026-04-26 | social-protection-shock-coverage | H → SR under §18 | (this commit) | ai-first | top-5 stable across SP/account weights |
| 2026-04-26 | water-stress-crop-diversification | H → SR under §18 | (this commit) | ai-first | top-4 narrowing — UZB perturbation-sensitive |
| 2026-04-26 | school-heat-disruption | H → SR under §18 | (this commit) | ai-first | honest narrowing to top-1 (KHM) — top-5 fails ±50% gate |
| 2026-04-26 | food-price-climate-transmission | (no promotion) | (this commit) | n/a | sensitivity-gate failure: no stable top-5; index needs reformulation; stays at PP |
| 2026-05-07 | remittance-resilience | SR → PP | (this commit) | ai-first | Demoted: SR earned under §18 by single composite-index screening only; new program loop applies (`research/factory.md`) |
| 2026-05-07 | climate-health-workdays | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | migration-displacement-signals | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | disaster-recovery-lag | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | grid-reliability-heat | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | port-hinterland-friction | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | social-protection-shock-coverage | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | water-stress-crop-diversification | SR → PP | (this commit) | ai-first | Same demotion reason |
| 2026-05-07 | school-heat-disruption | SR → PP | (this commit) | ai-first | Same demotion reason |

---

## How this file is kept honest

`scripts/check-wip.mjs` reads this file and `CONSTITUTION.md` §15 and
exits non-zero if the counts diverge or if the cap is exceeded. CI runs
this on every PR.
