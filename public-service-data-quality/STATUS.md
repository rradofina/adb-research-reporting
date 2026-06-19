# Public Service Data Quality — operating status

This is the per-program operating state for `public-service-data-quality`.
Repository-level focus and process rules live in `research/STATUS.md`,
`research/factory.md`, and `CLAUDE.md`. This file holds only what is
specific to PSDQ.

Last updated: 2026-06-19.

## Current

| Field | Value |
|---|---|
| Maturity label | PR (under §18 ai-first); **ai-first finished for current issue** as of 2026-05-07 (Mode A exit condition met) |
| Active stage | L3 source-disagreement module plus facility-validation sample, automated coded screen, AI public-source review ledger, 8-row candidate-resolution pass, richer public-source tag scan, 23-row coordinate-repair triage, 40-row public-map-gap triage, 40-row public-map-gap row-evidence ledger, 40-row targeted public-map inspection packet, 12-row first-source confirmation pass, 40-row targeted public-source confirmation pass, 16-row public-source decision ledger, 3-row possible same-facility review, 9-row priority name-conflict review, 6-row lower-priority name-conflict spot check, 115-upazila zero-OSM observability review, 39-row human-gated handoff matrix, 39-row human-validation worksheet, 39-row AI closure audit, 10-stage evidence ladder, 4-row source-repair public-evidence attachment, 4-row official-coordinate evidence, 4-row public-explanation search, 3-row correction-record follow-up, 3-row no-contact clarification packet, and 3-row registry-vintage review added; owner-only source contact or human validation remains the substantive source-repair, possible same-facility, priority/lower-priority name-conflict, and facility-level zero-OSM absence wall; PR maturity label unchanged |
| Active flagship | Yes, as of 2026-06-19 — rotated back in after the remittance L3 flow-weighting repair closed under Mode A. |
| Review mode | Mode A — AI-only review, default under §18 ACTIVE |
| Attestation chain | `ai-first` |
| Permanent archive | `/program/public-service-data-quality/evidence` |

## Current output target

A reviewer-credible PSDQ source-disagreement package for the showcase bench:
start from the Bangladesh exposure-ranked registry-map visual, package the
matching strata, validation sample, automated coded screen, AI row-review
ledger, candidate/source checks, coordinate-repair triage, public-map-gap
triage, row-evidence notes, targeted public-map inspection queue, first-row
public-source confirmation, 40-row targeted public-source confirmation,
public-source decision ledger, source-repair public evidence, official-coordinate
evidence, possible same-facility review, priority name-conflict review,
lower-priority name-conflict spot check,
zero-OSM upazila observability review,
human-gated handoff matrix,
human-validation worksheet,
AI closure audit,
evidence ladder,
public-explanation search, correction-record follow-up,
clarification packet, registry-vintage review, and caveats, make the source
upgrade clear in the public surface, and preserve the existing PR maturity
label without implying human-final review.

## Last completed

- **2026-06-19:** Added the Bangladesh facility-validation evidence ladder for
  the PSDQ source-disagreement showcase. New no-network script
  `scripts/build-bgd-facility-evidence-ladder.py` reads 10 committed summary
  JSON artifacts, then writes
  `generated/psdq-bgd-facility-validation-evidence-ladder.csv` and
  `generated/psdq-bgd-facility-validation-evidence-ladder-summary.json`.
  The ladder emits 10 stages and records 76 sampled facility rows, 40
  targeted public-source rows, 39 human-gated handoff rows, 39 AI
  closure-audit rows, 0 rows actionable without human or source-owner
  evidence, 39 keep-open-only terminal rows, and 39 human- or source-owner
  wall rows. Added `facility-validation-evidence-ladder.md`, wired evidence
  sync and review-packet inclusion, updated README/REPRODUCE/L3 notes, hook
  bank, showcase quality audit, showcase registry metadata, and added the
  evidence-ladder panel to `/showcase/psdq-source-disagreement`. This is a
  reader-navigation artifact, not a statistical funnel, source-owner response,
  human validation, ground truth, coordinate correction, row closure,
  same-facility reclassification, map-absence validation, a maturity
  promotion, or a human-final upgrade. Verification passed: ladder script
  rerun, script `py_compile`, evidence and reference sync, production site
  build, six deterministic gates plus `git diff --check`, review packet and
  zip rebuild, and Chrome CDP desktop/mobile QA at 1440x1100 and 390x900 with
  10 ladder stage cards, 4 summary cards, note/JSON/CSV links visible, no
  page-level or ladder-section horizontal overflow, no page errors, and only
  existing React Router future-flag warnings. Screenshots:
  `reporting-site/qa/showcase-psdq-evidence-ladder-desktop.png`,
  `reporting-site/qa/showcase-psdq-evidence-ladder-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-evidence-ladder-mobile.png`, and
  `reporting-site/qa/showcase-psdq-evidence-ladder-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh AI closure audit for the PSDQ
  facility-validation handoff queue. New no-network script
  `scripts/build-bgd-facility-ai-closure-audit.py` reads
  `generated/psdq-bgd-facility-validation-human-validation-worksheet.csv`,
  then writes
  `generated/psdq-bgd-facility-validation-ai-closure-audit.csv` and
  `generated/psdq-bgd-facility-validation-ai-closure-audit-summary.json`.
  The pass audits 39 worksheet rows across 5 handoff groups and 15 upazilas.
  It records 39 human- or source-owner wall rows, 0 external contacts, 0 AI
  closure rows, 0 AI same-facility reclassification rows, 0 AI map-absence
  language rows, 0 AI coordinate-correction rows, 0 rows actionable without
  human or source-owner evidence, and 39 keep-open-only rows. Added
  `facility-validation-ai-closure-audit.md`, wired evidence sync and
  review-packet inclusion, updated README/REPRODUCE/L3 notes, hook bank,
  showcase quality audit, showcase registry metadata, and added the AI
  closure-audit wall to `/showcase/psdq-source-disagreement`. This is a
  no-contact decision gate, not source-owner response, human validation,
  ground truth, coordinate correction, row closure, same-facility
  reclassification, map-absence validation, a maturity promotion, or a
  human-final upgrade. Verification passed: handoff/worksheet/audit chain
  rerun, audit script `py_compile`, evidence and reference sync, production
  site build, six deterministic gates plus `git diff --check`, review packet
  and zip rebuild, and Chrome CDP desktop/mobile QA at 1440x1100 and 390x900 with
  6 gate cards, 4 wall cards, 10 upazila cards, 12 row cards, audit note and
  CSV links visible, no page-level or section-level horizontal overflow, no
  page errors, and only existing React Router development warnings.
  Screenshots:
  `reporting-site/qa/showcase-psdq-ai-closure-audit-desktop.png`,
  `reporting-site/qa/showcase-psdq-ai-closure-audit-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-ai-closure-audit-mobile.png`, and
  `reporting-site/qa/showcase-psdq-ai-closure-audit-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh human-validation worksheet for the PSDQ
  facility-validation handoff queue. New no-network script
  `scripts/build-bgd-facility-human-validation-worksheet.py` reads
  `generated/psdq-bgd-facility-validation-human-gated-handoff.csv`, then
  writes
  `generated/psdq-bgd-facility-validation-human-validation-worksheet.csv` and
  `generated/psdq-bgd-facility-validation-human-validation-worksheet-summary.json`.
  The pass creates 39 worksheet rows across 5 handoff groups and 2 reviewer
  role classes. It pre-fills public evidence, review questions, minimum
  acceptable evidence rules, allowed decision values, and current public
  evidence gates; leaves 39 human-validation status fields and 39 proposed
  decision fields blank; and carries forward 0 external contacts, 0 prefilled
  closure rows, 0 prefilled reclassification rows, 0 prefilled map-absence
  rows, and 0 prefilled coordinate-correction rows. Added
  `facility-validation-human-validation-worksheet.md`, wired evidence sync and
  review-packet inclusion, updated README/REPRODUCE/L3 notes, and linked the
  worksheet downloads from `/showcase/psdq-source-disagreement`. This is a
  no-contact review instrument, not source-owner response, human validation,
  ground truth, coordinate correction, row closure, same-facility
  reclassification, map-absence validation, a maturity promotion, or a
  human-final upgrade. Verification passed: worksheet script rerun, script
  `py_compile`, evidence and reference sync, production site build, six
  deterministic gates plus `git diff --check`, review packet and zip rebuild,
  and agent-browser desktop/mobile QA at 1440x1100 and 390x900 with worksheet
  note/CSV links visible, 5 handoff group cards, 12 handoff row cards, no
  page-level or card-level horizontal overflow, no page errors, and only
  existing Vite / React Router development warnings. Screenshots:
  `reporting-site/qa/showcase-psdq-human-validation-worksheet-links-desktop.png`
  and
  `reporting-site/qa/showcase-psdq-human-validation-worksheet-links-mobile.png`.
