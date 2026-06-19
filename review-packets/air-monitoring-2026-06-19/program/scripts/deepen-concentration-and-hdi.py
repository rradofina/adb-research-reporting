"""Air-monitoring — deepening pass: (a) population concentration of the
zero-monitor headline, and (b) the development (HDI / GDP-per-capita)
confound on the observability gap.

Answers the two questions the screen left open:

  KEYSTONE (a) — `deep-questions.md` §4.2. The "~14.3M people in
  zero-public-monitor economies" regional headline is tested for
  concentration: each zero-monitor economy's share of the zero-monitor
  population total is computed, and the claim that Papua New Guinea +
  Timor-Leste alone carry ~84% (PNG alone ~74%) is confirmed or refuted
  from the panel. A regional aggregate that is ~84% two economies is a
  composite headline in the CONSTITUTION.md §6.4 sense and must not lead.

  KEYSTONE (b) — `deep-questions.md` §1.1 / §5. The gap-score multiplies
  two things lower-income economies can have together (high PM2.5, few
  public monitors). The decisive test is to partial log(people-per-monitor)
  on a development level series. This script fetches public WDI GDP per
  capita (`NY.GDP.PCAP.CD`) and runs that partial for economies with at
  least one public PM2.5 monitor. Zero-monitor economies remain a separate
  observability category because people-per-monitor is undefined at zero.

THE ONE RULE. Every number below is recomputed from committed/generated
data or a public API response cached by this script: the committed
`generated/air-monitoring-adb-panel.json` (OpenAQ v3 + WDI
EN.ATM.PM25.MC.M3 + WHO AAQ v6.1, snapshot 2026-04-23) and WDI
NY.GDP.PCAP.CD fetched through the World Bank API. No AI-supplied figures.
Spearman rho is hand-computed from ranks and cross-checked against scipy
where scipy is importable. The gap-score is a composite triage measure per
CONSTITUTION.md §6.4, never a country pollution ranking (§13.3 — this is a
measurement / coverage gap).
attestation_chain: ai-first.
"""
import csv
import glob
import json
import math
import os
import urllib.request
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/air-monitoring"
REPO = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research"
PANEL = f"{BASE}/generated/air-monitoring-adb-panel.json"
OUT = f"{BASE}/generated"
CACHE = f"{BASE}/.cache"
GDP_PC_CACHE = f"{CACHE}/wdi-NY.GDP.PCAP.CD.json"
GDP_PC_URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&per_page=20000"
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

# Token sequences that, in a cache filename, would indicate a per-economy
# development / income LEVEL series usable to partial out the confound.
# Matching is on TOKENS (filename split on non-alphanumerics), not raw
# substrings, so e.g. "withdrawal" does not spuriously match the UNDP "hdr"
# tag. Each hint is a tuple of consecutive tokens that must all appear in
# order. (A remittance-as-%-of-GDP ratio is explicitly NOT a level series.)
DEV_SERIES_HINTS = (
    ("hdi",), ("human", "development"), ("hdr",),        # UNDP HDI
    ("gdp", "pcap"), ("gdppcap",), ("gdp", "per", "capita"),  # WDI NY.GDP.PCAP.*
    ("ny", "gdp", "pcap"),
    ("gni", "pcap"), ("gnipcap",), ("gni", "per", "capita"),  # WDI NY.GNP.PCAP.*
    ("pcap", "pp"), ("pcap", "cd"), ("pcap", "kd"),
)
DEV_SERIES_ANTIHINTS = ("pct_gdp", "_gdp.json", "remittance")  # ratios, not levels


# ---------- statistics, hand-rolled so every figure is auditable ----------
def _ranks(xs):
    """Fractional (average) ranks, ties shared — standard Spearman handling."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # ranks are 1-based
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def _pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def spearman(xs, ys):
    """Spearman rho = Pearson on fractional ranks. Returns (rho, n)."""
    if len(xs) != len(ys) or len(xs) < 3:
        return None, len(xs)
    return _pearson(_ranks(xs), _ranks(ys)), len(xs)


def ols_residuals(xs, ys):
    """Simple y = a + b*x fit. Returns intercept, slope, residuals."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if n < 3 or sxx == 0:
        return None, None, [None] * n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = my - slope * mx
    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    return intercept, slope, residuals


