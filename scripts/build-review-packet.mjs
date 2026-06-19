#!/usr/bin/env node
// scripts/build-review-packet.mjs
// Builds the evidence packet a program owner emails to external red-team
// reviewers per CONSTITUTION.md §9.3 and red-team.md.
//
// Usage:
//   node scripts/build-review-packet.mjs --program {slug}
//
// Output: review-packets/{slug}-{YYYY-MM-DD}/
//   - README.md (cover letter; lists files + their SHA-256)
//   - {all SR/PR-tier program artifacts}
//   - shared/CONSTITUTION.md, references.bib, red-team.md, versions.json
//   - shared/manifest.sha256 (root manifest)
//   - shared/style-guide.md, research/wip-register.md
//
// The packet is a self-contained snapshot. The reviewer can read it
// without cloning the upstream repository, then optionally clone and
// run the pipeline if they want to verify reproduction.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

const program = arg("program");
if (!program) {
  console.error("Usage: node scripts/build-review-packet.mjs --program <slug>");
  process.exit(2);
}

const programDir = path.resolve(REPO_ROOT, program);
if (!fs.existsSync(programDir)) {
  console.error(`Program folder ${program}/ does not exist at repo root.`);
  process.exit(2);
}

const today = new Date().toISOString().slice(0, 10);
const packetDir = path.resolve(REPO_ROOT, "review-packets", `${program}-${today}`);
fs.mkdirSync(packetDir, { recursive: true });
fs.mkdirSync(path.join(packetDir, "shared"), { recursive: true });
fs.mkdirSync(path.join(packetDir, "program"), { recursive: true });

const PROGRAM_FILES = [
  "README.md",
  "STATUS.md",
  "REPRODUCE.md",
  "SOURCE-ACTION.md",
  "literature.md",
  "scoring.md",
  "pre-registration.md",
  "sensitivity.md",
  "sensitivity.json",
  "sensitivity-runs.json",
  "leave-one-out-runs.json",
  "coverage.md",
  "results.md",
  "source-disagreement-l3-module.md",
  "facility-validation-sample.md",
  "facility-validation-coded-screen.md",
  "facility-validation-ai-review.md",
  "facility-validation-candidate-resolution.md",
  "facility-validation-candidate-public-source-check.md",
  "facility-validation-coordinate-repair.md",
  "facility-validation-public-map-gap.md",
  "facility-validation-public-map-gap-evidence.md",
  "facility-validation-public-map-inspection.md",
  "facility-validation-public-source-confirmation.md",
  "facility-validation-public-source-confirmation-targeted-rows.md",
  "facility-validation-public-source-decision-ledger.md",
  "facility-validation-source-repair-public-evidence.md",
  "limitations.md",
  "upgrade-gap.md",
  "catchment-upgrade.md",
  "review-internal.md",
  "review-external.md",
  "SR-to-PR.md",
  "pipeline.ts",
];

// Publication-ladder tier files in articles/_brief, _blog, _social, _slides.
// The slide-deck source is the markdown; the built .pptx is included as
// a binary artifact under publication/.
const PUBLICATION_TIER_DIRS = ["_brief", "_blog", "_social", "_slides"];

const SHARED_FILES = [
  "CONSTITUTION.md",
  "CLAUDE.md",
  "references.bib",
  "red-team.md",
  "versions.json",
  "manifest.sha256",
  "research/style-guide.md",
  "research/wip-register.md",
  "research/coverage-matrix.md",
];

const sha256 = (file) => {
  const h = crypto.createHash("sha256");
  h.update(fs.readFileSync(file));
  return h.digest("hex");
};

function copyAndHash(src, dest) {
  if (!fs.existsSync(src)) return null;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  if (path.extname(dest).toLowerCase() === ".svg") {
    const text = fs.readFileSync(dest, "utf8");
    fs.writeFileSync(dest, text.replace(/[ \t]+(\r?\n)/g, "$1"));
  }
  return sha256(dest);
}

const programIncluded = [];
for (const f of PROGRAM_FILES) {
  const src = path.join(programDir, f);
  const dest = path.join(packetDir, "program", f);
  const hash = copyAndHash(src, dest);
  if (hash) programIncluded.push({ path: `program/${f}`, sha256: hash });
}

