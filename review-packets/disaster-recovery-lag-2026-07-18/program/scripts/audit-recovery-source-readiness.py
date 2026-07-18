"""Recovery-source readiness audit for disaster-recovery-lag.

The existing disaster report is a metric falsifier: it proves the EM-DAT
country-burden top two is not stable across defensible metrics. It still does
not measure recovery lag. This script checks the next source bridge needed for
that upgrade:

  1. The committed EM-DAT country-profiles workbook is aggregate
     country-year-disaster-type data and has no event id, month/day, or
     location fields that can support recovery curves.
  2. The public GDIS dataset supplies geocoded disaster locations and EM-DAT
     disaster identifiers for 1960-2018. It is downloaded from the PRIO mirror
     and cross-checked against NASA CMR/SEDAC metadata.
  3. NASA CMR identifies Black Marble VNP46A3 monthly nighttime lights as
     starting on 2012-01-01, creating a GDIS x VIIRS overlap window of
     2012-2018.

The output is a source-readiness object and an event queue. It is not a
recovery-lag estimate.
attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import openpyxl


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = PROGRAM / ".cache" / "gdis"
OUT = PROGRAM / "generated"
EMDAT_WORKBOOK = PROGRAM / ".cache" / "emdat_country_profiles.xlsx"

GDIS_PRIO_ZIP_URL = (
    "https://cdn.cloud.prio.org/files/cffb60dc-5978-4eec-a1d2-14551067d84d/"
    "gdis-1960-2018-disasterlocations-csv.zip?inline=true"
)
GDIS_CMR_GRANULES_URL = (
    "https://cmr.earthdata.nasa.gov/search/granules.json?"
    "collection_concept_id=C3540930147-ESDIS&page_size=20"
)
GDIS_NASA_PORTAL_URL = "https://data.nasa.gov/dataset/geocoded-disasters-gdis-dataset"
GDIS_DOI_URL = "https://doi.org/10.7927/61jv-th84"
GDIS_PRIO_PAGE_URL = "https://www.prio.org/publications/12638"
BLACK_MARBLE_COLLECTIONS_URL = (
    "https://cmr.earthdata.nasa.gov/search/collections.json?"
    + urllib.parse.urlencode({"keyword": "VNP46A3", "page_size": "5"})
)
BLACK_MARBLE_PRODUCT_URL = (
    "https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A3"
)

USER_AGENT = "DevelopmentBlindspotsLab/0.1 research pipeline"

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
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, path: Path, refresh_env: str = "DISASTER_RECOVERY_REFRESH") -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    from_cache = path.exists() and os.environ.get(refresh_env) != "1"
    if not from_cache:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as response:
            path.write_bytes(response.read())
    return {
        "url": url,
        "cache_path": str(path.relative_to(ROOT)),
        "retrieved_at": now_utc(),
        "from_cache": from_cache,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def fetch_json(url: str, path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    record = fetch(url, path)
    with path.open(encoding="utf-8") as f:
        return json.load(f), record


def inspect_emdat_workbook() -> dict[str, Any]:
    # This workbook reports a stale sheet dimension under read_only=True in
    # openpyxl, so read it in normal mode like process-disaster.py does.
    wb = openpyxl.load_workbook(EMDAT_WORKBOOK, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = [str(v) for v in rows[0]]
    cols = {h: i for i, h in enumerate(header)}
    data_rows = rows[2:]
    filtered = []
    for row in data_rows:
        if row is None or all(value is None for value in row) or len(row) < len(header):
            continue
        iso = row[cols["ISO"]]
        if iso not in ADB_DMCS:
            continue
        try:
            year = int(row[cols["Year"]])
        except (TypeError, ValueError):
            continue
        if 2000 <= year <= 2025:
            filtered.append(row)

    missing_for_recovery = [
        "disasterno",
        "event_id",
        "start_month",
        "start_day",
        "latitude",
        "longitude",
        "location",
    ]
    header_lower = {h.lower() for h in header}
    return {
        "file": str(EMDAT_WORKBOOK.relative_to(ROOT)),
        "sheet": ws.title,
        "rows_total_including_header_and_hxl": len(rows),
        "rows_in_adb_2000_2025_filter": len(filtered),
        "columns": header,
        "has_disaster_identifier": any(k in header_lower for k in ["disasterno", "disaster no", "disaster_id"]),
        "has_month_day": any("month" in h.lower() for h in header) and any("day" in h.lower() for h in header),
        "has_location_geometry": any(k in header_lower for k in ["latitude", "longitude", "location"]),
        "missing_fields_for_recovery_curve": missing_for_recovery,
        "readiness_lane": "aggregate_burden_only_no_event_recovery_join",
    }


def load_gdis_rows(zip_path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    with zipfile.ZipFile(zip_path) as zf:
        csv_name = next(name for name in zf.namelist() if name.lower().endswith(".csv"))
        codebook_name = next((name for name in zf.namelist() if "codebook" in name.lower()), None)
        with zf.open(csv_name) as f:
            wrapper = io.TextIOWrapper(f, encoding="utf-8-sig", newline="")
            rows = list(csv.DictReader(wrapper))
        members = [
            {
                "name": info.filename,
                "bytes": info.file_size,
            }
            for info in zf.infolist()
        ]
    return rows, {
        "csv_member": csv_name,
        "codebook_member": codebook_name,
        "members": members,
    }


def black_marble_metadata(collections: dict[str, Any]) -> dict[str, Any]:
    entries = collections.get("feed", {}).get("entry", [])
    v2 = next((entry for entry in entries if entry.get("short_name") == "VNP46A3" and entry.get("version_id") == "2"), None)
    selected = v2 or next((entry for entry in entries if entry.get("short_name") == "VNP46A3"), None)
    if not selected:
        raise RuntimeError("CMR did not return a VNP46A3 collection")
    return {
        "cmr_collection_id": selected.get("id"),
        "short_name": selected.get("short_name"),
        "version_id": selected.get("version_id"),
        "title": selected.get("title"),
        "time_start": selected.get("time_start"),
        "time_end": selected.get("time_end"),
        "product_page": BLACK_MARBLE_PRODUCT_URL,
    }


def summarize_gdis(gdis_rows: list[dict[str, str]], black_marble_start_year: int) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    total_locations = len(gdis_rows)
    total_ids = {row["id"] for row in gdis_rows}
    total_disasternos = {row["disasterno"] for row in gdis_rows}
    years = [int(row["year"]) for row in gdis_rows if row.get("year")]

    dmc_rows = [row for row in gdis_rows if row["iso3"] in ADB_DMCS]
    dmc_2000_2018 = [row for row in dmc_rows if 2000 <= int(row["year"]) <= 2018]
    dmc_viirs = [row for row in dmc_rows if black_marble_start_year <= int(row["year"]) <= 2018]

    by_country: dict[str, dict[str, Any]] = {}
    for iso, country in ADB_DMCS.items():
        rows_2000 = [row for row in dmc_2000_2018 if row["iso3"] == iso]
        rows_viirs = [row for row in dmc_viirs if row["iso3"] == iso]
        type_counts = Counter(row["disastertype"].strip() for row in rows_viirs)
        levels = Counter(row["level"] for row in rows_viirs if row.get("level"))
        by_country[iso] = {
            "iso3": iso,
            "country": country,
            "gdis_locations_2000_2018": len(rows_2000),
            "gdis_unique_ids_2000_2018": len({row["id"] for row in rows_2000}),
            "gdis_unique_disasternos_2000_2018": len({row["disasterno"] for row in rows_2000}),
            "gdis_locations_black_marble_window_2012_2018": len(rows_viirs),
            "gdis_unique_ids_black_marble_window_2012_2018": len({row["id"] for row in rows_viirs}),
            "gdis_unique_disasternos_black_marble_window_2012_2018": len({row["disasterno"] for row in rows_viirs}),
            "top_disaster_types_2012_2018": "; ".join(f"{k}:{v}" for k, v in type_counts.most_common(3)),
            "dominant_admin_levels_2012_2018": "; ".join(f"L{k}:{v}" for k, v in levels.most_common(3)),
            "readiness_lane": "gdis_viirs_overlap_geometry_queue" if rows_viirs else "no_gdis_viirs_overlap",
        }

    event_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in dmc_viirs:
        event_groups[(row["iso3"], row["id"])].append(row)

    event_queue = []
    for (iso, event_id), members in event_groups.items():
        first = members[0]
        levels = Counter(row["level"] for row in members if row.get("level"))
        adm1 = sorted({row["adm1"] for row in members if row.get("adm1")})
        adm2 = sorted({row["adm2"] for row in members if row.get("adm2")})
        event_queue.append(
            {
                "iso3": iso,
                "country": ADB_DMCS[iso],
                "gdis_id": event_id,
                "disasterno": first["disasterno"],
                "year": int(first["year"]),
                "disastertype": first["disastertype"].strip(),
                "locations": len(members),
                "admin_levels": "; ".join(f"L{k}:{v}" for k, v in levels.most_common()),
                "adm1_sample": "; ".join(adm1[:6]),
                "adm2_sample": "; ".join(adm2[:6]),
                "readiness_lane": "needs_emdat_event_date_and_black_marble_extraction",
            }
        )
    event_queue.sort(key=lambda row: (-row["locations"], row["iso3"], row["gdis_id"]))

    country_rows = sorted(
        by_country.values(),
        key=lambda row: (
            -row["gdis_unique_ids_black_marble_window_2012_2018"],
            -row["gdis_locations_black_marble_window_2012_2018"],
            row["iso3"],
        ),
    )

    summary = {
        "gdis_locations_total_csv": total_locations,
        "gdis_unique_ids_total_csv": len(total_ids),
        "gdis_unique_disasternos_total_csv": len(total_disasternos),
        "gdis_metadata_disaster_count_from_landing_pages": 9924,
        "gdis_year_min": min(years),
        "gdis_year_max": max(years),
        "adb_locations_all_years": len(dmc_rows),
        "adb_unique_ids_all_years": len({row["id"] for row in dmc_rows}),
        "adb_locations_2000_2018": len(dmc_2000_2018),
        "adb_unique_ids_2000_2018": len({row["id"] for row in dmc_2000_2018}),
        "adb_unique_disasternos_2000_2018": len({row["disasterno"] for row in dmc_2000_2018}),
        "adb_locations_black_marble_window_2012_2018": len(dmc_viirs),
        "adb_unique_ids_black_marble_window_2012_2018": len({row["id"] for row in dmc_viirs}),
        "adb_unique_disasternos_black_marble_window_2012_2018": len({row["disasterno"] for row in dmc_viirs}),
        "countries_with_gdis_viirs_overlap": sum(
            1 for row in country_rows if row["gdis_unique_ids_black_marble_window_2012_2018"] > 0
        ),
        "top_overlap_countries": country_rows[:8],
        "top_event_queue": event_queue[:20],
    }
    return summary, country_rows, event_queue


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"No rows to write: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    gdis_granules, gdis_cmr_record = fetch_json(GDIS_CMR_GRANULES_URL, CACHE / "gdis-cmr-granules.json")
    black_marble_collections, black_marble_record = fetch_json(
        BLACK_MARBLE_COLLECTIONS_URL, CACHE / "black-marble-vnp46a3-cmr-collections.json"
    )
    black_marble = black_marble_metadata(black_marble_collections)
    black_marble_start_year = int(str(black_marble["time_start"])[:4])

    gdis_zip_record = fetch(GDIS_PRIO_ZIP_URL, CACHE / "gdis-1960-2018-disasterlocations-csv.zip")
    gdis_rows, gdis_zip_members = load_gdis_rows(CACHE / "gdis-1960-2018-disasterlocations-csv.zip")
    emdat = inspect_emdat_workbook()
    gdis_summary, country_rows, event_queue = summarize_gdis(gdis_rows, black_marble_start_year)

    cmr_granules = []
    for entry in gdis_granules.get("feed", {}).get("entry", []):
        data_links = [
            link.get("href")
            for link in entry.get("links", [])
            if link.get("href") and "fedsearch/1.1/data" in link.get("rel", "")
        ]
        cmr_granules.append(
            {
                "title": entry.get("title"),
                "granule_size": entry.get("granule_size"),
                "updated": entry.get("updated"),
                "time_start": entry.get("time_start"),
                "time_end": entry.get("time_end"),
                "data_links": data_links,
            }
        )

    payload = {
        "program": "disaster-recovery-lag",
        "analysis": "Recovery-lag source-readiness audit",
        "claim_scope": (
            "Source-readiness object for a future recovery-lag metric. It checks "
            "whether the current EM-DAT aggregate workbook can join to event "
            "geography and whether public GDIS and NASA Black Marble sources "
            "create a feasible 2012-2018 pilot queue. It does not estimate "
            "recovery duration."
        ),
        "summary": {
            **gdis_summary,
            "current_emdat_rows_in_adb_2000_2025_filter": emdat["rows_in_adb_2000_2025_filter"],
            "current_emdat_has_disaster_identifier": emdat["has_disaster_identifier"],
            "current_emdat_has_month_day": emdat["has_month_day"],
            "current_emdat_has_location_geometry": emdat["has_location_geometry"],
            "black_marble_vnp46a3_time_start": black_marble["time_start"],
            "black_marble_vnp46a3_version": black_marble["version_id"],
            "recovery_curve_ready": False,
        },
        "source_gates": [
            {
                "gate": "Current EM-DAT cache",
                "status": "blocks_recovery_curve",
                "finding": (
                    "The committed workbook is country-year-disaster-type aggregate data; "
                    "it has no disaster identifier, month/day, or geometry columns."
                ),
            },
            {
                "gate": "GDIS event geography",
                "status": "usable_for_event_geography_through_2018",
                "finding": (
                    "The GDIS CSV supplies event/location identifiers, country, year, "
                    "disaster type, administrative names, and centroids."
                ),
            },
            {
                "gate": "Black Marble monthly nighttime lights",
                "status": "usable_proxy_window_from_2012",
                "finding": (
                    "NASA CMR returns VNP46A3 version 2 with time_start 2012-01-01; "
                    "intersecting that with GDIS v1 creates a 2012-2018 source queue."
                ),
            },
            {
                "gate": "Recovery metric",
                "status": "not_ready",
                "finding": (
                    "A true recovery-lag metric still needs an event-level EM-DAT table "
                    "with disasterno and event dates, plus Black Marble extraction over "
                    "GDIS footprints or an accepted affected-area proxy."
                ),
            },
        ],
        "sources": {
            "current_emdat_country_profiles": emdat,
            "gdis": {
                "nasa_portal": GDIS_NASA_PORTAL_URL,
                "doi": GDIS_DOI_URL,
                "prio_page": GDIS_PRIO_PAGE_URL,
                "prio_zip_download": gdis_zip_record,
                "cmr_granules": cmr_granules,
                "cmr_query": gdis_cmr_record,
                "zip_members": gdis_zip_members,
                "metadata_note": (
                    "NASA/SEDAC and the GDIS paper describe 39,953 locations for "
                    "9,924 disasters. The parsed CSV has 39,953 rows, 9,924 unique "
                    "GDIS id values, and 9,018 unique disasterno values."
                ),
            },
            "black_marble_vnp46a3": {
                **black_marble,
                "cmr_query": black_marble_record,
            },
        },
        "country_rows": country_rows,
        "event_queue_rows": event_queue,
        "attestation_chain": "ai-first",
        "generated_at": now_utc(),
    }

    with (OUT / "disaster-recovery-lag-recovery-source-readiness.json").open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    write_csv(OUT / "disaster-recovery-lag-recovery-source-readiness-country.csv", country_rows)
    write_csv(OUT / "disaster-recovery-lag-recovery-source-readiness-events.csv", event_queue)

    print("Disaster recovery source-readiness audit")
    print(f"  GDIS CSV locations: {gdis_summary['gdis_locations_total_csv']:,}")
    print(
        "  ADB GDIS x Black Marble overlap: "
        f"{gdis_summary['adb_unique_ids_black_marble_window_2012_2018']:,} unique GDIS ids, "
        f"{gdis_summary['adb_locations_black_marble_window_2012_2018']:,} locations"
    )
    print(
        "  Current EM-DAT aggregate has event id/date/geometry: "
        f"{emdat['has_disaster_identifier']}/{emdat['has_month_day']}/{emdat['has_location_geometry']}"
    )
    print(f"  Wrote {OUT / 'disaster-recovery-lag-recovery-source-readiness.json'}")


if __name__ == "__main__":
    main()