# ------------------------------ load panel --------------------------------
def load_panel():
    with open(PANEL, encoding="utf-8") as f:
        doc = json.load(f)
    return doc["rows"]


def _tokens(name):
    """Lower-case filename split into alphanumeric tokens."""
    out, cur = [], []
    for ch in name.lower():
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


def _has_subseq(tokens, hint):
    """True if the consecutive token tuple `hint` appears in `tokens`."""
    n, m = len(tokens), len(hint)
    return any(tuple(tokens[i:i + m]) == hint for i in range(n - m + 1)) if m <= n else False


def find_dev_series():
    """Search every on-disk cache for a usable development LEVEL series.

    Token-based so substrings like 'witHDRawal' do not false-match.
    Returns a list of candidate file paths (empty == data wall)."""
    hits = []
    for path in glob.glob(f"{REPO}/**/.cache/**/*.*", recursive=True):
        base = os.path.basename(path).lower()
        if any(a in base for a in DEV_SERIES_ANTIHINTS):
            continue
        toks = _tokens(base)
        if any(_has_subseq(toks, h) for h in DEV_SERIES_HINTS):
            hits.append(path)
    return sorted(set(hits))


def fetch_wdi_gdp_pc():
    """Fetch/cache WDI GDP per capita and return latest non-null value by ISO3."""
    if os.path.exists(GDP_PC_CACHE):
        with open(GDP_PC_CACHE, encoding="utf-8") as f:
            payload = json.load(f)
    else:
        with urllib.request.urlopen(GDP_PC_URL, timeout=60) as resp:
            api_payload = json.loads(resp.read().decode("utf-8"))
        payload = {
            "retrieved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_url": GDP_PC_URL,
            "indicator": "NY.GDP.PCAP.CD",
            "payload": api_payload,
        }
        with open(GDP_PC_CACHE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    raw = payload.get("payload", payload)
    records = raw[1] if isinstance(raw, list) and len(raw) > 1 else []
    latest = {}
    for rec in records:
        iso3 = rec.get("countryiso3code")
        value = rec.get("value")
        year = rec.get("date")
        if not iso3 or value is None or not year:
            continue
        try:
            year_i = int(year)
            value_f = float(value)
        except (TypeError, ValueError):
            continue
        if value_f <= 0:
            continue
        prev = latest.get(iso3)
        if prev is None or year_i > prev["year"]:
            latest[iso3] = {
                "year": year_i,
                "value_current_usd": value_f,
            }
    retrieved_at = payload.get("retrieved_at")
    source_url = payload.get("source_url", GDP_PC_URL)
    return latest, {"retrieved_at": retrieved_at, "url": source_url}


def main():
    rows = load_panel()

    # ---- Part (a): concentration of the zero-monitor population headline ----
    zero = [r for r in rows
            if r["pm25_locations"] == 0 and r["population"] > 0]
    zero.sort(key=lambda r: -r["population"])
    zero_total = sum(r["population"] for r in zero)

    conc = []
    for r in zero:
        conc.append({
            "iso3": r["iso3"], "country": r["country"],
            "subregion": r["subregion"],
            "population": r["population"],
            "pm25_exposure_ugm3": r["pm25_exposure_ugm3"],
            "share_of_zero_monitor_pop": round(r["population"] / zero_total, 4),
        })

    png = next((c for c in conc if c["iso3"] == "PNG"), None)
    tls = next((c for c in conc if c["iso3"] == "TLS"), None)
    png_share = png["share_of_zero_monitor_pop"] if png else 0.0
    tls_share = tls["share_of_zero_monitor_pop"] if tls else 0.0
    top2_share = png_share + tls_share
    # cumulative share to show how fast the tail collapses
    cum = 0.0
    for c in conc:
        cum += c["share_of_zero_monitor_pop"]
        c["cumulative_share"] = round(cum, 4)

    # ---- Part (b): the development / HDI confound ----
    # Build the analysis frame: all economies with population, exposure,
    # and (for people-per-monitor) at least the count present.
    frame = [r for r in rows
             if r["population"] > 0 and r["pm25_exposure_ugm3"] > 0]
    # people-per-monitor: undefined for zero monitors -> use the panel's
    # own convention only where a monitor exists; for the rank correlation
    # we report two variants:
    #   (i) over economies WITH >=1 monitor (ppm well-defined)
    #   (ii) gap-score correlations over the full exposed frame
    with_mon = [r for r in frame if r["pm25_locations"] > 0]

    gap = [r["pm25_observability_gap_score"] for r in frame]
    pm = [r["pm25_exposure_ugm3"] for r in frame]
    pop = [r["population"] for r in frame]
    logpop = [math.log10(p) for p in pop]

    rho_gap_pm, n1 = spearman(gap, pm)
    rho_gap_logpop, n2 = spearman(gap, logpop)

    ppm = [r["population"] / r["pm25_locations"] for r in with_mon]
    log_ppm = [math.log10(v) for v in ppm]
    gap_wm = [r["pm25_observability_gap_score"] for r in with_mon]
    pm_wm = [r["pm25_exposure_ugm3"] for r in with_mon]
    rho_gap_logppm, n3 = spearman(gap_wm, log_ppm)
    rho_logppm_pm, n4 = spearman(log_ppm, pm_wm)

    # cross-check rho against scipy if available (audit only; not headline path)
    scipy_check = {}
    try:
        from scipy.stats import spearmanr
        scipy_check = {
            "gap_vs_pm25": round(float(spearmanr(gap, pm).statistic), 4),
            "gap_vs_log10pop": round(float(spearmanr(gap, logpop).statistic), 4),
            "gap_vs_log10_ppm_withmon": round(float(spearmanr(gap_wm, log_ppm).statistic), 4),
            "log_ppm_vs_pm25_withmon": round(float(spearmanr(log_ppm, pm_wm).statistic), 4),
        }
    except Exception as e:  # scipy absent or errored -> hand figure still stands
        scipy_check = {"unavailable": str(e)}

    dev_series = find_dev_series()
    gdp_pc, gdp_meta = fetch_wdi_gdp_pc()

    with_mon_gdp = [r for r in with_mon if r["iso3"] in gdp_pc]
    log_gdp_wm = [math.log10(gdp_pc[r["iso3"]]["value_current_usd"]) for r in with_mon_gdp]
    log_ppm_wm = [math.log10(r["population"] / r["pm25_locations"]) for r in with_mon_gdp]
    gap_wm_gdp = [r["pm25_observability_gap_score"] for r in with_mon_gdp]
    pm_wm_gdp = [r["pm25_exposure_ugm3"] for r in with_mon_gdp]
    rho_logppm_loggdp, n_gdp_partial = spearman(log_ppm_wm, log_gdp_wm)
    rho_gap_loggdp_wm, _ = spearman(gap_wm_gdp, log_gdp_wm)
    rho_pm_loggdp_wm, _ = spearman(pm_wm_gdp, log_gdp_wm)
    intercept, slope, residuals = ols_residuals(log_gdp_wm, log_ppm_wm)

    residual_rows = []
    for r, resid in zip(with_mon_gdp, residuals):
        if resid is None:
            continue
        residual_rows.append({
            "iso3": r["iso3"],
            "country": r["country"],
            "subregion": r["subregion"],
            "population": r["population"],
            "pm25_locations": r["pm25_locations"],
            "people_per_monitor": round(r["population"] / r["pm25_locations"], 1),
            "pm25_exposure_ugm3": r["pm25_exposure_ugm3"],
            "gap_score": r["pm25_observability_gap_score"],
            "gdp_pc_year": gdp_pc[r["iso3"]]["year"],
            "gdp_pc_current_usd": round(gdp_pc[r["iso3"]]["value_current_usd"], 2),
            "log10_people_per_monitor_residual": round(resid, 4),
        })
    residual_rows.sort(key=lambda r: -r["log10_people_per_monitor_residual"])

    zero_gdp_rows = []
    for r in zero:
        meta = gdp_pc.get(r["iso3"])
        zero_gdp_rows.append({
            "iso3": r["iso3"],
            "country": r["country"],
            "population": r["population"],
            "pm25_exposure_ugm3": r["pm25_exposure_ugm3"],
            "gdp_pc_year": meta["year"] if meta else None,
            "gdp_pc_current_usd": round(meta["value_current_usd"], 2) if meta else None,
            "partial_status": "excluded_from_log_people_per_monitor_partial_because_pm25_locations_zero",
        })

    # ----------------------------- assemble ----------------------------------
    partial_note = (
        "The script fetches WDI NY.GDP.PCAP.CD and runs a simple OLS partial "
        "for economies with at least one public PM2.5 monitor: "
        "log10(people per monitor) on log10(GDP per capita). Zero-monitor "
        "economies are excluded from this residual because people per monitor "
        "is undefined at zero; they are reported separately as an observability "
        "category. This partial uses GDP per capita only, not UNDP HDI, and is "
        "descriptive rather than a causal test."
    )

    payload = {
        "program": "air-monitoring",
        "analysis": "population concentration of zero-monitor headline + development confound",
        "claim_scope": (
            "Deepening of the PM2.5 observability-gap screen. (a) Decomposes "
            "the ~14.3M zero-public-monitor population headline by economy "
            "share. (b) Tests the development (HDI / GDP-per-capita) confound "
            "on the gap-score. Both parts recompute only from the committed "
            "panel; the gap-score is a CONSTITUTION.md §6.4 triage composite, "
            "framed as a §13.3 measurement/coverage gap, never a pollution "
            "ranking."
        ),
        "source": {
            "name": "air-monitoring committed panel",
            "file": "generated/air-monitoring-adb-panel.json",
            "inputs": "OpenAQ v3 + WDI EN.ATM.PM25.MC.M3 + WHO AAQ v6.1",
            "snapshot": "2026-04-23",
            "license": "OpenAQ CC BY 4.0; WDI CC BY 4.0; WHO open",
            "development_confound_source": {
                "name": "World Bank WDI NY.GDP.PCAP.CD",
                "url": gdp_meta["url"],
                "cache": ".cache/wdi-NY.GDP.PCAP.CD.json",
                "retrieved_at": gdp_meta["retrieved_at"],
                "license": "WDI CC BY 4.0",
            },
        },
        "part_a_concentration": {
            "zero_monitor_economy_count": len(zero),
            "zero_monitor_population_total": zero_total,
            "png_share": png_share,
            "timor_share": tls_share,
            "png_plus_timor_share": round(top2_share, 4),
            "rows": conc,
            "composite_caution": (
                "Per CONSTITUTION.md §6.4, a regional total that is "
                f"{round(top2_share*100,1)}% two economies (PNG + Timor-Leste) "
                "is a composite and must not headline; name the two economies."
            ),
        },
        "part_b_confound": {
            "development_series_on_disk": dev_series,
            "wdi_gdp_per_capita_fetched": True,
            "confound_partial_runnable_from_public_wdi_gdp": n_gdp_partial >= 3,
            "rank_correlations_descriptive_only": {
                "spearman_gap_vs_pm25": (round(rho_gap_pm, 4) if rho_gap_pm is not None else None),
                "spearman_gap_vs_log10_population": (round(rho_gap_logpop, 4) if rho_gap_logpop is not None else None),
                "spearman_gap_vs_log10_people_per_monitor_withmon": (round(rho_gap_logppm, 4) if rho_gap_logppm is not None else None),
                "spearman_log_people_per_monitor_vs_pm25_withmon": (round(rho_logppm_pm, 4) if rho_logppm_pm is not None else None),
                "spearman_log_people_per_monitor_vs_log10_gdp_pc_withmon": (round(rho_logppm_loggdp, 4) if rho_logppm_loggdp is not None else None),
                "spearman_gap_score_vs_log10_gdp_pc_withmon": (round(rho_gap_loggdp_wm, 4) if rho_gap_loggdp_wm is not None else None),
                "spearman_pm25_vs_log10_gdp_pc_withmon": (round(rho_pm_loggdp_wm, 4) if rho_pm_loggdp_wm is not None else None),
                "n_full_exposed_frame": n1,
                "n_with_monitor_frame": n3,
                "n_with_monitor_and_gdp_pc": n_gdp_partial,
            },
            "gdp_partial": {
                "method": "OLS residual from log10(people_per_monitor) = a + b*log10(WDI GDP per capita current US$), monitored economies only",
                "intercept": round(intercept, 4) if intercept is not None else None,
                "slope": round(slope, 4) if slope is not None else None,
                "all_residuals": residual_rows,
                "top_positive_residuals_more_people_per_monitor_than_gdp_predicts": residual_rows[:10],
                "top_negative_residuals_fewer_people_per_monitor_than_gdp_predicts": list(reversed(residual_rows[-10:])),
                "zero_monitor_economies_excluded_from_partial": zero_gdp_rows,
                "interpretation_limit": partial_note,
            },
            "scipy_crosscheck": scipy_check,
            "data_wall": None,
        },
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/air-monitoring-concentration-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    with open(f"{OUT}/air-monitoring-concentration-deepening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["iso3", "country", "subregion", "population",
                    "pm25_exposure_ugm3", "share_of_zero_monitor_pop",
                    "cumulative_share"])
        for c in conc:
            w.writerow([c["iso3"], c["country"], c["subregion"],
                        c["population"], c["pm25_exposure_ugm3"],
                        c["share_of_zero_monitor_pop"], c["cumulative_share"]])

    # ------------------------------- stdout ----------------------------------
    print("=== PART (a) — concentration of the zero-monitor population headline ===")
    print(f"zero-public-monitor economies (pop>0): {len(zero)}")
    print(f"zero-monitor population total: {zero_total:,}")
    print(f"PNG share: {png_share*100:.1f}%   Timor-Leste share: {tls_share*100:.1f}%   "
          f"PNG+Timor: {top2_share*100:.1f}%")
    print("\niso  economy                          population   share   cum     PM2.5")
    for c in conc:
        print(f"{c['iso3']:<4} {c['country'][:30]:<30} {c['population']:>11,} "
              f"{c['share_of_zero_monitor_pop']*100:>5.1f}% {c['cumulative_share']*100:>5.1f}% "
              f"{c['pm25_exposure_ugm3']:>5.1f}")

    print("\n=== PART (b) — development (GDP-per-capita) confound ===")
    print(f"development LEVEL series found on disk: "
          f"{dev_series if dev_series else 'NONE'}")
    print(f"WDI GDP per capita fetched/cache: {GDP_PC_CACHE}")
    print(f"partial frame, monitored economies with GDP pc: n={n_gdp_partial}")
    print("\nrank correlations (Spearman rho, hand-computed; descriptive only):")
    print(f"  gap-score   vs PM2.5 exposure          : {rho_gap_pm:+.4f}  (n={n1})")
    print(f"  gap-score   vs log10(population)        : {rho_gap_logpop:+.4f}  (n={n2})")
    print(f"  gap-score   vs log10(people/monitor)*   : {rho_gap_logppm:+.4f}  (n={n3})   *economies with >=1 monitor")
    print(f"  log(ppl/mon) vs PM2.5 exposure*         : {rho_logppm_pm:+.4f}  (n={n4})   *economies with >=1 monitor")
    print(f"  log(ppl/mon) vs log10(GDP pc)*          : {rho_logppm_loggdp:+.4f}  (n={n_gdp_partial})   *economies with >=1 monitor + GDP")
    print(f"  gap-score    vs log10(GDP pc)*          : {rho_gap_loggdp_wm:+.4f}  (n={n_gdp_partial})   *economies with >=1 monitor + GDP")
    print("\nGDP partial: log10(people/monitor) = a + b*log10(GDP pc)")
    print(f"  intercept={intercept:.4f}  slope={slope:.4f}")
    print("  top positive residuals (more people per monitor than GDP predicts):")
    for r in residual_rows[:5]:
        print(f"    {r['iso3']:<3} {r['country'][:24]:<24} residual={r['log10_people_per_monitor_residual']:+.3f} "
              f"people/monitor={r['people_per_monitor']:,.0f} GDPpc={r['gdp_pc_current_usd']:,.0f}")
    if "unavailable" not in scipy_check:
        print(f"  scipy cross-check (rho): {scipy_check}")

    print(f"\nWrote {OUT}/air-monitoring-concentration-deepening.json + .csv")


if __name__ == "__main__":
    main()