- **2026-06-19:** Added the Bangladesh human-gated handoff matrix for the
  PSDQ facility-validation queue. New no-network script
  `scripts/build-bgd-facility-human-gated-handoff.py` reads the source-repair
  clarification packet, possible same-facility review, priority and
  lower-priority name-conflict reviews, and zero-OSM observability summary,
  then writes
  `generated/psdq-bgd-facility-validation-human-gated-handoff.csv` and
  `generated/psdq-bgd-facility-validation-human-gated-handoff-summary.json`.
  The pass consolidates 39 open rows across 5 groups and 15 upazilas: 3
  source-repair clarifications, 3 possible same-facility rows, 9 priority
  name-conflict rows, 6 lower-priority name-conflict rows, and 18 zero-OSM
  facility-row absence gates. It records 39 rows requiring human or
  source-owner action and allows 0 closures, 0 same-facility
  reclassifications, 0 map-absence uses, 0 coordinate corrections, and 0
  external contacts. Added `facility-validation-human-gated-handoff.md`,
  wired evidence sync and review-packet inclusion, updated
  README/REPRODUCE/L3 notes, hook bank, showcase quality audit, showcase
  registry metadata, and added the handoff wall to
  `/showcase/psdq-source-disagreement`. This is a no-contact reviewer queue,
  not source-owner response, human validation, ground truth, coordinate
  correction, row closure, same-facility reclassification, map-absence
  validation, a maturity promotion, or a human-final upgrade. Verification
  passed: human-gated handoff script rerun, script `py_compile`, evidence and
  reference sync, production site build, six deterministic gates plus
  `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with 5 group cards, 10 upazila
  cards, 12 handoff row cards, no page-level or card-level horizontal
  overflow, no page errors, no console messages, Durgapur, `0 closed`, and
  `0 map absence uses` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-human-gated-handoff-desktop.png`,
  `reporting-site/qa/showcase-psdq-human-gated-handoff-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-human-gated-handoff-mobile.png`, and
  `reporting-site/qa/showcase-psdq-human-gated-handoff-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh lower-priority name-conflict spot-check
  review for the PSDQ targeted public-source confirmation queue. New
  no-network script
  `scripts/build-bgd-facility-lower-priority-name-conflict-review.py` reads
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`,
  then writes
  `generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv`
  and
  `generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json`.
  The pass reviews the 6 deferred lower-priority name-conflict rows: all 6
  have DGHS profiles and OSM API records retrieved; 4 rows share reused
  public-map candidate features; all 6 candidates are at least 5 kilometers
  from the inspection point; 3 candidates are at least 10 kilometers away; 1
  candidate name score is at least 0.50; 0 candidate name scores are at least
  0.70; and the current artifacts contain 0 public alias/location sources. It
  allows 0 closures, 0 same-facility reclassifications, 0 map-absence uses, 0
  row reclassifications, and 0 external contacts. Added
  `facility-validation-lower-priority-name-conflict-review.md`, wired evidence
  sync and review-packet inclusion, updated README/REPRODUCE/L3 notes, hook
  bank, showcase quality audit, showcase registry metadata, and added the
  lower-priority name-conflict panel to `/showcase/psdq-source-disagreement`.
  This is a no-contact spot-check evidence gate, not source-owner response,
  human validation, ground truth, coordinate correction, row closure,
  same-facility reclassification, map-absence validation, a maturity
  promotion, or a human-final upgrade. Verification passed: lower-priority
  name-conflict script rerun, script `py_compile`, evidence sync, production
  site build, and agent-browser desktop/mobile QA at 1440x1100 and 390x900
  with 6 row cards, 4 candidate-cluster cards, no page-level or card-level
  horizontal overflow, no page errors, `momotaz clinic`, `Broadbank Clinic
  Quatere`, `0 alias source`, and `0 map absence uses` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-lower-name-conflict-review-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh zero-OSM upazila observability review
  for the PSDQ source-disagreement and facility-validation queue. New
  no-network script
  `scripts/build-bgd-facility-zero-osm-upazila-observability-review.py` reads
  `generated/psdq-bgd-exposure-ranked-disagreement.csv`,
  `generated/psdq-bgd-exposure-ranked-disagreement-summary.json`,
  `generated/psdq-bgd-facility-validation-public-map-inspection.csv`, and
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`,
  then writes
  `generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review.csv`
  and
  `generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json`.
  The pass reviews 115 active-registry upazilas with 0 joined OSM health
  features, covering 3,879 active DGHS clinical rows and 2,334,152 p85
  buildings in the 3 km under-observed proxy. It links 18 deferred inspection
  rows across 5 targeted upazilas while allowing 0 facility closures, 0
  facility-level absence uses, 0 coordinate corrections, 0 row
  reclassifications, and 0 external contacts. Added
  `facility-validation-zero-osm-upazila-observability-review.md`, wired
  evidence sync and review-packet inclusion, updated README/REPRODUCE/L3
  notes, hook bank, showcase quality audit, showcase registry metadata, and
  added the zero-OSM observability panel to
  `/showcase/psdq-source-disagreement`. This is an upazila-level
  observability packet, not facility-level absence evidence, source-owner
  response, human validation, ground truth, coordinate correction, row
  closure, same-facility reclassification, a maturity promotion, or a
  human-final upgrade. Verification passed: zero-OSM script rerun,
  program-script `py_compile`, evidence/reference/docs sync, production site
  build, six deterministic gates plus `git diff --check`, review packet and
  zip rebuild, and agent-browser desktop/mobile QA at 1440x1100 and 390x900
  with 8 division cards, 10 top-upazila cards, 8 targeted-strip cards, no
  page-level or card-level horizontal overflow, no page errors, Sonargaon,
  Chattogram, `0 closed`, and `0 facility absence uses` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-zero-osm-observability-desktop.png`,
  `reporting-site/qa/showcase-psdq-zero-osm-observability-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-zero-osm-observability-mobile.png`, and
  `reporting-site/qa/showcase-psdq-zero-osm-observability-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh priority name-conflict review for the
  PSDQ facility-validation decision ledger. New no-network script
  `scripts/build-bgd-facility-priority-name-conflict-review.py` reads
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`,
  then writes
  `generated/psdq-bgd-facility-validation-priority-name-conflict-review.csv`
  and
  `generated/psdq-bgd-facility-validation-priority-name-conflict-review-summary.json`.
  The pass reviews the 9 priority-1 name-conflict rows from the decision
  ledger: all 9 have DGHS profiles and OSM API records retrieved; 1 row has
  candidate name score at least 0.70; 6 candidates are at least 5 kilometers
  from the inspection point; 1 candidate is at least 10 kilometers from the
  inspection point; 4 candidate names contain an admin place name; and the
  current artifacts contain 0 public alias/location sources. It allows 0
  closures, 0 same-facility reclassifications, and 0 map-absence uses. Added
  `facility-validation-priority-name-conflict-review.md`, wired evidence sync
  and review-packet inclusion, updated README/REPRODUCE/L3 notes, hook bank,
  showcase quality audit, showcase registry metadata, and added the priority
  name-conflict panel to `/showcase/psdq-source-disagreement`. This is a
  no-contact evidence-gate packet, not source-owner response, human validation,
  ground truth, coordinate correction, row closure, same-facility
  reclassification, map-absence validation, a maturity promotion, or a
  human-final upgrade. Verification passed: priority name-conflict script
  rerun, program-script `py_compile`, evidence/reference/docs sync, production
  site build, six deterministic gates plus `git diff --check`, review packet
  and zip rebuild, and agent-browser desktop/mobile QA at 1440x1100 and
  390x900 with 9 rendered cards, no page-level or card-level horizontal
  overflow, no page errors, no console messages, Pabna, Narsingdi,
  `0 alias source`, and `0 closed` visible.
  Screenshots:
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-priority-name-conflict-review-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh possible same-facility review for the
  PSDQ facility-validation decision ledger. New no-network script
  `scripts/build-bgd-facility-possible-same-facility-review.py` reads
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`,
  then writes
  `generated/psdq-bgd-facility-validation-possible-same-facility-review.csv`
  and
  `generated/psdq-bgd-facility-validation-possible-same-facility-review-summary.json`.
  The pass reviews the 3 possible same-facility rows from the decision ledger:
  all 3 have DGHS profiles and OSM API records retrieved; 1 row has name score
  at least 0.95; all 3 candidates are at least 2 kilometers from the
  inspection point; and 0 rows are allowed for closure, same-facility
  reclassification, or map-absence language. Added
  `facility-validation-possible-same-facility-review.md`, wired evidence sync
  and review-packet inclusion, updated README/REPRODUCE/L3 notes, hook bank,
  showcase quality audit, showcase registry metadata, and added the possible
  same-facility panel to `/showcase/psdq-source-disagreement`. This is a
  no-contact evidence-gate packet, not source-owner response, human validation,
  ground truth, coordinate correction, row closure, same-facility
  reclassification, map-absence validation, a maturity promotion, or a
  human-final upgrade. Verification passed: possible same-facility script
  rerun, program-script `py_compile`, evidence/reference/docs sync, production
  site build, six deterministic gates plus `git diff --check`, review packet
  and zip rebuild, and agent-browser desktop/mobile QA at 1440x1100 and
  390x900 with 3 rendered cards, no page-level or card-level horizontal
  overflow, no page errors, no console messages, KPJ, Aichi, Chattogram, and
  `0 closed` visible. Screenshots:
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-possible-same-facility-review-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh source-repair registry-vintage review
  for the unresolved PSDQ facility-validation source-repair queue. New
  no-network script
  `scripts/build-bgd-facility-source-repair-registry-vintage-review.py` reads
  the clarification packet, public-explanation evidence CSV, and
  correction-record follow-up CSV, then writes
  `generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv`
  and
  `generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json`.
  The review covers the same 3 unresolved rows; all 3 have DGHS profile update
  timestamps; those timestamps were 1 to 12 days old at public-explanation
  retrieval; 0 public correction or coordinate-source records were found; and
  0 rows are allowed for closure, same-facility reclassification, or
  map-absence language. Added
  `facility-validation-source-repair-registry-vintage-review.md`, wired
  evidence sync and review-packet inclusion, updated README/REPRODUCE/L3 notes,
  hook bank, showcase quality audit, showcase registry metadata, and added the
  registry-vintage panel to `/showcase/psdq-source-disagreement`. This is a
  no-contact review packet, not source-owner response, human validation, ground
  truth, coordinate correction, row closure, same-facility reclassification, a
  maturity promotion, or a human-final upgrade. Verification passed:
  registry-vintage script rerun, program-script `py_compile`, evidence and
  reference sync, production site build, six deterministic gates plus
  `git diff --check`, and agent-browser desktop/mobile QA at 1440x1100 and
  390x900 with 3 rendered cards, no page-level horizontal overflow, no page
  errors, Durgapur and linked code `10000470` visible, the 1-12 day age range
  visible, and only existing Vite / React Router development warnings.
  Screenshots:
  `reporting-site/qa/showcase-psdq-registry-vintage-review-desktop.png`,
  `reporting-site/qa/showcase-psdq-registry-vintage-review-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-registry-vintage-review-mobile.png`, and
  `reporting-site/qa/showcase-psdq-registry-vintage-review-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh source-repair clarification packet for
  the unresolved PSDQ facility-validation source-repair queue. New no-network
  script
  `scripts/build-bgd-facility-source-repair-clarification-packet.py` reads
  `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`
  and writes
  `generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv`
  and
  `generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json`.
  The packet covers the 3 unresolved rows from the correction-record follow-up:
  the 2 shared-coordinate Narayanganj records and the Durgapur same-name
  cross-district conflict. It creates 3 source-owner or human-review questions,
  records 0 external contacts, carries forward 0 public correction or
  coordinate-source records found, and closes or reclassifies 0 rows. Added
  `facility-validation-source-repair-clarification-packet.md`, wired evidence
  sync and review-packet inclusion, updated README/REPRODUCE/L3 notes, hook
  bank, showcase quality audit, showcase registry metadata, and added the
  clarification-packet panel to `/showcase/psdq-source-disagreement`. This is a
  no-contact packet, not source-owner response, human validation, ground truth,
  coordinate correction, row closure, same-facility reclassification, a maturity
  promotion, or a human-final upgrade. Verification passed: clarification
  script rerun, program-script `py_compile`, evidence and reference sync,
  production site build, six deterministic gates plus `git diff --check`,
  review packet and zip rebuild, and agent-browser desktop/mobile QA at
  1440x1100 and 390x900 with 3 rendered cards, no page-level horizontal
  overflow, no page errors, Durgapur and linked code `10000470` visible, and
  only existing React Router development warnings. Screenshots:
  `reporting-site/qa/showcase-psdq-clarification-packet-desktop.png`,
  `reporting-site/qa/showcase-psdq-clarification-packet-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-clarification-packet-mobile.png`, and
  `reporting-site/qa/showcase-psdq-clarification-packet-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh source-repair correction-record
  follow-up for the unresolved PSDQ facility-validation source-repair queue.
  New live public-source script
  `scripts/followup-bgd-facility-source-repair-correction-records.py` reads
  `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`
  and selects the 3 rows still needing targeted public correction-record
  checks: the 2 shared-coordinate Narayanganj rows and the Durgapur same-name
  cross-district conflict. It writes
  `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv`
  and
  `generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json`.
  The pass checks 20 public official sources and retrieves all 20; finds 0
  public correction or coordinate-source records; confirms the DGHS dashboard
  target code for all 3 rows; confirms the linked Rajshahi Durgapur dashboard
  code for the Durgapur conflict; and closes or reclassifies 0 rows. Added
  `facility-validation-source-repair-correction-record-followup.md`, wired
  evidence sync and review-packet inclusion, updated README/REPRODUCE/L3 notes,
  hook bank, showcase quality audit, showcase registry metadata, and added the
  correction-record follow-up panel to `/showcase/psdq-source-disagreement`.
  This is public correction-record follow-up, not human validation, ground
  truth, coordinate correction, row closure, same-facility reclassification, a
  maturity promotion, or a human-final upgrade. Verification passed:
  correction-record script rerun, program-script `py_compile`, evidence and
  reference sync, production site build, six deterministic gates plus
  `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-correction-followup-desktop.png`,
  `reporting-site/qa/showcase-psdq-correction-followup-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-correction-followup-mobile.png`, and
  `reporting-site/qa/showcase-psdq-correction-followup-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh source-repair public-explanation
  evidence search for the PSDQ facility-validation source-repair queue. New
  live public-source script
  `scripts/search-bgd-facility-source-repair-public-explanations.py` reads
  `generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv`,
  joins cached DGHS public registry records, checks live DGHS profile tabs, and
  fetches linked official government health portals where available. It writes
  `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv`
  and
  `generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json`.
  The pass checks 4 source-repair rows, 8 live DGHS profile tabs, and 6
  official portal URLs; retrieves 5 official portal pages; finds 0 explicit
  public coordinate-source or coordinate-correction explanations; records 2
  rows sharing one official profile coordinate; records 1 row with a
  same-name cross-district DGHS registry sibling; and records 1 row where that
  same-name other-district coordinate is within 2 kilometers. The Netrakona
  Durgapur row is 747.0 meters from the separate Rajshahi Durgapur official
  record. All 4 source-repair rows remain open with 0 AI closures and 0 AI
  reclassifications. Added
  `facility-validation-source-repair-public-explanation-evidence.md`, wired
  evidence sync and review-packet inclusion, updated README/REPRODUCE/L3
  notes, and added the public-explanation panel to the showcase surface. This
  is public-source explanation evidence, not human validation, a coordinate
  correction, a row closure, a maturity promotion, or a human-final upgrade.
  Verification passed: public-explanation script rerun, program-script
  `py_compile`, production site build, six deterministic gates plus
  `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-explanation-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-explanation-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-public-explanation-mobile.png`, and
  `reporting-site/qa/showcase-psdq-public-explanation-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh source-repair official-coordinate
  evidence pass for the PSDQ facility-validation source-repair queue. New live
  public-source script
  `scripts/explain-bgd-facility-source-repair-official-coordinates.py` reads
  `generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv`,
  joins the targeted public-map inspection CSV, retrieves the 4 public DGHS
  profile pages, parses the embedded official map coordinate, and compares it
  with the pinned OSM candidate coordinate. It writes
  `generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv`
  and
  `generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json`.
  All 4 DGHS profiles were retrieved; all 4 expose official profile
  coordinates; all 4 coordinates match the inspection CSV; 2 rows share one
  official profile coordinate; 2 rows are at least 10 kilometers from the
  named OSM candidate; 1 row is at least 50 kilometers from the named OSM
  candidate; and 0 explicit coordinate-source explanations are exposed. All 4
  source-repair rows remain open with 0 AI closures and 0 AI
  reclassifications. Added
  `facility-validation-source-repair-official-coordinate-evidence.md`, wired
  evidence sync and review-packet inclusion, updated README/REPRODUCE/L3
  notes, and added the official-coordinate panel to the showcase surface. This
  is public-source coordinate evidence, not human validation, a coordinate
  correction, a row closure, a maturity promotion, or a human-final upgrade.
  Verification passed: official-coordinate script rerun, new script
  `py_compile`, program-script `py_compile`, production site build, six
  deterministic gates plus `git diff --check`, review packet and zip rebuild,
  and agent-browser desktop/mobile QA at 1440x1100 and 390x900 with no
  page-level horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-official-coordinate-evidence-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh source-repair public-evidence
  attachment for the PSDQ facility-validation decision ledger. New no-network
  script `scripts/attach-bgd-facility-source-repair-public-evidence.py` reads
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`,
  then writes
  `generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv`
  and
  `generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json`.
  The pass attaches public DGHS profile and OSM API evidence to all 4
  source-repair-first rows. All 4 have public evidence attached; 2 rows share
  one public-map candidate; 2 rows have candidate distance of at least 10
  kilometers; and 1 row has candidate distance of at least 50 kilometers. All
  4 source-repair rows remain open with 0 AI closures and 0 AI
  reclassifications. Added
  `facility-validation-source-repair-public-evidence.md`, wired evidence sync
  and review-packet inclusion, updated README/REPRODUCE/L3 notes, and prepared
  the showcase surface for source-repair evidence. This is public-source
  evidence attachment, not human validation, a source repair completion, a row
  closure, a maturity promotion, or a human-final upgrade. Verification
  passed: source-repair evidence script rerun, new script `py_compile`,
  program-script `py_compile`, production site build, six deterministic gates
  plus `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-source-repair-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-source-repair-evidence-desktop-cards.png`,
  `reporting-site/qa/showcase-psdq-source-repair-evidence-mobile.png`, and
  `reporting-site/qa/showcase-psdq-source-repair-evidence-mobile-cards.png`.
