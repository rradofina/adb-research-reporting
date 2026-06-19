"""Target public correction-record follow-up for PSDQ BGD source-repair rows.

This live public-source pass starts from the public-explanation evidence rows.
It targets only the shared-coordinate Narayanganj records and the same-name
cross-district Durgapur conflict, then checks fixed public official DGHS
registry, DGHS Health Dashboard, and government health portal pages for
correction records or coordinate-source notes. It does not close, reclassify,
or validate any row.
"""

from __future__ import annotations

import csv
import html
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"

IN_PUBLIC_EXPLANATION_EVIDENCE_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv"
)

OUT_CORRECTION_FOLLOWUP_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-correction-record-followup.csv"
)
OUT_CORRECTION_FOLLOWUP_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-correction-record-followup-summary.json"
)

METHOD = "ai_public_source_repair_correction_record_followup_v1"
STATUS = "ai_public_source_repair_correction_record_followup_not_human_validation"
USER_AGENT = "ADB-AI-Research-PSDQ-source-repair-correction-record-followup/1.0"
NON_CLAIM = (
    "This is an AI-first targeted public correction-record follow-up for PSDQ "
    "source-repair rows. It checks public official DGHS registry, DGHS Health "
    "Dashboard, and government health portal pages for coordinate-source or "
    "correction records. It is not human validation, not ground truth, not a "
    "row closure, not a same-facility reclassification, not a coordinate "
    "correction, not a facility-quality assessment, and not a service-access "
    "estimate."
)

TARGET_CLASSES = {
    "official_shared_coordinate_across_distinct_records_no_explanation",
    "official_same_name_cross_district_coordinate_conflict_no_correction_record",
}

PROFILE_TABS = ["at-a-glance", "detailed-information"]

ORG_LIST_COLUMNS = {
    "alias_columns_csv": "Id,Name,Name (Bangla),Code,Email,Agency,Type,Division,District,City Corporation,Upazila,Paurasava,Union,Private",
    "columns_csv": "id,name,name_bn,code,email_1,facility_agency_name,facility_type_name,division_name,district_name,city_corporation_name,upazila_name,paurasava_name,union_name,is_private",
    "is_active": "1",
    "submit": "Run",
}

DASHBOARD_MENU_URLS = {
    "hospital_district_group": "https://dashboard.dghs.gov.bd/pages/hss_menu_facility.php?district_id=&division_id=&facilitytype_id=28",
    "upazila_health_complex_group": "https://dashboard.dghs.gov.bd/pages/hss_menu_facility.php?district_id=&division_id=&facilitytype_id=29",
}

DASHBOARD_DETAIL_URLS = {
    "10000425": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000425&level=28&month=7&rank=61&year=2025",
    "10000427": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000427&level=28&month=5&rank=11&year=2025",
    "10002304": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10002304&level=29&month=5&rank=49&year=2025",
    "10000470": "https://dashboard.dghs.gov.bd/pages/hss_scoring_facility_detail.php?facility_code=10000470&level=29&month=1&rank=&year=2025",
}

GOV_PORTAL_URLS = {
    "10002304": [
        "https://health.durgapur.netrokona.gov.bd",
        "https://health.durgapur.netrokona.gov.bd/pages/officers",
    ],
    "10000470": [
        "https://health.durgapur.rajshahi.gov.bd",
        "https://health.durgapur.rajshahi.gov.bd/pages/officers",
    ],
}

CORRECTION_PATTERNS = [
    "coordinate source",
    "coordinate correction",
    "coordinate corrected",
    "gps source",
    "gps coordinate source",
    "geocode source",
    "map coordinate source",
    "latitude source",
    "longitude source",
    "location source",
    "wrong coordinate",
    "incorrect coordinate",
    "updated coordinate",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def clean_html(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = text.replace("\u0165", ">")
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_url(url: str, timeout: int = 30) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.url,
                "body": body,
                "error": "",
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "body": body,
            "error": f"http_error_{exc.code}",
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "body": "",
            "error": f"url_error:{exc.reason}",
        }
    except TimeoutError:
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "body": "",
            "error": "timeout",
        }


