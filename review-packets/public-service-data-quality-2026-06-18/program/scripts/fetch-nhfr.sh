#!/usr/bin/env bash
# Fetch DOH National Health Facility Registry (NHFR) — Philippines.
# Governed by CONSTITUTION.md §11 (committed cache for reproducibility).
#
# Output: 23 JSON pages of 2000 facilities each, cached at
#   ../.cache/nhfr_p{1..23}.json
# Total: ~44,267 active facilities, ~14.7 MB cache.
#
# Source: https://nhfr.doh.gov.ph/VActivefacilitiesList
# Access model: A (public, JWT-issued per landing page; no login required).
# License: Unstated. Public-information-disclosure framing per RA 9485.
#
# Usage:
#   bash scripts/fetch-nhfr.sh           # fetch (skip already-cached pages)
#   PSDQ_REFRESH=1 bash scripts/fetch-nhfr.sh   # force refresh

set -euo pipefail

CACHE_DIR="$(cd "$(dirname "$0")/.." && pwd)/.cache"
mkdir -p "$CACHE_DIR"

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
PAGE_SIZE=2000

refresh_jwt() {
  curl -sS -A "$UA" -o "$CACHE_DIR/nhfr_landing.html" \
    "https://nhfr.doh.gov.ph/VActivefacilitiesList" >/dev/null
}

read_jwt() {
  grep -oE 'API_JWT_TOKEN: "[^"]*"' "$CACHE_DIR/nhfr_landing.html" \
    | sed -E 's/.*"([^"]+)".*/\1/'
}

# Get a fresh JWT
refresh_jwt
JWT=$(read_jwt)

# Discover total record count from page 1
curl -sS -A "$UA" -H "X-Authorization: Bearer $JWT" --max-time 60 \
  -o "$CACHE_DIR/nhfr_p1.json" \
  "https://nhfr.doh.gov.ph/api/list/v_activefacilities?recperpage=${PAGE_SIZE}&start=1"

TOTAL=$(python -c "import json; print(json.load(open('$CACHE_DIR/nhfr_p1.json'))['totalRecordCount'])")
PAGES=$(( (TOTAL + PAGE_SIZE - 1) / PAGE_SIZE ))
echo "Total active facilities: $TOTAL  ->  $PAGES pages of $PAGE_SIZE"

# Fetch remaining pages (page 1 already done)
for p in $(seq 2 "$PAGES"); do
  OUT="$CACHE_DIR/nhfr_p${p}.json"
  if [ -f "$OUT" ] && [ -s "$OUT" ] && [ "${PSDQ_REFRESH:-}" != "1" ]; then
    echo "p$p cached"
    continue
  fi
  START=$(( (p - 1) * PAGE_SIZE + 1 ))
  for attempt in 1 2 3; do
    SC=$(curl -sS -A "$UA" -H "X-Authorization: Bearer $JWT" --max-time 90 \
      -o "$OUT" -w "%{http_code}" \
      "https://nhfr.doh.gov.ph/api/list/v_activefacilities?recperpage=${PAGE_SIZE}&start=${START}")
    SIZE=$(stat -c%s "$OUT" 2>/dev/null || stat -f%z "$OUT")
    if [ "$SC" = "200" ] && [ "$SIZE" -gt 50000 ]; then
      echo "p$p start=$START http=$SC size=$SIZE"
      break
    fi
    echo "p$p attempt $attempt failed (http=$SC size=$SIZE) — refreshing JWT and retrying"
    refresh_jwt
    JWT=$(read_jwt)
    sleep 5
  done
  sleep 1.2  # polite cadence
done

echo
echo "Cached pages:"
ls -1 "$CACHE_DIR"/nhfr_p*.json | wc -l