- **2026-06-19:** Added the Bangladesh public-source decision ledger for the
  targeted PSDQ facility-validation queue. New no-network script
  `scripts/build-bgd-facility-public-source-decision-ledger.py` reads
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`,
  then writes
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json`.
  The pass selects 16 reviewer decision rows from the 40 targeted
  confirmation rows: 4 source-repair rows, 3 possible same-facility rows, and
  9 priority-1 name-conflict rows. It defers 18 zero-OSM upazila
  observability rows and 6 lower-priority name-conflict spot checks. All 40
  targeted rows remain open with 0 AI closures and 0 AI reclassifications.
  Added `facility-validation-public-source-decision-ledger.md`, wired evidence
  sync and review-packet inclusion, updated README/REPRODUCE/L3 notes and the
  showcase registry, and added the decision-ledger panel to
  `/showcase/psdq-source-disagreement`. This is a public-source reviewer
  queue, not human validation, a row closure, a maturity promotion, or a
  human-final upgrade. Verification passed: decision-ledger script rerun,
  program-script `py_compile`, production site build, six deterministic gates
  plus `git diff --check`, review packet and zip rebuild, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-desktop-chart.png`,
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-public-source-decision-ledger-mobile-list.png`.
- **2026-06-19:** Added the Bangladesh targeted-row public-source
  confirmation pass for all 40 targeted public-map inspection rows. New live
  public-source script
  `scripts/confirm-bgd-facility-public-map-targeted-rows.py` reads
  `generated/psdq-bgd-facility-validation-public-map-inspection.csv`,
  retrieves the public DGHS profile page and public OSM API feature record for
  each targeted inspection row, and writes
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv`
  and
  `generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json`.
  The pass retrieves 40 DGHS profiles and 40 OSM API records; covers all 30
  priority-1 rows; all 40 rows have DGHS profile token support; 6 rows have
  live OSM candidate-name scores at or above 0.75; and all 40 rows remain
  open with 0 AI closures and 0 AI reclassifications. Confirmation lanes: 18
  zero-OSM context candidates outside the upazila, 15 candidate features
  retrieved but name conflict remains, 4 source-repair public sources
  retrieved, and 3 possible same-facility candidates needing manual location
  check. Added `facility-validation-public-source-confirmation-targeted-rows.md`,
  wired evidence sync and review-packet inclusion, updated README/REPRODUCE/L3
  notes and the showcase registry, and added the targeted-row confirmation
  panel to `/showcase/psdq-source-disagreement`. This is public-source
  confirmation, not human validation, a row closure, a maturity promotion, or
  a human-final upgrade. Verification passed: targeted-row confirmation
  script rerun, program-script `py_compile`, production site build, six
  deterministic gates plus `git diff --check`, review packet and zip rebuild,
  and agent-browser desktop/mobile QA at 1440x1100 and 390x900 with no
  page-level horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-desktop.png`,
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-desktop-chart.png`,
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-mobile.png`,
  and
  `reporting-site/qa/showcase-psdq-targeted-source-confirmation-mobile-list.png`.
