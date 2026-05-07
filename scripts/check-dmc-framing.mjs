#!/usr/bin/env node
// scripts/check-dmc-framing.mjs
// Enforces CONSTITUTION.md §13.3 — DMC framing.
// Findings frame as measurement gap / coverage gap / observability gap,
// not as DMC deficiency. This check flags forbidden framings.
//
// Heuristic only: it cannot perfectly detect intent. The author resolves
// flags inline with `<!-- style-guide:allow dmc-framing -->`.

import fs from "node:fs";
import path from "node:path";

const FORBIDDEN = [
  { rx: /\b(country|countries|nation|nations) (has|have) poor data\b/i, hint: 'use "the measurement gap for X in {country}"' },
  { rx: /\bunderdeveloped statistical capacity\b/i, hint: 'use "thin observation layer" or "sparse public-data coverage"' },
  { rx: /\bdeficient (country|countries|economy|economies)\b/i, hint: 'use "measurement gap" framing' },
  { rx: /\b(country|countries|economy|economies) (is|are) failing\b/i, hint: 'use "the data does not yet show …"' },
  { rx: /\b(country|countries) lacking proper records\b/i, hint: 'use "public records for X are not yet available"' },
  { rx: /\b(country|countries) (is|are) behind on\b/i, hint: 'use "{country} carries less public data on …"' },
  { rx: /\bfailing (country|countries|economy|economies)\b/i, hint: 'use "measurement gap" framing' },
  { rx: /\bweak (country|countries|economy|economies)\b/i, hint: 'use "the data does not yet show …"' },
];

const ROOTS = [
  ".",
  "luminosity-gap/research",
  "reporting-site/src/pages",
  "reporting-site/src/components",
  "articles",
];
const EXTS = [".md", ".tsx", ".ts", ".mdx"];
const EXCLUDE_DIRS = new Set(["node_modules", ".git", ".cache", "dist", "build", ".next", ".vercel", "generated", "review-packets"]);
const EXCLUDE_FILES = new Set([
  "research/style-guide.md",
  "scripts/check-dmc-framing.mjs",
  "CONSTITUTION.md",
  "CLAUDE.md",
]);

function walk(dir, out = []) {
  let entries;
  try { entries = fs.readdirSync(path.resolve(dir), { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (EXCLUDE_DIRS.has(e.name)) continue;
    const p = path.join(path.resolve(dir), e.name);
    const rel = path.relative(process.cwd(), p).replace(/\\/g, "/");
    if (EXCLUDE_FILES.has(rel)) continue;
    if (e.isDirectory()) walk(p, out);
    else if (EXTS.includes(path.extname(e.name))) out.push(p);
  }
  return out;
}

// File-level opt-out: a comment containing `style-guide:allow dmc-framing`
// anywhere in the file suppresses dmc-framing for that file.
const ALLOW_RX = /style-guide:allow\s+dmc-framing/i;

function scan(file) {
  const text = fs.readFileSync(file, "utf8");
  if (ALLOW_RX.test(text)) return [];
  const lines = text.split(/\r?\n/);
  const findings = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (const f of FORBIDDEN) {
      if (f.rx.test(line)) {
        findings.push({ line: i + 1, hint: f.hint, text: line.trim() });
      }
    }
  }
  return findings;
}

function main() {
  const files = ROOTS.flatMap((r) => walk(r));
  let total = 0;
  for (const f of files) {
    const found = scan(f);
    if (found.length === 0) continue;
    const rel = path.relative(process.cwd(), f).replace(/\\/g, "/");
    for (const x of found) {
      console.log(`${rel}:${x.line}: framing — ${x.hint}\n  → ${x.text}`);
      total++;
    }
  }
  if (total > 0) {
    console.log(`\nFAIL — ${total} forbidden DMC-framing occurrence(s).`);
    process.exit(1);
  }
  console.log(`OK — ${files.length} files scanned, DMC framing clean.`);
}

main();