// generated/ as a folder. Recurses one level so generated/charts/ is
// included; skips .log files.
const genSrc = path.join(programDir, "generated");
const genDest = path.join(packetDir, "program", "generated");
if (fs.existsSync(genSrc)) {
  const walk = (s, d, prefix) => {
    fs.mkdirSync(d, { recursive: true });
    for (const f of fs.readdirSync(s).filter((x) => !x.endsWith(".log"))) {
      const src = path.join(s, f);
      const dest = path.join(d, f);
      const stat = fs.statSync(src);
      if (stat.isDirectory()) {
        walk(src, dest, `${prefix}${f}/`);
        continue;
      }
      const hash = copyAndHash(src, dest);
      if (hash) programIncluded.push({ path: `program/generated/${prefix}${f}`, sha256: hash });
    }
  };
  walk(genSrc, genDest, "");
}

// scripts/ as a folder
const scrSrc = path.join(programDir, "scripts");
const scrDest = path.join(packetDir, "program", "scripts");
if (fs.existsSync(scrSrc)) {
  fs.mkdirSync(scrDest, { recursive: true });
  for (const f of fs.readdirSync(scrSrc)) {
    const src = path.join(scrSrc, f);
    const dest = path.join(scrDest, f);
    if (fs.statSync(src).isFile()) {
      const hash = copyAndHash(src, dest);
      if (hash) programIncluded.push({ path: `program/scripts/${f}`, sha256: hash });
    }
  }
}

const sharedIncluded = [];
const missingShared = [];
for (const f of SHARED_FILES) {
  const src = path.join(REPO_ROOT, f);
  const dest = path.join(packetDir, "shared", path.basename(f));
  const hash = copyAndHash(src, dest);
  if (hash) {
    sharedIncluded.push({ path: `shared/${path.basename(f)}`, sha256: hash });
  } else {
    missingShared.push(f);
  }
}
// versions.json is a §11 reproducibility artifact: a reviewer cannot
// rerun the pipeline without the version pins. If it is missing, the
// packet is incomplete — fail loudly rather than ship a packet whose
// reviewers will discover the gap when they try to clone the upstream repo.
if (missingShared.includes("versions.json")) {
  console.error(`FATAL: versions.json missing from ${REPO_ROOT}.`);
  console.error("Reviewers cannot reproduce the pipeline without source-version pins.");
  console.error("Restore versions.json (or the relevant pins) before building the packet.");
  process.exit(2);
}
if (missingShared.length) {
  console.warn(`Warning: ${missingShared.length} shared file(s) missing from packet: ${missingShared.join(", ")}`);
}

// Working paper (Tier 1) — find any article in articles/*.md that has a
// matching `program:` frontmatter field.
const publicationIncluded = [];
const articlesDir = path.join(REPO_ROOT, "articles");
if (fs.existsSync(articlesDir)) {
  for (const f of fs.readdirSync(articlesDir).filter((x) => x.endsWith(".md"))) {
    const text = fs.readFileSync(path.join(articlesDir, f), "utf8");
    const fm = (text.match(/^---\s*\n([\s\S]*?)\n---/) || [])[1] || "";
    const programField = (fm.match(/^program:\s*(.+)$/m) || [])[1]?.trim();
    if (programField === program) {
      const dest = path.join(packetDir, "publication", "1-working-paper", f);
      const hash = copyAndHash(path.join(articlesDir, f), dest);
      if (hash) publicationIncluded.push({ path: `publication/1-working-paper/${f}`, sha256: hash });
    }
  }
}

// Publication-ladder tiers 3-6. Each subdirectory under articles/_*/ is a
// tier; copy any markdown that matches this program slug.
const TIER_LABEL = { _brief: "3-brief", _blog: "4-blog", _social: "5-social", _slides: "6-slides" };
for (const dir of PUBLICATION_TIER_DIRS) {
  const tierSrc = path.join(REPO_ROOT, "articles", dir);
  if (!fs.existsSync(tierSrc)) continue;
  for (const f of fs.readdirSync(tierSrc).filter((x) => x.endsWith(".md"))) {
    const text = fs.readFileSync(path.join(tierSrc, f), "utf8");
    const fm = (text.match(/^---\s*\n([\s\S]*?)\n---/) || [])[1] || "";
    const programField = (fm.match(/^program:\s*(.+)$/m) || [])[1]?.trim();
    if (programField !== program) continue;
    const tierLabel = TIER_LABEL[dir];
    const dest = path.join(packetDir, "publication", tierLabel, f);
    const hash = copyAndHash(path.join(tierSrc, f), dest);
    if (hash) publicationIncluded.push({ path: `publication/${tierLabel}/${f}`, sha256: hash });
  }
}

