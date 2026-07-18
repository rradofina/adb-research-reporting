# Limitations and nonclaims — air-monitoring public QA observability

`attestation_chain: ai-first`. Updated 2026-07-19.

1. **Bounded public routes.** The finding applies to the named public sources
   and retrieval states in the committed ledger. It does not show that the
   missing records do not exist elsewhere.
2. **No private evidence.** Internal regulator QA files, credentialed portals,
   and nonpublic station logs are outside the public-data-only scope.
3. **Metadata is not certification.** Owner, provider, instrument, `isMonitor`,
   method, and dashboard-status fields help discovery but do not automatically
   validate station identity, calibration, inspection, or current grade.
4. **No same-station assumption.** Proximity and name similarity produce
   candidates, not validated joins.
5. **No coverage or exposure estimate.** The 831 denominator joins are geometry
   and custody checks until identity and monitor-grade gates close.
6. **No regulator or country ranking.** Differences in public evidence may
   reflect publication systems, language, archive design, or the audit frame;
   they are not performance scores.
7. **No causal inference.** The study does not estimate health effects,
   pollution determinants, monitor effects, or policy impacts.
8. **Dynamic public sources.** Dashboards and APIs can change after retrieval.
   Future releases should be treated as claim-changing evidence and versioned.

The public article should therefore use “not verifiable in the audited packet,”
not “does not exist.”
