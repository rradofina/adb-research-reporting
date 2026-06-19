"""Grid reliability source-readiness audit using public World Bank proxies.

This is a source audit, not a reliability estimate. It joins the existing
WRI generation fuel-concentration deepening to public World Bank firm-outage,
Doing Business, and B-READY utility-service indicators. The purpose is to ask
whether a public reliability-proxy crosswalk exists before the report makes
any claim about outages, reserve margins, dispatch, or heat stress.

Every number comes from the World Bank API or the committed
`grid-generation-deepening.json` artifact. Raw API responses are cached under
`.cache/wdi-reliability-proxies/` with SHA-256 hashes. Public data only.
attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/grid-reliability-heat")
CACHE = BASE / ".cache" / "wdi-reliability-proxies"
OUT = BASE / "generated"
GENERATION_ARTIFACT = OUT / "grid-generation-deepening.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
PER_PAGE = 20000
HIGH_GENERATION_HERFINDAHL = 0.8

ADB_DMCS = {
    "AFG": "Afghanistan",
    "ARM": "Armenia",
    "AZE": "Azerbaijan",
    "BGD": "Bangladesh",
    "BTN": "Bhutan",
    "BRN": "Brunei Darussalam",
    "KHM": "Cambodia",
    "CHN": "China",
    "FJI": "Fiji",
    "GEO": "Georgia",
    "HKG": "Hong Kong SAR, China",
    "IND": "India",
    "IDN": "Indonesia",
    "KAZ": "Kazakhstan",
    "KIR": "Kiribati",
    "KGZ": "Kyrgyzstan",
    "LAO": "Lao PDR",
    "MYS": "Malaysia",
    "MDV": "Maldives",
    "MHL": "Marshall Islands",
    "FSM": "Micronesia, Fed. Sts.",
    "MNG": "Mongolia",
    "MMR": "Myanmar",
    "NPL": "Nepal",
    "PAK": "Pakistan",
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
        "id": "IC.ELC.OUTG",
        "group": "catalog_no_adb_rows",
        "short_label": "Outages per firm/month (new series)",
    },
    {
        "id": "IC.ELC.OUTG.DY",
        "group": "catalog_no_adb_rows",
        "short_label": "Electrical outage days",
    },
    {
        "id": "IC.ELC.OUTG.HR",
        "group": "catalog_no_adb_rows",
        "short_label": "Average outage duration hours (new series)",
    },
    {
        "id": "IC.ELC.OUTG.ZS",
        "group": "firm_outage",
        "short_label": "Firms with electrical outages",
    },
    {
        "id": "IC.FRM.OUTG.ZS",
        "group": "firm_outage",
        "short_label": "Sales lost to outages",
    },
    {
        "id": "IC.FRM.INFRA.IN16",
        "group": "enterprise_survey_legacy",
        "short_label": "Firms with electrical outages (legacy)",
    },
    {
        "id": "IC.FRM.INFRA.IN2",
        "group": "enterprise_survey_legacy",
        "short_label": "Outages per month (legacy)",
    },
    {
        "id": "IC.FRM.INFRA.IN3_C",
        "group": "enterprise_survey_legacy",
        "short_label": "Typical outage duration hours (legacy)",
    },
    {
        "id": "IC.FRM.INFRA.IN4_C",
        "group": "enterprise_survey_legacy",
        "short_label": "Sales lost to outages (legacy)",
    },
    {
        "id": "IC.ELC.SAID.XD.DB1619",
        "group": "doing_business",
        "short_label": "SAIDI, Doing Business method",
    },
    {
        "id": "IC.ELC.RSTT.XD.08.DB1619",
        "group": "doing_business",
        "short_label": "Reliability/tariff transparency index",
    },
    {
        "id": "IC.BRE.US.OS",
        "group": "bready_utility_services",
        "short_label": "B-READY utility services overall",
    },
    {
        "id": "IC.BRE.US.P1",
        "group": "bready_utility_services",
        "short_label": "B-READY connection quality",
    },
    {
        "id": "IC.BRE.US.P2",
        "group": "bready_utility_services",
        "short_label": "B-READY utility reliability",
    },
    {
        "id": "IC.BRE.US.P3",
        "group": "bready_utility_services",
        "short_label": "B-READY transparency/safety",
    },
]

DISPLAY_INDICATORS = [
    "IC.ELC.OUTG.ZS",
    "IC.FRM.OUTG.ZS",
    "IC.FRM.INFRA.IN2",
    "IC.FRM.INFRA.IN3_C",
    "IC.ELC.SAID.XD.DB1619",
    "IC.ELC.RSTT.XD.08.DB1619",
    "IC.BRE.US.OS",
]


def slugify_indicator(indicator_id):
    return re.sub(r"[^A-Za-z0-9]+", "_", indicator_id).strip("_")


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_bytes(url, cache_path):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "adb-research-factory/1.0"})
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
        cache_path.write_bytes(raw)
        return raw, "live"
    except (urllib.error.URLError, TimeoutError) as exc:
        if cache_path.exists():
            return cache_path.read_bytes(), f"cache fallback after {exc.__class__.__name__}"
        raise


def fetch_json(url, cache_path):
    raw, mode = fetch_bytes(url, cache_path)
    try:
        return json.loads(raw.decode("utf-8-sig")), {
            "url": url,
            "cache_path": str(cache_path.relative_to(BASE)),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "fetch_mode": mode,
        }
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse JSON from {url}: {exc}") from exc


def unwrap_world_bank_rows(payload):
    if isinstance(payload, list) and len(payload) >= 2 and isinstance(payload[1], list):
        return payload[1]
    return []


def indicator_name(metadata_payload, fallback):
    rows = unwrap_world_bank_rows(metadata_payload)
    if rows and isinstance(rows[0], dict):
        return rows[0].get("name") or rows[0].get("sourceNote") or fallback
    return fallback


def latest_adb_values(data_payload):
    latest = {}
    observations_global = 0
    observations_adb = 0
    for row in unwrap_world_bank_rows(data_payload):
        if not isinstance(row, dict):
            continue
        value = row.get("value")
        if not isinstance(value, (int, float)):
            continue
        observations_global += 1
        iso = row.get("countryiso3code")
        if iso not in ADB_DMCS:
            continue
        observations_adb += 1
        year = int(row.get("date"))
        if iso not in latest or year > latest[iso]["year"]:
            latest[iso] = {
                "iso3": iso,
                "country": ADB_DMCS[iso],
                "year": year,
                "value": float(value),
            }
    return latest, observations_global, observations_adb


def load_generation_deepening():
    if not GENERATION_ARTIFACT.exists():
        raise FileNotFoundError(
            f"{GENERATION_ARTIFACT} is missing. Run grid-reliability-heat/scripts/deepen-generation.py first."
        )
    with GENERATION_ARTIFACT.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_latest_values(latest_by_indicator):
    out = {iso: {} for iso in ADB_DMCS}
    for indicator_id, latest in latest_by_indicator.items():
        key = slugify_indicator(indicator_id)
        for iso, record in latest.items():
            out[iso][f"{key}_value"] = record["value"]
            out[iso][f"{key}_year"] = record["year"]
    return out


def indicator_presence(row, indicator_ids):
    return [indicator_id for indicator_id in indicator_ids if row.get(f"{slugify_indicator(indicator_id)}_value") is not None]


def format_year_span(years):
    if not years:
        return None
    if min(years) == max(years):
        return str(min(years))
    return f"{min(years)}-{max(years)}"


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    retrieved_at = utc_stamp()
    generation = load_generation_deepening()
    generation_rows = {row["iso3"]: row for row in generation.get("rows_by_generation_herfindahl", [])}
    withheld_generation = set(generation.get("rows_withheld_low_coverage", []))
    all_generation_candidates = {}
    for row in generation.get("rows_by_generation_herfindahl", []):
        all_generation_candidates[row["iso3"]] = row
    for iso in withheld_generation:
        all_generation_candidates.setdefault(iso, {"iso3": iso, "country": ADB_DMCS.get(iso, iso)})

    latest_by_indicator = {}
    indicator_records = []
    cache_records = []

    for indicator in INDICATORS:
        indicator_id = indicator["id"]
        slug = slugify_indicator(indicator_id)
        data_url = (
            f"{WORLD_BANK_API_BASE}/country/all/indicator/{indicator_id}"
            f"?format=json&per_page={PER_PAGE}"
        )
        metadata_url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
        data_payload, data_record = fetch_json(data_url, CACHE / f"{slug}_data.json")
        metadata_payload, metadata_record = fetch_json(metadata_url, CACHE / f"{slug}_metadata.json")
        latest, observations_global, observations_adb = latest_adb_values(data_payload)
        latest_by_indicator[indicator_id] = latest

        years = sorted({record["year"] for record in latest.values()})
        indicator_records.append({
            "indicator_id": indicator_id,
            "indicator_name": indicator_name(metadata_payload, indicator["short_label"]),
            "short_label": indicator["short_label"],
            "group": indicator["group"],
            "adb_dmcs_with_latest": len(latest),
            "observations_global": observations_global,
            "observations_adb": observations_adb,
            "latest_year_span": format_year_span(years),
            "data_url": data_url,
            "metadata_url": metadata_url,
            "data_sha256": data_record["sha256"],
            "metadata_sha256": metadata_record["sha256"],
            "data_fetch_mode": data_record["fetch_mode"],
            "metadata_fetch_mode": metadata_record["fetch_mode"],
        })
        cache_records.append({**data_record, "indicator_id": indicator_id, "kind": "data"})
        cache_records.append({**metadata_record, "indicator_id": indicator_id, "kind": "metadata"})

    flat_latest = flatten_latest_values(latest_by_indicator)
    proxy_indicator_ids = [i["id"] for i in INDICATORS if i["group"] != "catalog_no_adb_rows"]
    firm_indicator_ids = [
        i["id"] for i in INDICATORS if i["group"] in {"firm_outage", "enterprise_survey_legacy"}
    ]
    db_indicator_ids = [i["id"] for i in INDICATORS if i["group"] == "doing_business"]
    bready_indicator_ids = [i["id"] for i in INDICATORS if i["group"] == "bready_utility_services"]

    country_rows = []
    for iso, country in ADB_DMCS.items():
        gen_row = all_generation_candidates.get(iso, {})
        row = {
            "iso3": iso,
            "country": country,
            "generation_concentration_ready": iso in generation_rows,
            "generation_withheld_low_coverage": iso in withheld_generation,
            "herfindahl_generation": gen_row.get("herfindahl_generation"),
            "herfindahl_capacity": gen_row.get("herfindahl_capacity"),
            "generation_coverage": gen_row.get("generation_coverage"),
            "top_fuel_generation": gen_row.get("top_fuel_generation"),
            "top_fuel_capacity": gen_row.get("top_fuel_capacity"),
        }
        row.update(flat_latest[iso])
        any_proxy = indicator_presence(row, proxy_indicator_ids)
        firm_proxy = indicator_presence(row, firm_indicator_ids)
        db_proxy = indicator_presence(row, db_indicator_ids)
        bready_proxy = indicator_presence(row, bready_indicator_ids)
        high_generation = (
            isinstance(row.get("herfindahl_generation"), (int, float))
            and row["herfindahl_generation"] >= HIGH_GENERATION_HERFINDAHL
        )
        row.update({
            "any_reliability_proxy_ready": bool(any_proxy),
            "firm_outage_proxy_ready": bool(firm_proxy),
            "doing_business_proxy_ready": bool(db_proxy),
            "bready_utility_proxy_ready": bool(bready_proxy),
            "proxy_indicator_count": len(any_proxy),
            "proxy_indicators_present": ";".join(any_proxy),
            "generation_and_proxy_ready": bool(row["generation_concentration_ready"] and any_proxy),
            "high_generation_concentration": high_generation,
            "high_generation_concentration_and_proxy": bool(high_generation and any_proxy),
        })
        country_rows.append(row)

    def count_if(predicate):
        return sum(1 for row in country_rows if predicate(row))

    source_years = []
    for row in country_rows:
        for indicator_id in proxy_indicator_ids:
            year = row.get(f"{slugify_indicator(indicator_id)}_year")
            if isinstance(year, int):
                source_years.append(year)

    high_generation_proxy_rows = [
        row for row in country_rows if row["high_generation_concentration_and_proxy"]
    ]
    high_generation_proxy_rows.sort(
        key=lambda row: (-(row.get("herfindahl_generation") or 0), row["iso3"])
    )

    summary = {
        "adb_dmc_roster_n": len(ADB_DMCS),
        "indicators_queried": len(INDICATORS),
        "indicators_with_adb_proxy_rows": sum(
            1 for record in indicator_records if record["adb_dmcs_with_latest"] > 0
        ),
        "generation_ranked_rows": len(generation_rows),
        "generation_withheld_low_coverage_rows": len(withheld_generation),
        "dmcs_with_any_reliability_proxy": count_if(lambda row: row["any_reliability_proxy_ready"]),
        "dmcs_with_firm_outage_proxy": count_if(lambda row: row["firm_outage_proxy_ready"]),
        "dmcs_with_doing_business_proxy": count_if(lambda row: row["doing_business_proxy_ready"]),
        "dmcs_with_bready_utility_proxy": count_if(lambda row: row["bready_utility_proxy_ready"]),
        "dmcs_with_generation_and_any_proxy": count_if(lambda row: row["generation_and_proxy_ready"]),
        "high_generation_herfindahl_threshold": HIGH_GENERATION_HERFINDAHL,
        "high_generation_concentration_rows": count_if(lambda row: row["high_generation_concentration"]),
        "high_generation_concentration_and_proxy_rows": len(high_generation_proxy_rows),
        "high_generation_concentration_without_proxy_rows": count_if(
            lambda row: row["high_generation_concentration"] and not row["any_reliability_proxy_ready"]
        ),
        "withheld_generation_but_proxy_rows": count_if(
            lambda row: row["generation_withheld_low_coverage"] and row["any_reliability_proxy_ready"]
        ),
        "proxy_latest_year_span": format_year_span(source_years),
    }

    headline_rows = []
    for row in high_generation_proxy_rows[:10]:
        headline_rows.append({
            "iso3": row["iso3"],
            "country": row["country"],
            "herfindahl_generation": row["herfindahl_generation"],
            "generation_coverage": row["generation_coverage"],
            "top_fuel_generation": row["top_fuel_generation"],
            "firms_with_outages_pct": row.get("IC_ELC_OUTG_ZS_value"),
            "firms_with_outages_year": row.get("IC_ELC_OUTG_ZS_year"),
            "sales_lost_to_outages_pct": row.get("IC_FRM_OUTG_ZS_value"),
            "sales_lost_to_outages_year": row.get("IC_FRM_OUTG_ZS_year"),
            "legacy_outages_per_month": row.get("IC_FRM_INFRA_IN2_value"),
            "legacy_outages_per_month_year": row.get("IC_FRM_INFRA_IN2_year"),
            "saidi": row.get("IC_ELC_SAID_XD_DB1619_value"),
            "saidi_year": row.get("IC_ELC_SAID_XD_DB1619_year"),
            "bready_utility_services": row.get("IC_BRE_US_OS_value"),
            "bready_utility_services_year": row.get("IC_BRE_US_OS_year"),
            "proxy_indicator_count": row["proxy_indicator_count"],
        })

    readiness = {
        "retrieved_at": retrieved_at,
        "world_bank_api_base": WORLD_BANK_API_BASE,
        "generation_artifact": str(GENERATION_ARTIFACT.relative_to(BASE)),
        "summary": summary,
        "indicator_records": indicator_records,
        "cache_records": cache_records,
        "country_rows": country_rows,
        "high_generation_proxy_rows": headline_rows,
        "display_indicators": DISPLAY_INDICATORS,
        "claim_scope": (
            "Public source-readiness audit only. World Bank firm-outage, Doing "
            "Business, and B-READY indicators are proxies with mixed vintages "
            "and methods; they do not measure reserve margin, dispatch, "
            "outage events, or heat-stress reliability."
        ),
    }

    combined = dict(generation)
    combined["analysis"] = "fuel-concentration generation deepening plus public reliability-proxy source-readiness"
    combined["reliability_proxy_readiness"] = readiness
    combined["claim_scope"] = (
        f"{generation.get('claim_scope', '')} Public reliability proxies were "
        "joined only to test source readiness; they are not used as a grid "
        "reliability ranking."
    ).strip()
    combined["generated_at"] = retrieved_at

    combined_path = OUT / "grid-generation-reliability-source-audit.json"
    readiness_json_path = OUT / "grid-public-reliability-proxy-readiness.json"
    country_csv_path = OUT / "grid-public-reliability-proxy-readiness-country.csv"
    indicator_csv_path = OUT / "grid-public-reliability-proxy-readiness-indicators.csv"

    readiness_json_path.write_text(json.dumps(readiness, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    country_fields = list(country_rows[0].keys())
    for indicator in INDICATORS:
        indicator_id = indicator["id"]
        key = slugify_indicator(indicator_id)
        for suffix in ("value", "year"):
            field = f"{key}_{suffix}"
            if field not in country_fields:
                country_fields.append(field)
    with country_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=country_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(country_rows)

    with indicator_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(indicator_records[0].keys()))
        writer.writeheader()
        writer.writerows(indicator_records)

    print("=== Public reliability-proxy source-readiness audit ===")
    print(f"Indicators queried: {summary['indicators_queried']}")
    print(f"DMCs with any public reliability proxy: {summary['dmcs_with_any_reliability_proxy']}")
    print(f"DMCs with generation concentration and any proxy: {summary['dmcs_with_generation_and_any_proxy']}")
    print(
        "High generation concentration + proxy rows: "
        f"{summary['high_generation_concentration_and_proxy_rows']}"
    )
    print(f"Proxy latest-year span: {summary['proxy_latest_year_span']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {country_csv_path}")
    print(f"Wrote {indicator_csv_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
