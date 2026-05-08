#!/usr/bin/env node
// scripts/check-composite-headline.mjs
// Enforces CONSTITUTION.md §6.4 — composite indices may appear in
// outputs but must not headline a program.
//
// Heuristic: scans the headline (first non-blank line after a # or H1) of
// results.md and articles/*.md. Flags if the headline contains "composite",
// "index", "score", "rank", or "ranking".

import fs from "node:fs";
import path from "node:path";

const ROOTS = ["articles", "luminosity-gap/research"];
const TARGET_PATTERNS = [/results\.md$/i, /\.md$/i];
const EXTS = [".md", ".mdx"];
const EXCLUDE_DIRS = new Set(["node_modules", ".git", ".cache", "dist", "review-packets", "_archive", "public"]);

const FORBIDDEN = /\b(composite|index|score|rank|ranking|leaderboard)\b/i;
const ALLOW_RX = /<!--\s*style-guide:allow\s+composite-headline\s*-->/i;

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

function headline(file) {
  const text = fs.readFileSync(file, "utf8");
  const lines = text.split(/\r?\n/);
  // Skip frontmatter
  let i = 0;
  if (lines[0]?.trim() === "---") {
    i = 1;
    while (i < lines.length && lines[i]?.trim() !== "---") i++;
    i++;
  }
  for (; i < lines.length; i++) {
    const m = lines[i].match(/^#\s+(.+)$/);
    if (m) return { line: i + 1, text: m[1].trim() };
  }
  return null;
}

function main() {
  const files = ROOTS.flatMap((r) => walk(r))
    .filter((f) => /(results\.md|article(s\/[^/]+)?\.md)$/i.test(f) || /articles/.test(f));
  let total = 0;
  for (const f of files) {
    const text = fs.readFileSync(f, "utf8");
    if (ALLOW_RX.test(text)) continue;
    const h = headline(f);
    if (!h) continue;
    if (FORBIDDEN.test(h.text)) {
      const rel = path.relative(process.cwd(), f).replace(/\\/g, "/");
      console.log(`${rel}:${h.line}: composite/ranking term in headline — "${h.text}"`);
      total++;
    }
  }
  if (total > 0) {
    console.log(`\nFAIL — ${total} composite-headline occurrence(s). §6.4 prohibits ranking/index headlines.`);
    process.exit(1);
  }
  console.log(`OK — ${files.length} files scanned, headlines clean.`);
}

main();