- **2026-06-19:** Added the Bangladesh first-row public-source confirmation
  pass for the targeted public-map inspection queue. New live public-source
  script `scripts/confirm-bgd-facility-public-map-first-rows.py` reads
  `generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`,
  retrieves the public DGHS profile page and public OSM API feature record for
  the first 12 inspection rows, and writes
  `generated/psdq-bgd-facility-validation-public-source-confirmation.csv` and
  `generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json`.
  The pass retrieves 12 DGHS profiles and 12 OSM API records; all 12 rows have
  DGHS profile token support; 2 rows have live OSM candidate-name scores at or
  above 0.75; and all 12 rows remain open with 0 AI closures and 0 AI
  reclassifications. Confirmation lanes: 7 candidate features retrieved but
  name conflict remains, 2 source-repair public sources retrieved, 2 zero-OSM
  context candidates outside the upazila, and 1 possible same-facility
  candidate needing manual location check. Added
  `facility-validation-public-source-confirmation.md`, wired evidence sync and
  review-packet inclusion, and updated README/REPRODUCE/L3 notes. This is
  public-source confirmation, not human validation, a row closure, a maturity
  promotion, or a human-final upgrade. Verification passed: confirmation
  script rerun, new script `py_compile`, program-script `py_compile`,
  production site build, six deterministic gates plus `git diff --check`, and
  agent-browser desktop/mobile QA at 1440x1100 and 390x900 with no page-level
  horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-confirmation-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-source-confirmation-desktop-chart.png`,
  `reporting-site/qa/showcase-psdq-public-source-confirmation-mobile.png`, and
  `reporting-site/qa/showcase-psdq-public-source-confirmation-mobile-list.png`.
- **2026-06-19:** Added the Bangladesh targeted public-map inspection packet
  for the PSDQ facility-validation public-map-gap rows. New no-network script
  `scripts/inspect-bgd-facility-public-map-targets.py` reads the 40-row
  row-evidence ledger and summary, the pinned all-Bangladesh OSM/Overpass
  health-feature cache, and public geoBoundaries ADM1/ADM2/ADM3 caches, then
  writes
  `generated/psdq-bgd-facility-validation-public-map-inspection.csv` and
  `generated/psdq-bgd-facility-validation-public-map-inspection-summary.json`.
  The packet inspects all 40 open rows, covers all 30 priority-1 rows, creates
  a 10-row named-upazila start queue and an 18-row zero-OSM upazila queue,
  records 22 same-upazila candidate public-map feature links and 6
  specific-name signals, and keeps all 40 rows open with 0 AI closures and 0
  AI reclassifications. Inspection lanes: 4 source-repair-first rows, 3
  possible public-map match or buffer cases, 15 facility-specific public-map
  absence candidates, and 18 upazila public-map observability gaps. Added
  `facility-validation-public-map-inspection.md`, wired evidence sync and
  review-packet inclusion, updated README/REPRODUCE/L3 notes and the showcase
  registry, and added the inspection panel to
  `/showcase/psdq-source-disagreement`. This is targeted public-map
  inspection, not human validation, a row closure, a maturity promotion, or a
  human-final upgrade. Verification passed: inspection script rerun, new
  script `py_compile`, program-script `py_compile`, production site build,
  six deterministic gates plus `git diff --check`, and agent-browser
  desktop/mobile QA at 1440x1100 and 390x900 with no page-level horizontal
  overflow and no page errors. The mobile inspection chart uses a compact
  queue list instead of the desktop SVG. Screenshots:
  `reporting-site/qa/showcase-psdq-public-map-inspection-desktop.png`,
  `reporting-site/qa/showcase-psdq-public-map-inspection-mobile.png`, and
  `reporting-site/qa/showcase-psdq-public-map-inspection-mobile-queue.png`.
- **2026-06-19:** Added the Bangladesh public-map-gap row-evidence ledger for
  the PSDQ facility-validation flags. New no-network script
  `scripts/build-bgd-facility-public-map-gap-row-evidence.py` reads the
  public-map-gap triage CSV and summary JSON, then writes
  `generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv` and
  `generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json`.
  The ledger gives all 40 open map-gap rows a DGHS source note, public profile
  URL, OSM coordinate-inspection URL, OSM feature or absence note, and
  keep-open reviewer action. It covers all 30 priority-1 high-exposure rows;
  all 40 rows remain open. Evidence tiers: 4 source-repair-first rows, 3
  possible match or buffer-review rows, 15 row-level public-map absence-review
  rows, and 18 upazila-level public-map observability rows. Added
  `facility-validation-public-map-gap-evidence.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, L3 note, and previous public-map-gap
  note. This is row-level public-source evidence, not human validation, a
  maturity promotion, or a human-final upgrade. Verification passed:
  row-evidence script rerun, program-script `py_compile`, production site build,
  six deterministic gates, `git diff --check`, and agent-browser desktop/mobile
  QA at 1440x1100 and 390x900 with no page-level horizontal overflow and no
  page errors. The mobile row-evidence chart was revised from a cropped wide
  SVG into a compact upazila list before final QA. Screenshots:
  `reporting-site/qa/showcase-psdq-row-evidence-desktop.png`,
  `reporting-site/qa/showcase-psdq-row-evidence-mobile.png`, and
  `reporting-site/qa/showcase-psdq-row-evidence-mobile-chart.png`.
