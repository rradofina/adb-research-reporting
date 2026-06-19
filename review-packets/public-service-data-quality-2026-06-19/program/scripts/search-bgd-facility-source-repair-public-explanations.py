"""Search public official pages for PSDQ BGD source-repair explanations.

This live public-source pass starts from the four official-coordinate evidence
rows. It checks whether public official pages explain the coordinates, whether
the same official registry contains duplicate-name or shared-coordinate clues,
and whether linked government portals add a correction/source note. It does not
close, reclassify, or validate any row.
"""

from __future__ import annotations

import csv
import html
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "generated"
CACHE_DIR = ROOT / ".cache"

IN_OFFICIAL_COORDINATE_EVIDENCE_CSV = (
    OUT_DIR / "psdq-bgd-facility-validation-source-repair-official-coordinate-evidence.csv"
)
IN_DGHS_PUBLIC_FACILITY_PAGES = CACHE_DIR / "bgd_public_facilities_p*.json"
IN_DGHS_DATATABLE_PAGES = CACHE_DIR / "bgd_dghs_p*.json"

OUT_PUBLIC_EXPLANATION_EVIDENCE_CSV = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-public-explanation-evidence.csv"
)
OUT_PUBLIC_EXPLANATION_EVIDENCE_SUMMARY_JSON = (
    OUT_DIR
    / "psdq-bgd-facility-validation-source-repair-public-explanation-evidence-summary.json"
)

METHOD = "ai_public_source_repair_public_explanation_search_v1"
STATUS = "ai_public_source_repair_public_explanation_search_not_human_validation"
USER_AGENT = "ADB-AI-Research-PSDQ-source-repair-public-explanation-search/1.0"
NON_CLAIM = (
    "This is an AI-first public-source explanation search for PSDQ "
    "source-repair rows. It checks public official DGHS profile pages, cached "
    "DGHS registry records, and public government health portals for coordinate "
    "source or correction explanations. It is not human validation, not ground "
    "truth, not a row closure, not a same-facility reclassification, not a "
    "facility-quality assessment, and not a service-access estimate."
)

OFFICIAL_PORTAL_OVERRIDES = {
    "10001476": [
        "https://health.bera.pabna.gov.bd",
        "https://health.bera.pabna.gov.bd/pages/officers",
    ],
    "10002304": [
        "https://health.durgapur.netrokona.gov.bd",
        "https://health.durgapur.netrokona.gov.bd/pages/officers",
        "https://health.durgapur.netrokona.gov.bd/views/staff-list",
    ],
}

EXPLICIT_EXPLANATION_PATTERNS = [
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
]

COORDINATE_TERMS = [
    "latitude",
    "longitude",
    "coordinate",
    "coordinates",
    "gps",
    "geocode",
    "map coordinate",
]

