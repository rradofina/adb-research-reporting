import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface PsdqExposureRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  join_key: string;
  registry_records: number;
  active_facilities: number;
  active_clinical_facilities: number;
  coordinate_facilities: number;
  osm_health: number;
  osm_hospital: number;
  osm_clinic: number;
  osm_doctors: number;
  osm_to_active_clinical_ratio: number;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  buildings_nearest_1km_p85: number;
  buildings_nearest_3km_p85: number;
  buildings_nearest_5km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
  has_open_buildings_denominator: number;
  has_osm_boundary_match: number;
}

interface PsdqExposureSummary {
  generated_at: string;
  program: string;
  country: string;
  source: string;
  method: string;
  osm: {
    osm_elements: number;
    assigned_features: number;
    unassigned_features: number;
    timestamp_osm_base: string;
    timestamp_areas_base: string;
  };
  exposure: {
    registry_admin_rows: number;
    rows_with_open_buildings_denominator: number;
    active_clinical_facilities: number;
    osm_health_joined: number;
    registry_minus_osm_clinical: number;
    buildings_nearest_3km_p85: number;
    underobserved_buildings_3km_p85_proxy: number;
  };
  top_exposure_gap_upazilas: PsdqExposureRow[];
  non_claim: string;
}

interface PsdqStrataRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  join_key: string;
  active_clinical_facilities: number;
  osm_health: number;
  osm_to_active_clinical_ratio: number | null;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  buildings_nearest_3km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
  has_open_buildings_denominator: number;
  has_osm_boundary_match: number;
  total_road_km?: number;
  classified_surface_share?: number;
  classified_unpaved_share?: number;
  road_context_score?: number;
}

interface PsdqRatioStratum {
  bucket: string;
  label: string;
  row_count: number;
  share_of_registry_rows: number | null;
  active_clinical_facilities: number;
  share_of_active_clinical_facilities: number | null;
  osm_health: number;
  osm_to_active_clinical_ratio: number | null;
  registry_minus_osm_clinical: number;
  buildings_nearest_3km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
}

interface PsdqSourceStrata {
  generated_at: string;
  goal_level: string;
  status: string;
  coverage: {
    registry_admin_rows: number;
    csv_registry_rows: number;
    rows_with_open_buildings_denominator: number;
    share_with_open_buildings_denominator: number | null;
    registry_rows_with_joined_osm_features: number;
    share_with_joined_osm_features: number | null;
    osm_elements_retrieved: number;
    osm_elements_assigned_to_boundary: number;
    osm_features_joined_to_registry: number;
    osm_features_not_joined_to_registry: number;
    active_clinical_facilities: number;
    osm_health_joined: number;
    registry_minus_osm_clinical: number;
    buildings_nearest_3km_p85: number;
    underobserved_buildings_3km_p85_proxy: number;
    rows_with_road_context: number;
    share_with_road_context: number | null;
    rows_with_surface_context: number;
    share_with_surface_context: number | null;
  };
  validation_strata: {
    rows_missing_open_buildings_denominator: number;
    share_missing_open_buildings_denominator: number | null;
    registry_rows_without_joined_osm_features: number;
    share_without_joined_osm_features: number | null;
    rows_with_zero_osm_health_features: number;
    share_with_zero_osm_health_features: number | null;
    rows_where_osm_equals_or_exceeds_registry: number;
    share_where_osm_equals_or_exceeds_registry: number | null;
    rows_with_zero_gap_or_osm_ge_registry: number;
    share_with_zero_gap_or_osm_ge_registry: number | null;
    rows_with_positive_registry_minus_osm_gap: number;
    rows_eligible_for_road_context: number;
    rows_eligible_for_road_surface_score: number;
    min_classified_surface_km_for_score: number;
    min_classified_surface_share_for_score: number;
  };
  ratio_strata: PsdqRatioStratum[];
  top_lists: {
    top_exposure_gap_upazilas: PsdqStrataRow[];
    top_zero_osm_high_proxy_upazilas: PsdqStrataRow[];
    top_osm_equals_or_exceeds_registry_upazilas: PsdqStrataRow[];
    top_road_context_upazilas: PsdqStrataRow[];
  };
}

interface PsdqValidationSampleGroup {
  sample_group: string;
  upazila_count: number;
  facility_rows: number;
  coordinate_ready_facility_rows: number;
}

interface PsdqValidationCode {
  code: string;
  meaning: string;
}

interface PsdqValidationSample {
  generated_at: string;
  status: string;
  goal_level: string;
  sample_summary: {
    sampled_upazilas: number;
    sampled_facility_rows: number;
    coordinate_ready_facility_rows: number;
    coding_sheet_rows: number;
    groups: PsdqValidationSampleGroup[];
  };
  validation_codes: PsdqValidationCode[];
  non_claim: string;
}

interface PsdqValidationCodeCount {
  validation_code: string;
  rows: number;
}

interface PsdqValidationGroupCount {
  sample_group: string;
  rows: number;
  confirmed_same_facility: number;
  probable_duplicate_or_alias: number;
  classification_mismatch: number;
  registry_coordinate_issue: number;
  missing_public_map_point: number;
  osm_only_candidate: number;
  unresolved_public_sources: number;
}

interface PsdqValidationCodedSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  screen_summary: {
    coded_rows: number;
    osm_candidate_rows: number;
    manual_review_recommended_rows: number;
    rows_with_any_osm_candidate_500m: number;
    rows_with_valid_coordinate: number;
    rows_inside_expected_upazila: number;
  };
  validation_code_counts: PsdqValidationCodeCount[];
  validation_code_counts_by_group: PsdqValidationGroupCount[];
  overpass_status_counts: Record<string, number>;
  coordinate_boundary_status_counts: Record<string, number>;
  non_claim: string;
}

interface PsdqAiReviewCount {
  name: string;
  rows: number;
}

interface PsdqAiReviewGroupCount {
  sample_group: string;
  rows: number;
  public_map_gap_at_valid_coordinate: number;
  registry_coordinate_repair: number;
  candidate_name_or_type_resolution: number;
  nearby_osm_without_registry_match: number;
  unresolved_public_source_check: number;
}

interface PsdqAiReviewSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  review_scope: {
    coded_rows: number;
    flagged_rows_reviewed: number;
    unflagged_rows_not_reopened: number;
    candidate_resolution_rows: number;
    rows_with_no_osm_health_candidate_500m: number;
    coordinate_source_issue_rows: number;
  };
  ai_review_bucket_counts: PsdqAiReviewCount[];
  ai_review_priority_counts: PsdqAiReviewCount[];
  validation_code_counts_in_review_queue: PsdqAiReviewCount[];
  ai_review_bucket_counts_by_group: PsdqAiReviewGroupCount[];
  non_claim: string;
}

interface PsdqCandidateResolutionCount {
  name: string;
  rows: number;
}

interface PsdqCandidateResolutionGroupCount {
  sample_group: string;
  rows: number;
  probable_same_facility_alias_or_campus: number;
  probable_same_site_classification_conflict: number;
  possible_alias_requires_name_check: number;
  local_script_candidate_requires_name_check: number;
  ambiguous_nearby_candidate: number;
  weak_nearby_osm_signal: number;
}

interface PsdqCandidateResolutionSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  resolution_scope: {
    candidate_resolution_rows_reviewed: number;
    rows_closed_as_confirmed_same_facility: number;
    rows_retained_open: number;
    rows_with_local_script_candidate: number;
  };
  candidate_resolution_code_counts: PsdqCandidateResolutionCount[];
  candidate_resolution_counts_by_group: PsdqCandidateResolutionGroupCount[];
  evidence_strength_counts: PsdqCandidateResolutionCount[];
  non_claim: string;
}

interface PsdqCandidatePublicSourceCheckGroupCount {
  candidate_resolution_code: string;
  rows: number;
  strong_same_site_osm_tag_support_requires_human_confirmation: number;
  same_site_type_or_label_conflict_requires_public_label_check: number;
  name_support_but_coordinate_or_function_conflict: number;
  nearby_features_do_not_support_registry_name: number;
}

interface PsdqCandidatePublicSourceCheckSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  confirmation_scope: {
    candidate_rows_checked: number;
    rows_closed_as_confirmed_same_facility: number;
    rows_retained_open: number;
    rows_with_specific_osm_name_tag_support: number;
    rows_with_best_public_name_within_50m: number;
  };
  public_source_check_code_counts: PsdqCandidateResolutionCount[];
  public_source_check_counts_by_resolution_lane: PsdqCandidatePublicSourceCheckGroupCount[];
  evidence_strength_counts: PsdqCandidateResolutionCount[];
  non_claim: string;
}

interface PsdqCountrySummary {
  iso3: string;
  country: string;
  source: string;
  totals: {
    osm_health: number;
    registry_principal: number;
    registry_clinical: number;
    registry_all: number;
    ratio_osm_to_clinical: number;
  };
  num_admin1: number;
  admin1_min_ratio_clinical: number;
  admin1_max_ratio_clinical: number;
  worst_admin1: string;
  best_admin1: string;
}

interface PsdqNationalSummary {
  generated_at: string;
  claim_scope: string;
  framing_rule: string;
  countries: PsdqCountrySummary[];
}

type MetricMode = "exposure" | "gap" | "ratio";

const METRIC_OPTIONS: Array<{ id: MetricMode; label: string }> = [
  { id: "exposure", label: "Exposure proxy" },
  { id: "gap", label: "Gap share" },
  { id: "ratio", label: "Lowest OSM / registry" },
];

const STRATA_LABELS: Record<string, string> = {
  no_clinical_registry: "No clinical registry",
  zero_osm: "Zero OSM",
  gt0_to_5pct: ">0 to <5%",
  "5_to_10pct": "5 to <10%",
  "10_to_20pct": "10 to <20%",
  "20_to_50pct": "20 to <50%",
  "50_to_100pct": "50 to <100%",
  osm_ge_registry: "OSM >= registry",
};

