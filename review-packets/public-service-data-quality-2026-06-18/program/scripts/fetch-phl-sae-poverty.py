"""Fetch Philippines poverty overlay source files for PSDQ.

The preferred source is PSA's 2023 city/municipality SAE Excel attachment.
PSA's main site can return a Cloudflare 403 to scripted clients, so this
fetcher records that status instead of fabricating a table. It also fetches
the accessible PSA OpenSTAT direct-estimate table for provinces and highly
urbanized/direct-estimate cities, which is used as an official supplemental
source in the downstream ADM3 join.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"

PSA_SAE_PAGE_URL = "https://psa.gov.ph/statistics/poverty-sae/stat-tables"
PSA_SAE_RELEASE_URL = "https://psa.gov.ph/statistics/poverty?page=7&pagina=2"
PSA_SAE_PRESS_PDF_URL = "https://psa.gov.ph/sites/default/files/phdsd/PressReleaseon-2023SAE_rev.pdf"
PSA_SAE_PRIMARY_URL = (
    "https://psa.gov.ph/sites/default/files/phdsd/"
    "2_2023%20SAE_with%20PSGC_noHUC_06Feb2026.xlsx"
)
PSA_SAE_FALLBACK_URL = (
    "https://psa.gov.ph/system/files/phdsd/"
    "2_2023%20SAE_with%20PSGC_noHUC_06Feb2026.xlsx"
)
PSA_SAE_ATTACHMENT_URLS = [
    PSA_SAE_PRIMARY_URL,
    PSA_SAE_FALLBACK_URL,
    PSA_SAE_PRIMARY_URL.replace("https://psa.gov.ph/", "https://www.psa.gov.ph/"),
    PSA_SAE_FALLBACK_URL.replace("https://psa.gov.ph/", "https://www.psa.gov.ph/"),
]
PSA_SAE_XLSX = CACHE / "psa-phl-2023-sae-with-psgc-nohuc.xlsx"

OPENSTAT_API_URL = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1E/FY/0041E3DF02A.px"
OPENSTAT_META = CACHE / "psa-openstat-fy-poverty-direct-meta.json"
OPENSTAT_CSV = CACHE / "psa-openstat-fy-poverty-direct-2023.csv"

STATUS_JSON = CACHE / "psa-phl-poverty-source-status.json"
OPENSTAT_ALT_SEARCH = CACHE / "openstat-sae-alternative-search.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": PSA_SAE_PAGE_URL,
}


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-sae", action="store_true", help="Exit non-zero if the SAE Excel is not cached.")
    parser.add_argument("--skip-sae-download", action="store_true", help="Do not attempt PSA main-site Excel download.")
    parser.add_argument(
        "--sae-xlsx",
        type=Path,
        help=(
            "Seed the cache from a manually downloaded official PSA SAE Excel workbook. "
            "Use this when the PSA static-file host shows a Cloudflare browser challenge."
        ),
    )
    return parser.parse_args()


def is_xlsx_payload(path: Path) -> bool:
    try:
        return path.exists() and path.stat().st_size > 0 and zipfile.is_zipfile(path)
    except OSError:
        return False


def response_blocker(response: requests.Response) -> dict[str, Any]:
    headers = {key.lower(): value for key, value in response.headers.items()}
    body_prefix = response.text[:240] if "text" in headers.get("content-type", "").lower() else ""
    cf_mitigated = headers.get("cf-mitigated")
    csp = headers.get("content-security-policy", "")
    looks_like_cf = (
        cf_mitigated == "challenge"
        or "cloudflare" in headers.get("server", "").lower()
        or "challenge-platform" in csp.lower()
        or "Just a moment" in body_prefix
    )
    return {
        "server": response.headers.get("server"),
        "cf_ray": response.headers.get("cf-ray"),
        "cf_mitigated": cf_mitigated,
        "cloudflare_challenge_detected": bool(looks_like_cf),
        "body_starts_with": body_prefix.strip()[:120] if body_prefix else None,
    }


def cache_manual_sae_excel(path: Path) -> dict[str, Any]:
    source = path.expanduser().resolve()
    item: dict[str, Any] = {
        "source_url": str(source),
        "cached_path": str(PSA_SAE_XLSX),
        "status": "manual_seed_attempt",
    }
    if not source.exists():
        item["status"] = "manual_seed_missing"
        return item
    if not is_xlsx_payload(source):
        item["status"] = "manual_seed_rejected"
        item["note"] = "The supplied path is not a readable XLSX/ZIP payload."
        item["bytes"] = source.stat().st_size
        return item
    CACHE.mkdir(parents=True, exist_ok=True)
    if source != PSA_SAE_XLSX.resolve():
        shutil.copyfile(source, PSA_SAE_XLSX)
    item["status"] = "manual_seed_cached"
    item["bytes"] = PSA_SAE_XLSX.stat().st_size
    return item


def download_sae_excel(skip_download: bool, manual_xlsx: Path | None) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    if manual_xlsx is not None:
        manual_attempt = cache_manual_sae_excel(manual_xlsx)
        attempts.append(manual_attempt)
        if manual_attempt.get("status") == "manual_seed_cached":
            return attempts

    if PSA_SAE_XLSX.exists() and is_xlsx_payload(PSA_SAE_XLSX):
        return [
            {
                "source_url": str(PSA_SAE_XLSX),
                "status": "already_cached",
                "bytes": PSA_SAE_XLSX.stat().st_size,
                "cached_path": str(PSA_SAE_XLSX),
            }
        ]
    if PSA_SAE_XLSX.exists():
        attempts.append(
            {
                "source_url": str(PSA_SAE_XLSX),
                "status": "cached_but_invalid_xlsx",
                "bytes": PSA_SAE_XLSX.stat().st_size,
                "cached_path": str(PSA_SAE_XLSX),
            }
        )
    if skip_download:
        return attempts + [
            {
                "source_url": PSA_SAE_PRIMARY_URL,
                "status": "skipped",
                "cached_path": str(PSA_SAE_XLSX),
            }
        ]

    for url in PSA_SAE_ATTACHMENT_URLS:
        item: dict[str, Any] = {"source_url": url, "cached_path": str(PSA_SAE_XLSX)}
        try:
            response = requests.get(url, headers=HEADERS, timeout=90)
            item.update(
                {
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type"),
                    "bytes": len(response.content),
                }
            )
            item.update(response_blocker(response))
            if response.ok and response.content.startswith(b"PK"):
                PSA_SAE_XLSX.write_bytes(response.content)
                item["status"] = "cached"
                item["bytes"] = PSA_SAE_XLSX.stat().st_size
                attempts.append(item)
                break
            item["status"] = "blocked_cloudflare_challenge" if item.get("cloudflare_challenge_detected") else "not_cached"
            item["note"] = (
                "PSA static-file host returned a browser/security challenge instead of the XLSX payload."
                if item["status"] == "blocked_cloudflare_challenge"
                else "PSA main-site response was not an XLSX payload."
            )
        except requests.RequestException as exc:
            item["status"] = "error"
            item["error"] = str(exc)
        attempts.append(item)
    return attempts


def openstat_year_value(meta: dict[str, Any], year: str) -> str:
    for variable in meta["variables"]:
        if variable["code"] == "Year":
            for value, text in zip(variable["values"], variable["valueTexts"], strict=True):
                if str(text) == year:
                    return str(value)
    raise ValueError(f"OpenSTAT year {year} not found")


def fetch_openstat_direct() -> dict[str, Any]:
    meta_response = requests.get(OPENSTAT_API_URL, headers=HEADERS, timeout=90)
    meta_response.raise_for_status()
    meta = meta_response.json()
    OPENSTAT_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    year_value = openstat_year_value(meta, "2023")
    query = {
        "query": [
            {
                "code": variable["code"],
                "selection": {
                    "filter": "item",
                    "values": variable["values"] if variable["code"] != "Year" else [year_value],
                },
            }
            for variable in meta["variables"]
        ],
        "response": {"format": "CSV"},
    }
    data_response = requests.post(OPENSTAT_API_URL, headers=HEADERS, json=query, timeout=120)
    data_response.raise_for_status()
    OPENSTAT_CSV.write_text(data_response.text, encoding="utf-8")

    with io.StringIO(data_response.text) as handle:
        rows = list(csv.DictReader(handle))
    return {
        "api_url": OPENSTAT_API_URL,
        "title": meta.get("title"),
        "cached_meta": str(OPENSTAT_META),
        "cached_csv": str(OPENSTAT_CSV),
        "rows": len(rows),
        "bytes": OPENSTAT_CSV.stat().st_size,
    }


def search_openstat_sae_alternatives() -> dict[str, Any]:
    """Record whether OpenSTAT exposes a city/municipal SAE table.

    This does not crawl the entire OpenSTAT catalog. It checks the official
    poverty-relevant API branches that plausibly contain a poverty SAE table.
    """

    base = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB"
    paths = ["1E/FY", "3D", "3E/CH", "3I/G01"]
    pattern = re.compile(r"(small area|\bsae\b|city.*municip|municip.*city)", re.IGNORECASE)
    matches: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for path in paths:
        url = f"{base}/{path}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=60)
            if not response.ok:
                errors.append({"path": path, "status_code": response.status_code})
                continue
            for row in response.json():
                text = str(row.get("text", ""))
                if pattern.search(text):
                    matches.append(
                        {
                            "path": f"{path}/{row.get('id', '')}",
                            "type": row.get("type"),
                            "text": text,
                            "updated": row.get("updated"),
                        }
                    )
        except (requests.RequestException, ValueError) as exc:
            errors.append({"path": path, "error": str(exc)})

    result = {
        "searched_at": now_utc(),
        "searched_paths": paths,
        "matches": matches,
        "errors": errors,
        "note": "No OpenSTAT city/municipality SAE endpoint was found in the poverty-relevant branches if matches is empty.",
    }
    OPENSTAT_ALT_SEARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    args = parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)

    sae_attempts = download_sae_excel(args.skip_sae_download, args.sae_xlsx)
    openstat: dict[str, Any]
    try:
        openstat = fetch_openstat_direct()
    except requests.RequestException as exc:
        openstat = {"api_url": OPENSTAT_API_URL, "status": "error", "error": str(exc)}

    openstat_sae_alternatives = search_openstat_sae_alternatives()

    status = {
        "generated_at": now_utc(),
        "program": "public-service-data-quality",
        "country": "Philippines",
        "preferred_source": {
            "name": "PSA 2023 City- and Municipal-level Small Area Poverty Estimates",
            "source_page_url": PSA_SAE_PAGE_URL,
            "release_url": PSA_SAE_RELEASE_URL,
            "press_release_pdf_url": PSA_SAE_PRESS_PDF_URL,
            "attachment_label": "2_2023 SAE_with PSGC_noHUC_06Feb2026.xlsx",
            "attachment_size_listed": "361.31 KB",
            "attachment_urls": PSA_SAE_ATTACHMENT_URLS,
            "manual_cache_path": str(PSA_SAE_XLSX),
            "cached": is_xlsx_payload(PSA_SAE_XLSX),
            "manual_resolution": (
                "Download the listed Excel attachment from the PSA page in a normal browser, "
                "then run `python public-service-data-quality/scripts/fetch-phl-sae-poverty.py "
                "--sae-xlsx <downloaded-xlsx>` to seed the deterministic cache."
            ),
        },
        "preferred_source_attempts": sae_attempts,
        "preferred_source_blocker": (
            "cloudflare_challenge"
            if any(item.get("cloudflare_challenge_detected") for item in sae_attempts)
            and not is_xlsx_payload(PSA_SAE_XLSX)
            else None
        ),
        "direct_estimate_source": {
            "name": "PSA OpenSTAT Table 2a direct poverty estimates",
            **openstat,
        },
        "openstat_sae_alternative_search": openstat_sae_alternatives,
        "license_note": "PSA government-site content is public domain unless otherwise stated; verify attachment-level terms before redistribution.",
        "non_claim": "OpenSTAT direct estimates are not a substitute for the city/municipality SAE table outside HUC/direct-estimate units.",
    }
    STATUS_JSON.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(status, ensure_ascii=False, indent=2))

    if args.require_sae and not is_xlsx_payload(PSA_SAE_XLSX):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
