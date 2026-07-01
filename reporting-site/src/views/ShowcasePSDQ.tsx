"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
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

interface PsdqCoordinateRepairGroupCount {
  sample_group: string;
  rows: number;
  missing_registry_coordinate_requires_source_retrieval: number;
  coordinate_reused_by_multiple_sampled_rows: number;
  coordinate_in_other_public_upazila_near_osm_health_feature: number;
  coordinate_in_other_public_upazila_no_near_osm_health_feature: number;
  coordinate_outside_public_adm3_boundary: number;
}

interface PsdqCoordinateRepairDistanceRow {
  review_id: string;
  facility_name: string;
  expected_upazila: string;
  observed_public_adm3_names: string;
  distance_to_expected_upazila_km: number;
  coordinate_repair_code: string;
  nearest_osm_health_distance_m: number;
}

interface PsdqCoordinateRepairSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  repair_scope: {
    coordinate_repair_rows_checked: number;
    missing_registry_coordinate_rows: number;
    valid_coordinate_rows: number;
    valid_coordinates_outside_expected_upazila: number;
    rows_inside_other_public_adm3: number;
    rows_outside_public_adm3_boundary: number;
    rows_with_nearest_osm_health_feature_within_500m: number;
    rows_with_duplicate_sample_coordinate: number;
    rows_at_least_50km_from_expected_upazila: number;
    max_distance_to_expected_upazila_km: number | null;
    median_distance_to_expected_upazila_km: number | null;
    rows_closed_as_coordinate_repaired: number;
    rows_retained_open: number;
  };
  coordinate_repair_code_counts: PsdqCandidateResolutionCount[];
  coordinate_repair_counts_by_group: PsdqCoordinateRepairGroupCount[];
  evidence_strength_counts: PsdqCandidateResolutionCount[];
  distance_chart_rows: PsdqCoordinateRepairDistanceRow[];
  non_claim: string;
}

interface PsdqPublicMapGapGroupCount {
  sample_group: string;
  rows: number;
  valid_coordinate_reused_within_sample_public_map_gap: number;
  same_upazila_specific_name_signal_far_from_registry_coordinate: number;
  same_upazila_specific_name_signal_outside_500m: number;
  threshold_sensitive_same_upazila_osm_500_1000m: number;
  zero_osm_in_expected_public_upazila: number;
  same_upazila_osm_present_but_not_at_facility: number;
  no_nearby_same_upazila_osm_health_signal_within_3km: number;
}

interface PsdqPublicMapGapUpazilaRow {
  join_key: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  public_map_gap_rows: number;
  active_clinical_facilities: number;
  osm_health: number;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  underobserved_buildings_3km_p85_proxy: number;
  coordinate_repair_rows_same_upazila: number;
  valid_coordinate_reused_within_sample_public_map_gap: number;
  same_upazila_specific_name_signal_far_from_registry_coordinate: number;
  same_upazila_specific_name_signal_outside_500m: number;
  threshold_sensitive_same_upazila_osm_500_1000m: number;
  zero_osm_in_expected_public_upazila: number;
  same_upazila_osm_present_but_not_at_facility: number;
  no_nearby_same_upazila_osm_health_signal_within_3km: number;
}

interface PsdqPublicMapGapSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  public_map_gap_scope: {
    public_map_gap_rows_checked: number;
    priority_1_high_exposure_rows: number;
    priority_3_spot_check_rows: number;
    rows_with_valid_coordinate: number;
    rows_inside_expected_upazila: number;
    rows_with_duplicate_sample_coordinate: number;
    rows_in_upazilas_with_coordinate_repair_flags: number;
    rows_in_zero_osm_expected_upazilas: number;
    rows_with_same_upazila_osm_health_features: number;
    rows_with_same_upazila_specific_name_signal_outside_500m: number;
    rows_with_same_upazila_specific_name_signal_far_from_registry_coordinate: number;
    rows_threshold_sensitive_500m_to_1km: number;
    rows_with_nearest_any_osm_health_within_1km: number;
    rows_with_nearest_any_osm_health_beyond_3km: number;
    rows_with_nearest_same_upazila_osm_health_beyond_3km: number;
    rows_closed_as_resolved: number;
    rows_retained_open: number;
  };
  public_map_gap_code_counts: PsdqCandidateResolutionCount[];
  public_map_gap_counts_by_group: PsdqPublicMapGapGroupCount[];
  evidence_strength_counts: PsdqCandidateResolutionCount[];
  upazila_queue_rows: PsdqPublicMapGapUpazilaRow[];
  non_claim: string;
}

interface PsdqPublicMapGapEvidenceUpazilaRow {
  join_key: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  row_evidence_rows: number;
  priority_1_rows: number;
  active_clinical_facilities: number;
  osm_health: number;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  underobserved_buildings_3km_p85_proxy: number;
  source_repair_before_row_absence: number;
  possible_match_or_buffer_review: number;
  row_level_public_map_absence_review: number;
  upazila_level_public_map_observability_review: number;
}

interface PsdqPublicMapGapEvidenceCardRow {
  row_evidence_id: string;
  evidence_rank: number;
  facility_name: string;
  upazila_name: string;
  district_name: string;
  priority_scope: string;
  public_map_gap_lane_label: string;
  row_evidence_tier: string;
  row_evidence_decision: string;
  row_evidence_reader_status: string;
  dghs_public_profile_url: string;
  registry_coordinate_osm_inspection_url: string;
  nearest_same_upazila_osm_health_url: string;
  best_same_upazila_name_osm_url: string;
  active_clinical_facilities: string;
  osm_health: string;
  underobserved_buildings_3km_p85_proxy: string;
  row_evidence_note: string;
}

interface PsdqPublicMapGapEvidenceSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  row_evidence_scope: {
    rows_with_row_evidence: number;
    priority_1_high_exposure_rows: number;
    priority_3_spot_check_rows: number;
    rows_with_dghs_public_profile_url: number;
    rows_with_registry_coordinate_osm_inspection_url: number;
    rows_with_same_upazila_osm_feature_url: number;
    rows_with_best_name_osm_feature_url: number;
    rows_kept_open: number;
    rows_closed_as_resolved: number;
  };
  row_evidence_tier_counts: PsdqCandidateResolutionCount[];
  row_evidence_decision_counts: PsdqCandidateResolutionCount[];
  public_map_gap_lane_counts: PsdqCandidateResolutionCount[];
  upazila_evidence_rows: PsdqPublicMapGapEvidenceUpazilaRow[];
  row_card_rows: PsdqPublicMapGapEvidenceCardRow[];
  non_claim: string;
}

interface PsdqPublicMapInspectionUpazilaRow {
  join_key: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  inspection_rows: number;
  priority_1_rows: number;
  source_repair_first: number;
  possible_public_map_match_or_buffer_case: number;
  facility_specific_public_map_absence_candidate: number;
  upazila_public_map_observability_gap: number;
  start_here_rows: number;
  active_clinical_facilities: number;
  osm_health: number;
  underobserved_buildings_3km_p85_proxy: number;
}

interface PsdqPublicMapInspectionCardRow {
  inspection_id: string;
  inspection_rank: number;
  focus_class: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  priority_scope: string;
  inspection_lane: string;
  inspection_decision: string;
  closure_eligibility: string;
  public_cache_finding: string;
  evidence_needed_to_close_or_reclassify: string;
  dghs_public_profile_url: string;
  registry_coordinate_osm_inspection_url: string;
  candidate_feature_1_url: string;
  candidate_feature_1_name: string;
  candidate_feature_1_distance_m: number;
  candidate_feature_1_name_score: number;
  candidate_feature_1_tags_compact: string;
}

interface PsdqPublicMapInspectionSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  unit: string;
  inspection_scope: {
    rows_inspected: number;
    priority_1_rows_inspected: number;
    start_here_named_upazila_rows: number;
    start_here_zero_osm_upazila_rows: number;
    rows_with_candidate_public_map_feature: number;
    rows_with_same_upazila_candidate_public_map_feature: number;
    rows_with_specific_name_signal_in_candidate_features: number;
    rows_kept_open: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  inspection_lane_counts: PsdqCandidateResolutionCount[];
  focus_class_counts: PsdqCandidateResolutionCount[];
  closure_eligibility_counts: PsdqCandidateResolutionCount[];
  reclassification_candidate_counts: PsdqCandidateResolutionCount[];
  upazila_inspection_rows: PsdqPublicMapInspectionUpazilaRow[];
  row_card_rows: PsdqPublicMapInspectionCardRow[];
  inspection_notes: string[];
  non_claim: string;
}

interface PsdqPublicSourceConfirmationCardRow {
  confirmation_id: string;
  confirmation_rank: number;
  inspection_id: string;
  facility_name: string;
  district_name: string;
  upazila_name: string;
  inspection_lane: string;
  public_source_confirmation_lane: string;
  dghs_profile_retrieved: boolean;
  dghs_profile_facility_token_coverage: number;
  candidate_osm_api_retrieved: boolean;
  candidate_osm_name_from_api: string;
  candidate_name_score_from_live_tags: number;
  candidate_distance_m_from_inspection: number;
  dghs_public_profile_url: string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
  evidence_needed_next: string;
}

interface PsdqPublicSourceConfirmationSummary {
  generated_at: string;
  retrieved_at: string;
  status: string;
  goal_level: string;
  confirmation_scope: {
    rows_checked: number;
    dghs_profiles_retrieved: number;
    osm_candidate_api_records_retrieved: number;
    rows_with_dghs_profile_token_support: number;
    rows_with_candidate_name_score_at_least_0_75: number;
    rows_kept_open: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  public_source_confirmation_lane_counts: PsdqCandidateResolutionCount[];
  inspection_lane_counts: PsdqCandidateResolutionCount[];
  focus_class_counts: PsdqCandidateResolutionCount[];
  row_card_rows: PsdqPublicSourceConfirmationCardRow[];
  confirmation_notes: string[];
  non_claim: string;
}

interface PsdqTargetedSourceConfirmationUpazilaRow {
  district_name: string;
  upazila_name: string;
  rows: number;
  priority_1_rows: number;
  dghs_profiles_retrieved: number;
  osm_candidate_api_records_retrieved: number;
  rows_with_candidate_name_score_at_least_0_75: number;
  dominant_confirmation_lane: string;
  source_repair_rows: number;
  possible_same_facility_rows: number;
  name_conflict_rows: number;
  zero_osm_context_rows: number;
}

interface PsdqTargetedSourceConfirmationSummary {
  generated_at: string;
  retrieved_at: string;
  status: string;
  goal_level: string;
  confirmation_scope: {
    rows_checked: number;
    priority_1_rows_checked: number;
    dghs_profiles_retrieved: number;
    osm_candidate_api_records_retrieved: number;
    rows_with_dghs_profile_token_support: number;
    rows_with_candidate_name_score_at_least_0_75: number;
    rows_kept_open: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  public_source_confirmation_lane_counts: PsdqCandidateResolutionCount[];
  inspection_lane_counts: PsdqCandidateResolutionCount[];
  focus_class_counts: PsdqCandidateResolutionCount[];
  priority_scope_counts: PsdqCandidateResolutionCount[];
  upazila_confirmation_rows: PsdqTargetedSourceConfirmationUpazilaRow[];
  row_card_rows: PsdqPublicSourceConfirmationCardRow[];
  confirmation_notes: string[];
  non_claim: string;
}

interface PsdqPublicSourceDecisionLedgerRow {
  decision_id: string;
  decision_rank: number;
  confirmation_id: string;
  inspection_id: string;
  facility_name: string;
  district_name: string;
  upazila_name: string;
  priority_scope: string;
  public_source_confirmation_lane: string;
  decision_track: string;
  decision_track_label: string;
  decision_action: string;
  decision_question: string;
  closure_or_reclassification_gate: string;
  candidate_osm_name_from_api: string;
  candidate_name_score_from_live_tags: number | string;
  candidate_distance_m_from_inspection: number | string;
  dghs_public_profile_url: string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
}

interface PsdqPublicSourceDecisionLedgerUpazilaRow {
  district_name: string;
  upazila_name: string;
  decision_rows: number;
  priority_1_rows: number;
  source_repair_first_rows: number;
  possible_same_facility_rows: number;
  high_exposure_name_conflict_rows: number;
  max_candidate_name_score: number;
  nearest_candidate_distance_m: number;
}

interface PsdqPublicSourceDecisionLedgerSummary {
  generated_at: string;
  source_retrieved_at: string;
  status: string;
  goal_level: string;
  selection_rule: string;
  decision_scope: {
    targeted_confirmation_rows: number;
    decision_ledger_rows: number;
    source_repair_rows: number;
    possible_same_facility_rows: number;
    high_exposure_name_conflict_rows: number;
    deferred_zero_osm_context_rows: number;
    deferred_lower_priority_name_conflict_rows: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  decision_track_counts: Array<{ name: string; label: string; rows: number }>;
  priority_scope_counts: PsdqCandidateResolutionCount[];
  confirmation_lane_counts_in_ledger: PsdqCandidateResolutionCount[];
  deferred_scope_counts: PsdqCandidateResolutionCount[];
  upazila_decision_rows: PsdqPublicSourceDecisionLedgerUpazilaRow[];
  decision_rows: PsdqPublicSourceDecisionLedgerRow[];
  decision_notes: string[];
  non_claim: string;
}

interface PsdqPossibleSameFacilityReviewRow {
  possible_same_facility_review_id: string;
  evidence_rank: number;
  evidence_method: string;
  status: string;
  decision_id: string;
  confirmation_id: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  priority_scope: string;
  focus_class: string;
  inspection_lane: string;
  public_source_confirmation_lane: string;
  dghs_profile_id: string;
  dghs_public_profile_url: string;
  dghs_profile_http_status: number | string;
  dghs_profile_retrieved: boolean | string;
  dghs_profile_facility_token_coverage: number | string;
  dghs_profile_public_name_token_coverage: number | string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
  candidate_osm_api_http_status: number | string;
  candidate_osm_api_retrieved: boolean | string;
  candidate_osm_type: string;
  candidate_osm_id: string;
  candidate_osm_name_from_api: string;
  candidate_osm_lat: number | string;
  candidate_osm_lon: number | string;
  candidate_osm_tags_compact: string;
  candidate_name_score_from_live_tags: number | string;
  candidate_distance_m_from_inspection: number | string;
  candidate_distance_band: string;
  name_evidence_class: string;
  decision_question: string;
  closure_or_reclassification_gate: string;
  minimum_evidence_to_close: string;
  minimum_evidence_to_reclassify_as_same_facility: string;
  minimum_evidence_to_keep_as_map_absence: string;
  review_action: string;
  row_closure_allowed_by_current_public_evidence: boolean | string;
  same_facility_reclassification_allowed_by_current_public_evidence: boolean | string;
  map_absence_language_allowed_by_current_public_evidence: boolean | string;
  external_contact_made: boolean | string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
  source_basis: string;
  non_claim: string;
}

interface PsdqPossibleSameFacilityReviewSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  possible_same_facility_scope: {
    decision_ledger_rows: number;
    possible_same_facility_rows: number;
    dghs_profiles_retrieved: number;
    osm_api_records_retrieved: number;
    rows_with_name_score_at_least_0_95: number;
    rows_with_candidate_distance_2km_or_more: number;
    min_candidate_distance_m: number | null;
    max_candidate_distance_m: number | null;
    min_candidate_name_score: number | null;
    max_candidate_name_score: number | null;
    external_contacts_made: number;
    rows_allowed_for_closure: number;
    rows_allowed_for_same_facility_reclassification: number;
    rows_allowed_for_map_absence_language: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  candidate_distance_band_counts: PsdqCandidateResolutionCount[];
  name_evidence_class_counts: PsdqCandidateResolutionCount[];
  review_rows: PsdqPossibleSameFacilityReviewRow[];
  review_notes: string[];
  non_claim: string;
}

interface PsdqPriorityNameConflictReviewRow {
  priority_name_conflict_review_id: string;
  evidence_rank: number;
  evidence_method: string;
  status: string;
  decision_id: string;
  confirmation_id: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  priority_scope: string;
  focus_class: string;
  inspection_lane: string;
  public_source_confirmation_lane: string;
  dghs_profile_id: string;
  dghs_public_profile_url: string;
  dghs_profile_http_status: number | string;
  dghs_profile_retrieved: boolean | string;
  dghs_profile_facility_token_coverage: number | string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
  candidate_osm_api_http_status: number | string;
  candidate_osm_api_retrieved: boolean | string;
  candidate_osm_type: string;
  candidate_osm_id: string;
  candidate_osm_name_from_api: string;
  candidate_osm_lat: number | string;
  candidate_osm_lon: number | string;
  candidate_osm_tags_compact: string;
  candidate_name_score_from_live_tags: number | string;
  candidate_distance_m_from_inspection: number | string;
  name_conflict_score_class: string;
  candidate_distance_band: string;
  candidate_contains_admin_place_name: boolean | string;
  name_conflict_review_class: string;
  decision_question: string;
  closure_or_reclassification_gate: string;
  public_alias_or_location_source_found_by_current_artifacts: boolean | string;
  minimum_evidence_to_close: string;
  minimum_evidence_to_reclassify_as_same_facility: string;
  minimum_evidence_to_keep_as_name_conflict: string;
  review_action: string;
  row_closure_allowed_by_current_public_evidence: boolean | string;
  same_facility_reclassification_allowed_by_current_public_evidence: boolean | string;
  map_absence_language_allowed_by_current_public_evidence: boolean | string;
  external_contact_made: boolean | string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
  source_basis: string;
  non_claim: string;
}

interface PsdqPriorityNameConflictReviewSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  priority_name_conflict_scope: {
    decision_ledger_rows: number;
    priority_name_conflict_rows: number;
    dghs_profiles_retrieved: number;
    osm_api_records_retrieved: number;
    rows_with_candidate_name_score_at_least_0_70: number;
    rows_with_candidate_distance_5km_or_more: number;
    rows_with_candidate_distance_10km_or_more: number;
    rows_where_candidate_contains_admin_place_name: number;
    public_alias_or_location_sources_found_by_current_artifacts: number;
    min_candidate_distance_m: number | null;
    max_candidate_distance_m: number | null;
    min_candidate_name_score: number | null;
    max_candidate_name_score: number | null;
    external_contacts_made: number;
    rows_allowed_for_closure: number;
    rows_allowed_for_same_facility_reclassification: number;
    rows_allowed_for_map_absence_language: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  name_conflict_review_class_counts: PsdqCandidateResolutionCount[];
  name_conflict_score_class_counts: PsdqCandidateResolutionCount[];
  candidate_distance_band_counts: PsdqCandidateResolutionCount[];
  review_rows: PsdqPriorityNameConflictReviewRow[];
  review_notes: string[];
  non_claim: string;
}

interface PsdqLowerPriorityNameConflictReviewRow {
  lower_priority_name_conflict_review_id: string;
  evidence_rank: number;
  evidence_method: string;
  status: string;
  confirmation_id: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  priority_scope: string;
  focus_class: string;
  inspection_lane: string;
  public_source_confirmation_lane: string;
  dghs_profile_id: string;
  dghs_public_profile_url: string;
  dghs_profile_http_status: number | string;
  dghs_profile_retrieved: boolean | string;
  dghs_profile_facility_token_coverage: number | string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
  candidate_osm_api_http_status: number | string;
  candidate_osm_api_retrieved: boolean | string;
  candidate_osm_type: string;
  candidate_osm_id: string;
  candidate_osm_name_from_api: string;
  candidate_osm_lat: number | string;
  candidate_osm_lon: number | string;
  candidate_osm_tags_compact: string;
  candidate_name_score_from_live_tags: number | string;
  candidate_distance_m_from_inspection: number | string;
  name_conflict_score_class: string;
  candidate_distance_band: string;
  candidate_contains_admin_place_name: boolean | string;
  candidate_reused_in_spot_check: boolean | string;
  candidate_spot_check_cluster_rows: number | string;
  spot_check_review_class: string;
  public_alias_or_location_source_found_by_current_artifacts: boolean | string;
  minimum_evidence_to_close: string;
  minimum_evidence_to_reclassify_as_same_facility: string;
  minimum_evidence_to_keep_as_name_conflict: string;
  review_action: string;
  row_closure_allowed_by_current_public_evidence: boolean | string;
  same_facility_reclassification_allowed_by_current_public_evidence: boolean | string;
  map_absence_language_allowed_by_current_public_evidence: boolean | string;
  external_contact_made: boolean | string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
  source_basis: string;
  non_claim: string;
}

interface PsdqLowerPriorityNameConflictCluster {
  candidate_cluster_id: string;
  candidate_osm_name_from_api: string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
  candidate_osm_tags_compact: string;
  spot_check_rows: number;
  districts: string;
  upazilas: string;
  facility_names: string;
  min_candidate_distance_m: number;
  max_candidate_distance_m: number;
  min_candidate_name_score: number;
  max_candidate_name_score: number;
  repeated_candidate_in_spot_check: boolean;
}

interface PsdqLowerPriorityNameConflictUpazilaRow {
  district_name: string;
  upazila_name: string;
  spot_check_rows: number;
  candidate_names: string;
  min_candidate_distance_m: number;
  max_candidate_distance_m: number;
  max_candidate_name_score: number;
}

interface PsdqLowerPriorityNameConflictReviewSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  lower_priority_name_conflict_scope: {
    targeted_confirmation_rows: number;
    decision_ledger_deferred_lower_priority_name_conflict_rows: number;
    lower_priority_name_conflict_rows: number;
    dghs_profiles_retrieved: number;
    osm_api_records_retrieved: number;
    unique_candidate_features: number;
    candidate_features_reused_by_multiple_rows: number;
    rows_sharing_reused_candidate_features: number;
    spot_check_districts: number;
    spot_check_upazilas: number;
    rows_with_candidate_name_score_at_least_0_50: number;
    rows_with_candidate_name_score_at_least_0_70: number;
    rows_with_candidate_distance_5km_or_more: number;
    rows_with_candidate_distance_10km_or_more: number;
    rows_where_candidate_contains_admin_place_name: number;
    public_alias_or_location_sources_found_by_current_artifacts: number;
    min_candidate_distance_m: number | null;
    max_candidate_distance_m: number | null;
    min_candidate_name_score: number | null;
    max_candidate_name_score: number | null;
    external_contacts_made: number;
    rows_allowed_for_closure: number;
    rows_allowed_for_same_facility_reclassification: number;
    rows_allowed_for_map_absence_language: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  spot_check_review_class_counts: PsdqCandidateResolutionCount[];
  name_conflict_score_class_counts: PsdqCandidateResolutionCount[];
  candidate_distance_band_counts: PsdqCandidateResolutionCount[];
  candidate_clusters: PsdqLowerPriorityNameConflictCluster[];
  upazila_rows: PsdqLowerPriorityNameConflictUpazilaRow[];
  review_rows: PsdqLowerPriorityNameConflictReviewRow[];
  review_notes: string[];
  non_claim: string;
}

interface PsdqZeroOsmObservabilityReviewRow {
  zero_osm_observability_review_id: string;
  evidence_rank: number;
  evidence_method: string;
  status: string;
  join_key: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  registry_records: number | string;
  active_clinical_facilities: number | string;
  coordinate_facilities: number | string;
  osm_health: number | string;
  registry_minus_osm_clinical: number | string;
  registry_gap_share: number | string;
  buildings_nearest_3km_p85: number | string;
  underobserved_buildings_3km_p85_proxy: number | string;
  has_open_buildings_denominator: boolean | string;
  has_osm_boundary_match: boolean | string;
  coordinate_share_of_active_clinical: number | string;
  zero_osm_observability_class: string;
  targeted_inspection_rows_in_current_queue: number | string;
  targeted_inspection_ids: string;
  targeted_inspection_facilities: string;
  nearest_public_map_context_name_from_inspection: string;
  nearest_public_map_context_distance_m_from_inspection: number | string;
  nearest_public_map_context_url_from_inspection: string;
  upazila_observability_language_allowed: boolean | string;
  facility_row_closure_allowed_by_current_public_evidence: boolean | string;
  facility_row_absence_language_allowed_by_current_public_evidence: boolean | string;
  coordinate_correction_allowed_by_current_public_evidence: boolean | string;
  minimum_evidence_to_close_facility_row: string;
  minimum_evidence_to_upgrade_upazila_context: string;
  review_action: string;
  source_basis: string;
  non_claim: string;
}

interface PsdqZeroOsmDivisionRow {
  division_name: string;
  zero_osm_upazilas: number;
  active_clinical_facilities: number;
  underobserved_buildings_3km_p85_proxy: number;
  targeted_inspection_rows: number;
}

interface PsdqZeroOsmTargetedInspectionRow {
  inspection_id: string;
  inspection_rank: number;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  join_key: string;
  active_clinical_facilities: number;
  osm_health: number;
  underobserved_buildings_3km_p85_proxy: number;
  nearest_national_feature_1_name: string;
  nearest_national_feature_1_distance_m: number | string;
  nearest_national_feature_1_url: string;
  inspection_decision: string;
  closure_eligibility: string;
  reclassification_candidate: string;
  public_cache_finding: string;
  evidence_needed_to_close_or_reclassify: string;
}

interface PsdqZeroOsmObservabilityReviewSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  zero_osm_observability_scope: {
    exposure_rows_read: number;
    zero_osm_active_registry_upazilas: number;
    active_clinical_facilities_in_zero_osm_upazilas: number;
    share_of_exposure_rows_zero_osm: number | null;
    share_of_active_clinical_facilities_zero_osm: number | null;
    zero_osm_upazilas_with_open_buildings_denominator: number;
    zero_osm_upazilas_with_osm_boundary_match: number;
    buildings_nearest_3km_p85_in_zero_osm_upazilas: number;
    underobserved_buildings_3km_p85_proxy_in_zero_osm_upazilas: number;
    targeted_inspection_rows_in_zero_osm_lane: number;
    targeted_zero_osm_upazilas: number;
    decision_ledger_deferred_zero_osm_context_rows: number;
    upazila_observability_language_allowed_rows: number;
    facility_rows_allowed_for_closure: number;
    facility_rows_allowed_for_absence_language: number;
    coordinate_corrections_allowed: number;
    external_contacts_made: number;
    rows_closed_as_resolved: number;
    rows_reclassified_or_corrected: number;
  };
  zero_osm_observability_class_counts: PsdqCandidateResolutionCount[];
  division_rows: PsdqZeroOsmDivisionRow[];
  top_zero_osm_upazila_rows: PsdqZeroOsmObservabilityReviewRow[];
  targeted_inspection_rows: PsdqZeroOsmTargetedInspectionRow[];
  review_notes: string[];
  non_claim: string;
}

interface PsdqHumanGatedHandoffGroup {
  name: string;
  label: string;
  rows: number;
}

interface PsdqHumanGatedHandoffUpazilaRow {
  district_name: string;
  upazila_name: string;
  handoff_rows: number;
  handoff_groups: string;
  source_repair_rows: number;
  possible_same_facility_rows: number;
  priority_name_conflict_rows: number;
  lower_priority_name_conflict_rows: number;
  zero_osm_absence_gate_rows: number;
}

interface PsdqHumanGatedHandoffRow {
  handoff_id: string;
  evidence_rank: number;
  status: string;
  handoff_group: string;
  handoff_group_label: string;
  source_artifact_id: string;
  source_artifact: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  candidate_name: string;
  candidate_feature_url: string;
  candidate_distance_m: number | string;
  candidate_name_score: number | string;
  blocker_label: string;
  required_next_evidence: string;
  public_evidence_basis: string;
  review_question: string;
  row_summary: string;
  human_or_owner_action_required: boolean | string;
  external_contact_made: boolean | string;
  row_closure_allowed_by_current_public_evidence: boolean | string;
  same_facility_reclassification_allowed_by_current_public_evidence: boolean | string;
  map_absence_language_allowed_by_current_public_evidence: boolean | string;
  coordinate_correction_allowed_by_current_public_evidence: boolean | string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_or_corrected: number | string;
  allowed_language_now: string;
  non_claim: string;
}

interface PsdqHumanGatedHandoffSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  handoff_scope: {
    handoff_rows: number;
    handoff_groups: number;
    upazilas_with_handoff_rows: number;
    human_or_owner_action_required_rows: number;
    external_contacts_made: number;
    rows_allowed_for_closure: number;
    rows_allowed_for_same_facility_reclassification: number;
    rows_allowed_for_map_absence_language: number;
    coordinate_corrections_allowed: number;
    rows_closed_as_resolved: number;
    rows_reclassified_or_corrected: number;
    candidate_distance_min_m: number | null;
    candidate_distance_max_m: number | null;
    candidate_name_score_min: number | null;
    candidate_name_score_max: number | null;
  };
  handoff_group_counts: PsdqHumanGatedHandoffGroup[];
  upazila_handoff_rows: PsdqHumanGatedHandoffUpazilaRow[];
  top_handoff_rows: PsdqHumanGatedHandoffRow[];
  review_notes: string[];
  non_claim: string;
}

interface PsdqAiClosureAuditGroup {
  name: string;
  label: string;
  wall_category: string;
  rows: number;
}

interface PsdqAiClosureAuditWall {
  name: string;
  rows: number;
}

interface PsdqAiClosureAuditUpazilaRow {
  district_name: string;
  upazila_name: string;
  audit_rows: number;
  source_repair_rows: number;
  possible_same_facility_rows: number;
  priority_name_conflict_rows: number;
  lower_priority_name_conflict_rows: number;
  zero_osm_absence_gate_rows: number;
  ai_actionable_without_human_or_source_owner_rows: number;
}

interface PsdqAiClosureAuditGate {
  label: string;
  rows: number;
}

interface PsdqAiClosureAuditRow {
  closure_audit_id: string;
  worksheet_id: string;
  handoff_id: string;
  evidence_rank: number;
  status: string;
  handoff_group: string;
  handoff_group_label: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  candidate_name: string;
  candidate_feature_url: string;
  candidate_distance_m: number | string;
  candidate_name_score: number | string;
  primary_reviewer_role: string;
  blocker_label: string;
  minimum_acceptable_evidence: string;
  current_public_evidence_gate: string;
  wall_category: string;
  ai_current_allowed_action: string;
  audit_decision: string;
  audit_rationale: string;
  required_next_evidence: string;
  allowed_language_now: string;
  non_claim: string;
}

interface PsdqAiClosureAuditSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  audit_scope: {
    audit_rows: number;
    handoff_groups: number;
    upazilas_with_audit_rows: number;
    human_or_source_owner_wall_rows: number;
    external_contacts_made: number;
    blank_human_validation_status_rows: number;
    blank_proposed_decision_rows: number;
    blank_source_owner_contact_rows: number;
    blank_public_evidence_reference_rows: number;
    blank_human_location_validation_reference_rows: number;
    ai_closure_possible_rows: number;
    ai_same_facility_reclassification_possible_rows: number;
    ai_map_absence_language_possible_rows: number;
    ai_coordinate_correction_possible_rows: number;
    ai_actionable_without_human_or_source_owner_rows: number;
    keep_open_only_rows: number;
  };
  handoff_group_counts: PsdqAiClosureAuditGroup[];
  wall_category_counts: PsdqAiClosureAuditWall[];
  upazila_audit_rows: PsdqAiClosureAuditUpazilaRow[];
  decision_gate_counts: PsdqAiClosureAuditGate[];
  top_audit_rows: PsdqAiClosureAuditRow[];
  review_notes: string[];
  non_claim: string;
}

