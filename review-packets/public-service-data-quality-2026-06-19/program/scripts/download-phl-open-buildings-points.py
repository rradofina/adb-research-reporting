"""Download Philippines-intersecting Google Open Buildings V3 point shards.

The downloads are resumable. If a `.part` file exists, the script requests
the remaining byte range. Completed files are stored under
`.cache/open-buildings/points/`.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache" / "open-buildings" / "points"
MANIFEST_JSON = ROOT / "generated" / "psdq-phl-open-buildings-tile-manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=3, help="Concurrent downloads.")
    parser.add_argument("--tiles", nargs="*", default=None, help="Optional tile_id subset.")
    parser.add_argument("--timeout", type=float, default=180, help="Request timeout in seconds.")
    return parser.parse_args()


def load_tiles(selected: list[str] | None) -> list[dict[str, Any]]:
    obj = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    tiles = obj["tiles"]
    if selected:
        wanted = set(selected)
        tiles = [tile for tile in tiles if tile["tile_id"] in wanted]
    return tiles


def local_path(tile_id: str) -> Path:
    return CACHE / f"{tile_id}_buildings.csv.gz"


def remote_size(url: str, timeout: float) -> int | None:
    r = requests.head(url, timeout=timeout)
    r.raise_for_status()
    n = r.headers.get("content-length")
    return int(n) if n else None


def download_tile(tile: dict[str, Any], timeout: float) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    tile_id = tile["tile_id"]
    url = tile["point_url"]
    dest = local_path(tile_id)
    part = dest.with_suffix(dest.suffix + ".part")
    size = remote_size(url, timeout)

    if dest.exists() and size and dest.stat().st_size == size:
        return f"{tile_id}: already complete ({size} bytes)"

    start = part.stat().st_size if part.exists() else 0
    headers = {"Range": f"bytes={start}-"} if start else {}
    with requests.get(url, headers=headers, stream=True, timeout=timeout) as r:
        if r.status_code == 416 and size and part.exists() and part.stat().st_size == size:
            part.replace(dest)
            return f"{tile_id}: completed from existing part"
        r.raise_for_status()
        mode = "ab" if start and r.status_code == 206 else "wb"
        if mode == "wb" and part.exists():
            part.unlink()
        with part.open(mode) as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    if size and part.stat().st_size != size:
        return f"{tile_id}: partial {part.stat().st_size}/{size} bytes"
    part.replace(dest)
    return f"{tile_id}: complete ({dest.stat().st_size} bytes)"


def main() -> None:
    args = parse_args()
    tiles = load_tiles(args.tiles)
    if not tiles:
        raise SystemExit("No tiles selected.")
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(download_tile, tile, args.timeout) for tile in tiles]
        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()
