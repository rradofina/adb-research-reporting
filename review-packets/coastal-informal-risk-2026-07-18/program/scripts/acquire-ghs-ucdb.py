"""Acquire and inventory the GHS-UCDB files used by the coastal study.

Downloads the V1.2 Exposure and General Characteristics thematic archives to
the repository cache, records byte counts and SHA-256 checksums, and inventories
their tabular schemas. Raw archives remain outside Git; the provenance record is
committed. Public data only. attestation_chain: ai-first.
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
CACHE = ROOT / ".cache" / "coastal-informal-risk-ghs-ucdb-r2024a-v1-2"
OUT = PROGRAM / "generated"
BASE = (
    "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_UCDB_GLOBE_R2024A/GHS_UCDB_THEME_GLOBE_R2024A"
)
PACKAGES = {
    "general_characteristics": (
        f"{BASE}/GHS_UCDB_THEME_GENERAL_CHARACTERISTICS_GLOBE_R2024A/V1-2/"
        "GHS_UCDB_THEME_GENERAL_CHARACTERISTICS_GLOBE_R2024A_V1_2.zip"
    ),
    "exposure": (
        f"{BASE}/GHS_UCDB_THEME_EXPOSURE_GLOBE_R2024A/V1-2/"
        "GHS_UCDB_THEME_EXPOSURE_GLOBE_R2024A_V1_2.zip"
    ),
}
USER_AGENT = "adb-research-factory/1.0 (public-data acquisition)"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def acquire(url: str, target: Path) -> dict:
    if target.exists():
        return {"fetch_mode": "cache", "status_code": 200, "headers": {}}

    partial = target.with_suffix(target.suffix + ".part")
    existing = partial.stat().st_size if partial.exists() else 0
    headers = {"User-Agent": USER_AGENT}
    if existing:
        headers["Range"] = f"bytes={existing}-"
    request = urllib.request.Request(url, headers=headers)
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=120) as response:
        status = int(getattr(response, "status", 200))
        if existing and status != 206:
            existing = 0
        mode = "ab" if existing and status == 206 else "wb"
        with partial.open(mode) as handle:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                handle.write(block)
        response_headers = dict(response.headers.items())
    partial.replace(target)
    print(f"Downloaded {target.name} in {time.perf_counter() - started:.1f}s")
    return {"fetch_mode": "live", "status_code": status, "headers": response_headers}


def csv_schema(zipped: zipfile.ZipFile, member: str) -> dict:
    with zipped.open(member) as raw:
        wrapper = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        reader = csv.reader(wrapper)
        header = next(reader, [])
        sample = [row for _, row in zip(range(2), reader)]
    return {"member": member, "columns": header, "sample_rows": sample}


def inventory(label: str, url: str) -> dict:
    target = CACHE / Path(url).name
    fetch = acquire(url, target)
    members = []
    schemas = []
    with zipfile.ZipFile(target) as zipped:
        for info in zipped.infolist():
            suffix = Path(info.filename).suffix.lower()
            members.append(
                {
                    "package": label,
                    "member": info.filename,
                    "suffix": suffix,
                    "compressed_bytes": info.compress_size,
                    "uncompressed_bytes": info.file_size,
                    "crc32": f"{info.CRC:08x}",
                }
            )
            if suffix == ".csv" and info.file_size:
                schemas.append(csv_schema(zipped, info.filename))
    return {
        "label": label,
        "url": url,
        "file": target.name,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "fetch_mode": fetch["fetch_mode"],
        "status_code": fetch["status_code"],
        "last_modified_header": fetch.get("headers", {}).get("Last-Modified"),
        "members": members,
        "schemas": schemas,
    }


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    packages = [inventory(label, url) for label, url in PACKAGES.items()]
    payload = {
        "program": "coastal-informal-risk",
        "analysis": "GHS-UCDB R2024A V1.2 acquisition and schema inventory",
        "attestation_chain": "ai-first",
        "generated_at": now_iso(),
        "retrieved_at": now_iso(),
        "license": "CC BY 4.0",
        "dataset_doi": "10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd",
        "claim_scope": (
            "Source qualification and custody. The archives measure harmonised urban-centre "
            "population and built-up surface in low-elevation coastal zones; they do not identify "
            "informal tenure, protection, service adequacy, or realized losses."
        ),
        "packages": packages,
    }
    json_path = OUT / "coastal-ghs-ucdb-inventory.json"
    csv_path = OUT / "coastal-ghs-ucdb-members.csv"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rows = [row for package in packages for row in package["members"]]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for package in packages:
        print(
            f"{package['label']}: {package['bytes']:,} bytes, "
            f"sha256={package['sha256']}, members={len(package['members'])}"
        )
        for schema in package["schemas"]:
            print(f"  CSV {schema['member']}: {len(schema['columns'])} columns")
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {csv_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
