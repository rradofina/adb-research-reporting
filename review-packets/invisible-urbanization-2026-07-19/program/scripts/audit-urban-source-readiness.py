"""Invisible urbanization source-readiness audit.

The committed report proves the +/-50% multiplier sweep is a tautology. This
script adds the next public source layer without pretending that the built-up
analysis has been done:

* WDI urban-share metadata, to show the old signal is national-definition based.
* GHSL built-up surface and SMOD public metadata pages, to show the source
  object that would replace the proxy.
* geoBoundaries ADM2 metadata for the current top-five economies, to show a
  boundary layer is visible but not yet intersected with GHSL.

The output is a source-readiness wall. It does not download GHSL rasters,
does not build a zonal statistic, and does not claim invisible urbanization on
the ground. Public data only. attestation_chain: ai-first.
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
CACHE = BASE / ".cache" / "urban-source-readiness"
OUT = BASE / "generated"
TAUTOLOGY_PATH = OUT / "invisible-urbanization-tautology.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
WDI_URBAN_SHARE = "SP.URB.TOTL.IN.ZS"
WDI_URBAN_GROWTH = "SP.URB.GROW"

GHSL_PAGES = [
    {
        "layer_role": "built_up_surface",
        "source_name": "GHSL GHS-BUILT-S R2023A product page",
        "url": "https://human-settlement.emergency.copernicus.eu/ghs_buS2023.php",
        "tokens": ["BUILT-S", "GHS-BUILT", "GHS_BUILT", "download"],
    },
    {
        "layer_role": "degree_of_urbanisation",
        "source_name": "GHSL GHS-SMOD R2023A product page",
        "url": "https://human-settlement.emergency.copernicus.eu/ghs_smod2023.php",
        "tokens": ["SMOD", "Degree of Urbanisation", "GHS_SMOD", "download"],
    },
    {
        "layer_role": "ghsl_download_catalog",
        "source_name": "GHSL download catalog",
        "url": "https://human-settlement.emergency.copernicus.eu/download.php",
        "tokens": ["GHS-BUILT-S", "GHS-SMOD", "R2023A", "download"],
    },
    {
        "layer_role": "gee_built_up_metadata",
        "source_name": "Earth Engine catalog metadata for GHSL built-up surface",
        "url": "https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_S",
        "tokens": ["JRC/GHSL/P2023A/GHS_BUILT_S", "GHS_BUILT", "built-up"],
    },
    {
        "layer_role": "gee_smod_metadata",
        "source_name": "Earth Engine catalog metadata for GHSL SMOD",
        "url": "https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_SMOD_V2-0",
        "tokens": ["JRC/GHSL/P2023A/GHS_SMOD", "GHS_SMOD", "Degree of Urbanisation"],
    },
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cache_name(url, suffix):
    stem = re.sub(r"[^A-Za-z0-9]+", "_", url).strip("_")[:120]
    return f"{stem}.{suffix}"


def fetch_bytes(url, suffix="html"):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / cache_name(url, suffix)
    if path.exists():
        data = path.read_bytes()
        return {
            "url": url,
            "cache_path": str(path.relative_to(BASE)),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "status_code": 200,
            "fetch_mode": "cache",
            "headers": {},
            "content": data,
        }
    req = urllib.request.Request(url, headers={"User-Agent": "adb-research-source-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
            headers = {k: v for k, v in resp.headers.items()}
            status = int(getattr(resp, "status", 200))
    except urllib.error.HTTPError as exc:
        data = exc.read()
        headers = {k: v for k, v in exc.headers.items()}
        status = int(exc.code)
    path.write_bytes(data)
    return {
        "url": url,
        "cache_path": str(path.relative_to(BASE)),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "status_code": status,
        "fetch_mode": "live",
        "headers": headers,
        "content": data,
    }


def fetch_json(url):
    record = fetch_bytes(url, "json")
    try:
        parsed = json.loads(record["content"].decode("utf-8"))
    except json.JSONDecodeError:
        parsed = None
    out = dict(record)
    out.pop("content", None)
    out["json_parse_ok"] = parsed is not None
    return parsed, out


def token_presence(text, tokens):
    lower = text.lower()
    return {token: (token.lower() in lower) for token in tokens}


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
    }


def ghsl_source_rows():
    rows = []
    records = []
    for page in GHSL_PAGES:
        record = fetch_bytes(page["url"], "html")
        text = record["content"].decode("utf-8", errors="replace")
        present = token_presence(text, page["tokens"])
        link_count = len(re.findall(r"https?://[^\"'<> ]+", text))
        download_mentions = len(re.findall(r"download", text, flags=re.I))
        rows.append({
            "layer_role": page["layer_role"],
            "source_name": page["source_name"],
            "source_url": page["url"],
            "public_metadata_reachable": record["status_code"] == 200,
            "bytes": record["bytes"],
            "sha256": record["sha256"],
            "tokens_found": "; ".join(k for k, v in present.items() if v),
            "tokens_missing": "; ".join(k for k, v in present.items() if not v),
            "link_count": link_count,
            "download_mentions": download_mentions,
            "status": "metadata visible" if record["status_code"] == 200 else "metadata request failed",
            "notes": "Metadata/source page checked only; no raster or Earth Engine export is downloaded.",
        })
        rec = dict(record)
        rec.pop("content", None)
        rec["query_type"] = "public_source_page"
        rec["layer_role"] = page["layer_role"]
        records.append(rec)
    return rows, records


def geoboundaries_rows(top5):
    rows = []
    records = []
    for iso3 in top5:
        url = f"https://www.geoboundaries.org/api/current/gbOpen/{iso3}/ADM2/"
        parsed, record = fetch_json(url)
        row = {
            "iso3": iso3,
            "layer_role": "admin_boundary_metadata",
            "source_name": "geoBoundaries gbOpen ADM2",
            "source_url": url,
            "public_metadata_reachable": record["status_code"] == 200 and isinstance(parsed, dict),
            "boundary_type": None,
            "boundary_year_represented": None,
            "download_url": None,
            "static_download_link": None,
            "license": None,
            "status": "metadata unavailable",
            "notes": "Metadata checked only; no boundary geometry is downloaded or intersected.",
        }
        if isinstance(parsed, dict):
            row.update({
                "boundary_type": parsed.get("boundaryType"),
                "boundary_year_represented": parsed.get("boundaryYearRepresented"),
                "download_url": parsed.get("gjDownloadURL"),
                "static_download_link": parsed.get("staticDownloadLink"),
                "license": parsed.get("license") or parsed.get("licenseDetail") or parsed.get("boundaryLicense"),
                "status": "ADM2 metadata visible",
            })
        rows.append(row)
        rec = dict(record)
        rec["query_type"] = "geoboundaries_adm2_metadata"
        rec["iso3"] = iso3
        records.append(rec)
    return rows, records


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with TAUTOLOGY_PATH.open(encoding="utf-8") as f:
        tautology = json.load(f)

    top5 = tautology["multiplier_sweep_is_rank_preserving"]["baseline_top5"]
    wdi_records = [wdi_metadata(WDI_URBAN_SHARE), wdi_metadata(WDI_URBAN_GROWTH)]
    ghsl_rows, ghsl_cache_records = ghsl_source_rows()
    boundary_rows, boundary_cache_records = geoboundaries_rows(top5)

    wdi_source_rows = [
        {
            "layer_role": (
                "old_proxy_urban_share"
                if row["indicator_id"] == WDI_URBAN_SHARE
                else "old_proxy_urban_growth"
            ),
            "source_name": (
                "World Bank WDI urban population share"
                if row["indicator_id"] == WDI_URBAN_SHARE
                else "World Bank WDI urban population growth"
            ),
            "source_url": row["metadata_url"],
            "key_id": row["indicator_id"],
            "public_metadata_reachable": row["metadata_status_code"] == 200,
            "joined_rows": tautology.get("n_dmcs"),
            "status": "metadata visible; national-definition based",
            "notes": row.get("source_note") or "",
        }
        for row in wdi_records
    ]

    source_rows = wdi_source_rows + [
        {
            "layer_role": row["layer_role"],
            "source_name": row["source_name"],
            "source_url": row["source_url"],
            "key_id": row["layer_role"],
            "public_metadata_reachable": row["public_metadata_reachable"],
            "joined_rows": 0,
            "status": row["status"],
            "notes": row["notes"],
        }
        for row in ghsl_rows
    ] + [
        {
            "layer_role": "analysis_ready_builtup_boundary_overlay",
            "source_name": "GHSL built-up or SMOD x administrative-boundary overlay",
            "source_url": "",
            "key_id": "not_computed",
            "public_metadata_reachable": False,
            "joined_rows": 0,
            "status": "not joined",
            "notes": "No GHSL raster, SMOD grid, boundary geometry, classification-history table, or zonal statistic is joined.",
        }
    ]

    boundary_years = [
        int(row["boundary_year_represented"])
        for row in boundary_rows
        if str(row.get("boundary_year_represented") or "").isdigit()
    ]
    summary = {
        "baseline_top5": top5,
        "wdi_metadata_records": len(wdi_records),
        "wdi_urban_definition_is_national": any(
            "national statistical offices" in (row.get("source_note") or "")
            for row in wdi_records
        ),
        "ghsl_public_metadata_pages_checked": len(ghsl_rows),
        "ghsl_public_metadata_pages_reachable": sum(1 for row in ghsl_rows if row["public_metadata_reachable"]),
        "ghsl_built_or_smod_token_rows": sum(
            1 for row in ghsl_rows if row["tokens_found"]
        ),
        "top5_geoboundaries_adm2_metadata_rows": len(boundary_rows),
        "top5_geoboundaries_adm2_reachable_rows": sum(1 for row in boundary_rows if row["public_metadata_reachable"]),
        "top5_boundary_year_min": min(boundary_years) if boundary_years else None,
        "top5_boundary_year_max": max(boundary_years) if boundary_years else None,
        "analysis_ready_builtup_boundary_overlay": False,
        "analysis_ready_classification_history": False,
        "analysis_ready_zonal_statistic": False,
        "owner_gated_or_unfinished_steps": [
            "No GHSL raster tile or Earth Engine export is downloaded.",
            "No GHS-SMOD grid is intersected with an administrative boundary.",
            "No national census or gazetted urban-boundary classification-history table is joined.",
            "No population-weighted built-up or SMOD zonal statistic is computed.",
            "The current WDI signal remains a triage proxy until the GHSL/boundary overlay is built.",
        ],
    }

    audit = {
        "program": "invisible-urbanization",
        "analysis": "tautology audit plus GHSL and boundary source-readiness wall",
        "claim_scope": (
            "Deepening of the committed invisible-urbanization proxy. It preserves "
            "the arithmetic tautology result, then records that public GHSL built-up "
            "surface, GHSL SMOD, WDI urban-definition metadata, and geoBoundaries "
            "ADM2 metadata are visible. It does not download rasters, intersect "
            "boundaries, build a classification-history ledger, or estimate hidden "
            "built-up population."
        ),
        "source": tautology.get("source"),
        "frozen_formula": tautology.get("frozen_formula"),
        "n_dmcs": tautology.get("n_dmcs"),
        "multiplier_sweep_is_rank_preserving": tautology.get("multiplier_sweep_is_rank_preserving"),
        "signal_is_two_wdi_series_multiplied": tautology.get("signal_is_two_wdi_series_multiplied"),
        "genuine_falsification_not_run": tautology.get("genuine_falsification_not_run"),
        "urban_source_readiness": {
            "program": "invisible-urbanization",
            "analysis": "GHSL built-up, SMOD, WDI urban-definition, and ADM2 boundary source-readiness audit",
            "claim_scope": (
                "Public source audit for replacing the WDI-only proxy. GHSL and "
                "boundary metadata are reachable, but the analysis-ready built-up "
                "boundary overlay remains false."
            ),
            "retrieved_at": now_iso(),
            "sources": {
                "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
                "wdi_indicators": [WDI_URBAN_SHARE, WDI_URBAN_GROWTH],
                "ghsl_pages": [row["url"] for row in GHSL_PAGES],
                "geoboundaries_api_pattern": "https://www.geoboundaries.org/api/current/gbOpen/{ISO3}/ADM2/",
            },
            "summary": summary,
            "wdi_indicator_records": wdi_records,
            "ghsl_source_rows": ghsl_rows,
            "geoboundaries_top5_rows": boundary_rows,
            "source_rows": source_rows,
            "cache_records": ghsl_cache_records + boundary_cache_records,
            "attestation_chain": "ai-first",
            "generated_at": now_iso(),
        },
        "invisible_urbanization_data_wall": (
            "GHSL built-up, GHSL SMOD, WDI urban-definition metadata, and "
            "geoBoundaries ADM2 metadata are now visible at source level. The "
            "analysis still has no raster download, boundary intersection, "
            "classification-history ledger, or population-weighted zonal statistic, "
            "so it is not an analysis-ready invisible-urbanization estimate."
        ),
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
    }

    (OUT / "invisible-urbanization-source-audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (OUT / "invisible-urbanization-source-readiness.json").write_text(
        json.dumps(audit["urban_source_readiness"], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    write_csv(
        OUT / "invisible-urbanization-source-readiness-sources.csv",
        source_rows,
        ["layer_role", "source_name", "source_url", "key_id", "public_metadata_reachable", "joined_rows", "status", "notes"],
    )
    write_csv(
        OUT / "invisible-urbanization-boundary-readiness.csv",
        boundary_rows,
        [
            "iso3",
            "layer_role",
            "source_name",
            "source_url",
            "public_metadata_reachable",
            "boundary_type",
            "boundary_year_represented",
            "download_url",
            "static_download_link",
            "license",
            "status",
            "notes",
        ],
    )

    print("=== Invisible urbanization source-readiness audit ===")
    print(f"Baseline top 5: {top5}")
    print(f"GHSL metadata pages reachable: {summary['ghsl_public_metadata_pages_reachable']}/{summary['ghsl_public_metadata_pages_checked']}")
    print(f"geoBoundaries ADM2 metadata reachable for top 5: {summary['top5_geoboundaries_adm2_reachable_rows']}/{summary['top5_geoboundaries_adm2_metadata_rows']}")
    print(f"WDI urban definition is national-office based: {summary['wdi_urban_definition_is_national']}")
    print(f"Analysis-ready built-up/boundary overlay: {summary['analysis_ready_builtup_boundary_overlay']}")
    print(f"Wrote {OUT / 'invisible-urbanization-source-audit.json'}")
    print(f"Wrote {OUT / 'invisible-urbanization-source-readiness-sources.csv'}")
    print(f"Wrote {OUT / 'invisible-urbanization-boundary-readiness.csv'}")


if __name__ == "__main__":
    main()
