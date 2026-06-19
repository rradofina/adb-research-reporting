"""Attach public-source evidence for PSDQ BGD source-repair rows.

This no-network pass reads the 16-row public-source decision ledger and the
upstream targeted confirmation packet, then attaches the already retrieved
public DGHS profile and OSM API evidence for the four source-repair-first rows.
It does not close, reclassify, or validate any row.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_DECISION_LEDGER_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-source-decision-ledger.csv"
IN_DECISION_LEDGER_SUMMARY_JSON = (
    OUT_DIR / "psdq-bgd-facility-validation-public-source-decision-ledger-summary.json"
)
IN_CONFIRMATION_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-source-confirmation-targeted-rows.csv"

OUT_SOURCE_REPAIR_EVIDENCE_CSV = (
    OUT_DIR / "psdq-bgd-facility-validation-source-repair-public-evidence.csv"
)
OUT_SOURCE_REPAIR_EVIDENCE_SUMMARY_JSON = (
    OUT_DIR / "psdq-bgd-facility-validation-source-repair-public-evidence-summary.json"
)

METHOD = "ai_public_source_repair_evidence_attachment_v1"
STATUS = "ai_public_source_repair_evidence_attachment_not_human_validation"
SOURCE_REPAIR_TRACK = "source_repair_first"
NON_CLAIM = (
    "This is an AI-first public-source evidence attachment for PSDQ "
    "source-repair rows. It attaches already retrieved public DGHS profile and "
    "OSM API evidence to reviewer questions. It is not human validation, not "
    "ground truth, not a row closure, not a same-facility reclassification, "
    "not a facility-quality assessment, and not a service-access estimate."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
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


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def evidence_class(row: dict[str, Any], shared_candidate_rows: int) -> str:
    distance = to_float(row.get("candidate_distance_m_from_inspection"))
    score = to_float(row.get("candidate_name_score_from_live_tags"))
    if shared_candidate_rows > 1:
        return "shared_public_map_candidate_across_multiple_dghs_rows"
    if distance >= 50_000:
        return "strong_name_but_extreme_coordinate_distance_conflict"
    if distance >= 10_000 and score >= 0.75:
        return "strong_name_but_long_coordinate_distance_conflict"
    if distance >= 10_000:
        return "long_coordinate_distance_source_check"
    return "source_repair_public_evidence_attached"


def reviewer_action(row: dict[str, Any], shared_candidate_rows: int) -> str:
    if shared_candidate_rows > 1:
        return (
            "Compare the two DGHS profiles and the shared OSM candidate before "
            "any duplicate-coordinate or same-facility interpretation."
        )
    if to_float(row.get("candidate_distance_m_from_inspection")) >= 10_000:
        return (
            "Resolve the DGHS coordinate/source question before using the OSM "
            "candidate as map-absence or same-facility evidence."
        )
    return "Attach the public profile and OSM evidence, then keep the row open for source-coordinate review."


def reviewer_question(row: dict[str, Any], shared_candidate_rows: int) -> str:
    if shared_candidate_rows > 1:
        return (
            "Why do multiple DGHS rows point to the same public OSM candidate, "
            "and does a public official source distinguish the records?"
        )
    return (
        "Does a public official source explain the DGHS coordinate or source "
        "used for this row before any map-absence label is considered?"
    )


def source_attachment_complete(row: dict[str, Any]) -> bool:
    return (
        to_bool(row.get("dghs_profile_retrieved"))
        and str(row.get("dghs_profile_http_status", "")) == "200"
        and to_bool(row.get("candidate_osm_api_retrieved"))
        and str(row.get("candidate_osm_api_http_status", "")) == "200"
    )


def candidate_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("candidate_feature_url") or "")].append(row)

    output = []
    for url, items in grouped.items():
        first = items[0]
        output.append(
            {
                "candidate_feature_url": url,
                "candidate_osm_api_url": first.get("candidate_osm_api_url", ""),
                "candidate_osm_name_from_api": first.get("candidate_osm_name_from_api", ""),
                "source_repair_rows": len(items),
                "districts": sorted({str(row.get("district_name") or "") for row in items}),
                "upazilas": sorted({str(row.get("upazila_name") or "") for row in items}),
                "facilities": [row.get("facility_name", "") for row in items],
                "max_distance_m": round(
                    max(to_float(row.get("candidate_distance_m_from_inspection")) for row in items), 1
                ),
                "max_name_score": round(
                    max(to_float(row.get("candidate_name_score_from_live_tags")) for row in items), 4
                ),
            }
        )
    return sorted(output, key=lambda row: (-row["source_repair_rows"], row["candidate_osm_name_from_api"]))


def main() -> None:
    if not IN_DECISION_LEDGER_CSV.exists():
        raise FileNotFoundError(IN_DECISION_LEDGER_CSV)
    if not IN_DECISION_LEDGER_SUMMARY_JSON.exists():
        raise FileNotFoundError(IN_DECISION_LEDGER_SUMMARY_JSON)
    if not IN_CONFIRMATION_CSV.exists():
        raise FileNotFoundError(IN_CONFIRMATION_CSV)

    decision_rows = read_csv(IN_DECISION_LEDGER_CSV)
    decision_summary = read_json(IN_DECISION_LEDGER_SUMMARY_JSON)
    confirmation_rows = read_csv(IN_CONFIRMATION_CSV)
    confirmation_by_id = {row["confirmation_id"]: row for row in confirmation_rows}

    source_repair_rows = [
        row for row in decision_rows if row.get("decision_track") == SOURCE_REPAIR_TRACK
    ]
    candidate_feature_counts = Counter(row.get("candidate_feature_url", "") for row in source_repair_rows)
    generated_at = now_utc()

    evidence_rows: list[dict[str, Any]] = []
    for index, row in enumerate(source_repair_rows, start=1):
        confirmation = confirmation_by_id.get(str(row.get("confirmation_id") or ""))
        if confirmation is None:
            raise KeyError(f"Missing confirmation row for {row.get('confirmation_id')}")

        shared_rows = candidate_feature_counts.get(row.get("candidate_feature_url", ""), 0)
        attached = source_attachment_complete(confirmation)
        evidence_rows.append(
            {
                "evidence_id": f"PSDQ-BGD-SRE-{index:03d}",
                "evidence_rank": index,
                "evidence_method": METHOD,
                "generated_at": generated_at,
                "source_retrieved_at": confirmation.get("retrieved_at", ""),
                "attestation_chain": "ai-first",
                "status": STATUS,
                "decision_id": row.get("decision_id", ""),
                "confirmation_id": row.get("confirmation_id", ""),
                "inspection_id": row.get("inspection_id", ""),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "priority_scope": row.get("priority_scope", ""),
                "decision_track": row.get("decision_track", ""),
                "decision_track_label": row.get("decision_track_label", ""),
                "source_repair_evidence_class": evidence_class(row, shared_rows),
                "source_repair_reviewer_action": reviewer_action(row, shared_rows),
                "source_repair_reviewer_question": reviewer_question(row, shared_rows),
                "closure_or_reclassification_gate": (
                    "Keep open unless a public official source establishes the intended "
                    "coordinate/source correction or confirms a duplicate/source error."
                ),
                "public_evidence_attached": attached,
                "dghs_public_profile_url": confirmation.get("dghs_public_profile_url", ""),
                "dghs_profile_http_status": confirmation.get("dghs_profile_http_status", ""),
                "dghs_profile_final_url": confirmation.get("dghs_profile_final_url", ""),
                "dghs_profile_contains_profile_id": confirmation.get("dghs_profile_contains_profile_id", ""),
                "dghs_profile_facility_token_coverage": confirmation.get(
                    "dghs_profile_facility_token_coverage", ""
                ),
                "dghs_profile_public_name_token_coverage": confirmation.get(
                    "dghs_profile_public_name_token_coverage", ""
                ),
                "candidate_feature_url": confirmation.get("candidate_feature_url", ""),
                "candidate_osm_api_url": confirmation.get("candidate_osm_api_url", ""),
                "candidate_osm_api_http_status": confirmation.get("candidate_osm_api_http_status", ""),
                "candidate_osm_type": confirmation.get("candidate_osm_type", ""),
                "candidate_osm_id": confirmation.get("candidate_osm_id", ""),
                "candidate_osm_name_from_api": confirmation.get("candidate_osm_name_from_api", ""),
                "candidate_osm_lat": confirmation.get("candidate_osm_lat", ""),
                "candidate_osm_lon": confirmation.get("candidate_osm_lon", ""),
                "candidate_osm_tags_compact": confirmation.get("candidate_osm_tags_compact", ""),
                "candidate_distance_m_from_inspection": confirmation.get(
                    "candidate_distance_m_from_inspection", ""
                ),
                "candidate_name_score_from_live_tags": confirmation.get(
                    "candidate_name_score_from_live_tags", ""
                ),
                "shared_public_map_candidate_rows": shared_rows,
                "source_basis": (
                    "Public DGHS profile URL and public OSM API feature URL from the "
                    "targeted confirmation packet, with HTTP status and retrieval timestamp."
                ),
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "non_claim": NON_CLAIM,
            }
        )

    evidence_class_counts = Counter(row["source_repair_evidence_class"] for row in evidence_rows)
    attached_count = sum(1 for row in evidence_rows if row["public_evidence_attached"])
    distances = [to_float(row.get("candidate_distance_m_from_inspection")) for row in evidence_rows]
    candidate_group_rows = candidate_groups(evidence_rows)

    summary = {
        "generated_at": generated_at,
        "source_retrieved_at": decision_summary.get("source_retrieved_at", ""),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 source-repair public-evidence attachment",
        "unit": "source-repair-first row selected from the PSDQ public-source decision ledger",
        "source_inputs": [
            {
                "path": str(IN_DECISION_LEDGER_CSV.relative_to(ROOT)),
                "role": "16-row public-source decision ledger",
            },
            {
                "path": str(IN_CONFIRMATION_CSV.relative_to(ROOT)),
                "role": "40-row targeted public-source confirmation CSV",
            },
        ],
        "selection_rule": "Include only decision-ledger rows where decision_track is source_repair_first.",
        "source_repair_scope": {
            "decision_ledger_rows": len(decision_rows),
            "source_repair_rows": len(evidence_rows),
            "public_evidence_attached_rows": attached_count,
            "dghs_profiles_attached": sum(
                1 for row in evidence_rows if str(row.get("dghs_profile_http_status", "")) == "200"
            ),
            "osm_api_records_attached": sum(
                1 for row in evidence_rows if str(row.get("candidate_osm_api_http_status", "")) == "200"
            ),
            "rows_with_shared_public_map_candidate": sum(
                1 for row in evidence_rows if int(row["shared_public_map_candidate_rows"]) > 1
            ),
            "rows_with_candidate_distance_10km_or_more": sum(1 for value in distances if value >= 10_000),
            "rows_with_candidate_distance_50km_or_more": sum(1 for value in distances if value >= 50_000),
            "max_candidate_distance_m": round(max(distances) if distances else 0.0, 1),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "source_repair_evidence_class_counts": [
            {"name": name, "rows": int(evidence_class_counts[name])}
            for name in sorted(evidence_class_counts)
        ],
        "candidate_feature_groups": candidate_group_rows,
        "evidence_rows": evidence_rows,
        "evidence_notes": [
            "This pass attaches public-source evidence only for the source-repair-first track.",
            "Rows with a shared public-map candidate are collision checks, not duplicate closures.",
            "Rows with long candidate distances remain source-coordinate checks, even when names match.",
            "All rows remain open pending a public official coordinate/source explanation.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = list(evidence_rows[0].keys()) if evidence_rows else []
    write_csv(OUT_SOURCE_REPAIR_EVIDENCE_CSV, evidence_rows, fields)
    write_json(OUT_SOURCE_REPAIR_EVIDENCE_SUMMARY_JSON, summary)

    print(
        "Built BGD source-repair public evidence: "
        f"{len(evidence_rows)} rows; {attached_count} public evidence attachments; "
        f"{summary['source_repair_scope']['rows_with_shared_public_map_candidate']} shared-candidate rows; "
        f"{summary['source_repair_scope']['rows_closed_as_resolved']} closed."
    )
    print(f"Wrote {OUT_SOURCE_REPAIR_EVIDENCE_CSV}")
    print(f"Wrote {OUT_SOURCE_REPAIR_EVIDENCE_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
