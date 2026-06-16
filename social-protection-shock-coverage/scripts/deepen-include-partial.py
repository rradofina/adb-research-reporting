"""Social Protection Shock Coverage — deepening pass: the dropped-leg artifact.

Answers the keystone in `social-protection-shock-coverage/deep-questions.md`
§1.1 (and §7). The headline names five DMCs — Bangladesh, Lao PDR, Myanmar,
Pakistan, Philippines — as the "top-5 shock-payment-readiness gap." But that
named set is NOT the descending order of the `shock_payment_readiness_gap`
value in the committed panel.

`process-sp.py` line 58 one-legged-averages economies missing a component:

    mean_readiness = (sp_v + acc_v)/2 if (s and a) else (sp_v if s else acc_v)

So an economy with only ASPIRE SP coverage (e.g. Vanuatu, no Findex account)
is scored on SP alone; an economy with only Findex account ownership (e.g.
Tajikistan, no ASPIRE SP coverage) is scored on account alone. The gap is
still computed and the economy still appears in the panel — but the published
"cluster" of five is silently restricted to economies that have BOTH WDI legs
populated. Vanuatu (gap ~13.6, the #2 value) and Tajikistan (gap ~3.7, the #5
value) out-rank Philippines (~2.8) and Bangladesh (~2.7) by the panel's own
metric, yet neither appears in the named five.

This script recomputes the EXACT same `shock_payment_readiness_gap` that
`process-sp.py` produces — same WDI loader (most-recent year per indicator),
same one-legged-average formula — for every economy that has at least the
poverty leg. It then:

  1. ranks all economies by gap value (the true value-ranked order),
  2. labels which legs each economy actually has (both / sp-only / acc-only),
  3. marks which economies are in the headline five vs excluded,
  4. flags every economy excluded from the named five *purely* because it is
     missing a leg yet out-ranks a named member on the value,
  5. as a robustness variant, re-ranks imputing the missing leg at the
     rankable-set mean of that leg (a documented imputation, NOT a headline),
     and reports whether VUT/TJK still displace PHL/BGD.

Every number traces to the committed WDI cache (World Bank WDI / ASPIRE /
Global Findex 2021, CC BY 4.0) re-read from the program cache — the same
source the headline uses. No new data, no network, no AI-supplied figures.
The readiness-gap is a triage measure per CONSTITUTION.md §6.4, not a country
quality ranking; per §13.3 the object is whether the index *observes*
shock-payment capacity, a measurement/observability gap. attestation_chain:
ai-first.
"""
import json, csv, os
from datetime import datetime, timezone

CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/social-protection-shock-coverage/.cache"
OUT = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/social-protection-shock-coverage/generated"
os.makedirs(OUT, exist_ok=True)

# Same DMC roster as process-sp.py.
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

# The published "cluster" — the named five in pre-registration.md §1 and
# literature.md §6. NOT derived here; quoted so the script can test the
# headline rather than restate it.
HEADLINE_FIVE = ["BGD", "LAO", "MMR", "PAK", "PHL"]


def load_wdi(path):
    """Identical to process-sp.py load_wdi: most-recent year per indicator
    per country, ADB roster only, numeric values only."""
    try:
        d = json.load(open(path, encoding="utf-8"))
    except FileNotFoundError:
        return {}
    if not isinstance(d, list) or len(d) < 2:
        return {}
    out = {}
    for row in d[1]:
        if not isinstance(row.get("value"), (int, float)):
            continue
        iso = row.get("countryiso3code")
        if iso not in ADB_NAMES:
            continue
        y = int(row.get("date"))
        if iso not in out or y > out[iso]["year"]:
            out[iso] = {"year": y, "value": float(row["value"])}
    return out


def gap_one_legged(p_val, s, a):
    """The committed formula in process-sp.py line 58-59, byte-for-byte logic.
    Returns (gap, mean_readiness, leg_label)."""
    sp_v = (s["value"] or 0) / 100 if s else 0.0
    acc_v = (a["value"] or 0) / 100 if a else 0.0
    if s and a:
        mean_readiness = (sp_v + acc_v) / 2
        leg = "both"
    elif s:
        mean_readiness = sp_v
        leg = "sp-only"
    else:
        mean_readiness = acc_v
        leg = "acc-only"
    gap = round(((p_val or 0) / 100) * (1 - mean_readiness) * 100, 1)
    return gap, mean_readiness, leg


