---
slug: pm25-observability-gap-cluster-blog
title: A station dot is not yet a coverage claim
subtitle: Across 24 economies, public monitor routes are visible—but not one station completes the chain needed for a verified population-coverage claim.
kind: blog
tier: blog
status: draft
attestation_chain: ai-first
constitution_ref: §18 ACTIVE 2026-04-25
authors: [{ name: Raymond Adofina, affiliation: Asian Development Bank }]
geographies: [regional]
topics: [air-quality, PM2.5, open-data, measurement]
program: air-monitoring
maturity: SR
abstract: >
  Public monitoring routes are easier to find than public station-level
  quality evidence. The study documents exactly where the chain breaks.
references: [who2026monitoring, openaq2026locations]
license: CC BY 4.0
banned_words_check: passing
dmc_framing_check: passing
updated_at: 2026-07-31
---

# The tempting map

Air-quality portals can produce a persuasive map in minutes: station dots,
PM2.5 readings, circles around locations, and population beneath those circles.
The hard question comes before the map. Does each dot represent a traceable,
current, quality-assured station—and can the same physical station be matched
across the official and aggregated sources?

![The audit reaches geometry, then stops at station identity](/programs/air-monitoring/generated/charts/air-monitoring-claim-ladder.svg)

# Not one station completes the chain

The public packet covers 24 economies and audits 239 official station rows. It
checks 44 official/OpenAQ identity candidates and computes 831 denominator
joins. The results that would authorize a coverage claim are all zero: no
validated same-station rows, complete quality-assured monitor rows,
station-radius-ready economies, or allowed coverage claims.

That does not mean the stations or QA records do not exist. It means the named
public routes do not expose enough joinable evidence to verify the intended
coverage claim.

# Why online is not the same as verified

The BMKG lane makes the distinction concrete. Twenty-two target rows have
method, display, and status context, and 21 appear online in the audited
dashboard. Yet the packet has no public station-specific inspection log,
calibration certificate, calibration-status row, or complete quality-assured
monitor row for that target queue.

![BMKG visibility does not close station-level QA](/programs/air-monitoring/generated/charts/air-monitoring-bmkg-closure.svg)

# The useful negative result

The study's output is not an empty page. It is a falsifiable boundary. A public
station certificate, inspection log, current calibration-status row, official
crosswalk, or station-keyed method-and-grade record changes the finding. Another
radius or another generic portal search does not.

![The evidence that would change the result is explicit](/programs/air-monitoring/generated/charts/air-monitoring-overturning-evidence.svg)

That is the value of working backward from the claim: data availability is
tested before a visually attractive but unsupported coverage story is allowed.
