# Reproduce the public-data-freshness study

`attestation_chain: ai-first` · 2026-07-19

## Environment

- Python 3.11 or newer
- `matplotlib`, `numpy`, and `pandas`
- Public HTTPS access to `api.worldbank.org` for a live refresh

No API key or production database is required. The published source vintage is
held in the repository's centralized committed research cache.

## Rebuild from the pinned cache

From the repository root:

```powershell
python public-data-freshness/scripts/build-freshness-panel.py
python public-data-freshness/scripts/build-figure-dossier.py
```

## Refresh the source vintage

```powershell
python public-data-freshness/scripts/build-freshness-panel.py --refresh
python public-data-freshness/scripts/build-figure-dossier.py
```

A refresh may change values because WDI revises observations and metadata. It
also retries public WDI objects, but it does not retry the documented ADB
Cloudflare access wall or silently replace the archived frozen indicator.

## Expected primary output for the 2026-07-19 vintage

- baseline possible / observed / missing cells: 756 / 709 / 47;
- absolute / relative review cells at three years: 212 / 74;
- disagreement cells and share: 138 / 19.464%;
- production-cycle-only share of absolute review cells: 65.0943%;
- 9 / 18 / 27 indicator disagreement: 24.7887% / 19.4640% / 20.1789%;
- leave-environment-out disagreement: 9.2210%;
- decision: `reshape_to_domain_concentrated_claim`.

## Verification

```powershell
node scripts/verify-manifest.mjs
node scripts/check-versions.mjs
node scripts/check-banned-words.mjs
node scripts/check-dmc-framing.mjs
node scripts/check-article-claims.mjs
```

The source inventory records URLs, retrieval times, response sizes, SHA-256
digests, and cache paths. The panel has one row per frozen economy × indicator
cell, including explicit missing rows. The figure manifest records 12 PNG/SVG
pairs generated only from committed evidence tables.

## Storage and deployment

Raw source objects live under
`luminosity-gap/.cache/research/public-data-freshness/` with provenance
sidecars and manifest hashes. Generated analytical tables, summaries, and
figures live under `public-data-freshness/generated/`. Vercel serves the
publication surface; it is not the research database or source archive.
