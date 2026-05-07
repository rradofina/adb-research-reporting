#!/usr/bin/env node
// scripts/check-citations.mjs
// Enforces CONSTITUTION.md §5.3 and CLAUDE.md — citations are by BibTeX
// key from /references.bib, never by bare URL in the body of an output.
//
// Heuristic: in research outputs (results.md, articles/), a bare URL in
// running prose is flagged. URLs inside <details>, code fences, or
// reference lists are allowed. This is intentionally narrow — the goal
// is to flag pretend-citations like "see https://example.com/study", not
// every URL.

import fs from "node:fs";
import path from "node:path";

const ROOTS = [
  "articles",
  "luminosity-gap/research",
];
const EXTS = [".md", ".mdx"];
const EXCLUDE_DIRS = new Set(["node_modules", ".git", ".cache", "dist"]);

const RESEARCH_FILE_PATTERN = /(results\.md|article\.md|brief\.md)$/i;
const ARTICLE_GLOB = /\barticles\b/;

const URL_RE = /https?:\/\/[^\s)\]>"']+/g;
const ALLOWED_HOSTS = [
  // Citation-style trailing references and DOI links may appear in
  // reference lists.
  "doi.org",
  "zenodo.org",
];

function walk(dir, out = []) {
  let entries;
  try { entries = fs.readdirSync(path.resolve(dir), { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (EXCLUDE_DIRS.has(e.name)) continue;
    const p = path.join(path.resolve(dir), e.name);
    if (e.isDirectory()) walk(p, out);
    else if (EXTS.includes(path.extname(e.name))) out.push(p);
  }
  return out;
}

function scan(file) {
  const text = fs.readFileSync(file, "utf8");
  const lines = text.split(/\r?\n/);
  const findings = [];
  let inFence = false;
  let inDetails = false;
  let inRefSection = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^```/.test(line)) inFence = !inFence;
    if (/<details/i.test(line)) inDetails = true;
    if (/<\/details>/i.test(line)) inDetails = false;
    if (/^\s*##\s+(references|bibliography)\b/i.test(line)) inRefSection = true;
    if (/^\s*##\s/.test(line) && !/^\s*##\s+(references|bibliography)\b/i.test(line)) inRefSection = false;
    if (inFence || inDetails || inRefSection) continue;
    if (/<!--\s*style-guide:allow\s+citations\s*-->/i.test(line)) continue;
    const matches = line.match(URL_RE);
    if (!matches) continue;
    for (const m of matches) {
      const host = m.replace(/^https?:\/\//, "").split("/")[0];
      if (ALLOWED_HOSTS.some((h) => host.endsWith(h))) continue;
      findings.push({ line: i + 1, url: m, text: line.trim() });
    }
  }
  return findings;
}

function main() {
  const files = ROOTS.flatMap((r) => walk(r))
    .filter((f) => RESEARCH_FILE_PATTERN.test(f) || ARTICLE_GLOB.test(f));
  let total = 0;
  for (const f of files) {
    const found = scan(f);
    if (found.length === 0) continue;
    const rel = path.relative(process.cwd(), f).replace(/\\/g, "/");
    for (const x of found) {
      console.log(`${rel}:${x.line}: bare URL in prose — ${x.url}\n  → ${x.text}`);
      total++;
    }
  }
  if (total > 0) {
    console.log(`\nFAIL — ${total} bare-URL citation(s). Use BibTeX keys from /references.bib.`);
    process.exit(1);
  }
  console.log(`OK — ${files.length} research files scanned, no bare-URL citations.`);
}

main();