def main():
    sp = load_wdi(f"{CACHE}/wdi_sp_coverage.json")
    acc = load_wdi(f"{CACHE}/wdi_findex_account.json")
    pov = load_wdi(f"{CACHE}/wdi_poverty_215.json")

    # --- Pass 1: committed one-legged gap for every economy with >= poverty leg.
    rows = []
    for iso, name in ADB_NAMES.items():
        s = sp.get(iso)
        a = acc.get(iso)
        p = pov.get(iso)
        if p is None or not (s or a):
            continue  # same exclusion as process-sp.py (gap = None)
        gap, mean_r, leg = gap_one_legged(p["value"], s, a)
        rows.append({
            "iso3": iso, "country": name,
            "poverty_pct": round(p["value"], 4), "poverty_year": p["year"],
            "sp_coverage_pct": round(s["value"], 4) if s else None,
            "sp_year": s["year"] if s else None,
            "findex_account_pct": round(a["value"], 4) if a else None,
            "findex_year": a["year"] if a else None,
            "legs_present": leg,
            "shock_payment_readiness_gap": gap,
            "in_headline_five": iso in HEADLINE_FIVE,
        })

    rows.sort(key=lambda r: -r["shock_payment_readiness_gap"])

    # True value-ranked order.
    print("=== TRUE value-ranked order of shock_payment_readiness_gap ===")
    print("    (every economy with at least the poverty leg; committed one-legged formula)")
    print(f"{'rank':>4}  {'iso':<4} {'economy':<20} {'gap':>6}  {'legs':<8} {'pov':>5} {'sp':>7} {'acc':>7}  hdln5")
    for i, r in enumerate(rows, 1):
        mark = "  <==" if r["in_headline_five"] else ""
        sp_s = f"{r['sp_coverage_pct']:.1f}" if r["sp_coverage_pct"] is not None else "  --"
        acc_s = f"{r['findex_account_pct']:.1f}" if r["findex_account_pct"] is not None else "  --"
        print(f"{i:>4}  {r['iso3']:<4} {r['country'][:20]:<20} {r['shock_payment_readiness_gap']:>6}  "
              f"{r['legs_present']:<8} {r['poverty_pct']:>5} {sp_s:>7} {acc_s:>7}{mark}")

    # --- The keystone test: economies ABOVE the lowest-ranked headline member
    #     that are EXCLUDED from the named five purely for missing a leg.
    headline_rows = [r for r in rows if r["in_headline_five"]]
    headline_ranks = {r["iso3"]: i for i, r in enumerate(rows, 1) if r["in_headline_five"]}
    worst_headline = min(headline_rows, key=lambda r: r["shock_payment_readiness_gap"])
    worst_gap = worst_headline["shock_payment_readiness_gap"]

    excluded_above = [
        r for r in rows
        if not r["in_headline_five"] and r["shock_payment_readiness_gap"] > worst_gap
    ]
    # Of those, which are excluded *purely* because they are missing a leg?
    excluded_missing_leg = [r for r in excluded_above if r["legs_present"] != "both"]

    print("\n=== KEYSTONE: economies that OUT-RANK the lowest headline member but are excluded ===")
    print(f"    lowest-ranked headline member: {worst_headline['iso3']} "
          f"({worst_headline['country']}) gap={worst_gap} at rank {headline_ranks[worst_headline['iso3']]}")
    for r in excluded_above:
        why = f"missing a leg ({r['legs_present']})" if r["legs_present"] != "both" else "has both legs"
        print(f"    {r['iso3']} {r['country'][:18]:<18} gap={r['shock_payment_readiness_gap']:>5}  "
              f"rank {rows.index(r)+1:>2}  legs={r['legs_present']:<8} -> excluded; {why}")

    # Explicit VUT / TJK vs PHL / BGD comparison the keystone asks for.
    by_iso = {r["iso3"]: r for r in rows}
    print("\n=== Explicit VUT / TJK vs PHL / BGD (the named-five tail) ===")
    for iso in ["VUT", "TJK", "PHL", "BGD"]:
        r = by_iso.get(iso)
        if r:
            tag = "NAMED FIVE" if r["in_headline_five"] else "EXCLUDED  "
            print(f"    {iso} {r['country'][:14]:<14} gap={r['shock_payment_readiness_gap']:>5}  "
                  f"rank {rows.index(r)+1:>2}  legs={r['legs_present']:<8} [{tag}]")
    vut, tjk = by_iso.get("VUT"), by_iso.get("TJK")
    phl, bgd = by_iso.get("PHL"), by_iso.get("BGD")
    if all([vut, tjk, phl, bgd]):
        print(f"\n    VUT ({vut['shock_payment_readiness_gap']}) > PHL "
              f"({phl['shock_payment_readiness_gap']})? {vut['shock_payment_readiness_gap'] > phl['shock_payment_readiness_gap']}")
        print(f"    VUT ({vut['shock_payment_readiness_gap']}) > BGD "
              f"({bgd['shock_payment_readiness_gap']})? {vut['shock_payment_readiness_gap'] > bgd['shock_payment_readiness_gap']}")
        print(f"    TJK ({tjk['shock_payment_readiness_gap']}) > PHL "
              f"({phl['shock_payment_readiness_gap']})? {tjk['shock_payment_readiness_gap'] > phl['shock_payment_readiness_gap']}")
        print(f"    TJK ({tjk['shock_payment_readiness_gap']}) > BGD "
              f"({bgd['shock_payment_readiness_gap']})? {tjk['shock_payment_readiness_gap'] > bgd['shock_payment_readiness_gap']}")

    # --- Robustness variant: impute the missing leg at the rankable-set mean
    #     of that leg, then re-rank. Documented imputation; NOT a headline.
    both_rows = [r for r in rows if r["legs_present"] == "both"]
    mean_sp = sum(r["sp_coverage_pct"] for r in both_rows) / len(both_rows)
    mean_acc = sum(r["findex_account_pct"] for r in both_rows) / len(both_rows)

    imp = []
    for r in rows:
        sp_v = (r["sp_coverage_pct"] if r["sp_coverage_pct"] is not None else mean_sp) / 100
        acc_v = (r["findex_account_pct"] if r["findex_account_pct"] is not None else mean_acc) / 100
        mean_r = (sp_v + acc_v) / 2
        g = round((r["poverty_pct"] / 100) * (1 - mean_r) * 100, 1)
        imp.append({**r, "gap_imputed": g})
    imp.sort(key=lambda r: -r["gap_imputed"])
    imp_top5 = [r["iso3"] for r in imp[:5]]

    print("\n=== Robustness variant: impute missing leg at rankable-set mean, re-rank ===")
    print(f"    rankable-set mean SP coverage = {mean_sp:.2f}%, mean Findex account = {mean_acc:.2f}%")
    print(f"{'rank':>4}  {'iso':<4} {'economy':<18} {'gap_imp':>8}  {'(committed gap)':>15}  legs")
    for i, r in enumerate(imp[:12], 1):
        print(f"{i:>4}  {r['iso3']:<4} {r['country'][:18]:<18} {r['gap_imputed']:>8}  "
              f"{r['shock_payment_readiness_gap']:>15}  {r['legs_present']}")
    print(f"\n    Imputed top-5: {imp_top5}")
    print(f"    Headline five: {sorted(HEADLINE_FIVE)}")
    entered = [i for i in imp_top5 if i not in HEADLINE_FIVE]
    dropped = [i for i in HEADLINE_FIVE if i not in imp_top5]
    print(f"    Enter under imputation: {entered}   Drop from headline five: {dropped}")

    # --- Write artifacts.
    payload = {
        "program": "social-protection-shock-coverage",
        "analysis": "dropped-leg artifact — true value-ranked order vs the headline five",
        "claim_scope": (
            "Deepening of the readiness-gap screen. Recomputes the identical "
            "shock_payment_readiness_gap that process-sp.py produces (most-recent "
            "WDI year per indicator; one-legged average for economies missing a "
            "component) for every economy with at least the poverty leg, then "
            "ranks by value and flags every economy excluded from the named five "
            "purely for missing a WDI leg. Triage measure (CONSTITUTION.md §6.4); "
            "a measurement/observability question (§13.3), not a country ranking."
        ),
        "source": {
            "name": "World Bank WDI (ASPIRE per_allsp.cov_pop_tot; Global Findex 2021 "
                    "FX.OWN.TOTL.ZS; poverty SI.POV.DDAY $2.15/day 2017 PPP)",
            "license": "CC BY 4.0",
            "retrieved_at": "2026-04-25 (program cache)",
            "wall_note": "Network blocked; all values re-read from the committed "
                         "program cache, identical to the headline pipeline source.",
        },
        "headline_five": sorted(HEADLINE_FIVE),
        "lowest_ranked_headline_member": {
            "iso3": worst_headline["iso3"], "gap": worst_gap,
            "value_rank": headline_ranks[worst_headline["iso3"]],
        },
        "value_ranked_order": [
            {"rank": i, "iso3": r["iso3"], "country": r["country"],
             "gap": r["shock_payment_readiness_gap"], "legs_present": r["legs_present"],
             "in_headline_five": r["in_headline_five"]}
            for i, r in enumerate(rows, 1)
        ],
        "excluded_but_outrank_lowest_headline": [
            {"iso3": r["iso3"], "country": r["country"],
             "gap": r["shock_payment_readiness_gap"],
             "value_rank": rows.index(r) + 1, "legs_present": r["legs_present"],
             "excluded_purely_for_missing_leg": r["legs_present"] != "both"}
            for r in excluded_above
        ],
        "excluded_for_missing_leg_count": len(excluded_missing_leg),
        "imputation_variant": {
            "rule": "impute missing leg at rankable-set (both-legs) mean of that leg",
            "mean_sp_coverage_pct": round(mean_sp, 4),
            "mean_findex_account_pct": round(mean_acc, 4),
            "imputed_top5": imp_top5,
            "entered_vs_headline": entered,
            "dropped_vs_headline": dropped,
            "rows": [
                {"rank": i, "iso3": r["iso3"], "country": r["country"],
                 "gap_imputed": r["gap_imputed"],
                 "gap_committed": r["shock_payment_readiness_gap"],
                 "legs_present": r["legs_present"]}
                for i, r in enumerate(imp, 1)
            ],
        },
        "rows": rows,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/social-protection-dropped-leg.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    with open(f"{OUT}/social-protection-dropped-leg.csv", "w", encoding="utf-8", newline="") as f:
        fields = ["iso3", "country", "poverty_pct", "poverty_year",
                  "sp_coverage_pct", "sp_year", "findex_account_pct", "findex_year",
                  "legs_present", "shock_payment_readiness_gap", "in_headline_five"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields})
    print(f"\nWrote {OUT}/social-protection-dropped-leg.json + .csv")


if __name__ == "__main__":
    main()
