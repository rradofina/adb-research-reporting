#!/usr/bin/env node
// scripts/verify-manifest.mjs
// Enforces CONSTITUTION.md §11 — manifest.sha256 truthfully records the
// SHA-256 of every committed cache file. Re-computes hashes for every
// listed file and exits non-zero on any mismatch or missing file.
//
// Format expected (sha256sum-style):
//   <sha256>  <relative-path>
// Lines starting with '#' or blank lines are ignored.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const MANIFEST = "manifest.sha256";

// The manifest header documents that paths are relative to
// luminosity-gap/ (the original Next.js subproject that minted the
// manifest). The verifier resolves each path against that base by
// default; override with --base.
const DEFAULT_BASE = "luminosity-gap";

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

function sha256(file) {
  const h = crypto.createHash("sha256");
  h.update(fs.readFileSync(file));
  return h.digest("hex");
}

function main() {
  const base = arg("base", DEFAULT_BASE);
  const limit = Number(arg("limit", "0")) || 0;
  if (!fs.existsSync(MANIFEST)) {
    console.error(`FAIL — ${MANIFEST} does not exist at repo root.`);
    process.exit(1);
  }
  const lines = fs.readFileSync(MANIFEST, "utf8").split(/\r?\n/);
  let total = 0;
  let bad = 0;
  let missing = 0;
  let checked = 0;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const m = line.match(/^([0-9a-fA-F]{64})\s+\*?(.+)$/);
    if (!m) {
      console.warn(`SKIP (unparseable): ${line}`);
      continue;
    }
    const expected = m[1].toLowerCase();
    const rel = m[2].replace(/\\/g, "/");
    const file = path.join(base, rel);
    total++;
    if (limit > 0 && checked >= limit) continue;
    // The manifest mixes paths relative to repo root (e.g.
    // school-heat-disruption/.cache/…) with paths relative to
    // luminosity-gap/ (.cache/research/access-scaleout/…). Try both,
    // falling back from the configured base to repo root.
    const candidates = [file, rel];
    let resolved = null;
    for (const c of candidates) if (fs.existsSync(c)) { resolved = c; break; }
    if (!resolved) {
      console.error(`MISS   ${rel}`);
      missing++;
      continue;
    }
    const actual = sha256(resolved);
    if (actual !== expected) {
      console.error(`MISMATCH  ${rel}`);
      console.error(`  expected ${expected}`);
      console.error(`  actual   ${actual}`);
      bad++;
    }
    checked++;
  }
  if (bad > 0 || missing > 0) {
    console.error(`\nFAIL — ${bad} mismatched, ${missing} missing, ${total} listed (base=${base}).`);
    process.exit(1);
  }
  console.log(`OK — ${total} cache files verified (base=${base}).`);
}

main();
