# The Blindspots Lab — research repository

This repository is a research factory governed by a written constitution. It
produces measurement-gap research on Asian Development Bank developing member
economies (DMCs) using public data only. Each program in the lab is one folder
at the repo root; each program follows a standard evidence-packet template;
every empirical number traces to a committed script and a public source.

The flagship program right now is **public-service-data-quality** (PSDQ): a
two-DMC pilot showing where OpenStreetMap and the official national
health-facility registry disagree, and how the disagreement tracks geography
(rural / conflict-affected). See
[`public-service-data-quality/STATUS.md`](public-service-data-quality/STATUS.md).

## How to read this repository

| If you want… | Read |
|---|---|
| The governance | [`CONSTITUTION.md`](CONSTITUTION.md) — 18 sections, the lab's binding rules |
| The current operating board | [`research/STATUS.md`](research/STATUS.md) — active flagship and session protocol |
| The process manual | [`research/factory.md`](research/factory.md) — program loop, publication ladder, review modes |
| One program | `{program}/README.md`, `{program}/STATUS.md`, `{program}/results.md` |
| The published work | The reader-facing site at `reporting-site/`; deployed routes are listed below |
| Reproducibility | `{program}/REPRODUCE.md` and `manifest.sha256` |
| AI-transparency disclosure | [`luminosity-gap/docs/AI_TRANSPARENCY.md`](luminosity-gap/docs/AI_TRANSPARENCY.md) |

## Operating mode

The lab is currently in **§18 AI-First Operating Mode** (`CONSTITUTION.md`
§18, ACTIVE since 2026-04-25). Under §18, AI executes gate-actions previously
reserved to the human owner. Every artifact carries an `attestation_chain`
field that names the actual review path taken: `ai-first` (AI self-review +
AI red-team synthesis only), `ai-first; owner-spot-checked` (Mode B partial
owner review), or `human-final` (Mode C full owner review + line-by-line
paper reading + real external reviewer contact + owner-signed commit).

This is honest labeling, not a workaround. The label tells a reader how much
trust the artifact has earned. Most artifacts in this repository today are
`ai-first`. The path to `human-final` is documented in each program's
`upgrade-gap.md` and in §18.5 of the Constitution.

## Repository structure

```
Research/
├── CONSTITUTION.md            governance of record (§1–§18)
├── CLAUDE.md, AGENTS.md       AI operating rules
├── README.md                  this file
├── LICENSE                    MIT — for code
├── LICENSE-CONTENT            CC BY 4.0 — for research artifacts
├── references.bib             shared bibliography (BibTeX)
├── versions.json              source version pins
├── manifest.sha256            per-file hash manifest
│
│ === ONE FOLDER PER PROGRAM ===
├── public-service-data-quality/    PR — active flagship
├── access-services/                SR
├── air-monitoring/                 SR
├── invisible-urbanization/         SR
├── coastal-informal-risk/          SR
├── flood-market-access/            SR
├── remittance-resilience/          PP
├── climate-health-workdays/        PP
├── migration-displacement-signals/ PP
├── disaster-recovery-lag/          PP
├── grid-reliability-heat/          PP
├── port-hinterland-friction/       PP
├── social-protection-shock-coverage/ PP
├── water-stress-crop-diversification/ PP
├── school-heat-disruption/         PP
├── food-price-climate-transmission/ PP
├── digital-performance/            PP
├── mpi-nighttime-lights/           H — original Program 0 (co-authored)
│
│ === SUPPORTING ===
├── articles/                  publication-ladder source
│   ├── *.md                   Tier 1 working papers
│   ├── _brief/                Tier 3 briefs
│   ├── _blog/                 Tier 4 blog posts
│   ├── _social/               Tier 5 social cards
│   └── _slides/               Tier 6 Quarto slide markdown
├── reporting-site/            Vite + React + Tailwind public site
├── luminosity-gap/            legacy Next.js site (original Program 0; see its README)
├── research/                  lab-ops files (STATUS, factory, register, decisions)
├── scripts/                   cross-program tooling and gates
├── review-packets/            built reviewer packets
├── _archive/                  retired material kept for the audit trail
└── supabase/                  database schema (long-format observations; mostly inactive)
```

## Per-program template

Every program folder follows the same shape:

```
{program}/
├── README.md                  overview
├── STATUS.md                  per-program operating board
├── REPRODUCE.md               exact rerun commands + cache map
├── literature.md              systematic Tier-A/B/C scan
├── pre-registration.md        frozen claim + falsification + arbitrary-numerics
├── scoring.md                 §3.3 rubric score
├── coverage.md                country/source coverage
├── sensitivity.md             ±50% test matrix + interpretation
├── sensitivity-runs.json      machine-readable sensitivity outputs
├── results.md                 main result + tables
├── limitations.md             what the artifact cannot establish
├── review-internal.md         §9.1+§9.2 self-review (Mode A)
├── review-external.md         §9.3 red-team synthesis (Mode A; AI-synthesized under §18.4)
├── upgrade-gap.md             what blocks human-final
├── pipeline.ts                TypeScript pipeline scaffold
│
├── scripts/                   Python / shell / TS pipelines
├── .cache/                    public-source caches (git-ignored — see .cache/README.md)
└── generated/                 deterministic outputs (CSVs, JSON, charts)
```

Some programs add program-specific extras: `SOURCE-ACTION.md` (manual-download
record), `catchment-upgrade.md` (method note), `SR-to-PR.md` (gate transition
memo). These are program-by-program judgment calls.

## The publication ladder (per `research/factory.md`)

A program is not "done" until every reader-depth has an honest version of
the result that fits its attention budget:

| Tier | Format | Length | Audience |
|---|---|---|---|
| 1. Working paper | Markdown article | 2,000–6,000 words | Peer reviewer, methodological reader |
| 2. Program page | React page on the lab site | n/a | Policy user navigating the site |
| 3. Brief | One-page summary | ~500 words, single chart | ADB-facing decision audience |
| 4. Blog post | Reader-facing narrative | ~600–900 words | General development-economics reader |
| 5. Social card | Tweet-length summary + chart | ≤ 280 chars + alt text | Social distribution |
| 6. Slide deck | Quarto markdown → `.pptx` | 8–15 slides | ADB internal presentation |
| 7. Evidence packet | Full reproducibility bundle | n/a | Reviewer who wants to rerun |

The visualization rule is per-program, not pre-built: each program identifies
the 1–2 visualizations its argument actually needs, and the same chart appears
at every tier from a single source-of-truth Python script.

## The five gates

Run before any maturity-label change:

```bash
node scripts/check-banned-words.mjs
node scripts/check-dmc-framing.mjs
node scripts/check-citations.mjs
node scripts/check-composite-headline.mjs
node scripts/check-wip.mjs
```

These enforce, respectively: §14 banned-words list, §13.3 measurement-gap
framing, §5.3 citation-by-BibTeX-key rule, §6.4 composite-as-headline
prohibition, and §8.1 work-in-progress cap.

## How to reproduce a result

1. Clone the repository.
2. Read the program's `REPRODUCE.md`.
3. Run the cache rehydration: `python {program}/scripts/fetch-*.py`.
4. Run the pipeline: `python {program}/scripts/process-*.py` (or whatever
   `REPRODUCE.md` lists).
5. Compare the regenerated `generated/*.csv` against `manifest.sha256`.
6. Build the site: `cd reporting-site && npm install && npm run build`.

Per CONSTITUTION.md §11, every number that appears in any output must trace
to (a) a committed script, (b) a committed or publicly pinnable source, and
(c) a recorded retrieval timestamp. Numbers that cannot trace this way do
not appear.

## License

This repository uses two licenses:

- **Code** — MIT License. See [`LICENSE`](LICENSE).
- **Research artifacts** (markdown articles, generated CSVs, charts,
  analysis documents under `articles/`, `{program}/results.md`,
  `{program}/limitations.md`, `{program}/literature.md`, etc.) — Creative
  Commons Attribution 4.0 International (CC BY 4.0). See
  [`LICENSE-CONTENT`](LICENSE-CONTENT).

The two-license pattern is standard for research repositories that bundle
software and scholarly content. CC BY 4.0 is consistent with ADB's modern
open-publishing practice. The lab is not an official ADB publication; the
license choice is the lab's, recorded under §13.4 of the Constitution.

## Owner

Repository owner and program owner: Raymond Adofina.
Co-author on Program 0 (mpi-nighttime-lights): Arturo Martinez Jr.
Amendments to the Constitution follow §16.

## Citation

If you cite work from this repository before any program reaches
human-final attestation, please name the artifact's `attestation_chain`
explicitly. For example:

> Adofina, R. (2026). *The OSM-vs-registry gap in Philippine and Bangladeshi
> health facilities*. Blindspots Lab working paper, ai-first attestation
> under CONSTITUTION.md §18.

The lab updates artifact attestation chains as programs progress through
the review modes (Mode A → B → C → human-final). Always cite the version
you actually read.
