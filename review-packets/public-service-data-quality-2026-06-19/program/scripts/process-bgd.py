"""Process BGD DGHS facility-registry data and compute OSM-vs-DGHS disagreement per ADM1."""
import json, glob, re, csv, os
from collections import Counter, defaultdict
from datetime import datetime, timezone
import html as htmlmod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
OUT_DIR = ROOT / "generated"
os.makedirs(OUT_DIR, exist_ok=True)

# Load BGD DGHS pages
files = []
for p in glob.glob(f"{CACHE}/bgd_dghs_p*.json"):
    m = re.search(r"bgd_dghs_p(\d+)\.json$", p)
    if m: files.append((int(m.group(1)), p))
files.sort()
all_recs = []
for _, p in files:
    d = json.load(open(p))
    all_recs.extend(d.get("data", []))
print(f"BGD DGHS total records: {len(all_recs)}")

# Check active status
active = [r for r in all_recs if r.get("is_active")]
print(f"Active facilities: {len(active)}")

# BGD division names -> ISO 3166-2:BD ADM1 codes (matches access-services schema)
DIVISION_TO_ADM1 = {
    "Barisal": "BD-A",
    "Barishal": "BD-A",
    "Chattogram": "BD-B",
    "Chittagong": "BD-B",
    "Dhaka": "BD-C",
    "Khulna": "BD-D",
    "Rajshahi": "BD-E",
    "Rajshani": "BD-E",
    "Rangpur": "BD-F",
    "Sylhet": "BD-G",
    "Mymensingh": "BD-H",
}

# Facility-type categories: inspect facility_type_name
# Count distinct types
type_counts = Counter(r.get("facility_type_name") for r in active)
print(f"\nDistinct facility types: {len(type_counts)}")
print("Top 25 types:")
for t, n in type_counts.most_common(25):
    print(f"  {n:>6}  {t}")

# Division distribution
div_counts = Counter(r.get("division_name") for r in active)
print(f"\nActive facilities per division:")
for d, n in sorted(div_counts.items(), key=lambda x: -x[1]):
    print(f"  {d:>18}  {n:>6}")
