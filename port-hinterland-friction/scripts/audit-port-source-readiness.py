"""Port-hinterland source-readiness audit.

The committed report shows the imports cap is mostly inert. This script adds
the next public source layer without claiming that a true port-to-hinterland
friction measure exists:

* WDI metadata and latest values for the old imports and LPI inputs.
* WDI metadata and latest values for container port traffic, road freight,
  rail freight, air freight, and additional LPI components.
* Explicit false flags for the missing objects: port performance, OD network,
  and hinterland travel-time joins.

The output is a source-readiness wall, not a port-performance ranking.
Public data only. attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "port-source-readiness"
OUT = BASE / "generated"
INERT_PATH = OUT / "port-hinterland-inert-parameter.json"
PANEL_PATH = OUT / "port-hinterland-friction-adb-panel.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"

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

INDICATORS = [
    {
        "id": "NE.IMP.GNFS.CD",
        "role": "old_trade_volume_proxy",
        "category": "old_proxy",
    },
    {
        "id": "LP.LPI.OVRL.XQ",
        "role": "old_lpi_overall_perception_score",
        "category": "old_proxy",
    },
    {
        "id": "LP.LPI.INFR.XQ",
        "role": "lpi_infrastructure_perception_score",
        "category": "lpi_component",
    },
    {
        "id": "LP.LPI.TIME.XQ",
        "role": "lpi_timeliness_perception_score",
        "category": "lpi_component",
    },
    {
        "id": "LP.LPI.ITRN.XQ",
        "role": "lpi_shipment_price_perception_score",
        "category": "lpi_component",
    },
    {
        "id": "LP.LPI.TRAC.XQ",
        "role": "lpi_tracking_perception_score",
        "category": "lpi_component",
    },
    {
        "id": "LP.LPI.CUST.XQ",
        "role": "lpi_customs_perception_score",
        "category": "lpi_component",
    },
    {
        "id": "IS.SHP.GOOD.TU",
        "role": "container_port_traffic_teu",
        "category": "actual_freight_proxy",
    },
    {
        "id": "IS.RRS.GOOD.MT.K6",
        "role": "rail_goods_million_ton_km",
        "category": "actual_freight_proxy",
    },
    {
        "id": "IS.ROD.GOOD.MT.K6",
        "role": "road_goods_million_ton_km",
        "category": "actual_freight_proxy",
    },
    {
        "id": "IS.AIR.GOOD.MT.K1",
        "role": "air_freight_million_ton_km",
        "category": "actual_freight_proxy",
    },
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cache_name(url):
    stem = re.sub(r"[^A-Za-z0-9]+", "_", url).strip("_")[:150]
    return f"{stem}.json"


def fetch_json(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / cache_name(url)
    if path.exists():
        data = path.read_bytes()
        fetch_mode = "cache"
        status = 200
        headers = {}
    else:
        req = urllib.request.Request(url, headers={"User-Agent": "adb-research-source-audit/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
                status = int(getattr(resp, "status", 200))
                headers = {k: v for k, v in resp.headers.items()}
        except urllib.error.HTTPError as exc:
            data = exc.read()
            status = int(exc.code)
            headers = {k: v for k, v in exc.headers.items()}
        path.write_bytes(data)
        fetch_mode = "live"
    try:
        parsed = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        parsed = None
    return parsed, {
        "url": url,
        "cache_path": str(path.relative_to(BASE)),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "status_code": status,
        "fetch_mode": fetch_mode,
        "headers": headers,
        "json_parse_ok": parsed is not None,
    }


def wdi_metadata(indicator_id):
    url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
    parsed, record = fetch_json(url)
    item = {}
    if isinstance(parsed, list) and len(parsed) > 1 and parsed[1]:
        item = parsed[1][0]
    return {
        "indicator_id": indicator_id,
        "indicator_name": item.get("name"),
        "source_note": item.get("sourceNote"),
        "source_organization": item.get("sourceOrganization"),
        "metadata_url": url,
        "metadata_sha256": record["sha256"],
        "metadata_bytes": record["bytes"],
        "metadata_fetch_mode": record["fetch_mode"],
        "metadata_status_code": record["status_code"],
        "metadata_json_parse_ok": record["json_parse_ok"],
    }, record


def wdi_latest_values(indicator_id):
    records = []
    latest = {}
    page = 1
    pages = 1
    while page <= pages:
        url = (
            f"{WORLD_BANK_API_BASE}/country/all/indicator/{indicator_id}"
            f"?format=json&per_page=20000&page={page}"
        )
        parsed, record = fetch_json(url)
        record["query_type"] = "wdi_indicator_data"
        record["indicator_id"] = indicator_id
        record["page"] = page
        records.append(record)
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
                latest[iso] = {
                    "indicator_id": indicator_id,
                    "year": year,
                    "value": float(value),
                }
        page += 1
    return latest, records


def load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def latest_year_span(latest):
    years = [row["year"] for row in latest.values()]
    if not years:
        return None, None
    return min(years), max(years)


def format_value(value):
    if value is None:
        return None
    return round(float(value), 4)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inert = load_json(INERT_PATH)
    panel = load_json(PANEL_PATH)
    baseline_top5 = inert.get("baseline_top5") or []
    rankable_iso = {row["iso3"] for row in inert.get("proxy_by_dmc", [])}
    friction_rank = {
        row["iso3"]: index + 1
        for index, row in enumerate(sorted(
            [r for r in panel.get("rows", []) if r.get("friction_exposure_index") is not None],
            key=lambda r: -r["friction_exposure_index"],
        ))
    }
    friction_score = {
        row["iso3"]: row.get("friction_exposure_index")
        for row in panel.get("rows", [])
    }

    metadata_rows = []
    values_by_indicator = {}
    cache_records = []
    for spec in INDICATORS:
        metadata, meta_record = wdi_metadata(spec["id"])
        latest, data_records = wdi_latest_values(spec["id"])
        values_by_indicator[spec["id"]] = latest
        ymin, ymax = latest_year_span(latest)
        metadata_rows.append({
            "layer_role": spec["role"],
            "indicator_id": spec["id"],
            "indicator_name": metadata.get("indicator_name"),
            "category": spec["category"],
            "source_url": metadata.get("metadata_url"),
            "public_metadata_reachable": metadata.get("metadata_status_code") == 200 and metadata.get("metadata_json_parse_ok"),
            "adb_rows_with_latest_value": len(latest),
            "rankable_rows_with_latest_value": sum(1 for iso in rankable_iso if iso in latest),
            "baseline_top5_rows_with_latest_value": sum(1 for iso in baseline_top5 if iso in latest),
            "latest_year_min": ymin,
            "latest_year_max": ymax,
            "status": "metadata and values visible" if latest else "metadata only or no DMC values",
            "notes": metadata.get("source_note") or "",
        })
        meta_record["query_type"] = "wdi_indicator_metadata"
        meta_record["indicator_id"] = spec["id"]
        cache_records.append(meta_record)
        cache_records.extend(data_records)

    indicator_by_role = {spec["role"]: spec["id"] for spec in INDICATORS}
    actual_roles = [
        "container_port_traffic_teu",
        "rail_goods_million_ton_km",
        "road_goods_million_ton_km",
        "air_freight_million_ton_km",
    ]
    source_country_rows = []
    for iso, country in sorted(ADB_NAMES.items(), key=lambda item: item[1]):
        row = {
            "iso3": iso,
            "country": country,
            "rankable_in_committed_panel": iso in rankable_iso,
            "baseline_top5": iso in baseline_top5,
            "friction_rank": friction_rank.get(iso),
            "friction_exposure_index": friction_score.get(iso),
        }
        years = []
        for spec in INDICATORS:
            latest = values_by_indicator[spec["id"]].get(iso)
            row[spec["role"]] = format_value(latest["value"]) if latest else None
            row[f"{spec['role']}_year"] = latest["year"] if latest else None
            if spec["role"] in actual_roles and latest:
                years.append(str(latest["year"]))
        row["any_actual_freight_proxy"] = any(row.get(role) is not None for role in actual_roles)
        row["actual_freight_proxy_years"] = ";".join(sorted(set(years)))
        source_country_rows.append(row)

    container_id = indicator_by_role["container_port_traffic_teu"]
    container_top5 = [
        {
            "iso3": iso,
            "country": ADB_NAMES[iso],
            "value": round(data["value"], 2),
            "year": data["year"],
        }
        for iso, data in sorted(
            values_by_indicator[container_id].items(),
            key=lambda item: -item[1]["value"],
        )[:5]
    ]
    rankable_with_container = sum(
        1 for iso in rankable_iso if iso in values_by_indicator[container_id]
    )
    rankable_with_any_actual = sum(
        1
        for iso in rankable_iso
        if any(values_by_indicator[indicator_by_role[role]].get(iso) for role in actual_roles)
    )
    top5_with_container = sum(
        1 for iso in baseline_top5 if iso in values_by_indicator[container_id]
    )
    top5_with_any_actual = sum(
        1
        for iso in baseline_top5
        if any(values_by_indicator[indicator_by_role[role]].get(iso) for role in actual_roles)
    )

    summary = {
        "baseline_top5": baseline_top5,
        "rankable_dmc_count": len(rankable_iso),
        "imports_cap_baseline_dmcs_reaching_cap": inert.get("dmcs_reaching_cap_baseline"),
        "max_proxy_observed": inert.get("max_proxy_observed"),
        "imports_to_reach_cap_usd_trillions": inert.get("imports_to_reach_cap_usd_trillions"),
        "wdi_indicators_requested": len(INDICATORS),
        "wdi_metadata_records_reachable": sum(1 for row in metadata_rows if row["public_metadata_reachable"]),
        "rankable_rows_with_container_port_traffic": rankable_with_container,
        "rankable_rows_with_any_actual_freight_proxy": rankable_with_any_actual,
        "baseline_top5_with_container_port_traffic": top5_with_container,
        "baseline_top5_with_any_actual_freight_proxy": top5_with_any_actual,
        "container_port_traffic_top5": container_top5,
        "actual_freight_proxy_coverage_by_indicator": {
            role: {
                "adb_rows": len(values_by_indicator[indicator_by_role[role]]),
                "rankable_rows": sum(1 for iso in rankable_iso if iso in values_by_indicator[indicator_by_role[role]]),
                "baseline_top5_rows": sum(1 for iso in baseline_top5 if iso in values_by_indicator[indicator_by_role[role]]),
            }
            for role in actual_roles
        },
        "analysis_ready_direct_port_performance": False,
        "analysis_ready_hinterland_travel_time": False,
        "analysis_ready_od_network_join": False,
        "owner_gated_or_unfinished_steps": [
            "No port-level dwell time, turnaround time, berth productivity, or port-call delay table is joined.",
            "No port-to-inland origin-destination network, route impedance, or corridor travel-time surface is built.",
            "No customs release-time, trucking cost, rail service, or inland terminal performance series is joined.",
            "Container traffic and freight ton-km are throughput proxies, not hinterland friction measures.",
            "LPI components remain perception survey scores and may not substitute for observed transit-time data.",
        ],
    }

    source_readiness = {
        "program": "port-hinterland-friction",
        "analysis": "public logistics, freight, and port-throughput source-readiness audit",
        "claim_scope": (
            "Public source audit for replacing the imports-cap robustness story "
            "with observed logistics evidence. WDI LPI components, container port "
            "traffic, and freight proxies are visible, but no direct port "
            "performance, OD network, or hinterland travel-time join is built."
        ),
        "retrieved_at": now_iso(),
        "sources": {
            "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
            "wdi_indicators": [spec["id"] for spec in INDICATORS],
        },
        "summary": summary,
        "source_rows": metadata_rows,
        "country_rows": source_country_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
    }

    audit = {
        "program": "port-hinterland-friction",
        "analysis": "inert imports-cap audit plus public logistics source-readiness wall",
        "claim_scope": (
            "Deepening of the committed port-hinterland friction proxy. It "
            "preserves the inert-cap finding, then records public WDI logistics, "
            "port-throughput, and freight-proxy availability while keeping direct "
            "port performance, OD network, and hinterland travel-time joins false."
        ),
        "source": inert.get("source"),
        "baseline_params": inert.get("baseline_params"),
        "imports_to_reach_cap_usd_trillions": inert.get("imports_to_reach_cap_usd_trillions"),
        "max_proxy_observed": inert.get("max_proxy_observed"),
        "dmcs_reaching_cap_baseline": inert.get("dmcs_reaching_cap_baseline"),
        "rankable_dmc_count": inert.get("rankable_dmc_count"),
        "proxy_by_dmc": inert.get("proxy_by_dmc"),
        "baseline_top5": inert.get("baseline_top5"),
        "committed_panel_top5": inert.get("committed_panel_top5"),
        "cap_perturbation": inert.get("cap_perturbation"),
        "binding_cap_test": inert.get("binding_cap_test"),
        "import_volume_top5": inert.get("import_volume_top5"),
        "friction_top5_equals_volume_top5_set": inert.get("friction_top5_equals_volume_top5_set"),
        "friction_top5_equals_volume_top5_order": inert.get("friction_top5_equals_volume_top5_order"),
        "port_source_readiness": source_readiness,
        "port_hinterland_data_wall": (
            "The cap problem is only the first weakness. Public WDI logistics "
            "and freight source layers are visible, including container port "
            "traffic and freight ton-kilometer proxies, but the analysis still "
            "has no port-performance table, no corridor OD network, and no "
            "hinterland travel-time statistic."
        ),
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
    }

    (OUT / "port-hinterland-source-audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "port-hinterland-source-readiness.json").write_text(
        json.dumps(source_readiness, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_csv(
        OUT / "port-hinterland-source-readiness-sources.csv",
        metadata_rows,
        [
            "layer_role",
            "indicator_id",
            "indicator_name",
            "category",
            "source_url",
            "public_metadata_reachable",
            "adb_rows_with_latest_value",
            "rankable_rows_with_latest_value",
            "baseline_top5_rows_with_latest_value",
            "latest_year_min",
            "latest_year_max",
            "status",
            "notes",
        ],
    )
    write_csv(
        OUT / "port-hinterland-public-logistics-signals.csv",
        source_country_rows,
        [
            "iso3",
            "country",
            "rankable_in_committed_panel",
            "baseline_top5",
            "friction_rank",
            "friction_exposure_index",
            "old_trade_volume_proxy",
            "old_trade_volume_proxy_year",
            "old_lpi_overall_perception_score",
            "old_lpi_overall_perception_score_year",
            "lpi_infrastructure_perception_score",
            "lpi_infrastructure_perception_score_year",
            "lpi_timeliness_perception_score",
            "lpi_timeliness_perception_score_year",
            "container_port_traffic_teu",
            "container_port_traffic_teu_year",
            "rail_goods_million_ton_km",
            "rail_goods_million_ton_km_year",
            "road_goods_million_ton_km",
            "road_goods_million_ton_km_year",
            "air_freight_million_ton_km",
            "air_freight_million_ton_km_year",
            "any_actual_freight_proxy",
            "actual_freight_proxy_years",
        ],
    )

    print("=== Port-hinterland source-readiness audit ===")
    print(f"Baseline top 5: {baseline_top5}")
    print(f"WDI metadata reachable: {summary['wdi_metadata_records_reachable']}/{summary['wdi_indicators_requested']}")
    print(f"Rankable rows with container traffic: {rankable_with_container}/{len(rankable_iso)}")
    print(f"Rankable rows with any actual freight proxy: {rankable_with_any_actual}/{len(rankable_iso)}")
    print(f"Baseline top 5 with any actual freight proxy: {top5_with_any_actual}/5")
    print(f"Direct hinterland travel-time join built: {summary['analysis_ready_hinterland_travel_time']}")
    print(f"Wrote {OUT / 'port-hinterland-source-audit.json'}")
    print(f"Wrote {OUT / 'port-hinterland-source-readiness-sources.csv'}")
    print(f"Wrote {OUT / 'port-hinterland-public-logistics-signals.csv'}")


if __name__ == "__main__":
    main()
