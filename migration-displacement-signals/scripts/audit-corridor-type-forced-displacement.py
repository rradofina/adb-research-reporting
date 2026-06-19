"""Migration corridor-type falsifier using UNHCR forced-displacement stocks.

The denominator-switch report shows that absolute UN DESA emigrant stock and
emigrant stock as a share of origin population tell different stories. This
script adds a public corridor-type check: how much of each origin's emigrant
stock is plausibly a forced-displacement stock rather than labor/family
diaspora stock?

The script queries the UNHCR Refugee Data Finder population API for 2024,
origin by origin, and sums refugees, asylum-seekers, and other people in need
of international protection across foreign asylum countries. It compares that
stock to the committed UN DESA emigrant-stock panel and the per-population
deepening. It does not classify labor migration, family reunification, student
mobility, or temporary work. It only identifies the forced-displacement part
that public UNHCR data can observe.

Public data only. Raw JSON responses are cached under
`.cache/unhcr-forced-displacement/` with SHA-256 hashes.
attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/migration-displacement-signals")
CACHE = BASE / ".cache" / "unhcr-forced-displacement"
OUT = BASE / "generated"
PANEL_PATH = OUT / "migration-displacement-adb-panel.json"
PER_POP_PATH = OUT / "migration-per-population-deepening.json"

UNHCR_API_BASE = "https://api.unhcr.org/population/v1/population/"
YEAR = 2024
LIMIT = 10000


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def number(value):
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    text = str(value).strip().replace(",", "")
    if not text or text in {"-", "NA", "N/A", "null"}:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def fetch_json(url, cache_path):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "adb-research-factory/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
        cache_path.write_bytes(raw)
        mode = "live"
    except (urllib.error.URLError, TimeoutError) as exc:
        if not cache_path.exists():
            raise
        raw = cache_path.read_bytes()
        mode = f"cache fallback after {exc.__class__.__name__}"
    return json.loads(raw.decode("utf-8-sig")), {
        "url": url,
        "cache_path": str(cache_path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "fetch_mode": mode,
    }


def build_url(origin_iso, page=1):
    params = {
        "year": str(YEAR),
        "coo": origin_iso,
        "coa_all": "true",
        "cf_type": "ISO",
        "limit": str(LIMIT),
        "page": str(page),
    }
    return f"{UNHCR_API_BASE}?{urllib.parse.urlencode(params)}"


def fetch_origin(origin_iso):
    first_url = build_url(origin_iso, page=1)
    payload, record = fetch_json(first_url, CACHE / f"{origin_iso}_page_1.json")
    items = list(payload.get("items") or [])
    cache_records = [{**record, "origin_iso3": origin_iso, "page": 1}]
    max_pages = int(payload.get("maxPages") or 1)
    for page in range(2, max_pages + 1):
        url = build_url(origin_iso, page=page)
        page_payload, page_record = fetch_json(url, CACHE / f"{origin_iso}_page_{page}.json")
        items.extend(page_payload.get("items") or [])
        cache_records.append({**page_record, "origin_iso3": origin_iso, "page": page})
    return items, cache_records


def load_inputs():
    if not PANEL_PATH.exists():
        raise FileNotFoundError(f"{PANEL_PATH} missing. Run scripts/process-migration.py first.")
    if not PER_POP_PATH.exists():
        raise FileNotFoundError(f"{PER_POP_PATH} missing. Run scripts/deepen-per-population.py first.")
    panel = json.loads(PANEL_PATH.read_text(encoding="utf-8"))
    per_pop = json.loads(PER_POP_PATH.read_text(encoding="utf-8"))
    per_pop_rows = {row["iso3"]: row for row in per_pop.get("rows_by_share", [])}
    for row in per_pop.get("rows_withheld_no_population", []):
        per_pop_rows.setdefault(row["iso3"], row)
    return panel, per_pop, per_pop_rows


def classify_forced_share(share):
    if share is None:
        return "missing emigrant-stock denominator"
    if share >= 0.5:
        return "forced-displacement majority"
    if share >= 0.1:
        return "substantial forced-displacement component"
    if share > 0:
        return "low forced-displacement share"
    return "no forced-displacement rows"


def summarize_origin(origin_iso, country, items):
    forced_corridors = []
    forced_abroad = 0.0
    refugees_abroad = 0.0
    asylum_seekers_abroad = 0.0
    oip_abroad = 0.0
    other_concern_abroad = 0.0
    idps_in_origin = 0.0
    host_community_in_origin = 0.0

    for row in items:
        coo_iso = row.get("coo_iso") or row.get("coo")
        coa_iso = row.get("coa_iso") or row.get("coa")
        refugees = number(row.get("refugees"))
        asylum = number(row.get("asylum_seekers"))
        oip = number(row.get("oip"))
        ooc = number(row.get("ooc"))
        idps = number(row.get("idps"))
        hst = number(row.get("hst"))
        if coa_iso and coo_iso and coa_iso != coo_iso:
            forced = refugees + asylum + oip
            forced_abroad += forced
            refugees_abroad += refugees
            asylum_seekers_abroad += asylum
            oip_abroad += oip
            other_concern_abroad += ooc
            if forced > 0:
                forced_corridors.append({
                    "origin_iso3": origin_iso,
                    "origin_country": country,
                    "asylum_iso3": coa_iso,
                    "asylum_country": row.get("coa_name") or coa_iso,
                    "forced_displacement_abroad": int(round(forced)),
                    "refugees": int(round(refugees)),
                    "asylum_seekers": int(round(asylum)),
                    "other_people_in_need_protection": int(round(oip)),
                })
        elif coa_iso == coo_iso == origin_iso:
            idps_in_origin += idps
            host_community_in_origin += hst

    forced_corridors.sort(key=lambda row: -row["forced_displacement_abroad"])
    return {
        "forced_abroad": int(round(forced_abroad)),
        "refugees_abroad": int(round(refugees_abroad)),
        "asylum_seekers_abroad": int(round(asylum_seekers_abroad)),
        "other_people_in_need_protection_abroad": int(round(oip_abroad)),
        "other_concern_abroad_not_in_main_sum": int(round(other_concern_abroad)),
        "idps_in_origin_context": int(round(idps_in_origin)),
        "host_community_in_origin_context": int(round(host_community_in_origin)),
        "top_forced_corridors": forced_corridors[:5],
        "all_forced_corridors": forced_corridors,
    }


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    panel, per_pop, per_pop_rows = load_inputs()

    country_rows = []
    corridor_rows = []
    cache_records = []
    panel_rows = panel.get("rows", [])
    absolute_top5 = per_pop.get("absolute_top5", [])
    share_top5 = per_pop.get("share_top5", [])

    for source_row in panel_rows:
        iso = source_row["iso3"]
        country = source_row["country"]
        items, records = fetch_origin(iso)
        cache_records.extend(records)
        summary = summarize_origin(iso, country, items)
        corridor_rows.extend(summary["all_forced_corridors"])
        per_row = per_pop_rows.get(iso, {})
        emigrant_stock = source_row.get("emigrant_stock_2024")
        population = per_row.get("population_total")
        forced_share = summary["forced_abroad"] / emigrant_stock if emigrant_stock else None
        forced_pop_share = summary["forced_abroad"] / population if population else None
        country_rows.append({
            "iso3": iso,
            "country": country,
            "emigrant_stock_2024": emigrant_stock,
            "rank_absolute": per_row.get("rank_absolute"),
            "rank_share": per_row.get("rank_share"),
            "emigrant_pct_of_population": per_row.get("emigrant_pct_of_population"),
            "population_total": population,
            "forced_abroad_2024": summary["forced_abroad"],
            "refugees_abroad_2024": summary["refugees_abroad"],
            "asylum_seekers_abroad_2024": summary["asylum_seekers_abroad"],
            "other_people_in_need_protection_abroad_2024": summary["other_people_in_need_protection_abroad"],
            "forced_abroad_share_of_emigrant_stock": round(forced_share, 4) if forced_share is not None else None,
            "forced_abroad_pct_of_emigrant_stock": round(forced_share * 100, 1) if forced_share is not None else None,
            "forced_abroad_pct_of_population": round(forced_pop_share * 100, 2) if forced_pop_share is not None else None,
            "idps_in_origin_context_2024": summary["idps_in_origin_context"],
            "classification": classify_forced_share(forced_share),
            "in_absolute_top5": iso in absolute_top5,
            "in_share_top5": iso in share_top5,
            "top_forced_corridors": summary["top_forced_corridors"],
        })

    country_rows.sort(key=lambda row: -(row["forced_abroad_2024"] or 0))
    corridor_rows.sort(key=lambda row: -row["forced_displacement_abroad"])

    forced_majority = [row for row in country_rows if row["classification"] == "forced-displacement majority"]
    substantial = [
        row for row in country_rows
        if row["classification"] in {"forced-displacement majority", "substantial forced-displacement component"}
    ]
    absolute_top5_rows = [row for row in country_rows if row["iso3"] in absolute_top5]
    share_top5_rows = [row for row in country_rows if row["iso3"] in share_top5]
    afghanistan = next((row for row in country_rows if row["iso3"] == "AFG"), None)

    summary = {
        "origins_queried": len(panel_rows),
        "origins_with_forced_abroad_rows": sum(1 for row in country_rows if row["forced_abroad_2024"] > 0),
        "forced_displacement_majority_origins": len(forced_majority),
        "substantial_forced_displacement_component_origins": len(substantial),
        "absolute_top5_forced_displacement_majority": [
            row["iso3"] for row in absolute_top5_rows if row["classification"] == "forced-displacement majority"
        ],
        "share_top5_forced_displacement_majority": [
            row["iso3"] for row in share_top5_rows if row["classification"] == "forced-displacement majority"
        ],
        "afghanistan_forced_abroad_pct_of_emigrant_stock": (
            afghanistan["forced_abroad_pct_of_emigrant_stock"] if afghanistan else None
        ),
        "afghanistan_forced_abroad_2024": afghanistan["forced_abroad_2024"] if afghanistan else None,
        "top_forced_origin_iso3": country_rows[0]["iso3"] if country_rows else None,
        "top_forced_origin_stock": country_rows[0]["forced_abroad_2024"] if country_rows else None,
        "international_forced_displacement_fields_in_main_sum": [
            "refugees",
            "asylum_seekers",
            "other people in need of international protection",
        ],
        "excluded_from_main_sum": [
            "IDPs because they are inside the origin country",
            "returned refugees and returned IDPs because they are solution/return stocks",
            "stateless and host community fields because they are not emigrant-stock corridor types",
        ],
    }

    payload = {
        "program": "migration-displacement-signals",
        "analysis": "corridor-type forced-displacement audit for emigrant-stock denominator switch",
        "claim_scope": (
            "Source-readiness and falsifier audit. UNHCR forced-displacement "
            "stocks identify the refugee/asylum/international-protection component "
            "of UN DESA emigrant-stock origins. This does not identify labor, "
            "family, student, or temporary work corridors, and it is not a welfare "
            "or fragility ranking."
        ),
        "year": YEAR,
        "retrieved_at": retrieved_at,
        "source": {
            "name": "UNHCR Refugee Data Finder population API",
            "url": UNHCR_API_BASE,
            "docs": "https://api.unhcr.org/docs/refugee-statistics.html",
            "methodology": "https://www.unhcr.org/refugee-statistics/methodology",
            "query_pattern": build_url("{ISO3}", page=1),
        },
        "summary": summary,
        "country_rows": country_rows,
        "top_forced_corridors": corridor_rows[:25],
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(per_pop)
    combined["analysis"] = "emigrant stock denominator switch plus UNHCR forced-displacement corridor-type audit"
    combined["corridor_type_falsifier"] = payload
    combined["claim_scope"] = (
        f"{per_pop.get('claim_scope', '')} UNHCR corridor-type data are used only "
        "as a forced-displacement falsifier; they do not classify labor/family "
        "migration and do not turn the share ranking into a welfare claim."
    ).strip()
    combined["generated_at"] = retrieved_at

    country_csv_rows = []
    for row in country_rows:
        flat = {key: value for key, value in row.items() if key != "top_forced_corridors"}
        top = row.get("top_forced_corridors") or []
        flat["top_forced_corridor_1"] = (
            f"{top[0]['asylum_iso3']} {top[0]['forced_displacement_abroad']}" if top else ""
        )
        country_csv_rows.append(flat)

    standalone_path = OUT / "migration-corridor-type-forced-displacement.json"
    combined_path = OUT / "migration-denominator-corridor-type-audit.json"
    country_csv_path = OUT / "migration-corridor-type-forced-displacement-country.csv"
    corridors_csv_path = OUT / "migration-corridor-type-forced-displacement-corridors.csv"
    standalone_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    with country_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(country_csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(country_csv_rows)

    corridor_fields = [
        "origin_iso3",
        "origin_country",
        "asylum_iso3",
        "asylum_country",
        "forced_displacement_abroad",
        "refugees",
        "asylum_seekers",
        "other_people_in_need_protection",
    ]
    with corridors_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=corridor_fields)
        writer.writeheader()
        writer.writerows(corridor_rows)

    print("=== Migration corridor-type forced-displacement audit ===")
    print(f"Origins queried: {summary['origins_queried']}")
    print(f"Origins with forced-displacement abroad rows: {summary['origins_with_forced_abroad_rows']}")
    print(f"Forced-displacement-majority origins: {summary['forced_displacement_majority_origins']}")
    print(f"Substantial forced-displacement component origins: {summary['substantial_forced_displacement_component_origins']}")
    print(
        "Afghanistan forced-abroad share of UN DESA emigrant stock: "
        f"{summary['afghanistan_forced_abroad_pct_of_emigrant_stock']}%"
    )
    print(f"Top forced origin: {summary['top_forced_origin_iso3']} ({summary['top_forced_origin_stock']:,})")
    print(f"Wrote {combined_path}")
    print(f"Wrote {country_csv_path}")
    print(f"Wrote {corridors_csv_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