interface PsdqEvidenceLadderStage {
  stage_order: number;
  stage_id: string;
  stage_label: string;
  source_summary_path: string;
  unit: string;
  row_count: number;
  supporting_rows: number;
  stage_type: string;
  reader_use: string;
  primary_gate: string;
  keep_open_rows: number;
  closed_rows: number;
  reclassified_rows: number;
  map_absence_rows: number;
  coordinate_correction_rows: number;
  human_or_source_owner_wall_rows: number;
  ai_actionable_rows: number;
  caveat: string;
}

interface PsdqEvidenceLadderSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  ladder_scope: {
    stages: number;
    input_summary_files: number;
    sampled_facility_rows: number;
    targeted_public_source_rows: number;
    human_gated_handoff_rows: number;
    ai_closure_audit_rows: number;
    ai_actionable_without_human_or_source_owner_rows: number;
    keep_open_only_rows: number;
    human_or_source_owner_wall_rows: number;
  };
  stage_rows: PsdqEvidenceLadderStage[];
  terminal_gate: {
    stage_id: string;
    stage_label: string;
    row_count: number;
    ai_actionable_rows: number;
    keep_open_rows: number;
    human_or_source_owner_wall_rows: number;
    primary_gate: string;
  };
  review_notes: string[];
  non_claim: string;
}

interface PsdqSourceRepairEvidenceRow {
  evidence_id: string;
  evidence_rank: number;
  status: string;
  decision_id: string;
  confirmation_id: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  priority_scope: string;
  source_repair_evidence_class: string;
  source_repair_reviewer_action: string;
  source_repair_reviewer_question: string;
  closure_or_reclassification_gate: string;
  public_evidence_attached: boolean | string;
  dghs_public_profile_url: string;
  dghs_profile_http_status: string;
  candidate_feature_url: string;
  candidate_osm_api_url: string;
  candidate_osm_api_http_status: string;
  candidate_osm_name_from_api: string;
  candidate_osm_tags_compact: string;
  candidate_distance_m_from_inspection: number | string;
  candidate_name_score_from_live_tags: number | string;
  shared_public_map_candidate_rows: number | string;
  source_basis: string;
}