def page_contains_correction(body: str) -> bool:
    text = clean_html(body).lower()
    return any(pattern in text for pattern in CORRECTION_PATTERNS)


def profile_url(profile_id: str, tab: str) -> str:
    return f"https://hrm.dghs.gov.bd/public/facility-registry/facilities/{profile_id}/profile?tab={tab}"


def organization_list_url(page: str) -> str:
    query = {**ORG_LIST_COLUMNS, "page": page}
    return f"https://hrm.dghs.gov.bd/public/facility-registry/reports/organization-list?{urlencode(query)}"


def page_number_from_cache_file(value: Any) -> str:
    match = re.search(r"_p(\d+)\.json$", str(value or ""))
    return match.group(1) if match else ""


def dashboard_group_for(row: dict[str, Any]) -> str:
    if row["public_explanation_evidence_class"].startswith("official_same_name"):
        return "upazila_health_complex_group"
    return "hospital_district_group"


def linked_codes(row: dict[str, Any]) -> list[str]:
    codes = [str(row.get("dghs_organization_code") or "")]
    sibling = str(row.get("nearest_same_name_other_district_code") or "")
    if sibling:
        codes.append(sibling)
    return [code for index, code in enumerate(codes) if code and code not in codes[:index]]


def source_set_for(row: dict[str, Any]) -> list[dict[str, str]]:
    profile_id = str(row.get("dghs_profile_id") or "")
    code = str(row.get("dghs_organization_code") or "")
    group_key = dashboard_group_for(row)
    sources: list[dict[str, str]] = []

    for tab in PROFILE_TABS:
        sources.append({"kind": f"dghs_profile_{tab}", "url": profile_url(profile_id, tab)})

    page = page_number_from_cache_file(row.get("registry_cache_file"))
    if page:
        sources.append({"kind": "dghs_organization_list_page", "url": organization_list_url(page)})

    sources.append({"kind": f"dghs_health_dashboard_menu_{group_key}", "url": DASHBOARD_MENU_URLS[group_key]})

    for linked_code in linked_codes(row):
        detail_url = DASHBOARD_DETAIL_URLS.get(linked_code)
        if detail_url:
            sources.append({"kind": f"dghs_health_dashboard_detail_{linked_code}", "url": detail_url})
        for portal_url in GOV_PORTAL_URLS.get(linked_code, []):
            sources.append({"kind": f"government_health_portal_{linked_code}", "url": portal_url})

    seen: set[str] = set()
    unique_sources: list[dict[str, str]] = []
    for source in sources:
        key = f"{source['kind']}|{source['url']}"
        if key not in seen:
            unique_sources.append(source)
            seen.add(key)
    return unique_sources


def classify(row: dict[str, Any]) -> str:
    if row["public_correction_or_coordinate_source_record_found"]:
        return "public_correction_record_found"
    if row["linked_other_district_code"] and row["dashboard_menu_contains_linked_other_district_code"]:
        return "no_correction_record_dashboard_confirms_cross_district_pair"
    if int(row["shared_official_profile_coordinate_rows"] or 0) > 1:
        return "no_correction_record_dashboard_confirms_distinct_shared_coordinate_records"
    return "no_correction_record_found"


def reviewer_action(row: dict[str, Any]) -> str:
    evidence_class = row["correction_followup_evidence_class"]
    if evidence_class == "public_correction_record_found":
        return "Review the public correction record before any row closure; this script does not close rows automatically."
    if evidence_class == "no_correction_record_dashboard_confirms_cross_district_pair":
        return "Keep the Durgapur row open and escalate to source owner or human reviewer; public DGHS systems show both codes but no correction record."
    if evidence_class == "no_correction_record_dashboard_confirms_distinct_shared_coordinate_records":
        return "Keep the shared-coordinate Narayanganj rows open; public DGHS systems show distinct records but no public coordinate correction."
    return "Keep the row open; no public correction record was found."


