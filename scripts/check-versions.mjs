#!/usr/bin/env node
// scripts/check-versions.mjs
// Reads versions.json and reports any source whose retrieved_on date is
// older than a configurable freshness threshold. Does not fail CI by
// default (sources can validly stay pinned for years); informational
// only. The author treats the report as a prompt to either re-pull the
// source or document the freeze.

import fs from "node:fs";

const VERSIONS_FILE = "versions.json";
const STALE_DAYS_DEFAULT = 180;

function daysAgo(iso) {
  if (!iso) return null;
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return null;
  return Math.floor((Date.now() - d.getTime()) / (1000 * 60 * 60 * 24));
}

function main() {
  const args = process.argv.slice(2);
  const stale = Number(args[0] ?? STALE_DAYS_DEFAULT);

  if (!fs.existsSync(VERSIONS_FILE)) {
    console.error(`${VERSIONS_FILE} missing at repo root`);
    process.exit(1);
  }
  const data = JSON.parse(fs.readFileSync(VERSIONS_FILE, "utf8"));
  const sources = data.sources ?? {};
  const rows = [];
  for (const [name, src] of Object.entries(sources)) {
    const candidates = ["retrieved_on", "retrieved_on_window"];
    let latest = null;
    for (const k of candidates) {
      const v = src[k];
      if (!v) continue;
      if (Array.isArray(v)) {
        latest = latest ? (v.at(-1) > latest ? v.at(-1) : latest) : v.at(-1);
      } else {
        latest = latest ? (v > latest ? v : latest) : v;
      }
    }
    const ageDays = daysAgo(latest);
    rows.push({ name, latest, ageDays });
  }

  rows.sort((a, b) => (b.ageDays ?? -1) - (a.ageDays ?? -1));

  console.log(`source\tlatest_retrieved_on\tage_days\tstatus`);
  let stales = 0;
  for (const r of rows) {
    let status = "fresh";
    if (r.ageDays === null) status = "no-date";
    else if (r.ageDays > stale) {
      status = "stale";
      stales++;
    }
    console.log(`${r.name}\t${r.latest ?? "—"}\t${r.ageDays ?? "—"}\t${status}`);
  }
  console.log(`\n${stales} source(s) older than ${stale} days; ${rows.length} total.`);
  // Informational; do not fail CI.
}

main();
