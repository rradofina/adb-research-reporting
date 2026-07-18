"""Social-protection shock-payment source-readiness audit.

The dropped-leg artifact shows that the named headline five depends on a
both-legs-present filter. This script adds a source audit for the legs
themselves:

  * ASPIRE all social protection and labor coverage is not a shock-payment
    delivery measure.
  * A narrower ASPIRE social safety-net coverage leg is available as a WDI
    diagnostic, but still does not identify emergency-transfer delivery.
  * The WDI poverty indicator metadata now names the line as $3.00/day
    (2021 PPP), while older program prose says $2.15/day (2017 PPP).

The audit fetches public WDI data/metadata, reruns a social-safety-net variant
of the readiness-gap screen, and records which actual shock-payment objects
remain unjoined. Public data only. attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "source-readiness"
OUT = BASE / "generated"
DROPPED_PATH = OUT / "social-protection-dropped-leg.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
PER_PAGE = 20000
WDI_ALL_SP = "per_allsp.cov_pop_tot"
WDI_SAFETY_NET = "per_sa_allsa.cov_pop_tot"
WDI_ACCOUNT = "FX.OWN.TOTL.ZS"
WDI_POVERTY = "SI.POV.DDAY"
WDI_POVERTY_GAP = "SI.POV.GAPS"

ADB_NAMES = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan", "BGD": "Bangladesh", "BTN": "Bhutan",
    "BRN": "Brunei Darussalam", "KHM": "Cambodia", "CHN": "China", "COK": "Cook Islands",
    "FJI": "Fiji", "GEO": "Georgia", "HKG": "Hong Kong SAR", "IND": "India", "IDN": "Indonesia",
    "KAZ": "Kazakhstan", "KIR": "Kiribati", "KGZ": "Kyrgyzstan", "LAO": "Lao PDR",
    "MYS": "Malaysia", "MDV": "Maldives", "MHL": "Marshall Islands", "FSM": "Micronesia",
    "MNG": "Mongolia", "MMR": "Myanmar", "NRU": "Nauru", "NPL": "Nepal",
    "PAK": "Pakistan", "PLW": "Palau", "PNG": "Papua New Guinea", "PHL": "Philippines",
    "WSM": "Samoa", "SLB": "Solomon Islands", "LKA": "Sri Lanka", "TJK": "Tajikistan",
    "THA": "Thailand", "TLS": "Timor-Leste", "TON": "Tonga", "TKM": "Turkmenistan",
    "TUV": "Tuvalu", "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam", "TWN": "Taiwan",
}

HEADLINE_FIVE = ["BGD", "LAO", "MMR", "PAK", "PHL"]


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def round_or_none(value, digits=2):
    if value is None:
        return None
    return round(float(value), digits)


def fetch_bytes(url, cache_path):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "adb-research-factory/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read()
            status = getattr(response, "status", None)
            response_headers = dict(response.headers.items())
        cache_path.write_bytes(raw)
        mode = "live"
    except (urllib.error.URLError, TimeoutError) as exc:
        if not cache_path.exists():
            raise
        raw = cache_path.read_bytes()
        status = None
        response_headers = {}
        mode = f"cache fallback after {exc.__class__.__name__}"
    return raw, {
        "url": url,
        "cache_path": str(cache_path.relative_to(BASE)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "status_code": status,
        "fetch_mode": mode,
        "response_headers": response_headers,
    }


def fetch_json(url, cache_path):
    raw, record = fetch_bytes(url, cache_path)
    try:
        return json.loads(raw.decode("utf-8-sig")), record
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse JSON from {url}: {exc}") from exc


def unwrap_world_bank_rows(payload):
    if isinstance(payload, list) and len(payload) >= 2 and isinstance(payload[1], list):
        return payload[1]
    return []


def parse_wdi_series(payload):
    out = defaultdict(dict)
    observations = 0
    for row in unwrap_world_bank_rows(payload):
        if not isinstance(row, dict):
            continue
        iso = row.get("countryiso3code")
        value = row.get("value")
        if iso not in ADB_NAMES or not isinstance(value, (int, float)):
            continue
        observations += 1
        out[iso][int(row["date"])] = float(value)
    return out, observations


def latest_dict(series):
    values = {}
    years = {}
    for iso in ADB_NAMES:
        years_for_iso = series.get(iso)
        if not years_for_iso:
            continue
        year = max(years_for_iso)
        values[iso] = float(years_for_iso[year])
        years[iso] = int(year)
    return values, years


def years_span(year_values):
    years = sorted({int(year) for year in year_values if year is not None})
    if not years:
        return None
    if years[0] == years[-1]:
        return str(years[0])
    return f"{years[0]}-{years[-1]}"


def wdi_country_all_url(indicator_id):
    return (
        f"{WORLD_BANK_API_BASE}/country/all/indicator/{indicator_id}"
        f"?format=json&per_page={PER_PAGE}"
    )


def fetch_wdi_indicator(indicator_id, cache_records):
    data_url = wdi_country_all_url(indicator_id)
    metadata_url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
    slug = slugify(indicator_id)
    data_payload, data_record = fetch_json(data_url, CACHE / f"wdi_{slug}_all.json")
    metadata_payload, metadata_record = fetch_json(metadata_url, CACHE / f"wdi_{slug}_metadata.json")
    series, observations = parse_wdi_series(data_payload)
    values, years = latest_dict(series)
    metadata_rows = unwrap_world_bank_rows(metadata_payload)
    metadata = metadata_rows[0] if metadata_rows else {}
    meta = data_payload[0] if isinstance(data_payload, list) and data_payload else {}
    record = {
        "indicator_id": indicator_id,
        "indicator_name": metadata.get("name"),
        "indicator_source": metadata.get("source", {}).get("value") if isinstance(metadata.get("source"), dict) else metadata.get("source"),
        "source_note": metadata.get("sourceNote"),
        "data_url": data_url,
        "metadata_url": metadata_url,
        "dmc_observations": observations,
        "dmc_latest_rows": len(values),
        "world_bank_lastupdated": meta.get("lastupdated"),
        "latest_year_span": years_span(years.values()),
        "data_sha256": data_record["sha256"],
        "metadata_sha256": metadata_record["sha256"],
        "data_fetch_mode": data_record["fetch_mode"],
        "metadata_fetch_mode": metadata_record["fetch_mode"],
    }
    cache_records.append({**data_record, "query_type": "wdi_indicator_data", "indicator_id": indicator_id})
    cache_records.append({**metadata_record, "query_type": "wdi_indicator_metadata", "indicator_id": indicator_id})
    return series, record


def gap_row(iso, poverty_values, poverty_years, coverage_values, coverage_years, account_values, account_years, coverage_label):
    poverty = poverty_values.get(iso)
    coverage = coverage_values.get(iso)
    account = account_values.get(iso)
    if poverty is None or (coverage is None and account is None):
        return None
    coverage_part = (coverage or 0.0) / 100.0
    account_part = (account or 0.0) / 100.0
    if coverage is not None and account is not None:
        mean_readiness = (coverage_part + account_part) / 2.0
        legs = "both"
    elif coverage is not None:
        mean_readiness = coverage_part
        legs = f"{coverage_label}-only"
    else:
        mean_readiness = account_part
        legs = "account-only"
    gap = round((poverty / 100.0) * (1.0 - mean_readiness) * 100.0, 1)
    return {
        "iso3": iso,
        "country": ADB_NAMES[iso],
        "poverty_pct": round_or_none(poverty, 4),
        "poverty_year": poverty_years.get(iso),
        "coverage_pct": round_or_none(coverage, 4),
        "coverage_year": coverage_years.get(iso),
        "findex_account_pct": round_or_none(account, 4),
        "findex_year": account_years.get(iso),
        "legs_present": legs,
        "gap": gap,
        "in_headline_five": iso in HEADLINE_FIVE,
    }


def compute_variant(coverage_values, coverage_years, account_values, account_years, poverty_values, poverty_years, coverage_label):
    rows = []
    for iso in ADB_NAMES:
        row = gap_row(
            iso,
            poverty_values,
            poverty_years,
            coverage_values,
            coverage_years,
            account_values,
            account_years,
            coverage_label,
        )
        if row:
            rows.append(row)
    rows.sort(key=lambda row: (-row["gap"], row["iso3"]))
    for index, row in enumerate(rows, 1):
        row["rank"] = index
    return rows


def source_row(layer_role, source_name, source_url, key_id, reachable, candidate_rows, joined_rows, status, notes):
    return {
        "layer_role": layer_role,
        "source_name": source_name,
        "source_url": source_url,
        "key_id": key_id,
        "public_metadata_reachable": bool(reachable),
        "candidate_rows": int(candidate_rows or 0),
        "joined_rows": int(joined_rows or 0),
        "status": status,
        "notes": notes,
    }


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_dropped_artifact():
    if not DROPPED_PATH.exists():
        raise FileNotFoundError(f"{DROPPED_PATH} missing. Run scripts/deepen-include-partial.py first.")
    return json.loads(DROPPED_PATH.read_text(encoding="utf-8"))


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    dropped = load_dropped_artifact()
    cache_records = []

    all_sp_series, all_sp_record = fetch_wdi_indicator(WDI_ALL_SP, cache_records)
    safety_net_series, safety_net_record = fetch_wdi_indicator(WDI_SAFETY_NET, cache_records)
    account_series, account_record = fetch_wdi_indicator(WDI_ACCOUNT, cache_records)
    poverty_series, poverty_record = fetch_wdi_indicator(WDI_POVERTY, cache_records)
    poverty_gap_series, poverty_gap_record = fetch_wdi_indicator(WDI_POVERTY_GAP, cache_records)

    all_sp_values, all_sp_years = latest_dict(all_sp_series)
    safety_net_values, safety_net_years = latest_dict(safety_net_series)
    account_values, account_years = latest_dict(account_series)
    poverty_values, poverty_years = latest_dict(poverty_series)
    poverty_gap_values, poverty_gap_years = latest_dict(poverty_gap_series)

    all_sp_rows = compute_variant(
        all_sp_values,
        all_sp_years,
        account_values,
        account_years,
        poverty_values,
        poverty_years,
        "all-sp",
    )
    safety_net_rows = compute_variant(
        safety_net_values,
        safety_net_years,
        account_values,
        account_years,
        poverty_values,
        poverty_years,
        "safety-net",
    )

    old_by_iso = {row["iso3"]: row for row in dropped.get("value_ranked_order", [])}
    safety_by_iso = {row["iso3"]: row for row in safety_net_rows}
    all_sp_by_iso = {row["iso3"]: row for row in all_sp_rows}
    rerank_rows = []
    for iso, country in sorted(ADB_NAMES.items(), key=lambda item: item[1]):
        old = old_by_iso.get(iso, {})
        all_sp = all_sp_by_iso.get(iso, {})
        safety = safety_by_iso.get(iso, {})
        rerank_rows.append({
            "iso3": iso,
            "country": country,
            "old_value_rank": old.get("rank"),
            "old_gap": old.get("gap"),
            "old_legs_present": old.get("legs_present"),
            "headline_member": iso in HEADLINE_FIVE,
            "all_sp_live_rank": all_sp.get("rank"),
            "all_sp_live_gap": all_sp.get("gap"),
            "all_sp_coverage_pct": all_sp.get("coverage_pct"),
            "all_sp_year": all_sp.get("coverage_year"),
            "safety_net_rank": safety.get("rank"),
            "safety_net_gap": safety.get("gap"),
            "safety_net_coverage_pct": safety.get("coverage_pct"),
            "safety_net_year": safety.get("coverage_year"),
            "findex_account_pct": safety.get("findex_account_pct") or all_sp.get("findex_account_pct"),
            "findex_year": safety.get("findex_year") or all_sp.get("findex_year"),
            "poverty_headcount_pct": safety.get("poverty_pct") or all_sp.get("poverty_pct"),
            "poverty_year": safety.get("poverty_year") or all_sp.get("poverty_year"),
            "poverty_gap_pct": round_or_none(poverty_gap_values.get(iso), 4),
            "poverty_gap_year": poverty_gap_years.get(iso),
            "safety_net_in_top5": bool(safety.get("rank") and safety.get("rank") <= 5),
            "safety_net_legs_present": safety.get("legs_present"),
        })
    rerank_rows.sort(key=lambda row: (row["safety_net_rank"] or 999, row["old_value_rank"] or 999, row["country"]))

    safety_top5 = [row["iso3"] for row in safety_net_rows[:5]]
    all_sp_live_top5 = [row["iso3"] for row in all_sp_rows[:5]]
    old_value_top5 = [row["iso3"] for row in dropped.get("value_ranked_order", [])[:5]]
    entered_safety = [iso for iso in safety_top5 if iso not in HEADLINE_FIVE]
    dropped_safety = [iso for iso in HEADLINE_FIVE if iso not in safety_top5]
    overlap_safety_headline = len(set(safety_top5) & set(HEADLINE_FIVE))

    old_source_name = str((dropped.get("source") or {}).get("name") or "")
    poverty_line_mismatch = "$2.15" in old_source_name and "$3.00" in str(poverty_record.get("indicator_name") or "")

    source_rows = [
        source_row(
            "old_coverage_proxy",
            "World Bank WDI ASPIRE all social protection and labor coverage",
            all_sp_record["data_url"],
            WDI_ALL_SP,
            all_sp_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(all_sp_values),
            "old proxy available; not shock-payment delivery",
            (
                f"{len(all_sp_values)} roster economies have latest all-SP coverage values; "
                f"latest-year span {all_sp_record['latest_year_span']}."
            ),
        ),
        source_row(
            "narrower_coverage_proxy",
            "World Bank WDI ASPIRE social safety-net coverage",
            safety_net_record["data_url"],
            WDI_SAFETY_NET,
            safety_net_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(safety_net_values),
            "narrower social-assistance diagnostic available",
            (
                f"{len(safety_net_values)} roster economies have latest social safety-net values; "
                f"latest-year span {safety_net_record['latest_year_span']}."
            ),
        ),
        source_row(
            "payment_account_proxy",
            "World Bank WDI Global Findex account ownership",
            account_record["data_url"],
            WDI_ACCOUNT,
            account_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(account_values),
            "account proxy available; not payment-rail use",
            (
                f"{len(account_values)} roster economies have latest account-ownership values; "
                f"latest-year span {account_record['latest_year_span']}."
            ),
        ),
        source_row(
            "poverty_denominator",
            "World Bank WDI poverty headcount",
            poverty_record["data_url"],
            WDI_POVERTY,
            poverty_record["dmc_latest_rows"] > 0,
            len(ADB_NAMES),
            len(poverty_values),
            "source label corrected" if not poverty_line_mismatch else "source label mismatch documented",
            (
                f"Current WDI metadata name is '{poverty_record['indicator_name']}'. "
                + (
                    "The inherited program source label still says $2.15/day 2017 PPP."
                    if poverty_line_mismatch
                    else "The committed program source label now uses the same $3.00/day 2021 PPP definition."
                )
            ),
        ),
        source_row(
            "actual_shock_payment_delivery",
            "Shock-program registry x beneficiary payment delivery object",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            (
                "No emergency-transfer program registry, beneficiary roster, payment rail, "
                "delivery-speed record, or shock-event trigger is joined."
            ),
        ),
    ]

    summary = {
        "roster_n": len(ADB_NAMES),
        "old_value_ranked_rows": len(dropped.get("value_ranked_order", [])),
        "old_headline_five": HEADLINE_FIVE,
        "old_value_top5": old_value_top5,
        "old_excluded_for_missing_leg_count": dropped.get("excluded_for_missing_leg_count"),
        "all_sp_latest_rows": len(all_sp_values),
        "safety_net_latest_rows": len(safety_net_values),
        "account_latest_rows": len(account_values),
        "poverty_latest_rows": len(poverty_values),
        "poverty_gap_latest_rows": len(poverty_gap_values),
        "all_sp_live_top5": all_sp_live_top5,
        "safety_net_variant_top5": safety_top5,
        "safety_net_entered_vs_headline": entered_safety,
        "safety_net_dropped_vs_headline": dropped_safety,
        "safety_net_headline_overlap_count": overlap_safety_headline,
        "safety_net_top5_rows": safety_net_rows[:5],
        "poverty_indicator_current_name": poverty_record.get("indicator_name"),
        "poverty_indicator_old_source_label": old_source_name,
        "poverty_line_label_mismatch_detected": poverty_line_mismatch,
        "all_sp_indicator_name": all_sp_record.get("indicator_name"),
        "safety_net_indicator_name": safety_net_record.get("indicator_name"),
        "account_indicator_name": account_record.get("indicator_name"),
        "program_registry_join_built": False,
        "beneficiary_roster_join_built": False,
        "payment_rail_use_join_built": False,
        "delivery_speed_join_built": False,
        "shock_event_trigger_join_built": False,
        "analysis_ready_shock_payment_coverage": False,
        "owner_gated_or_unfinished_steps": [
            "The old coverage leg is all social protection and labor coverage, not emergency cash-transfer delivery.",
            "The social safety-net WDI leg is narrower but still a national coverage proxy, not a beneficiary payment record.",
            "Findex account ownership is account availability, not active payment-rail use or last-mile delivery.",
            "The WDI poverty indicator and committed program label now use $3.00/day 2021 PPP; earlier program prose used $2.15/day 2017 PPP.",
            "No emergency program registry, beneficiary roster, payment rail, delivery-speed record, or shock trigger is joined.",
        ],
    }

    readiness = {
        "program": "social-protection-shock-coverage",
        "analysis": "social-protection source-readiness and social safety-net rerank",
        "claim_scope": (
            "Public source audit for the shock-payment readiness screen. It checks the WDI indicator "
            "metadata, reruns a narrower social safety-net coverage variant, and records that actual "
            "shock-payment delivery objects remain unjoined. This is not a beneficiary-level payment "
            "coverage, delivery-speed, or adaptive-social-protection estimate."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
            "wdi_indicators": [WDI_ALL_SP, WDI_SAFETY_NET, WDI_ACCOUNT, WDI_POVERTY, WDI_POVERTY_GAP],
        },
        "summary": summary,
        "indicator_records": [all_sp_record, safety_net_record, account_record, poverty_record, poverty_gap_record],
        "source_rows": source_rows,
        "rerank_rows": rerank_rows,
        "variant_rows": {
            "all_sp_live": all_sp_rows,
            "social_safety_net": safety_net_rows,
        },
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(dropped)
    combined["analysis"] = "dropped-leg artifact plus source-readiness and social safety-net rerank"
    combined["social_protection_source_readiness"] = readiness
    combined["claim_scope"] = (
        f"{dropped.get('claim_scope', '')} The combined source audit documents that the old all-SP "
        "coverage leg is not a shock-payment delivery measure, reruns a narrower social safety-net "
        "variant, and keeps actual beneficiary payment delivery at source-readiness only."
    ).strip()
    combined["social_protection_data_wall"] = (
        "The old coverage leg is all social protection and labor coverage. A narrower WDI social "
        "safety-net leg is available and changes the diagnostic top five, but the repository still "
        "has no emergency-transfer program registry, beneficiary roster, payment-rail use table, "
        "delivery-speed record, or shock-event trigger. Current WDI poverty metadata labels "
        "SI.POV.DDAY as $3.00/day 2021 PPP; the earlier $2.15/day 2017 PPP program label has been corrected."
    )
    combined["generated_at"] = retrieved_at

    readiness_path = OUT / "social-protection-source-readiness.json"
    combined_path = OUT / "social-protection-dropped-leg-source-audit.json"
    rerank_csv = OUT / "social-protection-social-safety-net-rerank.csv"
    source_csv = OUT / "social-protection-source-readiness-sources.csv"

    readiness_path.write_text(json.dumps(readiness, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(rerank_csv, rerank_rows, list(rerank_rows[0].keys()))
    write_csv(source_csv, source_rows, list(source_rows[0].keys()))

    print("=== Social-protection source-readiness audit ===")
    print(f"Old value top 5: {old_value_top5}")
    print(f"Social safety-net variant top 5: {safety_top5}")
    print(f"Safety-net entered vs headline: {entered_safety}")
    print(f"Safety-net dropped vs headline: {dropped_safety}")
    print(f"Poverty metadata name: {poverty_record.get('indicator_name')}")
    print(f"Poverty label mismatch detected: {poverty_line_mismatch}")
    print(f"Analysis-ready shock-payment coverage: {summary['analysis_ready_shock_payment_coverage']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {rerank_csv}")
    print(f"Wrote {source_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
