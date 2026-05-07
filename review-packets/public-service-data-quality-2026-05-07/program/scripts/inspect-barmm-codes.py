"""Resolve the 257 unmatched BARMM Maguindanao NHFR records by matching
the barangay name (extracted from each facility's hfhudname) against the
PSA/NAMRIA 2023 ADM4 layer within the BARMM region.

Finding (2026-05-07): NHFR uses an older PSGC vintage where many BARMM
Maguindanao barangays were assigned to different parent municipalities.
PSA/NAMRIA 2023 has reassigned them to existing ADM3 polygons. The
resolution is deterministic: extract barangay name from the facility
name (e.g., "AMBOLODTO BARANGAY HEALTH STATION" -> "AMBOLODTO"), look
up that name in PSA/NAMRIA ADM4 within ADM2 PH19087 + PH19088, take
the parent ADM3.

Output: generated/psdq-phl-nhfr-barmm-ctymun-resolution.json (a
crosswalk that downstream scripts can consume).
"""
import json
import re
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
GEN = ROOT / "generated"
GDB = CACHE / "phl-boundaries" / "gdb" / "phl_adm_psa_namria_20231106_GDB.gdb"

# Regex strips standard NHFR facility-type suffixes to leave the barangay
# (or municipality) name. NHFR facility names follow patterns like
# "{BARANGAY_NAME} BARANGAY HEALTH STATION", "{NAME} RURAL HEALTH UNIT",
# "{NAME} CLINIC AND HOSPITAL", etc.
SUFFIX_PATTERNS = [
    r"\s+BARANGAY HEALTH STATION$",
    r"\s+RURAL HEALTH UNIT$",
    r"\s+MAIN HEALTH CENTER$",
    r"\s+MUNICIPAL HEALTH OFFICE$",
    r"\s+CITY HEALTH OFFICE$",
    r"\s+BIRTHING HOME(?: AND CLINIC)?$",
    r"\s+LYING(?:-| )IN CLINIC.*$",
]


def extract_locality_name(facility_name: str) -> str | None:
    """Extract the locality (barangay or municipality) name from the
    NHFR facility name by stripping a known suffix pattern. Returns
    None if no recognizable suffix is present."""
    s = facility_name.strip()
    for pat in SUFFIX_PATTERNS:
        m = re.search(pat, s, flags=re.IGNORECASE)
        if m:
            return s[: m.start()].strip()
    return None


# 1. Collect NHFR records in 19087*/19088* ctymuncodes.
nhfr_files = sorted(CACHE.glob("nhfr_p*.json"))
records = []
for f in nhfr_files:
    data = json.loads(f.read_text(encoding="utf-8"))
    for row in data.get("v_activefacilities", []):
        cty = str(row.get("ctymuncode") or "")
        if cty.startswith(("19087", "19088")):
            records.append({
                "ctymuncode": cty,
                "bgycode": str(row.get("bgycode") or ""),
                "facility_name": (row.get("hfhudname") or "").strip(),
            })
print(f"NHFR records in 19087*/19088*: {len(records)}")

# 2. Load PSA/NAMRIA boundary data, filter to BARMM Maguindanao split.
# Suppress only pyogrio's known polygon-parts RuntimeWarning during read;
# do not silence module-wide warnings (a broad simplifier swallows real
# data-quality warnings from downstream code).
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="pyogrio.raw")
    adm3 = gpd.read_file(GDB, layer="phl_admbnda_adm3_psa_namria_20231106")
    adm4 = gpd.read_file(GDB, layer="phl_admbnda_adm4_psa_namria_20231106")
adm3_by_code = {r["ADM3_PCODE"]: r["ADM3_EN"] for _, r in adm3.iterrows()}
maguindanao_adm4 = adm4[adm4["ADM2_PCODE"].astype(str).isin(["PH19087", "PH19088"])]
print(f"PSA/NAMRIA ADM4 polygons in PH19087+PH19088: {len(maguindanao_adm4)}")

# Build a name -> [(adm4_pcode, adm3_pcode, adm3_en)] index. Several
# barangays share names across municipalities; we keep all candidates.
name_index: dict[str, list] = defaultdict(list)
for _, r in maguindanao_adm4.iterrows():
    name = str(r["ADM4_EN"]).strip().lower()
    name_index[name].append({
        "adm4_pcode": r["ADM4_PCODE"],
        "adm4_en": r["ADM4_EN"],
        "adm3_pcode": r["ADM3_PCODE"],
        "adm3_en": r["ADM3_EN"],
    })