- **2026-06-19:** Added the Bangladesh public-map-gap triage for the PSDQ
  facility-validation flags. New no-network script
  `scripts/triage-bgd-facility-public-map-gaps.py` reads the AI review
  ledger, coded-screen CSV, coordinate-repair CSV, exposure-ranked table, OSM
  upazila table, cached all-Bangladesh OSM health features, and cached DGHS
  public DataTables rows, then writes
  `generated/psdq-bgd-facility-validation-public-map-gap.csv` and
  `generated/psdq-bgd-facility-validation-public-map-gap-summary.json`. The
  triage keeps all 40 public-map-gap rows open: 30 priority-1 high-exposure
  rows, 18 zero-OSM expected-upazila rows, 2 reused valid-coordinate rows, 2
  far same-upazila name-signal rows, 1 same-upazila name signal outside 500
  meters, 2 buffer-sensitive 500m-to-1km rows, 3 OSM-present-not-at-facility
  rows, and 12 no-same-upazila-OSM-signal-within-3km rows. Added
  `facility-validation-public-map-gap.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, L3 note, hook bank, quality audit,
  showcase registry, and `/showcase/psdq-source-disagreement`. This is
  public-source triage, not human validation, a maturity promotion, or a
  human-final upgrade. Verification passed: new script rerun, new script
  `py_compile`, program-script `py_compile`, production site build, six
  deterministic gates, and agent-browser desktop/mobile QA at 1365px and
  375px with no page-level horizontal overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-public-map-gap-desktop.png` and
  `reporting-site/qa/showcase-psdq-public-map-gap-mobile.png`.
- **2026-06-19:** Added the Bangladesh coordinate-repair triage for the PSDQ
  facility-validation flags. New no-network script
  `scripts/triage-bgd-facility-coordinate-repairs.py` reads the AI review
  ledger, coded-screen CSV, public geoBoundaries ADM3, cached all-Bangladesh
  OSM health features, and cached DGHS public DataTables rows, then writes
  `generated/psdq-bgd-facility-validation-coordinate-repair.csv` and
  `generated/psdq-bgd-facility-validation-coordinate-repair-summary.json`.
  The triage keeps all 23 coordinate-repair rows open: 7 missing coordinates,
  2 reused sampled coordinates, 6 other-ADM3 coordinates near an OSM health
  feature, 5 other-ADM3 coordinates without a nearby OSM health feature, and
  3 outside the public ADM3 polygons used here. Sixteen usable suspect
  coordinates fall outside the expected sampled upazila; 4 are at least 50
  kilometers away and the largest measured distance is 351.4 kilometers. Added
  `facility-validation-coordinate-repair.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, L3 note, hook bank, quality audit,
  showcase registry, and `/showcase/psdq-source-disagreement`. This is
  source-repair triage, not human validation, a maturity promotion, or a
  human-final upgrade. Verification passed: new script `py_compile`,
  production site build, six deterministic gates, and agent-browser
  desktop/mobile QA at 1365px and 375px with no page-level horizontal overflow
  and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coordinate-repair-desktop.png` and
  `reporting-site/qa/showcase-psdq-coordinate-repair-mobile.png`.
