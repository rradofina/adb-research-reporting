import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ShowcaseQualityPanel } from "../components/ShowcaseQualityPanel";

interface ZeroMonitorRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_exposure_ugm3: number;
  share_of_zero_monitor_pop: number;
  cumulative_share: number;
}

interface ResidualRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_locations: number;
  people_per_monitor: number;
  pm25_exposure_ugm3: number;
  gap_score: number;
  gdp_pc_year: number | null;
  gdp_pc_current_usd: number | null;
  log10_people_per_monitor_residual: number;
}

interface AirPanelRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_locations: number;
  pm25_exposure_ugm3: number;
  pm25_above_who_guideline_5_ugm3: boolean;
  pm25_observability_gap_score: number;
  pm25_observability_status: string;
}

interface AirPanelData {
  program: string;
  claim_scope: string;
  sources: {
    openaq_v3: string;
    wdi_pm25: string;
    who_aaq: string;
    retrieved_at: string;
  };
  rows: AirPanelRow[];
}

interface DeepeningData {
  program: string;
  analysis: string;
  claim_scope: string;
  source: {
    name: string;
    file: string;
    inputs: string;
    snapshot: string;
    license: string;
    development_confound_source?: {
      name: string;
      url: string;
      cache: string;
      retrieved_at: string;
      license: string;
    };
  };
  part_a_concentration: {
    zero_monitor_economy_count: number;
    zero_monitor_population_total: number;
    png_share: number;
    timor_share: number;
    png_plus_timor_share: number;
    rows: ZeroMonitorRow[];
    composite_caution: string;
  };
  part_b_confound: {
    wdi_gdp_per_capita_fetched: boolean;
    confound_partial_runnable_from_public_wdi_gdp: boolean;
    rank_correlations_descriptive_only: {
      spearman_gap_vs_pm25: number;
      spearman_gap_vs_log10_population: number;
      spearman_gap_vs_log10_people_per_monitor_withmon: number;
      spearman_log_people_per_monitor_vs_pm25_withmon: number;
      spearman_log_people_per_monitor_vs_log10_gdp_pc_withmon: number;
      spearman_gap_score_vs_log10_gdp_pc_withmon: number;
      spearman_pm25_vs_log10_gdp_pc_withmon: number;
      n_full_exposed_frame: number;
      n_with_monitor_frame: number;
      n_with_monitor_and_gdp_pc: number;
    };
    gdp_partial: {
      method: string;
      intercept: number;
      slope: number;
      all_residuals?: ResidualRow[];
      top_positive_residuals_more_people_per_monitor_than_gdp_predicts: ResidualRow[];
      top_negative_residuals_fewer_people_per_monitor_than_gdp_predicts: ResidualRow[];
      zero_monitor_economies_excluded_from_partial: Array<{
        iso3: string;
        country: string;
        population: number;
        pm25_exposure_ugm3: number;
        gdp_pc_year: number | null;
        gdp_pc_current_usd: number | null;
        partial_status: string;
      }>;
      interpretation_limit: string;
    };
    data_wall: string | null;
  };
  attestation_chain: string;
  generated_at: string;
}

interface MetadataGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface MetadataQueueClassCount {
  name: string;
  rows: number;
}

interface MetadataUpgradeQueueRow {
  iso3: string;
  country: string;
  subregion: string;
  population: number;
  pm25_locations: number;
  pm25_exposure_ugm3: number;
  pm25_observability_gap_score: number;
  pm25_above_who_guideline_5_ugm3: boolean;
  baseline_gap_top5: boolean;
  zero_public_monitor_above_guideline: boolean;
  top_positive_gdp_residual: boolean;
  log10_people_per_monitor_residual: number | null;
  gdp_pc_year: number | null;
  gdp_pc_current_usd: number | null;
  station_coordinates_available_in_committed_artifacts: boolean;
  monitor_grade_available_in_committed_artifacts: boolean;
  monitor_first_seen_available_in_committed_artifacts: boolean;
  regulatory_inventory_available_in_committed_artifacts: boolean;
  station_radius_analysis_ready: boolean;
  upgrade_queue_class: string;
  next_evidence_needed: string;
  non_claim: string;
}

interface MetadataReadinessSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  readiness_scope: {
    panel_rows: number;
    countries_with_public_monitor_count: number;
    countries_with_pm25_exposure: number;
    zero_public_monitor_above_guideline_economies: number;
    monitored_economies_with_gdp_residuals: number;
    baseline_gap_top5_rows: number;
    positive_gdp_residual_queue_rows: number;
    unique_upgrade_queue_rows: number;
    station_level_cache_files: number;
    station_coordinate_rows_available: number;
    monitor_grade_rows_available: number;
    monitor_first_seen_rows_available: number;
    regulatory_inventory_rows_available: number;
    station_radius_analysis_ready: boolean;
  };
  evidence_gate_counts: MetadataGate[];
  upgrade_queue_class_counts: MetadataQueueClassCount[];
  top_upgrade_queue_rows: MetadataUpgradeQueueRow[];
  non_claim: string;
}

interface StationMetadataGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationMetadataCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  subregion: string;
  upgrade_queue_class: string;
  query_status: string;
  pm25_locations_in_committed_panel: number;
  openaq_pm25_locations_fetched: number;
  station_coordinate_rows: number;
  owner_or_provider_rows: number;
  monitor_grade_rows: number;
  first_seen_rows: number;
  last_seen_rows: number;
  pages_cached: number;
  query_variant: string | null;
  error: string | null;
}

interface StationMetadataStationRow {
  iso3: string;
  iso2: string;
  country: string;
  subregion: string;
  upgrade_queue_class: string;
  query_status: string;
  openaq_location_id: string | null;
  openaq_location_name: string | null;
  latitude: number | null;
  longitude: number | null;
  station_coordinate_available: boolean;
  owner_name: string | null;
  provider_name: string | null;
  owner_or_provider_available: boolean;
  monitor_grade_available: boolean;
  first_seen: string | null;
  first_seen_available: boolean;
  last_seen: string | null;
  last_seen_available: boolean;
  is_mobile: boolean | null;
  is_monitor: boolean | null;
  pm25_sensor_count: number;
  station_radius_analysis_ready: boolean;
}

interface StationMetadataSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  source_docs: string[];
  coverage_counts: {
    economies_targeted: number;
    economies_computed: number;
    economies_with_api_error: number;
    economies_blocked_by_api_key: number;
    economies_with_openaq_pm25_locations: number;
    economies_with_zero_openaq_pm25_locations: number;
    openaq_pm25_location_rows: number;
    station_coordinate_rows: number;
    owner_or_provider_rows: number;
    monitor_grade_rows: number;
    first_seen_rows: number;
    last_seen_rows: number;
    excluded_coordinate_qc_rows: number;
    pages_cached: number;
    station_radius_coordinate_input_available: boolean;
    station_radius_analysis_ready: boolean;
  };
  evidence_gate_counts: StationMetadataGate[];
  country_rows: StationMetadataCountryRow[];
  station_rows: StationMetadataStationRow[];
  non_claim: string;
}

interface StationRadiusReadinessGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusReadinessLane {
  lane: string;
  economies: number;
}

interface StationRadiusReadinessCountryRow {
  iso3: string;
  country: string;
  subregion: string;
  upgrade_queue_class: string;
  openaq_coordinate_rows: number;
  official_coordinate_rows: number;
  official_pm25_coordinate_rows: number;
  near_plus_name_candidate_rows: number;
  near_only_candidate_rows: number;
  name_overlap_not_near_candidate_rows: number;
  validated_same_station_join_rows: number;
  complete_monitor_grade_rows: number;
  gridded_population_denominator_files: number;
  gridded_pm25_denominator_files: number;
  station_radius_analysis_ready: boolean;
  readiness_lane: string;
  reader_use: string;
}

interface StationRadiusReadinessSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  coverage_counts: {
    upgrade_queue_economies: number;
    economies_with_any_coordinate_input: number;
    economies_with_openaq_coordinate_rows: number;
    economies_with_official_coordinate_rows: number;
    openaq_coordinate_rows: number;
    official_coordinate_rows: number;
    official_pm25_coordinate_rows: number;
    near_plus_name_candidate_rows: number;
    near_only_candidate_rows: number;
    name_overlap_not_near_candidate_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    boundary_reference_files_available: number;
    gridded_population_denominator_files: number;
    gridded_pm25_denominator_files: number;
    station_radius_ready_economies: number;
  };
  readiness_lane_counts: StationRadiusReadinessLane[];
  evidence_gate_counts: StationRadiusReadinessGate[];
  country_rows: StationRadiusReadinessCountryRow[];
  top_coordinate_ready_rows: StationRadiusReadinessCountryRow[];
  non_claim: string;
}

interface StationRadiusSourcePlanGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusSourcePlanDecision {
  decision: string;
  sources: number;
}

interface StationRadiusSourcePlanRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  source_family: string;
  source_decision: string;
  source_level_candidate_ready: boolean;
  raster_or_grid_file_committed: boolean;
  matched_gridded_terms: string;
  matched_license_terms: string;
  matched_vintage_terms: string;
  reader_use: string;
}

interface StationRadiusSourcePlanSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    seeded_source_urls: number;
    source_urls_retrieved: number;
    source_level_candidate_denominator_sources: number;
    population_candidate_sources: number;
    pm25_candidate_sources: number;
    context_only_sources: number;
    boundary_reference_sources: number;
    committed_population_raster_files: number;
    committed_pm25_grid_files: number;
    committed_boundary_reference_files: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  source_decision_counts: StationRadiusSourcePlanDecision[];
  evidence_gate_counts: StationRadiusSourcePlanGate[];
  proposed_method: {
    population_primary: string;
    population_sensitivity: string;
    pm25_primary: string;
    pm25_sensitivity: string;
    radius_sweep_km: number[];
    deduplication_rule_draft: string;
    grade_rule_draft: string;
  };
  source_records: StationRadiusSourcePlanRecord[];
  non_claim: string;
}

interface StationRadiusAcquisitionGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusAcquisitionDecision {
  decision: string;
  sources: number;
}

interface StationRadiusAcquisitionRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  source_family: string;
  source_level_candidate_ready: boolean;
  route_links_total: number;
  direct_file_route_links: number;
  cloud_or_listing_route_links: number;
  context_route_links: number;
  route_probe_attempts: number;
  route_probe_ok: number;
  route_probe_statuses: string;
  route_examples: string;
  route_decision: string;
  reader_use: string;
  blocking_gap: string;
}

interface StationRadiusAcquisitionSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    source_records: number;
    source_pages_retrieved: number;
    candidate_denominator_sources: number;
    candidate_sources_with_visible_routes: number;
    visible_route_links: number;
    direct_file_route_links: number;
    cloud_or_listing_route_links: number;
    context_route_links: number;
    route_probe_attempts: number;
    route_probe_ok: number;
    committed_population_raster_files: number;
    committed_pm25_grid_files: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  route_decision_counts: StationRadiusAcquisitionDecision[];
  evidence_gate_counts: StationRadiusAcquisitionGate[];
  route_records: StationRadiusAcquisitionRecord[];
  non_claim: string;
}

interface StationRadiusFileManifestGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusFileManifestStatus {
  status: string;
  records: number;
}

interface StationRadiusFileManifestRecord {
  manifest_key: string;
  source_key: string;
  source_name: string;
  source_family: string;
  source_role: string;
  denominator_type: string;
  candidate_role: string;
  source_plan_version: string;
  resolved_version: string;
  vintage: string;
  resolution: string;
  geography_scope: string;
  file_format: string;
  listing_url: string;
  file_name: string;
  exact_file_url: string;
  s3_bucket: string;
  s3_key: string;
  route_type: string;
  manifest_status: string;
  head_status: number | string;
  content_type: string;
  content_length_bytes: string;
  listing_size_hint: string;
  last_modified: string;
  etag: string;
  checksum_algorithm: string;
  reader_use: string;
  blocking_gap: string;
}

interface StationRadiusFileManifestSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    manifest_records: number;
    exact_file_or_object_records_visible: number;
    exact_population_file_records_visible: number;
    exact_pm25_file_records_visible: number;
    context_metadata_file_records_visible: number;
    shared_folder_routes_not_exact_file_manifest: number;
    records_with_server_size_bytes: number;
    records_with_s3_etag: number;
    current_acag_aws_records_with_source_plan_version_drift: number;
    source_plan_v6gl0204_or_v5_exact_file_records: number;
    denominator_files_downloaded: number;
    denominator_files_sha256_checksummed: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  manifest_status_counts: StationRadiusFileManifestStatus[];
  evidence_gate_counts: StationRadiusFileManifestGate[];
  manifest_records: StationRadiusFileManifestRecord[];
  non_claim: string;
}

interface StationRadiusDownloadFeasibilityGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusDownloadFeasibilityDecision {
  decision: string;
  records: number;
}

interface StationRadiusDownloadFeasibilityRole {
  role: string;
  records: number;
}

interface StationRadiusDownloadFeasibilitySize {
  size_class: string;
  records: number;
}

interface StationRadiusDownloadFeasibilityRecord {
  manifest_key: string;
  source_key: string;
  source_name: string;
  source_family: string;
  source_role: string;
  denominator_type: string;
  candidate_role: string;
  source_plan_version: string;
  resolved_version: string;
  vintage: string;
  resolution: string;
  geography_scope: string;
  file_format: string;
  route_type: string;
  manifest_status: string;
  exact_file_url: string;
  s3_key: string;
  content_length_bytes: number;
  size_mb: number;
  size_class: string;
  exact_route_visible: boolean;
  source_plan_version_drift: boolean;
  unresolved_shared_folder: boolean;
  download_feasibility: string;
  selection_role: string;
  first_wave_candidate: boolean;
  denominator_gate_closer: boolean;
  reader_use: string;
  proposed_action: string;
  blocking_gap: string;
}

interface StationRadiusDownloadFeasibilitySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    manifest_records_reviewed: number;
    exact_file_or_object_records_visible: number;
    safe_under_10mb_records: number;
    first_wave_download_candidates: number;
    conditional_pm25_checksum_candidates: number;
    metadata_or_route_test_candidates: number;
    population_denominator_selected_for_download: number;
    large_population_archives_deferred: number;
    moderate_or_large_pm25_objects_deferred: number;
    acag_version_decision_required_records: number;
    unresolved_shared_folder_routes: number;
    denominator_files_downloaded: number;
    denominator_files_sha256_checksummed: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  download_feasibility_counts: StationRadiusDownloadFeasibilityDecision[];
  selection_role_counts: StationRadiusDownloadFeasibilityRole[];
  size_class_counts: StationRadiusDownloadFeasibilitySize[];
  evidence_gate_counts: StationRadiusDownloadFeasibilityGate[];
  feasibility_records: StationRadiusDownloadFeasibilityRecord[];
  non_claim: string;
}

interface StationRadiusAcagVersionGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusAcagVersionDecision {
  decision: string;
  records: number;
}

interface StationRadiusAcagEvidenceType {
  evidence_type: string;
  records: number;
}

interface StationRadiusAcagVersionRow {
  record_key: string;
  evidence_type: string;
  source_name: string;
  source_role: string;
  planned_version: string;
  observed_version: string;
  selected_vintage: string;
  route_url: string;
  retrieved: boolean;
  http_status: number | string;
  matched_terms: string;
  s3_prefix: string;
  s3_key_count: number | string;
  first_year: string;
  latest_year: string;
  target_2023_object: string;
  target_2023_size_bytes: number;
  latest_2024_object: string;
  latest_2024_size_bytes: number;
  decision: string;
  allowed_use: string;
  not_allowed_use: string;
  next_action: string;
  blocking_gap: string;
}

interface StationRadiusAcagVersionSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  version_decision: string;
  coverage_counts: {
    evidence_rows: number;
    routes_retrieved: number;
    source_pages_retrieved: number;
    s3_prefixes_retrieved: number;
    v6gl03_s3_prefixes_with_2023_target: number;
    v6gl03_s3_prefixes_with_2024_visible: number;
    approved_2023_coarse_first_wave_objects: number;
    fine_resolution_second_wave_or_deferred_objects: number;
    legacy_v6gl0204_v5_box_routes_unresolved: number;
    legacy_v6gl0204_v5_exact_file_manifests: number;
    v6gl03_allowed_as_silent_replacement: number;
    selected_vintage: number;
    visible_latest_v6gl03_year: number;
    denominator_files_downloaded: number;
    denominator_files_sha256_checksummed: number;
    netcdf_variables_inspected: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  decision_counts: StationRadiusAcagVersionDecision[];
  evidence_type_counts: StationRadiusAcagEvidenceType[];
  evidence_gate_counts: StationRadiusAcagVersionGate[];
  acag_rows: StationRadiusAcagVersionRow[];
  non_claim: string;
}

interface StationRadiusAcagChecksumGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusAcagChecksumRow {
  record_key: string;
  source_role: string;
  observed_version: string;
  selected_vintage: string;
  s3_key: string;
  object_url: string;
  expected_size_bytes: number;
  expected_etag: string;
  downloaded: boolean;
  downloaded_this_run: boolean;
  cache_path: string;
  file_size_bytes: number;
  size_matches_expected: boolean;
  sha256: string;
  http_status: number | string;
  content_type: string;
  last_modified: string;
  netcdf_opened: boolean;
  netcdf_format: string;
  dimension_count: number;
  dimensions: string;
  variable_count: number;
  variables: string;
  coordinate_variables: string;
  pm25_variable_candidates: string;
  global_attributes: string;
  metadata_decision: string;
  reader_use: string;
  blocking_gap: string;
  retrieval_error: string;
  non_claim: string;
}

interface StationRadiusAcagChecksumSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  cache_policy: string;
  coverage_counts: {
    approved_coarse_candidate_files: number;
    downloaded_files: number;
    downloaded_this_run: number;
    sha256_checksummed_files: number;
    size_matches_expected_files: number;
    netcdf_files_opened: number;
    files_with_pm25_variable_candidates: number;
    files_with_lat_lon_coordinate_variables: number;
    population_denominator_files_selected: number;
    population_denominator_files_downloaded: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusAcagChecksumGate[];
  checksum_rows: StationRadiusAcagChecksumRow[];
  non_claim: string;
}

interface StationRadiusGhslTileGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusGhslCountryRow {
  iso3: string;
  country: string;
  readiness_lane: string;
  openaq_coordinate_rows_used: number;
  official_pm25_coordinate_rows_used: number;
  coordinate_rows_used: number;
  unique_coordinate_points: number;
  ghsl_population_tiles_selected: number;
  tile_ids: string;
  reader_use: string;
}

interface StationRadiusGhslTileRow {
  tile_id: string;
  tile_row: number;
  tile_col: number;
  south: number;
  west: number;
  north: number;
  east: number;
  selected_economies: string;
  selected_economy_count: number;
  coordinate_rows_touching_tile: number;
  openaq_coordinate_rows_touching_tile: number;
  official_pm25_coordinate_rows_touching_tile: number;
  ghsl_vintage: string;
  ghsl_resolution: string;
  exact_file_url: string;
  head_status: number | string;
  head_ok: boolean;
  content_type: string;
  content_length_bytes: number | string;
  size_mb: string;
  last_modified: string;
  selection_status: string;
  download_decision: string;
  blocking_gap: string;
  retrieval_error: string;
}

interface StationRadiusGhslTileSelectionSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  tile_grid_assumption: string;
  coverage_counts: {
    coordinate_ready_economies: number;
    coordinate_rows_used: number;
    openaq_coordinate_rows_used: number;
    official_pm25_coordinate_rows_used: number;
    unique_coordinate_points: number;
    draft_radius_buffer_km: number;
    ghsl_population_tile_urls_selected: number;
    ghsl_tile_head_probes: number;
    ghsl_tile_head_ok: number;
    ghsl_tile_head_failed: number;
    selected_tile_content_length_bytes_total: number;
    selected_tile_content_length_mb_total: number;
    population_denominator_files_downloaded: number;
    population_denominator_files_sha256_checksummed: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusGhslTileGate[];
  country_rows: StationRadiusGhslCountryRow[];
  tile_rows: StationRadiusGhslTileRow[];
  non_claim: string;
}

interface StationRadiusGhslTileChecksumGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusGhslTileChecksumRow {
  tile_id: string;
  selected_economies: string;
  coordinate_rows_touching_tile: number;
  head_ok: boolean;
  expected_size_bytes: number | string;
  expected_size_mb: number | string;
  exact_file_url: string;
  download_decision: string;
  downloaded: boolean;
  downloaded_this_run: boolean;
  cache_path: string;
  file_size_bytes: number | string;
  size_matches_expected: boolean;
  sha256: string;
  http_status: number | string;
  content_type: string;
  last_modified: string;
  zip_opened: boolean | string;
  geotiff_member_count: number | string;
  geotiff_members: string;
  geotiff_opened: boolean | string;
  raster_width: number | string;
  raster_height: number | string;
  raster_crs: string;
  raster_transform: string;
  raster_bounds: string;
  raster_dtype: string;
  transform_matches_10_degree_tile_bounds: boolean | string;
  blocking_gap: string;
  retrieval_error: string;
}

interface StationRadiusGhslTileChecksumSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  first_wave_rule: string;
  cache_policy: string;
  coverage_counts: {
    selected_tile_rows: number;
    first_wave_download_candidate_rows: number;
    downloaded_population_tile_files: number;
    downloaded_population_tile_files_this_run: number;
    sha256_checksummed_population_tile_files: number;
    downloaded_size_bytes_total: number;
    downloaded_size_mb_total: number;
    zip_files_opened: number;
    geotiff_members_found: number;
    geotiff_transform_inspected_files: number;
    geotiff_transform_matches_10_degree_tile_bounds: number;
    geotiff_transform_mismatch_files: number;
    selected_head_not_ok_blocked_tiles: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusGhslTileChecksumGate[];
  tile_checksum_rows: StationRadiusGhslTileChecksumRow[];
  non_claim: string;
}

interface StationRadiusGhslTileRoutingGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusGhslTileRoutingOriginRow {
  tile_id: string;
  raster_west: number;
  raster_south: number;
  raster_east: number;
  raster_north: number;
  derived_north_origin: number;
  derived_west_origin: number;
  mean_north_origin: number;
  mean_west_origin: number;
  sha256: string;
}

interface StationRadiusGhslTileRoutingRow {
  tile_id: string;
  previous_selected: boolean | string;
  corrected_selected: boolean | string;
  correction_status: string;
  previous_selected_economies: string;
  corrected_selected_economies: string;
  previous_coordinate_rows_touching_tile: number | string;
  corrected_coordinate_rows_touching_tile: number | string;
  prior_head_ok: boolean | string;
  prior_downloaded: boolean | string;
  prior_sha256: string;
  prior_raster_bounds: string;
}

interface StationRadiusGhslTileRoutingCountryRow {
  iso3: string;
  country: string;
  coordinate_rows_used: number;
  previous_tile_count: number;
  corrected_tile_count: number;
  retained_tile_count: number;
  added_tile_count: number;
  removed_tile_count: number;
  added_tile_ids: string;
  removed_tile_ids: string;
}

interface StationRadiusGhslTileRoutingSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  routing_rule: string;
  coverage_counts: {
    coordinate_ready_economies: number;
    coordinate_rows_used: number;
    openaq_coordinate_rows_used: number;
    official_pm25_coordinate_rows_used: number;
    origin_observation_rows: number;
    observed_north_origin: number;
    observed_west_origin: number;
    north_origin_range_degrees: number;
    west_origin_range_degrees: number;
    previous_tile_urls_selected: number;
    corrected_tile_urls_selected: number;
    retained_previous_tile_urls: number;
    added_corrected_tile_urls: number;
    removed_previous_tile_urls: number;
    corrected_tile_prior_head_ok: number;
    corrected_tile_prior_head_not_ok: number;
    corrected_tile_prior_head_unknown: number;
    downloaded_population_tiles_retained_by_corrected_routing: number;
    downloaded_population_tiles_removed_by_corrected_routing: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusGhslTileRoutingGate[];
  added_corrected_tile_ids: string[];
  removed_previous_tile_ids: string[];
  retained_previous_tile_ids: string[];
  origin_rows: StationRadiusGhslTileRoutingOriginRow[];
  country_rows: StationRadiusGhslTileRoutingCountryRow[];
  tile_rows: StationRadiusGhslTileRoutingRow[];
  non_claim: string;
}

interface StationRadiusGhslCorrectedCustodyGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusGhslCorrectedCustodyRow {
  tile_id: string;
  correction_status: string;
  corrected_selected_economies: string;
  corrected_coordinate_rows_touching_tile: number | string;
  custody_probe_source: string;
  custody_size_mb: number | string;
  download_decision: string;
  downloaded: boolean | string;
  downloaded_this_run: boolean | string;
  downloaded_from_prior_cache: boolean | string;
  file_size_bytes: number | string;
  sha256: string;
  sha256_matches_prior: boolean | string;
  geotiff_opened: boolean | string;
  raster_bounds: string;
  transform_matches_corrected_tile_bounds: boolean | string;
  blocking_gap: string;
  retrieval_error: string;
}

interface StationRadiusGhslCorrectedCustodySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  first_wave_rule: string;
  cache_policy: string;
  coverage_counts: {
    corrected_tile_rows: number;
    retained_corrected_tile_rows: number;
    added_corrected_tile_rows: number;
    current_head_ok_tiles: number;
    current_range_ok_tiles: number;
    current_probe_size_available_tiles: number;
    corrected_first_wave_eligible_rows: number;
    corrected_first_wave_download_candidate_rows: number;
    downloaded_population_tile_files: number;
    downloaded_population_tile_files_this_run: number;
    downloaded_population_tile_files_from_prior_cache: number;
    sha256_checksummed_population_tile_files: number;
    sha256_matches_prior_rows: number;
    downloaded_size_bytes_total: number;
    downloaded_size_mb_total: number;
    zip_files_opened: number;
    geotiff_opened_files: number;
    geotiff_transform_matches_corrected_bounds: number;
    geotiff_transform_mismatch_corrected_bounds: number;
    blocked_corrected_selected_tiles: number;
    deferred_corrected_selected_tiles: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusGhslCorrectedCustodyGate[];
  tile_custody_rows: StationRadiusGhslCorrectedCustodyRow[];
  non_claim: string;
}

interface StationRadiusGhslLargeCustodyGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusGhslLargeCustodyRow {
  tile_id: string;
  corrected_selected_economies: string;
  corrected_coordinate_rows_touching_tile: number | string;
  custody_probe_source: string;
  custody_size_mb: number | string;
  downloaded: boolean | string;
  downloaded_this_run: boolean | string;
  downloaded_from_prior_cache: boolean | string;
  file_size_bytes: number | string;
  sha256: string;
  geotiff_opened: boolean | string;
  raster_bounds: string;
  transform_matches_corrected_tile_bounds: boolean | string;
  blocking_gap: string;
  retrieval_error: string;
}

interface StationRadiusGhslLargeCustodySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_gate: string;
  target_rule: string;
  cache_policy: string;
  coverage_counts: {
    large_corrected_tile_rows: number;
    current_head_ok_large_tiles: number;
    downloaded_large_population_tile_files: number;
    downloaded_large_population_tile_files_this_run: number;
    downloaded_large_population_tile_files_from_prior_cache: number;
    sha256_checksummed_large_population_tile_files: number;
    downloaded_large_size_bytes_total: number;
    downloaded_large_size_mb_total: number;
    large_zip_files_opened: number;
    large_geotiff_opened_files: number;
    large_geotiff_transform_matches_corrected_bounds: number;
    large_geotiff_transform_mismatch_corrected_bounds: number;
    remaining_large_tile_blockers: number;
    first_wave_corrected_tile_files_in_custody: number;
    corrected_tile_files_in_custody_after_large_pass: number;
    corrected_tile_files_required: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusGhslLargeCustodyGate[];
  large_tile_custody_rows: StationRadiusGhslLargeCustodyRow[];
  non_claim: string;
}

interface StationRadiusMethodPrefreezeGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusMethodRuleRow {
  rule_id: string;
  gate: string;
  gate_status: string;
  evidence_rows: number | string;
  frozen_for_next_compute: boolean | string;
  claim_allowed: boolean | string;
  next_blocker: string;
  decision: string;
  blocking_gap: string;
}

interface StationRadiusMethodCountryRow {
  iso3: string;
  country: string;
  coordinate_rows_used: number | string;
  unique_coordinate_points: number | string;
  openaq_coordinate_rows_used: number | string;
  official_pm25_coordinate_rows_used: number | string;
  corrected_tile_count: number | string;
  population_tile_files_in_custody: number | string;
  population_tile_custody_complete: boolean | string;
  next_blocker: string;
}

interface StationRadiusMethodPrefreezeSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  method_stage: string;
  coverage_counts: {
    coordinate_economies: number;
    coordinate_rows_used: number;
    unique_coordinate_points: number;
    openaq_coordinate_rows_used: number;
    official_pm25_coordinate_rows_used: number;
    population_tile_files_required: number;
    population_tile_files_in_custody: number;
    coordinate_economies_with_full_population_tile_custody: number;
    pm25_coarse_files_in_custody: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    station_radius_ready_economies: number;
  };
  evidence_gate_counts: StationRadiusMethodPrefreezeGate[];
  method_rule_rows: StationRadiusMethodRuleRow[];
  country_rows: StationRadiusMethodCountryRow[];
  non_claim: string;
}

interface StationRadiusRuleGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusRuleSourceRow {
  source_key: string;
  source_family: string;
  title: string;
  url: string;
  retrieval_status: string;
  http_status: number | string;
  content_type: string;
  content_length_bytes: number | string;
  cache_path: string;
  sha256: string;
  retrieval_error: string;
}

interface StationRadiusRuleEvidenceRow {
  evidence_id: string;
  evidence_role: string;
  evidence_status: string;
  extracted_scale: string;
  extracted_value: string;
  radius_km: number | string;
  selected_for_rule?: boolean | string;
  source_snippet: string;
  reader_use: string;
  title: string;
  url: string;
  source_family: string;
  retrieval_status: string;
}

interface StationRadiusRuleSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_seed: string;
  coverage_counts: {
    seed_sources: number;
    retrieved_sources: number;
    retrieval_error_sources: number;
    evidence_rows: number;
    spatial_scale_evidence_rows: number;
    rule_selected_evidence_rows: number;
    primary_radius_km: number;
    lower_sensitivity_radius_km: number;
    upper_sensitivity_radius_km: number;
    radius_rule_frozen: boolean;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  radius_rule: {
    status: string;
    primary_radius_km: number;
    primary_label: string;
    sensitivity_radii_km: number[];
    tile_envelope_radius_km: number;
    tile_envelope_source: string;
    claim_guardrail: string;
  };
  evidence_gate_counts: StationRadiusRuleGate[];
  source_rows: StationRadiusRuleSourceRow[];
  evidence_rows: StationRadiusRuleEvidenceRow[];
  non_claim: string;
}

interface StationRadiusPm25ResolutionGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusPm25ResolutionRow {
  decision_id: string;
  decision_role: string;
  decision_status: string;
  selected: boolean | string;
  acag_record_key: string;
  source_role: string;
  observed_version: string;
  selected_vintage: number | string;
  selected_resolution: string;
  grid_family: string;
  object_url: string;
  cache_path: string;
  sha256: string;
  file_size_bytes: number | string;
  dimensions: string;
  variables: string;
  pm25_variable: string;
  radius_rule_context: string;
  reader_use: string;
  blocking_gap: string;
  claim_guardrail: string;
}

interface StationRadiusPm25ResolutionSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    checksummed_coarse_pm25_files: number;
    files_with_pm25_lat_lon: number;
    selected_primary_pm25_surfaces: number;
    consistency_lane_pm25_surfaces: number;
    selected_vintage: number;
    visible_latest_v6gl03_year: number;
    fine_resolution_second_wave_or_deferred_objects: number;
    radius_rule_frozen: boolean;
    primary_radius_km: number;
    lower_sensitivity_radius_km: number;
    upper_sensitivity_radius_km: number;
    coordinate_rows_used: number;
    population_tile_files_in_custody: number;
    station_radius_population_rows: number;
    station_radius_pm25_exposure_rows: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
  };
  pm25_resolution_decision: {
    status: string;
    selected_version: string;
    selected_vintage: number;
    selected_resolution: string;
    primary_dry_run_record_key: string;
    consistency_lane_record_key: string;
    deferred_lanes: string;
    claim_guardrail: string;
  };
  evidence_gate_counts: StationRadiusPm25ResolutionGate[];
  decision_rows: StationRadiusPm25ResolutionRow[];
  non_claim: string;
}

interface StationRadiusDenominatorJoinGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationRadiusDenominatorJoinCountryRow {
  iso3: string;
  country: string;
  radius_km: number | string;
  radius_role: string;
  coordinate_rows: number;
  unique_coordinate_points: number;
  openaq_coordinate_rows: number;
  official_pm25_coordinate_rows: number;
  population_rows_computed: number;
  pm25_rows_computed: number;
  candidate_population_buffer_sum: number;
  candidate_population_exact_coordinate_dedup_sum: number;
  mean_pm25_nearest_ugm3: number | string;
  mean_pm25_radius_ugm3: number | string;
  ghsl_tile_count: number;
  ghsl_tile_ids: string;
  country_union_population_computed: boolean | string;
  coverage_claim_allowed: boolean | string;
  validated_same_station_join_rows: number;
  complete_monitor_grade_rows: number;
  station_radius_ready: boolean | string;
  reader_use: string;
  blocking_gap: string;
}

interface StationRadiusDenominatorJoinSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    coordinate_economies: number;
    coordinate_rows_used: number;
    unique_coordinate_points: number;
    openaq_coordinate_rows_used: number;
    official_pm25_coordinate_rows_used: number;
    radius_bands_computed: number;
    candidate_coordinate_radius_rows: number;
    population_rows_computed: number;
    pm25_rows_computed: number;
    country_radius_summary_rows: number;
    population_raster_tiles_opened: number;
    acag_pm25_surface_opened: number;
    primary_radius_km: number;
    lower_sensitivity_radius_km: number;
    upper_sensitivity_radius_km: number;
    country_union_population_rows: number;
    country_union_population_computed: boolean;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
    coverage_claim_allowed: boolean;
  };
  evidence_gate_counts: StationRadiusDenominatorJoinGate[];
  radius_bands: Array<{ radius_role: string; radius_km: number }>;
  pm25_surface: {
    record_key: string;
    selected_vintage: string;
    cache_path: string;
    resolution_decision_status: string;
  };
  top_primary_radius_country_rows: StationRadiusDenominatorJoinCountryRow[];
  country_rows: StationRadiusDenominatorJoinCountryRow[];
  non_claim: string;
}

interface StationRadiusCountryUnionRow {
  iso3: string;
  country: string;
  radius_km: number | string;
  radius_role: string;
  coordinate_rows: number;
  unique_coordinate_points: number;
  openaq_coordinate_rows: number;
  official_pm25_coordinate_rows: number;
  unioned_population_sum: number | string;
  unioned_positive_cells: number;
  unioned_population_tile_count: number;
  unioned_population_windows_scanned: number;
  row_level_candidate_population_buffer_sum: number | string;
  row_level_exact_coordinate_dedup_sum: number | string;
  row_to_union_population_multiplier: number | string;
  exact_dedup_to_union_population_multiplier: number | string;
  population_overlap_removed_from_row_sum: number | string;
  unioned_pm25_cell_mean_ugm3: number | string;
  unioned_pm25_cell_count: number;
  unioned_pm25_computed: boolean | string;
  country_union_population_computed: boolean | string;
  coverage_claim_allowed: boolean | string;
  validated_same_station_join_rows: number;
  complete_monitor_grade_rows: number;
  station_radius_ready: boolean | string;
  reader_use: string;
  blocking_gap: string;
}

interface StationRadiusCountryUnionSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    coordinate_economies: number;
    coordinate_rows_used: number;
    unique_coordinate_points: number;
    openaq_coordinate_rows_used: number;
    official_pm25_coordinate_rows_used: number;
    radius_bands_computed: number;
    row_level_country_radius_rows_read: number;
    country_union_rows_computed: number;
    country_union_population_rows_computed: number;
    country_union_pm25_rows_computed: number;
    population_raster_tiles_opened: number;
    acag_pm25_surface_opened: number;
    primary_radius_km: number;
    lower_sensitivity_radius_km: number;
    upper_sensitivity_radius_km: number;
    validated_same_station_join_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_economies: number;
    coverage_claim_allowed: boolean;
  };
  evidence_gate_counts: StationRadiusDenominatorJoinGate[];
  radius_bands: Array<{ radius_role: string; radius_km: number }>;
  top_primary_radius_country_rows: StationRadiusCountryUnionRow[];
  country_rows: StationRadiusCountryUnionRow[];
  non_claim: string;
}

interface StationRadiusClaimGateRow {
  claim_gate_id: string;
  iso3: string;
  country: string;
  radius_km: number | string;
  coordinate_rows: number;
  openaq_coordinate_rows: number;
  official_pm25_coordinate_rows: number;
  unioned_population_sum: number | string;
  row_level_candidate_population_buffer_sum: number | string;
  row_to_union_population_multiplier: number | string;
  denominator_geometry_gate: string;
  station_identity_gate: string;
  monitor_grade_gate: string;
  station_radius_readiness_gate: string;
  coverage_claim_gate: string;
  coverage_claim_allowed: boolean | string;
  release_decision: string;
  reader_use: string;
  blocking_gaps: string;
  non_claim: string;
}

interface StationRadiusClaimGateSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  claim_rule: {
    rule: string;
    allowed: boolean;
    current_decision: string;
  };
  coverage_counts: {
    primary_radius_country_rows_checked: number;
    coordinate_economies: number;
    country_union_rows_computed: number;
    country_union_population_rows_computed: number;
    country_union_pm25_rows_computed: number;
    denominator_join_rows: number;
    ghsl_population_rows_computed: number;
    acag_pm25_rows_computed: number;
    validated_same_station_join_rows: number;
    candidate_review_rows: number;
    candidate_crosswalk_source_scan_rows: number;
    complete_monitor_grade_rows: number;
    station_method_classified_rows: number;
    current_status_confirmed_rows: number;
    calibration_status_available_rows: number;
    station_radius_ready_economies: number;
    station_radius_ready_rows: number;
    claim_allowed_country_rows: number;
    coverage_claim_allowed: boolean;
  };
  blocker_context_counts: {
    bmkg_target_rows: number;
    bmkg_method_classified_rows: number;
    bmkg_dashboard_current_online_rows: number;
    bmkg_station_specific_inspection_log_rows: number;
    bmkg_station_specific_calibration_certificate_rows: number;
    bmkg_calibration_status_rows: number;
    uzbekistan_unresolved_blocker_rows: number;
    uzbekistan_endpoint_mismatch_rows: number;
    uzbekistan_air_portal_resolution_rows: number;
    georgia_verified_report_closure_rows: number;
    georgia_indicator_exact_station_code_rows: number;
  };
  release_decision_counts: Array<{ release_decision: string; rows: number }>;
  evidence_gate_counts: StationRadiusDenominatorJoinGate[];
  display_rows: StationRadiusClaimGateRow[];
  non_claim: string;
}

interface RegulatorSourceGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface RegulatorSourceCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  subregion: string;
  upgrade_queue_class: string;
  openaq_pm25_rows: number;
  openaq_zero_pm25_rows: boolean;
  source_name: string;
  agency: string;
  url: string;
  source_tier: string;
  source_class: string;
  official_source_candidate: boolean;
  official_station_inventory_or_portal: boolean;
  station_inventory_signal: string;
  monitor_grade_signal_present: boolean;
  pm25_signal_present: boolean;
  official_station_count_claim: string;
  official_station_count_claim_present: boolean;
  source_note: string;
  next_validation_step: string;
  retrieval_status: string;
  http_status: number | null;
}

interface RegulatorSourceSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    economies_targeted: number;
    economies_with_official_source_candidate: number;
    economies_with_official_station_inventory_or_portal: number;
    economies_with_official_station_count_claim: number;
    economies_with_monitor_grade_signal: number;
    economies_with_pm25_signal: number;
    zero_openaq_economies_targeted: number;
    zero_openaq_economies_with_official_station_inventory_or_portal: number;
    zero_openaq_economies_with_official_regulator_page_no_station_inventory: number;
    zero_openaq_economies_with_development_partner_monitoring_reference: number;
    zero_openaq_economies_not_found_in_targeted_search: number;
    economies_not_found_in_targeted_search: number;
    development_partner_or_secondary_reference_rows: number;
    url_rows: number;
    url_rows_retrieved: number;
    url_rows_with_retrieval_error: number;
  };
  evidence_gate_counts: RegulatorSourceGate[];
  country_rows: RegulatorSourceCountryRow[];
  non_claim: string;
}

interface RegulatorStationGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface RegulatorStationCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  subregion: string;
  source_name: string;
  source_class: string;
  source_extraction_level: string;
  retrieval_status: string;
  official_rows_extracted: number;
  coordinate_rows: number;
  station_name_only_rows: number;
  count_only_rows: number;
  plan_count_only_rows: number;
  pm25_signal_rows: number;
  openaq_country_rows: number;
  nearest_openaq_within_5km_rows: number;
  name_overlap_rows: number;
  source_station_count_claim: string;
  retrieval_note: string;
}

interface RegulatorStationCoordinateRow {
  iso3: string;
  country: string;
  source_station_id: string;
  source_station_name: string;
  latitude: number | null;
  longitude: number | null;
  pm25_signal: boolean;
  nearest_openaq_location_name: string;
  nearest_openaq_distance_km: number | null;
  nearest_openaq_within_5km: boolean;
}

interface RegulatorStationSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    official_sources_targeted: number;
    official_sources_retrieved_or_extracted: number;
    countries_with_station_coordinates: number;
    official_station_coordinate_rows: number;
    official_station_name_only_rows: number;
    official_count_only_rows: number;
    official_plan_count_only_rows: number;
    countries_with_unresolved_extraction: number;
    official_rows_with_pm25_signal: number;
    official_coordinate_rows_near_openaq_within_5km: number;
    official_coordinate_rows_not_near_openaq_within_5km: number;
    official_rows_with_name_overlap_to_openaq: number;
    monitor_grade_rows: number;
    station_radius_analysis_ready: boolean;
  };
  evidence_gate_counts: RegulatorStationGate[];
  country_rows: RegulatorStationCountryRow[];
  top_coordinate_rows: RegulatorStationCoordinateRow[];
  non_claim: string;
}

interface MonitorGradeGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface OfficialOpenAQGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface OfficialOpenAQCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  official_coordinate_rows: number;
  openaq_coordinate_rows: number;
  near_and_name_overlap_candidate_rows: number;
  near_only_candidate_rows: number;
  name_overlap_not_near_candidate_rows: number;
  official_coordinate_without_openaq_candidate_rows: number;
  unique_near_openaq_candidate_ids: number;
  openaq_rows_not_used_as_near_candidate: number;
  validated_same_station_rows: number;
}

interface OfficialOpenAQSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    official_coordinate_rows_audited: number;
    countries_with_official_coordinate_rows: number;
    openaq_coordinate_rows_in_official_coordinate_countries: number;
    near_and_name_overlap_candidate_rows: number;
    near_only_candidate_rows: number;
    name_overlap_not_near_candidate_rows: number;
    official_coordinate_without_openaq_candidate_rows: number;
    unique_near_openaq_candidate_rows: number;
    openaq_rows_not_used_as_near_candidate: number;
    validated_same_station_rows: number;
    station_radius_reconciliation_ready: boolean;
  };
  evidence_gate_counts: OfficialOpenAQGate[];
  country_rows: OfficialOpenAQCountryRow[];
  non_claim: string;
}

interface OfficialOpenAQCandidateGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface OfficialOpenAQCandidateCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  candidate_rows: number;
  unique_openaq_candidate_ids: number;
  minimum_distance_km: number | null;
  maximum_distance_km: number | null;
  rows_with_public_evidence_status_not_yet_validated: number;
  validated_same_station_rows: number;
  station_radius_join_ready_rows: number;
}

interface OfficialOpenAQCandidateRow {
  candidate_review_id: string;
  iso3: string;
  country: string;
  source_name: string;
  source_station_id: string;
  source_station_name: string;
  nearest_openaq_location_id: string;
  nearest_openaq_location_name: string;
  nearest_openaq_distance_km: number | null;
  public_evidence_status: string;
  next_public_review_step: string;
}

interface OfficialOpenAQCandidateSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  coverage_counts: {
    candidate_rows: number;
    countries_with_candidates: number;
    near_plus_name_candidate_rows: number;
    rows_with_station_id_crosswalk: number;
    rows_with_public_current_status_confirmation: number;
    validated_same_station_rows: number;
    separate_nearby_station_rows: number;
    insufficient_public_evidence_rows: number;
    superseded_or_inactive_rows: number;
    station_radius_join_ready_rows: number;
  };
  evidence_gate_counts: OfficialOpenAQCandidateGate[];
  allowed_decisions: string[];
  minimum_validation_evidence: string;
  country_rows: OfficialOpenAQCandidateCountryRow[];
  candidate_rows: OfficialOpenAQCandidateRow[];
  non_claim: string;
}

interface OfficialOpenAQCandidateEvidenceGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface OfficialOpenAQCandidateEvidenceLane {
  lane: string;
  rows: number;
}

interface OfficialOpenAQCandidateEvidenceCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  candidate_rows: number;
  openaq_is_monitor_true_rows: number;
  openaq_is_monitor_false_rows: number;
  rows_with_owner_or_provider: number;
  rows_with_first_seen: number;
  crosswalk_like_public_signal_rows: number;
  validated_same_station_rows: number;
  station_radius_join_ready_rows: number;
}

interface OfficialOpenAQCandidateEvidenceRow {
  candidate_review_id: string;
  iso3: string;
  country: string;
  source_station_name: string;
  nearest_openaq_location_name: string;
  openaq_owner_name: string;
  openaq_provider_name: string;
  openaq_is_monitor: boolean;
  candidate_public_evidence_lane: string;
  reader_use: string;
}

interface OfficialOpenAQCandidateEvidenceSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    candidate_rows_audited: number;
    countries_with_candidates: number;
    unique_openaq_candidate_ids: number;
    rows_with_openaq_owner_or_provider: number;
    rows_with_openaq_is_monitor_true: number;
    rows_with_openaq_is_monitor_false: number;
    rows_with_first_seen: number;
    rows_with_last_seen: number;
    rows_with_station_id_exact_overlap: number;
    rows_with_official_agency_exact_in_openaq_owner_or_provider: number;
    rows_with_explicit_crosswalk_evidence: number;
    validated_same_station_rows: number;
    station_radius_join_ready_rows: number;
    keep_open_rows: number;
  };
  evidence_lane_counts: OfficialOpenAQCandidateEvidenceLane[];
  evidence_gate_counts: OfficialOpenAQCandidateEvidenceGate[];
  country_rows: OfficialOpenAQCandidateEvidenceCountryRow[];
  candidate_rows: OfficialOpenAQCandidateEvidenceRow[];
  non_claim: string;
}

interface CandidateCrosswalkSourceScanCountryRow {
  iso3: string;
  country: string;
  rows_scanned: number;
  separate_nearby_station_rows: number;
  validated_same_station_rows: number;
  station_radius_join_ready_rows: number;
}

interface CandidateCrosswalkSourceScanSourceRow {
  source_key: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: number;
  retrieval_bytes: number;
  matched_terms: string[];
  missing_terms: string[];
  source_note: string;
}

interface CandidateCrosswalkSourceScanRow {
  candidate_review_id: string;
  iso3: string;
  country: string;
  source_station_name: string;
  nearest_openaq_location_name: string;
  nearest_openaq_distance_km: number;
  openaq_provider_name: string;
  official_source_public_name_or_address: string;
  computed_coordinate_distance_km: number | null;
  allowed_review_decision: string;
  candidate_queue_status_after_scan: string;
  disambiguating_public_evidence: string;
  reader_use: string;
}

interface CandidateCrosswalkSourceScanSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    candidate_rows_total_before_scan: number;
    is_monitor_candidate_rows_scanned: number;
    non_monitor_candidate_rows_not_scanned: number;
    source_urls_seeded: number;
    source_urls_retrieved: number;
    rows_with_official_coordinate_evidence: number;
    rows_with_official_address_evidence: number;
    rows_with_openaq_coordinate_evidence: number;
    rows_screened_as_separate_nearby_stations: number;
    shared_station_id_rows: number;
    source_crosswalk_rows: number;
    documented_colocation_rows: number;
    validated_same_station_rows: number;
    station_radius_join_ready_rows: number;
  };
  country_rows: CandidateCrosswalkSourceScanCountryRow[];
  source_rows: CandidateCrosswalkSourceScanSourceRow[];
  candidate_rows: CandidateCrosswalkSourceScanRow[];
  non_claim: string;
}

interface CandidatePublicFeedSourceScanCountryRow {
  iso3: string;
  country: string;
  rows_scanned: number;
  public_feed_not_join_ready_rows: number;
  validated_same_station_rows: number;
  station_radius_join_ready_rows: number;
}

interface CandidatePublicFeedSourceScanRow {
  candidate_review_id: string;
  iso3: string;
  country: string;
  source_station_id: string;
  source_station_name: string;
  nearest_openaq_location_name: string;
  nearest_openaq_distance_km: number;
  computed_coordinate_distance_km: number | null;
  openaq_owner_name: string;
  openaq_provider_name: string;
  provider_context_source_keys: string;
  same_openaq_location_reused_in_scan: boolean;
  allowed_review_decision: string;
  candidate_queue_status_after_scan: string;
  disambiguating_public_evidence: string;
  reader_use: string;
}

interface CandidatePublicFeedSourceScanSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    candidate_rows_total_before_scan: number;
    public_feed_candidate_rows_scanned: number;
    is_monitor_candidate_rows_not_scanned_here: number;
    source_urls_seeded: number;
    source_urls_retrieved: number;
    rows_with_official_coordinate_evidence: number;
    rows_with_openaq_coordinate_evidence: number;
    rows_with_public_feed_owner_provider: number;
    openaq_not_is_monitor_rows: number;
    provider_context_retrieved_rows: number;
    same_openaq_location_reused_rows: number;
    official_agency_owner_provider_match_rows: number;
    shared_station_id_rows: number;
    source_owner_crosswalk_rows: number;
    current_status_crosswalk_rows: number;
    documented_colocation_rows: number;
    validated_same_station_rows: number;
    station_radius_join_ready_rows: number;
    rows_screened_public_feed_nearby_not_join_ready: number;
  };
  country_rows: CandidatePublicFeedSourceScanCountryRow[];
  source_rows: CandidateCrosswalkSourceScanSourceRow[];
  candidate_rows: CandidatePublicFeedSourceScanRow[];
  non_claim: string;
}

interface OneSignalLaneRow {
  signal_lane: string;
  label: string;
  status: string;
  rows: number;
  countries: number;
  minimum_distance_km: number | null;
  maximum_distance_km: number | null;
  reader_use: string;
}

interface OneSignalCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  queue_items: number;
  unique_official_station_keys: number;
  near_only_rows: number;
  name_only_not_near_rows: number;
  monitor_grade_provenance_only_rows: number;
  validated_same_station_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_join_ready_rows: number;
}

interface OneSignalSourceRow {
  source_key: string;
  iso3: string;
  country: string;
  source_name: string;
  source_url_present: boolean;
  queue_items: number;
  near_only_rows: number;
  name_only_not_near_rows: number;
  monitor_grade_provenance_only_rows: number;
}

interface OneSignalQueueRow {
  one_signal_id: string;
  signal_lane: string;
  review_priority: string;
  iso3: string;
  country: string;
  source_name: string;
  source_station_id: string;
  source_station_name: string;
  source_station_type: string;
  nearest_openaq_location_name: string;
  nearest_openaq_distance_km: number | "";
  missing_second_signal: string;
  grade_evidence_category: string;
  reader_use: string;
}

interface OneSignalReviewQueueSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    near_plus_name_candidate_rows_already_source_screened: number;
    one_signal_queue_items: number;
    unique_official_station_keys: number;
    countries_with_queue_items: number;
    near_only_candidate_rows: number;
    name_overlap_not_near_candidate_rows: number;
    monitor_grade_provenance_only_rows: number;
    validated_same_station_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_join_ready_rows: number;
  };
  lane_rows: OneSignalLaneRow[];
  country_rows: OneSignalCountryRow[];
  source_rows: OneSignalSourceRow[];
  evidence_gate_counts: MonitorGradeGate[];
  queue_rows: OneSignalQueueRow[];
  display_rows: OneSignalQueueRow[];
  non_claim: string;
}

interface MonitorGradeSourceValidationCountryRow {
  iso3: string;
  country: string;
  source_rows_scanned: number;
  source_rows_retrieved: number;
  monitor_grade_provenance_only_queue_items: number;
  method_or_standard_context_sources: number;
  official_or_automatic_context_sources: number;
  caution_sources: number;
  retrieval_failed_sources: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface MonitorGradeSourceValidationSourceRow {
  source_key: string;
  iso3: string;
  country: string;
  source_name: string;
  source_role: string;
  retrieved: boolean;
  queue_items_covered: number;
  matched_expected_terms: string;
  matched_method_terms: string;
  matched_caution_terms: string;
  source_grade_evidence_lane: string;
  source_validation_decision: string;
  reader_use: string;
}

interface MonitorGradeSourceValidationSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    source_urls_seeded: number;
    source_urls_retrieved: number;
    source_urls_failed: number;
    economies_scanned: number;
    monitor_grade_provenance_only_rows_covered: number;
    method_or_equipment_context_source_rows: number;
    standard_or_method_context_source_rows: number;
    official_or_automatic_context_source_rows: number;
    caution_language_source_rows: number;
    source_context_only_no_grade_language_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  evidence_gate_counts: MonitorGradeGate[];
  country_rows: MonitorGradeSourceValidationCountryRow[];
  source_rows: MonitorGradeSourceValidationSourceRow[];
  non_claim: string;
}

interface MonitorGradeStationReviewLaneRow {
  station_review_lane: string;
  label: string;
  rows: number;
  reader_use: string;
}

interface MonitorGradeStationReviewCountryRow {
  iso3: string;
  country: string;
  station_rows_reviewed: number;
  method_context_needs_station_confirmation_rows: number;
  caution_blocks_grade_rows: number;
  official_context_only_rows: number;
  current_status_confirmed_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface MonitorGradeStationReviewSourceGroupRow {
  source_group_key: string;
  iso3: string;
  country: string;
  source_name: string;
  source_rows_reviewed: number;
  station_rows_reviewed: number;
  station_review_lane: string;
  method_context_needs_station_confirmation_rows: number;
  caution_blocks_grade_rows: number;
  official_context_only_rows: number;
  matched_method_terms: string;
  matched_caution_terms: string;
  source_keys: string;
  reader_use: string;
}

interface MonitorGradeStationReviewSampleRow {
  station_review_id: string;
  station_review_lane: string;
  station_review_priority: string;
  iso3: string;
  country: string;
  source_name: string;
  source_station_id: string;
  source_station_name: string;
  source_station_type: string;
  matched_method_terms: string;
  matched_caution_terms: string;
  station_review_question: string;
  minimum_station_evidence: string;
}

interface MonitorGradeStationReviewSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    station_rows_reviewed: number;
    economies_reviewed: number;
    source_groups_reviewed: number;
    source_rows_joined: number;
    method_context_needs_station_confirmation_rows: number;
    caution_blocks_grade_rows: number;
    official_context_only_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  lane_rows: MonitorGradeStationReviewLaneRow[];
  country_rows: MonitorGradeStationReviewCountryRow[];
  source_group_rows: MonitorGradeStationReviewSourceGroupRow[];
  station_sample_rows: MonitorGradeStationReviewSampleRow[];
  evidence_gate_counts: MonitorGradeGate[];
  non_claim: string;
}

interface MonitorGradeStationMethodEvidenceLaneRow {
  row_evidence_lane: string;
  label: string;
  rows: number;
  reader_use: string;
}

interface MonitorGradeStationMethodEvidenceCountryRow {
  iso3: string;
  country: string;
  station_rows_reviewed: number;
  exact_official_rows_found: number;
  exact_pm25_signal_rows: number;
  row_level_instrument_hint_rows: number;
  row_level_pm25_portal_or_api_rows: number;
  exact_live_pm25_value_populated_rows: number;
  positive_raw_live_pm25_value_rows: number;
  negative_raw_live_pm25_value_rows: number;
  sentinel_raw_live_pm25_value_rows: number;
  missing_raw_live_pm25_value_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface MonitorGradeStationMethodEvidenceSourceGroupRow {
  source_group_key: string;
  iso3: string;
  country: string;
  source_name: string;
  station_rows_reviewed: number;
  row_evidence_lane: string;
  exact_source_evidence_type: string;
  exact_source_station_type: string;
  row_level_instrument_hint_rows: number;
  row_level_pm25_portal_or_api_rows: number;
  source_level_method_terms: string;
  row_level_method_hint_terms: string;
  reader_use: string;
}

interface MonitorGradeStationMethodEvidenceSampleRow {
  method_evidence_id: string;
  station_review_id: string;
  row_evidence_lane: string;
  iso3: string;
  country: string;
  source_name: string;
  source_station_id: string;
  source_station_name: string;
  source_station_type: string;
  exact_source_evidence_type: string;
  exact_source_station_type: string;
  exact_pm25_signal: boolean;
  exact_live_pm25_value_raw: string;
  exact_live_pm25_value_status: string;
  source_level_method_terms: string;
  row_level_method_hint_terms: string;
  reader_use: string;
}

interface MonitorGradeStationMethodEvidenceSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    method_context_station_rows_reviewed: number;
    economies_reviewed: number;
    source_groups_reviewed: number;
    exact_official_rows_found: number;
    exact_official_rows_missing: number;
    exact_pm25_signal_rows: number;
    exact_coordinate_rows: number;
    exact_live_pm25_value_populated_rows: number;
    positive_raw_live_pm25_value_rows: number;
    zero_raw_live_pm25_value_rows: number;
    negative_raw_live_pm25_value_rows: number;
    sentinel_raw_live_pm25_value_rows: number;
    missing_raw_live_pm25_value_rows: number;
    nonnumeric_raw_live_pm25_value_rows: number;
    public_current_row_observed_rows: number;
    row_level_instrument_hint_rows: number;
    row_level_pm25_portal_or_api_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  evidence_lane_rows: MonitorGradeStationMethodEvidenceLaneRow[];
  country_rows: MonitorGradeStationMethodEvidenceCountryRow[];
  source_group_rows: MonitorGradeStationMethodEvidenceSourceGroupRow[];
  station_sample_rows: MonitorGradeStationMethodEvidenceSampleRow[];
  evidence_gate_counts: MonitorGradeGate[];
  non_claim: string;
}

interface UzbekistanCurrentMethodAgeRow {
  api_reading_age_lane: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanCurrentMethodGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanCurrentMethodSampleRow {
  method_evidence_id: string;
  source_station_id: string;
  source_station_name: string;
  api_station_name: string;
  api_reading_date_iso: string;
  api_reading_age_days: number | "";
  api_reading_age_lane: string;
  api_pm25_value_raw: string;
  api_pm25_value_status: string;
  api_method_marker_terms: string;
  review_decision: string;
  reader_use: string;
}

interface UzbekistanCurrentMethodSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_uzbekistan_instrument_hint_rows: number;
    api_station_rows_returned: number;
    target_station_rows_found_in_current_api: number;
    station_level_horiba_marker_rows: number;
    api_reading_date_rows: number;
    api_reading_within_7_days_rows: number;
    api_reading_within_30_days_rows: number;
    api_reading_within_90_days_rows: number;
    api_reading_older_than_365_days_rows: number;
    positive_raw_pm25_value_rows: number;
    zero_raw_pm25_value_rows: number;
    negative_raw_pm25_value_rows: number;
    sentinel_raw_pm25_value_rows: number;
    missing_raw_pm25_value_rows: number;
    current_api_presence_confirmed_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  age_lane_rows: UzbekistanCurrentMethodAgeRow[];
  evidence_gate_counts: UzbekistanCurrentMethodGate[];
  station_sample_rows: UzbekistanCurrentMethodSampleRow[];
  non_claim: string;
}

interface UzbekistanStatusCertificationGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanStatusCertificationSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  retrieved: boolean;
  matched_method_terms: string[];
  matched_current_terms: string[];
  matched_certification_terms: string[];
  matched_calibration_terms: string[];
  source_note: string | null;
}

interface UzbekistanStatusCertificationSampleRow {
  source_station_id: string;
  source_station_name: string;
  official_region_name: string;
  official_detail_updated_iso: string;
  official_detail_pm25_value: string;
  additional_exact_station_source_keys: string;
  additional_context_source_keys: string;
  source_scan_decision: string;
}

interface UzbekistanStatusCertificationSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_uzbekistan_station_rows: number;
    source_urls_seeded: number;
    source_urls_retrieved: number;
    source_urls_failed: number;
    source_level_method_context_sources: number;
    source_level_current_context_sources: number;
    source_level_certification_context_sources: number;
    source_level_calibration_context_sources: number;
    additional_exact_station_source_mention_rows: number;
    tashkent_reference_grade_context_candidate_rows: number;
    district_commissioning_context_candidate_rows: number;
    regional_realtime_network_context_candidate_rows: number;
    official_detail_recent_measurement_rows: number;
    stale_detail_measurement_followup_rows: number;
    sentinel_detail_measurement_followup_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  source_records: UzbekistanStatusCertificationSourceRecord[];
  evidence_gate_counts: UzbekistanStatusCertificationGate[];
  station_sample_rows: UzbekistanStatusCertificationSampleRow[];
  non_claim: string;
}

interface UzbekistanBlockerFollowupGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanBlockerFollowupRow {
  source_station_id: string;
  review_focus: string;
  source_station_name: string;
  region_row_auto: string;
  region_row_updated_raw: string;
  detail_updated_iso: string;
  detail_updated_age_days: string | number;
  detail_pm25_value: string;
  detail_pm25_value_status: string;
  detail_negative_pollutant_count: number;
  detail_sentinel_minus_9999_pollutant_count: number;
  followup_decision: string;
  reader_use: string;
}

interface UzbekistanBlockerFollowupSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_blocker_rows: number;
    official_region_pages_seeded: number;
    official_region_pages_retrieved: number;
    official_detail_pages_retrieved: number;
    region_row_found_rows: number;
    region_row_updating_data_rows: number;
    region_row_horiba_context_rows: number;
    detail_page_retrieved_rows: number;
    stale_detail_blocker_rows: number;
    sentinel_pm25_blocker_rows: number;
    public_row_followup_resolved_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  evidence_gate_counts: UzbekistanBlockerFollowupGate[];
  station_rows: UzbekistanBlockerFollowupRow[];
  reader_warning: string;
}

interface UzbekistanEndpointConsistencyGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanEndpointCard {
  endpoint: string;
  routes: number;
  date_or_status: string;
  pm25: string;
  signal: string;
  tone: string;
}

interface UzbekistanEndpointConsistencyRow {
  source_station_id: string;
  source_station_name: string;
  review_focus: string;
  detail_updated_dates: string;
  detail_pm25_values: string;
  detail_cross_language_consistent: boolean;
  detail_any_stale_over_30_days: boolean;
  detail_any_pm25_sentinel: boolean;
  api_date_iso: string;
  api_pm25_value: string;
  api_pm25_value_status: string;
  region_updated_values: string;
  region_auto_values: string;
  api_detail_date_mismatch: boolean;
  api_detail_pm25_mismatch: boolean;
  region_detail_status_mismatch: boolean;
  endpoint_disagreement_count: number;
  endpoint_decision: string;
  reader_use: string;
  endpoint_cards: UzbekistanEndpointCard[];
}

interface UzbekistanEndpointConsistencySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_blocker_rows: number;
    source_routes_seeded: number;
    source_routes_retrieved: number;
    api_sources_retrieved: number;
    language_detail_pages_seeded: number;
    language_detail_pages_retrieved: number;
    language_region_rows_found: number;
    cross_language_detail_consistent_rows: number;
    api_detail_date_mismatch_rows: number;
    api_detail_pm25_mismatch_rows: number;
    region_detail_status_mismatch_rows: number;
    official_endpoint_disagreement_rows: number;
    detail_stale_over_30_days_rows: number;
    detail_pm25_sentinel_rows: number;
    unresolved_blocker_rows: number;
    public_endpoint_resolution_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  evidence_gate_counts: UzbekistanEndpointConsistencyGate[];
  station_rows: UzbekistanEndpointConsistencyRow[];
  non_claim: string;
}

interface UzbekistanExternalContextGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanExternalContextSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: string | number;
  matched_expected_terms: string[];
  matched_station_terms: string[];
  matched_status_terms: string[];
  matched_method_grade_terms: string[];
  matched_calibration_terms: string[];
  matched_caution_terms: string[];
  source_note: string;
}

interface UzbekistanExternalContextRow {
  source_station_id: string;
  source_station_name: string;
  review_focus: string;
  prior_followup_decision: string;
  prior_endpoint_decision: string;
  detail_updated_iso: string;
  detail_pm25_value: string;
  detail_pm25_value_status: string;
  api_date_iso: string;
  api_pm25_value: string;
  region_updated_values: string;
  external_source_context_keys: string;
  official_launch_context_keys: string;
  source_level_reference_context_keys: string;
  station_name_or_location_external_context_keys: string;
  exact_station_id_external_context_keys: string;
  external_exact_station_id_context: boolean;
  external_station_name_or_location_context: boolean;
  external_context_candidate: boolean;
  launch_context_only: boolean;
  source_level_reference_context_only: boolean;
  public_blocker_resolution_available: boolean;
  current_status_confirmed: boolean;
  station_method_classified: boolean;
  complete_monitor_grade_classification_available: boolean;
  station_radius_grade_assumption_ready: boolean;
  external_context_decision: string;
  reader_use: string;
}

interface UzbekistanExternalContextSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_blocker_rows: number;
    external_source_urls_seeded: number;
    external_source_urls_retrieved: number;
    official_commissioning_sources_retrieved: number;
    technical_context_sources_retrieved: number;
    rows_with_any_external_context: number;
    rows_with_launch_context_only: number;
    rows_with_source_level_reference_context_only: number;
    rows_with_station_name_or_location_external_context: number;
    rows_with_exact_station_id_external_context: number;
    public_blocker_resolution_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: { decision: string; rows: number }[];
  source_records: UzbekistanExternalContextSourceRecord[];
  evidence_gate_counts: UzbekistanExternalContextGate[];
  station_rows: UzbekistanExternalContextRow[];
  non_claim: string;
}

interface UzbekistanAirPortalNamespaceGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface UzbekistanAirPortalNamespaceSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: string | number;
  station_data_available?: boolean;
  api_error?: string;
  source_note: string;
}

interface UzbekistanAirPortalNamespaceRow {
  source_station_id: string;
  source_station_name: string;
  review_focus: string;
  prior_followup_decision: string;
  prior_endpoint_decision: string;
  official_detail_updated_iso: string;
  official_detail_pm25_value: string;
  official_detail_pm25_value_status: string;
  official_region_updated_values: string;
  air_portal_alternate_station_found: boolean;
  air_portal_alternate_station_id: string;
  air_portal_alternate_station_name: string;
  air_portal_alternate_station_active: boolean;
  air_portal_latitude: number | string;
  air_portal_longitude: number | string;
  air_portal_target_id_detail_found: boolean;
  air_portal_target_id_detail_error: string;
  air_portal_alternate_detail_found: boolean;
  air_portal_alternate_detail_datetime: string;
  air_portal_alternate_detail_date_iso: string;
  air_portal_alternate_detail_age_days: number | string;
  air_portal_alternate_detail_pm25_value: number | string;
  air_portal_alternate_detail_pm25_status: string;
  air_portal_detail_mirrors_official_detail: boolean;
  air_portal_detail_stale_over_30_days: boolean;
  air_portal_detail_pm25_sentinel: boolean;
  data_meteo_api_requires_email_application: boolean;
  endpoint_namespace_mismatch: boolean;
  active_flag_counted_as_status_closure: boolean;
  public_portal_resolution_available: boolean;
  current_status_confirmed: boolean;
  station_method_classified: boolean;
  complete_monitor_grade_classification_available: boolean;
  station_radius_grade_assumption_ready: boolean;
  portal_namespace_decision: string;
  reader_use: string;
}

interface UzbekistanAirPortalNamespaceSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_blocker_rows: number;
    source_urls_seeded: number;
    source_urls_retrieved: number;
    derived_detail_probe_routes: number;
    derived_detail_probe_routes_retrieved: number;
    data_meteo_api_landing_retrieved: number;
    data_meteo_email_application_required_rows: number;
    air_portal_station_list_retrieved: number;
    air_portal_station_objects: number;
    target_blocker_id_detail_probe_rows: number;
    target_blocker_id_detail_found_rows: number;
    alternate_station_name_match_rows: number;
    alternate_station_active_flag_rows: number;
    alternate_detail_rows_retrieved: number;
    alternate_detail_mirrors_official_detail_rows: number;
    alternate_detail_stale_rows: number;
    alternate_detail_sentinel_rows: number;
    endpoint_namespace_mismatch_rows: number;
    public_portal_resolution_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: { decision: string; rows: number }[];
  source_records: UzbekistanAirPortalNamespaceSourceRecord[];
  evidence_gate_counts: UzbekistanAirPortalNamespaceGate[];
  station_rows: UzbekistanAirPortalNamespaceRow[];
  non_claim: string;
}

interface IndonesiaGeorgiaRowMethodSourceGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface IndonesiaGeorgiaRowMethodSourceCountryRow {
  iso3: string;
  country: string;
  target_rows: number;
  source_urls_retrieved: number;
  source_urls_seeded_or_expanded: number;
  prior_exact_pm25_rows: number;
  positive_prior_raw_value_rows: number;
  missing_prior_raw_value_rows: number;
  same_page_method_context_candidate_rows: number;
  same_page_current_context_candidate_rows: number;
  station_context_candidate_rows: number;
  current_status_confirmed_rows: number;
  station_method_classified_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface IndonesiaGeorgiaRowMethodSourceDecision {
  decision: string;
  rows: number;
}

interface IndonesiaGeorgiaRowMethodSourceRecord {
  source_key: string;
  source_role: string;
  iso3: string;
  url: string;
  retrieved: boolean;
  expanded_for_station_id: string;
  matched_method_terms: string[];
  matched_current_terms: string[];
  matched_standard_terms: string[];
  source_note: string;
}

interface IndonesiaGeorgiaRowMethodSourceSampleRow {
  iso3: string;
  source_station_id: string;
  source_station_name: string;
  exact_live_pm25_value_status: string;
  exact_station_detail_timestamp_raw: string;
  same_page_method_context_candidate: boolean;
  station_alias_context_source_keys: string;
  source_scan_decision: string;
}

interface IndonesiaGeorgiaRowMethodSourceSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_indonesia_georgia_rows: number;
    target_indonesia_rows: number;
    target_georgia_rows: number;
    source_urls_seeded_or_expanded: number;
    source_urls_retrieved: number;
    source_urls_failed: number;
    prior_exact_pm25_rows: number;
    positive_prior_raw_value_rows: number;
    missing_prior_raw_value_rows: number;
    exact_station_detail_retrieved_rows: number;
    exact_station_detail_recent_within_30_days_rows: number;
    same_page_method_context_candidate_rows: number;
    same_page_current_context_candidate_rows: number;
    station_context_candidate_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  country_rows: IndonesiaGeorgiaRowMethodSourceCountryRow[];
  decision_counts: IndonesiaGeorgiaRowMethodSourceDecision[];
  evidence_gate_counts: IndonesiaGeorgiaRowMethodSourceGate[];
  source_records: IndonesiaGeorgiaRowMethodSourceRecord[];
  station_sample_rows: IndonesiaGeorgiaRowMethodSourceSampleRow[];
  non_claim: string;
}

interface StationCodeStatusMethodGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationCodeStatusMethodCountryRow {
  iso3: string;
  country: string;
  target_rows: number;
  exact_station_code_or_id_rows: number;
  pm25_row_or_equipment_rows: number;
  station_operating_description_context_rows: number;
  test_mode_or_blocker_rows: number;
  station_method_table_rows: number;
  current_status_confirmed_rows: number;
  station_method_classified_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface StationCodeStatusMethodDecision {
  decision: string;
  rows: number;
}

interface StationCodeStatusMethodSourceRecord {
  source_key: string;
  source_role: string;
  iso3: string;
  country: string;
  url: string;
  retrieval_url: string;
  retrieved: boolean;
  matched_method_terms: string[];
  matched_current_terms: string[];
  matched_standard_terms: string[];
  matched_caution_terms: string[];
  source_note: string;
}

interface StationCodeStatusMethodSampleRow {
  iso3: string;
  source_station_id: string;
  source_station_name: string;
  station_code_source_lane: string;
  pm25_row_or_equipment_listed: boolean;
  pm25_observation_rows: number;
  station_description_operating_context: boolean;
  station_test_mode_flag: boolean;
  source_scan_decision: string;
}

interface StationCodeStatusMethodSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_rows: number;
    target_georgia_rows: number;
    target_indonesia_rows: number;
    target_uzbekistan_blocker_rows: number;
    source_records_total: number;
    source_records_retrieved_or_carried_forward: number;
    exact_station_code_or_id_rows: number;
    georgia_station_code_api_rows: number;
    georgia_pm25_equipment_rows: number;
    georgia_pm25_hourly_observation_rows: number;
    georgia_operating_description_context_rows: number;
    georgia_test_mode_rows: number;
    indonesia_bmkg_payload_station_code_rows: number;
    indonesia_bmkg_xml_filename_rows: number;
    uzbekistan_unresolved_blocker_rows: number;
    station_method_table_rows: number;
    instrument_model_available_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  country_rows: StationCodeStatusMethodCountryRow[];
  decision_counts: StationCodeStatusMethodDecision[];
  evidence_gate_counts: StationCodeStatusMethodGate[];
  source_records: StationCodeStatusMethodSourceRecord[];
  station_sample_rows: StationCodeStatusMethodSampleRow[];
  non_claim: string;
}

interface StationGradeDecisionLedgerGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationGradeDecisionLedgerCountryRow {
  iso3: string;
  country: string;
  decision_rows: number;
  exact_station_code_or_id_source_rows: number;
  station_method_context_rows: number;
  operating_or_current_context_rows: number;
  raw_value_sanity_issue_rows: number;
  test_mode_or_blocker_rows: number;
  current_status_confirmed_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface StationGradeDecisionLedgerDecision {
  decision_lane: string;
  rows: number;
  reader_use: string;
  minimum_public_evidence_needed: string;
}

interface StationGradeDecisionLedgerSampleRow {
  iso3: string;
  source_station_id: string;
  source_station_name: string;
  decision_lane: string;
  row_evidence_lane: string;
  raw_value_sanity_issue_present: boolean;
  test_mode_or_blocker_present: boolean;
  source_threads: string;
  reader_use: string;
}

interface StationGradeDecisionLedgerSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    decision_rows: number;
    uzbekistan_rows: number;
    georgia_rows: number;
    indonesia_rows: number;
    exact_official_row_found_rows: number;
    exact_station_code_or_id_source_rows: number;
    pm25_row_or_equipment_rows: number;
    row_level_instrument_hint_rows: number;
    station_method_context_rows: number;
    station_code_context_rows: number;
    station_specific_context_rows: number;
    operating_or_current_context_rows: number;
    status_or_certification_context_rows: number;
    calibration_or_maintenance_context_rows: number;
    raw_value_sanity_issue_rows: number;
    test_mode_or_blocker_rows: number;
    stale_or_sentinel_blocker_rows: number;
    station_method_table_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  country_rows: StationGradeDecisionLedgerCountryRow[];
  decision_counts: StationGradeDecisionLedgerDecision[];
  evidence_gate_counts: StationGradeDecisionLedgerGate[];
  sample_rows: StationGradeDecisionLedgerSampleRow[];
  non_claim: string;
}

interface StationMethodClassificationGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface StationMethodClassificationCountryRow {
  iso3: string;
  country: string;
  target_rows: number;
  method_classified_rows: number;
  current_measurement_recent_rows: number;
  source_level_instrument_catalog_rows: number;
  unverified_or_blocker_caution_rows: number;
  current_status_confirmed_rows: number;
  calibration_status_available_rows: number;
  complete_monitor_grade_classification_rows: number;
  station_radius_grade_assumption_ready_rows: number;
}

interface StationMethodClassificationDecision {
  decision: string;
  rows: number;
}

interface StationMethodClassificationSampleRow {
  iso3: string;
  source_station_id: string;
  source_station_name: string;
  station_method_class: string;
  station_method_classified: boolean;
  current_measurement_recent: boolean;
  raw_value_or_blocker_caution: boolean;
  audit_decision: string;
}

interface StationMethodClassificationSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_rows: number;
    target_indonesia_rows: number;
    target_georgia_rows: number;
    target_uzbekistan_rows: number;
    source_records_total: number;
    source_records_retrieved: number;
    bmkg_method_classified_rows: number;
    bmkg_recent_exact_detail_rows: number;
    bmkg_regulation_calibration_context_rows: number;
    bmkg_bam1020_source_level_model_context_rows: number;
    georgia_source_level_catalog_rows: number;
    georgia_live_data_unverified_caution_rows: number;
    uzbekistan_instrument_hint_rows: number;
    raw_value_or_blocker_caution_rows: number;
    current_measurement_recent_rows: number;
    current_status_confirmed_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  country_rows: StationMethodClassificationCountryRow[];
  decision_counts: StationMethodClassificationDecision[];
  evidence_gate_counts: StationMethodClassificationGate[];
  station_sample_rows: StationMethodClassificationSampleRow[];
  non_claim: string;
}

interface BmkgOperationMaintenanceGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgOperationMaintenanceDecision {
  decision: string;
  rows: number;
}

interface BmkgOperationMaintenanceSampleRow {
  source_station_id: string;
  source_station_name: string;
  exact_station_detail_timestamp_raw: string;
  exact_station_detail_value_raw: string;
  daily_inspection_sop_context: boolean;
  maintenance_check_context: boolean;
  calibration_procedure_context: boolean;
  calibration_service_tariff_context: boolean;
  operation_maintenance_decision: string;
}

interface BmkgOperationMaintenanceSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_bmkg_rows: number;
    context_source_records: number;
    context_source_records_retrieved: number;
    exact_station_detail_records: number;
    exact_station_detail_records_retrieved: number;
    exact_station_detail_recent_within_30_days_rows: number;
    daily_inspection_sop_context_rows: number;
    daily_inspection_procedure_context_rows: number;
    maintenance_check_context_rows: number;
    calibration_procedure_context_rows: number;
    calibration_service_tariff_context_rows: number;
    regional_bam1020_model_context_rows: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    current_status_confirmed_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgOperationMaintenanceDecision[];
  evidence_gate_counts: BmkgOperationMaintenanceGate[];
  station_sample_rows: BmkgOperationMaintenanceSampleRow[];
  non_claim: string;
}

interface BmkgStationStatusGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgStationStatusDecision {
  decision: string;
  rows: number;
}

interface BmkgStationStatusSampleRow {
  source_station_id: string;
  source_station_name: string;
  detail_timestamp_raw: string;
  detail_value_ug_m3: string;
  detail_category_raw: string;
  page_bam_method_text_found: boolean;
  page_station_operational_status_found: boolean;
  station_specific_calibration_certificate_found: boolean;
  audit_decision: string;
}

interface BmkgStationValueRow {
  source_station_id: string;
  source_station_name: string;
  detail_value_ug_m3: number | null;
  detail_category_raw: string;
  detail_timestamp_raw: string;
  max_value_ug_m3: number | null;
}

interface BmkgStationStatusSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    target_bmkg_rows: number;
    detail_pages_retrieved: number;
    detail_pages_with_station_name_match: number;
    detail_pages_with_station_code_in_url: number;
    public_measurement_display_rows: number;
    parsed_timestamp_rows: number;
    parsed_value_rows: number;
    parsed_category_rows: number;
    page_pm25_method_text_rows: number;
    page_bam_method_text_rows: number;
    source_level_daily_inspection_sop_context_rows: number;
    source_level_maintenance_context_rows: number;
    source_level_calibration_context_rows: number;
    station_operational_status_page_rows: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    status_or_certificate_link_rows: number;
    current_status_confirmed_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgStationStatusDecision[];
  category_counts: Array<{ category: string; rows: number }>;
  evidence_gate_counts: BmkgStationStatusGate[];
  station_sample_rows: BmkgStationStatusSampleRow[];
  station_value_rows: BmkgStationValueRow[];
  non_claim: string;
}

interface BmkgApiParityGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgApiParityDecision {
  decision: string;
  rows: number;
}

interface BmkgApiParityStationRow {
  source_station_id: string;
  source_station_name: string;
  api_list_found: boolean;
  api_list_condition_label: string;
  api_detail_retrieved: boolean;
  api_detail_date_raw: string;
  api_detail_observation_count: number;
  api_detail_latest_hour: string | number;
  api_detail_latest_pm25_value: string | number;
  api_coordinates_available: boolean;
  api_list_detail_coordinate_match: boolean;
  api_payload_has_station_status_field: boolean;
  api_payload_has_inspection_field: boolean;
  api_payload_has_calibration_field: boolean;
  api_payload_has_certificate_field: boolean;
  api_payload_has_grade_field: boolean;
  api_payload_has_method_field: boolean;
  api_condition_is_air_quality_label_only: boolean;
  api_parity_decision: string;
  reader_use: string;
}

interface BmkgApiParityExtraRow {
  source_station_id: string;
  source_station_name: string;
  pm25_value: string | number;
  condition: string;
}

interface BmkgApiParitySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    source_routes_retrieved: number;
    auth_token_endpoint_retrieved: number;
    auth_token_obtained: number;
    pm25_list_api_retrieved: number;
    pm25_list_api_station_rows: number;
    pm25_list_api_extra_station_rows: number;
    target_station_files_in_list_api_rows: number;
    target_detail_api_routes_retrieved: number;
    target_detail_api_data_rows: number;
    target_detail_api_hourly_observation_rows: number;
    api_detail_coordinate_rows: number;
    api_coordinate_rows: number;
    api_list_detail_coordinate_match_rows: number;
    api_air_quality_condition_label_rows: number;
    api_station_status_field_rows: number;
    api_inspection_field_rows: number;
    api_calibration_field_rows: number;
    api_certificate_field_rows: number;
    api_grade_field_rows: number;
    api_method_field_rows: number;
    current_status_confirmed_rows: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgApiParityDecision[];
  evidence_gate_counts: BmkgApiParityGate[];
  station_rows: BmkgApiParityStationRow[];
  station_sample_rows: BmkgApiParityStationRow[];
  extra_api_station_rows: BmkgApiParityExtraRow[];
  non_claim: string;
}

interface BmkgRegionalStatusGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgRegionalStatusDecision {
  decision: string;
  rows: number;
}

interface BmkgRegionalStatusDisplayRow {
  source_station_id: string;
  source_station_name: string;
  matched_source_keys: string;
  matched_source_roles: string;
  source_url_count: number;
  exact_station_name_external_context: boolean;
  explicit_regional_status_online: boolean;
  status_source_key: string;
  status_source_url: string;
  status_timestamp_raw: string;
  status_value_ug_m3: string;
  status_category_raw: string;
  source_latitude: string;
  source_longitude: string;
  current_status_confirmed: boolean;
  complete_monitor_grade_classification_available: boolean;
  station_radius_grade_assumption_ready: boolean;
  regional_status_decision: string;
  reader_use: string;
}

interface BmkgRegionalStatusSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: string | number;
  retrieval_bytes: number;
  matched_expected_terms: string;
  matched_target_station_rows: number;
  retrieval_error: string;
  source_note: string;
}

interface BmkgRegionalStatusSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    regional_public_source_urls_seeded: number;
    regional_public_source_urls_retrieved: number;
    official_regional_station_status_sources_retrieved: number;
    public_information_or_service_sources_retrieved: number;
    rows_with_exact_station_name_external_context: number;
    rows_with_location_level_external_context: number;
    rows_with_regional_online_status: number;
    current_status_confirmed_rows: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgRegionalStatusDecision[];
  evidence_gate_counts: BmkgRegionalStatusGate[];
  display_rows: BmkgRegionalStatusDisplayRow[];
  source_records: BmkgRegionalStatusSourceRecord[];
  non_claim: string;
}

interface BmkgDashboardStatusGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgDashboardStatusDecision {
  decision: string;
  rows: number;
}

interface BmkgDashboardStatusDisplayRow {
  source_station_id: string;
  source_station_name: string;
  dashboard_location_key: string;
  dashboard_location_found: boolean;
  dashboard_status_raw: string;
  dashboard_timestamp_raw: string;
  dashboard_timestamp_iso: string;
  dashboard_timestamp_age_hours: number | string;
  dashboard_timestamp_current_within_30_days: boolean;
  dashboard_pm25_ug_m3: number | string;
  dashboard_category_raw: string;
  dashboard_latitude: number | string;
  dashboard_longitude: number | string;
  dashboard_timeseries_points: number;
  dashboard_positive_observation_count: number;
  dashboard_zero_observation_count: number;
  dashboard_last_label: string;
  explicit_dashboard_online: boolean;
  explicit_dashboard_delayed: boolean;
  current_status_confirmed: boolean;
  complete_monitor_grade_classification_available: boolean;
  station_radius_grade_assumption_ready: boolean;
  dashboard_status_decision: string;
  reader_use: string;
}

interface BmkgDashboardStatusSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: string | number;
  retrieval_bytes: number;
  matched_expected_terms: string;
  dashboard_location_count: number | string;
  matched_target_station_rows: number;
  retrieval_error: string;
  source_note: string;
}

interface BmkgDashboardStatusSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    dashboard_source_urls_seeded: number;
    dashboard_source_urls_retrieved: number;
    official_parent_page_sources_retrieved: number;
    official_dashboard_data_sources_retrieved: number;
    dashboard_locations_total: number;
    target_dashboard_location_rows: number;
    target_dashboard_current_timestamp_rows: number;
    target_dashboard_online_rows: number;
    target_dashboard_delayed_rows: number;
    current_status_confirmed_rows: number;
    target_latest_positive_pm25_rows: number;
    target_timeseries_observation_rows: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgDashboardStatusDecision[];
  evidence_gate_counts: BmkgDashboardStatusGate[];
  display_rows: BmkgDashboardStatusDisplayRow[];
  source_records: BmkgDashboardStatusSourceRecord[];
  non_claim: string;
}

interface BmkgGradeBasisGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgGradeBasisDecision {
  decision: string;
  rows: number;
}

interface BmkgGradeBasisStationRow {
  source_station_id: string;
  source_station_name: string;
  station_method_class: string;
  station_name_context_source_keys: string;
  grade_basis_decision: string;
}

interface BmkgGradeBasisSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: string | number;
  retrieval_bytes: number;
  matched_expected_terms: string;
  matched_method_terms: string;
  matched_technical_standard_terms: string;
  matched_daily_log_terms: string;
  matched_calibration_terms: string;
  matched_certificate_terms: string;
  matched_target_station_rows: number;
  retrieval_error: string;
  source_note: string;
}

interface BmkgGradeBasisSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    grade_basis_source_urls_seeded: number;
    grade_basis_source_urls_retrieved: number;
    official_standard_or_rule_sources_retrieved: number;
    official_service_or_tariff_sources_retrieved: number;
    official_report_or_ppid_sources_retrieved: number;
    rows_with_station_name_context_in_grade_basis_sources: number;
    source_level_method_basis_sources: number;
    source_level_technical_standard_sources: number;
    source_level_daily_log_or_inspection_sources: number;
    source_level_periodic_calibration_rule_sources: number;
    source_level_calibration_service_sources: number;
    source_level_certificate_request_or_output_sources: number;
    source_level_pm25_network_context_sources: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgGradeBasisDecision[];
  evidence_gate_counts: BmkgGradeBasisGate[];
  display_rows: BmkgGradeBasisStationRow[];
  source_records: BmkgGradeBasisSourceRecord[];
  non_claim: string;
}

interface BmkgStationPublicContextGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgStationPublicContextDecision {
  decision: string;
  rows: number;
}

interface BmkgStationPublicContextDisplayRow {
  source_station_id: string;
  source_station_name: string;
  public_context_source_keys: string;
  station_unit_or_exact_context_sources: number;
  city_or_deployment_context_sources: number;
  method_context_sources: number;
  calibration_context_sources: number;
  station_public_context_decision: string;
  reader_use: string;
}

interface BmkgStationPublicContextSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  source_match_scope: string;
  url: string;
  retrieved: boolean;
  http_status: string | number;
  matched_target_station_ids: string;
  matched_alias_terms: string;
  matched_expected_terms: string;
  matched_method_terms: string;
  matched_calibration_terms: string;
  matched_inspection_terms: string;
  matched_certificate_terms: string;
  matched_status_terms: string;
  retrieval_error: string;
  source_note: string;
}

interface BmkgStationPublicContextSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    station_public_context_source_urls_seeded: number;
    station_public_context_source_urls_retrieved: number;
    official_or_regulator_sources_retrieved: number;
    academic_or_journal_sources_retrieved: number;
    rows_with_any_public_station_context: number;
    rows_with_station_unit_or_exact_context: number;
    rows_with_city_or_deployment_context: number;
    rows_with_station_method_context: number;
    rows_with_station_calibration_context: number;
    rows_with_station_inspection_or_operation_context: number;
    rows_with_certificate_context_not_station_certificate: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgStationPublicContextDecision[];
  evidence_gate_counts: BmkgStationPublicContextGate[];
  display_rows: BmkgStationPublicContextDisplayRow[];
  source_records: BmkgStationPublicContextSourceRecord[];
  non_claim: string;
}

interface BmkgInstallationAuditGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgInstallationAuditDecision {
  decision: string;
  rows: number;
}

interface BmkgInstallationAuditDisplayRow {
  source_station_id: string;
  source_station_name: string;
  matched_source_keys: string;
  exact_station_audit_calibration_sources: number;
  pm25_installation_deployment_sources: number;
  installation_audit_decision: string;
  reader_use: string;
}

interface BmkgInstallationAuditSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  source_match_scope: string;
  retrieved: boolean;
  http_status: string | number;
  matched_target_station_ids: string;
  matched_pm25_terms: string;
  matched_installation_terms: string;
  matched_audit_terms: string;
  matched_calibration_terms: string;
  matched_operation_terms: string;
  source_note: string;
}

interface BmkgInstallationAuditSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    installation_audit_source_urls_seeded: number;
    installation_audit_source_urls_retrieved: number;
    official_sources_retrieved: number;
    rows_with_any_installation_or_audit_context: number;
    rows_with_exact_station_audit_calibration_context: number;
    rows_with_pm25_installation_deployment_context: number;
    source_level_operational_or_calibration_sources: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: BmkgInstallationAuditDecision[];
  evidence_gate_counts: BmkgInstallationAuditGate[];
  display_rows: BmkgInstallationAuditDisplayRow[];
  source_records: BmkgInstallationAuditSourceRecord[];
  non_claim: string;
}

interface BmkgNearClosureGate {
  gate: string;
  status: string;
  rows: number;
  note: string;
}

interface BmkgNearClosureLane {
  lane: string;
  rows: number;
}

interface BmkgNearClosureDisplayRow {
  source_station_id: string;
  source_station_name: string;
  station_method_class: string;
  method_classified: boolean;
  detail_page_display_found: boolean;
  station_page_bam_method_text_found: boolean;
  dashboard_status_raw: string;
  dashboard_current_status_confirmed: boolean;
  dashboard_delayed: boolean;
  source_level_grade_basis_available: boolean;
  source_level_periodic_calibration_rule_sources: number;
  source_level_calibration_service_sources: number;
  source_level_certificate_context_sources: number;
  station_unit_or_exact_context_sources: number;
  exact_station_audit_calibration_sources: number;
  pm25_installation_deployment_sources: number;
  station_specific_inspection_log_found: boolean;
  station_specific_calibration_certificate_found: boolean;
  calibration_status_available: boolean;
  complete_monitor_grade_classification_available: boolean;
  station_radius_grade_assumption_ready: boolean;
  visible_evidence_gate_count: number;
  blocking_gate_count: number;
  near_closure_lane: string;
  reader_use: string;
}

interface BmkgNearClosureSummary {
  generated_at: string;
  attestation_chain: string;
  status: string;
  method: string;
  counts: {
    bmkg_target_rows: number;
    station_method_classified_rows: number;
    detail_page_display_rows: number;
    dashboard_current_online_rows: number;
    dashboard_delayed_rows: number;
    source_level_grade_basis_rows: number;
    station_unit_or_exact_context_rows: number;
    exact_audit_calibration_context_rows: number;
    pm25_installation_deployment_context_rows: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_rows: number;
    complete_monitor_grade_rows: number;
    station_radius_ready_rows: number;
  };
  lane_counts: BmkgNearClosureLane[];
  evidence_gate_counts: BmkgNearClosureGate[];
  display_rows: BmkgNearClosureDisplayRow[];
  non_claim: string;
}

interface BmkgCertificateStatusTargetedGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgCertificateStatusTargetedLane {
  lane: string;
  sources: number;
}

interface BmkgCertificateStatusTargetedDecision {
  decision: string;
  rows: number;
}

interface BmkgCertificateStatusTargetedDisplayRow {
  source_station_id: string;
  source_station_name: string;
  targeted_source_keys: string;
  exact_station_maintenance_sources: number;
  exact_station_pm25_method_sources: number;
  exact_station_calibration_language_sources: number;
  exact_station_certificate_language_sources: number;
  certificate_status_decision: string;
  reader_use: string;
}

interface BmkgCertificateStatusTargetedSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  source_match_scope: string;
  retrieved: boolean;
  http_status: string | number;
  matched_target_station_ids: string;
  matched_expected_terms: string;
  matched_pm25_terms: string;
  matched_maintenance_terms: string;
  matched_calibration_terms: string;
  matched_certificate_terms: string;
  matched_status_terms: string;
  source_search_lane: string;
  source_note: string;
}

interface BmkgCertificateStatusTargetedSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    certificate_status_source_urls_seeded: number;
    certificate_status_source_urls_retrieved: number;
    exact_station_or_unit_source_urls_retrieved: number;
    source_level_inspection_service_or_certificate_routes_retrieved: number;
    rows_with_any_targeted_source_context: number;
    rows_with_exact_maintenance_context: number;
    rows_with_exact_pm25_method_context: number;
    rows_with_exact_calibration_language_context: number;
    rows_with_exact_certificate_language_not_certificate: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_from_this_scan_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  source_lane_counts: BmkgCertificateStatusTargetedLane[];
  decision_counts: BmkgCertificateStatusTargetedDecision[];
  evidence_gate_counts: BmkgCertificateStatusTargetedGate[];
  display_rows: BmkgCertificateStatusTargetedDisplayRow[];
  source_records: BmkgCertificateStatusTargetedSourceRecord[];
  non_claim: string;
}

interface BmkgPpidAccessRouteGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface BmkgPpidAccessRouteLane {
  lane: string;
  sources: number;
}

interface BmkgPpidAccessRouteDecision {
  decision: string;
  rows: number;
}

interface BmkgPpidAccessRouteDisplayRow {
  source_station_id: string;
  source_station_name: string;
  dashboard_status_raw: string;
  public_pm25_display_route_available: boolean;
  source_level_calibration_service_route_available: boolean;
  source_level_certificate_request_context_available: boolean;
  raw_data_exclusion_context_available: boolean;
  access_route_decision: string;
  reader_use: string;
}

interface BmkgPpidAccessRouteSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  source_scope: string;
  retrieved: boolean;
  http_status: string | number;
  matched_pm25_terms: string;
  matched_public_access_terms: string;
  matched_calibration_terms: string;
  matched_certificate_terms: string;
  matched_excluded_terms: string;
  matched_target_station_ids: string;
  source_lane: string;
  source_note: string;
}

interface BmkgPpidAccessRouteSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_bmkg_rows: number;
    ppid_access_source_urls_seeded: number;
    ppid_access_source_urls_retrieved: number;
    public_pm25_catalog_route_sources: number;
    public_pm25_station_display_sources: number;
    target_rows_on_public_pm25_display: number;
    source_level_calibration_service_routes: number;
    certificate_request_context_sources: number;
    raw_data_exclusion_context_sources: number;
    station_specific_inspection_log_rows: number;
    station_specific_calibration_certificate_rows: number;
    calibration_status_available_rows: number;
    current_status_confirmed_from_this_scan_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  source_lane_counts: BmkgPpidAccessRouteLane[];
  decision_counts: BmkgPpidAccessRouteDecision[];
  evidence_gate_counts: BmkgPpidAccessRouteGate[];
  display_rows: BmkgPpidAccessRouteDisplayRow[];
  source_records: BmkgPpidAccessRouteSourceRecord[];
  non_claim: string;
}

interface GeorgiaReportVerificationGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface GeorgiaReportVerificationDecision {
  decision: string;
  rows: number;
}

interface GeorgiaReportVerificationSampleRow {
  source_station_id: string;
  source_station_name: string;
  station_code_in_monthly_report: boolean;
  pm25_column_in_monthly_report: boolean;
  monthly_report_not_verified_label_present: boolean;
  report_verification_decision: string;
}

interface GeorgiaReportVerificationSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  report_month: string;
  coverage_counts: {
    target_georgia_rows: number;
    source_records: number;
    source_records_retrieved: number;
    station_code_in_monthly_report_rows: number;
    station_name_or_alias_in_monthly_report_rows: number;
    pm25_column_in_monthly_report_rows: number;
    monthly_report_not_verified_label_rows: number;
    monthly_report_verified_label_without_not_verified_rows: number;
    aqi_note_live_data_unverified_caution_rows: number;
    aqi_note_verified_reports_claim_rows: number;
    network_catalog_instrument_context_rows: number;
    current_measurement_recent_from_prior_audit_rows: number;
    verified_report_closure_available_rows: number;
    station_method_classified_rows: number;
    current_status_confirmed_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: GeorgiaReportVerificationDecision[];
  evidence_gate_counts: GeorgiaReportVerificationGate[];
  station_sample_rows: GeorgiaReportVerificationSampleRow[];
  non_claim: string;
}

interface GeorgiaReportExportLadderGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface GeorgiaReportExportLadderDecision {
  decision: string;
  rows: number;
}

interface GeorgiaReportExportLadderMonthRow {
  report_month: string;
  station_code_count_in_html: number;
  pm25_column_in_html: boolean;
  html_not_verified_label_present: boolean;
  html_verified_label_without_not_verified: boolean;
  xlsx_export_tested: boolean;
  xlsx_target_station_sheet_count: number | string;
  pdf_not_verified_label_present: boolean;
  report_export_decision: string;
}

interface GeorgiaReportExportLadderProbeRow {
  report_month: string;
  xlsx_retrieved: boolean;
  xlsx_sheet_count: number;
  xlsx_target_station_sheet_count: number;
  xlsx_pm25_present: boolean;
  xlsx_verification_label_present: boolean;
  pdf_retrieved: boolean;
  pdf_text_pages: number;
  pdf_pm25_present: boolean;
  pdf_not_verified_label_present: boolean;
  pdf_verified_label_without_not_verified: boolean;
}

interface GeorgiaReportExportLadderSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  start_month: string;
  months_to_scan: number;
  export_probe_months: string[];
  coverage_counts: {
    months_scanned: number;
    target_station_codes: number;
    html_months_retrieved: number;
    html_months_with_all_target_station_codes: number;
    html_months_with_pm25_column: number;
    html_not_verified_label_months: number;
    html_verified_label_without_not_verified_months: number;
    export_probe_months: number;
    xlsx_export_probe_months_retrieved: number;
    xlsx_export_probe_months_with_all_target_sheets: number;
    xlsx_export_probe_months_with_pm25: number;
    xlsx_export_probe_months_with_verification_label: number;
    pdf_export_probe_months_retrieved: number;
    pdf_export_probe_months_with_not_verified_label: number;
    pdf_export_probe_months_verified_without_not_verified: number;
    verified_report_closure_available_months: number;
    current_status_confirmed_months: number;
    station_method_classified_months: number;
    complete_monitor_grade_classification_months: number;
    station_radius_grade_assumption_ready_months: number;
  };
  decision_counts: GeorgiaReportExportLadderDecision[];
  evidence_gate_counts: GeorgiaReportExportLadderGate[];
  month_rows: GeorgiaReportExportLadderMonthRow[];
  export_probe_rows: GeorgiaReportExportLadderProbeRow[];
  non_claim: string;
}

interface GeorgiaVerificationPolicyGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface GeorgiaVerificationPolicyDecision {
  decision: string;
  rows: number;
}

interface GeorgiaVerificationPolicySourceRow {
  source_key: string;
  source_role: string;
  retrieved: boolean;
  matched_expected_terms: string;
  matched_verification_terms: string;
  matched_instrument_terms: string;
  matched_station_terms: string;
  policy_decision: string;
  reader_use: string;
}

interface GeorgiaVerificationPolicyBridge {
  policy_says_reports_are_verified_surface: boolean;
  scanned_report_surfaces_still_not_verified: boolean;
  verified_report_closure_available: boolean;
  decision: string;
  reader_use: string;
}

interface GeorgiaVerificationPolicySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    source_routes_targeted: number;
    source_routes_retrieved: number;
    policy_sources_retrieved: number;
    live_data_not_verified_policy_sources: number;
    verified_data_reports_policy_sources: number;
    report_generator_available_sources: number;
    network_method_context_sources: number;
    instrument_model_context_sources: number;
    network_or_instrument_context_sources: number;
    plan_validated_capture_rate_context_sources: number;
    plan_station_area_context_sources: number;
    exact_target_station_code_context_sources: number;
    months_scanned: number;
    target_station_codes: number;
    html_months_with_all_target_station_codes: number;
    html_not_verified_label_months: number;
    html_verified_label_without_not_verified_months: number;
    export_probe_months: number;
    xlsx_export_probe_months_with_all_target_sheets: number;
    xlsx_export_probe_months_with_verification_label: number;
    pdf_export_probe_months_with_not_verified_label: number;
    pdf_export_probe_months_verified_without_not_verified: number;
    verified_report_closure_available_months: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
    policy_report_surface_contradiction_rows: number;
  };
  decision_counts: GeorgiaVerificationPolicyDecision[];
  evidence_gate_counts: GeorgiaVerificationPolicyGate[];
  policy_bridge: GeorgiaVerificationPolicyBridge;
  source_rows: GeorgiaVerificationPolicySourceRow[];
  non_claim: string;
}

interface GeorgiaReportFrequencyGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface GeorgiaReportFrequencyDecision {
  decision: string;
  rows: number;
}

interface GeorgiaReportFrequencyRow {
  report_type: string;
  route_probes: number;
  valid_payload_routes: number;
  server_error_routes: number;
  html_not_verified_routes: number;
  pdf_not_verified_routes: number;
  xlsx_station_sheet_routes: number;
  verified_closure_routes: number;
  reader_use: string;
}

interface GeorgiaReportFrequencySampleRow {
  report_type: string;
  export_type: string;
  probe_date: string;
  http_status: number;
  valid_payload: boolean;
  station_code_matches: number;
  pm25_present: boolean;
  not_verified_label_present: boolean;
  verified_label_without_not_verified: boolean;
  xlsx_target_station_sheet_count: number;
  report_frequency_decision: string;
}

interface GeorgiaReportFrequencySummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    route_probes_targeted: number;
    routes_retrieved_200: number;
    valid_payload_routes: number;
    server_error_routes: number;
    annual_server_error_routes: number;
    daily_routes_tested: number;
    monthly_routes_tested: number;
    annual_routes_tested: number;
    html_not_verified_routes: number;
    pdf_not_verified_routes: number;
    html_pdf_not_verified_routes: number;
    xlsx_valid_routes: number;
    xlsx_all_target_station_sheet_routes: number;
    xlsx_verification_label_routes: number;
    routes_with_all_target_station_codes: number;
    routes_with_pm25: number;
    verified_label_without_not_verified_routes: number;
    verified_report_closure_available_routes: number;
    current_status_confirmed_routes: number;
    station_method_classified_routes: number;
    complete_monitor_grade_classification_routes: number;
    station_radius_grade_assumption_ready_routes: number;
  };
  frequency_rows: GeorgiaReportFrequencyRow[];
  decision_counts: GeorgiaReportFrequencyDecision[];
  evidence_gate_counts: GeorgiaReportFrequencyGate[];
  sample_rows: GeorgiaReportFrequencySampleRow[];
  non_claim: string;
}

interface GeorgiaNetworkLaunchGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface GeorgiaNetworkLaunchDecision {
  decision: string;
  rows: number;
}

interface GeorgiaNetworkLaunchCityRow {
  target_city: string;
  target_rows: number;
  public_source_context_rows: number;
  launch_source_context_rows: number;
  current_network_city_context_rows: number;
  standard_or_pm25_context_rows: number;
  station_code_context_rows: number;
  complete_grade_rows: number;
}

interface GeorgiaNetworkLaunchDisplayRow {
  source_station_id: string;
  source_station_name: string;
  target_city: string;
  launch_source_context: boolean;
  current_network_city_context: boolean;
  city_level_standard_equipment_context: boolean;
  station_code_in_source: boolean;
  network_launch_decision: string;
  reader_use: string;
}

interface GeorgiaNetworkLaunchSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  url: string;
  retrieved: boolean;
  http_status: number;
  retrieval_bytes: number;
  matched_city_terms: string[];
  matched_method_terms: string[];
  matched_current_terms: string[];
  source_note: string;
}

interface GeorgiaNetworkLaunchSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_georgia_rows: number;
    source_records: number;
    source_records_retrieved: number;
    current_network_source_records: number;
    launch_source_records: number;
    rows_with_public_source_context: number;
    rows_with_launch_source_context: number;
    rows_with_current_network_city_context: number;
    rows_with_standard_or_pm25_context: number;
    rows_with_pm25_pollutant_context: number;
    rows_with_station_name_or_address_context: number;
    rows_with_station_code_in_source: number;
    verified_report_closure_available_rows: number;
    current_status_confirmed_rows: number;
    station_method_classified_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: GeorgiaNetworkLaunchDecision[];
  evidence_gate_counts: GeorgiaNetworkLaunchGate[];
  city_rows: GeorgiaNetworkLaunchCityRow[];
  display_rows: GeorgiaNetworkLaunchDisplayRow[];
  source_records: GeorgiaNetworkLaunchSourceRecord[];
  non_claim: string;
}

interface GeorgiaIndicatorEndpointGate {
  gate: string;
  status: string;
  rows: number;
  reader_use: string;
}

interface GeorgiaIndicatorEndpointDecision {
  decision: string;
  rows: number;
}

interface GeorgiaIndicatorEndpointDisplayRow {
  source_station_id: string;
  source_station_name: string;
  target_city: string;
  matched_indicator_codes: string;
  matched_indicator_station_count: number;
  matched_indicator_pm25_station_count: number;
  indicator_endpoint_decision: string;
  reader_use: string;
}

interface GeorgiaIndicatorEndpointSourceRecord {
  source_key: string;
  source_name: string;
  source_role: string;
  retrieval_url: string;
  final_url: string;
  retrieved: boolean;
  http_status: string | number;
  content_type: string;
  retrieval_bytes: number;
  sha256: string;
  json_array_rows: number;
  matched_expected_terms: string;
  matched_station_code_terms: string;
  matched_pm25_terms: string;
  matched_verification_terms: string;
  matched_status_terms: string;
  retrieval_error: string;
  source_note: string;
}

interface GeorgiaIndicatorEndpointSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  source_scope: string;
  coverage_counts: {
    target_georgia_rows: number;
    source_routes_seeded: number;
    source_routes_retrieved: number;
    indicator_api_station_objects: number;
    daily_api_route_available: number;
    exact_indicator_station_code_rows: number;
    indicator_city_alias_context_rows: number;
    indicator_pm25_context_rows: number;
    indicator_verification_language_rows: number;
    daily_endpoint_verified_closure_rows: number;
    current_status_confirmed_rows: number;
    calibration_status_available_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready_rows: number;
  };
  decision_counts: GeorgiaIndicatorEndpointDecision[];
  evidence_gate_counts: GeorgiaIndicatorEndpointGate[];
  display_rows: GeorgiaIndicatorEndpointDisplayRow[];
  source_records: GeorgiaIndicatorEndpointSourceRecord[];
  non_claim: string;
}

interface MonitorGradeCountryRow {
  iso3: string;
  iso2: string;
  country: string;
  source_name: string;
  rows_audited: number;
  coordinate_rows: number;
  method_standard_signal_rows: number;
  automatic_or_official_portal_signal_rows: number;
  sensor_under_test_rows: number;
  plan_only_rows: number;
  complete_monitor_grade_classification_rows: number;
  dominant_grade_evidence_category: string;
}

interface MonitorGradeSummary {
  generated_at: string;
  program: string;
  attestation_chain: string;
  status: string;
  method: string;
  goal_level: string;
  coverage_counts: {
    official_station_rows_audited: number;
    official_coordinate_rows_audited: number;
    economies_audited: number;
    economies_with_method_standard_signal: number;
    method_standard_signal_rows: number;
    automatic_or_official_portal_signal_only_rows: number;
    sensor_under_test_rows: number;
    plan_only_no_grade_rows: number;
    no_public_grade_language_rows: number;
    complete_monitor_grade_classification_rows: number;
    station_radius_grade_assumption_ready: boolean;
  };
  evidence_gate_counts: MonitorGradeGate[];
  country_rows: MonitorGradeCountryRow[];
  non_claim: string;
}

type AirMode = "concentration" | "residual" | "exposure";

const MODES: Array<{ id: AirMode; label: string }> = [
  { id: "concentration", label: "Zero-monitor concentration" },
  { id: "residual", label: "GDP residuals" },
  { id: "exposure", label: "Exposure vs monitor count" },
];

function formatNumber(value: number | null | undefined, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
}

function pct(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${(value * 100).toFixed(digits)}%`;
}

function signed(value: number | null | undefined, digits = 3) {
  if (value === null || value === undefined || Number.isNaN(value)) return "missing";
  return `${value >= 0 ? "+" : ""}${value.toFixed(digits)}`;
}

function log10(value: number) {
  return Math.log(value) / Math.LN10;
}

function clamp(value: number, min: number, max: number) {
  return Math.max(min, Math.min(max, value));
}

function zeroByIso(rows: ZeroMonitorRow[], iso: string) {
  return rows.find((row) => row.iso3 === iso);
}

function residualByIso(rows: ResidualRow[], iso: string) {
  return rows.find((row) => row.iso3 === iso);
}

function sentenceCaseStatus(value: string) {
  return value.replaceAll("_", " ");
}

function gateTone(status: string) {
  if (status === "available" || status === "computed" || status === "available_prefreeze") return "available";
  if (
    status === "partly_available" ||
    status === "available_with_version_drift" ||
    status === "limited" ||
    status === "caution"
  ) return "pending";
  if (status === "not_yet_collected" || status.includes("not_collected")) return "pending";
  return "blocked";
}

export default function ShowcaseAirMonitoring() {
  const [deepening, setDeepening] = useState<DeepeningData | null>(null);
  const [panel, setPanel] = useState<AirPanelData | null>(null);
  const [metadataReadiness, setMetadataReadiness] = useState<MetadataReadinessSummary | null>(null);
  const [stationMetadata, setStationMetadata] = useState<StationMetadataSummary | null>(null);
  const [stationRadiusReadiness, setStationRadiusReadiness] =
    useState<StationRadiusReadinessSummary | null>(null);
  const [stationRadiusSourcePlan, setStationRadiusSourcePlan] =
    useState<StationRadiusSourcePlanSummary | null>(null);
  const [stationRadiusAcquisition, setStationRadiusAcquisition] =
    useState<StationRadiusAcquisitionSummary | null>(null);
  const [stationRadiusFileManifest, setStationRadiusFileManifest] =
    useState<StationRadiusFileManifestSummary | null>(null);
  const [stationRadiusDownloadFeasibility, setStationRadiusDownloadFeasibility] =
    useState<StationRadiusDownloadFeasibilitySummary | null>(null);
  const [stationRadiusAcagVersion, setStationRadiusAcagVersion] =
    useState<StationRadiusAcagVersionSummary | null>(null);
  const [stationRadiusAcagChecksum, setStationRadiusAcagChecksum] =
    useState<StationRadiusAcagChecksumSummary | null>(null);
  const [stationRadiusGhslTileSelection, setStationRadiusGhslTileSelection] =
    useState<StationRadiusGhslTileSelectionSummary | null>(null);
  const [stationRadiusGhslTileChecksum, setStationRadiusGhslTileChecksum] =
    useState<StationRadiusGhslTileChecksumSummary | null>(null);
  const [stationRadiusGhslTileRouting, setStationRadiusGhslTileRouting] =
    useState<StationRadiusGhslTileRoutingSummary | null>(null);
  const [stationRadiusGhslCorrectedCustody, setStationRadiusGhslCorrectedCustody] =
    useState<StationRadiusGhslCorrectedCustodySummary | null>(null);
  const [stationRadiusGhslLargeCustody, setStationRadiusGhslLargeCustody] =
    useState<StationRadiusGhslLargeCustodySummary | null>(null);
  const [stationRadiusMethodPrefreeze, setStationRadiusMethodPrefreeze] =
    useState<StationRadiusMethodPrefreezeSummary | null>(null);
  const [stationRadiusRuleSourceScan, setStationRadiusRuleSourceScan] =
    useState<StationRadiusRuleSummary | null>(null);
  const [stationRadiusPm25Resolution, setStationRadiusPm25Resolution] =
    useState<StationRadiusPm25ResolutionSummary | null>(null);
  const [stationRadiusDenominatorJoin, setStationRadiusDenominatorJoin] =
    useState<StationRadiusDenominatorJoinSummary | null>(null);
  const [stationRadiusCountryUnion, setStationRadiusCountryUnion] =
    useState<StationRadiusCountryUnionSummary | null>(null);
  const [stationRadiusClaimGate, setStationRadiusClaimGate] =
    useState<StationRadiusClaimGateSummary | null>(null);
  const [regulatorSource, setRegulatorSource] = useState<RegulatorSourceSummary | null>(null);
  const [regulatorStation, setRegulatorStation] = useState<RegulatorStationSummary | null>(null);
  const [officialOpenAQ, setOfficialOpenAQ] = useState<OfficialOpenAQSummary | null>(null);
  const [officialOpenAQCandidate, setOfficialOpenAQCandidate] = useState<OfficialOpenAQCandidateSummary | null>(null);
  const [officialOpenAQCandidateEvidence, setOfficialOpenAQCandidateEvidence] =
    useState<OfficialOpenAQCandidateEvidenceSummary | null>(null);
  const [candidateCrosswalkSourceScan, setCandidateCrosswalkSourceScan] =
    useState<CandidateCrosswalkSourceScanSummary | null>(null);
  const [candidatePublicFeedSourceScan, setCandidatePublicFeedSourceScan] =
    useState<CandidatePublicFeedSourceScanSummary | null>(null);
  const [oneSignalReviewQueue, setOneSignalReviewQueue] =
    useState<OneSignalReviewQueueSummary | null>(null);
  const [monitorGradeSourceValidation, setMonitorGradeSourceValidation] =
    useState<MonitorGradeSourceValidationSummary | null>(null);
  const [monitorGradeStationReview, setMonitorGradeStationReview] =
    useState<MonitorGradeStationReviewSummary | null>(null);
  const [monitorGradeStationMethodEvidence, setMonitorGradeStationMethodEvidence] =
    useState<MonitorGradeStationMethodEvidenceSummary | null>(null);
  const [uzbekistanCurrentMethod, setUzbekistanCurrentMethod] =
    useState<UzbekistanCurrentMethodSummary | null>(null);
  const [uzbekistanStatusCertification, setUzbekistanStatusCertification] =
    useState<UzbekistanStatusCertificationSummary | null>(null);
  const [uzbekistanBlockerFollowup, setUzbekistanBlockerFollowup] =
    useState<UzbekistanBlockerFollowupSummary | null>(null);
  const [uzbekistanEndpointConsistency, setUzbekistanEndpointConsistency] =
    useState<UzbekistanEndpointConsistencySummary | null>(null);
  const [uzbekistanExternalContext, setUzbekistanExternalContext] =
    useState<UzbekistanExternalContextSummary | null>(null);
  const [uzbekistanAirPortalNamespace, setUzbekistanAirPortalNamespace] =
    useState<UzbekistanAirPortalNamespaceSummary | null>(null);
  const [indonesiaGeorgiaRowMethodSource, setIndonesiaGeorgiaRowMethodSource] =
    useState<IndonesiaGeorgiaRowMethodSourceSummary | null>(null);
  const [stationCodeStatusMethod, setStationCodeStatusMethod] =
    useState<StationCodeStatusMethodSummary | null>(null);
  const [stationGradeDecisionLedger, setStationGradeDecisionLedger] =
    useState<StationGradeDecisionLedgerSummary | null>(null);
  const [stationMethodClassification, setStationMethodClassification] =
    useState<StationMethodClassificationSummary | null>(null);
  const [bmkgOperationMaintenance, setBmkgOperationMaintenance] =
    useState<BmkgOperationMaintenanceSummary | null>(null);
  const [bmkgStationStatus, setBmkgStationStatus] =
    useState<BmkgStationStatusSummary | null>(null);
  const [bmkgApiParity, setBmkgApiParity] =
    useState<BmkgApiParitySummary | null>(null);
  const [bmkgRegionalStatus, setBmkgRegionalStatus] =
    useState<BmkgRegionalStatusSummary | null>(null);
  const [bmkgDashboardStatus, setBmkgDashboardStatus] =
    useState<BmkgDashboardStatusSummary | null>(null);
  const [bmkgGradeBasis, setBmkgGradeBasis] =
    useState<BmkgGradeBasisSummary | null>(null);
  const [bmkgStationPublicContext, setBmkgStationPublicContext] =
    useState<BmkgStationPublicContextSummary | null>(null);
  const [bmkgInstallationAudit, setBmkgInstallationAudit] =
    useState<BmkgInstallationAuditSummary | null>(null);
  const [bmkgNearClosure, setBmkgNearClosure] =
    useState<BmkgNearClosureSummary | null>(null);
  const [bmkgCertificateStatusTargeted, setBmkgCertificateStatusTargeted] =
    useState<BmkgCertificateStatusTargetedSummary | null>(null);
  const [bmkgPpidAccessRoute, setBmkgPpidAccessRoute] =
    useState<BmkgPpidAccessRouteSummary | null>(null);
  const [georgiaReportVerification, setGeorgiaReportVerification] =
    useState<GeorgiaReportVerificationSummary | null>(null);
  const [georgiaReportExportLadder, setGeorgiaReportExportLadder] =
    useState<GeorgiaReportExportLadderSummary | null>(null);
  const [georgiaVerificationPolicy, setGeorgiaVerificationPolicy] =
    useState<GeorgiaVerificationPolicySummary | null>(null);
  const [georgiaReportFrequency, setGeorgiaReportFrequency] =
    useState<GeorgiaReportFrequencySummary | null>(null);
  const [georgiaNetworkLaunch, setGeorgiaNetworkLaunch] =
    useState<GeorgiaNetworkLaunchSummary | null>(null);
  const [georgiaIndicatorEndpoint, setGeorgiaIndicatorEndpoint] =
    useState<GeorgiaIndicatorEndpointSummary | null>(null);
  const [monitorGrade, setMonitorGrade] = useState<MonitorGradeSummary | null>(null);
  const [mode, setMode] = useState<AirMode>("concentration");
  const [focusIso, setFocusIso] = useState("PNG");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/programs/air-monitoring/generated/air-monitoring-concentration-deepening.json").then((r) => {
        if (!r.ok) throw new Error(`deepening HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-adb-panel.json").then((r) => {
        if (!r.ok) throw new Error(`panel HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-metadata-readiness-audit-summary.json").then((r) => {
        if (!r.ok) throw new Error(`metadata readiness HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-openaq-station-metadata-summary.json").then((r) => {
        if (!r.ok) throw new Error(`station metadata HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-regulator-source-inventory-summary.json").then((r) => {
        if (!r.ok) throw new Error(`regulator source HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-regulator-station-extraction-summary.json").then((r) => {
        if (!r.ok) throw new Error(`regulator station HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-official-openaq-reconciliation-summary.json").then((r) => {
        if (!r.ok) throw new Error(`official OpenAQ reconciliation HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`official OpenAQ candidate review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`official OpenAQ candidate evidence HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json").then((r) => {
        if (!r.ok) throw new Error(`official OpenAQ candidate crosswalk source scan HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json").then((r) => {
        if (!r.ok) throw new Error(`official OpenAQ candidate public-feed source scan HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-one-signal-review-queue-summary.json").then((r) => {
        if (!r.ok) throw new Error(`one-signal review queue HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-monitor-grade-source-validation-scan-summary.json").then((r) => {
        if (!r.ok) throw new Error(`monitor grade source validation HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-monitor-grade-station-review-queue-summary.json").then((r) => {
        if (!r.ok) throw new Error(`monitor grade station review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-monitor-grade-station-method-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`monitor grade station method evidence HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-uzbekistan-station-current-method-scan-summary.json").then((r) => {
        if (!r.ok) throw new Error(`Uzbekistan station current method scan HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-uzbekistan-status-certification-source-scan-summary.json").then((r) => {
        if (!r.ok) throw new Error(`Uzbekistan status certification source scan HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json").then((r) => {
        if (!r.ok) throw new Error(`Uzbekistan blocker row follow-up HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/air-monitoring/generated/air-monitoring-monitor-grade-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`monitor grade HTTP ${r.status}`);
        return r.json();
      }),
    ])
      .then(([
        deepeningPayload,
        panelPayload,
        metadataPayload,
        stationMetadataPayload,
        regulatorSourcePayload,
        regulatorStationPayload,
        officialOpenAQPayload,
        officialOpenAQCandidatePayload,
        officialOpenAQCandidateEvidencePayload,
        candidateCrosswalkSourceScanPayload,
        candidatePublicFeedSourceScanPayload,
        oneSignalReviewQueuePayload,
        monitorGradeSourceValidationPayload,
        monitorGradeStationReviewPayload,
        monitorGradeStationMethodEvidencePayload,
        uzbekistanCurrentMethodPayload,
        uzbekistanStatusCertificationPayload,
        uzbekistanBlockerFollowupPayload,
        monitorGradePayload,
      ]) => {
        setDeepening(deepeningPayload);
        setPanel(panelPayload);
        setMetadataReadiness(metadataPayload);
        setStationMetadata(stationMetadataPayload);
        setRegulatorSource(regulatorSourcePayload);
        setRegulatorStation(regulatorStationPayload);
        setOfficialOpenAQ(officialOpenAQPayload);
        setOfficialOpenAQCandidate(officialOpenAQCandidatePayload);
        setOfficialOpenAQCandidateEvidence(officialOpenAQCandidateEvidencePayload);
        setCandidateCrosswalkSourceScan(candidateCrosswalkSourceScanPayload);
        setCandidatePublicFeedSourceScan(candidatePublicFeedSourceScanPayload);
        setOneSignalReviewQueue(oneSignalReviewQueuePayload);
        setMonitorGradeSourceValidation(monitorGradeSourceValidationPayload);
        setMonitorGradeStationReview(monitorGradeStationReviewPayload);
        setMonitorGradeStationMethodEvidence(monitorGradeStationMethodEvidencePayload);
        setUzbekistanCurrentMethod(uzbekistanCurrentMethodPayload);
        setUzbekistanStatusCertification(uzbekistanStatusCertificationPayload);
        setUzbekistanBlockerFollowup(uzbekistanBlockerFollowupPayload);
        setMonitorGrade(monitorGradePayload);
      })
      .catch((err) => setError(String(err)));
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-readiness-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius denominator readiness HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusReadiness(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-source-plan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius denominator source plan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusSourcePlan(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-acquisition-routes-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius denominator acquisition routes HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusAcquisition(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-file-manifest-prefreeze-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius denominator file manifest HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusFileManifest(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-download-feasibility-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius denominator download feasibility HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusDownloadFeasibility(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-acag-version-decision-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius ACAG version decision HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusAcagVersion(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-acag-coarse-checksums-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius ACAG coarse checksum HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusAcagChecksum(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-selection-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius GHSL population tile selection HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusGhslTileSelection(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-checksums-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius GHSL population tile checksums HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusGhslTileChecksum(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-tile-routing-correction-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius GHSL tile routing correction HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusGhslTileRouting(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-corrected-population-tile-custody-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius GHSL corrected tile custody HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusGhslCorrectedCustody(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-large-population-tile-custody-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius GHSL large tile custody HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusGhslLargeCustody(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-method-prefreeze-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius method prefreeze HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusMethodPrefreeze(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-radius-rule-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius radius-rule source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusRuleSourceScan(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-pm25-resolution-decision-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius PM2.5 resolution decision HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusPm25Resolution(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-join-dry-run-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius denominator join dry run HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusDenominatorJoin(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-country-unioned-catchment-dry-run-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius country union dry run HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusCountryUnion(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-radius-coverage-claim-gate-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`station-radius coverage claim gate HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationRadiusClaimGate(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-uzbekistan-endpoint-consistency-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Uzbekistan endpoint consistency HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setUzbekistanEndpointConsistency(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Uzbekistan blocker external context HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setUzbekistanExternalContext(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Uzbekistan Air Uzbekistan portal namespace HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setUzbekistanAirPortalNamespace(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Indonesia/Georgia row method source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setIndonesiaGeorgiaRowMethodSource(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-code-status-method-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Station-code status/method source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationCodeStatusMethod(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-grade-decision-ledger-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Station-grade decision ledger HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationGradeDecisionLedger(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-station-method-classification-audit-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Station-method classification audit HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setStationMethodClassification(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-operation-maintenance-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG operation/maintenance source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgOperationMaintenance(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-station-specific-status-audit-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG station-specific status audit HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgStationStatus(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-api-parity-status-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG API parity status HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgApiParity(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG regional status source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgRegionalStatus(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-dashboard-status-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG dashboard status source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgDashboardStatus(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-grade-basis-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG grade-basis source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgGradeBasis(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-station-public-context-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG station public-context source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgStationPublicContext(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-installation-audit-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG installation/audit source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgInstallationAudit(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-near-closure-ledger-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG near-closure ledger HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgNearClosure(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-certificate-status-targeted-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG certificate/status targeted source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgCertificateStatusTargeted(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-bmkg-ppid-access-route-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`BMKG PPID/PTSP access-route scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setBmkgPpidAccessRoute(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-georgia-report-verification-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Georgia report verification source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setGeorgiaReportVerification(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-georgia-report-export-ladder-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Georgia report export ladder HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setGeorgiaReportExportLadder(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-georgia-verification-policy-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Georgia verification policy HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setGeorgiaVerificationPolicy(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-georgia-report-frequency-matrix-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Georgia report frequency HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setGeorgiaReportFrequency(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Georgia station network launch source scan HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setGeorgiaNetworkLaunch(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  useEffect(() => {
    let isActive = true;

    fetch("/programs/air-monitoring/generated/air-monitoring-georgia-indicator-endpoint-mismatch-summary.json")
      .then((r) => {
        if (!r.ok) throw new Error(`Georgia indicator endpoint mismatch HTTP ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        if (isActive) setGeorgiaIndicatorEndpoint(payload);
      })
      .catch((err) => {
        if (isActive) setError((current) => current || String(err));
      });

    return () => {
      isActive = false;
    };
  }, []);

  const zeroRows = deepening?.part_a_concentration.rows ?? [];
  const residualRows =
    deepening?.part_b_confound.gdp_partial.top_positive_residuals_more_people_per_monitor_than_gdp_predicts ?? [];
  const allResidualRows = useMemo(() => {
    if (!deepening) return [];
    const allRows = deepening.part_b_confound.gdp_partial.all_residuals;
    if (allRows && allRows.length > 0) return allRows;
    const positives = deepening.part_b_confound.gdp_partial.top_positive_residuals_more_people_per_monitor_than_gdp_predicts;
    const negatives = deepening.part_b_confound.gdp_partial.top_negative_residuals_fewer_people_per_monitor_than_gdp_predicts;
    const map = new Map<string, ResidualRow>();
    [...positives, ...negatives].forEach((row) => map.set(row.iso3, row));
    return Array.from(map.values());
  }, [deepening]);

  const focusZero = deepening ? zeroByIso(zeroRows, focusIso) : undefined;
  const focusResidual = residualByIso(residualRows, focusIso) || residualByIso(allResidualRows, focusIso);
  const focusPanel = panel?.rows.find((row) => row.iso3 === focusIso);
  const focusOptions = mode === "residual" ? residualRows : zeroRows;

  useEffect(() => {
    if (!deepening) return;
    if (mode === "residual" && !residualRows.some((row) => row.iso3 === focusIso)) {
      setFocusIso(residualRows[0]?.iso3 ?? "AZE");
    }
    if (mode !== "residual" && !zeroRows.some((row) => row.iso3 === focusIso)) {
      setFocusIso("PNG");
    }
  }, [deepening, focusIso, mode, residualRows, zeroRows]);

  return (
    <article className="showcase-page air-showcase">
      <header className="showcase-hero air-hero">
        <div className="showcase-hero-copy">
          <p className="kicker kicker-crimson">ADB/ERDI-aligned showcase prototype</p>
          <h1 className="showcase-title showcase-title-wide">
            When OpenAQ Is Not the Regulator Map
          </h1>
          <p className="showcase-lede">
            The air-monitoring pass starts with a public-source observability
            problem: OpenAQ shows no public PM2.5 monitor for 13 ADB-region
            economies above the WHO annual guideline. It then checks the
            official-source trail: station metadata, regulator candidates, and
            official station tables show where OpenAQ visibility diverges from
            the public regulator map.
          </p>
          <div className="showcase-meta">
            <span>{deepening?.attestation_chain || "ai-first"}</span>
            <span>L2/L3 evidence sprint</span>
            <span>Observability screen, not a pollution ranking</span>
          </div>
        </div>
        <div className="showcase-hero-panel air-hero-panel" aria-label="Air-monitoring evidence summary">
          {deepening ? (
            <>
              <AirHeroConcentration data={deepening} />
              <div className="air-hero-stats">
                <div>
                  <span className="showcase-stat-value">
                    {deepening.part_a_concentration.zero_monitor_economy_count}
                  </span>
                  <span className="showcase-stat-label">zero-public-monitor economies above the WHO PM2.5 guideline</span>
                </div>
                <div>
                  <span className="showcase-stat-value">
                    {pct(deepening.part_a_concentration.png_plus_timor_share)}
                  </span>
                  <span className="showcase-stat-label">of that population is in Papua New Guinea and Timor-Leste</span>
                </div>
              </div>
            </>
          ) : (
            <p className="showcase-loading">{error || "Loading air-monitoring evidence..."}</p>
          )}
        </div>
      </header>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">Measurement problem</p>
          <h2>The regional total hides the unit that matters.</h2>
          <p>
            A dashboard can say 13 economies have no public PM2.5 monitor
            visible in OpenAQ while exposure exceeds the WHO annual guideline.
            That is a useful starting point, but it is not yet a planning
            statement. Papua New Guinea alone carries nearly three quarters of
            the population in that zero-monitor group, while most remaining
            economies are small island states.
          </p>
        </div>
        <div className="showcase-note">
          <p>
            <strong>Data gap.</strong> OpenAQ is a public monitor-visibility
            source, not a complete regulatory inventory. WDI PM2.5 is a
            modeled exposure series. The report therefore treats the result as
            a public observability screen, not as proof that no monitor exists
            on the ground.
          </p>
        </div>
      </section>

      <AirMetadataReadinessPanel summary={metadataReadiness} />

      <AirStationMetadataPanel summary={stationMetadata} />

      <AirStationRadiusReadinessPanel summary={stationRadiusReadiness} />

      <AirStationRadiusSourcePlanPanel summary={stationRadiusSourcePlan} />

      <AirStationRadiusAcquisitionPanel summary={stationRadiusAcquisition} />

      <AirStationRadiusFileManifestPanel summary={stationRadiusFileManifest} />

      <AirStationRadiusDownloadFeasibilityPanel summary={stationRadiusDownloadFeasibility} />

      <AirStationRadiusAcagVersionPanel summary={stationRadiusAcagVersion} />

      <AirStationRadiusAcagChecksumPanel summary={stationRadiusAcagChecksum} />

      <AirStationRadiusGhslTileSelectionPanel summary={stationRadiusGhslTileSelection} />

      <AirStationRadiusGhslTileChecksumPanel summary={stationRadiusGhslTileChecksum} />

      <AirStationRadiusGhslTileRoutingPanel summary={stationRadiusGhslTileRouting} />

      <AirStationRadiusGhslCorrectedCustodyPanel summary={stationRadiusGhslCorrectedCustody} />

      <AirStationRadiusGhslLargeCustodyPanel summary={stationRadiusGhslLargeCustody} />

      <AirStationRadiusMethodPrefreezePanel summary={stationRadiusMethodPrefreeze} />

      <AirStationRadiusRuleSourcePanel summary={stationRadiusRuleSourceScan} />

      <AirStationRadiusPm25ResolutionPanel summary={stationRadiusPm25Resolution} />

      <AirStationRadiusDenominatorJoinPanel summary={stationRadiusDenominatorJoin} />

      <AirStationRadiusCountryUnionPanel summary={stationRadiusCountryUnion} />

      <AirStationRadiusClaimGatePanel summary={stationRadiusClaimGate} />

      <AirRegulatorSourcePanel summary={regulatorSource} />

      <AirRegulatorStationPanel summary={regulatorStation} />

      <AirOfficialOpenAQPanel summary={officialOpenAQ} />

      <AirOfficialOpenAQCandidatePanel summary={officialOpenAQCandidate} />

      <AirOfficialOpenAQCandidateEvidencePanel summary={officialOpenAQCandidateEvidence} />

      <AirCandidateCrosswalkSourceScanPanel summary={candidateCrosswalkSourceScan} />

      <AirCandidatePublicFeedSourceScanPanel summary={candidatePublicFeedSourceScan} />

      <AirOneSignalReviewQueuePanel summary={oneSignalReviewQueue} />

      <AirMonitorGradeSourceValidationPanel summary={monitorGradeSourceValidation} />

      <AirMonitorGradeStationReviewPanel summary={monitorGradeStationReview} />

      <AirMonitorGradeStationMethodEvidencePanel summary={monitorGradeStationMethodEvidence} />

      <AirUzbekistanCurrentMethodPanel summary={uzbekistanCurrentMethod} />

      <AirUzbekistanStatusCertificationPanel summary={uzbekistanStatusCertification} />

      <AirUzbekistanBlockerFollowupPanel summary={uzbekistanBlockerFollowup} />

      <AirUzbekistanEndpointConsistencyPanel summary={uzbekistanEndpointConsistency} />

      <AirUzbekistanExternalContextPanel summary={uzbekistanExternalContext} />

      <AirUzbekistanAirPortalNamespacePanel summary={uzbekistanAirPortalNamespace} />

      <AirIndonesiaGeorgiaRowMethodSourcePanel summary={indonesiaGeorgiaRowMethodSource} />

      <AirStationCodeStatusMethodPanel summary={stationCodeStatusMethod} />

      <AirStationGradeDecisionLedgerPanel summary={stationGradeDecisionLedger} />

      <AirStationMethodClassificationPanel summary={stationMethodClassification} />

      <AirBmkgOperationMaintenancePanel summary={bmkgOperationMaintenance} />

      <AirBmkgStationStatusPanel summary={bmkgStationStatus} />

      <AirBmkgApiParityPanel summary={bmkgApiParity} />

      <AirBmkgRegionalStatusPanel summary={bmkgRegionalStatus} />

      <AirBmkgDashboardStatusPanel summary={bmkgDashboardStatus} />

      <AirBmkgGradeBasisPanel summary={bmkgGradeBasis} />

      <AirBmkgStationPublicContextPanel summary={bmkgStationPublicContext} />

      <AirBmkgInstallationAuditPanel summary={bmkgInstallationAudit} />

      <AirBmkgNearClosurePanel summary={bmkgNearClosure} />

      <AirBmkgCertificateStatusTargetedPanel summary={bmkgCertificateStatusTargeted} />

      <AirBmkgPpidAccessRoutePanel summary={bmkgPpidAccessRoute} />

      <AirGeorgiaReportVerificationPanel summary={georgiaReportVerification} />

      <AirGeorgiaReportExportLadderPanel summary={georgiaReportExportLadder} />

      <AirGeorgiaVerificationPolicyPanel summary={georgiaVerificationPolicy} />

      <AirGeorgiaReportFrequencyPanel summary={georgiaReportFrequency} />

      <AirGeorgiaNetworkLaunchPanel summary={georgiaNetworkLaunch} />

      <AirGeorgiaIndicatorEndpointPanel summary={georgiaIndicatorEndpoint} />

      <AirMonitorGradePanel summary={monitorGrade} />

      <section className="showcase-explorer">
        <div className="showcase-explorer-head">
          <div>
            <p className="kicker kicker-crimson">Interactive evidence view</p>
            <h2>Split the headline before using it.</h2>
            <p>
              The first view decomposes the zero-monitor population. The second
              view adds GDP per capita and asks which monitored economies have
              more people per public monitor than their income level predicts.
              The third view returns to the original observability panel.
            </p>
          </div>
          <div className="showcase-controls">
            {MODES.map((option) => (
              <button
                key={option.id}
                className={option.id === mode ? "active" : ""}
                onClick={() => setMode(option.id)}
                type="button"
              >
                {option.label}
              </button>
            ))}
            <label>
              Focus economy
              <select value={focusIso} onChange={(event) => setFocusIso(event.target.value)}>
                {focusOptions.map((row) => (
                  <option key={row.iso3} value={row.iso3}>
                    {row.country}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>

        <div className="air-evidence-grid">
          <div className="air-main-chart">
            {!deepening || !panel ? (
              <p className="showcase-loading">{error || "Loading chart data..."}</p>
            ) : mode === "concentration" ? (
              <ZeroMonitorChart rows={zeroRows} focusIso={focusIso} />
            ) : mode === "residual" ? (
              <GdpResidualChart
                rows={allResidualRows}
                positiveRows={residualRows}
                focusIso={focusIso}
                intercept={deepening.part_b_confound.gdp_partial.intercept}
                slope={deepening.part_b_confound.gdp_partial.slope}
              />
            ) : (
              <ExposureMonitorChart rows={panel.rows} focusIso={focusIso} />
            )}
          </div>
          <div className="air-side-panel">
            {mode === "concentration" ? (
              <ZeroMonitorPanel row={focusZero} deepening={deepening} />
            ) : mode === "residual" ? (
              <ResidualPanel row={focusResidual} deepening={deepening} />
            ) : (
              <ExposurePanel row={focusPanel} panel={panel} />
            )}
          </div>
        </div>
      </section>

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-blue">What changed after deepening</p>
          <h2>The stronger question is not “who has the worst air.”</h2>
          <p>
            The upgraded sprint changes the frame. The zero-monitor total is a
            Papua New Guinea and Timor-Leste concentration story. Among
            monitored economies, GDP per capita explains a substantial part of
            public monitor density: the Spearman correlation between the
            gap-score and log GDP per capita is{" "}
            {deepening
              ? deepening.part_b_confound.rank_correlations_descriptive_only.spearman_gap_score_vs_log10_gdp_pc_withmon.toFixed(3)
              : "loading"}
            . The residual view is therefore a source-improvement list, not a
            league table.
          </p>
        </div>
        <div className="showcase-note">
          <p>
            <strong>Non-claim.</strong> The GDP residual is descriptive. It
            does not identify why a monitor network is thin, whether a monitor
            is regulatory grade, or how city-level exposure differs from the
            national WDI value.
          </p>
        </div>
      </section>

      <ShowcaseQualityPanel reportId={6} />

      <section className="showcase-section showcase-two-col">
        <div className="showcase-section-copy">
          <p className="kicker kicker-crimson">Operational use</p>
          <h2>Use it as a monitor-inventory QA list.</h2>
          <p>
            For a country team, regulator, or statistics office, this screen
            can prioritize where to audit public monitor inventories, classify
            monitor grade, and compare OpenAQ visibility with national
            regulator records. The next statistical upgrade is subnational:
            monitor catchments, gridded PM2.5, urban population exposure, and
            station metadata freshness.
          </p>
        </div>
        <div className="showcase-links">
          <a href="/programs/air-monitoring/generated/air-monitoring-concentration-deepening.json" download>
            Deepening JSON
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-concentration-deepening.csv" download>
            Zero-monitor CSV
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-adb-panel.json" download>
            Source panel JSON
          </a>
          <a href="/programs/air-monitoring/metadata-readiness-audit.md" download>
            Metadata audit note
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-metadata-readiness-audit-summary.json" download>
            Metadata audit JSON
          </a>
          <a href="/programs/air-monitoring/station-metadata-source-access.md" download>
            Station metadata note
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-openaq-station-metadata-summary.json" download>
            Station metadata JSON
          </a>
          <a href="/programs/air-monitoring/generated/air-monitoring-openaq-station-metadata.csv" download>
            Station metadata CSV
          </a>
          <Link to="/air-monitoring?view=evidence">Program evidence</Link>
        </div>
      </section>
    </article>
  );
}

function AirMetadataReadinessPanel({ summary }: { summary: MetadataReadinessSummary | null }) {
  const scope = summary?.readiness_scope;
  const gateRows = summary?.evidence_gate_counts ?? [];
  const queueRows = summary?.top_upgrade_queue_rows.slice(0, 10) ?? [];
  const classCounts = summary?.upgrade_queue_class_counts ?? [];

  return (
    <section className="showcase-section air-metadata-section" aria-label="Air-monitoring metadata-readiness audit">
      <div className="air-metadata-head">
        <div>
          <p className="kicker kicker-crimson">Metadata-readiness wall</p>
          <h2>The next claim is blocked at station metadata.</h2>
          <p>
            The audit reads the committed country panel and GDP-confound
            deepening, then asks whether the evidence is ready for
            station-radius, monitor-grade, station-vintage, or regulatory
            inventory language. The answer is not yet: the public route keeps
            the blocked station-level gates visible before the observability
            claim is widened.
          </p>
        </div>
        <div className="air-metadata-nonclaim">
          <strong>Non-claim</strong>
          <p>
            OpenAQ-visible zero is not proof that no monitor exists on the
            ground. It means no public OpenAQ PM2.5 location is present in the
            committed panel until a national regulator inventory is checked.
          </p>
        </div>
      </div>

      {summary && scope ? (
        <>
          <div className="air-metadata-stat-grid">
            <div>
              <span>Country-panel rows</span>
              <strong>{formatNumber(scope.panel_rows)}</strong>
              <em>monitor count and PM2.5 exposure available</em>
            </div>
            <div>
              <span>Upgrade-queue rows</span>
              <strong>{formatNumber(scope.unique_upgrade_queue_rows)}</strong>
              <em>baseline, residual, or zero-monitor evidence need</em>
            </div>
            <div>
              <span>Station-coordinate rows</span>
              <strong>{formatNumber(scope.station_coordinate_rows_available)}</strong>
              <em>required for radius or catchment claims</em>
            </div>
            <div>
              <span>Station-radius ready</span>
              <strong>{scope.station_radius_analysis_ready ? "yes" : "no"}</strong>
              <em>station-level cache files: {formatNumber(scope.station_level_cache_files)}</em>
            </div>
          </div>

          <div className="air-metadata-gate-grid">
            {gateRows.map((gate) => (
              <article key={gate.gate} className={`air-metadata-gate air-metadata-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-metadata-queue-layout">
            <div className="air-metadata-class-list">
              <h3>Queue classes</h3>
              {classCounts.map((item) => (
                <div key={item.name}>
                  <span>{sentenceCaseStatus(item.name)}</span>
                  <strong>{formatNumber(item.rows)}</strong>
                </div>
              ))}
            </div>

            <div className="air-metadata-queue">
              {queueRows.map((row) => (
                <article key={row.iso3} className="air-metadata-queue-card">
                  <div>
                    <span>{row.iso3}</span>
                    <strong>{row.country}</strong>
                  </div>
                  <dl>
                    <div>
                      <dt>PM2.5 locations</dt>
                      <dd>{formatNumber(row.pm25_locations)}</dd>
                    </div>
                    <div>
                      <dt>Gap score</dt>
                      <dd>{formatNumber(row.pm25_observability_gap_score)}</dd>
                    </div>
                    <div>
                      <dt>GDP residual</dt>
                      <dd>{signed(row.log10_people_per_monitor_residual)}</dd>
                    </div>
                  </dl>
                  <p>{row.next_evidence_needed}</p>
                </article>
              ))}
            </div>
          </div>

          <div className="air-metadata-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/metadata-readiness-audit.md" download>
              Audit note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-metadata-readiness-audit-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-metadata-readiness-audit.csv" download>
              Audit CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading metadata-readiness audit...</p>
      )}
    </section>
  );
}

function AirStationMetadataPanel({ summary }: { summary: StationMetadataSummary | null }) {
  const counts = summary?.coverage_counts;
  const countryRows = summary?.country_rows ?? [];
  const stationRows = summary?.station_rows ?? [];
  const countriesWithStations = countryRows
    .filter((row) => row.openaq_pm25_locations_fetched > 0)
    .sort((a, b) => b.openaq_pm25_locations_fetched - a.openaq_pm25_locations_fetched);
  const zeroCountries = countryRows.filter((row) => row.openaq_pm25_locations_fetched === 0);

  return (
    <section className="showcase-section air-station-section" aria-label="OpenAQ station metadata source access">
      <div className="air-station-head">
        <div>
          <p className="kicker kicker-blue">Station-source access</p>
          <h2>OpenAQ returns station coordinates, but not the final coverage claim.</h2>
          <p>
            The source pass queries OpenAQ v3 for the same 24 upgrade-queue
            economies. It turns the station-metadata wall into a map-ready
            coordinate extract while keeping monitor-grade, regulator inventory,
            and station-radius coverage outside the claim.
          </p>
        </div>
        <div className="air-station-nonclaim">
          <strong>Still not proven</strong>
          <p>
            A zero in OpenAQ is still only OpenAQ-visible zero. Owner/provider
            fields are provenance, not monitor-grade validation.
            {counts
              ? ` ${formatNumber(counts.excluded_coordinate_qc_rows)} rows were also excluded before mapping because coordinates fell outside broad target-country bounds.`
              : " Coordinate plausibility checks are applied before mapping."}
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-station-stat-grid">
            <div>
              <span>OpenAQ PM2.5 rows</span>
              <strong>{formatNumber(counts.openaq_pm25_location_rows)}</strong>
              <em>{formatNumber(counts.station_coordinate_rows)} have coordinates</em>
            </div>
            <div>
              <span>Economies with rows</span>
              <strong>{formatNumber(counts.economies_with_openaq_pm25_locations)}</strong>
              <em>of {formatNumber(counts.economies_targeted)} upgrade-queue economies</em>
            </div>
            <div>
              <span>Still zero in OpenAQ</span>
              <strong>{formatNumber(counts.economies_with_zero_openaq_pm25_locations)}</strong>
              <em>requires regulator inventory cross-check</em>
            </div>
            <div>
              <span>Station-radius ready</span>
              <strong>{counts.station_radius_analysis_ready ? "yes" : "no"}</strong>
              <em>monitor-grade rows: {formatNumber(counts.monitor_grade_rows)}</em>
            </div>
            <div>
              <span>Coordinate QC exclusions</span>
              <strong>{formatNumber(counts.excluded_coordinate_qc_rows)}</strong>
              <em>outside broad target-country bounds</em>
            </div>
          </div>

          <div className="air-station-layout">
            <StationCoordinateMap rows={stationRows} countryRows={countryRows} />
            <div className="air-station-country-list">
              <h3>Where OpenAQ returned rows</h3>
              {countriesWithStations.map((row) => (
                <div key={row.iso3} className="air-station-country-row">
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.openaq_pm25_locations_fetched)}</b>
                  <em>{formatNumber(row.first_seen_rows)} first-seen</em>
                </div>
              ))}
            </div>
          </div>

          <div className="air-station-zero-strip">
            <span>Zero OpenAQ PM2.5 rows after v3 query</span>
            <div>
              {zeroCountries.map((row) => (
                <b key={row.iso3}>{row.iso3}</b>
              ))}
            </div>
          </div>

          <div className="air-station-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-station-gate air-station-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-station-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-metadata-source-access.md" download>
              Source-access note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-openaq-station-metadata-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-openaq-station-metadata.csv" download>
              Station CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading OpenAQ station metadata...</p>
      )}
    </section>
  );
}

function AirStationRadiusReadinessPanel({ summary }: { summary: StationRadiusReadinessSummary | null }) {
  const counts = summary?.coverage_counts;
  const lanes = summary?.readiness_lane_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.top_coordinate_ready_rows ?? [];
  const laneTotal = Math.max(1, lanes.reduce((sum, row) => sum + row.economies, 0));
  const maxCoordinateRows = Math.max(
    1,
    ...rows.map((row) => row.openaq_coordinate_rows + row.official_coordinate_rows),
  );

  return (
    <section className="showcase-section air-radius-readiness-section" aria-label="Station-radius denominator readiness wall">
      <div className="air-radius-readiness-head">
        <div>
          <p className="kicker kicker-crimson">Station-radius readiness wall</p>
          <h2>The map is blocked by denominators, not dots.</h2>
          <p>
            The station map now has coordinates from OpenAQ and official public
            sources. This pass asks the harder planning question: can those
            points be turned into catchment population or PM2.5 exposure? The
            answer is still no because denominator rasters, validated joins,
            complete grade rows, and radius rules are not in the committed
            evidence package.
          </p>
        </div>
        <div className="air-radius-readiness-callout">
          <span>Radius-ready economies</span>
          <strong>{formatNumber(counts?.station_radius_ready_economies ?? 0)}</strong>
          <p>Coordinates are input evidence. They are not a coverage surface.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-radius-readiness-stat-grid">
            <div>
              <span>OpenAQ coordinate rows</span>
              <strong>{formatNumber(counts.openaq_coordinate_rows)}</strong>
              <em>{formatNumber(counts.economies_with_openaq_coordinate_rows)} economies</em>
            </div>
            <div>
              <span>Official coordinate rows</span>
              <strong>{formatNumber(counts.official_coordinate_rows)}</strong>
              <em>{formatNumber(counts.economies_with_official_coordinate_rows)} economies</em>
            </div>
            <div>
              <span>Candidate proximity rows</span>
              <strong>{formatNumber(counts.near_plus_name_candidate_rows + counts.near_only_candidate_rows)}</strong>
              <em>screening signals, not joins</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_join_rows)}</strong>
              <em>required before de-duplication</em>
            </div>
            <div>
              <span>Population denominator files</span>
              <strong>{formatNumber(counts.gridded_population_denominator_files)}</strong>
              <em>no radius intersections yet</em>
            </div>
            <div>
              <span>PM2.5 denominator files</span>
              <strong>{formatNumber(counts.gridded_pm25_denominator_files)}</strong>
              <em>no exposure surface yet</em>
            </div>
          </div>

          <div className="air-radius-readiness-story-grid">
            <div className="air-radius-readiness-lane-grid" aria-label="Station-radius readiness lanes">
              {lanes.map((lane) => (
                <article key={lane.lane} className={`air-radius-readiness-lane air-radius-readiness-lane-${lane.lane}`}>
                  <div>
                    <span>{sentenceCaseStatus(lane.lane)}</span>
                    <strong>{formatNumber(lane.economies)} economies</strong>
                  </div>
                  <div className="air-radius-readiness-track">
                    <i style={{ width: `${Math.max(6, (lane.economies / laneTotal) * 100)}%` }} />
                  </div>
                </article>
              ))}
            </div>

            <div className="air-radius-readiness-flow" aria-label="Station-radius prerequisite flow">
              {gates.map((gate, index) => (
                <article key={gate.gate} className={`air-radius-readiness-rung air-radius-readiness-rung-${gateTone(gate.status)}`}>
                  <b>{index + 1}</b>
                  <div>
                    <strong>{gate.gate}</strong>
                    <span>{sentenceCaseStatus(gate.status)} / {formatNumber(gate.rows)} rows</span>
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div className="air-radius-readiness-country-grid" aria-label="Coordinate-heavy economies still blocked from station-radius analysis">
            {rows.map((row) => {
              const coordinateRows = row.openaq_coordinate_rows + row.official_coordinate_rows;
              const candidateRows = row.near_plus_name_candidate_rows + row.near_only_candidate_rows;
              return (
                <article key={row.iso3} className={`air-radius-readiness-country air-radius-readiness-country-${row.readiness_lane}`}>
                  <div>
                    <span>{row.iso3}</span>
                    <strong>{row.country}</strong>
                    <b>{formatNumber(coordinateRows)} coord.</b>
                  </div>
                  <div className="air-radius-readiness-meter">
                    <i style={{ width: `${Math.max(4, (coordinateRows / maxCoordinateRows) * 100)}%` }} />
                  </div>
                  <dl>
                    <div>
                      <dt>OpenAQ</dt>
                      <dd>{formatNumber(row.openaq_coordinate_rows)}</dd>
                    </div>
                    <div>
                      <dt>Official</dt>
                      <dd>{formatNumber(row.official_coordinate_rows)}</dd>
                    </div>
                    <div>
                      <dt>Candidates</dt>
                      <dd>{formatNumber(candidateRows)}</dd>
                    </div>
                    <div>
                      <dt>Ready</dt>
                      <dd>{row.station_radius_analysis_ready ? "yes" : "no"}</dd>
                    </div>
                  </dl>
                  <p>{row.reader_use}</p>
                </article>
              );
            })}
          </div>

          <div className="air-radius-readiness-gate-grid" aria-label="Station-radius evidence gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-radius-readiness-gate air-radius-readiness-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-radius-readiness-nonclaim">{summary.non_claim}</p>

          <div className="air-radius-readiness-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-denominator-readiness.md" download>
              Download readiness note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-readiness-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-readiness.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius denominator readiness wall...</p>
      )}
    </section>
  );
}

function AirStationRadiusSourcePlanPanel({ summary }: { summary: StationRadiusSourcePlanSummary | null }) {
  const counts = summary?.coverage_counts;
  const records = summary?.source_records ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const method = summary?.proposed_method;
  const decisionRows = summary?.source_decision_counts ?? [];
  const maxDecisionSources = Math.max(1, ...decisionRows.map((row) => row.sources));
  const termCount = (value: string | undefined) => (value ? value.split("||").filter(Boolean).length : 0);
  const cardTone = (record: StationRadiusSourcePlanRecord) => {
    if (record.source_level_candidate_ready) return "ready";
    if (record.source_role === "boundary_reference" || record.source_decision.startsWith("context_only")) return "context";
    return "blocked";
  };

  return (
    <section className="showcase-section air-radius-source-plan-section" aria-label="Station-radius denominator source plan">
      <div className="air-radius-source-plan-head">
        <div>
          <p className="kicker kicker-crimson">Denominator source plan</p>
          <h2>The source route exists; the map still does not.</h2>
          <p>
            The next upgrade is no longer a vague request for better data.
            This scan verifies the public source pages that could support a
            future catchment map, then keeps the hard gates visible: no
            denominator files are pinned, no raster intersection method is
            frozen, and the station join and grade ledgers still have zero
            closure rows.
          </p>
        </div>
        <div className="air-radius-source-plan-callout">
          <span>Pinned denominator grids</span>
          <strong>
            {formatNumber((counts?.committed_population_raster_files ?? 0) + (counts?.committed_pm25_grid_files ?? 0))}
          </strong>
          <p>Source pages are enough to plan. They are not enough to map.</p>
        </div>
      </div>

      {summary && counts && method ? (
        <>
          <div className="air-radius-source-plan-stat-grid">
            <div className="air-radius-source-plan-stat">
              <span>Source pages retrieved</span>
              <strong>{formatNumber(counts.source_urls_retrieved)} / {formatNumber(counts.seeded_source_urls)}</strong>
              <em>public pages fetched and hashed</em>
            </div>
            <div className="air-radius-source-plan-stat">
              <span>Candidate denominators</span>
              <strong>{formatNumber(counts.source_level_candidate_denominator_sources)}</strong>
              <em>source-level ready, files not pinned</em>
            </div>
            <div className="air-radius-source-plan-stat">
              <span>Population candidates</span>
              <strong>{formatNumber(counts.population_candidate_sources)}</strong>
              <em>GHSL baseline, WorldPop sensitivity</em>
            </div>
            <div className="air-radius-source-plan-stat">
              <span>PM2.5 candidates</span>
              <strong>{formatNumber(counts.pm25_candidate_sources)}</strong>
              <em>ACAG current plus algorithm sensitivity</em>
            </div>
            <div className="air-radius-source-plan-stat">
              <span>Context-only sources</span>
              <strong>{formatNumber(counts.context_only_sources)}</strong>
              <em>WHO validation/context, not radius denominators</em>
            </div>
            <div className="air-radius-source-plan-stat">
              <span>Radius-ready economies</span>
              <strong>{formatNumber(counts.station_radius_ready_economies)}</strong>
              <em>join and grade ledgers still block the map</em>
            </div>
          </div>

          <div className="air-radius-source-plan-source-grid" aria-label="Public denominator source decisions">
            {records.map((record) => (
              <article
                key={record.source_key}
                className={`air-radius-source-plan-source air-radius-source-plan-source-${cardTone(record)}`}
              >
                <div>
                  <span>{record.source_family} / {sentenceCaseStatus(record.source_role)}</span>
                  <strong>{record.source_name}</strong>
                  <b>{sentenceCaseStatus(record.source_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Grid terms</dt>
                    <dd>{formatNumber(termCount(record.matched_gridded_terms))}</dd>
                  </div>
                  <div>
                    <dt>License</dt>
                    <dd>{formatNumber(termCount(record.matched_license_terms))}</dd>
                  </div>
                  <div>
                    <dt>Vintage</dt>
                    <dd>{formatNumber(termCount(record.matched_vintage_terms))}</dd>
                  </div>
                  <div>
                    <dt>File</dt>
                    <dd>{record.raster_or_grid_file_committed ? "pinned" : "none"}</dd>
                  </div>
                </dl>
                <p>{record.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-radius-source-plan-method-grid" aria-label="Draft station-radius method spine">
            <article className="air-radius-source-plan-method">
              <span>Population primary</span>
              <strong>GHSL first</strong>
              <p>{method.population_primary}</p>
            </article>
            <article className="air-radius-source-plan-method">
              <span>Population sensitivity</span>
              <strong>WorldPop check</strong>
              <p>{method.population_sensitivity}</p>
            </article>
            <article className="air-radius-source-plan-method">
              <span>PM2.5 primary</span>
              <strong>ACAG V6</strong>
              <p>{method.pm25_primary}</p>
            </article>
            <article className="air-radius-source-plan-method">
              <span>Radius sweep</span>
              <strong>{method.radius_sweep_km.join(" / ")} km</strong>
              <p>Draft only. Freeze the sweep in pre-registration before any catchment computation.</p>
            </article>
            <article className="air-radius-source-plan-method">
              <span>Join and grade rule</span>
              <strong>Two layers</strong>
              <p>{method.grade_rule_draft}</p>
            </article>
          </div>

          <div className="air-radius-source-plan-decision-grid" aria-label="Source-plan decision distribution">
            {decisionRows.map((row) => (
              <article key={row.decision}>
                <div>
                  <span>{sentenceCaseStatus(row.decision)}</span>
                  <strong>{formatNumber(row.sources)} source{row.sources === 1 ? "" : "s"}</strong>
                </div>
                <div className="air-radius-source-plan-track">
                  <i style={{ width: `${Math.max(7, (row.sources / maxDecisionSources) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-radius-source-plan-gate-grid" aria-label="Station-radius source-plan gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-radius-source-plan-gate air-radius-source-plan-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-radius-source-plan-nonclaim">{summary.non_claim}</p>

          <div className="air-radius-source-plan-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-denominator-source-plan.md" download>
              Download source plan
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-source-plan-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-source-plan.csv" download>
              Download source CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius denominator source plan...</p>
      )}
    </section>
  );
}

function AirStationRadiusAcquisitionPanel({ summary }: { summary: StationRadiusAcquisitionSummary | null }) {
  const counts = summary?.coverage_counts;
  const records = summary?.route_records ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const decisions = summary?.route_decision_counts ?? [];
  const maxDecisionSources = Math.max(1, ...decisions.map((row) => row.sources));
  const pinnedFiles = (counts?.committed_population_raster_files ?? 0) + (counts?.committed_pm25_grid_files ?? 0);
  const routeTone = (record: StationRadiusAcquisitionRecord) => {
    if (record.source_level_candidate_ready) return "candidate";
    if (record.route_decision.startsWith("context")) return "context";
    if (record.route_decision.startsWith("boundary")) return "boundary";
    return "blocked";
  };
  const firstRoute = (record: StationRadiusAcquisitionRecord) => {
    const first = record.route_examples.split(" || ")[0] || "No route example captured";
    const [label, href] = first.split(" => ");
    return { label: label || first, href: href || "" };
  };

  return (
    <section className="showcase-section air-radius-acquisition-section" aria-label="Station-radius denominator acquisition routes">
      <div className="air-radius-acquisition-head">
        <div>
          <p className="kicker kicker-blue">Acquisition route scan</p>
          <h2>The doors are visible; the files are still outside the package.</h2>
          <p>
            The source-plan wall says which public sources can support a future
            denominator. This pass checks whether those pages expose actual
            download, listing, Box, AWS, or context routes, then keeps the
            exact-file and checksum gates closed.
          </p>
        </div>
        <div className="air-radius-acquisition-callout">
          <span>Candidate sources with routes</span>
          <strong>
            {formatNumber(counts?.candidate_sources_with_visible_routes ?? 0)}
            <small> / {formatNumber(counts?.candidate_denominator_sources ?? 0)}</small>
          </strong>
          <p>Route visibility is progress. It is not a denominator file.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-radius-acquisition-stat-grid">
            <div>
              <span>Source pages retrieved</span>
              <strong>{formatNumber(counts.source_pages_retrieved)} / {formatNumber(counts.source_records)}</strong>
              <em>route scan inputs</em>
            </div>
            <div>
              <span>Visible route links</span>
              <strong>{formatNumber(counts.visible_route_links)}</strong>
              <em>download, listing, cloud, or context links</em>
            </div>
            <div>
              <span>Cloud/listing routes</span>
              <strong>{formatNumber(counts.cloud_or_listing_route_links)}</strong>
              <em>directories, Box, AWS, listings</em>
            </div>
            <div>
              <span>HEAD probes ok</span>
              <strong>{formatNumber(counts.route_probe_ok)} / {formatNumber(counts.route_probe_attempts)}</strong>
              <em>light route checks, no file downloads</em>
            </div>
            <div>
              <span>Pinned denominator files</span>
              <strong>{formatNumber(pinnedFiles)}</strong>
              <em>no raster or grid checksum yet</em>
            </div>
            <div>
              <span>Radius-ready economies</span>
              <strong>{formatNumber(counts.station_radius_ready_economies)}</strong>
              <em>join and grade gates still block</em>
            </div>
          </div>

          <div className="air-radius-acquisition-route-grid" aria-label="Acquisition route records">
            {records.map((record) => {
              const example = firstRoute(record);
              return (
                <article
                  key={record.source_key}
                  className={`air-radius-acquisition-route air-radius-acquisition-route-${routeTone(record)}`}
                >
                  <div>
                    <span>{record.source_family} / {sentenceCaseStatus(record.source_role)}</span>
                    <strong>{record.source_name}</strong>
                    <b>{sentenceCaseStatus(record.route_decision)}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Routes</dt>
                      <dd>{formatNumber(record.route_links_total)}</dd>
                    </div>
                    <div>
                      <dt>Cloud/listing</dt>
                      <dd>{formatNumber(record.cloud_or_listing_route_links)}</dd>
                    </div>
                    <div>
                      <dt>Direct/context</dt>
                      <dd>{formatNumber(record.direct_file_route_links + record.context_route_links)}</dd>
                    </div>
                    <div>
                      <dt>Probe ok</dt>
                      <dd>{formatNumber(record.route_probe_ok)} / {formatNumber(record.route_probe_attempts)}</dd>
                    </div>
                  </dl>
                  <p>{record.reader_use}</p>
                  <div className="air-radius-acquisition-example">
                    <span>First route example</span>
                    {example.href ? (
                      <a href={example.href}>{example.label}</a>
                    ) : (
                      <em>{example.label}</em>
                    )}
                  </div>
                  <p className="air-radius-acquisition-gap">{record.blocking_gap}</p>
                </article>
              );
            })}
          </div>

          <div className="air-radius-acquisition-decision-grid" aria-label="Acquisition route decisions">
            {decisions.map((row) => (
              <article key={row.decision}>
                <div>
                  <span>{sentenceCaseStatus(row.decision)}</span>
                  <strong>{formatNumber(row.sources)} source{row.sources === 1 ? "" : "s"}</strong>
                </div>
                <div className="air-radius-acquisition-track">
                  <i style={{ width: `${Math.max(7, (row.sources / maxDecisionSources) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-radius-acquisition-gate-grid" aria-label="Acquisition route gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-radius-acquisition-gate air-radius-acquisition-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-radius-acquisition-nonclaim">{summary.non_claim}</p>

          <div className="air-radius-acquisition-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-denominator-acquisition-routes.md" download>
              Download route scan
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-acquisition-routes-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-acquisition-routes.csv" download>
              Download route CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius denominator acquisition routes...</p>
      )}
    </section>
  );
}

function AirStationRadiusFileManifestPanel({ summary }: { summary: StationRadiusFileManifestSummary | null }) {
  const counts = summary?.coverage_counts;
  const records = summary?.manifest_records ?? [];
  const statusRows = summary?.manifest_status_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const maxStatusRecords = Math.max(1, ...statusRows.map((row) => row.records));
  const downloaded = (counts?.denominator_files_downloaded ?? 0) + (counts?.denominator_files_sha256_checksummed ?? 0);
  const formatBytes = (value: string | number) => {
    const bytes = Number(value || 0);
    if (!Number.isFinite(bytes) || bytes <= 0) return "not listed";
    if (bytes >= 1_000_000_000) return `${(bytes / 1_000_000_000).toFixed(1)} GB`;
    if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
    return `${formatNumber(bytes)} B`;
  };
  const recordTone = (record: StationRadiusFileManifestRecord) => {
    if (record.manifest_status.includes("shared_folder")) return "unresolved";
    if (record.denominator_type === "population") return "population";
    if (record.denominator_type === "pm25") return "pm25";
    return "context";
  };

  return (
    <section className="showcase-section air-radius-file-section" aria-label="Station-radius denominator file-manifest prefreeze">
      <div className="air-radius-file-head">
        <div>
          <p className="kicker kicker-blue">File-manifest prefreeze</p>
          <h2>The filenames are real; the denominator is still untouched.</h2>
          <p>
            The route scan is now resolved into exact public file URLs and S3
            object keys where the source exposes them. The manifest also makes
            the unresolved ACAG Box routes and current-version drift visible
            before any raster or grid enters the package.
          </p>
        </div>
        <div className="air-radius-file-callout">
          <span>Exact file or object records</span>
          <strong>
            {formatNumber(counts?.exact_file_or_object_records_visible ?? 0)}
            <small> / {formatNumber(counts?.manifest_records ?? 0)}</small>
          </strong>
          <p>Visible names and server metadata only. No denominator file is downloaded.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-radius-file-stat-grid">
            <div>
              <span>Manifest rows</span>
              <strong>{formatNumber(counts.manifest_records)}</strong>
              <em>file, object, metadata, and unresolved route records</em>
            </div>
            <div>
              <span>Population files</span>
              <strong>{formatNumber(counts.exact_population_file_records_visible)}</strong>
              <em>GHSL and WorldPop exact archive or tile URLs</em>
            </div>
            <div>
              <span>PM2.5 objects</span>
              <strong>{formatNumber(counts.exact_pm25_file_records_visible)}</strong>
              <em>current ACAG AWS objects, not the older Box route</em>
            </div>
            <div>
              <span>Version drift rows</span>
              <strong>{formatNumber(counts.current_acag_aws_records_with_source_plan_version_drift)}</strong>
              <em>V6.GL.03 visible while source plan named V6.GL.02.04/V5</em>
            </div>
            <div>
              <span>Box routes unresolved</span>
              <strong>{formatNumber(counts.shared_folder_routes_not_exact_file_manifest)}</strong>
              <em>shared folders still lack exact file manifests</em>
            </div>
            <div>
              <span>Downloads/checksums</span>
              <strong>{formatNumber(downloaded)}</strong>
              <em>radius computation remains blocked</em>
            </div>
          </div>

          <div className="air-radius-file-record-grid" aria-label="File and object manifest records">
            {records.map((record) => {
              const target = record.s3_key || record.exact_file_url || record.file_name || "No exact path captured";
              const externalHref = record.exact_file_url.startsWith("http") ? record.exact_file_url : "";
              return (
                <article
                  key={record.manifest_key}
                  className={`air-radius-file-record air-radius-file-record-${recordTone(record)}`}
                >
                  <div>
                    <span>{sentenceCaseStatus(record.denominator_type)} / {record.source_family}</span>
                    <strong>{record.manifest_key}</strong>
                    <b>{record.resolved_version || record.source_plan_version || "version unresolved"}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Scope</dt>
                      <dd>{record.geography_scope}</dd>
                    </div>
                    <div>
                      <dt>Size</dt>
                      <dd>{formatBytes(record.content_length_bytes)}</dd>
                    </div>
                    <div>
                      <dt>Route</dt>
                      <dd>{sentenceCaseStatus(record.route_type || "unresolved")}</dd>
                    </div>
                    <div>
                      <dt>HEAD</dt>
                      <dd>{record.head_status || "not probed"}</dd>
                    </div>
                  </dl>
                  <p>{record.reader_use}</p>
                  <div className="air-radius-file-path">
                    <span>{record.file_format || "source path"}</span>
                    {externalHref ? (
                      <a href={externalHref}>{target}</a>
                    ) : (
                      <code>{target}</code>
                    )}
                  </div>
                  <p className="air-radius-file-gap">{record.blocking_gap}</p>
                </article>
              );
            })}
          </div>

          <div className="air-radius-file-status-grid" aria-label="Manifest status counts">
            {statusRows.map((row) => (
              <article key={row.status}>
                <div>
                  <span>{sentenceCaseStatus(row.status)}</span>
                  <strong>{formatNumber(row.records)} record{row.records === 1 ? "" : "s"}</strong>
                </div>
                <div className="air-radius-file-track">
                  <i style={{ width: `${Math.max(7, (row.records / maxStatusRecords) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-radius-file-gate-grid" aria-label="File-manifest gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-radius-file-gate air-radius-file-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-radius-file-nonclaim">{summary.non_claim}</p>

          <div className="air-radius-file-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-denominator-file-manifest-prefreeze.md" download>
              Download manifest note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-file-manifest-prefreeze-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-file-manifest-prefreeze.csv" download>
              Download manifest CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius denominator file manifest...</p>
      )}
    </section>
  );
}

function AirStationRadiusDownloadFeasibilityPanel({ summary }: { summary: StationRadiusDownloadFeasibilitySummary | null }) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.download_feasibility_counts ?? [];
  const sizes = summary?.size_class_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const records = useMemo(() => {
    const rows = [...(summary?.feasibility_records ?? [])];
    return rows.sort((a, b) => {
      if (a.first_wave_candidate !== b.first_wave_candidate) return a.first_wave_candidate ? -1 : 1;
      return (a.content_length_bytes || 0) - (b.content_length_bytes || 0);
    });
  }, [summary]);
  const maxDecisionRecords = Math.max(1, ...decisions.map((row) => row.records));
  const maxSizeRecords = Math.max(1, ...sizes.map((row) => row.records));
  const formatBytes = (value: number) => {
    const bytes = Number(value || 0);
    if (!Number.isFinite(bytes) || bytes <= 0) return "unlisted";
    if (bytes >= 1_000_000_000) return `${(bytes / 1_000_000_000).toFixed(1)} GB`;
    if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
    return `${formatNumber(bytes)} B`;
  };
  const decisionTone = (record: StationRadiusDownloadFeasibilityRecord) => {
    if (record.download_feasibility.includes("blocked")) return "blocked";
    if (record.download_feasibility.includes("defer") || record.download_feasibility.includes("second_wave")) return "deferred";
    if (record.download_feasibility.includes("conditional")) return "candidate";
    if (record.first_wave_candidate) return "safe";
    return "review";
  };

  return (
    <section className="showcase-section air-radius-download-section" aria-label="Station-radius denominator download feasibility gate">
      <div className="air-radius-download-head">
        <div>
          <p className="kicker kicker-blue">Download feasibility gate</p>
          <h2>The next download is a decision, not a map.</h2>
          <p>
            The manifest now becomes a file-by-file triage table. It names the
            small checksum candidates, separates metadata and route tests from
            true denominators, and keeps ACAG version drift visible before any
            raster, NetCDF, or catchment layer enters the evidence packet.
          </p>
        </div>
        <div className="air-radius-download-callout">
          <span>First-wave candidates</span>
          <strong>{formatNumber(counts?.first_wave_download_candidates ?? 0)}</strong>
          <p>Identified only. No denominator file has been downloaded or checksummed.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-radius-download-stat-grid">
            <div>
              <span>Manifest rows reviewed</span>
              <strong>{formatNumber(counts.manifest_records_reviewed)}</strong>
              <em>all prefreeze rows classified</em>
            </div>
            <div>
              <span>Safe under 10 MB</span>
              <strong>{formatNumber(counts.safe_under_10mb_records)}</strong>
              <em>small enough for a checksum test</em>
            </div>
            <div>
              <span>Conditional PM2.5</span>
              <strong>{formatNumber(counts.conditional_pm25_checksum_candidates)}</strong>
              <em>ACAG V6.GL.03 coarse objects after version decision</em>
            </div>
            <div>
              <span>Population selected</span>
              <strong>{formatNumber(counts.population_denominator_selected_for_download)}</strong>
              <em>route-test tile is not a DMC denominator</em>
            </div>
            <div>
              <span>Large deferrals</span>
              <strong>{formatNumber(counts.large_population_archives_deferred + counts.moderate_or_large_pm25_objects_deferred)}</strong>
              <em>large archives or second-wave fine objects</em>
            </div>
            <div>
              <span>Downloads/checksums</span>
              <strong>{formatNumber(counts.denominator_files_downloaded + counts.denominator_files_sha256_checksummed)}</strong>
              <em>still zero by design</em>
            </div>
          </div>

          <div className="air-radius-download-lane-grid" aria-label="Download decision rows">
            {records.map((record) => {
              const target = record.s3_key || record.exact_file_url || record.manifest_key;
              return (
                <article
                  key={record.manifest_key}
                  className={`air-radius-download-record air-radius-download-record-${decisionTone(record)}`}
                >
                  <div className="air-radius-download-record-head">
                    <span>{record.first_wave_candidate ? "First-wave candidate" : sentenceCaseStatus(record.selection_role)}</span>
                    <strong>{record.manifest_key}</strong>
                    <b>{formatBytes(record.content_length_bytes)} / {sentenceCaseStatus(record.size_class)}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Source</dt>
                      <dd>{record.source_family}</dd>
                    </div>
                    <div>
                      <dt>Type</dt>
                      <dd>{sentenceCaseStatus(record.denominator_type)}</dd>
                    </div>
                    <div>
                      <dt>Version drift</dt>
                      <dd>{record.source_plan_version_drift ? "yes" : "no"}</dd>
                    </div>
                    <div>
                      <dt>Gate closer</dt>
                      <dd>{record.denominator_gate_closer ? "yes" : "no"}</dd>
                    </div>
                  </dl>
                  <p>{record.reader_use}</p>
                  <p className="air-radius-download-action">{record.proposed_action}</p>
                  <div className="air-radius-download-path">
                    <span>{sentenceCaseStatus(record.download_feasibility)}</span>
                    <code>{target}</code>
                  </div>
                </article>
              );
            })}
          </div>

          <div className="air-radius-download-lists">
            <div>
              <span>Download decisions</span>
              {decisions.map((row) => (
                <article key={row.decision}>
                  <strong>{sentenceCaseStatus(row.decision)}</strong>
                  <b>{formatNumber(row.records)} rows</b>
                  <i style={{ width: `${Math.max(8, (row.records / maxDecisionRecords) * 100)}%` }} />
                </article>
              ))}
            </div>
            <div>
              <span>Size classes</span>
              {sizes.map((row) => (
                <article key={row.size_class}>
                  <strong>{sentenceCaseStatus(row.size_class)}</strong>
                  <b>{formatNumber(row.records)} rows</b>
                  <i style={{ width: `${Math.max(8, (row.records / maxSizeRecords) * 100)}%` }} />
                </article>
              ))}
            </div>
          </div>

          <div className="air-radius-download-gate-grid" aria-label="Download-feasibility gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-radius-download-gate air-radius-download-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-radius-download-nonclaim">{summary.non_claim}</p>

          <div className="air-radius-download-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-denominator-download-feasibility.md" download>
              Download feasibility note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-download-feasibility-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-download-feasibility.csv" download>
              Download decision CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius denominator download feasibility...</p>
      )}
    </section>
  );
}

function AirStationRadiusAcagVersionPanel({ summary }: { summary: StationRadiusAcagVersionSummary | null }) {
  const counts = summary?.coverage_counts;
  const gates = summary?.evidence_gate_counts ?? [];
  const decisions = summary?.decision_counts ?? [];
  const evidenceTypes = summary?.evidence_type_counts ?? [];
  const rows = useMemo(() => {
    const order: Record<string, number> = {
      registry_page: 0,
      method_documentation_page: 1,
      s3_prefix_listing: 2,
      source_page: 3,
      box_shared_folder_page: 4,
    };
    return [...(summary?.acag_rows ?? [])].sort((a, b) => {
      const left = order[a.evidence_type] ?? 9;
      const right = order[b.evidence_type] ?? 9;
      if (left !== right) return left - right;
      return a.record_key.localeCompare(b.record_key);
    });
  }, [summary]);
  const maxDecisionRecords = Math.max(1, ...decisions.map((row) => row.records));
  const asNumber = (value: number | string | undefined) => {
    const parsed = Number(value ?? 0);
    return Number.isFinite(parsed) ? parsed : 0;
  };
  const formatBytes = (value: number | string | undefined) => {
    const bytes = asNumber(value);
    if (bytes <= 0) return "no file";
    if (bytes >= 1_000_000_000) return `${(bytes / 1_000_000_000).toFixed(1)} GB`;
    if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
    return `${formatNumber(bytes)} B`;
  };
  const rowTone = (row: StationRadiusAcagVersionRow) => {
    if (row.decision.includes("approved")) return "approved";
    if (row.decision.includes("second_wave")) return "deferred";
    if (row.decision.includes("defer")) return "deferred";
    if (row.decision.includes("unresolved")) return "blocked";
    if (row.evidence_type.includes("documentation") || row.evidence_type.includes("registry")) return "context";
    return "review";
  };

  return (
    <section className="showcase-section air-acag-version-section" aria-label="ACAG version-decision gate">
      <div className="air-acag-version-head">
        <div>
          <p className="kicker kicker-blue">ACAG version decision</p>
          <h2>Current ACAG becomes a pilot lane, not a silent substitution.</h2>
          <p>
            The source plan named V6.GL.02.04 and V5 Box routes. The public AWS
            path now exposes V6.GL.03 objects. This gate records the decision:
            use V6.GL.03 only as the current-version pilot lane, keep legacy
            routes unresolved, and do not widen the monitoring claim.
          </p>
        </div>
        <div className="air-acag-version-callout">
          <span>Selected vintage</span>
          <strong>{counts?.selected_vintage ?? "2023"}</strong>
          <p>2024 objects are visible, but this package keeps 2023 until the method is amended.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-acag-version-decision">
            <span>Decision</span>
            <p>{summary.version_decision}</p>
          </div>

          <div className="air-acag-version-stat-grid">
            <div>
              <span>Evidence routes</span>
              <strong>{formatNumber(counts.routes_retrieved)}</strong>
              <em>all checked routes retrieved</em>
            </div>
            <div>
              <span>S3 prefixes</span>
              <strong>{formatNumber(counts.s3_prefixes_retrieved)}</strong>
              <em>annual object listings, not downloads</em>
            </div>
            <div>
              <span>First-wave coarse</span>
              <strong>{formatNumber(counts.approved_2023_coarse_first_wave_objects)}</strong>
              <em>Asia pilot plus global sanity object</em>
            </div>
            <div>
              <span>2024 visible</span>
              <strong>{formatNumber(counts.v6gl03_s3_prefixes_with_2024_visible)}</strong>
              <em>visible but not selected</em>
            </div>
            <div>
              <span>Legacy Box unresolved</span>
              <strong>{formatNumber(counts.legacy_v6gl0204_v5_box_routes_unresolved)}</strong>
              <em>not exact file manifests</em>
            </div>
            <div>
              <span>Silent replacements</span>
              <strong>{formatNumber(counts.v6gl03_allowed_as_silent_replacement)}</strong>
              <em>not allowed</em>
            </div>
          </div>

          <div className="air-acag-version-gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-acag-version-gate air-acag-version-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-acag-version-row-grid" aria-label="ACAG version evidence rows">
            {rows.map((row) => {
              const target = row.target_2023_object || row.route_url;
              return (
                <article key={row.record_key} className={`air-acag-version-row air-acag-version-row-${rowTone(row)}`}>
                  <div className="air-acag-version-row-head">
                    <span>{sentenceCaseStatus(row.evidence_type)}</span>
                    <strong>{row.record_key}</strong>
                    <b>{row.observed_version}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Vintage</dt>
                      <dd>{row.selected_vintage}</dd>
                    </div>
                    <div>
                      <dt>Keys</dt>
                      <dd>{formatNumber(asNumber(row.s3_key_count))}</dd>
                    </div>
                    <div>
                      <dt>Years</dt>
                      <dd>{row.first_year && row.latest_year ? `${row.first_year}-${row.latest_year}` : "page"}</dd>
                    </div>
                    <div>
                      <dt>2023 size</dt>
                      <dd>{formatBytes(row.target_2023_size_bytes)}</dd>
                    </div>
                  </dl>
                  <p>{row.allowed_use}</p>
                  <p className="air-acag-version-block">{row.not_allowed_use}</p>
                  <div className="air-acag-version-path">
                    <span>{sentenceCaseStatus(row.decision)}</span>
                    <code>{target}</code>
                  </div>
                  {row.latest_2024_object ? (
                    <small>2024 visible: {formatBytes(row.latest_2024_size_bytes)} / not selected</small>
                  ) : null}
                </article>
              );
            })}
          </div>

          <div className="air-acag-version-lists">
            <div>
              <span>Decision ledger</span>
              {decisions.map((row) => (
                <article key={row.decision}>
                  <strong>{sentenceCaseStatus(row.decision)}</strong>
                  <b>{formatNumber(row.records)} rows</b>
                  <i style={{ width: `${Math.max(8, (row.records / maxDecisionRecords) * 100)}%` }} />
                </article>
              ))}
            </div>
            <div>
              <span>Evidence types</span>
              {evidenceTypes.map((row) => (
                <article key={row.evidence_type}>
                  <strong>{sentenceCaseStatus(row.evidence_type)}</strong>
                  <b>{formatNumber(row.records)} rows</b>
                </article>
              ))}
            </div>
          </div>

          <p className="air-acag-version-nonclaim">{summary.non_claim}</p>

          <div className="air-acag-version-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-acag-version-decision.md" download>
              Download version note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-acag-version-decision-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-acag-version-decision.csv" download>
              Download decision CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading ACAG version decision...</p>
      )}
    </section>
  );
}

function AirStationRadiusAcagChecksumPanel({ summary }: { summary: StationRadiusAcagChecksumSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.checksum_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const asNumber = (value: number | string | undefined) => {
    const parsed = Number(value ?? 0);
    return Number.isFinite(parsed) ? parsed : 0;
  };
  const formatBytes = (value: number | string | undefined) => {
    const bytes = asNumber(value);
    if (bytes <= 0) return "no file";
    if (bytes >= 1_000_000_000) return `${(bytes / 1_000_000_000).toFixed(1)} GB`;
    if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
    return `${formatNumber(bytes)} B`;
  };

  return (
    <section className="showcase-section air-acag-checksum-section" aria-label="ACAG coarse checksum gate">
      <div className="air-acag-checksum-head">
        <div>
          <p className="kicker kicker-blue">Checksum gate</p>
          <h2>The first PM2.5 files are hashed, not interpreted.</h2>
          <p>
            This pass crosses from route discovery into reproducible data
            custody. It downloads only the two approved 2023 V6.GL.03 coarse
            PM2.5 NetCDF files, records hashes and metadata, and stops before
            population denominators, exposure surfaces, or station catchments.
          </p>
        </div>
        <div className="air-acag-checksum-cache">
          <span>Cache policy</span>
          <strong>Ignored raw NetCDF</strong>
          <p>{summary?.cache_policy ?? "Raw ACAG files remain outside the committed tree."}</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-acag-checksum-stat-grid">
            <div>
              <span>Downloaded</span>
              <strong>{formatNumber(counts.downloaded_files)}</strong>
              <em>approved coarse files</em>
            </div>
            <div>
              <span>SHA-256 hashes</span>
              <strong>{formatNumber(counts.sha256_checksummed_files)}</strong>
              <em>committed checksum ledger</em>
            </div>
            <div>
              <span>NetCDF opened</span>
              <strong>{formatNumber(counts.netcdf_files_opened)}</strong>
              <em>metadata inspected</em>
            </div>
            <div>
              <span>PM2.5 variables</span>
              <strong>{formatNumber(counts.files_with_pm25_variable_candidates)}</strong>
              <em>PM25(lat, lon) candidates</em>
            </div>
            <div>
              <span>Population denominators</span>
              <strong>{formatNumber(counts.population_denominator_files_downloaded)}</strong>
              <em>not selected or cached</em>
            </div>
            <div>
              <span>Exposure rows</span>
              <strong>{formatNumber(counts.station_radius_pm25_exposure_rows)}</strong>
              <em>no catchment claim</em>
            </div>
          </div>

          <div className="air-acag-checksum-gates" aria-label="ACAG checksum evidence gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-acag-checksum-gate air-acag-checksum-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-acag-checksum-row-grid" aria-label="Downloaded ACAG checksum rows">
            {rows.map((row) => (
              <article key={row.record_key} className="air-acag-checksum-row">
                <div className="air-acag-checksum-row-head">
                  <span>{sentenceCaseStatus(row.source_role)}</span>
                  <strong>{row.record_key}</strong>
                  <b>{row.observed_version} / {row.selected_vintage}</b>
                </div>
                <dl>
                  <div>
                    <dt>Size</dt>
                    <dd>{formatBytes(row.file_size_bytes)}</dd>
                  </div>
                  <div>
                    <dt>Format</dt>
                    <dd>{row.netcdf_format}</dd>
                  </div>
                  <div>
                    <dt>Dimensions</dt>
                    <dd>{row.dimensions}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.pm25_variable_candidates}</dd>
                  </div>
                </dl>
                <div className="air-acag-checksum-hash">
                  <span>SHA-256</span>
                  <code>{row.sha256}</code>
                </div>
                <div className="air-acag-checksum-path">
                  <span>Cached file</span>
                  <code>{row.cache_path}</code>
                </div>
                <div className="air-acag-checksum-path">
                  <span>S3 object</span>
                  <code>{row.s3_key}</code>
                </div>
                <p>{row.reader_use}</p>
                <p className="air-acag-checksum-block">{row.blocking_gap}</p>
              </article>
            ))}
          </div>

          <p className="air-acag-checksum-nonclaim">{summary.non_claim}</p>

          <div className="air-acag-checksum-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-acag-coarse-checksums.md" download>
              Download checksum note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-acag-coarse-checksums-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-acag-coarse-checksums.csv" download>
              Download checksum CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading ACAG coarse checksum gate...</p>
      )}
    </section>
  );
}

function AirStationRadiusGhslTileSelectionPanel({ summary }: { summary: StationRadiusGhslTileSelectionSummary | null }) {
  const counts = summary?.coverage_counts;
  const countryRows = [...(summary?.country_rows ?? [])].sort(
    (a, b) => b.coordinate_rows_used - a.coordinate_rows_used
  );
  const tileRows = summary?.tile_rows ?? [];
  const maxCountryRows = Math.max(1, ...countryRows.map((row) => Number(row.coordinate_rows_used) || 0));
  const headOkRows = tileRows.filter((row) => row.head_ok);
  const failedRows = tileRows.filter((row) => !row.head_ok);
  const formatBytes = (value: number | string | undefined) => {
    const bytes = Number(value ?? 0);
    if (!Number.isFinite(bytes) || bytes <= 0) return "size unconfirmed";
    if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
    return `${formatNumber(bytes)} B`;
  };
  const headLabel = (row: StationRadiusGhslTileRow) => {
    if (row.head_ok) return row.head_status ? `HEAD ${row.head_status}` : "HEAD OK";
    if (row.retrieval_error.toLowerCase().includes("timed out")) return "timeout";
    if (row.retrieval_error) return "not reached";
    return "HEAD not OK";
  };

  return (
    <section className="showcase-section air-ghsl-tile-section" aria-label="GHSL population tile-selection gate">
      <div className="air-ghsl-tile-head">
        <div>
          <p className="kicker kicker-blue">Population denominator queue</p>
          <h2>Population is now a bounded tile queue, not a catchment count.</h2>
          <p>
            This gate turns station coordinates into exact GHSL population tile
            URLs before any raster body is downloaded. The queue is visible,
            the partial HEAD wall is visible, and every catchment number stays
            at zero until file custody and raster checks close.
          </p>
        </div>
        <div className="air-ghsl-tile-callout">
          <span>Draft radius buffer</span>
          <strong>{formatNumber(counts?.draft_radius_buffer_km ?? 0)} km</strong>
          <p>Used only to over-select tiles around station coordinates; radius rules are not frozen.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-ghsl-tile-stat-grid">
            <div>
              <span>Economies queued</span>
              <strong>{formatNumber(counts.coordinate_ready_economies)}</strong>
              <em>coordinate-ready only</em>
            </div>
            <div>
              <span>Coordinate rows</span>
              <strong>{formatNumber(counts.coordinate_rows_used)}</strong>
              <em>{formatNumber(counts.unique_coordinate_points)} unique points</em>
            </div>
            <div>
              <span>Tile URLs</span>
              <strong>{formatNumber(counts.ghsl_population_tile_urls_selected)}</strong>
              <em>selected for future custody</em>
            </div>
            <div>
              <span>HEAD OK</span>
              <strong>{formatNumber(counts.ghsl_tile_head_ok)} / {formatNumber(counts.ghsl_tile_head_probes)}</strong>
              <em>{formatNumber(counts.ghsl_tile_head_failed)} still failed</em>
            </div>
            <div>
              <span>Known-size subset</span>
              <strong>{formatNumber(counts.selected_tile_content_length_mb_total, 1)} MB</strong>
              <em>from successful HEAD only</em>
            </div>
            <div>
              <span>Population files</span>
              <strong>{formatNumber(counts.population_denominator_files_downloaded)}</strong>
              <em>no ZIPs or hashes yet</em>
            </div>
          </div>

          <div className="air-ghsl-tile-gates" aria-label="GHSL population evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-ghsl-tile-gate air-ghsl-tile-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-ghsl-tile-queue">
            <div className="air-ghsl-tile-country-list" aria-label="Country tile queue">
              <div className="air-ghsl-tile-subhead">
                <span>Country queue</span>
                <strong>{formatNumber(countryRows.length)} economies</strong>
              </div>
              {countryRows.map((row) => {
                const share = Math.max(5, Math.round((row.coordinate_rows_used / maxCountryRows) * 100));
                return (
                  <article key={row.iso3} className="air-ghsl-tile-country-card">
                    <div>
                      <span>{row.iso3}</span>
                      <strong>{row.country}</strong>
                      <em>{formatNumber(row.ghsl_population_tiles_selected)} tile URLs</em>
                    </div>
                    <div className="air-ghsl-tile-meter" aria-hidden="true">
                      <i style={{ width: `${share}%` }} />
                    </div>
                    <dl>
                      <div>
                        <dt>Rows</dt>
                        <dd>{formatNumber(row.coordinate_rows_used)}</dd>
                      </div>
                      <div>
                        <dt>OpenAQ</dt>
                        <dd>{formatNumber(row.openaq_coordinate_rows_used)}</dd>
                      </div>
                      <div>
                        <dt>Official</dt>
                        <dd>{formatNumber(row.official_pm25_coordinate_rows_used)}</dd>
                      </div>
                    </dl>
                    <code>{row.tile_ids}</code>
                  </article>
                );
              })}
            </div>

            <div className="air-ghsl-tile-wall" aria-label="Selected GHSL tile URL wall">
              <div className="air-ghsl-tile-subhead">
                <span>Selected tiles</span>
                <strong>{formatNumber(headOkRows.length)} reached, {formatNumber(failedRows.length)} still blocked</strong>
              </div>
              <div className="air-ghsl-tile-card-grid">
                {tileRows.map((row) => (
                  <article
                    key={row.tile_id}
                    className={`air-ghsl-tile-card ${row.head_ok ? "air-ghsl-tile-card-ok" : "air-ghsl-tile-card-failed"}`}
                  >
                    <div className="air-ghsl-tile-card-head">
                      <span>{row.selected_economies.replaceAll("||", " + ")}</span>
                      <strong>{row.tile_id}</strong>
                      <b>{headLabel(row)}</b>
                    </div>
                    <dl>
                      <div>
                        <dt>Coord. rows</dt>
                        <dd>{formatNumber(row.coordinate_rows_touching_tile)}</dd>
                      </div>
                      <div>
                        <dt>Size</dt>
                        <dd>{row.size_mb ? `${row.size_mb} MB` : formatBytes(row.content_length_bytes)}</dd>
                      </div>
                      <div>
                        <dt>Bounds</dt>
                        <dd>{row.west} to {row.east} E</dd>
                      </div>
                    </dl>
                    <p>{row.head_ok ? row.last_modified : row.retrieval_error}</p>
                  </article>
                ))}
              </div>
            </div>
          </div>

          <p className="air-ghsl-tile-assumption">{summary.tile_grid_assumption}</p>
          <p className="air-ghsl-tile-nonclaim">{summary.non_claim}</p>

          <div className="air-ghsl-tile-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-ghsl-population-tile-selection.md" download>
              Download tile-selection note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-selection-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-selection.csv" download>
              Download tile CSV
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-selection-country.csv" download>
              Download country CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading GHSL population tile-selection gate...</p>
      )}
    </section>
  );
}

function AirStationRadiusGhslTileChecksumPanel({ summary }: { summary: StationRadiusGhslTileChecksumSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.tile_checksum_rows ?? [];
  const firstWaveRows = rows.filter((row) => row.download_decision === "selected_first_wave_download_candidate");
  const downloadedRows = firstWaveRows.filter((row) => row.downloaded);
  const failedRows = firstWaveRows.filter((row) => !row.downloaded);
  const isTrue = (value: boolean | string | undefined) => value === true || String(value).toLowerCase() === "true";
  const formatBytes = (value: number | string | undefined) => {
    const bytes = Number(value ?? 0);
    if (!Number.isFinite(bytes) || bytes <= 0) return "no file";
    if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    if (bytes >= 1_000) return `${(bytes / 1_000).toFixed(1)} KB`;
    return `${formatNumber(bytes)} B`;
  };

  return (
    <section className="showcase-section air-ghsl-checksum-section" aria-label="GHSL population tile checksum and transform gate">
      <div className="air-ghsl-checksum-head">
        <div>
          <p className="kicker kicker-blue">File custody gate</p>
          <h2>The first ZIPs open, but the grid assumption breaks.</h2>
          <p>
            Four selected GHSL population tiles are now downloaded, hashed, and
            readable as GeoTIFFs. Their inspected bounds do not match the simple
            10-degree routing assumption, so the method has to correct tile
            routing before any station-radius population is computed.
          </p>
        </div>
        <div className="air-ghsl-checksum-warning">
          <span>Transform mismatch</span>
          <strong>{formatNumber(counts?.geotiff_transform_mismatch_files ?? 0)}</strong>
          <p>Every inspected first-wave raster is readable, but not ready for catchment use.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-ghsl-checksum-stat-grid">
            <div>
              <span>Selected tiles</span>
              <strong>{formatNumber(counts.selected_tile_rows)}</strong>
              <em>from the prior queue</em>
            </div>
            <div>
              <span>First wave</span>
              <strong>{formatNumber(counts.first_wave_download_candidate_rows)}</strong>
              <em>HEAD OK and &lt;= 60 MB</em>
            </div>
            <div>
              <span>Downloaded</span>
              <strong>{formatNumber(counts.downloaded_population_tile_files)}</strong>
              <em>{formatNumber(counts.downloaded_size_mb_total, 1)} MB cached</em>
            </div>
            <div>
              <span>SHA-256 hashes</span>
              <strong>{formatNumber(counts.sha256_checksummed_population_tile_files)}</strong>
              <em>committed checksum rows</em>
            </div>
            <div>
              <span>Transform matches</span>
              <strong>{formatNumber(counts.geotiff_transform_matches_10_degree_tile_bounds)}</strong>
              <em>{formatNumber(counts.geotiff_transform_mismatch_files)} mismatches</em>
            </div>
            <div>
              <span>Population rows</span>
              <strong>{formatNumber(counts.station_radius_population_rows)}</strong>
              <em>no catchment output</em>
            </div>
          </div>

          <div className="air-ghsl-checksum-gates" aria-label="GHSL checksum evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-ghsl-checksum-gate air-ghsl-checksum-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-ghsl-checksum-rule">
            <span>First-wave rule</span>
            <p>{summary.first_wave_rule}</p>
          </div>

          <div className="air-ghsl-checksum-row-grid" aria-label="First-wave GHSL tile custody rows">
            {firstWaveRows.map((row) => {
              const opened = isTrue(row.geotiff_opened);
              const boundsMatch = isTrue(row.transform_matches_10_degree_tile_bounds);
              const boundsLabel = opened ? (boundsMatch ? "match" : "mismatch") : "not inspected";
              return (
                <article
                  key={row.tile_id}
                  className={`air-ghsl-checksum-row ${row.downloaded ? "air-ghsl-checksum-row-downloaded" : "air-ghsl-checksum-row-failed"}`}
                >
                  <div className="air-ghsl-checksum-row-head">
                    <span>{row.selected_economies.replaceAll("||", " + ")}</span>
                    <strong>{row.tile_id}</strong>
                    <b>{row.downloaded ? "downloaded" : "download failed"}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Size</dt>
                      <dd>{formatBytes(row.file_size_bytes || row.expected_size_bytes)}</dd>
                    </div>
                    <div>
                      <dt>GeoTIFF</dt>
                      <dd>{opened ? "opened" : "not opened"}</dd>
                    </div>
                    <div>
                      <dt>Bounds</dt>
                      <dd>{boundsLabel}</dd>
                    </div>
                  </dl>
                  {row.sha256 ? (
                    <div className="air-ghsl-checksum-hash">
                      <span>SHA-256</span>
                      <code>{row.sha256}</code>
                    </div>
                  ) : null}
                  {row.raster_bounds ? (
                    <div className="air-ghsl-checksum-path">
                      <span>Raster bounds</span>
                      <code>{row.raster_bounds}</code>
                    </div>
                  ) : null}
                  <p>{row.blocking_gap}</p>
                  {row.retrieval_error ? <p className="air-ghsl-checksum-error">{row.retrieval_error}</p> : null}
                </article>
              );
            })}
          </div>

          <p className="air-ghsl-checksum-nonclaim">{summary.non_claim}</p>

          <div className="air-ghsl-checksum-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-ghsl-population-tile-checksums.md" download>
              Download checksum note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-checksums-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-population-tile-checksums.csv" download>
              Download checksum CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading GHSL population tile checksum gate...</p>
      )}
    </section>
  );
}

function AirStationRadiusGhslTileRoutingPanel({ summary }: { summary: StationRadiusGhslTileRoutingSummary | null }) {
  const counts = summary?.coverage_counts;
  const changedRows = (summary?.tile_rows ?? []).filter((row) => row.correction_status !== "retained_by_corrected_origin");
  const countryChanges = (summary?.country_rows ?? []).filter((row) => row.added_tile_count > 0 || row.removed_tile_count > 0);
  const originRows = summary?.origin_rows ?? [];

  const correctionLabel = (status: string) => {
    if (status === "added_by_corrected_origin") return "added";
    if (status === "removed_by_corrected_origin") return "removed";
    return "retained";
  };
  const isTruthyEvidence = (value: boolean | string | undefined) => value === true || String(value).toLowerCase() === "true";

  return (
    <section className="showcase-section air-ghsl-routing-section" aria-label="GHSL tile routing correction gate">
      <div className="air-ghsl-routing-head">
        <div>
          <p className="kicker kicker-ochre">Routing correction</p>
          <h2>The corrected grid changes the denominator queue.</h2>
          <p>
            The first downloaded GeoTIFFs reveal a consistent GHSL origin, so
            the station-coordinate queue is rerun against that observed grid
            before any catchment population is computed.
          </p>
        </div>
        <div className="air-ghsl-routing-callout">
          <span>Queue change</span>
          <strong>{formatNumber(counts?.added_corrected_tile_urls ?? 0)} added / {formatNumber(counts?.removed_previous_tile_urls ?? 0)} removed</strong>
          <p>
            One added tile still has no HEAD or checksum custody. One previously
            downloaded tile is no longer selected under the corrected origin.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-ghsl-routing-stat-grid">
            <div>
              <span>Origin rasters</span>
              <strong>{formatNumber(counts.origin_observation_rows)}</strong>
              <em>opened GeoTIFFs</em>
            </div>
            <div>
              <span>Previous queue</span>
              <strong>{formatNumber(counts.previous_tile_urls_selected)}</strong>
              <em>simple-grid tile IDs</em>
            </div>
            <div>
              <span>Corrected queue</span>
              <strong>{formatNumber(counts.corrected_tile_urls_selected)}</strong>
              <em>observed-origin tile IDs</em>
            </div>
            <div>
              <span>Retained</span>
              <strong>{formatNumber(counts.retained_previous_tile_urls)}</strong>
              <em>carry prior evidence</em>
            </div>
            <div>
              <span>Added</span>
              <strong>{formatNumber(counts.added_corrected_tile_urls)}</strong>
              <em>{summary.added_corrected_tile_ids.join(", ") || "none"}</em>
            </div>
            <div>
              <span>Removed</span>
              <strong>{formatNumber(counts.removed_previous_tile_urls)}</strong>
              <em>{summary.removed_previous_tile_ids.join(", ") || "none"}</em>
            </div>
          </div>

          <div className="air-ghsl-routing-gates" aria-label="GHSL routing correction evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-ghsl-routing-gate air-ghsl-routing-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-ghsl-routing-rule">
            <span>Corrected routing rule</span>
            <p>{summary.routing_rule}</p>
          </div>

          <div className="air-ghsl-routing-origin-grid" aria-label="Observed GHSL origin rows">
            {originRows.map((row) => (
              <article key={row.tile_id} className="air-ghsl-routing-origin-card">
                <span>{row.tile_id}</span>
                <strong>{formatNumber(row.derived_north_origin, 8)} north / {formatNumber(row.derived_west_origin, 8)} west</strong>
                <code>
                  {formatNumber(row.raster_west, 6)},{formatNumber(row.raster_south, 6)},
                  {formatNumber(row.raster_east, 6)},{formatNumber(row.raster_north, 6)}
                </code>
              </article>
            ))}
          </div>

          <div className="air-ghsl-routing-change-grid" aria-label="GHSL routing changed tile rows">
            {changedRows.map((row) => {
              const priorHead = row.prior_head_ok === "" ? "unknown" : isTruthyEvidence(row.prior_head_ok) ? "HEAD OK" : "HEAD not OK";
              const priorDownloaded = row.prior_downloaded === "" ? "not checked" : isTruthyEvidence(row.prior_downloaded) ? "downloaded" : "not downloaded";
              const economies = row.corrected_selected_economies || row.previous_selected_economies || "no economy";
              return (
                <article
                  key={row.tile_id}
                  className={`air-ghsl-routing-change air-ghsl-routing-change-${correctionLabel(row.correction_status)}`}
                >
                  <div>
                    <span>{correctionLabel(row.correction_status)}</span>
                    <strong>{row.tile_id}</strong>
                    <em>{economies.replaceAll("||", " + ")}</em>
                  </div>
                  <dl>
                    <div>
                      <dt>Corrected rows</dt>
                      <dd>{formatNumber(Number(row.corrected_coordinate_rows_touching_tile || 0))}</dd>
                    </div>
                    <div>
                      <dt>Prior HEAD</dt>
                      <dd>{priorHead}</dd>
                    </div>
                    <div>
                      <dt>Custody</dt>
                      <dd>{priorDownloaded}</dd>
                    </div>
                  </dl>
                  {row.prior_sha256 ? (
                    <code>{row.prior_sha256}</code>
                  ) : null}
                </article>
              );
            })}
          </div>

          <div className="air-ghsl-routing-country-grid" aria-label="Countries with corrected GHSL queue changes">
            {countryChanges.map((row) => (
              <article key={row.iso3} className="air-ghsl-routing-country-card">
                <span>{row.iso3}</span>
                <strong>{row.country}</strong>
                <dl>
                  <div>
                    <dt>Previous</dt>
                    <dd>{formatNumber(row.previous_tile_count)}</dd>
                  </div>
                  <div>
                    <dt>Corrected</dt>
                    <dd>{formatNumber(row.corrected_tile_count)}</dd>
                  </div>
                  <div>
                    <dt>Added</dt>
                    <dd>{row.added_tile_ids || "none"}</dd>
                  </div>
                  <div>
                    <dt>Removed</dt>
                    <dd>{row.removed_tile_ids || "none"}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <p className="air-ghsl-routing-nonclaim">{summary.non_claim}</p>

          <div className="air-ghsl-routing-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-ghsl-tile-routing-correction.md" download>
              Download correction note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-tile-routing-correction-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-tile-routing-correction.csv" download>
              Download tile CSV
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-tile-routing-correction-country.csv" download>
              Download country CSV
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-tile-routing-correction-origin.csv" download>
              Download origin CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading GHSL tile routing correction gate...</p>
      )}
    </section>
  );
}

function AirStationRadiusGhslCorrectedCustodyPanel({ summary }: { summary: StationRadiusGhslCorrectedCustodySummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.tile_custody_rows ?? [];
  const isTruthyEvidence = (value: boolean | string | undefined) => value === true || String(value).toLowerCase() === "true";
  const deferredRows = rows.filter((row) => row.download_decision.startsWith("deferred"));
  const downloadedRows = rows
    .filter((row) => isTruthyEvidence(row.downloaded))
    .sort((a, b) => Number(b.file_size_bytes || 0) - Number(a.file_size_bytes || 0));
  const formatSize = (value: number | string | undefined) => {
    const mb = Number(value ?? 0);
    if (!Number.isFinite(mb) || mb <= 0) return "size missing";
    return `${formatNumber(mb, 1)} MB`;
  };
  const formatBytes = (value: number | string | undefined) => {
    const bytes = Number(value ?? 0);
    if (!Number.isFinite(bytes) || bytes <= 0) return "size missing";
    return `${formatNumber(bytes / 1_000_000, 1)} MB`;
  };
  const decisionLabel = (decision: string) => {
    if (decision.startsWith("deferred")) return "deferred large tile";
    if (decision === "retained_corrected_queue_cached_zip") return "cached custody";
    if (decision === "corrected_first_wave_download_candidate") return "download candidate";
    if (decision.startsWith("blocked")) return "blocked probe";
    return decision.replaceAll("_", " ");
  };

  return (
    <section className="showcase-section air-ghsl-custody-section" aria-label="GHSL corrected population tile custody gate">
      <div className="air-ghsl-custody-head">
        <div>
          <p className="kicker kicker-green">Corrected custody</p>
          <h2>The denominator gap is now three large tiles.</h2>
          <p>
            The corrected queue is probed again against public GHSL files. Most
            selected population tiles are now downloaded, hashed, and checked
            against the corrected origin; the remaining gap is explicit large
            tile custody, not an invisible routing error.
          </p>
        </div>
        <div className="air-ghsl-custody-callout">
          <span>Corrected queue in custody</span>
          <strong>{formatNumber(counts?.downloaded_population_tile_files ?? 0)} / {formatNumber(counts?.corrected_tile_rows ?? 0)}</strong>
          <p>
            {formatNumber(counts?.geotiff_transform_matches_corrected_bounds ?? 0)} opened rasters match corrected bounds.
            {counts?.deferred_corrected_selected_tiles ? ` ${formatNumber(counts.deferred_corrected_selected_tiles)} large tiles remain deferred.` : " No selected tile is blocked."}
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-ghsl-custody-stat-grid">
            <div>
              <span>Current probes</span>
              <strong>{formatNumber(counts.current_probe_size_available_tiles)}</strong>
              <em>of {formatNumber(counts.corrected_tile_rows)} corrected URLs</em>
            </div>
            <div>
              <span>First-wave eligible</span>
              <strong>{formatNumber(counts.corrected_first_wave_eligible_rows)}</strong>
              <em>at or below 60 MB</em>
            </div>
            <div>
              <span>ZIPs in custody</span>
              <strong>{formatNumber(counts.downloaded_population_tile_files)}</strong>
              <em>{formatNumber(counts.downloaded_size_mb_total, 1)} MB cached</em>
            </div>
            <div>
              <span>SHA-256 hashes</span>
              <strong>{formatNumber(counts.sha256_checksummed_population_tile_files)}</strong>
              <em>{formatNumber(counts.sha256_matches_prior_rows)} match prior cache</em>
            </div>
            <div>
              <span>Corrected matches</span>
              <strong>{formatNumber(counts.geotiff_transform_matches_corrected_bounds)}</strong>
              <em>{formatNumber(counts.geotiff_transform_mismatch_corrected_bounds)} mismatches</em>
            </div>
            <div>
              <span>Deferred large tiles</span>
              <strong>{formatNumber(counts.deferred_corrected_selected_tiles)}</strong>
              <em>not used for catchments</em>
            </div>
          </div>

          <div className="air-ghsl-custody-gates" aria-label="GHSL corrected custody evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-ghsl-custody-gate air-ghsl-custody-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-ghsl-custody-rule">
            <span>First-wave rule</span>
            <p>{summary.first_wave_rule}</p>
          </div>

          <div className="air-ghsl-custody-deferred-grid" aria-label="Deferred large corrected GHSL tiles">
            {deferredRows.map((row) => (
              <article key={row.tile_id} className="air-ghsl-custody-deferred-card">
                <span>{decisionLabel(row.download_decision)}</span>
                <strong>{row.tile_id}</strong>
                <em>{row.corrected_selected_economies.replaceAll("||", " + ")}</em>
                <dl>
                  <div>
                    <dt>Current size</dt>
                    <dd>{formatSize(row.custody_size_mb)}</dd>
                  </div>
                  <div>
                    <dt>Probe</dt>
                    <dd>{row.custody_probe_source || "none"}</dd>
                  </div>
                  <div>
                    <dt>Rows touched</dt>
                    <dd>{formatNumber(Number(row.corrected_coordinate_rows_touching_tile || 0))}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-ghsl-custody-download-grid" aria-label="Downloaded corrected GHSL population tiles">
            {downloadedRows.map((row) => (
              <article key={row.tile_id} className="air-ghsl-custody-download-card">
                <span>{isTruthyEvidence(row.downloaded_from_prior_cache) ? "cached" : "downloaded"}</span>
                <strong>{row.tile_id}</strong>
                <em>{row.corrected_selected_economies.replaceAll("||", " + ")}</em>
                <dl>
                  <div>
                    <dt>Size</dt>
                    <dd>{formatBytes(row.file_size_bytes)}</dd>
                  </div>
                  <div>
                    <dt>Bounds</dt>
                    <dd>{isTruthyEvidence(row.transform_matches_corrected_tile_bounds) ? "match" : "check"}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <p className="air-ghsl-custody-nonclaim">{summary.non_claim}</p>

          <div className="air-ghsl-custody-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-ghsl-corrected-population-tile-custody.md" download>
              Download custody note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-corrected-population-tile-custody-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-corrected-population-tile-custody.csv" download>
              Download custody CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading GHSL corrected tile custody gate...</p>
      )}
    </section>
  );
}

function AirStationRadiusGhslLargeCustodyPanel({ summary }: { summary: StationRadiusGhslLargeCustodySummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.large_tile_custody_rows ?? [];
  const isTruthyEvidence = (value: boolean | string | undefined) => value === true || String(value).toLowerCase() === "true";
  const formatSize = (value: number | string | undefined) => {
    const mb = Number(value ?? 0);
    if (!Number.isFinite(mb) || mb <= 0) return "size missing";
    return `${formatNumber(mb, 1)} MB`;
  };
  const formatBytes = (value: number | string | undefined) => {
    const bytes = Number(value ?? 0);
    if (!Number.isFinite(bytes) || bytes <= 0) return "size missing";
    return `${formatNumber(bytes / 1_000_000, 1)} MB`;
  };

  return (
    <section className="showcase-section air-ghsl-large-section" aria-label="GHSL large corrected population tile custody gate">
      <div className="air-ghsl-large-head">
        <div>
          <p className="kicker kicker-green">Large tile custody</p>
          <h2>Population file custody is now 21 of 21.</h2>
          <p>
            The three large corrected GHSL tiles that were deliberately left
            out of the first-wave pass are now downloaded, hashed, and opened.
            This closes the population file-custody gap while leaving the
            station-radius method and join rules unfrozen.
          </p>
        </div>
        <div className="air-ghsl-large-callout">
          <span>Corrected files in custody</span>
          <strong>{formatNumber(counts?.corrected_tile_files_in_custody_after_large_pass ?? 0)} / {formatNumber(counts?.corrected_tile_files_required ?? 0)}</strong>
          <p>
            {formatNumber(counts?.downloaded_large_population_tile_files ?? 0)} large ZIPs add
            {counts ? ` ${formatNumber(counts.downloaded_large_size_mb_total, 1)} MB` : " file"} custody evidence.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-ghsl-large-stat-grid">
            <div>
              <span>Large probes</span>
              <strong>{formatNumber(counts.current_head_ok_large_tiles)}</strong>
              <em>of {formatNumber(counts.large_corrected_tile_rows)} URLs</em>
            </div>
            <div>
              <span>Large ZIPs</span>
              <strong>{formatNumber(counts.downloaded_large_population_tile_files)}</strong>
              <em>{formatNumber(counts.downloaded_large_size_mb_total, 1)} MB cached</em>
            </div>
            <div>
              <span>Large hashes</span>
              <strong>{formatNumber(counts.sha256_checksummed_large_population_tile_files)}</strong>
              <em>{formatNumber(counts.downloaded_large_population_tile_files_this_run)} downloaded on final run</em>
            </div>
            <div>
              <span>Bounds matches</span>
              <strong>{formatNumber(counts.large_geotiff_transform_matches_corrected_bounds)}</strong>
              <em>{formatNumber(counts.large_geotiff_transform_mismatch_corrected_bounds)} mismatches</em>
            </div>
            <div>
              <span>Full custody</span>
              <strong>{formatNumber(counts.corrected_tile_files_in_custody_after_large_pass)}</strong>
              <em>of {formatNumber(counts.corrected_tile_files_required)} corrected tiles</em>
            </div>
            <div>
              <span>Catchment rows</span>
              <strong>{formatNumber(counts.station_radius_population_rows)}</strong>
              <em>method still not frozen</em>
            </div>
          </div>

          <div className="air-ghsl-large-gates" aria-label="Large corrected GHSL custody evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-ghsl-large-gate air-ghsl-large-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-ghsl-large-rule">
            <span>Target rule</span>
            <p>{summary.target_rule}</p>
          </div>

          <div className="air-ghsl-large-card-grid" aria-label="Large corrected GHSL population tiles">
            {rows.map((row) => (
              <article key={row.tile_id} className="air-ghsl-large-card">
                <span>{isTruthyEvidence(row.downloaded_from_prior_cache) ? "cached after retry" : "downloaded on final run"}</span>
                <strong>{row.tile_id}</strong>
                <em>{row.corrected_selected_economies.replaceAll("||", " + ")}</em>
                <dl>
                  <div>
                    <dt>Probe size</dt>
                    <dd>{formatSize(row.custody_size_mb)}</dd>
                  </div>
                  <div>
                    <dt>File size</dt>
                    <dd>{formatBytes(row.file_size_bytes)}</dd>
                  </div>
                  <div>
                    <dt>Rows touched</dt>
                    <dd>{formatNumber(Number(row.corrected_coordinate_rows_touching_tile || 0))}</dd>
                  </div>
                  <div>
                    <dt>Bounds</dt>
                    <dd>{isTruthyEvidence(row.transform_matches_corrected_tile_bounds) ? "match" : "check"}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <p className="air-ghsl-large-nonclaim">{summary.non_claim}</p>

          <div className="air-ghsl-large-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-ghsl-large-population-tile-custody.md" download>
              Download large-tile note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-large-population-tile-custody-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-ghsl-large-population-tile-custody.csv" download>
              Download custody CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading GHSL large tile custody gate...</p>
      )}
    </section>
  );
}

function AirStationRadiusMethodPrefreezePanel({ summary }: { summary: StationRadiusMethodPrefreezeSummary | null }) {
  const counts = summary?.coverage_counts;
  const rules = summary?.method_rule_rows ?? [];
  const countries = summary?.country_rows ?? [];
  const isTruthyEvidence = (value: boolean | string | undefined) => value === true || String(value).toLowerCase() === "true";
  const ruleTone = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized.includes("blocked") || normalized.includes("not_")) return "blocked";
    if (normalized.includes("available")) return "available";
    if (normalized.includes("prefrozen")) return "prefrozen";
    return "pending";
  };

  return (
    <section className="showcase-section air-method-section" aria-label="Station-radius method prefreeze gate">
      <div className="air-method-head">
        <div>
          <p className="kicker kicker-blue">Method prefreeze</p>
          <h2>The map is still locked, but the evidence frame is no longer loose.</h2>
          <p>
            This gate turns the custody work into a reproducible method ledger:
            which rows can enter a dry run, which file denominators are fixed,
            and which claims remain blocked before any station-radius visual can
            become a result.
          </p>
        </div>
        <div className="air-method-lock">
          <span>Publication state</span>
          <strong>{summary ? sentenceCaseStatus(summary.method_stage) : "Loading"}</strong>
          <p>
            {counts
              ? `${formatNumber(counts.population_tile_files_in_custody)} of ${formatNumber(counts.population_tile_files_required)} population tiles are in custody; ${formatNumber(counts.station_radius_population_rows)} catchment rows exist.`
              : "Reading method ledger."}
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-method-stat-grid">
            <div>
              <span>Coordinate rows</span>
              <strong>{formatNumber(counts.coordinate_rows_used)}</strong>
              <em>{formatNumber(counts.unique_coordinate_points)} unique points</em>
            </div>
            <div>
              <span>Population custody</span>
              <strong>{formatNumber(counts.population_tile_files_in_custody)} / {formatNumber(counts.population_tile_files_required)}</strong>
              <em>{formatNumber(counts.coordinate_economies_with_full_population_tile_custody)} economies complete</em>
            </div>
            <div>
              <span>PM2.5 custody</span>
              <strong>{formatNumber(counts.pm25_coarse_files_in_custody)}</strong>
              <em>coarse pilot files</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_join_rows)}</strong>
              <em>no source-family merge</em>
            </div>
            <div>
              <span>Complete grade rows</span>
              <strong>{formatNumber(counts.complete_monitor_grade_rows)}</strong>
              <em>no regulatory coverage claim</em>
            </div>
            <div>
              <span>Catchment rows</span>
              <strong>{formatNumber(counts.station_radius_population_rows)}</strong>
              <em>map remains locked</em>
            </div>
          </div>

          <div className="air-method-gate-rail" aria-label="Station-radius method evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-method-gate air-method-gate-${ruleTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-method-rule-grid" aria-label="Station-radius method rule ledger">
            {rules.map((rule) => (
              <article key={rule.rule_id} className={`air-method-rule air-method-rule-${ruleTone(rule.gate_status)}`}>
                <span>{sentenceCaseStatus(rule.gate_status)}</span>
                <strong>{rule.gate}</strong>
                <em>
                  {isTruthyEvidence(rule.frozen_for_next_compute)
                    ? "Frozen for dry run"
                    : `Blocked: ${sentenceCaseStatus(rule.next_blocker)}`}
                </em>
                <p>{rule.decision}</p>
              </article>
            ))}
          </div>

          <div className="air-method-country-wall" aria-label="Station-radius country prefreeze rows">
            {countries.map((row) => {
              const coordinateRows = Number(row.coordinate_rows_used || 0);
              const custody = Number(row.population_tile_files_in_custody || 0);
              const tiles = Number(row.corrected_tile_count || 0);
              return (
                <article key={row.iso3} className="air-method-country">
                  <div>
                    <span>{row.iso3}</span>
                    <strong>{formatNumber(coordinateRows)} rows</strong>
                  </div>
                  <div className="air-method-country-meter" aria-hidden="true">
                    <i style={{ width: `${Math.max(10, Math.min(100, (coordinateRows / 85) * 100))}%` }} />
                  </div>
                  <p>
                    {formatNumber(Number(row.unique_coordinate_points || 0))} unique points;
                    {" "}
                    {formatNumber(custody)} of {formatNumber(tiles)} GHSL tiles in custody.
                  </p>
                </article>
              );
            })}
          </div>

          <p className="air-method-nonclaim">{summary.non_claim}</p>

          <div className="air-method-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-method-prefreeze.md" download>
              Download method note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-method-prefreeze-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-method-prefreeze.csv" download>
              Download ledger CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius method prefreeze...</p>
      )}
    </section>
  );
}

function AirStationRadiusRuleSourcePanel({ summary }: { summary: StationRadiusRuleSummary | null }) {
  const counts = summary?.coverage_counts;
  const rule = summary?.radius_rule;
  const selectedEvidence = (summary?.evidence_rows ?? []).filter(
    (row) => String(row.selected_for_rule).toLowerCase() === "true",
  );
  const radiusMarkers = rule
    ? [
        {
          key: "lower",
          label: `${rule.sensitivity_radii_km[0]} km`,
          value: rule.sensitivity_radii_km[0],
          title: "Lower sensitivity",
          text: "Middle-to-neighborhood boundary.",
        },
        {
          key: "primary",
          label: `${rule.primary_radius_km} km`,
          value: rule.primary_radius_km,
          title: "Primary diagnostic",
          text: rule.primary_label,
        },
        {
          key: "upper",
          label: `${rule.sensitivity_radii_km[1]} km`,
          value: rule.sensitivity_radii_km[1],
          title: "Upper sensitivity",
          text: "Urban-scale upper band and tile envelope.",
        },
      ]
    : [];
  const positionPct = (value: number) => {
    const lower = rule?.sensitivity_radii_km[0] ?? 0.5;
    const upper = rule?.sensitivity_radii_km[1] ?? 50;
    const ratio = Math.log10(value / lower) / Math.log10(upper / lower);
    return Math.max(0, Math.min(100, ratio * 100));
  };
  const evidenceRadius = (row: StationRadiusRuleEvidenceRow) => {
    if (row.radius_km === "" || row.radius_km === undefined) return "scale rule";
    return `${row.radius_km} km`;
  };
  const gateTone = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized.includes("available") || normalized.includes("frozen")) return "available";
    if (normalized.includes("partial") || normalized.includes("not_computed")) return "pending";
    return "blocked";
  };

  return (
    <section className="showcase-section air-radius-rule-section" aria-label="Station-radius source-based radius rule">
      <div className="air-radius-rule-head">
        <div>
          <p className="kicker kicker-blue">Radius-rule source wall</p>
          <h2>The radius now has a source; the catchment still has no result.</h2>
          <p>
            The scan retrieves the public spatial-scale sources, freezes a
            diagnostic 4 km PM2.5 neighborhood band, and keeps 0.5 km and 50 km
            sensitivity bands visible before any population or exposure row is
            computed.
          </p>
        </div>
        <div className="air-radius-rule-callout">
          <span>Rule state</span>
          <strong>{rule ? sentenceCaseStatus(rule.status) : "Loading"}</strong>
          <p>
            {counts
              ? `${formatNumber(counts.rule_selected_evidence_rows)} selected source rows; ${formatNumber(counts.station_radius_population_rows)} catchment rows.`
              : "Reading source scan."}
          </p>
        </div>
      </div>

      {summary && counts && rule ? (
        <>
          <div className="air-radius-rule-ladder" aria-label="Source-frozen station-radius bands">
            <div className="air-radius-rule-ladder-copy">
              <span>Diagnostic band</span>
              <strong>{rule.primary_radius_km} km primary</strong>
              <p>{rule.claim_guardrail}</p>
            </div>
            <div className="air-radius-rule-track" aria-hidden="true">
              <i />
              {radiusMarkers.map((marker) => (
                <b
                  key={marker.key}
                  className={`air-radius-rule-marker air-radius-rule-marker-${marker.key}`}
                  style={{ left: `${positionPct(marker.value)}%` }}
                >
                  <span>{marker.label}</span>
                </b>
              ))}
            </div>
            <div className="air-radius-rule-marker-grid">
              {radiusMarkers.map((marker) => (
                <article key={marker.key} className={`air-radius-rule-band air-radius-rule-band-${marker.key}`}>
                  <span>{marker.title}</span>
                  <strong>{marker.label}</strong>
                  <p>{marker.text}</p>
                </article>
              ))}
            </div>
          </div>

          <div className="air-radius-rule-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.retrieved_sources)} / {formatNumber(counts.seed_sources)}</strong>
              <em>{formatNumber(counts.retrieval_error_sources)} retrieval errors</em>
            </div>
            <div>
              <span>Selected evidence</span>
              <strong>{formatNumber(counts.rule_selected_evidence_rows)}</strong>
              <em>{formatNumber(counts.spatial_scale_evidence_rows)} spatial-scale rows</em>
            </div>
            <div>
              <span>Primary radius</span>
              <strong>{formatNumber(counts.primary_radius_km)} km</strong>
              <em>neighborhood-scale upper bound</em>
            </div>
            <div>
              <span>Sensitivity</span>
              <strong>{formatNumber(counts.lower_sensitivity_radius_km)} / {formatNumber(counts.upper_sensitivity_radius_km)} km</strong>
              <em>source-frozen bands</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_join_rows)}</strong>
              <em>identity still blocked</em>
            </div>
            <div>
              <span>Catchment rows</span>
              <strong>{formatNumber(counts.station_radius_population_rows)}</strong>
              <em>map still locked</em>
            </div>
          </div>

          <div className="air-radius-rule-source-grid" aria-label="Radius-rule public sources">
            {summary.source_rows.map((source) => (
              <article key={source.source_key} className={`air-radius-rule-source air-radius-rule-source-${source.retrieval_status}`}>
                <span>{sentenceCaseStatus(source.source_family)}</span>
                <strong>{source.title}</strong>
                <p>
                  {sentenceCaseStatus(source.retrieval_status)}; HTTP {source.http_status};
                  {" "}
                  {formatNumber(Number(source.content_length_bytes || 0))} bytes cached.
                </p>
                <a href={source.url}>Open source</a>
              </article>
            ))}
          </div>

          <div className="air-radius-rule-evidence-grid" aria-label="Selected radius-rule source evidence">
            {selectedEvidence.map((row) => (
              <article key={row.evidence_id} className={`air-radius-rule-evidence air-radius-rule-evidence-${row.evidence_role}`}>
                <span>{sentenceCaseStatus(row.evidence_role)}</span>
                <strong>{evidenceRadius(row)}</strong>
                <em>{row.extracted_scale}</em>
                <p>{row.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-radius-rule-gate-grid" aria-label="Radius-rule evidence gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-radius-rule-gate air-radius-rule-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-radius-rule-nonclaim">{summary.non_claim}</p>

          <div className="air-radius-rule-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-radius-rule-source-scan.md" download>
              Download source note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-radius-rule-source-scan-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-radius-rule-source-scan.csv" download>
              Download evidence CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius radius-rule source scan...</p>
      )}
    </section>
  );
}

function AirStationRadiusPm25ResolutionPanel({ summary }: { summary: StationRadiusPm25ResolutionSummary | null }) {
  const counts = summary?.coverage_counts;
  const decision = summary?.pm25_resolution_decision;
  const selectedRow = summary?.decision_rows.find((row) => String(row.selected).toLowerCase() === "true");
  const consistencyRows = summary?.decision_rows.filter((row) => String(row.selected).toLowerCase() !== "true") ?? [];
  const gateTone = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized.includes("available") || normalized.includes("frozen")) return "available";
    if (normalized.includes("not_computed") || normalized.includes("defer")) return "pending";
    return "blocked";
  };

  return (
    <section className="showcase-section air-pm25-resolution-section" aria-label="Station-radius PM2.5 resolution decision">
      <div className="air-pm25-resolution-head">
        <div>
          <p className="kicker kicker-blue">PM2.5 grid decision</p>
          <h2>The pollutant grid is frozen for a dry run, not for a claim.</h2>
          <p>
            This gate chooses the already check-summed ACAG coarse annual PM2.5
            lane for the next denominator join. It keeps fine-resolution and
            2024 objects out of the first pass until they are separately pinned.
          </p>
        </div>
        <div className="air-pm25-resolution-callout">
          <span>Grid state</span>
          <strong>{decision ? "PM2.5 resolution frozen" : "Loading"}</strong>
          <p>
            {counts
              ? `${formatNumber(counts.checksummed_coarse_pm25_files)} coarse files in custody; ${formatNumber(counts.station_radius_pm25_exposure_rows)} exposure rows.`
              : "Reading PM2.5 decision."}
          </p>
        </div>
      </div>

      {summary && counts && decision ? (
        <>
          <div className="air-pm25-resolution-flow" aria-label="PM2.5 resolution dry-run lanes">
            <article className="air-pm25-resolution-primary">
              <span>Primary dry-run surface</span>
              <strong>{decision.selected_version} {decision.selected_vintage}</strong>
              <em>{decision.selected_resolution}</em>
              <p>{selectedRow?.reader_use ?? "Global coarse PM2.5 grid selected for the first dry-run lane."}</p>
            </article>
            <article className="air-pm25-resolution-secondary">
              <span>Consistency lane</span>
              <strong>Asia coarse 2023</strong>
              <em>{consistencyRows[0]?.selected_resolution ?? decision.selected_resolution}</em>
              <p>{consistencyRows[0]?.reader_use ?? "Regional coarse PM2.5 grid retained for consistency checks."}</p>
            </article>
            <article className="air-pm25-resolution-deferred">
              <span>Deferred</span>
              <strong>{formatNumber(counts.fine_resolution_second_wave_or_deferred_objects)} fine objects</strong>
              <em>{formatNumber(counts.visible_latest_v6gl03_year)} visible but unselected</em>
              <p>{decision.deferred_lanes}</p>
            </article>
          </div>

          <div className="air-pm25-resolution-stat-grid">
            <div>
              <span>Coordinate rows</span>
              <strong>{formatNumber(counts.coordinate_rows_used)}</strong>
              <em>ready for dry-run join</em>
            </div>
            <div>
              <span>Population tiles</span>
              <strong>{formatNumber(counts.population_tile_files_in_custody)}</strong>
              <em>in custody</em>
            </div>
            <div>
              <span>Radius rule</span>
              <strong>{formatNumber(counts.primary_radius_km)} km</strong>
              <em>{formatNumber(counts.lower_sensitivity_radius_km)} / {formatNumber(counts.upper_sensitivity_radius_km)} km sensitivity</em>
            </div>
            <div>
              <span>PM2.5 files</span>
              <strong>{formatNumber(counts.checksummed_coarse_pm25_files)}</strong>
              <em>{formatNumber(counts.files_with_pm25_lat_lon)} with PM25(lat,lon)</em>
            </div>
            <div>
              <span>Exposure rows</span>
              <strong>{formatNumber(counts.station_radius_pm25_exposure_rows)}</strong>
              <em>not computed</em>
            </div>
            <div>
              <span>Ready economies</span>
              <strong>{formatNumber(counts.station_radius_ready_economies)}</strong>
              <em>join still blocked</em>
            </div>
          </div>

          <div className="air-pm25-resolution-row-grid" aria-label="PM2.5 resolution decision rows">
            {summary.decision_rows.map((row) => (
              <article key={row.decision_id} className={`air-pm25-resolution-row air-pm25-resolution-row-${row.grid_family}`}>
                <span>{sentenceCaseStatus(row.decision_role)}</span>
                <strong>{row.acag_record_key}</strong>
                <em>{row.selected_resolution}; {row.dimensions}</em>
                <p>{row.claim_guardrail}</p>
              </article>
            ))}
          </div>

          <div className="air-pm25-resolution-gate-grid" aria-label="PM2.5 resolution gates">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-pm25-resolution-gate air-pm25-resolution-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-pm25-resolution-nonclaim">{summary.non_claim}</p>

          <div className="air-pm25-resolution-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-pm25-resolution-decision.md" download>
              Download decision note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-pm25-resolution-decision-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-pm25-resolution-decision.csv" download>
              Download decision CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius PM2.5 resolution decision...</p>
      )}
    </section>
  );
}

function AirStationRadiusDenominatorJoinPanel({ summary }: { summary: StationRadiusDenominatorJoinSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.top_primary_radius_country_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const asNumber = (value: number | string | undefined) => {
    const parsed = Number(value ?? 0);
    return Number.isFinite(parsed) ? parsed : 0;
  };
  const compact = (value: number | string | undefined) => {
    const parsed = asNumber(value);
    if (parsed >= 1_000_000_000) return `${(parsed / 1_000_000_000).toFixed(1)}B`;
    if (parsed >= 1_000_000) return `${(parsed / 1_000_000).toFixed(1)}M`;
    if (parsed >= 1_000) return `${(parsed / 1_000).toFixed(1)}K`;
    return formatNumber(parsed);
  };
  const gateTone = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized.includes("computed")) return "computed";
    if (normalized.includes("not_ready") || normalized.includes("not_computed")) return "blocked";
    return "available";
  };
  const maxPopulation = Math.max(
    1,
    ...rows.map((row) => asNumber(row.candidate_population_exact_coordinate_dedup_sum)),
  );

  return (
    <section className="showcase-section air-denominator-join-section" aria-label="Station-radius denominator join dry run">
      <div className="air-denominator-join-head">
        <div>
          <p className="kicker kicker-crimson">Denominator join dry run</p>
          <h2>The buffers touch real cells; the claim still stops at the gate.</h2>
          <p>
            This pass connects the frozen candidate coordinate universe to GHSL population cells and the selected
            ACAG coarse annual PM2.5 grid. It is row-level denominator evidence, not a monitor-coverage statement.
          </p>
        </div>
        <div className="air-denominator-join-callout">
          <span>Join state</span>
          <strong>{counts ? `${formatNumber(counts.candidate_coordinate_radius_rows)} physical joins` : "Loading"}</strong>
          <p>
            {counts
              ? `${formatNumber(counts.station_radius_ready_economies)} ready economies; ${formatNumber(counts.country_union_population_rows)} unioned catchment rows.`
              : "Reading denominator dry run."}
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-denominator-join-flow" aria-label="Denominator join evidence flow">
            <article>
              <span>Frozen coordinate universe</span>
              <strong>{formatNumber(counts.coordinate_rows_used)}</strong>
              <em>{formatNumber(counts.unique_coordinate_points)} unique points</em>
              <p>OpenAQ and official PM2.5 coordinate rows are kept source-family separated.</p>
            </article>
            <article>
              <span>Denominators opened</span>
              <strong>{formatNumber(counts.population_raster_tiles_opened)} GHSL tiles</strong>
              <em>{summary.pm25_surface.record_key}</em>
              <p>The script opens cached ZIP/GeoTIFF tiles and the selected ACAG NetCDF surface.</p>
            </article>
            <article className="air-denominator-join-brake">
              <span>Claim brake</span>
              <strong>{formatNumber(counts.validated_same_station_join_rows)} joins</strong>
              <em>{formatNumber(counts.complete_monitor_grade_rows)} complete-grade rows</em>
              <p>Zero validated station joins and zero complete-grade rows keep coverage language blocked.</p>
            </article>
          </div>

          <div className="air-denominator-radius-band" aria-label="Computed radius bands">
            {summary.radius_bands.map((band) => (
              <article key={band.radius_role} className={`air-denominator-radius air-denominator-radius-${band.radius_role}`}>
                <span>{sentenceCaseStatus(band.radius_role)}</span>
                <strong>{formatNumber(band.radius_km, band.radius_km < 1 ? 1 : 0)} km</strong>
                <em>{band.radius_role === "primary" ? "source-frozen diagnostic band" : "sensitivity band"}</em>
              </article>
            ))}
          </div>

          <div className="air-denominator-country-grid" aria-label="Primary 4 km denominator diagnostics by economy">
            {rows.map((row) => {
              const population = asNumber(row.candidate_population_exact_coordinate_dedup_sum);
              const width = `${Math.max(4, (population / maxPopulation) * 100)}%`;
              return (
                <article key={row.iso3} className="air-denominator-country-row">
                  <div>
                    <span>{row.iso3}</span>
                    <strong>{row.country}</strong>
                    <em>{formatNumber(row.coordinate_rows)} rows; {formatNumber(row.unique_coordinate_points)} unique points</em>
                  </div>
                  <div className="air-denominator-country-bar">
                    <i style={{ width }} />
                  </div>
                  <dl>
                    <div>
                      <dt>Candidate population</dt>
                      <dd>{compact(population)}</dd>
                    </div>
                    <div>
                      <dt>Nearest PM2.5</dt>
                      <dd>{formatNumber(asNumber(row.mean_pm25_nearest_ugm3), 1)}</dd>
                    </div>
                    <div>
                      <dt>Tiles</dt>
                      <dd>{formatNumber(row.ghsl_tile_count)}</dd>
                    </div>
                  </dl>
                </article>
              );
            })}
          </div>

          <div className="air-denominator-gate-grid" aria-label="Denominator join gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-denominator-gate air-denominator-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-denominator-nonclaim">{summary.non_claim}</p>

          <div className="air-denominator-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-denominator-join-dry-run.md" download>
              Download evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-join-dry-run-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-join-dry-run-country.csv" download>
              Download country CSV
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-denominator-join-dry-run.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius denominator join dry run...</p>
      )}
    </section>
  );
}

function AirStationRadiusCountryUnionPanel({ summary }: { summary: StationRadiusCountryUnionSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.top_primary_radius_country_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const asNumber = (value: number | string | undefined) => {
    const parsed = Number(value ?? 0);
    return Number.isFinite(parsed) ? parsed : 0;
  };
  const truthy = (value: boolean | string | undefined) =>
    value === true || String(value ?? "").toLowerCase() === "true";
  const compact = (value: number | string | undefined) => {
    const parsed = asNumber(value);
    if (parsed >= 1_000_000_000) return `${(parsed / 1_000_000_000).toFixed(1)}B`;
    if (parsed >= 1_000_000) return `${(parsed / 1_000_000).toFixed(1)}M`;
    if (parsed >= 1_000) return `${(parsed / 1_000).toFixed(1)}K`;
    return formatNumber(parsed);
  };
  const gateTone = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized.includes("computed")) return "computed";
    if (normalized.includes("blocked") || normalized.includes("not_ready")) return "blocked";
    return "available";
  };
  const top = rows[0];
  const maxRowBuffer = Math.max(
    1,
    ...rows.map((row) => asNumber(row.row_level_candidate_population_buffer_sum)),
  );

  return (
    <section className="showcase-section air-denominator-join-section air-union-section" aria-label="Station-radius country-unioned catchment dry run">
      <div className="air-denominator-join-head">
        <div>
          <p className="kicker kicker-crimson">Country-unioned dry run</p>
          <h2>Unioning turns the pile-up into a method warning.</h2>
          <p>
            This pass counts each GHSL population cell once within an economy and radius band. It exposes how much
            duplicate buffer mass was in the row-level diagnostic, while keeping the result outside coverage language.
          </p>
        </div>
        <div className="air-denominator-join-callout air-union-callout">
          <span>Largest primary contrast</span>
          <strong>
            {top ? `${formatNumber(asNumber(top.row_to_union_population_multiplier), 2)}x row buffer` : "Loading"}
          </strong>
          <p>
            {top
              ? `${top.iso3}: ${compact(top.row_level_candidate_population_buffer_sum)} row-buffer sum vs ${compact(top.unioned_population_sum)} unioned denominator.`
              : "Reading country-unioned catchment dry run."}
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-denominator-join-flow" aria-label="Country-unioned catchment evidence flow">
            <article>
              <span>Unioned denominator rows</span>
              <strong>{formatNumber(counts.country_union_rows_computed)}</strong>
              <em>{formatNumber(counts.radius_bands_computed)} radius bands</em>
              <p>Each row is an economy/radius union of candidate-coordinate GHSL cells.</p>
            </article>
            <article>
              <span>Overlap made visible</span>
              <strong>{top ? compact(top.population_overlap_removed_from_row_sum) : "Loading"}</strong>
              <em>{top ? `${top?.iso3} row-buffer overlap` : "primary 4 km contrast"}</em>
              <p>The comparison separates duplicate candidate-buffer mass from a unioned denominator.</p>
            </article>
            <article className="air-denominator-join-brake">
              <span>Claim brake</span>
              <strong>{formatNumber(counts.validated_same_station_join_rows)} joins</strong>
              <em>{formatNumber(counts.complete_monitor_grade_rows)} complete-grade rows</em>
              <p>Unioned geometry is not enough: station identity, grade evidence, and claim permission remain blocked.</p>
            </article>
          </div>

          <div className="air-denominator-country-grid air-union-country-grid" aria-label="Primary 4 km country-unioned diagnostics by economy">
            {rows.map((row) => {
              const unioned = asNumber(row.unioned_population_sum);
              const rowBuffer = asNumber(row.row_level_candidate_population_buffer_sum);
              const rowWidth = `${Math.max(4, (rowBuffer / maxRowBuffer) * 100)}%`;
              const unionWidth = `${Math.max(4, (unioned / maxRowBuffer) * 100)}%`;
              return (
                <article key={row.iso3} className="air-denominator-country-row air-union-country-row">
                  <div>
                    <span>{row.iso3}</span>
                    <strong>{row.country}</strong>
                    <em>{formatNumber(row.coordinate_rows)} rows; {formatNumber(row.unique_coordinate_points)} unique points</em>
                  </div>
                  <div className="air-union-bars" aria-label={`${row.country} row buffer versus unioned denominator`}>
                    <div>
                      <span>Row buffer</span>
                      <div className="air-union-bar air-union-bar-row">
                        <i style={{ width: rowWidth }} />
                      </div>
                    </div>
                    <div>
                      <span>Unioned</span>
                      <div className="air-union-bar air-union-bar-unioned">
                        <i style={{ width: unionWidth }} />
                      </div>
                    </div>
                  </div>
                  <dl>
                    <div>
                      <dt>Unioned denominator</dt>
                      <dd>{compact(unioned)}</dd>
                    </div>
                    <div>
                      <dt>Row/union</dt>
                      <dd>{formatNumber(asNumber(row.row_to_union_population_multiplier), 2)}x</dd>
                    </div>
                    <div>
                      <dt>ACAG cells</dt>
                      <dd>{truthy(row.unioned_pm25_computed) ? formatNumber(row.unioned_pm25_cell_count) : "0"}</dd>
                    </div>
                  </dl>
                </article>
              );
            })}
          </div>

          <div className="air-denominator-gate-grid" aria-label="Country union gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-denominator-gate air-denominator-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-denominator-nonclaim">{summary.non_claim}</p>

          <div className="air-denominator-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-country-unioned-catchment-dry-run.md" download>
              Download evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-country-unioned-catchment-dry-run-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-country-unioned-catchment-dry-run.csv" download>
              Download country CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius country-unioned catchment dry run...</p>
      )}
    </section>
  );
}

function AirStationRadiusClaimGatePanel({ summary }: { summary: StationRadiusClaimGateSummary | null }) {
  const counts = summary?.coverage_counts;
  const context = summary?.blocker_context_counts;
  const rows = summary?.display_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const asNumber = (value: number | string | undefined) => {
    const parsed = Number(value ?? 0);
    return Number.isFinite(parsed) ? parsed : 0;
  };
  const compact = (value: number | string | undefined, digits = 1) => {
    const parsed = asNumber(value);
    if (Math.abs(parsed) >= 1_000_000) return `${formatNumber(parsed / 1_000_000, digits)}m`;
    if (Math.abs(parsed) >= 1_000) return `${formatNumber(parsed / 1_000, digits)}k`;
    return formatNumber(parsed, digits);
  };
  const localGateTone = (status: string) => {
    const normalized = status.toLowerCase();
    if (normalized.includes("computed")) return "computed";
    if (normalized.includes("partly") || normalized.includes("partial")) return "partly";
    if (normalized.includes("blocked")) return "blocked";
    return "available";
  };
  const maxPopulation = Math.max(1, ...rows.map((row) => asNumber(row.unioned_population_sum)));
  const blockerCards = context
    ? [
        {
          label: "BMKG near-closure",
          value: context.bmkg_method_classified_rows,
          detail: `${formatNumber(context.bmkg_calibration_status_rows)} calibration/status rows; ${formatNumber(context.bmkg_station_specific_calibration_certificate_rows)} station certificates`,
        },
        {
          label: "Uzbekistan blocker rows",
          value: context.uzbekistan_unresolved_blocker_rows,
          detail: `${formatNumber(context.uzbekistan_endpoint_mismatch_rows)} endpoint mismatches; ${formatNumber(context.uzbekistan_air_portal_resolution_rows)} namespace closures`,
        },
        {
          label: "Georgia station-code closure",
          value: context.georgia_verified_report_closure_rows,
          detail: `${formatNumber(context.georgia_indicator_exact_station_code_rows)} exact indicator station-code rows`,
        },
      ]
    : [];

  return (
    <section className="showcase-section air-denominator-join-section air-claim-gate-section" aria-label="Station-radius coverage claim gate">
      <div className="air-denominator-join-head">
        <div>
          <p className="kicker kicker-crimson">Coverage claim gate</p>
          <h2>The map is allowed to be useful; the claim is not allowed through.</h2>
          <p>
            This gate reads the denominator geometry, same-station identity checks, and monitor-grade ledgers before the
            page can say anything that sounds like monitor coverage or people served.
          </p>
        </div>
        <div className="air-denominator-join-callout air-claim-gate-callout">
          <span>Coverage permission</span>
          <strong>{summary?.claim_rule.allowed ? "Allowed" : "Blocked"}</strong>
          <p>
            {counts
              ? `${formatNumber(counts.claim_allowed_country_rows)} of ${formatNumber(counts.primary_radius_country_rows_checked)} primary-radius economy rows can use coverage language.`
              : "Reading the coverage-claim rule."}
          </p>
        </div>
      </div>

      {summary && counts && context ? (
        <>
          <div className="air-claim-gate-rule">
            <span>Mechanical rule</span>
            <p>{summary.claim_rule.rule}</p>
          </div>

          <div className="air-denominator-join-flow air-claim-gate-flow" aria-label="Coverage claim gate evidence flow">
            <article>
              <span>Computed geometry</span>
              <strong>{formatNumber(counts.country_union_rows_computed)} union rows</strong>
              <em>{formatNumber(counts.denominator_join_rows)} row-level joins</em>
              <p>Country/radius denominators are computed, including the unioned GHSL population layer.</p>
            </article>
            <article className="air-denominator-join-brake">
              <span>Evidence lift still missing</span>
              <strong>{formatNumber(counts.validated_same_station_join_rows)} validated joins</strong>
              <em>{formatNumber(counts.complete_monitor_grade_rows)} complete-grade rows</em>
              <p>The station identity and grade prerequisites remain at zero.</p>
            </article>
            <article className="air-claim-gate-stop">
              <span>Near-closure is not closure</span>
              <strong>{formatNumber(context.bmkg_method_classified_rows)} BMKG method rows</strong>
              <em>{formatNumber(context.bmkg_calibration_status_rows)} certificates/status records</em>
              <p>Method and dashboard evidence improve the review queue, but they do not release coverage language.</p>
            </article>
          </div>

          <div className="air-denominator-gate-grid air-claim-gate-grid" aria-label="Coverage claim evidence gates">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-denominator-gate air-denominator-gate-${localGateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-claim-gate-row-grid" aria-label="Largest blocked primary-radius rows">
            {rows.map((row) => {
              const unioned = asNumber(row.unioned_population_sum);
              const width = `${Math.max(4, (unioned / maxPopulation) * 100)}%`;
              const missing = row.blocking_gaps.split("||").filter(Boolean);
              return (
                <article key={row.claim_gate_id} className="air-claim-gate-row">
                  <div>
                    <span>{row.iso3}</span>
                    <strong>{row.country}</strong>
                    <em>{formatNumber(row.coordinate_rows)} coordinate rows</em>
                  </div>
                  <div>
                    <span>Unioned denominator</span>
                    <strong>{compact(unioned)}</strong>
                    <div className="air-claim-gate-bar" aria-label={`${row.country} blocked denominator scale`}>
                      <i style={{ width }} />
                    </div>
                  </div>
                  <div>
                    <span>{sentenceCaseStatus(row.release_decision)}</span>
                    <p>{missing.join(", ")}</p>
                  </div>
                </article>
              );
            })}
          </div>

          <div className="air-claim-gate-blocker-grid" aria-label="Source-specific blocker context">
            {blockerCards.map((card) => (
              <article key={card.label} className="air-claim-gate-blocker">
                <span>{card.label}</span>
                <strong>{formatNumber(card.value)} rows</strong>
                <p>{card.detail}</p>
              </article>
            ))}
          </div>

          <p className="air-denominator-nonclaim">{summary.non_claim}</p>

          <div className="air-denominator-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-radius-coverage-claim-gate.md" download>
              Download evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-coverage-claim-gate-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-radius-coverage-claim-gate.csv" download>
              Download gate CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-radius coverage claim gate...</p>
      )}
    </section>
  );
}

function AirRegulatorSourcePanel({ summary }: { summary: RegulatorSourceSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.country_rows ?? [];
  const groups = [
    {
      key: "official",
      title: "Official inventory or portal",
      rows: rows.filter((row) => row.official_station_inventory_or_portal),
    },
    {
      key: "regulator-page",
      title: "Regulator page, no inventory found",
      rows: rows.filter((row) => row.source_class === "official_regulator_page_no_station_inventory"),
    },
    {
      key: "partner",
      title: "Development-partner reference",
      rows: rows.filter((row) => row.source_class === "development_partner_monitoring_reference"),
    },
    {
      key: "gap",
      title: "Targeted-search gap",
      rows: rows.filter((row) => row.source_class === "not_found_in_targeted_search"),
    },
  ];

  return (
    <section className="showcase-section air-regulator-section" aria-label="Regulator source inventory discovery">
      <div className="air-regulator-head">
        <div>
          <p className="kicker kicker-crimson">Regulator-source wall</p>
          <h2>Official sources start to answer what OpenAQ cannot.</h2>
          <p>
            The discovery pass checks whether each upgrade-queue economy has a
            public regulator, official portal, government project, or partner
            source that can be inspected before the report treats OpenAQ as a
            coverage statement.
          </p>
        </div>
        <div className="air-regulator-nonclaim">
          <strong>Still not validation</strong>
          <p>
            A source candidate is not a reconciled station table. Monitor-grade
            classification remains at zero rows until official station metadata
            distinguishes regulatory or reference monitors from other feeds.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-regulator-stat-grid">
            <div>
              <span>Official source candidates</span>
              <strong>{formatNumber(counts.economies_with_official_source_candidate)}</strong>
              <em>of {formatNumber(counts.economies_targeted)} upgrade-queue economies</em>
            </div>
            <div>
              <span>Inventory or portal candidates</span>
              <strong>{formatNumber(counts.economies_with_official_station_inventory_or_portal)}</strong>
              <em>not yet reconciled to OpenAQ rows</em>
            </div>
            <div>
              <span>Station-count claims</span>
              <strong>{formatNumber(counts.economies_with_official_station_count_claim)}</strong>
              <em>need station-table extraction</em>
            </div>
            <div>
              <span>Zero-OpenAQ search gaps</span>
              <strong>{formatNumber(counts.zero_openaq_economies_not_found_in_targeted_search)}</strong>
              <em>not proof that no monitor exists</em>
            </div>
            <div>
              <span>Monitor-grade rows</span>
              <strong>{formatNumber(counts.economies_with_monitor_grade_signal)}</strong>
              <em>classification still blocked</em>
            </div>
          </div>

          <div className="air-regulator-zero-grid">
            <div>
              <span>Zero-OpenAQ official portal</span>
              <strong>{formatNumber(counts.zero_openaq_economies_with_official_station_inventory_or_portal)}</strong>
            </div>
            <div>
              <span>Regulator page, no inventory</span>
              <strong>{formatNumber(counts.zero_openaq_economies_with_official_regulator_page_no_station_inventory)}</strong>
            </div>
            <div>
              <span>Partner monitoring reference</span>
              <strong>{formatNumber(counts.zero_openaq_economies_with_development_partner_monitoring_reference)}</strong>
            </div>
            <div>
              <span>Still targeted-search gaps</span>
              <strong>{formatNumber(counts.zero_openaq_economies_not_found_in_targeted_search)}</strong>
            </div>
          </div>

          <div className="air-regulator-source-grid">
            {groups.map((group) => (
              <article key={group.key} className={`air-regulator-group air-regulator-group-${group.key}`}>
                <div className="air-regulator-group-head">
                  <h3>{group.title}</h3>
                  <strong>{formatNumber(group.rows.length)}</strong>
                </div>
                <div className="air-regulator-country-stack">
                  {group.rows.map((row) => (
                    <div key={row.iso3} className="air-regulator-country">
                      <div>
                        <span>{row.iso3}</span>
                        <strong>{row.country}</strong>
                        {row.openaq_zero_pm25_rows ? <b>zero OpenAQ</b> : null}
                      </div>
                      <p>{row.source_name}</p>
                      <em>{row.official_station_count_claim || row.next_validation_step}</em>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>

          <div className="air-regulator-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-regulator-gate air-regulator-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-regulator-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/regulator-source-inventory.md" download>
              Source note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-regulator-source-inventory-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-regulator-source-inventory.csv" download>
              Inventory CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading regulator-source inventory...</p>
      )}
    </section>
  );
}

function extractionLevelLabel(level: string) {
  return sentenceCaseStatus(level).replace("station coordinates", "coordinate rows");
}

function gradeCategoryLabel(category: string) {
  switch (category) {
    case "method_standard_signal":
      return "method-standard signal";
    case "automatic_or_official_portal_signal":
      return "automatic or portal signal";
    case "sensor_under_test_signal":
      return "sensor under test";
    case "plan_only_no_grade":
      return "plan only";
    case "no_public_grade_language_found":
      return "no public grade language";
    default:
      return sentenceCaseStatus(category);
  }
}

function oneSignalLaneLabel(lane: string) {
  switch (lane) {
    case "near_only_candidate":
      return "Near only";
    case "name_overlap_not_near_candidate":
      return "Name only, not near";
    case "monitor_grade_provenance_only":
      return "Official or automatic only";
    default:
      return sentenceCaseStatus(lane);
  }
}

function monitorGradeSourceLaneLabel(lane: string) {
  switch (lane) {
    case "method_or_equipment_context_found":
      return "method or equipment";
    case "standard_or_method_context_found":
      return "standard or method";
    case "official_or_automatic_context_found":
      return "official or automatic";
    case "caution_language_found":
      return "caution";
    case "retrieval_failed":
      return "retrieval failed";
    case "source_context_only_no_grade_language":
      return "no grade language";
    default:
      return sentenceCaseStatus(lane);
  }
}

function monitorGradeStationLaneLabel(lane: string) {
  switch (lane) {
    case "method_context_needs_station_confirmation":
      return "method context";
    case "caution_blocks_grade":
      return "caution blocks grade";
    case "official_context_only":
      return "official context only";
    default:
      return sentenceCaseStatus(lane);
  }
}

function monitorGradeMethodLaneLabel(lane: string) {
  switch (lane) {
    case "row_level_instrument_hint":
      return "instrument hint";
    case "row_level_pm25_portal_or_api":
      return "PM2.5 portal/API";
    case "exact_row_not_found":
      return "row not found";
    default:
      return sentenceCaseStatus(lane);
  }
}

function AirRegulatorStationPanel({ summary }: { summary: RegulatorStationSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.country_rows ?? [];
  const coordinateCountries = rows
    .filter((row) => row.coordinate_rows > 0)
    .sort((a, b) => b.coordinate_rows - a.coordinate_rows);
  const nonCoordinateRows = rows.filter((row) => row.coordinate_rows === 0);
  const maxCoordinateRows = Math.max(1, ...coordinateCountries.map((row) => row.coordinate_rows));

  return (
    <section className="showcase-section air-regulator-station-section" aria-label="Official station-source extraction">
      <div className="air-regulator-station-head">
        <div>
          <p className="kicker kicker-blue">Station-table extraction</p>
          <h2>The official map is wider than the OpenAQ map.</h2>
          <p>
            The second source pass extracts station tables and public portal
            rows from the official candidates. It separates hard coordinate
            evidence from named stations, network counts, and project plans,
            then compares official coordinates with OpenAQ as a screening
            diagnostic.
          </p>
        </div>
        <div className="air-regulator-station-nonclaim">
          <strong>Proximity is not a match</strong>
          <p>
            A station within 5 km of an OpenAQ row is only a candidate for
            reconciliation. A station outside 5 km is not proof that OpenAQ is
            wrong. Monitor-grade and catchment claims remain blocked.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-regulator-station-stat-grid">
            <div>
              <span>Official coordinate rows</span>
              <strong>{formatNumber(counts.official_station_coordinate_rows)}</strong>
              <em>from {formatNumber(counts.countries_with_station_coordinates)} economies</em>
            </div>
            <div>
              <span>Near OpenAQ rows</span>
              <strong>{formatNumber(counts.official_coordinate_rows_near_openaq_within_5km)}</strong>
              <em>within 5 km, screening only</em>
            </div>
            <div>
              <span>Not near OpenAQ rows</span>
              <strong>{formatNumber(counts.official_coordinate_rows_not_near_openaq_within_5km)}</strong>
              <em>requires source reconciliation</em>
            </div>
            <div>
              <span>Name/count/plan rows</span>
              <strong>
                {formatNumber(
                  counts.official_station_name_only_rows +
                    counts.official_count_only_rows +
                    counts.official_plan_count_only_rows,
                )}
              </strong>
              <em>not catchment-ready</em>
            </div>
            <div>
              <span>Monitor-grade rows</span>
              <strong>{formatNumber(counts.monitor_grade_rows)}</strong>
              <em>still blocked</em>
            </div>
          </div>

          <div className="air-official-reconciliation">
            <div className="air-official-bars" aria-label="Official coordinate rows compared with OpenAQ proximity candidates">
              <div className="air-official-bars-head">
                <span>Official coordinate rows by source</span>
                <b>{formatNumber(counts.official_station_coordinate_rows)} total</b>
              </div>
              {coordinateCountries.map((row) => {
                const officialWidth = `${Math.max(5, (row.coordinate_rows / maxCoordinateRows) * 100)}%`;
                const nearWidth = `${Math.max(
                  row.nearest_openaq_within_5km_rows > 0 ? 3 : 0,
                  (row.nearest_openaq_within_5km_rows / row.coordinate_rows) * 100,
                )}%`;
                return (
                  <div key={row.iso3} className="air-official-bar-row">
                    <div className="air-official-bar-label">
                      <span>{row.iso3}</span>
                      <strong>{row.country}</strong>
                    </div>
                    <div className="air-official-bar-track">
                      <i style={{ width: officialWidth }} />
                      <b style={{ width: nearWidth }} />
                    </div>
                    <div className="air-official-bar-values">
                      <strong>{formatNumber(row.coordinate_rows)}</strong>
                      <span>{formatNumber(row.nearest_openaq_within_5km_rows)} near</span>
                      <em>{formatNumber(row.openaq_country_rows)} OpenAQ</em>
                    </div>
                  </div>
                );
              })}
              <div className="air-official-legend">
                <span><i /> official coordinate rows</span>
                <span><b /> within 5 km of OpenAQ</span>
              </div>
            </div>

            <div className="air-official-limited">
              <h3>Useful, but not coordinate-ready</h3>
              {nonCoordinateRows.map((row) => (
                <div key={row.iso3} className={`air-official-limited-row air-official-limited-${row.source_extraction_level}`}>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{extractionLevelLabel(row.source_extraction_level)}</b>
                  <p>{row.source_station_count_claim || row.source_name}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="air-regulator-station-country-grid">
            {rows.map((row) => (
              <article key={row.iso3} className={`air-regulator-station-country air-regulator-station-country-${row.source_extraction_level}`}>
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{extractionLevelLabel(row.source_extraction_level)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Official rows</dt>
                    <dd>{formatNumber(row.official_rows_extracted)}</dd>
                  </div>
                  <div>
                    <dt>Coordinates</dt>
                    <dd>{formatNumber(row.coordinate_rows)}</dd>
                  </div>
                  <div>
                    <dt>PM2.5 signal</dt>
                    <dd>{formatNumber(row.pm25_signal_rows)}</dd>
                  </div>
                  <div>
                    <dt>Near OpenAQ</dt>
                    <dd>{formatNumber(row.nearest_openaq_within_5km_rows)}</dd>
                  </div>
                </dl>
                <p>{row.source_station_count_claim || row.source_name}</p>
              </article>
            ))}
          </div>

          <div className="air-regulator-station-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-regulator-station-gate air-regulator-station-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-regulator-station-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/regulator-station-extraction.md" download>
              Extraction note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-regulator-station-extraction-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-regulator-station-extraction.csv" download>
              Station CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading official station-source extraction...</p>
      )}
    </section>
  );
}

function AirOfficialOpenAQPanel({ summary }: { summary: OfficialOpenAQSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = [...(summary?.country_rows ?? [])].sort(
    (a, b) => b.official_coordinate_rows - a.official_coordinate_rows,
  );
  const totalRows = Math.max(1, counts?.official_coordinate_rows_audited ?? 0);
  const lanes = counts
    ? [
        {
          key: "near-name",
          label: "Near + name",
          rows: counts.near_and_name_overlap_candidate_rows,
          detail: "candidate only; still not a same-station join",
          tone: "strong",
        },
        {
          key: "near",
          label: "Near only",
          rows: counts.near_only_candidate_rows,
          detail: "within 5 km, without name overlap",
          tone: "near",
        },
        {
          key: "name",
          label: "Name only",
          rows: counts.name_overlap_not_near_candidate_rows,
          detail: "name signal without the proximity signal",
          tone: "name",
        },
        {
          key: "none",
          label: "No candidate",
          rows: counts.official_coordinate_without_openaq_candidate_rows,
          detail: "official coordinate rows needing source review",
          tone: "none",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-official-openaq-section" aria-label="Official to OpenAQ reconciliation audit">
      <div className="air-official-openaq-head">
        <div>
          <p className="kicker kicker-blue">Official/OpenAQ reconciliation</p>
          <h2>A candidate join is still not a station crosswalk.</h2>
          <p>
            The audit turns the proximity diagnostic into a reconciliation
            ladder. It keeps official station rows and OpenAQ rows separate
            unless both signals are visible, and even then the row remains a
            candidate until a station ID or source crosswalk validates it.
          </p>
        </div>
        <div className="air-official-openaq-nonclaim">
          <strong>Validated joins remain zero</strong>
          <p>
            {formatNumber(counts?.validated_same_station_rows ?? 0)} rows are
            validated same-station joins. Catchment analysis should wait until
            candidates become documented station crosswalk rows.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-official-openaq-stat-grid">
            <div>
              <span>Official coordinates</span>
              <strong>{formatNumber(counts.official_coordinate_rows_audited)}</strong>
              <em>{formatNumber(counts.countries_with_official_coordinate_rows)} economies</em>
            </div>
            <div>
              <span>OpenAQ coordinates</span>
              <strong>{formatNumber(counts.openaq_coordinate_rows_in_official_coordinate_countries)}</strong>
              <em>same official-coordinate economies</em>
            </div>
            <div>
              <span>Near + name candidates</span>
              <strong>{formatNumber(counts.near_and_name_overlap_candidate_rows)}</strong>
              <em>most plausible lane</em>
            </div>
            <div>
              <span>One-signal candidates</span>
              <strong>
                {formatNumber(counts.near_only_candidate_rows + counts.name_overlap_not_near_candidate_rows)}
              </strong>
              <em>review queue, not joins</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_rows)}</strong>
              <em>station-radius blocked</em>
            </div>
          </div>

          <div className="air-official-openaq-lanes" aria-label="Official to OpenAQ reconciliation lanes">
            {lanes.map((lane) => {
              const width = lane.rows > 0 ? `${Math.max(5, (lane.rows / totalRows) * 100)}%` : "0%";
              return (
                <article key={lane.key} className={`air-official-openaq-lane air-official-openaq-lane-${lane.tone}`}>
                  <div>
                    <span>{lane.label}</span>
                    <strong>{formatNumber(lane.rows)}</strong>
                  </div>
                  <div className="air-official-openaq-track">
                    <i style={{ width }} />
                  </div>
                  <p>{lane.detail}</p>
                </article>
              );
            })}
          </div>

          <div className="air-official-openaq-country-grid">
            {rows.map((row) => (
              <article key={row.iso3} className="air-official-openaq-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.validated_same_station_rows)} validated</b>
                </div>
                <dl>
                  <div>
                    <dt>Official</dt>
                    <dd>{formatNumber(row.official_coordinate_rows)}</dd>
                  </div>
                  <div>
                    <dt>OpenAQ</dt>
                    <dd>{formatNumber(row.openaq_coordinate_rows)}</dd>
                  </div>
                  <div>
                    <dt>Near+name</dt>
                    <dd>{formatNumber(row.near_and_name_overlap_candidate_rows)}</dd>
                  </div>
                  <div>
                    <dt>One signal</dt>
                    <dd>{formatNumber(row.near_only_candidate_rows + row.name_overlap_not_near_candidate_rows)}</dd>
                  </div>
                  <div>
                    <dt>No candidate</dt>
                    <dd>{formatNumber(row.official_coordinate_without_openaq_candidate_rows)}</dd>
                  </div>
                </dl>
                <p>
                  {formatNumber(row.openaq_rows_not_used_as_near_candidate)} OpenAQ rows are not used as a near
                  candidate by any official coordinate row.
                </p>
              </article>
            ))}
          </div>

          <div className="air-official-openaq-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-official-openaq-gate air-official-openaq-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-official-openaq-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/official-openaq-reconciliation.md" download>
              Audit note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-reconciliation-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-reconciliation.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading official-to-OpenAQ reconciliation audit...</p>
      )}
    </section>
  );
}

function AirOfficialOpenAQCandidatePanel({ summary }: { summary: OfficialOpenAQCandidateSummary | null }) {
  const counts = summary?.coverage_counts;
  const countryRows = [...(summary?.country_rows ?? [])].sort((a, b) => b.candidate_rows - a.candidate_rows);
  const candidateRows = [...(summary?.candidate_rows ?? [])]
    .sort((a, b) => (a.nearest_openaq_distance_km ?? 999999) - (b.nearest_openaq_distance_km ?? 999999))
    .slice(0, 6);
  const flow = counts
    ? [
        {
          key: "queue",
          label: "Review queue",
          rows: counts.candidate_rows,
          detail: "near plus name signal",
          tone: "queue",
        },
        {
          key: "crosswalk",
          label: "Crosswalk evidence",
          rows: counts.rows_with_station_id_crosswalk,
          detail: "shared ID or documented crosswalk",
          tone: "blocked",
        },
        {
          key: "confirmed",
          label: "Current-status evidence",
          rows: counts.rows_with_public_current_status_confirmation,
          detail: "public confirmation naming both records",
          tone: "blocked",
        },
        {
          key: "ready",
          label: "Radius-ready joins",
          rows: counts.station_radius_join_ready_rows,
          detail: "usable in catchment analysis",
          tone: "blocked",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-openaq-candidate-section" aria-label="Official OpenAQ candidate review worksheet">
      <div className="air-openaq-candidate-head">
        <div>
          <p className="kicker kicker-blue">Candidate station-crosswalk review</p>
          <h2>The strongest candidates still need proof.</h2>
          <p>
            The worksheet filters the reconciliation audit to the near-plus-name
            lane and turns each row into a reviewer question. It shows exactly
            what public evidence would be needed before a candidate becomes a
            station crosswalk.
          </p>
        </div>
        <div className="air-openaq-candidate-nonclaim">
          <strong>Worksheet, not validation</strong>
          <p>
            {formatNumber(counts?.validated_same_station_rows ?? 0)} rows are
            validated same-station joins and {formatNumber(counts?.station_radius_join_ready_rows ?? 0)} rows are
            station-radius-ready.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-openaq-candidate-stat-grid">
            <div>
              <span>Candidate rows</span>
              <strong>{formatNumber(counts.candidate_rows)}</strong>
              <em>{formatNumber(counts.countries_with_candidates)} economies</em>
            </div>
            <div>
              <span>Near + name</span>
              <strong>{formatNumber(counts.near_plus_name_candidate_rows)}</strong>
              <em>worksheet selection rule</em>
            </div>
            <div>
              <span>Still open</span>
              <strong>{formatNumber(counts.insufficient_public_evidence_rows)}</strong>
              <em>not yet validated</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_rows)}</strong>
              <em>crosswalk remains empty</em>
            </div>
          </div>

          <div className="air-openaq-candidate-flow" aria-label="Candidate review flow">
            {flow.map((step) => (
              <article key={step.key} className={`air-openaq-candidate-flow-card air-openaq-candidate-flow-card-${step.tone}`}>
                <span>{step.label}</span>
                <strong>{formatNumber(step.rows)}</strong>
                <p>{step.detail}</p>
              </article>
            ))}
          </div>

          <div className="air-openaq-candidate-rule">
            <div>
              <span>Minimum validation evidence</span>
              <p>{summary.minimum_validation_evidence}</p>
            </div>
            <div>
              <span>Allowed decisions</span>
              <ul>
                {summary.allowed_decisions.map((decision) => (
                  <li key={decision}>{sentenceCaseStatus(decision)}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="air-openaq-candidate-country-grid">
            {countryRows.map((row) => (
              <article key={row.iso3} className="air-openaq-candidate-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.candidate_rows)} open</b>
                </div>
                <dl>
                  <div>
                    <dt>OpenAQ IDs</dt>
                    <dd>{formatNumber(row.unique_openaq_candidate_ids)}</dd>
                  </div>
                  <div>
                    <dt>Min km</dt>
                    <dd>{formatNumber(row.minimum_distance_km, 3)}</dd>
                  </div>
                  <div>
                    <dt>Max km</dt>
                    <dd>{formatNumber(row.maximum_distance_km, 3)}</dd>
                  </div>
                  <div>
                    <dt>Validated</dt>
                    <dd>{formatNumber(row.validated_same_station_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-openaq-candidate-row-list">
            {candidateRows.map((row) => (
              <article key={row.candidate_review_id} className="air-openaq-candidate-row">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{formatNumber(row.nearest_openaq_distance_km, 3)} km</b>
                </div>
                <p>
                  OpenAQ: {row.nearest_openaq_location_name}
                </p>
                <p>{sentenceCaseStatus(row.public_evidence_status)}</p>
              </article>
            ))}
          </div>

          <div className="air-openaq-candidate-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-openaq-candidate-gate air-openaq-candidate-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-openaq-candidate-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/official-openaq-candidate-review.md" download>
              Worksheet note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-review-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-review.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading official/OpenAQ candidate review worksheet...</p>
      )}
    </section>
  );
}

function AirOfficialOpenAQCandidateEvidencePanel({
  summary,
}: {
  summary: OfficialOpenAQCandidateEvidenceSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const countryRows = [...(summary?.country_rows ?? [])].sort((a, b) => b.candidate_rows - a.candidate_rows);
  const evidenceRows = [...(summary?.candidate_rows ?? [])]
    .sort((a, b) => Number(b.openaq_is_monitor) - Number(a.openaq_is_monitor))
    .slice(0, 6);
  const laneRows = summary?.evidence_lane_counts ?? [];

  return (
    <section className="showcase-section air-openaq-evidence-section" aria-label="Official OpenAQ candidate public evidence audit">
      <div className="air-openaq-evidence-head">
        <div>
          <p className="kicker kicker-blue">Candidate public evidence</p>
          <h2>OpenAQ metadata sharpens the queue, but does not close it.</h2>
          <p>
            This pass attaches owner/provider, isMonitor, sensor-count, and
            vintage fields to the 13 candidate rows. The split helps reviewers
            decide what to inspect next while keeping validated joins at zero.
          </p>
        </div>
        <div className="air-openaq-evidence-nonclaim">
          <strong>No crosswalk found</strong>
          <p>
            Crosswalk rows: {formatNumber(counts?.rows_with_explicit_crosswalk_evidence ?? 0)}.
            Validated joins: {formatNumber(counts?.validated_same_station_rows ?? 0)}.
            Radius-ready rows: {formatNumber(counts?.station_radius_join_ready_rows ?? 0)}.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-openaq-evidence-stat-grid">
            <div>
              <span>Candidate rows</span>
              <strong>{formatNumber(counts.candidate_rows_audited)}</strong>
              <em>{formatNumber(counts.unique_openaq_candidate_ids)} OpenAQ IDs</em>
            </div>
            <div>
              <span>Owner/provider</span>
              <strong>{formatNumber(counts.rows_with_openaq_owner_or_provider)}</strong>
              <em>metadata present</em>
            </div>
            <div>
              <span>isMonitor true</span>
              <strong>{formatNumber(counts.rows_with_openaq_is_monitor_true)}</strong>
              <em>not grade certification</em>
            </div>
            <div>
              <span>Not isMonitor</span>
              <strong>{formatNumber(counts.rows_with_openaq_is_monitor_false)}</strong>
              <em>nearby public-feed caution</em>
            </div>
            <div>
              <span>Explicit crosswalk</span>
              <strong>{formatNumber(counts.rows_with_explicit_crosswalk_evidence)}</strong>
              <em>still missing</em>
            </div>
          </div>

          <div className="air-openaq-evidence-lanes">
            {laneRows.map((lane) => (
              <article key={lane.lane} className={`air-openaq-evidence-lane air-openaq-evidence-lane-${lane.lane}`}>
                <span>{sentenceCaseStatus(lane.lane)}</span>
                <strong>{formatNumber(lane.rows)}</strong>
              </article>
            ))}
          </div>

          <div className="air-openaq-evidence-country-grid">
            {countryRows.map((row) => (
              <article key={row.iso3} className="air-openaq-evidence-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.candidate_rows)} candidates</b>
                </div>
                <dl>
                  <div>
                    <dt>Monitor</dt>
                    <dd>{formatNumber(row.openaq_is_monitor_true_rows)}</dd>
                  </div>
                  <div>
                    <dt>Not monitor</dt>
                    <dd>{formatNumber(row.openaq_is_monitor_false_rows)}</dd>
                  </div>
                  <div>
                    <dt>First seen</dt>
                    <dd>{formatNumber(row.rows_with_first_seen)}</dd>
                  </div>
                  <div>
                    <dt>Crosswalk</dt>
                    <dd>{formatNumber(row.crosswalk_like_public_signal_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-openaq-evidence-row-grid">
            {evidenceRows.map((row) => (
              <article key={row.candidate_review_id} className={row.openaq_is_monitor ? "air-openaq-evidence-row is-monitor" : "air-openaq-evidence-row"}>
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.nearest_openaq_location_name}</strong>
                  <b>{row.openaq_is_monitor ? "isMonitor" : "not isMonitor"}</b>
                </div>
                <p>
                  {row.openaq_provider_name || row.openaq_owner_name || "Owner/provider missing"}; official row: {row.source_station_name}
                </p>
              </article>
            ))}
          </div>

          <div className="air-openaq-evidence-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-openaq-evidence-gate air-openaq-evidence-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-openaq-evidence-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/official-openaq-candidate-public-evidence.md" download>
              Evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-public-evidence-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-public-evidence.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading candidate public-evidence audit...</p>
      )}
    </section>
  );
}

function AirCandidateCrosswalkSourceScanPanel({
  summary,
}: {
  summary: CandidateCrosswalkSourceScanSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const rows = summary?.candidate_rows ?? [];
  const sourceRows = summary?.source_rows ?? [];

  return (
    <section className="showcase-section air-crosswalk-scan-section" aria-label="Official OpenAQ candidate crosswalk source scan">
      <div className="air-crosswalk-scan-head">
        <div>
          <p className="kicker kicker-crimson">Crosswalk source scan</p>
          <h2>The strongest candidate joins split apart under public sources.</h2>
          <p>
            The 6 OpenAQ isMonitor candidates were checked first. Public source
            pages separate all 6 as nearby stations, so validated joins and
            radius-ready rows stay at zero.
          </p>
        </div>
        <div className="air-crosswalk-scan-callout">
          <span>Decision</span>
          <strong>{formatNumber(counts?.rows_screened_as_separate_nearby_stations ?? 0)}</strong>
          <p>screened as separate nearby stations</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-crosswalk-scan-stat-grid">
            <div>
              <span>Rows scanned</span>
              <strong>{formatNumber(counts.is_monitor_candidate_rows_scanned)}</strong>
              <em>OpenAQ isMonitor candidates</em>
            </div>
            <div>
              <span>Separate nearby</span>
              <strong>{formatNumber(counts.rows_screened_as_separate_nearby_stations)}</strong>
              <em>not join-ready</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_rows)}</strong>
              <em>still zero</em>
            </div>
            <div>
              <span>Source URLs</span>
              <strong>{formatNumber(counts.source_urls_retrieved)}</strong>
              <em>{formatNumber(counts.source_urls_seeded)} seeded</em>
            </div>
            <div>
              <span>Not isMonitor</span>
              <strong>{formatNumber(counts.non_monitor_candidate_rows_not_scanned)}</strong>
              <em>handled below</em>
            </div>
          </div>

          <div className="air-crosswalk-scan-country-grid">
            {summary.country_rows.map((row) => (
              <article key={row.iso3} className="air-crosswalk-scan-country">
                <span>{row.iso3}</span>
                <strong>{row.country}</strong>
                <b>{formatNumber(row.separate_nearby_station_rows)} separate / {formatNumber(row.rows_scanned)} scanned</b>
                <p>{formatNumber(row.validated_same_station_rows)} validated joins; {formatNumber(row.station_radius_join_ready_rows)} radius-ready rows.</p>
              </article>
            ))}
          </div>

          <div className="air-crosswalk-scan-row-grid">
            {rows.map((row) => (
              <article key={row.candidate_review_id} className="air-crosswalk-scan-row">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{row.nearest_openaq_location_name}</b>
                </div>
                <p>{row.reader_use}</p>
                <small>
                  Distance: {row.computed_coordinate_distance_km !== null ? `${formatNumber(row.computed_coordinate_distance_km, 3)} km computed` : `${formatNumber(row.nearest_openaq_distance_km, 3)} km candidate diagnostic`}
                </small>
              </article>
            ))}
          </div>

          <div className="air-crosswalk-scan-source-grid">
            {sourceRows.map((source) => (
              <article key={source.source_key} className={source.retrieved ? "air-crosswalk-scan-source is-retrieved" : "air-crosswalk-scan-source"}>
                <span>{sentenceCaseStatus(source.source_role)}</span>
                <strong>{sentenceCaseStatus(source.source_key)}</strong>
                <b>{source.retrieved ? "retrieved" : "not retrieved"} · {formatNumber(source.matched_terms.length)} matched terms</b>
                <p>{source.source_note}</p>
              </article>
            ))}
          </div>

          <div className="air-crosswalk-scan-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/official-openaq-candidate-crosswalk-source-scan.md" download>
              Evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-crosswalk-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading candidate crosswalk source scan...</p>
      )}
    </section>
  );
}

function AirCandidatePublicFeedSourceScanPanel({
  summary,
}: {
  summary: CandidatePublicFeedSourceScanSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const rows = summary?.candidate_rows ?? [];
  const sourceRows = summary?.source_rows ?? [];

  return (
    <section className="showcase-section air-public-feed-scan-section" aria-label="Official OpenAQ candidate public-feed source scan">
      <div className="air-public-feed-scan-head">
        <div>
          <p className="kicker kicker-crimson">Public-feed source scan</p>
          <h2>The nearby public feeds stay out of the station crosswalk.</h2>
          <p>
            The 7 candidate rows not marked isMonitor in OpenAQ were checked
            against official coordinates and provider-context pages. All 7 stay
            public-feed nearby rows, not validated joins.
          </p>
        </div>
        <div className="air-public-feed-scan-callout">
          <span>Decision</span>
          <strong>{formatNumber(counts?.rows_screened_public_feed_nearby_not_join_ready ?? 0)}</strong>
          <p>public-feed rows not join-ready</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-public-feed-scan-stat-grid">
            <div>
              <span>Rows scanned</span>
              <strong>{formatNumber(counts.public_feed_candidate_rows_scanned)}</strong>
              <em>not isMonitor in OpenAQ</em>
            </div>
            <div>
              <span>Not join-ready</span>
              <strong>{formatNumber(counts.rows_screened_public_feed_nearby_not_join_ready)}</strong>
              <em>public-feed nearby rows</em>
            </div>
            <div>
              <span>Validated joins</span>
              <strong>{formatNumber(counts.validated_same_station_rows)}</strong>
              <em>still zero</em>
            </div>
            <div>
              <span>Source URLs</span>
              <strong>{formatNumber(counts.source_urls_retrieved)}</strong>
              <em>{formatNumber(counts.source_urls_seeded)} seeded</em>
            </div>
            <div>
              <span>Reused OpenAQ</span>
              <strong>{formatNumber(counts.same_openaq_location_reused_rows)}</strong>
              <em>duplicate nearest feed rows</em>
            </div>
          </div>

          <div className="air-public-feed-scan-country-grid">
            {summary.country_rows.map((row) => (
              <article key={row.iso3} className="air-public-feed-scan-country">
                <span>{row.iso3}</span>
                <strong>{row.country}</strong>
                <b>{formatNumber(row.public_feed_not_join_ready_rows)} not join-ready / {formatNumber(row.rows_scanned)} scanned</b>
                <p>{formatNumber(row.validated_same_station_rows)} validated joins; {formatNumber(row.station_radius_join_ready_rows)} radius-ready rows.</p>
              </article>
            ))}
          </div>

          <div className="air-public-feed-scan-row-grid">
            {rows.map((row) => (
              <article key={row.candidate_review_id} className={row.same_openaq_location_reused_in_scan ? "air-public-feed-scan-row has-reuse" : "air-public-feed-scan-row"}>
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{row.nearest_openaq_location_name}</b>
                </div>
                <p>{row.reader_use}</p>
                <small>
                  {row.openaq_owner_name} / {row.openaq_provider_name} · {row.computed_coordinate_distance_km !== null ? `${formatNumber(row.computed_coordinate_distance_km, 3)} km` : `${formatNumber(row.nearest_openaq_distance_km, 3)} km`}
                </small>
              </article>
            ))}
          </div>

          <div className="air-public-feed-scan-source-grid">
            {sourceRows.map((source) => (
              <article key={source.source_key} className={source.retrieved ? "air-public-feed-scan-source is-retrieved" : "air-public-feed-scan-source"}>
                <span>{sentenceCaseStatus(source.source_role)}</span>
                <strong>{sentenceCaseStatus(source.source_key)}</strong>
                <b>{source.retrieved ? "retrieved" : "not retrieved"} · {formatNumber(source.matched_terms.length)} matched terms</b>
                <p>{source.source_note}</p>
              </article>
            ))}
          </div>

          <div className="air-public-feed-scan-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/official-openaq-candidate-public-feed-source-scan.md" download>
              Evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-official-openaq-candidate-public-feed-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading candidate public-feed source scan...</p>
      )}
    </section>
  );
}

function AirOneSignalReviewQueuePanel({
  summary,
}: {
  summary: OneSignalReviewQueueSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const laneRows = summary?.lane_rows ?? [];
  const countryRows = [...(summary?.country_rows ?? [])].sort((a, b) => b.queue_items - a.queue_items);
  const sourceRows = [...(summary?.source_rows ?? [])].sort((a, b) => b.queue_items - a.queue_items).slice(0, 8);
  const sampleRows = summary
    ? summary.lane_rows.flatMap((lane) =>
        summary.queue_rows.filter((row) => row.signal_lane === lane.signal_lane).slice(0, 5),
      )
    : [];
  const maxLaneRows = Math.max(1, ...laneRows.map((row) => row.rows));

  return (
    <section className="showcase-section air-one-signal-section" aria-label="One-signal review queue">
      <div className="air-one-signal-head">
        <div>
          <p className="kicker kicker-blue">One-signal queue</p>
          <h2>The easy candidate lane is gone. What remains is one signal short.</h2>
          <p>
            After the 13 near-plus-name rows were source-screened, the review
            queue moves to weaker evidence: proximity without a name signal,
            name overlap without proximity, and official or automatic station
            provenance without complete grade documentation.
          </p>
        </div>
        <div className="air-one-signal-callout">
          <span>Review wall</span>
          <strong>{formatNumber(counts?.one_signal_queue_items ?? 0)}</strong>
          <p>items still outside station-radius and complete grade claims</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-one-signal-stat-grid">
            <div>
              <span>Already screened</span>
              <strong>{formatNumber(counts.near_plus_name_candidate_rows_already_source_screened)}</strong>
              <em>near-plus-name rows</em>
            </div>
            <div>
              <span>Queue items</span>
              <strong>{formatNumber(counts.one_signal_queue_items)}</strong>
              <em>{formatNumber(counts.unique_official_station_keys)} official station keys</em>
            </div>
            <div>
              <span>Countries</span>
              <strong>{formatNumber(counts.countries_with_queue_items)}</strong>
              <em>with unresolved one-signal rows</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>classifications</em>
            </div>
            <div>
              <span>Radius-ready</span>
              <strong>{formatNumber(counts.station_radius_join_ready_rows)}</strong>
              <em>still blocked</em>
            </div>
          </div>

          <div className="air-one-signal-lanes" aria-label="One-signal evidence lanes">
            {laneRows.map((lane) => {
              const width = lane.rows > 0 ? `${Math.max(5, (lane.rows / maxLaneRows) * 100)}%` : "0%";
              return (
                <article key={lane.signal_lane} className={`air-one-signal-lane air-one-signal-lane-${lane.signal_lane}`}>
                  <div>
                    <span>{sentenceCaseStatus(lane.status)}</span>
                    <strong>{lane.label}</strong>
                    <b>{formatNumber(lane.rows)} rows / {formatNumber(lane.countries)} countries</b>
                  </div>
                  <div className="air-one-signal-track">
                    <i style={{ width }} />
                  </div>
                  <p>{lane.reader_use}</p>
                  {lane.minimum_distance_km !== null && lane.maximum_distance_km !== null ? (
                    <small>
                      {formatNumber(lane.minimum_distance_km, 3)}-{formatNumber(lane.maximum_distance_km, 3)} km
                    </small>
                  ) : (
                    <small>no distance test in this lane</small>
                  )}
                </article>
              );
            })}
          </div>

          <div className="air-one-signal-country-grid">
            {countryRows.map((row) => (
              <article key={row.iso3} className="air-one-signal-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.queue_items)} queue items</b>
                </div>
                <dl>
                  <div>
                    <dt>Near</dt>
                    <dd>{formatNumber(row.near_only_rows)}</dd>
                  </div>
                  <div>
                    <dt>Name</dt>
                    <dd>{formatNumber(row.name_only_not_near_rows)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(row.monitor_grade_provenance_only_rows)}</dd>
                  </div>
                  <div>
                    <dt>Ready</dt>
                    <dd>{formatNumber(row.station_radius_join_ready_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-one-signal-row-grid">
            {sampleRows.map((row) => (
              <article key={row.one_signal_id} className={`air-one-signal-row air-one-signal-row-${row.signal_lane}`}>
                <div>
                  <span>{oneSignalLaneLabel(row.signal_lane)}</span>
                  <strong>{row.country} · {row.source_station_name || row.source_station_id || "official row"}</strong>
                  <b>{row.nearest_openaq_location_name || gradeCategoryLabel(row.grade_evidence_category)}</b>
                </div>
                <p>{row.missing_second_signal}</p>
                <small>
                  {row.nearest_openaq_distance_km !== "" && typeof row.nearest_openaq_distance_km === "number"
                    ? `${formatNumber(row.nearest_openaq_distance_km, 3)} km from nearest OpenAQ row`
                    : sentenceCaseStatus(row.review_priority)}
                </small>
              </article>
            ))}
          </div>

          <div className="air-one-signal-source-grid">
            {sourceRows.map((source) => (
              <article key={source.source_key} className="air-one-signal-source">
                <span>{source.iso3}</span>
                <strong>{source.source_name}</strong>
                <b>{formatNumber(source.queue_items)} queue items</b>
                <p>
                  {formatNumber(source.near_only_rows)} near-only;{" "}
                  {formatNumber(source.name_only_not_near_rows)} name-only;{" "}
                  {formatNumber(source.monitor_grade_provenance_only_rows)} grade-provenance-only.
                </p>
              </article>
            ))}
          </div>

          <div className="air-one-signal-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-one-signal-gate air-one-signal-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-one-signal-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/one-signal-review-queue.md" download>
              Queue note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-one-signal-review-queue-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-one-signal-review-queue.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading one-signal review queue...</p>
      )}
    </section>
  );
}

function AirMonitorGradeSourceValidationPanel({
  summary,
}: {
  summary: MonitorGradeSourceValidationSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const methodContextCount = counts
    ? counts.method_or_equipment_context_source_rows + counts.standard_or_method_context_source_rows
    : 0;
  const countryRows = [...(summary?.country_rows ?? [])].sort(
    (a, b) => b.monitor_grade_provenance_only_queue_items - a.monitor_grade_provenance_only_queue_items,
  );
  const sourceRows = summary?.source_rows ?? [];

  return (
    <section className="showcase-section air-grade-source-section" aria-label="Monitor-grade source-validation scan">
      <div className="air-grade-source-head">
        <div>
          <p className="kicker kicker-sage">Grade source validation</p>
          <h2>Method clues appear. Grade certification still does not.</h2>
          <p>
            The scan retrieves public source pages for the non-Bangladesh
            provenance-only lane. It separates method, equipment, standard,
            official-context, and caution language without converting any row
            into a complete monitor-grade classification.
          </p>
        </div>
        <div className="air-grade-source-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>station-radius assumptions remain blocked</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-source-stat-grid">
            <div>
              <span>Source URLs</span>
              <strong>{formatNumber(counts.source_urls_retrieved)}</strong>
              <em>{formatNumber(counts.source_urls_seeded)} seeded</em>
            </div>
            <div>
              <span>Rows covered</span>
              <strong>{formatNumber(counts.monitor_grade_provenance_only_rows_covered)}</strong>
              <em>provenance-only queue</em>
            </div>
            <div>
              <span>Method context</span>
              <strong>{formatNumber(methodContextCount)}</strong>
              <em>source rows, not certifications</em>
            </div>
            <div>
              <span>Caution</span>
              <strong>{formatNumber(counts.caution_language_source_rows)}</strong>
              <em>source row</em>
            </div>
            <div>
              <span>Radius-ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>still zero</em>
            </div>
          </div>

          <div className="air-grade-source-country-grid">
            {countryRows.map((row) => (
              <article key={row.iso3} className="air-grade-source-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.monitor_grade_provenance_only_queue_items)} covered rows</b>
                </div>
                <dl>
                  <div>
                    <dt>Sources</dt>
                    <dd>{formatNumber(row.source_rows_retrieved)}</dd>
                  </div>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(row.method_or_standard_context_sources)}</dd>
                  </div>
                  <div>
                    <dt>Context</dt>
                    <dd>{formatNumber(row.official_or_automatic_context_sources)}</dd>
                  </div>
                  <div>
                    <dt>Ready</dt>
                    <dd>{formatNumber(row.station_radius_grade_assumption_ready_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-source-card-grid">
            {sourceRows.map((source) => (
              <article
                key={source.source_key}
                className={`air-grade-source-card air-grade-source-card-${source.source_grade_evidence_lane}`}
              >
                <div>
                  <span>{source.iso3} · {sentenceCaseStatus(source.source_role)}</span>
                  <strong>{source.source_name}</strong>
                  <b>{monitorGradeSourceLaneLabel(source.source_grade_evidence_lane)}</b>
                </div>
                <p>{source.reader_use}</p>
                <small>
                  {formatNumber(source.queue_items_covered)} queue rows ·{" "}
                  {source.matched_method_terms || source.matched_expected_terms || "no matched terms"}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-source-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-grade-source-gate air-grade-source-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-source-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/monitor-grade-source-validation-scan.md" download>
              Source scan note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-source-validation-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-source-validation-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading monitor-grade source-validation scan...</p>
      )}
    </section>
  );
}

function AirMonitorGradeStationReviewPanel({
  summary,
}: {
  summary: MonitorGradeStationReviewSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const totalRows = Math.max(1, counts?.station_rows_reviewed ?? 0);
  const countryRows = [...(summary?.country_rows ?? [])].sort(
    (a, b) => b.station_rows_reviewed - a.station_rows_reviewed,
  );
  const sourceGroups = summary?.source_group_rows ?? [];
  const sampleRows = summary?.station_sample_rows ?? [];

  return (
    <section className="showcase-section air-grade-station-section" aria-label="Monitor-grade station-review queue">
      <div className="air-grade-station-head">
        <div>
          <p className="kicker kicker-blue">Station review queue</p>
          <h2>Method context is not yet station status.</h2>
          <p>
            The row-level queue projects source-validation clues back onto the
            138 provenance-only station rows. It shows where method context is
            worth reviewing, where caution language blocks grade promotion, and
            where official portal context is still the only public signal.
          </p>
        </div>
        <div className="air-grade-station-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>station-level current status is still missing</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-station-stat-grid">
            <div>
              <span>Station rows</span>
              <strong>{formatNumber(counts.station_rows_reviewed)}</strong>
              <em>{formatNumber(counts.economies_reviewed)} economies</em>
            </div>
            <div>
              <span>Method review</span>
              <strong>{formatNumber(counts.method_context_needs_station_confirmation_rows)}</strong>
              <em>needs station confirmation</em>
            </div>
            <div>
              <span>Caution</span>
              <strong>{formatNumber(counts.caution_blocks_grade_rows)}</strong>
              <em>blocked rows</em>
            </div>
            <div>
              <span>Official only</span>
              <strong>{formatNumber(counts.official_context_only_rows)}</strong>
              <em>weaker evidence lane</em>
            </div>
            <div>
              <span>Radius-ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>still zero</em>
            </div>
          </div>

          <div className="air-grade-station-lanes" aria-label="Station review lanes">
            {summary.lane_rows.map((lane) => (
              <article key={lane.station_review_lane} className={`air-grade-station-lane air-grade-station-lane-${lane.station_review_lane}`}>
                <div>
                  <span>{monitorGradeStationLaneLabel(lane.station_review_lane)}</span>
                  <strong>{formatNumber(lane.rows)} rows</strong>
                </div>
                <div className="air-grade-station-track">
                  <i style={{ width: `${Math.max(4, (lane.rows / totalRows) * 100)}%` }} />
                </div>
                <p>{lane.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-station-country-grid">
            {countryRows.map((row) => (
              <article key={row.iso3} className="air-grade-station-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.station_rows_reviewed)} station rows</b>
                </div>
                <dl>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(row.method_context_needs_station_confirmation_rows)}</dd>
                  </div>
                  <div>
                    <dt>Caution</dt>
                    <dd>{formatNumber(row.caution_blocks_grade_rows)}</dd>
                  </div>
                  <div>
                    <dt>Official</dt>
                    <dd>{formatNumber(row.official_context_only_rows)}</dd>
                  </div>
                  <div>
                    <dt>Ready</dt>
                    <dd>{formatNumber(row.station_radius_grade_assumption_ready_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-station-source-grid">
            {sourceGroups.map((source) => (
              <article key={source.source_group_key} className={`air-grade-station-source air-grade-station-source-${source.station_review_lane}`}>
                <div>
                  <span>{source.iso3} · {formatNumber(source.source_rows_reviewed)} source rows</span>
                  <strong>{source.source_name}</strong>
                  <b>{monitorGradeStationLaneLabel(source.station_review_lane)}</b>
                </div>
                <p>{source.reader_use}</p>
                <small>
                  {formatNumber(source.station_rows_reviewed)} station rows ·{" "}
                  {source.matched_caution_terms || source.matched_method_terms || source.source_keys}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-station-row-grid">
            {sampleRows.slice(0, 12).map((row) => (
              <article key={row.station_review_id} className={`air-grade-station-row air-grade-station-row-${row.station_review_lane}`}>
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{monitorGradeStationLaneLabel(row.station_review_lane)}</b>
                </div>
                <p>{row.station_review_question}</p>
                <small>{row.matched_caution_terms || row.matched_method_terms || row.source_station_type}</small>
              </article>
            ))}
          </div>

          <div className="air-grade-station-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-grade-station-gate air-grade-station-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-station-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/monitor-grade-station-review-queue.md" download>
              Station review note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-station-review-queue-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-station-review-queue.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading monitor-grade station-review queue...</p>
      )}
    </section>
  );
}

function AirMonitorGradeStationMethodEvidencePanel({
  summary,
}: {
  summary: MonitorGradeStationMethodEvidenceSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const totalRows = Math.max(1, counts?.method_context_station_rows_reviewed ?? 0);
  const laneRows = summary?.evidence_lane_rows ?? [];
  const countryRows = [...(summary?.country_rows ?? [])].sort(
    (a, b) => b.station_rows_reviewed - a.station_rows_reviewed,
  );
  const sourceGroups = summary?.source_group_rows ?? [];
  const sampleRows = summary?.station_sample_rows ?? [];
  const rawLiveValueOkRows = counts
    ? counts.positive_raw_live_pm25_value_rows + counts.zero_raw_live_pm25_value_rows
    : 0;
  const rawLiveValueIssueRows = counts
    ? counts.negative_raw_live_pm25_value_rows +
      counts.sentinel_raw_live_pm25_value_rows +
      counts.missing_raw_live_pm25_value_rows +
      counts.nonnumeric_raw_live_pm25_value_rows
    : 0;

  return (
    <section className="showcase-section air-grade-method-section" aria-label="Monitor-grade station method-evidence audit">
      <div className="air-grade-method-head">
        <div>
          <p className="kicker kicker-blue">Exact-row method audit</p>
          <h2>Exact rows sharpen the queue without closing it.</h2>
          <p>
            The audit joins the 66 method-context station rows back to exact
            official extraction rows. It separates rows where the official row
            carries instrument wording from rows where the public evidence is
            still only a PM2.5 portal or API record.
          </p>
        </div>
        <div className="air-grade-method-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>exact-row evidence improves review priority, not station-radius readiness</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid">
            <div>
              <span>Method-context rows</span>
              <strong>{formatNumber(counts.method_context_station_rows_reviewed)}</strong>
              <em>{formatNumber(counts.economies_reviewed)} economies</em>
            </div>
            <div>
              <span>Exact official rows</span>
              <strong>{formatNumber(counts.exact_official_rows_found)}</strong>
              <em>{formatNumber(counts.exact_official_rows_missing)} missing joins</em>
            </div>
            <div>
              <span>PM2.5 signal</span>
              <strong>{formatNumber(counts.exact_pm25_signal_rows)}</strong>
              <em>{formatNumber(counts.exact_coordinate_rows)} coordinate rows</em>
            </div>
            <div>
              <span>Instrument hints</span>
              <strong>{formatNumber(counts.row_level_instrument_hint_rows)}</strong>
              <em>exact row wording</em>
            </div>
            <div>
              <span>Raw values ok</span>
              <strong>{formatNumber(rawLiveValueOkRows)}</strong>
              <em>nonnegative raw PM2.5</em>
            </div>
            <div>
              <span>Raw value issues</span>
              <strong>{formatNumber(rawLiveValueIssueRows)}</strong>
              <em>negative, sentinel, or missing</em>
            </div>
          </div>

          <div className="air-grade-method-bridge" aria-label="Exact row evidence bridge">
            {laneRows.map((lane) => (
              <article key={lane.row_evidence_lane} className={`air-grade-method-lane air-grade-method-lane-${lane.row_evidence_lane}`}>
                <div>
                  <span>{monitorGradeMethodLaneLabel(lane.row_evidence_lane)}</span>
                  <strong>{formatNumber(lane.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track">
                  <i style={{ width: lane.rows > 0 ? `${Math.max(4, (lane.rows / totalRows) * 100)}%` : "0%" }} />
                </div>
                <p>{lane.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-country-grid">
            {countryRows.map((row) => (
              <article key={row.iso3} className="air-grade-method-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.station_rows_reviewed)} station rows</b>
                </div>
                <dl>
                  <div>
                    <dt>Exact</dt>
                    <dd>{formatNumber(row.exact_official_rows_found)}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{formatNumber(row.exact_pm25_signal_rows)}</dd>
                  </div>
                  <div>
                    <dt>Hints</dt>
                    <dd>{formatNumber(row.row_level_instrument_hint_rows)}</dd>
                  </div>
                  <div>
                    <dt>Portal</dt>
                    <dd>{formatNumber(row.row_level_pm25_portal_or_api_rows)}</dd>
                  </div>
                  <div>
                    <dt>Raw+</dt>
                    <dd>{formatNumber(row.positive_raw_live_pm25_value_rows)}</dd>
                  </div>
                  <div>
                    <dt>Issue</dt>
                    <dd>
                      {formatNumber(
                        row.negative_raw_live_pm25_value_rows +
                          row.sentinel_raw_live_pm25_value_rows +
                          row.missing_raw_live_pm25_value_rows,
                      )}
                    </dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-source-grid">
            {sourceGroups.map((source) => (
              <article key={source.source_group_key} className={`air-grade-method-source air-grade-method-source-${source.row_evidence_lane}`}>
                <div>
                  <span>{source.iso3} · {source.exact_source_evidence_type}</span>
                  <strong>{source.source_name}</strong>
                  <b>{monitorGradeMethodLaneLabel(source.row_evidence_lane)}</b>
                </div>
                <p>{source.reader_use}</p>
                <small>
                  {formatNumber(source.station_rows_reviewed)} rows ·{" "}
                  {source.row_level_method_hint_terms || source.source_level_method_terms || source.exact_source_station_type}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid">
            {sampleRows.slice(0, 12).map((row) => (
              <article key={row.method_evidence_id} className={`air-grade-method-row air-grade-method-row-${row.row_evidence_lane}`}>
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{monitorGradeMethodLaneLabel(row.row_evidence_lane)}</b>
                </div>
                <p>{row.reader_use}</p>
                <small>
                  {row.row_level_method_hint_terms || row.source_level_method_terms || row.exact_source_station_type}
                  {" · "}
                  {sentenceCaseStatus(row.exact_live_pm25_value_status)}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/monitor-grade-station-method-evidence.md" download>
              Method-evidence note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-station-method-evidence-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-station-method-evidence.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading monitor-grade station method-evidence audit...</p>
      )}
    </section>
  );
}

function AirUzbekistanCurrentMethodPanel({
  summary,
}: {
  summary: UzbekistanCurrentMethodSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const ageRows = summary?.age_lane_rows ?? [];
  const sampleRows = summary?.station_sample_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rawValueIssueRows = counts
    ? counts.negative_raw_pm25_value_rows + counts.sentinel_raw_pm25_value_rows + counts.missing_raw_pm25_value_rows
    : 0;
  const totalTargetRows = Math.max(1, counts?.target_uzbekistan_instrument_hint_rows ?? 0);

  return (
    <section className="showcase-section air-uzb-current-section" aria-label="Uzbekistan station current and method scan">
      <div className="air-uzb-current-head">
        <div>
          <p className="kicker kicker-blue">Uzbekistan current-method scan</p>
          <h2>The rows are present; the dates are not current.</h2>
          <p>
            The scan re-checks the 28 Uzbekistan instrument-hint station rows
            against the public Uzhydromet maps API. The station IDs and HORIBA
            markers remain visible, but most target rows have old reading dates
            or raw-value cautions.
          </p>
        </div>
        <div className="air-uzb-current-callout">
          <span>Older than 365 days</span>
          <strong>{formatNumber(counts?.api_reading_older_than_365_days_rows ?? 0)}</strong>
          <p>API presence is not current operating status</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-uzb-current-stat-grid">
            <div>
              <span>Target rows</span>
              <strong>{formatNumber(counts.target_uzbekistan_instrument_hint_rows)}</strong>
              <em>Uzbekistan instrument hints</em>
            </div>
            <div>
              <span>API rows found</span>
              <strong>{formatNumber(counts.target_station_rows_found_in_current_api)}</strong>
              <em>{formatNumber(counts.api_station_rows_returned)} API rows returned</em>
            </div>
            <div>
              <span>HORIBA markers</span>
              <strong>{formatNumber(counts.station_level_horiba_marker_rows)}</strong>
              <em>station-level marker fields</em>
            </div>
            <div>
              <span>Within 30 days</span>
              <strong>{formatNumber(counts.api_reading_within_30_days_rows)}</strong>
              <em>{formatNumber(counts.api_reading_within_7_days_rows)} within 7 days</em>
            </div>
            <div>
              <span>Raw issues</span>
              <strong>{formatNumber(rawValueIssueRows)}</strong>
              <em>negative, sentinel, or missing</em>
            </div>
            <div>
              <span>Grade-ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>still blocked</em>
            </div>
          </div>

          <div className="air-uzb-current-age-grid">
            {ageRows.map((row) => (
              <article key={row.api_reading_age_lane} className={`air-uzb-current-age air-uzb-current-age-${row.api_reading_age_lane}`}>
                <div>
                  <span>{sentenceCaseStatus(row.api_reading_age_lane)}</span>
                  <strong>{formatNumber(row.rows)} rows</strong>
                </div>
                <div className="air-uzb-current-track">
                  <i style={{ width: row.rows > 0 ? `${Math.max(4, (row.rows / totalTargetRows) * 100)}%` : "0%" }} />
                </div>
                <p>{row.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-row-grid">
            {sampleRows.slice(0, 12).map((row) => (
              <article key={row.method_evidence_id} className={`air-uzb-current-row air-uzb-current-row-${row.api_reading_age_lane}`}>
                <div>
                  <span>UZB · {row.source_station_id}</span>
                  <strong>{row.api_station_name || row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.api_reading_age_lane)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Date</dt>
                    <dd>{row.api_reading_date_iso || "missing"}</dd>
                  </div>
                  <div>
                    <dt>Age</dt>
                    <dd>{row.api_reading_age_days === "" ? "n/a" : `${formatNumber(row.api_reading_age_days)}d`}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.api_pm25_value_raw || "n/a"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <small>
                  {sentenceCaseStatus(row.api_pm25_value_status)}
                  {" · "}
                  {row.api_method_marker_terms ? "HORIBA marker" : "method marker missing"}
                </small>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-uzb-current-gate air-uzb-current-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/uzbekistan-station-current-method-scan.md" download>
              Uzbekistan scan note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-station-current-method-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-station-current-method-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Uzbekistan station current/method scan...</p>
      )}
    </section>
  );
}

function AirUzbekistanStatusCertificationPanel({
  summary,
}: {
  summary: UzbekistanStatusCertificationSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const gates = summary?.evidence_gate_counts ?? [];
  const stationRows = summary?.station_sample_rows ?? [];
  const sourceRows = summary?.source_records ?? [];
  const targetRows = Math.max(1, counts?.target_uzbekistan_station_rows ?? 0);
  const sourceRowsTotal = Math.max(1, counts?.source_urls_seeded ?? 0);
  const contextCandidateRows = counts
    ? counts.tashkent_reference_grade_context_candidate_rows
      + counts.district_commissioning_context_candidate_rows
      + counts.regional_realtime_network_context_candidate_rows
    : 0;
  const followupRows = counts
    ? counts.stale_detail_measurement_followup_rows + counts.sentinel_detail_measurement_followup_rows
    : 0;
  const ladder = counts
    ? [
        {
          key: "operating",
          label: "Operating or online context",
          rows: counts.source_level_current_context_sources,
          denominator: sourceRowsTotal,
          detail: "source rows, not station-status closure",
        },
        {
          key: "reference",
          label: "Reference-grade or standards context",
          rows: counts.source_level_certification_context_sources,
          denominator: sourceRowsTotal,
          detail: "source-level context unless station IDs are named",
        },
        {
          key: "maintenance",
          label: "Maintenance or training context",
          rows: counts.source_level_calibration_context_sources,
          denominator: sourceRowsTotal,
          detail: "helps review queue, not per-station calibration",
        },
        {
          key: "exact",
          label: "Additional exact station mentions",
          rows: counts.additional_exact_station_source_mention_rows,
          denominator: targetRows,
          detail: "Uchtepa and Yangi O'zbekiston event context",
        },
        {
          key: "context",
          label: "Weaker context candidates",
          rows: contextCandidateRows,
          denominator: targetRows,
          detail: "Tashkent, Almazar, and Aral Sea context only",
        },
        {
          key: "followup",
          label: "Follow-up blockers",
          rows: followupRows,
          denominator: targetRows,
          detail: "stale timestamps or sentinel PM2.5",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-uzb-current-section air-uzb-status-section" aria-label="Uzbekistan status and certification source scan">
      <div className="air-uzb-current-head">
        <div>
          <p className="kicker kicker-sage">Uzbekistan status/certification scan</p>
          <h2>The source context improves; the grade gate stays closed.</h2>
          <p>
            This pass checks public regulator, owner, development-partner, and
            technical sources after the station-detail ID gate. The result is a
            stronger source ladder, not a station-radius permission slip.
          </p>
        </div>
        <div className="air-uzb-current-callout">
          <span>Current-status confirmed</span>
          <strong>{formatNumber(counts?.current_status_confirmed_rows ?? 0)}</strong>
          <p>Source-level context cannot certify exact station operation</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-uzb-current-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.source_urls_retrieved)}</strong>
              <em>{formatNumber(counts.source_urls_seeded)} seeded URLs</em>
            </div>
            <div>
              <span>Method context</span>
              <strong>{formatNumber(counts.source_level_method_context_sources)}</strong>
              <em>source rows</em>
            </div>
            <div>
              <span>Operating context</span>
              <strong>{formatNumber(counts.source_level_current_context_sources)}</strong>
              <em>online, real-time, or commissioned</em>
            </div>
            <div>
              <span>Exact station mentions</span>
              <strong>{formatNumber(counts.additional_exact_station_source_mention_rows)}</strong>
              <em>event context only</em>
            </div>
            <div>
              <span>Follow-up blockers</span>
              <strong>{formatNumber(followupRows)}</strong>
              <em>stale or sentinel rows</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>radius still blocked</em>
            </div>
          </div>

          <div className="air-uzb-current-age-grid">
            {ladder.map((step) => (
              <article key={step.key} className={`air-uzb-current-age air-uzb-status-ladder-${step.key}`}>
                <div>
                  <span>{step.label}</span>
                  <strong>{formatNumber(step.rows)} rows</strong>
                </div>
                <div className="air-uzb-current-track">
                  <i style={{ width: step.rows > 0 ? `${Math.max(4, (step.rows / step.denominator) * 100)}%` : "0%" }} />
                </div>
                <p>{step.detail}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-row-grid">
            {stationRows.slice(0, 14).map((row) => (
              <article key={`${row.source_station_id}-${row.source_scan_decision}`} className="air-uzb-current-row air-uzb-status-row">
                <div>
                  <span>UZB · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.source_scan_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Updated</dt>
                    <dd>{row.official_detail_updated_iso || "missing"}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.official_detail_pm25_value || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>Region</dt>
                    <dd>{row.official_region_name || "n/a"}</dd>
                  </div>
                </dl>
                <p>
                  Exact source: {row.additional_exact_station_source_keys || "none"}.
                  {" "}Context: {row.additional_context_source_keys || "none"}.
                </p>
                <small>current-status and complete-grade fields remain false</small>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-row-grid">
            {sourceRows.slice(0, 6).map((source) => (
              <article key={source.source_key} className="air-uzb-current-row air-uzb-status-source">
                <div>
                  <span>{source.source_role}</span>
                  <strong>{source.source_name}</strong>
                  <b>{source.retrieved ? "retrieved" : "not retrieved"}</b>
                </div>
                <dl>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(source.matched_method_terms.length)}</dd>
                  </div>
                  <div>
                    <dt>Status</dt>
                    <dd>{formatNumber(source.matched_current_terms.length)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(source.matched_certification_terms.length)}</dd>
                  </div>
                </dl>
                <p>{source.source_note || "Source note recorded in the generated summary."}</p>
                <small>
                  {source.matched_certification_terms.slice(0, 2).join(" · ") || "no certification term"}
                </small>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-uzb-current-gate air-uzb-current-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/uzbekistan-status-certification-source-scan.md" download>
              Status/certification note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-status-certification-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-status-certification-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Uzbekistan status/certification source scan...</p>
      )}
    </section>
  );
}

function AirUzbekistanBlockerFollowupPanel({
  summary,
}: {
  summary: UzbekistanBlockerFollowupSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const rows = summary?.station_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const total = Math.max(1, counts?.target_blocker_rows ?? rows.length);
  const ladder = counts
    ? [
        {
          key: "detail",
          label: "Exact detail pages",
          rows: counts.official_detail_pages_retrieved,
          denominator: total,
          detail: "public official station pages",
        },
        {
          key: "region",
          label: "Region rows found",
          rows: counts.region_row_found_rows,
          denominator: total,
          detail: "matching official table rows",
        },
        {
          key: "stale",
          label: "Stale blockers",
          rows: counts.stale_detail_blocker_rows,
          denominator: total,
          detail: "older than 30 days",
        },
        {
          key: "sentinel",
          label: "Sentinel blocker",
          rows: counts.sentinel_pm25_blocker_rows,
          denominator: total,
          detail: "PM2.5 equals -9999",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-uzb-current-section air-uzb-blocker-section" aria-label="Uzbekistan blocker row follow-up">
      <div className="air-uzb-current-head">
        <div>
          <p className="kicker kicker-crimson">Uzbekistan blocker follow-up</p>
          <h2>Three rows still stop the radius claim.</h2>
          <p>
            This pass goes row by row through the stale and sentinel cases left
            by the source scan. It retrieves the exact official pages again,
            then asks whether the blocker is actually resolved.
          </p>
        </div>
        <div className="air-uzb-current-callout air-uzb-blocker-callout">
          <span>Resolved blockers</span>
          <strong>{formatNumber(counts?.public_row_followup_resolved_rows ?? 0)}</strong>
          <p>Every row remains outside current-status and radius claims</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-uzb-current-stat-grid">
            <div>
              <span>Detail pages</span>
              <strong>{formatNumber(counts.official_detail_pages_retrieved)}</strong>
              <em>{formatNumber(total)} target blocker rows</em>
            </div>
            <div>
              <span>Region rows</span>
              <strong>{formatNumber(counts.region_row_found_rows)}</strong>
              <em>official table matches</em>
            </div>
            <div>
              <span>Stale rows</span>
              <strong>{formatNumber(counts.stale_detail_blocker_rows)}</strong>
              <em>plus Updating data</em>
            </div>
            <div>
              <span>Sentinel row</span>
              <strong>{formatNumber(counts.sentinel_pm25_blocker_rows)}</strong>
              <em>PM2.5 = -9999</em>
            </div>
            <div>
              <span>Current status</span>
              <strong>{formatNumber(counts.current_status_confirmed_rows)}</strong>
              <em>explicit closures</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>still blocked</em>
            </div>
          </div>

          <div className="air-uzb-current-age-grid air-uzb-blocker-ladder">
            {ladder.map((step) => (
              <article key={step.key} className={`air-uzb-current-age air-uzb-blocker-ladder-${step.key}`}>
                <div>
                  <span>{step.label}</span>
                  <strong>{formatNumber(step.rows)} rows</strong>
                </div>
                <div className="air-uzb-current-track">
                  <i style={{ width: step.rows > 0 ? `${Math.max(4, (step.rows / step.denominator) * 100)}%` : "0%" }} />
                </div>
                <p>{step.detail}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-row-grid air-uzb-blocker-row-grid">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-uzb-current-row air-uzb-blocker-row">
                <div>
                  <span>UZB · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.followup_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Detail age</dt>
                    <dd>{row.detail_updated_age_days || "n/a"} days</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.detail_pm25_value || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>Row signal</dt>
                    <dd>{row.region_row_auto || row.region_row_updated_raw || "n/a"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <small>
                  {sentenceCaseStatus(row.review_focus)} · {sentenceCaseStatus(row.detail_pm25_value_status)}
                </small>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-uzb-current-gate air-uzb-current-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/uzbekistan-blocker-row-followup.md" download>
              Blocker note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-blocker-row-followup.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Uzbekistan blocker-row follow-up...</p>
      )}
    </section>
  );
}

function AirUzbekistanEndpointConsistencyPanel({
  summary,
}: {
  summary: UzbekistanEndpointConsistencySummary | null;
}) {
  const counts = summary?.coverage_counts;
  const rows = summary?.station_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const total = Math.max(1, counts?.target_blocker_rows ?? rows.length);
  const mismatchRows = counts?.official_endpoint_disagreement_rows ?? 0;
  const mismatchStats = counts
    ? [
        {
          key: "date",
          label: "API/date mismatch",
          rows: counts.api_detail_date_mismatch_rows,
          detail: "API date differs from detail page",
        },
        {
          key: "pm25",
          label: "PM2.5 mismatch",
          rows: counts.api_detail_pm25_mismatch_rows,
          detail: "API and detail values diverge",
        },
        {
          key: "region",
          label: "Region/detail mismatch",
          rows: counts.region_detail_status_mismatch_rows,
          detail: "regional row conflicts with detail page",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-uzb-current-section air-uzb-endpoint-section" aria-label="Uzbekistan official endpoint consistency check">
      <div className="air-uzb-current-head">
        <div>
          <p className="kicker kicker-blue">Uzbekistan endpoint consistency</p>
          <h2>The same station ID tells three stories.</h2>
          <p>
            This check compares the maps API, language detail pages, and
            language regional rows for IDs 107, 728, and 737. The detail pages
            agree across languages, but the official endpoint set still does
            not give a public correction or grade/status closure.
          </p>
        </div>
        <div className="air-uzb-current-callout air-uzb-endpoint-callout">
          <span>Public endpoint resolutions</span>
          <strong>{formatNumber(counts?.public_endpoint_resolution_rows ?? 0)}</strong>
          <p>{formatNumber(mismatchRows)} of {formatNumber(total)} rows still disagree across official surfaces</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-uzb-current-stat-grid air-uzb-endpoint-stat-grid">
            <div>
              <span>Source routes</span>
              <strong>{formatNumber(counts.source_routes_retrieved)}</strong>
              <em>of {formatNumber(counts.source_routes_seeded)} official routes</em>
            </div>
            <div>
              <span>Detail pages</span>
              <strong>{formatNumber(counts.language_detail_pages_retrieved)}</strong>
              <em>English, Russian, Uzbek</em>
            </div>
            <div>
              <span>Detail agreement</span>
              <strong>{formatNumber(counts.cross_language_detail_consistent_rows)}</strong>
              <em>same date and PM2.5 across languages</em>
            </div>
            <div>
              <span>Endpoint mismatch</span>
              <strong>{formatNumber(counts.official_endpoint_disagreement_rows)}</strong>
              <em>target rows</em>
            </div>
            <div>
              <span>Sentinel detail</span>
              <strong>{formatNumber(counts.detail_pm25_sentinel_rows)}</strong>
              <em>PM2.5 blocker row</em>
            </div>
            <div>
              <span>Radius ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>claim remains closed</em>
            </div>
          </div>

          <div className="air-uzb-endpoint-mismatch-grid">
            {mismatchStats.map((item) => (
              <article key={item.key} className={`air-uzb-endpoint-mismatch air-uzb-endpoint-mismatch-${item.key}`}>
                <div>
                  <span>{item.label}</span>
                  <strong>{formatNumber(item.rows)} rows</strong>
                </div>
                <div className="air-uzb-current-track">
                  <i style={{ width: item.rows > 0 ? `${Math.max(4, (item.rows / total) * 100)}%` : "0%" }} />
                </div>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-endpoint-row-grid">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-uzb-endpoint-row">
                <div className="air-uzb-endpoint-row-title">
                  <span>UZB · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.endpoint_decision)}</b>
                </div>
                <div className="air-uzb-endpoint-card-grid">
                  {row.endpoint_cards.map((card) => (
                    <div key={card.endpoint} className={`air-uzb-endpoint-card air-uzb-endpoint-card-${gateTone(card.tone)}`}>
                      <span>{card.endpoint}</span>
                      <strong>{card.date_or_status || "n/a"}</strong>
                      <em>{card.pm25 ? `PM2.5 ${card.pm25}` : `${formatNumber(card.routes)} routes`}</em>
                      <b>{sentenceCaseStatus(card.signal)}</b>
                    </div>
                  ))}
                </div>
                <dl>
                  <div>
                    <dt>Date mismatch</dt>
                    <dd>{row.api_detail_date_mismatch ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>PM2.5 mismatch</dt>
                    <dd>{row.api_detail_pm25_mismatch ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Region mismatch</dt>
                    <dd>{row.region_detail_status_mismatch ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-gate-grid air-uzb-endpoint-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-uzb-current-gate air-uzb-current-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/uzbekistan-endpoint-consistency.md" download>
              Endpoint note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-endpoint-consistency-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-endpoint-consistency.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Uzbekistan endpoint consistency check...</p>
      )}
    </section>
  );
}

function AirUzbekistanExternalContextPanel({
  summary,
}: {
  summary: UzbekistanExternalContextSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const rows = summary?.station_rows ?? [];
  const sources = summary?.source_records ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const total = Math.max(1, counts?.target_blocker_rows ?? rows.length);
  const contextStats = counts
    ? [
        {
          key: "launch",
          label: "Launch context",
          rows: counts.rows_with_launch_context_only,
          detail: "Sergili/Sergeli appears in official launch context",
        },
        {
          key: "reference",
          label: "Reference context",
          rows: counts.rows_with_source_level_reference_context_only,
          detail: "Tashkent source-level context, not exact blocker closure",
        },
        {
          key: "id",
          label: "Exact station-ID context",
          rows: counts.rows_with_exact_station_id_external_context,
          detail: "no source names IDs 107, 728, or 737 with closure",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-uzb-current-section air-uzb-external-section" aria-label="Uzbekistan blocker external context wall">
      <div className="air-uzb-current-head">
        <div>
          <p className="kicker kicker-sage">Uzbekistan external context</p>
          <h2>Launch context is not a sentinel fix.</h2>
          <p>
            This pass leaves the telemetry endpoints alone and checks public
            official or technical context outside those pages. It asks whether
            a source names station IDs 107, 728, or 737 with a correction,
            current-status record, calibration record, or grade basis.
          </p>
        </div>
        <div className="air-uzb-current-callout air-uzb-external-callout">
          <span>Exact station-ID closures</span>
          <strong>{formatNumber(counts?.public_blocker_resolution_rows ?? 0)}</strong>
          <p>{formatNumber(counts?.external_source_urls_retrieved ?? 0)} external sources retrieved; blockers stay open</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-uzb-current-stat-grid air-uzb-external-stat-grid">
            <div>
              <span>External sources</span>
              <strong>{formatNumber(counts.external_source_urls_retrieved)}</strong>
              <em>of {formatNumber(counts.external_source_urls_seeded)} seeded</em>
            </div>
            <div>
              <span>Context rows</span>
              <strong>{formatNumber(counts.rows_with_any_external_context)}</strong>
              <em>of {formatNumber(total)} blocker rows</em>
            </div>
            <div>
              <span>Name/location context</span>
              <strong>{formatNumber(counts.rows_with_station_name_or_location_external_context)}</strong>
              <em>not station-ID closure</em>
            </div>
            <div>
              <span>Exact ID context</span>
              <strong>{formatNumber(counts.rows_with_exact_station_id_external_context)}</strong>
              <em>IDs 107, 728, 737</em>
            </div>
            <div>
              <span>Current status</span>
              <strong>{formatNumber(counts.current_status_confirmed_rows)}</strong>
              <em>public closures</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>still blocked</em>
            </div>
          </div>

          <div className="air-uzb-external-context-grid">
            {contextStats.map((item) => (
              <article key={item.key} className={`air-uzb-external-context air-uzb-external-context-${item.key}`}>
                <div>
                  <span>{item.label}</span>
                  <strong>{formatNumber(item.rows)} rows</strong>
                </div>
                <div className="air-uzb-current-track">
                  <i style={{ width: item.rows > 0 ? `${Math.max(4, (item.rows / total) * 100)}%` : "0%" }} />
                </div>
                <p>{item.detail}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-external-source-grid">
            {sources.map((source) => (
              <article key={source.source_key} className={`air-uzb-external-source air-uzb-external-source-${gateTone(source.retrieved ? "available" : "not_ready")}`}>
                <div>
                  <span>{sentenceCaseStatus(source.source_role)}</span>
                  <strong>{source.source_name}</strong>
                </div>
                <dl>
                  <div>
                    <dt>Status</dt>
                    <dd>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</dd>
                  </div>
                  <div>
                    <dt>Station terms</dt>
                    <dd>{formatNumber(source.matched_station_terms.length)}</dd>
                  </div>
                  <div>
                    <dt>Grade terms</dt>
                    <dd>{formatNumber(source.matched_method_grade_terms.length)}</dd>
                  </div>
                </dl>
                <p>{source.source_note}</p>
                <a href={source.url}>Source</a>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-row-grid air-uzb-external-row-grid">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-uzb-current-row air-uzb-external-row">
                <div>
                  <span>UZB · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.external_context_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Detail</dt>
                    <dd>{row.detail_updated_iso || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.detail_pm25_value || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>ID closure</dt>
                    <dd>{row.external_exact_station_id_context ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <small>
                  {row.official_launch_context_keys || row.source_level_reference_context_keys || row.prior_endpoint_decision}
                </small>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-gate-grid air-uzb-external-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-uzb-current-gate air-uzb-current-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/uzbekistan-blocker-external-context.md" download>
              External-context note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-blocker-external-context.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Uzbekistan blocker external-context wall...</p>
      )}
    </section>
  );
}

function AirUzbekistanAirPortalNamespacePanel({
  summary,
}: {
  summary: UzbekistanAirPortalNamespaceSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const rows = summary?.station_rows ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sources = summary?.source_records ?? [];
  const total = Math.max(1, counts?.target_blocker_rows ?? rows.length);
  const seededSources = sources.filter((source) => !source.source_role.includes("detail_probe"));
  const targetIdProbes = sources.filter((source) => source.source_role === "target_id_detail_probe");
  const mirrorShare = counts ? counts.alternate_detail_mirrors_official_detail_rows / total : 0;
  const metricCards = counts
    ? [
        {
          key: "stations",
          label: "Portal Horiba stations",
          value: counts.air_portal_station_objects,
          detail: "second namespace exposed",
        },
        {
          key: "matches",
          label: "Alternate matches",
          value: counts.alternate_station_name_match_rows,
          detail: "of 3 blocker rows",
        },
        {
          key: "original",
          label: "Original ID hits",
          value: counts.target_blocker_id_detail_found_rows,
          detail: "IDs 107, 728, 737",
        },
        {
          key: "mirror",
          label: "Mirrored details",
          value: counts.alternate_detail_mirrors_official_detail_rows,
          detail: `${pct(mirrorShare)} mirror the blocker`,
        },
        {
          key: "stale",
          label: "Stale alternates",
          value: counts.alternate_detail_stale_rows,
          detail: "older than 30 days",
        },
        {
          key: "sentinel",
          label: "Sentinel alternate",
          value: counts.alternate_detail_sentinel_rows,
          detail: "PM2.5 is -9999",
        },
        {
          key: "status",
          label: "Current-status closures",
          value: counts.current_status_confirmed_rows,
          detail: "active flag is not closure",
        },
        {
          key: "grade",
          label: "Complete-grade rows",
          value: counts.complete_monitor_grade_classification_rows,
          detail: "still zero",
        },
      ]
    : [];

  const displayNumber = (value: number | string | null | undefined, digits = 0) => {
    if (typeof value === "number") return formatNumber(value, digits);
    return value === null || value === undefined || value === "" ? "n/a" : String(value);
  };

  return (
    <section className="showcase-section air-uzb-current-section air-uzb-external-section air-uzb-portal-section" aria-label="Uzbekistan Air Uzbekistan portal namespace wall">
      <div className="air-uzb-current-head">
        <div>
          <p className="kicker kicker-blue">Uzbekistan portal namespace</p>
          <h2>The second portal finds the stations, not the closure.</h2>
          <p>
            Air Uzbekistan exposes a public Horiba station list and detail API.
            This scan checks whether that portal accepts blocker IDs 107, 728,
            and 737, or only maps the same stations to alternate IDs that still
            carry the stale or sentinel evidence.
          </p>
        </div>
        <div className="air-uzb-current-callout air-uzb-portal-callout">
          <span>Portal blocker resolutions</span>
          <strong>{formatNumber(counts?.public_portal_resolution_rows ?? 0)}</strong>
          <p>
            {formatNumber(counts?.alternate_station_name_match_rows ?? 0)} alternate namespace matches;
            original IDs still fail
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-uzb-current-stat-grid air-uzb-portal-stat-grid">
            {metricCards.map((card) => (
              <div key={card.key}>
                <span>{card.label}</span>
                <strong>{formatNumber(card.value)}</strong>
                <em>{card.detail}</em>
              </div>
            ))}
          </div>

          <div className="air-uzb-portal-bridge-grid" aria-label="Uzbekistan portal namespace decisions">
            <article className="air-uzb-portal-bridge air-uzb-portal-bridge-source">
              <span>Source object</span>
              <strong>Data portal plus Horiba endpoint</strong>
              <p>
                The Data/Meteo landing page documents API modules but points to
                an email/application route. The Air Uzbekistan page exposes a
                no-login Horiba station list and detail endpoint.
              </p>
            </article>
            <article className="air-uzb-portal-bridge air-uzb-portal-bridge-namespace">
              <span>Namespace test</span>
              <strong>107/728/737 are not Air Uzbekistan IDs</strong>
              <p>
                The portal detail route returns station records for IDs 1, 20,
                and 26, while probes for the original blocker IDs return station
                not found payloads.
              </p>
            </article>
            <article className="air-uzb-portal-bridge air-uzb-portal-bridge-closure">
              <span>Closure test</span>
              <strong>Active flags stay out of the status count</strong>
              <p>
                The alternate station list marks the rows active, but the
                detail values still mirror the exact official blocker rows, so
                current-status and grade closures remain zero.
              </p>
            </article>
          </div>

          <div className="air-uzb-current-row-grid air-uzb-portal-row-grid" aria-label="Uzbekistan portal namespace rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-uzb-current-row air-uzb-portal-row">
                <div>
                  <span>UZB · {row.source_station_id} to portal {row.air_portal_alternate_station_id || "none"}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.portal_namespace_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Portal name</dt>
                    <dd>{row.air_portal_alternate_station_name || "not found"}</dd>
                  </div>
                  <div>
                    <dt>Active flag</dt>
                    <dd>{row.air_portal_alternate_station_active ? "present" : "absent"}</dd>
                  </div>
                  <div>
                    <dt>Original ID</dt>
                    <dd>{row.air_portal_target_id_detail_found ? "accepted" : "not found"}</dd>
                  </div>
                  <div>
                    <dt>Portal date</dt>
                    <dd>{row.air_portal_alternate_detail_date_iso || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>Portal PM2.5</dt>
                    <dd>{displayNumber(row.air_portal_alternate_detail_pm25_value, 3)}</dd>
                  </div>
                  <div>
                    <dt>Mirrors official</dt>
                    <dd>{row.air_portal_detail_mirrors_official_detail ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <small>
                  {row.air_portal_target_id_detail_error || row.prior_endpoint_decision}
                </small>
              </article>
            ))}
          </div>

          <div className="air-uzb-portal-source-grid" aria-label="Uzbekistan portal source records">
            {seededSources.map((source) => (
              <article key={source.source_key} className={`air-uzb-external-source air-uzb-portal-source air-uzb-external-source-${gateTone(source.retrieved ? "available" : "not_ready")}`}>
                <div>
                  <span>{sentenceCaseStatus(source.source_role)}</span>
                  <strong>{source.source_name}</strong>
                </div>
                <dl>
                  <div>
                    <dt>Status</dt>
                    <dd>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</dd>
                  </div>
                  <div>
                    <dt>Role</dt>
                    <dd>{sentenceCaseStatus(source.source_role)}</dd>
                  </div>
                </dl>
                <p>{source.source_note}</p>
                <a href={source.url}>Source</a>
              </article>
            ))}
          </div>

          <div className="air-uzb-portal-probe-grid" aria-label="Uzbekistan portal target ID probes">
            {targetIdProbes.map((source) => (
              <article key={source.source_key} className={`air-uzb-portal-probe air-uzb-portal-probe-${source.station_data_available ? "available" : "blocked"}`}>
                <span>{source.source_key.replace("air_uzbekistan_horiba_target_id_", "Target ID ")}</span>
                <strong>{source.station_data_available ? "Station data found" : "Station not found"}</strong>
                <p>{source.api_error || "The target ID returned a station record."}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-gate-grid air-uzb-portal-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-uzb-current-gate air-uzb-current-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-uzb-current-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/uzbekistan-air-portal-namespace.md" download>
              Portal namespace note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-uzbekistan-air-portal-namespace.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Uzbekistan Air Uzbekistan portal namespace wall...</p>
      )}
    </section>
  );
}

function AirIndonesiaGeorgiaRowMethodSourcePanel({
  summary,
}: {
  summary: IndonesiaGeorgiaRowMethodSourceSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const countries = summary?.country_rows ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sourceRecords = (summary?.source_records ?? []).filter((source) => !source.expanded_for_station_id);
  const sampleRows = summary?.station_sample_rows ?? [];
  const total = Math.max(1, counts?.target_indonesia_georgia_rows ?? 0);
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-row-method-section" aria-label="Indonesia and Georgia row method source scan">
      <div className="air-grade-method-head">
        <div>
          <p className="kicker kicker-crimson">Indonesia/Georgia source scan</p>
          <h2>Better row context, still no grade closure.</h2>
          <p>
            The next loop checks the 38 exact PM2.5 portal/API rows outside
            Uzbekistan. Indonesia gains same-page BMKG method context; Georgia
            remains source and station-alias context only.
          </p>
        </div>
        <div className="air-grade-method-callout air-row-method-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>Station-radius assumptions remain blocked in both countries</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid">
            <div>
              <span>Target rows</span>
              <strong>{formatNumber(counts.target_indonesia_georgia_rows)}</strong>
              <em>{formatNumber(counts.target_indonesia_rows)} IDN, {formatNumber(counts.target_georgia_rows)} GEO</em>
            </div>
            <div>
              <span>Sources</span>
              <strong>{formatNumber(counts.source_urls_retrieved)}</strong>
              <em>{formatNumber(counts.source_urls_seeded_or_expanded)} seeded or expanded URLs</em>
            </div>
            <div>
              <span>BMKG context</span>
              <strong>{formatNumber(counts.same_page_method_context_candidate_rows)}</strong>
              <em>same-page method candidates</em>
            </div>
            <div>
              <span>Georgia context</span>
              <strong>{formatNumber(countries.find((row) => row.iso3 === "GEO")?.station_context_candidate_rows ?? 0)}</strong>
              <em>station-alias candidates</em>
            </div>
            <div>
              <span>Current status</span>
              <strong>{formatNumber(counts.current_status_confirmed_rows)}</strong>
              <em>explicit closures</em>
            </div>
            <div>
              <span>Radius ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>still blocked</em>
            </div>
          </div>

          <div className="air-grade-method-bridge" aria-label="Indonesia and Georgia row-method source decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className={`air-grade-method-lane air-row-method-lane air-row-method-lane-${decision.decision}`}>
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
                <p>
                  {decision.decision.includes("bmkg")
                    ? "Exact BMKG detail pages now carry same-page PM2.5 display and Beta Attenuation language."
                    : decision.decision.includes("georgia")
                      ? "Georgia rows have station or place context, but not station-code method closure."
                      : "Country source context exists, but it is still not connected enough for row closure."}
                </p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-country-grid">
            {countries.map((row) => (
              <article key={row.iso3} className="air-grade-method-country air-row-method-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.target_rows)} target rows</b>
                </div>
                <dl>
                  <div>
                    <dt>Sources</dt>
                    <dd>{formatNumber(row.source_urls_retrieved)}</dd>
                  </div>
                  <div>
                    <dt>Prior exact</dt>
                    <dd>{formatNumber(row.prior_exact_pm25_rows)}</dd>
                  </div>
                  <div>
                    <dt>Raw +</dt>
                    <dd>{formatNumber(row.positive_prior_raw_value_rows)}</dd>
                  </div>
                  <div>
                    <dt>Same page</dt>
                    <dd>{formatNumber(row.same_page_method_context_candidate_rows)}</dd>
                  </div>
                  <div>
                    <dt>Context</dt>
                    <dd>{formatNumber(row.station_context_candidate_rows)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(row.complete_monitor_grade_classification_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-source-grid">
            {sourceRecords.map((source) => (
              <article key={source.source_key} className="air-grade-method-source air-row-method-source">
                <div>
                  <span>{source.iso3} source</span>
                  <strong>{source.source_key}</strong>
                  <b>{sentenceCaseStatus(source.source_role)}</b>
                </div>
                <p>{source.source_note}</p>
                <small>
                  Method {formatNumber(source.matched_method_terms.length)} · Current {formatNumber(source.matched_current_terms.length)} · Standard {formatNumber(source.matched_standard_terms.length)}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid">
            {sampleRows.map((row) => (
              <article key={`${row.iso3}-${row.source_station_id}`} className="air-grade-method-row air-row-method-row">
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.source_scan_decision)}</b>
                </div>
                <p>
                  {row.same_page_method_context_candidate
                    ? `BMKG detail page timestamp: ${row.exact_station_detail_timestamp_raw || "not parsed"}.`
                    : row.station_alias_context_source_keys
                      ? `Context source keys: ${row.station_alias_context_source_keys}.`
                      : "Only source-level context was found for this row."}
                </p>
                <small>{sentenceCaseStatus(row.exact_live_pm25_value_status)}</small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/indonesia-georgia-row-method-source-scan.md" download>
              Source scan note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-indonesia-georgia-row-method-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading Indonesia/Georgia row-method source scan...</p>
      )}
    </section>
  );
}

function AirStationCodeStatusMethodPanel({
  summary,
}: {
  summary: StationCodeStatusMethodSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const countries = summary?.country_rows ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sourceRecords = summary?.source_records ?? [];
  const sampleRows = summary?.station_sample_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const countryTotal = Math.max(1, countries.reduce((sum, row) => sum + row.target_rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-station-code-section" aria-label="Station-code status and method source scan">
      <div className="air-grade-method-head">
        <div>
          <p className="kicker kicker-blue">Station-code closure scan</p>
          <h2>Georgia improves; grade still closed.</h2>
          <p>
            The stricter pass checks 41 exact station-code or station-ID rows.
            Georgia moves from alias context to official station-code API
            evidence; Indonesia and Uzbekistan remain blocked for status and
            grade closure.
          </p>
        </div>
        <div className="air-grade-method-callout air-station-code-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>Station-radius assumptions remain at zero after the stricter scan</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid">
            <div>
              <span>Target rows</span>
              <strong>{formatNumber(counts.target_rows)}</strong>
              <em>{formatNumber(counts.target_georgia_rows)} GEO, {formatNumber(counts.target_indonesia_rows)} IDN, {formatNumber(counts.target_uzbekistan_blocker_rows)} UZB</em>
            </div>
            <div>
              <span>Exact code/ID</span>
              <strong>{formatNumber(counts.exact_station_code_or_id_rows)}</strong>
              <em>public station row trace</em>
            </div>
            <div>
              <span>Georgia API</span>
              <strong>{formatNumber(counts.georgia_station_code_api_rows)}</strong>
              <em>station-code rows</em>
            </div>
            <div>
              <span>PM2.5 equipment</span>
              <strong>{formatNumber(counts.georgia_pm25_equipment_rows)}</strong>
              <em>Georgia rows list PM2.5</em>
            </div>
            <div>
              <span>Operating context</span>
              <strong>{formatNumber(counts.georgia_operating_description_context_rows)}</strong>
              <em>Georgia descriptions</em>
            </div>
            <div>
              <span>Still blocked</span>
              <strong>{formatNumber(counts.georgia_test_mode_rows + counts.uzbekistan_unresolved_blocker_rows)}</strong>
              <em>test-mode or UZB blockers</em>
            </div>
          </div>

          <div className="air-grade-method-country-grid">
            {countries.map((row) => (
              <article key={row.iso3} className="air-grade-method-country air-station-code-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.target_rows)} target rows</b>
                </div>
                <div className="air-grade-method-track air-station-code-track">
                  <i style={{ width: `${Math.max(5, (row.target_rows / countryTotal) * 100)}%` }} />
                </div>
                <dl>
                  <div>
                    <dt>Exact</dt>
                    <dd>{formatNumber(row.exact_station_code_or_id_rows)}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{formatNumber(row.pm25_row_or_equipment_rows)}</dd>
                  </div>
                  <div>
                    <dt>Operating</dt>
                    <dd>{formatNumber(row.station_operating_description_context_rows)}</dd>
                  </div>
                  <div>
                    <dt>Blocked</dt>
                    <dd>{formatNumber(row.test_mode_or_blocker_rows)}</dd>
                  </div>
                  <div>
                    <dt>Method table</dt>
                    <dd>{formatNumber(row.station_method_table_rows)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(row.complete_monitor_grade_classification_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-bridge" aria-label="Station-code status source decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className={`air-grade-method-lane air-station-code-lane air-station-code-lane-${decision.decision}`}>
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-station-code-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
                <p>
                  {decision.decision.includes("georgia_station_code_pm25")
                    ? "Exact Georgia station-code API rows list PM2.5 and operating-description context, but no method table or certification."
                    : decision.decision.includes("test_mode")
                      ? "The Georgia Tazakendi row is explicitly marked as working in test mode."
                      : decision.decision.includes("indonesia")
                        ? "BMKG rows have exact payload/station-code context and prior same-page method context, but no station status table."
                        : "Uzbekistan rows remain stale or sentinel blockers carried forward from exact official pages."}
                </p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-source-grid">
            {sourceRecords.map((source) => (
              <article key={source.source_key} className="air-grade-method-source air-station-code-source">
                <div>
                  <span>{source.iso3} source</span>
                  <strong>{source.source_key}</strong>
                  <b>{sentenceCaseStatus(source.source_role)}</b>
                </div>
                <p>{source.source_note}</p>
                <small>
                  Method {formatNumber(source.matched_method_terms.length)} · Current {formatNumber(source.matched_current_terms.length)} · Standard {formatNumber(source.matched_standard_terms.length)} · Caution {formatNumber(source.matched_caution_terms.length)}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid">
            {sampleRows.map((row) => (
              <article key={`${row.iso3}-${row.source_station_id}`} className="air-grade-method-row air-station-code-row">
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.source_scan_decision)}</b>
                </div>
                <p>
                  {row.station_test_mode_flag
                    ? "Public row is marked as working in test mode."
                    : row.station_description_operating_context
                      ? "Station-code description includes operating-context language."
                      : row.iso3 === "UZB"
                        ? "Exact blocker row remains outside grade and radius assumptions."
                        : "Exact payload context exists, but no station status/method table was found."}
                </p>
                <small>
                  PM2.5 {row.pm25_row_or_equipment_listed ? "listed" : "not listed"} · hourly rows {formatNumber(row.pm25_observation_rows)}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-code-status-method-source-scan.md" download>
              Source scan note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-code-status-method-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-code-status-method-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-code status/method source scan...</p>
      )}
    </section>
  );
}

function AirStationGradeDecisionLedgerPanel({
  summary,
}: {
  summary: StationGradeDecisionLedgerSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const countries = summary?.country_rows ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sampleRows = summary?.sample_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const countryTotal = Math.max(1, countries.reduce((sum, row) => sum + row.decision_rows, 0));
  const cautionRows =
    gates.find((gate) => gate.gate === "Raw-value or blocker caution")?.rows ??
    ((counts?.raw_value_sanity_issue_rows ?? 0) + (counts?.test_mode_or_blocker_rows ?? 0));

  return (
    <section className="showcase-section air-grade-method-section air-decision-ledger-section" aria-label="Station-grade decision ledger">
      <div className="air-grade-method-head air-decision-ledger-head">
        <div>
          <p className="kicker kicker-crimson">Station-grade decision ledger</p>
          <h2>The blocker is now row-level, not vague.</h2>
          <p>
            The ledger turns the exact station evidence into one decision row
            per method-context station. It shows where station-code, detail-ID,
            method, operating, and QA clues exist, then keeps grade and radius
            assumptions at zero.
          </p>
        </div>
        <div className="air-grade-method-callout air-decision-ledger-callout">
          <span>Radius-ready rows</span>
          <strong>{formatNumber(counts?.station_radius_grade_assumption_ready_rows ?? 0)}</strong>
          <p>All rows still require explicit current-status and grade closure</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-decision-ledger-stat-grid">
            <div>
              <span>Decision rows</span>
              <strong>{formatNumber(counts.decision_rows)}</strong>
              <em>{formatNumber(counts.uzbekistan_rows)} UZB, {formatNumber(counts.indonesia_rows)} IDN, {formatNumber(counts.georgia_rows)} GEO</em>
            </div>
            <div>
              <span>Exact source trail</span>
              <strong>{formatNumber(counts.exact_station_code_or_id_source_rows)}</strong>
              <em>code, detail ID, or official row</em>
            </div>
            <div>
              <span>PM2.5 evidence</span>
              <strong>{formatNumber(counts.pm25_row_or_equipment_rows)}</strong>
              <em>row or equipment context</em>
            </div>
            <div>
              <span>Method context</span>
              <strong>{formatNumber(counts.station_method_context_rows)}</strong>
              <em>not method-class closure</em>
            </div>
            <div>
              <span>Caution rows</span>
              <strong>{formatNumber(cautionRows)}</strong>
              <em>raw-value or blocker rows</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>no promotions</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-decision-ledger-bridge" aria-label="Station-grade ledger decision lanes">
            {decisions.map((decision) => (
              <article key={decision.decision_lane} className={`air-grade-method-lane air-decision-ledger-lane air-decision-ledger-lane-${decision.decision_lane}`}>
                <div>
                  <span>{sentenceCaseStatus(decision.decision_lane)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-decision-ledger-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
                <p>{decision.reader_use}</p>
                <small>{decision.minimum_public_evidence_needed}</small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-country-grid air-decision-ledger-country-grid">
            {countries.map((row) => (
              <article key={row.iso3} className="air-grade-method-country air-decision-ledger-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.decision_rows)} decision rows</b>
                </div>
                <div className="air-grade-method-track air-decision-ledger-track">
                  <i style={{ width: `${Math.max(5, (row.decision_rows / countryTotal) * 100)}%` }} />
                </div>
                <dl>
                  <div>
                    <dt>Exact</dt>
                    <dd>{formatNumber(row.exact_station_code_or_id_source_rows)}</dd>
                  </div>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(row.station_method_context_rows)}</dd>
                  </div>
                  <div>
                    <dt>Current ctx</dt>
                    <dd>{formatNumber(row.operating_or_current_context_rows)}</dd>
                  </div>
                  <div>
                    <dt>QA issue</dt>
                    <dd>{formatNumber(row.raw_value_sanity_issue_rows)}</dd>
                  </div>
                  <div>
                    <dt>Blocker</dt>
                    <dd>{formatNumber(row.test_mode_or_blocker_rows)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(row.complete_monitor_grade_classification_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid air-decision-ledger-row-grid">
            {sampleRows.map((row) => (
              <article key={`${row.iso3}-${row.source_station_id}`} className={`air-grade-method-row air-decision-ledger-row air-decision-ledger-row-${row.decision_lane}`}>
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.decision_lane)}</b>
                </div>
                <p>{row.reader_use}</p>
                <small>
                  {sentenceCaseStatus(row.row_evidence_lane)} · {row.raw_value_sanity_issue_present ? "raw-value caution" : "raw-value open"} · {row.test_mode_or_blocker_present ? "blocker present" : "no explicit blocker"}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-decision-ledger-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-decision-ledger-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-decision-ledger-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-grade-decision-ledger.md" download>
              Ledger note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-grade-decision-ledger-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-grade-decision-ledger.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-grade decision ledger...</p>
      )}
    </section>
  );
}

function AirStationMethodClassificationPanel({
  summary,
}: {
  summary: StationMethodClassificationSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const countries = summary?.country_rows ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sampleRows = summary?.station_sample_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const countryTotal = Math.max(1, countries.reduce((sum, row) => sum + row.target_rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-method-classification-section" aria-label="Station-method classification audit">
      <div className="air-grade-method-head air-method-classification-head">
        <div>
          <p className="kicker kicker-blue">Station-method classification audit</p>
          <h2>A method class is not a grade claim.</h2>
          <p>
            This audit checks whether the exact station rows now have enough
            public method evidence to classify the PM2.5 measurement method. It
            upgrades the BMKG method lane while keeping status, calibration,
            complete grade, and radius gates closed.
          </p>
        </div>
        <div className="air-grade-method-callout air-method-classification-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>Method evidence improved, but station-grade certification did not.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-method-classification-stat-grid">
            <div>
              <span>Audit rows</span>
              <strong>{formatNumber(counts.target_rows)}</strong>
              <em>{formatNumber(counts.target_indonesia_rows)} IDN, {formatNumber(counts.target_georgia_rows)} GEO, {formatNumber(counts.target_uzbekistan_rows)} UZB</em>
            </div>
            <div>
              <span>BMKG method class</span>
              <strong>{formatNumber(counts.bmkg_method_classified_rows)}</strong>
              <em>Beta Attenuation Monitoring</em>
            </div>
            <div>
              <span>Recent measurement visible</span>
              <strong>{formatNumber(counts.current_measurement_recent_rows)}</strong>
              <em>display or hourly observation</em>
            </div>
            <div>
              <span>Georgia caution</span>
              <strong>{formatNumber(counts.georgia_live_data_unverified_caution_rows)}</strong>
              <em>live data not verified</em>
            </div>
            <div>
              <span>Blocker caution</span>
              <strong>{formatNumber(counts.raw_value_or_blocker_caution_rows)}</strong>
              <em>raw-value or blocker rows</em>
            </div>
            <div>
              <span>Status confirmed</span>
              <strong>{formatNumber(counts.current_status_confirmed_rows)}</strong>
              <em>no status promotions</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-method-classification-bridge" aria-label="Station-method classification decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className={`air-grade-method-lane air-method-classification-lane air-method-classification-lane-${decision.decision}`}>
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-method-classification-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-grade-method-country-grid air-method-classification-country-grid">
            {countries.map((row) => (
              <article key={row.iso3} className="air-grade-method-country air-method-classification-country">
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{formatNumber(row.target_rows)} audit rows</b>
                </div>
                <div className="air-grade-method-track air-method-classification-track">
                  <i style={{ width: `${Math.max(5, (row.target_rows / countryTotal) * 100)}%` }} />
                </div>
                <dl>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(row.method_classified_rows)}</dd>
                  </div>
                  <div>
                    <dt>Recent</dt>
                    <dd>{formatNumber(row.current_measurement_recent_rows)}</dd>
                  </div>
                  <div>
                    <dt>Catalog</dt>
                    <dd>{formatNumber(row.source_level_instrument_catalog_rows)}</dd>
                  </div>
                  <div>
                    <dt>Caution</dt>
                    <dd>{formatNumber(row.unverified_or_blocker_caution_rows)}</dd>
                  </div>
                  <div>
                    <dt>Status</dt>
                    <dd>{formatNumber(row.current_status_confirmed_rows)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(row.complete_monitor_grade_classification_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid air-method-classification-row-grid">
            {sampleRows.map((row) => (
              <article key={`${row.iso3}-${row.source_station_id}`} className={`air-grade-method-row air-method-classification-row air-method-classification-row-${row.iso3.toLowerCase()}`}>
                <div>
                  <span>{row.iso3} · {row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{row.station_method_classified ? row.station_method_class : "method not closed"}</b>
                </div>
                <p>{sentenceCaseStatus(row.audit_decision)}</p>
                <small>
                  {row.current_measurement_recent ? "recent measurement visible" : "no recent measurement visibility"} · {row.raw_value_or_blocker_caution ? "caution present" : "no row caution"}
                </small>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-method-classification-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-method-classification-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-method-classification-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/station-method-classification-audit.md" download>
              Audit note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-method-classification-audit-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-station-method-classification-audit.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading station-method classification audit...</p>
      )}
    </section>
  );
}

function AirBmkgOperationMaintenancePanel({
  summary,
}: {
  summary: BmkgOperationMaintenanceSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.station_sample_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-operation-section" aria-label="BMKG operation and maintenance source scan">
      <div className="air-grade-method-head air-bmkg-operation-head">
        <div>
          <p className="kicker kicker-blue">BMKG operation and maintenance scan</p>
          <h2>Operation context is still not certification.</h2>
          <p>
            The BMKG rows now have BAM method classification. This pass checks
            public BMKG SOP, regulation, tariff, model-note, and exact station
            pages for the missing station-status and calibration-evidence layer.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-operation-callout">
          <span>Station certificates found</span>
          <strong>{formatNumber(counts?.station_specific_calibration_certificate_rows ?? 0)}</strong>
          <p>The source wall improves context, not row-level certification.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-operation-stat-grid">
            <div>
              <span>BMKG rows tested</span>
              <strong>{formatNumber(counts.target_bmkg_rows)}</strong>
              <em>already BAM method-classified</em>
            </div>
            <div>
              <span>Source records</span>
              <strong>{formatNumber(counts.context_source_records + counts.exact_station_detail_records)}</strong>
              <em>{formatNumber(counts.context_source_records)} context, {formatNumber(counts.exact_station_detail_records)} station pages</em>
            </div>
            <div>
              <span>Daily SOP context</span>
              <strong>{formatNumber(counts.daily_inspection_sop_context_rows)}</strong>
              <em>BMKG BAM-1020 inspection SOP</em>
            </div>
            <div>
              <span>Maintenance context</span>
              <strong>{formatNumber(counts.maintenance_check_context_rows)}</strong>
              <em>source-level check terms</em>
            </div>
            <div>
              <span>Calibration context</span>
              <strong>{formatNumber(Math.max(counts.calibration_procedure_context_rows, counts.calibration_service_tariff_context_rows))}</strong>
              <em>procedure or service/tariff, not certificate</em>
            </div>
            <div>
              <span>Current status closed</span>
              <strong>{formatNumber(counts.current_status_confirmed_rows)}</strong>
              <em>no status promotions</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-operation-bridge" aria-label="BMKG operation and maintenance decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-bmkg-operation-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-operation-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-operation-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-operation-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid air-bmkg-operation-row-grid">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-grade-method-row air-bmkg-operation-row">
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                </div>
                <p>{row.exact_station_detail_timestamp_raw || "No timestamp parsed"}</p>
                <em>
                  SOP {row.daily_inspection_sop_context ? "yes" : "no"} /
                  maintenance {row.maintenance_check_context ? "yes" : "no"} /
                  calibration context {(row.calibration_procedure_context || row.calibration_service_tariff_context) ? "yes" : "no"}
                </em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-operation-downloads">
            <a href="/programs/air-monitoring/bmkg-operation-maintenance-source-scan.md">Read the note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-operation-maintenance-source-scan-summary.json">Download JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-operation-maintenance-source-scan.csv">Download CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG operation/maintenance source scan...</p>
      )}
    </section>
  );
}

function AirBmkgStationStatusPanel({
  summary,
}: {
  summary: BmkgStationStatusSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.station_sample_rows ?? [];
  const valueRows = [...(summary?.station_value_rows ?? [])].sort(
    (a, b) => (b.detail_value_ug_m3 ?? -1) - (a.detail_value_ug_m3 ?? -1),
  );
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const maxValue = Math.max(1, ...valueRows.map((row) => row.detail_value_ug_m3 ?? 0));

  const categoryTone = (category: string) => {
    const lower = category.toLowerCase();
    if (lower.includes("tidak") || lower.includes("berbahaya")) return "hot";
    if (lower.includes("sedang")) return "warm";
    return "cool";
  };

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-status-section" aria-label="BMKG station-specific status and calibration audit">
      <div className="air-grade-method-head air-bmkg-status-head">
        <div>
          <p className="kicker kicker-blue">BMKG station-specific closure audit</p>
          <h2>Public telemetry is visible. Certification is still missing.</h2>
          <p>
            This pass re-fetches the 22 exact BMKG station-detail pages, parses
            their PM2.5 display snapshots, and tests whether those same pages
            provide operational-status, inspection-log, or calibration-certificate
            evidence for each station.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-status-callout">
          <span>Complete grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)}</strong>
          <p>Visible readings are not status or calibration certification.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-status-stat-grid">
            <div>
              <span>Station pages</span>
              <strong>{formatNumber(counts.detail_pages_retrieved)}</strong>
              <em>{formatNumber(counts.target_bmkg_rows)} BMKG target rows</em>
            </div>
            <div>
              <span>Display snapshots parsed</span>
              <strong>{formatNumber(counts.public_measurement_display_rows)}</strong>
              <em>timestamp, PM2.5 value, and category</em>
            </div>
            <div>
              <span>BAM method text</span>
              <strong>{formatNumber(counts.page_bam_method_text_rows)}</strong>
              <em>station-page method language</em>
            </div>
            <div>
              <span>Status certifications</span>
              <strong>{formatNumber(counts.current_status_confirmed_rows)}</strong>
              <em>no station status closure</em>
            </div>
            <div>
              <span>Calibration certificates</span>
              <strong>{formatNumber(counts.station_specific_calibration_certificate_rows)}</strong>
              <em>no target-row certificate</em>
            </div>
            <div>
              <span>Radius-ready rows</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>not a catchment denominator</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-status-bridge" aria-label="BMKG station-specific status decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-bmkg-status-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-status-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-bmkg-status-value-wall" aria-label="BMKG public PM2.5 station display snapshot">
            <div>
              <p className="kicker">Station display snapshot</p>
              <h3>Values are visible, but they do not close the certificate gate.</h3>
              <p>
                Snapshot from exact BMKG station pages at {valueRows[0]?.detail_timestamp_raw || "retrieval time"}.
                Bars are scaled to the largest parsed display value in this audit.
              </p>
            </div>
            <div className="air-bmkg-status-value-list">
              {valueRows.map((row) => {
                const value = row.detail_value_ug_m3 ?? 0;
                return (
                  <article key={row.source_station_id} className={`air-bmkg-status-value-row air-bmkg-status-value-${categoryTone(row.detail_category_raw)}`}>
                    <div>
                      <span>{row.source_station_id}</span>
                      <strong>{row.source_station_name}</strong>
                      <em>{row.detail_category_raw || "unparsed"}</em>
                    </div>
                    <div className="air-bmkg-status-value-meter">
                      <i style={{ width: `${Math.max(2, (value / maxValue) * 100)}%` }} />
                    </div>
                    <b>{row.detail_value_ug_m3 === null ? "n/a" : formatNumber(row.detail_value_ug_m3, 1)}</b>
                  </article>
                );
              })}
            </div>
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-status-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-status-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid air-bmkg-status-row-grid">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-grade-method-row air-bmkg-status-row">
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                </div>
                <p>{row.detail_value_ug_m3 || "n/a"} ug/m3 · {row.detail_category_raw || "category not parsed"}</p>
                <em>
                  BAM {row.page_bam_method_text_found ? "yes" : "no"} /
                  status {row.page_station_operational_status_found ? "yes" : "no"} /
                  certificate {row.station_specific_calibration_certificate_found ? "yes" : "no"}
                </em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-status-downloads">
            <a href="/programs/air-monitoring/bmkg-station-specific-status-audit.md">Read the note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-station-specific-status-audit-summary.json">Download JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-station-specific-status-audit.csv">Download CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG station-specific status audit...</p>
      )}
    </section>
  );
}

function AirBmkgApiParityPanel({
  summary,
}: {
  summary: BmkgApiParitySummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.station_sample_rows ?? [];
  const extras = summary?.extra_api_station_rows ?? [];
  const total = Math.max(1, counts?.target_bmkg_rows ?? 0);
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const maxPm25 = Math.max(
    1,
    ...rows.map((row) => Number(row.api_detail_latest_pm25_value) || 0),
  );
  const fieldRows =
    (counts?.api_station_status_field_rows ?? 0) +
    (counts?.api_inspection_field_rows ?? 0) +
    (counts?.api_calibration_field_rows ?? 0) +
    (counts?.api_certificate_field_rows ?? 0) +
    (counts?.api_grade_field_rows ?? 0) +
    (counts?.api_method_field_rows ?? 0);

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-api-section" aria-label="BMKG API telemetry and status-field check">
      <div className="air-grade-method-head air-bmkg-api-head">
        <div>
          <p className="kicker kicker-blue">BMKG API parity check</p>
          <h2>The API is live, but it is silent on certification.</h2>
          <p>
            This pass follows the public BMKG app token flow and checks the
            official PM2.5 list/detail APIs for the same 22 station rows. The
            APIs expose telemetry, coordinates, and condition labels; they do
            not expose status, inspection, calibration, certificate, grade, or
            method fields.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-api-callout">
          <span>Status/certificate fields</span>
          <strong>{formatNumber(fieldRows)}</strong>
          <p>{formatNumber(counts?.target_detail_api_routes_retrieved ?? 0)} detail API routes still stay telemetry-only</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-api-stat-grid">
            <div>
              <span>Public token flow</span>
              <strong>{formatNumber(counts.auth_token_obtained)}</strong>
              <em>transient token obtained, not persisted</em>
            </div>
            <div>
              <span>List API rows</span>
              <strong>{formatNumber(counts.pm25_list_api_station_rows)}</strong>
              <em>{formatNumber(counts.target_station_files_in_list_api_rows)} of {formatNumber(total)} target files present</em>
            </div>
            <div>
              <span>Detail APIs</span>
              <strong>{formatNumber(counts.target_detail_api_routes_retrieved)}</strong>
              <em>{formatNumber(counts.target_detail_api_hourly_observation_rows)} hourly observations</em>
            </div>
            <div>
              <span>Detail coordinates</span>
              <strong>{formatNumber(counts.api_detail_coordinate_rows)}</strong>
              <em>{formatNumber(counts.api_list_detail_coordinate_match_rows)} list/detail coordinate matches</em>
            </div>
            <div>
              <span>Condition labels</span>
              <strong>{formatNumber(counts.api_air_quality_condition_label_rows)}</strong>
              <em>KONDISI is air quality, not station status</em>
            </div>
            <div>
              <span>Radius ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>API telemetry does not close the gate</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-api-bridge" aria-label="BMKG API parity decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-bmkg-api-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-api-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-bmkg-api-field-wall">
            <div>
              <p className="kicker">API field wall</p>
              <h3>Telemetry fields are abundant. Closure fields are absent.</h3>
              <p>
                The list API has {formatNumber(counts.pm25_list_api_extra_station_rows)} extra station files outside this target queue.
                One target detail route is not present in the list API, so list/detail parity also remains imperfect.
              </p>
            </div>
            <div className="air-bmkg-api-field-grid">
              {[
                ["status", counts.api_station_status_field_rows],
                ["inspection", counts.api_inspection_field_rows],
                ["calibration", counts.api_calibration_field_rows],
                ["certificate", counts.api_certificate_field_rows],
                ["grade", counts.api_grade_field_rows],
                ["method", counts.api_method_field_rows],
              ].map(([label, value]) => (
                <div key={label}>
                  <span>{label}</span>
                  <strong>{formatNumber(Number(value))}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="air-bmkg-api-row-grid">
            {rows.map((row) => {
              const pm25 = Number(row.api_detail_latest_pm25_value) || 0;
              return (
                <article key={row.source_station_id} className={`air-bmkg-api-row ${row.api_list_found ? "" : "air-bmkg-api-row-missing"}`}>
                  <div>
                    <span>{row.source_station_id}</span>
                    <strong>{row.source_station_name}</strong>
                    <b>{sentenceCaseStatus(row.api_parity_decision)}</b>
                  </div>
                  <div className="air-bmkg-api-meter">
                    <i style={{ width: `${Math.max(2, (pm25 / maxPm25) * 100)}%` }} />
                  </div>
                  <dl>
                    <div>
                      <dt>Latest</dt>
                      <dd>{formatNumber(pm25, 1)}</dd>
                    </div>
                    <div>
                      <dt>Hour</dt>
                      <dd>{row.api_detail_latest_hour || "n/a"}</dd>
                    </div>
                    <div>
                      <dt>List</dt>
                      <dd>{row.api_list_found ? "yes" : "no"}</dd>
                    </div>
                    <div>
                      <dt>Fields</dt>
                      <dd>{row.api_payload_has_station_status_field ? "status" : "0"}</dd>
                    </div>
                  </dl>
                  <p>{row.reader_use}</p>
                </article>
              );
            })}
          </div>

          {extras.length > 0 && (
            <div className="air-bmkg-api-extra-strip" aria-label="Extra BMKG API station files outside target queue">
              <span>Extra list API files outside target queue</span>
              {extras.map((row) => (
                <b key={row.source_station_id}>
                  {row.source_station_id}: {row.source_station_name} ({formatNumber(Number(row.pm25_value) || 0, 1)})
                </b>
              ))}
            </div>
          )}

          <div className="air-grade-method-gate-grid air-bmkg-api-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-api-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-api-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-api-parity-status.md" download>
              API note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-api-parity-status-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-api-parity-status.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG API parity/status check...</p>
      )}
    </section>
  );
}

function AirBmkgRegionalStatusPanel({
  summary,
}: {
  summary: BmkgRegionalStatusSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-regional-section" aria-label="BMKG regional station-status source scan">
      <div className="air-grade-method-head air-bmkg-regional-head">
        <div>
          <p className="kicker kicker-blue">BMKG regional status scan</p>
          <h2>One status gate moves, but the grade gate stays closed.</h2>
          <p>
            This pass leaves the central station-detail and API surfaces and checks
            regional BMKG status and analysis pages, public-information,
            service, and regulator sources. Banjarbaru gets explicit regional
            ONLINE status; the added analysis pages expand station/site context
            without closing calibration or complete-grade evidence.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-regional-callout">
          <span>Current-status rows</span>
          <strong>{formatNumber(counts?.current_status_confirmed_rows ?? 0)}</strong>
          <p>Useful movement, not a station-radius or grade promotion.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-regional-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.regional_public_source_urls_retrieved)}</strong>
              <em>of {formatNumber(counts.regional_public_source_urls_seeded)} seeded routes</em>
            </div>
            <div>
              <span>Station/site context</span>
              <strong>{formatNumber(counts.rows_with_exact_station_name_external_context)}</strong>
              <em>status, regulator, or analysis source</em>
            </div>
            <div>
              <span>Regional ONLINE rows</span>
              <strong>{formatNumber(counts.rows_with_regional_online_status)}</strong>
              <em>official Kalimantan Selatan page</em>
            </div>
            <div>
              <span>Calibration certificates</span>
              <strong>{formatNumber(counts.station_specific_calibration_certificate_rows)}</strong>
              <em>still absent in public sources</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>status alone is not enough</em>
            </div>
            <div>
              <span>Radius ready</span>
              <strong>{formatNumber(counts.station_radius_grade_assumption_ready_rows)}</strong>
              <em>no catchment denominator yet</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-regional-bridge" aria-label="BMKG regional status scan decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-bmkg-regional-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-regional-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-bmkg-regional-evidence-wall" aria-label="BMKG regional station evidence rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className={`air-bmkg-regional-row ${row.current_status_confirmed ? "air-bmkg-regional-row-closed" : ""}`}>
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.regional_status_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Status</dt>
                    <dd>{row.explicit_regional_status_online ? "ONLINE" : "not closed"}</dd>
                  </div>
                  <div>
                    <dt>Time</dt>
                    <dd>{row.status_timestamp_raw || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.status_value_ug_m3 || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{row.complete_monitor_grade_classification_available ? "closed" : "open"}</dd>
                  </div>
                </dl>
                {row.source_latitude && row.source_longitude && (
                  <p>
                    Regional page coordinates: {row.source_latitude}, {row.source_longitude}; category {row.status_category_raw || "n/a"}.
                  </p>
                )}
                <em>{row.reader_use}</em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-regional-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-regional-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-bmkg-regional-source-grid" aria-label="BMKG regional status source records">
            {sources.map((source) => (
              <article key={source.source_key} className={source.matched_target_station_rows > 0 ? "air-bmkg-regional-source-matched" : ""}>
                <div>
                  <span>{sentenceCaseStatus(source.source_role)}</span>
                  <strong>{sentenceCaseStatus(source.source_key)}</strong>
                </div>
                <p>{source.source_name}</p>
                <em>
                  HTTP {source.http_status || "n/a"} · {formatNumber(source.matched_target_station_rows)} target rows · {source.retrieved ? "retrieved" : "not retrieved"}
                </em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-regional-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-regional-status-source-scan.md" download>
              Regional status note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-regional-status-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG regional status source scan...</p>
      )}
    </section>
  );
}

function AirBmkgDashboardStatusPanel({
  summary,
}: {
  summary: BmkgDashboardStatusSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-dashboard-section" aria-label="BMKG dashboard current-status source scan">
      <div className="air-grade-method-head air-bmkg-dashboard-head">
        <div>
          <p className="kicker kicker-blue">BMKG dashboard status scan</p>
          <h2>The status wall moves, but the grade wall does not.</h2>
          <p>
            The official BMKG climate-information page embeds a CEWS PM2.5
            dashboard with a public data object. This scan matches every target
            BMKG row to that dashboard, closes current dashboard status for the
            ONLINE rows, and keeps calibration, grade, and radius evidence open.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-dashboard-callout">
          <span>Current ONLINE rows</span>
          <strong>{formatNumber(counts?.current_status_confirmed_rows ?? 0)}</strong>
          <p>Pekanbaru remains a current DELAYED caution row.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-dashboard-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.dashboard_source_urls_retrieved)}</strong>
              <em>of {formatNumber(counts.dashboard_source_urls_seeded)} parent/dashboard routes</em>
            </div>
            <div>
              <span>Dashboard locations</span>
              <strong>{formatNumber(counts.dashboard_locations_total)}</strong>
              <em>public CEWS PM2.5 locations</em>
            </div>
            <div>
              <span>Target rows matched</span>
              <strong>{formatNumber(counts.target_dashboard_location_rows)}</strong>
              <em>of {formatNumber(counts.target_bmkg_rows)} BMKG rows</em>
            </div>
            <div>
              <span>Current DELAYED</span>
              <strong>{formatNumber(counts.target_dashboard_delayed_rows)}</strong>
              <em>visible but not current-online</em>
            </div>
            <div>
              <span>Series observations</span>
              <strong>{formatNumber(counts.target_timeseries_observation_rows)}</strong>
              <em>dashboard points across target rows</em>
            </div>
            <div>
              <span>Calibration certificates</span>
              <strong>{formatNumber(counts.station_specific_calibration_certificate_rows)}</strong>
              <em>still absent from dashboard fields</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-dashboard-bridge" aria-label="BMKG dashboard status scan decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-bmkg-dashboard-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-dashboard-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-bmkg-dashboard-status-wall" aria-label="BMKG dashboard status rows">
            {rows.map((row) => (
              <article
                key={row.source_station_id}
                className={`air-bmkg-dashboard-tile ${row.current_status_confirmed ? "air-bmkg-dashboard-tile-online" : "air-bmkg-dashboard-tile-delayed"}`}
              >
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.dashboard_location_key || row.source_station_name}</strong>
                  <b>{row.dashboard_status_raw || "not found"}</b>
                </div>
                <dl>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{formatNumber(Number(row.dashboard_pm25_ug_m3), 1)}</dd>
                  </div>
                  <div>
                    <dt>Category</dt>
                    <dd>{row.dashboard_category_raw || "n/a"}</dd>
                  </div>
                  <div>
                    <dt>Points</dt>
                    <dd>{formatNumber(row.dashboard_timeseries_points)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{row.complete_monitor_grade_classification_available ? "closed" : "open"}</dd>
                  </div>
                </dl>
                <p>
                  Latest dashboard timestamp: {row.dashboard_timestamp_raw || "n/a"}; last series label {row.dashboard_last_label || "n/a"}.
                </p>
                <em>{row.reader_use}</em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-dashboard-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-dashboard-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-bmkg-dashboard-source-grid" aria-label="BMKG dashboard source records">
            {sources.map((source) => (
              <article key={source.source_key} className={source.matched_target_station_rows > 0 ? "air-bmkg-dashboard-source-matched" : ""}>
                <div>
                  <span>{sentenceCaseStatus(source.source_role)}</span>
                  <strong>{sentenceCaseStatus(source.source_key)}</strong>
                </div>
                <p>{source.source_name}</p>
                <em>
                  HTTP {source.http_status || "n/a"} · {formatNumber(source.matched_target_station_rows)} target rows · {source.retrieved ? "retrieved" : "not retrieved"}
                </em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-dashboard-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-dashboard-status-source-scan.md" download>
              Dashboard status note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-dashboard-status-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-dashboard-status-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG dashboard status source scan...</p>
      )}
    </section>
  );
}

function AirBmkgGradeBasisPanel({
  summary,
}: {
  summary: BmkgGradeBasisSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sources = summary?.source_records ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const sourceLevelCalibration =
    (counts?.source_level_periodic_calibration_rule_sources ?? 0) +
    (counts?.source_level_calibration_service_sources ?? 0);
  const stationClosure =
    (counts?.station_specific_calibration_certificate_rows ?? 0) +
    (counts?.calibration_status_available_rows ?? 0);
  const sourceFamilies = counts
    ? [
        {
          label: "Standards and SOP",
          value: counts.official_standard_or_rule_sources_retrieved,
          detail: "method, operating rule, inspection, and logbook context",
        },
        {
          label: "Service and tariff",
          value: counts.official_service_or_tariff_sources_retrieved,
          detail: "public calibration-service route context",
        },
        {
          label: "PPID and reports",
          value: counts.official_report_or_ppid_sources_retrieved,
          detail: "agency-level public-information and certificate context",
        },
      ]
    : [];
  const termCount = (value: string) => value.split("||").filter(Boolean).length;

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-grade-section" aria-label="BMKG grade-basis source scan">
      <div className="air-grade-method-head air-bmkg-grade-head">
        <div>
          <p className="kicker kicker-blue">BMKG grade-basis scan</p>
          <h2>The method wall is stronger. The station certificate wall is still closed.</h2>
          <p>
            This pass tests official BMKG standards, SOPs, service pages, PPID
            records, and reports for the 22 target BAM rows. It improves the
            source-level method and calibration-rule basis, but it does not
            produce station-level inspection logs, calibration certificates, or
            complete monitor-grade classifications.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-grade-callout">
          <span>Station certificate rows</span>
          <strong>{formatNumber(stationClosure)}</strong>
          <p>{formatNumber(counts?.grade_basis_source_urls_retrieved ?? 0)} official sources retrieved; none close row-level calibration status.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-grade-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.grade_basis_source_urls_retrieved)}</strong>
              <em>of {formatNumber(counts.grade_basis_source_urls_seeded)} seeded grade-basis routes</em>
            </div>
            <div>
              <span>Method basis</span>
              <strong>{formatNumber(counts.source_level_method_basis_sources)}</strong>
              <em>BAM or PM2.5 method context sources</em>
            </div>
            <div>
              <span>Technical standards</span>
              <strong>{formatNumber(counts.source_level_technical_standard_sources)}</strong>
              <em>standard, equipment, or operating-rule context</em>
            </div>
            <div>
              <span>Inspection rules</span>
              <strong>{formatNumber(counts.source_level_daily_log_or_inspection_sources)}</strong>
              <em>daily inspection or logbook context</em>
            </div>
            <div>
              <span>Calibration route/rule</span>
              <strong>{formatNumber(sourceLevelCalibration)}</strong>
              <em>periodic rule plus service-route sources</em>
            </div>
            <div>
              <span>Complete grade rows</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>source-level rules are not row-level certificates</em>
            </div>
          </div>

          <div className="air-bmkg-grade-family-grid" aria-label="BMKG grade-basis source families">
            {sourceFamilies.map((family) => (
              <article key={family.label} className="air-bmkg-grade-family">
                <span>{family.label}</span>
                <strong>{formatNumber(family.value)}</strong>
                <p>{family.detail}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-bridge air-bmkg-grade-bridge" aria-label="BMKG grade-basis source scan decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-bmkg-grade-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-grade-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
                <p>Station-level grade promotion remains blocked for every target BMKG row.</p>
              </article>
            ))}
          </div>

          <div className="air-bmkg-grade-source-grid" aria-label="BMKG grade-basis source records">
            {sources.map((source) => {
              const sourceTone = source.matched_calibration_terms
                ? "air-bmkg-grade-source-calibration"
                : source.matched_method_terms
                  ? "air-bmkg-grade-source-method"
                  : "air-bmkg-grade-source-empty";
              return (
                <article key={source.source_key} className={`air-bmkg-grade-source-card ${sourceTone}`}>
                  <div>
                    <span>{sentenceCaseStatus(source.source_role)}</span>
                    <strong>{source.source_name}</strong>
                    <b>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Method</dt>
                      <dd>{formatNumber(termCount(source.matched_method_terms))}</dd>
                    </div>
                    <div>
                      <dt>Standard</dt>
                      <dd>{formatNumber(termCount(source.matched_technical_standard_terms))}</dd>
                    </div>
                    <div>
                      <dt>Inspect</dt>
                      <dd>{formatNumber(termCount(source.matched_daily_log_terms))}</dd>
                    </div>
                    <div>
                      <dt>Calibrate</dt>
                      <dd>{formatNumber(termCount(source.matched_calibration_terms))}</dd>
                    </div>
                    <div>
                      <dt>Cert</dt>
                      <dd>{formatNumber(termCount(source.matched_certificate_terms))}</dd>
                    </div>
                    <div>
                      <dt>Rows</dt>
                      <dd>{formatNumber(source.matched_target_station_rows)}</dd>
                    </div>
                  </dl>
                  <p>{source.source_note}</p>
                </article>
              );
            })}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-grade-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-grade-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-grade-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-grade-basis-source-scan.md" download>
              Grade-basis note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-grade-basis-source-scan-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-grade-basis-source-scan.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG grade-basis source scan...</p>
      )}
    </section>
  );
}

function AirBmkgStationPublicContextPanel({
  summary,
}: {
  summary: BmkgStationPublicContextSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const termCount = (value: string) => value.split("||").filter(Boolean).length;

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-station-context-section" aria-label="BMKG station public-context source scan">
      <div className="air-grade-method-head air-bmkg-station-context-head">
        <div>
          <p className="kicker kicker-blue">BMKG station public-context source scan</p>
          <h2>Station papers name some rows. Certificates still do not appear.</h2>
          <p>
            This layer moves beyond central BMKG standards and checks station-unit
            publications, regulator reports, and station studies. It adds public
            station or deployment context for selected BMKG rows, while keeping
            inspection-log, calibration-certificate, status, complete-grade, and
            radius gates closed.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-station-context-callout">
          <span>Station certificate rows</span>
          <strong>{formatNumber(counts?.station_specific_calibration_certificate_rows ?? 0)}</strong>
          <p>{formatNumber(counts?.rows_with_any_public_station_context ?? 0)} rows gain public station or deployment context, not certification.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-station-context-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.station_public_context_source_urls_retrieved)}/{formatNumber(counts.station_public_context_source_urls_seeded)}</strong>
              <em>station-context routes</em>
            </div>
            <div>
              <span>Rows with context</span>
              <strong>{formatNumber(counts.rows_with_any_public_station_context)}</strong>
              <em>station/unit or deployment-area matches</em>
            </div>
            <div>
              <span>Station/unit exact</span>
              <strong>{formatNumber(counts.rows_with_station_unit_or_exact_context)}</strong>
              <em>stronger than city-only context</em>
            </div>
            <div>
              <span>Method context</span>
              <strong>{formatNumber(counts.rows_with_station_method_context)}</strong>
              <em>matched source contains BAM/PM2.5 terms</em>
            </div>
            <div>
              <span>Calibration language</span>
              <strong>{formatNumber(counts.rows_with_station_calibration_context)}</strong>
              <em>not certificate or current status</em>
            </div>
            <div>
              <span>Complete grade rows</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>station context is not grade closure</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-station-context-bridge" aria-label="BMKG station-context decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className={`air-grade-method-lane air-bmkg-station-context-lane air-bmkg-station-context-lane-${decision.decision}`}>
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-station-context-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
                <p>{decision.decision.includes("no_new") ? "No seeded source matched this row." : "Context moves the evidence trail, not the certificate gate."}</p>
              </article>
            ))}
          </div>

          <div className="air-bmkg-station-context-row-grid" aria-label="BMKG station-context matched rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className={`air-bmkg-station-context-row air-bmkg-station-context-row-${row.station_public_context_decision}`}>
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.station_public_context_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Unit</dt>
                    <dd>{formatNumber(row.station_unit_or_exact_context_sources)}</dd>
                  </div>
                  <div>
                    <dt>City</dt>
                    <dd>{formatNumber(row.city_or_deployment_context_sources)}</dd>
                  </div>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(row.method_context_sources)}</dd>
                  </div>
                  <div>
                    <dt>Calib.</dt>
                    <dd>{formatNumber(row.calibration_context_sources)}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <em>{sentenceCaseStatus(row.public_context_source_keys)}</em>
              </article>
            ))}
          </div>

          <div className="air-bmkg-station-context-source-grid" aria-label="BMKG station-context source records">
            {sources.map((source) => {
              const sourceTone = source.source_match_scope.includes("exact") || source.source_match_scope.includes("unit")
                ? "air-bmkg-station-context-source-exact"
                : source.matched_target_station_ids
                  ? "air-bmkg-station-context-source-city"
                  : "air-bmkg-station-context-source-empty";
              return (
                <article key={source.source_key} className={`air-bmkg-station-context-source ${sourceTone}`}>
                  <div>
                    <span>{sentenceCaseStatus(source.source_role)}</span>
                    <strong>{source.source_name}</strong>
                    <b>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Rows</dt>
                      <dd>{formatNumber(termCount(source.matched_target_station_ids))}</dd>
                    </div>
                    <div>
                      <dt>Alias</dt>
                      <dd>{formatNumber(termCount(source.matched_alias_terms))}</dd>
                    </div>
                    <div>
                      <dt>Method</dt>
                      <dd>{formatNumber(termCount(source.matched_method_terms))}</dd>
                    </div>
                    <div>
                      <dt>Calib.</dt>
                      <dd>{formatNumber(termCount(source.matched_calibration_terms))}</dd>
                    </div>
                  </dl>
                  <p>{source.source_note}</p>
                </article>
              );
            })}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-station-context-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-station-context-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-station-context-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-station-public-context-source-scan.md" download>
              Download station-context note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-station-public-context-source-scan-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-station-public-context-source-scan.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading BMKG station public-context source scan...</p>
      )}
    </section>
  );
}

function AirBmkgInstallationAuditPanel({
  summary,
}: {
  summary: BmkgInstallationAuditSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const termCount = (value: string) => value.split("||").filter(Boolean).length;

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-station-context-section air-bmkg-install-audit-section" aria-label="BMKG installation/audit source scan">
      <div className="air-grade-method-head air-bmkg-station-context-head air-bmkg-install-audit-head">
        <div>
          <p className="kicker kicker-blue">BMKG installation/audit source scan</p>
          <h2>One station shows audit context. Certificates still stay closed.</h2>
          <p>
            This pass moves from station studies to official BMKG installation,
            audit/calibration, public-information, and operational-monitoring
            routes. It adds one exact station audit/calibration signal and a
            2020 PM2.5 installation layer, while still finding no station
            certificate or calibration-status record.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-station-context-callout air-bmkg-install-audit-callout">
          <span>Station certificate rows</span>
          <strong>{formatNumber(counts?.station_specific_calibration_certificate_rows ?? 0)}</strong>
          <p>{formatNumber(counts?.rows_with_exact_station_audit_calibration_context ?? 0)} exact audit/calibration row, not certificate closure.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-station-context-stat-grid air-bmkg-install-audit-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.installation_audit_source_urls_retrieved)}/{formatNumber(counts.installation_audit_source_urls_seeded)}</strong>
              <em>official installation/audit routes</em>
            </div>
            <div>
              <span>Rows with context</span>
              <strong>{formatNumber(counts.rows_with_any_installation_or_audit_context)}</strong>
              <em>installation or audit context</em>
            </div>
            <div>
              <span>Exact audit row</span>
              <strong>{formatNumber(counts.rows_with_exact_station_audit_calibration_context)}</strong>
              <em>Kototabang station-level context</em>
            </div>
            <div>
              <span>Install/deploy rows</span>
              <strong>{formatNumber(counts.rows_with_pm25_installation_deployment_context)}</strong>
              <em>official PM2.5 installation layer</em>
            </div>
            <div>
              <span>Source-level routes</span>
              <strong>{formatNumber(counts.source_level_operational_or_calibration_sources)}</strong>
              <em>operations or calibration context only</em>
            </div>
            <div>
              <span>Complete grade rows</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>no certificate/status closure</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-station-context-bridge air-bmkg-install-audit-bridge" aria-label="BMKG installation/audit decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className={`air-grade-method-lane air-bmkg-station-context-lane air-bmkg-station-context-lane-${decision.decision} air-bmkg-install-audit-lane`}>
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-station-context-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
                <p>{decision.decision.includes("no_installation") ? "No seeded official source matched this row." : "Context moves the evidence trail, not the certificate gate."}</p>
              </article>
            ))}
          </div>

          <div className="air-bmkg-station-context-row-grid air-bmkg-install-audit-row-grid" aria-label="BMKG installation/audit matched rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className={`air-bmkg-station-context-row air-bmkg-install-audit-row air-bmkg-station-context-row-${row.installation_audit_decision}`}>
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.installation_audit_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Audit</dt>
                    <dd>{formatNumber(row.exact_station_audit_calibration_sources)}</dd>
                  </div>
                  <div>
                    <dt>Install</dt>
                    <dd>{formatNumber(row.pm25_installation_deployment_sources)}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <em>{sentenceCaseStatus(row.matched_source_keys)}</em>
              </article>
            ))}
          </div>

          <div className="air-bmkg-station-context-source-grid air-bmkg-install-audit-source-grid" aria-label="BMKG installation/audit source records">
            {sources.map((source) => {
              const sourceTone = source.source_match_scope.includes("exact")
                ? "air-bmkg-station-context-source-exact"
                : source.matched_target_station_ids
                  ? "air-bmkg-station-context-source-city"
                  : "air-bmkg-station-context-source-empty";
              return (
                <article key={source.source_key} className={`air-bmkg-station-context-source air-bmkg-install-audit-source ${sourceTone}`}>
                  <div>
                    <span>{sentenceCaseStatus(source.source_role)}</span>
                    <strong>{source.source_name}</strong>
                    <b>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</b>
                  </div>
                  <dl>
                    <div>
                      <dt>Rows</dt>
                      <dd>{formatNumber(termCount(source.matched_target_station_ids))}</dd>
                    </div>
                    <div>
                      <dt>PM2.5</dt>
                      <dd>{formatNumber(termCount(source.matched_pm25_terms))}</dd>
                    </div>
                    <div>
                      <dt>Audit</dt>
                      <dd>{formatNumber(termCount(source.matched_audit_terms))}</dd>
                    </div>
                    <div>
                      <dt>Calib.</dt>
                      <dd>{formatNumber(termCount(source.matched_calibration_terms))}</dd>
                    </div>
                  </dl>
                  <p>{source.source_note}</p>
                </article>
              );
            })}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-station-context-gate-grid air-bmkg-install-audit-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-station-context-gate air-bmkg-install-audit-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-bmkg-station-context-downloads air-bmkg-install-audit-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-installation-audit-source-scan.md" download>
              Download installation/audit note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-installation-audit-source-scan-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-installation-audit-source-scan.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading BMKG installation/audit source scan...</p>
      )}
    </section>
  );
}

function AirBmkgNearClosurePanel({
  summary,
}: {
  summary: BmkgNearClosureSummary | null;
}) {
  const counts = summary?.counts;
  const lanes = summary?.lane_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const laneTotal = Math.max(1, lanes.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-near-closure-section" aria-label="BMKG near-closure ledger">
      <div className="air-grade-method-head air-bmkg-near-closure-head">
        <div>
          <p className="kicker kicker-blue">BMKG near-closure ledger</p>
          <h2>Many gates are visible. The certificate gate is still empty.</h2>
          <p>
            This ledger combines the BMKG method classification, station-detail
            displays, CEWS dashboard status, source-level standards, station
            public-context scan, and installation/audit scan into one row-level
            closure view. It shows how close the evidence gets before the
            station-specific certificate, inspection log, or calibration-status
            gate stops the grade claim.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-near-closure-callout">
          <span>Complete-grade rows</span>
          <strong>{formatNumber(counts?.complete_monitor_grade_rows ?? 0)}</strong>
          <p>{formatNumber(counts?.station_specific_calibration_certificate_rows ?? 0)} public station-specific PM2.5 certificates in the current evidence stack.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-near-closure-stat-grid">
            <div>
              <span>BMKG rows</span>
              <strong>{formatNumber(counts.bmkg_target_rows)}</strong>
              <em>target station-detail rows</em>
            </div>
            <div>
              <span>ONLINE dashboard</span>
              <strong>{formatNumber(counts.dashboard_current_online_rows)}</strong>
              <em>{formatNumber(counts.dashboard_delayed_rows)} delayed row</em>
            </div>
            <div>
              <span>Method classified</span>
              <strong>{formatNumber(counts.station_method_classified_rows)}</strong>
              <em>BAM source-supported rows</em>
            </div>
            <div>
              <span>Source-level basis</span>
              <strong>{formatNumber(counts.source_level_grade_basis_rows)}</strong>
              <em>rules, service, certificate context</em>
            </div>
            <div>
              <span>Exact audit context</span>
              <strong>{formatNumber(counts.exact_audit_calibration_context_rows)}</strong>
              <em>context only, not certificate</em>
            </div>
            <div>
              <span>Calibration certificates</span>
              <strong>{formatNumber(counts.station_specific_calibration_certificate_rows)}</strong>
              <em>the closure blocker</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-bmkg-near-closure-lane-grid" aria-label="BMKG near-closure lanes">
            {lanes.map((lane) => (
              <article key={lane.lane} className={`air-grade-method-lane air-bmkg-near-closure-lane air-bmkg-near-closure-lane-${lane.lane}`}>
                <div>
                  <span>{sentenceCaseStatus(lane.lane)}</span>
                  <strong>{formatNumber(lane.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-bmkg-near-closure-track">
                  <i style={{ width: `${Math.max(4, (lane.rows / laneTotal) * 100)}%` }} />
                </div>
                <p>{lane.lane.includes("audit") ? "Closest row: exact audit/calibration context is visible but not a station PM2.5 certificate." : "Evidence remains useful as review targeting, not as grade closure."}</p>
              </article>
            ))}
          </div>

          <div className="air-bmkg-near-closure-row-grid" aria-label="BMKG near-closure station rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className={`air-bmkg-near-closure-row air-bmkg-near-closure-row-${row.near_closure_lane}`}>
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.near_closure_lane)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Visible</dt>
                    <dd>{formatNumber(row.visible_evidence_gate_count)}</dd>
                  </div>
                  <div>
                    <dt>Blocking</dt>
                    <dd>{formatNumber(row.blocking_gate_count)}</dd>
                  </div>
                  <div>
                    <dt>Status</dt>
                    <dd>{row.dashboard_status_raw || "missing"}</dd>
                  </div>
                  <div>
                    <dt>Cert.</dt>
                    <dd>{row.station_specific_calibration_certificate_found ? "yes" : "0"}</dd>
                  </div>
                </dl>
                <ul>
                  <li>Method: {row.method_classified ? row.station_method_class : "not classified"}</li>
                  <li>Source-level calibration routes: {formatNumber(row.source_level_periodic_calibration_rule_sources + row.source_level_calibration_service_sources)}</li>
                  <li>Exact/audit context: {formatNumber(row.exact_station_audit_calibration_sources)}</li>
                </ul>
                <p>{row.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-near-closure-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-near-closure-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.note}</p>
              </article>
            ))}
          </div>

          <p className="air-bmkg-near-closure-nonclaim">{summary.non_claim}</p>

          <div className="air-grade-method-downloads air-bmkg-near-closure-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-near-closure-ledger.md" download>
              Download near-closure note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-near-closure-ledger-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-near-closure-ledger.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading BMKG near-closure ledger...</p>
      )}
    </section>
  );
}

function AirBmkgCertificateStatusTargetedPanel({
  summary,
}: {
  summary: BmkgCertificateStatusTargetedSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const lanes = summary?.source_lane_counts ?? [];
  const decisions = summary?.decision_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const laneTotal = Math.max(1, lanes.reduce((sum, row) => sum + row.sources, 0));
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const termCount = (value: string) => value.split("||").filter(Boolean).length;

  return (
    <section className="showcase-section air-grade-method-section air-bmkg-certificate-section" aria-label="BMKG targeted certificate/status source scan">
      <div className="air-grade-method-head air-bmkg-certificate-head">
        <div>
          <p className="kicker kicker-blue">BMKG certificate/status search wall</p>
          <h2>The next search found maintenance context, not the missing certificate.</h2>
          <p>
            The previous ledger identified the exact closure blocker. This
            targeted pass follows the public-source trail around that blocker:
            Kototabang station-unit maintenance and audit pages, GAW station
            publications, BMKG inspection SOPs, service/tariff routes, and PPID
            certificate-request context. The reader can see where the search
            touched the wall instead of treating the absence as silence.
          </p>
        </div>
        <div className="air-grade-method-callout air-bmkg-certificate-callout">
          <span>Station certificates</span>
          <strong>{formatNumber(counts?.station_specific_calibration_certificate_rows ?? 0)}</strong>
          <p>
            {formatNumber(counts?.certificate_status_source_urls_retrieved ?? 0)} targeted public sources checked; {formatNumber(counts?.rows_with_exact_maintenance_context ?? 0)} station row gained exact maintenance context.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-bmkg-certificate-stat-grid">
            <div>
              <span>Sources checked</span>
              <strong>{formatNumber(counts.certificate_status_source_urls_retrieved)}</strong>
              <em>of {formatNumber(counts.certificate_status_source_urls_seeded)} seeded URLs</em>
            </div>
            <div>
              <span>Exact sources</span>
              <strong>{formatNumber(counts.exact_station_or_unit_source_urls_retrieved)}</strong>
              <em>Kototabang-focused station/unit trail</em>
            </div>
            <div>
              <span>Source-level routes</span>
              <strong>{formatNumber(counts.source_level_inspection_service_or_certificate_routes_retrieved)}</strong>
              <em>SOP, service, or certificate-request context</em>
            </div>
            <div>
              <span>Matched rows</span>
              <strong>{formatNumber(counts.rows_with_any_targeted_source_context)}</strong>
              <em>of {formatNumber(counts.target_bmkg_rows)} BMKG rows</em>
            </div>
            <div>
              <span>Calibration language</span>
              <strong>{formatNumber(counts.rows_with_exact_calibration_language_context)}</strong>
              <em>exact context only</em>
            </div>
            <div>
              <span>Complete grade</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>closure still blocked</em>
            </div>
          </div>

          <div className="air-bmkg-certificate-story-grid">
            <div className="air-bmkg-certificate-lane-grid" aria-label="BMKG certificate/status source-search lanes">
              {lanes.map((lane) => (
                <article key={lane.lane} className={`air-bmkg-certificate-lane air-bmkg-certificate-lane-${lane.lane}`}>
                  <div>
                    <span>{sentenceCaseStatus(lane.lane)}</span>
                    <strong>{formatNumber(lane.sources)} sources</strong>
                  </div>
                  <div className="air-bmkg-certificate-track">
                    <i style={{ width: `${Math.max(5, (lane.sources / laneTotal) * 100)}%` }} />
                  </div>
                </article>
              ))}
            </div>

            <div className="air-bmkg-certificate-decision-grid" aria-label="BMKG certificate/status station decisions">
              {decisions.map((decision) => (
                <article key={decision.decision} className={`air-bmkg-certificate-decision air-bmkg-certificate-decision-${decision.decision}`}>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                  <div className="air-bmkg-certificate-track">
                    <i style={{ width: `${Math.max(5, (decision.rows / decisionTotal) * 100)}%` }} />
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div className="air-bmkg-certificate-row-grid" aria-label="BMKG certificate/status matched station rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-bmkg-certificate-row">
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.certificate_status_decision)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Sources</dt>
                    <dd>{formatNumber(termCount(row.targeted_source_keys))}</dd>
                  </div>
                  <div>
                    <dt>Maint.</dt>
                    <dd>{formatNumber(row.exact_station_maintenance_sources)}</dd>
                  </div>
                  <div>
                    <dt>Calib.</dt>
                    <dd>{formatNumber(row.exact_station_calibration_language_sources)}</dd>
                  </div>
                  <div>
                    <dt>Cert.</dt>
                    <dd>{formatNumber(row.exact_station_certificate_language_sources)}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <em>{sentenceCaseStatus(row.targeted_source_keys)}</em>
              </article>
            ))}
          </div>

          <div className="air-bmkg-certificate-source-grid" aria-label="BMKG certificate/status source records">
            {sources.map((source) => (
              <article key={source.source_key} className={`air-bmkg-certificate-source air-bmkg-certificate-source-${source.source_search_lane}`}>
                <div>
                  <span>{sentenceCaseStatus(source.source_search_lane)}</span>
                  <strong>{source.source_name}</strong>
                  <b>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</b>
                </div>
                <dl>
                  <div>
                    <dt>Rows</dt>
                    <dd>{formatNumber(termCount(source.matched_target_station_ids))}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{formatNumber(termCount(source.matched_pm25_terms))}</dd>
                  </div>
                  <div>
                    <dt>Maint.</dt>
                    <dd>{formatNumber(termCount(source.matched_maintenance_terms))}</dd>
                  </div>
                  <div>
                    <dt>Cert.</dt>
                    <dd>{formatNumber(termCount(source.matched_certificate_terms))}</dd>
                  </div>
                </dl>
                <p>{source.source_note}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-certificate-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-certificate-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-bmkg-near-closure-nonclaim air-bmkg-certificate-nonclaim">{summary.non_claim}</p>

          <div className="air-grade-method-downloads air-bmkg-certificate-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-certificate-status-targeted-source-scan.md" download>
              Download certificate/status note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-certificate-status-targeted-source-scan-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-certificate-status-targeted-source-scan.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading BMKG targeted certificate/status source scan...</p>
      )}
    </section>
  );
}

function AirBmkgPpidAccessRoutePanel({
  summary,
}: {
  summary: BmkgPpidAccessRouteSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const lanes = summary?.source_lane_counts ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const laneTotal = Math.max(1, lanes.reduce((sum, row) => sum + row.sources, 0));
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const termCount = (value: string) => value.split("||").filter(Boolean).length;

  return (
    <section className="showcase-section air-bmkg-ppid-section" aria-label="BMKG PPID and PTSP access-route wall">
      <div className="air-bmkg-ppid-head">
        <div>
          <p className="kicker kicker-blue">BMKG PPID/PTSP access-route wall</p>
          <h2>The public route shows readings, not certificates.</h2>
          <p>
            BMKG rows are close enough to look convincing: BAM method, public
            PM2.5 display, dashboard status, and service routes are visible.
            This wall checks the official PPID/PTSP taxonomy before any row is
            promoted as complete monitor-grade evidence.
          </p>
        </div>
        <div className="air-bmkg-ppid-callout">
          <span>Station certificate rows</span>
          <strong>{formatNumber(counts?.station_specific_calibration_certificate_rows ?? 0)}</strong>
          <p>Public display is not the same as a calibration/status record.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-bmkg-ppid-stat-grid">
            <div>
              <span>Sources retrieved</span>
              <strong>{formatNumber(counts.ppid_access_source_urls_retrieved)}</strong>
              <em>of {formatNumber(counts.ppid_access_source_urls_seeded)} PPID/PTSP routes</em>
            </div>
            <div>
              <span>Public display rows</span>
              <strong>{formatNumber(counts.target_rows_on_public_pm25_display)}</strong>
              <em>of {formatNumber(counts.target_bmkg_rows)} BMKG targets</em>
            </div>
            <div>
              <span>PM2.5 catalog routes</span>
              <strong>{formatNumber(counts.public_pm25_catalog_route_sources)}</strong>
              <em>public-information taxonomy</em>
            </div>
            <div>
              <span>Calibration service routes</span>
              <strong>{formatNumber(counts.source_level_calibration_service_routes)}</strong>
              <em>source-level context only</em>
            </div>
            <div>
              <span>Certificate request context</span>
              <strong>{formatNumber(counts.certificate_request_context_sources)}</strong>
              <em>not a public station record</em>
            </div>
            <div>
              <span>Complete grade rows</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>no promotions</em>
            </div>
          </div>

          <div className="air-bmkg-ppid-story-grid">
            <div className="air-bmkg-ppid-lane-grid" aria-label="BMKG PPID source lanes">
              {lanes.map((lane) => (
                <article key={lane.lane} className={`air-bmkg-ppid-lane air-bmkg-ppid-lane-${lane.lane}`}>
                  <div>
                    <span>{sentenceCaseStatus(lane.lane)}</span>
                    <strong>{formatNumber(lane.sources)} sources</strong>
                  </div>
                  <div className="air-bmkg-ppid-track">
                    <i style={{ width: `${Math.max(5, (lane.sources / laneTotal) * 100)}%` }} />
                  </div>
                </article>
              ))}
            </div>

            <div className="air-bmkg-ppid-decision-grid" aria-label="BMKG PPID row decisions">
              {decisions.map((decision) => (
                <article key={decision.decision} className="air-bmkg-ppid-decision">
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                  <div className="air-bmkg-ppid-track">
                    <i style={{ width: `${Math.max(5, (decision.rows / decisionTotal) * 100)}%` }} />
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div className="air-bmkg-ppid-row-grid" aria-label="BMKG PPID target row decisions">
            {rows.map((row) => (
              <article key={row.source_station_id} className={`air-bmkg-ppid-row air-bmkg-ppid-row-${row.dashboard_status_raw.toLowerCase()}`}>
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                  <b>{sentenceCaseStatus(row.dashboard_status_raw || "unknown")}</b>
                </div>
                <dl>
                  <div>
                    <dt>Display</dt>
                    <dd>{row.public_pm25_display_route_available ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Service</dt>
                    <dd>{row.source_level_calibration_service_route_available ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Request</dt>
                    <dd>{row.source_level_certificate_request_context_available ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Raw limit</dt>
                    <dd>{row.raw_data_exclusion_context_available ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <em>{sentenceCaseStatus(row.access_route_decision)}</em>
              </article>
            ))}
          </div>

          <div className="air-bmkg-ppid-source-grid" aria-label="BMKG PPID and PTSP source records">
            {sources.map((source) => (
              <article key={source.source_key} className={`air-bmkg-ppid-source air-bmkg-ppid-source-${source.source_lane}`}>
                <div>
                  <span>{sentenceCaseStatus(source.source_lane)}</span>
                  <strong>{source.source_name}</strong>
                  <b>{source.retrieved ? `HTTP ${source.http_status}` : "not retrieved"}</b>
                </div>
                <dl>
                  <div>
                    <dt>Rows</dt>
                    <dd>{formatNumber(termCount(source.matched_target_station_ids))}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{formatNumber(termCount(source.matched_pm25_terms))}</dd>
                  </div>
                  <div>
                    <dt>Access</dt>
                    <dd>{formatNumber(termCount(source.matched_public_access_terms))}</dd>
                  </div>
                  <div>
                    <dt>Cert.</dt>
                    <dd>{formatNumber(termCount(source.matched_certificate_terms))}</dd>
                  </div>
                </dl>
                <p>{source.source_note}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-bmkg-ppid-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-bmkg-ppid-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-bmkg-ppid-nonclaim">{summary.non_claim}</p>

          <div className="air-grade-method-downloads air-bmkg-ppid-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/bmkg-ppid-access-route-scan.md" download>
              Download PPID/PTSP note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-ppid-access-route-scan-summary.json" download>
              Download summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-bmkg-ppid-access-route-scan.csv" download>
              Download row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading BMKG PPID/PTSP access-route scan...</p>
      )}
    </section>
  );
}

function AirGeorgiaReportVerificationPanel({
  summary,
}: {
  summary: GeorgiaReportVerificationSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.station_sample_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-georgia-report-section" aria-label="Georgia report verification source scan">
      <div className="air-grade-method-head air-georgia-report-head">
        <div>
          <p className="kicker kicker-blue">Georgia report verification scan</p>
          <h2>Official report rows still fail the verification gate.</h2>
          <p>
            The live Georgia data were already caution-labeled. This pass
            checks the official monthly report route for exact station codes,
            PM2.5 columns, and whether the report page removes that caution.
          </p>
        </div>
        <div className="air-grade-method-callout air-georgia-report-callout">
          <span>Verified closures</span>
          <strong>{formatNumber(counts?.verified_report_closure_available_rows ?? 0)}</strong>
          <p>Report rows exist, but the fetched page still says not verified.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-georgia-report-stat-grid">
            <div>
              <span>Georgia rows tested</span>
              <strong>{formatNumber(counts.target_georgia_rows)}</strong>
              <em>report month {summary.report_month}</em>
            </div>
            <div>
              <span>Station codes in report</span>
              <strong>{formatNumber(counts.station_code_in_monthly_report_rows)}</strong>
              <em>exact report-route rows</em>
            </div>
            <div>
              <span>PM2.5 report rows</span>
              <strong>{formatNumber(counts.pm25_column_in_monthly_report_rows)}</strong>
              <em>official monthly table columns</em>
            </div>
            <div>
              <span>Not-verified label</span>
              <strong>{formatNumber(counts.monthly_report_not_verified_label_rows)}</strong>
              <em>caution retained</em>
            </div>
            <div>
              <span>AQI note caution</span>
              <strong>{formatNumber(counts.aqi_note_live_data_unverified_caution_rows)}</strong>
              <em>live automatic data not verified</em>
            </div>
            <div>
              <span>Complete grade rows</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>no grade promotions</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-georgia-report-bridge" aria-label="Georgia report verification decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-georgia-report-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-georgia-report-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-georgia-report-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-georgia-report-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-row-grid air-georgia-report-row-grid">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-grade-method-row air-georgia-report-row">
                <div>
                  <span>{row.source_station_id}</span>
                  <strong>{row.source_station_name}</strong>
                </div>
                <p>{row.pm25_column_in_monthly_report ? "PM2.5 report row found" : "PM2.5 report row not found"}</p>
                <em>
                  code {row.station_code_in_monthly_report ? "yes" : "no"} /
                  not verified {row.monthly_report_not_verified_label_present ? "yes" : "no"}
                </em>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-georgia-report-downloads">
            <a href="/programs/air-monitoring/georgia-report-verification-source-scan.md">Read the note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-report-verification-source-scan-summary.json">Download JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-report-verification-source-scan.csv">Download CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading Georgia report verification source scan...</p>
      )}
    </section>
  );
}

function AirGeorgiaReportExportLadderPanel({
  summary,
}: {
  summary: GeorgiaReportExportLadderSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const months = summary?.month_rows ?? [];
  const probes = summary?.export_probe_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));

  return (
    <section className="showcase-section air-grade-method-section air-georgia-export-section" aria-label="Georgia report export verification ladder">
      <div className="air-grade-method-head air-georgia-export-head">
        <div>
          <p className="kicker kicker-crimson">Georgia export ladder</p>
          <h2>Two years of report pages do not remove the caution.</h2>
          <p>
            The one-month report check could have been a timing problem. This
            pass scans the official monthly route backward and probes the XLSX
            and PDF exports exposed by the same report page.
          </p>
        </div>
        <div className="air-grade-method-callout air-georgia-export-callout">
          <span>Clean verified months</span>
          <strong>{formatNumber(counts?.html_verified_label_without_not_verified_months ?? 0)}</strong>
          <p>Station-code PM2.5 rows appear; verification closure does not.</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-georgia-export-stat-grid">
            <div>
              <span>Months scanned</span>
              <strong>{formatNumber(counts.months_scanned)}</strong>
              <em>ending {summary.start_month}</em>
            </div>
            <div>
              <span>HTML retrieved</span>
              <strong>{formatNumber(counts.html_months_retrieved)}</strong>
              <em>official monthly routes</em>
            </div>
            <div>
              <span>PM2.5 report months</span>
              <strong>{formatNumber(counts.html_months_with_pm25_column)}</strong>
              <em>all target station codes present</em>
            </div>
            <div>
              <span>Not-verified months</span>
              <strong>{formatNumber(counts.html_not_verified_label_months)}</strong>
              <em>caution retained</em>
            </div>
            <div>
              <span>Export probes</span>
              <strong>{formatNumber(counts.export_probe_months)}</strong>
              <em>XLSX and PDF checked</em>
            </div>
            <div>
              <span>Verified closures</span>
              <strong>{formatNumber(counts.verified_report_closure_available_months)}</strong>
              <em>no promotions</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-georgia-export-bridge" aria-label="Georgia report export decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-georgia-export-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} months</strong>
                </div>
                <div className="air-grade-method-track air-georgia-export-track">
                  <i style={{ width: `${Math.max(4, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-georgia-export-ladder-wall">
            <div>
              <span>24-month runway</span>
              <h3>Every month has the row; no month clears the label.</h3>
              <p>
                Each tile is an official monthly report route. Solid warning
                tiles retain the not-verified footer; outlined tiles also had
                XLSX/PDF export probes.
              </p>
            </div>
            <div className="air-georgia-export-month-grid">
              {months.map((row) => (
                <article
                  key={row.report_month}
                  className={`air-georgia-export-month ${
                    row.html_verified_label_without_not_verified
                      ? "air-georgia-export-month-clear"
                      : row.xlsx_export_tested
                        ? "air-georgia-export-month-probe"
                        : "air-georgia-export-month-blocked"
                  }`}
                >
                  <span>{row.report_month}</span>
                  <strong>{row.html_not_verified_label_present ? "not verified" : "label open"}</strong>
                  <em>
                    {formatNumber(row.station_code_count_in_html)} codes / {row.pm25_column_in_html ? "PM2.5" : "no PM2.5"}
                  </em>
                  {row.xlsx_export_tested ? <b>export probe</b> : null}
                </article>
              ))}
            </div>
          </div>

          <div className="air-georgia-export-probe-grid">
            {probes.map((row) => (
              <article key={row.report_month} className="air-georgia-export-probe">
                <div>
                  <span>{row.report_month}</span>
                  <strong>Export probe</strong>
                </div>
                <dl>
                  <div>
                    <dt>XLSX sheets</dt>
                    <dd>
                      {formatNumber(row.xlsx_target_station_sheet_count)}/{formatNumber(counts.target_station_codes)}
                    </dd>
                  </div>
                  <div>
                    <dt>XLSX label</dt>
                    <dd>{row.xlsx_verification_label_present ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>PDF pages</dt>
                    <dd>{formatNumber(row.pdf_text_pages)}</dd>
                  </div>
                  <div>
                    <dt>PDF caution</dt>
                    <dd>{row.pdf_not_verified_label_present ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>
                  XLSX carries station sheets and PM2.5; PDF keeps the
                  not-verified footer. Neither route closes the grade gate.
                </p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-georgia-export-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-georgia-export-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-georgia-export-downloads">
            <a href="/programs/air-monitoring/georgia-report-export-ladder.md">Read the note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-report-export-ladder-summary.json">Download JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-report-export-ladder.csv">Download CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading Georgia report export ladder...</p>
      )}
    </section>
  );
}

function AirGeorgiaVerificationPolicyPanel({
  summary,
}: {
  summary: GeorgiaVerificationPolicySummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const sources = summary?.source_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const bridge = summary?.policy_bridge;
  const closureRows =
    (counts?.verified_report_closure_available_months ?? 0) +
    (counts?.current_status_confirmed_rows ?? 0) +
    (counts?.station_method_classified_rows ?? 0) +
    (counts?.complete_monitor_grade_classification_rows ?? 0);

  return (
    <section className="showcase-section air-grade-method-section air-georgia-policy-section" aria-label="Georgia verification policy wall">
      <div className="air-grade-method-head air-georgia-policy-head">
        <div>
          <p className="kicker kicker-blue">Georgia verification policy wall</p>
          <h2>The policy points to reports. The reports still point back to caution.</h2>
          <p>
            The portal says live automatic-station data are not verified and
            directs readers to reports for verified data. The report/export
            ladder then shows the public report surfaces we can retrieve still
            carry not-verified labels or no verification label.
          </p>
        </div>
        <div className="air-grade-method-callout air-georgia-policy-callout">
          <span>Closure rows</span>
          <strong>{formatNumber(closureRows)}</strong>
          <p>policy, reports, network pages, and plan context do not close station status</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-georgia-policy-stat-grid">
            <div>
              <span>Official source routes</span>
              <strong>{formatNumber(counts.source_routes_retrieved)}</strong>
              <em>of {formatNumber(counts.source_routes_targeted)} retrieved</em>
            </div>
            <div>
              <span>Live-data caution</span>
              <strong>{formatNumber(counts.live_data_not_verified_policy_sources)}</strong>
              <em>automatic station data not verified</em>
            </div>
            <div>
              <span>Reports named</span>
              <strong>{formatNumber(counts.verified_data_reports_policy_sources)}</strong>
              <em>verification surface in policy text</em>
            </div>
            <div>
              <span>Not-verified HTML months</span>
              <strong>{formatNumber(counts.html_not_verified_label_months)}</strong>
              <em>of {formatNumber(counts.months_scanned)} report pages</em>
            </div>
            <div>
              <span>PDF caution probes</span>
              <strong>{formatNumber(counts.pdf_export_probe_months_with_not_verified_label)}</strong>
              <em>of {formatNumber(counts.export_probe_months)} exports</em>
            </div>
            <div>
              <span>Verified closures</span>
              <strong>{formatNumber(counts.verified_report_closure_available_months)}</strong>
              <em>target station codes remain open</em>
            </div>
          </div>

          <div className="air-georgia-policy-bridge" aria-label="Georgia policy to report bridge">
            <article>
              <span>Policy rule</span>
              <strong>{bridge?.policy_says_reports_are_verified_surface ? "reports" : "missing"}</strong>
              <p>Official text directs verification away from live map data.</p>
            </article>
            <article>
              <span>Report surface</span>
              <strong>{bridge?.scanned_report_surfaces_still_not_verified ? "caution" : "clear"}</strong>
              <p>The 24-month ladder keeps the fetched report surface open.</p>
            </article>
            <article>
              <span>Reader decision</span>
              <strong>{bridge?.verified_report_closure_available ? "promote" : "keep blocked"}</strong>
              <p>{bridge?.reader_use}</p>
            </article>
          </div>

          <div className="air-grade-method-bridge air-georgia-policy-decision-grid" aria-label="Georgia verification policy decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-georgia-policy-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-georgia-policy-track">
                  <i style={{ width: `${Math.max(5, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-georgia-policy-source-grid">
            {sources.map((row) => (
              <article key={row.source_key} className="air-georgia-policy-source">
                <div>
                  <span>{row.source_role}</span>
                  <strong>{sentenceCaseStatus(row.source_key)}</strong>
                </div>
                <p>{row.reader_use}</p>
                <dl>
                  <div>
                    <dt>Expected</dt>
                    <dd>{row.matched_expected_terms ? formatNumber(row.matched_expected_terms.split("||").filter(Boolean).length) : "0"}</dd>
                  </div>
                  <div>
                    <dt>Verification</dt>
                    <dd>{row.matched_verification_terms ? formatNumber(row.matched_verification_terms.split("||").filter(Boolean).length) : "0"}</dd>
                  </div>
                  <div>
                    <dt>Instrument</dt>
                    <dd>{row.matched_instrument_terms ? formatNumber(row.matched_instrument_terms.split("||").filter(Boolean).length) : "0"}</dd>
                  </div>
                  <div>
                    <dt>Station areas</dt>
                    <dd>{row.matched_station_terms ? formatNumber(row.matched_station_terms.split("||").filter(Boolean).length) : "0"}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-georgia-policy-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-georgia-policy-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-georgia-policy-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/georgia-verification-policy.md">Policy note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-verification-policy-summary.json">Summary JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-verification-policy.csv">Source CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading Georgia verification-policy wall...</p>
      )}
    </section>
  );
}

function AirGeorgiaReportFrequencyPanel({
  summary,
}: {
  summary: GeorgiaReportFrequencySummary | null;
}) {
  const counts = summary?.coverage_counts;
  const frequencies = summary?.frequency_rows ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const samples = summary?.sample_rows ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const closureRoutes =
    (counts?.verified_report_closure_available_routes ?? 0) +
    (counts?.current_status_confirmed_routes ?? 0) +
    (counts?.complete_monitor_grade_classification_routes ?? 0);

  return (
    <section className="showcase-section air-grade-method-section air-georgia-frequency-section" aria-label="Georgia report frequency matrix">
      <div className="air-grade-method-head air-georgia-frequency-head">
        <div>
          <p className="kicker kicker-blue">Georgia report-frequency matrix</p>
          <h2>Daily reports repeat the caution. Annual reports do not open.</h2>
          <p>
            The policy says verified data are in reports, so this pass tests the
            daily, monthly, and annual report routes directly. Daily and monthly
            human-readable outputs keep the caution; annual probes return server
            errors for the tested formats.
          </p>
        </div>
        <div className="air-grade-method-callout air-georgia-frequency-callout">
          <span>Closure routes</span>
          <strong>{formatNumber(closureRoutes)}</strong>
          <p>frequency tests do not close verification, status, or grade</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-georgia-frequency-stat-grid">
            <div>
              <span>Route probes</span>
              <strong>{formatNumber(counts.route_probes_targeted)}</strong>
              <em>daily, monthly, annual</em>
            </div>
            <div>
              <span>Valid payloads</span>
              <strong>{formatNumber(counts.valid_payload_routes)}</strong>
              <em>daily/monthly only</em>
            </div>
            <div>
              <span>Annual server errors</span>
              <strong>{formatNumber(counts.annual_server_error_routes)}</strong>
              <em>tested date formats</em>
            </div>
            <div>
              <span>HTML/PDF cautions</span>
              <strong>{formatNumber(counts.html_pdf_not_verified_routes)}</strong>
              <em>not-verified payloads</em>
            </div>
            <div>
              <span>XLSX station sheets</span>
              <strong>{formatNumber(counts.xlsx_all_target_station_sheet_routes)}</strong>
              <em>verification labels: {formatNumber(counts.xlsx_verification_label_routes)}</em>
            </div>
            <div>
              <span>Verified closures</span>
              <strong>{formatNumber(counts.verified_report_closure_available_routes)}</strong>
              <em>target station codes remain open</em>
            </div>
          </div>

          <div className="air-georgia-frequency-grid" aria-label="Georgia report frequency outcomes">
            {frequencies.map((row) => (
              <article key={row.report_type} className={`air-georgia-frequency-card air-georgia-frequency-card-${row.report_type}`}>
                <div>
                  <span>{row.report_type}</span>
                  <strong>{formatNumber(row.route_probes)} probes</strong>
                </div>
                <p>{row.reader_use}</p>
                <dl>
                  <div>
                    <dt>Valid</dt>
                    <dd>{formatNumber(row.valid_payload_routes)}</dd>
                  </div>
                  <div>
                    <dt>Server errors</dt>
                    <dd>{formatNumber(row.server_error_routes)}</dd>
                  </div>
                  <div>
                    <dt>HTML caution</dt>
                    <dd>{formatNumber(row.html_not_verified_routes)}</dd>
                  </div>
                  <div>
                    <dt>PDF caution</dt>
                    <dd>{formatNumber(row.pdf_not_verified_routes)}</dd>
                  </div>
                  <div>
                    <dt>XLSX sheets</dt>
                    <dd>{formatNumber(row.xlsx_station_sheet_routes)}</dd>
                  </div>
                  <div>
                    <dt>Closures</dt>
                    <dd>{formatNumber(row.verified_closure_routes)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-bridge air-georgia-frequency-decision-grid" aria-label="Georgia report frequency decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-georgia-frequency-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-georgia-frequency-track">
                  <i style={{ width: `${Math.max(5, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-georgia-frequency-sample-grid">
            {samples.slice(0, 12).map((row) => (
              <article
                key={`${row.report_type}-${row.export_type}-${row.probe_date}`}
                className={`air-georgia-frequency-sample air-georgia-frequency-sample-${row.export_type}`}
              >
                <div>
                  <span>{row.report_type} / {row.export_type}</span>
                  <strong>{row.probe_date}</strong>
                </div>
                <dl>
                  <div>
                    <dt>HTTP</dt>
                    <dd>{formatNumber(row.http_status)}</dd>
                  </div>
                  <div>
                    <dt>Stations</dt>
                    <dd>{formatNumber(row.station_code_matches)}</dd>
                  </div>
                  <div>
                    <dt>PM2.5</dt>
                    <dd>{row.pm25_present ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Caution</dt>
                    <dd>{row.not_verified_label_present ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>{sentenceCaseStatus(row.report_frequency_decision)}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-georgia-frequency-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-georgia-frequency-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-georgia-frequency-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/georgia-report-frequency-matrix.md">Frequency note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-report-frequency-matrix-summary.json">Summary JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-report-frequency-matrix.csv">Source CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading Georgia report-frequency matrix...</p>
      )}
    </section>
  );
}

function AirGeorgiaNetworkLaunchPanel({
  summary,
}: {
  summary: GeorgiaNetworkLaunchSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const cities = summary?.city_rows ?? [];
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const closureRows =
    (counts?.verified_report_closure_available_rows ?? 0) +
    (counts?.current_status_confirmed_rows ?? 0) +
    (counts?.calibration_status_available_rows ?? 0) +
    (counts?.complete_monitor_grade_classification_rows ?? 0);

  return (
    <section className="showcase-section air-grade-method-section air-georgia-network-section" aria-label="Georgia station network and launch source scan">
      <div className="air-grade-method-head air-georgia-network-head">
        <div>
          <p className="kicker kicker-crimson">Georgia NEA network/launch scan</p>
          <h2>Official launch pages add context. Station codes still do not close.</h2>
          <p>
            After the report-frequency matrix kept Georgia verification open,
            this pass checks NEA network and station-launch pages. The sources
            improve public station-owner context for named cities, but they do
            not provide station-code verification, calibration, or current-status
            records.
          </p>
        </div>
        <div className="air-grade-method-callout air-georgia-network-callout">
          <span>Closure rows</span>
          <strong>{formatNumber(closureRows)}</strong>
          <p>city-level context is not complete monitor-grade evidence</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-georgia-network-stat-grid">
            <div>
              <span>NEA sources</span>
              <strong>{formatNumber(counts.source_records_retrieved)} / {formatNumber(counts.source_records)}</strong>
              <em>network and launch pages</em>
            </div>
            <div>
              <span>Georgia rows</span>
              <strong>{formatNumber(counts.target_georgia_rows)}</strong>
              <em>station-code queue</em>
            </div>
            <div>
              <span>Public context</span>
              <strong>{formatNumber(counts.rows_with_public_source_context)}</strong>
              <em>city or source context</em>
            </div>
            <div>
              <span>Launch context</span>
              <strong>{formatNumber(counts.rows_with_launch_source_context)}</strong>
              <em>station-city launches</em>
            </div>
            <div>
              <span>Current network</span>
              <strong>{formatNumber(counts.rows_with_current_network_city_context)}</strong>
              <em>city-level only</em>
            </div>
            <div>
              <span>Station codes</span>
              <strong>{formatNumber(counts.rows_with_station_code_in_source)}</strong>
              <em>no source-code closure</em>
            </div>
          </div>

          <div className="air-georgia-network-city-grid" aria-label="Georgia city-level source bridge">
            {cities.map((row) => (
              <article key={row.target_city} className={row.complete_grade_rows ? "air-georgia-network-city air-georgia-network-city-ready" : "air-georgia-network-city"}>
                <div>
                  <span>{row.target_city}</span>
                  <strong>{formatNumber(row.target_rows)} rows</strong>
                </div>
                <dl>
                  <div>
                    <dt>Context</dt>
                    <dd>{formatNumber(row.public_source_context_rows)}</dd>
                  </div>
                  <div>
                    <dt>Launch</dt>
                    <dd>{formatNumber(row.launch_source_context_rows)}</dd>
                  </div>
                  <div>
                    <dt>Current</dt>
                    <dd>{formatNumber(row.current_network_city_context_rows)}</dd>
                  </div>
                  <div>
                    <dt>Grade</dt>
                    <dd>{formatNumber(row.complete_grade_rows)}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>

          <div className="air-grade-method-bridge air-georgia-network-decision-grid" aria-label="Georgia NEA network launch decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-georgia-network-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-georgia-network-track">
                  <i style={{ width: `${Math.max(5, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-georgia-network-row-grid" aria-label="Georgia station network target rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-georgia-network-row">
                <div>
                  <span>{row.target_city}</span>
                  <strong>{row.source_station_id}</strong>
                </div>
                <p>{row.source_station_name}</p>
                <dl>
                  <div>
                    <dt>Launch</dt>
                    <dd>{row.launch_source_context ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Network</dt>
                    <dd>{row.current_network_city_context ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>PM2.5/std</dt>
                    <dd>{row.city_level_standard_equipment_context ? "yes" : "no"}</dd>
                  </div>
                  <div>
                    <dt>Code</dt>
                    <dd>{row.station_code_in_source ? "yes" : "no"}</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-georgia-network-source-grid" aria-label="Georgia NEA network launch source records">
            {sources.map((source) => (
              <article key={source.source_key} className={`air-georgia-network-source air-georgia-network-source-${source.source_role}`}>
                <div>
                  <span>{source.source_role.replaceAll("_", " ")}</span>
                  <strong>{source.source_name}</strong>
                </div>
                <dl>
                  <div>
                    <dt>HTTP</dt>
                    <dd>{formatNumber(source.http_status)}</dd>
                  </div>
                  <div>
                    <dt>Cities</dt>
                    <dd>{formatNumber(source.matched_city_terms.length)}</dd>
                  </div>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(source.matched_method_terms.length)}</dd>
                  </div>
                  <div>
                    <dt>Current</dt>
                    <dd>{formatNumber(source.matched_current_terms.length)}</dd>
                  </div>
                </dl>
                <p>{source.source_note}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-georgia-network-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-georgia-network-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-grade-method-downloads air-georgia-network-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/georgia-station-network-launch-source-scan.md">Network/launch note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan-summary.json">Summary JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-station-network-launch-source-scan.csv">Row CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading Georgia station network/launch source scan...</p>
      )}
    </section>
  );
}

function AirGeorgiaIndicatorEndpointPanel({
  summary,
}: {
  summary: GeorgiaIndicatorEndpointSummary | null;
}) {
  const counts = summary?.coverage_counts;
  const decisions = summary?.decision_counts ?? [];
  const gates = summary?.evidence_gate_counts ?? [];
  const rows = summary?.display_rows ?? [];
  const sources = summary?.source_records ?? [];
  const termCount = (value: string) => value.split("||").filter(Boolean).length;
  const decisionTotal = Math.max(1, decisions.reduce((sum, row) => sum + row.rows, 0));
  const closureRows =
    (counts?.exact_indicator_station_code_rows ?? 0) +
    (counts?.daily_endpoint_verified_closure_rows ?? 0) +
    (counts?.current_status_confirmed_rows ?? 0) +
    (counts?.calibration_status_available_rows ?? 0) +
    (counts?.complete_monitor_grade_classification_rows ?? 0);

  return (
    <section className="showcase-section air-grade-method-section air-georgia-network-section air-georgia-indicator-section" aria-label="Georgia indicator endpoint mismatch scan">
      <div className="air-grade-method-head air-georgia-network-head air-georgia-indicator-head">
        <div>
          <p className="kicker kicker-blue">Georgia indicator endpoint mismatch</p>
          <h2>The official indicator API is real, but it is not the report-code bridge.</h2>
          <p>
            The air.gov.ge page template exposes indicator and daily API routes.
            This pass checks whether those endpoints name the 16 target station
            codes from the report surface. The indicator endpoint returns a
            broad station object layer, but the target codes do not appear.
          </p>
        </div>
        <div className="air-grade-method-callout air-georgia-network-callout air-georgia-indicator-callout">
          <span>Exact code matches</span>
          <strong>{formatNumber(counts?.exact_indicator_station_code_rows ?? 0)}</strong>
          <p>city aliases remain non-closure evidence</p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-grade-method-stat-grid air-georgia-network-stat-grid air-georgia-indicator-stat-grid">
            <div>
              <span>Routes retrieved</span>
              <strong>{formatNumber(counts.source_routes_retrieved)} / {formatNumber(counts.source_routes_seeded)}</strong>
              <em>indicator plus daily probe</em>
            </div>
            <div>
              <span>Indicator objects</span>
              <strong>{formatNumber(counts.indicator_api_station_objects)}</strong>
              <em>official API station layer</em>
            </div>
            <div>
              <span>Target rows</span>
              <strong>{formatNumber(counts.target_georgia_rows)}</strong>
              <em>report-code queue</em>
            </div>
            <div>
              <span>City alias context</span>
              <strong>{formatNumber(counts.indicator_city_alias_context_rows)}</strong>
              <em>different code namespace</em>
            </div>
            <div>
              <span>PM2.5 alias rows</span>
              <strong>{formatNumber(counts.indicator_pm25_context_rows)}</strong>
              <em>no PM2.5 closure in this layer</em>
            </div>
            <div>
              <span>Closure rows</span>
              <strong>{formatNumber(closureRows)}</strong>
              <em>status, calibration, grade still open</em>
            </div>
          </div>

          <div className="air-grade-method-bridge air-georgia-network-decision-grid air-georgia-indicator-decision-grid" aria-label="Georgia indicator endpoint decisions">
            {decisions.map((decision) => (
              <article key={decision.decision} className="air-grade-method-lane air-georgia-network-lane air-georgia-indicator-lane">
                <div>
                  <span>{sentenceCaseStatus(decision.decision)}</span>
                  <strong>{formatNumber(decision.rows)} rows</strong>
                </div>
                <div className="air-grade-method-track air-georgia-network-track air-georgia-indicator-track">
                  <i style={{ width: `${Math.max(5, (decision.rows / decisionTotal) * 100)}%` }} />
                </div>
              </article>
            ))}
          </div>

          <div className="air-georgia-network-row-grid air-georgia-indicator-row-grid" aria-label="Georgia indicator endpoint target rows">
            {rows.map((row) => (
              <article key={row.source_station_id} className="air-georgia-network-row air-georgia-indicator-row">
                <div>
                  <span>{row.target_city}</span>
                  <strong>{row.source_station_id}</strong>
                </div>
                <p>{row.source_station_name}</p>
                <dl>
                  <div>
                    <dt>Alias codes</dt>
                    <dd>{formatNumber(termCount(row.matched_indicator_codes))}</dd>
                  </div>
                  <div>
                    <dt>Alias stations</dt>
                    <dd>{formatNumber(row.matched_indicator_station_count)}</dd>
                  </div>
                  <div>
                    <dt>PM2.5 alias</dt>
                    <dd>{formatNumber(row.matched_indicator_pm25_station_count)}</dd>
                  </div>
                  <div>
                    <dt>Exact code</dt>
                    <dd>0</dd>
                  </div>
                </dl>
                <p>{row.reader_use}</p>
                <em>{sentenceCaseStatus(row.indicator_endpoint_decision)}</em>
              </article>
            ))}
          </div>

          <div className="air-georgia-network-source-grid air-georgia-indicator-source-grid" aria-label="Georgia indicator endpoint source records">
            {sources.map((source) => (
              <article key={source.source_key} className={`air-georgia-network-source air-georgia-indicator-source air-georgia-indicator-source-${source.source_role}`}>
                <div>
                  <span>{source.source_role.replaceAll("_", " ")}</span>
                  <strong>{source.source_name}</strong>
                </div>
                <dl>
                  <div>
                    <dt>HTTP</dt>
                    <dd>{source.http_status ? formatNumber(Number(source.http_status)) : "open"}</dd>
                  </div>
                  <div>
                    <dt>JSON rows</dt>
                    <dd>{formatNumber(source.json_array_rows)}</dd>
                  </div>
                  <div>
                    <dt>Codes</dt>
                    <dd>{formatNumber(termCount(source.matched_station_code_terms))}</dd>
                  </div>
                  <div>
                    <dt>Verified</dt>
                    <dd>{formatNumber(termCount(source.matched_verification_terms))}</dd>
                  </div>
                </dl>
                <p>{source.source_note}</p>
                {source.retrieval_error ? <p>{source.retrieval_error}</p> : null}
              </article>
            ))}
          </div>

          <div className="air-grade-method-gate-grid air-georgia-network-gate-grid air-georgia-indicator-gate-grid">
            {gates.map((gate) => (
              <article key={gate.gate} className={`air-grade-method-gate air-georgia-network-gate air-georgia-indicator-gate air-grade-method-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <em>{formatNumber(gate.rows)} rows</em>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <p className="air-georgia-indicator-nonclaim">{summary.non_claim}</p>

          <div className="air-grade-method-downloads air-georgia-network-downloads air-georgia-indicator-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/georgia-indicator-endpoint-mismatch.md">Endpoint mismatch note</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-indicator-endpoint-mismatch-summary.json">Summary JSON</a>
            <a href="/programs/air-monitoring/generated/air-monitoring-georgia-indicator-endpoint-mismatch.csv">Row CSV</a>
          </div>
        </>
      ) : (
        <p className="air-grade-method-loading">Loading Georgia indicator endpoint mismatch scan...</p>
      )}
    </section>
  );
}

function AirMonitorGradePanel({ summary }: { summary: MonitorGradeSummary | null }) {
  const counts = summary?.coverage_counts;
  const rows = summary?.country_rows ?? [];
  const totalRows = Math.max(1, counts?.official_station_rows_audited ?? rows.reduce((sum, row) => sum + row.rows_audited, 0));
  const countryRows = [...rows].sort((a, b) => {
    const methodDelta = b.method_standard_signal_rows - a.method_standard_signal_rows;
    if (methodDelta !== 0) return methodDelta;
    return b.rows_audited - a.rows_audited;
  });
  const ladder = counts
    ? [
        {
          key: "method",
          label: "Method-standard signal",
          rows: counts.method_standard_signal_rows,
          detail: `${formatNumber(counts.economies_with_method_standard_signal)} economy with source-specific method language`,
          tone: "method",
        },
        {
          key: "portal",
          label: "Automatic or portal only",
          rows: counts.automatic_or_official_portal_signal_only_rows,
          detail: "provenance signal, not monitor-grade certification",
          tone: "portal",
        },
        {
          key: "sensor",
          label: "Sensor under test",
          rows: counts.sensor_under_test_rows,
          detail: "explicit caution rows, not regulatory-grade evidence",
          tone: "sensor",
        },
        {
          key: "missing",
          label: "No grade language found",
          rows: counts.no_public_grade_language_rows,
          detail: "official rows still need method documentation",
          tone: "missing",
        },
        {
          key: "complete",
          label: "Complete classification",
          rows: counts.complete_monitor_grade_classification_rows,
          detail: "station-radius assumptions remain blocked",
          tone: "blocked",
        },
      ]
    : [];

  return (
    <section className="showcase-section air-monitor-grade-section" aria-label="Monitor-grade evidence audit">
      <div className="air-monitor-grade-head">
        <div>
          <p className="kicker kicker-sage">Monitor-grade evidence</p>
          <h2>Monitor grade is a source-language ladder, not a yes/no.</h2>
          <p>
            The audit reads the official station rows and separates explicit
            method-standard language from weaker automatic-station or portal
            provenance. Bangladesh moves above a flat zero, but the regional
            classification remains incomplete.
          </p>
        </div>
        <div className="air-monitor-grade-nonclaim">
          <strong>Still not grade-ready</strong>
          <p>
            Complete monitor-grade classification remains at{" "}
            {formatNumber(counts?.complete_monitor_grade_classification_rows ?? 0)} rows.
            The next claim should be source reconciliation, not station-radius
            population coverage.
          </p>
        </div>
      </div>

      {summary && counts ? (
        <>
          <div className="air-monitor-grade-stat-grid">
            <div>
              <span>Official rows audited</span>
              <strong>{formatNumber(counts.official_station_rows_audited)}</strong>
              <em>{formatNumber(counts.official_coordinate_rows_audited)} have coordinates</em>
            </div>
            <div>
              <span>Method-standard signal</span>
              <strong>{formatNumber(counts.method_standard_signal_rows)}</strong>
              <em>{formatNumber(counts.economies_with_method_standard_signal)} economy</em>
            </div>
            <div>
              <span>Portal-only signal</span>
              <strong>{formatNumber(counts.automatic_or_official_portal_signal_only_rows)}</strong>
              <em>not certification</em>
            </div>
            <div>
              <span>Sensor under test</span>
              <strong>{formatNumber(counts.sensor_under_test_rows)}</strong>
              <em>caution rows</em>
            </div>
            <div>
              <span>Complete classifications</span>
              <strong>{formatNumber(counts.complete_monitor_grade_classification_rows)}</strong>
              <em>catchment still blocked</em>
            </div>
          </div>

          <div className="air-monitor-grade-ladder" aria-label="Monitor-grade evidence ladder by row count">
            {ladder.map((step) => {
              const width = step.rows > 0 ? `${Math.max(5, (step.rows / totalRows) * 100)}%` : "0%";
              return (
                <article key={step.key} className={`air-monitor-grade-ladder-card air-monitor-grade-ladder-card-${step.tone}`}>
                  <div>
                    <span>{step.label}</span>
                    <strong>{formatNumber(step.rows)}</strong>
                  </div>
                  <div className="air-monitor-grade-ladder-track">
                    <i style={{ width }} />
                  </div>
                  <p>{step.detail}</p>
                </article>
              );
            })}
          </div>

          <div className="air-monitor-grade-country-grid">
            {countryRows.map((row) => (
              <article
                key={row.iso3}
                className={`air-monitor-grade-country air-monitor-grade-country-${row.dominant_grade_evidence_category}`}
              >
                <div>
                  <span>{row.iso3}</span>
                  <strong>{row.country}</strong>
                  <b>{gradeCategoryLabel(row.dominant_grade_evidence_category)}</b>
                </div>
                <dl>
                  <div>
                    <dt>Rows</dt>
                    <dd>{formatNumber(row.rows_audited)}</dd>
                  </div>
                  <div>
                    <dt>Method</dt>
                    <dd>{formatNumber(row.method_standard_signal_rows)}</dd>
                  </div>
                  <div>
                    <dt>Portal</dt>
                    <dd>{formatNumber(row.automatic_or_official_portal_signal_rows)}</dd>
                  </div>
                  <div>
                    <dt>Sensor</dt>
                    <dd>{formatNumber(row.sensor_under_test_rows)}</dd>
                  </div>
                  <div>
                    <dt>Complete</dt>
                    <dd>{formatNumber(row.complete_monitor_grade_classification_rows)}</dd>
                  </div>
                </dl>
                <p>{row.source_name}</p>
              </article>
            ))}
          </div>

          <div className="air-monitor-grade-gate-grid">
            {summary.evidence_gate_counts.map((gate) => (
              <article key={gate.gate} className={`air-monitor-grade-gate air-monitor-grade-gate-${gateTone(gate.status)}`}>
                <span>{sentenceCaseStatus(gate.status)}</span>
                <strong>{gate.gate}</strong>
                <b>{formatNumber(gate.rows)} rows</b>
                <p>{gate.reader_use}</p>
              </article>
            ))}
          </div>

          <div className="air-monitor-grade-downloads">
            <span>{summary.method}</span>
            <a href="/programs/air-monitoring/monitor-grade-evidence.md" download>
              Audit note
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-evidence-summary.json" download>
              Summary JSON
            </a>
            <a href="/programs/air-monitoring/generated/air-monitoring-monitor-grade-evidence.csv" download>
              Row CSV
            </a>
          </div>
        </>
      ) : (
        <p className="showcase-loading">Loading monitor-grade evidence audit...</p>
      )}
    </section>
  );
}

function StationCoordinateMap({
  rows,
  countryRows,
}: {
  rows: StationMetadataStationRow[];
  countryRows: StationMetadataCountryRow[];
}) {
  const plotted = rows.filter(
    (row) =>
      row.latitude !== null &&
      row.longitude !== null &&
      Number.isFinite(row.latitude) &&
      Number.isFinite(row.longitude),
  );
  const width = 820;
  const height = 430;
  const lonMin = 42;
  const lonMax = 145;
  const latMin = -12;
  const latMax = 45;
  const x = (lon: number) => ((lon - lonMin) / (lonMax - lonMin)) * width;
  const y = (lat: number) => height - ((lat - latMin) / (latMax - latMin)) * height;
  const maxCountry = Math.max(1, ...countryRows.map((row) => row.openaq_pm25_locations_fetched));
  const countryCounts = new Map(countryRows.map((row) => [row.iso3, row.openaq_pm25_locations_fetched]));

  return (
    <div className="air-station-map-wrap">
      <svg viewBox={`0 0 ${width} ${height}`} className="air-station-map" role="img" aria-label="OpenAQ PM2.5 station coordinates for upgrade-queue economies">
        <defs>
          <radialGradient id="airStationGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.95" />
            <stop offset="55%" stopColor="#007db8" stopOpacity="0.75" />
            <stop offset="100%" stopColor="#007db8" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect x="0" y="0" width={width} height={height} rx="0" className="air-map-bg" />
        {[50, 70, 90, 110, 130].map((lon) => (
          <g key={`lon-${lon}`}>
            <line x1={x(lon)} x2={x(lon)} y1={0} y2={height} className="air-map-grid" />
            <text x={x(lon) + 4} y={height - 10} className="air-map-tick">
              {lon}E
            </text>
          </g>
        ))}
        {[-10, 0, 15, 30, 45].map((lat) => (
          <g key={`lat-${lat}`}>
            <line x1={0} x2={width} y1={y(lat)} y2={y(lat)} className="air-map-grid" />
            <text x={8} y={y(lat) - 5} className="air-map-tick">
              {lat} deg
            </text>
          </g>
        ))}
        <path
          d={`M ${x(60)} ${y(36)} C ${x(76)} ${y(30)}, ${x(88)} ${y(24)}, ${x(96)} ${y(16)} S ${x(113)} ${y(2)}, ${x(126)} ${y(-6)}`}
          className="air-map-region-line"
        />
        {plotted.map((row) => {
          const lon = row.longitude ?? 0;
          const lat = row.latitude ?? 0;
          const countryCount = countryCounts.get(row.iso3) ?? 1;
          const radius = 3.2 + (countryCount / maxCountry) * 5.5;
          return (
            <g key={`${row.iso3}-${row.openaq_location_id}`}>
              <circle cx={x(lon)} cy={y(lat)} r={radius + 8} className="air-station-glow" />
              <circle
                cx={x(lon)}
                cy={y(lat)}
                r={radius}
                className={row.is_monitor ? "air-station-dot air-station-monitor" : "air-station-dot air-station-sensor"}
              />
            </g>
          );
        })}
        {["BGD", "IDN", "MYS", "AFG", "UZB"].map((iso) => {
          const station = plotted.find((row) => row.iso3 === iso);
          if (!station || station.latitude === null || station.longitude === null) return null;
          return (
            <text key={iso} x={x(station.longitude) + 10} y={y(station.latitude) - 8} className="air-map-label">
              {iso}
            </text>
          );
        })}
      </svg>
      <div className="air-station-map-legend">
        <span><b className="legend-dot monitor" /> OpenAQ isMonitor row</span>
        <span><b className="legend-dot sensor" /> Other public PM2.5 sensor row</span>
        <span>{formatNumber(plotted.length)} coordinate rows, no catchment radius applied</span>
      </div>
    </div>
  );
}

function AirHeroConcentration({ data }: { data: DeepeningData }) {
  const top = data.part_a_concentration.rows.slice(0, 3);
  const restShare = 1 - top.reduce((sum, row) => sum + row.share_of_zero_monitor_pop, 0);
  const segments = [
    ...top.map((row) => ({
      key: row.iso3,
      label: row.iso3,
      share: row.share_of_zero_monitor_pop,
      background: row.iso3 === "PNG" ? "#007db8" : row.iso3 === "TLS" ? "#5a8227" : "#fbb00e",
      color: row.iso3 === "FJI" ? "#212529" : "#ffffff",
    })),
    { key: "REST", label: "REST", share: Math.max(0, restShare), background: "#9b2226", color: "#ffffff" },
  ];
  let x = 0;
  return (
    <div className="air-hero-stack-wrap">
      <div className="air-hero-stack" aria-label="Zero-monitor population share">
        {segments.map((segment) => {
          const width = segment.share * 100;
          const style = {
            left: `${x}%`,
            width: `${width}%`,
            background: segment.background,
            color: segment.color,
          };
          x += width;
          return (
            <span key={segment.key} className={`air-stack-segment air-stack-${segment.key.toLowerCase()}`} style={style}>
              {segment.label}
            </span>
          );
        })}
      </div>
      <p>
        PNG is {pct(data.part_a_concentration.png_share)}. PNG + Timor-Leste
        is {pct(data.part_a_concentration.png_plus_timor_share)}.
      </p>
    </div>
  );
}

function ZeroMonitorChart({ rows, focusIso }: { rows: ZeroMonitorRow[]; focusIso: string }) {
  const width = 760;
  const rowH = 36;
  const margin = { top: 34, right: 110, bottom: 34, left: 150 };
  const height = margin.top + margin.bottom + rows.length * rowH;
  const x = (value: number) => margin.left + value * (width - margin.left - margin.right);

  return (
    <div className="air-chart-wrap">
      <svg className="air-zero-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Zero-monitor population concentration chart">
        <text x={margin.left} y={18} className="air-chart-title">
          Zero-monitor population share
        </text>
        <line x1={margin.left} x2={x(1)} y1={height - margin.bottom + 4} y2={height - margin.bottom + 4} className="air-axis" />
        {[0, 0.25, 0.5, 0.75, 1].map((tick) => (
          <g key={tick}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top - 8} y2={height - margin.bottom + 4} className="air-grid" />
            <text x={x(tick)} y={height - 10} textAnchor="middle" className="air-tick">
              {pct(tick, 0)}
            </text>
          </g>
        ))}
        {rows.map((row, index) => {
          const y = margin.top + index * rowH;
          const barW = Math.max(2, x(row.share_of_zero_monitor_pop) - margin.left);
          const isFocus = row.iso3 === focusIso;
          const isTop2 = row.iso3 === "PNG" || row.iso3 === "TLS";
          return (
            <g key={row.iso3} className={isFocus ? "is-focus" : ""}>
              <text x={margin.left - 12} y={y + 18} textAnchor="end" className="air-label">
                {row.iso3}
              </text>
              <rect
                x={margin.left}
                y={y + 4}
                width={barW}
                height={22}
                rx={2}
                className={isTop2 ? "air-zero-bar air-zero-top2" : "air-zero-bar"}
              />
              <circle cx={x(row.cumulative_share)} cy={y + 15} r={isFocus ? 5 : 3.5} className="air-cumulative-dot" />
              <text x={margin.left + barW + 8} y={y + 18} className="air-value">
                {pct(row.share_of_zero_monitor_pop)}
              </text>
            </g>
          );
        })}
        <text x={x(0.8351)} y={margin.top - 14} textAnchor="middle" className="air-callout">
          PNG + TLS = 83.5%
        </text>
      </svg>
    </div>
  );
}

function GdpResidualChart({
  rows,
  positiveRows,
  focusIso,
  intercept,
  slope,
}: {
  rows: ResidualRow[];
  positiveRows: ResidualRow[];
  focusIso: string;
  intercept: number;
  slope: number;
}) {
  const width = 780;
  const height = 480;
  const margin = { top: 34, right: 34, bottom: 58, left: 72 };
  const valid = rows.filter((row) => row.gdp_pc_current_usd && row.people_per_monitor > 0);
  const xs = valid.map((row) => log10(row.gdp_pc_current_usd || 1));
  const ys = valid.map((row) => log10(row.people_per_monitor));
  const xMin = Math.floor(Math.min(...xs) * 10) / 10;
  const xMax = Math.ceil(Math.max(...xs) * 10) / 10;
  const yMin = Math.floor(Math.min(...ys) * 10) / 10;
  const yMax = Math.ceil(Math.max(...ys) * 10) / 10;
  const x = (value: number) => margin.left + ((value - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
  const y = (value: number) => height - margin.bottom - ((value - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);
  const topSet = new Set(positiveRows.slice(0, 5).map((row) => row.iso3));

  return (
    <div className="air-chart-wrap">
      <svg className="air-residual-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="GDP residual chart for public PM2.5 monitor density">
        <text x={margin.left} y={20} className="air-chart-title">
          Monitor density against GDP per capita
        </text>
        {[3, 4, 5].map((tick) => (
          <g key={`x-${tick}`}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} className="air-grid" />
            <text x={x(tick)} y={height - 22} textAnchor="middle" className="air-tick">
              {tick === 3 ? "$1k" : tick === 4 ? "$10k" : "$100k"}
            </text>
          </g>
        ))}
        {[5, 6, 7].map((tick) => (
          <g key={`y-${tick}`}>
            <line x1={margin.left} x2={width - margin.right} y1={y(tick)} y2={y(tick)} className="air-grid" />
            <text x={margin.left - 10} y={y(tick) + 4} textAnchor="end" className="air-tick">
              {tick === 5 ? "100k" : tick === 6 ? "1M" : "10M"}
            </text>
          </g>
        ))}
        <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom} y2={height - margin.bottom} className="air-axis" />
        <line x1={margin.left} x2={margin.left} y1={margin.top} y2={height - margin.bottom} className="air-axis" />
        <line
          x1={x(xMin)}
          y1={y(intercept + slope * xMin)}
          x2={x(xMax)}
          y2={y(intercept + slope * xMax)}
          className="air-fit-line"
        />
        {valid.map((row) => {
          const px = x(log10(row.gdp_pc_current_usd || 1));
          const py = y(log10(row.people_per_monitor));
          const isFocus = row.iso3 === focusIso;
          const isTop = topSet.has(row.iso3);
          return (
            <g key={row.iso3}>
              <circle
                cx={px}
                cy={py}
                r={isFocus ? 8 : isTop ? 6 : 4}
                className={isTop ? "air-residual-point air-residual-top" : "air-residual-point"}
              />
              {(isFocus || isTop) && (
                <text x={px + 8} y={py - 8} className="air-point-label">
                  {row.iso3}
                </text>
              )}
            </g>
          );
        })}
        <text x={width / 2} y={height - 6} textAnchor="middle" className="air-axis-label">
          GDP per capita, current US$ (log scale)
        </text>
        <text transform={`translate(18 ${height / 2}) rotate(-90)`} textAnchor="middle" className="air-axis-label">
          people per public PM2.5 monitor (log scale)
        </text>
      </svg>
    </div>
  );
}

function ExposureMonitorChart({ rows, focusIso }: { rows: AirPanelRow[]; focusIso: string }) {
  const plotted = rows.filter((row) => row.population > 0 && row.pm25_exposure_ugm3 > 0);
  const width = 780;
  const height = 480;
  const margin = { top: 34, right: 38, bottom: 58, left: 70 };
  const xMin = 0;
  const xMax = 50;
  const yMin = -0.1;
  const yMax = 3.4;
  const x = (value: number) => margin.left + ((value - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
  const y = (locations: number) => {
    const logValue = locations === 0 ? 0 : log10(locations + 1);
    return height - margin.bottom - ((logValue - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);
  };

  return (
    <div className="air-chart-wrap">
      <svg className="air-exposure-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="PM2.5 exposure versus public monitor count">
        <text x={margin.left} y={20} className="air-chart-title">
          Exposure versus public PM2.5 monitor count
        </text>
        {[5, 15, 30, 45].map((tick) => (
          <g key={`x-${tick}`}>
            <line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} className="air-grid" />
            <text x={x(tick)} y={height - 22} textAnchor="middle" className="air-tick">
              {tick}
            </text>
          </g>
        ))}
        {[0, 1, 2, 3].map((tick) => (
          <g key={`y-${tick}`}>
            <line x1={margin.left} x2={width - margin.right} y1={height - margin.bottom - ((tick - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom)} y2={height - margin.bottom - ((tick - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom)} className="air-grid" />
            <text x={margin.left - 10} y={height - margin.bottom - ((tick - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom) + 4} textAnchor="end" className="air-tick">
              {tick === 0 ? "0" : `10^${tick}`}
            </text>
          </g>
        ))}
        <line x1={x(5)} x2={x(5)} y1={margin.top} y2={height - margin.bottom} className="air-guide" />
        {plotted.map((row) => {
          const isZero = row.pm25_locations === 0;
          const isFocus = row.iso3 === focusIso;
          const radius = clamp(Math.sqrt(row.population) / 2200, 3.5, 16);
          return (
            <g key={row.iso3}>
              <circle
                cx={x(row.pm25_exposure_ugm3)}
                cy={y(row.pm25_locations)}
                r={isFocus ? radius + 3 : radius}
                className={isZero ? "air-exposure-point air-zero-point" : "air-exposure-point"}
              />
              {(isFocus || row.iso3 === "PNG" || row.iso3 === "TLS") && (
                <text
                  x={x(row.pm25_exposure_ugm3) + (row.iso3 === "TLS" ? 28 : 8)}
                  y={y(row.pm25_locations) + (row.iso3 === "TLS" ? 16 : -8)}
                  className="air-point-label"
                >
                  {row.iso3}
                </text>
              )}
            </g>
          );
        })}
        <text x={width / 2} y={height - 6} textAnchor="middle" className="air-axis-label">
          WDI PM2.5 exposure, micrograms per cubic meter
        </text>
        <text transform={`translate(18 ${height / 2}) rotate(-90)`} textAnchor="middle" className="air-axis-label">
          public PM2.5 monitor locations in OpenAQ (log count)
        </text>
      </svg>
    </div>
  );
}

function ZeroMonitorPanel({ row, deepening }: { row: ZeroMonitorRow | undefined; deepening: DeepeningData | null }) {
  if (!deepening || !row) return <p className="showcase-loading">Choose a zero-monitor economy.</p>;
  return (
    <>
      <p className="kicker kicker-blue">Selected zero-monitor economy</p>
      <h3>{row.country}</h3>
      <dl className="air-readout">
        <div>
          <dt>Population in zero-monitor group</dt>
          <dd>{formatNumber(row.population)}</dd>
        </div>
        <div>
          <dt>Share of zero-monitor population</dt>
          <dd>{pct(row.share_of_zero_monitor_pop)}</dd>
        </div>
        <div>
          <dt>PM2.5 exposure</dt>
          <dd>{row.pm25_exposure_ugm3.toFixed(1)} µg/m3</dd>
        </div>
        <div>
          <dt>Source snapshot</dt>
          <dd>{deepening.source.snapshot}</dd>
        </div>
      </dl>
      <p>
        The regional total is {formatNumber(deepening.part_a_concentration.zero_monitor_population_total)} people,
        but the first two rows account for {pct(deepening.part_a_concentration.png_plus_timor_share)} of it.
      </p>
    </>
  );
}

function ResidualPanel({ row, deepening }: { row: ResidualRow | undefined; deepening: DeepeningData | null }) {
  if (!deepening || !row) return <p className="showcase-loading">Choose a residual row.</p>;
  return (
    <>
      <p className="kicker kicker-blue">GDP-adjusted monitor-density residual</p>
      <h3>{row.country}</h3>
      <dl className="air-readout">
        <div>
          <dt>Residual</dt>
          <dd>{signed(row.log10_people_per_monitor_residual)}</dd>
        </div>
        <div>
          <dt>People per monitor</dt>
          <dd>{formatNumber(row.people_per_monitor)}</dd>
        </div>
        <div>
          <dt>GDP per capita</dt>
          <dd>${formatNumber(row.gdp_pc_current_usd, 0)} ({row.gdp_pc_year})</dd>
        </div>
        <div>
          <dt>PM2.5 exposure</dt>
          <dd>{row.pm25_exposure_ugm3.toFixed(1)} µg/m3</dd>
        </div>
      </dl>
      <p>
        Positive residuals mean the economy has more people per visible public
        PM2.5 monitor than the simple GDP-per-capita relationship predicts.
      </p>
    </>
  );
}

function ExposurePanel({ row, panel }: { row: AirPanelRow | undefined; panel: AirPanelData | null }) {
  if (!panel || !row) return <p className="showcase-loading">Choose an economy.</p>;
  return (
    <>
      <p className="kicker kicker-blue">Original observability panel</p>
      <h3>{row.country}</h3>
      <dl className="air-readout">
        <div>
          <dt>PM2.5 locations in OpenAQ</dt>
          <dd>{formatNumber(row.pm25_locations)}</dd>
        </div>
        <div>
          <dt>PM2.5 exposure</dt>
          <dd>{row.pm25_exposure_ugm3.toFixed(1)} µg/m3</dd>
        </div>
        <div>
          <dt>Gap score</dt>
          <dd>{formatNumber(row.pm25_observability_gap_score)}</dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>{row.pm25_observability_status.replaceAll("_", " ")}</dd>
        </div>
      </dl>
      <p>
        The score is a triage composite. It helps decide where to audit public
        monitor visibility; it is not an official assessment of air quality or
        monitoring performance.
      </p>
    </>
  );
}
