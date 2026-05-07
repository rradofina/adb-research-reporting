"""Prepare a Bangladesh Open Buildings tile manifest for PSDQ.

The manifest identifies Google Open Buildings V3 S2 level-4 tiles that
intersect Bangladesh's geoBoundaries ADM0 polygon, then records the point and
polygon download URLs. The facility-buffer pipeline uses point CSVs because
they are much smaller than polygon CSVs and are sufficient for count
denominators.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from shapely.geometry import shape


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"
RAW_DIR = CACHE / "open-buildings"

TILES_URL = "https://openbuildings-public-dot-gweb-research.uw.r.appspot.com/public/tiles.geojson"
THRESHOLDS_URL = "https://storage.googleapis.com/open-buildings-data/v3/score_thresholds_s2_level_4.csv"
GEOBOUNDARIES_API = "https://www.geoboundaries.org/api/current/gbOpen/BGD/ADM0"

TILES_FILE = RAW_DIR / "open-buildings-v3-tiles.geojson"
THRESHOLDS_FILE = RAW_DIR / "score_thresholds_s2_level_4.csv"
BGD_BOUNDARY_FILE = RAW_DIR / "geoBoundaries-BGD-ADM0.geojson"
MANIFEST_JSON = OUT_DIR / "psdq-bgd-open-buildings-tile-manifest.json"
MANIFEST_CSV = OUT_DIR / "psdq-bgd-open-buildings-tile-manifest.csv"


def fetch_json(url: str) -> dict[str, Any]:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.json()


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    path.write_bytes(r.content)


def head_size_mb(url: str) -> float | None:
    try:
        r = requests.head(url, timeout=60)
        r.raise_for_status()
        n = r.headers.get("content-length")
        return round(int(n) / 1024 / 1024, 2) if n else None
    except Exception:
        return None


def load_thresholds() -> dict[str, dict[str, Any]]:
    download(THRESHOLDS_URL, THRESHOLDS_FILE)
    out: dict[str, dict[str, Any]] = {}
    with THRESHOLDS_FILE.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            out[row["s2_token"]] = {
                "confidence_threshold_80_precision": parse_float(row.get("confidence_threshold_80%_precision")),
                "confidence_threshold_85_precision": parse_float(row.get("confidence_threshold_85%_precision")),
                "confidence_threshold_90_precision": parse_float(row.get("confidence_threshold_90%_precision")),
                "building_count": parse_int(row.get("building_count")),
                "building_count_85_precision": parse_int(row.get("building_count_85%_precision")),
                "building_count_90_precision": parse_int(row.get("building_count_90%_precision")),
                "num_samples": parse_int(row.get("num_samples")),
            }
    return out


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tiles_obj = fetch_json(TILES_URL)
    TILES_FILE.write_text(json.dumps(tiles_obj), encoding="utf-8")

    boundary_meta = fetch_json(GEOBOUNDARIES_API)
    boundary_url = boundary_meta["gjDownloadURL"]
    download(boundary_url, BGD_BOUNDARY_FILE)
    boundary_obj = json.loads(BGD_BOUNDARY_FILE.read_text(encoding="utf-8"))
    boundary_geom = shape(boundary_obj["features"][0]["geometry"])

    thresholds = load_thresholds()
    rows = []
    for feature in tiles_obj["features"]:
        geom = shape(feature["geometry"])
        if not geom.intersects(boundary_geom):
            continue
        props = feature["properties"]
        tile_id = props["tile_id"]
        polygon_url = props["tile_url"]
        point_url = polygon_url.replace("/polygons_s2_level_4_gzip/", "/points_s2_level_4_gzip/")
        rows.append(
            {
                "tile_id": tile_id,
                "polygon_url": polygon_url,
                "point_url": point_url,
                "polygon_size_mb_catalog": float(props["size_mb"]),
                "point_size_mb_head": head_size_mb(point_url),
                **thresholds.get(tile_id, {}),
            }
        )

    rows.sort(key=lambda r: r["tile_id"])
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "program": "public-service-data-quality",
        "country": "Bangladesh",
        "source": {
            "open_buildings_tiles": TILES_URL,
            "open_buildings_thresholds": THRESHOLDS_URL,
            "boundary": boundary_url,
            "boundary_source": "geoBoundaries gbOpen BGD ADM0",
        },
        "method": "Intersect Google Open Buildings V3 tile polygons with Bangladesh ADM0; use point CSVs for nearest-facility building denominators.",
        "tiles": rows,
        "totals": {
            "tile_count": len(rows),
            "polygon_size_mb_catalog": round(sum(r["polygon_size_mb_catalog"] for r in rows), 2),
            "point_size_mb_head": round(sum((r["point_size_mb_head"] or 0) for r in rows), 2),
            "building_count_catalog": sum((r.get("building_count") or 0) for r in rows),
            "building_count_85_precision_catalog": sum((r.get("building_count_85_precision") or 0) for r in rows),
            "building_count_90_precision_catalog": sum((r.get("building_count_90_precision") or 0) for r in rows),
        },
        "non_claim": "Tile-level catalog counts include areas outside Bangladesh where S2 tiles cross borders; downstream scripts filter points to the Bangladesh ADM0 polygon.",
    }
    MANIFEST_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["tile_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {MANIFEST_JSON}")
    print(f"Wrote {MANIFEST_CSV}")
    print(
        f"{payload['totals']['tile_count']} tiles; "
        f"{payload['totals']['point_size_mb_head']:.2f} MB point gzip total"
    )


if __name__ == "__main__":
    main()
