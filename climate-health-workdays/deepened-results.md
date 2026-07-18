# Deepened results — From proxy stability to construct failure

`attestation_chain: ai-first` · 2026-07-18

## The original stability result was real but insufficient

The inherited proxy's leading set changes little under its own ±50% parameter
suite. That establishes internal stability. It does not establish that the
score measures heat-related work loss.

The direct construct check changes the decision. Across 2018–2020, the proxy's
baseline top three and the Lancet heat top three never overlap. Across all 21
year-and-parameter tests, overlap never exceeds one.

## Full-rank evidence

Spearman rank correlations are 0.119 in 2018, 0.119 in 2019, and 0.169 in
2020. The low values are consistent with the leading-set result and show that
the disagreement is not confined to the cutoff.

## Rank reversals

In 2020:

- Afghanistan is proxy rank 2 and heat rank 28.
- Cambodia is proxy rank 15 and heat rank 1.
- India is proxy rank 1 and heat rank 5.
- Myanmar is proxy rank 7 and heat rank 2.
- Thailand is proxy rank 10 and heat rank 3.

These movements identify a construct mismatch, not a policy ranking.

## Unit correction

The Lancet country workbook reports sector totals in thousands of hours and a
separate total rate in hours per employed person. The build script converts
sector totals by ×1,000 and retains `TotalSunWHLpp`. Visual QA caught the
uncorrected scale because per-worker bars initially collapsed near zero.

After correction, India records about 247.4 billion potential heat-loss hours
in 2024 and 419 hours per employed person; Cambodia records about 5.6 billion
and 573 hours per employed person. The correction changes levels, not ranks or
the construct-validation decision.

## Worker denominator repair

The former “exposed outdoor workers” count multiplied an employment share by
total population. It is kept only as an error diagnostic. Using WDI employed
people aged 15+ instead makes the Afghanistan, India, and Bangladesh estimates
close to the Lancet modelled outdoor-worker counts. This does not validate the
proxy; it removes a separate denominator error.

## Decision

The publishable contribution is the negative external validation, not the old
stable ranking. Further national proxy tuning would repeat the wall. The next
claim-enabling object is observed labor behavior.
