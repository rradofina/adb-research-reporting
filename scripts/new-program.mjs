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
  ["article.md", "article.md"],
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

  console.log(`Created ${slug}`);
  console.log("Next: fill README.md, literature.md, pre-registration.md, then add deterministic scripts.");
}

main();