CORRECTION_TERMS = [
    "correction",
    "corrected",
    "coordinate correction",
    "updated coordinate",
    "wrong coordinate",
    "incorrect coordinate",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def natural_page_key(path: Path) -> tuple[str, int]:
    match = re.search(r"_p(\d+)\.json$", path.name)
    return path.stem, int(match.group(1)) if match else 0


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


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def clean_html(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = text.replace("\u0165", ">")
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_name(value: Any) -> str:
    text = clean_html(value).lower()
    text = text.replace("&amp;", "and")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def compact_text(value: Any, limit: int = 240) -> str:
    text = clean_html(value)
    return text[:limit].strip()


def extract_profile_id(value: Any) -> str:
    match = re.search(r"/facilities/(\d+)/profile", str(value or ""))
    if match:
        return match.group(1)
    match = re.search(r">\s*(\d+)\s*<", str(value or ""))
    return match.group(1) if match else ""


def profile_url(profile_id: Any, tab: str | None = None) -> str:
    url = f"https://hrm.dghs.gov.bd/public/facility-registry/facilities/{profile_id}/profile"
    if tab:
        url = f"{url}?tab={tab}"
    return url


def fetch_url(url: str, timeout: int = 30) -> dict[str, Any]:
    if not url:
        return {
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
            body = response.read().decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.url,
                "content_type": response.headers.get("content-type", ""),
                "body": body,
                "error": "",
            }
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return {
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "body": body,
            "error": f"http_error_{exc.code}",
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "body": "",
            "error": f"url_error:{exc.reason}",
        }
    except TimeoutError:
        return {
            "ok": False,
            "status": "",
            "final_url": url,
            "content_type": "",
            "body": "",
            "error": "timeout",
        }


def text_has_any(text: str, patterns: list[str]) -> bool:
    lowered = clean_html(text).lower()
    return any(pattern in lowered for pattern in patterns)


def extract_last_updated(body: str) -> str:
    text = clean_html(body)
    match = re.search(r"Last updated on\s+([0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9:]+)", text)
    return match.group(1).strip() if match else ""


def extract_profile_lat_lon(body: str) -> tuple[str, str]:
    text = clean_html(body)
    lat_match = re.search(r"Latitude\s+([-0-9.]+)", text)
    lon_match = re.search(r"Longitude\s+([-0-9.]+)", text)
    iframe_match = re.search(
        r"maps\.google\.com/maps\?q=([-0-9.]+),([-0-9.]+)",
        body,
        flags=re.IGNORECASE,
    )
    if lat_match and lon_match:
        return lat_match.group(1), lon_match.group(1)
    if iframe_match:
        return iframe_match.group(1), iframe_match.group(2)
    return "", ""


def parse_datatable_name(value: Any) -> str:
    return clean_html(value)


def load_datatable_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(CACHE_DIR.glob("bgd_dghs_p*.json"), key=natural_page_key):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload.get("data", []):
            profile_id = extract_profile_id(item.get("id") or item.get("name"))
            name = parse_datatable_name(item.get("name"))
            records.append(
                {
                    "profile_id": profile_id,
                    "name": name,
                    "normalized_name": normalize_name(name),
                    "code": str(item.get("code") or ""),
                    "email_1": item.get("email_1") or "",
                    "facility_type_name": item.get("facility_type_name") or "",
                    "division_name": item.get("division_name") or "",
                    "district_name": item.get("district_name") or "",
                    "city_corporation_name": item.get("city_corporation_name") or "",
                    "upazila_name": item.get("upazila_name") or "",
                    "paurasava_name": item.get("paurasava_name") or "",
                    "union_name": item.get("union_name") or "",
                    "source_cache_file": path.name,
                }
            )
    return records


def find_public_facility_records(codes: set[str]) -> dict[str, dict[str, Any]]:
    remaining = {str(code) for code in codes if str(code)}
    found: dict[str, dict[str, Any]] = {}
    for path in sorted(CACHE_DIR.glob("bgd_public_facilities_p*.json"), key=natural_page_key):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in (payload.get("data") or {}).get("items", []):
            code = str(item.get("code") or "")
            if code in remaining:
                record = dict(item)
                record["source_cache_file"] = path.name
                found[code] = record
                remaining.remove(code)
        if not remaining:
            break
    return found


def haversine_m(lat1: Any, lon1: Any, lat2: Any, lon2: Any) -> float:
    phi1 = math.radians(to_float(lat1))
    phi2 = math.radians(to_float(lat2))
    delta_phi = math.radians(to_float(lat2) - to_float(lat1))
    delta_lambda = math.radians(to_float(lon2) - to_float(lon1))
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return 6_371_000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def unique_urls(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for url in urls:
        if url and url not in seen:
            output.append(url)
            seen.add(url)
    return output


def portal_urls_for(record: dict[str, Any]) -> list[str]:
    code = str(record.get("code") or "")
    urls = []
    website = str(record.get("website_url") or "")
    if website:
        urls.append(website.replace("http://", "https://", 1))
    urls.extend(OFFICIAL_PORTAL_OVERRIDES.get(code, []))
    return unique_urls(urls)


def classify_evidence(row: dict[str, Any]) -> str:
    if row["explicit_coordinate_source_or_correction_explanation_found"]:
        return "public_coordinate_source_or_correction_explanation_found"
    if to_float(row["nearest_same_name_other_district_coordinate_distance_m"]) <= 2_000 and row[
        "nearest_same_name_other_district_code"
    ]:
        return "official_same_name_cross_district_coordinate_conflict_no_correction_record"
    if int(row["shared_official_profile_coordinate_rows"] or 0) > 1:
        return "official_shared_coordinate_across_distinct_records_no_explanation"
    if int(row["official_gov_portal_pages_retrieved"] or 0) > 0:
        return "official_profile_and_gov_portal_no_coordinate_explanation"
    return "official_profile_exposes_coordinate_no_public_explanation"


def reviewer_action(row: dict[str, Any]) -> str:
    evidence_class = row["public_explanation_evidence_class"]
    if evidence_class == "public_coordinate_source_or_correction_explanation_found":
        return "Review the explicit public explanation before any row closure; this script does not close rows automatically."
    if evidence_class == "official_same_name_cross_district_coordinate_conflict_no_correction_record":
        return (
            "Escalate as an official same-name cross-district coordinate conflict; "
            "do not treat the Netrakona coordinate as resolved without a correction "
            "record or human validation."
        )
    if evidence_class == "official_shared_coordinate_across_distinct_records_no_explanation":
        return (
            "Escalate as a shared-coordinate question across distinct official "
            "records; keep both rows open until a public source explains the shared "
            "site or a reviewer validates the records."
        )
    return "Keep the row open; public official pages confirm the record but do not explain the coordinate source or correction."


def main() -> None:
    for path in [IN_OFFICIAL_COORDINATE_EVIDENCE_CSV]:
        if not path.exists():
            raise FileNotFoundError(path)

    official_rows = read_csv(IN_OFFICIAL_COORDINATE_EVIDENCE_CSV)
    datatable_records = load_datatable_records()
    datatable_by_profile_id = {record["profile_id"]: record for record in datatable_records}
    datatable_by_name: dict[str, list[dict[str, Any]]] = {}
    for record in datatable_records:
        datatable_by_name.setdefault(record["normalized_name"], []).append(record)

    target_profile_ids = [
        extract_profile_id(row.get("dghs_public_profile_url")) for row in official_rows
    ]
    target_codes = {
        datatable_by_profile_id.get(profile_id, {}).get("code", "")
        for profile_id in target_profile_ids
    }
    same_name_codes: set[str] = set()
    for profile_id in target_profile_ids:
        record = datatable_by_profile_id.get(profile_id, {})
        for sibling in datatable_by_name.get(record.get("normalized_name", ""), []):
            same_name_codes.add(str(sibling.get("code") or ""))
    public_records_by_code = find_public_facility_records(target_codes | same_name_codes)

    retrieved_at = now_utc()
    output_rows: list[dict[str, Any]] = []

    for index, official_row in enumerate(official_rows, start=1):
        profile_id = extract_profile_id(official_row.get("dghs_public_profile_url"))
        datatable_record = datatable_by_profile_id.get(profile_id)
        if datatable_record is None:
            raise KeyError(f"Missing DGHS datatable record for profile {profile_id}")

        code = str(datatable_record.get("code") or "")
        public_record = public_records_by_code.get(code)
        if public_record is None:
            raise KeyError(f"Missing DGHS public-facilities cache record for code {code}")

        at_a_glance = fetch_url(profile_url(profile_id, "at-a-glance"))
        detailed = fetch_url(profile_url(profile_id, "detailed-information"))
        detail_lat, detail_lon = extract_profile_lat_lon(str(detailed.get("body") or ""))

        page_bodies = [str(at_a_glance.get("body") or ""), str(detailed.get("body") or "")]
        source_pages_checked = 2
        explicit_found = any(text_has_any(body, EXPLICIT_EXPLANATION_PATTERNS) for body in page_bodies)
        profile_coordinate_terms_found = any(text_has_any(body, COORDINATE_TERMS) for body in page_bodies)
        profile_correction_terms_found = any(text_has_any(body, CORRECTION_TERMS) for body in page_bodies)

        portal_urls = portal_urls_for(public_record)
        portal_statuses: list[str] = []
        portal_pages_retrieved = 0
        portal_coordinate_terms_found = 0
        portal_correction_terms_found = 0
        portal_snippets: list[str] = []
        for url in portal_urls:
            fetched = fetch_url(url)
            source_pages_checked += 1
            portal_statuses.append(f"{url}={fetched.get('status') or fetched.get('error')}")
            body = str(fetched.get("body") or "")
            if fetched.get("ok"):
                portal_pages_retrieved += 1
                portal_snippets.append(compact_text(body, 160))
            if text_has_any(body, COORDINATE_TERMS):
                portal_coordinate_terms_found += 1
            if text_has_any(body, CORRECTION_TERMS):
                portal_correction_terms_found += 1
            if text_has_any(body, EXPLICIT_EXPLANATION_PATTERNS):
                explicit_found = True

        same_name_records = datatable_by_name.get(datatable_record["normalized_name"], [])
        cross_district_siblings = [
            sibling
            for sibling in same_name_records
            if sibling.get("code") != code
            and (
                sibling.get("district_name") != datatable_record.get("district_name")
                or sibling.get("division_name") != datatable_record.get("division_name")
            )
        ]

        nearest_sibling: dict[str, Any] = {}
        nearest_sibling_distance = 0.0
        for sibling in cross_district_siblings:
            sibling_public = public_records_by_code.get(str(sibling.get("code") or ""), {})
            if not sibling_public.get("latitude") or not sibling_public.get("longitude"):
                continue
            distance = haversine_m(
                public_record.get("latitude"),
                public_record.get("longitude"),
                sibling_public.get("latitude"),
                sibling_public.get("longitude"),
            )
            if not nearest_sibling or distance < nearest_sibling_distance:
                nearest_sibling = {**sibling, **{f"public_{key}": value for key, value in sibling_public.items()}}
                nearest_sibling_distance = distance

        provisional_row = {
            "public_explanation_evidence_id": f"PSDQ-BGD-SRPE-{index:03d}",
            "evidence_rank": index,
            "evidence_method": METHOD,
            "retrieved_at": retrieved_at,
            "attestation_chain": "ai-first",
            "status": STATUS,
            "official_coordinate_evidence_id": official_row.get("official_coordinate_evidence_id", ""),
            "source_repair_evidence_id": official_row.get("source_repair_evidence_id", ""),
            "decision_id": official_row.get("decision_id", ""),
            "inspection_id": official_row.get("inspection_id", ""),
            "facility_name": official_row.get("facility_name", ""),
            "facility_type_name": official_row.get("facility_type_name", ""),
            "dghs_profile_id": profile_id,
            "dghs_organization_code": code,
            "dghs_public_profile_url": profile_url(profile_id),
            "division_name": datatable_record.get("division_name", ""),
            "district_name": datatable_record.get("district_name", ""),
            "upazila_name": datatable_record.get("upazila_name", ""),
            "registry_lat": public_record.get("latitude", ""),
            "registry_lon": public_record.get("longitude", ""),
            "registry_mailing_address": public_record.get("mailing_address", ""),
            "registry_village_or_street": public_record.get("village_code", ""),
            "registry_house_number": public_record.get("house_number", ""),
            "registry_union_name": public_record.get("union_name", ""),
            "registry_website_url": public_record.get("website_url", ""),
            "registry_facebook_url": public_record.get("facebook_url", ""),
            "registry_updated_at": public_record.get("updated_at", ""),
            "registry_cache_file": public_record.get("source_cache_file", ""),
            "profile_at_a_glance_http_status": at_a_glance.get("status", ""),
            "profile_detail_http_status": detailed.get("status", ""),
            "profile_last_updated_at": extract_last_updated(str(at_a_glance.get("body") or "")),
            "profile_detail_lat": detail_lat,
            "profile_detail_lon": detail_lon,
            "profile_coordinate_terms_found": profile_coordinate_terms_found,
            "profile_correction_terms_found": profile_correction_terms_found,
            "official_gov_portal_urls_checked": " | ".join(portal_urls),
            "official_gov_portal_statuses": " | ".join(portal_statuses),
            "official_gov_portal_pages_retrieved": portal_pages_retrieved,
            "official_gov_portal_coordinate_terms_found": portal_coordinate_terms_found,
            "official_gov_portal_correction_terms_found": portal_correction_terms_found,
            "official_gov_portal_text_snippet": " || ".join(portal_snippets[:2]),
            "source_pages_checked": source_pages_checked,
            "same_name_dghs_registry_records": len(same_name_records),
            "same_name_cross_district_dghs_registry_records": len(cross_district_siblings),
            "shared_official_profile_coordinate_rows": official_row.get(
                "shared_official_profile_coordinate_rows", ""
            ),
            "nearest_same_name_other_district_code": nearest_sibling.get("code", ""),
            "nearest_same_name_other_district_name": nearest_sibling.get("name", ""),
            "nearest_same_name_other_district_division": nearest_sibling.get("division_name", ""),
            "nearest_same_name_other_district_district": nearest_sibling.get("district_name", ""),
            "nearest_same_name_other_district_upazila": nearest_sibling.get("upazila_name", ""),
            "nearest_same_name_other_district_lat": nearest_sibling.get("public_latitude", ""),
            "nearest_same_name_other_district_lon": nearest_sibling.get("public_longitude", ""),
            "nearest_same_name_other_district_coordinate_distance_m": (
                round(nearest_sibling_distance, 1) if nearest_sibling else ""
            ),
            "nearest_same_name_other_district_profile_url": (
                profile_url(nearest_sibling.get("profile_id")) if nearest_sibling else ""
            ),
            "explicit_coordinate_source_or_correction_explanation_found": explicit_found,
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
            "source_basis": (
                "Live public DGHS profile tabs, cached public DGHS registry pages, "
                "and linked public government health portals where available."
            ),
            "non_claim": NON_CLAIM,
        }
        provisional_row["public_explanation_evidence_class"] = classify_evidence(provisional_row)
        provisional_row["public_explanation_reviewer_action"] = reviewer_action(provisional_row)
        output_rows.append(provisional_row)

    class_counter = Counter(row["public_explanation_evidence_class"] for row in output_rows)
    summary = {
        "generated_at": retrieved_at,
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "attestation_chain": "ai-first",
        "status": STATUS,
        "goal_level": "L3 source-repair public-explanation search",
        "unit": "source-repair-first row selected from the PSDQ official-coordinate evidence pass",
        "source_inputs": [
            {
                "path": str(IN_OFFICIAL_COORDINATE_EVIDENCE_CSV.relative_to(ROOT)),
                "role": "4-row source-repair official-coordinate evidence CSV",
            },
            {
                "path": str(IN_DGHS_DATATABLE_PAGES.relative_to(ROOT)),
                "role": "cached DGHS public DataTables organization records for same-name registry search",
            },
            {
                "path": str(IN_DGHS_PUBLIC_FACILITY_PAGES.relative_to(ROOT)),
                "role": "cached DGHS public facilities JSON pages for official address, coordinate, website, and update fields",
            },
        ],
        "selection_rule": "Include only rows in the 4-row source-repair official-coordinate evidence pass.",
        "public_explanation_scope": {
            "source_repair_rows": len(output_rows),
            "live_dghs_profile_tabs_checked": sum(
                2
                for row in output_rows
                if row["profile_at_a_glance_http_status"] and row["profile_detail_http_status"]
            ),
            "rows_with_profile_detail_coordinates": sum(
                1 for row in output_rows if row["profile_detail_lat"] and row["profile_detail_lon"]
            ),
            "official_gov_portal_urls_checked": sum(
                len(str(row["official_gov_portal_urls_checked"] or "").split(" | "))
                for row in output_rows
                if row["official_gov_portal_urls_checked"]
            ),
            "official_gov_portal_pages_retrieved": sum(
                int(row["official_gov_portal_pages_retrieved"] or 0) for row in output_rows
            ),
            "explicit_coordinate_source_or_correction_explanations_found": sum(
                1
                for row in output_rows
                if row["explicit_coordinate_source_or_correction_explanation_found"]
            ),
            "rows_with_shared_official_profile_coordinate": sum(
                1
                for row in output_rows
                if int(row["shared_official_profile_coordinate_rows"] or 0) > 1
            ),
            "rows_with_same_name_cross_district_dghs_registry_record": sum(
                1
                for row in output_rows
                if int(row["same_name_cross_district_dghs_registry_records"] or 0) > 0
            ),
            "rows_with_same_name_other_district_coordinate_within_2km": sum(
                1
                for row in output_rows
                if row["nearest_same_name_other_district_code"]
                and to_float(row["nearest_same_name_other_district_coordinate_distance_m"]) <= 2_000
            ),
            "rows_closed_as_resolved": 0,
            "rows_reclassified_as_same_facility": 0,
        },
        "public_explanation_evidence_class_counts": [
            {"name": name, "rows": int(class_counter[name])} for name in sorted(class_counter)
        ],
        "evidence_rows": output_rows,
        "evidence_notes": [
            "The public DGHS profile pages and cached DGHS registry records expose coordinates, addresses, codes, and update timestamps.",
            "This pass found no explicit public coordinate-source or coordinate-correction explanation for the four source-repair rows.",
            "Two Narayanganj records continue to share one official coordinate while showing distinct official addresses.",
            "The Netrakona Durgapur record has a same-name Rajshahi DGHS registry sibling whose official coordinate is within 2 kilometers of the Netrakona row's official coordinate.",
            "Rows remain open pending an official explanation, correction record, or human validation.",
        ],
        "non_claim": NON_CLAIM,
    }

    fields = [
        "public_explanation_evidence_id",
        "evidence_rank",
        "evidence_method",
        "retrieved_at",
        "attestation_chain",
        "status",
        "official_coordinate_evidence_id",
        "source_repair_evidence_id",
        "decision_id",
        "inspection_id",
        "facility_name",
        "facility_type_name",
        "dghs_profile_id",
        "dghs_organization_code",
        "dghs_public_profile_url",
        "division_name",
        "district_name",
        "upazila_name",
        "registry_lat",
        "registry_lon",
        "registry_mailing_address",
        "registry_village_or_street",
        "registry_house_number",
        "registry_union_name",
        "registry_website_url",
        "registry_facebook_url",
        "registry_updated_at",
        "registry_cache_file",
        "profile_at_a_glance_http_status",
        "profile_detail_http_status",
        "profile_last_updated_at",
        "profile_detail_lat",
        "profile_detail_lon",
        "profile_coordinate_terms_found",
        "profile_correction_terms_found",
        "official_gov_portal_urls_checked",
        "official_gov_portal_statuses",
        "official_gov_portal_pages_retrieved",
        "official_gov_portal_coordinate_terms_found",
        "official_gov_portal_correction_terms_found",
        "official_gov_portal_text_snippet",
        "source_pages_checked",
        "same_name_dghs_registry_records",
        "same_name_cross_district_dghs_registry_records",
        "shared_official_profile_coordinate_rows",
        "nearest_same_name_other_district_code",
        "nearest_same_name_other_district_name",
        "nearest_same_name_other_district_division",
        "nearest_same_name_other_district_district",
        "nearest_same_name_other_district_upazila",
        "nearest_same_name_other_district_lat",
        "nearest_same_name_other_district_lon",
        "nearest_same_name_other_district_coordinate_distance_m",
        "nearest_same_name_other_district_profile_url",
        "explicit_coordinate_source_or_correction_explanation_found",
        "public_explanation_evidence_class",
        "public_explanation_reviewer_action",
        "rows_closed_as_resolved",
        "rows_reclassified_as_same_facility",
        "source_basis",
        "non_claim",
    ]
    write_csv(OUT_PUBLIC_EXPLANATION_EVIDENCE_CSV, output_rows, fields)
    write_json(OUT_PUBLIC_EXPLANATION_EVIDENCE_SUMMARY_JSON, summary)

    scope = summary["public_explanation_scope"]
    print(
        "Built BGD source-repair public-explanation evidence: "
        f"{scope['source_repair_rows']} rows; "
        f"{scope['explicit_coordinate_source_or_correction_explanations_found']} explicit explanations; "
        f"{scope['rows_with_same_name_other_district_coordinate_within_2km']} same-name cross-district coordinate conflicts within 2km; "
        f"{scope['rows_closed_as_resolved']} closed."
    )
    print(f"Wrote {OUT_PUBLIC_EXPLANATION_EVIDENCE_CSV}")
    print(f"Wrote {OUT_PUBLIC_EXPLANATION_EVIDENCE_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
