"""Flood market-access source-readiness audit.

The decomposition artifact shows that the existing flood-market-access proxy
is a national event-count and population screen. This script adds the source
wall for the object the program name would actually require:

  rural population-weighted travel time to markets, recomputed after observed
  flood footprints cut road-network edges.

It queries public metadata/index routes for OSM road extracts, WFP market-price
data, WorldPop population grids, and observed flood-footprint candidates. It
records raw-response hashes and combines the source wall with the committed
index decomposition.

It does not download full road extracts, build a road graph, geocode markets,
download population rasters, run Earth Engine, download flood rasters, cut
network edges, compute routes, or estimate access loss.
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

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "flood-access-source-readiness"
OUT = BASE / "generated"
DECOMPOSITION_PATH = OUT / "flood-decompose-deepening.json"

HDX_WFP_PACKAGE_API = "https://data.humdata.org/api/3/action/package_show?id=wfp-food-prices"
GEOFABRIK_ASIA = "https://download.geofabrik.de/asia.html"
GEOFABRIK_OCEANIA = "https://download.geofabrik.de/australia-oceania.html"
WORLDPOP_WPGP = "https://www.worldpop.org/rest/data/pop/wpgp"
GFD_CLOUD_TO_STREET = "https://global-flood-database.cloudtostreet.ai/"
GFD_EARTH_ENGINE_CATALOG = "https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1"
NASA_NRT_FLOOD_PRODUCTS = "https://www.earthdata.nasa.gov/data/instruments/viirs/near-real-time-data/nrt-global-flood-products"
CMR_COLLECTIONS = "https://cmr.earthdata.nasa.gov/search/collections.json"

RANGE_BYTES = 4095


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cache_name(prefix, url):
    parsed = urllib.parse.urlparse(url)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{parsed.netloc}_{parsed.path}_{parsed.query}")
    return f"{prefix}_{slug.strip('_')[:120]}"


def fetch_bytes(url, cache_path, accept="*/*", extra_headers=None):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    headers = {
        "Accept": accept,
        "User-Agent": "adb-research-factory/1.0",
    }
    if extra_headers:
        headers.update(extra_headers)
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
            status = getattr(response, "status", None)
            response_headers = dict(response.headers.items())
        cache_path.write_bytes(raw)
        mode = "live"
    except (urllib.error.URLError, TimeoutError) as exc:
        if not cache_path.exists():
            raise
        raw = cache_path.read_bytes()
        status = None
        response_headers = {}
        mode = f"cache fallback after {exc.__class__.__name__}"
    return raw, {
        "url": url,
        "cache_path": str(cache_path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status_code": status,
        "fetch_mode": mode,
        "response_headers": response_headers,
    }


def fetch_text(url, cache_path):
    raw, record = fetch_bytes(url, cache_path, accept="text/html, text/plain, */*")
    return raw.decode("utf-8-sig", errors="replace"), record


def fetch_json(url, cache_path):
    raw, record = fetch_bytes(url, cache_path, accept="application/json")
    return json.loads(raw.decode("utf-8-sig")), record


def fetch_range(url, cache_path, end_byte=RANGE_BYTES):
    raw, record = fetch_bytes(
        url,
        cache_path,
        accept="text/csv, text/plain, */*",
        extra_headers={"Range": f"bytes=0-{end_byte}"},
    )
    record["range_request"] = f"bytes=0-{end_byte}"
    return raw, record


def fetch_head(url):
    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={
                "Accept": "*/*",
                "User-Agent": "adb-research-factory/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            return {
                "url": url,
                "status_code": getattr(response, "status", None),
                "fetch_mode": "live",
                "response_headers": dict(response.headers.items()),
            }
    except (urllib.error.URLError, TimeoutError) as exc:
        return {
            "url": url,
            "status_code": None,
            "fetch_mode": f"failed after {exc.__class__.__name__}",
            "response_headers": {},
            "error": str(exc),
        }


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
    path = urllib.parse.urlparse(str(url or "")).path.lower()
    if "." not in path:
        return ""
    return path.rsplit(".", 1)[-1]


def parse_csv_header(raw):
    sample = raw.decode("utf-8-sig", errors="replace")
    first_line = sample.splitlines()[0] if sample.splitlines() else ""
    if not first_line:
        return []
    return next(csv.reader([first_line]))


def compact_url(url, limit=120):
    text = str(url or "")
    return text if len(text) <= limit else f"{text[:limit - 3]}..."


def source_row(layer_role, source_name, source_url, key_id, reachable, candidate_links, sample_data_links, status, notes):
    return {
        "layer_role": layer_role,
        "source_name": source_name,
        "source_url": source_url,
        "key_id": key_id,
        "public_metadata_reachable": bool(reachable),
        "candidate_links": int(candidate_links or 0),
        "sample_data_links": int(sample_data_links or 0),
        "status": status,
        "notes": notes,
    }


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_decomposition_artifact():
    if not DECOMPOSITION_PATH.exists():
        raise FileNotFoundError(f"{DECOMPOSITION_PATH} missing. Run scripts/deepen-decompose.py first.")
    return json.loads(DECOMPOSITION_PATH.read_text(encoding="utf-8"))


def audit_geofabrik(cache_records, link_rows):
    pages = [
        ("Asia", GEOFABRIK_ASIA, "geofabrik_asia.html"),
        ("Australia-Oceania", GEOFABRIK_OCEANIA, "geofabrik_oceania.html"),
    ]
    all_pbf = []
    latest_pbf = []
    page_records = []
    for region, url, filename in pages:
        page_html, record = fetch_text(url, CACHE / filename)
        cache_records.append({**record, "query_type": "geofabrik_extract_index", "region": region})
        page_records.append({**record, "region": region})
        links = extract_links(page_html, url)
        pbf_links = []
        for link in links:
            href = link["href"]
            if not href.endswith(".osm.pbf"):
                continue
            if href in pbf_links:
                continue
            pbf_links.append(href)
        all_pbf.extend(pbf_links)
        latest_pbf.extend([href for href in pbf_links if href.endswith("-latest.osm.pbf")])

    all_pbf = sorted(set(all_pbf))
    latest_pbf = sorted(set(latest_pbf))
    for href in latest_pbf[:40]:
        link_rows.append({
            "layer_role": "road_network",
            "source_name": "Geofabrik OpenStreetMap extract index",
            "href": href,
            "rel_or_label": "latest .osm.pbf extract",
            "file_type": file_type(href),
            "selected_for_analysis": False,
        })

    return source_row(
        "road_network",
        "Geofabrik OpenStreetMap extract indexes",
        f"{GEOFABRIK_ASIA}; {GEOFABRIK_OCEANIA}",
        "Asia and Australia-Oceania .osm.pbf extract indexes",
        any(record["fetch_mode"].startswith("live") or record["bytes"] > 0 for record in page_records),
        len(all_pbf),
        len(latest_pbf),
        "extract indexes reachable; no road graph or travel-time engine built",
        f"{len(all_pbf)} unique .osm.pbf links are visible, including {len(latest_pbf)} latest extract links; none are downloaded or routed.",
    ), {
        "total_pbf_links": len(all_pbf),
        "latest_pbf_links": len(latest_pbf),
        "sample_latest_links": latest_pbf[:20],
    }


def audit_wfp(cache_records, link_rows):
    payload, record = fetch_json(HDX_WFP_PACKAGE_API, CACHE / "hdx_wfp_food_prices_package.json")
    cache_records.append({**record, "query_type": "hdx_package_show", "package_id": "wfp-food-prices"})
    result = payload.get("result", {}) or {}
    resources = result.get("resources", []) or []
    csv_resources = [r for r in resources if str(r.get("format") or "").upper() == "CSV"]
    main_resource = csv_resources[0] if csv_resources else (resources[0] if resources else {})
    resource_url = main_resource.get("url") or main_resource.get("download_url") or main_resource.get("alt_url") or ""

    head_record = fetch_head(resource_url) if resource_url else {}
    if head_record:
        cache_records.append({**head_record, "query_type": "wfp_csv_head", "cache_path": ""})

    header_fields = []
    header_record = {}
    if resource_url:
        raw, header_record = fetch_range(resource_url, CACHE / "wfpvam_foodprices_header_sample.csv")
        cache_records.append({**header_record, "query_type": "wfp_csv_range_header_sample"})
        header_fields = parse_csv_header(raw)

    fields_lower = {field.strip().lower() for field in header_fields}
    coord_fields = {"lat", "latitude", "lon", "long", "longitude", "x", "y"}
    geocoded_fields_visible = bool(fields_lower & coord_fields)
    size_bytes = main_resource.get("size") or (head_record.get("response_headers") or {}).get("Content-Length")
    size_mb = round(int(size_bytes) / 1_000_000, 1) if str(size_bytes).isdigit() else None

    if resource_url:
        link_rows.append({
            "layer_role": "market_locations",
            "source_name": "HDX/WFP Global Food Prices Database",
            "href": resource_url,
            "rel_or_label": main_resource.get("name") or "CSV resource",
            "file_type": file_type(resource_url),
            "selected_for_analysis": False,
        })

    return source_row(
        "market_locations",
        "HDX/WFP Global Food Prices Database",
        HDX_WFP_PACKAGE_API,
        main_resource.get("id") or "wfp-food-prices",
        payload.get("success", False),
        len(resources),
        len(csv_resources),
        "market-price CSV resource visible; full file and geocoded market points not joined",
        (
            f"Package has {len(resources)} resource(s), {len(csv_resources)} CSV resource(s), "
            f"main CSV size {size_mb} MB, and header fields {', '.join(header_fields[:8])}. "
            f"Coordinate fields visible in the sampled header: {geocoded_fields_visible}."
        ),
    ), {
        "package_title": result.get("title"),
        "resource_id": main_resource.get("id"),
        "resource_name": main_resource.get("name"),
        "resource_url": resource_url,
        "resource_size_bytes": int(size_bytes) if str(size_bytes).isdigit() else None,
        "resource_size_mb": size_mb,
        "csv_resource_count": len(csv_resources),
        "header_fields": header_fields,
        "geocoded_fields_visible_in_sample_header": geocoded_fields_visible,
        "head_content_length": (head_record.get("response_headers") or {}).get("Content-Length"),
        "range_content_range": (header_record.get("response_headers") or {}).get("Content-Range"),
    }


def audit_worldpop(cache_records, link_rows, panel_iso):
    payload, record = fetch_json(WORLDPOP_WPGP, CACHE / "worldpop_wpgp.json")
    cache_records.append({**record, "query_type": "worldpop_population_dataset_list"})
    if isinstance(payload, dict):
        rows = payload.get("data") or []
    elif isinstance(payload, list):
        rows = payload
    else:
        rows = []

    panel_rows = [row for row in rows if str(row.get("iso3") or "") in panel_iso]
    panel_iso_with_rows = sorted({str(row.get("iso3")) for row in panel_rows if row.get("iso3")})
    years = []
    for row in rows:
        try:
            years.append(int(row.get("popyear")))
        except (TypeError, ValueError):
            continue
    latest_year = max(years) if years else None

    link_rows.append({
        "layer_role": "population_weight",
        "source_name": "WorldPop REST dataset list",
        "href": WORLDPOP_WPGP,
        "rel_or_label": "wpgp population dataset API",
        "file_type": "json",
        "selected_for_analysis": False,
    })

    return source_row(
        "population_weight",
        "WorldPop gridded population dataset catalog",
        WORLDPOP_WPGP,
        "wpgp",
        bool(rows),
        len(rows),
        len(panel_rows),
        "dataset catalog reachable; no population raster downloaded or zonal weight computed",
        (
            f"{len(rows)} WorldPop dataset rows are visible; {len(panel_rows)} rows cover "
            f"{len(panel_iso_with_rows)} economies in the flood panel; latest listed year is {latest_year}."
        ),
    ), {
        "dataset_rows": len(rows),
        "panel_rows": len(panel_rows),
        "panel_iso_with_rows": len(panel_iso_with_rows),
        "panel_iso_list_with_rows": panel_iso_with_rows,
        "latest_year": latest_year,
        "sample_panel_rows": panel_rows[:5],
    }


def cmr_keyword_url(keyword):
    return f"{CMR_COLLECTIONS}?{urllib.parse.urlencode({'keyword': keyword, 'page_size': '10'})}"


def audit_flood_footprints(cache_records, link_rows):
    cloud_page, cloud_record = fetch_text(GFD_CLOUD_TO_STREET, CACHE / "global_flood_database_cloudtostreet.html")
    cache_records.append({**cloud_record, "query_type": "global_flood_database_site"})

    ee_page, ee_record = fetch_text(GFD_EARTH_ENGINE_CATALOG, CACHE / "global_flood_database_earth_engine_catalog.html")
    cache_records.append({**ee_record, "query_type": "earth_engine_data_catalog", "dataset_id": "GLOBAL_FLOOD_DB/MODIS_EVENTS/V1"})

    nrt_page, nrt_record = fetch_text(NASA_NRT_FLOOD_PRODUCTS, CACHE / "nasa_nrt_global_flood_products.html")
    cache_records.append({**nrt_record, "query_type": "nasa_nrt_global_flood_products"})

    cmr_url = cmr_keyword_url("Dartmouth Flood Observatory")
    cmr_payload, cmr_record = fetch_json(cmr_url, CACHE / "cmr_dartmouth_flood_observatory_collections.json")
    cache_records.append({**cmr_record, "query_type": "cmr_keyword_search", "keyword": "Dartmouth Flood Observatory"})
    cmr_entries = cmr_payload.get("feed", {}).get("entry", []) or []

    has_dataset_id = "GLOBAL_FLOOD_DB/MODIS_EVENTS/V1" in ee_page
    event_count_match = re.search(r"([0-9][0-9,]*)\s+flood events", ee_page, re.I)
    event_count = int(event_count_match.group(1).replace(",", "")) if event_count_match else None
    has_2000_2018 = bool(re.search(r"2000\s*-\s*2018|2000-2018", ee_page))
    has_modis_viirs_nrt = "MODIS" in nrt_page and "VIIRS" in nrt_page and re.search(r"flood products", nrt_page, re.I)

    for href, label in [
        (GFD_CLOUD_TO_STREET, "Global Flood Database project page"),
        (GFD_EARTH_ENGINE_CATALOG, "Earth Engine catalog: GLOBAL_FLOOD_DB/MODIS_EVENTS/V1"),
        (NASA_NRT_FLOOD_PRODUCTS, "NASA NRT Global Flood Products"),
        (cmr_url, "NASA CMR keyword search: Dartmouth Flood Observatory"),
    ]:
        link_rows.append({
            "layer_role": "observed_flood_footprint",
            "source_name": "Observed flood-footprint candidate metadata",
            "href": href,
            "rel_or_label": label,
            "file_type": file_type(href) or "html/json",
            "selected_for_analysis": False,
        })

    return source_row(
        "observed_flood_footprint",
        "Global Flood Database and NASA NRT flood-product metadata",
        GFD_EARTH_ENGINE_CATALOG,
        "GLOBAL_FLOOD_DB/MODIS_EVENTS/V1",
        has_dataset_id or ("Global Flood Database" in cloud_page),
        4 + len(cmr_entries),
        0,
        "public catalog pages reachable; no event raster, SAR/MODIS mask, or network overlay downloaded",
        (
            f"Earth Engine catalog exposes dataset ID={has_dataset_id}, "
            f"event count parsed={event_count}, period flag 2000-2018={has_2000_2018}; "
            f"NASA NRT MODIS/VIIRS page visible={bool(has_modis_viirs_nrt)}; "
            f"CMR flood-discovery entries={len(cmr_entries)}."
        ),
    ), {
        "gfd_cloud_page_reachable": cloud_record["fetch_mode"].startswith("live") or cloud_record["bytes"] > 0,
        "earth_engine_catalog_reachable": ee_record["fetch_mode"].startswith("live") or ee_record["bytes"] > 0,
        "earth_engine_dataset_id_visible": has_dataset_id,
        "earth_engine_event_count_parsed": event_count,
        "earth_engine_period_2000_2018_visible": has_2000_2018,
        "nasa_nrt_page_reachable": nrt_record["fetch_mode"].startswith("live") or nrt_record["bytes"] > 0,
        "nasa_nrt_modis_viirs_flood_products_visible": bool(has_modis_viirs_nrt),
        "cmr_keyword_url": cmr_url,
        "cmr_keyword_entry_count": len(cmr_entries),
        "cmr_keyword_entries": [
            {
                "id": entry.get("id"),
                "short_name": entry.get("short_name"),
                "title": entry.get("title"),
                "data_center": entry.get("data_center"),
            }
            for entry in cmr_entries[:10]
        ],
    }


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    decomposition = load_decomposition_artifact()
    panel_iso = {str(row.get("iso3")) for row in decomposition.get("rows", []) if row.get("iso3")}

    cache_records = []
    source_rows = []
    link_rows = []

    geofabrik_row, geofabrik_detail = audit_geofabrik(cache_records, link_rows)
    source_rows.append(geofabrik_row)
    wfp_row, wfp_detail = audit_wfp(cache_records, link_rows)
    source_rows.append(wfp_row)
    worldpop_row, worldpop_detail = audit_worldpop(cache_records, link_rows, panel_iso)
    source_rows.append(worldpop_row)
    flood_row, flood_detail = audit_flood_footprints(cache_records, link_rows)
    source_rows.append(flood_row)
    source_rows.append(source_row(
        "analysis_ready_access_join",
        "Road x market x population x observed-flood network overlay",
        "",
        "not_computed",
        False,
        0,
        0,
        "not joined",
        "No OSM extract, WFP market table, WorldPop raster, or flood-footprint layer is joined into a routed access-loss estimate.",
    ))

    summary = {
        "access_source_layers_checked": 4,
        "road_extract_total_pbf_links_visible": geofabrik_detail["total_pbf_links"],
        "road_extract_latest_pbf_links_visible": geofabrik_detail["latest_pbf_links"],
        "market_package_resources": wfp_row["candidate_links"],
        "market_csv_resources": wfp_detail["csv_resource_count"],
        "market_csv_size_mb": wfp_detail["resource_size_mb"],
        "market_csv_header_fields": wfp_detail["header_fields"],
        "market_coordinate_fields_visible_in_sample_header": wfp_detail["geocoded_fields_visible_in_sample_header"],
        "worldpop_dataset_rows": worldpop_detail["dataset_rows"],
        "worldpop_panel_rows": worldpop_detail["panel_rows"],
        "worldpop_panel_iso_with_rows": worldpop_detail["panel_iso_with_rows"],
        "worldpop_latest_year": worldpop_detail["latest_year"],
        "gfd_earth_engine_dataset_id_visible": flood_detail["earth_engine_dataset_id_visible"],
        "gfd_earth_engine_event_count_parsed": flood_detail["earth_engine_event_count_parsed"],
        "gfd_earth_engine_period_2000_2018_visible": flood_detail["earth_engine_period_2000_2018_visible"],
        "nasa_nrt_modis_viirs_flood_products_visible": flood_detail["nasa_nrt_modis_viirs_flood_products_visible"],
        "cmr_flood_discovery_entries": flood_detail["cmr_keyword_entry_count"],
        "road_graph_built": False,
        "market_points_joined": False,
        "population_grid_downloaded": False,
        "observed_flood_footprint_downloaded": False,
        "flooded_edges_cut": False,
        "routed_travel_time_computed": False,
        "population_weighted_access_loss_estimated": False,
        "analysis_ready_network_join": False,
        "headline_top4": decomposition.get("a_headline", {}).get("top4_reproduced", []),
        "per_capita_top4": decomposition.get("b_strip_size_terms", {}).get("top4_per_capita_per_million", []),
        "dropped_per_capita": decomposition.get("b_strip_size_terms", {}).get("dropped_per_capita", []),
        "owner_gated_or_unfinished_steps": [
            "No Geofabrik/OSM extract is downloaded and no routable graph or bridge-edge table is built.",
            "The WFP CSV resource is visible, but only a header sample is inspected; market coordinates are not confirmed or geocoded.",
            "No WorldPop raster is downloaded and no settlement/population weight is computed.",
            "Observed flood-footprint catalogs are visible, but no MODIS/SAR/event raster is downloaded or exported.",
            "No road edges are cut by a flood footprint, no market routes are recomputed, and no access-loss estimate is produced.",
        ],
    }

    payload = {
        "program": "flood-market-access",
        "analysis": "flood market-access source-readiness audit",
        "claim_scope": (
            "Source-readiness wall for the road, market, population, and observed-flood layers "
            "needed after the index decomposition. Public metadata/index pages are visible for "
            "all four required layer families, but the analysis-ready routed access object remains "
            "uncomputed. This is not a flood-market-access, road-isolation, market-service, or "
            "access-loss estimate."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "hdx_wfp_package_api": HDX_WFP_PACKAGE_API,
            "geofabrik_asia": GEOFABRIK_ASIA,
            "geofabrik_australia_oceania": GEOFABRIK_OCEANIA,
            "worldpop_wpgp": WORLDPOP_WPGP,
            "global_flood_database_project": GFD_CLOUD_TO_STREET,
            "global_flood_database_earth_engine_catalog": GFD_EARTH_ENGINE_CATALOG,
            "nasa_nrt_global_flood_products": NASA_NRT_FLOOD_PRODUCTS,
            "nasa_cmr_collections": CMR_COLLECTIONS,
        },
        "summary": summary,
        "source_rows": source_rows,
        "geofabrik_detail": geofabrik_detail,
        "wfp_detail": wfp_detail,
        "worldpop_detail": worldpop_detail,
        "flood_footprint_detail": flood_detail,
        "sample_link_rows": link_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(decomposition)
    combined["analysis"] = "flood index decomposition plus access source-readiness wall"
    combined["access_source_readiness"] = payload
    combined["claim_scope"] = (
        f"{decomposition.get('claim_scope', '')} The source-readiness layer verifies public "
        "metadata/index routes for roads, markets, population, and observed flood footprints only; "
        "it does not compute a road-market-flood routing object."
    ).strip()
    combined["flood_data_wall"] = (
        "Public Geofabrik/OSM extract indexes, WFP market-price metadata, WorldPop population "
        "catalog rows, and Global Flood Database/NASA flood-product pages are reachable, but the "
        "repository still has no road graph, no geocoded market join, no downloaded population "
        "raster, no flood-footprint raster, no cut road edges, no routed travel time, and no "
        "population-weighted access-loss estimate."
    )
    combined["generated_at"] = retrieved_at

    standalone_path = OUT / "flood-access-source-readiness.json"
    combined_path = OUT / "flood-decomposition-access-source-audit.json"
    source_csv_path = OUT / "flood-access-source-readiness-sources.csv"
    links_csv_path = OUT / "flood-access-source-readiness-links.csv"

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

    print("=== Flood access source-readiness audit ===")
    print(f"Geofabrik .osm.pbf links visible: {summary['road_extract_total_pbf_links_visible']}")
    print(f"Latest .osm.pbf links visible: {summary['road_extract_latest_pbf_links_visible']}")
    print(f"WFP CSV resources: {summary['market_csv_resources']}")
    print(f"WFP CSV sampled coordinate fields visible: {summary['market_coordinate_fields_visible_in_sample_header']}")
    print(f"WorldPop panel rows: {summary['worldpop_panel_rows']}")
    print(f"GFD Earth Engine dataset ID visible: {summary['gfd_earth_engine_dataset_id_visible']}")
    print(f"Analysis-ready network join: {summary['analysis_ready_network_join']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {source_csv_path}")
    print(f"Wrote {links_csv_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
