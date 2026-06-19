"""Climate-health workdays labor-denominator and heat-source audit.

The existing deepening proves a construct problem: at the tighter PM2.5 cap,
the workday-loss proxy drifts toward an outdoor-labor-share ranking. This
script adds the source repair for the other exposed-count problem:

  published exposed outdoor = outdoor employment share x total population

WDI employment shares are shares of total employment, and WDI employment-to-
population is a 15+ ratio. The observed repair therefore uses public WDI
employment-to-population, total population, and population ages 0-14 share to
derive employed 15+ persons before applying the already committed outdoor
employment share.

The script also checks whether the public CCKP national tasmax route is
reachable for the rankable DMCs. That is source readiness only: it does not
join gridded heat, worker locations, hours, occupations, WBGT, or observed
lost workdays.

Raw public responses are cached under .cache/labor-heat-source-readiness/
with SHA-256 hashes. Public data only. attestation_chain: ai-first.
"""

import csv
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CACHE = BASE / ".cache" / "labor-heat-source-readiness"
OUT = BASE / "generated"
DEEPENING_PATH = OUT / "climate-health-workdays-deepening.json"

WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
PER_PAGE = 20000
WDI_INDICATORS = {
    "SL.EMP.TOTL.SP.ZS": "Employment to population ratio, 15+, total (%)",
    "SP.POP.TOTL": "Population, total",
    "SP.POP.0014.TO.ZS": "Population ages 0-14 (% of total population)",
}
CCKP_API_BASE = "https://cckpapi.worldbank.org/cckp/v1"
CCKP_BASELINE_PERIOD = "1995-2014"
CCKP_FUTURE_PERIOD = "2040-2059"
CCKP_FUTURE_SCENARIO = "ssp245"


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


def round_or_none(value, digits=1):
    if value is None:
        return None
    return round(value, digits)


def fetch_bytes(url, cache_path, headers=None):
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    request_headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "adb-research-factory/1.0",
    }
    if headers:
        request_headers.update(headers)
    try:
        request = urllib.request.Request(url, headers=request_headers)
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


def fetch_json(url, cache_path, headers=None):
    raw, record = fetch_bytes(url, cache_path, headers=headers)
    try:
        return json.loads(raw.decode("utf-8-sig")), record
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse JSON from {url}: {exc}") from exc


def unwrap_world_bank_rows(payload):
    if isinstance(payload, list) and len(payload) >= 2 and isinstance(payload[1], list):
        return payload[1]
    return []


def latest_wdi_values(payload, iso_set):
    latest = {}
    observations = 0
    for row in unwrap_world_bank_rows(payload):
        if not isinstance(row, dict):
            continue
        iso = row.get("countryiso3code")
        value = row.get("value")
        if iso not in iso_set or not isinstance(value, (int, float)):
            continue
        observations += 1
        year = int(row.get("date"))
        if iso not in latest or year > latest[iso]["year"]:
            latest[iso] = {
                "iso3": iso,
                "year": year,
                "value": float(value),
                "indicator": row.get("indicator", {}).get("id"),
                "indicator_name": row.get("indicator", {}).get("value"),
                "country_name_wdi": row.get("country", {}).get("value"),
            }
    return latest, observations


def wdi_country_url(countries, indicator_id):
    country_part = ";".join(sorted(countries))
    return (
        f"{WORLD_BANK_API_BASE}/country/{country_part}/indicator/{indicator_id}"
        f"?format=json&per_page={PER_PAGE}"
    )


def fetch_wdi_indicator(countries, indicator_id, cache_records):
    data_url = wdi_country_url(countries, indicator_id)
    metadata_url = f"{WORLD_BANK_API_BASE}/indicator/{indicator_id}?format=json"
    slug = slugify(indicator_id)
    data_payload, data_record = fetch_json(data_url, CACHE / f"wdi_{slug}_rankable.json")
    metadata_payload, metadata_record = fetch_json(metadata_url, CACHE / f"wdi_{slug}_metadata.json")
    latest, observations = latest_wdi_values(data_payload, set(countries))
    metadata_rows = unwrap_world_bank_rows(metadata_payload)
    metadata = metadata_rows[0] if metadata_rows else {}
    meta = data_payload[0] if isinstance(data_payload, list) and data_payload else {}
    record = {
        "indicator_id": indicator_id,
        "indicator_name": metadata.get("name") or WDI_INDICATORS[indicator_id],
        "data_url": data_url,
        "metadata_url": metadata_url,
        "rankable_dmcs_with_latest_value": len(latest),
        "rankable_observations": observations,
        "world_bank_lastupdated": meta.get("lastupdated"),
        "data_sha256": data_record["sha256"],
        "metadata_sha256": metadata_record["sha256"],
        "data_fetch_mode": data_record["fetch_mode"],
        "metadata_fetch_mode": metadata_record["fetch_mode"],
    }
    cache_records.append({**data_record, "query_type": "wdi_indicator_data", "indicator_id": indicator_id})
    cache_records.append({**metadata_record, "query_type": "wdi_indicator_metadata", "indicator_id": indicator_id})
    return latest, record


