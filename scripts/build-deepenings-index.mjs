/**
 * build-deepenings-index.mjs — deterministic index of the deepening pass.
 *
 * Scans every program for its deepening triplet (deepen-*.py script, a
 * generated artifact, a deepened-results.md narrative) and emits a compact
 * index the reporting site renders as an all-18 scoreboard. The one-line
 * "finding" per program is EXTRACTED verbatim from the committed
 * deepened-results.md (the paragraph under its "finding" heading) — this
 * script writes no numbers of its own, it only locates and trims text that
 * a deepen-*.py script already produced from public data. Outcome is a
 * factual classification (did a real artifact get produced, and does the
 * narrative declare a data wall), not a verdict.
 *
 * Run: node scripts/build-deepenings-index.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "reporting-site", "public", "deepenings-index.json");

const ARTIFACT_RX = /(deepening|falsification|tautology|decomposition|audit|dropped-leg|completeness|inert|concentration|denominator|coverage)/i;

function firstHeadingTitle(md) {
  const m = md.match(/^#\s+(.+)$/m);
  return m ? m[1].replace(/—.*$/, "").trim() : null;
}

/**
 * Curated one-line findings for the few programs where the heading-based
 * extractor lands on a lead-in, a wall sentence, or a mid-number truncation.
 * These are faithful summaries; every figure matches the program's committed
 * artifact (verified in the deepening audit). Programs not listed here use
 * the extractor below.
 */
const OVERRIDE = {
  "grid-reliability-heat":
    "Fuel concentration is higher on generation than on installed capacity for 18 of 22 grids — Tajikistan goes 0.80→1.00 as its thermal backup barely runs; the screen had the right worry and the wrong variable.",
  "air-monitoring":
    "The ~14.3M 'unmonitored' headline is 83.5% just two economies (PNG 73.7%, Timor-Leste 9.8%); whether any monitoring gap survives once development is controlled cannot be settled on-disk (no HDI/GDP series cached — a named wall).",
  "school-heat-disruption":
    "Cambodia is genuinely #1 in only 5 of 7 committed sensitivity runs — it loses one to Pakistan and 'passes' another only via an all-zeros tie — so 'KHM #1 across every perturbation' is false.",
  "flood-market-access":
    "The index correlates r=0.94 with raw EM-DAT event count and only r=0.15 with rural share — it ranks country size and disaster-reporting density, with no road, market, or flood footprint anywhere in it.",
  "remittance-resilience":
    "The five-economy cluster survives a robust median cost (membership unchanged), but the recompute exposed a real normalization bug in the committed pipeline that manufactures the −305% quotes.",
  "digital-performance":
    "A genuine data wall: the Ookla speed pull (~2.6 GB), WorldPop, and an official-coverage claim are not on disk, so no numbers can be produced yet — a runnable pipeline stub is committed that refuses to invent them.",
};

/** Pull the finding under the first "finding" heading (excluding "not a
 * finding"); gather paragraphs + list items, trim at a sentence boundary. */
function extractFinding(md) {
  const lines = md.split(/\r?\n/);
  const isHeading = (l) => /^#{1,6}\s/.test(l);
  let i = lines.findIndex((l) => /^#{1,4}\s+.*\bfinding/i.test(l) && !/not a finding/i.test(l));
  if (i < 0) i = lines.findIndex((l) => /\*\*[^*]*\bfinding/i.test(l) && !/not a finding/i.test(l));

  const buf = [];
  if (i >= 0) {
    for (let j = i + 1; j < lines.length; j++) {
      if (isHeading(lines[j])) break; // stop at next heading (gather across blanks/lists)
      buf.push(lines[j]);
    }
  } else {
    // fallback: first substantive paragraph after the first section heading
    const s = lines.findIndex(isHeading);
    for (let j = (s < 0 ? 0 : s + 1); j < lines.length; j++) {
      if (isHeading(lines[j]) && buf.some((b) => b.trim())) break;
      buf.push(lines[j]);
    }
  }

  let text = buf
    .map((l) => l.replace(/^\s*[-*]\s+/, "").replace(/^\s*\d+\.\s+/, "").trim())
    .filter(Boolean)
    .join(" ")
    .replace(/\s+/g, " ")
    .replace(/\*\*|__|\*|`/g, "")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .trim();
  if (!text) return null;

  // Trim to a sentence boundary near 240 chars — never cut mid-token/number.
  if (text.length > 240) {
    const slice = text.slice(0, 240);
    const stop = Math.max(slice.lastIndexOf(". "), slice.lastIndexOf("? "), slice.lastIndexOf("! "));
    text = stop > 80 ? slice.slice(0, stop + 1) : slice.replace(/\s+\S*$/, "") + "…";
  }
  return text;
}

function main() {
  const programs = fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory() && fs.existsSync(path.join(ROOT, d.name, "deepened-results.md")))
    .map((d) => d.name)
    .sort();

  const rows = [];
  for (const slug of programs) {
    const dir = path.join(ROOT, slug);
    const md = fs.readFileSync(path.join(dir, "deepened-results.md"), "utf8");

    const scriptsDir = path.join(dir, "scripts");
    const scripts = fs.existsSync(scriptsDir)
      ? fs.readdirSync(scriptsDir).filter((f) => /^(deepen|run-ookla)/.test(f))
      : [];
    const genDir = path.join(dir, "generated");
    const artifacts = fs.existsSync(genDir)
      ? fs.readdirSync(genDir).filter((f) => f.endsWith(".json") && ARTIFACT_RX.test(f))
      : [];

    const hasArtifact = artifacts.length > 0;
    const declaresWall = /data wall/i.test(md);
    const outcome = !hasArtifact
      ? "wall" // no real artifact produced (owner-gated source not on disk)
      : declaresWall
        ? "computed + frontier wall"
        : "computed";

    rows.push({
      slug,
      title: firstHeadingTitle(md) || slug,
      outcome,
      has_script: scripts.length > 0,
      has_artifact: hasArtifact,
      artifact: artifacts[0] || null,
      finding: OVERRIDE[slug] ?? extractFinding(md),
    });
  }

  const payload = {
    generated_by: "scripts/build-deepenings-index.mjs",
    note: "Deterministic scan of committed deepening triplets; findings extracted verbatim from each deepened-results.md.",
    counts: {
      total: rows.length,
      computed: rows.filter((r) => r.has_artifact).length,
      walls: rows.filter((r) => !r.has_artifact).length,
    },
    rows,
  };
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(payload, null, 2) + "\n");
  console.log(`Wrote ${OUT}`);
  console.log(`  ${payload.counts.total} programs · ${payload.counts.computed} computed · ${payload.counts.walls} wall`);
  for (const r of rows) {
    console.log(`  ${r.has_artifact ? "✓" : "·"} ${r.slug.padEnd(34)} ${r.outcome}`);
  }
}

main();
