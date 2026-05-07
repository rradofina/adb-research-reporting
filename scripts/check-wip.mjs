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
