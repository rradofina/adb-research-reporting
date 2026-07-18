"""Build the prospective WDI public-data freshness panel.

The frozen design is in ``public-data-freshness/pre-registration.md``. This
script does not choose indicators after seeing results. It retrieves the 27
frozen WDI series, preserves raw public responses in the Constitution §11
cache, and computes the calendar-age/source-relative decomposition for the
42-economy WDI-compatible ADB DMC roster.

Public data only. Missing values are never imputed. The output is a
measurement/coverage diagnostic, not a rating of an economy or statistical
office. attestation_chain: ai-first.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import statistics
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROGRAM = Path(__file__).resolve().parents[1]
ROOT = PROGRAM.parent
CACHE = ROOT / "luminosity-gap" / ".cache" / "research" / "public-data-freshness"
OUT = PROGRAM / "generated"
API = "https://api.worldbank.org/v2"
SNAPSHOT_YEAR = 2026
BASELINE_CAP = 2025
BASELINE_THRESHOLD = 3.0

ADB_DMCS = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan",
    "BGD": "Bangladesh", "BTN": "Bhutan", "BRN": "Brunei Darussalam",
    "KHM": "Cambodia", "CHN": "China, People's Republic of",
    "COK": "Cook Islands", "FJI": "Fiji", "GEO": "Georgia",
    "HKG": "Hong Kong, China", "IND": "India", "IDN": "Indonesia",
    "KAZ": "Kazakhstan", "KIR": "Kiribati", "KGZ": "Kyrgyz Republic",
    "LAO": "Lao People's Democratic Republic", "MYS": "Malaysia",
    "MDV": "Maldives", "MHL": "Marshall Islands",
    "FSM": "Micronesia, Federated States of", "MNG": "Mongolia",
    "MMR": "Myanmar", "NRU": "Nauru", "NPL": "Nepal",
    "PAK": "Pakistan", "PLW": "Palau", "PNG": "Papua New Guinea",
    "PHL": "Philippines", "WSM": "Samoa", "SLB": "Solomon Islands",
    "LKA": "Sri Lanka", "TJK": "Tajikistan", "THA": "Thailand",
    "TLS": "Timor-Leste", "TON": "Tonga", "TKM": "Turkmenistan",
    "TUV": "Tuvalu", "UZB": "Uzbekistan", "VUT": "Vanuatu",
    "VNM": "Viet Nam",
}

# Frozen descriptive coverage group. Papua New Guinea and Timor-Leste remain
# in the full DMC panel but are not classified as small-island economies here.
PACIFIC_SMALL_ISLAND = {
    "COK", "FJI", "KIR", "MHL", "FSM", "NRU",
    "PLW", "WSM", "SLB", "TON", "TUV", "VUT",
}

DOMAINS = [
    ("Demography", ["SP.POP.TOTL", "SP.DYN.LE00.IN", "SP.DYN.TFRT.IN"]),
    ("Poverty and inequality", ["SI.POV.DDAY", "SI.POV.NAHC", "SI.POV.GINI"]),
    ("Health", ["SH.XPD.CHEX.GD.ZS", "SH.DYN.MORT", "SH.STA.MMRT"]),
    ("Education", ["SE.PRM.ENRR", "SE.SEC.ENRR", "SE.ADT.LITR.ZS"]),
    ("Labor and social conditions", ["SL.UEM.TOTL.ZS", "SL.TLF.CACT.ZS", "SL.EMP.VULN.ZS"]),
    ("Infrastructure and digital access", ["EG.ELC.ACCS.ZS", "IT.NET.USER.ZS", "IT.CEL.SETS.P2"]),
    ("Environment and climate", ["EN.ATM.PM25.MC.M3", "AG.LND.FRST.ZS", "EN.ATM.CO2E.PC"]),
    ("Economy and structure", ["NY.GDP.MKTP.KD.ZG", "NV.AGR.TOTL.ZS", "FP.CPI.TOTL.ZG"]),
    ("External and public finance", ["BX.TRF.PWKR.DT.GD.ZS", "NE.TRD.GNFS.ZS", "GC.DOD.TOTL.GD.ZS"]),
]

CODE_TO_DOMAIN = {code: domain for domain, codes in DOMAINS for code in codes}
CODE_TO_POSITION = {code: position + 1 for _, codes in DOMAINS for position, code in enumerate(codes)}
ALL_CODES = [code for _, codes in DOMAINS for code in codes]

ADB_BASIC_STATS_CSV = "https://data.adb.org/media/15086/download"
ADB_BASIC_STATS_METADATA = "https://data.adb.org/dataset/basic-statistics-asia-and-pacific"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def cache_paths(name: str, suffix: str) -> tuple[Path, Path]:
    safe = name.replace("/", "_")
    return CACHE / f"{safe}.{suffix}.gz", CACHE / f"{safe}.provenance.json"


def read_cached(data_path: Path, provenance_path: Path) -> tuple[bytes, dict[str, Any]]:
    payload = gzip.decompress(data_path.read_bytes())
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if sha256_bytes(payload) != provenance["raw_sha256"]:
        raise ValueError(f"cache hash mismatch: {data_path}")
    return payload, provenance


def write_cache(
    data_path: Path,
    provenance_path: Path,
    payload: bytes,
    url: str,
    retrieved_at: str,
) -> dict[str, Any]:
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_bytes(gzip.compress(payload, compresslevel=9, mtime=0))
    provenance = {
        "url": url,
        "retrieved_at": retrieved_at,
        "raw_bytes": len(payload),
        "raw_sha256": sha256_bytes(payload),
        "compressed_bytes": data_path.stat().st_size,
        "compressed_sha256": sha256_bytes(data_path.read_bytes()),
        "attestation_chain": "ai-first",
    }
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return provenance


def fetch(
    name: str,
    url: str,
    suffix: str,
    refresh: bool,
    expect_json: bool,
) -> tuple[bytes, dict[str, Any]]:
    data_path, provenance_path = cache_paths(name, suffix)
    status = "cache"
    error = None
    payload: bytes
    provenance: dict[str, Any]
    if refresh or not (data_path.exists() and provenance_path.exists()):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "adb-research-factory/1.0 public-data-freshness"},
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = response.read()
            if expect_json:
                json.loads(payload)
            provenance = write_cache(data_path, provenance_path, payload, url, utc_now())
            status = "live"
        except Exception as exc:
            if not (data_path.exists() and provenance_path.exists()):
                raise
            payload, provenance = read_cached(data_path, provenance_path)
            status = "cache_fallback_after_fetch_error"
            error = f"{type(exc).__name__}: {exc}"
    else:
        payload, provenance = read_cached(data_path, provenance_path)

    record = {
        "name": name,
        "url": url,
        "cache_path": relative(data_path),
        "provenance_path": relative(provenance_path),
        "retrieved_at": provenance["retrieved_at"],
        "raw_bytes": provenance["raw_bytes"],
        "raw_sha256": provenance["raw_sha256"],
        "compressed_bytes": data_path.stat().st_size,
        "compressed_sha256": sha256_bytes(data_path.read_bytes()),
        "retrieval_status": status,
        "retrieval_error": error,
        "access": "public HTTPS; no authentication",
    }
    return payload, record


def fetch_wdi_code(code: str, refresh: bool) -> tuple[str, list[Any], list[Any], list[dict[str, Any]], str | None]:
    series_url = f"{API}/country/all/indicator/{code}?format=json&per_page=20000"
    meta_url = f"{API}/indicator/{code}?format=json"
    series_bytes, series_record = fetch(f"wdi-series-{code}", series_url, "json", refresh, True)
    meta_bytes, meta_record = fetch(f"wdi-metadata-{code}", meta_url, "json", refresh, True)
    series = json.loads(series_bytes)
    metadata = json.loads(meta_bytes)
    source_failure = None
    if not isinstance(series, list) or len(series) < 2 or not isinstance(series[1], list):
        source_failure = "WDI returned no observation table; the frozen code is unavailable or archived"
        series = [{}, []]
    if not isinstance(metadata, list) or len(metadata) < 2 or not isinstance(metadata[1], list):
        metadata = [{}, []]
        source_failure = (source_failure + "; " if source_failure else "") + "WDI returned no indicator metadata table"
    return code, series, metadata, [series_record, meta_record], source_failure


def numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def load_country_catalog(refresh: bool) -> tuple[set[str], dict[str, Any]]:
    url = f"{API}/country?format=json&per_page=400"
    payload, record = fetch("wdi-country-catalog", url, "json", refresh, True)
    obj = json.loads(payload)
    rows = obj[1] if isinstance(obj, list) and len(obj) > 1 else []
    # WDI aggregate rows have an empty region id. Country/economy rows do not.
    codes = {
        row.get("id") for row in rows
        if isinstance(row, dict)
        and row.get("id")
        and (row.get("region") or {}).get("id")
    }
    return codes, record


def parse_series(series: list[Any], valid_global_codes: set[str], cap: int) -> dict[str, Any]:
    rows = series[1]
    by_iso: dict[str, dict[int, float]] = defaultdict(dict)
    global_years: list[int] = []
    for row in rows:
        if not isinstance(row, dict) or not numeric(row.get("value")):
            continue
        try:
            year = int(row.get("date"))
        except (TypeError, ValueError):
            continue
        if year > cap:
            continue
        iso3 = row.get("countryiso3code")
        if iso3 in valid_global_codes:
            global_years.append(year)
        if iso3 in ADB_DMCS:
            by_iso[iso3][year] = float(row["value"])
    dmc_latest = {
        iso3: {"year": max(years), "value": years[max(years)]}
        for iso3, years in by_iso.items() if years
    }
    return {
        "global_frontier": max(global_years) if global_years else None,
        "dmc_frontier": max((v["year"] for v in dmc_latest.values()), default=None),
        "dmc_latest": dmc_latest,
    }


def metadata_fields(code: str, series: list[Any], metadata: list[Any]) -> dict[str, Any]:
    header = series[0] if series and isinstance(series[0], dict) else {}
    row = metadata[1][0] if len(metadata) > 1 and metadata[1] else {}
    return {
        "code": code,
        "name": row.get("name") or code,
        "source_id": (row.get("source") or {}).get("id"),
        "source_name": (row.get("source") or {}).get("value"),
        "source_note": row.get("sourceNote") or "",
        "source_organization": row.get("sourceOrganization") or "",
        "api_last_updated": header.get("lastupdated"),
    }


def selected_codes(set_size: int) -> list[str]:
    per_domain = {9: 1, 18: 2, 27: 3}[set_size]
    return [code for _, codes in DOMAINS for code in codes[:per_domain]]


def build_cells(
    parsed: dict[tuple[str, int], dict[str, Any]],
    metadata: dict[str, dict[str, Any]],
    source_by_code: dict[str, dict[str, Any]],
    codes: list[str],
    cap: int,
    threshold: float,
    frontier_mode: str,
) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    for code in codes:
        info = parsed[(code, cap)]
        frontier = info[f"{frontier_mode}_frontier"]
        for iso3, country in ADB_DMCS.items():
            observation = info["dmc_latest"].get(iso3)
            if observation is None or frontier is None:
                latest_year = value = calendar_age = relative_lag = production_age = None
                absolute_review = relative_review = disagreement = production_cycle_only = False
                missing = True
            else:
                latest_year = observation["year"]
                value = observation["value"]
                calendar_age = SNAPSHOT_YEAR - latest_year
                relative_lag = frontier - latest_year
                production_age = SNAPSHOT_YEAR - frontier
                absolute_review = calendar_age >= threshold
                relative_review = relative_lag >= threshold
                disagreement = absolute_review != relative_review
                production_cycle_only = absolute_review and not relative_review
                missing = False
                if calendar_age != production_age + relative_lag:
                    raise AssertionError(f"clock identity failed for {iso3} {code}")
            source = source_by_code[code]
            cells.append({
                "iso3": iso3,
                "country": country,
                "pacific_small_island": iso3 in PACIFIC_SMALL_ISLAND,
                "indicator_code": code,
                "indicator_name": metadata[code]["name"],
                "domain": CODE_TO_DOMAIN[code],
                "indicator_position": CODE_TO_POSITION[code],
                "reference_cap": cap,
                "frontier_mode": frontier_mode,
                "review_threshold_years": threshold,
                "latest_year": latest_year,
                "value": value,
                "frontier_year": frontier,
                "calendar_age_years": calendar_age,
                "production_age_years": production_age,
                "relative_lag_years": relative_lag,
                "missing": missing,
                "absolute_review": absolute_review,
                "relative_review": relative_review,
                "classification_disagreement": disagreement,
                "production_cycle_only": production_cycle_only,
                "retrieved_at": source["retrieved_at"],
                "response_sha256": source["raw_sha256"],
                "api_last_updated": metadata[code]["api_last_updated"],
                "attestation_chain": "ai-first",
            })
    return cells


def share(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def quantile(values: list[int | float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(float(v) for v in values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def summarize(cells: list[dict[str, Any]]) -> dict[str, Any]:
    observed = [row for row in cells if not row["missing"]]
    absolute = [row for row in observed if row["absolute_review"]]
    relative = [row for row in observed if row["relative_review"]]
    disagree = [row for row in observed if row["classification_disagreement"]]
    production_only = [row for row in observed if row["production_cycle_only"]]
    summary: dict[str, Any] = {
        "possible_cells": len(cells),
        "observed_cells": len(observed),
        "missing_cells": len(cells) - len(observed),
        "observed_share": share(len(observed), len(cells)),
        "missing_share": share(len(cells) - len(observed), len(cells)),
        "absolute_review_cells": len(absolute),
        "relative_review_cells": len(relative),
        "disagreement_cells": len(disagree),
        "production_cycle_only_cells": len(production_only),
        "absolute_review_share_observed": share(len(absolute), len(observed)),
        "relative_review_share_observed": share(len(relative), len(observed)),
        "disagreement_share_observed": share(len(disagree), len(observed)),
        "production_cycle_only_share_absolute": share(len(production_only), len(absolute)),
    }
    for field in ("calendar_age_years", "production_age_years", "relative_lag_years"):
        values = [row[field] for row in observed if row[field] is not None]
        summary[f"{field}_median"] = statistics.median(values) if values else None
        summary[f"{field}_q1"] = quantile(values, 0.25)
        summary[f"{field}_q3"] = quantile(values, 0.75)
    return summary


def grouped_summary(cells: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in cells:
        groups[str(row[field])].append(row)
    output = []
    for group, rows in sorted(groups.items()):
        output.append({field: group, **summarize(rows)})
    return output


def sensitivity_runs(
    parsed: dict[tuple[str, int], dict[str, Any]],
    metadata: dict[str, dict[str, Any]],
    source_by_code: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []

    def add_run(name: str, size: int, threshold: float, cap: int, frontier: str, omit_domain: str | None = None) -> None:
        codes = selected_codes(size)
        if omit_domain:
            codes = [code for code in codes if CODE_TO_DOMAIN[code] != omit_domain]
        cells = build_cells(parsed, metadata, source_by_code, codes, cap, threshold, frontier)
        runs.append({
            "run": name,
            "indicator_set_size": len(codes),
            "frozen_set_label": size,
            "threshold_literal_years": threshold,
            "threshold_effective_integer_years": math.ceil(threshold),
            "reference_cap": cap,
            "frontier_mode": frontier,
            "omitted_domain": omit_domain,
            **summarize(cells),
        })

    for size in (9, 18, 27):
        add_run(f"set_{size}", size, BASELINE_THRESHOLD, BASELINE_CAP, "global")
    for threshold in (1.5, 3.0, 4.5):
        add_run(f"threshold_{threshold:g}", 18, threshold, BASELINE_CAP, "global")
    for frontier in ("global", "dmc"):
        add_run(f"frontier_{frontier}", 18, BASELINE_THRESHOLD, BASELINE_CAP, frontier)
    for cap in (2025, 2024):
        add_run(f"cap_{cap}", 18, BASELINE_THRESHOLD, cap, "global")
    for domain, _ in DOMAINS:
        add_run(f"leave_out_{domain}", 18, BASELINE_THRESHOLD, BASELINE_CAP, "global", domain)
    return runs


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cache_manifest() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(CACHE.glob("*")):
        if path.is_file():
            rows.append({
                "sha256": sha256_bytes(path.read_bytes()),
                "bytes": path.stat().st_size,
                "path": relative(path),
            })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="redownload public sources")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    valid_global_codes, country_record = load_country_catalog(args.refresh)
    source_inventory: list[dict[str, Any]] = [country_record]
    series_by_code: dict[str, list[Any]] = {}
    metadata_payload_by_code: dict[str, list[Any]] = {}
    failures: list[dict[str, str]] = []

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch_wdi_code, code, args.refresh): code for code in ALL_CODES}
        for future in as_completed(futures):
            code = futures[future]
            try:
                result_code, series, metadata_payload, records, source_failure = future.result()
                series_by_code[result_code] = series
                metadata_payload_by_code[result_code] = metadata_payload
                source_inventory.extend(records)
                if source_failure:
                    failures.append({"code": result_code, "error": source_failure})
                    print(f"SOURCE FAILURE {result_code}: {source_failure}")
                else:
                    print(f"fetched {result_code}")
            except Exception as exc:
                failures.append({"code": code, "error": f"{type(exc).__name__}: {exc}"})
                print(f"FAILED {code}: {exc}")

    # Both ADB URLs returned a Cloudflare challenge to the non-interactive
    # client on 2026-07-19. CLAUDE.md names that as a hard access wall, so the
    # script records it and does not make a third automated pass. These objects
    # frame relevance/licensing only and do not contribute panel values.
    for name, url in (
        ("adb-basic-statistics-2026", ADB_BASIC_STATS_CSV),
        ("adb-basic-statistics-metadata", ADB_BASIC_STATS_METADATA),
    ):
        source_inventory.append({
            "name": name,
            "url": url,
            "cache_path": None,
            "provenance_path": None,
            "retrieved_at": None,
            "raw_bytes": None,
            "raw_sha256": None,
            "compressed_bytes": None,
            "compressed_sha256": None,
            "retrieval_status": "access_blocked_cloudflare_challenge_2026-07-19",
            "retrieval_error": "HTTP 403 with Cf-Mitigated: challenge; no bypass attempted",
            "access": "public page; automated retrieval blocked",
            "role": "policy-domain and licensing context; not an empirical panel input",
        })

    if failures:
        write_json(OUT / "retrieval-failures.json", {"failures": failures, "generated_at": utc_now()})
    if len(series_by_code) != len(ALL_CODES):
        raise RuntimeError(f"received {len(series_by_code)}/{len(ALL_CODES)} frozen indicator responses")

    metadata = {
        code: metadata_fields(code, series_by_code[code], metadata_payload_by_code[code])
        for code in ALL_CODES
    }
    source_by_code = {
        code: next(row for row in source_inventory if row["name"] == f"wdi-series-{code}")
        for code in ALL_CODES
    }
    parsed = {
        (code, cap): parse_series(series_by_code[code], valid_global_codes, cap)
        for code in ALL_CODES for cap in (2024, 2025)
    }

    baseline_cells = build_cells(
        parsed, metadata, source_by_code, selected_codes(18),
        BASELINE_CAP, BASELINE_THRESHOLD, "global",
    )
    all_cells = build_cells(
        parsed, metadata, source_by_code, selected_codes(27),
        BASELINE_CAP, BASELINE_THRESHOLD, "global",
    )
    sensitivity = sensitivity_runs(parsed, metadata, source_by_code)
    baseline_summary = summarize(baseline_cells)
    run_by_name = {row["run"]: row for row in sensitivity}
    set_results = [run_by_name[f"set_{size}"]["disagreement_share_observed"] for size in (9, 18, 27)]
    leave_out_runs = [row for row in sensitivity if row["run"].startswith("leave_out_")]
    leave_out_min = min(
        (row["disagreement_share_observed"] for row in leave_out_runs if row["disagreement_share_observed"] is not None),
        default=None,
    )
    threshold_pass = 0.10
    primary_pass = baseline_summary["disagreement_share_observed"] is not None and baseline_summary["disagreement_share_observed"] >= threshold_pass
    all_sets_pass = all(value is not None and value >= threshold_pass for value in set_results)
    coverage_pass = baseline_summary["observed_share"] is not None and baseline_summary["observed_share"] >= 0.50
    single_domain_dependence = leave_out_min is not None and leave_out_min < threshold_pass
    if primary_pass and all_sets_pass and coverage_pass and not single_domain_dependence:
        decision = "advance_broad_cross_domain_claim"
    elif primary_pass and all_sets_pass and coverage_pass and single_domain_dependence:
        decision = "reshape_to_domain_concentrated_claim"
    else:
        decision = "retract_primary_or_reshape_to_coverage"

    indicator_summary = grouped_summary(all_cells, "indicator_code")
    for row in indicator_summary:
        code = row["indicator_code"]
        row.update({
            "indicator_name": metadata[code]["name"],
            "domain": CODE_TO_DOMAIN[code],
            "global_frontier_2025": parsed[(code, 2025)]["global_frontier"],
            "dmc_frontier_2025": parsed[(code, 2025)]["dmc_frontier"],
            "api_last_updated": metadata[code]["api_last_updated"],
        })
    domain_summary = grouped_summary(baseline_cells, "domain")
    coverage_groups = grouped_summary(baseline_cells, "pacific_small_island")

    summary = {
        "program": "public-data-freshness",
        "attestation_chain": "ai-first",
        "generated_at": utc_now(),
        "freeze_commit": "fc9f170",
        "snapshot_year": SNAPSHOT_YEAR,
        "reference_cap": BASELINE_CAP,
        "roster_n": len(ADB_DMCS),
        "indicator_counts": {"lower": 9, "baseline": 18, "upper": 27},
        "retrieved_indicator_response_count": len(series_by_code),
        "valid_indicator_count": len(ALL_CODES) - len({row["code"] for row in failures}),
        "retrieval_failures": failures,
        "primary": baseline_summary,
        "decision_gate": {
            "required_disagreement_share": threshold_pass,
            "set_disagreement_shares_9_18_27": set_results,
            "primary_pass": primary_pass,
            "all_set_sizes_pass": all_sets_pass,
            "minimum_coverage_pass": coverage_pass,
            "leave_one_domain_out_minimum": leave_out_min,
            "single_domain_dependence": single_domain_dependence,
            "decision": decision,
        },
        "non_claim": (
            "This is an economy-by-indicator measurement and coverage diagnostic. "
            "It is not a rating of an economy, statistical office, data quality, "
            "or formal dissemination timeliness."
        ),
    }

    panel_payload = {
        "summary": summary,
        "metadata": [metadata[code] | {"domain": CODE_TO_DOMAIN[code], "position": CODE_TO_POSITION[code]} for code in ALL_CODES],
        "rows": all_cells,
    }
    write_csv(OUT / "freshness-panel.csv", all_cells)
    write_json(OUT / "freshness-panel.json", panel_payload)
    write_json(OUT / "freshness-summary.json", summary)
    write_csv(OUT / "freshness-sensitivity.csv", sensitivity)
    write_json(OUT / "freshness-sensitivity.json", {"runs": sensitivity, "generated_at": summary["generated_at"]})
    write_csv(OUT / "freshness-indicator-summary.csv", indicator_summary)
    write_csv(OUT / "freshness-domain-summary.csv", domain_summary)
    write_csv(OUT / "freshness-coverage-groups.csv", coverage_groups)
    write_json(OUT / "freshness-source-inventory.json", {
        "sources": sorted(source_inventory, key=lambda row: row["name"]),
        "indicator_metadata": [metadata[code] for code in ALL_CODES],
        "generated_at": summary["generated_at"],
        "attestation_chain": "ai-first",
    })
    manifest_rows = cache_manifest()
    write_csv(OUT / "freshness-cache-manifest.csv", manifest_rows)
    (OUT / "freshness-cache-manifest.sha256").write_text(
        "".join(f"{row['sha256']} *{row['path']}\n" for row in manifest_rows),
        encoding="utf-8",
    )

    print(json.dumps(summary["primary"], indent=2))
    print(json.dumps(summary["decision_gate"], indent=2))
    print(f"wrote {len(all_cells)} cells and {len(sensitivity)} sensitivity runs")


if __name__ == "__main__":
    main()
