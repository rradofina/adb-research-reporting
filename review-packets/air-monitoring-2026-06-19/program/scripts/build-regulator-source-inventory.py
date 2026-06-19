"""Build a regulator-source inventory for the air-monitoring upgrade queue.

This is a source-discovery artifact. It records public source candidates for
regulator inventories and monitor-grade validation; it does not validate station
coverage or count monitors on the ground.
"""

from __future__ import annotations

import csv
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PROGRAM_DIR.parent
SEED_PATH = PROGRAM_DIR / "source-inputs" / "regulator-source-inventory-seed.csv"
STATION_SUMMARY_PATH = PROGRAM_DIR / "generated" / "air-monitoring-openaq-station-metadata-summary.json"
OUTPUT_CSV = PROGRAM_DIR / "generated" / "air-monitoring-regulator-source-inventory.csv"
OUTPUT_JSON = PROGRAM_DIR / "generated" / "air-monitoring-regulator-source-inventory-summary.json"

METHOD = "air_monitoring_regulator_source_inventory_v1"
USER_AGENT = "ADB-Research-Factory/1.0 regulator-source-inventory"
TIMEOUT_SECONDS = 18

OFFICIAL_SOURCE_CLASSES = {
    "official_station_inventory",
    "official_air_quality_portal",
    "official_station_plan",
}


@dataclass
class Retrieval:
    retrieval_status: str
    http_status: int | None
    content_type: str | None
    final_url: str | None
    error: str | None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fetch_status(url: str) -> Retrieval:
    if not url:
        return Retrieval("not_applicable_no_url", None, None, None, None)

    headers = {"User-Agent": USER_AGENT}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return Retrieval(
                    retrieval_status="retrieved",
                    http_status=response.status,
                    content_type=response.headers.get("content-type"),
                    final_url=response.geturl(),
                    error=None,
                )
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405, 406, 501}:
                continue
            return Retrieval(
                retrieval_status="http_error",
                http_status=exc.code,
                content_type=exc.headers.get("content-type") if exc.headers else None,
                final_url=exc.geturl(),
                error=str(exc),
            )
        except Exception as exc:  # noqa: BLE001 - retrieval diagnostics are data here.
            if method == "HEAD":
                continue
            return Retrieval(
                retrieval_status="retrieval_error",
                http_status=None,
                content_type=None,
                final_url=None,
                error=f"{type(exc).__name__}: {exc}",
            )

    return Retrieval("retrieval_error", None, None, None, "No retrieval attempt completed")


def normalize_bool_signal(value: str) -> bool:
    return value.strip().lower() in {"yes", "planned", "partial", "likely"}


def normalize_monitor_grade_signal(value: str) -> bool:
    return value.strip().lower() == "yes"


