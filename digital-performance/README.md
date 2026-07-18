# The network is present. Use still lags.

`attestation_chain: ai-first` · Prepared research paper · 2026-07-19

Across the 34 ADB developing member economies with exact-year ITU observations
in 2024, reported 4G/LTE population coverage exceeds internet use by a median
of **14.3 percentage points**. The difference is positive in 31 cases. Median
coverage is 98.0%; median use is 82.2%.

This is an availability-to-use measurement study. It does not equate signal
range with service quality, affordability, digital skill, or welfare. It also
does not interpret people who are within network range but offline as a single
population with a single barrier.

## Why this replaces the inherited plan

The inherited program proposed downloading roughly 2.6 GB of Ookla tiles and
ranking connected testers by speed. That object can describe performance
conditional on testing, but it cannot measure adoption among people who never
generate a test. The rebuilt study starts with two smaller official objects
that answer the prior question: whether network availability and actual use
coincide.

## Public data objects

- ITU DataHub `i271GA`: population within range of at least a 4G/LTE signal.
- ITU DataHub `i99H`: individuals using the Internet in the previous three
  months.
- ITU DataHub `i271mb_5GB_GNI`: 5 GB mobile-data basket as a share of GNI per
  capita, used as a secondary affordability diagnostic.
- ITU rural and urban internet-use disaggregations, used only where both are
  available for the same economy and year.

Raw responses remain under `.cache/`; the committed source inventory records
their URLs, retrieval times, byte counts, and SHA-256 digests.

## Evidence package

- `generated/digital-performance-coverage-use-panel.csv`: 391 exact-year pairs
  across 39 roster economies, 2012–2024.
- `generated/digital-performance-coverage-use-summary.json`: headline rule,
  coverage, exclusions, and claim guard.
- `generated/digital-performance-source-inventory.json`: retrieval custody.
- `generated/digital-performance-figure-dossier.json`: metrics and 12 earned
  evidence figures.
- `sensitivity-runs.json`: ±50% sample-floor check and secondary diagnostics.

## Reproduce

```powershell
python digital-performance/scripts/build-coverage-use-gap.py --refresh
python digital-performance/scripts/build-figure-dossier.py
```

See `REPRODUCE.md` for the full environment, expected outputs, and verification
checks.
