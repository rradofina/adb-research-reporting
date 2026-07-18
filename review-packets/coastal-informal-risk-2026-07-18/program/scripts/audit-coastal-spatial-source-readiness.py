"""Coastal informal-risk spatial source-readiness audit.

The denominator deepening shows that the national coastal-informal proxy is
partly a country-size screen. This script adds the next public-source wall:
are the settlement, elevation, and coastal-inundation source layers visible
enough to plan a true spatial overlay?

It queries public metadata/index pages for GHSL settlement/built-up evidence,
NASA CMR metadata for NASADEM elevation tiles, and the WRI Aqueduct Floods
coastal hazard-map index. It records raw-response hashes and combines the
source wall with the committed no-population rerank artifact.

It does not download rasters, choose a return period, compute a low-elevation
band, intersect informal-settlement footprints with surge zones, or estimate
exposed population.
attestation_chain: ai-first.
"""

import csv
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/coastal-informal-risk")
CACHE = BASE / ".cache" / "coastal-spatial-source-readiness"
OUT = BASE / "generated"
DENOM_PATH = OUT / "coastal-drop-population-deepening.json"

GHSL_DOWNLOAD_URL = "https://human-settlement.emergency.copernicus.eu/download.php"
GHSL_CATALOG_URL = "https://data.jrc.ec.europa.eu/collection/ghsl"
WRI_AQUEDUCT_INDEX_URL = "https://wri-projects.s3.amazonaws.com/AqueductFloodTool/download/v2/index.html"
CMR_COLLECTIONS = "https://cmr.earthdata.nasa.gov/search/collections.json"
CMR_GRANULES = "https://cmr.earthdata.nasa.gov/search/granules.json"
NASADEM_SHORT_NAME = "NASADEM_HGT"


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cache_name(prefix, url):
    parsed = urllib.parse.urlparse(url)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{parsed.netloc}_{parsed.path}_{parsed.query}")
    return f"{prefix}_{slug.strip('_')[:120]}"


def fetch_bytes(url, cache_path, accept="*/*"):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": accept,
                "User-Agent": "adb-research-factory/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
            status = getattr(response, "status", None)
        cache_path.write_bytes(raw)
        mode = "live"
    except (urllib.error.URLError, TimeoutError) as exc:
        if not cache_path.exists():
            raise
        raw = cache_path.read_bytes()
        status = None
        mode = f"cache fallback after {exc.__class__.__name__}"
    return raw, {
        "url": url,
        "cache_path": str(cache_path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status_code": status,
        "fetch_mode": mode,
    }


def fetch_text(url, cache_path):
    raw, record = fetch_bytes(url, cache_path, accept="text/html, text/plain, */*")
    return raw.decode("utf-8-sig", errors="replace"), record


def fetch_json(url, cache_path):
    raw, record = fetch_bytes(url, cache_path, accept="application/json")
    return json.loads(raw.decode("utf-8-sig")), record


def extract_links(page_html, base_url):
    links = []
    pattern = re.compile(r"<a\s+[^>]*href=['\"]([^'\"]+)['\"][^>]*>(.*?)</a>", re.I | re.S)
    for match in pattern.finditer(page_html):
        href = html.unescape(match.group(1).strip())
        label = re.sub(r"<[^>]+>", " ", match.group(2))
        label = html.unescape(re.sub(r"\s+", " ", label)).strip()
        links.append({
            "href": urllib.parse.urljoin(base_url, href),
            "label": label,
        })
    return links


def file_type(url):
    path = urllib.parse.urlparse(url).path.lower()
    if "." not in path:
        return ""
    return path.rsplit(".", 1)[-1]


def link_counts(links):
    counts = {
        "data_links": 0,
        "https_data_links": 0,
        "s3_links": 0,
        "protected_https_data_links": 0,
        "documentation_links": 0,
    }
    for link in links or []:
        rel = str(link.get("rel") or "")
        href = str(link.get("href") or "")
        if "data#" in rel:
            counts["data_links"] += 1
            if href.startswith("https://"):
                counts["https_data_links"] += 1
            if "lp-prod-protected" in href:
                counts["protected_https_data_links"] += 1
        if "s3#" in rel or href.startswith("s3://"):
            counts["s3_links"] += 1
        if "documentation#" in rel or "metadata#" in rel:
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
        })
    return rows


def collection_url(short_name):
    params = {"short_name": short_name, "page_size": "5"}
    return f"{CMR_COLLECTIONS}?{urllib.parse.urlencode(params)}"


