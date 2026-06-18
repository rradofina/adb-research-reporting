"""Fetch public-source confirmation details for the first PSDQ inspection rows.

This pass follows the targeted public-map inspection packet. It opens the
public DGHS profile URL and the OSM API record for the first inspection-card
rows, records what was retrieved, and keeps every row open unless public
evidence is strong enough for a later manual source decision.

It is intentionally a public-source confirmation packet, not human validation,
not ground truth, and not a row-closure script.
"""

from __future__ import annotations

import csv
import html
import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_INSPECTION_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-map-inspection-summary.json"
OUT_CONFIRMATION_CSV = OUT_DIR / "psdq-bgd-facility-validation-public-source-confirmation.csv"
OUT_CONFIRMATION_SUMMARY_JSON = OUT_DIR / "psdq-bgd-facility-validation-public-source-confirmation-summary.json"

METHOD = "ai_public_source_confirmation_first_rows_v1"
STATUS = "ai_public_source_confirmation_not_human_validation"
ROW_LIMIT = 12
USER_AGENT = "ADB-AI-Research-PSDQ-public-source-confirmation/1.0 (public evidence audit)"
NON_CLAIM = (
    "This is an AI-first public-source confirmation packet for the first "
    "targeted PSDQ public-map inspection rows. It retrieves public DGHS "
    "profile pages and public OSM API feature records. It is not human "
    "validation, not ground truth, not a facility-quality assessment, and not "
    "a service-access estimate."
)

NAME_STOPWORDS = {
    "and",
    "bangladesh",
    "bed",
    "care",
    "center",
    "centre",
    "clinic",
    "college",
    "community",
    "complex",
    "diagnostic",
    "district",
    "general",
    "health",
    "hospital",
    "limited",
    "ltd",
    "medical",
    "nursing",
    "private",
    "pvt",
    "sadar",
    "specialized",
    "upazila",
}

