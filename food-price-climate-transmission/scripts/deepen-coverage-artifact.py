"""Food Price-Climate Transmission — deepening pass: the joint high-high
set as a coverage artifact.

Answers the keystone in `food-price-climate-transmission/deep-questions.md`
§5.1: the reformulated headline ("LAO + PAK in the joint top-N of CPI
inflation AND agricultural-imports share, stable across every N from 3 to
10") only ranks the DMCs that happen to hold BOTH WDI indicators in a
compatible window. The screen is an intersection of two rankings; an
intersection is silent about every economy missing on either axis. The
question: is "LAO + PAK stable" a fact about food prices, or a fact about
which two economies had both numbers on disk?

This script does three on-disk recomputations, all from the same committed
public caches the headline uses (WDI FP.CPI.TOTL.ZG and
TM.VAL.AGRI.ZS.UN, lastupdated 2026-04-08, CC BY 4.0), re-read from the
program cache:

  (a) COVERAGE LEDGER. For each DMC, what does the cache hold on each
      indicator (latest year), and which DMCs are dropped from the joint
      ranking because they are missing the OTHER leg. Surfaces the
      economies that would plausibly enter the high-high set if observed:
      Tajikistan (ag-imports 4.12%, above Pakistan; no CPI in the extract),
      Vanuatu (CPI 11.18%; no ag-imports), Micronesia (CPI 5.41%; no
      ag-imports).

  (b) FILL THE MISSING LEG. Re-run the intersection after filling each
      dropped economy's missing leg from ANY OTHER YEAR present in the same
      cached WDI series, then re-rank. Tests whether the gap is a vintage
      gap (fillable) or a total absence (not fillable).

  (c) COMMON-VINTAGE re-run. Restrict both indicators to a single shared
      year and re-run the intersection, to see whether the stale-denominator
      mixing (Bangladesh's 2018 import share against a 2024 CPI) is what
      keeps the pair together.

Per CONSTITUTION.md §6.4 the rank intersection is a triage qualifier, not a
country food-security ranking; per §13.3 the framing is a measurement /
coverage gap, not a DMC deficiency. Every number traces to the committed
cache. No network, no new data, no AI-supplied figures.
attestation_chain: ai-first.
"""
import json
import csv
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("D:/Users/Raymond/OneDrive/Desktop/ADB/Research/food-price-climate-transmission")
CACHE = ROOT / ".cache"
OUT = ROOT / "generated"
os.makedirs(OUT, exist_ok=True)

# Same DMC roster + names as process-food.py / reformulated.py.
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


