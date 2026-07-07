#!/usr/bin/env python
"""Build the PSDQ evidence ledger for the showcase page.

This is a no-network derivative artifact. It reads committed PSDQ Bangladesh
summary JSON files and collapses the accumulated source-disagreement,
validation, repair, and human-gated artifacts into one reader-facing ledger.
The ledger is a presentation/navigation artifact, not a new validation result.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"

OUT_JSON = GENERATED_DIR / "psdq-evidence-ledger.json"
OUT_CSV = GENERATED_DIR / "psdq-evidence-ledger.csv"
STANDARD_JSON = GENERATED_DIR / "evidence-ledger.json"
STANDARD_CSV = GENERATED_DIR / "evidence-ledger.csv"

METHOD = "psdq_evidence_ledger_v1"
STATUS = "computed_psdq_evidence_ledger"
ATTESTATION = "ai-first"
PROGRAM = "public-service-data-quality"

NON_CLAIM = (
    "This is an AI-first evidence ledger for the PSDQ Bangladesh "
    "source-disagreement showcase. It summarizes committed public-data "
    "artifacts so a reader can follow the evidence chain. It is not human "
    "validation, not source-owner outreach, not ground truth, not a row "
    "closure, not a same-facility reclassification, not a coordinate "
    "correction, not a facility-quality assessment, and not a service-access "
    "estimate."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def n(value: Any) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def f(value: Any) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return 0.0


def get(data: dict[str, Any], *path: str) -> Any:
    current: Any = data
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def fmt(value: Any) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.1f}"
    return f"{n(value):,}"


def rel(path: str) -> str:
    return path.replace("\\", "/")


def first_scope(data: dict[str, Any], *scope_names: str) -> dict[str, Any]:
    for name in scope_names:
        value = data.get(name)
        if isinstance(value, dict):
            return value
    return {}


def count_from(data: dict[str, Any], paths: list[tuple[str, ...]]) -> int:
    for path in paths:
        value = get(data, *path)
        if value is not None:
            return n(value)
    return 0


def source_count(data: dict[str, Any]) -> int:
    inputs = data.get("source_inputs")
    if isinstance(inputs, list):
        return len(inputs)
    if data.get("source_input"):
        return 1
    return 0


def standard_non_claim(data: dict[str, Any]) -> str:
    value = data.get("non_claim")
    return str(value) if value else NON_CLAIM


def exposure_finding(data: dict[str, Any]) -> str:
    exposure = get(data, "exposure") or {}
    return (
        f"Bangladesh has {fmt(exposure.get('registry_admin_rows'))} DGHS registry "
        f"upazila rows, {fmt(exposure.get('active_clinical_facilities'))} active "
        f"clinical facilities, and {fmt(exposure.get('osm_health_joined'))} joined "
        f"OSM health features; the registry-minus-OSM clinical gap is "
        f"{fmt(exposure.get('registry_minus_osm_clinical'))}."
    )


def strata_finding(data: dict[str, Any]) -> str:
    coverage = get(data, "coverage") or {}
    strata = get(data, "validation_strata") or {}
    return (
        f"The L3 strata keep {fmt(strata.get('rows_with_zero_osm_health_features'))} "
        f"of {fmt(coverage.get('registry_admin_rows'))} upazila rows with active "
        f"registry facilities and zero joined OSM health features, while "
        f"{fmt(strata.get('rows_where_osm_equals_or_exceeds_registry'))} rows have "
        "OSM equal to or above the registry count."
    )


def sample_finding(data: dict[str, Any]) -> str:
    scope = get(data, "sample_summary") or {}
    return (
        f"The validation design selects {fmt(scope.get('sampled_upazilas'))} "
        f"upazilas and {fmt(scope.get('sampled_facility_rows'))} DGHS facility "
        f"rows; {fmt(scope.get('coordinate_ready_facility_rows'))} rows are "
        "coordinate-ready before any validation claim."
    )


def coded_finding(data: dict[str, Any]) -> str:
    scope = get(data, "screen_summary") or {}
    return (
        f"The automated screen codes {fmt(scope.get('coded_rows'))} facility rows, "
        f"recommends manual review for {fmt(scope.get('manual_review_recommended_rows'))}, "
        f"finds {fmt(scope.get('rows_with_any_osm_candidate_500m'))} rows with any "
        f"OSM candidate within 500 m, and flags {fmt(get(data, 'overpass_status_counts', 'skipped_coordinate_issue'))} "
        "coordinate-issue rows."
    )


def ai_review_finding(data: dict[str, Any]) -> str:
    scope = get(data, "review_scope") or {}
    return (
        f"The AI public-source review reads {fmt(scope.get('flagged_rows_reviewed'))} "
        f"flagged rows, sends {fmt(scope.get('candidate_resolution_rows'))} to "
        f"candidate resolution, records {fmt(scope.get('rows_with_no_osm_health_candidate_500m'))} "
        f"rows with no 500 m OSM health candidate, and keeps "
        f"{fmt(scope.get('coordinate_source_issue_rows'))} coordinate-source rows open."
    )


def candidate_resolution_finding(data: dict[str, Any]) -> str:
    scope = get(data, "resolution_scope") or {}
    return (
        f"The candidate-resolution pass reviews {fmt(scope.get('candidate_resolution_rows_reviewed'))} "
        f"rows, closes {fmt(scope.get('rows_closed_as_confirmed_same_facility'))}, "
        f"and retains {fmt(scope.get('rows_retained_open'))} open for stronger public or human evidence."
    )


def candidate_source_check_finding(data: dict[str, Any]) -> str:
    scope = get(data, "confirmation_scope") or {}
    return (
        f"The candidate public-source check reviews {fmt(scope.get('candidate_rows_checked'))} "
        f"rows; {fmt(scope.get('rows_with_specific_osm_name_tag_support'))} have "
        f"specific OSM name-tag support, but {fmt(scope.get('rows_closed_as_confirmed_same_facility'))} "
        "are closed as confirmed same-facility rows."
    )


def coordinate_repair_finding(data: dict[str, Any]) -> str:
    scope = get(data, "repair_scope") or {}
    return (
        f"The coordinate-repair triage checks {fmt(scope.get('coordinate_repair_rows_checked'))} "
        f"rows, finds {fmt(scope.get('valid_coordinates_outside_expected_upazila'))} "
        f"valid coordinates outside the expected upazila, and closes "
        f"{fmt(scope.get('rows_closed_as_coordinate_repaired'))} as repaired."
    )


def public_map_gap_finding(data: dict[str, Any]) -> str:
    scope = get(data, "public_map_gap_scope") or {}
    return (
        f"The public-map-gap triage checks {fmt(scope.get('public_map_gap_rows_checked'))} "
        f"rows, including {fmt(scope.get('priority_1_high_exposure_rows'))} high-exposure "
        f"rows; {fmt(scope.get('rows_with_nearest_any_osm_health_beyond_3km'))} have the "
        "nearest OSM health feature beyond 3 km, and 0 are closed."
    )


def row_evidence_finding(data: dict[str, Any]) -> str:
    scope = get(data, "row_evidence_scope") or {}
    return (
        f"The row-evidence ledger attaches public profile and map links to "
        f"{fmt(scope.get('rows_with_row_evidence'))} rows, keeps "
        f"{fmt(scope.get('rows_kept_open'))} open, and closes "
        f"{fmt(scope.get('rows_closed_as_resolved'))}."
    )


def inspection_finding(data: dict[str, Any]) -> str:
    scope = get(data, "inspection_scope") or {}
    return (
        f"The targeted public-map inspection checks {fmt(scope.get('rows_inspected'))} "
        f"rows; all {fmt(scope.get('rows_with_candidate_public_map_feature'))} have a "
        f"candidate public-map feature, but {fmt(scope.get('rows_closed_as_resolved'))} "
        "are closed or reclassified."
    )


def confirmation_finding(data: dict[str, Any]) -> str:
    scope = get(data, "confirmation_scope") or {}
    return (
        f"The public-source confirmation packet checks {fmt(scope.get('rows_checked'))} "
        f"rows, retrieves {fmt(scope.get('dghs_profiles_retrieved'))} DGHS profiles and "
        f"{fmt(scope.get('osm_candidate_api_records_retrieved'))} OSM API records, "
        f"and closes {fmt(scope.get('rows_closed_as_resolved'))}."
    )


def decision_ledger_finding(data: dict[str, Any]) -> str:
    scope = get(data, "decision_scope") or {}
    return (
        f"The public-source decision ledger narrows {fmt(scope.get('targeted_confirmation_rows'))} "
        f"targeted rows to {fmt(scope.get('decision_ledger_rows'))} reviewer rows: "
        f"{fmt(scope.get('source_repair_rows'))} source-repair, "
        f"{fmt(scope.get('possible_same_facility_rows'))} possible same-facility, and "
        f"{fmt(scope.get('high_exposure_name_conflict_rows'))} high-exposure name-conflict rows."
    )


def possible_same_finding(data: dict[str, Any]) -> str:
    scope = get(data, "possible_same_facility_scope") or {}
    return (
        f"The possible same-facility review checks {fmt(scope.get('possible_same_facility_rows'))} "
        f"rows and allows {fmt(scope.get('rows_allowed_for_same_facility_reclassification'))} "
        "same-facility reclassifications under current public evidence."
    )


def priority_name_conflict_finding(data: dict[str, Any]) -> str:
    scope = get(data, "priority_name_conflict_scope") or {}
    return (
        f"The priority name-conflict review checks {fmt(scope.get('priority_name_conflict_rows'))} "
        f"rows; current artifacts find {fmt(scope.get('public_alias_or_location_sources_found_by_current_artifacts'))} "
        "public alias/location sources and allow 0 closures."
    )


def lower_priority_name_conflict_finding(data: dict[str, Any]) -> str:
    scope = get(data, "lower_priority_name_conflict_scope") or {}
    return (
        f"The lower-priority name-conflict spot check reviews {fmt(scope.get('lower_priority_name_conflict_rows'))} "
        f"rows, including {fmt(scope.get('rows_sharing_reused_candidate_features'))} rows sharing reused "
        "candidate features, and allows 0 closures."
    )


def zero_osm_finding(data: dict[str, Any]) -> str:
    scope = get(data, "zero_osm_observability_scope") or {}
    return (
        f"The zero-OSM observability review identifies {fmt(scope.get('zero_osm_active_registry_upazilas'))} "
        f"upazilas with active registry facilities and zero joined OSM health features, "
        f"covering {fmt(scope.get('active_clinical_facilities_in_zero_osm_upazilas'))} active clinical facilities."
    )


def source_repair_public_finding(data: dict[str, Any]) -> str:
    scope = get(data, "source_repair_scope") or {}
    return (
        f"The source-repair evidence attachment covers {fmt(scope.get('source_repair_rows'))} rows, "
        f"attaches public evidence to {fmt(scope.get('public_evidence_attached_rows'))}, "
        f"and closes {fmt(scope.get('rows_closed_as_resolved'))}."
    )


def official_coordinate_finding(data: dict[str, Any]) -> str:
    scope = get(data, "official_coordinate_scope") or {}
    return (
        f"The official-coordinate pass exposes profile coordinates for {fmt(scope.get('official_profile_coordinates_exposed'))} "
        f"rows, finds {fmt(scope.get('explicit_coordinate_source_explanations_found'))} explicit coordinate-source "
        "explanations, and closes 0 rows."
    )


def public_explanation_finding(data: dict[str, Any]) -> str:
    scope = get(data, "public_explanation_scope") or {}
    return (
        f"The public-explanation search checks {fmt(scope.get('official_gov_portal_urls_checked'))} "
        f"official portal URLs, retrieves {fmt(scope.get('official_gov_portal_pages_retrieved'))} pages, "
        f"and finds {fmt(scope.get('explicit_coordinate_source_or_correction_explanations_found'))} explicit correction explanations."
    )


def correction_followup_finding(data: dict[str, Any]) -> str:
    scope = get(data, "correction_followup_scope") or {}
    return (
        f"The correction-record follow-up checks {fmt(scope.get('official_sources_checked'))} official sources "
        f"for {fmt(scope.get('targeted_rows'))} rows and finds "
        f"{fmt(scope.get('public_correction_or_coordinate_source_records_found'))} public correction records."
    )


def clarification_finding(data: dict[str, Any]) -> str:
    scope = get(data, "clarification_scope") or {}
    return (
        f"The clarification packet leaves {fmt(scope.get('targeted_rows'))} rows requiring source-owner "
        f"clarification and {fmt(scope.get('rows_requiring_human_location_validation_if_no_source_owner_response'))} "
        "requiring human location validation if no source-owner response exists."
    )


def registry_vintage_finding(data: dict[str, Any]) -> str:
    scope = get(data, "registry_vintage_scope") or {}
    return (
        f"The registry-vintage review finds profile update timestamps for {fmt(scope.get('rows_with_profile_update_timestamp'))} "
        f"rows, but {fmt(scope.get('public_correction_or_coordinate_source_records_found'))} public correction or "
        "coordinate-source records."
    )


def handoff_finding(data: dict[str, Any]) -> str:
    scope = get(data, "handoff_scope") or {}
    return (
        f"The human-gated handoff consolidates {fmt(scope.get('handoff_rows'))} open rows across "
        f"{fmt(scope.get('handoff_groups'))} groups; {fmt(scope.get('human_or_owner_action_required_rows'))} "
        "require human or source-owner action and 0 are allowed for closure."
    )


def worksheet_finding(data: dict[str, Any]) -> str:
    scope = get(data, "worksheet_scope") or {}
    return (
        f"The worksheet pre-fills {fmt(scope.get('worksheet_rows'))} review rows and leaves "
        f"{fmt(scope.get('blank_human_validation_status_rows'))} human-validation statuses blank by design."
    )


def closure_audit_finding(data: dict[str, Any]) -> str:
    scope = get(data, "audit_scope") or {}
    return (
        f"The AI closure audit checks {fmt(scope.get('audit_rows'))} unresolved rows and records "
        f"{fmt(scope.get('human_or_source_owner_wall_rows'))} human/source-owner wall rows, "
        f"{fmt(scope.get('ai_actionable_without_human_or_source_owner_rows'))} AI-actionable rows, and "
        f"{fmt(scope.get('keep_open_only_rows'))} keep-open-only rows."
    )


def evidence_ladder_finding(data: dict[str, Any]) -> str:
    scope = get(data, "ladder_scope") or {}
    terminal = get(data, "terminal_gate") or {}
    return (
        f"The evidence ladder indexes {fmt(scope.get('stages'))} stages and ends at "
        f"{fmt(terminal.get('human_or_source_owner_wall_rows'))} human/source-owner wall rows with "
        f"{fmt(terminal.get('ai_actionable_rows'))} AI-actionable rows."
    )


FindingFn = Callable[[dict[str, Any]], str]


SPECS: list[dict[str, Any]] = [
    {
        "id": "exposure-ranked-disagreement",
        "group": "source disagreement",
        "title": "Exposure-ranked registry-map disagreement",
        "summary": "generated/psdq-bgd-exposure-ranked-disagreement-summary.json",
        "csv": "generated/psdq-bgd-exposure-ranked-disagreement.csv",
        "artifact": "source-disagreement-l3-module.md",
        "count_paths": [("exposure", "registry_admin_rows")],
        "finding": exposure_finding,
        "reader_use": "Shows why the Bangladesh source-disagreement queue exists before any access-map claim.",
    },
    {
        "id": "source-disagreement-strata",
        "group": "source disagreement",
        "title": "Formal L3 source-disagreement strata",
        "summary": "generated/psdq-bgd-source-disagreement-strata.json",
        "csv": "generated/psdq-bgd-source-disagreement-strata.csv",
        "artifact": "source-disagreement-l3-module.md",
        "count_paths": [("coverage", "registry_admin_rows")],
        "finding": strata_finding,
        "reader_use": "Separates registry-map disagreement into validation strata and claim boundaries.",
    },
    {
        "id": "facility-validation-sample",
        "group": "facility validation",
        "title": "Facility-validation sample design",
        "summary": "generated/psdq-bgd-facility-validation-sample.json",
        "csv": "generated/psdq-bgd-facility-validation-sample-facilities.csv",
        "artifact": "facility-validation-sample.md",
        "count_paths": [("sample_summary", "sampled_facility_rows")],
        "finding": sample_finding,
        "reader_use": "Defines the row sample without treating sample selection as validation.",
    },
    {
        "id": "coded-screen",
        "group": "facility validation",
        "title": "Automated public-source coded screen",
        "summary": "generated/psdq-bgd-facility-validation-coded-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-coded-screen.csv",
        "artifact": "facility-validation-coded-screen.md",
        "count_paths": [("screen_summary", "coded_rows")],
        "finding": coded_finding,
        "reader_use": "Turns sampled facility rows into a public-source review queue.",
    },
    {
        "id": "ai-public-source-review",
        "group": "facility validation",
        "title": "AI public-source review ledger",
        "summary": "generated/psdq-bgd-facility-validation-ai-review-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-ai-review.csv",
        "artifact": "facility-validation-ai-review.md",
        "count_paths": [("review_scope", "flagged_rows_reviewed")],
        "finding": ai_review_finding,
        "reader_use": "Names the workstreams produced by the coded screen.",
    },
    {
        "id": "candidate-resolution",
        "group": "candidate review",
        "title": "Candidate-resolution pass",
        "summary": "generated/psdq-bgd-facility-validation-candidate-resolution-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-candidate-resolution.csv",
        "artifact": "facility-validation-candidate-resolution.md",
        "count_paths": [("resolution_scope", "candidate_resolution_rows_reviewed")],
        "finding": candidate_resolution_finding,
        "reader_use": "Checks whether nearby public-map candidates can close rows without human validation.",
    },
    {
        "id": "candidate-public-source-check",
        "group": "candidate review",
        "title": "Candidate public-source tag check",
        "summary": "generated/psdq-bgd-facility-validation-candidate-public-source-check-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-candidate-public-source-check.csv",
        "artifact": "facility-validation-candidate-public-source-check.md",
        "count_paths": [("confirmation_scope", "candidate_rows_checked")],
        "finding": candidate_source_check_finding,
        "reader_use": "Adds tag evidence while keeping rows open unless evidence is strong enough.",
    },
    {
        "id": "coordinate-repair",
        "group": "source repair",
        "title": "Coordinate-repair triage",
        "summary": "generated/psdq-bgd-facility-validation-coordinate-repair-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-coordinate-repair.csv",
        "artifact": "facility-validation-coordinate-repair.md",
        "count_paths": [("repair_scope", "coordinate_repair_rows_checked")],
        "finding": coordinate_repair_finding,
        "reader_use": "Shows why public registry coordinates need source-owner or human confirmation.",
    },
    {
        "id": "public-map-gap",
        "group": "public-map gap",
        "title": "Public-map-gap triage",
        "summary": "generated/psdq-bgd-facility-validation-public-map-gap-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-public-map-gap.csv",
        "artifact": "facility-validation-public-map-gap.md",
        "count_paths": [("public_map_gap_scope", "public_map_gap_rows_checked")],
        "finding": public_map_gap_finding,
        "reader_use": "Separates map-absence context from row-level closure evidence.",
    },
    {
        "id": "row-evidence-ledger",
        "group": "public-map gap",
        "title": "Row-level public-source evidence ledger",
        "summary": "generated/psdq-bgd-facility-validation-public-map-gap-evidence-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-public-map-gap-evidence.csv",
        "artifact": "facility-validation-public-map-gap-evidence.md",
        "count_paths": [("row_evidence_scope", "rows_with_row_evidence")],
        "finding": row_evidence_finding,
        "reader_use": "Converts row-level inspection evidence into links and status notes.",
    },
    {
        "id": "targeted-public-map-inspection",
        "group": "public-map gap",
        "title": "Targeted public-map inspection",
        "summary": "generated/psdq-bgd-facility-validation-public-map-inspection-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-public-map-inspection.csv",
        "artifact": "facility-validation-public-map-inspection.md",
        "count_paths": [("inspection_scope", "rows_inspected")],
        "finding": inspection_finding,
        "reader_use": "Shows what the public map can and cannot resolve for selected rows.",
    },
    {
        "id": "first-public-source-confirmation",
        "group": "public-source confirmation",
        "title": "First-row public-source confirmation",
        "summary": "generated/psdq-bgd-facility-validation-public-source-confirmation-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-public-source-confirmation.csv",
        "artifact": "facility-validation-public-source-confirmation.md",
        "count_paths": [("confirmation_scope", "rows_checked")],
        "finding": confirmation_finding,
        "reader_use": "Tests the public-source confirmation route before scaling to all targeted rows.",
    },
    {
        "id": "targeted-public-source-confirmation",
        "group": "public-source confirmation",
        "title": "Targeted public-source confirmation",
        "summary": "generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv",
        "artifact": "facility-validation-public-source-confirmation-targeted-rows.md",
        "count_paths": [("confirmation_scope", "rows_checked")],
        "finding": confirmation_finding,
        "reader_use": "Scales public DGHS profile and OSM API retrieval to the targeted row set.",
    },
    {
        "id": "public-source-decision-ledger",
        "group": "public-source confirmation",
        "title": "Public-source decision ledger",
        "summary": "generated/psdq-bgd-facility-validation-public-source-decision-ledger-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-public-source-decision-ledger.csv",
        "artifact": "facility-validation-public-source-decision-ledger.md",
        "count_paths": [("decision_scope", "decision_ledger_rows")],
        "finding": decision_ledger_finding,
        "reader_use": "Narrows the next review questions into source repair, possible same-facility, and name-conflict lanes.",
    },
    {
        "id": "possible-same-facility-review",
        "group": "human/source-owner gate",
        "title": "Possible same-facility review",
        "summary": "generated/psdq-bgd-facility-validation-possible-same-facility-review-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-possible-same-facility-review.csv",
        "artifact": "facility-validation-possible-same-facility-review.md",
        "count_paths": [("possible_same_facility_scope", "possible_same_facility_rows")],
        "finding": possible_same_finding,
        "reader_use": "Keeps possible same-facility rows open until identity and location evidence are both strong enough.",
    },
    {
        "id": "priority-name-conflict-review",
        "group": "human/source-owner gate",
        "title": "Priority name-conflict review",
        "summary": "generated/psdq-bgd-facility-validation-priority-name-conflict-review-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-priority-name-conflict-review.csv",
        "artifact": "facility-validation-priority-name-conflict-review.md",
        "count_paths": [("priority_name_conflict_scope", "priority_name_conflict_rows")],
        "finding": priority_name_conflict_finding,
        "reader_use": "Prevents high-exposure name conflicts from becoming map-absence claims without support.",
    },
    {
        "id": "lower-priority-name-conflict-review",
        "group": "human/source-owner gate",
        "title": "Lower-priority name-conflict spot check",
        "summary": "generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-lower-priority-name-conflict-review.csv",
        "artifact": "facility-validation-lower-priority-name-conflict-review.md",
        "count_paths": [("lower_priority_name_conflict_scope", "lower_priority_name_conflict_rows")],
        "finding": lower_priority_name_conflict_finding,
        "reader_use": "Documents repeated-candidate risks outside the priority-1 queue.",
    },
    {
        "id": "zero-osm-observability-review",
        "group": "public-map gap",
        "title": "Zero-OSM upazila observability review",
        "summary": "generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-zero-osm-upazila-observability-review.csv",
        "artifact": "facility-validation-zero-osm-upazila-observability-review.md",
        "count_paths": [("zero_osm_observability_scope", "zero_osm_active_registry_upazilas")],
        "finding": zero_osm_finding,
        "reader_use": "Allows upazila-level observability language but not facility-level absence claims.",
    },
    {
        "id": "source-repair-public-evidence",
        "group": "source repair",
        "title": "Source-repair public-evidence attachment",
        "summary": "generated/psdq-bgd-facility-validation-source-repair-public-evidence-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-source-repair-public-evidence.csv",
        "artifact": "facility-validation-source-repair-public-evidence.md",
        "count_paths": [("source_repair_scope", "source_repair_rows")],
        "finding": source_repair_public_finding,
        "reader_use": "Attaches public DGHS/OSM evidence before any repair decision.",
    },
    {
        "id": "official-coordinate-evidence",
        "group": "source repair",
        "title": "Official-coordinate evidence pass",
        "summary": "generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv",
        "artifact": "facility-validation-source-repair-official-coordinate-evidence.md",
        "count_paths": [("official_coordinate_scope", "source_repair_rows")],
        "finding": official_coordinate_finding,
        "reader_use": "Checks what the public official profile coordinate itself can prove.",
    },
    {
        "id": "public-explanation-evidence",
        "group": "source repair",
        "title": "Public-explanation search",
        "summary": "generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv",
        "artifact": "facility-validation-source-repair-public-explanation-evidence.md",
        "count_paths": [("public_explanation_scope", "source_repair_rows")],
        "finding": public_explanation_finding,
        "reader_use": "Searches public official pages for coordinate-source or correction explanations.",
    },
    {
        "id": "correction-record-followup",
        "group": "source repair",
        "title": "Correction-record follow-up",
        "summary": "generated/psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-source-repair-correction-record-followup.csv",
        "artifact": "facility-validation-source-repair-correction-record-followup.md",
        "count_paths": [("correction_followup_scope", "targeted_rows")],
        "finding": correction_followup_finding,
        "reader_use": "Checks whether official public records explain the coordinate conflict.",
    },
    {
        "id": "clarification-packet",
        "group": "human/source-owner gate",
        "title": "No-contact clarification packet",
        "summary": "generated/psdq-bgd-facility-validation-source-repair-clarification-packet-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-source-repair-clarification-packet.csv",
        "artifact": "facility-validation-source-repair-clarification-packet.md",
        "count_paths": [("clarification_scope", "targeted_rows")],
        "finding": clarification_finding,
        "reader_use": "Turns unresolved source-repair rows into source-owner or human-review questions without contact.",
    },
    {
        "id": "registry-vintage-review",
        "group": "human/source-owner gate",
        "title": "Registry-vintage review",
        "summary": "generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-source-repair-registry-vintage-review.csv",
        "artifact": "facility-validation-source-repair-registry-vintage-review.md",
        "count_paths": [("registry_vintage_scope", "targeted_rows")],
        "finding": registry_vintage_finding,
        "reader_use": "Shows that recent registry timestamps still do not resolve the public correction-record gap.",
    },
    {
        "id": "human-gated-handoff",
        "group": "human/source-owner gate",
        "title": "Human-gated handoff matrix",
        "summary": "generated/psdq-bgd-facility-validation-human-gated-handoff-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-human-gated-handoff.csv",
        "artifact": "facility-validation-human-gated-handoff.md",
        "count_paths": [("handoff_scope", "handoff_rows")],
        "finding": handoff_finding,
        "reader_use": "Names the exact rows that require source-owner or human action.",
    },
    {
        "id": "human-validation-worksheet",
        "group": "human/source-owner gate",
        "title": "Human-validation worksheet",
        "summary": "generated/psdq-bgd-facility-validation-human-validation-worksheet-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-human-validation-worksheet.csv",
        "artifact": "facility-validation-human-validation-worksheet.md",
        "count_paths": [("worksheet_scope", "worksheet_rows")],
        "finding": worksheet_finding,
        "reader_use": "Provides the future human-review form without pre-filling decisions.",
    },
    {
        "id": "ai-closure-audit",
        "group": "human/source-owner gate",
        "title": "AI closure audit",
        "summary": "generated/psdq-bgd-facility-validation-ai-closure-audit-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-ai-closure-audit.csv",
        "artifact": "facility-validation-ai-closure-audit.md",
        "count_paths": [("audit_scope", "audit_rows")],
        "finding": closure_audit_finding,
        "reader_use": "Applies the stopping rule: current public evidence permits keep-open language only.",
    },
    {
        "id": "evidence-ladder",
        "group": "evidence navigation",
        "title": "Ten-stage evidence ladder",
        "summary": "generated/psdq-bgd-facility-validation-evidence-ladder-summary.json",
        "csv": "generated/psdq-bgd-facility-validation-evidence-ladder.csv",
        "artifact": "facility-validation-evidence-ladder.md",
        "count_paths": [("ladder_scope", "stages")],
        "finding": evidence_ladder_finding,
        "reader_use": "Gives the public page one compact navigation layer instead of stacked wall sections.",
    },
]


def build_row(spec: dict[str, Any]) -> dict[str, Any]:
    summary_path = PROGRAM_DIR / spec["summary"]
    data = read_json(summary_path)
    finding: FindingFn = spec["finding"]
    return {
        "ledger_id": spec["id"],
        "group": spec["group"],
        "title": spec["title"],
        "status": data.get("status", "summary"),
        "goal_level": data.get("goal_level", ""),
        "method": data.get("method", data.get("selection_rule", "")),
        "attestation_chain": data.get("attestation_chain", ATTESTATION),
        "generated_at": data.get("generated_at", ""),
        "checked_rows": count_from(data, spec["count_paths"]),
        "source_inputs_count": source_count(data),
        "substantive_finding": finding(data),
        "reader_use": spec["reader_use"],
        "artifact_path": rel(spec["artifact"]),
        "summary_path": rel(spec["summary"]),
        "csv_path": rel(spec["csv"]),
        "non_claim": standard_non_claim(data),
    }


def main() -> None:
    exposure = read_json(GENERATED_DIR / "psdq-bgd-exposure-ranked-disagreement-summary.json")
    strata = read_json(GENERATED_DIR / "psdq-bgd-source-disagreement-strata.json")
    sample = read_json(GENERATED_DIR / "psdq-bgd-facility-validation-sample.json")
    ladder = read_json(GENERATED_DIR / "psdq-bgd-facility-validation-evidence-ladder-summary.json")
    closure = read_json(GENERATED_DIR / "psdq-bgd-facility-validation-ai-closure-audit-summary.json")
    handoff = read_json(GENERATED_DIR / "psdq-bgd-facility-validation-human-gated-handoff-summary.json")

    exposure_scope = get(exposure, "exposure") or {}
    strata_coverage = get(strata, "coverage") or {}
    strata_validation = get(strata, "validation_strata") or {}
    sample_scope = get(sample, "sample_summary") or {}
    ladder_scope = get(ladder, "ladder_scope") or {}
    closure_scope = get(closure, "audit_scope") or {}
    handoff_scope = get(handoff, "handoff_scope") or {}

    rows = [build_row(spec) for spec in SPECS]

    headline_counts = {
        "ledger_rows": len(rows),
        "supporting_summary_files_indexed": len(SPECS),
        "registry_admin_rows": n(strata_coverage.get("registry_admin_rows")),
        "rows_with_open_buildings_denominator": n(strata_coverage.get("rows_with_open_buildings_denominator")),
        "active_clinical_facilities": n(exposure_scope.get("active_clinical_facilities")),
        "osm_health_joined": n(exposure_scope.get("osm_health_joined")),
        "registry_minus_osm_clinical": n(exposure_scope.get("registry_minus_osm_clinical")),
        "rows_with_zero_osm_health_features": n(strata_validation.get("rows_with_zero_osm_health_features")),
        "share_with_zero_osm_health_features": f(strata_validation.get("share_with_zero_osm_health_features")),
        "rows_where_osm_equals_or_exceeds_registry": n(strata_validation.get("rows_where_osm_equals_or_exceeds_registry")),
        "sampled_upazilas": n(sample_scope.get("sampled_upazilas")),
        "sampled_facility_rows": n(sample_scope.get("sampled_facility_rows")),
        "coordinate_ready_facility_rows": n(sample_scope.get("coordinate_ready_facility_rows")),
        "evidence_ladder_stages": n(ladder_scope.get("stages")),
        "targeted_public_source_rows": n(ladder_scope.get("targeted_public_source_rows")),
        "human_gated_handoff_rows": n(handoff_scope.get("handoff_rows")),
        "human_or_source_owner_wall_rows": n(closure_scope.get("human_or_source_owner_wall_rows")),
        "ai_actionable_without_human_or_source_owner_rows": n(
            closure_scope.get("ai_actionable_without_human_or_source_owner_rows")
        ),
        "keep_open_only_rows": n(closure_scope.get("keep_open_only_rows")),
        "external_contacts_made": n(closure_scope.get("external_contacts_made")),
        "rows_allowed_for_closure": n(handoff_scope.get("rows_allowed_for_closure")),
        "rows_allowed_for_same_facility_reclassification": n(
            handoff_scope.get("rows_allowed_for_same_facility_reclassification")
        ),
        "rows_allowed_for_map_absence_language": n(handoff_scope.get("rows_allowed_for_map_absence_language")),
        "coordinate_corrections_allowed": n(handoff_scope.get("coordinate_corrections_allowed")),
    }

    payload = {
        "program": PROGRAM,
        "status": STATUS,
        "method": METHOD,
        "attestation_chain": ATTESTATION,
        "generated_at": now_utc(),
        "finding": {
            "headline": (
                "Bangladesh registry-map disagreement is visible at upazila scale, "
                "but row-level repair is now explicitly human/source-owner gated."
            ),
            "claim": (
                f"The PSDQ Bangladesh L3 module joins {headline_counts['registry_admin_rows']:,} DGHS "
                f"upazila rows with {headline_counts['active_clinical_facilities']:,} active clinical "
                f"facilities to {headline_counts['osm_health_joined']:,} joined OSM health features; "
                f"the facility-validation chain ends with {headline_counts['human_or_source_owner_wall_rows']:,} "
                "human/source-owner wall rows and 0 AI-actionable closures."
            ),
            "maturity": "L3 evidence module; PR ai-first package; not human-final.",
            "reader_use": (
                "Use this as a source-quality and validation-priority screen before any travel-time, "
                "catchment, service-access, or facility-availability claim."
            ),
        },
        "headline_counts": headline_counts,
        "reader_first_test": {
            "remember": (
                "The public data are strong enough to show registry-map disagreement and weak enough "
                "to block row closure without human or source-owner evidence."
            ),
            "hero_visual": "Evidence-gate matrix plus one generated evidence ledger.",
            "cautions": [
                "The registry is not assumed to be ground truth.",
                "OSM absence is not facility absence.",
                "No source owner or human reviewer was contacted under ai-first mode.",
            ],
            "audit_route": "generated/evidence-ledger.json and generated/evidence-ledger.csv",
        },
        "data_to_visual_contract": {
            "source": "public-service-data-quality/generated/evidence-ledger.json",
            "transform": "reporting-site/src/components/EvidenceLedger.tsx renders grouped rows, filtering, and ledger links.",
            "claim_role": "Supports the headline and makes the human/source-owner gate visible.",
            "mobile_proof": "375 px browser QA required after site build.",
            "fallback": "The evidence ledger table lists every artifact row, substantive finding, and download link.",
        },
        "rows": rows,
        "outputs": {
            "json": rel(STANDARD_JSON.relative_to(PROGRAM_DIR).as_posix()),
            "csv": rel(STANDARD_CSV.relative_to(PROGRAM_DIR).as_posix()),
            "legacy_json": rel(OUT_JSON.relative_to(PROGRAM_DIR).as_posix()),
            "legacy_csv": rel(OUT_CSV.relative_to(PROGRAM_DIR).as_posix()),
        },
        "non_claim": NON_CLAIM,
    }

    fields = [
        "ledger_id",
        "group",
        "title",
        "status",
        "goal_level",
        "method",
        "attestation_chain",
        "generated_at",
        "checked_rows",
        "source_inputs_count",
        "substantive_finding",
        "reader_use",
        "artifact_path",
        "summary_path",
        "csv_path",
        "non_claim",
    ]
    write_json(OUT_JSON, payload)
    write_json(STANDARD_JSON, payload)
    write_csv(OUT_CSV, rows, fields)
    write_csv(STANDARD_CSV, rows, fields)
    print(f"Wrote {OUT_JSON} ({len(rows)} ledger rows)")
    print(f"Wrote {STANDARD_JSON}")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {STANDARD_CSV}")


if __name__ == "__main__":
    main()