- **2026-06-19:** Added the Bangladesh candidate public-source check for the
  PSDQ facility-validation flags. New no-network script
  `scripts/check-bgd-facility-candidate-public-sources.py` reads the
  candidate-resolution CSV, OSM-candidates CSV, pinned all-Bangladesh OSM tags,
  and cached DGHS DataTables rows, then writes
  `generated/psdq-bgd-facility-validation-candidate-public-source-check.csv`
  and
  `generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json`.
  The scan keeps all 8 candidate rows open while separating them into 2 strong
  same-site OSM tag-support rows, 2 same-site type/label conflicts, 2
  name-support rows with coordinate/function conflicts, and 2 nearby-feature
  rows without registry-name support. Added
  `facility-validation-candidate-public-source-check.md`, updated README,
  REPRODUCE, evidence sync/review-packet inclusion, the L3 note, hook bank,
  quality audit, and `/showcase/psdq-source-disagreement`. This is AI
  public-source evidence scanning, not human validation, a maturity promotion,
  or a human-final upgrade. Verification passed: new script and program-script
  `py_compile`, production site build, six deterministic gates, and
  agent-browser desktop/mobile QA at 1365px and 375px with no page-level
  horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-public-source-check-desktop.png` and
  `reporting-site/qa/showcase-psdq-public-source-check-mobile.png`.
- **2026-06-19:** Added the Bangladesh candidate-resolution pass for the
  PSDQ facility-validation flags. New no-network script
  `scripts/resolve-bgd-facility-candidate-rows.py` reads the AI review ledger,
  OSM-candidates CSV, and AI review summary, then writes
  `generated/psdq-bgd-facility-validation-candidate-resolution.csv` and
  `generated/psdq-bgd-facility-validation-candidate-resolution-summary.json`.
  The pass keeps all 8 candidate-resolution rows open while separating them
  into 1 probable alias/campus lane, 2 same-site classification-conflict lanes,
  2 possible aliases, 1 local-script name gap, 1 ambiguous nearby candidate,
  and 1 weak nearby OSM signal. Added
  `facility-validation-candidate-resolution.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, the L3 note, and
  `/showcase/psdq-source-disagreement`. This is AI public-source candidate
  resolution, not human validation, a maturity promotion, or a human-final
  upgrade. Verification passed: new script and program-script `py_compile`,
  production site build, six deterministic gates, review-packet rebuild, and
  agent-browser desktop/mobile QA at 1365px and 375px with no page-level
  horizontal overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-candidate-resolution-desktop.png` and
  `reporting-site/qa/showcase-psdq-candidate-resolution-mobile.png`. Rebuilt
  review packet folder and zip:
  `review-packets/public-service-data-quality-2026-06-18/` and
  `review-packets/public-service-data-quality-2026-06-18.zip`.
- **2026-06-19:** Added the Bangladesh AI public-source review ledger for the
  PSDQ facility-validation flags. New no-network script
  `scripts/review-bgd-facility-validation-flags.py` reads the coded-screen
  CSV, OSM-candidates CSV, and coded-summary JSON, then writes
  `generated/psdq-bgd-facility-validation-ai-review.csv` and
  `generated/psdq-bgd-facility-validation-ai-review-summary.json`. The ledger
  keeps all 71 flagged rows open while separating them into 40 public-map-gap
  checks, 23 coordinate-source repairs, 6 name/type resolution rows, and 2
  nearby-OSM-without-registry-match rows. Added
  `facility-validation-ai-review.md`, updated README, REPRODUCE,
  evidence sync/review-packet inclusion, hook bank, quality audit, and
  `/showcase/psdq-source-disagreement`. This is AI public-source review, not
  human validation, a maturity promotion, or a human-final upgrade.
  Verification passed: new script and program-script `py_compile`, production
  site build, six deterministic gates, and browser QA at 1365px desktop and
  375px mobile with no page-level horizontal overflow and no page errors.
  Screenshots:
  `reporting-site/qa/showcase-psdq-ai-review-desktop.png` and
  `reporting-site/qa/showcase-psdq-ai-review-mobile.png`. Rebuilt review
  packet folder and zip:
  `review-packets/public-service-data-quality-2026-06-18/` and
  `review-packets/public-service-data-quality-2026-06-18.zip`.
- **2026-06-19:** Added the automated Bangladesh facility-validation coded
  screen for the PSDQ source-disagreement L3 module. New no-network script
  `scripts/code-bgd-facility-validation-sample.py` reads the 76-row validation
  sheet, cached all-Bangladesh OSM health-feature pull, and geoBoundaries ADM3,
  then writes `generated/psdq-bgd-facility-validation-coded-screen.csv`,
  `generated/psdq-bgd-facility-validation-osm-candidates.csv`, and
  `generated/psdq-bgd-facility-validation-coded-summary.json`. The automated
  screen codes 40 rows as missing public-map points, 23 as registry coordinate
  issues, 5 as confirmed same-facility matches, 3 as probable aliases, 3 as
  classification mismatches, and 2 as OSM-only candidates. Added
  `facility-validation-coded-screen.md`, updated the L3 note, README,
  REPRODUCE, evidence sync/review-packet inclusion, showcase registry, hook
  bank, quality audit, and `/showcase/psdq-source-disagreement`. The route now
  fetches the coded-summary JSON, shows a grouped coded-screen chart, and
  links the coded-screen downloads. This is automated triage, not manual
  validation, a maturity promotion, or a human-final upgrade. Browser QA
  passed at 1365px desktop and 375px mobile with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-coded-screen-desktop.png` and
  `reporting-site/qa/showcase-psdq-coded-screen-mobile.png`.
