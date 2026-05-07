#!/usr/bin/env node
// scripts/refresh-manifest.mjs
// Recomputes SHA-256 for files in manifest.sha256 that mismatch or are
// missing. The owner runs this when a pipeline rerun produces new output
// and the new output is canonical (i.e., the rerun was deliberate, not
// drift the owner needs to investigate).
//
// Constitution §11: manifest is the truthful record of what the
// repository's caches and outputs hash to. AI may recompute the hash
// when files change deterministically. The owner attests in the commit
// message that the rerun was deliberate.
//
// Usage:
//   node scripts/refresh-manifest.mjs --dry-run
//   node scripts/refresh-manifest.mjs --apply
//
// Arguments:
//   --apply   Rewrites manifest.sha256 in place (otherwise dry-run).
//   --filter <substring>  Only refresh entries whose path contains substring.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const MANIFEST = "manifest.sha256";
const apply = process.argv.includes("--apply");
const removeMissing = process.argv.includes("--remove-missing");
const fi = process.argv.indexOf("--filter");
const filter = fi >= 0 ? process.argv[fi + 1] : null;

if (!fs.existsSync(MANIFEST)) {
  console.error(`${MANIFEST} missing`);
  process.exit(1);
}

const sha256 = (file) => {
  const h = crypto.createHash("sha256");
  h.update(fs.readFileSync(file));
  return h.digest("hex");
};

const lines = fs.readFileSync(MANIFEST, "utf8").split(/\r?\n/);
const out = [];
let updated = 0;
let unchanged = 0;
let missing = 0;

for (const raw of lines) {
  const m = raw.match(/^([0-9a-fA-F]{64})\s+\*?(.+)$/);
  if (!m) { out.push(raw); continue; }
  const expected = m[1].toLowerCase();
  const rel = m[2].replace(/\\/g, "/");
  if (filter && !rel.includes(filter)) { out.push(raw); continue; }

  // Try repo-root and luminosity-gap/ as bases (matches verify-manifest.mjs).
  const candidates = [rel, path.join("luminosity-gap", rel)];
  let resolved = null;
  for (const c of candidates) if (fs.existsSync(c)) { resolved = c; break; }

  if (!resolved) {
    if (removeMissing) {
      console.warn(`REMOVE  ${rel}  (file no longer exists)`);
      missing++;
      continue;  // skip pushing — entry is dropped
    }
    console.warn(`MISS    ${rel}  (cannot recompute — file missing; --remove-missing to drop)`);
    missing++;
    out.push(raw);
    continue;
  }

  const actual = sha256(resolved);
  if (actual === expected) {
    unchanged++;
    out.push(raw);
    continue;
  }
  console.log(`UPDATE  ${rel}\n  was ${expected}\n  now ${actual}`);
  out.push(`${actual} *${rel}`);
  updated++;
}

console.log(`\n${updated} entries to update, ${unchanged} unchanged, ${missing} missing.`);
if (!apply) {
  console.log("Dry run. Re-run with --apply to write manifest.sha256.");
  process.exit(0);
}
if (updated === 0 && missing === 0) {
  console.log("Nothing to apply.");
  process.exit(0);
}
fs.writeFileSync(MANIFEST, out.join("\n"));
console.log(`Wrote ${MANIFEST}.`);
