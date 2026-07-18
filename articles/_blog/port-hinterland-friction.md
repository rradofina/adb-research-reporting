---
title: A national proxy failed when vessel time entered the test
slug: port-friction-trade-volume-cluster-blog
program: port-hinterland-friction
attestation_chain: ai-first
maturity: PP
status: draft
---

# A national proxy failed when vessel time entered the test

A country can import a great deal and still operate efficient ports. Another
can handle less trade while vessels spend longer in port. That distinction is
obvious once stated, but it disappeared inside an inherited national screen
that multiplied trade scale by a perceived logistics-performance gap and
called the result port-hinterland friction.

The screen was reproducible. Its label was not yet validated.

## A direct port-time check

The World Bank Container Port Performance Index (CPPI) supplies the missing
port-side object: standardized vessel-time performance at individual ports
[@worldbank2025cppi]. The main test uses 2025 scores, retains ports with at
least 48 sampled calls, and summarizes 65 ports across 13 matched ADB
developing member economies.

The inherited top five were China, India, Indonesia, Viet Nam, and Thailand.
The five weaker CPPI country diagnostics in the main test were Bangladesh,
Georgia, Indonesia, the Philippines, and Cambodia. Only Indonesia appears in
both.

![The inherited ordering changes sharply when observed port time is used.](/programs/port-hinterland-friction/generated/charts/port-rank-inversion.svg)

China moves from inherited rank 1 to observed-disadvantage rank 12. India
moves from 2 to 10. The large-trade cluster is not the weak-port-time cluster.

## The result survives reasonable choices

The analysis changes the CPPI year, the minimum number of sampled calls, and
the way ports are summarized within an economy. The 24- and 72-call variants
are the required ±50% checks around the 48-call baseline. Across all 20
specifications, top-five overlap stays between zero and two; four variants
share no economy with the inherited set.

Correlation does not rescue the original label. The median and lower-quartile
intervals cross zero. The call-weighted association is −0.57, with a 95%
bootstrap interval from −0.83 to −0.11. In the strongest diagnostic, the
inherited “friction” score rises as observed port performance improves.

## What the negative result is good for

This does not make import value or LPI useless. Imports describe exposure and
LPI describes broad perceived logistics conditions. The rejected step is
treating their product as observed port or hinterland friction.

It also does not turn CPPI into a full corridor measure. CPPI ends at the port
boundary. It does not observe the trip to an inland destination, customs
release, route reliability, network impedance, or logistics cost.

World Bank LPI 2.0 identifies the qualified next source: observed shipment
indicators for 2023–2024, including corridor lead time for landlocked economies
[@worldbank2026lpi2]. That interactive file is behind an access challenge in
this environment. Rather than insert another proxy, the study leaves the
hinterland gate visibly open.

The practical lesson is methodological: validate a composite label against a
direct object before polishing its ranking. A negative construct test can save
more analytical effort than another round of tuning.

`attestation_chain: ai-first` · Not externally reviewed.