const ALL_DIVISIONS = "All divisions";

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function pct(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${(value * 100).toFixed(digits)}%`;
}

function metricValue(row: PsdqExposureRow, metric: MetricMode) {
  if (metric === "gap") return row.registry_gap_share;
  if (metric === "ratio") return row.osm_to_active_clinical_ratio;
  return row.underobserved_buildings_3km_p85_proxy;
}

function metricLabel(row: PsdqExposureRow, metric: MetricMode) {
  if (metric === "gap") return pct(row.registry_gap_share, 0);
  if (metric === "ratio") return pct(row.osm_to_active_clinical_ratio, 1);
  return formatNumber(row.underobserved_buildings_3km_p85_proxy);
}

function parseCsv(text: string): PsdqExposureRow[] {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return [];
  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index] || ""]));
    const num = (key: string) => Number(row[key] || 0);
    return {
      division_name: row.division_name,
      district_name: row.district_name,
      upazila_name: row.upazila_name,
      join_key: row.join_key,
      registry_records: num("registry_records"),
      active_facilities: num("active_facilities"),
      active_clinical_facilities: num("active_clinical_facilities"),
      coordinate_facilities: num("coordinate_facilities"),
      osm_health: num("osm_health"),
      osm_hospital: num("osm_hospital"),
      osm_clinic: num("osm_clinic"),
      osm_doctors: num("osm_doctors"),
      osm_to_active_clinical_ratio: num("osm_to_active_clinical_ratio"),
      registry_minus_osm_clinical: num("registry_minus_osm_clinical"),
      registry_gap_share: num("registry_gap_share"),
      buildings_nearest_1km_p85: num("buildings_nearest_1km_p85"),
      buildings_nearest_3km_p85: num("buildings_nearest_3km_p85"),
      buildings_nearest_5km_p85: num("buildings_nearest_5km_p85"),
      underobserved_buildings_3km_p85_proxy: num("underobserved_buildings_3km_p85_proxy"),
      has_open_buildings_denominator: num("has_open_buildings_denominator"),
      has_osm_boundary_match: num("has_osm_boundary_match"),
    };
  });
}

function parseCsvLine(line: string) {
  const cells: string[] = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      cells.push(cell);
      cell = "";
    } else {
      cell += char;
    }
  }
  cells.push(cell);
  return cells;
}

export default function ShowcasePSDQ() {
  const [summary, setSummary] = useState<PsdqExposureSummary | null>(null);
  const [strata, setStrata] = useState<PsdqSourceStrata | null>(null);
  const [validationSample, setValidationSample] = useState<PsdqValidationSample | null>(null);
  const [codedSummary, setCodedSummary] = useState<PsdqValidationCodedSummary | null>(null);
  const [aiReviewSummary, setAiReviewSummary] = useState<PsdqAiReviewSummary | null>(null);
  const [candidateResolutionSummary, setCandidateResolutionSummary] =
    useState<PsdqCandidateResolutionSummary | null>(null);
  const [candidatePublicSourceCheckSummary, setCandidatePublicSourceCheckSummary] =
    useState<PsdqCandidatePublicSourceCheckSummary | null>(null);
  const [national, setNational] = useState<PsdqNationalSummary | null>(null);
  const [rows, setRows] = useState<PsdqExposureRow[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json").then((r) => {
        if (!r.ok) throw new Error(`summary HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/public-service-data-quality-summary.json").then((r) => {
        if (!r.ok) throw new Error(`national HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.json").then((r) => {
        if (!r.ok) throw new Error(`strata HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-sample.json").then((r) => {
        if (!r.ok) throw new Error(`validation sample HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coded-summary.json").then((r) => {
        if (!r.ok) throw new Error(`coded validation HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`AI review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution-summary.json").then((r) => {
        if (!r.ok) throw new Error(`candidate resolution HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json").then((r) => {
        if (!r.ok) throw new Error(`candidate public source check HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.csv").then((r) => {
        if (!r.ok) throw new Error(`csv HTTP ${r.status}`);
        return r.text();
      }),
    ])
      .then(([
        summaryPayload,
        nationalPayload,
        strataPayload,
        validationSamplePayload,
        codedPayload,
        aiReviewPayload,
        candidateResolutionPayload,
        candidatePublicSourceCheckPayload,
        csvText,
      ]) => {
        setSummary(summaryPayload);
        setNational(nationalPayload);
        setStrata(strataPayload);
        setValidationSample(validationSamplePayload);
        setCodedSummary(codedPayload);
        setAiReviewSummary(aiReviewPayload);
        setCandidateResolutionSummary(candidateResolutionPayload);
        setCandidatePublicSourceCheckSummary(candidatePublicSourceCheckPayload);
        setRows(parseCsv(csvText));
      })
      .catch((err) => setError(String(err)));
  }, []);

  const topRow = summary?.top_exposure_gap_upazilas[0];
  const bangladesh = national?.countries.find((country) => country.iso3 === "BGD");

  return (
    <article className="showcase-page">
      <header className="showcase-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When the Map and Registry Disagree
          </h1>
          <p className="showcase-lede">
            This PSDQ report uses the Bangladesh facility-registry deepening to
            ask a narrower question: where does a public map under-observe the
            official clinical registry in places with a large nearby building
            denominator?
          </p>
          <div className="showcase-meta">
            <span>ai-first</span>
            <span>L3 source-disagreement module</span>
            <span>Measurement gap, not facility quality</span>
          </div>
        </div>
        <div className="showcase-hero-panel psdq-hero-panel" aria-label="PSDQ evidence summary">
          {summary ? (
            <>
              <PsdqHeroRails rows={summary.top_exposure_gap_upazilas.slice(0, 3)} />
              <div className="psdq-hero-stats">
                <div>
                  <span className="showcase-stat-value">
                    {strata
                      ? `${strata.coverage.rows_with_open_buildings_denominator}/${strata.coverage.registry_admin_rows}`
                      : summary.exposure.registry_admin_rows}
                  </span>
                  <span className="showcase-stat-label">rows with building denominator</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {formatNumber(summary.exposure.underobserved_buildings_3km_p85_proxy)}
                  </span>
                  <span className="showcase-stat-label">under-observed building proxy</span>
                </div>
                {strata && (
                  <>
                    <div>
                      <span className="showcase-stat-value">
                        {formatNumber(strata.validation_strata.rows_with_zero_osm_health_features)}
                      </span>
                      <span className="showcase-stat-label">zero-OSM rows to validate</span>
                    </div>
                    <div>
                      <span className="showcase-stat-value">
                        {formatNumber(strata.validation_strata.rows_where_osm_equals_or_exceeds_registry)}
                      </span>
                      <span className="showcase-stat-label">OSM &gt;= registry rows</span>
                    </div>
                  </>
                )}
              </div>
            </>
          ) : (
            <span className="showcase-loading">
              {error ? `Could not load PSDQ artifacts: ${error}` : "Loading evidence packet..."}
            </span>
          )}
        </div>
      </header>

      <section className="showcase-section">
        <div className="showcase-section-copy">
          <p className="kicker">The data gap</p>
          <h2>A service-access map can fail before travel time is modeled.</h2>
          <p>
            Facility catchments, service-coverage maps, and road-access
            diagnostics often start by joining a public map to an official
            registry. PSDQ makes the join visible first. The point is not to
            declare a winner between sources; it is to show where the sources
            are too far apart for a planning chart to hide the disagreement.
          </p>
        </div>
      </section>

      {strata && <PsdqValidationPanel strata={strata} />}

      {validationSample && <PsdqValidationSamplePanel sample={validationSample} />}

      {codedSummary && <PsdqValidationCodedPanel summary={codedSummary} />}

      {aiReviewSummary && <PsdqAiReviewPanel summary={aiReviewSummary} />}

      {candidateResolutionSummary && <PsdqCandidateResolutionPanel summary={candidateResolutionSummary} />}

      {candidatePublicSourceCheckSummary && (
        <PsdqCandidatePublicSourceCheckPanel summary={candidatePublicSourceCheckSummary} />
      )}

      {summary && rows.length > 0 && <PsdqExplorer summary={summary} rows={rows} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The largest planning risk is not only the largest facility gap.</h2>
          <p>
            The L3 source-disagreement view pairs the registry-map disagreement with
            Google Open Buildings p85 denominators near coordinate-ready
            facilities. That makes the visual operational: a small public-map
            ratio matters more where many buildings sit near the facilities
            whose visibility is being checked.
          </p>
        </div>
        <div className="showcase-fact-list">
          {topRow && (
            <div>
              <span>Highest exposure-proxy row</span>
              <strong>
                {topRow.upazila_name}, {topRow.district_name}:{" "}
                {formatNumber(topRow.active_clinical_facilities)} DGHS clinical /{" "}
                {formatNumber(topRow.osm_health)} OSM health;{" "}
                {formatNumber(topRow.underobserved_buildings_3km_p85_proxy)} proxy
              </strong>
            </div>
          )}
          {bangladesh && (
            <div>
              <span>National clinical-tier context</span>
              <strong>
                OSM captures {pct(bangladesh.totals.ratio_osm_to_clinical, 1)} of
                DGHS clinical-tier registry counts in the committed PSDQ panel
              </strong>
            </div>
          )}
          {summary && (
            <div>
              <span>Source retrieval record</span>
              <strong>
                OSM base {summary.osm.timestamp_osm_base}; generated {summary.generated_at}
              </strong>
            </div>
          )}
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What this does not mean</p>
          <h2>A registry-map gap is not a verified access or quality result.</h2>
          <p>
            The exposure proxy is not population, households, service demand,
            poverty, travel time, or proof that either source is ground truth.
            It is a source-quality screen that should trigger facility-level
            matching, registry validation, and source-vintage review before a
            service-access claim is made.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Reproduce the deepening</p>
          <code>python public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py</code>
          <code>python public-service-data-quality/scripts/build-bgd-source-disagreement-strata.py</code>
          <a href="/programs/public-service-data-quality/source-disagreement-l3-module.md" download>
            Download L3 evidence note
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.json" download>
            Download strata JSON
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-source-disagreement-strata.csv" download>
            Download strata CSV
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json" download>
            Download summary JSON
          </a>
          <a href="/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement.csv" download>
            Download ranked CSV
          </a>
          <Link to="/public-service-data-quality?view=evidence">
            Read PSDQ evidence packet
          </Link>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={4} />

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">Operational use</p>
          <h2>Use the disagreement screen before drawing the access map.</h2>
          <p>
            A health ministry, statistics office, or ADB operations team could
            use this view as a source-QA gate: identify where registry and
            public-map counts diverge, prioritize validation samples, and keep
            the caveat visible when downstream catchment or road-access
            analysis depends on facility locations.
          </p>
        </div>
        <div className="showcase-source-box">
          <p className="showcase-source-title">Related source QA reports</p>
          <Link to="/showcase/access-map-completeness">Access map-completeness audit</Link>
          <Link to="/showcase/remittance-flow-weighting">Remittance flow-weighting module</Link>
          <Link to="/showcase/air-monitoring-observability">Air-monitoring observability</Link>
          <Link to="/factory">Factory rules</Link>
        </div>
      </section>
    </article>
  );
}

function PsdqValidationPanel({ strata }: { strata: PsdqSourceStrata }) {
  const zeroOsmRow = strata.top_lists.top_zero_osm_high_proxy_upazilas[0];
  const counterExample = strata.top_lists.top_osm_equals_or_exceeds_registry_upazilas[0];
  const roadRow = strata.top_lists.top_road_context_upazilas[0];

  return (
    <section className="showcase-section psdq-validation-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Source validation stack</p>
          <h2>The useful result is the QA ledger behind the map.</h2>
          <p>
            The L3 module does not ask a reader to trust a chart by eye. It
            exposes the rows that can support an exposure screen, the rows that
            still need source validation, and the counterexamples where OSM
            equals or exceeds the registry count.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Open Buildings coverage</span>
            <strong>
              {formatNumber(strata.coverage.rows_with_open_buildings_denominator)} of{" "}
              {formatNumber(strata.coverage.registry_admin_rows)} registry rows have the denominator
            </strong>
          </div>
          <div>
            <span>OSM feature-join residue</span>
            <strong>
              {formatNumber(strata.validation_strata.registry_rows_without_joined_osm_features)} rows
              have no joined OSM feature row; {formatNumber(strata.coverage.osm_features_not_joined_to_registry)} OSM features
              stay outside registry rows
            </strong>
          </div>
          <div>
            <span>Counterexample guardrail</span>
            <strong>
              {formatNumber(strata.validation_strata.rows_where_osm_equals_or_exceeds_registry)} rows have OSM
              counts equal to or above the active registry count
            </strong>
          </div>
          <div>
            <span>Road context eligibility</span>
            <strong>
              {formatNumber(strata.validation_strata.rows_eligible_for_road_surface_score)} rows meet the
              classified-road threshold for the road-context score
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-strata-chart-wrap">
        <PsdqStrataChart strata={strata.ratio_strata} />
      </div>

      <div className="showcase-month-readout psdq-validation-readout">
        <div>
          <span>Zero-OSM validation row</span>
          <strong>
            {zeroOsmRow
              ? `${zeroOsmRow.upazila_name}, ${zeroOsmRow.district_name}: ${formatNumber(zeroOsmRow.active_clinical_facilities)} DGHS clinical and ${formatNumber(zeroOsmRow.underobserved_buildings_3km_p85_proxy)} proxy`
              : "No zero-OSM row in the current artifact"}
          </strong>
        </div>
        <div>
          <span>OSM-above-registry row</span>
          <strong>
            {counterExample
              ? `${counterExample.upazila_name}, ${counterExample.district_name}: ${formatNumber(counterExample.osm_health)} OSM / ${formatNumber(counterExample.active_clinical_facilities)} DGHS`
              : "No OSM-above-registry row in the current artifact"}
          </strong>
        </div>
        <div>
          <span>Road-context top row</span>
          <strong>
            {roadRow
              ? `${roadRow.upazila_name}, ${roadRow.district_name}: score ${formatNumber(roadRow.road_context_score)}`
              : "Road-context artifact not loaded"}
          </strong>
        </div>
      </div>
    </section>
  );
}

function PsdqValidationSamplePanel({ sample }: { sample: PsdqValidationSample }) {
  return (
    <section className="showcase-section psdq-sample-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Facility validation sample</p>
          <h2>The next task is bounded before anyone starts matching by eye.</h2>
          <p>
            The sample design turns the upazila-level source ledger into a
            public-source coding sheet. It selects rows from high-gap,
            zero-OSM, OSM-above-registry, and comparison groups, then leaves
            the validation outcomes blank until a reviewer checks DGHS rows
            against public OSM evidence.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Sampled upazilas</span>
            <strong>{formatNumber(sample.sample_summary.sampled_upazilas)} rows across four groups</strong>
          </div>
          <div>
            <span>Coding sheet size</span>
            <strong>{formatNumber(sample.sample_summary.coding_sheet_rows)} DGHS facility rows</strong>
          </div>
          <div>
            <span>Coordinate-ready review rows</span>
            <strong>{formatNumber(sample.sample_summary.coordinate_ready_facility_rows)} rows include DGHS coordinates</strong>
          </div>
          <div>
            <span>Artifact status</span>
            <strong>{sample.status.replaceAll("_", " ")}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-sample-grid" aria-label="PSDQ facility validation sample groups">
        {sample.sample_summary.groups.map((group) => (
          <div key={group.sample_group}>
            <span>{sampleGroupLabel(group.sample_group)}</span>
            <strong>{formatNumber(group.upazila_count)} upazilas</strong>
            <em>
              {formatNumber(group.facility_rows)} DGHS rows;{" "}
              {formatNumber(group.coordinate_ready_facility_rows)} coordinate-ready
            </em>
          </div>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Reproduce and code the sample</p>
        <code>python public-service-data-quality/scripts/design-bgd-facility-validation-sample.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-sample.md" download>
          Download validation sample note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-sample.json" download>
          Download sample JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-sample-upazilas.csv" download>
          Download upazila sample CSV
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-sample-facilities.csv" download>
          Download facility sample CSV
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coding-sheet.csv" download>
          Download blank coding sheet
        </a>
        <p className="psdq-method-note">
          Non-claim: {sample.non_claim} Validation codes available:{" "}
          {sample.validation_codes.map((item) => item.code).join(", ")}.
        </p>
      </div>
    </section>
  );
}

const VALIDATION_CODE_ORDER = [
  "missing_public_map_point",
  "registry_coordinate_issue",
  "confirmed_same_facility",
  "probable_duplicate_or_alias",
  "classification_mismatch",
  "osm_only_candidate",
  "unresolved_public_sources",
] as const;

const VALIDATION_CODE_LABELS: Record<string, string> = {
  confirmed_same_facility: "Confirmed",
  probable_duplicate_or_alias: "Probable alias",
  classification_mismatch: "Class mismatch",
  registry_coordinate_issue: "Coordinate issue",
  missing_public_map_point: "Missing map point",
  osm_only_candidate: "OSM-only",
  unresolved_public_sources: "Unresolved",
};

function validationCodeColor(code: string) {
  const colors: Record<string, string> = {
    confirmed_same_facility: "#5A8227",
    probable_duplicate_or_alias: "#007DB8",
    classification_mismatch: "#7A4E15",
    registry_coordinate_issue: "#D97706",
    missing_public_map_point: "#9B2226",
    osm_only_candidate: "#4A5568",
    unresolved_public_sources: "#A0AEC0",
  };
  return colors[code] || "#6c757d";
}

function validationCount(summary: PsdqValidationCodedSummary, code: string) {
  return summary.validation_code_counts.find((item) => item.validation_code === code)?.rows || 0;
}

function PsdqValidationCodedPanel({ summary }: { summary: PsdqValidationCodedSummary }) {
  return (
    <section className="showcase-section psdq-coded-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Automated coded screen</p>
          <h2>The first source check separates map absence from coordinate problems.</h2>
          <p>
            The coded screen filters the cached Bangladesh OSM health-feature
            pull within 500 meters of each sampled DGHS coordinate and checks
            whether the coordinate sits inside the sampled upazila boundary.
            The result is a flagged source-review queue, not a final validation claim.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows coded</span>
            <strong>{formatNumber(summary.screen_summary.coded_rows)} sampled DGHS rows</strong>
          </div>
          <div>
            <span>Missing public-map point</span>
            <strong>{formatNumber(validationCount(summary, "missing_public_map_point"))} rows</strong>
          </div>
          <div>
            <span>Registry coordinate issue</span>
            <strong>{formatNumber(validationCount(summary, "registry_coordinate_issue"))} rows</strong>
          </div>
          <div>
            <span>Flagged review queue</span>
            <strong>{formatNumber(summary.screen_summary.manual_review_recommended_rows)} rows</strong>
          </div>
        </div>
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqValidationCodeChart groups={summary.validation_code_counts_by_group} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ validation code legend">
        {VALIDATION_CODE_ORDER.filter((code) => validationCount(summary, code) > 0).map((code) => (
          <span key={code}>
            <i style={{ background: validationCodeColor(code) }} /> {VALIDATION_CODE_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the coded screen</p>
        <code>python public-service-data-quality/scripts/code-bgd-facility-validation-sample.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-coded-screen.md" download>
          Download coded-screen note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coded-summary.json" download>
          Download coded summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coded-screen.csv" download>
          Download coded screen CSV
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-osm-candidates.csv" download>
          Download OSM candidates CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqValidationCodeChart({ groups }: { groups: PsdqValidationGroupCount[] }) {
  const width = 1040;
  const rowHeight = 58;
  const headerHeight = 54;
  const height = headerHeight + groups.length * rowHeight + 26;
  const labelX = 0;
  const barX = 230;
  const barWidth = 540;
  const countX = 805;

  return (
    <svg
      className="psdq-coded-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Automated validation codes by PSDQ sample group"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Automated validation-code screen
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: sampled DGHS facility row; source: coded validation summary JSON
      </text>
      <text x={barX} y={52} className="psdq-chart-head">
        Code mix
      </text>
      <text x={countX} y={52} className="psdq-chart-head">
        Missing / coordinate / confirmed
      </text>

      {groups.map((group, index) => {
        const y = headerHeight + index * rowHeight;
        let x = barX;
        return (
          <g key={group.sample_group}>
            <text x={labelX} y={y + 18} className="psdq-row-label">
              {sampleGroupLabel(group.sample_group)}
            </text>
            <text x={labelX} y={y + 36} className="psdq-row-sub">
              {formatNumber(group.rows)} sampled rows
            </text>
            <rect x={barX} y={y} width={barWidth} height={24} fill="#eef2f5" />
            {VALIDATION_CODE_ORDER.map((code) => {
              const value = Number(group[code] || 0);
              const segmentWidth = group.rows > 0 ? (value / group.rows) * barWidth : 0;
              const segment = (
                <rect
                  key={code}
                  x={x}
                  y={y}
                  width={Math.max(0, segmentWidth)}
                  height={24}
                  fill={validationCodeColor(code)}
                >
                  <title>{`${sampleGroupLabel(group.sample_group)}: ${formatNumber(value)} ${VALIDATION_CODE_LABELS[code]}`}</title>
                </rect>
              );
              x += segmentWidth;
              return segment;
            })}
            <text x={countX} y={y + 17} className="psdq-value">
              {formatNumber(group.missing_public_map_point)} / {formatNumber(group.registry_coordinate_issue)} /{" "}
              {formatNumber(group.confirmed_same_facility)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

const AI_REVIEW_BUCKET_ORDER = [
  "public_map_gap_at_valid_coordinate",
  "registry_coordinate_repair",
  "candidate_name_or_type_resolution",
  "nearby_osm_without_registry_match",
  "unresolved_public_source_check",
] as const;

const AI_REVIEW_BUCKET_LABELS: Record<string, string> = {
  public_map_gap_at_valid_coordinate: "Public-map gap",
  registry_coordinate_repair: "Coordinate repair",
  candidate_name_or_type_resolution: "Name/type resolution",
  nearby_osm_without_registry_match: "Nearby OSM, no match",
  unresolved_public_source_check: "Unresolved source",
};

function aiReviewBucketColor(bucket: string) {
  const colors: Record<string, string> = {
    public_map_gap_at_valid_coordinate: "#9B2226",
    registry_coordinate_repair: "#D97706",
    candidate_name_or_type_resolution: "#007DB8",
    nearby_osm_without_registry_match: "#4A5568",
    unresolved_public_source_check: "#A0AEC0",
  };
  return colors[bucket] || "#6c757d";
}

function aiReviewCount(summary: PsdqAiReviewSummary, bucket: string) {
  return summary.ai_review_bucket_counts.find((item) => item.name === bucket)?.rows || 0;
}

function PsdqAiReviewPanel({ summary }: { summary: PsdqAiReviewSummary }) {
  const priorityOne =
    summary.ai_review_priority_counts.find((item) => item.name === "priority_1_candidate_resolution")?.rows || 0;
  const highExposureGap =
    summary.ai_review_priority_counts.find((item) => item.name === "priority_1_high_exposure_map_gap")?.rows || 0;

  return (
    <section className="showcase-section psdq-ai-review-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">AI public-source review ledger</p>
          <h2>The 71-row queue now has named evidence workstreams.</h2>
          <p>
            The AI review pass does not close the validation task. It reads the
            automated coded screen and OSM candidate table, then separates the
            flagged rows into workstreams a reviewer can act on: public-map
            absence at a usable coordinate, registry-coordinate repair,
            name/type resolution, and nearby OSM features without a registry
            name match.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Flagged rows reviewed</span>
            <strong>{formatNumber(summary.review_scope.flagged_rows_reviewed)} rows remain open</strong>
          </div>
          <div>
            <span>Candidate-resolution first</span>
            <strong>{formatNumber(priorityOne)} rows have OSM candidates that need name/type inspection</strong>
          </div>
          <div>
            <span>High-exposure map gaps</span>
            <strong>{formatNumber(highExposureGap)} rows have no OSM health point in high-gap groups</strong>
          </div>
          <div>
            <span>Coordinate-source repair</span>
            <strong>{formatNumber(summary.review_scope.coordinate_source_issue_rows)} rows before map matching</strong>
          </div>
        </div>
      </div>

      <div className="psdq-ai-review-grid">
        {AI_REVIEW_BUCKET_ORDER.filter((bucket) => aiReviewCount(summary, bucket) > 0).map((bucket) => (
          <div key={bucket}>
            <span>{AI_REVIEW_BUCKET_LABELS[bucket]}</span>
            <strong>{formatNumber(aiReviewCount(summary, bucket))}</strong>
            <em>{aiReviewBucketMeaning(bucket)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqAiReviewBucketChart groups={summary.ai_review_bucket_counts_by_group} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ AI review bucket legend">
        {AI_REVIEW_BUCKET_ORDER.filter((bucket) => aiReviewCount(summary, bucket) > 0).map((bucket) => (
          <span key={bucket}>
            <i style={{ background: aiReviewBucketColor(bucket) }} /> {AI_REVIEW_BUCKET_LABELS[bucket]}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the review ledger</p>
        <code>python public-service-data-quality/scripts/review-bgd-facility-validation-flags.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-ai-review.md" download>
          Download AI review note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review-summary.json" download>
          Download AI review summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-ai-review.csv" download>
          Download row-review CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function aiReviewBucketMeaning(bucket: string) {
  const meanings: Record<string, string> = {
    public_map_gap_at_valid_coordinate: "No pinned OSM health feature within 500m.",
    registry_coordinate_repair: "Coordinate missing or outside expected upazila.",
    candidate_name_or_type_resolution: "Nearby candidate exists, but name or class is unresolved.",
    nearby_osm_without_registry_match: "OSM health feature nearby, weak row-level match.",
    unresolved_public_source_check: "Available public artifacts do not support a stable row code.",
  };
  return meanings[bucket] || bucket.replaceAll("_", " ");
}

const CANDIDATE_RESOLUTION_ORDER = [
  "probable_same_facility_alias_or_campus",
  "probable_same_site_classification_conflict",
  "possible_alias_requires_name_check",
  "local_script_candidate_requires_name_check",
  "ambiguous_nearby_candidate",
  "weak_nearby_osm_signal",
] as const;

const CANDIDATE_RESOLUTION_LABELS: Record<string, string> = {
  probable_same_facility_alias_or_campus: "Alias/campus signal",
  probable_same_site_classification_conflict: "Same-site type conflict",
  possible_alias_requires_name_check: "Possible alias",
  local_script_candidate_requires_name_check: "Local-script name gap",
  ambiguous_nearby_candidate: "Ambiguous nearby",
  weak_nearby_osm_signal: "Weak nearby signal",
};

function candidateResolutionColor(code: string) {
  const colors: Record<string, string> = {
    probable_same_facility_alias_or_campus: "#005F73",
    probable_same_site_classification_conflict: "#007DB8",
    possible_alias_requires_name_check: "#D97706",
    local_script_candidate_requires_name_check: "#0F766E",
    ambiguous_nearby_candidate: "#4A5568",
    weak_nearby_osm_signal: "#A0AEC0",
  };
  return colors[code] || "#6c757d";
}

function candidateResolutionCount(summary: PsdqCandidateResolutionSummary, code: string) {
  return summary.candidate_resolution_code_counts.find((item) => item.name === code)?.rows || 0;
}

function PsdqCandidateResolutionPanel({ summary }: { summary: PsdqCandidateResolutionSummary }) {
  const aliasSignals =
    candidateResolutionCount(summary, "probable_same_facility_alias_or_campus") +
    candidateResolutionCount(summary, "possible_alias_requires_name_check");
  const typeConflicts = candidateResolutionCount(summary, "probable_same_site_classification_conflict");
  const weakOrAmbiguous =
    candidateResolutionCount(summary, "ambiguous_nearby_candidate") +
    candidateResolutionCount(summary, "weak_nearby_osm_signal");

  return (
    <section className="showcase-section psdq-candidate-resolution-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Candidate-resolution pass</p>
          <h2>The eight candidate cases are no longer one blurry queue.</h2>
          <p>
            The second pass reads the AI review ledger and ranked OSM
            candidates, then sorts the 8 row-level candidate cases into review
            lanes. It keeps every row open: the value is a sharper worklist,
            not a same-facility decision.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Candidate rows reviewed</span>
            <strong>{formatNumber(summary.resolution_scope.candidate_resolution_rows_reviewed)} rows</strong>
          </div>
          <div>
            <span>Confirmed same-facility closures</span>
            <strong>{formatNumber(summary.resolution_scope.rows_closed_as_confirmed_same_facility)} rows</strong>
          </div>
          <div>
            <span>Alias or campus checks</span>
            <strong>{formatNumber(aliasSignals)} rows still need public-name confirmation</strong>
          </div>
          <div>
            <span>Type-conflict checks</span>
            <strong>{formatNumber(typeConflicts)} rows need classification review</strong>
          </div>
          <div>
            <span>Weak or ambiguous signals</span>
            <strong>{formatNumber(weakOrAmbiguous)} rows should not be treated as matches</strong>
          </div>
        </div>
      </div>

      <div className="psdq-resolution-grid">
        {CANDIDATE_RESOLUTION_ORDER.filter((code) => candidateResolutionCount(summary, code) > 0).map((code) => (
          <div key={code}>
            <span>{CANDIDATE_RESOLUTION_LABELS[code]}</span>
            <strong>{formatNumber(candidateResolutionCount(summary, code))}</strong>
            <em>{candidateResolutionMeaning(code)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqCandidateResolutionChart groups={summary.candidate_resolution_counts_by_group} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ candidate-resolution lane legend">
        {CANDIDATE_RESOLUTION_ORDER.filter((code) => candidateResolutionCount(summary, code) > 0).map((code) => (
          <span key={code}>
            <i style={{ background: candidateResolutionColor(code) }} /> {CANDIDATE_RESOLUTION_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the candidate pass</p>
        <code>python public-service-data-quality/scripts/resolve-bgd-facility-candidate-rows.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-candidate-resolution.md" download>
          Download candidate-resolution note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution-summary.json" download>
          Download candidate-resolution summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-resolution.csv" download>
          Download candidate-resolution CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function candidateResolutionMeaning(code: string) {
  const meanings: Record<string, string> = {
    probable_same_facility_alias_or_campus: "Very close, category-compatible, but still open.",
    probable_same_site_classification_conflict: "Nearby feature, type conflict unresolved.",
    possible_alias_requires_name_check: "Name signal exists; public name source needed.",
    local_script_candidate_requires_name_check: "Close non-Latin OSM name needs source check.",
    ambiguous_nearby_candidate: "Mixed distance, name, or type evidence.",
    weak_nearby_osm_signal: "Nearby feature exists, but row match is weak.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function PsdqCandidateResolutionChart({ groups }: { groups: PsdqCandidateResolutionGroupCount[] }) {
  const width = 1040;
  const rowHeight = 58;
  const headerHeight = 54;
  const height = headerHeight + groups.length * rowHeight + 26;
  const labelX = 0;
  const barX = 230;
  const barWidth = 540;
  const countX = 805;

  return (
    <svg
      className="psdq-coded-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Candidate-resolution lanes by PSDQ sample group"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Eight candidate cases, kept open by review lane
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: sampled DGHS row queued for candidate-level public-source resolution
      </text>
      <text x={barX} y={52} className="psdq-chart-head">
        Lane mix
      </text>
      <text x={countX} y={52} className="psdq-chart-head">
        Alias / type / weak
      </text>

      {groups.map((group, index) => {
        const y = headerHeight + index * rowHeight;
        let x = barX;
        return (
          <g key={group.sample_group}>
            <text x={labelX} y={y + 18} className="psdq-row-label">
              {sampleGroupLabel(group.sample_group)}
            </text>
            <text x={labelX} y={y + 36} className="psdq-row-sub">
              {formatNumber(group.rows)} candidate rows
            </text>
            <rect x={barX} y={y} width={barWidth} height={24} fill="#eef2f5" />
            {CANDIDATE_RESOLUTION_ORDER.map((code) => {
              const value = Number(group[code] || 0);
              const segmentWidth = group.rows > 0 ? (value / group.rows) * barWidth : 0;
              const segment = (
                <rect
                  key={code}
                  x={x}
                  y={y}
                  width={Math.max(0, segmentWidth)}
                  height={24}
                  fill={candidateResolutionColor(code)}
                >
                  <title>{`${sampleGroupLabel(group.sample_group)}: ${formatNumber(value)} ${CANDIDATE_RESOLUTION_LABELS[code]}`}</title>
                </rect>
              );
              x += segmentWidth;
              return segment;
            })}
            <text x={countX} y={y + 17} className="psdq-value">
              {formatNumber(group.probable_same_facility_alias_or_campus + group.possible_alias_requires_name_check)} /{" "}
              {formatNumber(group.probable_same_site_classification_conflict)} /{" "}
              {formatNumber(group.ambiguous_nearby_candidate + group.weak_nearby_osm_signal)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

const PUBLIC_SOURCE_CHECK_ORDER = [
  "strong_same_site_osm_tag_support_requires_human_confirmation",
  "same_site_type_or_label_conflict_requires_public_label_check",
  "name_support_but_coordinate_or_function_conflict",
  "nearby_features_do_not_support_registry_name",
] as const;

const PUBLIC_SOURCE_CHECK_LABELS: Record<string, string> = {
  strong_same_site_osm_tag_support_requires_human_confirmation: "Same-site tag support",
  same_site_type_or_label_conflict_requires_public_label_check: "Type/label conflict",
  name_support_but_coordinate_or_function_conflict: "Name plus conflict",
  nearby_features_do_not_support_registry_name: "No registry-name support",
};

function publicSourceCheckColor(code: string) {
  const colors: Record<string, string> = {
    strong_same_site_osm_tag_support_requires_human_confirmation: "#005F73",
    same_site_type_or_label_conflict_requires_public_label_check: "#D97706",
    name_support_but_coordinate_or_function_conflict: "#007DB8",
    nearby_features_do_not_support_registry_name: "#4A5568",
  };
  return colors[code] || "#6c757d";
}

function publicSourceCheckCount(summary: PsdqCandidatePublicSourceCheckSummary, code: string) {
  return summary.public_source_check_code_counts.find((item) => item.name === code)?.rows || 0;
}

function PsdqCandidatePublicSourceCheckPanel({ summary }: { summary: PsdqCandidatePublicSourceCheckSummary }) {
  const strongSupport = publicSourceCheckCount(
    summary,
    "strong_same_site_osm_tag_support_requires_human_confirmation",
  );
  const unresolved =
    publicSourceCheckCount(summary, "nearby_features_do_not_support_registry_name") +
    publicSourceCheckCount(summary, "name_support_but_coordinate_or_function_conflict");

  return (
    <section className="showcase-section psdq-public-source-check-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Richer public-source tag scan</p>
          <h2>The strongest evidence is still a worklist, not a closure.</h2>
          <p>
            The next pass reads full OSM tags and cached DGHS registry fields.
            It uses `name:en`, `name:bn`, address, operator, website,
            emergency, and healthcare tags to separate same-site evidence from
            coordinate, function, and nearby-feature conflicts.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows checked</span>
            <strong>{formatNumber(summary.confirmation_scope.candidate_rows_checked)} candidate rows</strong>
          </div>
          <div>
            <span>Rows closed</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_closed_as_confirmed_same_facility)} same-facility closures</strong>
          </div>
          <div>
            <span>Specific OSM name-tag support</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_with_specific_osm_name_tag_support)} rows</strong>
          </div>
          <div>
            <span>Same-site tag support</span>
            <strong>{formatNumber(strongSupport)} rows still need confirmation</strong>
          </div>
          <div>
            <span>Still unresolved</span>
            <strong>{formatNumber(unresolved)} rows have conflict or weak name support</strong>
          </div>
        </div>
      </div>

      <div className="psdq-source-check-grid">
        {PUBLIC_SOURCE_CHECK_ORDER.filter((code) => publicSourceCheckCount(summary, code) > 0).map((code) => (
          <div key={code}>
            <span>{PUBLIC_SOURCE_CHECK_LABELS[code]}</span>
            <strong>{formatNumber(publicSourceCheckCount(summary, code))}</strong>
            <em>{publicSourceCheckMeaning(code)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqPublicSourceCheckChart groups={summary.public_source_check_counts_by_resolution_lane} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ public-source check lane legend">
        {PUBLIC_SOURCE_CHECK_ORDER.map((code) => (
          <span key={code}>
            <i style={{ background: publicSourceCheckColor(code) }} /> {PUBLIC_SOURCE_CHECK_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the source check</p>
        <code>python public-service-data-quality/scripts/check-bgd-facility-candidate-public-sources.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-candidate-public-source-check.md" download>
          Download public-source check note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json" download>
          Download public-source check summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-candidate-public-source-check.csv" download>
          Download public-source check CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function publicSourceCheckMeaning(code: string) {
  const meanings: Record<string, string> = {
    strong_same_site_osm_tag_support_requires_human_confirmation: "OSM tags support the sampled name at same-site distance.",
    same_site_type_or_label_conflict_requires_public_label_check: "The point is close, but the public labels differ.",
    name_support_but_coordinate_or_function_conflict: "Name support exists, but distance or function blocks closure.",
    nearby_features_do_not_support_registry_name: "Nearby OSM features do not support the registry name.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function PsdqPublicSourceCheckChart({ groups }: { groups: PsdqCandidatePublicSourceCheckGroupCount[] }) {
  const width = 1040;
  const rowHeight = 58;
  const headerHeight = 54;
  const height = headerHeight + groups.length * rowHeight + 26;
  const labelX = 0;
  const barX = 285;
  const barWidth = 500;
  const countX = 820;

  return (
    <svg
      className="psdq-coded-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Public-source check lanes by PSDQ candidate-resolution lane"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Public-source tag support for the eight open candidate rows
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: sampled DGHS row; source: cached DGHS registry rows and pinned OSM tags
      </text>
      <text x={barX} y={52} className="psdq-chart-head">
        Source-check mix
      </text>
      <text x={countX} y={52} className="psdq-chart-head">
        Strong / conflict / weak
      </text>

      {groups.map((group, index) => {
        const y = headerHeight + index * rowHeight;
        let x = barX;
        return (
          <g key={group.candidate_resolution_code}>
            <text x={labelX} y={y + 18} className="psdq-row-label">
              {CANDIDATE_RESOLUTION_LABELS[group.candidate_resolution_code] || group.candidate_resolution_code.replaceAll("_", " ")}
            </text>
            <text x={labelX} y={y + 36} className="psdq-row-sub">
              {formatNumber(group.rows)} candidate rows
            </text>
            <rect x={barX} y={y} width={barWidth} height={24} fill="#eef2f5" />
            {PUBLIC_SOURCE_CHECK_ORDER.map((code) => {
              const value = Number(group[code] || 0);
              const segmentWidth = group.rows > 0 ? (value / group.rows) * barWidth : 0;
              const segment = (
                <rect
                  key={code}
                  x={x}
                  y={y}
                  width={Math.max(0, segmentWidth)}
                  height={24}
                  fill={publicSourceCheckColor(code)}
                >
                  <title>{`${group.candidate_resolution_code}: ${formatNumber(value)} ${PUBLIC_SOURCE_CHECK_LABELS[code]}`}</title>
                </rect>
              );
              x += segmentWidth;
              return segment;
            })}
            <text x={countX} y={y + 17} className="psdq-value">
              {formatNumber(group.strong_same_site_osm_tag_support_requires_human_confirmation)} /{" "}
              {formatNumber(
                group.same_site_type_or_label_conflict_requires_public_label_check +
                  group.name_support_but_coordinate_or_function_conflict,
              )} /{" "}
              {formatNumber(group.nearby_features_do_not_support_registry_name)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function PsdqAiReviewBucketChart({ groups }: { groups: PsdqAiReviewGroupCount[] }) {
  const width = 1040;
  const rowHeight = 58;
  const headerHeight = 54;
  const height = headerHeight + groups.length * rowHeight + 26;
  const labelX = 0;
  const barX = 230;
  const barWidth = 540;
  const countX = 805;

  return (
    <svg
      className="psdq-coded-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="AI public-source review buckets by PSDQ sample group"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        AI review workstreams for flagged rows
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: sampled DGHS row still requiring review; source: AI review summary JSON
      </text>
      <text x={barX} y={52} className="psdq-chart-head">
        Workstream mix
      </text>
      <text x={countX} y={52} className="psdq-chart-head">
        Map gap / coordinate / candidate
      </text>

      {groups.map((group, index) => {
        const y = headerHeight + index * rowHeight;
        let x = barX;
        return (
          <g key={group.sample_group}>
            <text x={labelX} y={y + 18} className="psdq-row-label">
              {sampleGroupLabel(group.sample_group)}
            </text>
            <text x={labelX} y={y + 36} className="psdq-row-sub">
              {formatNumber(group.rows)} flagged rows
            </text>
            <rect x={barX} y={y} width={barWidth} height={24} fill="#eef2f5" />
            {AI_REVIEW_BUCKET_ORDER.map((bucket) => {
              const value = Number(group[bucket] || 0);
              const segmentWidth = group.rows > 0 ? (value / group.rows) * barWidth : 0;
              const segment = (
                <rect
                  key={bucket}
                  x={x}
                  y={y}
                  width={Math.max(0, segmentWidth)}
                  height={24}
                  fill={aiReviewBucketColor(bucket)}
                >
                  <title>{`${sampleGroupLabel(group.sample_group)}: ${formatNumber(value)} ${AI_REVIEW_BUCKET_LABELS[bucket]}`}</title>
                </rect>
              );
              x += segmentWidth;
              return segment;
            })}
            <text x={countX} y={y + 17} className="psdq-value">
              {formatNumber(group.public_map_gap_at_valid_coordinate)} /{" "}
              {formatNumber(group.registry_coordinate_repair)} /{" "}
              {formatNumber(group.candidate_name_or_type_resolution + group.nearby_osm_without_registry_match)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function sampleGroupLabel(group: string) {
  const labels: Record<string, string> = {
    high_exposure_gap: "High exposure gap",
    zero_osm_high_proxy: "Zero OSM, high proxy",
    osm_ge_registry: "OSM >= registry",
    comparison_mid_ratio: "Mid-ratio comparison",
  };
  return labels[group] || group.replaceAll("_", " ");
}

function PsdqStrataChart({ strata }: { strata: PsdqRatioStratum[] }) {
  const width = 1040;
  const rowHeight = 38;
  const headerHeight = 58;
  const bottom = 20;
  const height = headerHeight + strata.length * rowHeight + bottom;
  const labelX = 0;
  const barX = 210;
  const barWidth = 250;
  const activeX = 500;
  const osmX = 650;
  const proxyX = 780;
  const maxRows = Math.max(1, ...strata.map((row) => row.row_count));

  return (
    <svg
      className="psdq-strata-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Bangladesh PSDQ ratio strata and validation buckets"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Ratio strata used as validation gates
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: DGHS registry upazila row; source: generated PSDQ L3 strata JSON
      </text>
      <text x={barX} y={54} className="psdq-chart-head">
        Rows
      </text>
      <text x={activeX} y={54} className="psdq-chart-head">
        DGHS clinical
      </text>
      <text x={osmX} y={54} className="psdq-chart-head">
        OSM health
      </text>
      <text x={proxyX} y={54} className="psdq-chart-head">
        Under-observed proxy
      </text>

      {strata.map((row, index) => {
        const y = headerHeight + index * rowHeight;
        const rowWidth = (row.row_count / maxRows) * barWidth;
        return (
          <g key={row.bucket}>
            <text x={labelX} y={y + 16} className="psdq-row-label">
              {STRATA_LABELS[row.bucket] || row.label}
            </text>
            <rect x={barX} y={y} width={barWidth} height={18} fill="#eef2f5" />
            <rect
              x={barX}
              y={y}
              width={Math.max(1, rowWidth)}
              height={18}
              fill={strataBucketColor(row.bucket)}
            >
              <title>{`${row.label}: ${formatNumber(row.row_count)} rows`}</title>
            </rect>
            <text x={barX + barWidth + 12} y={y + 14} className="psdq-value">
              {formatNumber(row.row_count)}
            </text>
            <text x={activeX} y={y + 14} className="psdq-value">
              {formatNumber(row.active_clinical_facilities)}
            </text>
            <text x={osmX} y={y + 14} className="psdq-value">
              {formatNumber(row.osm_health)}
            </text>
            <text x={proxyX} y={y + 14} className="psdq-value">
              {formatNumber(row.underobserved_buildings_3km_p85_proxy)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function strataBucketColor(bucket: string) {
  if (bucket === "zero_osm") return "#9b2226";
  if (bucket === "osm_ge_registry") return "#5A8227";
  if (bucket === "no_clinical_registry") return "#6c757d";
  return "#007DB8";
}

function PsdqHeroRails({ rows }: { rows: PsdqExposureRow[] }) {
  const maxClinical = Math.max(1, ...rows.map((row) => row.active_clinical_facilities));
  return (
    <div className="psdq-hero-rails" aria-label="Top PSDQ registry-map rows">
      <p className="showcase-source-title">Registry visible on the public map</p>
      {rows.map((row) => (
        <div className="psdq-hero-row" key={row.join_key}>
          <div>
            <strong>{row.upazila_name}</strong>
            <span>{row.district_name}</span>
          </div>
          <div className="psdq-hero-bars" aria-label={`${row.upazila_name} registry and OSM counts`}>
            <i
              className="psdq-registry-bar"
              style={{ width: `${Math.max(3, (row.active_clinical_facilities / maxClinical) * 100)}%` }}
            />
            <i
              className="psdq-osm-bar"
              style={{ width: `${Math.max(2, (row.osm_health / maxClinical) * 100)}%` }}
            />
          </div>
          <em>{pct(row.osm_to_active_clinical_ratio, 0)}</em>
        </div>
      ))}
      <div className="shock-hero-key">
        <span><i className="psdq-registry-key" /> DGHS clinical registry</span>
        <span><i className="psdq-osm-key" /> OSM health features</span>
      </div>
    </div>
  );
}

function PsdqExplorer({
  summary,
  rows,
}: {
  summary: PsdqExposureSummary;
  rows: PsdqExposureRow[];
}) {
  const [metric, setMetric] = useState<MetricMode>("exposure");
  const [division, setDivision] = useState(ALL_DIVISIONS);
  const [selectedJoinKey, setSelectedJoinKey] = useState("");

  const divisions = useMemo(
    () => [
      ALL_DIVISIONS,
      ...Array.from(new Set(rows.map((row) => row.division_name))).sort((a, b) => a.localeCompare(b)),
    ],
    [rows],
  );

  const filteredRows = useMemo(() => {
    const pool = rows.filter((row) => {
      const inDivision = division === ALL_DIVISIONS || row.division_name === division;
      return inDivision && row.has_open_buildings_denominator === 1 && row.active_clinical_facilities >= 20;
    });
    return pool.sort((a, b) => {
      if (metric === "ratio") {
        return (
          a.osm_to_active_clinical_ratio - b.osm_to_active_clinical_ratio ||
          b.active_clinical_facilities - a.active_clinical_facilities
        );
      }
      return metricValue(b, metric) - metricValue(a, metric);
    });
  }, [division, metric, rows]);

  const displayRows = filteredRows.slice(0, 16);
  const selectedRow =
    filteredRows.find((row) => row.join_key === selectedJoinKey) ||
    displayRows[0] ||
    filteredRows[0];

  return (
    <section className="showcase-section showcase-explorer">
      <div className="showcase-explorer-head">
        <div>
          <p className="kicker">Interactive evidence view</p>
          <h2>Rank the gap by the question being asked.</h2>
          <p>
            The chart keeps the source disagreement visible. Blue cells are the
            OSM-visible share of the DGHS clinical registry; red cells are the
            registry share not visible in the public-map count. The bar on the
            right is the 3 km p85 under-observed building proxy.
          </p>
        </div>
        <div className="showcase-controls" aria-label="PSDQ explorer controls">
          <div className="showcase-filter-buttons psdq-filter-buttons" role="group" aria-label="Select PSDQ metric">
            {METRIC_OPTIONS.map((option) => (
              <button
                key={option.id}
                type="button"
                className={metric === option.id ? "showcase-control-active" : ""}
                onClick={() => {
                  setMetric(option.id);
                  setSelectedJoinKey("");
                }}
              >
                {option.label}
              </button>
            ))}
          </div>
          <label>
            <span>Division</span>
            <select
              value={division}
              onChange={(event) => {
                setDivision(event.target.value);
                setSelectedJoinKey("");
              }}
            >
              {divisions.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span>Focus upazila</span>
            <select
              value={selectedRow?.join_key || ""}
              onChange={(event) => setSelectedJoinKey(event.target.value)}
            >
              {filteredRows.slice(0, 80).map((row) => (
                <option key={row.join_key} value={row.join_key}>
                  {row.upazila_name}, {row.district_name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      <div className="psdq-chart-wrap">
        <PsdqDisagreementChart
          rows={displayRows}
          metric={metric}
          selectedJoinKey={selectedRow?.join_key}
          onSelect={setSelectedJoinKey}
        />
      </div>

      <div className="freshness-legend psdq-legend" aria-label="PSDQ source legend">
        <span><i style={{ background: "#007DB8" }} /> OSM-visible registry share</span>
        <span><i style={{ background: "#9b2226" }} /> Registry share not visible in OSM count</span>
        <span><i style={{ background: "#FBB00E" }} /> Selected row</span>
        <span><i style={{ background: "#5A8227" }} /> Under-observed building proxy</span>
      </div>

      <div className="showcase-month-readout">
        <div>
          <span>Selected upazila</span>
          <strong>
            {selectedRow
              ? `${selectedRow.upazila_name}, ${selectedRow.district_name}, ${selectedRow.division_name}`
              : "Select a row"}
          </strong>
        </div>
        <div>
          <span>Registry and public-map counts</span>
          <strong>
            {selectedRow
              ? `${formatNumber(selectedRow.active_clinical_facilities)} DGHS clinical; ${formatNumber(selectedRow.osm_health)} OSM health; ${pct(selectedRow.osm_to_active_clinical_ratio, 1)} OSM / registry`
              : "missing"}
          </strong>
        </div>
        <div>
          <span>Exposure proxy</span>
          <strong>
            {selectedRow
              ? `${formatNumber(selectedRow.underobserved_buildings_3km_p85_proxy)} of ${formatNumber(selectedRow.buildings_nearest_3km_p85)} p85 buildings`
              : "missing"}
          </strong>
        </div>
      </div>

      <p className="psdq-method-note">
        Source method: {summary.method} Non-claim: {summary.non_claim}
      </p>
    </section>
  );
}

function PsdqDisagreementChart({
  rows,
  metric,
  selectedJoinKey,
  onSelect,
}: {
  rows: PsdqExposureRow[];
  metric: MetricMode;
  selectedJoinKey?: string;
  onSelect: (joinKey: string) => void;
}) {
  const width = 1040;
  const rowHeight = 40;
  const headerHeight = 58;
  const bottom = 22;
  const height = headerHeight + rows.length * rowHeight + bottom;
  const labelWidth = 232;
  const cellCount = 24;
  const cellSize = 8;
  const cellGap = 2;
  const stripX = labelWidth + 8;
  const stripWidth = cellCount * cellSize + (cellCount - 1) * cellGap;
  const ratioX = stripX + stripWidth + 32;
  const countX = ratioX + 86;
  const barX = countX + 152;
  const barWidth = 210;
  const maxProxy = Math.max(1, ...rows.map((row) => row.underobserved_buildings_3km_p85_proxy));

  return (
    <svg
      className="psdq-disagreement-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Bangladesh PSDQ registry-map source disagreement by upazila"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Source disagreement workbench
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Rows shown: 20+ DGHS clinical facilities and an Open Buildings denominator; sorted by {metric}
      </text>
      <text x={stripX} y={54} className="psdq-chart-head">
        OSM-visible registry share
      </text>
      <text x={ratioX} y={54} className="psdq-chart-head">
        OSM / reg
      </text>
      <text x={countX} y={54} className="psdq-chart-head">
        DGHS / OSM
      </text>
      <text x={barX} y={54} className="psdq-chart-head">
        Under-observed building proxy
      </text>

      {rows.map((row, rowIndex) => {
        const y = headerHeight + rowIndex * rowHeight;
        const visibleCells = Math.max(
          0,
          Math.min(cellCount, Math.floor(row.osm_to_active_clinical_ratio * cellCount)),
        );
        const selected = row.join_key === selectedJoinKey;
        const proxyWidth = (row.underobserved_buildings_3km_p85_proxy / maxProxy) * barWidth;
        return (
          <g
            key={row.join_key}
            className="psdq-chart-row"
            onMouseEnter={() => onSelect(row.join_key)}
            onClick={() => onSelect(row.join_key)}
          >
            <rect
              x={0}
              y={y - 6}
              width={width}
              height={rowHeight - 4}
              fill={selected ? "rgba(251, 176, 14, 0.13)" : "transparent"}
            />
            <text x={0} y={y + 10} className={selected ? "psdq-row-label psdq-row-selected" : "psdq-row-label"}>
              {row.upazila_name}
            </text>
            <text x={0} y={y + 26} className="psdq-row-sub">
              {row.district_name}, {row.division_name}
            </text>
            {Array.from({ length: cellCount }).map((_, cellIndex) => (
              <rect
                key={`${row.join_key}-${cellIndex}`}
                x={stripX + cellIndex * (cellSize + cellGap)}
                y={y}
                width={cellSize}
                height={18}
                rx={1.5}
                fill={cellIndex < visibleCells ? "#007DB8" : "#9b2226"}
                opacity={cellIndex < visibleCells ? 0.95 : 0.38}
              >
                <title>
                  {`${row.upazila_name}: ${pct(row.osm_to_active_clinical_ratio, 1)} OSM / registry`}
                </title>
              </rect>
            ))}
            <text x={ratioX} y={y + 13} className={selected ? "psdq-value psdq-row-selected" : "psdq-value"}>
              {pct(row.osm_to_active_clinical_ratio, 1)}
            </text>
            <text x={countX} y={y + 13} className="psdq-value">
              {formatNumber(row.active_clinical_facilities)} / {formatNumber(row.osm_health)}
            </text>
            <rect x={barX} y={y} width={barWidth} height={18} fill="#eef2f5" />
            <rect
              x={barX}
              y={y}
              width={Math.max(1, proxyWidth)}
              height={18}
              fill={selected ? "#FBB00E" : "#5A8227"}
            />
            <text x={barX + barWidth + 12} y={y + 13} className="psdq-value">
              {metricLabel(row, metric)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
