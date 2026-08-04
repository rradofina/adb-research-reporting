---
slug: about-the-lab
title: About the Development Blindspots Lab
subtitle: We measure what official data misses across ADB developing member economies — public sources only, every number from a committed script, every claim under an explicit Constitution.
kind: blog
status: draft
authors:
  - { name: Raymond Adofina, affiliation: Asian Development Bank }
geographies: []
topics: [governance, methodology]
program: meta
maturity: H
abstract: >
  The Blindspots Lab studies the difference between official data and reality
  across Asian Development Bank developing member economies. Public data only.
  Every empirical number traces to a committed script. The current issue uses
  Constitution §18 AI-first attestation, with source lineage, sensitivity checks,
  caveats, and status labels made explicit. This first article describes what
  binds the lab and why it exists.
doi:
published_at: 2026-04-25
updated_at: 2026-07-31
references:
  - sandefur2015badata
  - alkire2024mpi
  - markhof2025records
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
---

# Why the lab exists

Most development research treats published statistics as ground truth and
builds causal inference on top. This lab does the opposite. For each
measurement that policymakers and lenders rely on, we ask how wrong it
could be — and which direction. The answer is rarely small and random.

Sandefur and Glassman 2015 [@sandefur2015badata] documented the political
economy of administrative data in African statistical systems: enrollment
counts persistently overshoot survey-derived counts, the gap correlates
with funding incentives, and the cleanup, if it happens, lags by years.
Markhof and colleagues 2025 [@markhof2025records] found a 9-percentage-
point gap between phone-survey-measured and administrative
COVID-vaccination coverage in low- and middle-income countries that
persists after correcting for respondent-selection effects, suggesting
the gap is in the recordkeeping. These are not isolated failures — they
are the shape of the measurement layer that ADB developing member
economies operate inside.

The lab's program register collects eighteen domains where that layer is
load-bearing: poverty, public-service quality, air quality, climate
exposure, remittances, mobility, school heat days, port-hinterland
friction, food prices, grid reliability, disaster recovery, and others.
Each domain is its own program. Each program is governed by the same
Constitution. Each program targets a specific, falsifiable claim about a
specific measurement gap.

# What the Constitution forces us to do

The Constitution at the upstream repository binds every program. It does
five things a first-time reader should know:

1. It sets the gates between four claim-maturity tiers — Hypothesis →
   Prepared Pipeline → Screening Result → finished for issue (internal
   PR code) — and the exact artifacts each transition requires.
2. It caps work-in-progress at one human-final PR and three
   Screening-Result programs in normal human-final mode. Under §18
   AI-first operating mode, the cap is suspended and the attestation
   chain is labeled instead.
3. It bans composite indices as headline findings. Composite indices may
   appear as triage instruments and are labeled as such.
4. It bans framing findings as country deficiency. The framing is
   measurement gap, coverage gap, or observability gap.
5. It defines AI's role by operating mode. Outside §18, AI is a bounded
   assistant and humans hold every gate. Under current §18 ACTIVE mode,
   AI executes disclosed gate-actions with `attestation_chain: ai-first`;
   human-final status remains owner-only and requires the §18.5 upgrade
   path.

Five additional disciplines anchor the work to the data: every empirical
value traces to a committed script and a public source; every cache file
is hashed in `manifest.sha256`; every external version is pinned in
`versions.json`; every retrieval has a row-level timestamp; and any
arbitrary numeric — threshold, weight, buffer, cutoff — is tested at
±50% before it appears in a finished current-issue claim.

# Where the lab stands today

Of the eighteen registered programs, seven are finished for the current
issue under Constitution §18 AI-first attestation. Eight are Screening
Results: useful empirical signals, but not final research outputs. One
is a Program Prospectus because the PM2.5 layer is computed while the
heat layer remains an upgrade. One is Prepared Pipeline, meaning the
engineering path exists but no empirical claim should be made yet. One
remains Hypothesis inside this repository until the external
nighttime-lights track is reconciled.

The reporting site you are reading is the lab's public face. It separates
the scan-first brief layer from the full evidence packets: each topic
shows the finish state, the chart, the source stack, the caveat, and the
next step before a reader opens the underlying files.

# How to read any output in ninety seconds

A first reader of any program output should look for five things, in
this order:

1. The headline finding — one sentence, no hedges. If the headline is
   a ranking or composite, the program has violated §6.4.
2. The pre-registration commit hash, dated before the pipeline run.
3. The sensitivity table. If the answer flips inside ±50%, the
   conclusion does not survive.
4. The limitations. Verbatim reviewer objections that could not be
   resolved appear here. They are not buried.
5. The replication archive. A clean clone at the frozen tag plus the
   self-hosted archive reproduces every value; a Zenodo DOI remains an
   optional venue-facing deposit.

If any of those five is missing, the program is not finished for the
current issue.

# What comes next

The next work is not to blur the labels. It is to move selected
Screening Results forward one at a time: replace proxies with
policy-grade measures, rerun sensitivity where needed, and convert the
AI-first evidence chain into a human-final paper track only when the
literature, caveats, and replication package are strong enough.

— Raymond Adofina · 2026-07-31
