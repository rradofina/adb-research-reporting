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
  { key: "air_monitoring_metadata_readiness_audit", file: "metadata-readiness-audit.md", label: "Air-monitoring metadata-readiness audit" },
  { key: "air_monitoring_station_metadata_source_access", file: "station-metadata-source-access.md", label: "Air-monitoring OpenAQ station-metadata source access" },
  { key: "air_monitoring_regulator_source_inventory", file: "regulator-source-inventory.md", label: "Air-monitoring regulator-source inventory" },
  { key: "air_monitoring_regulator_station_extraction", file: "regulator-station-extraction.md", label: "Air-monitoring official station-source extraction" },
  { key: "air_monitoring_monitor_grade_evidence", file: "monitor-grade-evidence.md", label: "Air-monitoring monitor-grade evidence audit" },
  { key: "air_monitoring_official_openaq_reconciliation", file: "official-openaq-reconciliation.md", label: "Air-monitoring official-to-OpenAQ reconciliation audit" },
  { key: "air_monitoring_official_openaq_candidate_review", file: "official-openaq-candidate-review.md", label: "Air-monitoring official/OpenAQ candidate review worksheet" },
  { key: "air_monitoring_official_openaq_candidate_public_evidence", file: "official-openaq-candidate-public-evidence.md", label: "Air-monitoring official/OpenAQ candidate public-evidence audit" },
  { key: "air_monitoring_official_openaq_candidate_crosswalk_source_scan", file: "official-openaq-candidate-crosswalk-source-scan.md", label: "Air-monitoring official/OpenAQ candidate crosswalk source scan" },
  { key: "air_monitoring_official_openaq_candidate_public_feed_source_scan", file: "official-openaq-candidate-public-feed-source-scan.md", label: "Air-monitoring official/OpenAQ candidate public-feed source scan" },
  { key: "air_monitoring_one_signal_review_queue", file: "one-signal-review-queue.md", label: "Air-monitoring one-signal review queue" },
  { key: "air_monitoring_monitor_grade_source_validation_scan", file: "monitor-grade-source-validation-scan.md", label: "Air-monitoring monitor-grade source-validation scan" },
  { key: "air_monitoring_monitor_grade_station_review_queue", file: "monitor-grade-station-review-queue.md", label: "Air-monitoring monitor-grade station-review queue" },
  { key: "air_monitoring_monitor_grade_station_method_evidence", file: "monitor-grade-station-method-evidence.md", label: "Air-monitoring monitor-grade station method-evidence audit" },
  { key: "air_monitoring_uzbekistan_station_current_method_scan", file: "uzbekistan-station-current-method-scan.md", label: "Air-monitoring Uzbekistan station current/method scan" },
  { key: "air_monitoring_uzbekistan_method_policy_source_scan", file: "uzbekistan-method-policy-source-scan.md", label: "Air-monitoring Uzbekistan method-policy source scan" },
  { key: "air_monitoring_uzbekistan_station_specific_source_evidence", file: "uzbekistan-station-specific-source-evidence.md", label: "Air-monitoring Uzbekistan station-specific source evidence" },
  { key: "air_monitoring_uzbekistan_status_certification_source_scan", file: "uzbekistan-status-certification-source-scan.md", label: "Air-monitoring Uzbekistan status/certification source scan" },
  { key: "air_monitoring_uzbekistan_blocker_row_followup", file: "uzbekistan-blocker-row-followup.md", label: "Air-monitoring Uzbekistan blocker-row follow-up" },
  { key: "air_monitoring_uzbekistan_endpoint_consistency", file: "uzbekistan-endpoint-consistency.md", label: "Air-monitoring Uzbekistan endpoint consistency check" },
  { key: "air_monitoring_uzbekistan_blocker_external_context", file: "uzbekistan-blocker-external-context.md", label: "Air-monitoring Uzbekistan blocker external-context wall" },
  { key: "air_monitoring_indonesia_georgia_row_method_source_scan", file: "indonesia-georgia-row-method-source-scan.md", label: "Air-monitoring Indonesia/Georgia row-method source scan" },
  { key: "air_monitoring_station_code_status_method_source_scan", file: "station-code-status-method-source-scan.md", label: "Air-monitoring station-code status/method source scan" },
  { key: "air_monitoring_station_grade_decision_ledger", file: "station-grade-decision-ledger.md", label: "Air-monitoring station-grade decision ledger" },
  { key: "air_monitoring_station_method_classification_audit", file: "station-method-classification-audit.md", label: "Air-monitoring station-method classification audit" },
  { key: "air_monitoring_bmkg_operation_maintenance_source_scan", file: "bmkg-operation-maintenance-source-scan.md", label: "Air-monitoring BMKG operation/maintenance source scan" },
  { key: "air_monitoring_bmkg_station_specific_status_audit", file: "bmkg-station-specific-status-audit.md", label: "Air-monitoring BMKG station-specific status audit" },
  { key: "air_monitoring_bmkg_api_parity_status", file: "bmkg-api-parity-status.md", label: "Air-monitoring BMKG API telemetry/status-field check" },
  { key: "air_monitoring_bmkg_regional_status_source_scan", file: "bmkg-regional-status-source-scan.md", label: "Air-monitoring BMKG regional status source scan" },
  { key: "air_monitoring_bmkg_dashboard_status_source_scan", file: "bmkg-dashboard-status-source-scan.md", label: "Air-monitoring BMKG dashboard current-status source scan" },
  { key: "air_monitoring_bmkg_grade_basis_source_scan", file: "bmkg-grade-basis-source-scan.md", label: "Air-monitoring BMKG grade-basis source scan" },
  { key: "air_monitoring_bmkg_station_public_context_source_scan", file: "bmkg-station-public-context-source-scan.md", label: "Air-monitoring BMKG station public-context source scan" },
  { key: "air_monitoring_bmkg_installation_audit_source_scan", file: "bmkg-installation-audit-source-scan.md", label: "Air-monitoring BMKG installation/audit source scan" },
  { key: "air_monitoring_georgia_report_verification_source_scan", file: "georgia-report-verification-source-scan.md", label: "Air-monitoring Georgia report verification source scan" },
  { key: "air_monitoring_georgia_report_export_ladder", file: "georgia-report-export-ladder.md", label: "Air-monitoring Georgia report export verification ladder" },
  { key: "air_monitoring_georgia_verification_policy", file: "georgia-verification-policy.md", label: "Air-monitoring Georgia verification-policy wall" },
  { key: "air_monitoring_georgia_report_frequency_matrix", file: "georgia-report-frequency-matrix.md", label: "Air-monitoring Georgia report-frequency verification matrix" },
  { key: "source_disagreement_l3", file: "source-disagreement-l3-module.md", label: "Source-disagreement L3 module" },
  { key: "facility_validation_sample", file: "facility-validation-sample.md", label: "Facility-validation sample design" },
  { key: "facility_validation_coded_screen", file: "facility-validation-coded-screen.md", label: "Facility-validation coded screen" },
  { key: "facility_validation_ai_review", file: "facility-validation-ai-review.md", label: "Facility-validation AI review ledger" },
  { key: "facility_validation_candidate_resolution", file: "facility-validation-candidate-resolution.md", label: "Facility-validation candidate-resolution pass" },
  { key: "facility_validation_candidate_public_source_check", file: "facility-validation-candidate-public-source-check.md", label: "Facility-validation candidate public-source check" },
  { key: "facility_validation_coordinate_repair", file: "facility-validation-coordinate-repair.md", label: "Facility-validation coordinate-repair triage" },
  { key: "facility_validation_public_map_gap", file: "facility-validation-public-map-gap.md", label: "Facility-validation public-map-gap triage" },
  { key: "facility_validation_public_map_gap_evidence", file: "facility-validation-public-map-gap-evidence.md", label: "Facility-validation public-map-gap row evidence" },
  { key: "facility_validation_public_map_inspection", file: "facility-validation-public-map-inspection.md", label: "Facility-validation targeted public-map inspection" },
  { key: "facility_validation_public_source_confirmation", file: "facility-validation-public-source-confirmation.md", label: "Facility-validation public-source confirmation" },
  { key: "facility_validation_public_source_confirmation_targeted_rows", file: "facility-validation-public-source-confirmation-targeted-rows.md", label: "Facility-validation targeted-row public-source confirmation" },
  { key: "facility_validation_public_source_decision_ledger", file: "facility-validation-public-source-decision-ledger.md", label: "Facility-validation public-source decision ledger" },
  { key: "facility_validation_possible_same_facility_review", file: "facility-validation-possible-same-facility-review.md", label: "Facility-validation possible same-facility review" },
  { key: "facility_validation_priority_name_conflict_review", file: "facility-validation-priority-name-conflict-review.md", label: "Facility-validation priority name-conflict review" },
  { key: "facility_validation_lower_priority_name_conflict_review", file: "facility-validation-lower-priority-name-conflict-review.md", label: "Facility-validation lower-priority name-conflict review" },
  { key: "facility_validation_zero_osm_upazila_observability_review", file: "facility-validation-zero-osm-upazila-observability-review.md", label: "Facility-validation zero-OSM upazila observability review" },
  { key: "facility_validation_evidence_ladder", file: "facility-validation-evidence-ladder.md", label: "Facility-validation evidence ladder" },
  { key: "facility_validation_human_gated_handoff", file: "facility-validation-human-gated-handoff.md", label: "Facility-validation human-gated handoff matrix" },
  { key: "facility_validation_human_validation_worksheet", file: "facility-validation-human-validation-worksheet.md", label: "Facility-validation human-validation worksheet" },
  { key: "facility_validation_ai_closure_audit", file: "facility-validation-ai-closure-audit.md", label: "Facility-validation AI closure audit" },
  { key: "facility_validation_source_repair_public_evidence", file: "facility-validation-source-repair-public-evidence.md", label: "Facility-validation source-repair public evidence" },
  { key: "facility_validation_source_repair_official_coordinate_evidence", file: "facility-validation-source-repair-official-coordinate-evidence.md", label: "Facility-validation source-repair official-coordinate evidence" },
  { key: "facility_validation_source_repair_public_explanation_evidence", file: "facility-validation-source-repair-public-explanation-evidence.md", label: "Facility-validation source-repair public explanation evidence" },
  { key: "facility_validation_source_repair_correction_record_followup", file: "facility-validation-source-repair-correction-record-followup.md", label: "Facility-validation source-repair correction-record follow-up" },
  { key: "facility_validation_source_repair_clarification_packet", file: "facility-validation-source-repair-clarification-packet.md", label: "Facility-validation source-repair clarification packet" },
  { key: "facility_validation_source_repair_registry_vintage_review", file: "facility-validation-source-repair-registry-vintage-review.md", label: "Facility-validation source-repair registry-vintage review" },
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
