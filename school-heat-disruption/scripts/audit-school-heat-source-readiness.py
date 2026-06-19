"""School heat source-readiness audit.

The existing school-heat report is an honest sensitivity audit: Cambodia
survives only after a degenerate all-zero run and a rank-losing Pakistan run
are named. This script adds the next public source wall without claiming that
school disruption has been measured:

* WDI metadata and latest values for the old school-heat proxy inputs plus
  school-system context indicators.
* CCKP public tasmax rows for Cambodia and Pakistan, the top-one and the
  rank-losing challenger in the sensitivity file.
* OpenStreetMap/Overpass school-count visibility for Cambodia and Pakistan.
* A UNICEF public climate-related school-disruption source pointer.

The result records the real missing object: no national school-calendar table,
daily school-day heat series, school-location heat overlay, enrollment-weighted
exposure, or closure/attendance outcome join is built here. Public data only.
attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "school-source-readiness"
OUT = BASE / "generated"
SENSITIVITY_PATH = OUT / "school-heat-sensitivity-audit.json"
PANEL_PATH = OUT / "school-heat-adb-panel.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
CCKP_URL_PATTERN = (
    "https://cckpapi.worldbank.org/cckp/v1/"
    "cmip6-x0.25_climatology_tasmax_climatology_annual_1995-2014_"
    "median_historical_ensemble_all_mean/{iso3}"
)
OVERPASS_ENDPOINT = "https://overpass-api.de/api/interpreter"
UNICEF_DISRUPTION_PDF = (
    "https://www.unicefusa.org/sites/default/files/2025-01/"
    "UNICEF-Global-snapshot-climate-related-school-disruptions-2024.pdf"
)

TARGETS = {
    "KHM": {"country": "Cambodia", "alpha2": "KH", "role": "baseline_top_one"},
    "PAK": {"country": "Pakistan", "alpha2": "PK", "role": "rank_losing_challenger"},
}

ADB_NAMES = {
    "AFG": "Afghanistan",
    "ARM": "Armenia",
    "AZE": "Azerbaijan",
    "BGD": "Bangladesh",
    "BTN": "Bhutan",
    "BRN": "Brunei Darussalam",
    "KHM": "Cambodia",
    "CHN": "China",
    "COK": "Cook Islands",
    "FJI": "Fiji",
    "GEO": "Georgia",
    "HKG": "Hong Kong SAR",
    "IND": "India",
    "IDN": "Indonesia",
    "KAZ": "Kazakhstan",
    "KIR": "Kiribati",
    "KGZ": "Kyrgyzstan",
    "LAO": "Lao PDR",
    "MYS": "Malaysia",
    "MDV": "Maldives",
    "MHL": "Marshall Islands",
    "FSM": "Micronesia",
    "MNG": "Mongolia",
    "MMR": "Myanmar",
    "NRU": "Nauru",
    "NPL": "Nepal",
    "PAK": "Pakistan",
    "PLW": "Palau",
    "PNG": "Papua New Guinea",
    "PHL": "Philippines",
    "WSM": "Samoa",
    "SLB": "Solomon Islands",
    "LKA": "Sri Lanka",
    "TJK": "Tajikistan",
    "THA": "Thailand",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TKM": "Turkmenistan",
    "TUV": "Tuvalu",
    "UZB": "Uzbekistan",
    "VUT": "Vanuatu",
    "VNM": "Viet Nam",
    "TWN": "Taiwan",
}

WDI_INDICATORS = [
    {
        "id": "SE.PRM.ENRL.TC.ZS",
        "role": "old_primary_pupil_teacher_ratio_proxy",
        "category": "old_proxy",
    },
    {
        "id": "SP.POP.0014.TO.ZS",
        "role": "old_child_population_share_proxy",
        "category": "old_proxy",
    },
    {
        "id": "SP.POP.TOTL",
        "role": "old_population_denominator",
        "category": "old_proxy",
    },
    {
        "id": "SE.PRM.DURS",
        "role": "primary_duration_context_not_calendar",
        "category": "school_system_context",
    },
    {
        "id": "SE.PRM.ENRR",
        "role": "primary_gross_enrollment_context",
        "category": "enrollment_context",
    },
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cache_name(url, suffix):
    stem = re.sub(r"[^A-Za-z0-9]+", "_", url).strip("_")[:150]
    return f"{stem}.{suffix}"


def sanitize_headers(headers):
    out = {}
    for key, value in headers.items():
        if key.lower() == "set-cookie":
            continue
        out[key] = value
    return out


def fetch_bytes(url, suffix="bin", timeout=60, method="GET", body=None, headers=None):
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / cache_name(url, suffix)
    if cache_path.exists():
        raw = cache_path.read_bytes()
        return raw, {
            "url": url,
            "cache_path": str(cache_path.relative_to(BASE)),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "status_code": 200,
            "fetch_mode": "cache",
            "response_headers": {},
        }

    request_headers = {
        "Accept": "application/json, text/html, application/pdf, */*",
        "User-Agent": "adb-research-source-audit/1.0",
    }
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(url, data=body, method=method, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            status = int(getattr(response, "status", 200))
            response_headers = sanitize_headers(dict(response.headers.items()))
        cache_path.write_bytes(raw)
        mode = "live"
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        status = int(exc.code)
        response_headers = sanitize_headers(dict(exc.headers.items()))
        cache_path.write_bytes(raw)
        mode = "http_error"
    except (urllib.error.URLError, TimeoutError) as exc:
        raw = b""
        status = None
        response_headers = {}
        mode = f"failed:{exc.__class__.__name__}"
    return raw, {
        "url": url,
        "cache_path": str(cache_path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status_code": status,
        "fetch_mode": mode,
        "response_headers": response_headers,
    }


def fetch_json(url, timeout=60):
    raw, record = fetch_bytes(url, "json", timeout=timeout)
    try:
        parsed = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    record["json_parse_ok"] = parsed is not None
    return parsed, record


def unwrap_world_bank_rows(payload):
    if isinstance(payload, list) and len(payload) >= 2 and isinstance(payload[1], list):
        return payload[1]
    return []


def wdi_metadata(indicator_id):
    url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
    parsed, record = fetch_json(url)
    row = unwrap_world_bank_rows(parsed)[0] if unwrap_world_bank_rows(parsed) else {}
    return {
        "indicator_id": indicator_id,
        "indicator_name": row.get("name"),
        "source_note": row.get("sourceNote"),
        "source_organization": row.get("sourceOrganization"),
        "metadata_url": url,
        "metadata_status_code": record["status_code"],
        "metadata_json_parse_ok": record["json_parse_ok"],
        "metadata_sha256": record["sha256"],
    }, {**record, "query_type": "wdi_indicator_metadata", "indicator_id": indicator_id}


def wdi_latest_values(indicator_id):
    page = 1
    pages = 1
    latest = {}
    records = []
    while page <= pages:
        url = (
            f"{WORLD_BANK_API_BASE}/country/all/indicator/{indicator_id}"
            f"?format=json&per_page=20000&page={page}"
        )
        parsed, record = fetch_json(url)
        records.append({**record, "query_type": "wdi_indicator_data", "indicator_id": indicator_id, "page": page})
        if not (isinstance(parsed, list) and len(parsed) > 1):
            break
        meta = parsed[0] if isinstance(parsed[0], dict) else {}
        pages = int(meta.get("pages") or 1)
        for row in parsed[1] or []:
            iso = row.get("countryiso3code")
            value = row.get("value")
            if iso not in ADB_NAMES or not isinstance(value, (int, float)):
                continue
            try:
                year = int(row.get("date"))
            except (TypeError, ValueError):
                continue
            if iso not in latest or year > latest[iso]["year"]:
                latest[iso] = {"year": year, "value": float(value)}
        page += 1
    return latest, records


def latest_year_span(values):
    years = [row["year"] for row in values.values()]
    if not years:
        return None, None
    return min(years), max(years)


def parse_cckp_tasmax(payload, iso3):
    data = {}
    if isinstance(payload, dict):
        data = payload.get("data", {}).get(iso3, {})
    for period, value in data.items():
        if isinstance(value, (int, float)):
            return period, float(value)
    return None, None


def fetch_cckp_target(iso3):
    url = CCKP_URL_PATTERN.format(iso3=iso3)
    parsed, record = fetch_json(url)
    period, value = parse_cckp_tasmax(parsed, iso3)
    return {
        "iso3": iso3,
        "country": TARGETS[iso3]["country"],
        "source_url": url,
        "public_source_reachable": record["status_code"] == 200 and record["json_parse_ok"],
        "period_key": period,
        "tasmax_value": round(value, 4) if value is not None else None,
        "status_code": record["status_code"],
        "bytes": record["bytes"],
        "sha256": record["sha256"],
    }, {**record, "query_type": "cckp_tasmax", "iso3": iso3}


def overpass_school_query(alpha2):
    return (
        "[out:json][timeout:25];"
        f"area[\"ISO3166-1\"=\"{alpha2}\"][admin_level=2]->.searchArea;"
        "("
        "node[\"amenity\"=\"school\"](area.searchArea);"
        "way[\"amenity\"=\"school\"](area.searchArea);"
        "relation[\"amenity\"=\"school\"](area.searchArea);"
        ");"
        "out count;"
    )


def parse_overpass_count(payload):
    if not isinstance(payload, dict):
        return None, None, None, None, None
    osm3s = payload.get("osm3s") if isinstance(payload.get("osm3s"), dict) else {}
    elements = payload.get("elements") if isinstance(payload.get("elements"), list) else []
    if not elements:
        return None, None, None, osm3s.get("timestamp_osm_base"), osm3s.get("timestamp_areas_base")
    tags = elements[0].get("tags", {}) if isinstance(elements[0], dict) else {}
    def as_int(key):
        try:
            return int(tags.get(key))
        except (TypeError, ValueError):
            return None
    total = as_int("total")
    nodes = as_int("nodes")
    ways = as_int("ways")
    relations = as_int("relations")
    return total, nodes, ways, osm3s.get("timestamp_osm_base"), osm3s.get("timestamp_areas_base")


def fetch_overpass_school_count(iso3):
    target = TARGETS[iso3]
    query = overpass_school_query(target["alpha2"])
    url = f"{OVERPASS_ENDPOINT}?data={urllib.parse.quote(query, safe='')}"
    parsed, record = fetch_json(url, timeout=75)
    total, nodes, ways, osm_timestamp, areas_timestamp = parse_overpass_count(parsed)
    return {
        "iso3": iso3,
        "country": target["country"],
        "source_url": OVERPASS_ENDPOINT,
        "query_alpha2": target["alpha2"],
        "public_source_reachable": record["status_code"] == 200 and record["json_parse_ok"],
        "osm_school_count_total": total,
        "osm_school_count_nodes": nodes,
        "osm_school_count_ways": ways,
        "osm_timestamp_osm_base": osm_timestamp,
        "osm_timestamp_areas_base": areas_timestamp,
        "status_code": record["status_code"],
        "bytes": record["bytes"],
        "sha256": record["sha256"],
    }, {**record, "query_type": "overpass_school_count", "iso3": iso3}


def fetch_unicef_disruption_source():
    raw, record = fetch_bytes(UNICEF_DISRUPTION_PDF, "pdf", timeout=90)
    lower = raw.lower()
    tokens = {
        token: lower.count(token.encode("utf-8"))
        for token in ["school", "climate", "heat", "closure", "disruption"]
    }
    return {
        "layer_role": "observed_school_disruption_source_pointer",
        "source_name": "UNICEF global snapshot of climate-related school disruptions in 2024",
        "source_url": UNICEF_DISRUPTION_PDF,
        "key_id": "unicef_school_disruptions_2024_pdf",
        "public_metadata_reachable": record["status_code"] == 200 and record["bytes"] > 0,
        "candidate_rows": 1,
        "joined_rows": 0,
        "status": "source visible; country closure rows not parsed" if record["status_code"] == 200 else "source request failed",
        "notes": f"PDF byte-token counts: {tokens}. No country-year closure table is extracted or joined.",
    }, {**record, "query_type": "unicef_school_disruption_pdf"}


def load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_row(layer_role, source_name, source_url, key_id, reachable, candidate_rows, joined_rows, status, notes):
    return {
        "layer_role": layer_role,
        "source_name": source_name,
        "source_url": source_url,
        "key_id": key_id,
        "public_metadata_reachable": bool(reachable),
        "candidate_rows": int(candidate_rows or 0),
        "joined_rows": int(joined_rows or 0),
        "status": status,
        "notes": notes or "",
    }


def panel_rank(rows):
    ranked = [
        row for row in rows
        if isinstance(row.get("school_heat_pressure_index"), (int, float))
    ]
    ranked.sort(key=lambda row: (-row["school_heat_pressure_index"], row["iso3"]))
    return {row["iso3"]: index + 1 for index, row in enumerate(ranked)}


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = now_iso()

    sensitivity = load_json(SENSITIVITY_PATH)
    panel = load_json(PANEL_PATH)
    panel_rows = {row["iso3"]: row for row in panel.get("rows", [])}
    ranks = panel_rank(panel.get("rows", []))
    counts = sensitivity.get("counts", {})

    cache_records = []
    wdi_source_rows = []
    values_by_indicator = {}
    for spec in WDI_INDICATORS:
        metadata, meta_record = wdi_metadata(spec["id"])
        latest, data_records = wdi_latest_values(spec["id"])
        values_by_indicator[spec["id"]] = latest
        cache_records.append(meta_record)
        cache_records.extend(data_records)
        ymin, ymax = latest_year_span(latest)
        wdi_source_rows.append(source_row(
            spec["role"],
            metadata.get("indicator_name") or spec["id"],
            metadata.get("metadata_url"),
            spec["id"],
            metadata.get("metadata_status_code") == 200 and metadata.get("metadata_json_parse_ok"),
            len(ADB_NAMES),
            len(latest),
            "metadata and latest values visible" if latest else "metadata only or no DMC values",
            (
                f"Category {spec['category']}; ADB latest-year span {ymin}-{ymax}. "
                f"{metadata.get('source_note') or ''}"
            ).strip(),
        ))

    cckp_rows = []
    for iso3 in TARGETS:
        row, record = fetch_cckp_target(iso3)
        cckp_rows.append(row)
        cache_records.append(record)

    osm_rows = []
    for iso3 in TARGETS:
        row, record = fetch_overpass_school_count(iso3)
        osm_rows.append(row)
        cache_records.append(record)

    unicef_row, unicef_record = fetch_unicef_disruption_source()
    cache_records.append(unicef_record)

    cckp_by_iso = {row["iso3"]: row for row in cckp_rows}
    osm_by_iso = {row["iso3"]: row for row in osm_rows}
    target_country_rows = []
    old_indicator_ids = ["SE.PRM.ENRL.TC.ZS", "SP.POP.0014.TO.ZS", "SP.POP.TOTL"]
    for iso3, target in TARGETS.items():
        panel_row = panel_rows.get(iso3, {})
        cckp = cckp_by_iso.get(iso3, {})
        osm = osm_by_iso.get(iso3, {})
        row = {
            "iso3": iso3,
            "country": target["country"],
            "source_role": target["role"],
            "baseline_rank": ranks.get(iso3),
            "school_heat_pressure_index": panel_row.get("school_heat_pressure_index"),
            "children_0_14_millions": panel_row.get("children_0_14_millions"),
            "annual_tasmax_1995_2014_celsius": panel_row.get("annual_tasmax_1995_2014_celsius"),
            "primary_pupil_teacher_ratio": panel_row.get("primary_pupil_teacher_ratio"),
            "ptr_year": panel_row.get("ptr_year"),
            "cckp_source_reachable": cckp.get("public_source_reachable"),
            "cckp_tasmax_value": cckp.get("tasmax_value"),
            "cckp_period_key": cckp.get("period_key"),
            "osm_source_reachable": osm.get("public_source_reachable"),
            "osm_school_count_total": osm.get("osm_school_count_total"),
            "osm_school_count_nodes": osm.get("osm_school_count_nodes"),
            "osm_school_count_ways": osm.get("osm_school_count_ways"),
            "osm_timestamp_osm_base": osm.get("osm_timestamp_osm_base"),
            "osm_timestamp_areas_base": osm.get("osm_timestamp_areas_base"),
            "analysis_ready_school_calendar_join": False,
            "analysis_ready_school_day_heat_join": False,
            "analysis_ready_school_location_join": False,
            "analysis_ready_closure_outcome_join": False,
        }
        for indicator_id in old_indicator_ids:
            latest = values_by_indicator.get(indicator_id, {}).get(iso3)
            short = indicator_id.lower().replace(".", "_")
            row[f"{short}_latest_value"] = latest["value"] if latest else None
            row[f"{short}_latest_year"] = latest["year"] if latest else None
        target_country_rows.append(row)

    cckp_source_rows = [
        source_row(
            "cckp_country_tasmax_source",
            f"World Bank CCKP annual tasmax 1995-2014 historical for {row['iso3']}",
            row["source_url"],
            row["iso3"],
            row["public_source_reachable"],
            1,
            1 if row.get("tasmax_value") is not None else 0,
            "country tasmax row visible" if row.get("tasmax_value") is not None else "country tasmax row unavailable",
            f"Parsed period key {row.get('period_key')}; value is source-readiness context only.",
        )
        for row in cckp_rows
    ]
    osm_source_rows = [
        source_row(
            "osm_school_location_source_visibility",
            f"OpenStreetMap amenity=school Overpass count for {row['iso3']}",
            row["source_url"],
            row["iso3"],
            row["public_source_reachable"],
            1,
            1 if row.get("osm_school_count_total") is not None else 0,
            "school amenity count visible" if row.get("osm_school_count_total") is not None else "school amenity count unavailable",
            (
                f"Count {row.get('osm_school_count_total')}; OSM timestamp "
                f"{row.get('osm_timestamp_osm_base')}. This is not an enrollment or heat overlay."
            ),
        )
        for row in osm_rows
    ]
    missing_join_rows = [
        source_row(
            "analysis_ready_school_calendar_join",
            "National school-term calendar joined to daily heat",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            "No public national term-date table is parsed, normalized by country, or joined to heat days.",
        ),
        source_row(
            "analysis_ready_school_day_heat_join",
            "Daily school-day heat or WBGT series",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            "No ERA5, CCKP daily, WBGT, or in-session heat series is computed for school days.",
        ),
        source_row(
            "analysis_ready_school_location_join",
            "School geocodes intersected with local heat and population",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            "OSM count visibility is not a school-location heat overlay; no school points are downloaded or intersected.",
        ),
        source_row(
            "analysis_ready_closure_outcome_join",
            "Closure, attendance, or learning outcome joined",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            "The UNICEF source pointer is not parsed into a country-date closure or learning-outcome panel.",
        ),
    ]
    source_rows = wdi_source_rows + cckp_source_rows + osm_source_rows + [unicef_row] + missing_join_rows

    old_wdi_complete_targets = 0
    for iso3 in TARGETS:
        if all(iso3 in values_by_indicator.get(indicator_id, {}) for indicator_id in old_indicator_ids):
            old_wdi_complete_targets += 1

    summary = {
        "baseline_top1": "KHM",
        "rank_losing_challenger": "PAK",
        "runs_total": counts.get("runs_total"),
        "degenerate_all_zero": counts.get("degenerate_all_zero"),
        "rank_losing_for_khm": counts.get("rank_losing_for_khm"),
        "khm_top1_among_discriminating": counts.get("khm_top1_among_discriminating"),
        "discriminating": counts.get("discriminating"),
        "target_country_rows": len(TARGETS),
        "old_wdi_complete_target_rows": old_wdi_complete_targets,
        "wdi_indicators_requested": len(WDI_INDICATORS),
        "wdi_metadata_records_reachable": sum(1 for row in wdi_source_rows if row["public_metadata_reachable"]),
        "cckp_target_rows_reachable": sum(1 for row in cckp_rows if row["public_source_reachable"]),
        "cckp_target_rows_with_value": sum(1 for row in cckp_rows if row.get("tasmax_value") is not None),
        "osm_target_rows_reachable": sum(1 for row in osm_rows if row["public_source_reachable"]),
        "osm_target_rows_with_school_count": sum(1 for row in osm_rows if row.get("osm_school_count_total") is not None),
        "osm_school_count_total_targets": sum(
            int(row.get("osm_school_count_total") or 0)
            for row in osm_rows
            if row.get("osm_school_count_total") is not None
        ),
        "unicef_disruption_source_reachable": unicef_row["public_metadata_reachable"],
        "analysis_ready_school_calendar_join": False,
        "analysis_ready_school_day_heat_join": False,
        "analysis_ready_school_location_join": False,
        "analysis_ready_enrollment_weighted_exposure": False,
        "analysis_ready_closure_outcome_join": False,
        "owner_gated_or_unfinished_steps": [
            "No national school-term or school-day calendar is parsed and joined.",
            "No daily heat, humid heat, or WBGT series is computed for in-session days.",
            "No school geocodes are downloaded, cleaned, deduplicated, or intersected with heat and population.",
            "No enrollment-weighted exposure denominator is joined.",
            "No school closure, attendance, or learning outcome panel is joined.",
            "The Cambodia top-one narrowing remains an index-internal sensitivity result, not a school-disruption measurement.",
        ],
    }

    readiness = {
        "program": "school-heat-disruption",
        "analysis": "public school calendar, school-location, heat, and disruption source-readiness audit",
        "claim_scope": (
            "Public source audit for the school-heat screen. It preserves the "
            "Cambodia top-one sensitivity narrowing, verifies public WDI and "
            "CCKP source visibility, checks OSM school-count visibility for "
            "Cambodia and Pakistan, and records a UNICEF disruption source "
            "pointer. It does not build school calendars, school-day heat, "
            "school-location overlays, enrollment-weighted exposure, or "
            "closure/learning outcomes."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
            "wdi_indicators": [spec["id"] for spec in WDI_INDICATORS],
            "cckp_url_pattern": CCKP_URL_PATTERN,
            "overpass_endpoint": OVERPASS_ENDPOINT,
            "unicef_disruption_pdf": UNICEF_DISRUPTION_PDF,
        },
        "summary": summary,
        "wdi_source_rows": wdi_source_rows,
        "cckp_target_rows": cckp_rows,
        "osm_school_count_rows": osm_rows,
        "target_country_rows": target_country_rows,
        "source_rows": source_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(sensitivity)
    combined["analysis"] = "top-1 sensitivity audit plus public school-heat source-readiness wall"
    combined["claim_scope"] = (
        f"{sensitivity.get('claim_scope', '')} The combined source audit adds "
        "public WDI, CCKP, OSM, and UNICEF source checks while keeping school "
        "calendars, school-day heat, school-location overlays, enrollment-"
        "weighted exposure, and closure outcomes outside claim scope."
    ).strip()
    combined["school_heat_source_readiness"] = readiness
    combined["school_heat_data_wall"] = (
        "WDI inputs, CCKP country tasmax rows, OSM school-count visibility, "
        "and a UNICEF school-disruption source pointer are now visible at "
        "source level. The analysis still has no school calendar, no daily "
        "school-day heat or WBGT series, no school-location heat overlay, no "
        "enrollment-weighted exposure, and no closure or learning outcome join."
    )
    combined["attestation_chain"] = "ai-first"
    combined["generated_at"] = retrieved_at

    (OUT / "school-heat-source-audit.json").write_text(
        json.dumps(combined, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "school-heat-source-readiness.json").write_text(
        json.dumps(readiness, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_csv(
        OUT / "school-heat-source-readiness-sources.csv",
        source_rows,
        [
            "layer_role",
            "source_name",
            "source_url",
            "key_id",
            "public_metadata_reachable",
            "candidate_rows",
            "joined_rows",
            "status",
            "notes",
        ],
    )
    write_csv(
        OUT / "school-heat-khm-pak-source-readiness.csv",
        target_country_rows,
        list(target_country_rows[0].keys()),
    )

    print("=== School heat source-readiness audit ===")
    print(f"Baseline top one: {summary['baseline_top1']}")
    print(f"Rank-losing challenger: {summary['rank_losing_challenger']}")
    print(f"KHM top-one among discriminating runs: {summary['khm_top1_among_discriminating']}/{summary['discriminating']}")
    print(f"WDI metadata reachable: {summary['wdi_metadata_records_reachable']}/{summary['wdi_indicators_requested']}")
    print(f"CCKP target rows with value: {summary['cckp_target_rows_with_value']}/{summary['target_country_rows']}")
    print(f"OSM target rows with school count: {summary['osm_target_rows_with_school_count']}/{summary['target_country_rows']}")
    print(f"UNICEF disruption source reachable: {summary['unicef_disruption_source_reachable']}")
    print(f"School calendar join built: {summary['analysis_ready_school_calendar_join']}")
    print(f"Wrote {OUT / 'school-heat-source-audit.json'}")
    print(f"Wrote {OUT / 'school-heat-source-readiness-sources.csv'}")
    print(f"Wrote {OUT / 'school-heat-khm-pak-source-readiness.csv'}")


if __name__ == "__main__":
    main()
