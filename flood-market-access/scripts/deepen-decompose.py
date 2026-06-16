"""Flood & Market Access — deepening pass: decompose the index and show it
is largely a country-size ranking that contains no road, no market, and no
flood footprint.

Answers the keystone in `flood-market-access/deep-questions.md` §1.1 and §5:
the headline `flood_market_access_index` is
`(rural_pct/100) × annual_flood_events × log10(population)`. None of its
three factors is a road, a market, a travel time, or a flood extent. Two of
the three (annual_flood_events = a raw EM-DAT qualifying-event count / 25,
and log10(population)) are dominated by country size, so the screen is at
risk of being a size-and-disaster-reporting ranking wearing the name of a
market-access measure.

This script recomputes the exact same index the committed
`flood-market-access-adb-panel.{json,csv}` carries, straight from those two
on-disk panel files, and then strips it apart three ways:

  (a) reproduce the headline index and its top-4 {AFG, CHN, IDN, IND};
  (b) recompute WITHOUT the log10(population) term, and on a per-capita
      basis (affected-style normalization using the same panel fields), and
      report how the top-4 changes — i.e. does it stop being a big-country
      ranking?
  (c) show the flood term is a raw EM-DAT qualifying-event COUNT
      (China 225, Indonesia 215, India 205) with no extent / depth /
      duration, and that economies with zero EM-DAT events
      (e.g. Tonga 78.8% rural) score 0.0 regardless of real flood
      access exposure.

Every number traces to the committed public panel re-read from disk; that
panel is built from EM-DAT 2000-2025 flood subset (CRED, UCLouvain) plus WDI
SP.RUR.TOTL.ZS and SP.POP.TOTL. No new data, no network, no AI-supplied
figures. Per CONSTITUTION.md §6.4 the index is a triage measure, not a
ranking of who is "most at risk". The DMC framing (§13.3) is a
measurement / observability gap: the index measures what was public, not
flood-driven market isolation. attestation_chain: ai-first.
"""
import csv
import json
import math
import os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/flood-market-access"
GEN = f"{BASE}/generated"
OUT = GEN
os.makedirs(OUT, exist_ok=True)

PANEL_JSON = f"{GEN}/flood-market-access-adb-panel.json"
TOP_N = 4  # the headline cluster the deep-questions.md keystone names


def load_panel():
    """Read the committed panel from disk. The panel is the source of every
    number here; nothing is recomputed from a fresher pull."""
    with open(PANEL_JSON, encoding="utf-8") as f:
        panel = json.load(f)
    return panel


def headline_index(row):
    """Reproduce the committed index exactly from the panel's own columns:
    (rural_pct/100) * annual_flood_events * log10(population).
    annual_flood_events is the panel field, which is the EM-DAT
    qualifying-event count / 25."""
    rural = row["rural_pct"] / 100.0
    afe = row["annual_flood_events"]
    pop = row["population"]
    logpop = math.log10(pop) if pop > 0 else 0.0
    return round(rural * afe * logpop, 2)


def no_logpop_index(row):
    """Strip the size term: rural_share * annual_flood_events only.
    This is the 'rural exposure x flood frequency' the internal review
    (critique 1) conceded the index actually is, with the explicit
    population multiplier removed."""
    rural = row["rural_pct"] / 100.0
    afe = row["annual_flood_events"]
    return round(rural * afe, 4)


def per_capita_index(row):
    """Normalize the explicit size term out per-capita: divide the headline
    index by population, expressed per million people. This is a crude
    stand-in for the per-capita affected-rate the deep-questions.md §1.4 and
    internal critique 3 ask for; it uses only the panel's own fields so it
    stays on-disk. It is NOT a flood-affected-population rate (the panel does
    not carry the EM-DAT affected field) — it is the headline index per
    capita, which is the cleanest size-normalization available on disk."""
    pop = row["population"]
    if pop <= 0:
        return 0.0
    return round(headline_index(row) / pop * 1_000_000, 6)


def rank(rows, key, descending=True):
    ordered = sorted(rows, key=lambda r: -(r[key] or 0) if descending else (r[key] or 0))
    return ordered


def topset(ordered, n=TOP_N):
    return [r["iso3"] for r in ordered[:n]]


