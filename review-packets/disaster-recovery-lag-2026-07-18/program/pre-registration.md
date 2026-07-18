# Pre-registration and claim-reshape record

`attestation_chain: ai-first` · Frozen 2026-07-18 before the full daily-orbit extraction

## Why the original claim was retired

The inherited claim named China and India as a metric-stable disaster-burden
top two. Its recorded kill rule required retraction if any alternative metric
changed at least one member. Events per year, total deaths, and events per
million all trigger that rule. The public article therefore does not preserve
the old headline.

## Research question

Can GDIS administrative centroids joined to public daily VIIRS-DNB radiance
produce a stable recovery month for Typhoon Haiyan under reasonable choices of
spatial window, reducer, recovery threshold, and persistence?

## Frozen pilot

- Event: Typhoon Haiyan, GDIS disaster number `2013-0433`, 8 November 2013.
- Units: seven GDIS administrative centroids—Aklan, Capiz, Cebu, Iloilo,
  Leyte, Palawan, and Samar.
- Window: May 2013–October 2014; six scheduled dates per month, 108 in all.
- Quality: valid radiance, confidently clear, nighttime, no stray light,
  lightning, or no-data flag.
- Main specification: 50 km square half-width, mean radiance, same-orbit Manila
  reference, 90% of the pre-event baseline, sustained for two months.
- Valid month: at least two paired nights and 25 valid pixels per window.

## Positive rule

The construct validates only if at least three centroids have four or more
valid baseline months, an identified main-specification recovery month, and
the same month under every radius, reducer, threshold, and persistence variant.

## Required sensitivity

Radius 25/50/75 km and persistence one/two/three months implement the required
±50% tests. Reducer varies between mean and p75; threshold varies among
80/90/100%. The cross-product yields 54 variants per centroid.

## Decision labels

- **Validated:** the positive rule passes.
- **Not validated:** the rule fails, but the source remains potentially usable
  after better footprints, baselines, or auxiliary outcomes.
- **Infeasible:** public extraction cannot be completed.

The observed outcome is **not validated**. This label was fixed before the
reader-facing narrative was written.
