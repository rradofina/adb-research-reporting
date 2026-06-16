"""Migration & Displacement Signals — deepening pass: emigrant stock as a
SHARE of origin population, not as an absolute count.

Answers the keystone in `migration-displacement-signals/deep-questions.md`
§1.1 (and the §5 "question we are most afraid to ask") with a real
recomputation. The headline ranks *absolute* emigrant stock, and its top
five — IND, CHN, BGD, AFG, PHL — are five of the most populous economies in
scope. The deep question: is the absolute top-5 a migration-intensity
finding, or mostly a population ranking that dissolves into a small-island
ordering once each DMC's emigrant stock is divided by its own population?

This script recomputes the ranking on emigrant stock as a fraction of
origin population. The numerator is the committed program panel's
`emigrant_stock_2024` (UN DESA International Migrant Stock 2024, CC BY 3.0
IGO). The denominator is World Bank WDI `SP.POP.TOTL` (Population, total),
mid-year 2024 — the same indicator the school-heat and climate-health
programs cache. No WDI population file is committed inside this program's
own `.cache/`, so the denominator is read from a sibling program's cached
WDI pull already on disk:
`school-heat-disruption/.cache/wdi_pop.json`. This is on-disk public data,
re-read locally; there is no network call. (Wall-note: the population pull
lives in a sibling program cache rather than this program's; mirroring it
into this program's `.cache/` is a future tidy-up, not a number change.)

Three DMCs — Cook Islands (COK), Niue (NIU), Taiwan (TWN) — have no
`SP.POP.TOTL` value in the WDI cache and are reported with a withheld share
rather than on a fabricated denominator.

Every number traces to committed/cached public sources re-read from disk.
No new data, no network, no AI-supplied figures. Per CONSTITUTION.md §13.3
this is a measurement/observability framing — what the stock matrix can and
cannot resolve about migration intensity — not a ranking of which DMC
migrates "too much." attestation_chain: ai-first.
"""
import csv, json, os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/migration-displacement-signals"
PANEL = f"{BASE}/generated/migration-displacement-adb-panel.json"
# WDI SP.POP.TOTL is not committed in this program's own .cache/. The
# nearest on-disk copy is the school-heat program's cached WDI pull. Same
# indicator (SP.POP.TOTL), same World Bank API vintage (lastupdated
# 2026-04-08). On-disk only; no network.
POP_CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/school-heat-disruption/.cache/wdi_pop.json"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

POP_YEAR = "2024"  # match UN DESA 2024 vintage; fall back to 2023 only if absent


def load_population():
    """iso3 -> (population, year_used). World Bank WDI JSON is [meta, data]."""
    raw = json.load(open(POP_CACHE, encoding="utf-8"))
    data = raw[1]
    indicator = data[0]["indicator"]["id"] if data else "?"
    by_iso_year = {}
    for r in data:
        iso = r.get("countryiso3code")
        y = r.get("date")
        v = r.get("value")
        if iso and v is not None:
            by_iso_year.setdefault(iso, {})[y] = v
    pop = {}
    for iso, years in by_iso_year.items():
        if POP_YEAR in years:
            pop[iso] = (int(round(years[POP_YEAR])), POP_YEAR)
        elif "2023" in years:  # documented fallback
            pop[iso] = (int(round(years["2023"])), "2023")
    return pop, indicator


