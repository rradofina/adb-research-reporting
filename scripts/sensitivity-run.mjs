#!/usr/bin/env node
// scripts/sensitivity-run.mjs
// Generic sensitivity-suite runner. Implements CONSTITUTION.md §6.6 by
// driving any program pipeline that follows the convention:
//
//   - The program ships a `sensitivity.json` listing arbitrary numerics
//     and their pre-registered values.
//   - The pipeline is invoked as:
//       node {slug}/scripts/run.mjs --params <path>
//     or, for TS pipelines:
//       npx tsx {slug}/pipeline.ts --params <path>
//   - The pipeline writes its primary output to
//       generated/{slug}-{suffix}.json
//
// Usage:
//   node scripts/sensitivity-run.mjs --program {slug}
//
// Output:
//   {slug}/generated/sensitivity/baseline.json
//   {slug}/generated/sensitivity/{param}-minus50.json
//   {slug}/generated/sensitivity/{param}-plus50.json
//   {slug}/sensitivity.md (table updated with deltas)

import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

const program = arg("program");
if (!program) {
  console.error("Usage: node scripts/sensitivity-run.mjs --program <slug>");
  process.exit(2);
}

const programDir = path.resolve(program);
if (!fs.existsSync(programDir)) {
  console.error(`Program folder ${program}/ does not exist at repo root.`);
  process.exit(2);
}

const manifestPath = path.join(programDir, "sensitivity.json");
if (!fs.existsSync(manifestPath)) {
  console.error(`Missing ${program}/sensitivity.json. Required for §6.6 sensitivity suite.`);
  console.error(`Expected schema:`);
  console.error(JSON.stringify({
    pipeline: "scripts/run.mjs",
    runner: "node | tsx",
    parameters: [
      { name: "buffer_km", baseline: 5, unit: "km" },
      { name: "score_threshold", baseline: 18, unit: "points" }
    ]
  }, null, 2));
  process.exit(2);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const pipeline = manifest.pipeline ?? "scripts/run.mjs";
const runner = manifest.runner ?? "node";
const parameters = manifest.parameters ?? [];

const outDir = path.join(programDir, "generated", "sensitivity");
fs.mkdirSync(outDir, { recursive: true });

function paramsFile(name, value) {
  const p = path.join(outDir, `params-${name}.json`);
  const baseline = Object.fromEntries(parameters.map((x) => [x.name, x.baseline]));
  baseline[name] = value;
  fs.writeFileSync(p, JSON.stringify(baseline, null, 2));
  return p;
}

function invoke(label, paramsPath) {
  const cmd = runner === "tsx" ? "npx" : runner;
  const args = runner === "tsx"
    ? ["tsx", path.join(programDir, pipeline), "--params", paramsPath]
    : [path.join(programDir, pipeline), "--params", paramsPath];
  console.log(`▶ ${label} :: ${cmd} ${args.join(" ")}`);
  const result = spawnSync(cmd, args, { stdio: "inherit", env: { ...process.env, SENSITIVITY_LABEL: label } });
  return result.status === 0;
}

// 1. Baseline
const baselineParams = path.join(outDir, "params-baseline.json");
fs.writeFileSync(
  baselineParams,
  JSON.stringify(Object.fromEntries(parameters.map((p) => [p.name, p.baseline])), null, 2),
);
let ok = invoke("baseline", baselineParams);

// 2. ±50% per parameter
const results = [{ name: "baseline", ok }];
for (const p of parameters) {
  const minusName = `${p.name}-minus50`;
  const plusName = `${p.name}-plus50`;
  const minus = invoke(minusName, paramsFile(minusName, p.baseline * 0.5));
  const plus  = invoke(plusName,  paramsFile(plusName,  p.baseline * 1.5));
  results.push({ name: minusName, ok: minus });
  results.push({ name: plusName,  ok: plus });
}

// 3. Summary
console.log("\nSensitivity-suite results:");
for (const r of results) {
  console.log(`  ${r.ok ? "OK  " : "FAIL"} ${r.name}`);
}
const allOk = results.every((r) => r.ok);
if (!allOk) {
  console.error(`\n${results.filter((r) => !r.ok).length} sensitivity-run(s) failed. The program cannot advance to PR until these are resolved.`);
  process.exit(1);
}
console.log(`\nAll ${results.length} runs passed. Author updates ${program}/sensitivity.md §1 with the deltas now.`);
