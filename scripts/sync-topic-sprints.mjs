#!/usr/bin/env node
// Mirror L2 topic-sprint artifacts into reporting-site/public so showcase
// pages can render the same generated evidence packets a reviewer downloads.

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const SRC = path.join(REPO_ROOT, "research", "topic-sprints");
const DEST = path.join(REPO_ROOT, "reporting-site", "public", "topic-sprints");

if (!fs.existsSync(SRC)) {
  console.log("skip sync-topic-sprints (research/topic-sprints not present)");
  process.exit(0);
}

fs.rmSync(DEST, { recursive: true, force: true });
fs.mkdirSync(DEST, { recursive: true });

const copied = [];

copyDir(path.join(SRC, "generated"), path.join(DEST, "generated"));

const reportsDest = path.join(DEST, "reports");
fs.mkdirSync(reportsDest, { recursive: true });
for (const entry of fs.readdirSync(SRC)) {
  if (!entry.endsWith("-sprint.md")) continue;
  const srcPath = path.join(SRC, entry);
  const destPath = path.join(reportsDest, entry);
  fs.copyFileSync(srcPath, destPath);
  copied.push(record(srcPath, destPath));
}

const index = {
  generated_at: new Date().toISOString(),
  source: "research/topic-sprints",
  files: copied.sort((a, b) => a.file.localeCompare(b.file)),
};

fs.writeFileSync(path.join(DEST, "index.json"), JSON.stringify(index, null, 2));
console.log(`Synced ${copied.length} topic-sprint file(s) -> ${DEST}/`);

function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
      copied.push(record(srcPath, destPath));
    }
  }
}

function record(srcPath, destPath) {
  const buffer = fs.readFileSync(destPath);
  const stat = fs.statSync(destPath);
  return {
    file: path.relative(DEST, destPath).replaceAll("\\", "/"),
    source: path.relative(REPO_ROOT, srcPath).replaceAll("\\", "/"),
    size: stat.size,
    size_human: humanBytes(stat.size),
    sha256: crypto.createHash("sha256").update(buffer).digest("hex"),
  };
}

function humanBytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}
