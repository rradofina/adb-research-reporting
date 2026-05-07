# Zenodo deposition

Per `CONSTITUTION.md` §10. Every Publication-Ready program deposits a
replication archive on Zenodo before the gate is closed. The DOI is
recorded in the article frontmatter and in the program's `results.md`.

---

## Deposition checklist (§10)

1. Repository at the frozen commit hash. Tag the commit as
   `{slug}-pr-{YYYY-MM-DD}`.
2. Build the archive:
   ```bash
   git archive --format=zip --prefix={slug}/ {tag} \
     {slug}/ research/ scripts/ versions.json manifest.sha256 \
     references.bib CONSTITUTION.md > {slug}-pr-{YYYY-MM-DD}.zip
   ```
3. Reserve a DOI on Zenodo Sandbox first; verify the deposition
   metadata renders. Then promote to Zenodo production.
4. Upload the archive to Zenodo. Use the metadata template at
   `research/templates/zenodo-metadata.json`, filling every `{}`.
5. After deposition, record the DOI in:
   - `articles/{program}/{article-slug}.md` frontmatter (`doi:` and
     `zenodo:` blocks)
   - `{slug}/results.md` §6
   - `research/zenodo/{slug}.json` (committed copy of the deposition
     metadata as accepted by Zenodo)

## Why Zenodo

- Long-lived (CERN-backed); 20-year preservation guarantee.
- Open-license-friendly: CC BY 4.0 is the default for the lab.
- Versioned: a future replication archive supersedes by minting a new
  DOI under the same concept DOI.
- Free for any researcher; no institutional gating.

## Banned in deposition

- Any file containing API keys, service-role secrets, or credentials
  (`*.key`, `adb-research-*.json`, `.env*`).
- Source files where the upstream license forbids redistribution
  (CC BY-NC-SA derivatives — Ookla, ACAG, Kyrgyz NSC).

The `scripts/zenodo-deposit.mjs` helper does a final scan and refuses
to upload if either condition triggers.
