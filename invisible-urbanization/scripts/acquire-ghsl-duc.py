"""Acquire and inventory the official GHSL Degree of Urbanisation package.

This is the first data object for reshaping the invisible-urbanization program.
It downloads the GHS-DUC R2023A V2.0 archive to the repository-level cache,
records its checksum and HTTP metadata, inventories every member, and writes a
small schema sample for each distinct tabular layout. Raw source files remain
uncommitted; the inventory and provenance record are committed.

The package classifies GADM 4.1 administrative units using the GHSL Degree of
Urbanisation method. It is not a ledger of national legal urban designations,
so this script makes no claim that any settlement is officially misclassified.

Public data only. attestation_chain: ai-first.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = ROOT / ".cache" / "invisible-urbanization-ghsl-duc-r2023a-v2"
OUT = PROGRAM / "generated"

PACKAGE_URL = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_DUC_GLOBE_R2023A/V2-0/GHS_DUC_MT_GLOBE_R2023A_V2_0.zip"
)
PACKAGE_PATH = CACHE / "GHS_DUC_MT_GLOBE_R2023A_V2_0.zip"
USER_AGENT = "adb-research-factory/1.0 (public-data acquisition)"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def acquire() -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    if PACKAGE_PATH.exists():
        return {
            "fetch_mode": "cache",
            "status_code": 200,
            "headers": {},
        }

    partial = PACKAGE_PATH.with_suffix(".zip.part")
    existing = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": USER_AGENT}
    if existing:
        headers["Range"] = f"bytes={existing}-"
    request = urllib.request.Request(PACKAGE_URL, headers=headers)
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=120) as response:
        status = int(getattr(response, "status", 200))
        if existing and status != 206:
            existing = 0
        mode = "ab" if existing and status == 206 else "wb"
        response_bytes = int(response.headers.get("Content-Length", "0"))
        total = existing + response_bytes
        copied = existing
        with partial.open(mode) as target:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                target.write(block)
                copied += len(block)
                if copied and copied % (50 * 1024 * 1024) < len(block):
                    print(
                        f"Downloaded {copied / 1024**2:.0f} MiB"
                        + (f" of {total / 1024**2:.0f} MiB" if total else ""),
                        flush=True,
                    )
        response_headers = {key: value for key, value in response.headers.items()}
    partial.replace(PACKAGE_PATH)
    print(f"Download finished in {time.perf_counter() - started:.1f}s", flush=True)
    return {"fetch_mode": "live", "status_code": status, "headers": response_headers}


def sniff_csv(zipped: zipfile.ZipFile, member: str) -> dict:
    with zipped.open(member) as raw:
        wrapper = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        reader = csv.reader(wrapper)
        header = next(reader, [])
        sample = []
        for _ in range(3):
            row = next(reader, None)
            if row is None:
                break
            sample.append(row)
    return {"member": member, "columns": header, "sample_rows": sample}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fetch = acquire()
    package_sha256 = sha256(PACKAGE_PATH)

    with zipfile.ZipFile(PACKAGE_PATH) as zipped:
        members = []
        schema_by_columns: dict[tuple[str, ...], dict] = {}
        for info in zipped.infolist():
            suffix = Path(info.filename).suffix.lower()
            row = {
                "member": info.filename,
                "suffix": suffix,
                "compressed_bytes": info.compress_size,
                "uncompressed_bytes": info.file_size,
                "crc32": f"{info.CRC:08x}",
            }
            members.append(row)
            if suffix == ".csv" and info.file_size:
                schema = sniff_csv(zipped, info.filename)
                key = tuple(schema["columns"])
                if key not in schema_by_columns:
                    schema_by_columns[key] = schema

    payload = {
        "program": "invisible-urbanization",
        "analysis": "GHSL Degree of Urbanisation R2023A V2.0 acquisition and schema inventory",
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "claim_scope": (
            "Source qualification only. The archive classifies GADM 4.1 administrative units "
            "using the GHSL Degree of Urbanisation method; it does not encode national legal "
            "urban designations and does not by itself identify invisible urbanization."
        ),
        "source": {
            "publisher": "European Commission Joint Research Centre",
            "product": "GHS-DUC R2023A V2.0",
            "url": PACKAGE_URL,
            "retrieved_at": now_iso(),
            "fetch_mode": fetch["fetch_mode"],
            "status_code": fetch["status_code"],
            "content_length_header": fetch.get("headers", {}).get("Content-Length"),
            "last_modified_header": fetch.get("headers", {}).get("Last-Modified"),
            "local_cache_name": PACKAGE_PATH.name,
            "bytes": PACKAGE_PATH.stat().st_size,
            "sha256": package_sha256,
        },
        "archive": {
            "member_count": len(members),
            "csv_member_count": sum(row["suffix"] == ".csv" for row in members),
            "xlsx_member_count": sum(row["suffix"] == ".xlsx" for row in members),
            "distinct_csv_schemas": len(schema_by_columns),
            "members": members,
            "schema_samples": list(schema_by_columns.values()),
        },
    }

    json_path = OUT / "invisible-urbanization-ghsl-duc-inventory.json"
    csv_path = OUT / "invisible-urbanization-ghsl-duc-members.csv"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(members[0]))
        writer.writeheader()
        writer.writerows(members)

    print("=== GHS-DUC acquisition and inventory ===")
    print(f"Archive bytes: {PACKAGE_PATH.stat().st_size:,}")
    print(f"SHA-256: {package_sha256}")
    print(f"Members: {len(members)}")
    print(f"CSV members: {payload['archive']['csv_member_count']}")
    print(f"Distinct CSV schemas: {len(schema_by_columns)}")
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {csv_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
