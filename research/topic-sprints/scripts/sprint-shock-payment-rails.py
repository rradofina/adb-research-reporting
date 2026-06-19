"""L2 hook sprint: shock exposure versus payment-use rails.

This is exploratory new-topic triage, not a promoted program claim.

Question:
    Do public sources show DMCs where disaster exposure is visible, but the
    payment-use rails needed for post-shock delivery are weaker or differently
    measured than headline account ownership suggests?

Public inputs:
    - Existing repo panel from World Bank ASPIRE, Global Findex, and WDI
      poverty data.
    - Existing repo panel from EM-DAT country profiles via the HDX mirror.
    - World Bank API payment-use indicators from Global Financial Development,
      G20 Financial Inclusion Indicators, and WDI/Findex.

Outputs:
    - research/topic-sprints/generated/shock-payment-rails-sprint.csv
    - research/topic-sprints/generated/shock-payment-rails-sprint.json
    - research/topic-sprints/generated/charts/shock-payment-rails-scatter.png
    - research/topic-sprints/generated/charts/shock-payment-rails-scatter.svg

attestation_chain: ai-first
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
CACHE = BASE / ".cache"
OUT = BASE / "generated"
CHARTS = OUT / "charts"
CACHE.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

SOCIAL_PANEL = ROOT / "social-protection-shock-coverage" / "generated" / "social-protection-adb-panel.json"
DISASTER_PANEL = ROOT / "disaster-recovery-lag" / "generated" / "disaster-recovery-lag-adb-panel.json"

API_BASE = "https://api.worldbank.org/v2/country/all/indicator"
RETRIEVED_AT = datetime.now(timezone.utc)
CURRENT_YEAR = RETRIEVED_AT.year
FINDEX_2025_DOWNLOAD_PAGE = "https://www.worldbank.org/en/publication/globalfindex/download-data"
FINDEX_2025_COUNTRY_CSV_URL = (
    "https://thedocs.worldbank.org/en/doc/"
    "be6615202d1f08a25855c8ac2d615122-0050012025/related/"
    "GlobalFindexDatabase2025.csv"
)
G2PX_KNOWLEDGE_URL = "https://www.worldbank.org/en/programs/g2px/knowledge"
FINDEX_2025_CACHE = CACHE / "GlobalFindexDatabase2025.csv"

FINDEX_2025_CANDIDATE_VARIABLES = {
    "account_t_d": "candidate account-ownership variable",
    "g20_made": "candidate digital-payment made variable",
    "g20_received": "candidate digital-payment received variable",
    "g20_any": "candidate any digital-payment variable",
    "fing2p": "candidate government-to-person payment variable",
    "fing2p_acc": "candidate G2P-to-account variable",
    "fing2p_cash": "candidate G2P-cash variable",
    "fing2p_fin": "candidate G2P-financial-institution variable",
    "fing2p_mob": "candidate G2P-mobile-money variable",
    "merchant_pay": "candidate merchant-payment variable",
}

PAYMENT_INDICATORS = {
    "FX.OWN.TOTL.ZS": {
        "short": "account_ownership",
        "label": (
            "Account ownership at a financial institution or with a "
            "mobile-money-service provider (% of population ages 15+)"
        ),
        "source": "World Development Indicators / Global Findex",
    },
    "GFDD.AI.22": {
        "short": "digital_payment_use",
        "label": "Electronic payments used to make payments (% age 15+)",
        "source": "Global Financial Development / Global Findex",
    },
    "GFDD.AI.09": {
        "short": "government_payment_account_use",
        "label": "Account used to receive government payments (% age 15+)",
        "source": "Global Financial Development / Global Findex",
    },
    "gf7_n": {
        "short": "active_account",
        "label": "Active account (% age 15+)",
        "source": "G20 Financial Inclusion Indicators",
    },
}

COUNTRY_ALIASES = {
    "afghanistan": "AFG",
    "armenia": "ARM",
    "azerbaijan": "AZE",
    "bangladesh": "BGD",
    "bhutan": "BTN",
    "brunei darussalam": "BRN",
    "cambodia": "KHM",
    "china": "CHN",
    "china, people's republic of": "CHN",
    "cook islands": "COK",
    "fiji": "FJI",
    "georgia": "GEO",
    "hong kong sar, china": "HKG",
    "hong kong, china": "HKG",
    "india": "IND",
    "indonesia": "IDN",
    "kazakhstan": "KAZ",
    "kiribati": "KIR",
    "kyrgyz republic": "KGZ",
    "kyrgyzstan": "KGZ",
    "lao pdr": "LAO",
    "lao people's democratic republic": "LAO",
    "malaysia": "MYS",
    "maldives": "MDV",
    "marshall islands": "MHL",
    "micronesia, fed. sts.": "FSM",
    "micronesia, federated states of": "FSM",
    "mongolia": "MNG",
    "myanmar": "MMR",
    "nauru": "NRU",
    "nepal": "NPL",
    "pakistan": "PAK",
    "palau": "PLW",
    "papua new guinea": "PNG",
    "philippines": "PHL",
    "samoa": "WSM",
    "solomon islands": "SLB",
    "sri lanka": "LKA",
    "tajikistan": "TJK",
    "thailand": "THA",
    "timor-leste": "TLS",
    "tonga": "TON",
    "turkmenistan": "TKM",
    "tuvalu": "TUV",
    "uzbekistan": "UZB",
    "vanuatu": "VUT",
    "viet nam": "VNM",
    "vietnam": "VNM",
}


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_float(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def normalize_iso(row: dict, known_iso3: set[str]) -> str | None:
    iso3 = row.get("countryiso3code")
    if isinstance(iso3, str) and iso3 in known_iso3:
        return iso3
    country = row.get("country")
    if isinstance(country, dict):
        name = country.get("value", "")
    else:
        name = str(country or "")
    return COUNTRY_ALIASES.get(name.strip().casefold())


def fetch_indicator(code: str) -> tuple[str, Path, dict, list[dict], str, str | None]:
    url = f"{API_BASE}/{code}?format=json&per_page=20000"
    cache_path = CACHE / f"wb-{code}.json"
    request = Request(url, headers={"User-Agent": "ADB-research-topic-sprint/1.0"})
    retrieval_status = "live"
    retrieval_error = None
    try:
        with urlopen(request, timeout=90) as response:
            payload = json.load(response)
        with cache_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        if not cache_path.exists():
            raise
        retrieval_status = "cache_reused_after_fetch_error"
        retrieval_error = f"{type(exc).__name__}: {exc}"
        with cache_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(f"Unexpected World Bank API payload for {code}")
    return url, cache_path, payload[0], payload[1], retrieval_status, retrieval_error


def parse_source_year(year) -> int | None:
    try:
        return int(year)
    except (TypeError, ValueError):
        return None


def reference_age(year) -> int | None:
    parsed = parse_source_year(year)
    if parsed is None:
        return None
    return CURRENT_YEAR - parsed


def gap_flag(value: float | None) -> str:
    if value is None:
        return "missing_gap"
    if value >= 40:
        return "large_gap"
    if value >= 20:
        return "watch_gap"
    return "small_or_negative_gap"


def observability_tier(
    events_per_year: float | None,
    digital_pct: float | None,
    gov_pct: float | None,
    account_pct: float | None,
    sp_coverage: float | None,
) -> str:
    if events_per_year is None:
        return "exposure_missing"
    if digital_pct is not None and gov_pct is not None and sp_coverage is not None:
        return "two_rail_proxy"
    if digital_pct is not None:
        return "payment_use_proxy"
    if account_pct is not None:
        return "account_proxy_only"
    return "payment_rail_missing"


def payment_vintage_status(digital_year, has_findex_2025_candidate: bool) -> str:
    parsed = parse_source_year(digital_year)
    if parsed is None and has_findex_2025_candidate:
        return "api_missing_findex2025_candidate"
    if parsed is None:
        return "payment_use_missing"
    if has_findex_2025_candidate and parsed < 2024:
        return "api_payment_use_lags_findex2025"
    if parsed < 2021:
        return "older_api_payment_use"
    return "api_payment_use_current_for_endpoint"


def source_context(year) -> str:
    age = reference_age(year)
    if age is None:
        return "missing_public_field"
    if age <= 2:
        return "near_current_public_series"
    if age <= 5:
        return "standard_lag_public_series"
    return "older_public_vintage"


def build_evidence_flags(
    *,
    events_per_year: float | None,
    digital_pct: float | None,
    gov_pct: float | None,
    sp_coverage: float | None,
    account_gap: float | None,
    sp_gov_gap: float | None,
    digital_year,
    has_findex_2025_candidate: bool,
) -> list[str]:
    flags = ["no_direct_emergency_transfer_measure"]
    if events_per_year is None:
        flags.append("disaster_exposure_missing")
    if digital_pct is None:
        flags.append("digital_payment_use_missing")
    if gov_pct is None:
        flags.append("government_payment_account_use_missing")
    if sp_coverage is None:
        flags.append("social_protection_coverage_missing")
    if account_gap is not None and account_gap >= 40:
        flags.append("large_account_minus_payment_use_gap")
    elif account_gap is not None and account_gap >= 20:
        flags.append("watch_account_minus_payment_use_gap")
    if sp_gov_gap is not None and sp_gov_gap >= 40:
        flags.append("large_sp_minus_government_payment_gap")
    elif sp_gov_gap is not None and sp_gov_gap >= 20:
        flags.append("watch_sp_minus_government_payment_gap")
    parsed_digital_year = parse_source_year(digital_year)
    if parsed_digital_year is not None and parsed_digital_year < 2021:
        flags.append("older_payment_use_vintage")
    if has_findex_2025_candidate:
        flags.append("findex2025_2024_candidate_row_available")
        if parsed_digital_year is None or parsed_digital_year < 2024:
            flags.append("api_payment_use_endpoint_lags_findex2025")
    else:
        flags.append("findex2025_2024_candidate_row_missing")
    return flags


def fetch_findex_2025_inventory(known_iso3: set[str]) -> tuple[dict, set[str], dict[str, int]]:
    request = Request(
        FINDEX_2025_COUNTRY_CSV_URL,
        headers={"User-Agent": "ADB-research-topic-sprint/1.0"},
    )
    retrieval_status = "live"
    retrieval_error = None
    response_headers = {}
    try:
        with urlopen(request, timeout=120) as response:
            content = response.read()
            response_headers = dict(response.headers)
        with FINDEX_2025_CACHE.open("wb") as f:
            f.write(content)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        if not FINDEX_2025_CACHE.exists():
            retrieval_status = "unavailable"
            retrieval_error = f"{type(exc).__name__}: {exc}"
            return {
                "source": "Global Findex Database 2025 country-level CSV",
                "download_page_url": FINDEX_2025_DOWNLOAD_PAGE,
                "country_csv_url": FINDEX_2025_COUNTRY_CSV_URL,
                "g2px_knowledge_url": G2PX_KNOWLEDGE_URL,
                "retrieval_status": retrieval_status,
                "retrieval_error": retrieval_error,
                "cache_path": repo_rel(FINDEX_2025_CACHE),
                "dmc_2024_all_group_rows": 0,
                "candidate_variable_counts": {
                    key: 0 for key in FINDEX_2025_CANDIDATE_VARIABLES
                },
                "candidate_variable_labels": FINDEX_2025_CANDIDATE_VARIABLES,
                "use_rule": (
                    "Inventory only. Candidate Findex 2025 variable codes must "
                    "be mapped to the official glossary before replacing the "
                    "World Bank API payment-use series."
                ),
            }, set(), {}
        retrieval_status = "cache_reused_after_fetch_error"
        retrieval_error = f"{type(exc).__name__}: {exc}"

    rows_2024 = []
    with FINDEX_2025_CACHE.open("r", encoding="iso-8859-2", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row.get("codewb") in known_iso3
                and row.get("year") == "2024"
                and row.get("group") == "all"
                and row.get("group2") == "all"
            ):
                rows_2024.append(row)

    candidate_iso3 = {row["codewb"] for row in rows_2024}
    candidate_counts = {
        variable: sum(
            1
            for row in rows_2024
            if row.get(variable) not in (None, "", "NA")
        )
        for variable in FINDEX_2025_CANDIDATE_VARIABLES
    }
    candidate_count_by_iso = {
        row["codewb"]: sum(
            1
            for variable in FINDEX_2025_CANDIDATE_VARIABLES
            if row.get(variable) not in (None, "", "NA")
        )
        for row in rows_2024
    }
    inventory = {
        "source": "Global Findex Database 2025 country-level CSV",
        "download_page_url": FINDEX_2025_DOWNLOAD_PAGE,
        "country_csv_url": FINDEX_2025_COUNTRY_CSV_URL,
        "g2px_knowledge_url": G2PX_KNOWLEDGE_URL,
        "retrieval_status": retrieval_status,
        "retrieval_error": retrieval_error,
        "cache_path": repo_rel(FINDEX_2025_CACHE),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "http_last_modified": response_headers.get("Last-Modified"),
        "row_filter": "DMC ISO3 rows where year=2024, group=all, group2=all",
        "dmc_2024_all_group_rows": len(rows_2024),
        "candidate_variable_counts": candidate_counts,
        "candidate_variable_labels": FINDEX_2025_CANDIDATE_VARIABLES,
        "use_rule": (
            "Inventory only. Candidate Findex 2025 variable codes must be "
            "mapped to the official glossary before replacing the World Bank "
            "API payment-use series in the chart."
        ),
    }
    return inventory, candidate_iso3, candidate_count_by_iso


def latest_values_by_iso(rows: list[dict], known_iso3: set[str]) -> dict[str, dict]:
    latest = {}
    for row in rows:
        value = get_float(row.get("value"))
        if value is None:
            continue
        iso3 = normalize_iso(row, known_iso3)
        if iso3 is None:
            continue
        year = int(row["date"])
        if iso3 not in latest or year > latest[iso3]["year"]:
            latest[iso3] = {
                "value": value,
                "year": year,
                "api_country": row.get("country", {}).get("value"),
            }
    return latest


def read_source_panels() -> tuple[dict, dict, dict[str, str], set[str]]:
    social = load_json(SOCIAL_PANEL)
    disaster = load_json(DISASTER_PANEL)
    social_rows = {row["iso3"]: row for row in social["rows"]}
    disaster_rows = {row["iso3"]: row for row in disaster["rows"]}
    countries = {
        row["iso3"]: row.get("country", row["iso3"])
        for row in social["rows"]
        if row["iso3"] != "TWN"
    }
    countries.update({
        row["iso3"]: row.get("country", row["iso3"])
        for row in disaster["rows"]
        if row["iso3"] != "TWN"
    })
    return social_rows, disaster_rows, countries, set(countries)


def build_joined_rows() -> tuple[list[dict], list[dict], dict, dict, dict]:
    social_rows, disaster_rows, countries, known_iso3 = read_source_panels()
    (
        findex_2025_inventory,
        findex_2025_candidate_iso3,
        findex_2025_candidate_count_by_iso,
    ) = fetch_findex_2025_inventory(known_iso3)
    payment_values = {}
    source_records = []

    for code, details in PAYMENT_INDICATORS.items():
        url, cache_path, meta, api_rows, retrieval_status, retrieval_error = fetch_indicator(code)
        latest = latest_values_by_iso(api_rows, known_iso3)
        payment_values[code] = latest
        latest_reference_year = max((v["year"] for v in latest.values()), default=None)
        source_records.append({
            "indicator_code": code,
            "short": details["short"],
            "label": details["label"],
            "source": details["source"],
            "url": url,
            "cache_path": repo_rel(cache_path),
            "retrieval_status": retrieval_status,
            "retrieval_error": retrieval_error,
            "api_total": meta.get("total"),
            "api_lastupdated": meta.get("lastupdated"),
            "dmc_latest_value_count": len(latest),
            "latest_reference_years": sorted({v["year"] for v in latest.values()}),
            "latest_reference_year": latest_reference_year,
            "latest_reference_age_years": reference_age(latest_reference_year),
            "source_context": source_context(latest_reference_year),
        })

    rows = []
    for iso3, country in sorted(countries.items(), key=lambda item: item[1]):
        social = social_rows.get(iso3, {})
        disaster = disaster_rows.get(iso3, {})
        account_api = payment_values["FX.OWN.TOTL.ZS"].get(iso3)
        account_existing = get_float(social.get("findex_account_pct"))
        account_pct = (
            account_api["value"]
            if account_api is not None
            else account_existing
        )
        account_year = (
            account_api["year"]
            if account_api is not None
            else social.get("findex_year")
        )

        digital = payment_values["GFDD.AI.22"].get(iso3)
        government = payment_values["GFDD.AI.09"].get(iso3)
        active = payment_values["gf7_n"].get(iso3)

        events_per_year = get_float(disaster.get("events_per_year"))
        total_affected = get_float(disaster.get("total_affected"))
        poverty = get_float(social.get("poverty_headcount_215_pct"))
        sp_coverage = get_float(social.get("sp_coverage_pct"))
        digital_pct = digital["value"] if digital else None
        gov_pct = government["value"] if government else None
        active_pct = active["value"] if active else None

        account_minus_digital = (
            account_pct - digital_pct
            if account_pct is not None and digital_pct is not None
            else None
        )
        sp_minus_government = (
            sp_coverage - gov_pct
            if sp_coverage is not None and gov_pct is not None
            else None
        )

        has_plot_value = events_per_year is not None and digital_pct is not None
        has_findex_2025_candidate = iso3 in findex_2025_candidate_iso3
        tier = observability_tier(
            events_per_year,
            digital_pct,
            gov_pct,
            account_pct,
            sp_coverage,
        )
        vintage_status = payment_vintage_status(
            digital["year"] if digital else None,
            has_findex_2025_candidate,
        )
        evidence_flags = build_evidence_flags(
            events_per_year=events_per_year,
            digital_pct=digital_pct,
            gov_pct=gov_pct,
            sp_coverage=sp_coverage,
            account_gap=account_minus_digital,
            sp_gov_gap=sp_minus_government,
            digital_year=digital["year"] if digital else None,
            has_findex_2025_candidate=has_findex_2025_candidate,
        )
        rows.append({
            "iso3": iso3,
            "country": country,
            "events_per_year_2000_2025": round(events_per_year, 4)
            if events_per_year is not None else None,
            "total_events_2000_2025": disaster.get("total_events_2000_2025"),
            "total_affected_2000_2025": int(total_affected)
            if total_affected is not None else None,
            "sp_coverage_pct": round(sp_coverage, 4)
            if sp_coverage is not None else None,
            "sp_coverage_year": social.get("sp_coverage_year"),
            "account_ownership_pct": round(account_pct, 4)
            if account_pct is not None else None,
            "account_ownership_year": account_year,
            "digital_payment_use_pct": round(digital_pct, 4)
            if digital_pct is not None else None,
            "digital_payment_use_year": digital["year"] if digital else None,
            "government_payment_account_use_pct": round(gov_pct, 4)
            if gov_pct is not None else None,
            "government_payment_account_use_year": government["year"] if government else None,
            "active_account_pct": round(active_pct, 4) if active_pct is not None else None,
            "active_account_year": active["year"] if active else None,
            "poverty_headcount_215_pct": round(poverty, 4)
            if poverty is not None else None,
            "poverty_year": social.get("poverty_year"),
            "account_minus_digital_payment_pct": round(account_minus_digital, 4)
            if account_minus_digital is not None else None,
            "sp_minus_government_payment_account_pct": round(sp_minus_government, 4)
            if sp_minus_government is not None else None,
            "observability_tier": tier,
            "payment_vintage_status": vintage_status,
            "digital_payment_source_context": source_context(digital["year"] if digital else None),
            "digital_payment_age_years": reference_age(digital["year"] if digital else None),
            "account_to_digital_year_gap": (
                parse_source_year(account_year) - parse_source_year(digital["year"])
                if account_year is not None and digital is not None
                else None
            ),
            "account_gap_flag": gap_flag(account_minus_digital),
            "sp_government_payment_gap_flag": gap_flag(sp_minus_government),
            "has_findex2025_2024_candidate_row": has_findex_2025_candidate,
            "findex2025_candidate_variable_count": (
                findex_2025_candidate_count_by_iso.get(iso3, 0)
            ),
            "evidence_flags": "; ".join(evidence_flags),
            "has_disaster_data": bool(disaster),
            "has_digital_payment_use": digital_pct is not None,
            "has_government_payment_account_use": gov_pct is not None,
            "has_plot_value": has_plot_value,
        })

    observability_order = {
        "two_rail_proxy": 0,
        "payment_use_proxy": 1,
        "account_proxy_only": 2,
        "payment_rail_missing": 3,
        "exposure_missing": 4,
    }
    observability_counts = {
        tier: sum(1 for r in rows if r["observability_tier"] == tier)
        for tier in observability_order
    }
    payment_vintage_counts = {
        status: sum(1 for r in rows if r["payment_vintage_status"] == status)
        for status in sorted({r["payment_vintage_status"] for r in rows})
    }
    coverage = {
        "dmc_rows": len(rows),
        "rows_with_disaster_event_frequency": sum(
            1 for r in rows if r["events_per_year_2000_2025"] is not None
        ),
        "rows_with_sp_coverage": sum(1 for r in rows if r["sp_coverage_pct"] is not None),
        "rows_with_account_ownership": sum(
            1 for r in rows if r["account_ownership_pct"] is not None
        ),
        "rows_with_digital_payment_use": sum(
            1 for r in rows if r["digital_payment_use_pct"] is not None
        ),
        "rows_with_government_payment_account_use": sum(
            1 for r in rows if r["government_payment_account_use_pct"] is not None
        ),
        "rows_with_active_account": sum(
            1 for r in rows if r["active_account_pct"] is not None
        ),
        "rows_with_plot_value": sum(1 for r in rows if r["has_plot_value"]),
        "rows_with_two_rail_proxy": observability_counts["two_rail_proxy"],
        "rows_with_payment_use_proxy": observability_counts["payment_use_proxy"],
        "rows_with_account_proxy_only": observability_counts["account_proxy_only"],
        "rows_with_payment_rail_missing": observability_counts["payment_rail_missing"],
        "rows_with_exposure_missing": observability_counts["exposure_missing"],
        "rows_with_findex2025_2024_candidate_row": sum(
            1 for r in rows if r["has_findex2025_2024_candidate_row"]
        ),
        "rows_where_api_payment_lags_findex2025": sum(
            1
            for r in rows
            if r["payment_vintage_status"]
            in ("api_payment_use_lags_findex2025", "api_missing_findex2025_candidate")
        ),
        "rows_with_large_account_payment_gap": sum(
            1 for r in rows if r["account_gap_flag"] == "large_gap"
        ),
        "rows_with_exposure_and_large_account_gap": sum(
            1
            for r in rows
            if r["account_gap_flag"] == "large_gap"
            and (r["events_per_year_2000_2025"] or 0) >= 5
        ),
        "observability_tier_counts": observability_counts,
        "payment_vintage_status_counts": payment_vintage_counts,
        "findex2025_candidate_variable_counts": (
            findex_2025_inventory["candidate_variable_counts"]
        ),
    }

    direct_flags = sorted(
        [
            r for r in rows
            if r["events_per_year_2000_2025"] is not None
            and r["digital_payment_use_pct"] is not None
        ],
        key=lambda r: (
            -r["events_per_year_2000_2025"],
            r["digital_payment_use_pct"],
            r["country"],
        ),
    )[:12]

    account_gap_flags = sorted(
        [
            r for r in rows
            if r["account_minus_digital_payment_pct"] is not None
        ],
        key=lambda r: (
            -r["account_minus_digital_payment_pct"],
            -(
                r["events_per_year_2000_2025"]
                if r["events_per_year_2000_2025"] is not None else -1
            ),
            r["country"],
        ),
    )[:12]

    observability_watch_order = {
        "payment_rail_missing": 0,
        "account_proxy_only": 1,
        "payment_use_proxy": 2,
        "two_rail_proxy": 3,
        "exposure_missing": 4,
    }
    source_observability_watchlist = sorted(
        rows,
        key=lambda r: (
            -(
                r["events_per_year_2000_2025"]
                if r["events_per_year_2000_2025"] is not None else -1
            ),
            observability_watch_order.get(r["observability_tier"], 9),
            -(
                r["account_minus_digital_payment_pct"]
                if r["account_minus_digital_payment_pct"] is not None else -1
            ),
            r["country"],
        ),
    )[:12]

    summaries = {
        "highest_disaster_exposure_with_payment_use_top12": direct_flags,
        "largest_account_minus_digital_payment_gap_top12": account_gap_flags,
        "source_observability_watchlist_top12": source_observability_watchlist,
    }
    return rows, source_records, coverage, summaries, findex_2025_inventory


def marker_size(total_affected) -> float:
    if not isinstance(total_affected, (int, float)) or total_affected <= 0:
        return 50.0
    return 35.0 + min(500.0, 28.0 * math.log10(total_affected + 1))


def write_scatter(rows: list[dict]) -> tuple[Path, Path]:
    plot_rows = [
        row for row in rows
        if row["events_per_year_2000_2025"] is not None
        and row["digital_payment_use_pct"] is not None
    ]
    if not plot_rows:
        raise ValueError("No rows available for shock-payment scatter")

    fig = plt.figure(figsize=(15.2, 8.8))
    grid = GridSpec(1, 2, width_ratios=[2.15, 1], wspace=0.28, figure=fig)
    ax = fig.add_subplot(grid[0, 0])
    gap_ax = fig.add_subplot(grid[0, 1])

    missing_sp_rows = []
    colored_rows = []
    for row in plot_rows:
        if row["sp_coverage_pct"] is None:
            missing_sp_rows.append(row)
        else:
            colored_rows.append(row)

    if colored_rows:
        scatter = ax.scatter(
            [r["events_per_year_2000_2025"] for r in colored_rows],
            [r["digital_payment_use_pct"] for r in colored_rows],
            s=[marker_size(r["total_affected_2000_2025"]) for r in colored_rows],
            c=[r["sp_coverage_pct"] for r in colored_rows],
            cmap="viridis",
            vmin=0,
            vmax=100,
            alpha=0.82,
            linewidth=0.7,
            edgecolor="#1f2937",
        )
        colorbar = fig.colorbar(scatter, ax=ax, fraction=0.045, pad=0.02)
        colorbar.set_label("ASPIRE social-protection coverage (% population)")

    if missing_sp_rows:
        ax.scatter(
            [r["events_per_year_2000_2025"] for r in missing_sp_rows],
            [r["digital_payment_use_pct"] for r in missing_sp_rows],
            s=[marker_size(r["total_affected_2000_2025"]) for r in missing_sp_rows],
            facecolors="#f9fafb",
            alpha=0.82,
            linewidth=0.7,
            edgecolor="#6b7280",
            label="SP coverage missing",
        )

    label_rows = sorted(
        plot_rows,
        key=lambda r: (
            -r["events_per_year_2000_2025"],
            r["digital_payment_use_pct"],
        ),
    )[:8]
    label_rows += [
        r for r in plot_rows
        if r["events_per_year_2000_2025"] >= 1.5 and r["digital_payment_use_pct"] < 25
    ]
    seen = set()
    for row in label_rows:
        if row["iso3"] in seen:
            continue
        seen.add(row["iso3"])
        ax.annotate(
            row["iso3"],
            (row["events_per_year_2000_2025"], row["digital_payment_use_pct"]),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=8,
            color="#111827",
        )

    ax.set_title("Shock exposure versus payment-use")
    ax.set_xlabel("EM-DAT recorded disasters per year, 2000-2025")
    ax.set_ylabel("Electronic payments used to make payments (% age 15+), latest public value")
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0, top=max(100, max(r["digital_payment_use_pct"] for r in plot_rows) + 5))

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#9ca3af",
            markeredgecolor="#1f2937",
            markersize=8,
            label="Bubble size: total people affected in EM-DAT records",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="#f9fafb",
            markeredgecolor="#6b7280",
            markersize=8,
            label="Hollow fill: SP coverage missing",
        ),
    ]
    ax.legend(handles=legend_handles, loc="lower right", frameon=False, fontsize=8)

    gap_rows = sorted(
        [
            r for r in rows
            if r["account_minus_digital_payment_pct"] is not None
            and r["events_per_year_2000_2025"] is not None
        ],
        key=lambda r: (
            -r["account_minus_digital_payment_pct"],
            -r["events_per_year_2000_2025"],
            r["country"],
        ),
    )[:10]
    gap_labels = [r["iso3"] for r in gap_rows]
    gap_values = [r["account_minus_digital_payment_pct"] for r in gap_rows]
    gap_colors = [
        "#007db8" if r["events_per_year_2000_2025"] >= 5 else "#8ab6d6"
        for r in gap_rows
    ]
    gap_ax.barh(gap_labels, gap_values, color=gap_colors)
    gap_ax.invert_yaxis()
    gap_ax.set_title("Account ownership is not payment use")
    gap_ax.set_xlabel("Account minus digital use (percentage points)")
    gap_ax.grid(True, axis="x", color="#e5e7eb", linewidth=0.8)
    gap_ax.set_axisbelow(True)
    for y, row in enumerate(gap_rows):
        gap_ax.text(
            row["account_minus_digital_payment_pct"] + 1,
            y,
            f"{row['account_minus_digital_payment_pct']:.0f} pp",
            va="center",
            fontsize=8,
            color="#111827",
        )
    gap_ax.text(
        0.02,
        0.02,
        "Darker bars: at least five EM-DAT events per year",
        transform=gap_ax.transAxes,
        fontsize=8,
        color="#4b5563",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8, "pad": 2},
    )

    fig.suptitle(
        "Public shock-payment sources separate exposure, coverage, and payment use",
        fontsize=15,
        y=0.98,
    )
    fig.text(
        0.055,
        0.02,
        "L2 sprint visual. Digital-payment use is not a measure of shock-payment receipt; "
        "ASPIRE coverage pools social-protection types; EM-DAT affected counts are event records and may double-count people.\n"
        "Sources: World Bank API payment indicators, repo ASPIRE/Findex/WDI social-protection panel, "
        "and EM-DAT country profiles via HDX.",
        fontsize=8,
        color="#4b5563",
    )

    fig.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.17, wspace=0.32)
    png_path = CHARTS / "shock-payment-rails-scatter.png"
    svg_path = CHARTS / "shock-payment-rails-scatter.svg"
    fig.savefig(png_path, dpi=180)
    fig.savefig(svg_path)
    plt.close(fig)
    with svg_path.open("r", encoding="utf-8") as f:
        svg_lines = [line.rstrip() for line in f]
    with svg_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines) + "\n")
    return png_path, svg_path


def write_outputs(
    rows,
    source_records,
    coverage,
    summaries,
    findex_2025_inventory,
    png_path,
    svg_path,
):
    csv_path = OUT / "shock-payment-rails-sprint.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    status = (
        "promote_to_program_prospectus_candidate"
        if coverage["rows_with_plot_value"] >= 15
        and coverage["rows_with_digital_payment_use"] >= 15
        else "defer_until_payment_use_coverage_improves"
    )
    decision = (
        "Promote as a program prospectus candidate: the first visual joins "
        "shock exposure to a direct payment-use variable, and the table shows "
        "why account ownership should not be treated as delivery readiness."
        if status == "promote_to_program_prospectus_candidate"
        else "Defer: public payment-use coverage is too sparse for a credible "
        "DMC-facing first visual."
    )

    payload = {
        "attestation_chain": "ai-first",
        "goal_level": "L2 hook sprint",
        "hook": "Shock-payment rails after disasters",
        "status": status,
        "decision": decision,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "retrieval_started_at": RETRIEVED_AT.isoformat(),
        "inputs": {
            "social_protection_panel": repo_rel(SOCIAL_PANEL),
            "disaster_panel": repo_rel(DISASTER_PANEL),
            "world_bank_payment_indicators": source_records,
            "findex_2025_country_level_inventory": findex_2025_inventory,
        },
        "source_sanity": {
            "unit": (
                "Each row is an economy joined across disaster event frequency, "
                "social-protection coverage, poverty, and payment-use indicators."
            ),
            "payment_use_caveat": (
                "Electronic payment use, government-payment account use, active "
                "account, and account ownership measure different concepts. None "
                "is a direct measure of whether emergency transfers arrived after "
                "a disaster."
            ),
            "disaster_caveat": (
                "EM-DAT event counts and affected totals are recorded disaster "
                "event records over 2000-2025. Affected totals can double-count "
                "people exposed to multiple events."
            ),
            "social_protection_caveat": (
                "ASPIRE coverage pools multiple social-protection instruments "
                "and reporting years. It is not a post-shock payment-channel "
                "measure."
            ),
            "use_limit": (
                "This sprint can promote a new topic to prospectus. It cannot "
                "support a public ranking or causal claim without literature, "
                "vintage checks, payment-channel validation, and sensitivity "
                "tests."
            ),
            "findex_2025_inventory_rule": (
                "Global Findex 2025 country-level data are inventoried as a "
                "candidate 2024 source because the public download reports "
                "2024 rows and payment/G2P variable codes. The sprint does "
                "not replace the World Bank API payment-use series until "
                "the Findex 2025 variable glossary is mapped and audited."
            ),
            "observability_protocol": (
                "Two-rail proxy means the row has disaster frequency, "
                "digital-payment use, government-payment account use, and "
                "ASPIRE social-protection coverage. Payment-use proxy keeps "
                "direct electronic-payment use but lacks at least one program "
                "or government-payment leg. Account-proxy-only is not enough "
                "for delivery-readiness language."
            ),
        },
        "first_visual": {
            "type": "scatter",
            "question": (
                "Where are disaster event frequency and observed payment-use "
                "rails misaligned in public sources?"
            ),
            "outputs": {
                "png": repo_rel(png_path),
                "svg": repo_rel(svg_path),
            },
        },
        "coverage": coverage,
        "triage_summaries": summaries,
        "rows": rows,
    }

    json_path = OUT / "shock-payment-rails-sprint.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    return csv_path, json_path, payload


def main():
    rows, source_records, coverage, summaries, findex_2025_inventory = build_joined_rows()
    png_path, svg_path = write_scatter(rows)
    csv_path, json_path, payload = write_outputs(
        rows,
        source_records,
        coverage,
        summaries,
        findex_2025_inventory,
        png_path,
        svg_path,
    )

    print("L2 new-topic sprint complete")
    print(f"DMC rows: {coverage['dmc_rows']}")
    print(f"Rows with disaster frequency: {coverage['rows_with_disaster_event_frequency']}")
    print(f"Rows with digital-payment use: {coverage['rows_with_digital_payment_use']}")
    print(f"Rows with government-payment account use: {coverage['rows_with_government_payment_account_use']}")
    print(f"Rows with plot value: {coverage['rows_with_plot_value']}")
    print(f"Two-rail proxy rows: {coverage['rows_with_two_rail_proxy']}")
    print(f"Findex 2025 candidate rows: {coverage['rows_with_findex2025_2024_candidate_row']}")
    print(f"API payment-use rows lagging Findex 2025: {coverage['rows_where_api_payment_lags_findex2025']}")
    print(f"Decision: {payload['status']}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
