#!/usr/bin/env node
// scripts/check-banned-words.mjs
// Enforces CONSTITUTION.md §14 — banned words in any output.
// Exits 0 if clean, 1 if any banned word is present.
//
// Run from repository root:
//   node scripts/check-banned-words.mjs
//
// To opt out for a single occurrence (logged in the PR description):
//   <!-- style-guide:allow banned-words -->

import fs from "node:fs";
import path from "node:path";

// Banned phrases. Whole-word match, case-insensitive. The `wordBoundary`
// flag controls whether we match as a word or as a substring.
const BANNED = [
  { phrase: "revolutionary", wordBoundary: true },
  { phrase: "unprecedented", wordBoundary: true },
  { phrase: "game-changing", wordBoundary: true },
  { phrase: "game changing", wordBoundary: false },
  { phrase: "groundbreaking", wordBoundary: true },
  { phrase: "world-class", wordBoundary: true },
  { phrase: "world class", wordBoundary: false },
  { phrase: "cutting-edge", wordBoundary: true },
  { phrase: "cutting edge", wordBoundary: false },
  { phrase: "state-of-the-art", wordBoundary: true },
  { phrase: "state of the art", wordBoundary: false },
  { phrase: "best-in-class", wordBoundary: true },
  { phrase: "best in class", wordBoundary: false },
  { phrase: "paradigm shift", wordBoundary: false },
  { phrase: "paradigm-shift", wordBoundary: true },
  { phrase: "paradigm-shifting", wordBoundary: true },
];

// Files to scan. Globs are not used so this script has no dependencies.
const ROOTS = [
  ".",
  "luminosity-gap/research",
  "reporting-site/src/pages",
  "reporting-site/src/components",
  "articles",
];

const EXTS = [".md", ".tsx", ".ts", ".mdx"];
const EXCLUDE_DIRS = new Set([
  "node_modules",
  ".git",
  ".cache",
  "dist",
  "build",
  ".next",
  ".vercel",
  "generated",
  // review packets are verbatim file snapshots; the source files are
  // already checked at their canonical paths.
  "review-packets",
  // _archive holds frozen historical artifacts; the live source is
  // checked at its canonical path.
  "_archive",
  // reporting-site/public/docs holds verbatim sync of CONSTITUTION.md
  // and other governance docs (sync-docs.mjs); checking them again
  // produces false positives because §14 of the Constitution names
  // the very banned words it prohibits.
  "docs",
  // reporting-site/public/articles is the synced article output from
  // sync-articles.mjs; the source files in articles/ are already scanned.
  "public",
]);
const EXCLUDE_FILES = new Set([
  // The style guide itself lists banned words — must not flag itself.
  "research/style-guide.md",
  "scripts/check-banned-words.mjs",
  // Constitution lists them as banned by name.
  "CONSTITUTION.md",
  "CLAUDE.md",
  // Skill files are meta-content for AI assistants and legitimately
  // list banned words for instructional purposes (the avoid-list).
  ".claude/skills/arturo-martinez-style.md",
  ".claude/skills/wb-decdg-spi-style.md",
  ".codex/skills/adb-erdi-research-style/SKILL.md",
]);

function walk(dir, out = []) {
  const abs = path.resolve(dir);
  let entries;
  try {
    entries = fs.readdirSync(abs, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (EXCLUDE_DIRS.has(e.name)) continue;
    const p = path.join(abs, e.name);
    const rel = path.relative(process.cwd(), p).replace(/\\/g, "/");
    if (EXCLUDE_FILES.has(rel)) continue;
    if (e.isDirectory()) walk(p, out);
    else if (EXTS.includes(path.extname(e.name))) out.push(p);
  }
  return out;
}

// Opt-out: a comment containing `style-guide:allow banned-words`
// anywhere in the file suppresses banned-words for that file. Author
// must justify in the comment. Logged in PR description.
const ALLOW_RX = /style-guide:allow\s+banned-words/i;

function scan(file) {
  const text = fs.readFileSync(file, "utf8");
  if (ALLOW_RX.test(text)) return [];
  const lines = text.split(/\r?\n/);
  const findings = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (const b of BANNED) {
      const re = b.wordBoundary
        ? new RegExp(`\\b${escape(b.phrase)}\\b`, "i")
        : new RegExp(escape(b.phrase), "i");
      if (re.test(line)) {
        findings.push({ line: i + 1, phrase: b.phrase, text: line.trim() });
      }
    }
  }
  return findings;
}

function escape(s) {
  return s.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
}

function main() {
  const files = ROOTS.flatMap((r) => walk(r));
  let total = 0;
  for (const f of files) {
    const found = scan(f);
    if (found.length === 0) continue;
    const rel = path.relative(process.cwd(), f).replace(/\\/g, "/");
    for (const x of found) {
      console.log(`${rel}:${x.line}: banned "${x.phrase}" — ${x.text}`);
      total++;
    }
  }
  if (total > 0) {
    console.log(`\nFAIL — ${total} banned-word occurrence(s) across ${files.length} files scanned.`);
    process.exit(1);
  }
  console.log(`OK — ${files.length} files scanned, no banned words.`);
}

main();
