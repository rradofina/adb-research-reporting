# Repository scripts

Deterministic checks and runners that govern this repository. Each script
runs from the repository root with no external dependencies (Node 20+
only). CI executes the gating subset on every PR.

## Gating checks (CI-blocking)

| Script | Constitution ref | Behavior |
|---|---|---|
| `check-banned-words.mjs` | §14 | Fails on any banned phrase in committed prose |
| `check-dmc-framing.mjs` | §13.3 | Fails on forbidden DMC-deficiency framings |
| `check-citations.mjs` | §5.3 | Fails on bare URLs in research outputs |
| `check-composite-headline.mjs` | §6.4 | Fails when a composite/ranking term headlines a result |
| `verify-manifest.mjs` | §11 | Fails on any cache-file SHA-256 mismatch |
| `check-wip.mjs` | §8.1, §18 | Fails when WIP register exceeds 1 PR + 3 SR unless §18 ACTIVE explicitly suspends caps |

## Informational checks

| Script | Behavior |
|---|---|
| `check-versions.mjs` | Reports versions.json sources older than N days (default 180) |
| `coverage-matrix.mjs` | Generates research/coverage-matrix.md from public/data/*.json |
| `verify-showcase-bench.mjs` | Verifies the 20-report showcase registry against committed evidence paths, public audit artifacts, route coverage, and quality/depth records |

## Pipeline drivers

| Script | Behavior |
|---|---|
| `new-program.mjs` | Creates a new research-program skeleton from `research/templates/` |
| `sensitivity-run.mjs` | Runs the §6.6 sensitivity suite for a program; expects `{slug}/sensitivity.json` |

Program-specific pipelines live inside each research folder. Current PSDQ
Python drivers include:

| Script | Behavior |
|---|---|
| `public-service-data-quality/scripts/fetch-phl-sae-poverty.py` | Attempts the PSA 2023 SAE poverty attachment, records Cloudflare/source-access status, accepts `--sae-xlsx <path>` for an official browser-downloaded workbook, and caches PSA OpenSTAT 2023 direct estimates |
| `public-service-data-quality/scripts/build-phl-admin3-poverty-context.py` | Joins official poverty fields onto the Philippines ADM3 context; emits explicit missing-source statuses instead of imputing poverty |

The full PSDQ process and rerun command sequence are documented in
`public-service-data-quality/REPRODUCE.md`.

## Conventions

- Scripts are `.mjs` (ESM Node) with no third-party dependencies.
- Exit code 0 on success. Exit code 1 on policy failure. Exit code 2 on
  configuration error (missing input file, bad arguments).
- All scripts are runnable as `node scripts/{name}.mjs` from repo root.

## Inline opt-out

Each enforcement script honors a single-line opt-out comment per finding:

```markdown
<!-- style-guide:allow banned-words -->
<!-- style-guide:allow dmc-framing -->
<!-- style-guide:allow citations -->
<!-- style-guide:allow composite-headline -->
```

Opt-outs must be logged in the PR description and reviewed by the
supervisor.
