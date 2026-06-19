"""Fetch DGHS public facilities JSON pages for the PSDQ catchment upgrade.

The endpoint is paginated at 50 records per page. This fetcher is intentionally
polite and resumable: existing page files are skipped unless --force is set.
Run a full pull only when you are ready to validate and use the coordinate
fields downstream.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
URL_TEMPLATE = "https://hrm.dghs.gov.bd/public/facilities/json?page={page}"
USER_AGENT = "ADB-Research-PSDQ/0.1 (public-data research; polite paginated fetch)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=1, help="First page to fetch.")
    parser.add_argument("--end", type=int, default=None, help="Last page to fetch. Defaults to endpoint-reported last_page.")
    parser.add_argument("--sleep", type=float, default=0.75, help="Seconds to wait between requests.")
    parser.add_argument("--force", action="store_true", help="Refetch pages even if cache files already exist.")
    parser.add_argument("--timeout", type=float, default=60, help="Per-request timeout in seconds.")
    return parser.parse_args()


def cache_path(page: int) -> Path:
    return CACHE / f"bgd_public_facilities_p{page}.json"


def fetch_page(page: int, timeout: float) -> dict[str, Any]:
    url = URL_TEMPLATE.format(page=page)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw)


def load_or_fetch(page: int, force: bool, timeout: float) -> dict[str, Any]:
    path = cache_path(page)
    if path.exists() and not force:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    obj = fetch_page(page, timeout)
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    tmp.replace(path)
    return obj


def page_data(obj: dict[str, Any]) -> dict[str, Any]:
    data = obj.get("data", obj)
    if not isinstance(data, dict):
        raise ValueError("Unexpected DGHS response shape: missing data object")
    return data


def main() -> None:
    args = parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)

    first = load_or_fetch(args.start, args.force, args.timeout)
    first_data = page_data(first)
    last_page = int(first_data.get("last_page") or args.start)
    end = args.end if args.end is not None else last_page

    print(
        f"DGHS public facilities: fetching pages {args.start}-{end} "
        f"(endpoint reports last_page={last_page}, total={first_data.get('total')})"
    )
    print(f"page {args.start}: cached {len(first_data.get('items') or [])} records")

    for page in range(args.start + 1, end + 1):
        try:
            obj = load_or_fetch(page, args.force, args.timeout)
            data = page_data(obj)
            print(f"page {page}: cached {len(data.get('items') or [])} records")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            raise SystemExit(f"Failed on page {page}: {exc}") from exc
        if args.sleep > 0 and page < end:
            time.sleep(args.sleep)

    print("Done. Rerun scripts/audit-catchment-readiness.py before analysis.")


if __name__ == "__main__":
    main()
