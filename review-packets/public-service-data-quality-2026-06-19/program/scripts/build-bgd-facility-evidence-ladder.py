"""Build a no-contact evidence ladder for the PSDQ BGD validation chain.

This no-network pass reads committed summary JSON files and creates a compact
stage-by-stage ladder from source-disagreement strata through the human-gated
handoff and AI closure audit. It is a reader-navigation artifact, not a new
validation result.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

OUT_LADDER_CSV = OUT_DIR / "psdq-bgd-facility-validation-evidence-ladder.csv"
OUT_LADDER_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-evidence-ladder-summary.json"

METHOD = "ai_evidence_ladder_from_committed_psdq_summaries_v1"
STATUS = "ai_evidence_ladder_not_validation"
NON_CLAIM = (
    "This is an AI-first no-contact evidence ladder for the PSDQ Bangladesh "
    "facility-validation chain. It summarizes committed summary artifacts so "
    "a reader can follow the audit sequence. It is not external outreach, not "
    "human validation, not ground truth, not a row closure, not a "
    "same-facility reclassification, not a coordinate correction, not a "
    "facility-quality assessment, and not a service-access estimate."
)


INPUTS = {
    "strata": OUT_DIR / "psdq-bgd-source-disagreement-strata.json",
    "sample": OUT_DIR / "psdq-bgd-facility-validation-sample.json",
    "coded": OUT_DIR / "psdq-bgd-facility-validation-coded-summary.json",
    "ai_review": OUT_DIR / "psdq-bgd-facility-validation-ai-review-summary.json",
    "inspection": OUT_DIR / "psdq-bgd-facility-validation-public-map-inspection-summary.json",
    "confirmation": OUT_DIR / "psdq-bgd-facility-validation-public-source-confirmation-targeted-rows-summary.json",
    "decision": OUT_DIR / "psdq-bgd-facility-validation-public-source-decision-ledger-summary.json",
    "handoff": OUT_DIR / "psdq-bgd-facility-validation-human-gated-handoff-summary.json",
    "worksheet": OUT_DIR / "psdq-bgd-facility-validation-human-validation-worksheet-summary.json",
    "closure_audit": OUT_DIR / "psdq-bgd-facility-validation-ai-closure-audit-summary.json",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def n(value: Any) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def source_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def stage(
    *,
    stage_order: int,
    stage_id: str,
    stage_label: str,
    source_key: str,
    unit: str,
    row_count: int,
    stage_type: str,
    reader_use: str,
    keep_open_rows: int = 0,
    closed_rows: int = 0,
    reclassified_rows: int = 0,
    map_absence_rows: int = 0,
    coordinate_correction_rows: int = 0,
    human_or_source_owner_wall_rows: int = 0,
    ai_actionable_rows: int = 0,
    supporting_rows: int = 0,
    primary_gate: str = "",
    caveat: str = "",
    generated_at: str = "",
) -> dict[str, Any]:
    return {
        "stage_order": stage_order,
        "stage_id": stage_id,
        "stage_label": stage_label,
        "generated_at": generated_at,
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "source_summary_key": source_key,
        "source_summary_path": source_path(INPUTS[source_key]),
        "unit": unit,
        "row_count": row_count,
        "supporting_rows": supporting_rows,
        "stage_type": stage_type,
        "reader_use": reader_use,
        "primary_gate": primary_gate,
        "keep_open_rows": keep_open_rows,
        "closed_rows": closed_rows,
        "reclassified_rows": reclassified_rows,
        "map_absence_rows": map_absence_rows,
        "coordinate_correction_rows": coordinate_correction_rows,
        "human_or_source_owner_wall_rows": human_or_source_owner_wall_rows,
        "ai_actionable_rows": ai_actionable_rows,
        "caveat": caveat,
        "non_claim": NON_CLAIM,
    }


def build_rows(generated_at: str) -> list[dict[str, Any]]:
    data = {key: read_json(path) for key, path in INPUTS.items()}
    strata_coverage = data["strata"]["coverage"]
    sample_scope = data["sample"]["sample_summary"]
    coded_scope = data["coded"]["screen_summary"]
    ai_review_scope = data["ai_review"]["review_scope"]
    inspection_scope = data["inspection"]["inspection_scope"]
    confirmation_scope = data["confirmation"]["confirmation_scope"]
    decision_scope = data["decision"]["decision_scope"]
    handoff_scope = data["handoff"]["handoff_scope"]
    worksheet_scope = data["worksheet"]["worksheet_scope"]
    audit_scope = data["closure_audit"]["audit_scope"]

    return [
        stage(
            stage_order=1,
            stage_id="source_disagreement_strata",
            stage_label="Source-disagreement strata",
            source_key="strata",
            unit="DGHS registry upazila row",
            row_count=n(strata_coverage["registry_admin_rows"]),
            supporting_rows=n(strata_coverage["active_clinical_facilities"]),
            stage_type="source_disagreement_context",
            reader_use="Show where registry-map disagreement is concentrated before facility-row review.",
            primary_gate="Context only; not a facility validation result.",
            caveat="Upazila source disagreement cannot identify which individual facility row is correct.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=2,
            stage_id="validation_sample_design",
            stage_label="Validation sample design",
            source_key="sample",
            unit="sampled DGHS facility row",
            row_count=n(sample_scope["sampled_facility_rows"]),
            supporting_rows=n(sample_scope["sampled_upazilas"]),
            stage_type="sample_design",
            reader_use="Select a reproducible facility-row sample from the strata.",
            primary_gate="Design artifact only; no validation outcomes.",
            caveat="Sampling makes the review tractable but does not estimate a national error rate.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=3,
            stage_id="automated_coded_screen",
            stage_label="Automated coded screen",
            source_key="coded",
            unit="sampled DGHS facility row",
            row_count=n(coded_scope["coded_rows"]),
            supporting_rows=n(coded_scope["manual_review_recommended_rows"]),
            stage_type="automated_public_source_screen",
            reader_use="Separate rows needing public-source review from rows not reopened.",
            primary_gate="Automated triage only; not human validation.",
            keep_open_rows=n(coded_scope["manual_review_recommended_rows"]),
            caveat="Public-source codes are review triggers, not ground-truth labels.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=4,
            stage_id="ai_public_source_review",
            stage_label="AI public-source review ledger",
            source_key="ai_review",
            unit="flagged sampled row",
            row_count=n(ai_review_scope["flagged_rows_reviewed"]),
            supporting_rows=n(ai_review_scope["candidate_resolution_rows"]),
            stage_type="ai_public_source_review",
            reader_use="Group flagged rows into coordinate, map-gap, candidate, and unresolved-source lanes.",
            primary_gate="AI review can organize evidence but cannot validate rows.",
            keep_open_rows=n(ai_review_scope["flagged_rows_reviewed"]),
            caveat="The ledger names workstreams; it does not close rows.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=5,
            stage_id="targeted_public_map_inspection",
            stage_label="Targeted public-map inspection",
            source_key="inspection",
            unit="targeted public-map inspection row",
            row_count=n(inspection_scope["rows_inspected"]),
            supporting_rows=n(inspection_scope["rows_with_candidate_public_map_feature"]),
            stage_type="public_map_inspection_queue",
            reader_use="Attach candidate public-map context and row-level inspection links.",
            primary_gate="Candidate context is not a same-facility decision.",
            keep_open_rows=n(inspection_scope["rows_kept_open"]),
            closed_rows=n(inspection_scope["rows_closed_as_resolved"]),
            reclassified_rows=n(inspection_scope["rows_reclassified_as_same_facility"]),
            caveat="Candidate proximity and names can guide review but cannot replace identity/location validation.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=6,
            stage_id="targeted_public_source_confirmation",
            stage_label="Targeted public-source confirmation",
            source_key="confirmation",
            unit="targeted inspection row",
            row_count=n(confirmation_scope["rows_checked"]),
            supporting_rows=n(confirmation_scope["dghs_profiles_retrieved"]),
            stage_type="public_source_retrieval",
            reader_use="Retrieve public DGHS profile pages and public OSM API records for inspection rows.",
            primary_gate="Retrieved public records are evidence inputs, not validation outcomes.",
            keep_open_rows=n(confirmation_scope["rows_kept_open"]),
            closed_rows=n(confirmation_scope["rows_closed_as_resolved"]),
            reclassified_rows=n(confirmation_scope["rows_reclassified_as_same_facility"]),
            caveat="A retrieved profile or candidate record does not by itself prove same-facility identity.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=7,
            stage_id="public_source_decision_ledger",
            stage_label="Public-source decision ledger",
            source_key="decision",
            unit="targeted row selected for next decision",
            row_count=n(decision_scope["decision_ledger_rows"]),
            supporting_rows=n(decision_scope["targeted_confirmation_rows"]),
            stage_type="decision_queue",
            reader_use="Prioritize source repair, possible same-facility, and priority name-conflict questions.",
            primary_gate="Decision queue, not closure.",
            keep_open_rows=n(decision_scope["decision_ledger_rows"]),
            closed_rows=n(decision_scope["rows_closed_as_resolved"]),
            reclassified_rows=n(decision_scope["rows_reclassified_as_same_facility"]),
            caveat="Some lower-priority and zero-OSM rows are deferred to separate gate reviews.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=8,
            stage_id="human_gated_handoff",
            stage_label="Human-gated handoff matrix",
            source_key="handoff",
            unit="unresolved handoff row",
            row_count=n(handoff_scope["handoff_rows"]),
            supporting_rows=n(handoff_scope["upazilas_with_handoff_rows"]),
            stage_type="human_or_source_owner_wall",
            reader_use="Consolidate open rows that require source-owner clarification or human validation.",
            primary_gate="Human or source-owner evidence required.",
            keep_open_rows=n(handoff_scope["handoff_rows"]),
            closed_rows=n(handoff_scope["rows_allowed_for_closure"]),
            reclassified_rows=n(handoff_scope["rows_allowed_for_same_facility_reclassification"]),
            map_absence_rows=n(handoff_scope["rows_allowed_for_map_absence_language"]),
            coordinate_correction_rows=n(handoff_scope["coordinate_corrections_allowed"]),
            human_or_source_owner_wall_rows=n(handoff_scope["human_or_owner_action_required_rows"]),
            caveat="The matrix is a reviewer queue, not validation.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=9,
            stage_id="human_validation_worksheet",
            stage_label="Human-validation worksheet",
            source_key="worksheet",
            unit="blank human-review worksheet row",
            row_count=n(worksheet_scope["worksheet_rows"]),
            supporting_rows=n(worksheet_scope["blank_human_validation_status_rows"]),
            stage_type="blank_human_review_instrument",
            reader_use="Provide the future reviewer with row-specific rules and blank decision fields.",
            primary_gate="Human-review fields intentionally blank.",
            keep_open_rows=n(worksheet_scope["worksheet_rows"]),
            closed_rows=n(worksheet_scope["prefilled_closure_allowed_rows"]),
            reclassified_rows=n(worksheet_scope["prefilled_reclassification_allowed_rows"]),
            map_absence_rows=n(worksheet_scope["prefilled_map_absence_allowed_rows"]),
            coordinate_correction_rows=n(worksheet_scope["prefilled_coordinate_correction_allowed_rows"]),
            human_or_source_owner_wall_rows=n(worksheet_scope["worksheet_rows"]),
            caveat="A blank decision field is unresolved evidence, not negative evidence.",
            generated_at=generated_at,
        ),
        stage(
            stage_order=10,
            stage_id="ai_closure_audit",
            stage_label="AI closure audit",
            source_key="closure_audit",
            unit="audited worksheet row",
            row_count=n(audit_scope["audit_rows"]),
            supporting_rows=n(audit_scope["keep_open_only_rows"]),
            stage_type="ai_keep_open_gate",
            reader_use="Audit whether any current row can be closed by AI from public evidence alone.",
            primary_gate="Keep-open only under current public evidence.",
            keep_open_rows=n(audit_scope["keep_open_only_rows"]),
            closed_rows=n(audit_scope["ai_closure_possible_rows"]),
            reclassified_rows=n(audit_scope["ai_same_facility_reclassification_possible_rows"]),
            map_absence_rows=n(audit_scope["ai_map_absence_language_possible_rows"]),
            coordinate_correction_rows=n(audit_scope["ai_coordinate_correction_possible_rows"]),
            human_or_source_owner_wall_rows=n(audit_scope["human_or_source_owner_wall_rows"]),
            ai_actionable_rows=n(audit_scope["ai_actionable_without_human_or_source_owner_rows"]),
            caveat="The AI loop stops here until a public official source, source-owner response, or human validation resolves a row.",
            generated_at=generated_at,
        ),
    ]


def main() -> None:
    generated_at = now_utc()
    rows = build_rows(generated_at)
    fields = list(rows[0].keys()) if rows else []
    write_csv(OUT_LADDER_CSV, rows, fields)

    terminal = rows[-1]
    summary = {
        "generated_at": generated_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 evidence-ladder navigation artifact",
        "unit": "PSDQ Bangladesh facility-validation evidence stage",
        "source_inputs": [
            {"key": key, "path": source_path(path)}
            for key, path in INPUTS.items()
        ],
        "selection_rule": (
            "Read committed PSDQ Bangladesh facility-validation summary JSON "
            "files and emit one row per evidence stage. Counts are stage counts, "
            "not a statistical attrition funnel."
        ),
        "ladder_scope": {
            "stages": len(rows),
            "input_summary_files": len(INPUTS),
            "sampled_facility_rows": next(row["row_count"] for row in rows if row["stage_id"] == "validation_sample_design"),
            "targeted_public_source_rows": next(row["row_count"] for row in rows if row["stage_id"] == "targeted_public_source_confirmation"),
            "human_gated_handoff_rows": next(row["row_count"] for row in rows if row["stage_id"] == "human_gated_handoff"),
            "ai_closure_audit_rows": terminal["row_count"],
            "ai_actionable_without_human_or_source_owner_rows": terminal["ai_actionable_rows"],
            "keep_open_only_rows": terminal["keep_open_rows"],
            "human_or_source_owner_wall_rows": terminal["human_or_source_owner_wall_rows"],
        },
        "stage_rows": rows,
        "terminal_gate": {
            "stage_id": terminal["stage_id"],
            "stage_label": terminal["stage_label"],
            "row_count": terminal["row_count"],
            "ai_actionable_rows": terminal["ai_actionable_rows"],
            "keep_open_rows": terminal["keep_open_rows"],
            "human_or_source_owner_wall_rows": terminal["human_or_source_owner_wall_rows"],
            "primary_gate": terminal["primary_gate"],
        },
        "review_notes": [
            "This ladder is a navigation artifact, not a new empirical finding.",
            "Stage counts use different units and should not be read as an attrition rate.",
            "The terminal gate remains owner-only source-owner contact or human location validation.",
        ],
        "non_claim": NON_CLAIM,
    }
    write_json(OUT_LADDER_SUMMARY_JSON, summary)

    print(
        "Built BGD evidence ladder: "
        f"{summary['ladder_scope']['stages']} stages; "
        f"{summary['ladder_scope']['ai_actionable_without_human_or_source_owner_rows']} AI-actionable terminal rows; "
        f"{summary['ladder_scope']['keep_open_only_rows']} keep-open terminal rows."
    )
    print(f"Wrote {OUT_LADDER_CSV}")
    print(f"Wrote {OUT_LADDER_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
