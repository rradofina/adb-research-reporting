"""Black Marble source-readiness audit for the MPI x nighttime-lights report.

The MPI decomposition report is owner-gated for the actual nighttime-lights
join. This script does the AI-doable part only: it queries public NASA CMR
metadata for selected Black Marble nighttime-lights products, records raw
response hashes, and combines that source wall with the committed OPHI MPI
dimension decomposition.

It does not download radiance rasters, authenticate to Earthdata or Earth
Engine, compute zonal statistics, or estimate a poverty model.
attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/mpi-nighttime-lights")
CACHE = BASE / ".cache" / "ntl-source-readiness"
OUT = BASE / "generated"
DECOMP_PATH = OUT / "mpi-dimension-decomposition.json"

CMR_COLLECTIONS = "https://cmr.earthdata.nasa.gov/search/collections.json"
CMR_GRANULES = "https://cmr.earthdata.nasa.gov/search/granules.json"
SHORT_NAMES = ["VNP46A3", "VNP46A4"]


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def collection_url(short_name):
    params = {"short_name": short_name, "page_size": "10"}
    return f"{CMR_COLLECTIONS}?{urllib.parse.urlencode(params)}"


def granule_url(concept_id):
    params = {
        "collection_concept_id": concept_id,
        "page_size": "1",
        "sort_key[]": "-start_date",
    }
    return f"{CMR_GRANULES}?{urllib.parse.urlencode(params)}"


def link_counts(links):
    counts = {
        "data_links": 0,
        "https_data_links": 0,
        "s3_links": 0,
        "service_links": 0,
        "documentation_links": 0,
    }
    for link in links or []:
        rel = str(link.get("rel") or "")
        href = str(link.get("href") or "")
        if rel.endswith("/data#") or "data#" in rel:
            counts["data_links"] += 1
            if href.startswith("https://"):
                counts["https_data_links"] += 1
        if rel.endswith("/s3#") or "s3#" in rel or href.startswith("s3://"):
            counts["s3_links"] += 1
        if rel.endswith("/service#") or "service#" in rel:
            counts["service_links"] += 1
        if rel.endswith("/documentation#") or "documentation#" in rel:
            counts["documentation_links"] += 1
    return counts


def compact_links(links):
    rows = []
    for link in links or []:
        rows.append({
            "rel": link.get("rel"),
            "type": link.get("type"),
            "title": link.get("title"),
            "href": link.get("href"),
            "inherited": bool(link.get("inherited")),
        })
    return rows


def latest_version_rows(rows):
    latest = {}
    for row in rows:
        short = row["short_name"]
        version = int(row["version_id"]) if str(row.get("version_id", "")).isdigit() else -1
        if short not in latest or version > latest[short]["_version_number"]:
            latest[short] = {**row, "_version_number": version}
    return [{key: value for key, value in row.items() if key != "_version_number"} for row in latest.values()]


def load_decomposition():
    if not DECOMP_PATH.exists():
        raise FileNotFoundError(f"{DECOMP_PATH} missing. Run scripts/deepen-mpi-decomposition.py first.")
    return json.loads(DECOMP_PATH.read_text(encoding="utf-8"))


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    decomp = load_decomposition()

    collection_rows = []
    granule_rows = []
    granule_link_rows = []
    cache_records = []

    for short_name in SHORT_NAMES:
        url = collection_url(short_name)
        payload, record = fetch_json(url, CACHE / f"collections_{short_name}.json")
        cache_records.append({**record, "query_type": "collections", "short_name": short_name})
        entries = payload.get("feed", {}).get("entry", []) or []
        for entry in entries:
            links = compact_links(entry.get("links") or [])
            counts = link_counts(links)
            collection_rows.append({
                "short_name": entry.get("short_name") or short_name,
                "version_id": entry.get("version_id"),
                "concept_id": entry.get("id"),
                "title": entry.get("title"),
                "time_start": entry.get("time_start"),
                "time_end": entry.get("time_end"),
                "updated": entry.get("updated"),
                "data_links": counts["data_links"],
                "https_data_links": counts["https_data_links"],
                "s3_links": counts["s3_links"],
                "service_links": counts["service_links"],
                "documentation_links": counts["documentation_links"],
            })

    current_collections = latest_version_rows(collection_rows)

    for collection in current_collections:
        concept_id = collection["concept_id"]
        if not concept_id:
            continue
        url = granule_url(concept_id)
        payload, record = fetch_json(url, CACHE / f"granules_{concept_id}.json")
        cache_records.append({
            **record,
            "query_type": "sample_granule",
            "short_name": collection["short_name"],
            "concept_id": concept_id,
        })
        entries = payload.get("feed", {}).get("entry", []) or []
        if not entries:
            granule_rows.append({
                "short_name": collection["short_name"],
                "concept_id": concept_id,
                "granule_id": None,
                "title": None,
                "time_start": None,
                "time_end": None,
                "updated": None,
                "data_links": 0,
                "https_data_links": 0,
                "s3_links": 0,
                "service_links": 0,
                "documentation_links": 0,
            })
            continue
        entry = entries[0]
        links = compact_links(entry.get("links") or [])
        counts = link_counts(links)
        granule_row = {
            "short_name": collection["short_name"],
            "concept_id": concept_id,
            "granule_id": entry.get("id"),
            "title": entry.get("title"),
            "time_start": entry.get("time_start"),
            "time_end": entry.get("time_end"),
            "updated": entry.get("updated"),
            "data_links": counts["data_links"],
            "https_data_links": counts["https_data_links"],
            "s3_links": counts["s3_links"],
            "service_links": counts["service_links"],
            "documentation_links": counts["documentation_links"],
        }
        granule_rows.append(granule_row)
        for link in links:
            granule_link_rows.append({
                "short_name": collection["short_name"],
                "concept_id": concept_id,
                "granule_id": entry.get("id"),
                **link,
            })

    current_ids = {row["short_name"]: row["concept_id"] for row in current_collections}
    current_versions = {row["short_name"]: row["version_id"] for row in current_collections}
    latest_granule_starts = {row["short_name"]: row["time_start"] for row in granule_rows}
    latest_granule_updates = {row["short_name"]: row["updated"] for row in granule_rows}
    earliest_start = min((row["time_start"] for row in current_collections if row.get("time_start")), default=None)

    summary = {
        "short_names_queried": SHORT_NAMES,
        "collections_found": len(collection_rows),
        "current_collection_candidates": len(current_collections),
        "current_collection_ids": current_ids,
        "current_versions": current_versions,
        "earliest_current_collection_start": earliest_start,
        "sample_granules_checked": len(granule_rows),
        "sample_granules_with_https_data_links": sum(1 for row in granule_rows if row["https_data_links"] > 0),
        "sample_granules_with_s3_links": sum(1 for row in granule_rows if row["s3_links"] > 0),
        "latest_sample_granule_start": latest_granule_starts,
        "latest_sample_granule_updated": latest_granule_updates,
        "mpi_economies_scoped": decomp.get("n_adb_economies"),
        "mean_ntl_blind_dim_pct": decomp.get("mean_ntl_blind_dim_pct"),
        "mean_ntl_blind_ind_pct": decomp.get("mean_ntl_blind_ind_pct"),
        "analysis_ready_raster_join": False,
        "owner_gated_or_unfinished_steps": [
            "Earthdata/LAADS or Earth Engine authenticated raster access was not attempted.",
            "No VIIRS/Black Marble raster was downloaded or archived by this script.",
            "No geoBoundaries ADM1/ADM2, WorldPop, or GHSL zonal statistic was computed here.",
            "No subnational MPI to nighttime-lights join or poverty model is estimated.",
            "Coauthor/owner decision remains required before this owner-led Program 0 track advances.",
        ],
    }

    payload = {
        "program": "mpi-nighttime-lights",
        "analysis": "Black Marble nighttime-lights source-readiness audit for MPI blind-spot decomposition",
        "claim_scope": (
            "Source-readiness and methods-wall audit. NASA CMR metadata confirms "
            "public Black Marble collection and sample granule records for the "
            "nighttime-lights side, while the actual raster download, zonal "
            "statistics, and MPI join remain uncomputed and owner-gated."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "nasa_cmr_collections": CMR_COLLECTIONS,
            "nasa_cmr_granules": CMR_GRANULES,
            "queried_short_names": SHORT_NAMES,
            "black_marble_project_page": "https://www.earthdata.nasa.gov/data/projects/black-marble",
        },
        "summary": summary,
        "collection_rows": collection_rows,
        "current_collection_rows": current_collections,
        "sample_granule_rows": granule_rows,
        "sample_granule_link_rows": granule_link_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(decomp)
    combined["analysis"] = "MPI dimension decomposition plus Black Marble source-readiness audit"
    combined["ntl_source_readiness"] = payload
    combined["claim_scope"] = (
        f"{decomp.get('analysis', '')} The source-readiness layer confirms CMR "
        "metadata and sample links only; it does not compute an NTL x MPI join."
    ).strip()
    combined["ntl_data_wall"] = (
        "Public NASA CMR metadata and sample Black Marble data links are visible, "
        "but this repository still has no authenticated raster pull, no population-"
        "weighted zonal statistics, no subnational MPI crosswalk, and no coauthor "
        "attestation for the owner-led NTL x MPI track."
    )
    combined["generated_at"] = retrieved_at

    standalone_path = OUT / "mpi-nightlight-source-readiness.json"
    combined_path = OUT / "mpi-nightlight-blindspot-source-audit.json"
    collections_csv_path = OUT / "mpi-nightlight-source-readiness-collections.csv"
    granule_links_csv_path = OUT / "mpi-nightlight-source-readiness-granule-links.csv"

    standalone_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    collection_fields = [
        "short_name", "version_id", "concept_id", "title", "time_start",
        "time_end", "updated", "data_links", "https_data_links", "s3_links",
        "service_links", "documentation_links",
    ]
    with collections_csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=collection_fields)
        writer.writeheader()
        writer.writerows(collection_rows)

    link_fields = [
        "short_name", "concept_id", "granule_id", "rel", "type", "title",
        "href", "inherited",
    ]
    with granule_links_csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=link_fields)
        writer.writeheader()
        writer.writerows(granule_link_rows)

    print("=== MPI x NTL source-readiness audit ===")
    print(f"Collections found: {summary['collections_found']}")
    print(f"Current collection candidates: {summary['current_collection_candidates']}")
    print(f"Current collection IDs: {summary['current_collection_ids']}")
    print(f"Sample granules checked: {summary['sample_granules_checked']}")
    print(f"Sample granules with HTTPS data links: {summary['sample_granules_with_https_data_links']}")
    print(f"Analysis-ready raster join: {summary['analysis_ready_raster_join']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {collections_csv_path}")
    print(f"Wrote {granule_links_csv_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