interface PsdqSourceRepairEvidenceSummary {
  generated_at: string;
  source_retrieved_at: string;
  status: string;
  goal_level: string;
  selection_rule: string;
  source_repair_scope: {
    decision_ledger_rows: number;
    source_repair_rows: number;
    public_evidence_attached_rows: number;
    dghs_profiles_attached: number;
    osm_api_records_attached: number;
    rows_with_shared_public_map_candidate: number;
    rows_with_candidate_distance_10km_or_more: number;
    rows_with_candidate_distance_50km_or_more: number;
    max_candidate_distance_m: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  source_repair_evidence_class_counts: PsdqCandidateResolutionCount[];
  candidate_feature_groups: Array<{
    candidate_feature_url: string;
    candidate_osm_api_url: string;
    candidate_osm_name_from_api: string;
    source_repair_rows: number;
    districts: string[];
    upazilas: string[];
    facilities: string[];
    max_distance_m: number;
    max_name_score: number;
  }>;
  evidence_rows: PsdqSourceRepairEvidenceRow[];
  evidence_notes: string[];
  non_claim: string;
}

interface PsdqOfficialCoordinateEvidenceRow {
  official_coordinate_evidence_id: string;
  evidence_rank: number;
  status: string;
  source_repair_evidence_id: string;
  decision_id: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  district_name: string;
  upazila_name: string;
  dghs_public_profile_url: string;
  dghs_profile_http_status: number | string;
  dghs_profile_retrieved: boolean | string;
  dghs_profile_map_lat: number | string;
  dghs_profile_map_lon: number | string;
  dghs_profile_map_iframe_url: string;
  dghs_profile_organization_name: string;
  dghs_profile_division_name: string;
  dghs_profile_district_name: string;
  dghs_profile_upazilla_name: string;
  dghs_profile_facility_email: string;
  dghs_profile_matches_inspection_registry_coordinate: boolean | string;
  dghs_profile_to_inspection_registry_distance_m: number | string;
  candidate_feature_url: string;
  candidate_osm_name: string;
  candidate_osm_lat: number | string;
  candidate_osm_lon: number | string;
  candidate_osm_tags_compact: string;
  dghs_profile_to_osm_candidate_distance_m: number | string;
  candidate_distance_m_from_inspection: number | string;
  candidate_name_score_from_live_tags: number | string;
  shared_official_profile_coordinate_rows: number | string;
  official_coordinate_evidence_class: string;
  source_repair_reviewer_action: string;
  explicit_coordinate_source_explanation_found: boolean | string;
  source_explanation_status: string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
}

interface PsdqOfficialCoordinateEvidenceSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  selection_rule: string;
  official_coordinate_scope: {
    source_repair_rows: number;
    dghs_profiles_retrieved: number;
    official_profile_coordinates_exposed: number;
    profile_coordinates_match_inspection_registry_coordinates: number;
    rows_with_shared_official_profile_coordinate: number;
    rows_with_official_coordinate_distance_10km_or_more_from_osm_candidate: number;
    rows_with_official_coordinate_distance_50km_or_more_from_osm_candidate: number;
    max_official_coordinate_to_osm_candidate_distance_m: number;
    explicit_coordinate_source_explanations_found: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  official_coordinate_evidence_class_counts: PsdqCandidateResolutionCount[];
  evidence_rows: PsdqOfficialCoordinateEvidenceRow[];
  evidence_notes: string[];
  non_claim: string;
}

interface PsdqPublicExplanationEvidenceRow {
  public_explanation_evidence_id: string;
  evidence_rank: number;
  status: string;
  official_coordinate_evidence_id: string;
  source_repair_evidence_id: string;
  decision_id: string;
  inspection_id: string;
  facility_name: string;
  facility_type_name: string;
  dghs_profile_id: string;
  dghs_organization_code: string;
  dghs_public_profile_url: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  registry_lat: number | string;
  registry_lon: number | string;
  registry_mailing_address: string;
  registry_village_or_street: string;
  registry_house_number: string;
  registry_union_name: string;
  registry_website_url: string;
  registry_updated_at: string;
  profile_last_updated_at: string;
  profile_detail_lat: number | string;
  profile_detail_lon: number | string;
  official_gov_portal_urls_checked: string;
  official_gov_portal_statuses: string;
  official_gov_portal_pages_retrieved: number | string;
  official_gov_portal_coordinate_terms_found: number | string;
  official_gov_portal_correction_terms_found: number | string;
  source_pages_checked: number | string;
  same_name_dghs_registry_records: number | string;
  same_name_cross_district_dghs_registry_records: number | string;
  shared_official_profile_coordinate_rows: number | string;
  nearest_same_name_other_district_code: string;
  nearest_same_name_other_district_name: string;
  nearest_same_name_other_district_division: string;
  nearest_same_name_other_district_district: string;
  nearest_same_name_other_district_upazila: string;
  nearest_same_name_other_district_lat: number | string;
  nearest_same_name_other_district_lon: number | string;
  nearest_same_name_other_district_coordinate_distance_m: number | string;
  nearest_same_name_other_district_profile_url: string;
  explicit_coordinate_source_or_correction_explanation_found: boolean | string;
  public_explanation_evidence_class: string;
  public_explanation_reviewer_action: string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
}

interface PsdqPublicExplanationEvidenceSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  selection_rule: string;
  public_explanation_scope: {
    source_repair_rows: number;
    live_dghs_profile_tabs_checked: number;
    rows_with_profile_detail_coordinates: number;
    official_gov_portal_urls_checked: number;
    official_gov_portal_pages_retrieved: number;
    explicit_coordinate_source_or_correction_explanations_found: number;
    rows_with_shared_official_profile_coordinate: number;
    rows_with_same_name_cross_district_dghs_registry_record: number;
    rows_with_same_name_other_district_coordinate_within_2km: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  public_explanation_evidence_class_counts: PsdqCandidateResolutionCount[];
  evidence_rows: PsdqPublicExplanationEvidenceRow[];
  evidence_notes: string[];
  non_claim: string;
}

interface PsdqCorrectionRecordFollowupRow {
  correction_followup_evidence_id: string;
  evidence_rank: number;
  status: string;
  public_explanation_evidence_id: string;
  official_coordinate_evidence_id: string;
  source_repair_evidence_id: string;
  decision_id: string;
  inspection_id: string;
  facility_name: string;
  dghs_profile_id: string;
  dghs_organization_code: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  shared_official_profile_coordinate_rows: number | string;
  linked_other_district_code: string;
  linked_other_district_name: string;
  linked_other_district_division: string;
  linked_other_district_district: string;
  linked_other_district_upazila: string;
  linked_other_district_coordinate_distance_m: number | string;
  targeted_reason: string;
  official_sources_checked: number | string;
  official_sources_retrieved: number | string;
  official_source_statuses: string;
  dashboard_menu_contains_target_code: boolean | string;
  dashboard_menu_contains_linked_other_district_code: boolean | string;
  public_correction_or_coordinate_source_record_found: boolean | string;
  correction_source_kinds: string;
  correction_followup_evidence_class: string;
  correction_followup_reviewer_action: string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
}

interface PsdqCorrectionRecordFollowupSummary {
  generated_at: string;
  status: string;
  goal_level: string;
  selection_rule: string;
  correction_followup_scope: {
    targeted_rows: number;
    official_sources_checked: number;
    official_sources_retrieved: number;
    public_correction_or_coordinate_source_records_found: number;
    rows_with_dashboard_target_code_confirmation: number;
    rows_with_dashboard_linked_other_district_code_confirmation: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  correction_followup_evidence_class_counts: PsdqCandidateResolutionCount[];
  evidence_rows: PsdqCorrectionRecordFollowupRow[];
  evidence_notes: string[];
  non_claim: string;
}

interface PsdqClarificationPacketRow {
  clarification_packet_id: string;
  evidence_rank: number;
  evidence_method: string;
  status: string;
  correction_followup_evidence_id: string;
  public_explanation_evidence_id: string;
  official_coordinate_evidence_id: string;
  source_repair_evidence_id: string;
  decision_id: string;
  inspection_id: string;
  facility_name: string;
  dghs_profile_id: string;
  dghs_organization_code: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  linked_or_sibling_codes_csv: string;
  linked_other_district_code: string;
  linked_other_district_name: string;
  linked_other_district_division: string;
  linked_other_district_district: string;
  linked_other_district_upazila: string;
  linked_other_district_coordinate_distance_m: number | string;
  clarification_issue_class: string;
  clarification_issue_label: string;
  clarification_question: string;
  human_review_prompt: string;
  public_evidence_basis: string;
  dghs_profile_url: string;
  dghs_dashboard_target_detail_url: string;
  dghs_dashboard_linked_detail_url: string;
  external_contact_made: boolean | string;
  owner_action_required_to_contact_source: boolean | string;
  rows_closed_as_resolved: number | string;
  rows_reclassified_as_same_facility: number | string;
  packet_use_boundary: string;
  non_claim: string;
}

interface PsdqClarificationPacketSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  clarification_scope: {
    targeted_rows: number;
    rows_requiring_source_owner_clarification: number;
    rows_requiring_human_location_validation_if_no_source_owner_response: number;
    public_correction_or_coordinate_source_records_found: number;
    external_contacts_made: number;
    rows_closed_as_resolved: number;
    rows_reclassified_as_same_facility: number;
  };
  clarification_issue_class_counts: PsdqCandidateResolutionCount[];
  packet_rows: PsdqClarificationPacketRow[];
  packet_notes: string[];
  non_claim: string;
}

interface PsdqRegistryVintageReviewRow {
  registry_vintage_review_id: string;
  evidence_rank: number;
  evidence_method: string;
  status: string;
  clarification_packet_id: string;
  correction_followup_evidence_id: string;
  public_explanation_evidence_id: string;
  official_coordinate_evidence_id: string;
  source_repair_evidence_id: string;
  facility_name: string;
  dghs_profile_id: string;
  dghs_organization_code: string;
  division_name: string;
  district_name: string;
  upazila_name: string;
  linked_or_sibling_codes_csv: string;
  linked_other_district_code: string;
  linked_other_district_district: string;
  linked_other_district_upazila: string;
  linked_other_district_coordinate_distance_m: number | string;
  clarification_issue_class: string;
  clarification_issue_label: string;
  profile_last_updated_at: string;
  profile_update_age_days_at_public_explanation_retrieval: number | string;
  registry_updated_at_from_cached_dghs_row: string;
  profile_timestamp_found: boolean | string;
  public_explanation_retrieved_at: string;
  official_sources_checked: number | string;
  official_sources_retrieved: number | string;
  public_correction_or_coordinate_source_record_found: boolean | string;
  external_contact_made: boolean | string;
  row_closure_allowed_by_current_public_evidence: boolean | string;
  same_facility_reclassification_allowed_by_current_public_evidence: boolean | string;
  map_absence_language_allowed_by_current_public_evidence: boolean | string;
  minimum_evidence_to_close: string;
  minimum_evidence_to_reclassify: string;
  map_absence_language_gate: string;
  registry_vintage_review_action: string;
  non_claim: string;
}

interface PsdqRegistryVintageReviewSummary {
  generated_at: string;
  status: string;
  method: string;
  goal_level: string;
  selection_rule: string;
  registry_vintage_scope: {
    targeted_rows: number;
    rows_with_profile_update_timestamp: number;
    rows_with_profile_update_age_14_days_or_less_at_public_explanation_retrieval: number;
    public_correction_or_coordinate_source_records_found: number;
    external_contacts_made: number;
    rows_allowed_for_closure: number;
    rows_allowed_for_same_facility_reclassification: number;
    rows_allowed_for_map_absence_language: number;
    min_profile_update_age_days_at_public_explanation_retrieval: number | null;
    max_profile_update_age_days_at_public_explanation_retrieval: number | null;
  };
  clarification_issue_class_counts: PsdqCandidateResolutionCount[];
  review_rows: PsdqRegistryVintageReviewRow[];
  review_notes: string[];
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
const PSDQ_PRIORITY_1 = "priority_1_high_exposure";

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
  const [coordinateRepairSummary, setCoordinateRepairSummary] = useState<PsdqCoordinateRepairSummary | null>(null);
  const [publicMapGapSummary, setPublicMapGapSummary] = useState<PsdqPublicMapGapSummary | null>(null);
  const [publicMapGapEvidenceSummary, setPublicMapGapEvidenceSummary] =
    useState<PsdqPublicMapGapEvidenceSummary | null>(null);
  const [publicMapInspectionSummary, setPublicMapInspectionSummary] =
    useState<PsdqPublicMapInspectionSummary | null>(null);
  const [publicSourceConfirmationSummary, setPublicSourceConfirmationSummary] =
    useState<PsdqPublicSourceConfirmationSummary | null>(null);
  const [targetedSourceConfirmationSummary, setTargetedSourceConfirmationSummary] =
    useState<PsdqTargetedSourceConfirmationSummary | null>(null);
  const [publicSourceDecisionLedgerSummary, setPublicSourceDecisionLedgerSummary] =
    useState<PsdqPublicSourceDecisionLedgerSummary | null>(null);
  const [possibleSameFacilityReviewSummary, setPossibleSameFacilityReviewSummary] =
    useState<PsdqPossibleSameFacilityReviewSummary | null>(null);
  const [priorityNameConflictReviewSummary, setPriorityNameConflictReviewSummary] =
    useState<PsdqPriorityNameConflictReviewSummary | null>(null);
  const [lowerPriorityNameConflictReviewSummary, setLowerPriorityNameConflictReviewSummary] =
    useState<PsdqLowerPriorityNameConflictReviewSummary | null>(null);
  const [zeroOsmObservabilityReviewSummary, setZeroOsmObservabilityReviewSummary] =
    useState<PsdqZeroOsmObservabilityReviewSummary | null>(null);
  const [humanGatedHandoffSummary, setHumanGatedHandoffSummary] =
    useState<PsdqHumanGatedHandoffSummary | null>(null);
  const [evidenceLadderSummary, setEvidenceLadderSummary] =
    useState<PsdqEvidenceLadderSummary | null>(null);
  const [aiClosureAuditSummary, setAiClosureAuditSummary] =
    useState<PsdqAiClosureAuditSummary | null>(null);
  const [sourceRepairEvidenceSummary, setSourceRepairEvidenceSummary] =
    useState<PsdqSourceRepairEvidenceSummary | null>(null);
  const [officialCoordinateEvidenceSummary, setOfficialCoordinateEvidenceSummary] =
    useState<PsdqOfficialCoordinateEvidenceSummary | null>(null);
  const [publicExplanationEvidenceSummary, setPublicExplanationEvidenceSummary] =
    useState<PsdqPublicExplanationEvidenceSummary | null>(null);
  const [correctionRecordFollowupSummary, setCorrectionRecordFollowupSummary] =
    useState<PsdqCorrectionRecordFollowupSummary | null>(null);
  const [clarificationPacketSummary, setClarificationPacketSummary] =
    useState<PsdqClarificationPacketSummary | null>(null);
  const [registryVintageReviewSummary, setRegistryVintageReviewSummary] =
    useState<PsdqRegistryVintageReviewSummary | null>(null);
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
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair-summary.json").then((r) => {
        if (!r.ok) throw new Error(`coordinate repair HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-summary.json").then((r) => {
        if (!r.ok) throw new Error(`public map gap HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`public map gap evidence HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection-summary.json").then((r) => {
        if (!r.ok) throw new Error(`public map inspection HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json").then((r) => {
        if (!r.ok) throw new Error(`public source confirmation HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json").then((r) => {
        if (!r.ok) throw new Error(`targeted source confirmation HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json").then((r) => {
        if (!r.ok) throw new Error(`public source decision ledger HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-possible-same-facility-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`possible same-facility review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-priority-name-conflict-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`priority name-conflict review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`lower-priority name-conflict review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`zero-OSM upazila observability review HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-human-gated-handoff-summary.json").then((r) => {
        if (!r.ok) throw new Error(`human-gated handoff HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-evidence-ladder-summary.json").then((r) => {
        if (!r.ok) throw new Error(`evidence ladder HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-ai-closure-audit-summary.json").then((r) => {
        if (!r.ok) throw new Error(`AI closure audit HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`source repair public evidence HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`source repair official coordinate evidence HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json").then((r) => {
        if (!r.ok) throw new Error(`source repair public explanation evidence HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json").then((r) => {
        if (!r.ok) throw new Error(`source repair correction-record follow-up HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json").then((r) => {
        if (!r.ok) throw new Error(`source repair clarification packet HTTP ${r.status}`);
        return r.json();
      }),
      fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json").then((r) => {
        if (!r.ok) throw new Error(`source repair registry-vintage review HTTP ${r.status}`);
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
        coordinateRepairPayload,
        publicMapGapPayload,
        publicMapGapEvidencePayload,
        publicMapInspectionPayload,
        publicSourceConfirmationPayload,
        targetedSourceConfirmationPayload,
        publicSourceDecisionLedgerPayload,
        possibleSameFacilityReviewPayload,
        priorityNameConflictReviewPayload,
        lowerPriorityNameConflictReviewPayload,
        zeroOsmObservabilityReviewPayload,
        humanGatedHandoffPayload,
        evidenceLadderPayload,
        aiClosureAuditPayload,
        sourceRepairEvidencePayload,
        officialCoordinateEvidencePayload,
        publicExplanationEvidencePayload,
        correctionRecordFollowupPayload,
        clarificationPacketPayload,
        registryVintageReviewPayload,
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
        setCoordinateRepairSummary(coordinateRepairPayload);
        setPublicMapGapSummary(publicMapGapPayload);
        setPublicMapGapEvidenceSummary(publicMapGapEvidencePayload);
        setPublicMapInspectionSummary(publicMapInspectionPayload);
        setPublicSourceConfirmationSummary(publicSourceConfirmationPayload);
        setTargetedSourceConfirmationSummary(targetedSourceConfirmationPayload);
        setPublicSourceDecisionLedgerSummary(publicSourceDecisionLedgerPayload);
        setPossibleSameFacilityReviewSummary(possibleSameFacilityReviewPayload);
        setPriorityNameConflictReviewSummary(priorityNameConflictReviewPayload);
        setLowerPriorityNameConflictReviewSummary(lowerPriorityNameConflictReviewPayload);
        setZeroOsmObservabilityReviewSummary(zeroOsmObservabilityReviewPayload);
        setHumanGatedHandoffSummary(humanGatedHandoffPayload);
        setEvidenceLadderSummary(evidenceLadderPayload);
        setAiClosureAuditSummary(aiClosureAuditPayload);
        setSourceRepairEvidenceSummary(sourceRepairEvidencePayload);
        setOfficialCoordinateEvidenceSummary(officialCoordinateEvidencePayload);
        setPublicExplanationEvidenceSummary(publicExplanationEvidencePayload);
        setCorrectionRecordFollowupSummary(correctionRecordFollowupPayload);
        setClarificationPacketSummary(clarificationPacketPayload);
        setRegistryVintageReviewSummary(registryVintageReviewPayload);
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
          <p className="kicker kicker-crimson">Public-data evidence note</p>
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
            <span>Evidence package</span>
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

      {evidenceLadderSummary && (
        <PsdqEvidenceLadderPanel summary={evidenceLadderSummary} />
      )}

      {validationSample && <PsdqValidationSamplePanel sample={validationSample} />}

      {codedSummary && <PsdqValidationCodedPanel summary={codedSummary} />}

      {aiReviewSummary && <PsdqAiReviewPanel summary={aiReviewSummary} />}

      {candidateResolutionSummary && <PsdqCandidateResolutionPanel summary={candidateResolutionSummary} />}

      {candidatePublicSourceCheckSummary && (
        <PsdqCandidatePublicSourceCheckPanel summary={candidatePublicSourceCheckSummary} />
      )}

      {coordinateRepairSummary && <PsdqCoordinateRepairPanel summary={coordinateRepairSummary} />}

      {publicMapGapSummary && <PsdqPublicMapGapPanel summary={publicMapGapSummary} />}

      {publicMapGapEvidenceSummary && <PsdqPublicMapGapEvidencePanel summary={publicMapGapEvidenceSummary} />}

      {publicMapInspectionSummary && <PsdqPublicMapInspectionPanel summary={publicMapInspectionSummary} />}

      {publicSourceConfirmationSummary && (
        <PsdqPublicSourceConfirmationPanel summary={publicSourceConfirmationSummary} />
      )}

      {targetedSourceConfirmationSummary && (
        <PsdqTargetedSourceConfirmationPanel summary={targetedSourceConfirmationSummary} />
      )}

      {publicSourceDecisionLedgerSummary && (
        <PsdqPublicSourceDecisionLedgerPanel summary={publicSourceDecisionLedgerSummary} />
      )}

      {possibleSameFacilityReviewSummary && (
        <PsdqPossibleSameFacilityReviewPanel summary={possibleSameFacilityReviewSummary} />
      )}

      {priorityNameConflictReviewSummary && (
        <PsdqPriorityNameConflictReviewPanel summary={priorityNameConflictReviewSummary} />
      )}

      {lowerPriorityNameConflictReviewSummary && (
        <PsdqLowerPriorityNameConflictReviewPanel summary={lowerPriorityNameConflictReviewSummary} />
      )}

      {zeroOsmObservabilityReviewSummary && (
        <PsdqZeroOsmObservabilityReviewPanel summary={zeroOsmObservabilityReviewSummary} />
      )}

      {humanGatedHandoffSummary && (
        <PsdqHumanGatedHandoffPanel summary={humanGatedHandoffSummary} />
      )}

      {aiClosureAuditSummary && (
        <PsdqAiClosureAuditPanel summary={aiClosureAuditSummary} />
      )}

      {sourceRepairEvidenceSummary && (
        <PsdqSourceRepairPublicEvidencePanel summary={sourceRepairEvidenceSummary} />
      )}

      {officialCoordinateEvidenceSummary && (
        <PsdqOfficialCoordinateEvidencePanel summary={officialCoordinateEvidenceSummary} />
      )}

      {publicExplanationEvidenceSummary && (
        <PsdqPublicExplanationEvidencePanel summary={publicExplanationEvidenceSummary} />
      )}

      {correctionRecordFollowupSummary && (
        <PsdqCorrectionRecordFollowupPanel summary={correctionRecordFollowupSummary} />
      )}

      {clarificationPacketSummary && (
        <PsdqClarificationPacketPanel summary={clarificationPacketSummary} />
      )}

      {registryVintageReviewSummary && (
        <PsdqRegistryVintageReviewPanel summary={registryVintageReviewSummary} />
      )}

      {summary && rows.length > 0 && <PsdqExplorer summary={summary} rows={rows} />}

      <section className="showcase-section showcase-two-col">
        <div>
          <p className="kicker">What the first visual suggests</p>
          <h2>The largest planning risk is not only the largest facility gap.</h2>
          <p>
            The source-disagreement evidence view pairs the registry-map disagreement with
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
            Download evidence note
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
          <Link href="/public-service-data-quality?view=evidence">
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
          <Link href="/showcase/access-map-completeness">Access map-completeness audit</Link>
          <Link href="/showcase/remittance-flow-weighting">Remittance flow-weighting module</Link>
          <Link href="/showcase/air-monitoring-observability">Air-monitoring observability</Link>
          <Link href="/factory">Factory rules</Link>
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
            The evidence module does not ask a reader to trust a chart by eye. It
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

function evidenceLadderStageColor(stageType: string) {
  if (stageType.includes("source_disagreement")) return "#005E7C";
  if (stageType.includes("sample")) return "#007DB8";
  if (stageType.includes("automated")) return "#5A8227";
  if (stageType.includes("ai")) return "#8A6A00";
  if (stageType.includes("public")) return "#9B2226";
  if (stageType.includes("human")) return "#002569";
  return "#6c757d";
}

function evidenceLadderStageKind(stageType: string) {
  if (stageType.includes("human")) return "human gate";
  if (stageType.includes("ai")) return "AI gate";
  if (stageType.includes("public")) return "public source";
  if (stageType.includes("automated")) return "automated screen";
  if (stageType.includes("sample")) return "sample design";
  if (stageType.includes("source_disagreement")) return "source context";
  return stageType.replaceAll("_", " ");
}

function PsdqEvidenceLadderPanel({ summary }: { summary: PsdqEvidenceLadderSummary }) {
  const scope = summary.ladder_scope;
  const terminal = summary.terminal_gate;
  const stages = summary.stage_rows.slice().sort((a, b) => a.stage_order - b.stage_order);

  return (
    <section className="showcase-section psdq-evidence-ladder-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Evidence ladder</p>
          <h2>The reader can now see where the AI loop stops.</h2>
          <p>
            The ladder reads committed summaries and turns the PSDQ facility
            review into a stage-by-stage evidence map. It is not a funnel: the
            unit changes from upazila registry rows to sampled facility rows to
            worksheet rows.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Stage summaries read</span>
            <strong>
              {formatNumber(scope.input_summary_files)} files, {formatNumber(scope.stages)} stages
            </strong>
          </div>
          <div>
            <span>Validation sample</span>
            <strong>{formatNumber(scope.sampled_facility_rows)} sampled facility rows</strong>
          </div>
          <div>
            <span>Terminal audit</span>
            <strong>{formatNumber(scope.ai_closure_audit_rows)} worksheet rows audited</strong>
          </div>
          <div>
            <span>AI-actionable now</span>
            <strong>{formatNumber(scope.ai_actionable_without_human_or_source_owner_rows)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-evidence-ladder-summary-grid">
        <article>
          <span>Targeted public-source rows</span>
          <strong>{formatNumber(scope.targeted_public_source_rows)}</strong>
          <p>rows with retrieved public-source context</p>
        </article>
        <article>
          <span>Human-gated handoff</span>
          <strong>{formatNumber(scope.human_gated_handoff_rows)}</strong>
          <p>rows requiring source-owner or human action</p>
        </article>
        <article>
          <span>Keep-open terminal rows</span>
          <strong>{formatNumber(scope.keep_open_only_rows)}</strong>
          <p>only current allowed language</p>
        </article>
        <article>
          <span>Human/source-owner wall</span>
          <strong>{formatNumber(scope.human_or_source_owner_wall_rows)}</strong>
          <p>rows blocked from AI closure or reclassification</p>
        </article>
      </div>

      <div className="psdq-evidence-ladder-rail" aria-label="PSDQ facility-validation evidence ladder">
        {stages.map((stage) => {
          const color = evidenceLadderStageColor(stage.stage_type);
          return (
            <article key={stage.stage_id} style={{ borderColor: color }}>
              <div className="psdq-evidence-ladder-card-head">
                <span>Stage {stage.stage_order}</span>
                <strong>{stage.stage_label}</strong>
                <em>{evidenceLadderStageKind(stage.stage_type)}</em>
              </div>
              <div className="psdq-evidence-ladder-row-count" style={{ color }}>
                <b>{formatNumber(stage.row_count)}</b>
                <span>{stage.unit}</span>
              </div>
              <p>{stage.reader_use}</p>
              <div className="psdq-evidence-ladder-chips">
                <span>support {formatNumber(stage.supporting_rows)}</span>
                <span>keep-open {formatNumber(stage.keep_open_rows)}</span>
                {stage.human_or_source_owner_wall_rows > 0 && (
                  <span>wall {formatNumber(stage.human_or_source_owner_wall_rows)}</span>
                )}
                {stage.ai_actionable_rows > 0 ? (
                  <span>AI-actionable {formatNumber(stage.ai_actionable_rows)}</span>
                ) : (
                  <span>AI-actionable 0</span>
                )}
              </div>
              <div className="psdq-evidence-ladder-gate">
                <span>Gate</span>
                <p>{stage.primary_gate}</p>
              </div>
              <code>{stage.source_summary_path}</code>
            </article>
          );
        })}
      </div>

      <div className="psdq-evidence-ladder-terminal">
        <div>
          <span>{terminal.stage_label}</span>
          <strong>{terminal.primary_gate}</strong>
          <p>
            {formatNumber(terminal.keep_open_rows)} rows remain keep-open only;
            {` ${formatNumber(terminal.ai_actionable_rows)} `}rows are AI-actionable
            without human or source-owner evidence.
          </p>
        </div>
        <div className="psdq-evidence-ladder-terminal-metrics">
          <span>audit rows {formatNumber(terminal.row_count)}</span>
          <span>wall rows {formatNumber(terminal.human_or_source_owner_wall_rows)}</span>
          <span>status {summary.status.replaceAll("_", " ")}</span>
        </div>
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the evidence ladder</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-evidence-ladder.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-evidence-ladder.md" download>
          Download evidence-ladder note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-evidence-ladder-summary.json" download>
          Download evidence-ladder summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-evidence-ladder.csv" download>
          Download evidence-ladder CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
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

const COORDINATE_REPAIR_ORDER = [
  "missing_registry_coordinate_requires_source_retrieval",
  "coordinate_reused_by_multiple_sampled_rows",
  "coordinate_in_other_public_upazila_near_osm_health_feature",
  "coordinate_in_other_public_upazila_no_near_osm_health_feature",
  "coordinate_outside_public_adm3_boundary",
] as const;

const COORDINATE_REPAIR_LABELS: Record<string, string> = {
  missing_registry_coordinate_requires_source_retrieval: "Missing coordinate",
  coordinate_reused_by_multiple_sampled_rows: "Reused coordinate",
  coordinate_in_other_public_upazila_near_osm_health_feature: "Other ADM3 + OSM clue",
  coordinate_in_other_public_upazila_no_near_osm_health_feature: "Other ADM3, no OSM clue",
  coordinate_outside_public_adm3_boundary: "Outside ADM3 boundary",
};

function coordinateRepairColor(code: string) {
  const colors: Record<string, string> = {
    missing_registry_coordinate_requires_source_retrieval: "#4A5568",
    coordinate_reused_by_multiple_sampled_rows: "#002569",
    coordinate_in_other_public_upazila_near_osm_health_feature: "#007DB8",
    coordinate_in_other_public_upazila_no_near_osm_health_feature: "#D97706",
    coordinate_outside_public_adm3_boundary: "#9B2226",
  };
  return colors[code] || "#6c757d";
}

function coordinateRepairCount(summary: PsdqCoordinateRepairSummary, code: string) {
  return summary.coordinate_repair_code_counts.find((item) => item.name === code)?.rows || 0;
}

function PsdqCoordinateRepairPanel({ summary }: { summary: PsdqCoordinateRepairSummary }) {
  const validRows = summary.repair_scope.valid_coordinate_rows;
  const maxDistance = summary.repair_scope.max_distance_to_expected_upazila_km;

  return (
    <section className="showcase-section psdq-coordinate-repair-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Coordinate-source repair</p>
          <h2>The next failure mode is the registry coordinate itself.</h2>
          <p>
            The coordinate triage pass reads the 23 rows already flagged for
            registry-coordinate repair and checks whether each coordinate can
            support map matching. It separates missing coordinates, reused
            coordinates, and coordinates that fall in another public ADM3 before
            the report treats a row as a public-map absence case.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Coordinate-repair rows checked</span>
            <strong>{formatNumber(summary.repair_scope.coordinate_repair_rows_checked)} rows; all remain open</strong>
          </div>
          <div>
            <span>Missing registry coordinates</span>
            <strong>{formatNumber(summary.repair_scope.missing_registry_coordinate_rows)} rows need a public coordinate source</strong>
          </div>
          <div>
            <span>Outside named upazila</span>
            <strong>{formatNumber(validRows)} usable coordinates fall outside the expected public ADM3</strong>
          </div>
          <div>
            <span>Nearby OSM clue</span>
            <strong>
              {formatNumber(summary.repair_scope.rows_with_nearest_osm_health_feature_within_500m)} suspect coordinates sit within 500m of an OSM health point
            </strong>
          </div>
          <div>
            <span>Exact-coordinate reuse</span>
            <strong>{formatNumber(summary.repair_scope.rows_with_duplicate_sample_coordinate)} sampled rows reuse a coordinate</strong>
          </div>
          <div>
            <span>Largest public-boundary mismatch</span>
            <strong>
              {maxDistance === null ? "missing" : `${formatNumber(maxDistance, 1)} km`} from the named sampled upazila
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-coordinate-grid">
        {COORDINATE_REPAIR_ORDER.filter((code) => coordinateRepairCount(summary, code) > 0).map((code) => (
          <div key={code}>
            <span>{COORDINATE_REPAIR_LABELS[code]}</span>
            <strong>{formatNumber(coordinateRepairCount(summary, code))}</strong>
            <em>{coordinateRepairMeaning(code)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqCoordinateRepairDistanceChart rows={summary.distance_chart_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ coordinate-repair lane legend">
        {COORDINATE_REPAIR_ORDER.filter((code) => coordinateRepairCount(summary, code) > 0).map((code) => (
          <span key={code}>
            <i style={{ background: coordinateRepairColor(code) }} /> {COORDINATE_REPAIR_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the coordinate-repair triage</p>
        <code>python public-service-data-quality/scripts/triage-bgd-facility-coordinate-repairs.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-coordinate-repair.md" download>
          Download coordinate-repair note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair-summary.json" download>
          Download coordinate-repair summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-coordinate-repair.csv" download>
          Download coordinate-repair CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function coordinateRepairMeaning(code: string) {
  const meanings: Record<string, string> = {
    missing_registry_coordinate_requires_source_retrieval: "No usable lat/lon for map matching.",
    coordinate_reused_by_multiple_sampled_rows: "The same coordinate appears on multiple sampled facility rows.",
    coordinate_in_other_public_upazila_near_osm_health_feature: "The coordinate falls in another ADM3 and near a public OSM health feature.",
    coordinate_in_other_public_upazila_no_near_osm_health_feature: "The coordinate falls in another ADM3 with no nearby OSM health clue.",
    coordinate_outside_public_adm3_boundary: "The coordinate is outside the public Bangladesh ADM3 polygons used here.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function shortChartLabel(value: string, limit = 32) {
  if (value.length <= limit) return value;
  return `${value.slice(0, limit - 1)}...`;
}

function PsdqCoordinateRepairDistanceChart({ rows }: { rows: PsdqCoordinateRepairDistanceRow[] }) {
  const width = 1040;
  const rowHeight = 34;
  const headerHeight = 72;
  const bottomPadding = 38;
  const height = headerHeight + rows.length * rowHeight + bottomPadding;
  const labelX = 0;
  const axisX = 360;
  const axisWidth = 560;
  const countX = 940;
  const maxDistance = Math.max(1, ...rows.map((row) => Number(row.distance_to_expected_upazila_km || 0)));
  const ticks = [0, 50, 100, 200, Math.ceil(maxDistance / 50) * 50].filter(
    (tick, index, arr) => tick <= Math.ceil(maxDistance / 50) * 50 && arr.indexOf(tick) === index,
  );
  const scale = (value: number) => axisX + (Math.min(value, maxDistance) / maxDistance) * axisWidth;

  return (
    <svg
      className="psdq-coded-chart psdq-coordinate-distance-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Distance from suspect registry coordinates to the named sampled upazila"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Suspect registry coordinates, distance back to named upazila
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: sampled DGHS row with usable but wrong-admin coordinate; source: coordinate-repair summary JSON
      </text>
      <text x={axisX} y={60} className="psdq-chart-head">
        Kilometers from expected public ADM3/upazila
      </text>
      <line x1={axisX} x2={axisX + axisWidth} y1={headerHeight - 8} y2={headerHeight - 8} stroke="#b6c2cc" />
      {ticks.map((tick) => (
        <g key={tick}>
          <line
            x1={scale(tick)}
            x2={scale(tick)}
            y1={headerHeight - 14}
            y2={height - bottomPadding + 4}
            stroke={tick === 0 ? "#8796a5" : "#dde4ea"}
          />
          <text x={scale(tick)} y={height - 10} textAnchor="middle" className="psdq-row-sub">
            {formatNumber(tick)}
          </text>
        </g>
      ))}

      {rows.map((row, index) => {
        const distance = Number(row.distance_to_expected_upazila_km || 0);
        const y = headerHeight + index * rowHeight + 10;
        const x = scale(distance);
        const observed = row.observed_public_adm3_names || "outside public ADM3";
        return (
          <g key={`${row.review_id}-${row.facility_name}`}>
            <text x={labelX} y={y - 2} className="psdq-row-label">
              {shortChartLabel(row.facility_name)}
            </text>
            <text x={labelX} y={y + 14} className="psdq-row-sub">
              {shortChartLabel(`${row.expected_upazila} -> ${observed}`, 42)}
            </text>
            <line x1={axisX} x2={x} y1={y + 2} y2={y + 2} stroke={coordinateRepairColor(row.coordinate_repair_code)} strokeWidth={3} />
            <circle cx={x} cy={y + 2} r={5.5} fill={coordinateRepairColor(row.coordinate_repair_code)}>
              <title>
                {`${row.facility_name}: ${formatNumber(distance, 1)} km from ${row.expected_upazila}; observed ${observed}; nearest OSM health ${formatNumber(Number(row.nearest_osm_health_distance_m || 0), 0)}m`}
              </title>
            </circle>
            <text x={countX} y={y + 6} className="psdq-value" textAnchor="end">
              {formatNumber(distance, 1)} km
            </text>
          </g>
        );
      })}
    </svg>
  );
}

const PUBLIC_MAP_GAP_ORDER = [
  "valid_coordinate_reused_within_sample_public_map_gap",
  "same_upazila_specific_name_signal_far_from_registry_coordinate",
  "same_upazila_specific_name_signal_outside_500m",
  "threshold_sensitive_same_upazila_osm_500_1000m",
  "zero_osm_in_expected_public_upazila",
  "same_upazila_osm_present_but_not_at_facility",
  "no_nearby_same_upazila_osm_health_signal_within_3km",
] as const;

const PUBLIC_MAP_GAP_LABELS: Record<string, string> = {
  valid_coordinate_reused_within_sample_public_map_gap: "Reused valid coordinate",
  same_upazila_specific_name_signal_far_from_registry_coordinate: "Far same-name signal",
  same_upazila_specific_name_signal_outside_500m: "Name signal outside 500m",
  threshold_sensitive_same_upazila_osm_500_1000m: "500m to 1km sensitive",
  zero_osm_in_expected_public_upazila: "Zero OSM in upazila",
  same_upazila_osm_present_but_not_at_facility: "OSM present, not facility",
  no_nearby_same_upazila_osm_health_signal_within_3km: "No same-upazila OSM within 3km",
};

function publicMapGapColor(code: string) {
  const colors: Record<string, string> = {
    valid_coordinate_reused_within_sample_public_map_gap: "#002569",
    same_upazila_specific_name_signal_far_from_registry_coordinate: "#7A4E15",
    same_upazila_specific_name_signal_outside_500m: "#007DB8",
    threshold_sensitive_same_upazila_osm_500_1000m: "#FBB00E",
    zero_osm_in_expected_public_upazila: "#9B2226",
    same_upazila_osm_present_but_not_at_facility: "#D97706",
    no_nearby_same_upazila_osm_health_signal_within_3km: "#4A5568",
  };
  return colors[code] || "#6c757d";
}

function publicMapGapCount(summary: PsdqPublicMapGapSummary, code: string) {
  return summary.public_map_gap_code_counts.find((item) => item.name === code)?.rows || 0;
}

function PsdqPublicMapGapPanel({ summary }: { summary: PsdqPublicMapGapSummary }) {
  const outsideBufferNameSignals =
    summary.public_map_gap_scope.rows_with_same_upazila_specific_name_signal_far_from_registry_coordinate +
    summary.public_map_gap_scope.rows_with_same_upazila_specific_name_signal_outside_500m;

  return (
    <section className="showcase-section psdq-public-map-gap-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Public-map-gap triage</p>
          <h2>The 40 missing-map rows now have an inspection queue.</h2>
          <p>
            After separating coordinate-source failures, the public-map-gap
            pass keeps every valid-coordinate row open and sorts it by what a
            reviewer should check next: duplicate coordinates, same-upazila
            name signals, matching-radius sensitivity, zero-OSM upazilas, or
            row-level absence from nearby public-map health features.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Public-map-gap rows checked</span>
            <strong>
              {formatNumber(summary.public_map_gap_scope.public_map_gap_rows_checked)} rows;{" "}
              {formatNumber(summary.public_map_gap_scope.rows_closed_as_resolved)} closed
            </strong>
          </div>
          <div>
            <span>Priority-1 queue</span>
            <strong>{formatNumber(summary.public_map_gap_scope.priority_1_high_exposure_rows)} high-exposure rows</strong>
          </div>
          <div>
            <span>Zero-OSM expected upazilas</span>
            <strong>{formatNumber(summary.public_map_gap_scope.rows_in_zero_osm_expected_upazilas)} rows</strong>
          </div>
          <div>
            <span>Coordinate reuse warning</span>
            <strong>{formatNumber(summary.public_map_gap_scope.rows_with_duplicate_sample_coordinate)} rows reuse a sampled coordinate</strong>
          </div>
          <div>
            <span>Name support outside buffer</span>
            <strong>{formatNumber(outsideBufferNameSignals)} rows need row-level source review</strong>
          </div>
          <div>
            <span>Coordinate-repair overlap</span>
            <strong>{formatNumber(summary.public_map_gap_scope.rows_in_upazilas_with_coordinate_repair_flags)} rows sit in upazilas with repair flags</strong>
          </div>
        </div>
      </div>

      <div className="psdq-public-map-gap-grid">
        {PUBLIC_MAP_GAP_ORDER.filter((code) => publicMapGapCount(summary, code) > 0).map((code) => (
          <div key={code}>
            <span>{PUBLIC_MAP_GAP_LABELS[code]}</span>
            <strong>{formatNumber(publicMapGapCount(summary, code))}</strong>
            <em>{publicMapGapMeaning(code)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqPublicMapGapQueueChart rows={summary.upazila_queue_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ public-map-gap lane legend">
        {PUBLIC_MAP_GAP_ORDER.filter((code) => publicMapGapCount(summary, code) > 0).map((code) => (
          <span key={code}>
            <i style={{ background: publicMapGapColor(code) }} /> {PUBLIC_MAP_GAP_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the public-map-gap triage</p>
        <code>python public-service-data-quality/scripts/triage-bgd-facility-public-map-gaps.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-public-map-gap.md" download>
          Download public-map-gap note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-summary.json" download>
          Download public-map-gap summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap.csv" download>
          Download public-map-gap CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function publicMapGapMeaning(code: string) {
  const meanings: Record<string, string> = {
    valid_coordinate_reused_within_sample_public_map_gap: "Valid coordinate, but another sampled row uses it.",
    same_upazila_specific_name_signal_far_from_registry_coordinate: "Strong same-upazila name support appears far from the registry coordinate.",
    same_upazila_specific_name_signal_outside_500m: "Specific same-upazila OSM name support sits outside the original buffer.",
    threshold_sensitive_same_upazila_osm_500_1000m: "An OSM health feature appears just outside the 500m rule.",
    zero_osm_in_expected_public_upazila: "The pinned OSM pull has no joined health feature in that upazila.",
    same_upazila_osm_present_but_not_at_facility: "The upazila has mapped health features, but not at the sampled coordinate.",
    no_nearby_same_upazila_osm_health_signal_within_3km: "No same-upazila OSM health clue sits within 3km.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function PsdqPublicMapGapQueueChart({ rows }: { rows: PsdqPublicMapGapUpazilaRow[] }) {
  const width = 1040;
  const rowHeight = 46;
  const headerHeight = 64;
  const height = headerHeight + rows.length * rowHeight + 26;
  const labelX = 0;
  const barX = 240;
  const barWidth = 310;
  const clinicalX = 590;
  const osmX = 675;
  const proxyX = 760;
  const repairX = 955;

  return (
    <svg
      className="psdq-coded-chart psdq-public-map-gap-chart"
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      role="img"
      aria-label="Public-map-gap upazila queue after coordinate screening"
    >
      <text x={0} y={18} className="showcase-heatmap-title">
        Public-map-gap queue, upazila context after coordinate screening
      </text>
      <text x={0} y={38} className="showcase-heatmap-year">
        Unit: sampled DGHS row still open; source: public-map-gap summary JSON
      </text>
      <text x={barX} y={58} className="psdq-chart-head">
        Open-row lane mix
      </text>
      <text x={clinicalX} y={58} className="psdq-chart-head">
        DGHS
      </text>
      <text x={osmX} y={58} className="psdq-chart-head">
        OSM
      </text>
      <text x={proxyX} y={58} className="psdq-chart-head">
        Under-observed proxy
      </text>
      <text x={repairX} y={58} className="psdq-chart-head" textAnchor="end">
        Repair flags
      </text>

      {rows.map((row, index) => {
        const y = headerHeight + index * rowHeight;
        let x = barX;
        return (
          <g key={row.join_key}>
            <text x={labelX} y={y + 15} className="psdq-row-label">
              {row.upazila_name}
            </text>
            <text x={labelX} y={y + 31} className="psdq-row-sub">
              {row.district_name}, {row.division_name}
            </text>
            <rect x={barX} y={y} width={barWidth} height={22} fill="#eef2f5" />
            {PUBLIC_MAP_GAP_ORDER.map((code) => {
              const value = Number(row[code] || 0);
              const segmentWidth = row.public_map_gap_rows > 0 ? (value / row.public_map_gap_rows) * barWidth : 0;
              const segment = (
                <rect
                  key={code}
                  x={x}
                  y={y}
                  width={Math.max(0, segmentWidth)}
                  height={22}
                  fill={publicMapGapColor(code)}
                >
                  <title>{`${row.upazila_name}: ${formatNumber(value)} ${PUBLIC_MAP_GAP_LABELS[code]}`}</title>
                </rect>
              );
              x += segmentWidth;
              return segment;
            })}
            <text x={barX + barWidth + 12} y={y + 16} className="psdq-value">
              {formatNumber(row.public_map_gap_rows)}
            </text>
            <text x={clinicalX} y={y + 16} className="psdq-value">
              {formatNumber(row.active_clinical_facilities)}
            </text>
            <text x={osmX} y={y + 16} className="psdq-value">
              {formatNumber(row.osm_health)}
            </text>
            <text x={proxyX} y={y + 16} className="psdq-value">
              {formatNumber(row.underobserved_buildings_3km_p85_proxy)}
            </text>
            <text x={repairX} y={y + 16} className="psdq-value" textAnchor="end">
              {row.coordinate_repair_rows_same_upazila > 0
                ? formatNumber(row.coordinate_repair_rows_same_upazila)
                : "none"}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

const ROW_EVIDENCE_TIER_ORDER = [
  "source_repair_before_row_absence",
  "possible_match_or_buffer_review",
  "row_level_public_map_absence_review",
  "upazila_level_public_map_observability_review",
] as const;

const ROW_EVIDENCE_TIER_LABELS: Record<string, string> = {
  source_repair_before_row_absence: "Source repair first",
  possible_match_or_buffer_review: "Match or buffer review",
  row_level_public_map_absence_review: "Row-level absence review",
  upazila_level_public_map_observability_review: "Upazila observability",
};

function rowEvidenceColor(code: string) {
  const colors: Record<string, string> = {
    source_repair_before_row_absence: "#002569",
    possible_match_or_buffer_review: "#FBB00E",
    row_level_public_map_absence_review: "#007DB8",
    upazila_level_public_map_observability_review: "#9B2226",
  };
  return colors[code] || "#6c757d";
}

function rowEvidenceCount(summary: PsdqPublicMapGapEvidenceSummary, code: string) {
  return summary.row_evidence_tier_counts.find((item) => item.name === code)?.rows || 0;
}

function rowEvidenceMeaning(code: string) {
  const meanings: Record<string, string> = {
    source_repair_before_row_absence: "Duplicate coordinate or far same-name signal comes before map absence language.",
    possible_match_or_buffer_review: "The row could change under wider matching or alias inspection.",
    row_level_public_map_absence_review: "Same-upazila OSM exists, but not at the sampled DGHS coordinate.",
    upazila_level_public_map_observability_review: "The pinned health-feature cache has no joined OSM health feature in the upazila.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function PsdqPublicMapGapEvidencePanel({ summary }: { summary: PsdqPublicMapGapEvidenceSummary }) {
  return (
    <section className="showcase-section psdq-row-evidence-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Row-level public-source evidence</p>
          <h2>The inspection queue now tells reviewers what source to open.</h2>
          <p>
            The row-evidence pass keeps all public-map-gap rows open, but it
            stops treating them as one bucket. Every row gets a DGHS source
            note, public profile link, OSM coordinate-inspection link, OSM
            feature or absence note, and a reviewer action.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows with row evidence</span>
            <strong>
              {formatNumber(summary.row_evidence_scope.rows_with_row_evidence)} rows;{" "}
              {formatNumber(summary.row_evidence_scope.rows_closed_as_resolved)} closed
            </strong>
          </div>
          <div>
            <span>Priority-1 coverage</span>
            <strong>{formatNumber(summary.row_evidence_scope.priority_1_high_exposure_rows)} high-exposure rows</strong>
          </div>
          <div>
            <span>DGHS source links</span>
            <strong>{formatNumber(summary.row_evidence_scope.rows_with_dghs_public_profile_url)} profile URLs</strong>
          </div>
          <div>
            <span>Map inspection links</span>
            <strong>{formatNumber(summary.row_evidence_scope.rows_with_registry_coordinate_osm_inspection_url)} OSM coordinate views</strong>
          </div>
          <div>
            <span>Same-upazila OSM links</span>
            <strong>{formatNumber(summary.row_evidence_scope.rows_with_same_upazila_osm_feature_url)} rows</strong>
          </div>
          <div>
            <span>Rows kept open</span>
            <strong>{formatNumber(summary.row_evidence_scope.rows_kept_open)} source-review rows</strong>
          </div>
        </div>
      </div>

      <div className="psdq-row-evidence-grid">
        {ROW_EVIDENCE_TIER_ORDER.map((code) => (
          <div key={code}>
            <span>{ROW_EVIDENCE_TIER_LABELS[code]}</span>
            <strong>{formatNumber(rowEvidenceCount(summary, code))}</strong>
            <em>{rowEvidenceMeaning(code)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqPublicMapGapEvidenceQueueChart rows={summary.upazila_evidence_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ row-evidence tier legend">
        {ROW_EVIDENCE_TIER_ORDER.map((code) => (
          <span key={code}>
            <i style={{ background: rowEvidenceColor(code) }} /> {ROW_EVIDENCE_TIER_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="psdq-row-evidence-cards" aria-label="Top PSDQ row-evidence cards">
        {summary.row_card_rows.slice(0, 8).map((row) => (
          <article key={row.row_evidence_id} className="psdq-row-evidence-card">
            <div>
              <span>#{formatNumber(row.evidence_rank)} · {row.priority_scope.replaceAll("_", " ")}</span>
              <h3>{row.facility_name}</h3>
              <p>{row.upazila_name}, {row.district_name}</p>
            </div>
            <div className="psdq-row-evidence-tier" style={{ borderColor: rowEvidenceColor(row.row_evidence_tier) }}>
              {ROW_EVIDENCE_TIER_LABELS[row.row_evidence_tier] || row.row_evidence_tier.replaceAll("_", " ")}
            </div>
            <p>{row.row_evidence_reader_status}</p>
            <p className="psdq-row-evidence-note">{row.row_evidence_note}</p>
            <div className="psdq-row-evidence-links">
              {row.dghs_public_profile_url && (
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS profile
                </a>
              )}
              {row.registry_coordinate_osm_inspection_url && (
                <a href={row.registry_coordinate_osm_inspection_url} target="_blank" rel="noreferrer">
                  OSM coordinate
                </a>
              )}
              {row.nearest_same_upazila_osm_health_url && (
                <a href={row.nearest_same_upazila_osm_health_url} target="_blank" rel="noreferrer">
                  Nearest OSM health
                </a>
              )}
              {row.best_same_upazila_name_osm_url && (
                <a href={row.best_same_upazila_name_osm_url} target="_blank" rel="noreferrer">
                  Best name signal
                </a>
              )}
            </div>
          </article>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the row-evidence ledger</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-public-map-gap-row-evidence.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-public-map-gap-evidence.md" download>
          Download row-evidence note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json" download>
          Download row-evidence summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv" download>
          Download row-evidence CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function rowEvidenceTierValue(row: PsdqPublicMapGapEvidenceUpazilaRow, code: string) {
  return Number(row[code as keyof PsdqPublicMapGapEvidenceUpazilaRow] || 0);
}

function PsdqPublicMapGapEvidenceQueueChart({ rows }: { rows: PsdqPublicMapGapEvidenceUpazilaRow[] }) {
  const width = 1040;
  const rowHeight = 46;
  const headerHeight = 64;
  const height = headerHeight + rows.length * rowHeight + 26;
  const labelX = 0;
  const barX = 240;
  const barWidth = 310;
  const priorityX = 590;
  const clinicalX = 675;
  const osmX = 760;
  const proxyX = 955;

  return (
    <>
      <svg
        className="psdq-coded-chart psdq-row-evidence-chart"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="Public-map-gap row-evidence queue by upazila"
      >
        <text x={0} y={18} className="showcase-heatmap-title">
          Row-evidence queue, public-source action by upazila
        </text>
        <text x={0} y={38} className="showcase-heatmap-year">
          Unit: sampled DGHS row kept open; source: row-evidence summary JSON
        </text>
        <text x={barX} y={58} className="psdq-chart-head">
          Evidence tier mix
        </text>
        <text x={priorityX} y={58} className="psdq-chart-head">
          P1
        </text>
        <text x={clinicalX} y={58} className="psdq-chart-head">
          DGHS
        </text>
        <text x={osmX} y={58} className="psdq-chart-head">
          OSM
        </text>
        <text x={proxyX} y={58} className="psdq-chart-head" textAnchor="end">
          Under-observed proxy
        </text>

        {rows.map((row, index) => {
          const y = headerHeight + index * rowHeight;
          let x = barX;
          return (
            <g key={row.join_key}>
              <text x={labelX} y={y + 15} className="psdq-row-label">
                {row.upazila_name}
              </text>
              <text x={labelX} y={y + 31} className="psdq-row-sub">
                {row.district_name}, {row.division_name}
              </text>
              <rect x={barX} y={y} width={barWidth} height={22} fill="#eef2f5" />
              {ROW_EVIDENCE_TIER_ORDER.map((code) => {
                const value = rowEvidenceTierValue(row, code);
                const segmentWidth = row.row_evidence_rows > 0 ? (value / row.row_evidence_rows) * barWidth : 0;
                const segment = (
                  <rect
                    key={code}
                    x={x}
                    y={y}
                    width={Math.max(0, segmentWidth)}
                    height={22}
                    fill={rowEvidenceColor(code)}
                  >
                    <title>{`${row.upazila_name}: ${formatNumber(value)} ${ROW_EVIDENCE_TIER_LABELS[code]}`}</title>
                  </rect>
                );
                x += segmentWidth;
                return segment;
              })}
              <text x={barX + barWidth + 12} y={y + 16} className="psdq-value">
                {formatNumber(row.row_evidence_rows)}
              </text>
              <text x={priorityX} y={y + 16} className="psdq-value">
                {formatNumber(row.priority_1_rows)}
              </text>
              <text x={clinicalX} y={y + 16} className="psdq-value">
                {formatNumber(row.active_clinical_facilities)}
              </text>
              <text x={osmX} y={y + 16} className="psdq-value">
                {formatNumber(row.osm_health)}
              </text>
              <text x={proxyX} y={y + 16} className="psdq-value" textAnchor="end">
                {formatNumber(row.underobserved_buildings_3km_p85_proxy)}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="psdq-row-evidence-mobile-list" aria-label="Mobile public-map-gap row-evidence queue">
        <div>
          <strong>Row-evidence queue by upazila</strong>
          <span>Unit: sampled DGHS row kept open</span>
        </div>
        {rows.map((row) => (
          <article key={row.join_key}>
            <div>
              <strong>{row.upazila_name}</strong>
              <span>{row.district_name}, {row.division_name}</span>
            </div>
            <div className="psdq-row-evidence-mobile-bar" aria-label={`${row.upazila_name} evidence tier mix`}>
              {ROW_EVIDENCE_TIER_ORDER.map((code) => {
                const value = rowEvidenceTierValue(row, code);
                if (value <= 0) {
                  return null;
                }
                return (
                  <i
                    key={code}
                    title={`${formatNumber(value)} ${ROW_EVIDENCE_TIER_LABELS[code]}`}
                    style={{
                      background: rowEvidenceColor(code),
                      width: `${Math.max(8, (value / row.row_evidence_rows) * 100)}%`,
                    }}
                  />
                );
              })}
            </div>
            <div className="psdq-row-evidence-mobile-metrics">
              <span><b>{formatNumber(row.row_evidence_rows)}</b> rows</span>
              <span><b>{formatNumber(row.priority_1_rows)}</b> P1</span>
              <span><b>{formatNumber(row.active_clinical_facilities)}</b> DGHS</span>
              <span><b>{formatNumber(row.osm_health)}</b> OSM</span>
              <span><b>{formatNumber(row.underobserved_buildings_3km_p85_proxy)}</b> proxy</span>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}

const PUBLIC_MAP_INSPECTION_LANE_ORDER = [
  "source_repair_first",
  "possible_public_map_match_or_buffer_case",
  "facility_specific_public_map_absence_candidate",
  "upazila_public_map_observability_gap",
] as const;

const PUBLIC_MAP_INSPECTION_LANE_LABELS: Record<string, string> = {
  source_repair_first: "Source repair first",
  possible_public_map_match_or_buffer_case: "Possible map match or buffer case",
  facility_specific_public_map_absence_candidate: "Facility-specific absence candidate",
  upazila_public_map_observability_gap: "Upazila observability gap",
};

function publicMapInspectionColor(code: string) {
  const colors: Record<string, string> = {
    source_repair_first: "#002569",
    possible_public_map_match_or_buffer_case: "#FBB00E",
    facility_specific_public_map_absence_candidate: "#007DB8",
    upazila_public_map_observability_gap: "#9B2226",
  };
  return colors[code] || "#6c757d";
}

function publicMapInspectionCount(summary: PsdqPublicMapInspectionSummary, code: string) {
  return summary.inspection_lane_counts.find((item) => item.name === code)?.rows || 0;
}

function publicMapInspectionMeaning(code: string) {
  const meanings: Record<string, string> = {
    source_repair_first: "Coordinate or duplicate-row questions must be resolved before map absence language.",
    possible_public_map_match_or_buffer_case: "A mapped candidate exists outside the original rule and needs alias or buffer review.",
    facility_specific_public_map_absence_candidate: "The row is a candidate for manual public-map absence review, not closure.",
    upazila_public_map_observability_gap: "The upazila-level public-map layer is sparse enough that row-level absence is too strong.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function publicMapInspectionLaneValue(row: PsdqPublicMapInspectionUpazilaRow, code: string) {
  return Number(row[code as keyof PsdqPublicMapInspectionUpazilaRow] || 0);
}

function focusClassLabel(code: string) {
  const labels: Record<string, string> = {
    start_here_named_upazila: "Start with named-upazila rows",
    start_here_zero_osm_upazila_queue: "Zero-OSM upazila queue",
    priority_1_follow_on: "Priority-1 follow-on",
    priority_3_spot_check_backstop: "Priority-3 backstop",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function PsdqPublicMapInspectionPanel({ summary }: { summary: PsdqPublicMapInspectionSummary }) {
  return (
    <section className="showcase-section psdq-public-map-inspection-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Targeted public-map inspection</p>
          <h2>The queue is sharper, but no row is closed by AI.</h2>
          <p>
            This pass takes the 40 row-evidence records and asks what a
            reviewer should open first. It ranks public-map candidates, keeps
            source-repair rows out of absence claims, separates zero-OSM
            upazilas from facility-specific rows, and records what evidence
            would be needed before any row is closed or reclassified.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows inspected</span>
            <strong>
              {formatNumber(summary.inspection_scope.rows_inspected)} rows;{" "}
              {formatNumber(summary.inspection_scope.rows_closed_as_resolved)} closed
            </strong>
          </div>
          <div>
            <span>Priority-1 coverage</span>
            <strong>{formatNumber(summary.inspection_scope.priority_1_rows_inspected)} high-exposure rows</strong>
          </div>
          <div>
            <span>Start-here named rows</span>
            <strong>{formatNumber(summary.inspection_scope.start_here_named_upazila_rows)} rows with same-upazila review value</strong>
          </div>
          <div>
            <span>Zero-OSM upazila queue</span>
            <strong>{formatNumber(summary.inspection_scope.start_here_zero_osm_upazila_rows)} rows</strong>
          </div>
          <div>
            <span>Same-upazila candidates</span>
            <strong>{formatNumber(summary.inspection_scope.rows_with_same_upazila_candidate_public_map_feature)} candidate links</strong>
          </div>
          <div>
            <span>Specific-name signals</span>
            <strong>{formatNumber(summary.inspection_scope.rows_with_specific_name_signal_in_candidate_features)} rows</strong>
          </div>
        </div>
      </div>

      <div className="psdq-public-map-inspection-grid">
        {PUBLIC_MAP_INSPECTION_LANE_ORDER.map((code) => (
          <div key={code}>
            <span>{PUBLIC_MAP_INSPECTION_LANE_LABELS[code]}</span>
            <strong>{formatNumber(publicMapInspectionCount(summary, code))}</strong>
            <em>{publicMapInspectionMeaning(code)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-inspection-focus-strip" aria-label="PSDQ public-map inspection focus classes">
        {summary.focus_class_counts.map((item) => (
          <div key={item.name}>
            <span>{focusClassLabel(item.name)}</span>
            <strong>{formatNumber(item.rows)}</strong>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqPublicMapInspectionQueueChart rows={summary.upazila_inspection_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ public-map inspection lane legend">
        {PUBLIC_MAP_INSPECTION_LANE_ORDER.map((code) => (
          <span key={code}>
            <i style={{ background: publicMapInspectionColor(code) }} /> {PUBLIC_MAP_INSPECTION_LANE_LABELS[code]}
          </span>
        ))}
      </div>

      <div className="psdq-public-map-inspection-cards" aria-label="Top PSDQ targeted public-map inspection rows">
        {summary.row_card_rows.slice(0, 12).map((row) => (
          <article key={row.inspection_id} className="psdq-public-map-inspection-card">
            <div>
              <span>#{formatNumber(row.inspection_rank)} · {focusClassLabel(row.focus_class)}</span>
              <h3>{row.facility_name}</h3>
              <p>{row.upazila_name}, {row.district_name} · {row.facility_type_name}</p>
            </div>
            <div
              className="psdq-row-evidence-tier"
              style={{ borderColor: publicMapInspectionColor(row.inspection_lane) }}
            >
              {PUBLIC_MAP_INSPECTION_LANE_LABELS[row.inspection_lane] || row.inspection_lane.replaceAll("_", " ")}
            </div>
            <dl className="psdq-inspection-candidate">
              <div>
                <dt>Candidate</dt>
                <dd>{row.candidate_feature_1_name || "No named candidate"}</dd>
              </div>
              <div>
                <dt>Distance</dt>
                <dd>{formatNumber(row.candidate_feature_1_distance_m, 0)} m</dd>
              </div>
              <div>
                <dt>Name score</dt>
                <dd>{formatNumber(row.candidate_feature_1_name_score, 2)}</dd>
              </div>
            </dl>
            <p>{row.public_cache_finding}</p>
            <p className="psdq-row-evidence-note">{row.evidence_needed_to_close_or_reclassify}</p>
            <div className="psdq-row-evidence-links">
              {row.dghs_public_profile_url && (
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS profile
                </a>
              )}
              {row.registry_coordinate_osm_inspection_url && (
                <a href={row.registry_coordinate_osm_inspection_url} target="_blank" rel="noreferrer">
                  OSM coordinate
                </a>
              )}
              {row.candidate_feature_1_url && (
                <a href={row.candidate_feature_1_url} target="_blank" rel="noreferrer">
                  Candidate feature
                </a>
              )}
            </div>
          </article>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the targeted public-map inspection packet</p>
        <code>python public-service-data-quality/scripts/inspect-bgd-facility-public-map-targets.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-public-map-inspection.md" download>
          Download inspection note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection-summary.json" download>
          Download inspection summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-map-inspection.csv" download>
          Download inspection CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqPublicMapInspectionQueueChart({ rows }: { rows: PsdqPublicMapInspectionUpazilaRow[] }) {
  const width = 1040;
  const rowHeight = 46;
  const headerHeight = 64;
  const height = headerHeight + rows.length * rowHeight + 26;
  const labelX = 0;
  const barX = 240;
  const barWidth = 310;
  const priorityX = 590;
  const clinicalX = 675;
  const osmX = 760;
  const proxyX = 955;

  return (
    <>
      <svg
        className="psdq-coded-chart psdq-public-map-inspection-chart"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="Targeted public-map inspection queue by upazila"
      >
        <text x={0} y={18} className="showcase-heatmap-title">
          Targeted public-map inspection queue
        </text>
        <text x={0} y={38} className="showcase-heatmap-year">
          Unit: sampled DGHS row kept open; source: inspection summary JSON
        </text>
        <text x={barX} y={58} className="psdq-chart-head">
          Inspection lane mix
        </text>
        <text x={priorityX} y={58} className="psdq-chart-head">
          P1
        </text>
        <text x={clinicalX} y={58} className="psdq-chart-head">
          DGHS
        </text>
        <text x={osmX} y={58} className="psdq-chart-head">
          OSM
        </text>
        <text x={proxyX} y={58} className="psdq-chart-head" textAnchor="end">
          Under-observed proxy
        </text>

        {rows.map((row, index) => {
          const y = headerHeight + index * rowHeight;
          let x = barX;
          return (
            <g key={row.join_key}>
              <text x={labelX} y={y + 15} className="psdq-row-label">
                {row.upazila_name}
              </text>
              <text x={labelX} y={y + 31} className="psdq-row-sub">
                {row.district_name}, {row.division_name}
              </text>
              <rect x={barX} y={y} width={barWidth} height={22} fill="#eef2f5" />
              {PUBLIC_MAP_INSPECTION_LANE_ORDER.map((code) => {
                const value = publicMapInspectionLaneValue(row, code);
                const segmentWidth = row.inspection_rows > 0 ? (value / row.inspection_rows) * barWidth : 0;
                const segment = (
                  <rect
                    key={code}
                    x={x}
                    y={y}
                    width={Math.max(0, segmentWidth)}
                    height={22}
                    fill={publicMapInspectionColor(code)}
                  >
                    <title>{`${row.upazila_name}: ${formatNumber(value)} ${PUBLIC_MAP_INSPECTION_LANE_LABELS[code]}`}</title>
                  </rect>
                );
                x += segmentWidth;
                return segment;
              })}
              <text x={barX + barWidth + 12} y={y + 16} className="psdq-value">
                {formatNumber(row.inspection_rows)}
              </text>
              <text x={priorityX} y={y + 16} className="psdq-value">
                {formatNumber(row.priority_1_rows)}
              </text>
              <text x={clinicalX} y={y + 16} className="psdq-value">
                {formatNumber(row.active_clinical_facilities)}
              </text>
              <text x={osmX} y={y + 16} className="psdq-value">
                {formatNumber(row.osm_health)}
              </text>
              <text x={proxyX} y={y + 16} className="psdq-value" textAnchor="end">
                {formatNumber(row.underobserved_buildings_3km_p85_proxy)}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="psdq-public-map-inspection-mobile-list" aria-label="Mobile targeted public-map inspection queue">
        <div>
          <strong>Inspection queue by upazila</strong>
          <span>Unit: sampled DGHS row kept open</span>
        </div>
        {rows.map((row) => (
          <article key={row.join_key}>
            <div>
              <strong>{row.upazila_name}</strong>
              <span>{row.district_name}, {row.division_name}</span>
            </div>
            <div className="psdq-public-map-inspection-mobile-bar" aria-label={`${row.upazila_name} inspection lane mix`}>
              {PUBLIC_MAP_INSPECTION_LANE_ORDER.map((code) => {
                const value = publicMapInspectionLaneValue(row, code);
                if (value <= 0) {
                  return null;
                }
                return (
                  <i
                    key={code}
                    title={`${formatNumber(value)} ${PUBLIC_MAP_INSPECTION_LANE_LABELS[code]}`}
                    style={{
                      background: publicMapInspectionColor(code),
                      width: `${Math.max(8, (value / row.inspection_rows) * 100)}%`,
                    }}
                  />
                );
              })}
            </div>
            <div className="psdq-row-evidence-mobile-metrics">
              <span><b>{formatNumber(row.inspection_rows)}</b> rows</span>
              <span><b>{formatNumber(row.priority_1_rows)}</b> P1</span>
              <span><b>{formatNumber(row.start_here_rows)}</b> start</span>
              <span><b>{formatNumber(row.osm_health)}</b> OSM</span>
              <span><b>{formatNumber(row.underobserved_buildings_3km_p85_proxy)}</b> proxy</span>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}

const PUBLIC_SOURCE_CONFIRMATION_LABELS: Record<string, string> = {
  candidate_feature_retrieved_but_name_conflict_keep_open: "Candidate retrieved, name conflict",
  possible_same_facility_candidate_needs_manual_location_check: "Possible same facility, manual location check",
  source_repair_public_sources_retrieved_keep_open: "Source repair, sources retrieved",
  zero_osm_context_candidate_outside_upazila_keep_open: "Zero-OSM context, outside-upazila candidate",
};

function publicSourceConfirmationColor(code: string) {
  const colors: Record<string, string> = {
    candidate_feature_retrieved_but_name_conflict_keep_open: "#007DB8",
    possible_same_facility_candidate_needs_manual_location_check: "#FBB00E",
    source_repair_public_sources_retrieved_keep_open: "#002569",
    zero_osm_context_candidate_outside_upazila_keep_open: "#9B2226",
  };
  return colors[code] || "#6c757d";
}

function publicSourceConfirmationLabel(code: string) {
  return PUBLIC_SOURCE_CONFIRMATION_LABELS[code] || code.replaceAll("_", " ");
}

function PsdqPublicSourceConfirmationPanel({ summary }: { summary: PsdqPublicSourceConfirmationSummary }) {
  return (
    <section className="showcase-section psdq-public-source-confirmation-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">First-row public-source confirmation</p>
          <h2>The source links open, but the rows still stay open.</h2>
          <p>
            This pass fetches the public DGHS profile and the public OSM API
            record for the first targeted inspection rows. It records source
            reachability and live tag support, then keeps the row-level
            decision separate from API availability.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows checked</span>
            <strong>
              {formatNumber(summary.confirmation_scope.rows_checked)} rows;{" "}
              {formatNumber(summary.confirmation_scope.rows_closed_as_resolved)} closed
            </strong>
          </div>
          <div>
            <span>DGHS profiles retrieved</span>
            <strong>{formatNumber(summary.confirmation_scope.dghs_profiles_retrieved)} public profiles</strong>
          </div>
          <div>
            <span>OSM API records retrieved</span>
            <strong>{formatNumber(summary.confirmation_scope.osm_candidate_api_records_retrieved)} candidate features</strong>
          </div>
          <div>
            <span>DGHS token support</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_with_dghs_profile_token_support)} rows</strong>
          </div>
          <div>
            <span>High candidate-name score</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_with_candidate_name_score_at_least_0_75)} rows at 0.75+</strong>
          </div>
          <div>
            <span>Rows kept open</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_kept_open)} public-source rows</strong>
          </div>
        </div>
      </div>

      <div className="psdq-public-source-confirmation-grid">
        {summary.public_source_confirmation_lane_counts.map((item) => (
          <div key={item.name}>
            <span>{publicSourceConfirmationLabel(item.name)}</span>
            <strong>{formatNumber(item.rows)}</strong>
            <em>{publicSourceConfirmationMeaning(item.name)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqPublicSourceConfirmationScoreChart rows={summary.row_card_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ public-source confirmation lane legend">
        {summary.public_source_confirmation_lane_counts.map((item) => (
          <span key={item.name}>
            <i style={{ background: publicSourceConfirmationColor(item.name) }} />{" "}
            {publicSourceConfirmationLabel(item.name)}
          </span>
        ))}
      </div>

      <div className="psdq-public-source-confirmation-cards" aria-label="First PSDQ public-source confirmation rows">
        {summary.row_card_rows.map((row) => (
          <article key={row.confirmation_id} className="psdq-public-source-confirmation-card">
            <div>
              <span>#{formatNumber(row.confirmation_rank)} · {row.inspection_id}</span>
              <h3>{row.facility_name}</h3>
              <p>{row.upazila_name}, {row.district_name}</p>
            </div>
            <div
              className="psdq-row-evidence-tier"
              style={{ borderColor: publicSourceConfirmationColor(row.public_source_confirmation_lane) }}
            >
              {publicSourceConfirmationLabel(row.public_source_confirmation_lane)}
            </div>
            <dl className="psdq-confirmation-score-grid">
              <div>
                <dt>DGHS</dt>
                <dd>{row.dghs_profile_retrieved ? "retrieved" : "missing"}</dd>
              </div>
              <div>
                <dt>OSM API</dt>
                <dd>{row.candidate_osm_api_retrieved ? "retrieved" : "missing"}</dd>
              </div>
              <div>
                <dt>Name score</dt>
                <dd>{formatNumber(row.candidate_name_score_from_live_tags, 2)}</dd>
              </div>
            </dl>
            <p>
              Candidate: {row.candidate_osm_name_from_api || "unnamed OSM feature"} at{" "}
              {formatNumber(row.candidate_distance_m_from_inspection, 0)} m.
            </p>
            <p className="psdq-row-evidence-note">{row.evidence_needed_next}</p>
            <div className="psdq-row-evidence-links">
              <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                DGHS profile
              </a>
              <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                OSM feature
              </a>
              <a href={row.candidate_osm_api_url} target="_blank" rel="noreferrer">
                OSM API
              </a>
            </div>
          </article>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the public-source confirmation packet</p>
        <code>python public-service-data-quality/scripts/confirm-bgd-facility-public-map-first-rows.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-public-source-confirmation.md" download>
          Download confirmation note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json" download>
          Download confirmation summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation.csv" download>
          Download confirmation CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function publicSourceConfirmationMeaning(code: string) {
  const meanings: Record<string, string> = {
    candidate_feature_retrieved_but_name_conflict_keep_open:
      "The public candidate exists, but name support is not enough for row-level labeling.",
    possible_same_facility_candidate_needs_manual_location_check:
      "Public source retrieval supports a closer look, not automatic reclassification.",
    source_repair_public_sources_retrieved_keep_open:
      "The source links open, but duplicate-coordinate or coordinate-source repair comes first.",
    zero_osm_context_candidate_outside_upazila_keep_open:
      "The candidate is context for sparse public mapping, not row-level evidence.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function PsdqPublicSourceConfirmationScoreChart({ rows }: { rows: PsdqPublicSourceConfirmationCardRow[] }) {
  const width = 1040;
  const rowHeight = 46;
  const headerHeight = 64;
  const height = headerHeight + rows.length * rowHeight + 26;
  const labelX = 0;
  const laneX = 300;
  const scoreX = 620;
  const barWidth = 240;
  const scoreValueX = scoreX + barWidth + 16;
  const dghsX = 925;
  const osmX = 1000;

  return (
    <>
      <svg
        className="psdq-coded-chart psdq-public-source-confirmation-chart"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="First-row public-source confirmation scores"
      >
        <text x={0} y={18} className="showcase-heatmap-title">
          First-row public-source confirmation
        </text>
        <text x={0} y={38} className="showcase-heatmap-year">
          Unit: first inspection row; source: live DGHS profile and OSM API retrieval
        </text>
        <text x={laneX} y={58} className="psdq-chart-head">
          Confirmation lane
        </text>
        <text x={scoreX} y={58} className="psdq-chart-head">
          OSM name score
        </text>
        <text x={dghsX} y={58} className="psdq-chart-head">
          DGHS
        </text>
        <text x={osmX} y={58} className="psdq-chart-head">
          OSM API
        </text>

        {rows.map((row, index) => {
          const y = headerHeight + index * rowHeight;
          const score = Math.max(0, Math.min(1, row.candidate_name_score_from_live_tags || 0));
          return (
            <g key={row.confirmation_id}>
              <text x={labelX} y={y + 15} className="psdq-row-label">
                {shortChartLabel(row.facility_name, 40)}
              </text>
              <text x={labelX} y={y + 31} className="psdq-row-sub">
                {row.upazila_name}, {row.district_name}
              </text>
              <rect
                x={laneX}
                y={y}
                width={260}
                height={22}
                fill={publicSourceConfirmationColor(row.public_source_confirmation_lane)}
                opacity={0.9}
              >
                <title>{publicSourceConfirmationLabel(row.public_source_confirmation_lane)}</title>
              </rect>
              <rect x={scoreX} y={y} width={barWidth} height={22} fill="#eef2f5" />
              <rect
                x={scoreX}
                y={y}
                width={Math.max(2, score * barWidth)}
                height={22}
                fill={score >= 0.75 ? "#5A8227" : "#007DB8"}
              />
              <text x={scoreValueX} y={y + 16} className="psdq-value">
                {formatNumber(score, 2)}
              </text>
              <text x={dghsX} y={y + 16} className="psdq-value">
                {row.dghs_profile_retrieved ? "yes" : "no"}
              </text>
              <text x={osmX} y={y + 16} className="psdq-value">
                {row.candidate_osm_api_retrieved ? "yes" : "no"}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="psdq-public-source-confirmation-mobile-list" aria-label="Mobile public-source confirmation scores">
        <div>
          <strong>First-row confirmation scores</strong>
          <span>Unit: first inspection row kept open</span>
        </div>
        {rows.map((row) => (
          <article key={row.confirmation_id}>
            <div>
              <strong>{row.facility_name}</strong>
              <span>{row.upazila_name}, {row.district_name}</span>
            </div>
            <i
              style={{
                background: publicSourceConfirmationColor(row.public_source_confirmation_lane),
                width: "100%",
              }}
            />
            <div className="psdq-row-evidence-mobile-metrics">
              <span><b>{row.dghs_profile_retrieved ? "yes" : "no"}</b> DGHS</span>
              <span><b>{row.candidate_osm_api_retrieved ? "yes" : "no"}</b> OSM API</span>
              <span><b>{formatNumber(row.candidate_name_score_from_live_tags, 2)}</b> score</span>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}

function PsdqTargetedSourceConfirmationPanel({ summary }: { summary: PsdqTargetedSourceConfirmationSummary }) {
  return (
    <section className="showcase-section psdq-targeted-source-confirmation-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Targeted-row public-source confirmation</p>
          <h2>All 40 source links open; none close the row.</h2>
          <p>
            The second confirmation pass extends the retrieval check to every
            targeted inspection row. The result is stronger evidence for the
            review queue: public source availability is documented, while row
            classification remains separate from source reachability.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows checked</span>
            <strong>
              {formatNumber(summary.confirmation_scope.rows_checked)} rows;{" "}
              {formatNumber(summary.confirmation_scope.rows_closed_as_resolved)} closed
            </strong>
          </div>
          <div>
            <span>Priority-1 rows covered</span>
            <strong>{formatNumber(summary.confirmation_scope.priority_1_rows_checked)} rows</strong>
          </div>
          <div>
            <span>DGHS profiles retrieved</span>
            <strong>{formatNumber(summary.confirmation_scope.dghs_profiles_retrieved)} public profiles</strong>
          </div>
          <div>
            <span>OSM API records retrieved</span>
            <strong>{formatNumber(summary.confirmation_scope.osm_candidate_api_records_retrieved)} candidate features</strong>
          </div>
          <div>
            <span>High candidate-name score</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_with_candidate_name_score_at_least_0_75)} rows at 0.75+</strong>
          </div>
          <div>
            <span>Rows kept open</span>
            <strong>{formatNumber(summary.confirmation_scope.rows_kept_open)} public-source rows</strong>
          </div>
        </div>
      </div>

      <div className="psdq-public-source-confirmation-grid">
        {summary.public_source_confirmation_lane_counts.map((item) => (
          <div key={item.name}>
            <span>{publicSourceConfirmationLabel(item.name)}</span>
            <strong>{formatNumber(item.rows)}</strong>
            <em>{publicSourceConfirmationMeaning(item.name)}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqTargetedSourceConfirmationUpazilaChart rows={summary.upazila_confirmation_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ targeted-row public-source confirmation lane legend">
        {summary.public_source_confirmation_lane_counts.map((item) => (
          <span key={item.name}>
            <i style={{ background: publicSourceConfirmationColor(item.name) }} />{" "}
            {publicSourceConfirmationLabel(item.name)}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the targeted-row confirmation packet</p>
        <code>python public-service-data-quality/scripts/confirm-bgd-facility-public-map-targeted-rows.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-public-source-confirmation-targeted-rows.md" download>
          Download targeted-row confirmation note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json" download>
          Download targeted-row summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv" download>
          Download targeted-row CSV
        </a>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqTargetedSourceConfirmationUpazilaChart({ rows }: { rows: PsdqTargetedSourceConfirmationUpazilaRow[] }) {
  const width = 1040;
  const rowHeight = 42;
  const headerHeight = 66;
  const height = headerHeight + rows.length * rowHeight + 30;
  const labelX = 0;
  const barX = 300;
  const barWidth = 500;
  const countX = 830;
  const scoreX = 930;

  return (
    <>
      <svg
        className="psdq-coded-chart psdq-targeted-source-confirmation-chart"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="Targeted-row public-source confirmation by upazila"
      >
        <text x={0} y={18} className="showcase-heatmap-title">
          Targeted-row confirmation lanes by upazila
        </text>
        <text x={0} y={38} className="showcase-heatmap-year">
          Unit: targeted inspection row; source: live DGHS profile and OSM API retrieval
        </text>
        <text x={barX} y={58} className="psdq-chart-head">
          Public-source lane mix
        </text>
        <text x={countX} y={58} className="psdq-chart-head">
          rows
        </text>
        <text x={scoreX} y={58} className="psdq-chart-head">
          0.75+ score
        </text>

        {rows.map((row, index) => {
          const y = headerHeight + index * rowHeight;
          const total = Math.max(1, row.rows);
          const segments = [
            ["source_repair_public_sources_retrieved_keep_open", row.source_repair_rows],
            ["possible_same_facility_candidate_needs_manual_location_check", row.possible_same_facility_rows],
            ["candidate_feature_retrieved_but_name_conflict_keep_open", row.name_conflict_rows],
            ["zero_osm_context_candidate_outside_upazila_keep_open", row.zero_osm_context_rows],
          ] as const;
          let x = barX;
          return (
            <g key={`${row.district_name}-${row.upazila_name}`}>
              <text x={labelX} y={y + 15} className="psdq-row-label">
                {shortChartLabel(row.upazila_name, 30)}
              </text>
              <text x={labelX} y={y + 31} className="psdq-row-sub">
                {row.district_name}; {formatNumber(row.priority_1_rows)} priority-1 rows
              </text>
              {segments.map(([lane, count]) => {
                const segmentWidth = (count / total) * barWidth;
                const currentX = x;
                x += segmentWidth;
                if (count <= 0) return null;
                return (
                  <rect
                    key={lane}
                    x={currentX}
                    y={y}
                    width={Math.max(2, segmentWidth)}
                    height={22}
                    fill={publicSourceConfirmationColor(lane)}
                  >
                    <title>
                      {publicSourceConfirmationLabel(lane)}: {formatNumber(count)} rows
                    </title>
                  </rect>
                );
              })}
              <text x={countX} y={y + 16} className="psdq-value">
                {formatNumber(row.rows)}
              </text>
              <text x={scoreX} y={y + 16} className="psdq-value">
                {formatNumber(row.rows_with_candidate_name_score_at_least_0_75)}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="psdq-targeted-source-confirmation-mobile-list" aria-label="Mobile targeted-row confirmation by upazila">
        <div>
          <strong>Targeted-row confirmation by upazila</strong>
          <span>Unit: targeted inspection row kept open</span>
        </div>
        {rows.map((row) => {
          const total = Math.max(1, row.rows);
          const segments = [
            ["source_repair_public_sources_retrieved_keep_open", row.source_repair_rows],
            ["possible_same_facility_candidate_needs_manual_location_check", row.possible_same_facility_rows],
            ["candidate_feature_retrieved_but_name_conflict_keep_open", row.name_conflict_rows],
            ["zero_osm_context_candidate_outside_upazila_keep_open", row.zero_osm_context_rows],
          ] as const;
          return (
            <article key={`${row.district_name}-${row.upazila_name}`}>
              <div>
                <strong>{row.upazila_name}</strong>
                <span>{row.district_name}; {formatNumber(row.priority_1_rows)} priority-1 rows</span>
              </div>
              <div className="psdq-targeted-confirmation-mobile-bar">
                {segments.map(([lane, count]) => {
                  if (count <= 0) return null;
                  return (
                    <i
                      key={lane}
                      style={{
                        background: publicSourceConfirmationColor(lane),
                        width: `${Math.max(3, (count / total) * 100)}%`,
                      }}
                    />
                  );
                })}
              </div>
              <div className="psdq-row-evidence-mobile-metrics">
                <span><b>{formatNumber(row.rows)}</b> rows</span>
                <span><b>{formatNumber(row.dghs_profiles_retrieved)}</b> DGHS</span>
                <span><b>{formatNumber(row.rows_with_candidate_name_score_at_least_0_75)}</b> 0.75+</span>
              </div>
            </article>
          );
        })}
      </div>
    </>
  );
}

function decisionLedgerColor(code: string) {
  const colors: Record<string, string> = {
    source_repair_first: "#002569",
    possible_same_facility_location_review: "#FBB00E",
    high_exposure_name_conflict_review: "#007DB8",
    lower_priority_name_conflict_deferred: "#8796a5",
    zero_osm_upazila_observability_deferred: "#9B2226",
  };
  return colors[code] || "#6c757d";
}

function decisionLedgerMeaning(code: string) {
  const meanings: Record<string, string> = {
    source_repair_first: "Resolve coordinate or source repair before any map-absence label.",
    possible_same_facility_location_review: "Check identity and location before any same-facility reclassification.",
    high_exposure_name_conflict_review: "Keep in the high-exposure queue until a public alias or location source resolves the name conflict.",
  };
  return meanings[code] || code.replaceAll("_", " ");
}

function PsdqPublicSourceDecisionLedgerPanel({ summary }: { summary: PsdqPublicSourceDecisionLedgerSummary }) {
  return (
    <section className="showcase-section psdq-public-source-decision-ledger-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Public-source decision ledger</p>
          <h2>The next 16 rows are a review queue, not a closure list.</h2>
          <p>
            After source retrieval, the ledger narrows the next public-source
            work to rows where a reviewer can ask a row-level question. It
            keeps zero-OSM upazila context out of the decision queue and keeps
            all rows open until public evidence supports a change.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows read</span>
            <strong>{formatNumber(summary.decision_scope.targeted_confirmation_rows)} targeted confirmations</strong>
          </div>
          <div>
            <span>Decision ledger</span>
            <strong>
              {formatNumber(summary.decision_scope.decision_ledger_rows)} rows;{" "}
              {formatNumber(summary.decision_scope.rows_closed_as_resolved)} closed
            </strong>
          </div>
          <div>
            <span>Source repair first</span>
            <strong>{formatNumber(summary.decision_scope.source_repair_rows)} rows</strong>
          </div>
          <div>
            <span>Possible same facility</span>
            <strong>{formatNumber(summary.decision_scope.possible_same_facility_rows)} rows</strong>
          </div>
          <div>
            <span>Priority-1 name conflict</span>
            <strong>{formatNumber(summary.decision_scope.high_exposure_name_conflict_rows)} rows</strong>
          </div>
          <div>
            <span>Deferred context</span>
            <strong>
              {formatNumber(summary.decision_scope.deferred_zero_osm_context_rows + summary.decision_scope.deferred_lower_priority_name_conflict_rows)} rows
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-public-source-decision-ledger-grid">
        {summary.decision_track_counts.map((item) => (
          <div key={item.name}>
            <span>{item.label}</span>
            <strong>{formatNumber(item.rows)}</strong>
            <em>{decisionLedgerMeaning(item.name)}</em>
          </div>
        ))}
        {summary.deferred_scope_counts.map((item) => (
          <div key={item.name}>
            <span>{item.name === "zero_osm_upazila_observability_deferred" ? "Zero-OSM context deferred" : "Lower-priority name conflicts deferred"}</span>
            <strong>{formatNumber(item.rows)}</strong>
            <em>{item.name === "zero_osm_upazila_observability_deferred" ? "Upazila observability context, not row-level evidence." : "Spot-check rows wait behind the priority-1 queue."}</em>
          </div>
        ))}
      </div>

      <div className="psdq-coded-chart-wrap">
        <PsdqDecisionLedgerRowChart rows={summary.decision_rows} />
      </div>

      <div className="freshness-legend psdq-coded-legend" aria-label="PSDQ public-source decision ledger legend">
        {summary.decision_track_counts.map((item) => (
          <span key={item.name}>
            <i style={{ background: decisionLedgerColor(item.name) }} /> {item.label}
          </span>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the public-source decision ledger</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-public-source-decision-ledger.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-public-source-decision-ledger.md" download>
          Download decision-ledger note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json" download>
          Download decision-ledger summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv" download>
          Download decision-ledger CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqDecisionLedgerRowChart({ rows }: { rows: PsdqPublicSourceDecisionLedgerRow[] }) {
  const width = 1040;
  const rowHeight = 44;
  const headerHeight = 66;
  const height = headerHeight + rows.length * rowHeight + 30;
  const labelX = 0;
  const trackX = 330;
  const trackWidth = 240;
  const scoreX = 600;
  const scoreWidth = 170;
  const distanceX = 820;
  const distanceBarWidth = 125;
  const maxDistance = Math.max(1, ...rows.map((row) => Number(row.candidate_distance_m_from_inspection || 0)));

  return (
    <>
      <svg
        className="psdq-coded-chart psdq-public-source-decision-ledger-chart"
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        role="img"
        aria-label="Public-source decision ledger rows"
      >
        <text x={0} y={18} className="showcase-heatmap-title">
          Decision ledger: row-level reviewer questions
        </text>
        <text x={0} y={38} className="showcase-heatmap-year">
          Unit: selected targeted inspection row; source: public-source decision ledger summary JSON
        </text>
        <text x={trackX} y={58} className="psdq-chart-head">
          Decision track
        </text>
        <text x={scoreX} y={58} className="psdq-chart-head">
          OSM name score
        </text>
        <text x={distanceX} y={58} className="psdq-chart-head">
          Candidate distance
        </text>

        {rows.map((row, index) => {
          const y = headerHeight + index * rowHeight;
          const score = Math.max(0, Math.min(1, Number(row.candidate_name_score_from_live_tags || 0)));
          const distance = Math.max(0, Number(row.candidate_distance_m_from_inspection || 0));
          const distanceWidth = Math.max(2, (distance / maxDistance) * distanceBarWidth);
          return (
            <g key={row.decision_id}>
              <text x={labelX} y={y + 15} className="psdq-row-label">
                {shortChartLabel(row.facility_name, 40)}
              </text>
              <text x={labelX} y={y + 31} className="psdq-row-sub">
                {row.upazila_name}, {row.district_name}
              </text>
              <rect
                x={trackX}
                y={y}
                width={trackWidth}
                height={22}
                fill={decisionLedgerColor(row.decision_track)}
              >
                <title>{row.decision_track_label}</title>
              </rect>
              <rect x={scoreX} y={y} width={scoreWidth} height={22} fill="#eef2f5" />
              <rect
                x={scoreX}
                y={y}
                width={Math.max(2, score * scoreWidth)}
                height={22}
                fill={score >= 0.75 ? "#5A8227" : "#007DB8"}
              />
              <text x={scoreX + scoreWidth + 12} y={y + 16} className="psdq-value">
                {formatNumber(score, 2)}
              </text>
              <rect x={distanceX} y={y} width={distanceBarWidth} height={22} fill="#eef2f5" />
              <rect x={distanceX} y={y} width={distanceWidth} height={22} fill="#5A8227" />
              <text x={distanceX + distanceBarWidth + 12} y={y + 16} className="psdq-value">
                {formatNumber(distance / 1000, 1)} km
              </text>
            </g>
          );
        })}
      </svg>
      <div className="psdq-public-source-decision-ledger-mobile-list" aria-label="Mobile public-source decision ledger rows">
        <div>
          <strong>Decision ledger rows</strong>
          <span>Unit: selected row kept open</span>
        </div>
        {rows.map((row) => {
          const score = Number(row.candidate_name_score_from_live_tags || 0);
          const distanceKm = Number(row.candidate_distance_m_from_inspection || 0) / 1000;
          return (
            <article key={row.decision_id}>
              <div>
                <strong>{row.facility_name}</strong>
                <span>{row.upazila_name}, {row.district_name}</span>
              </div>
              <div
                className="psdq-row-evidence-tier"
                style={{ borderColor: decisionLedgerColor(row.decision_track) }}
              >
                {row.decision_track_label}
              </div>
              <span>Candidate: {row.candidate_osm_name_from_api || "unnamed OSM feature"}</span>
              <div className="psdq-row-evidence-mobile-metrics">
                <span><b>{formatNumber(score, 2)}</b> score</span>
                <span><b>{formatNumber(distanceKm, 1)} km</b> distance</span>
                <span><b>{row.priority_scope === PSDQ_PRIORITY_1 ? "yes" : "no"}</b> priority-1</span>
              </div>
            </article>
          );
        })}
      </div>
    </>
  );
}

function possibleSameFacilityColor(code: string) {
  const colors: Record<string, string> = {
    name_support_strong_location_unresolved: "#5A8227",
    name_support_partial_location_unresolved: "#FBB00E",
    name_support_weak_location_unresolved: "#A33A2A",
  };
  return colors[code] || "#6c757d";
}

function possibleSameFacilityLabel(code: string) {
  const labels: Record<string, string> = {
    name_support_strong_location_unresolved: "Strong name, location unresolved",
    name_support_partial_location_unresolved: "Partial name, location unresolved",
    name_support_weak_location_unresolved: "Weak name, location unresolved",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function possibleSameFacilityDistanceLabel(code: string) {
  const labels: Record<string, string> = {
    candidate_2km_to_under_3km_from_inspection_point: "2-3 km from inspection point",
    candidate_3km_or_more_from_inspection_point: "3 km or more from inspection point",
    candidate_1km_to_under_2km_from_inspection_point: "1-2 km from inspection point",
    candidate_under_1km_from_inspection_point: "Under 1 km from inspection point",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function PsdqPossibleSameFacilityReviewPanel({ summary }: { summary: PsdqPossibleSameFacilityReviewSummary }) {
  const maxDistance = Math.max(
    1,
    ...summary.review_rows.map((row) => Number(row.candidate_distance_m_from_inspection || 0))
  );
  const minDistance = summary.possible_same_facility_scope.min_candidate_distance_m;
  const maxDistanceScope = summary.possible_same_facility_scope.max_candidate_distance_m;
  const minScore = summary.possible_same_facility_scope.min_candidate_name_score;
  const maxScore = summary.possible_same_facility_scope.max_candidate_name_score;

  return (
    <section className="showcase-section psdq-possible-same-facility-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Possible same-facility review</p>
          <h2>A matching name is not enough when location is still unresolved.</h2>
          <p>
            The review packet isolates the three public-map candidates that
            could be same-facility matches. It puts name support beside
            candidate distance, then keeps every row open until identity and
            location are supported together.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows reviewed</span>
            <strong>{formatNumber(summary.possible_same_facility_scope.possible_same_facility_rows)}</strong>
          </div>
          <div>
            <span>Public sources retrieved</span>
            <strong>
              {formatNumber(summary.possible_same_facility_scope.dghs_profiles_retrieved)} DGHS /{" "}
              {formatNumber(summary.possible_same_facility_scope.osm_api_records_retrieved)} OSM
            </strong>
          </div>
          <div>
            <span>Name score range</span>
            <strong>{formatNumber(minScore ?? 0, 2)}-{formatNumber(maxScore ?? 0, 2)}</strong>
          </div>
          <div>
            <span>Distance range</span>
            <strong>
              {formatNumber((minDistance ?? 0) / 1000, 1)}-{formatNumber((maxDistanceScope ?? 0) / 1000, 1)} km
            </strong>
          </div>
          <div>
            <span>2 km or more</span>
            <strong>{formatNumber(summary.possible_same_facility_scope.rows_with_candidate_distance_2km_or_more)} rows</strong>
          </div>
          <div>
            <span>Closure / reclass / map absence</span>
            <strong>
              {formatNumber(summary.possible_same_facility_scope.rows_allowed_for_closure)} /{" "}
              {formatNumber(summary.possible_same_facility_scope.rows_allowed_for_same_facility_reclassification)} /{" "}
              {formatNumber(summary.possible_same_facility_scope.rows_allowed_for_map_absence_language)}
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-possible-same-facility-grid">
        {summary.review_rows.map((row) => {
          const color = possibleSameFacilityColor(row.name_evidence_class);
          const score = Number(row.candidate_name_score_from_live_tags || 0);
          const distance = Number(row.candidate_distance_m_from_inspection || 0);
          const scoreWidth = Math.max(4, Math.min(100, score * 100));
          const distanceWidth = Math.max(4, Math.min(100, (distance / maxDistance) * 100));
          return (
            <article key={row.possible_same_facility_review_id} style={{ borderColor: color }}>
              <div className="psdq-possible-same-facility-card-head">
                <span>{row.possible_same_facility_review_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.upazila_name}, {row.district_name}</em>
              </div>
              <div className="psdq-possible-same-facility-class" style={{ background: color }}>
                {possibleSameFacilityLabel(row.name_evidence_class)}
              </div>
              <div className="psdq-possible-same-facility-links">
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS {row.dghs_profile_http_status}
                </a>
                <a href={row.candidate_osm_api_url} target="_blank" rel="noreferrer">
                  OSM API {row.candidate_osm_api_http_status}
                </a>
                <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                  Map feature
                </a>
              </div>
              <div className="psdq-possible-same-facility-candidate">
                <span>Candidate</span>
                <strong>{row.candidate_osm_name_from_api || "Unnamed OSM feature"}</strong>
                <em>{row.candidate_osm_type} {row.candidate_osm_id}; {row.candidate_osm_tags_compact}</em>
              </div>
              <div className="psdq-possible-same-facility-pair">
                <div>
                  <span>Name support</span>
                  <strong>{formatNumber(score, 2)}</strong>
                  <i aria-label="Name-score bar">
                    <b style={{ width: `${scoreWidth}%`, background: color }} />
                  </i>
                </div>
                <div>
                  <span>Location distance</span>
                  <strong>{formatNumber(distance / 1000, 1)} km</strong>
                  <i aria-label="Distance bar">
                    <b style={{ width: `${distanceWidth}%`, background: "#002569" }} />
                  </i>
                </div>
              </div>
              <div className="psdq-possible-same-facility-distance">
                {possibleSameFacilityDistanceLabel(row.candidate_distance_band)}
              </div>
              <p>{row.review_action}</p>
              <div className="psdq-possible-same-facility-gates">
                <div>
                  <span>Reclassify only if</span>
                  <p>{row.minimum_evidence_to_reclassify_as_same_facility}</p>
                </div>
                <div>
                  <span>Keep as map absence only if</span>
                  <p>{row.minimum_evidence_to_keep_as_map_absence}</p>
                </div>
              </div>
              <div className="psdq-possible-same-facility-status">
                <span>keep open</span>
                <span>0 closed</span>
                <span>0 reclassified</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the possible same-facility review</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-possible-same-facility-review.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-possible-same-facility-review.md" download>
          Download possible same-facility review note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-possible-same-facility-review-summary.json" download>
          Download possible same-facility summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-possible-same-facility-review.csv" download>
          Download possible same-facility CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function priorityNameConflictColor(code: string) {
  const colors: Record<string, string> = {
    near_name_candidate_still_needs_alias_or_location_source: "#5A8227",
    admin_place_name_candidate_still_needs_facility_alias_source: "#FBB00E",
    distant_different_name_candidate_nearby_context_only: "#A33A2A",
    different_name_candidate_needs_public_alias_check: "#007DB8",
  };
  return colors[code] || "#6c757d";
}

function priorityNameConflictLabel(code: string) {
  const labels: Record<string, string> = {
    near_name_candidate_still_needs_alias_or_location_source: "Near name, alias source needed",
    admin_place_name_candidate_still_needs_facility_alias_source: "Place name, facility alias needed",
    distant_different_name_candidate_nearby_context_only: "Distant different-name context",
    different_name_candidate_needs_public_alias_check: "Different name, alias check needed",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function priorityNameConflictDistanceLabel(code: string) {
  const labels: Record<string, string> = {
    candidate_10km_or_more_from_inspection_point: "10 km or more from inspection point",
    candidate_5km_to_under_10km_from_inspection_point: "5-10 km from inspection point",
    candidate_2km_to_under_5km_from_inspection_point: "2-5 km from inspection point",
    candidate_under_2km_from_inspection_point: "Under 2 km from inspection point",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function PsdqPriorityNameConflictReviewPanel({ summary }: { summary: PsdqPriorityNameConflictReviewSummary }) {
  const maxDistance = Math.max(
    1,
    ...summary.review_rows.map((row) => Number(row.candidate_distance_m_from_inspection || 0))
  );
  const minDistance = summary.priority_name_conflict_scope.min_candidate_distance_m;
  const maxDistanceScope = summary.priority_name_conflict_scope.max_candidate_distance_m;
  const minScore = summary.priority_name_conflict_scope.min_candidate_name_score;
  const maxScore = summary.priority_name_conflict_scope.max_candidate_name_score;

  return (
    <section className="showcase-section psdq-priority-name-conflict-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Priority name-conflict review</p>
          <h2>Nine high-exposure rows have public candidates, but no alias source yet.</h2>
          <p>
            The review separates public-map visibility from row resolution.
            Every row has a retrieved DGHS profile and OSM feature, but the
            current artifacts do not show a public alias or location source
            that resolves the name conflict.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows reviewed</span>
            <strong>{formatNumber(summary.priority_name_conflict_scope.priority_name_conflict_rows)}</strong>
          </div>
          <div>
            <span>Public sources retrieved</span>
            <strong>
              {formatNumber(summary.priority_name_conflict_scope.dghs_profiles_retrieved)} DGHS /{" "}
              {formatNumber(summary.priority_name_conflict_scope.osm_api_records_retrieved)} OSM
            </strong>
          </div>
          <div>
            <span>Name score range</span>
            <strong>{formatNumber(minScore ?? 0, 2)}-{formatNumber(maxScore ?? 0, 2)}</strong>
          </div>
          <div>
            <span>Distance range</span>
            <strong>
              {formatNumber((minDistance ?? 0) / 1000, 1)}-{formatNumber((maxDistanceScope ?? 0) / 1000, 1)} km
            </strong>
          </div>
          <div>
            <span>5 km or more</span>
            <strong>{formatNumber(summary.priority_name_conflict_scope.rows_with_candidate_distance_5km_or_more)} rows</strong>
          </div>
          <div>
            <span>Alias/location sources</span>
            <strong>{formatNumber(summary.priority_name_conflict_scope.public_alias_or_location_sources_found_by_current_artifacts)}</strong>
          </div>
          <div>
            <span>Admin-place candidate names</span>
            <strong>{formatNumber(summary.priority_name_conflict_scope.rows_where_candidate_contains_admin_place_name)} rows</strong>
          </div>
          <div>
            <span>Closure / reclass / map absence</span>
            <strong>
              {formatNumber(summary.priority_name_conflict_scope.rows_allowed_for_closure)} /{" "}
              {formatNumber(summary.priority_name_conflict_scope.rows_allowed_for_same_facility_reclassification)} /{" "}
              {formatNumber(summary.priority_name_conflict_scope.rows_allowed_for_map_absence_language)}
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-priority-name-conflict-grid">
        {summary.review_rows.map((row) => {
          const color = priorityNameConflictColor(row.name_conflict_review_class);
          const score = Number(row.candidate_name_score_from_live_tags || 0);
          const distance = Number(row.candidate_distance_m_from_inspection || 0);
          const scoreWidth = Math.max(4, Math.min(100, score * 100));
          const distanceWidth = Math.max(4, Math.min(100, (distance / maxDistance) * 100));
          return (
            <article key={row.priority_name_conflict_review_id} style={{ borderColor: color }}>
              <div className="psdq-priority-name-conflict-card-head">
                <span>{row.priority_name_conflict_review_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.upazila_name}, {row.district_name}</em>
              </div>
              <div className="psdq-priority-name-conflict-class" style={{ background: color }}>
                {priorityNameConflictLabel(row.name_conflict_review_class)}
              </div>
              <div className="psdq-priority-name-conflict-links">
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS {row.dghs_profile_http_status}
                </a>
                <a href={row.candidate_osm_api_url} target="_blank" rel="noreferrer">
                  OSM API {row.candidate_osm_api_http_status}
                </a>
                <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                  Map feature
                </a>
              </div>
              <div className="psdq-priority-name-conflict-candidate">
                <span>Candidate</span>
                <strong>{row.candidate_osm_name_from_api || "Unnamed OSM feature"}</strong>
                <em>{row.candidate_osm_type} {row.candidate_osm_id}; {row.candidate_osm_tags_compact}</em>
              </div>
              <div className="psdq-priority-name-conflict-pair">
                <div>
                  <span>Name support</span>
                  <strong>{formatNumber(score, 2)}</strong>
                  <i aria-label="Name-score bar">
                    <b style={{ width: `${scoreWidth}%`, background: color }} />
                  </i>
                </div>
                <div>
                  <span>Distance</span>
                  <strong>{formatNumber(distance / 1000, 1)} km</strong>
                  <i aria-label="Distance bar">
                    <b style={{ width: `${distanceWidth}%`, background: "#002569" }} />
                  </i>
                </div>
              </div>
              <div className="psdq-priority-name-conflict-distance">
                {priorityNameConflictDistanceLabel(row.candidate_distance_band)}
              </div>
              <div className="psdq-priority-name-conflict-flags">
                <span>{asBoolean(row.candidate_contains_admin_place_name) ? "admin-place name" : "no admin-place name"}</span>
                <span>{asBoolean(row.public_alias_or_location_source_found_by_current_artifacts) ? "alias source found" : "0 alias source"}</span>
              </div>
              <p>{row.review_action}</p>
              <div className="psdq-priority-name-conflict-gates">
                <div>
                  <span>Reclassify only if</span>
                  <p>{row.minimum_evidence_to_reclassify_as_same_facility}</p>
                </div>
                <div>
                  <span>Keep as name conflict only if</span>
                  <p>{row.minimum_evidence_to_keep_as_name_conflict}</p>
                </div>
              </div>
              <div className="psdq-priority-name-conflict-status">
                <span>keep open</span>
                <span>0 closed</span>
                <span>0 reclassified</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the priority name-conflict review</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-priority-name-conflict-review.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-priority-name-conflict-review.md" download>
          Download priority name-conflict review note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-priority-name-conflict-review-summary.json" download>
          Download priority name-conflict summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-priority-name-conflict-review.csv" download>
          Download priority name-conflict CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function lowerPriorityNameConflictColor(code: string) {
  const colors: Record<string, string> = {
    repeated_candidate_pair_context_only: "#9B2226",
    single_candidate_10km_or_more_context_only: "#002569",
    partial_name_support_still_unresolved: "#007DB8",
    different_name_spot_check_still_unresolved: "#5A8227",
  };
  return colors[code] || "#6c757d";
}

function lowerPriorityNameConflictLabel(code: string) {
  const labels: Record<string, string> = {
    repeated_candidate_pair_context_only: "Repeated candidate, context only",
    single_candidate_10km_or_more_context_only: "Single candidate 10 km+",
    partial_name_support_still_unresolved: "Partial name support unresolved",
    different_name_spot_check_still_unresolved: "Different-name spot check unresolved",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function PsdqLowerPriorityNameConflictReviewPanel({ summary }: { summary: PsdqLowerPriorityNameConflictReviewSummary }) {
  const scope = summary.lower_priority_name_conflict_scope;
  const maxDistance = Math.max(
    1,
    ...summary.review_rows.map((row) => Number(row.candidate_distance_m_from_inspection || 0))
  );
  const maxClusterRows = Math.max(1, ...summary.candidate_clusters.map((row) => row.spot_check_rows));
  const minDistance = scope.min_candidate_distance_m;
  const maxDistanceScope = scope.max_candidate_distance_m;
  const minScore = scope.min_candidate_name_score;
  const maxScore = scope.max_candidate_name_score;

  return (
    <section className="showcase-section psdq-lower-name-conflict-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Lower-priority name-conflict spot check</p>
          <h2>Six backstop rows repeat the same warning: candidate retrieval is not row resolution.</h2>
          <p>
            The spot check looks beyond the high-exposure queue. Two public-map
            candidates each appear for two DGHS community-clinic rows, and every
            candidate remains at least 5 km from the inspection point.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows reviewed</span>
            <strong>{formatNumber(scope.lower_priority_name_conflict_rows)}</strong>
          </div>
          <div>
            <span>Candidate features</span>
            <strong>{formatNumber(scope.unique_candidate_features)}</strong>
          </div>
          <div>
            <span>Rows on reused candidates</span>
            <strong>{formatNumber(scope.rows_sharing_reused_candidate_features)} rows</strong>
          </div>
          <div>
            <span>Distance range</span>
            <strong>
              {formatNumber((minDistance ?? 0) / 1000, 1)}-{formatNumber((maxDistanceScope ?? 0) / 1000, 1)} km
            </strong>
          </div>
          <div>
            <span>Name score range</span>
            <strong>{formatNumber(minScore ?? 0, 2)}-{formatNumber(maxScore ?? 0, 2)}</strong>
          </div>
          <div>
            <span>5 km or more</span>
            <strong>{formatNumber(scope.rows_with_candidate_distance_5km_or_more)} rows</strong>
          </div>
          <div>
            <span>Alias/location sources</span>
            <strong>{formatNumber(scope.public_alias_or_location_sources_found_by_current_artifacts)}</strong>
          </div>
          <div>
            <span>Closure / reclass / map absence</span>
            <strong>
              {formatNumber(scope.rows_allowed_for_closure)} /{" "}
              {formatNumber(scope.rows_allowed_for_same_facility_reclassification)} /{" "}
              {formatNumber(scope.rows_allowed_for_map_absence_language)}
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-lower-name-conflict-clusters">
        {summary.candidate_clusters.map((cluster) => {
          const width = Math.max(8, Math.min(100, (cluster.spot_check_rows / maxClusterRows) * 100));
          return (
            <article key={cluster.candidate_cluster_id}>
              <div>
                <span>{cluster.candidate_cluster_id}</span>
                <strong>{cluster.candidate_osm_name_from_api || "Unnamed OSM feature"}</strong>
                <em>{cluster.upazilas}, {cluster.districts}</em>
              </div>
              <i aria-label={`${cluster.candidate_osm_name_from_api} reused-candidate row bar`}>
                <b style={{ width: `${width}%` }} />
              </i>
              <p>
                {formatNumber(cluster.spot_check_rows)} spot-check row{cluster.spot_check_rows === 1 ? "" : "s"};
                distance {formatNumber(cluster.min_candidate_distance_m / 1000, 1)}-{formatNumber(cluster.max_candidate_distance_m / 1000, 1)} km;
                name score {formatNumber(cluster.min_candidate_name_score, 2)}-{formatNumber(cluster.max_candidate_name_score, 2)}.
              </p>
              <p>{cluster.facility_names}</p>
              <a href={cluster.candidate_feature_url} target="_blank" rel="noreferrer">
                Map feature
              </a>
            </article>
          );
        })}
      </div>

      <div className="psdq-priority-name-conflict-grid psdq-lower-name-conflict-grid">
        {summary.review_rows.map((row) => {
          const color = lowerPriorityNameConflictColor(row.spot_check_review_class);
          const score = Number(row.candidate_name_score_from_live_tags || 0);
          const distance = Number(row.candidate_distance_m_from_inspection || 0);
          const scoreWidth = Math.max(4, Math.min(100, score * 100));
          const distanceWidth = Math.max(4, Math.min(100, (distance / maxDistance) * 100));
          return (
            <article key={row.lower_priority_name_conflict_review_id} style={{ borderColor: color }}>
              <div className="psdq-priority-name-conflict-card-head">
                <span>{row.lower_priority_name_conflict_review_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.upazila_name}, {row.district_name}</em>
              </div>
              <div className="psdq-priority-name-conflict-class" style={{ background: color }}>
                {lowerPriorityNameConflictLabel(row.spot_check_review_class)}
              </div>
              <div className="psdq-priority-name-conflict-links">
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS {row.dghs_profile_http_status}
                </a>
                <a href={row.candidate_osm_api_url} target="_blank" rel="noreferrer">
                  OSM API {row.candidate_osm_api_http_status}
                </a>
                <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                  Map feature
                </a>
              </div>
              <div className="psdq-priority-name-conflict-candidate">
                <span>Candidate</span>
                <strong>{row.candidate_osm_name_from_api || "Unnamed OSM feature"}</strong>
                <em>{row.candidate_osm_type} {row.candidate_osm_id}; {row.candidate_osm_tags_compact}</em>
              </div>
              <div className="psdq-priority-name-conflict-pair">
                <div>
                  <span>Name support</span>
                  <strong>{formatNumber(score, 2)}</strong>
                  <i aria-label="Name-score bar">
                    <b style={{ width: `${scoreWidth}%`, background: color }} />
                  </i>
                </div>
                <div>
                  <span>Distance</span>
                  <strong>{formatNumber(distance / 1000, 1)} km</strong>
                  <i aria-label="Distance bar">
                    <b style={{ width: `${distanceWidth}%`, background: "#002569" }} />
                  </i>
                </div>
              </div>
              <div className="psdq-priority-name-conflict-distance">
                {priorityNameConflictDistanceLabel(row.candidate_distance_band)}
              </div>
              <div className="psdq-priority-name-conflict-flags">
                <span>{asBoolean(row.candidate_reused_in_spot_check) ? `${formatNumber(Number(row.candidate_spot_check_cluster_rows || 0))} rows share candidate` : "single candidate"}</span>
                <span>{asBoolean(row.public_alias_or_location_source_found_by_current_artifacts) ? "alias source found" : "0 alias source"}</span>
              </div>
              <p>{row.review_action}</p>
              <div className="psdq-priority-name-conflict-gates">
                <div>
                  <span>Reclassify only if</span>
                  <p>{row.minimum_evidence_to_reclassify_as_same_facility}</p>
                </div>
                <div>
                  <span>Keep as name conflict only if</span>
                  <p>{row.minimum_evidence_to_keep_as_name_conflict}</p>
                </div>
              </div>
              <div className="psdq-priority-name-conflict-status">
                <span>spot check</span>
                <span>0 closed</span>
                <span>0 reclassified</span>
                <span>0 map absence uses</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the lower-priority name-conflict spot check</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-lower-priority-name-conflict-review.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-lower-priority-name-conflict-review.md" download>
          Download lower-priority name-conflict review note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json" download>
          Download lower-priority name-conflict summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv" download>
          Download lower-priority name-conflict CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function zeroOsmObservabilityColor(code: string) {
  const colors: Record<string, string> = {
    zero_osm_boundary_join_residue_review_first: "#6c757d",
    zero_osm_high_building_proxy: "#007DB8",
    zero_osm_high_registry_count: "#9B2226",
    zero_osm_observability_context: "#5A8227",
    zero_osm_missing_open_buildings_denominator: "#8A6A00",
  };
  return colors[code] || "#6c757d";
}

function zeroOsmObservabilityLabel(code: string) {
  const labels: Record<string, string> = {
    zero_osm_boundary_join_residue_review_first: "Boundary join first",
    zero_osm_high_building_proxy: "High building proxy",
    zero_osm_high_registry_count: "High registry count",
    zero_osm_observability_context: "Observability context",
    zero_osm_missing_open_buildings_denominator: "Missing denominator",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function PsdqZeroOsmObservabilityReviewPanel({ summary }: { summary: PsdqZeroOsmObservabilityReviewSummary }) {
  const scope = summary.zero_osm_observability_scope;
  const topRows = summary.top_zero_osm_upazila_rows.slice(0, 10);
  const targetedRows = summary.targeted_inspection_rows.slice(0, 8);
  const maxDivisionUpazilas = Math.max(1, ...summary.division_rows.map((row) => row.zero_osm_upazilas));
  const maxProxy = Math.max(
    1,
    ...topRows.map((row) => Number(row.underobserved_buildings_3km_p85_proxy || 0))
  );

  return (
    <section className="showcase-section psdq-zero-osm-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Zero-OSM upazila observability review</p>
          <h2>One hundred fifteen upazilas have registry rows, but zero joined OSM health features.</h2>
          <p>
            The review keeps the zero-OSM signal at the right level. It is a
            source-observability queue for upazilas, not proof that any
            specific DGHS facility is absent from the public map.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Zero-OSM upazilas</span>
            <strong>{formatNumber(scope.zero_osm_active_registry_upazilas)}</strong>
          </div>
          <div>
            <span>Active DGHS clinical rows</span>
            <strong>{formatNumber(scope.active_clinical_facilities_in_zero_osm_upazilas)}</strong>
          </div>
          <div>
            <span>Share of exposure rows</span>
            <strong>{pct(scope.share_of_exposure_rows_zero_osm, 1)}</strong>
          </div>
          <div>
            <span>Targeted queue</span>
            <strong>
              {formatNumber(scope.targeted_inspection_rows_in_zero_osm_lane)} rows /{" "}
              {formatNumber(scope.targeted_zero_osm_upazilas)} upazilas
            </strong>
          </div>
          <div>
            <span>Boundary matches</span>
            <strong>
              {formatNumber(scope.zero_osm_upazilas_with_osm_boundary_match)} /{" "}
              {formatNumber(scope.zero_osm_active_registry_upazilas)}
            </strong>
          </div>
          <div>
            <span>Closure / absence / corrections</span>
            <strong>
              {formatNumber(scope.facility_rows_allowed_for_closure)} /{" "}
              {formatNumber(scope.facility_rows_allowed_for_absence_language)} /{" "}
              {formatNumber(scope.coordinate_corrections_allowed)}
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-zero-osm-division-grid">
        {summary.division_rows.map((row) => {
          const width = Math.max(4, (row.zero_osm_upazilas / maxDivisionUpazilas) * 100);
          return (
            <article key={row.division_name}>
              <div>
                <strong>{row.division_name}</strong>
                <span>{formatNumber(row.zero_osm_upazilas)} upazilas</span>
              </div>
              <i aria-label={`${row.division_name} zero-OSM upazila bar`}>
                <b style={{ width: `${width}%` }} />
              </i>
              <p>
                {formatNumber(row.active_clinical_facilities)} active DGHS rows;{" "}
                {formatNumber(row.underobserved_buildings_3km_p85_proxy)} proxy buildings;{" "}
                {formatNumber(row.targeted_inspection_rows)} targeted rows.
              </p>
            </article>
          );
        })}
      </div>

      <div className="psdq-zero-osm-grid">
        {topRows.map((row) => {
          const color = zeroOsmObservabilityColor(row.zero_osm_observability_class);
          const proxy = Number(row.underobserved_buildings_3km_p85_proxy || 0);
          const proxyWidth = Math.max(4, Math.min(100, (proxy / maxProxy) * 100));
          return (
            <article key={row.zero_osm_observability_review_id} style={{ borderColor: color }}>
              <div className="psdq-zero-osm-card-head">
                <span>{row.zero_osm_observability_review_id}</span>
                <strong>{row.upazila_name}</strong>
                <em>{row.district_name}, {row.division_name}</em>
              </div>
              <div className="psdq-zero-osm-class" style={{ background: color }}>
                {zeroOsmObservabilityLabel(row.zero_osm_observability_class)}
              </div>
              <div className="psdq-zero-osm-meter">
                <div>
                  <span>DGHS clinical</span>
                  <strong>{formatNumber(Number(row.active_clinical_facilities || 0))}</strong>
                </div>
                <div>
                  <span>OSM health</span>
                  <strong>{formatNumber(Number(row.osm_health || 0))}</strong>
                </div>
                <div>
                  <span>Targeted rows</span>
                  <strong>{formatNumber(Number(row.targeted_inspection_rows_in_current_queue || 0))}</strong>
                </div>
              </div>
              <div className="psdq-zero-osm-proxy">
                <span>3 km p85 under-observed proxy</span>
                <strong>{formatNumber(proxy)}</strong>
                <i aria-label="Under-observed building proxy bar">
                  <b style={{ width: `${proxyWidth}%`, background: color }} />
                </i>
              </div>
              <div className="psdq-zero-osm-flags">
                <span>{asBoolean(row.has_open_buildings_denominator) ? "Open Buildings denominator" : "missing denominator"}</span>
                <span>{asBoolean(row.has_osm_boundary_match) ? "OSM boundary match" : "boundary join residue"}</span>
                <span>{asBoolean(row.upazila_observability_language_allowed) ? "upazila context allowed" : "context blocked"}</span>
              </div>
              <p>{row.review_action}</p>
              {row.targeted_inspection_facilities && (
                <div className="psdq-zero-osm-targeted">
                  <span>Inspection examples</span>
                  <p>{row.targeted_inspection_facilities}</p>
                </div>
              )}
              <div className="psdq-zero-osm-gates">
                <div>
                  <span>Close row only if</span>
                  <p>{row.minimum_evidence_to_close_facility_row}</p>
                </div>
                <div>
                  <span>Upgrade context only if</span>
                  <p>{row.minimum_evidence_to_upgrade_upazila_context}</p>
                </div>
              </div>
              <div className="psdq-zero-osm-status">
                <span>upazila context</span>
                <span>0 closed</span>
                <span>0 facility absence uses</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="psdq-zero-osm-targeted-strip">
        {targetedRows.map((row) => (
          <article key={row.inspection_id}>
            <span>{row.inspection_id}</span>
            <strong>{row.facility_name}</strong>
            <em>{row.upazila_name}, {row.district_name}</em>
            <p>
              Nearest public-map context: {row.nearest_national_feature_1_name || "none in compact record"}{" "}
              {row.nearest_national_feature_1_distance_m
                ? `at ${formatNumber(Number(row.nearest_national_feature_1_distance_m) / 1000, 1)} km`
                : ""}
            </p>
          </article>
        ))}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the zero-OSM upazila observability review</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-zero-osm-upazila-observability-review.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-zero-osm-upazila-observability-review.md" download>
          Download zero-OSM observability review note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json" download>
          Download zero-OSM observability summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review.csv" download>
          Download zero-OSM observability CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function humanGatedHandoffColor(code: string) {
  const colors: Record<string, string> = {
    source_repair_owner_clarification: "#9B2226",
    possible_same_facility_location_validation: "#007DB8",
    priority_name_conflict_alias_location_validation: "#002569",
    lower_priority_name_conflict_alias_location_validation: "#5A8227",
    zero_osm_facility_row_absence_validation: "#8A6A00",
  };
  return colors[code] || "#6c757d";
}

function PsdqHumanGatedHandoffPanel({ summary }: { summary: PsdqHumanGatedHandoffSummary }) {
  const scope = summary.handoff_scope;
  const maxGroupRows = Math.max(1, ...summary.handoff_group_counts.map((row) => row.rows));
  const topUpazilas = summary.upazila_handoff_rows.slice(0, 10);
  const maxUpazilaRows = Math.max(1, ...topUpazilas.map((row) => row.handoff_rows));
  const handoffRows = summary.top_handoff_rows.slice(0, 12);
  const distanceMin = scope.candidate_distance_min_m;
  const distanceMax = scope.candidate_distance_max_m;
  const nameScoreMin = scope.candidate_name_score_min;
  const nameScoreMax = scope.candidate_name_score_max;

  return (
    <section className="showcase-section psdq-human-gated-handoff-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Human-gated handoff matrix</p>
          <h2>The AI loop has reached the owner-or-human validation wall.</h2>
          <p>
            The handoff matrix consolidates the open source-repair, possible
            same-facility, name-conflict, and zero-OSM rows into one reviewer
            queue. It shows exactly what still needs source-owner
            clarification or human location validation before any stronger
            row language can be used.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Open handoff rows</span>
            <strong>{formatNumber(scope.handoff_rows)}</strong>
          </div>
          <div>
            <span>Human or owner action</span>
            <strong>{formatNumber(scope.human_or_owner_action_required_rows)} rows</strong>
          </div>
          <div>
            <span>Groups / upazilas</span>
            <strong>
              {formatNumber(scope.handoff_groups)} / {formatNumber(scope.upazilas_with_handoff_rows)}
            </strong>
          </div>
          <div>
            <span>Candidate distance range</span>
            <strong>
              {distanceMin == null || distanceMax == null
                ? "n/a"
                : `${formatNumber(distanceMin / 1000, 1)}-${formatNumber(distanceMax / 1000, 1)} km`}
            </strong>
          </div>
          <div>
            <span>Name score range</span>
            <strong>
              {nameScoreMin == null || nameScoreMax == null
                ? "n/a"
                : `${formatNumber(nameScoreMin, 2)}-${formatNumber(nameScoreMax, 2)}`}
            </strong>
          </div>
          <div>
            <span>External contacts</span>
            <strong>{formatNumber(scope.external_contacts_made)}</strong>
          </div>
          <div>
            <span>Closure / reclass / map absence</span>
            <strong>
              {formatNumber(scope.rows_allowed_for_closure)} /{" "}
              {formatNumber(scope.rows_allowed_for_same_facility_reclassification)} /{" "}
              {formatNumber(scope.rows_allowed_for_map_absence_language)}
            </strong>
          </div>
          <div>
            <span>Coordinate corrections</span>
            <strong>{formatNumber(scope.coordinate_corrections_allowed)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-human-gated-group-grid">
        {summary.handoff_group_counts.map((group) => {
          const color = humanGatedHandoffColor(group.name);
          const width = Math.max(8, (group.rows / maxGroupRows) * 100);
          return (
            <article key={group.name} style={{ borderColor: color }}>
              <span>{group.name.replaceAll("_", " ")}</span>
              <strong>{formatNumber(group.rows)} rows</strong>
              <p>{group.label}</p>
              <i aria-label={`${group.label} handoff row bar`}>
                <b style={{ width: `${width}%`, background: color }} />
              </i>
              <em>human gated; 0 closed</em>
            </article>
          );
        })}
      </div>

      <div className="psdq-human-gated-upazila-grid">
        {topUpazilas.map((row) => {
          const width = Math.max(8, (row.handoff_rows / maxUpazilaRows) * 100);
          return (
            <article key={`${row.district_name}-${row.upazila_name}`}>
              <div>
                <span>{row.district_name}</span>
                <strong>{row.upazila_name}</strong>
                <em>{formatNumber(row.handoff_rows)} handoff rows</em>
              </div>
              <i aria-label={`${row.upazila_name} handoff row concentration bar`}>
                <b style={{ width: `${width}%` }} />
              </i>
              <p>{row.handoff_groups}</p>
              <div className="psdq-human-gated-lane-chips">
                <span>source {formatNumber(row.source_repair_rows)}</span>
                <span>same {formatNumber(row.possible_same_facility_rows)}</span>
                <span>priority {formatNumber(row.priority_name_conflict_rows)}</span>
                <span>lower {formatNumber(row.lower_priority_name_conflict_rows)}</span>
                <span>zero-OSM {formatNumber(row.zero_osm_absence_gate_rows)}</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="psdq-human-gated-row-grid">
        {handoffRows.map((row) => {
          const color = humanGatedHandoffColor(row.handoff_group);
          const distance = Number(row.candidate_distance_m || 0);
          const score = Number(row.candidate_name_score || 0);
          return (
            <article key={row.handoff_id} style={{ borderColor: color }}>
              <div className="psdq-human-gated-card-head">
                <span>{row.handoff_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.upazila_name}, {row.district_name}</em>
              </div>
              <div className="psdq-human-gated-class" style={{ background: color }}>
                {row.handoff_group_label}
              </div>
              {row.candidate_name && (
                <div className="psdq-human-gated-candidate">
                  <span>Public-map candidate</span>
                  <strong>{row.candidate_name}</strong>
                  <em>
                    {distance ? `${formatNumber(distance / 1000, 1)} km` : "distance n/a"}
                    {score ? `; name score ${formatNumber(score, 2)}` : ""}
                  </em>
                  {row.candidate_feature_url && (
                    <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                      Map feature
                    </a>
                  )}
                </div>
              )}
              <div className="psdq-human-gated-blocker">
                <span>Blocker</span>
                <strong>{row.blocker_label}</strong>
              </div>
              <p>{row.review_question}</p>
              <div className="psdq-human-gated-evidence">
                <div>
                  <span>Required next evidence</span>
                  <p>{row.required_next_evidence}</p>
                </div>
                <div>
                  <span>Public basis so far</span>
                  <p>{row.public_evidence_basis}</p>
                </div>
              </div>
              <div className="psdq-human-gated-status">
                <span>{asBoolean(row.human_or_owner_action_required) ? "human gated" : "AI-only"}</span>
                <span>{asBoolean(row.external_contact_made) ? "contact made" : "0 contacts"}</span>
                <span>{formatNumber(Number(row.rows_closed_as_resolved || 0))} closed</span>
                <span>{formatNumber(Number(row.rows_reclassified_or_corrected || 0))} reclassified</span>
                <span>{asBoolean(row.map_absence_language_allowed_by_current_public_evidence) ? "map absence allowed" : "0 map absence uses"}</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the human-gated handoff matrix</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-human-gated-handoff.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-human-gated-handoff.md" download>
          Download human-gated handoff note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-human-gated-handoff-summary.json" download>
          Download human-gated summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-human-gated-handoff.csv" download>
          Download human-gated CSV
        </a>
        <a href="/programs/public-service-data-quality/facility-validation-human-validation-worksheet.md" download>
          Download human-validation worksheet note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-human-validation-worksheet-summary.json" download>
          Download worksheet summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-human-validation-worksheet.csv" download>
          Download worksheet CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function aiClosureWallColor(code: string) {
  const colors: Record<string, string> = {
    facility_level_absence_validation: "#8A6A00",
    public_alias_location_or_human_validation: "#002569",
    identity_and_location_validation: "#007DB8",
    source_owner_or_human_location_validation: "#9B2226",
  };
  return colors[code] || "#6c757d";
}

function aiClosureWallLabel(code: string) {
  const labels: Record<string, string> = {
    facility_level_absence_validation: "Facility-level absence validation",
    public_alias_location_or_human_validation: "Public alias/location or human validation",
    identity_and_location_validation: "Identity and location validation",
    source_owner_or_human_location_validation: "Source-owner or human location validation",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function aiClosureGateLabel(label: string) {
  return label
    .replace("AI ", "")
    .replace(" possible now", "")
    .replace(" without human or source owner now", "")
    .replace("same-facility", "same facility");
}

function PsdqAiClosureAuditPanel({ summary }: { summary: PsdqAiClosureAuditSummary }) {
  const scope = summary.audit_scope;
  const blockedGates = summary.decision_gate_counts.filter((gate) => gate.label !== "Keep-open only");
  const keepOpenGate = summary.decision_gate_counts.find((gate) => gate.label === "Keep-open only");
  const maxWallRows = Math.max(1, ...summary.wall_category_counts.map((row) => row.rows));
  const topUpazilas = summary.upazila_audit_rows.slice(0, 10);
  const maxUpazilaRows = Math.max(1, ...topUpazilas.map((row) => row.audit_rows));
  const auditRows = summary.top_audit_rows.slice(0, 12);

  return (
    <section className="showcase-section psdq-ai-closure-audit-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">AI closure audit</p>
          <h2>The current evidence permits keep-open language only.</h2>
          <p>
            The audit reads the human-validation worksheet and checks whether
            any row can be closed, reclassified, corrected, or used for
            map-absence language without source-owner or human-validation
            evidence. The result is a row-level stopping rule for the AI loop.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Rows audited</span>
            <strong>{formatNumber(scope.audit_rows)}</strong>
          </div>
          <div>
            <span>Human/source-owner wall</span>
            <strong>{formatNumber(scope.human_or_source_owner_wall_rows)} rows</strong>
          </div>
          <div>
            <span>AI-actionable now</span>
            <strong>{formatNumber(scope.ai_actionable_without_human_or_source_owner_rows)}</strong>
          </div>
          <div>
            <span>Keep-open only</span>
            <strong>{formatNumber(scope.keep_open_only_rows)} rows</strong>
          </div>
          <div>
            <span>Blank human statuses</span>
            <strong>{formatNumber(scope.blank_human_validation_status_rows)}</strong>
          </div>
          <div>
            <span>External contacts</span>
            <strong>{formatNumber(scope.external_contacts_made)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-ai-closure-gate-grid">
        {blockedGates.map((gate) => (
          <article key={gate.label}>
            <span>{aiClosureGateLabel(gate.label)}</span>
            <strong>{formatNumber(gate.rows)}</strong>
            <p>not allowed by current public evidence</p>
          </article>
        ))}
        {keepOpenGate && (
          <article className="psdq-ai-closure-keep-open">
            <span>{keepOpenGate.label}</span>
            <strong>{formatNumber(keepOpenGate.rows)}</strong>
            <p>current allowed language</p>
          </article>
        )}
      </div>

      <div className="psdq-ai-closure-wall-grid">
        {summary.wall_category_counts.map((wall) => {
          const width = Math.max(8, (wall.rows / maxWallRows) * 100);
          const color = aiClosureWallColor(wall.name);
          return (
            <article key={wall.name} style={{ borderColor: color }}>
              <span>{aiClosureWallLabel(wall.name)}</span>
              <strong>{formatNumber(wall.rows)} rows</strong>
              <i aria-label={`${aiClosureWallLabel(wall.name)} audit row bar`}>
                <b style={{ width: `${width}%`, background: color }} />
              </i>
              <p>requires source-owner, public official, or human-location evidence</p>
            </article>
          );
        })}
      </div>

      <div className="psdq-ai-closure-upazila-grid">
        {topUpazilas.map((row) => {
          const width = Math.max(8, (row.audit_rows / maxUpazilaRows) * 100);
          return (
            <article key={`${row.district_name}-${row.upazila_name}`}>
              <div>
                <span>{row.district_name}</span>
                <strong>{row.upazila_name}</strong>
                <em>{formatNumber(row.audit_rows)} audit rows</em>
              </div>
              <i aria-label={`${row.upazila_name} AI closure-audit row bar`}>
                <b style={{ width: `${width}%` }} />
              </i>
              <div className="psdq-ai-closure-chips">
                <span>source {formatNumber(row.source_repair_rows)}</span>
                <span>same {formatNumber(row.possible_same_facility_rows)}</span>
                <span>priority {formatNumber(row.priority_name_conflict_rows)}</span>
                <span>lower {formatNumber(row.lower_priority_name_conflict_rows)}</span>
                <span>zero-OSM {formatNumber(row.zero_osm_absence_gate_rows)}</span>
                <span>AI-actionable {formatNumber(row.ai_actionable_without_human_or_source_owner_rows)}</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="psdq-ai-closure-row-grid">
        {auditRows.map((row) => {
          const color = humanGatedHandoffColor(row.handoff_group);
          const distance = Number(row.candidate_distance_m || 0);
          const score = Number(row.candidate_name_score || 0);
          return (
            <article key={row.closure_audit_id} style={{ borderColor: color }}>
              <div className="psdq-ai-closure-card-head">
                <span>{row.closure_audit_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.upazila_name}, {row.district_name}</em>
              </div>
              <div className="psdq-human-gated-class" style={{ background: color }}>
                {row.handoff_group_label}
              </div>
              {row.candidate_name && (
                <div className="psdq-ai-closure-candidate">
                  <span>Candidate context</span>
                  <strong>{row.candidate_name}</strong>
                  <em>
                    {distance ? `${formatNumber(distance / 1000, 1)} km` : "distance n/a"}
                    {score ? `; name score ${formatNumber(score, 2)}` : ""}
                  </em>
                  {row.candidate_feature_url && (
                    <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                      Map feature
                    </a>
                  )}
                </div>
              )}
              <div className="psdq-ai-closure-blocker">
                <span>Audit wall</span>
                <strong>{aiClosureWallLabel(row.wall_category)}</strong>
                <p>{row.audit_rationale}</p>
              </div>
              <div className="psdq-ai-closure-gate">
                <span>Current public evidence gate</span>
                <p>{row.current_public_evidence_gate}</p>
              </div>
              <div className="psdq-ai-closure-status">
                <span>{row.ai_current_allowed_action.replaceAll("_", " ")}</span>
                <span>{row.audit_decision.replaceAll("_", " ")}</span>
                <span>0 AI closure</span>
              </div>
              <p>{row.allowed_language_now}</p>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the AI closure audit</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-ai-closure-audit.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-ai-closure-audit.md" download>
          Download AI closure-audit note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-ai-closure-audit-summary.json" download>
          Download AI closure-audit summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-ai-closure-audit.csv" download>
          Download AI closure-audit CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function sourceRepairEvidenceColor(code: string) {
  const colors: Record<string, string> = {
    shared_public_map_candidate_across_multiple_dghs_rows: "#002569",
    strong_name_but_long_coordinate_distance_conflict: "#007DB8",
    strong_name_but_extreme_coordinate_distance_conflict: "#9B2226",
    source_repair_public_evidence_attached: "#5A8227",
  };
  return colors[code] || "#6c757d";
}

function sourceRepairEvidenceLabel(code: string) {
  const labels: Record<string, string> = {
    shared_public_map_candidate_across_multiple_dghs_rows: "Shared public-map candidate",
    strong_name_but_long_coordinate_distance_conflict: "Long-distance source check",
    strong_name_but_extreme_coordinate_distance_conflict: "Extreme-distance source check",
    source_repair_public_evidence_attached: "Public evidence attached",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function officialCoordinateEvidenceColor(code: string) {
  if (code.includes("shared")) return "#007DB8";
  if (code.includes("extreme")) return "#A33A2A";
  if (code.includes("long")) return "#8A6A00";
  return "#5A8227";
}

function officialCoordinateEvidenceLabel(code: string) {
  const labels: Record<string, string> = {
    official_profile_coordinate_shared_by_multiple_dghs_rows: "Shared official coordinate",
    official_profile_coordinate_long_distance_from_named_osm_candidate: "Long-distance official coordinate",
    official_profile_coordinate_extreme_distance_from_named_osm_candidate: "Extreme-distance official coordinate",
    official_profile_coordinate_near_named_osm_candidate: "Nearby official coordinate",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function publicExplanationEvidenceColor(code: string) {
  if (code.includes("cross_district")) return "#A33A2A";
  if (code.includes("shared_coordinate")) return "#007DB8";
  if (code.includes("gov_portal")) return "#5A8227";
  return "#6c757d";
}

function publicExplanationEvidenceLabel(code: string) {
  const labels: Record<string, string> = {
    official_same_name_cross_district_coordinate_conflict_no_correction_record:
      "Same-name cross-district conflict",
    official_shared_coordinate_across_distinct_records_no_explanation:
      "Shared coordinate, no explanation",
    official_profile_and_gov_portal_no_coordinate_explanation:
      "Official pages, no coordinate note",
    official_profile_exposes_coordinate_no_public_explanation:
      "Official coordinate, no explanation",
    public_coordinate_source_or_correction_explanation_found:
      "Public explanation found",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function correctionRecordFollowupColor(code: string) {
  if (code.includes("cross_district")) return "#A33A2A";
  if (code.includes("shared_coordinate")) return "#007DB8";
  if (code.includes("correction_record_found")) return "#5A8227";
  return "#6c757d";
}

function correctionRecordFollowupLabel(code: string) {
  const labels: Record<string, string> = {
    no_correction_record_dashboard_confirms_cross_district_pair:
      "Dashboard confirms cross-district pair",
    no_correction_record_dashboard_confirms_distinct_shared_coordinate_records:
      "Dashboard confirms distinct shared-coordinate records",
    no_correction_record_found:
      "No public correction record",
    public_correction_record_found:
      "Public correction record found",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function clarificationPacketColor(code: string) {
  if (code.includes("cross_district")) return "#A33A2A";
  if (code.includes("shared_coordinate")) return "#007DB8";
  return "#6c757d";
}

function clarificationPacketLabel(code: string) {
  const labels: Record<string, string> = {
    source_owner_cross_district_coordinate_clarification:
      "Source-owner cross-district question",
    source_owner_shared_coordinate_clarification:
      "Source-owner shared-coordinate question",
    source_owner_unresolved_coordinate_clarification:
      "Unresolved coordinate question",
  };
  return labels[code] || code.replaceAll("_", " ");
}

function dghsProfileUrl(profileId: string) {
  return `https://hrm.dghs.gov.bd/public/facility-registry/facilities/${profileId}/profile?tab=at-a-glance`;
}

function dghsDashboardDetailUrl(code: string) {
  const urls: Record<string, string> = {
    "10000425": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000425&level=28&month=7&rank=61&year=2025",
    "10000427": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000427&level=28&month=5&rank=11&year=2025",
    "10002304": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10002304&level=29&month=5&rank=49&year=2025",
    "10000470": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000470&level=29&month=1&rank=&year=2025",
  };
  return urls[code] || `https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=${code}`;
}

function firstUrl(value: string) {
  return String(value || "").split(" | ").find(Boolean) || "";
}

function formatCoordinate(value: number | string) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed.toFixed(5) : String(value);
}

function asBoolean(value: boolean | string) {
  return value === true || String(value).toLowerCase() === "true";
}

function PsdqSourceRepairPublicEvidencePanel({ summary }: { summary: PsdqSourceRepairEvidenceSummary }) {
  const maxDistance = Math.max(
    1,
    ...summary.evidence_rows.map((row) => Number(row.candidate_distance_m_from_inspection || 0))
  );

  return (
    <section className="showcase-section psdq-source-repair-evidence-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Source-repair public evidence</p>
          <h2>Four rows now carry their public evidence before any outcome label.</h2>
          <p>
            The first source-repair pass attaches the DGHS profile and OSM API
            evidence already retrieved for the repair queue. It separates a
            shared-candidate collision from long-distance coordinate-source
            checks and keeps every row open.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Source-repair rows</span>
            <strong>{formatNumber(summary.source_repair_scope.source_repair_rows)}</strong>
          </div>
          <div>
            <span>Evidence attached</span>
            <strong>{formatNumber(summary.source_repair_scope.public_evidence_attached_rows)} rows</strong>
          </div>
          <div>
            <span>Shared candidate</span>
            <strong>{formatNumber(summary.source_repair_scope.rows_with_shared_public_map_candidate)} rows</strong>
          </div>
          <div>
            <span>10 km or more</span>
            <strong>{formatNumber(summary.source_repair_scope.rows_with_candidate_distance_10km_or_more)} rows</strong>
          </div>
          <div>
            <span>50 km or more</span>
            <strong>{formatNumber(summary.source_repair_scope.rows_with_candidate_distance_50km_or_more)} row</strong>
          </div>
          <div>
            <span>Rows closed</span>
            <strong>{formatNumber(summary.source_repair_scope.rows_closed_as_resolved)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-source-repair-evidence-grid">
        {summary.evidence_rows.map((row) => {
          const distance = Number(row.candidate_distance_m_from_inspection || 0);
          const score = Number(row.candidate_name_score_from_live_tags || 0);
          const distanceWidth = Math.max(2, Math.min(100, (distance / maxDistance) * 100));
          const color = sourceRepairEvidenceColor(row.source_repair_evidence_class);
          return (
            <article key={row.evidence_id} style={{ borderColor: color }}>
              <div className="psdq-source-repair-card-head">
                <span>{row.evidence_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.upazila_name}, {row.district_name}</em>
              </div>
              <div className="psdq-source-repair-class" style={{ background: color }}>
                {sourceRepairEvidenceLabel(row.source_repair_evidence_class)}
              </div>
              <div className="psdq-source-repair-links">
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS {row.dghs_profile_http_status}
                </a>
                <a href={row.candidate_osm_api_url} target="_blank" rel="noreferrer">
                  OSM API {row.candidate_osm_api_http_status}
                </a>
                <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                  Map feature
                </a>
              </div>
              <div className="psdq-source-repair-candidate">
                <span>Candidate</span>
                <strong>{row.candidate_osm_name_from_api}</strong>
                <em>{row.candidate_osm_tags_compact}</em>
              </div>
              <div className="psdq-source-repair-metrics">
                <span><b>{formatNumber(score, 2)}</b> name score</span>
                <span><b>{formatNumber(distance / 1000, 1)} km</b> candidate distance</span>
                <span><b>{formatNumber(Number(row.shared_public_map_candidate_rows || 0))}</b> shared-candidate rows</span>
              </div>
              <div className="psdq-source-repair-distance" aria-label="Candidate distance share of maximum distance">
                <i style={{ width: `${distanceWidth}%`, background: color }} />
              </div>
              <p>{row.source_repair_reviewer_question}</p>
              <div className="psdq-source-repair-status">
                <span>{asBoolean(row.public_evidence_attached) ? "Public evidence attached" : "Evidence attachment incomplete"}</span>
                <span>0 closed</span>
                <span>0 reclassified</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the source-repair evidence attachment</p>
        <code>python public-service-data-quality/scripts/attach-bgd-facility-source-repair-public-evidence.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-source-repair-public-evidence.md" download>
          Download source-repair evidence note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json" download>
          Download source-repair evidence summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv" download>
          Download source-repair evidence CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqOfficialCoordinateEvidencePanel({ summary }: { summary: PsdqOfficialCoordinateEvidenceSummary }) {
  const maxDistance = Math.max(
    1,
    ...summary.evidence_rows.map((row) => Number(row.dghs_profile_to_osm_candidate_distance_m || 0))
  );

  return (
    <section className="showcase-section psdq-official-coordinate-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Official coordinate evidence</p>
          <h2>The public DGHS pages expose the coordinates, but not the reason.</h2>
          <p>
            The next pass retrieves each DGHS profile page and parses the
            embedded official map coordinate. The coordinates match the
            inspection CSV, but the profiles do not expose an explicit
            coordinate-source explanation, so the four rows stay open.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Profiles retrieved</span>
            <strong>{formatNumber(summary.official_coordinate_scope.dghs_profiles_retrieved)} / {formatNumber(summary.official_coordinate_scope.source_repair_rows)}</strong>
          </div>
          <div>
            <span>Official coordinates exposed</span>
            <strong>{formatNumber(summary.official_coordinate_scope.official_profile_coordinates_exposed)}</strong>
          </div>
          <div>
            <span>Match inspection CSV</span>
            <strong>{formatNumber(summary.official_coordinate_scope.profile_coordinates_match_inspection_registry_coordinates)} rows</strong>
          </div>
          <div>
            <span>Shared official coordinate</span>
            <strong>{formatNumber(summary.official_coordinate_scope.rows_with_shared_official_profile_coordinate)} rows</strong>
          </div>
          <div>
            <span>Source explanations found</span>
            <strong>{formatNumber(summary.official_coordinate_scope.explicit_coordinate_source_explanations_found)}</strong>
          </div>
          <div>
            <span>Rows closed</span>
            <strong>{formatNumber(summary.official_coordinate_scope.rows_closed_as_resolved)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-official-coordinate-grid">
        {summary.evidence_rows.map((row) => {
          const distance = Number(row.dghs_profile_to_osm_candidate_distance_m || 0);
          const score = Number(row.candidate_name_score_from_live_tags || 0);
          const distanceWidth = Math.max(2, Math.min(100, (distance / maxDistance) * 100));
          const color = officialCoordinateEvidenceColor(row.official_coordinate_evidence_class);
          return (
            <article key={row.official_coordinate_evidence_id} style={{ borderColor: color }}>
              <div className="psdq-official-coordinate-card-head">
                <span>{row.official_coordinate_evidence_id}</span>
                <strong>{row.facility_name}</strong>
                <em>{row.dghs_profile_division_name} / {row.dghs_profile_district_name} / {row.dghs_profile_upazilla_name}</em>
              </div>
              <div className="psdq-official-coordinate-class" style={{ background: color }}>
                {officialCoordinateEvidenceLabel(row.official_coordinate_evidence_class)}
              </div>
              <div className="psdq-official-coordinate-links">
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS {row.dghs_profile_http_status}
                </a>
                <a href={row.dghs_profile_map_iframe_url} target="_blank" rel="noreferrer">
                  DGHS map
                </a>
                <a href={row.candidate_feature_url} target="_blank" rel="noreferrer">
                  OSM feature
                </a>
              </div>
              <div className="psdq-official-coordinate-route">
                <div className="psdq-official-coordinate-point">
                  <span>Official DGHS coordinate</span>
                  <strong>{formatCoordinate(row.dghs_profile_map_lat)}, {formatCoordinate(row.dghs_profile_map_lon)}</strong>
                  <em>{row.dghs_profile_organization_name}</em>
                </div>
                <div className="psdq-official-coordinate-rail" aria-label="Official-to-OSM coordinate distance share of maximum distance">
                  <i style={{ width: `${distanceWidth}%`, background: color }} />
                </div>
                <div className="psdq-official-coordinate-point">
                  <span>Pinned OSM candidate</span>
                  <strong>{formatCoordinate(row.candidate_osm_lat)}, {formatCoordinate(row.candidate_osm_lon)}</strong>
                  <em>{row.candidate_osm_name}</em>
                </div>
              </div>
              <div className="psdq-official-coordinate-metrics">
                <span><b>{formatNumber(distance / 1000, 1)} km</b> official-to-OSM gap</span>
                <span><b>{formatNumber(score, 2)}</b> name score</span>
                <span><b>{formatNumber(Number(row.shared_official_profile_coordinate_rows || 0))}</b> shared official-coordinate rows</span>
              </div>
              <p>{row.source_repair_reviewer_action}</p>
              <div className="psdq-official-coordinate-status">
                <span>{asBoolean(row.explicit_coordinate_source_explanation_found) ? "Explanation found" : "No source explanation field"}</span>
                <span>{asBoolean(row.dghs_profile_matches_inspection_registry_coordinate) ? "Matches inspection CSV" : "Differs from inspection CSV"}</span>
                <span>0 closed</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the official-coordinate evidence</p>
        <code>python public-service-data-quality/scripts/explain-bgd-facility-source-repair-official-coordinates.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-source-repair-official-coordinate-evidence.md" download>
          Download official-coordinate evidence note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json" download>
          Download official-coordinate summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv" download>
          Download official-coordinate CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqPublicExplanationEvidencePanel({ summary }: { summary: PsdqPublicExplanationEvidenceSummary }) {
  const maxConflictDistance = Math.max(
    1,
    ...summary.evidence_rows.map((row) => Number(row.nearest_same_name_other_district_coordinate_distance_m || 0))
  );

  return (
    <section className="showcase-section psdq-public-explanation-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Public explanation search</p>
          <h2>The official trail makes one row more suspicious, not more settled.</h2>
          <p>
            The next loop checks the live DGHS profile tabs, cached official
            registry records, and linked government health portals for public
            coordinate-source or correction notes. No explicit explanation is
            exposed. The strongest new clue is structural: the Netrakona
            Durgapur coordinate sits within one kilometer of a separate Rajshahi
            Durgapur official record.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Source-repair rows</span>
            <strong>{formatNumber(summary.public_explanation_scope.source_repair_rows)}</strong>
          </div>
          <div>
            <span>DGHS profile tabs checked</span>
            <strong>{formatNumber(summary.public_explanation_scope.live_dghs_profile_tabs_checked)}</strong>
          </div>
          <div>
            <span>Official portal pages retrieved</span>
            <strong>{formatNumber(summary.public_explanation_scope.official_gov_portal_pages_retrieved)}</strong>
          </div>
          <div>
            <span>Explicit explanations found</span>
            <strong>{formatNumber(summary.public_explanation_scope.explicit_coordinate_source_or_correction_explanations_found)}</strong>
          </div>
          <div>
            <span>Cross-district conflict rows</span>
            <strong>{formatNumber(summary.public_explanation_scope.rows_with_same_name_other_district_coordinate_within_2km)}</strong>
          </div>
          <div>
            <span>Rows closed</span>
            <strong>{formatNumber(summary.public_explanation_scope.rows_closed_as_resolved)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-public-explanation-grid">
        {summary.evidence_rows.map((row) => {
          const color = publicExplanationEvidenceColor(row.public_explanation_evidence_class);
          const conflictDistance = Number(row.nearest_same_name_other_district_coordinate_distance_m || 0);
          const conflictWidth = row.nearest_same_name_other_district_code
            ? Math.max(4, Math.min(100, (conflictDistance / maxConflictDistance) * 100))
            : Math.max(4, Math.min(100, (Number(row.shared_official_profile_coordinate_rows || 0) / 2) * 100));
          const portalUrl = firstUrl(row.official_gov_portal_urls_checked);
          return (
            <article key={row.public_explanation_evidence_id} style={{ borderColor: color }}>
              <div className="psdq-public-explanation-card-head">
                <span>{row.public_explanation_evidence_id}</span>
                <strong>{row.facility_name}</strong>
                <em>DGHS code {row.dghs_organization_code} / {row.division_name} / {row.district_name}</em>
              </div>
              <div className="psdq-public-explanation-class" style={{ background: color }}>
                {publicExplanationEvidenceLabel(row.public_explanation_evidence_class)}
              </div>
              <div className="psdq-public-explanation-links">
                <a href={row.dghs_public_profile_url} target="_blank" rel="noreferrer">
                  DGHS profile
                </a>
                {portalUrl && (
                  <a href={portalUrl} target="_blank" rel="noreferrer">
                    Official portal
                  </a>
                )}
                {row.nearest_same_name_other_district_profile_url && (
                  <a href={row.nearest_same_name_other_district_profile_url} target="_blank" rel="noreferrer">
                    Sibling record
                  </a>
                )}
              </div>
              <div className="psdq-public-explanation-route">
                <div className="psdq-public-explanation-node">
                  <span>Current official record</span>
                  <strong>{formatCoordinate(row.registry_lat)}, {formatCoordinate(row.registry_lon)}</strong>
                  <em>{row.registry_mailing_address || row.registry_village_or_street}</em>
                </div>
                <div className="psdq-public-explanation-rail" aria-label="Public explanation evidence intensity">
                  <i style={{ width: `${conflictWidth}%`, background: color }} />
                </div>
                <div className="psdq-public-explanation-node">
                  <span>{row.nearest_same_name_other_district_code ? "Nearest same-name official record" : "Public explanation result"}</span>
                  <strong>
                    {row.nearest_same_name_other_district_code
                      ? `${row.nearest_same_name_other_district_code} / ${formatNumber(conflictDistance)} m`
                      : `${formatNumber(Number(row.shared_official_profile_coordinate_rows || 0))} shared coordinate rows`}
                  </strong>
                  <em>
                    {row.nearest_same_name_other_district_code
                      ? `${row.nearest_same_name_other_district_district}, ${row.nearest_same_name_other_district_upazila}`
                      : "No public coordinate-source or correction explanation"}
                  </em>
                </div>
              </div>
              <div className="psdq-public-explanation-metrics">
                <span><b>{formatNumber(Number(row.source_pages_checked || 0))}</b> pages checked</span>
                <span><b>{formatNumber(Number(row.official_gov_portal_pages_retrieved || 0))}</b> portals retrieved</span>
                <span><b>{row.profile_last_updated_at || "not parsed"}</b> profile update</span>
              </div>
              <p>{row.public_explanation_reviewer_action}</p>
              <div className="psdq-public-explanation-status">
                <span>{asBoolean(row.explicit_coordinate_source_or_correction_explanation_found) ? "Explanation found" : "No explicit explanation"}</span>
                <span>{formatNumber(Number(row.same_name_dghs_registry_records || 0))} same-name official records</span>
                <span>0 closed</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the public-explanation search</p>
        <code>python public-service-data-quality/scripts/search-bgd-facility-source-repair-public-explanations.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-source-repair-public-explanation-evidence.md" download>
          Download public-explanation evidence note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json" download>
          Download public-explanation summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv" download>
          Download public-explanation CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqCorrectionRecordFollowupPanel({ summary }: { summary: PsdqCorrectionRecordFollowupSummary }) {
  const maxSources = Math.max(
    1,
    ...summary.evidence_rows.map((row) => Number(row.official_sources_retrieved || 0))
  );
  const maxDistance = Math.max(
    1,
    ...summary.evidence_rows.map((row) => Number(row.linked_other_district_coordinate_distance_m || 0))
  );

  return (
    <section className="showcase-section psdq-correction-followup-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Correction-record follow-up</p>
          <h2>The dashboard confirms the records, but still gives no correction trail.</h2>
          <p>
            The follow-up narrows the search to the unresolved Narayanganj
            shared-coordinate rows and the Durgapur same-name cross-district
            conflict. Public DGHS registry and Health Dashboard pages confirm
            the official codes, but the checked pages do not expose a public
            correction or coordinate-source record.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Targeted rows</span>
            <strong>{formatNumber(summary.correction_followup_scope.targeted_rows)}</strong>
          </div>
          <div>
            <span>Official sources retrieved</span>
            <strong>
              {formatNumber(summary.correction_followup_scope.official_sources_retrieved)} /{" "}
              {formatNumber(summary.correction_followup_scope.official_sources_checked)}
            </strong>
          </div>
          <div>
            <span>Correction records found</span>
            <strong>{formatNumber(summary.correction_followup_scope.public_correction_or_coordinate_source_records_found)}</strong>
          </div>
          <div>
            <span>Target codes confirmed</span>
            <strong>{formatNumber(summary.correction_followup_scope.rows_with_dashboard_target_code_confirmation)} rows</strong>
          </div>
          <div>
            <span>Linked code confirmed</span>
            <strong>{formatNumber(summary.correction_followup_scope.rows_with_dashboard_linked_other_district_code_confirmation)} row</strong>
          </div>
          <div>
            <span>Rows closed</span>
            <strong>{formatNumber(summary.correction_followup_scope.rows_closed_as_resolved)}</strong>
          </div>
        </div>
      </div>

      <div className="psdq-correction-followup-grid">
        {summary.evidence_rows.map((row) => {
          const color = correctionRecordFollowupColor(row.correction_followup_evidence_class);
          const linkedDistance = Number(row.linked_other_district_coordinate_distance_m || 0);
          const sourcesRetrieved = Number(row.official_sources_retrieved || 0);
          const signalWidth = linkedDistance > 0
            ? Math.max(6, Math.min(100, (linkedDistance / maxDistance) * 100))
            : Math.max(6, Math.min(100, (sourcesRetrieved / maxSources) * 100));
          const sourceStatuses = row.official_source_statuses.split(" | ").filter(Boolean).slice(0, 4);
          return (
            <article key={row.correction_followup_evidence_id} style={{ borderColor: color }}>
              <div className="psdq-correction-followup-card-head">
                <span>{row.correction_followup_evidence_id}</span>
                <strong>{row.facility_name}</strong>
                <em>DGHS code {row.dghs_organization_code} / {row.division_name} / {row.district_name}</em>
              </div>
              <div className="psdq-correction-followup-class" style={{ background: color }}>
                {correctionRecordFollowupLabel(row.correction_followup_evidence_class)}
              </div>
              <div className="psdq-correction-followup-links">
                <a href={dghsProfileUrl(row.dghs_profile_id)} target="_blank" rel="noreferrer">
                  DGHS profile
                </a>
                <a href={dghsDashboardDetailUrl(row.dghs_organization_code)} target="_blank" rel="noreferrer">
                  Dashboard code
                </a>
                {row.linked_other_district_code && (
                  <a href={dghsDashboardDetailUrl(row.linked_other_district_code)} target="_blank" rel="noreferrer">
                    Linked code
                  </a>
                )}
              </div>
              <div className="psdq-correction-followup-route">
                <div className="psdq-correction-followup-node">
                  <span>Target official code</span>
                  <strong>{row.dghs_organization_code}</strong>
                  <em>
                    {asBoolean(row.dashboard_menu_contains_target_code)
                      ? "Dashboard menu confirms target code"
                      : "Target code not confirmed in dashboard menu"}
                  </em>
                </div>
                <div className="psdq-correction-followup-rail" aria-label="Correction-record follow-up evidence intensity">
                  <i style={{ width: `${signalWidth}%`, background: color }} />
                </div>
                <div className="psdq-correction-followup-node">
                  <span>{row.linked_other_district_code ? "Linked official code" : "Correction-record result"}</span>
                  <strong>
                    {row.linked_other_district_code
                      ? `${row.linked_other_district_code} / ${formatNumber(linkedDistance)} m`
                      : "0 public records"}
                  </strong>
                  <em>
                    {row.linked_other_district_code
                      ? `${row.linked_other_district_district}, ${row.linked_other_district_upazila}`
                      : "No public correction or coordinate-source record"}
                  </em>
                </div>
              </div>
              <div className="psdq-correction-followup-metrics">
                <span><b>{formatNumber(Number(row.official_sources_checked || 0))}</b> sources checked</span>
                <span><b>{formatNumber(sourcesRetrieved)}</b> sources retrieved</span>
                <span><b>{asBoolean(row.public_correction_or_coordinate_source_record_found) ? "yes" : "no"}</b> correction found</span>
              </div>
              <p>{row.correction_followup_reviewer_action}</p>
              <div className="psdq-correction-followup-status">
                <span>{asBoolean(row.dashboard_menu_contains_target_code) ? "Target code confirmed" : "Target code not confirmed"}</span>
                <span>{row.linked_other_district_code ? "Linked code checked" : "Shared coordinate checked"}</span>
                <span>0 closed</span>
              </div>
              <div className="psdq-correction-followup-sources" aria-label="Official source retrieval statuses">
                {sourceStatuses.map((status) => (
                  <code key={`${row.correction_followup_evidence_id}-${status}`}>{status}</code>
                ))}
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the correction-record follow-up</p>
        <code>python public-service-data-quality/scripts/followup-bgd-facility-source-repair-correction-records.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-source-repair-correction-record-followup.md" download>
          Download correction-record follow-up note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json" download>
          Download correction-record summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv" download>
          Download correction-record CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqClarificationPacketPanel({ summary }: { summary: PsdqClarificationPacketSummary }) {
  const maxDistance = Math.max(
    1,
    ...summary.packet_rows.map((row) => Number(row.linked_other_district_coordinate_distance_m || 0))
  );

  return (
    <section className="showcase-section psdq-clarification-packet-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Clarification packet</p>
          <h2>The public record now becomes three exact source questions.</h2>
          <p>
            The packet turns the unresolved Narayanganj and Durgapur source
            repair rows into source-owner questions and human-review prompts.
            It records the public evidence basis, but it does not contact any
            source owner, validate a coordinate, close a row, or reclassify a
            facility pair.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Targeted rows</span>
            <strong>{formatNumber(summary.clarification_scope.targeted_rows)}</strong>
          </div>
          <div>
            <span>Source-owner questions</span>
            <strong>{formatNumber(summary.clarification_scope.rows_requiring_source_owner_clarification)}</strong>
          </div>
          <div>
            <span>Human review prompts</span>
            <strong>{formatNumber(summary.clarification_scope.rows_requiring_human_location_validation_if_no_source_owner_response)}</strong>
          </div>
          <div>
            <span>Correction records found</span>
            <strong>{formatNumber(summary.clarification_scope.public_correction_or_coordinate_source_records_found)}</strong>
          </div>
          <div>
            <span>External contacts made</span>
            <strong>{formatNumber(summary.clarification_scope.external_contacts_made)}</strong>
          </div>
          <div>
            <span>Closed / reclassified</span>
            <strong>
              {formatNumber(summary.clarification_scope.rows_closed_as_resolved)} /{" "}
              {formatNumber(summary.clarification_scope.rows_reclassified_as_same_facility)}
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-clarification-packet-grid">
        {summary.packet_rows.map((row) => {
          const color = clarificationPacketColor(row.clarification_issue_class);
          const linkedDistance = Number(row.linked_other_district_coordinate_distance_m || 0);
          const signalWidth = linkedDistance > 0
            ? Math.max(8, Math.min(100, (linkedDistance / maxDistance) * 100))
            : 62;
          const linkedCodes = row.linked_or_sibling_codes_csv.split(",").filter(Boolean);
          const linkedOrSibling = row.linked_other_district_code || linkedCodes[0] || "";
          const linkedUrl = row.dghs_dashboard_linked_detail_url || (linkedOrSibling ? dghsDashboardDetailUrl(linkedOrSibling) : "");
          const evidenceBits = row.public_evidence_basis.split("; ").filter(Boolean);
          return (
            <article key={row.clarification_packet_id} style={{ borderColor: color }}>
              <div className="psdq-clarification-packet-card-head">
                <span>{row.clarification_packet_id}</span>
                <strong>{row.facility_name}</strong>
                <em>DGHS code {row.dghs_organization_code} / {row.division_name} / {row.district_name}</em>
              </div>
              <div className="psdq-clarification-packet-class" style={{ background: color }}>
                {clarificationPacketLabel(row.clarification_issue_class)}
              </div>
              <div className="psdq-clarification-packet-links">
                <a href={row.dghs_profile_url} target="_blank" rel="noreferrer">
                  DGHS profile
                </a>
                <a href={row.dghs_dashboard_target_detail_url} target="_blank" rel="noreferrer">
                  Target dashboard
                </a>
                {linkedUrl && (
                  <a href={linkedUrl} target="_blank" rel="noreferrer">
                    Linked dashboard
                  </a>
                )}
              </div>
              <div className="psdq-clarification-packet-route">
                <div className="psdq-clarification-packet-node">
                  <span>Target official code</span>
                  <strong>{row.dghs_organization_code}</strong>
                  <em>{row.upazila_name}, {row.district_name}</em>
                </div>
                <div className="psdq-clarification-packet-rail" aria-label="Clarification packet evidence path">
                  <i style={{ width: `${signalWidth}%`, background: color }} />
                </div>
                <div className="psdq-clarification-packet-node">
                  <span>{row.linked_other_district_code ? "Linked official code" : "Sibling official code"}</span>
                  <strong>
                    {linkedDistance > 0
                      ? `${linkedOrSibling} / ${formatNumber(linkedDistance)} m`
                      : linkedOrSibling || "No linked code"}
                  </strong>
                  <em>
                    {row.linked_other_district_code
                      ? `${row.linked_other_district_district}, ${row.linked_other_district_upazila}`
                      : "Shared official-coordinate question"}
                  </em>
                </div>
              </div>
              <div className="psdq-clarification-packet-metrics">
                <span><b>{asBoolean(row.external_contact_made) ? "yes" : "no"}</b> external contact</span>
                <span><b>{asBoolean(row.owner_action_required_to_contact_source) ? "yes" : "no"}</b> owner action</span>
                <span><b>{formatNumber(Number(row.rows_closed_as_resolved || 0))}</b> rows closed</span>
              </div>
              <div className="psdq-clarification-packet-question">
                <span>Source-owner question</span>
                <p>{row.clarification_question}</p>
              </div>
              <div className="psdq-clarification-packet-question">
                <span>Human-review prompt</span>
                <p>{row.human_review_prompt}</p>
              </div>
              <div className="psdq-clarification-packet-status">
                <span>0 contacts</span>
                <span>0 closed</span>
                <span>0 reclassified</span>
              </div>
              <div className="psdq-clarification-packet-sources" aria-label="Clarification packet evidence basis">
                {evidenceBits.map((item) => (
                  <code key={`${row.clarification_packet_id}-${item}`}>{item}</code>
                ))}
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the clarification packet</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-source-repair-clarification-packet.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-source-repair-clarification-packet.md" download>
          Download clarification packet note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json" download>
          Download clarification packet summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv" download>
          Download clarification packet CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
  );
}

function PsdqRegistryVintageReviewPanel({ summary }: { summary: PsdqRegistryVintageReviewSummary }) {
  const maxAge = Math.max(
    1,
    ...summary.review_rows.map((row) => Number(row.profile_update_age_days_at_public_explanation_retrieval || 0))
  );
  const minAge = summary.registry_vintage_scope.min_profile_update_age_days_at_public_explanation_retrieval;
  const maxAgeScope = summary.registry_vintage_scope.max_profile_update_age_days_at_public_explanation_retrieval;

  return (
    <section className="showcase-section psdq-registry-vintage-section">
      <div className="showcase-two-col">
        <div>
          <p className="kicker">Registry-vintage review</p>
          <h2>Recent profile timestamps still do not close the coordinate question.</h2>
          <p>
            The review joins the clarification packet to public DGHS profile
            update timestamps and correction-record status. The unresolved rows
            look current enough to deserve review, but profile recency is not a
            coordinate-source record or human validation.
          </p>
        </div>
        <div className="showcase-fact-list">
          <div>
            <span>Targeted rows</span>
            <strong>{formatNumber(summary.registry_vintage_scope.targeted_rows)}</strong>
          </div>
          <div>
            <span>Profile timestamps</span>
            <strong>{formatNumber(summary.registry_vintage_scope.rows_with_profile_update_timestamp)}</strong>
          </div>
          <div>
            <span>14 days or less</span>
            <strong>{formatNumber(summary.registry_vintage_scope.rows_with_profile_update_age_14_days_or_less_at_public_explanation_retrieval)}</strong>
          </div>
          <div>
            <span>Age range at retrieval</span>
            <strong>{minAge ?? "n/a"}-{maxAgeScope ?? "n/a"} days</strong>
          </div>
          <div>
            <span>Correction records found</span>
            <strong>{formatNumber(summary.registry_vintage_scope.public_correction_or_coordinate_source_records_found)}</strong>
          </div>
          <div>
            <span>Closure / map absence allowed</span>
            <strong>
              {formatNumber(summary.registry_vintage_scope.rows_allowed_for_closure)} /{" "}
              {formatNumber(summary.registry_vintage_scope.rows_allowed_for_map_absence_language)}
            </strong>
          </div>
        </div>
      </div>

      <div className="psdq-registry-vintage-grid">
        {summary.review_rows.map((row) => {
          const color = clarificationPacketColor(row.clarification_issue_class);
          const age = Number(row.profile_update_age_days_at_public_explanation_retrieval || 0);
          const ageWidth = Math.max(8, Math.min(100, (age / maxAge) * 100));
          const linkedCodes = row.linked_or_sibling_codes_csv.split(",").filter(Boolean);
          const linkedOrSibling = row.linked_other_district_code || linkedCodes[0] || "";
          return (
            <article key={row.registry_vintage_review_id} style={{ borderColor: color }}>
              <div className="psdq-registry-vintage-card-head">
                <span>{row.registry_vintage_review_id}</span>
                <strong>{row.facility_name}</strong>
                <em>DGHS code {row.dghs_organization_code} / {row.division_name} / {row.district_name}</em>
              </div>
              <div className="psdq-registry-vintage-class" style={{ background: color }}>
                {row.clarification_issue_label}
              </div>
              <div className="psdq-registry-vintage-links">
                <a href={dghsProfileUrl(row.dghs_profile_id)} target="_blank" rel="noreferrer">
                  DGHS profile
                </a>
                <a href={dghsDashboardDetailUrl(row.dghs_organization_code)} target="_blank" rel="noreferrer">
                  Target dashboard
                </a>
                {linkedOrSibling && (
                  <a href={dghsDashboardDetailUrl(linkedOrSibling)} target="_blank" rel="noreferrer">
                    Linked dashboard
                  </a>
                )}
              </div>
              <div className="psdq-registry-vintage-route">
                <div className="psdq-registry-vintage-node">
                  <span>Profile last updated</span>
                  <strong>{row.profile_last_updated_at || "not parsed"}</strong>
                  <em>{formatNumber(age)} days old at public-explanation retrieval</em>
                </div>
                <div className="psdq-registry-vintage-rail" aria-label="Profile update age relative to oldest targeted row">
                  <i style={{ width: `${ageWidth}%`, background: color }} />
                </div>
                <div className="psdq-registry-vintage-node">
                  <span>{row.linked_other_district_code ? "Linked official code" : "Sibling official code"}</span>
                  <strong>
                    {row.linked_other_district_code && row.linked_other_district_coordinate_distance_m
                      ? `${linkedOrSibling} / ${formatNumber(Number(row.linked_other_district_coordinate_distance_m))} m`
                      : linkedOrSibling || "No linked code"}
                  </strong>
                  <em>
                    {row.linked_other_district_code
                      ? `${row.linked_other_district_district}, ${row.linked_other_district_upazila}`
                      : "Shared official-coordinate question"}
                  </em>
                </div>
              </div>
              <div className="psdq-registry-vintage-metrics">
                <span><b>{asBoolean(row.public_correction_or_coordinate_source_record_found) ? "yes" : "no"}</b> correction record</span>
                <span><b>{asBoolean(row.row_closure_allowed_by_current_public_evidence) ? "yes" : "no"}</b> closure allowed</span>
                <span><b>{asBoolean(row.map_absence_language_allowed_by_current_public_evidence) ? "yes" : "no"}</b> map absence allowed</span>
              </div>
              <p>{row.registry_vintage_review_action}</p>
              <div className="psdq-registry-vintage-gates">
                <div>
                  <span>Minimum evidence to close</span>
                  <p>{row.minimum_evidence_to_close}</p>
                </div>
                <div>
                  <span>Minimum evidence to reclassify</span>
                  <p>{row.minimum_evidence_to_reclassify}</p>
                </div>
                <div>
                  <span>Map-absence gate</span>
                  <p>{row.map_absence_language_gate}</p>
                </div>
              </div>
              <div className="psdq-registry-vintage-status">
                <span>timestamp is context</span>
                <span>0 closed</span>
                <span>0 map-absence uses</span>
              </div>
            </article>
          );
        })}
      </div>

      <div className="showcase-source-box psdq-sample-downloads">
        <p className="showcase-source-title">Download the registry-vintage review</p>
        <code>python public-service-data-quality/scripts/build-bgd-facility-source-repair-registry-vintage-review.py</code>
        <a href="/programs/public-service-data-quality/facility-validation-source-repair-registry-vintage-review.md" download>
          Download registry-vintage review note
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json" download>
          Download registry-vintage summary JSON
        </a>
        <a href="/programs/public-service-data-quality/generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv" download>
          Download registry-vintage CSV
        </a>
        <p className="psdq-method-note">
          Selection rule: {summary.selection_rule}
        </p>
        <p className="psdq-method-note">
          Non-claim: {summary.non_claim}
        </p>
      </div>
    </section>
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
        Unit: DGHS registry upazila row; source: generated PSDQ strata JSON
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
