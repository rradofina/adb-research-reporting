#!/usr/bin/env node
// scripts/sync-evidence.mjs
// Copies each program's evidence-packet artifacts into
// reporting-site/public/programs/{slug}/ for the Evidence page renderer.
// Generates a per-program manifest.json with file metadata + SHA-256.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const DEST_ROOT = path.join(REPO_ROOT, "reporting-site", "public", "programs");

const PROGRAMS = [
  "public-service-data-quality",
  "remittance-resilience",
  "migration-displacement-signals",
  "climate-health-workdays",
  "disaster-recovery-lag",
  "grid-reliability-heat",
  "port-hinterland-friction",
  "water-stress-crop-diversification",
  "social-protection-shock-coverage",
  "school-heat-disruption",
  "food-price-climate-transmission",
  "coastal-informal-risk",
  "flood-market-access",
  "invisible-urbanization",
  "access-services",
  "air-monitoring",
  "digital-performance",
  "mpi-nighttime-lights",
];

// Search bases for program folders. Some programs live at the repo root,
// others under luminosity-gap/research/.
const SEARCH_BASES = [REPO_ROOT, path.join(REPO_ROOT, "luminosity-gap", "research")];

function programDir(slug) {
  for (const base of SEARCH_BASES) {
    const p = path.join(base, slug);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

const ARTIFACTS = [
  { key: "readme", file: "README.md", label: "Overview" },
  { key: "reproduce", file: "REPRODUCE.md", label: "Reproducibility guide" },
  { key: "source_action", file: "SOURCE-ACTION.md", label: "Source action packet" },
  { key: "literature", file: "literature.md", label: "Literature review" },
  { key: "scoring", file: "scoring.md", label: "Scoring rubric" },
  { key: "preregistration", file: "pre-registration.md", label: "Pre-registration" },
  { key: "sensitivity", file: "sensitivity.md", label: "Sensitivity suite" },
  { key: "sensitivity_runs", file: "sensitivity-runs.json", label: "Sensitivity-run output" },
  { key: "coverage", file: "coverage.md", label: "Coverage" },
  { key: "results", file: "results.md", label: "Results" },
  { key: "source_disagreement_l3", file: "source-disagreement-l3-module.md", label: "Source-disagreement L3 module" },
  { key: "facility_validation_sample", file: "facility-validation-sample.md", label: "Facility-validation sample design" },
  { key: "review_internal", file: "review-internal.md", label: "Internal review" },
  { key: "review_external", file: "review-external.md", label: "External red-team review" },
  { key: "limitations", file: "limitations.md", label: "Limitations" },
  { key: "upgrade_gap", file: "upgrade-gap.md", label: "Upgrade-gap memo" },
  { key: "sr_to_pr", file: "SR-to-PR.md", label: "Gate request — SR → PR" },
];

const sha256 = (file) => {
  const h = crypto.createHash("sha256");
  h.update(fs.readFileSync(file));
  return h.digest("hex");
};

function bytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}

function extractAttestationChain(text) {
  const m = text.match(/attestation_chain:\s*([a-z\-]+)/i);
  return m ? m[1] : null;
}

function syncProgram(slug) {
  const dir = programDir(slug);
  if (!dir) return { slug, found: false };

  const dest = path.join(DEST_ROOT, slug);
  fs.mkdirSync(dest, { recursive: true });

  const included = [];
  for (const a of ARTIFACTS) {
    const src = path.join(dir, a.file);
    if (!fs.existsSync(src)) continue;
    const destFile = path.join(dest, a.file);
    fs.copyFileSync(src, destFile);
    const stat = fs.statSync(src);
    const text = a.file.endsWith(".md") ? fs.readFileSync(src, "utf8") : null;
    included.push({
      key: a.key,
      file: a.file,
      label: a.label,
      size: stat.size,
      size_human: bytes(stat.size),
      mtime: stat.mtime.toISOString(),
      sha256: sha256(src),
      attestation_chain: text ? extractAttestationChain(text) : null,
    });
  }

  // Also expose the latest generated/* files as downloads. Recurses one level
  // into subdirectories (e.g., generated/charts/) so chart and other binary
  // artifacts sync alongside the JSON/CSV outputs.
  const generatedDir = path.join(dir, "generated");
  const generatedIncluded = [];
  const walkAndCopy = (srcDir, destDir, relPrefix) => {
    fs.mkdirSync(destDir, { recursive: true });
    for (const f of fs.readdirSync(srcDir).filter((name) => !name.endsWith(".log"))) {
      const src = path.join(srcDir, f);
      const stat = fs.statSync(src);
      if (stat.isDirectory()) {
        walkAndCopy(src, path.join(destDir, f), `${relPrefix}${f}/`);
        continue;
      }
      const destFile = path.join(destDir, f);
      fs.copyFileSync(src, destFile);
      generatedIncluded.push({
        file: `generated/${relPrefix}${f}`,
        size: stat.size,
        size_human: bytes(stat.size),
        sha256: sha256(src),
      });
    }
  };
  if (fs.existsSync(generatedDir)) {
    walkAndCopy(generatedDir, path.join(dest, "generated"), "");
  }

  // Look for any article in articles/ that references this program
  const articlesDir = path.join(REPO_ROOT, "articles");
  const articles = [];
  if (fs.existsSync(articlesDir)) {
    for (const f of fs.readdirSync(articlesDir).filter((x) => x.endsWith(".md"))) {
      const text = fs.readFileSync(path.join(articlesDir, f), "utf8");
      const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
      if (!m) continue;
      const fm = m[1];
      const program = (fm.match(/^program:\s*(.+)$/m) || [])[1]?.trim();
      const slugMatch = (fm.match(/^slug:\s*(.+)$/m) || [])[1]?.trim();
      if (program === slug && slugMatch) {
        articles.push({
          slug: slugMatch,
          title: (fm.match(/^title:\s*(.+)$/m) || [])[1]?.trim(),
          attestation_chain: (fm.match(/^attestation_chain:\s*(.+)$/m) || [])[1]?.trim(),
        });
      }
    }
  }

  // Compute permanent-URL placeholder for §10.3
  const permanentUrl = `/program/${slug}/evidence`;

  // Hero visual (visual-first refactor, 2026-05-19). Each program may produce
  // generated/charts/{slug}-thumbnail.{png,svg,json}; if all three exist, the
  // manifest exposes a `hero` block the React site reads.
  let hero = null;
  const heroJson = path.join(dir, "generated", "charts", `${slug}-thumbnail.json`);
  const heroPng = path.join(dir, "generated", "charts", `${slug}-thumbnail.png`);
  const heroSvg = path.join(dir, "generated", "charts", `${slug}-thumbnail.svg`);
  if (fs.existsSync(heroJson) && fs.existsSync(heroPng) && fs.existsSync(heroSvg)) {
    try {
      const sidecar = JSON.parse(fs.readFileSync(heroJson, "utf8"));
      hero = {
        png: `generated/charts/${slug}-thumbnail.png`,
        svg: `generated/charts/${slug}-thumbnail.svg`,
        json: `generated/charts/${slug}-thumbnail.json`,
        title: sidecar.title,
        caption: sidecar.caption,
        headline_number: sidecar.headline_number,
        visual_form: sidecar.visual_form,
        source: sidecar.source,
        attestation_chain: sidecar.attestation_chain || "ai-first",
        generated_at: sidecar.generated_at,
        dimensions: sidecar.dimensions,
        sha256: sidecar.sha256,
      };
    } catch (err) {
      console.warn(`  hero sidecar parse failed for ${slug}: ${err.message}`);
    }
  }

  const manifest = {
    program: slug,
    permanent_url: permanentUrl,
    generated_at: new Date().toISOString(),
    hero,
    artifacts: included,
    generated_files: generatedIncluded,
    articles,
  };

  fs.writeFileSync(
    path.join(dest, "manifest.json"),
    `${JSON.stringify(manifest, null, 2)}\n`,
  );

  return { slug, found: true, count: included.length, generated: generatedIncluded.length };
}

const results = PROGRAMS.map(syncProgram);
fs.mkdirSync(DEST_ROOT, { recursive: true });
fs.writeFileSync(
  path.join(DEST_ROOT, "index.json"),
  `${JSON.stringify({
    generated_at: new Date().toISOString(),
    programs: results.filter((r) => r.found).map((r) => r.slug),
  }, null, 2)}\n`,
);

// Aggregate heroes for the visual-first home page (added 2026-05-19).
// Lets the home page do ONE fetch instead of 18 manifest.json loads.
const heroes = [];
for (const r of results.filter((x) => x.found)) {
  const manifestPath = path.join(DEST_ROOT, r.slug, "manifest.json");
  if (!fs.existsSync(manifestPath)) continue;
  try {
    const m = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    heroes.push({
      slug: r.slug,
      hero: m.hero || null,
    });
  } catch {
    heroes.push({ slug: r.slug, hero: null });
  }
}
fs.writeFileSync(
  path.join(DEST_ROOT, "heroes.json"),
  `${JSON.stringify({ generated_at: new Date().toISOString(), heroes }, null, 2)}\n`,
);

console.log(`Synced ${results.filter((r) => r.found).length}/${results.length} programs:`);
for (const r of results) {
  if (r.found) console.log(`  ${r.slug.padEnd(40)} ${r.count} artifacts, ${r.generated} generated files`);
  else console.log(`  ${r.slug.padEnd(40)} (no folder found)`);
}