def granule_url(concept_id):
    params = {
        "collection_concept_id": concept_id,
        "page_size": "1",
        "sort_key[]": "-start_date",
    }
    return f"{CMR_GRANULES}?{urllib.parse.urlencode(params)}"


def load_denominator_artifact():
    if not DENOM_PATH.exists():
        raise FileNotFoundError(f"{DENOM_PATH} missing. Run scripts/deepen-drop-population.py first.")
    return json.loads(DENOM_PATH.read_text(encoding="utf-8"))


def audit_ghsl(cache_records, link_rows):
    page_html, record = fetch_text(GHSL_DOWNLOAD_URL, CACHE / "ghsl_download_page.html")
    cache_records.append({**record, "query_type": "ghsl_download_page"})
    catalog_html, catalog_record = fetch_text(GHSL_CATALOG_URL, CACHE / "ghsl_catalog_page.html")
    cache_records.append({**catalog_record, "query_type": "ghsl_catalog_page"})

    links = extract_links(page_html, GHSL_DOWNLOAD_URL)
    built_links = [
        link for link in links
        if "GHS_BUILT_S" in link["href"] or "GHS_BUILT_S" in link["label"] or "GHS-BUILT-S" in link["label"]
    ]
    data_package_links = [
        link for link in links
        if "Data Package 2023" in link["label"] or "GHSL_Data_Package_2023" in link["href"]
    ]

    for link in built_links + data_package_links[:1]:
        link_rows.append({
            "layer_role": "settlement_footprint",
            "source_name": "GHSL/JRC download page",
            "href": link["href"],
            "rel_or_label": link["label"],
            "file_type": file_type(link["href"]),
            "selected_for_analysis": False,
        })

    return {
        "layer_role": "settlement_footprint",
        "source_name": "GHSL/JRC Global Human Settlement Layer",
        "source_url": GHSL_DOWNLOAD_URL,
        "key_id": "GHS_BUILT_S metadata candidates",
        "public_metadata_reachable": record["fetch_mode"].startswith("live") or record["bytes"] > 0,
        "candidate_links": len(built_links),
        "sample_data_links": 0,
        "status": "metadata page reachable; settlement/built-up links visible; no raster tile pulled",
        "notes": (
            f"Download page has {len(built_links)} GHS_BUILT_S link candidates; "
            f"catalog page has GHSL text={('Global Human Settlement' in catalog_html)}. "
            "No GHSL raster is downloaded or mosaicked here."
        ),
    }


def audit_wri(cache_records, link_rows):
    page_html, record = fetch_text(WRI_AQUEDUCT_INDEX_URL, CACHE / "wri_aqueduct_floods_v2_index.html")
    cache_records.append({**record, "query_type": "wri_aqueduct_floods_v2_index"})
    links = extract_links(page_html, WRI_AQUEDUCT_INDEX_URL)
    coastal_links = []
    seen = set()
    for link in links:
        if "inuncoast" not in link["href"] and "inuncoast" not in link["label"]:
            continue
        if link["href"] in seen:
            continue
        seen.add(link["href"])
        coastal_links.append(link)

    tif_links = [link for link in coastal_links if file_type(link["href"]) == "tif"]
    pickle_links = [link for link in coastal_links if file_type(link["href"]) == "pickle"]
    return_periods = sorted({
        match.group(1)
        for link in coastal_links
        for match in [re.search(r"_rp([0-9]{4}_[0-9])", link["href"])]
        if match
    })

    for link in coastal_links[:25]:
        link_rows.append({
            "layer_role": "coastal_hazard",
            "source_name": "WRI Aqueduct Floods Hazard Maps v2",
            "href": link["href"],
            "rel_or_label": link["label"],
            "file_type": file_type(link["href"]),
            "selected_for_analysis": False,
        })

    return {
        "layer_role": "coastal_hazard",
        "source_name": "WRI Aqueduct Floods Hazard Maps v2",
        "source_url": WRI_AQUEDUCT_INDEX_URL,
        "key_id": "inuncoast coastal inundation depth files",
        "public_metadata_reachable": record["fetch_mode"].startswith("live") or record["bytes"] > 0,
        "candidate_links": len(coastal_links),
        "sample_data_links": len(tif_links),
        "status": "coastal hazard-map index reachable; no return period selected or raster downloaded",
        "notes": (
            f"{len(coastal_links)} unique inuncoast links, including {len(tif_links)} GeoTIFF links "
            f"and {len(pickle_links)} pickle links; return-period tokens visible: {len(return_periods)}."
        ),
    }, {
        "coastal_links": len(coastal_links),
        "coastal_tif_links": len(tif_links),
        "coastal_pickle_links": len(pickle_links),
        "return_period_tokens": return_periods,
    }


