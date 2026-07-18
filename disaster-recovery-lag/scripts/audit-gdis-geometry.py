"""Audit gross GDIS coordinate-country mismatches in the VIIRS overlap window.

The audit uses Natural Earth 1:50m country polygons already committed under
opensrc/. A row is labelled a gross mismatch only when its centroid is more
than 1,000 km from the polygon assigned by its GDIS ISO3 code. The deliberately
high threshold avoids treating small-island and coastline generalisation as a
source error.

attestation_chain: ai-first
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import geopandas as gpd
from shapely.geometry import Point


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
GDIS_ZIP = PROGRAM / ".cache" / "gdis" / "gdis-1960-2018-disasterlocations-csv.zip"
BOUNDARIES = ROOT / "opensrc" / "world-boundaries" / "ne_50m_admin_0_countries.geojson"
OUT = PROGRAM / "generated"
THRESHOLD_KM = 1000

ADB_DMCS = {
    "AFG", "ARM", "AZE", "BGD", "BTN", "BRN", "KHM", "CHN", "FJI", "GEO",
    "IND", "IDN", "KAZ", "KIR", "KGZ", "LAO", "MYS", "MDV", "MHL", "FSM",
    "MNG", "MMR", "NPL", "PAK", "PNG", "PHL", "WSM", "SLB", "LKA", "TJK",
    "THA", "TLS", "TON", "TKM", "TUV", "UZB", "VUT", "VNM",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with zipfile.ZipFile(GDIS_ZIP) as archive:
        member = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
        with archive.open(member) as raw:
            rows = list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")))
    selected = [row for row in rows if row.get("iso3") in ADB_DMCS and 2012 <= int(row["year"]) <= 2018]

    countries = gpd.read_file(BOUNDARIES).to_crs(6933)
    polygons = {
        iso3: countries[
            (countries["ADM0_A3"] == iso3)
            | (countries["ISO_A3"] == iso3)
            | (countries["SOV_A3"] == iso3)
        ].geometry.union_all()
        for iso3 in ADB_DMCS
    }
    points = gpd.GeoSeries(
        [Point(float(row["longitude"]), float(row["latitude"])) for row in selected],
        crs=4326,
    ).to_crs(6933)

    audited: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    for row, point in zip(selected, points):
        distance_km = float(point.distance(polygons[row["iso3"]]) / 1000)
        output = {
            "iso3": row["iso3"],
            "gdis_id": row["id"],
            "disasterno": row["disasterno"],
            "year": int(row["year"]),
            "disastertype": row["disastertype"].strip(),
            "adm1": row["adm1"],
            "adm2": row["adm2"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "distance_to_country_polygon_km": distance_km,
            "gross_mismatch": distance_km > THRESHOLD_KM,
        }
        audited.append(output)
        if output["gross_mismatch"]:
            mismatches.append(output)

    write_csv(OUT / "disaster-recovery-gdis-geometry-audit.csv", audited)
    payload = {
        "program": "disaster-recovery-lag",
        "analysis": "GDIS coordinate-country gross mismatch audit",
        "window": "ADB analysis roster, 2012-2018 GDIS x VIIRS overlap window",
        "rows_audited": len(audited),
        "gross_mismatch_threshold_km": THRESHOLD_KM,
        "gross_mismatch_rows": len(mismatches),
        "gross_mismatch_share": len(mismatches) / len(audited),
        "mismatches": mismatches,
        "interpretation": (
            "The threshold is a gross-error screen, not a full geocoding validation. "
            "Rows near coasts or small islands are not labelled mismatches unless their "
            "projected distance exceeds 1,000 km."
        ),
        "sources": {
            "gdis": {"file": str(GDIS_ZIP.relative_to(ROOT)), "sha256": sha256(GDIS_ZIP)},
            "natural_earth": {"file": str(BOUNDARIES.relative_to(ROOT)), "sha256": sha256(BOUNDARIES)},
        },
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with (OUT / "disaster-recovery-gdis-geometry-audit.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"Audited {len(audited):,} GDIS rows; gross mismatches: {len(mismatches)}")


if __name__ == "__main__":
    main()