// Built slide deck (.pptx) from reporting-site/public/programs/{slug}/
const pptxSrc = path.join(REPO_ROOT, "reporting-site", "public", "programs", program, `${program}-deck.pptx`);
if (fs.existsSync(pptxSrc)) {
  const dest = path.join(packetDir, "publication", "6-slides", `${program}-deck.pptx`);
  const hash = copyAndHash(pptxSrc, dest);
  if (hash) publicationIncluded.push({ path: `publication/6-slides/${program}-deck.pptx`, sha256: hash });
}

const cover = `# Review packet — ${program} — ${today}

This is a self-contained snapshot of the evidence the program owner
asks the reviewer to assess. Per CONSTITUTION.md §9.3 and red-team.md.

## How to read this packet (suggested order, by attention budget)

**If you have 2 minutes:** \`publication/5-social/\` (the tweet card).

**If you have 10 minutes:** \`publication/3-brief/\` (one-page brief).

**If you have 20 minutes:** \`publication/4-blog/\` (~750-word narrative
post for a general dev-econ reader) or \`publication/6-slides/*.pptx\`
(the ADB internal slide deck — open in PowerPoint or LibreOffice).

**If you have 90 minutes (full review):**

1. Read \`shared/CONSTITUTION.md\` for the rules every program in the
   lab is governed by. The relevant sections for this review are §6
   (methods), §7 (claim-maturity gates), §9 (review process), §13.3
   (DMC framing), §14 (taste heuristics), and §18 (AI-First Operating
   Mode — currently active; affects attestation chain).
2. Read \`program/README.md\` for the program overview, then
   \`program/STATUS.md\` for the current operating state.
3. Read \`program/literature.md\` for the systematic Tier-A/B/C scan.
4. Read \`program/pre-registration.md\` for the frozen claim,
   falsification condition, and arbitrary-numerics inventory.
5. Read \`program/sensitivity.md\` and \`program/sensitivity-runs.json\`
   for the ±50 percent test results.
6. Read \`program/results.md\` for the screening artifact.
7. Read \`program/limitations.md\` and \`program/upgrade-gap.md\` for
   what the result cannot establish and what blocks human-final.
8. Read \`publication/1-working-paper/*.md\` for the long-form paper.
9. Optionally re-run the pipeline per \`program/REPRODUCE.md\`. Source
   caches and code are under \`program/scripts/\` and \`program/generated/\`.

## What the program owner asks of you

- Read the artifacts in this packet.
- Flag issues on measurement, identification, reproducibility, or
  framing (per Constitution §13.3 — measurement gap, not DMC deficiency).
- Optionally write a short response. The owner commits your written
  comments verbatim alongside written responses, per §9.3.
- Disclose any conflict of interest (per red-team.md §conflict-of-interest).

Estimated reading time: 90–120 minutes for the program artifacts
without re-running the pipeline. Turnaround per red-team.md is 4 weeks
from acceptance.

Credit is by acknowledgment in the published article. You are not an
author. Compensation, if any, follows institutional norms.

## Files in this packet

### Publication ladder

The publication ladder (\`research/factory.md\`) requires every program to
have an honest version of its result at every reader-depth. This packet
includes all six text/binary tiers (the React program page on the lab
website is Tier 2 and is not included here).

${publicationIncluded.map((f) => `- \`${f.path}\`  \`${f.sha256.slice(0, 12)}…\``).join("\n")}

### Program artifacts

${programIncluded.map((f) => `- \`${f.path}\`  \`${f.sha256.slice(0, 12)}…\``).join("\n")}

### Shared governance

${sharedIncluded.map((f) => `- \`${f.path}\`  \`${f.sha256.slice(0, 12)}…\``).join("\n")}

## Manifest

The full SHA-256 of every file in this packet is at \`packet-manifest.sha256\`.

— Generated ${new Date().toISOString()} by \`scripts/build-review-packet.mjs\`.
`;

fs.writeFileSync(path.join(packetDir, "README.md"), cover);

const manifestLines = [
  "# Packet manifest. Each file in this review packet, with SHA-256.",
  ...[...publicationIncluded, ...programIncluded, ...sharedIncluded].map((f) => `${f.sha256} *${f.path}`),
];
fs.writeFileSync(path.join(packetDir, "packet-manifest.sha256"), manifestLines.join("\n") + "\n");

console.log(`Built review packet: ${packetDir}`);
console.log(`  ${publicationIncluded.length} publication-tier files, ${programIncluded.length} program files, ${sharedIncluded.length} shared files.`);
console.log(`\nNext: zip the folder and email to reviewers per red-team.md §outreach-template:`);
console.log(`  cd "${path.dirname(packetDir)}" && zip -r "${path.basename(packetDir)}.zip" "${path.basename(packetDir)}"`);
