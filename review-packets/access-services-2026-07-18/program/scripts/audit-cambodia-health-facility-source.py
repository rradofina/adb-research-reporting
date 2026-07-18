"""Cambodia public health-facility source audit for the access map.

This extends the OSM-completeness deepening without changing its claim scope.
The access panel's Cambodia row is based on OSM health amenities by ADM1. This
script retrieves the public HDX Cambodia Health Facilities package, parses the
government health center, health post, and referral hospital point layers, and
compares those source counts with the already committed OSM panel.

Important scope note:
  - The HDX file is a 2010 MoH/OCHA public-facility inventory, not a complete
    2026 all-provider clinical registry.
  - Operational District points are parsed as source context but are not counted
    as facilities.
  - The ODC page documents a separate national-hospital layer; this script uses
    the HDX package because it is the reproducible API route reachable from the
    pipeline.

Every empirical number comes from public source data fetched by this script or
from the committed legacy access ADM1 panel.
attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
import urllib.request
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import geopandas as gpd


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = PROGRAM / ".cache" / "khm-health-facility"
OUT = PROGRAM / "generated"
LEGACY_ADM1 = (
    ROOT
    / "luminosity-gap"
    / "research"
    / "access-services"
    / "generated"
    / "access-services-computed-admin1.csv"
)

HDX_PACKAGE_API = "https://data.humdata.org/api/3/action/package_show?id=cambodia-health"
HDX_DATASET_URL = "https://data.humdata.org/dataset/cambodia-health"
ODC_DATASET_URL = "https://data.opendevelopmentcambodia.net/en/dataset/health-facility-of-cambodia-2010"
USER_AGENT = "DevelopmentBlindspotsLab/0.1 research pipeline"

LAYER_FILES = {
    "health_center": "khm_hltfacp_healthcenter_gov.shp",
    "health_post": "khm_hltfacp_healthpost_gov.shp",
    "operational_district": "khm_hltfacp_od_gov.shp",
    "referral_hospital": "khm_hltfacp_referral_gov.shp",
}

NAME_CROSSWALK = {
    "Banteay Mean Chey": "Banteay Meanchey",
    "Banteay Meanchey": "Banteay Meanchey",
    "Bantey Meanchey": "Banteay Meanchey",
    "Battam Bang": "Battambang",
    "Battambang": "Battambang",
    "Kampong Spueu": "Kampong Speu",
    "Kampong Speu": "Kampong Speu",
    "Kaoh Kong": "Koh Kong",
    "Koh Kong": "Koh Kong",
    "Mondul Kiri": "Mondulkiri",
    "Mondulkiri": "Mondulkiri",
    "Oddar Mean chey": "Oddar Meanchey",
    "Oddar Meanchey": "Oddar Meanchey",
    "Oddor Meanchey": "Oddar Meanchey",
    "Preah Sihanouk": "Preah Sihanouk",
    "Ratanak Kiri": "Ratanakiri Province",
    "Ratanakiri Province": "Ratanakiri Province",
    "Sihaknouk Vill": "Preah Sihanouk",
    "Sihanoukville": "Preah Sihanouk",
    "Siem Reap": "Siem Reap",
    "Siemreap": "Siem Reap",
    "Stung  Treng": "Stung Treng",
    "Stung Treng": "Stung Treng",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_name(value: str | None) -> str:
    cleaned = " ".join((value or "").strip().split())
    return NAME_CROSSWALK.get(cleaned, cleaned)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_bytes(url: str, path: Path, refresh_env: str) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    from_cache = path.exists() and os.environ.get(refresh_env) != "1"
    if not from_cache:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=120) as response:
            path.write_bytes(response.read())
    return {
        "url": url,
        "cache_path": str(path.relative_to(ROOT)),
        "retrieved_at": now_utc(),
        "from_cache": from_cache,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def load_hdx_package() -> tuple[dict[str, Any], dict[str, Any]]:
    package_path = CACHE / "hdx-cambodia-health-package.json"
    record = fetch_bytes(HDX_PACKAGE_API, package_path, "ACCESS_KHM_REFRESH")
    with package_path.open(encoding="utf-8") as f:
        payload = json.load(f)
    if not payload.get("success"):
        raise RuntimeError("HDX package API returned success=false")
    return payload["result"], record


def download_hdx_zip(package: dict[str, Any]) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    resources = package.get("resources") or []
    if not resources:
        raise RuntimeError("HDX package has no resources")
    resource = resources[0]
    url = resource["url"]
    zip_path = CACHE / "health_facility.zip"
    record = fetch_bytes(url, zip_path, "ACCESS_KHM_REFRESH")
    record.update(
        {
            "name": resource.get("name"),
            "format": resource.get("format"),
            "resource_id": resource.get("id"),
            "created": resource.get("created"),
            "last_modified": resource.get("last_modified"),
        }
    )
    return zip_path, resource, record


def read_source_layers(zip_path: Path) -> tuple[dict[str, dict[str, int]], list[dict[str, Any]], dict[str, int]]:
    tmp = Path(tempfile.mkdtemp(prefix="khm-health-facility-"))
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp)
        health_dir = tmp / "Health"
        counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        raw_name_rows: list[dict[str, Any]] = []
        layer_totals: dict[str, int] = {}

        for layer, filename in LAYER_FILES.items():
            shp = health_dir / filename
            gdf = gpd.read_file(shp)
            layer_totals[layer] = int(len(gdf))
            for _, row in gdf.iterrows():
                raw_name = str(row.get("PNAME") or "").strip()
                normalized = normalize_name(raw_name)
                counts[normalized][layer] += 1
                raw_name_rows.append(
                    {
                        "layer": layer,
                        "raw_province_name": raw_name,
                        "normalized_province_name": normalized,
                    }
                )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return counts, raw_name_rows, layer_totals


def load_access_khm_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with LEGACY_ADM1.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["iso3"] != "KHM":
                continue
            rows.append(
                {
                    "iso3": row["iso3"],
                    "admin1_code": row["admin1_code"],
                    "admin1_name": row["admin1_name"],
                    "normalized_admin1_name": normalize_name(row["admin1_name"]),
                    "population_year": int(row["population_year"]),
                    "population": int(float(row["population"])),
                    "population_source": row["population_source"],
                    "osm_health_facilities": int(float(row["health_facilities"])),
                    "osm_schools": int(float(row["schools"])),
                    "osm_markets": int(float(row["markets"])),
                    "osm_people_per_health_facility": int(float(row["people_per_health_facility"])),
                    "access_stress_index": float(row["access_stress_index"]),
                    "osm_timestamp": row["osm_timestamp"],
                }
            )
    return rows


def build_join_rows(
    access_rows: list[dict[str, Any]], source_counts: dict[str, dict[str, int]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in access_rows:
        counts = source_counts.get(row["normalized_admin1_name"], {})
        health_centers = int(counts.get("health_center", 0))
        health_posts = int(counts.get("health_post", 0))
        referral_hospitals = int(counts.get("referral_hospital", 0))
        operational_districts = int(counts.get("operational_district", 0))
        government_facilities = health_centers + health_posts + referral_hospitals
        population = row["population"]
        osm = row["osm_health_facilities"]
        if government_facilities:
            gov_ppf = round(population / government_facilities)
            capture = round(osm / government_facilities, 4)
            load_ratio = round(row["osm_people_per_health_facility"] / gov_ppf, 2)
            status = "joined_public_facility_inventory"
        else:
            gov_ppf = None
            capture = None
            load_ratio = None
            status = "no_2010_source_province_match"

        note = ""
        if row["admin1_name"] == "Tbong Khmum":
            note = "Not present as a distinct PNAME in the 2010 source; needs boundary-year crosswalk."
        elif government_facilities and osm > government_facilities:
            note = "OSM count exceeds the 2010 public-facility inventory; interpret as scope/vintage mismatch."

        rows.append(
            {
                **row,
                "source_join_status": status,
                "government_health_centers_2010": health_centers,
                "government_health_posts_2010": health_posts,
                "government_referral_hospitals_2010": referral_hospitals,
                "operational_district_points_2010_context": operational_districts,
                "government_facilities_2010_included": government_facilities,
                "government_people_per_facility_2010": gov_ppf,
                "osm_to_government_facility_ratio": capture,
                "osm_load_to_government_load_ratio": load_ratio,
                "join_note": note,
            }
        )

    joined = [row for row in rows if row["government_people_per_facility_2010"] is not None]
    osm_rank = {
        row["admin1_code"]: rank
        for rank, row in enumerate(
            sorted(joined, key=lambda item: item["osm_people_per_health_facility"], reverse=True),
            start=1,
        )
    }
    gov_rank = {
        row["admin1_code"]: rank
        for rank, row in enumerate(
            sorted(joined, key=lambda item: item["government_people_per_facility_2010"], reverse=True),
            start=1,
        )
    }
    for row in rows:
        row["rank_osm_health_load_joined_only"] = osm_rank.get(row["admin1_code"])
        row["rank_government_health_load_2010_joined_only"] = gov_rank.get(row["admin1_code"])
        if row["admin1_code"] in osm_rank and row["admin1_code"] in gov_rank:
            row["rank_shift_after_2010_inventory"] = (
                osm_rank[row["admin1_code"]] - gov_rank[row["admin1_code"]]
            )
        else:
            row["rank_shift_after_2010_inventory"] = None
    return rows


def summarize(
    access_rows: list[dict[str, Any]],
    join_rows: list[dict[str, Any]],
    source_counts: dict[str, dict[str, int]],
    layer_totals: dict[str, int],
) -> dict[str, Any]:
    joined = [row for row in join_rows if row["government_facilities_2010_included"]]
    osm_total = sum(row["osm_health_facilities"] for row in access_rows)
    government_total = sum(
        counts.get("health_center", 0)
        + counts.get("health_post", 0)
        + counts.get("referral_hospital", 0)
        for counts in source_counts.values()
    )
    oddar = next(row for row in join_rows if row["admin1_name"] == "Oddar Meanchey")
    phnom_penh = next(row for row in join_rows if row["admin1_name"] == "Phnom Penh")
    unmatched = [row["admin1_name"] for row in join_rows if not row["government_facilities_2010_included"]]
    rank_changed = [
        row
        for row in joined
        if row["rank_shift_after_2010_inventory"] not in (None, 0)
    ]
    largest_load_ratios = sorted(
        [row for row in joined if row["osm_load_to_government_load_ratio"] is not None],
        key=lambda item: item["osm_load_to_government_load_ratio"],
        reverse=True,
    )[:8]

    return {
        "access_khm_rows": len(access_rows),
        "joined_rows": len(joined),
        "unmatched_rows": len(unmatched),
        "unmatched_admin1_names": unmatched,
        "source_normalized_provinces": len(source_counts),
        "source_layer_totals": layer_totals,
        "government_facilities_2010_included_total": government_total,
        "operational_district_points_2010_context_total": layer_totals.get("operational_district", 0),
        "osm_health_facilities_access_panel_total": osm_total,
        "national_osm_to_government_facility_ratio": round(osm_total / government_total, 4)
        if government_total
        else None,
        "rank_changed_after_2010_inventory": len(rank_changed),
        "rank_joined_total": len(joined),
        "oddar_meanchey": {
            "osm_health_facilities": oddar["osm_health_facilities"],
            "government_facilities_2010_included": oddar["government_facilities_2010_included"],
            "osm_people_per_health_facility": oddar["osm_people_per_health_facility"],
            "government_people_per_facility_2010": oddar["government_people_per_facility_2010"],
            "osm_load_to_government_load_ratio": oddar["osm_load_to_government_load_ratio"],
            "rank_osm": oddar["rank_osm_health_load_joined_only"],
            "rank_government": oddar["rank_government_health_load_2010_joined_only"],
        },
        "phnom_penh_scope_warning": {
            "osm_health_facilities": phnom_penh["osm_health_facilities"],
            "government_facilities_2010_included": phnom_penh["government_facilities_2010_included"],
            "osm_to_government_facility_ratio": phnom_penh["osm_to_government_facility_ratio"],
            "note": phnom_penh["join_note"],
        },
        "largest_osm_load_ratios": [
            {
                "admin1_name": row["admin1_name"],
                "osm_health_facilities": row["osm_health_facilities"],
                "government_facilities_2010_included": row["government_facilities_2010_included"],
                "osm_people_per_health_facility": row["osm_people_per_health_facility"],
                "government_people_per_facility_2010": row["government_people_per_facility_2010"],
                "osm_load_to_government_load_ratio": row["osm_load_to_government_load_ratio"],
            }
            for row in largest_load_ratios
        ],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    package, package_record = load_hdx_package()
    zip_path, resource, zip_record = download_hdx_zip(package)
    source_counts, raw_name_rows, layer_totals = read_source_layers(zip_path)
    access_rows = load_access_khm_rows()
    join_rows = build_join_rows(access_rows, source_counts)
    summary = summarize(access_rows, join_rows, source_counts, layer_totals)

    raw_name_summary: dict[str, dict[str, Any]] = {}
    for raw in raw_name_rows:
        key = f"{raw['layer']}|{raw['raw_province_name']}"
        current = raw_name_summary.setdefault(
            key,
            {
                "layer": raw["layer"],
                "raw_province_name": raw["raw_province_name"],
                "normalized_province_name": raw["normalized_province_name"],
                "rows": 0,
            },
        )
        current["rows"] += 1

    payload = {
        "program": "access-services",
        "analysis": "Cambodia public health-facility source audit for OSM access-map completeness",
        "claim_scope": (
            "Source-discovery and partial source-join audit. Compares Cambodia "
            "OSM health amenities from the committed access ADM1 panel with the "
            "public 2010 HDX/MoH/OCHA government health center, health post, "
            "and referral hospital point layers. Not a travel-time access "
            "measure, not service capacity, and not a complete 2026 all-provider "
            "clinical registry."
        ),
        "sources": {
            "hdx_package_api": HDX_PACKAGE_API,
            "hdx_dataset_page": HDX_DATASET_URL,
            "hdx_resource": {
                "name": resource.get("name"),
                "id": resource.get("id"),
                "format": resource.get("format"),
                "url": resource.get("url"),
                "created": resource.get("created"),
                "last_modified": resource.get("last_modified"),
            },
            "odc_dataset_page": ODC_DATASET_URL,
            "odc_context": (
                "ODC describes the Cambodia health-facility dataset as originally "
                "established by the Ministry of Health and contributed by OCHA to "
                "HDX, with separate ODC national-hospital resources. The numeric "
                "join in this artifact uses the HDX package ZIP only."
            ),
            "access_adm1_panel": str(LEGACY_ADM1.relative_to(ROOT)),
            "license_note": "HDX/ODC source page reports Creative Commons Attribution / CC BY context; see source pages.",
        },
        "retrieval": {
            "package_api": package_record,
            "health_facility_zip": zip_record,
        },
        "method": {
            "facility_layers_counted": ["health_center", "health_post", "referral_hospital"],
            "context_layers_not_counted_as_facilities": ["operational_district"],
            "name_normalization": NAME_CROSSWALK,
            "caveats": [
                "The HDX source vintage is 2010 while the access-panel OSM timestamp is 2026.",
                "The HDX package is a government/public-facility inventory, not a complete all-provider registry.",
                "Operational District points are administrative context and are not counted as facilities.",
                "One access-panel province has no distinct PNAME match in the 2010 source and needs a boundary-year crosswalk.",
                "Where OSM exceeds the public-facility source count, interpret the result as scope/vintage mismatch, not over-mapping proof.",
            ],
        },
        "summary": summary,
        "rows": join_rows,
        "raw_source_name_summary": sorted(raw_name_summary.values(), key=lambda x: (x["layer"], x["raw_province_name"])),
        "attestation_chain": "ai-first",
        "generated_at": now_utc(),
    }

    with (OUT / "access-cambodia-health-facility-source-audit.json").open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")

    write_csv(OUT / "access-cambodia-health-facility-source-audit.csv", join_rows)
    write_csv(
        OUT / "access-cambodia-health-facility-source-names.csv",
        sorted(raw_name_summary.values(), key=lambda x: (x["layer"], x["raw_province_name"])),
    )

    print("Cambodia health-facility source audit")
    print(f"  HDX zip sha256: {zip_record['sha256']}")
    print(
        "  Oddar Meanchey: "
        f"{summary['oddar_meanchey']['osm_health_facilities']} OSM points vs "
        f"{summary['oddar_meanchey']['government_facilities_2010_included']} public-source facilities; "
        f"{summary['oddar_meanchey']['osm_load_to_government_load_ratio']}x load difference"
    )
    print(
        "  Joined rows: "
        f"{summary['joined_rows']}/{summary['access_khm_rows']} "
        f"({summary['rank_changed_after_2010_inventory']} rank changes among joined rows)"
    )
    print(f"  Wrote {OUT / 'access-cambodia-health-facility-source-audit.json'}")
    print(f"  Wrote {OUT / 'access-cambodia-health-facility-source-audit.csv'}")


if __name__ == "__main__":
    main()