# 3. For each NHFR record, extract a candidate locality name and look
#    it up. Vote per ctymuncode.
unmatched_ctymuncodes = sorted({r["ctymuncode"] for r in records
                                if f"PH{r['ctymuncode']}" not in adm3_by_code})

resolution = {}
for cty in unmatched_ctymuncodes:
    group = [r for r in records if r["ctymuncode"] == cty]
    adm3_votes = Counter()
    matched_barangays = []
    unmatched_facility_names = []
    sample_facilities = []
    for r in group:
        if len(sample_facilities) < 3:
            sample_facilities.append(r["facility_name"])
        locality = extract_locality_name(r["facility_name"])
        if not locality:
            unmatched_facility_names.append(r["facility_name"])
            continue
        candidates = name_index.get(locality.lower())
        if candidates and len(candidates) == 1:
            c = candidates[0]
            adm3_votes[c["adm3_pcode"]] += 1
            if len(matched_barangays) < 3:
                matched_barangays.append(f"{locality} -> {c['adm3_en']}")
        else:
            unmatched_facility_names.append(r["facility_name"])

    total_votes = sum(adm3_votes.values())
    if total_votes:
        winner_pcode, winner_count = adm3_votes.most_common(1)[0]
        resolution[cty] = {
            "attempted_pcode": f"PH{cty}",
            "n_nhfr_records": len(group),
            "name_resolved_count": total_votes,
            "psa_adm3_pcode": winner_pcode,
            "psa_adm3_name": adm3_by_code.get(winner_pcode),
            "winner_share": round(winner_count / total_votes, 3),
            "all_adm3_votes": dict(adm3_votes),
            "sample_resolved_barangays": matched_barangays,
            "sample_facilities": sample_facilities,
            "unresolved_facility_names": unmatched_facility_names[:5],
            "rule": "name-resolved" if winner_count == total_votes else "name-resolved-majority",
        }
    else:
        resolution[cty] = {
            "attempted_pcode": f"PH{cty}",
            "n_nhfr_records": len(group),
            "name_resolved_count": 0,
            "rule": "unresolved",
            "sample_facilities": sample_facilities,
            "unresolved_facility_names": unmatched_facility_names[:5],
        }

# 4. Print results.
n_resolved = sum(1 for r in resolution.values() if r["rule"].startswith("name-resolved"))
n_records_resolved = sum(r.get("name_resolved_count", 0) for r in resolution.values())
n_unmatched_records = sum(1 for r in records if f"PH{r['ctymuncode']}" not in adm3_by_code)
print(f"\nResolved ctymuncodes: {n_resolved} of {len(resolution)}")
print(f"Records resolved (out of {n_unmatched_records}): {n_records_resolved}")
print()
for cty, info in sorted(resolution.items()):
    if info["rule"].startswith("name-resolved"):
        print(f"  {info['attempted_pcode']} ({info['n_nhfr_records']} rec) -> {info['psa_adm3_pcode']} '{info['psa_adm3_name']}' "
              f"({info['name_resolved_count']}/{info['n_nhfr_records']} barangay name matches, share {info['winner_share']})")
    else:
        print(f"  {info['attempted_pcode']} ({info['n_nhfr_records']} rec) -> UNRESOLVED  samples={info['sample_facilities'][:1]}")

# 5. Write the crosswalk.
out = GEN / "psdq-phl-nhfr-barmm-ctymun-resolution.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({
    "generated_by": "scripts/inspect-barmm-codes.py",
    "purpose": "Deterministic crosswalk from NHFR BARMM Maguindanao ctymuncodes (older PSGC vintage) to PSA/NAMRIA 2023 ADM3 PCODEs, via barangay-name lookup against PSA/NAMRIA ADM4 within ADM2 PH19087+PH19088.",
    "framing": "Code-vintage crosswalk only. The rule is: take the barangay name from the NHFR facility name suffix pattern, look it up in PSA/NAMRIA ADM4 within BARMM Maguindanao, take the parent ADM3. Per ctymuncode the rule is the majority winner across that group's records.",
    "non_imputation": "No new poverty, building, or service quantity is generated. Only the spatial assignment of NHFR records to PSA/NAMRIA ADM3 is changed for the resolved cases.",
    "summary": {
        "total_nhfr_records_in_19087_19088": len(records),
        "directly_matched_records": len(records) - sum(r.get("n_nhfr_records", 0) for r in resolution.values()),
        "ctymuncodes_unmatched_directly": len(unmatched_ctymuncodes),
        "ctymuncodes_resolved_by_barangay_name": n_resolved,
        "records_resolved_by_barangay_name": n_records_resolved,
    },
    "resolution": resolution,
}, indent=2), encoding="utf-8")
print(f"\nWrote {out.relative_to(ROOT)}")