def main() -> int:
    generated_at = now_iso()
    seed_rows = read_csv(SEED_PATH)
    station_summary = read_json(STATION_SUMMARY_PATH)

    seed_by_iso = {row["iso3"]: row for row in seed_rows}
    country_rows = station_summary["country_rows"]
    missing = [row["iso3"] for row in country_rows if row["iso3"] not in seed_by_iso]
    extra = [iso3 for iso3 in seed_by_iso if iso3 not in {row["iso3"] for row in country_rows}]
    if missing or extra:
        raise SystemExit(f"Seed/target mismatch. missing={missing}; extra={extra}")

    output_rows: list[dict[str, Any]] = []
    for country in country_rows:
        seed = seed_by_iso[country["iso3"]]
        retrieval = fetch_status(seed.get("url", "").strip())
        source_class = seed["source_class"]
        source_tier = seed["source_tier"]
        station_signal = seed["station_inventory_signal"]
        monitor_grade_signal = seed["monitor_grade_signal"]
        pm25_signal = seed["pm25_signal"]
        output_rows.append(
            {
                "generated_at": generated_at,
                "attestation_chain": "ai-first",
                "status": "computed",
                "method": METHOD,
                "iso3": country["iso3"],
                "iso2": country["iso2"],
                "country": country["country"],
                "subregion": country["subregion"],
                "upgrade_queue_class": country["upgrade_queue_class"],
                "openaq_pm25_rows": country["openaq_pm25_locations_fetched"],
                "openaq_zero_pm25_rows": country["openaq_pm25_locations_fetched"] == 0,
                "source_name": seed["source_name"],
                "agency": seed["agency"],
                "url": seed["url"],
                "source_tier": source_tier,
                "source_class": source_class,
                "official_source_candidate": source_tier.startswith("official"),
                "official_station_inventory_or_portal": source_class in OFFICIAL_SOURCE_CLASSES,
                "station_inventory_signal": station_signal,
                "station_inventory_signal_present": normalize_bool_signal(station_signal),
                "monitor_grade_signal": monitor_grade_signal,
                "monitor_grade_signal_present": normalize_monitor_grade_signal(monitor_grade_signal),
                "pm25_signal": pm25_signal,
                "pm25_signal_present": normalize_bool_signal(pm25_signal),
                "official_station_count_claim": seed["official_station_count_claim"],
                "official_station_count_claim_present": bool(seed["official_station_count_claim"].strip()),
                "source_note": seed["source_note"],
                "next_validation_step": seed["next_validation_step"],
                "search_query": seed["search_query"],
                **asdict(retrieval),
                "non_claim": (
                    "This is a regulator-source discovery pass. It does not validate monitor grade, "
                    "does not prove no monitor exists, does not reconcile source station counts with "
                    "OpenAQ rows, and does not compute station-radius population coverage."
                ),
            }
        )

    counts = {
        "economies_targeted": len(output_rows),
        "economies_with_official_source_candidate": sum(row["official_source_candidate"] for row in output_rows),
        "economies_with_official_station_inventory_or_portal": sum(
            row["official_station_inventory_or_portal"] for row in output_rows
        ),
        "economies_with_official_station_count_claim": sum(
            row["official_station_count_claim_present"] for row in output_rows
        ),
        "economies_with_monitor_grade_signal": sum(row["monitor_grade_signal_present"] for row in output_rows),
        "economies_with_pm25_signal": sum(row["pm25_signal_present"] for row in output_rows),
        "zero_openaq_economies_targeted": sum(row["openaq_zero_pm25_rows"] for row in output_rows),
        "zero_openaq_economies_with_official_station_inventory_or_portal": sum(
            row["openaq_zero_pm25_rows"] and row["official_station_inventory_or_portal"] for row in output_rows
        ),
        "zero_openaq_economies_with_official_regulator_page_no_station_inventory": sum(
            row["openaq_zero_pm25_rows"]
            and row["source_class"] == "official_regulator_page_no_station_inventory"
            for row in output_rows
        ),
        "zero_openaq_economies_with_development_partner_monitoring_reference": sum(
            row["openaq_zero_pm25_rows"]
            and row["source_class"] == "development_partner_monitoring_reference"
            for row in output_rows
        ),
        "zero_openaq_economies_not_found_in_targeted_search": sum(
            row["openaq_zero_pm25_rows"] and row["source_class"] == "not_found_in_targeted_search"
            for row in output_rows
        ),
        "economies_not_found_in_targeted_search": sum(
            row["source_class"] == "not_found_in_targeted_search" for row in output_rows
        ),
        "development_partner_or_secondary_reference_rows": sum(
            row["source_tier"] in {"development_partner", "secondary"}
            or row["source_class"] == "development_partner_monitoring_reference"
            for row in output_rows
        ),
        "url_rows": sum(bool(row["url"]) for row in output_rows),
        "url_rows_retrieved": sum(row["retrieval_status"] == "retrieved" for row in output_rows),
        "url_rows_with_retrieval_error": sum(
            row["retrieval_status"] in {"http_error", "retrieval_error"} for row in output_rows
        ),
    }

    evidence_gates = [
        {
            "gate": "Official regulator or portal source candidate",
            "status": "computed",
            "rows": counts["economies_with_official_source_candidate"],
            "reader_use": "Moves beyond OpenAQ by identifying public official sources to inspect.",
        },
        {
            "gate": "Official station inventory or air-quality portal",
            "status": "partly_available",
            "rows": counts["economies_with_official_station_inventory_or_portal"],
            "reader_use": "Candidate source for regulator cross-check; not yet reconciled to OpenAQ rows.",
        },
        {
            "gate": "Official station-count claim",
            "status": "partly_available",
            "rows": counts["economies_with_official_station_count_claim"],
            "reader_use": "A count claim exists in the source note but still needs table extraction and station-level join.",
        },
        {
            "gate": "Monitor-grade classification",
            "status": "not_ready",
            "rows": counts["economies_with_monitor_grade_signal"],
            "reader_use": "No source in this pass reliably classifies all OpenAQ rows by regulatory/reference grade.",
        },
        {
            "gate": "Zero-OpenAQ regulator cross-check",
            "status": "not_ready",
            "rows": counts["zero_openaq_economies_with_official_station_inventory_or_portal"],
            "reader_use": "Only official source candidates; zero-OpenAQ remains not proof of no monitor.",
        },
    ]

    summary = {
        "generated_at": generated_at,
        "program": "air-monitoring",
        "attestation_chain": "ai-first",
        "status": "computed",
        "method": METHOD,
        "goal_level": "L3 regulator-source discovery",
        "source_inputs": [
            {"path": str(SEED_PATH.relative_to(PROGRAM_DIR)), "role": "curated public source candidate seed"},
            {
                "path": str(STATION_SUMMARY_PATH.relative_to(PROGRAM_DIR)),
                "role": "OpenAQ station-metadata target queue and row counts",
            },
        ],
        "coverage_counts": counts,
        "evidence_gate_counts": evidence_gates,
        "country_rows": output_rows,
        "outputs": {
            "csv": str(OUTPUT_CSV.relative_to(PROGRAM_DIR)),
            "summary_json": str(OUTPUT_JSON.relative_to(PROGRAM_DIR)),
        },
        "review_notes": [
            "Official source candidate means a source to inspect, not validated station coverage.",
            "Official station-count claims must be extracted into station-level tables before comparing with OpenAQ.",
            "Zero-OpenAQ economies remain unresolved until regulator inventories or credible official no-monitor statements are found.",
        ],
        "non_claim": (
            "This is a regulator-source discovery pass. It does not validate monitor grade, "
            "does not prove no monitor exists, does not reconcile source station counts with "
            "OpenAQ rows, and does not compute station-radius population coverage."
        ),
    }

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)
    with OUTPUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(
        "Built regulator-source inventory: "
        f"{counts['economies_targeted']} target economies; "
        f"{counts['economies_with_official_station_inventory_or_portal']} official inventory/portal candidates; "
        f"{counts['economies_not_found_in_targeted_search']} targeted-search gaps."
    )
    print(f"Wrote {OUTPUT_CSV.relative_to(REPO_DIR)}")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