TAG_KEYS_FOR_REVIEW = [
    "amenity",
    "healthcare",
    "name",
    "name:en",
    "name:bn",
    "official_name",
    "alt_name",
    "operator",
    "addr:city",
    "addr:street",
    "website",
    "phone",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def normalize_text(value: Any) -> str:
    text = html.unescape(str(value or "")).lower()
    text = re.sub(r"<script[\s\S]*?</script>", " ", text)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def name_tokens(value: Any) -> set[str]:
    return {
        token
        for token in normalize_text(value).split()
        if len(token) > 2 and token not in NAME_STOPWORDS and not token.isdigit()
    }


def token_coverage(needles: set[str], haystack_text: str) -> float:
    if not needles:
        return 0.0
    haystack = set(normalize_text(haystack_text).split())
    return round(len(needles & haystack) / len(needles), 4)


def name_support_score(left: str, right: str) -> float:
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    sequence = SequenceMatcher(None, left_norm, right_norm).ratio()
    left_tokens = name_tokens(left_norm)
    right_tokens = name_tokens(right_norm)
    overlap = len(left_tokens & right_tokens) / len(left_tokens | right_tokens) if left_tokens and right_tokens else 0.0
    substring = 0.0
    if len(left_norm) >= 6 and len(right_norm) >= 6 and (left_norm in right_norm or right_norm in left_norm):
        substring = min(len(left_norm), len(right_norm)) / max(len(left_norm), len(right_norm))
    return round(max(sequence, overlap, substring), 4)


def compact_tags(tags: dict[str, Any]) -> str:
    pairs = []
    for key in TAG_KEYS_FOR_REVIEW:
        value = tags.get(key)
        if value not in (None, ""):
            pairs.append(f"{key}={value}")
    return "; ".join(pairs)


def fetch_url(url: str, timeout: int = 20) -> dict[str, Any]:
    if not url:
        return {
            "url": "",
            "ok": False,
            "status": "",
            "final_url": "",
            "content_type": "",
            "body": "",
            "error": "missing_url",
        }
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            return {
                "url": url,
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.url,
                "content_type": response.headers.get("content-type", ""),
                "body": body.decode("utf-8", errors="replace"),
                "error": "",
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "url": url,
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "body": body,
            "error": f"http_error_{exc.code}",
        }
    except URLError as exc:
        return {
            "url": url,
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "body": "",
            "error": f"url_error:{exc.reason}",
        }
    except TimeoutError:
        return {
            "url": url,
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "body": "",
            "error": "timeout",
        }


def osm_api_url(osm_feature_url: str) -> str:
    match = re.search(r"openstreetmap\.org/(node|way|relation)/(\d+)", str(osm_feature_url or ""))
    if not match:
        return ""
    osm_type, osm_id = match.groups()
    return f"https://api.openstreetmap.org/api/0.6/{osm_type}/{osm_id}.json"


def parse_osm_payload(body: str) -> dict[str, Any]:
    if not body:
        return {"tags": {}, "element_type": "", "element_id": "", "name": "", "lat": "", "lon": ""}
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return {"tags": {}, "element_type": "", "element_id": "", "name": "", "lat": "", "lon": ""}
    elements = payload.get("elements") or []
    if not elements:
        return {"tags": {}, "element_type": "", "element_id": "", "name": "", "lat": "", "lon": ""}
    element = elements[0]
    tags = element.get("tags") or {}
    center = element.get("center") or {}
    return {
        "tags": tags,
        "element_type": str(element.get("type") or ""),
        "element_id": str(element.get("id") or ""),
        "name": str(tags.get("name") or tags.get("name:en") or tags.get("name:bn") or ""),
        "lat": element.get("lat") or center.get("lat") or "",
        "lon": element.get("lon") or center.get("lon") or "",
    }


def profile_signal(row: dict[str, Any], profile_body: str) -> dict[str, Any]:
    facility_tokens = name_tokens(row.get("facility_name", ""))
    dghs_public_tokens = name_tokens(row.get("dghs_public_name", ""))
    profile_text = normalize_text(profile_body)
    dghs_id = str(row.get("dghs_public_profile_url", "")).rstrip("/").split("/")[-2]
    if not dghs_id.isdigit():
        dghs_id = str(row.get("dghs_id", ""))
    return {
        "dghs_profile_facility_token_coverage": token_coverage(facility_tokens, profile_text),
        "dghs_profile_public_name_token_coverage": token_coverage(dghs_public_tokens, profile_text),
        "dghs_profile_contains_profile_id": bool(dghs_id and dghs_id in profile_text),
    }


def confirmation_lane(row: dict[str, Any], dghs_ok: bool, osm_ok: bool, osm_name_score: float) -> tuple[str, str]:
    inspection_lane = str(row.get("inspection_lane") or "")
    focus_class = str(row.get("focus_class") or "")
    if not dghs_ok:
        return (
            "dghs_profile_unreachable_keep_open",
            "DGHS public profile was not retrieved in this run; keep the row open and retry before interpreting the candidate.",
        )
    if not osm_ok:
        return (
            "osm_candidate_unreachable_keep_open",
            "The OSM candidate API record was not retrieved in this run; keep the row open and retry before interpreting the candidate.",
        )
    if focus_class == "start_here_zero_osm_upazila_queue":
        return (
            "zero_osm_context_candidate_outside_upazila_keep_open",
            "The nearest public-map candidate is context for an upazila observability gap, not row-level evidence of the DGHS facility.",
        )
    if inspection_lane == "source_repair_first":
        return (
            "source_repair_public_sources_retrieved_keep_open",
            "Public sources are reachable, but the duplicate-coordinate or source-repair question must be resolved before any map absence label.",
        )
    if inspection_lane == "possible_public_map_match_or_buffer_case" or osm_name_score >= 0.75:
        return (
            "possible_same_facility_candidate_needs_manual_location_check",
            "Public sources retrieve a plausible named candidate, but manual location or official-source confirmation is required before reclassification.",
        )
    return (
        "candidate_feature_retrieved_but_name_conflict_keep_open",
        "Public sources retrieve the candidate feature, but the name support is not strong enough for a row-level label without manual confirmation.",
    )


def count_rows(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    counter = Counter(str(row.get(key, "")) for row in rows)
    return [{"name": name, "rows": int(counter[name])} for name in sorted(counter) if name]


def main() -> None:
    if not IN_INSPECTION_SUMMARY_JSON.exists():
        raise FileNotFoundError(IN_INSPECTION_SUMMARY_JSON)

    inspection_summary = read_json(IN_INSPECTION_SUMMARY_JSON)
    source_rows = inspection_summary.get("row_card_rows", [])[:ROW_LIMIT]
    retrieved_at = now_utc()
    output_rows: list[dict[str, Any]] = []

    for index, row in enumerate(source_rows, start=1):
        dghs_url = str(row.get("dghs_public_profile_url") or "")
        candidate_url = str(row.get("candidate_feature_1_url") or "")
        candidate_api_url = osm_api_url(candidate_url)

        dghs_fetch = fetch_url(dghs_url)
        time.sleep(0.15)
        osm_fetch = fetch_url(candidate_api_url)
        time.sleep(0.15)

        osm_payload = parse_osm_payload(osm_fetch.get("body", ""))
        osm_name = str(osm_payload.get("name") or row.get("candidate_feature_1_name") or "")
        osm_name_score_live = name_support_score(str(row.get("facility_name") or ""), osm_name)
        profile = profile_signal(row, dghs_fetch.get("body", ""))
        lane, evidence_needed = confirmation_lane(
            row,
            bool(dghs_fetch.get("ok")),
            bool(osm_fetch.get("ok")),
            osm_name_score_live,
        )

        output_rows.append(
            {
                "confirmation_id": f"PSDQ-BGD-PSC-{index:03d}",
                "confirmation_rank": index,
                "confirmation_method": METHOD,
                "retrieved_at": retrieved_at,
                "attestation_chain": "ai-first",
                "inspection_id": row.get("inspection_id", ""),
                "inspection_rank": row.get("inspection_rank", ""),
                "focus_class": row.get("focus_class", ""),
                "facility_name": row.get("facility_name", ""),
                "facility_type_name": row.get("facility_type_name", ""),
                "district_name": row.get("district_name", ""),
                "upazila_name": row.get("upazila_name", ""),
                "priority_scope": row.get("priority_scope", ""),
                "inspection_lane": row.get("inspection_lane", ""),
                "inspection_decision": row.get("inspection_decision", ""),
                "dghs_public_profile_url": dghs_url,
                "dghs_profile_http_status": dghs_fetch.get("status", ""),
                "dghs_profile_retrieved": bool(dghs_fetch.get("ok")),
                "dghs_profile_final_url": dghs_fetch.get("final_url", ""),
                "dghs_profile_error": dghs_fetch.get("error", ""),
                **profile,
                "candidate_feature_url": candidate_url,
                "candidate_osm_api_url": candidate_api_url,
                "candidate_osm_api_http_status": osm_fetch.get("status", ""),
                "candidate_osm_api_retrieved": bool(osm_fetch.get("ok")),
                "candidate_osm_api_error": osm_fetch.get("error", ""),
                "candidate_osm_type": osm_payload.get("element_type", ""),
                "candidate_osm_id": osm_payload.get("element_id", ""),
                "candidate_osm_name_from_api": osm_payload.get("name", ""),
                "candidate_osm_lat": osm_payload.get("lat", ""),
                "candidate_osm_lon": osm_payload.get("lon", ""),
                "candidate_osm_tags_compact": compact_tags(osm_payload.get("tags", {})),
                "candidate_distance_m_from_inspection": row.get("candidate_feature_1_distance_m", ""),
                "candidate_name_score_from_inspection": row.get("candidate_feature_1_name_score", ""),
                "candidate_name_score_from_live_tags": osm_name_score_live,
                "public_source_confirmation_lane": lane,
                "confirmation_decision": "keep_open_public_source_confirmation_required",
                "rows_closed_as_resolved": 0,
                "rows_reclassified_as_same_facility": 0,
                "evidence_needed_next": evidence_needed,
                "source_basis": "Live public DGHS profile URL and public OSM API feature URL, recorded with HTTP status and retrieval timestamp.",
                "non_claim": NON_CLAIM,
            }
        )

    fields = [
        "confirmation_id",
        "confirmation_rank",
        "confirmation_method",
        "retrieved_at",
        "attestation_chain",
        "inspection_id",
        "inspection_rank",
        "focus_class",
        "facility_name",
        "facility_type_name",
        "district_name",
        "upazila_name",
        "priority_scope",
        "inspection_lane",
        "inspection_decision",
        "dghs_public_profile_url",
        "dghs_profile_http_status",
        "dghs_profile_retrieved",
        "dghs_profile_final_url",
        "dghs_profile_error",
        "dghs_profile_facility_token_coverage",
        "dghs_profile_public_name_token_coverage",
        "dghs_profile_contains_profile_id",
        "candidate_feature_url",
        "candidate_osm_api_url",
        "candidate_osm_api_http_status",
        "candidate_osm_api_retrieved",
        "candidate_osm_api_error",
        "candidate_osm_type",
        "candidate_osm_id",
        "candidate_osm_name_from_api",
        "candidate_osm_lat",
        "candidate_osm_lon",
        "candidate_osm_tags_compact",
        "candidate_distance_m_from_inspection",
        "candidate_name_score_from_inspection",
        "candidate_name_score_from_live_tags",
        "public_source_confirmation_lane",
        "confirmation_decision",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "evidence_needed_next",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_CONFIRMATION_CSV, output_rows, fields)

    summary = {
        "generated_at": now_utc(),
        "retrieved_at": retrieved_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 first-row public-source confirmation packet",
        "unit": "sampled DGHS public-map-gap row from targeted inspection queue",
        "source_inputs": [
            {
                "path": str(IN_INSPECTION_SUMMARY_JSON.relative_to(ROOT)),
                "role": "targeted public-map inspection summary",
            }
        ],
        "confirmation_scope": {
            "rows_checked": len(output_rows),
            "dghs_profiles_retrieved": sum(1 for row in output_rows if row["dghs_profile_retrieved"]),
            "osm_candidate_api_records_retrieved": sum(1 for row in output_rows if row["candidate_osm_api_retrieved"]),
            "rows_with_dghs_profile_token_support": sum(
                1
                for row in output_rows
                if float(row["dghs_profile_facility_token_coverage"] or 0) >= 0.5
                or float(row["dghs_profile_public_name_token_coverage"] or 0) >= 0.5
            ),
            "rows_with_candidate_name_score_at_least_0_75": sum(
                1 for row in output_rows if float(row["candidate_name_score_from_live_tags"] or 0) >= 0.75
            ),
            "rows_kept_open": len(output_rows),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "public_source_confirmation_lane_counts": count_rows(output_rows, "public_source_confirmation_lane"),
        "inspection_lane_counts": count_rows(output_rows, "inspection_lane"),
        "focus_class_counts": count_rows(output_rows, "focus_class"),
        "row_card_rows": [
            {
                "confirmation_id": row["confirmation_id"],
                "confirmation_rank": row["confirmation_rank"],
                "inspection_id": row["inspection_id"],
                "facility_name": row["facility_name"],
                "district_name": row["district_name"],
                "upazila_name": row["upazila_name"],
                "inspection_lane": row["inspection_lane"],
                "public_source_confirmation_lane": row["public_source_confirmation_lane"],
                "dghs_profile_retrieved": row["dghs_profile_retrieved"],
                "dghs_profile_facility_token_coverage": row["dghs_profile_facility_token_coverage"],
                "candidate_osm_api_retrieved": row["candidate_osm_api_retrieved"],
                "candidate_osm_name_from_api": row["candidate_osm_name_from_api"],
                "candidate_name_score_from_live_tags": row["candidate_name_score_from_live_tags"],
                "candidate_distance_m_from_inspection": row["candidate_distance_m_from_inspection"],
                "dghs_public_profile_url": row["dghs_public_profile_url"],
                "candidate_feature_url": row["candidate_feature_url"],
                "candidate_osm_api_url": row["candidate_osm_api_url"],
                "evidence_needed_next": row["evidence_needed_next"],
            }
            for row in output_rows
        ],
        "confirmation_notes": [
            "This packet records public-source retrieval and tag support for the first targeted inspection rows.",
            "Every row remains open because API retrieval and name support are not by themselves human validation.",
            "Rows with plausible same-facility signals need manual location or official-source confirmation before reclassification.",
            "Zero-OSM upazila rows remain observability cases unless a public source identifies the DGHS facility at the coordinate.",
        ],
        "non_claim": NON_CLAIM,
    }
    write_json(OUT_CONFIRMATION_SUMMARY_JSON, summary)

    print(
        "Built BGD first-row public-source confirmation: "
        f"{len(output_rows)} rows, "
        f"{summary['confirmation_scope']['dghs_profiles_retrieved']} DGHS profiles retrieved, "
        f"{summary['confirmation_scope']['osm_candidate_api_records_retrieved']} OSM API records retrieved, "
        "0 closed."
    )
    print(f"Wrote {OUT_CONFIRMATION_CSV}")
    print(f"Wrote {OUT_CONFIRMATION_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
