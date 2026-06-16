# Deepened result — the wall is the result: who is missing from the speed data

`attestation_chain: ai-first`

This is the deepening pass for a Stage-1 program, and it is honest about why
it produces no figures yet. Unlike the other deepened results in this repo,
there is **no recomputation here, because there is no data on disk to
recompute.** The program holds committed Ookla Speedtest SQL but has never
executed it; no Ookla parquet, no population grid, and no official-coverage
claim are cached. Inventing per-DMC speeds or a blank-tile share would
violate the non-suspendable rule that every empirical number trace to a
committed script hitting a public source. So this pass does two things that
are real: it makes the wall precise, and it commits a runnable pipeline that
computes the keystone the moment the inputs are fetched. Per
`CONSTITUTION.md` §13.3 the object is a measurement / observability gap, not
a country ranking; per §6.4 any composite is triage only.

Runner: `scripts/run-ookla-deepening.py`. Committed SQL it supersedes:
`luminosity-gap/research/digital-performance/generated/ookla-fixed-2026-q1.sql`
and `ookla-mobile-2026-q1.sql`.

## The question

`deep-questions.md` §1.1 and §7 name the keystone: before executing the
committed median-speed SQL, settle whether the median is even measuring the
right population. A Speedtest is run by someone who already owns a capable
device and a connection. The median Ookla speed is therefore conditional on
being a tester — a population that excludes the unconnected, the rural, and
the data-rationed: exactly the people a digital-development gap is about. An
economy with thin rural coverage can post a healthy median precisely because
its unconnected rural population never generates a test. The keystone metric
is the share of each DMC's population living in z16 tiles that produced
**zero** Ookla samples, and the correlation of that blank-tile share with
rurality. If the blank-tile share is large and skewed toward the rural poor,
the planned median-speed product measures the connected and names itself
after the unconnected, and the program should be rebuilt around who is
missing from the data rather than how fast the present testers are.

## DATA WALL — no number can be produced on disk

There is nothing to compute against. The program's `NEGATIVE-RESULT.md`
already records the program as staying at Prepared Pipeline; this pass
confirms why and converts the "why not" into an exact, runnable fetch list.

**What is blocked, named exactly:**

1. **Ookla Speedtest Open Data — fixed + mobile, one quarter (~2.6 GB
   total global parquet).** Access model A: AWS S3, unauthenticated, read
   with the no-sign-request flag. License **CC BY-NC-SA 4.0** —
   non-commercial and share-alike, flagged in `data-access-audit.md` §6, so
   derived products may inform publications but not a commercial product.
   The committed SQL points at the 2026-Q1 fixed and mobile tile files. The
   schema is one row per z16 tile (~610.8 m at the equator) that recorded at
   least one test, carrying per-tile average download, upload, and latency
   plus test and device counts. The decisive property: a tile with zero
   tests has **no row at all**, so the unconnected are invisible in this
   file by construction — which is exactly why the keystone is computed
   against a population grid, not against the Ookla file alone.
2. **WorldPop 100 m constrained population per DMC** (CC BY 4.0, access A,
   `data-access-audit.md` §3.1). This is the denominator that exists
   everywhere, including the blank tiles Ookla omits, and is what turns "a
   tile had no test" into "this many people live where no test was run."
3. **geoBoundaries gbOpen ADM0/ADM1 per DMC** (CC BY 4.0, access A) for
   assigning tiles to DMCs and splitting urban from rural — the committed
   pilot SQL uses crude lon/lat bounding boxes for the Philippines and
   Bangladesh only and computes means, which the runner replaces with real
   boundaries, population-weighted medians, and the full DMC roster.
4. **The missing fourth side — an official-coverage claim** (ITU coverage
   series, or a regulator/operator coverage map). This is the genuinely
   absent input, and it is not large data — it is a *different* dataset the
   program does not yet have. Per `deep-questions.md` §1.3, without it the
   pipeline yields a selection-bias diagnostic, not a measurement gap: the
   repo's premise (§13.3) is claimed-coverage minus measured-presence, and
   only side three of that subtraction (measured presence, via Ookla) is in
   hand. The runner emits a machine-readable flag
   (`official_coverage_side_present: false`) so no downstream step mistakes
   the diagnostic for the gap.

**Blocked status, stated plainly.** The binding constraints, in order: the
local environment has no DuckDB (neither binary nor Python module), so the
committed SQL cannot execute here at all; the ~2.6 GB Ookla fetch plus the
per-DMC WorldPop rasters are a disk-and-bandwidth job that `NEGATIVE-RESULT.md`
explicitly defers to a dedicated pipeline session; and the official-coverage
side is not yet acquired in any form. The Ookla S3 objects themselves are
publicly reachable, so this is not a paywall — it is a tooling-plus-volume
wall on sides one to three, and a genuine missing-dataset wall on side four.
None of these is a hard wall requiring the owner's identity or attestation;
they are work items, and the runner is staged so that work produces real
numbers rather than estimated ones.

**The selection-bias caveat that must shape the analysis.** Even once sides
one to three are fetched and the medians compute cleanly, the median is a
statistic about test-takers. It must never be reported as a population
connectivity figure. The blank-tile share is not a footnote to the speed
product; it is the result that decides whether the speed product is
admissible at all. If most of a DMC's population sits in zero-sample tiles,
the honest headline is the silence, not the speed.

## What the analysis will show once run

The runner computes, per DMC, entirely from the committed public sources:

- **Blank-tile population share** — the population in z16 tiles that appear
  in neither the fixed nor the mobile Ookla file, over total DMC population.
  This is the keystone number; it is currently unknown and is not estimated
  here.
- **Rural-versus-urban blank-tile share** and a panel-level rank correlation
  between blank-tile share and rurality, to test the §1.1 hypothesis that
  the silence concentrates among the rural poor.
- **Population-weighted median fixed and mobile download** over tested tiles
  — the connected-only figure, reported only alongside its blank-tile share
  so it can never stand alone as a coverage claim.
- **±50% sensitivity** (`CONSTITUTION.md` §6.6) on the urban/rural cutoff and
  the tile-binning tolerance, computed deterministically, not attested.

The decision rule is pre-committed: if the blank-tile share is large and
rurality-skewed, the median-speed product is retired or rebuilt around the
missing population joined to side four; if it is small and flat, the speed
product is admissible but still only as performance-conditional-on-use, never
as adoption or affordability. That decision is to be made from the computed
blank-tile share, not from this document.

## What this does and does not settle

- **Settles:** the program cannot ship any empirical figure today; the exact
  inputs, their licenses, and their access models are now pinned; and the
  keystone is a runnable computation rather than a plan.
- **Does not settle:** every empirical question. The blank-tile share, the
  rurality correlation, and the medians are all unknown until the runner
  executes against real inputs.
- **Honestly bounded:** the first three inputs are a tooling-and-volume
  exercise; the fourth (official coverage) is a separate acquisition without
  which this remains a selection-bias diagnostic, not a §13.3 measurement
  gap.

## Reproduce

DuckDB is not installed in this environment; install it, place the inputs
under `digital-performance/.cache/`, then run the keystone computation:

```bash
pip install duckdb
python digital-performance/scripts/run-ookla-deepening.py --year 2026 --quarter 1
```

Run with no inputs to print the precise, current wall and exit without
writing anything (this is the present behavior, and it produces zero
figures):

```bash
python digital-performance/scripts/run-ookla-deepening.py
```
