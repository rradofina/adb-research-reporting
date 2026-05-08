#!/usr/bin/env node
// scripts/sync-docs.mjs
// Mirrors the lab's governance documents into reporting-site/public/docs/
// so they can be rendered in-site (not only on GitHub). The list is the
// "open by default" set: anyone reading the site should be able to read
// the binding rules without leaving for a code host.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const DEST = path.join(REPO_ROOT, "reporting-site", "public", "docs");

// (source path relative to REPO_ROOT, dest filename in public/docs/)
const DOCS = [
  ["CONSTITUTION.md",                "constitution.md"],
  ["CLAUDE.md",                       "operating-rules.md"],
  ["AGENTS.md",                       "agents.md"],
  ["README.md",                       "repo-readme.md"],
  ["LICENSE",                         "license.txt"],
  ["LICENSE-CONTENT",                 "license-content.txt"],
  ["research/factory.md",             "factory.md"],
  ["research/STATUS.md",              "status.md"],
  ["research/wip-register.md",        "wip-register.md"],
  ["red-team.md",                     "red-team.md"],
  ["data-access-audit.md",            "data-access-audit.md"],
  ["sources.md",                      "sources.md"],
  ["versions.json",                   "versions.json"],
  ["manifest.sha256",                 "manifest.sha256"],
];

fs.mkdirSync(DEST, { recursive: true });

const index = [];
for (const [src, dest] of DOCS) {
  const srcPath = path.join(REPO_ROOT, src);
  const destPath = path.join(DEST, dest);
  if (!fs.existsSync(srcPath)) {
    console.warn(`  skip ${src} (not found)`);
    continue;
  }
  fs.copyFileSync(srcPath, destPath);
  const stat = fs.statSync(destPath);
  index.push({
    file: dest,
    source: src,
    size: stat.size,
    size_human: humanBytes(stat.size),
  });
}

fs.writeFileSync(path.join(DEST, "index.json"), JSON.stringify(index, null, 2));
console.log(`Synced ${index.length} doc(s) → ${DEST}/`);

function humanBytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}
