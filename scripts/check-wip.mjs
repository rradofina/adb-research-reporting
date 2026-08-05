#!/usr/bin/env node
// scripts/check-wip.mjs
// Enforces CONSTITUTION.md §8.1 — WIP cap (max 1 PR + 3 SR programs).
// Reads research/wip-register.md and parses the PR/SR counts. When §18
// AI-First acceleration is active and the register explicitly suspends caps,
// this reports the counts but does not fail the gate.
//
// This is a deterministic check; the Constitution and register together are
// the gate.

import fs from "node:fs";

const FILE = "research/wip-register.md";
const CONSTITUTION = "CONSTITUTION.md";

function section18Active() {
  if (!fs.existsSync(CONSTITUTION)) return false;
  const constitution = fs.readFileSync(CONSTITUTION, "utf8");
  const section = constitution.match(/##\s+18\.\s+AI-First[\s\S]*?(?=\n##\s+\d+\.|\s*$)/i);
  return Boolean(section && /\*\*Status:\s*ACTIVE\.\*\*/i.test(section[0]));
}

// Parse the §15 program register table into {slug -> label}. The table's status
// cell leads with the maturity in bold, e.g. "**SR under §18 — ...**" or
// "**PP — demoted 2026-05-07**"; the location cell carries the program folder.
// Before 2026-08-05 this gate read only the register file, so a §15 row could
// carry a label and a claim its own program had retired and nothing failed.
function constitutionLabels() {
  if (!fs.existsSync(CONSTITUTION)) return null;
  const rows = fs.readFileSync(CONSTITUTION, "utf8").split(/\r?\n/);
  const labels = new Map();
  for (const row of rows) {
    if (!row.startsWith("|")) continue;
    const cells = row.split("|").map((c) => c.trim());
    // | # | Program | Location | Status | Scoring | Owner | Last updated |
    if (cells.length < 8 || !/^\d+$/.test(cells[1])) continue;
    const slug = cells[3].match(/`([a-z0-9-]+)\//)?.[1];
    if (!slug) continue;
    // The maturity is the first token of the status cell. Most rows bold it;
    // row 0 does not, so accept either form rather than report a false
    // divergence for a formatting difference.
    const label = cells[4].match(/^\**\s*(PR|SR|PP|H|Ret)\b/i)?.[1];
    labels.set(slug, label ? label.toUpperCase() : "UNPARSED");
  }
  return labels;
}

// Which maturity section of the register a program is listed under.
function registerLabels(text) {
  const labels = new Map();
  const SECTIONS = [
    [/^#+\s+Publication-Ready\b/i, "PR"],
    [/^#+\s+Screening Result\b/i, "SR"],
    [/^#+\s+Prepared Pipeline\b/i, "PP"],
    [/^#+\s+Hypothesis\b/i, "H"],
    [/^#+\s+Retired\b/i, "RET"],
  ];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    if (/^#+\s/.test(line)) {
      current = SECTIONS.find(([rx]) => rx.test(line))?.[1] ?? null;
      continue;
    }
    if (!current) continue;
    const slug = line.match(/^[-*]\s+\*\*([a-z0-9-]+)\*\*/)?.[1];
    if (slug) labels.set(slug, current);
  }
  return labels;
}

function capsSuspendedByRegister(text) {
  return /§18\s+ACTIVE[\s\S]{0,160}caps?\s+suspended/i.test(text)
    || /caps?\s+suspended[\s\S]{0,160}§18\s+ACTIVE/i.test(text);
}

function main() {
  if (!fs.existsSync(FILE)) {
    console.error(`${FILE} missing`);
    process.exit(1);
  }
  const text = fs.readFileSync(FILE, "utf8");
  const lines = text.split(/\r?\n/);
  let inPR = false;
  let inSR = false;
  let prCount = 0;
  let srCount = 0;
  for (const line of lines) {
    if (/^#+\s+Publication-Ready\b/i.test(line)) {
      inPR = true; inSR = false; continue;
    }
    if (/^#+\s+Screening Result\b/i.test(line)) {
      inSR = true; inPR = false; continue;
    }
    if (/^#+\s/.test(line)) { inPR = false; inSR = false; continue; }
    // Count list items that aren't "(none)" placeholder.
    if (/^[-*]\s+/.test(line) && !/\(none\)/i.test(line)) {
      if (inPR) prCount++;
      else if (inSR) srCount++;
    }
  }

  const PR_CAP = 1;
  const SR_CAP = 3;
  const section18 = section18Active();
  const capsSuspended = section18 && capsSuspendedByRegister(text);
  console.log(`PR programs: ${prCount} (cap ${PR_CAP})`);
  console.log(`SR programs: ${srCount} (cap ${SR_CAP})`);

  // Cross-check §15 against the register. A program listed in both must carry
  // the same maturity in both; a divergence means one public surface is
  // claiming more (or less) than the governance file that authorizes it.
  const constitution = constitutionLabels();
  const register = registerLabels(text);
  if (constitution) {
    const divergences = [];
    for (const [slug, cLabel] of constitution) {
      const rLabel = register.get(slug);
      if (!rLabel) continue; // register does not list every program
      if (cLabel !== rLabel) divergences.push(`${slug}: §15 says ${cLabel}, register says ${rLabel}`);
    }
    console.log(`§15 rows parsed: ${constitution.size}; register entries: ${register.size}`);
    if (divergences.length > 0) {
      for (const d of divergences) console.error(`  DIVERGENCE — ${d}`);
      console.error(`FAIL — ${divergences.length} maturity divergence(s) between CONSTITUTION.md §15 and ${FILE}.`);
      process.exit(1);
    }
    console.log("OK — §15 and the register agree on every program listed in both.");
  }

  if (capsSuspended) {
    console.log(`OK — WIP cap suspended under CONSTITUTION.md §18 ACTIVE.`);
    return;
  }

  if (prCount > PR_CAP || srCount > SR_CAP) {
    console.error(`FAIL — WIP cap exceeded.`);
    process.exit(1);
  }
  console.log(`OK — WIP cap respected.`);
}

main();
