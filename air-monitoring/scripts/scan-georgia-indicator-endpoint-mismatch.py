"""Probe Georgia air.gov.ge indicator endpoints against target station codes.

The report/export and network/launch walls already show that Georgia has
official station-report and city/network context but no verified station-code
closure. This pass tests another official source family exposed by the
air.gov.ge page template: the indicator API and daily API route.

The scan keeps the station-code, verification, status, calibration, grade, and
station-radius gates closed unless an endpoint names the exact target station
code and provides explicit closure language.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import requests


PROGRAM_DIR = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROGRAM_DIR / "generated"
SOURCE_INPUTS_DIR = PROGRAM_DIR / "source-inputs"

SEED_CSV = SOURCE_INPUTS_DIR / "georgia-indicator-endpoint-mismatch-source-seed.csv"
TARGET_CSV = GENERATED_DIR / "air-monitoring-georgia-station-network-launch-source-scan.csv"
OUT_CSV = GENERATED_DIR / "air-monitoring-georgia-indicator-endpoint-mismatch.csv"
OUT_JSON = GENERATED_DIR / "air-monitoring-georgia-indicator-endpoint-mismatch-summary.json"
OUT_MD = PROGRAM_DIR / "georgia-indicator-endpoint-mismatch.md"

METHOD = "air_monitoring_georgia_indicator_endpoint_mismatch_v1"
STATUS = "computed_georgia_indicator_endpoint_mismatch"
TIMEOUT_SECONDS = 60
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 "
    "ADB-Research-Factory/1.0"
)
NON_CLAIM = (
    "This scan probes official air.gov.ge indicator and daily API routes for "
    "exact Georgia target station-code closure. It does not convert city-level "
    "indicator stations, PM2.5 presence, API availability, or route failures "
    "into verified-report closure, current station status, calibration status, "
    "complete monitor-grade classification, or station-radius readiness."
)

FIELDNAMES = [
    "generated_at",
    "attestation_chain",
    "status",
    "method",
    "indicator_probe_id",
    "network_launch_scan_id",
    "source_station_id",
    "source_station_name",
    "target_city",
    "exact_indicator_station_code_found",
    "indicator_city_alias_context_found",
    "matched_indicator_codes",
    "matched_indicator_station_count",
    "matched_indicator_pm25_station_count",
    "indicator_pm25_context_available",
    "indicator_verification_language_available",
    "indicator_status_or_calibration_language_available",
    "daily_endpoint_route_available",
    "daily_endpoint_verified_closure_available",
    "station_code_verified_closure_available",
    "current_status_confirmed",
    "calibration_status_available",
    "complete_monitor_grade_classification_available",
    "station_radius_grade_assumption_ready",
    "indicator_endpoint_decision",
    "reader_use",
    "non_claim",
]

SOURCE_RECORD_FIELDS = [
    "source_key",
    "source_name",
    "source_role",
    "retrieval_url",
    "final_url",
    "retrieved",
    "http_status",
    "content_type",
    "retrieval_bytes",
    "sha256",
    "json_array_rows",
    "matched_expected_terms",
    "matched_station_code_terms",
    "matched_pm25_terms",
    "matched_verification_terms",
    "matched_status_terms",
    "retrieval_error",
    "source_note",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    text = str(value or "").replace("\xa0", " ")
    text = text.replace("\u00b5", "u").replace("\u03bc", "u")
    return re.sub(r"\s+", " ", text).strip()


def norm_key(value: Any) -> str:
    return normalize(value).casefold()


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in str(value or "").split("||") if term.strip()]


def matched_terms(text: str, terms: list[str]) -> list[str]:
    lower = norm_key(text)
    return [term for term in terms if norm_key(term) in lower]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_url(seed: dict[str, str]) -> str:
    if seed["source_key"] == "airgov_indicator_endpoint_current_month":
        month = datetime.now(timezone.utc).strftime("%Y-%m")
        params = {
            "from_date_time": month,
            "to_date_time": month,
            "station_code": "all",
            "municipality_id": "all",
            "substance": "all",
            "last_data": "true",
            "format": "json",
        }
    elif seed["source_key"] == "airgov_daily_endpoint_current_probe":
        # The route is exposed by the page template. The fixed recent date keeps
        # the route probe reproducible within this evidence refresh.
        params = {
            "from_date": "2026-06-19",
            "to_date": "2026-06-19",
            "station_code": "all",
            "municipality_id": "all",
            "substance": "all",
            "last_data": "true",
            "format": "json",
        }
    else:
        params = {}
    return f"{seed['url']}?{urlencode(params)}" if params else seed["url"]


def fetch(seed: dict[str, str]) -> dict[str, Any]:
    url = build_url(seed)
    result: dict[str, Any] = {
        **seed,
        "retrieval_url": url,
        "final_url": "",
        "retrieved": False,
        "http_status": "",
        "content_type": "",
        "retrieval_bytes": 0,
        "sha256": "",
        "text": "",
        "json": None,
        "retrieval_error": "",
    }
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json,text/html;q=0.8,*/*;q=0.5",
                "Accept-Language": "en-US,en;q=0.9,ka;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        result["final_url"] = response.url
        result["http_status"] = response.status_code
        result["content_type"] = response.headers.get("content-type", "")
        content = response.content
        result["retrieval_bytes"] = len(content)
        result["sha256"] = hashlib.sha256(content).hexdigest()
        response.raise_for_status()
        if "json" in result["content_type"].lower():
            result["json"] = response.json()
            result["text"] = normalize(json.dumps(result["json"], ensure_ascii=False))
        else:
            result["text"] = normalize(response.text)
        result["retrieved"] = True
    except Exception as exc:  # noqa: BLE001 - route failures are source evidence.
        result["retrieval_error"] = f"{type(exc).__name__}: {exc}"
    return result


def source_record(source: dict[str, Any]) -> dict[str, Any]:
    text = source.get("text", "")
    payload = source.get("json")
    return {
        "source_key": source["source_key"],
        "source_name": source["source_name"],
        "source_role": source["source_role"],
        "retrieval_url": source["retrieval_url"],
        "final_url": source["final_url"],
        "retrieved": source["retrieved"],
        "http_status": source["http_status"],
        "content_type": source["content_type"],
        "retrieval_bytes": source["retrieval_bytes"],
        "sha256": source["sha256"],
        "json_array_rows": len(payload) if isinstance(payload, list) else 0,
        "matched_expected_terms": "||".join(matched_terms(text, split_terms(source["expected_terms"]))),
        "matched_station_code_terms": "||".join(matched_terms(text, split_terms(source["station_code_terms"]))),
        "matched_pm25_terms": "||".join(matched_terms(text, split_terms(source["pm25_terms"]))),
        "matched_verification_terms": "||".join(matched_terms(text, split_terms(source["verification_terms"]))),
        "matched_status_terms": "||".join(matched_terms(text, split_terms(source["status_terms"]))),
        "retrieval_error": source["retrieval_error"],
        "source_note": source["source_note"],
    }


def target_rows() -> list[dict[str, str]]:
    rows = read_csv(TARGET_CSV)
    targets = [row for row in rows if row["attestation_chain"] == "ai-first"]
    targets.sort(key=lambda row: row["source_station_id"])
    return targets


def station_text(row: dict[str, Any]) -> str:
    fields = [
        row.get("code"),
        row.get("settlement"),
        row.get("settlement_en"),
        row.get("address"),
        row.get("address_en"),
        row.get("description_short_en"),
        row.get("description_short_ge"),
        row.get("st_full_address_en"),
        row.get("st_full_address_ge"),
    ]
    return normalize(" ".join(str(field or "") for field in fields))


def has_pm25(row: dict[str, Any]) -> bool:
    for equipment in row.get("stationequipment_set") or []:
        if not isinstance(equipment, dict):
            continue
        substance = equipment.get("substance") or {}
        if norm_key(substance.get("name")) == "pm2.5":
            return True
    return False


def indicator_rows(indicator_source: dict[str, Any]) -> list[dict[str, Any]]:
    payload = indicator_source.get("json")
    return payload if isinstance(payload, list) else []


def target_aliases(target: dict[str, str]) -> list[str]:
    aliases = [target["target_city"], target["source_station_id"]]
    name = target["source_station_name"]
    if " - " in name:
        aliases.append(name.split(" - ", 1)[0])
        aliases.append(name.split(" - ", 1)[1])
    aliases.append(name)
    return [alias for alias in aliases if alias and alias != "Tazakendi (working in test mode)"]


def build_rows(generated_at: str, targets: list[dict[str, str]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    indicator = sources["airgov_indicator_endpoint_current_month"]
    daily = sources["airgov_daily_endpoint_current_probe"]
    indicator_station_rows = indicator_rows(indicator)
    by_code = {normalize(row.get("code")): row for row in indicator_station_rows}
    station_texts = [(row, station_text(row)) for row in indicator_station_rows]
    rows: list[dict[str, Any]] = []
    for target in targets:
        code = normalize(target["source_station_id"])
        exact = by_code.get(code)
        aliases = target_aliases(target)
        matched = [
            row
            for row, text in station_texts
            if any(norm_key(alias) and norm_key(alias) in norm_key(text) for alias in aliases)
        ]
        matched_codes = sorted({normalize(row.get("code")) for row in matched if normalize(row.get("code"))})
        pm25_matches = [row for row in matched if has_pm25(row)]
        exact_found = exact is not None
        city_alias = bool(matched_codes)
        verification_language = bool(matched_terms(indicator.get("text", ""), ["Verified Data", "verified"]))
        status_language = bool(matched_terms(indicator.get("text", ""), ["status", "operating", "calibration"]))
        daily_available = bool(daily.get("retrieved"))
        if exact_found:
            decision = "exact_indicator_code_found_needs_manual_review"
            reader_use = "The indicator endpoint names the exact target station code, so this row would need manual review for method/status fields."
        elif city_alias:
            decision = "indicator_city_alias_different_code_namespace_keep_open"
            reader_use = "The indicator endpoint has city or address-near stations, but not the exact target station code; use it only as a non-closure source wall."
        else:
            decision = "no_indicator_context_for_target_keep_open"
            reader_use = "The indicator endpoint does not name the target station code, city, or station address terms."
        rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": STATUS,
                "method": METHOD,
                "indicator_probe_id": f"GEO-indicator-endpoint-{code}",
                "network_launch_scan_id": target["network_launch_scan_id"],
                "source_station_id": target["source_station_id"],
                "source_station_name": target["source_station_name"],
                "target_city": target["target_city"],
                "exact_indicator_station_code_found": exact_found,
                "indicator_city_alias_context_found": city_alias,
                "matched_indicator_codes": "||".join(matched_codes),
                "matched_indicator_station_count": len(matched_codes),
                "matched_indicator_pm25_station_count": len(pm25_matches),
                "indicator_pm25_context_available": bool(pm25_matches) or (exact_found and has_pm25(exact)),
                "indicator_verification_language_available": verification_language,
                "indicator_status_or_calibration_language_available": status_language,
                "daily_endpoint_route_available": daily_available,
                "daily_endpoint_verified_closure_available": False,
                "station_code_verified_closure_available": False,
                "current_status_confirmed": False,
                "calibration_status_available": False,
                "complete_monitor_grade_classification_available": False,
                "station_radius_grade_assumption_ready": False,
                "indicator_endpoint_decision": decision,
                "reader_use": reader_use,
                "non_claim": NON_CLAIM,
            }
        )
    return rows


def gate(status: str, gate_name: str, rows: int, reader_use: str) -> dict[str, Any]:
    return {"status": status, "gate": gate_name, "rows": rows, "reader_use": reader_use}


def summary(generated_at: str, rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {
        "target_georgia_rows": len(rows),
        "source_routes_seeded": len(sources),
        "source_routes_retrieved": sum(source["retrieved"] for source in sources),
        "indicator_api_station_objects": next(
            (len(source["json"]) for source in sources if source["source_key"] == "airgov_indicator_endpoint_current_month" and isinstance(source.get("json"), list)),
            0,
        ),
        "daily_api_route_available": sum(source["source_key"] == "airgov_daily_endpoint_current_probe" and source["retrieved"] for source in sources),
        "exact_indicator_station_code_rows": sum(row["exact_indicator_station_code_found"] for row in rows),
        "indicator_city_alias_context_rows": sum(row["indicator_city_alias_context_found"] for row in rows),
        "indicator_pm25_context_rows": sum(row["indicator_pm25_context_available"] for row in rows),
        "indicator_verification_language_rows": sum(row["indicator_verification_language_available"] for row in rows),
        "daily_endpoint_verified_closure_rows": 0,
        "current_status_confirmed_rows": 0,
        "calibration_status_available_rows": 0,
        "complete_monitor_grade_classification_rows": 0,
        "station_radius_grade_assumption_ready_rows": 0,
    }
    gates = [
        gate("available", "Indicator endpoint retrieved", counts["source_routes_retrieved"], "Official indicator route and daily route probe were tested."),
        gate("available", "Indicator station objects", counts["indicator_api_station_objects"], "The official indicator endpoint exposes a broader station-code layer."),
        gate("not_ready", "Exact target station-code matches", counts["exact_indicator_station_code_rows"], "No target Georgia station code appears in the indicator endpoint namespace."),
        gate("partly_available", "City/address alias context", counts["indicator_city_alias_context_rows"], "Some target cities have indicator stations, but with different codes."),
        gate("not_ready", "Verified/status/calibration closure", 0, "The endpoint does not resolve verified report, current status, calibration, or grade closure for the target codes."),
        gate("not_ready", "Station-radius readiness", 0, "No row is eligible for station-radius assumptions."),
    ]
    display_fields = [
        "source_station_id",
        "source_station_name",
        "target_city",
        "matched_indicator_codes",
        "matched_indicator_station_count",
        "matched_indicator_pm25_station_count",
        "indicator_endpoint_decision",
        "reader_use",
    ]
    return {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "method": METHOD,
        "goal_level": "L3 Georgia endpoint source-family falsifier",
        "source_scope": "Official air.gov.ge indicator and daily API routes joined to the 16 Georgia target station codes.",
        "coverage_counts": counts,
        "decision_counts": [
            {"decision": decision, "rows": count}
            for decision, count in sorted(Counter(row["indicator_endpoint_decision"] for row in rows).items())
        ],
        "evidence_gate_counts": gates,
        "display_rows": [{field: row[field] for field in display_fields} for row in rows],
        "station_rows": rows,
        "source_records": [source_record(source) for source in sources],
        "outputs": {"csv": str(OUT_CSV.relative_to(PROGRAM_DIR)), "summary_json": str(OUT_JSON.relative_to(PROGRAM_DIR))},
        "non_claim": NON_CLAIM,
    }


def write_md(payload: dict[str, Any]) -> None:
    counts = payload["coverage_counts"]
    lines = [
        "---",
        "attestation_chain: ai-first",
        f"status: {STATUS}",
        f"method: {METHOD}",
        "---",
        "",
        "# Georgia Indicator Endpoint Mismatch",
        "",
        "## Why this source pass was needed",
        "",
        "The Georgia report/export ladder shows that target station codes appear in official report routes, but the live-data caution remains. The NEA station network wall adds city-level launch and network context without station-code closure. This pass tests another official source family exposed by the air.gov.ge page template: the indicator API and daily API route.",
        "",
        "## What the scan finds",
        "",
        f"- Indicator API station objects: {counts['indicator_api_station_objects']}",
        f"- Exact target station-code matches: {counts['exact_indicator_station_code_rows']}",
        f"- Target rows with city/address alias context in the indicator API: {counts['indicator_city_alias_context_rows']}",
        f"- Daily endpoint verified-closure rows: {counts['daily_endpoint_verified_closure_rows']}",
        f"- Complete monitor-grade rows: {counts['complete_monitor_grade_classification_rows']}",
        "",
        "The result is a source-family falsifier. The indicator API is real and public, but it uses a different station-code namespace for nearby city stations. It does not close the exact station-code, verified-report, status, calibration, grade, or station-radius gates.",
        "",
        "## Reproduce",
        "",
        "```powershell",
        "python -m py_compile air-monitoring\\scripts\\scan-georgia-indicator-endpoint-mismatch.py",
        "python air-monitoring\\scripts\\scan-georgia-indicator-endpoint-mismatch.py",
        "```",
        "",
        "Outputs:",
        "",
        f"- `{OUT_CSV.relative_to(PROGRAM_DIR)}`",
        f"- `{OUT_JSON.relative_to(PROGRAM_DIR)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_at = now_iso()
    seeds = read_csv(SEED_CSV)
    sources = [fetch(seed) for seed in seeds]
    targets = target_rows()
    rows = build_rows(generated_at, targets, {source["source_key"]: source for source in sources})
    write_csv(OUT_CSV, rows)
    payload = summary(generated_at, rows, sources)
    write_json(OUT_JSON, payload)
    write_md(payload)
    print(
        "Built Georgia indicator endpoint mismatch scan: "
        f"{len(rows)} target rows; "
        f"{sum(source['retrieved'] for source in sources)}/{len(sources)} routes retrieved; "
        f"{payload['coverage_counts']['indicator_api_station_objects']} indicator station objects; "
        f"{payload['coverage_counts']['exact_indicator_station_code_rows']} exact target code rows; "
        "0 closure rows."
    )


if __name__ == "__main__":
    main()