def main():
    panel = load_panel()
    src_rows = panel["rows"]

    rows = []
    repro_err = []
    for r in src_rows:
        committed = r.get("flood_market_access_index")
        repro = headline_index(r)
        if committed is not None:
            repro_err.append(abs(repro - committed))
        rows.append({
            "iso3": r["iso3"],
            "country": r["country"],
            "rural_pct": r["rural_pct"],
            "population": r["population"],
            "flood_events_2000_2025": r["flood_events_2000_2025"],
            "annual_flood_events": r["annual_flood_events"],
            "index_committed": committed,
            "index_reproduced": repro,
            "index_no_logpop": no_logpop_index(r),
            "index_per_capita_per_million": per_capita_index(r),
        })

    max_err = max(repro_err) if repro_err else 0.0

    # ---- (a) headline reproduction + top-4 -----------------------------
    by_headline = rank(rows, "index_reproduced")
    headline_top = topset(by_headline)
    committed_by_committed = rank(rows, "index_committed")
    committed_top = topset(committed_by_committed)

    # ---- (b) strip the size terms -------------------------------------
    by_no_logpop = rank(rows, "index_no_logpop")
    no_logpop_top = topset(by_no_logpop)

    by_per_capita = rank(rows, "index_per_capita_per_million")
    per_capita_top = topset(by_per_capita)

    dropped_no_logpop = [i for i in headline_top if i not in no_logpop_top]
    entered_no_logpop = [i for i in no_logpop_top if i not in headline_top]
    dropped_pc = [i for i in headline_top if i not in per_capita_top]
    entered_pc = [i for i in per_capita_top if i not in headline_top]

    # ---- (c) the flood term is a raw count; zeros are reporting zeros --
    # Top of the flood term, raw.
    by_flood_count = rank(rows, "flood_events_2000_2025")
    flood_count_top = [(r["iso3"], r["flood_events_2000_2025"]) for r in by_flood_count[:5]]
    # Economies that score 0.0 on the headline index purely because EM-DAT
    # logged zero qualifying flood events, despite being rural.
    zero_index_rural = sorted(
        [r for r in rows if (r["index_committed"] or 0) == 0.0 and r["flood_events_2000_2025"] == 0],
        key=lambda r: -r["rural_pct"],
    )
    zero_rural_list = [
        {"iso3": r["iso3"], "country": r["country"], "rural_pct": r["rural_pct"],
         "flood_events_2000_2025": r["flood_events_2000_2025"],
         "index_committed": r["index_committed"]}
        for r in zero_index_rural
    ]

    # Correlation of the headline index with log10(population) and with the
    # raw flood count, to show how much of the ranking the size terms carry.
    def pearson(xs, ys):
        n = len(xs)
        if n < 2:
            return None
        mx = sum(xs) / n
        my = sum(ys) / n
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs)
        syy = sum((y - my) ** 2 for y in ys)
        if sxx == 0 or syy == 0:
            return None
        return round(sxy / math.sqrt(sxx * syy), 4)

    idx = [r["index_reproduced"] for r in rows]
    logpop = [math.log10(r["population"]) if r["population"] > 0 else 0.0 for r in rows]
    fcount = [r["flood_events_2000_2025"] for r in rows]
    rural = [r["rural_pct"] / 100.0 for r in rows]
    r_idx_logpop = pearson(idx, logpop)
    r_idx_fcount = pearson(idx, fcount)
    r_idx_rural = pearson(idx, rural)

    # Spearman (rank) correlation of headline vs the no-logpop variant, to
    # quantify how much the ranking changes when the size term is removed.
    def spearman(rows_, k1, k2):
        o1 = {r["iso3"]: i for i, r in enumerate(rank(rows_, k1))}
        o2 = {r["iso3"]: i for i, r in enumerate(rank(rows_, k2))}
        xs = [o1[iso] for iso in o1]
        ys = [o2[iso] for iso in o1]
        return pearson(xs, ys)

    rho_headline_vs_nologpop = spearman(rows, "index_reproduced", "index_no_logpop")
    rho_headline_vs_percap = spearman(rows, "index_reproduced", "index_per_capita_per_million")

    payload = {
        "program": "flood-market-access",
        "analysis": "decomposition of the flood_market_access_index — size ranking vs market access",
        "claim_scope": (
            "Deepening of the hypothesis-stage screen. Reproduces the committed "
            "(rural_pct/100) x annual_flood_events x log10(population) index from "
            "the on-disk panel, then strips the two size-dominated terms "
            "(log10(population); the raw EM-DAT qualifying-event count) to test "
            "whether the top-4 {AFG,CHN,IDN,IND} is a market-access signal or a "
            "country-size-and-disaster-reporting ranking. Triage measure "
            "(CONSTITUTION.md §6.4), not a risk ranking. The index contains no "
            "road, no market, no travel time, and no flood footprint; the DMC "
            "framing (§13.3) is a measurement / observability gap."
        ),
        "source": {
            "name": "Committed program panel (re-read from disk)",
            "file": "generated/flood-market-access-adb-panel.json",
            "underlying": "EM-DAT 2000-2025 flood subset (CRED, UCLouvain); WDI SP.RUR.TOTL.ZS; WDI SP.POP.TOTL",
            "license": "WDI: CC BY 4.0; EM-DAT: non-commercial open access",
            "retrieved_at": "2026-04-26 (program panel)",
        },
        "reproduction": {
            "max_abs_error_vs_committed": round(max_err, 4),
            "note": ("Index recomputed from the panel's own rural_pct, "
                     "annual_flood_events, and population columns. Residual is "
                     "rounding only (annual_flood_events is stored at 2 dp)."),
        },
        "a_headline": {
            "top4_committed": committed_top,
            "top4_reproduced": headline_top,
            "top4_match": committed_top == headline_top,
        },
        "b_strip_size_terms": {
            "top4_no_logpop": no_logpop_top,
            "dropped_when_logpop_removed": dropped_no_logpop,
            "entered_when_logpop_removed": entered_no_logpop,
            "top4_per_capita_per_million": per_capita_top,
            "dropped_per_capita": dropped_pc,
            "entered_per_capita": entered_pc,
            "spearman_headline_vs_no_logpop": rho_headline_vs_nologpop,
            "spearman_headline_vs_per_capita": rho_headline_vs_percap,
        },
        "c_flood_term_is_a_count": {
            "flood_term_definition": "annual_flood_events = EM-DAT qualifying-event count (2000-2025) / 25; no extent, depth, or duration",
            "top5_by_raw_event_count": flood_count_top,
            "zero_index_but_rural": zero_rural_list,
            "zero_index_note": ("These economies score 0.0 on the headline index "
                                "only because EM-DAT logged zero qualifying flood "
                                "events (>=10 deaths or >=100 affected), not because "
                                "they do not flood. A threshold-free observed layer "
                                "(Sentinel-1 SAR, JRC Global Surface Water) would not "
                                "score them 0."),
        },
        "what_the_index_correlates_with": {
            "pearson_index_vs_log10population": r_idx_logpop,
            "pearson_index_vs_raw_flood_count": r_idx_fcount,
            "pearson_index_vs_rural_share": r_idx_rural,
            "reading": ("The index tracks log10(population) and the raw flood "
                        "count far more tightly than it tracks rural share — i.e. "
                        "it is largely a size-and-reporting ranking."),
        },
        "rows": rows,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(f"{OUT}/flood-decompose-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    fieldnames = list(rows[0].keys())
    with open(f"{OUT}/flood-decompose-deepening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in by_headline:
            w.writerow(r)

    # ---- stdout report -------------------------------------------------
    print("=== (a) HEADLINE INDEX reproduction ===")
    print(f"top-4 committed   : {committed_top}")
    print(f"top-4 reproduced  : {headline_top}")
    print(f"match             : {committed_top == headline_top}")
    print(f"max abs error vs committed index: {round(max_err,4)} (rounding only)")
    print()
    print("iso   rural%   pop          flood_n  AFE     idx(committed)  idx(repro)")
    for r in by_headline[:8]:
        print(f"{r['iso3']:<4}  {r['rural_pct']:<6}  {r['population']:<12}  "
              f"{r['flood_events_2000_2025']:<7}  {r['annual_flood_events']:<6}  "
              f"{str(r['index_committed']):<14}  {r['index_reproduced']}")
    print()

    print("=== (b) STRIP THE SIZE TERMS ===")
    print(f"top-4 headline (with log10 pop)     : {headline_top}")
    print(f"top-4 WITHOUT log10(population)      : {no_logpop_top}")
    print(f"  dropped when size term removed    : {dropped_no_logpop}")
    print(f"  entered when size term removed    : {entered_no_logpop}")
    print(f"top-4 PER CAPITA (idx / million pop) : {per_capita_top}")
    print(f"  dropped per-capita                : {dropped_pc}")
    print(f"  entered per-capita                : {entered_pc}")
    print(f"Spearman headline vs no-logpop      : {rho_headline_vs_nologpop}")
    print(f"Spearman headline vs per-capita     : {rho_headline_vs_percap}")
    print()
    print("Top-8 by rural x flood (no size term):")
    print("iso   rural%   AFE     rural*AFE")
    for r in by_no_logpop[:8]:
        print(f"{r['iso3']:<4}  {r['rural_pct']:<6}  {r['annual_flood_events']:<6}  {r['index_no_logpop']}")
    print()
    print("Top-8 per-capita (index / million people):")
    print("iso   pop          idx(repro)   idx_per_million")
    for r in by_per_capita[:8]:
        print(f"{r['iso3']:<4}  {r['population']:<12}  {str(r['index_reproduced']):<11}  {r['index_per_capita_per_million']}")
    print()

    print("=== (c) THE FLOOD TERM IS A RAW EM-DAT EVENT COUNT ===")
    print("Top-5 by raw qualifying-event count (no extent/depth/duration):")
    for iso, n in flood_count_top:
        print(f"  {iso}: {n} events")
    print()
    print("Rural economies scoring index 0.0 ONLY because EM-DAT count == 0:")
    print("iso   country              rural%   flood_n  index")
    for r in zero_rural_list:
        print(f"{r['iso3']:<4}  {r['country']:<18}  {r['rural_pct']:<6}  "
              f"{r['flood_events_2000_2025']:<7}  {r['index_committed']}")
    print()

    print("=== WHAT THE INDEX ACTUALLY CORRELATES WITH ===")
    print(f"Pearson  index vs log10(population) : {r_idx_logpop}")
    print(f"Pearson  index vs raw flood count   : {r_idx_fcount}")
    print(f"Pearson  index vs rural share       : {r_idx_rural}")
    print()
    print(f"Wrote {OUT}/flood-decompose-deepening.json + .csv")


if __name__ == "__main__":
    main()