def cckp_url(iso3, period, scenario):
    return (
        f"{CCKP_API_BASE}/cmip6-x0.25_climatology_tasmax_climatology_annual_"
        f"{period}_median_{scenario}_ensemble_all_mean/{iso3}?format=json"
    )


def parse_cckp_value(payload, iso3):
    data = payload.get("data") if isinstance(payload, dict) else None
    country_data = data.get(iso3) if isinstance(data, dict) else None
    if not isinstance(country_data, dict):
        return None, None
    for period_key, value in country_data.items():
        if isinstance(value, (int, float)):
            return period_key, float(value)
    return None, None


def fetch_cckp_tasmax(iso3, period, scenario, cache_records):
    url = cckp_url(iso3, period, scenario)
    cache_name = f"cckp_tasmax_{period}_{scenario}_{iso3}.json"
    payload, record = fetch_json(
        url,
        CACHE / cache_name,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://climateknowledgeportal.worldbank.org/",
        },
    )
    key, value = parse_cckp_value(payload, iso3)
    cache_records.append({
        **record,
        "query_type": "cckp_tasmax_climatology",
        "iso3": iso3,
        "period": period,
        "scenario": scenario,
        "value_key": key,
    })
    return {
        "url": url,
        "period": period,
        "scenario": scenario,
        "value_key": key,
        "tasmax_c": value,
        "sha256": record["sha256"],
        "fetch_mode": record["fetch_mode"],
        "status_code": record["status_code"],
    }


def load_deepening():
    if not DEEPENING_PATH.exists():
        raise FileNotFoundError(
            f"{DEEPENING_PATH} missing. Run climate-health-workdays/scripts/deepen-cap-and-laborforce.py first."
        )
    return json.loads(DEEPENING_PATH.read_text(encoding="utf-8"))


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


