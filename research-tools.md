# Research Tools Registry

Curated list of external repos, MCPs, and platforms that materially help
this research program. Each entry includes: what it does, when to use it,
and how it integrates with our governance.

Verified 2026-04-25. New entries get appended; deprecated entries are
struck through, not deleted (so historical context is preserved).

---

## 1. Data ingestion (saves us writing wrappers)

### 1.1 World Bank — Data360 MCP server
- **Repo:** `llnormll/world-bank-data-mcp` ([github](https://github.com/llnormll/world-bank-data-mcp))
- **What it is:** MCP server exposing the World Bank Data360 API (1,000+ economic and social indicators across 200+ countries) directly to LLM agents.
- **Why we want it:** instead of hand-rolling `curl` calls per WDI indicator, an agent (or Claude Code) can query "give me PHL latest poverty %GDP and GDP per capita 2018–2024" through MCP. Cuts the per-program WDI loader to 3 lines.
- **Integration:** add to `.claude/settings.json` as an MCP server when we want agent-driven indicator pulls. Constitution §11 reproducibility still holds — the MCP queries get cached and SHA-manifested.

### 1.2 World Bank — `pipr` (PIP API client)
- **Repo:** `worldbank/pipr` ([github](https://github.com/worldbank/pipr))
- **What it is:** R client for the **Poverty and Inequality Platform** (PIP), the canonical poverty data source replacing PovCalNet.
- **Why we want it:** Program 16 (social protection), Program 14 (remittance × poverty), and any future poverty-focused programs all need PIP. PIP is the primary source for $2.15/day poverty headcounts.
- **Integration:** call from R or via the underlying REST API in Python. Mirror to `obs.country_value` under indicator slug `pip.poverty_headcount_215`.

### 1.3 World Bank — LSMS organisation
- **Repo:** `lsms-worldbank/*` ([github](https://github.com/lsms-worldbank))
- **What it is:** all LSMS-ISA tooling, harmonization scripts, and a longitudinal cross-country agricultural panel for Sub-Saharan Africa.
- **Why we want it:** LSMS surveys are the canonical micro-source for Programs 14 (remittance HH-level), 17 (water/crop), 9 (food prices). Their harmonization scripts save us months.
- **Integration:** clone as git submodule under `external/lsms` when we move past country-aggregate analysis.

### 1.4 Python: `world_bank_data` and `wbdata`
- **Repos:** `mwouts/world_bank_data` ([github](https://github.com/mwouts/world_bank_data)), `OliverSherouse/wbdata`
- **What:** clean Python wrappers for WDI API; pandas-friendly.
- **Why:** replace our hand-rolled `curl + json.load` pattern in 9 program scripts. Single-line indicator pulls.
- **Integration:** add to a `requirements.txt`; refactor `load_wdi(...)` helpers across program scripts.

### 1.5 R: `WDI`
- **Repo:** `vincentarelbundock/WDI` ([github](https://github.com/vincentarelbundock/WDI))
- **What:** the R-language WDI client.
- **Why:** ADBI working papers and many co-authors prefer R. Having the R path alive means we can hand a script to an external collaborator without forcing Python on them.

---

## 2. Literature & citation (the systematic-scan layer)

### 2.1 Academix — multi-source academic search MCP
- **Repo:** `xingyulu23/Academix` ([github](https://github.com/xingyulu23/Academix))
- **What:** unified MCP over OpenAlex + DBLP + Semantic Scholar + arXiv + CrossRef.
- **Why:** Constitution §4.2 requires Tier-A/B systematic literature scans across multiple databases. This is the agent-callable version of that workflow. One query → unified results across 5 databases.
- **Integration:** add as MCP server. When drafting `<program>/literature.md`, agent calls Academix, then human owner reviews per Constitution §4.

### 2.2 OpenAlex MCP servers
- **Repos:** `cyanheads/openalex-mcp-server` ([github](https://github.com/cyanheads/openalex-mcp-server)) — 270M publications via STDIO/HTTP
- **Repo:** `hbiaou/openalex-mcp` ([github](https://github.com/hbiaou/openalex-mcp))
- **Why:** OpenAlex is the largest free academic catalog (replaced Microsoft Academic Graph). For per-program literature scans this is the single highest-leverage MCP.
- **Integration:** preferred over Academix when you only want OpenAlex.

### 2.3 paper-search-mcp
- **Repo:** `openags/paper-search-mcp` ([github](https://github.com/openags/paper-search-mcp))
- **What:** MCP for arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, IACR, Semantic Scholar, Crossref, OpenAlex.
- **Why:** broadest source coverage of any single MCP.

### 2.4 Paperlib — local paper library
- **Repo:** `Future-Scholars/paperlib` ([github](https://github.com/Future-Scholars/paperlib))
- **What:** local PDF management with RSS subscription to topic feeds, DOI auto-resolve, BibTeX export.
- **Why:** when the literature.md file points to 30+ entries, you want the PDFs locally. Paperlib is the open-source Mendeley equivalent.

### 2.5 Zenodo
- **Platform:** [zenodo.org](https://zenodo.org)
- **What:** DOI minting + permanent archival for code + data + reports.
- **Why:** Constitution §10.3 requires a Zenodo DOI for every publication-ready claim. Free for research use.
- **Integration:** GitHub → Zenodo auto-DOI on release. Each `<program>/generated/` snapshot at publication-ready becomes a versioned Zenodo deposit.

### 2.6 OSF (Open Science Framework)
- **Platform:** [osf.io](https://osf.io)
- **Why:** preregistration + project management. Constitution §6.1 ("first testable claim committed before data pull") is a poor-man's pre-registration; OSF makes it formal.
- **Integration:** when a program reaches Prepared pipeline, OSF-preregister the falsification condition. Adds a citable timestamp.

---

## 3. Reproducibility & orchestration (when we outgrow plain scripts)

### 3.1 Dagster
- **Repo:** [dagster.io](https://dagster.io) / `dagster-io/dagster`
- **What:** asset-based pipeline orchestration with software-engineering best practices baked in.
- **Why:** when our 14 program scripts become 30+ and we need lineage, asset-level testing, and observability. Dagster's "asset" abstraction maps 1:1 to our `obs.indicator` rows.
- **Integration:** later. Each `process-*.py` becomes a Dagster asset. Sync-to-Supabase becomes a Dagster sensor. Don't migrate prematurely.

### 3.2 DVC (Data Version Control)
- **Repo:** [dvc.org](https://dvc.org)
- **What:** git-like versioning for large data files.
- **Why:** our `.cache/research/` is 110+ MB and growing. Once we add EE rasters, will exceed GitHub's 100 MB file cap. DVC tracks data hashes in git but stores files on S3/GCS/local.
- **Integration:** when total cache exceeds 1 GB.

### 3.3 World Bank — Reproducible Research Initiative
- **Org:** [github.com/worldbank](https://github.com/worldbank/reproducible-research-policy)
- **What:** WB's institutional standards for reproducible development-economics research.
- **Why:** our Constitution §11 borrows ideas from this; cross-checking against WB conventions makes our outputs ADB-and-WB-publishable without methodology pushback.

### 3.4 reproduciblework — `aeturrell/example-reproducible-research`
- **Repo:** [github](https://github.com/aeturrell/example-reproducible-research)
- **What:** template repo from the *Coding for Economists* book.
- **Why:** worth a once-over for how a clean repro-research repo is laid out; we can borrow ideas if useful.

---

## 4. Methodology (poverty / measurement-gap-specific)

### 4.1 thinkingmachines/ph-poverty-mapping
- **Repo:** [github](https://github.com/thinkingmachines/ph-poverty-mapping)
- **What:** Philippines-specific poverty mapping using ML + satellite + OSM, by Thinking Machines (PH-based data lab).
- **Why:** **directly relevant**. ADB DMC focus, OSM+satellite combination, Philippines pilot — same shape as Program 13 and Program 4. Look at their data-prep scripts as a reference implementation.

### 4.2 dime-worldbank/big-data-poverty-estimation
- **Repo:** [github](https://github.com/dime-worldbank/big-data-poverty-estimation)
- **What:** ML models that ingest DHS + satellite + OSM + Facebook HRSL to estimate poverty at sub-national scale.
- **Why:** combines the same data sources we already have access to (DHS, OSM, HRSL via §3 of `data-access-audit.md`). Their feature engineering is a head-start for any future ML-based program (P4, P6).

### 4.3 nealjean/predicting-poverty
- **Repo:** [github](https://github.com/nealjean/predicting-poverty)
- **What:** the seminal Jean et al. 2016 *Science* paper code — satellite + machine learning → poverty.
- **Why:** classic reference. Replication-quality. If we need to motivate a "satellite as poverty proxy" claim, this is the canonical citation.

### 4.4 Joaquin Salas — `joaquinsalas/poverty`
- **Repo:** [github](https://github.com/joaquinsalas/poverty)
- **What:** Sentinel-2 + ML for Mexico poverty mapping. Includes NN, SVR, XGBoost regressions vs. census poverty.
- **Why:** more recent than Jean et al; uses publicly accessible Sentinel-2 (which we now have via Earth Engine).

### 4.5 OPHI methodology
- **Org:** Oxford Poverty and Human Development Initiative
- **What:** the Alkire-Foster MPI methodology + R/Stata implementation
- **Why:** Program 0 (MPI × NTL with Arturo) lives here. OPHI publishes their methodology in working papers and implementation notes; a serious MPI program must follow these.

---

## 5. Autonomous / agent-driven research (use with caution)

### 5.1 karpathy/autoresearch
- **Repo:** [github](https://github.com/karpathy/autoresearch)
- **What:** AI agent runs nanochat training experiments unsupervised; one GPU, one file (`train.py`), one metric (val_bpb).
- **Verdict:** **not directly applicable.** This is an ML-training experiment loop. Our work is human-in-loop measurement research.
- **What's worth borrowing:** the `program.md` skill-style design — a single Markdown that holds instructions + constraints + stopping criteria. We adopt this pattern as `.claude/skills/<task>.md` for repeatable agent tasks.

### 5.2 AutoResearchClaw
- **Repo:** `aiming-lab/AutoResearchClaw` ([github](https://github.com/aiming-lab/AutoResearchClaw))
- **What:** "fully autonomous research from idea to paper" — multi-agent peer review, LaTeX paper generation, real literature from OpenAlex/Semantic Scholar/arXiv.
- **Verdict:** **interesting, do not adopt wholesale.** AI-generated papers presented as research violate Constitution §2.5 (AI does not generate empirical numbers) and §12 (AI may not advance maturity labels). We can borrow individual tools (literature ingestion, related-work auto-summary) without buying into the autonomous pipeline.

---

## 6. Adoption order

When you're ready to integrate beyond what we've already built:

1. **OpenAlex MCP** — biggest single-step gain for §4.2 systematic literature scans. Enables `claude` to do tier-A/B database searches programmatically.
2. **World Bank Data360 MCP** — replaces hand-rolled WDI loaders across 9 program scripts.
3. **Zenodo + GitHub release** — DOI minting for the first Screening-Result-promoted program.
4. **Paperlib** — once `references.bib` exceeds ~30 entries.
5. **DVC** — when `.cache/` exceeds 1 GB.
6. **Dagster** — when scripts exceed 30 programs, or when we hire a second analyst.

Don't adopt these preemptively. Each adds maintenance burden; pull the trigger only when the friction is real.

---

## 7. Skill files (`.claude/skills/`)

Karpathy-style `program.md` skill files for repeatable research tasks. Each
is an instruction-and-constraint document the agent follows. Stored at
repository root under `.claude/skills/<task>.md`.

To be authored:
- `systematic-literature-scan.md` — runs Tier-A/B/C scan per Constitution §4.2, returns verified BibTeX entries
- `program-onboard.md` — given a program slug, drafts literature.md + scoring.md + first-pass pipeline scaffold
- `multi-country-extend.md` — given a program already at SR for one DMC, extend to additional DMCs using the data-access-audit
- `article-draft.md` — given a program slug + article kind (blog/brief/working_paper), draft `pub.article.body_md` with auto-cited indicators
- `red-team-prompt.md` — generates the review-packet email + checklist for external red-team reviewers per §9.3

---

## Amendment log

- **2026-04-25** — Initial registry. 18 entries across data ingestion (5),
  literature/citation (6), reproducibility/orchestration (4), methodology
  (5), autonomous-research (2), plus an adoption-order recommendation
  and a skill-files plan.