def main():
    panel = json.loads(open(PANEL, encoding="utf-8").read())
    rows = panel["rows"]
    pop, pop_indicator = load_population()

    # Build per-DMC records: emigrant stock + population + share.
    recs = []
    withheld = []  # (iso, country, emigrant_stock) with no population denominator
    for r in rows:
        iso = r["iso3"]
        country = r["country"]
        emig = r.get("emigrant_stock_2024")
        if emig is None:
            continue
        p = pop.get(iso)
        if p is None:
            withheld.append({"iso3": iso, "country": country,
                             "emigrant_stock_2024": emig,
                             "reason": "no SP.POP.TOTL value in WDI cache (WDI does not report this economy)"})
            continue
        population, pyear = p
        share = emig / population if population else None
        recs.append({
            "iso3": iso, "country": country,
            "emigrant_stock_2024": emig,
            "population_total": population,
            "population_year": pyear,
            "emigrant_share_of_population": round(share, 6) if share is not None else None,
            "emigrant_pct_of_population": round(100.0 * share, 2) if share is not None else None,
        })

    # Two rankings, side by side.
    by_abs = sorted(recs, key=lambda x: -x["emigrant_stock_2024"])
    by_share = sorted(recs, key=lambda x: -x["emigrant_share_of_population"])

    abs_rank = {x["iso3"]: i + 1 for i, x in enumerate(by_abs)}
    share_rank = {x["iso3"]: i + 1 for i, x in enumerate(by_share)}
    for x in recs:
        x["rank_absolute"] = abs_rank[x["iso3"]]
        x["rank_share"] = share_rank[x["iso3"]]

    abs_top5 = [x["iso3"] for x in by_abs[:5]]
    share_top5 = [x["iso3"] for x in by_share[:5]]
    survivors = [i for i in abs_top5 if i in share_top5]
    dropped = [i for i in abs_top5 if i not in share_top5]
    entered = [i for i in share_top5 if i not in abs_top5]

    # Where does each absolute-top-5 DMC land on the share ranking?
    abs_top5_on_share = [(i, share_rank[i],
                          next(x["emigrant_pct_of_population"] for x in recs if x["iso3"] == i))
                         for i in abs_top5]

    payload = {
        "program": "migration-displacement-signals",
        "analysis": "emigrant stock as a share of origin population vs absolute emigrant stock",
        "claim_scope": (
            "Deepening of the absolute emigrant-stock screen. Recomputes the "
            "ranking on emigrant stock divided by origin population. Numerator: "
            "UN DESA International Migrant Stock 2024 emigrant_stock_2024 (committed "
            "panel). Denominator: World Bank WDI SP.POP.TOTL mid-year 2024, read "
            "from an on-disk sibling-program cache (school-heat-disruption). "
            "Measurement/observability framing per CONSTITUTION.md §13.3, not a "
            "fragility or 'migrates-too-much' ranking. Share withheld where WDI "
            "reports no population for the economy."
        ),
        "sources": {
            "numerator": {
                "name": "UN DESA International Migrant Stock 2024",
                "field": "emigrant_stock_2024",
                "license": "CC BY 3.0 IGO",
                "via": "generated/migration-displacement-adb-panel.json",
            },
            "denominator": {
                "name": "World Bank WDI Population, total",
                "indicator": pop_indicator,
                "year": POP_YEAR,
                "license": "CC BY 4.0",
                "via_on_disk": "school-heat-disruption/.cache/wdi_pop.json",
                "wall_note": ("WDI population not committed in this program's own "
                              ".cache/; read from sibling-program cache on disk. "
                              "No network."),
            },
        },
        "absolute_top5": abs_top5,
        "share_top5": share_top5,
        "survivors_in_both_top5": survivors,
        "dropped_from_top5_on_share": dropped,
        "entered_top5_on_share": entered,
        "absolute_top5_position_on_share_ranking": abs_top5_on_share,
        "rows_by_share": by_share,
        "rows_withheld_no_population": withheld,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/migration-per-population-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    flat = [{
        "iso3": x["iso3"], "country": x["country"],
        "emigrant_stock_2024": x["emigrant_stock_2024"],
        "population_total": x["population_total"],
        "population_year": x["population_year"],
        "emigrant_pct_of_population": x["emigrant_pct_of_population"],
        "rank_absolute": x["rank_absolute"],
        "rank_share": x["rank_share"],
    } for x in by_share]
    with open(f"{OUT}/migration-per-population-deepening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(flat[0].keys()))
        w.writeheader()
        for x in flat:
            w.writerow(x)

    # ---- stdout report ----
    print("=== Absolute top-5 (headline):", abs_top5)
    print("=== Share top-5 (deepened)   :", share_top5)
    print("=== Survive both top-5       :", survivors or "(none)")
    print("=== Dropped on share         :", dropped or "(none)")
    print("=== Entered on share         :", entered or "(none)")
    print()
    print("Where the absolute top-5 lands on the SHARE ranking:")
    for iso, rk, pct in abs_top5_on_share:
        nm = next(x["country"] for x in recs if x["iso3"] == iso)
        print(f"  {iso:<4} {nm[:22]:<22} share-rank #{rk:<3} ({pct}% of population)")
    print()
    print("Top 12 by emigrant share of population (the deepened ranking):")
    print(f"  {'rk':>2} {'iso':<4} {'country':<22} {'emig stock':>12} {'population':>14} {'% of pop':>9} {'abs-rk':>7}")
    for i, x in enumerate(by_share[:12], 1):
        print(f"  {i:>2} {x['iso3']:<4} {x['country'][:22]:<22} "
              f"{x['emigrant_stock_2024']:>12,} {x['population_total']:>14,} "
              f"{x['emigrant_pct_of_population']:>8}% {x['rank_absolute']:>7}")
    print()
    print("Bottom of share ranking — the big-population economies the headline elevates:")
    for x in sorted(recs, key=lambda y: y["emigrant_share_of_population"])[:5]:
        print(f"  {x['iso3']:<4} {x['country'][:22]:<22} {x['emigrant_pct_of_population']:>6}% of population "
              f"(abs-rank #{x['rank_absolute']}, share-rank #{x['rank_share']})")
    print()
    print("Withheld (no WDI population denominator on disk):")
    for w_ in withheld:
        print(f"  {w_['iso3']:<4} {w_['country'][:22]:<22} emig={w_['emigrant_stock_2024']:>10,}  — {w_['reason']}")
    print(f"\nWrote {OUT}/migration-per-population-deepening.json + .csv")


if __name__ == "__main__":
    main()