def audit_nasadem(cache_records, link_rows):
    url = collection_url(NASADEM_SHORT_NAME)
    payload, record = fetch_json(url, CACHE / "nasadem_hgt_collections.json")
    cache_records.append({**record, "query_type": "cmr_collections", "short_name": NASADEM_SHORT_NAME})
    entries = payload.get("feed", {}).get("entry", []) or []
    collection_rows = []
    for entry in entries:
        collection_rows.append({
            "short_name": entry.get("short_name") or NASADEM_SHORT_NAME,
            "version_id": entry.get("version_id"),
            "concept_id": entry.get("id"),
            "title": entry.get("title"),
            "time_start": entry.get("time_start"),
            "time_end": entry.get("time_end"),
            "updated": entry.get("updated"),
            "cloud_hosted": bool(entry.get("cloud_hosted")),
            "online_access_flag": bool(entry.get("online_access_flag")),
            "data_center": entry.get("data_center"),
            "processing_level_id": entry.get("processing_level_id"),
            "boxes": "; ".join(entry.get("boxes") or []),
        })
    current = next((row for row in collection_rows if row["short_name"] == NASADEM_SHORT_NAME), collection_rows[0] if collection_rows else {})

    granule_rows = []
    granule_link_counts = {
        "data_links": 0,
        "https_data_links": 0,
        "s3_links": 0,
        "protected_https_data_links": 0,
        "documentation_links": 0,
    }
    concept_id = current.get("concept_id")
    if concept_id:
        g_url = granule_url(concept_id)
        g_payload, g_record = fetch_json(g_url, CACHE / f"nasadem_hgt_granules_{concept_id}.json")
        cache_records.append({**g_record, "query_type": "cmr_sample_granule", "concept_id": concept_id})
        granules = g_payload.get("feed", {}).get("entry", []) or []
        if granules:
            granule = granules[0]
            links = compact_links(granule.get("links") or [])
            granule_link_counts = link_counts(links)
            granule_rows.append({
                "granule_id": granule.get("id"),
                "title": granule.get("title"),
                "time_start": granule.get("time_start"),
                "updated": granule.get("updated"),
                **granule_link_counts,
            })
            for link in links:
                link_rows.append({
                    "layer_role": "elevation_dem",
                    "source_name": "NASA CMR NASADEM_HGT sample granule",
                    "href": link.get("href"),
                    "rel_or_label": link.get("rel") or link.get("title"),
                    "file_type": file_type(link.get("href") or ""),
                    "selected_for_analysis": False,
                })

    return {
        "layer_role": "elevation_dem",
        "source_name": "NASA CMR NASADEM_HGT",
        "source_url": url,
        "key_id": current.get("concept_id"),
        "public_metadata_reachable": bool(collection_rows),
        "candidate_links": len(collection_rows),
        "sample_data_links": granule_link_counts["https_data_links"],
        "status": "CMR collection and sample-granule metadata reachable; raster access not attempted",
        "notes": (
            f"Concept {current.get('concept_id')} has cloud_hosted={current.get('cloud_hosted')} "
            f"and sample HTTPS data links={granule_link_counts['https_data_links']}; "
            f"protected HTTPS data links={granule_link_counts['protected_https_data_links']}."
        ),
    }, {
        "collection_rows": collection_rows,
        "sample_granule_rows": granule_rows,
        "concept_id": current.get("concept_id"),
        "title": current.get("title"),
        "time_start": current.get("time_start"),
        "updated": current.get("updated"),
        **granule_link_counts,
    }


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    denominator = load_denominator_artifact()
    cache_records = []
    source_rows = []
    link_rows = []

    source_rows.append(audit_ghsl(cache_records, link_rows))
    nasadem_row, nasadem_detail = audit_nasadem(cache_records, link_rows)
    source_rows.append(nasadem_row)
    wri_row, wri_detail = audit_wri(cache_records, link_rows)
    source_rows.append(wri_row)
    source_rows.append({
        "layer_role": "analysis_ready_overlay",
        "source_name": "Settlement x elevation x coastal-hazard overlay",
        "source_url": "",
        "key_id": "not_computed",
        "public_metadata_reachable": False,
        "candidate_links": 0,
        "sample_data_links": 0,
        "status": "not joined",
        "notes": "No GHSL, NASADEM, WRI coastal hazard, population, or informality-mask raster overlay is computed here.",
    })

    summary = {
        "spatial_source_layers_checked": 3,
        "ghsl_built_settlement_link_candidates": source_rows[0]["candidate_links"],
        "nasadem_concept_id": nasadem_detail.get("concept_id"),
        "nasadem_sample_https_data_links": nasadem_detail.get("https_data_links", 0),
        "nasadem_sample_s3_links": nasadem_detail.get("s3_links", 0),
        "nasadem_sample_protected_https_data_links": nasadem_detail.get("protected_https_data_links", 0),
        "wri_coastal_links": wri_detail["coastal_links"],
        "wri_coastal_tif_links": wri_detail["coastal_tif_links"],
        "wri_coastal_return_period_tokens": wri_detail["return_period_tokens"],
        "analysis_ready_overlay": False,
        "raster_layers_downloaded": 0,
        "settlement_elevation_surge_joined": False,
        "no_population_top5": denominator.get("nopop_top5", []),
        "entered_top5_when_pop_removed": denominator.get("entered_top5_when_pop_removed", []),
        "dropped_from_top5_when_pop_removed": denominator.get("dropped_from_top5_when_pop_removed", []),
        "owner_gated_or_unfinished_steps": [
            "No GHSL or other settlement raster tile is downloaded, mosaicked, or classified.",
            "No NASADEM tile is downloaded and no low-elevation band is derived.",
            "No WRI Aqueduct coastal GeoTIFF is downloaded, clipped, or assigned a return period.",
            "No CRS harmonization, resampling, population weighting, informality mask, or zonal statistic is computed.",
            "No settlement-level, coastline-level, or exposed-population result is produced.",
        ],
    }

    payload = {
        "program": "coastal-informal-risk",
        "analysis": "coastal informal-risk spatial source-readiness audit",
        "claim_scope": (
            "Source-readiness wall for the spatial layers needed after the no-population "
            "denominator audit. Public metadata/index pages are visible for settlement, "
            "elevation, and coastal-hazard inputs, but the analysis-ready overlay remains "
            "uncomputed. This is not a storm-surge exposure or informal-settlement footprint result."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "ghsl_download_page": GHSL_DOWNLOAD_URL,
            "ghsl_catalog_page": GHSL_CATALOG_URL,
            "nasadem_cmr_collections": CMR_COLLECTIONS,
            "nasadem_cmr_granules": CMR_GRANULES,
            "wri_aqueduct_floods_v2_index": WRI_AQUEDUCT_INDEX_URL,
        },
        "summary": summary,
        "source_rows": source_rows,
        "nasadem_detail": nasadem_detail,
        "sample_link_rows": link_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(denominator)
    combined["analysis"] = "coastal denominator rerank plus spatial source-readiness wall"
    combined["coastal_source_readiness"] = payload
    combined["claim_scope"] = (
        f"{denominator.get('claim_scope', '')} The source-readiness layer verifies public "
        "settlement, elevation, and coastal-hazard metadata only; it does not compute the "
        "settlement-footprint-in-surge-zone exposure object."
    ).strip()
    combined["coastal_data_wall"] = (
        "Public GHSL/JRC, NASADEM CMR, and WRI Aqueduct coastal-hazard source pages are reachable, "
        "but this repository still has no downloaded rasters, no selected return period, no "
        "low-elevation mask, no settlement-footprint overlay, and no exposed-population estimate."
    )
    combined["generated_at"] = retrieved_at

    standalone_path = OUT / "coastal-spatial-source-readiness.json"
    combined_path = OUT / "coastal-denominator-spatial-source-audit.json"
    source_csv_path = OUT / "coastal-spatial-source-readiness-sources.csv"
    links_csv_path = OUT / "coastal-spatial-source-readiness-links.csv"

    standalone_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    write_csv(source_csv_path, source_rows, [
        "layer_role",
        "source_name",
        "source_url",
        "key_id",
        "public_metadata_reachable",
        "candidate_links",
        "sample_data_links",
        "status",
        "notes",
    ])
    write_csv(links_csv_path, link_rows, [
        "layer_role",
        "source_name",
        "href",
        "rel_or_label",
        "file_type",
        "selected_for_analysis",
    ])

    print("=== Coastal spatial source-readiness audit ===")
    print(f"GHSL GHS_BUILT_S link candidates: {summary['ghsl_built_settlement_link_candidates']}")
    print(f"NASADEM concept: {summary['nasadem_concept_id']}")
    print(f"NASADEM sample HTTPS data links: {summary['nasadem_sample_https_data_links']}")
    print(f"WRI coastal links: {summary['wri_coastal_links']}")
    print(f"WRI coastal GeoTIFF links: {summary['wri_coastal_tif_links']}")
    print(f"Analysis-ready overlay: {summary['analysis_ready_overlay']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {source_csv_path}")
    print(f"Wrote {links_csv_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