def years_span(values):
    years = sorted({int(v["year"]) for v in values if v and isinstance(v.get("year"), int)})
    if not years:
        return None
    if years[0] == years[-1]:
        return str(years[0])
    return f"{years[0]}-{years[-1]}"


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    retrieved_at = utc_stamp()
    deepening = load_deepening()
    cap = deepening.get("cap_saturation", {})
    cap_rows = cap.get("rows", [])
    rankable_rows = [row for row in cap_rows if row.get("iso3")]
    rankable_isos = sorted({row["iso3"] for row in rankable_rows})

    cache_records = []
    indicator_records = []
    wdi_latest = {}
    for indicator_id in WDI_INDICATORS:
        latest, record = fetch_wdi_indicator(rankable_isos, indicator_id, cache_records)
        wdi_latest[indicator_id] = latest
        indicator_records.append(record)

    denominator_rows = []
    cckp_success_baseline = 0
    cckp_success_future = 0
    cckp_success_both = 0

    for row in rankable_rows:
        iso = row["iso3"]
        emp = wdi_latest["SL.EMP.TOTL.SP.ZS"].get(iso)
        pop = wdi_latest["SP.POP.TOTL"].get(iso)
        age = wdi_latest["SP.POP.0014.TO.ZS"].get(iso)
        baseline = fetch_cckp_tasmax(iso, CCKP_BASELINE_PERIOD, "historical", cache_records)
        future = fetch_cckp_tasmax(iso, CCKP_FUTURE_PERIOD, CCKP_FUTURE_SCENARIO, cache_records)

        if baseline["tasmax_c"] is not None:
            cckp_success_baseline += 1
        if future["tasmax_c"] is not None:
            cckp_success_future += 1
        if baseline["tasmax_c"] is not None and future["tasmax_c"] is not None:
            cckp_success_both += 1

        population_total = pop["value"] if pop else None
        pop_0_14_pct = age["value"] if age else None
        emp_to_pop_pct = emp["value"] if emp else None
        outdoor_share = row.get("outdoor_labor_share_pct")
        published_value = row.get("published_exposed_outdoor_millions_x_total_pop")
        if published_value is None:
            published_value = next(
                (
                    lab.get("published_exposed_outdoor_millions_x_total_pop")
                    for lab in deepening.get("denominator_correction", {}).get("rows", [])
                    if lab.get("iso3") == iso
                ),
                None,
            )
        if (
            published_value is None
            and population_total is not None
            and isinstance(outdoor_share, (int, float))
        ):
            published_value = (population_total * (outdoor_share / 100.0)) / 1_000_000.0
        population_15plus_m = None
        employed_15plus_m = None
        observed_exposed_m = None
        ratio = None
        difference = None
        if (
            population_total is not None
            and pop_0_14_pct is not None
            and emp_to_pop_pct is not None
            and isinstance(outdoor_share, (int, float))
        ):
            population_15plus_m = (population_total * (1 - pop_0_14_pct / 100.0)) / 1_000_000.0
            employed_15plus_m = population_15plus_m * (emp_to_pop_pct / 100.0)
            observed_exposed_m = employed_15plus_m * (outdoor_share / 100.0)
            if published_value is not None and observed_exposed_m:
                ratio = published_value / observed_exposed_m
                difference = published_value - observed_exposed_m

        denominator_rows.append({
            "iso3": iso,
            "country": row.get("country"),
            "rank_cap45": row.get("rank_cap45"),
            "rank_cap22_5": row.get("rank_cap22_5"),
            "rank_labor": row.get("rank_labor"),
            "pm25_ugm3": round_or_none(row.get("pm25_ugm3"), 2),
            "outdoor_labor_share_pct": round_or_none(outdoor_share, 1),
            "published_exposed_outdoor_millions_x_total_pop": round_or_none(published_value, 1),
            "wdi_population_total": round_or_none(population_total, 0),
            "wdi_population_total_year": pop["year"] if pop else None,
            "wdi_pop_0_14_pct": round_or_none(pop_0_14_pct, 2),
            "wdi_pop_0_14_year": age["year"] if age else None,
            "population_15plus_millions": round_or_none(population_15plus_m, 2),
            "employment_to_population_15plus_pct": round_or_none(emp_to_pop_pct, 2),
            "employment_to_population_year": emp["year"] if emp else None,
            "observed_employed_15plus_millions": round_or_none(employed_15plus_m, 2),
            "observed_exposed_outdoor_worker_millions": round_or_none(observed_exposed_m, 2),
            "published_to_observed_worker_ratio": round_or_none(ratio, 2),
            "difference_millions_published_minus_observed": round_or_none(difference, 2),
            "baseline_tasmax_1995_2014_c": round_or_none(baseline["tasmax_c"], 2),
            "baseline_tasmax_value_key": baseline["value_key"],
            "future_tasmax_2040_2059_ssp245_c": round_or_none(future["tasmax_c"], 2),
            "future_tasmax_value_key": future["value_key"],
            "tasmax_delta_c": round_or_none(
                future["tasmax_c"] - baseline["tasmax_c"]
                if future["tasmax_c"] is not None and baseline["tasmax_c"] is not None
                else None,
                2,
            ),
            "denominator_status": (
                "observed WDI denominator joined"
                if observed_exposed_m is not None
                else "missing one or more WDI denominator fields"
            ),
            "heat_source_status": (
                "national CCKP tasmax visible; no worker heat-exposure join"
                if baseline["tasmax_c"] is not None and future["tasmax_c"] is not None
                else "CCKP tasmax incomplete for this row"
            ),
            "cckp_baseline_url": baseline["url"],
            "cckp_future_url": future["url"],
        })

    top3_isos = set((cap.get("ranking_cap45") or [])[:3])
    top3_rows = [row for row in denominator_rows if row["iso3"] in top3_isos]
    top3_rows.sort(key=lambda r: r["rank_cap45"] or 999)
    joined_denominator_rows = [
        row for row in denominator_rows
        if row["observed_exposed_outdoor_worker_millions"] is not None
    ]
    ratios = [
        row["published_to_observed_worker_ratio"]
        for row in joined_denominator_rows
        if isinstance(row["published_to_observed_worker_ratio"], (int, float))
    ]
    deltas = [
        row["tasmax_delta_c"]
        for row in denominator_rows
        if isinstance(row["tasmax_delta_c"], (int, float))
    ]
    india = next((row for row in denominator_rows if row["iso3"] == "IND"), {})

    source_rows = [
        source_row(
            "labor_denominator",
            "World Bank WDI employment-to-population, population, and ages 0-14 indicators",
            f"{WORLD_BANK_API_BASE}/",
            "SL.EMP.TOTL.SP.ZS; SP.POP.TOTL; SP.POP.0014.TO.ZS",
            all(record["rankable_dmcs_with_latest_value"] > 0 for record in indicator_records),
            len(rankable_isos),
            len(joined_denominator_rows),
            "joined into observed denominator repair",
            (
                f"{len(joined_denominator_rows)} of {len(rankable_isos)} rankable DMCs have the three "
                "public WDI fields needed to derive employed 15+ persons before applying the outdoor share."
            ),
        ),
        source_row(
            "national_heat_source",
            "World Bank CCKP CMIP6 national tasmax climatology",
            CCKP_API_BASE,
            "tasmax 1995-2014 historical and 2040-2059 SSP2-4.5",
            cckp_success_baseline > 0 or cckp_success_future > 0,
            len(rankable_isos) * 2,
            cckp_success_baseline + cckp_success_future,
            "source visible; not joined to workers or work hours",
            (
                f"Baseline tasmax values were parsed for {cckp_success_baseline} rankable DMCs and "
                f"future SSP2-4.5 tasmax values for {cckp_success_future}; this is country-level source "
                "readiness, not worker heat exposure."
            ),
        ),
        source_row(
            "worker_heat_join",
            "Worker location x heat x work-hours exposure object",
            "",
            "not_computed",
            False,
            0,
            0,
            "not joined",
            (
                "No gridded heat or WBGT, worker-location surface, sectoral work-hours schedule, "
                "or observed lost-workday outcome is joined."
            ),
        ),
    ]

    summary = {
        "rankable_dmcs": len(rankable_isos),
        "wdi_denominator_indicators_queried": len(WDI_INDICATORS),
        "wdi_denominator_rows_joined": len(joined_denominator_rows),
        "wdi_employment_to_population_latest_year_span": years_span(wdi_latest["SL.EMP.TOTL.SP.ZS"].values()),
        "wdi_population_latest_year_span": years_span(wdi_latest["SP.POP.TOTL"].values()),
        "wdi_pop_0_14_latest_year_span": years_span(wdi_latest["SP.POP.0014.TO.ZS"].values()),
        "top3_denominator_rows_joined": sum(
            1 for row in top3_rows if row["observed_exposed_outdoor_worker_millions"] is not None
        ),
        "india_published_exposed_outdoor_millions_x_total_pop": india.get("published_exposed_outdoor_millions_x_total_pop"),
        "india_observed_employed_15plus_millions": india.get("observed_employed_15plus_millions"),
        "india_observed_exposed_outdoor_worker_millions": india.get("observed_exposed_outdoor_worker_millions"),
        "india_published_to_observed_worker_ratio": india.get("published_to_observed_worker_ratio"),
        "india_denominator_difference_millions": india.get("difference_millions_published_minus_observed"),
        "published_to_observed_worker_ratio_min": round_or_none(min(ratios), 2) if ratios else None,
        "published_to_observed_worker_ratio_max": round_or_none(max(ratios), 2) if ratios else None,
        "cckp_baseline_tasmax_rows": cckp_success_baseline,
        "cckp_future_tasmax_rows": cckp_success_future,
        "cckp_baseline_and_future_rows": cckp_success_both,
        "cckp_tasmax_delta_min_c": round_or_none(min(deltas), 2) if deltas else None,
        "cckp_tasmax_delta_max_c": round_or_none(max(deltas), 2) if deltas else None,
        "worker_heat_exposure_join_built": False,
        "work_hours_join_built": False,
        "wbgt_or_heat_stress_metric_built": False,
        "causal_workday_loss_estimate_built": False,
        "analysis_ready_heat_workday_loss": False,
        "owner_gated_or_unfinished_steps": [
            "The observed denominator repair now uses public WDI population, ages 0-14 share, and employment-to-population 15+ fields.",
            "The CCKP national tasmax route is visible, but country means are not gridded worker exposure.",
            "No WBGT, hours-worked, occupation schedule, subnational labor denominator, or observed lost-workday outcome is joined.",
            "The PM2.5 cap-saturation finding remains a measurement caution, not a health-impact estimate.",
        ],
    }

    readiness = {
        "program": "climate-health-workdays",
        "analysis": "observed labor-denominator repair and heat-source readiness",
        "claim_scope": (
            "Public source audit for the climate-health workday proxy. It repairs the exposed-worker "
            "denominator with observed WDI fields and verifies a public CCKP national tasmax route, "
            "but it does not estimate heat exposure, worker lost workdays, or causal health impacts."
        ),
        "retrieved_at": retrieved_at,
        "sources": {
            "world_bank_wdi_api_base": WORLD_BANK_API_BASE,
            "wdi_indicators": list(WDI_INDICATORS.keys()),
            "world_bank_cckp_api_base": CCKP_API_BASE,
            "cckp_baseline_period": CCKP_BASELINE_PERIOD,
            "cckp_future_period": CCKP_FUTURE_PERIOD,
            "cckp_future_scenario": CCKP_FUTURE_SCENARIO,
        },
        "summary": summary,
        "indicator_records": indicator_records,
        "source_rows": source_rows,
        "denominator_rows": denominator_rows,
        "top3_observed_denominator_rows": top3_rows,
        "cache_records": cache_records,
        "attestation_chain": "ai-first",
        "generated_at": retrieved_at,
    }

    combined = dict(deepening)
    combined["analysis"] = "cap-saturation plus observed labor-denominator and heat-source readiness audit"
    combined["labor_heat_source_readiness"] = readiness
    combined["denominator_correction_observed"] = {
        "wall_note": (
            "The previous assumed 0.40/0.50/0.60 employment-to-population band is superseded here. "
            "This combined artifact fetches public WDI SL.EMP.TOTL.SP.ZS, SP.POP.TOTL, and "
            "SP.POP.0014.TO.ZS, derives population 15+, and then applies the committed outdoor "
            "employment share to observed employed 15+ persons."
        ),
        "rows": denominator_rows,
        "top3_rows": top3_rows,
    }
    if isinstance(combined.get("denominator_correction"), dict):
        combined["denominator_correction"] = dict(combined["denominator_correction"])
        combined["denominator_correction"]["wall_note"] = (
            "Superseded in this combined artifact by denominator_correction_observed, which uses "
            "public WDI employment-to-population 15+, total population, and ages 0-14 share."
        )
    combined["climate_health_data_wall"] = (
        "The denominator repair now uses observed public WDI employment-to-population 15+, total "
        "population, and ages 0-14 share for rankable rows. Public CCKP national tasmax values are "
        "reachable, but the artifact still has no gridded worker heat exposure, work-hours schedule, "
        "WBGT/heat-stress metric, or observed lost-workday outcome."
    )
    combined["claim_scope"] = (
        f"{deepening.get('claim_scope', '')} The combined source audit supersedes the old assumed "
        "employment-to-population band with observed WDI denominator fields and keeps the CCKP "
        "tasmax layer at source-readiness only."
    ).strip()
    combined["generated_at"] = retrieved_at

    readiness_path = OUT / "climate-health-labor-heat-source-readiness.json"
    combined_path = OUT / "climate-health-workdays-denominator-source-audit.json"
    denominator_csv = OUT / "climate-health-labor-denominator-observed.csv"
    source_csv = OUT / "climate-health-labor-heat-source-readiness-sources.csv"

    readiness_path.write_text(json.dumps(readiness, indent=2, ensure_ascii=False), encoding="utf-8")
    combined_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(denominator_csv, denominator_rows, list(denominator_rows[0].keys()))
    write_csv(source_csv, source_rows, list(source_rows[0].keys()))

    print("=== Climate-health labor/heat source-readiness audit ===")
    print(f"Rankable DMCs: {summary['rankable_dmcs']}")
    print(f"WDI denominator rows joined: {summary['wdi_denominator_rows_joined']}")
    print(
        "India published/observed exposed-worker ratio: "
        f"{summary['india_published_to_observed_worker_ratio']}"
    )
    print(f"CCKP baseline/future rows: {cckp_success_baseline}/{cckp_success_future}")
    print(f"Analysis-ready heat workday loss: {summary['analysis_ready_heat_workday_loss']}")
    print(f"Wrote {combined_path}")
    print(f"Wrote {denominator_csv}")
    print(f"Wrote {source_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