- **2026-06-19:** Added the Bangladesh facility-validation sample design for
  the PSDQ source-disagreement L3 module. New no-network script
  `scripts/design-bgd-facility-validation-sample.py` reads the L3 strata,
  exposure-ranked disagreement table, and DGHS facility-coordinate extract,
  then writes `generated/psdq-bgd-facility-validation-sample.json`,
  `generated/psdq-bgd-facility-validation-sample-upazilas.csv`,
  `generated/psdq-bgd-facility-validation-sample-facilities.csv`, and
  `generated/psdq-bgd-facility-validation-coding-sheet.csv`. The design
  covers 20 sampled upazilas and 76 DGHS facility rows; 69 sampled facility
  rows are coordinate-ready. Added `facility-validation-sample.md`, updated
  the source-disagreement L3 note, README, REPRODUCE, evidence sync and
  review-packet inclusion, showcase registry, hook bank, quality audit, and
  `/showcase/psdq-source-disagreement`. The route now fetches the sample JSON,
  shows a validation-sample panel, and links the blank coding sheet. This is
  not a validation outcome, maturity promotion, or human-final upgrade.
  Verification completed so far: sample script and `py_compile` passed;
  `npm run build` passed; six deterministic gates passed; browser QA passed at
  1365px desktop and 375px mobile with no page-level horizontal overflow and
  no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-validation-sample-desktop.png` and
  `reporting-site/qa/showcase-psdq-validation-sample-mobile.png`.
- **2026-06-19:** Added the Bangladesh source-disagreement L3 evidence module
  for the showcase bench. New no-network script
  `scripts/build-bgd-source-disagreement-strata.py` reads the existing BGD
  exposure-ranked disagreement and road-context artifacts, then writes
  `generated/psdq-bgd-source-disagreement-strata.{json,csv}` with ratio
  buckets, validation residues, and top validation rows. Added
  `source-disagreement-l3-module.md`, updated `REPRODUCE.md`, `README.md`,
  evidence sync/review-packet inclusion, the showcase registry, the hook bank,
  and `/showcase/psdq-source-disagreement`. The route now fetches the strata
  JSON, shows the validation ledger before the interactive workbench, and links
  directly to the L3 note and downloads. Rebuilt review packet folder and zip:
  `review-packets/public-service-data-quality-2026-06-18/` and
  `review-packets/public-service-data-quality-2026-06-18.zip` (UTC-dated by
  the packet script). Verification completed: strata script passed;
  `npm run build` passed; six deterministic gates passed; browser QA
  passed at 1365px desktop and 375px mobile with no page-level horizontal
  overflow and no page errors. Screenshots:
  `reporting-site/qa/showcase-psdq-l3-desktop.png` and
  `reporting-site/qa/showcase-psdq-l3-mobile.png`. This is not a maturity
  promotion and not a human-final upgrade.
- **2026-06-19:** Reopened PSDQ as the active flagship for the showcase
  source-disagreement L3 deepening loop after the remittance flow-weighting
  repair was committed as `225d4d2`. The next output is not a new maturity
  promotion. It is a tighter evidence spine around
  `/showcase/psdq-source-disagreement`: matching strata, validation notes,
  source caveats, and a public-surface QA pass.
- **2026-06-16:** Added a showcase-native PSDQ source-disagreement visual
  uplift at `/showcase/psdq-source-disagreement`. The surface reads the
  committed Bangladesh exposure-ranked disagreement CSV/JSON and the PSDQ
  national summary from `reporting-site/public/programs/public-service-data-quality/generated/`.
  It frames the registry-map problem as source QA before service-access
  mapping, not as a facility-quality, access, or ground-truth claim. The
  interactive workbench ranks upazila rows by Open Buildings under-observed
  proxy, registry gap share, or lowest OSM/registry ratio, with division and
  focus controls. Browser QA captured desktop/mobile first-view and visual
  screenshots under `reporting-site/qa/`; checks confirmed 16 rendered SVG
  rows, working metric toggle, no page-level horizontal overflow, mobile chart
  overflow contained in the chart scroller, and zero page errors. Console
  output contained only existing Vite/React Router development warnings.
  Maturity label unchanged.
- **2026-05-12:** ADB/ERDI-style polish pass on PSDQ public surfaces under
  the new `/goal` skill's flagship bar. Three live-surface edits + one
  governance alignment, no claim change. **Live edits** (shipped to the
  site via `articles/measurement-gap-philippines-bangladesh.md` →
  `reporting-site/public/articles/`, verified in viewport at 1280px and
  375px): (1) article subtitle tightened from a dense two-sentence
  tongue-twister using the stale "screening result" label to a
  finding+benchmark formulation matching the working-paper convention; (2)
  article abstract restructured to lead with the 17.1% / 11.8% headline
  numbers and the 9.8× within-country gradient (NCR 63.5% vs BARMM 6.5%)
  before the upgrade-pass and attestation context; (3) article opening of
  "# The question" rewritten from textbook-pedagogical ("Two questions sit
  underneath any planning exercise") to stakes-led ADB/ERDI register
  ("Project teams that build facility catchments, service-coverage maps,
  and travel-time isochrones routinely combine public maps with official
  registries… A planner who treats the gap as noise will treat coverage
  problems as present-but-small when they are present-and-systematic").
  The Topic.tsx page renders the article-frontmatter `title` as h1 and
  `subtitle` as the prominently-displayed hook beneath it — so the
  finding-led hook lives in the subtitle, with the descriptive title above
  matching ADB working-paper convention. **Governance alignment**:
  `CLAUDE.md` hard-walls table line 78 changed from "real internal review
  with Arturo" to "real internal review by an owner-designated reviewer"
  — aligns with `/goal` skill's standing wording, makes the human-final
  hard-wall structural rather than personnel-specific.
  **Non-shipping edit (reverted)**: I initially also edited the h1 +
  subhead on `reporting-site/src/pages/ProgramPSDQ.tsx`, but viewport
  verification revealed `ProgramPSDQ.tsx` is orphan code — not imported
  by the router; the live `/<slug>` route is served by Topic.tsx. The
  ProgramPSDQ edit was reverted to its pre-pass state to keep the diff
  history honest. All five gates pass; `sync-articles.mjs` re-synced 25
  articles; `npm run build` succeeds in 4.80s. Mode A exit condition
  unchanged; PSDQ remains **ai-first finished for current issue** under
  the same attestation chain.
- **2026-05-07:** Browser-checked the three PSDQ public surfaces
  (`/program/public-service-data-quality`, the article, and the evidence
  page) at desktop (1280px) and mobile (375px). All three render the new
  poverty-overlay numbers correctly: 1,642 ADM3 rows, 1,632 joined (1,597
  SAE + 35 OpenSTAT), 10 explicit source-missing. Console: 0 errors. Fixed
  one mobile regression on the Evidence page (rendered-markdown tables and
  inline `<code>` were not constrained); added ~10 lines of additive CSS to
  `reporting-site/src/index.css` giving rendered-markdown tables
  `overflow-x: auto` and inline `<code>` `overflow-wrap: anywhere`. After
  fix: document width 376 ≈ viewport 375, 33/33 markdown tables now
  scrollable, 436/436 inline `<code>` blocks now wrap. All five gates pass;
  `npm run build` succeeds in 7.00s.
- **2026-05-05:** Owner manually downloaded the official PSA 2023 SAE
  workbook and seeded the deterministic cache via
  `python scripts/fetch-phl-sae-poverty.py --sae-xlsx <path>`. Generated
  `psdq-phl-admin3-poverty-context.{csv,json}`: 1,597 SAE rows + 35
  OpenSTAT direct-estimate rows joined, 10 ADM3 rows still source-missing
  and not imputed.
- **Earlier:** Hardened the PSA fetcher (`sites/default`, `system/files`,
  `www` variants; Cloudflare blocker recorded as source-status). Added
  `SOURCE-ACTION.md`, `REPRODUCE.md`, `upgrade-gap.md`. Updated the public
  program page with a poverty-source-status panel that distinguishes SAE,
  OpenSTAT direct-estimate, and source-missing rows. Updated the
  reader-facing working paper to reflect the ADM3/upazila granular
  upgrade, Bangladesh road context, and the reproducibility runbook.

## Next focused work

Current loop:

1. Owner-only source-owner contact or human location validation is now the
   substantive source-repair, possible same-facility, priority and
   lower-priority name-conflict, and facility-level zero-OSM absence wall for the
   unresolved Durgapur same-name cross-district coordinate conflict, the two
   shared-coordinate Narayanganj rows, the three possible same-facility
   public-map candidates, the nine priority name-conflict candidates, the six
   lower-priority name-conflict candidates, and
   any specific DGHS row sitting inside a zero-OSM upazila context. AI must
   not contact DGHS, any facility, or any external reviewer.
2. Keep source-repair-first rows before any map-absence or same-facility
   language because coordinate/source repair changes the interpretation.
3. Keep zero-OSM upazila observability rows separate from row-level absence
   candidates because the nearest candidate feature is context, not direct
   evidence of the DGHS row.
4. Keep source-repair-first rows separate from possible same-facility public
   map matches, facility-specific absence candidates, and upazila-level public
   map observability cases.
5. Keep possible same-facility rows open until public evidence or human
   validation supports identity and location together.
6. Keep priority name-conflict rows open until public alias/location evidence
   or human validation resolves the name conflict.
7. Use only public DGHS rows, OSM/Overpass evidence, public map inspection
   links, public government health portals, and other public official pages. Do
   not use private facility lists or owner-only credentials. Stop if validation
   requires non-public access.
8. Close or reclassify a row only if public evidence supports the change. If
   public evidence is insufficient, keep the row unresolved and record the
   specific source question.
9. Rerun sync/build/gates/browser QA after any public-surface change.

Historical publication-ladder closeout remains below for context.

The current flagship has the working paper, program page, and evidence
packet. The publication ladder defined in `research/factory.md` requires
four more tiers before PSDQ counts as "finished for current issue" under
the new loop standard:

1. **PSDQ brief** — **done 2026-05-07**: `articles/_brief/public-service-data-quality.md`,
   ~600 words including frontmatter, single chart (PHL ADM1 choropleth SVG).
   Slug `public-service-data-quality-brief`, available at
   `/findings/public-service-data-quality-brief`. Verified at desktop and
   mobile (chart 712px / 277px respectively, zero overflow). All gates pass.
   Co-amendment: extended `scripts/sync-articles.mjs` to recurse into
   publication-ladder tier subdirectories (`articles/_brief/`, `_blog/`,
   `_social/`, `_slides/`) and tag each entry with a `tier` field in
   `index.json`.
2. **PSDQ blog post** — **done 2026-05-07**:
   `articles/_blog/public-service-data-quality.md`, ~750 words narrative
   for the general dev-econ reader. Same chart as the brief (PHL ADM1
   choropleth SVG) under the visualization-rule single-source-of-truth
   principle. Slug `public-service-data-quality-blog`, available at
   `/findings/public-service-data-quality-blog`. Verified at desktop and
   mobile, all gates pass. Cites Macharia 2025, Sandefur & Glassman 2015,
   South et al. 2021, Maina et al. 2019.
3. **PSDQ social card** — **done 2026-05-07**:
   `articles/_social/public-service-data-quality.md`. Tweet body 252/280
   chars: "Two maps of the same country don't agree…". Same chart as
   brief and blog (PHL ADM1 choropleth SVG). Includes alt text describing
   the visual gradient and links back to brief, blog, working paper, and
   evidence packet. Slug `public-service-data-quality-social`, available
   at `/findings/public-service-data-quality-social`. All gates pass.
4. **PSDQ slide deck** — **done 2026-05-07**:
   - Source: `articles/_slides/public-service-data-quality.md` (Quarto
     markdown, 11 slides, attestation chain `ai-first`).
   - Build: `scripts/build-slides.mjs` regenerates the choropleths via
     `build-choropleth.py` (single source of truth — same charts as
     brief, blog, social, program page), then runs `quarto render
     --to pptx` and moves the artifact into the program's public folder.
   - Output: `reporting-site/public/programs/public-service-data-quality/public-service-data-quality-deck.pptx`
     (~702 KB with embedded charts).
   - Quarto 1.9.37 installed via winget at `C:\Program Files\Quarto\bin`.
     Build passes 5/5 gates.
   - Slide content covers: question · headline · PHL choropleth ·
     BGD choropleth · ±50% sensitivity · ADM3 poverty overlay ·
     why-it-matters · explicit non-claims · reproducibility ·
     attestation chain.
4. **Reviewer-ready source/method packet**: bundled `results.md`,
   `sensitivity.md`, `limitations.md`, the poverty-context CSV, the
   manifest, and a one-page cover letter — refresh from the 2026-04-25
   packet at `review-packets/`.
5. **Reviewer-ready packet** — **done 2026-05-07**:
   `review-packets/public-service-data-quality-2026-05-07/` (folder, 90
   files: 6 publication-tier + 75 program + 9 shared) and `.zip`
   (6.1 MB, emailable). The packet bundles the full publication ladder
   (working paper, brief, blog, social card, slide deck `.pptx` + source)
   plus all program artifacts (literature, pre-reg, sensitivity,
   limitations, reviews, generated CSVs, choropleth charts, scripts) plus
   shared governance (Constitution, references.bib, red-team.md outreach
   template, versions.json, manifest.sha256). Cover README orients the
   reviewer by attention budget (2 min, 10 min, 20 min, 90 min). Built
   by extended `scripts/build-review-packet.mjs` (now recurses into
   generated/ subfolders, includes publication-ladder tiers, includes
   the built `.pptx`). Co-amendment in `build-choropleth.py`: added
   geometry simplification (0.005° ADM1, 0.001° ADM3) so SVG file sizes
   are publishable (1.0 MB and 4.3 MB respectively, down from 336 MB
   and 357 MB at full PSA/NAMRIA precision).
6. **Resolve the 257 unresolved Philippines NHFR records** — **done
   2026-05-07** (249 of 257 resolved, residue 8): all 257 were in BARMM
   Maguindanao ctymuncode prefixes PH19087* and PH19088*, a code-vintage
   mismatch where NHFR uses an older PSGC numbering and PSA/NAMRIA 2023
   has reassigned the same barangays to modern ADM3 polygons. New
   resolver `scripts/inspect-barmm-codes.py` extracts the barangay name
   from each NHFR facility name (the prefix before "BARANGAY HEALTH
   STATION", "RURAL HEALTH UNIT", etc.), looks the name up in PSA/NAMRIA
   2023 ADM4 within ADM2 PH19087+PH19088, and takes the parent ADM3.
   Per ctymuncode the resolution is the majority winner — every resolved
   group had unanimous votes (share = 1.0). 17 of 18 ctymuncode groups
   resolved; 249 of 257 records assigned to a specific ADM3. Resolver
   wired into `scripts/build-phl-admin3-open-buildings-context.py` as
   the `barmm_barangay_name_resolved` rule. Audit trail at
   `generated/psdq-phl-nhfr-barmm-ctymun-resolution.json`. New ADM3 match
   rate is 99.98% overall and 99.98% for clinical-tier records (was
   99.42% / 99.31%). The remaining 8 records are all in a single
   ctymuncode (1908807) whose facility names do not contain a recognizable
   barangay name (e.g., "ABPI-SAMAMA MEDICAL LYING IN CLINIC AND
   HOSPITAL"); they are kept explicitly unresolved as a source-quality
   residue and are not imputed. Updated docs: `README.md`,
   `upgrade-gap.md`, working paper, this file.
6. **PSDQ choropleth map** — Python build **done 2026-05-07**:
   `scripts/build-choropleth.py` produces three publication-ready
   maps as PNG + SVG:
   - `generated/charts/psdq-choropleth-phl-adm1.{png,svg}` — Philippines
     OSM/NHFR clinical-tier ratio per ADM1 (17 regions). Includes the
     DOH-NHFR ↔ PSA-PSGC code mapping (six regions use different codes
     across the two systems).
   - `generated/charts/psdq-choropleth-bgd-adm1.{png,svg}` — Bangladesh
     OSM/DGHS clinical-tier ratio per ADM1 (8 divisions).
   - `generated/charts/psdq-choropleth-phl-adm3-poverty.{png,svg}` —
     PHL ADM3 official 2023 poverty incidence (1,632 of 1,642 polygons
     joined to PSA SAE + OpenSTAT direct; 10 explicit source-missing).
   Synced to `reporting-site/public/programs/public-service-data-quality/generated/charts/`.
   Sub-steps status:
   - **Done 2026-05-07**: Embedded the three choropleth SVGs into the
     PSDQ program page as a "Spatial picture" section between the
     header and the granularity-upgrade section. Verified at desktop
     (1280px, two-column grid for ADM1 maps + full-width ADM3 poverty)
     and mobile (375px, single-column stack, zero horizontal overflow,
     zero console errors). Production build passes (84 modules, 537 KB
     JS / 46 KB CSS). Same SVG files load on both surfaces; alt text
     describes the visual story; captions cite the underlying CSV.
   - **Pending**: Use the same script's logic as the chart in the
     Quarto slide deck (Tier 6) and the brief (Tier 3). The slide-deck
     and brief should call the same Python via Quarto code blocks, not
     a separate render. The React component upgrade (`react-simple-maps`
     for interactivity) is deferred until a program needs zoom/pan; the
     static SVG is sufficient for PSDQ.

Then the **review loop** (`research/factory.md`):

6. Owner picks review mode (Mode A, B, or C). Default is Mode A.
7. AI runs the chosen mode's review steps and iterates to convergence.
8. Exit condition: AI self-convergence under Mode A; spot-check approval
   + AI self-convergence under Mode B; owner final-final under Mode C.

Only after the exit condition fires does AI move to the next program.

### Mode A iteration — done 2026-05-07

Owner picked Mode A (AI-only review, the §18 default). Iteration ran
in three passes:

1. **§9.1 self-review + §9.2 critique-pass** — added 2026-05-07
   addendum to `review-internal.md`. 8 critique points raised against
   the new artifacts; written responses to each. One self-found
   correction (B.8 named the wrong top-5 ranking list — fixed in the
   same iteration).
2. **§9.3 red-team synthesis (continued)** — added 2026-05-07
   addendum to `review-external.md`. 6 candidate-institution
   objections on the new artifacts (KEMRI, HeiGIT, WB DECDG, OPHI,
   PIDS, BIDS) with written responses. §18.4 explicit non-claim
   reproduced verbatim.
3. **AI second-opinion code review** (Mode A optional step) —
   `feature-dev:code-reviewer` sub-agent in an independent session
   reviewed the new code and flagged 3 critical + 4 important issues.
   Resolved 3/3 critical and 3/4 important in the same iteration:
   - BARMM crosswalk now enforces a 0.75 winner-share floor
     (`barmm_resolver_admission_stats` records admitted/dropped/
     skipped per crosswalk load)
   - `inspect-barmm-codes.py` warnings are now scoped, not module-wide
   - `retrieved_at` reads from `versions.json` (stable across clean
     clones), not file mtime
   - `build-choropleth.py` now fails loudly on unjoined polygons
     (`_check_join_or_fail`) instead of producing all-grey maps
   - `build-slides.mjs` now uses `execFileSync` with argv (no shell
     interpolation)
   - `build-review-packet.mjs` now exits non-zero if `versions.json`
     missing
   - exposure_proxy=0 collapse documented inline
4. **`limitations.md` §7 added** — 6 new unresolved-residue items
   carried over from the addendum (8-record BARMM residue, regex
   pattern set, simplification tolerances, PSA workbook re-host,
   caveat-loss across tiers, BGD ADM1 N=8).

Exit condition: AI cannot find a further substantive critique on the
listed artifacts. PSDQ is **ai-first finished for current issue**
under Mode A. The artifact remains upgrade-eligible to human-final
via §18.5 (owner-only steps: line-by-line paper reading, real
reviewer contact, owner-signed commit).

The 2026-05-07 review packet at
`review-packets/public-service-data-quality-2026-05-07/` (and `.zip`,
6.1 MB) reflects this state. The reviewer who receives this packet
sees both the 2026-04-25 reviews and the 2026-05-07 Mode A addenda
in `review-internal.md` and `review-external.md`.

## Current blockers

- **10 ADM3 rows still without a source match** in the Philippines poverty
  overlay: Special Geographic Area rows, City of San Juan, Palawan Kalayaan.
  Kept explicit and non-imputed.
- **257 unresolved Philippines NHFR records** after direct-code + PSA PSGC
  correspondence resolution. Below human-final threshold; needs targeted
  source review before any human-final claim.
- **Human-final maturity** is owner-only per §18.5: line-by-line paper
  reading, external reviewer contact (Macharia / Zipf / PIDS / BIDS),
  internal review with Arturo, owner-signed commit. Cannot be reached
  through AI-only review (Mode A).
- **India and Indonesia extensions** are scope-gated until a public
  facility-registry path exists (India) or owner-provisioned SATUSEHAT
  access exists (Indonesia).

## Handoff prompt

Use this to continue a fresh session focused on PSDQ:

```text
Read research/STATUS.md and public-service-data-quality/STATUS.md, plus
CLAUDE.md and research/factory.md. PSDQ is the active flagship. Continue
the publication-ladder build and the review-loop steps listed in
public-service-data-quality/STATUS.md. State the chosen review mode
before iterating; default is Mode A under §18 ACTIVE.
```
