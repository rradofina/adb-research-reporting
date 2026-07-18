#!/usr/bin/env node
// scripts/new-program.mjs
// Creates a research-program skeleton from the standard templates.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const TEMPLATE_DIR = path.join(REPO_ROOT, "research", "templates");

const TEMPLATE_MAP = [
  ["literature-review.md", "literature.md"],
  ["pre-registration.md", "pre-registration.md"],
  ["scoring.md", "scoring.md"],
  ["coverage.md", "coverage.md"],
  ["results.md", "results.md"],
  ["sensitivity.md", "sensitivity.md"],
  ["limitations.md", "limitations.md"],
  ["review-internal.md", "review-internal.md"],
  ["review-external.md", "review-external.md"],
];

function usage() {
  console.error('Usage: node scripts/new-program.mjs <slug> "<Program title>"');
  process.exit(2);
}

function assertSafeSlug(slug) {
  if (!/^[a-z0-9][a-z0-9-]{1,80}$/.test(slug)) {
    console.error("Slug must be lowercase letters/numbers/hyphens, 2-81 chars.");
    process.exit(2);
  }
}

function writeIfMissing(file, content) {
  if (fs.existsSync(file)) return;
  fs.writeFileSync(file, content);
}

function main() {
  const [slug, ...titleParts] = process.argv.slice(2);
  const title = titleParts.join(" ").trim();
  if (!slug || !title) usage();
  assertSafeSlug(slug);

  const target = path.resolve(REPO_ROOT, slug);
  if (!target.startsWith(REPO_ROOT + path.sep)) {
    console.error("Resolved target escaped repository root.");
    process.exit(2);
  }
  if (fs.existsSync(target)) {
    console.error(`${slug} already exists; refusing to overwrite.`);
    process.exit(1);
  }

  fs.mkdirSync(target, { recursive: true });
  fs.mkdirSync(path.join(target, ".cache"), { recursive: true });
  fs.mkdirSync(path.join(target, "generated"), { recursive: true });
  fs.mkdirSync(path.join(target, "scripts"), { recursive: true });

  writeIfMissing(
    path.join(target, "README.md"),
    `# ${title}\n\n**Status:** Hypothesis.\n\n## Research question\n\nTODO.\n\n## Why this belongs in the factory\n\nTODO: identify the measurement gap, target users, and marginal contribution.\n\n## Public data plan\n\n| Source | Indicator | Unit | License | Retrieval plan |\n|---|---|---|---|---|\n| TODO | TODO | TODO | TODO | TODO |\n\n## Reproduce\n\n\`\`\`bash\n# Add deterministic fetch/process commands here.\n\`\`\`\n\n## Current gate\n\nDo not promote beyond Hypothesis until literature, pre-registration, coverage,\nresults, sensitivity, limitations, and review artifacts are filled.\n`,
  );

  for (const [srcName, destName] of TEMPLATE_MAP) {
    const src = path.join(TEMPLATE_DIR, srcName);
    const dest = path.join(target, destName);
    if (!fs.existsSync(src)) {
      console.error(`Template missing: ${src}`);
      process.exit(2);
    }
    fs.copyFileSync(src, dest);
  }

  writeIfMissing(path.join(target, ".cache", ".gitkeep"), "");
  writeIfMissing(path.join(target, "generated", ".gitkeep"), "");
  writeIfMissing(path.join(target, "scripts", ".gitkeep"), "");

  writeIfMissing(
    path.join(target, "REPRODUCE.md"),
    `# Reproduce — ${title}\n\n\`attestation_chain: ai-first\`\n\n## Environment\n\nTODO: pin runtime and package versions.\n\n## Fetch public data\n\n\`\`\`bash\n# TODO: deterministic retrieval command\n\`\`\`\n\n## Build the result\n\n\`\`\`bash\n# TODO: committed processing and sensitivity commands\n\`\`\`\n\n## Verify\n\nTODO: name generated artifacts and checksum command.\n`,
  );
  writeIfMissing(
    path.join(target, "upgrade-gap.md"),
    `# Conclusion and next evidence upgrade — ${title}\n\n\`attestation_chain: ai-first\`\n\n## What the current evidence supports\n\nTODO.\n\n## What it does not support\n\nTODO.\n\n## Highest-value next data object\n\nTODO: name the public data object and the claim it could change.\n`,
  );
  writeIfMissing(
    path.join(target, "figure-plan.md"),
    `# Figure plan — ${title}\n\n\`attestation_chain: ai-first\`\n\nRead \`research/VISUAL-RESEARCH-STANDARD.md\` before filling this plan. A PNG and SVG of the same figure count once.\n\n| Figure | Research role | Literature link | Source object | Unit and coverage | Transform script | Claim test | Uncertainty | Mobile fallback | Status |\n|---|---|---|---|---|---|---|---|---|---|\n| 1 | Observability / coverage | TODO | TODO | TODO | TODO | TODO | TODO | Table | Planned |\n| 2 | Hero / main claim | TODO | TODO | TODO | TODO | TODO | TODO | Table | Planned |\n| 3 | Sensitivity / limitation | TODO | TODO | TODO | TODO | TODO | TODO | Table | Planned |\n\nDo not add a figure whose source object, claim test, and distinct role cannot be named.\n`,
  );

  const articleTemplate = path.join(TEMPLATE_DIR, "article.md");
  if (!fs.existsSync(articleTemplate)) {
    console.error(`Template missing: ${articleTemplate}`);
    process.exit(2);
  }
  const today = new Date().toISOString().slice(0, 10);
  const article = fs.readFileSync(articleTemplate, "utf8")
    .replaceAll("kebab-case-slug", slug)
    .replaceAll("{program-title}", title)
    .replaceAll("{program-slug}", slug)
    .replaceAll("YYYY-MM-DD", today);
  writeIfMissing(path.join(REPO_ROOT, "articles", `${slug}.md`), article);

  console.log(`Created ${slug}`);
  console.log("Next: register the program, start from a public data object and rough visual, fill figure-plan.md, then fill the research-story sections.");
}

main();