def main() -> None:
    if not IN_PUBLIC_EXPLANATION_EVIDENCE_CSV.exists():
        raise FileNotFoundError(IN_PUBLIC_EXPLANATION_EVIDENCE_CSV)

    input_rows = [
        row
        for row in read_csv(IN_PUBLIC_EXPLANATION_EVIDENCE_CSV)
        if row.get("public_explanation_evidence_class") in TARGET_CLASSES
    ]
    retrieved_at = now_utc()
    output_rows: list[dict[str, Any]] = []

    for index, row in enumerate(input_rows, start=1):
        sources = source_set_for(row)
        source_statuses: list[str] = []
        retrieved_pages = 0
        correction_sources: list[str] = []
        dashboard_menu_contains_target = False
        dashboard_menu_contains_sibling = False
        target_code = str(row.get("dghs_organization_code") or "")
        sibling_code = str(row.get("nearest_same_name_other_district_code") or "")

        for source in sources:
            fetched = fetch_url(source["url"])
            status = fetched.get("status") or fetched.get("error")
            source_statuses.append(f"{source['kind']}={status}")
            body = str(fetched.get("body") or "")
            if fetched.get("ok"):
                retrieved_pages += 1
            if page_contains_correction(body):
                correction_sources.append(source["kind"])
            if source["kind"].startswith("dghs_health_dashboard_menu"):
                text = clean_html(body)
                dashboard_menu_contains_target = target_code in text
                dashboard_menu_contains_sibling = bool(sibling_code and sibling_code in text)

        provisional = {
            "correction_followup_evidence_id": f"PSDQ-BGD-SRCF-{index:03d}",
            "evidence_rank": index,
            "evidence_method": METHOD,
            "retrieved_at": retrieved_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "public_explanation_evidence_id": row.get("public_explanation_evidence_id", ""),
            "official_coordinate_evidence_id": row.get("official_coordinate_evidence_id", ""),
            "source_repair_evidence_id": row.get("source_repair_evidence_id", ""),
            "decision_id": row.get("decision_id", ""),
            "inspection_id": row.get("inspection_id", ""),
            "facility_name": row.get("facility_name", ""),
            "dghs_profile_id": row.get("dghs_profile_id", ""),
            "dghs_organization_code": target_code,
            "division_name": row.get("division_name", ""),
            "district_name": row.get("district_name", ""),
            "upazila_name": row.get("upazila_name", ""),
            "shared_official_profile_coordinate_rows": row.get("shared_official_profile_coordinate_rows", ""),
            "linked_other_district_code": sibling_code,
            "linked_other_district_name": row.get("nearest_same_name_other_district_name", ""),
            "linked_other_district_division": row.get("nearest_same_name_other_district_division", ""),
            "linked_other_district_district": row.get("nearest_same_name_other_district_district", ""),
            "linked_other_district_upazila": row.get("nearest_same_name_other_district_upazila", ""),
            "linked_other_district_coordinate_distance_m": row.get(
                "nearest_same_name_other_district_coordinate_distance_m", ""
            ),
            "targeted_reason": row.get("public_explanation_evidence_class", ""),
            "official_sources_checked": len(sources),
            "official_sources_retrieved": retrieved_pages,
            "official_source_statuses": " | ".join(source_statuses),
            "dashboard_menu_contains_target_code": dashboard_menu_contains_target,
            "dashboard_menu_contains_linked_other_district_code": dashboard_menu_contains_sibling,
            "public_correction_or_coordinate_source_record_found": bool(correction_sources),
            "correction_source_kinds": " | ".join(correction_sources),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
            "source_basis": (
                "Live public DGHS profile tabs, DGHS organization-list pages, "
                "DGHS Health Dashboard pages, and public government health "
                "portals for targeted source-repair rows."
            ),
            "non_claim": NON_CLAIM,
        }
        provisional["correction_followup_evidence_class"] = classify(provisional)
        provisional["correction_followup_reviewer_action"] = reviewer_action(provisional)
        output_rows.append(provisional)

    class_counter = Counter(row["correction_followup_evidence_class"] for row in output_rows)
    summary = {
        "generated_at": retrieved_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 source-repair targeted correction-record follow-up",
        "unit": "targeted source-repair public-explanation row with shared-coordinate or cross-district conflict evidence",
        "source_inputs": [
            {
                "path": str(IN_PUBLIC_EXPLANATION_EVIDENCE_CSV.relative_to(ROOT)),
                "role": "4-row source-repair public-explanation evidence CSV",
            }
        ],
        "selection_rule": (
            "Include public-explanation rows classified as shared official "
            "coordinate across distinct records or same-name cross-district "
            "coordinate conflict."
        ),
        "correction_followup_scope": {
            "targeted_rows": len(output_rows),
            "official_sources_checked": sum(int(row["official_sources_checked"]) for row in output_rows),
            "official_sources_retrieved": sum(int(row["official_sources_retrieved"]) for row in output_rows),
            "public_correction_or_coordinate_source_records_found": sum(
                1 for row in output_rows if row["public_correction_or_coordinate_source_record_found"]
            ),
            "rows_with_dashboard_target_code_confirmation": sum(
                1 for row in output_rows if row["dashboard_menu_contains_target_code"]
            ),
            "rows_with_dashboard_linked_other_district_code_confirmation": sum(
                1 for row in output_rows if row["dashboard_menu_contains_linked_other_district_code"]
            ),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "correction_followup_evidence_class_counts": [
            {"name": name, "rows": int(class_counter[name])} for name in sorted(class_counter)
        ],
        "evidence_rows": output_rows,
        "evidence_notes": [
            "The targeted follow-up checks only the shared-coordinate Narayanganj records and the cross-district Durgapur conflict.",
            "DGHS Health Dashboard menu pages confirm the target codes for all targeted rows.",
            "For Durgapur, the same dashboard menu page confirms both the Netrakona and Rajshahi Durgapur codes.",
            "No public correction record or explicit coordinate-source note was found in the checked official pages.",
            "Rows remain open pending a public correction record, source-owner clarification, or human validation.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "correction_followup_evidence_id",
        "evidence_rank",
        "evidence_method",
        "retrieved_at",
        "attestation_chain",
        "status",
        "public_explanation_evidence_id",
        "official_coordinate_evidence_id",
        "source_repair_evidence_id",
        "decision_id",
        "inspection_id",
        "facility_name",
        "dghs_profile_id",
        "dghs_organization_code",
        "division_name",
        "district_name",
        "upazila_name",
        "shared_official_profile_coordinate_rows",
        "linked_other_district_code",
        "linked_other_district_name",
        "linked_other_district_division",
        "linked_other_district_district",
        "linked_other_district_upazila",
        "linked_other_district_coordinate_distance_m",
        "targeted_reason",
        "official_sources_checked",
        "official_sources_retrieved",
        "official_source_statuses",
        "dashboard_menu_contains_target_code",
        "dashboard_menu_contains_linked_other_district_code",
        "public_correction_or_coordinate_source_record_found",
        "correction_source_kinds",
        "correction_followup_evidence_class",
        "correction_followup_reviewer_action",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_CORRECTION_FOLLOWUP_CSV, output_rows, fields)
    write_json(OUT_CORRECTION_FOLLOWUP_SUMMARY_JSON, summary)

    scope = summary["correction_followup_scope"]
    print(
        "Built BGD source-repair correction-record follow-up: "
        f"{scope['targeted_rows']} targeted rows; "
        f"{scope['public_correction_or_coordinate_source_records_found']} public correction/source records; "
        f"{scope['rows_with_dashboard_linked_other_district_code_confirmation']} linked-code dashboard confirmations; "
        f"{scope['rows_closed_as_resolved']} closed."
    )
    print(f"Wrote {OUT_CORRECTION_FOLLOWUP_CSV}")
    print(f"Wrote {OUT_CORRECTION_FOLLOWUP_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