def load_series(path):
    """Return {iso3: {year: value}} for every ADB DMC present in a cached
    WDI extract. Mirrors process-food.py's parser but keeps ALL years, not
    just the latest, so we can test year-fills and common vintages."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    out = defaultdict(dict)
    if not isinstance(d, list) or len(d) < 2:
        return out
    for row in d[1]:
        iso = row.get("countryiso3code")
        if iso not in ADB_NAMES:
            continue
        if not isinstance(row.get("value"), (int, float)):
            continue
        out[iso][int(row["date"])] = float(row["value"])
    return out


def latest(series_by_iso, iso):
    """Latest-year (value, year) for one DMC, the rule process-food.py uses."""
    yrs = series_by_iso.get(iso)
    if not yrs:
        return None, None
    y = max(yrs)
    return yrs[y], y


def intersection_topN(cpi_vals, imp_vals, N):
    """Joint high-high set: DMCs in top-N of BOTH dicts {iso: value}."""
    cpi_rank = sorted(cpi_vals, key=lambda k: -cpi_vals[k])
    imp_rank = sorted(imp_vals, key=lambda k: -imp_vals[k])
    return sorted(set(cpi_rank[:N]) & set(imp_rank[:N]))


def main():
    cpi = load_series(CACHE / "wdi_food_inflation.json")      # FP.CPI.TOTL.ZG
    imp = load_series(CACHE / "wdi_ag_imports.json")          # TM.VAL.AGRI.ZS.UN

    # ----- (a) COVERAGE LEDGER ------------------------------------------------
    # Latest-year value of each indicator per DMC, exactly the panel's rule.
    ledger = []
    for iso, name in sorted(ADB_NAMES.items(), key=lambda x: x[1]):
        cv, cy = latest(cpi, iso)
        iv, iy = latest(imp, iso)
        ledger.append({
            "iso3": iso, "country": name,
            "cpi_pct": round(cv, 2) if cv is not None else None, "cpi_year": cy,
            "ag_imports_pct_merch": round(iv, 2) if iv is not None else None, "ag_year": iy,
            "has_cpi": cv is not None, "has_imp": iv is not None,
            "in_joint_universe": cv is not None and iv is not None,
        })

    have_cpi = {r["iso3"] for r in ledger if r["has_cpi"]}
    have_imp = {r["iso3"] for r in ledger if r["has_imp"]}
    joint_universe = sorted(have_cpi & have_imp)
    dropped_no_cpi = sorted([r["iso3"] for r in ledger if r["has_imp"] and not r["has_cpi"]])
    dropped_no_imp = sorted([r["iso3"] for r in ledger if r["has_cpi"] and not r["has_imp"]])
    neither = sorted([r["iso3"] for r in ledger if not r["has_cpi"] and not r["has_imp"]])

    print("=" * 78)
    print("(a) COVERAGE LEDGER — who has each indicator, who is dropped")
    print("=" * 78)
    print(f"DMC roster                         : {len(ADB_NAMES)}")
    print(f"Have CPI (FP.CPI.TOTL.ZG)          : {len(have_cpi)}")
    print(f"Have ag-imports (TM.VAL.AGRI.ZS.UN): {len(have_imp)}")
    print(f"Joint universe (BOTH, ranked)      : {len(joint_universe)}  -> {joint_universe}")
    print(f"Dropped: have ag-imports, NO CPI   : {dropped_no_cpi}")
    print(f"Dropped: have CPI, NO ag-imports   : {dropped_no_imp}")
    print(f"Dropped: neither indicator         : {neither}")

    # Where would the dropped economies rank on the leg they DO have?
    # Build latest-year value dicts over the joint universe + each dropped DMC.
    cpi_latest = {r["iso3"]: r["cpi_pct"] for r in ledger if r["has_cpi"]}
    imp_latest = {r["iso3"]: r["ag_imports_pct_merch"] for r in ledger if r["has_imp"]}

    def rank_of(iso, valdict):
        order = sorted(valdict, key=lambda k: -valdict[k])
        return order.index(iso) + 1 if iso in order else None

    print("\nDropped economies, ranked on the single leg they DO hold:")
    print(f"  (CPI ranking spans {len(cpi_latest)} DMCs; "
          f"ag-imports ranking spans {len(imp_latest)} DMCs)")
    for iso in dropped_no_cpi:
        print(f"  {iso} ({ADB_NAMES[iso]:<12}): ag-imports {imp_latest[iso]:>5}%  "
              f"= rank {rank_of(iso, imp_latest)}/{len(imp_latest)} on the import axis; "
              f"CPI absent -> cannot enter joint set")
    for iso in dropped_no_imp:
        print(f"  {iso} ({ADB_NAMES[iso]:<12}): CPI        {cpi_latest[iso]:>5}%  "
              f"= rank {rank_of(iso, cpi_latest)}/{len(cpi_latest)} on the CPI axis; "
              f"ag-imports absent -> cannot enter joint set")

    # ----- committed (latest-year) intersection, the headline -----------------
    print("\n" + "=" * 78)
    print("COMMITTED intersection (latest-year per DMC, the panel's rule)")
    print("=" * 78)
    committed_runs = {}
    for N in (3, 5, 8, 10):
        s = intersection_topN(cpi_latest, imp_latest, N)
        committed_runs[N] = s
        print(f"  top-{N:<2} intersection: {s}")
    committed_common = sorted(set.intersection(*[set(committed_runs[N]) for N in committed_runs]))
    print(f"  common across N in [3,10]: {committed_common}")

    # ----- (b) FILL THE MISSING LEG FROM ANY OTHER YEAR -----------------------
    print("\n" + "=" * 78)
    print("(b) FILL MISSING LEG from any other year present in the cache, re-rank")
    print("=" * 78)
    cpi_filled = dict(cpi_latest)
    imp_filled = dict(imp_latest)
    fill_log = []
    for iso in dropped_no_cpi:                       # need a CPI from any year
        yrs = cpi.get(iso, {})
        if yrs:
            y = max(yrs)
            cpi_filled[iso] = round(yrs[y], 2)
            fill_log.append((iso, "CPI", cpi_filled[iso], y, "filled from cache"))
        else:
            fill_log.append((iso, "CPI", None, None, "NO value in any cached year"))
    for iso in dropped_no_imp:                       # need an ag-import from any year
        yrs = imp.get(iso, {})
        if yrs:
            y = max(yrs)
            imp_filled[iso] = round(yrs[y], 2)
            fill_log.append((iso, "ag-imports", imp_filled[iso], y, "filled from cache"))
        else:
            fill_log.append((iso, "ag-imports", None, None, "NO value in any cached year"))

    for iso, leg, val, yr, note in fill_log:
        vs = f"{val}%" if val is not None else "  -  "
        ys = f"(year {yr})" if yr is not None else ""
        print(f"  {iso} ({ADB_NAMES[iso]:<12}) {leg:<11}: {vs:<8} {ys:<12} {note}")

    fillable = sorted({iso for iso, _, v, _, _ in fill_log if v is not None})
    unfillable = sorted({iso for iso, _, v, _, _ in fill_log if v is None})
    print(f"\n  Fillable from another cached year : {fillable if fillable else '(none)'}")
    print(f"  Unfillable (indicator wholly absent): {unfillable}")

    print("\n  Intersection AFTER filling every fillable leg:")
    filled_runs = {}
    for N in (3, 5, 8, 10):
        s = intersection_topN(cpi_filled, imp_filled, N)
        filled_runs[N] = s
        delta = sorted(set(s) - set(committed_runs[N]))
        note = f"  (+{delta} vs committed)" if delta else "  (unchanged vs committed)"
        print(f"  top-{N:<2} intersection: {s}{note}")
    filled_common = sorted(set.intersection(*[set(filled_runs[N]) for N in filled_runs]))
    print(f"  common across N in [3,10]: {filled_common}")

    # ----- (c) COMMON-VINTAGE re-run ------------------------------------------
    # For each candidate year y, intersect DMCs that have BOTH indicators in y.
    print("\n" + "=" * 78)
    print("(c) COMMON-VINTAGE re-run — both indicators from the SAME year y")
    print("=" * 78)
    years = sorted({yy for s in (cpi, imp) for iso in s for yy in s[iso]}, reverse=True)
    common_vintage = {}
    for y in years:
        cpi_y = {iso: round(cpi[iso][y], 2) for iso in cpi if y in cpi[iso]}
        imp_y = {iso: round(imp[iso][y], 2) for iso in imp if y in imp[iso]}
        both_y = sorted(set(cpi_y) & set(imp_y))
        if len(both_y) < 5:
            continue
        top5 = intersection_topN(cpi_y, imp_y, 5)
        top8 = intersection_topN(cpi_y, imp_y, 8)
        common_vintage[y] = {"n_both": len(both_y), "top5": top5, "top8": top8}
        print(f"  year {y}: {len(both_y):>2} DMCs have both | "
              f"top-5 joint = {top5} | top-8 joint = {top8}")

    # ----- conclusion fields --------------------------------------------------
    lao_pak_committed = {"LAO", "PAK"}.issubset(set(committed_common))
    lao_pak_filled = {"LAO", "PAK"}.issubset(set(filled_common))
    print("\n" + "=" * 78)
    print("CONCLUSION FIELDS")
    print("=" * 78)
    print(f"  'LAO+PAK' common to all committed N : {lao_pak_committed}")
    print(f"  'LAO+PAK' common after filling legs : {lao_pak_filled}")
    print(f"  Economies with a high single leg but excluded for the missing one:")
    print(f"    TJK ag-imports {imp_latest.get('TJK')}% (rank {rank_of('TJK', imp_latest)}/{len(imp_latest)}), CPI absent")
    print(f"    VUT CPI {cpi_latest.get('VUT')}% (rank {rank_of('VUT', cpi_latest)}/{len(cpi_latest)}), ag-imports absent")
    print(f"    FSM CPI {cpi_latest.get('FSM')}% (rank {rank_of('FSM', cpi_latest)}/{len(cpi_latest)}), ag-imports absent")

    payload = {
        "program": "food-price-climate-transmission",
        "analysis": "joint high-high intersection as a coverage artifact (deep-questions.md §5.1)",
        "claim_scope": (
            "Deepening of the reformulated joint-vulnerability screen. Recomputes "
            "the identical CPI x ag-imports rank intersection the headline uses, "
            "but exposes (a) which DMCs are dropped for missing one leg, (b) the "
            "set after filling each missing leg from any other cached year, and "
            "(c) the set restricted to a common vintage. Triage qualifier "
            "(CONSTITUTION.md §6.4), not a food-security ranking; measurement/"
            "coverage-gap framing (§13.3)."
        ),
        "sources": {
            "wdi_cpi": "WDI FP.CPI.TOTL.ZG (Inflation, consumer prices, annual %), CC BY 4.0",
            "wdi_ag_imports": "WDI TM.VAL.AGRI.ZS.UN (Agricultural raw materials imports, % of merchandise imports), CC BY 4.0",
            "cache_lastupdated": "2026-04-08 (program cache, both extracts)",
            "note_indicator_label": (
                "TM.VAL.AGRI.ZS.UN is 'agricultural RAW MATERIALS imports', not food "
                "imports; the import axis does not measure the food-import exposure the "
                "transmission claim implies."
            ),
        },
        "roster_n": len(ADB_NAMES),
        "have_cpi_n": len(have_cpi),
        "have_imp_n": len(have_imp),
        "joint_universe": joint_universe,
        "joint_universe_n": len(joint_universe),
        "dropped_have_imp_no_cpi": dropped_no_cpi,
        "dropped_have_cpi_no_imp": dropped_no_imp,
        "dropped_neither": neither,
        "committed_runs": {str(k): v for k, v in committed_runs.items()},
        "committed_common_across_N": committed_common,
        "fill_log": [
            {"iso3": iso, "leg": leg, "filled_value": v, "filled_year": yr, "note": note}
            for iso, leg, v, yr, note in fill_log
        ],
        "fillable": fillable,
        "unfillable_indicator_absent": unfillable,
        "filled_runs": {str(k): v for k, v in filled_runs.items()},
        "filled_common_across_N": filled_common,
        "common_vintage_runs": {str(k): v for k, v in common_vintage.items()},
        "lao_pak_common_committed": lao_pak_committed,
        "lao_pak_common_after_fill": lao_pak_filled,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (OUT / "food-price-coverage-deepening.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Flat ledger CSV.
    with open(OUT / "food-price-coverage-deepening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ledger[0].keys()))
        w.writeheader()
        for r in ledger:
            w.writerow(r)

    print(f"\nWrote {OUT}/food-price-coverage-deepening.json + .csv")


if __name__ == "__main__":
    main()
