# Pipeline-required — Digital Performance

> **Superseded on 2026-07-19.** This historical note documents the retired
> speed-first route. The program now has an executed, exact-year ITU
> availability–use measurement study. Ookla remains a separate future
> performance layer; see `README.md` and `results.md`.

`attestation_chain: n/a`. 2026-04-27.

## Status

This program has SQL files at `luminosity-gap/research/digital-performance/generated/` (`ookla-fixed-2026-q1.sql`, `ookla-mobile-2026-q1.sql`) but no executed output. The SQL targets the Ookla Speedtest by Speedtest Open Data — a parquet file at `s3://ookla-open-data/parquet/performance/`.

**The program does NOT advance under §18 in this session.** It stays at PP (Prepared Pipeline).

## What's needed

1. Pull the Ookla parquet file (~ 2.6 GB for 2026-Q1 fixed + mobile).
   No API key required; CC BY-NC-SA 4.0 license (non-commercial-
   redistribution clause flagged in `data-access-audit.md`).
2. Execute the committed SQL via DuckDB.
3. Output: per-DMC fixed + mobile median download/upload speeds,
   plus a "digital performance gap" measure (e.g., DMCs above WHO/
   ITU broadband threshold).
4. Sensitivity: ±50% on the threshold values.
5. Standard SR-tier evidence packet.

## §18.5 scope

The pipeline is mechanical (SQL execution); the data fetch is the
non-trivial step due to file size. Estimated build effort: 2-3
hours including SR-tier artifact writing.

## Why not now

In-session bandwidth and disk-space considerations. Better done in a
dedicated pipeline session with proper Ookla-data caching.
