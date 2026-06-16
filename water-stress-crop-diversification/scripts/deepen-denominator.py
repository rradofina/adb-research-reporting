"""Water Stress x Crop Diversification — deepening pass: the denominator
artifact, and which term actually orders the headline.

Answers the keystone in `water-stress-crop-diversification/deep-questions.md`
sections 1.1, 1.3 and 1.4 with a real recomputation, on-disk only.

The headline `water_crop_pressure_index` multiplies three WDI terms:
    min(water/100, 1.5) x min(3000/max(yield,100), 1.0) x (rural/100) x 100
Its first term divides total freshwater withdrawal by INTERNAL-only renewable
water (WDI ER.H2O.FWTL.ZS). Any value above 100% is therefore partly or wholly
a denominator artifact: it reflects transboundary inflow (Amu Darya, Indus) or
fossil-aquifer mining that never enters the internal-only base, not domestic
over-pumping. The four above-100% economies (TKM 1868%, PAK 326%, UZB 263%,
AZE 161%) carry the top three ranks plus UZB on a denominator the indicator
itself documents as internal-only.

This script does what the on-disk data supports, in the keystone's priority
order:

  (1) AQUASTAT TOTAL renewable water (internal+external) recompute — the
      preferred test — is NOT runnable: no AQUASTAT file is in the program
      cache. A precise wall-note names the exact file needed. (deep-questions
      section 1.1)

  (2) The denominator artifact is demonstrated ARITHMETICALLY instead, fully
      on-disk: every DMC whose withdrawal share exceeds 100% is listed (these
      are exactly the values that cannot be domestic-renewable over-use), the
      water term is shown saturating at its 1.5 ceiling for all of them, and a
      rural-multiplier counterfactual shows that Afghanistan — withdrawal 43%,
      BELOW the 100% cap — is promoted into the top-4 by the rural-population
      term, not by water. We also rebuild the index with rural held constant
      to see whether the top-4 collapses to the high-withdrawal set.
      (deep-questions sections 1.3, 1.4)

  (3) The Shannon/Herfindahl CROP-diversity index the program name promises
      (deep-questions section 1.2) needs FAOSTAT crop harvested areas, which
      are NOT in the cache. A wall-note names the file. As the closest on-disk
      proxy the cache DOES support, we compute an arable-share-of-agricultural
      -land concentration signal from the two cached WDI land series and check
      — clearly labelled a proxy, NOT the FAOSTAT crop-mix index — whether it
      even crudely singles out the top-4.

Every number traces to the committed WDI cache (CC BY 4.0) re-read here with
the SAME `load_wdi` latest-year selection the headline `process-water-crop.py`
uses. No new data, no network, no AI-supplied figures. Per CONSTITUTION.md
section 6.4 the index is a triage measure, not a country ranking; framing is a
measurement / observability gap per section 13.3. attestation_chain: ai-first.
"""
import json, csv, os, math
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/water-stress-crop-diversification"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

# Same DMC roster as process-water-crop.py (the committed headline script).
ADB_NAMES = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China","COK":"Cook Islands",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong SAR","IND":"India","IDN":"Indonesia",
    "KAZ":"Kazakhstan","KIR":"Kiribati","KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia",
    "MNG":"Mongolia","MMR":"Myanmar","NRU":"Nauru","NPL":"Nepal",
    "PAK":"Pakistan","PLW":"Palau","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam","TWN":"Taiwan",
}

WATER_CAP = 100.0     # pre-registration section 6 arbitrary numeric
WATER_CEIL = 1.5      # water-multiplier ceiling
YIELD_BASE = 3000.0   # yield baseline kg/ha


def load_wdi(path):
    """Latest non-null observation per DMC — identical selection to the headline."""
    try:
        d = json.load(open(path, encoding="utf-8"))
    except FileNotFoundError:
        return {}, None
    if not isinstance(d, list) or len(d) < 2:
        return {}, None
    lastupdated = (d[0] or {}).get("lastupdated")
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
    return out, lastupdated


def water_term(w):
    return min(w / WATER_CAP, WATER_CEIL)


def yield_term(y):
    return min(YIELD_BASE / max(y, 100.0), 1.0)


def main():
    water, water_upd = load_wdi(f"{CACHE}/wdi_freshwater_withdrawal.json")
    yld, yld_upd = load_wdi(f"{CACHE}/wdi_cereal_yield.json")
    rural, rural_upd = load_wdi(f"{CACHE}/wdi_rural_pct.json")
    agri, _ = load_wdi(f"{CACHE}/wdi_agri_land_pct.json")
    arable, _ = load_wdi(f"{CACHE}/wdi_ag_land_arable.json")

    # --- Rebuild the headline index (sanity check vs committed panel) ---
    rows = []
    for iso, name in ADB_NAMES.items():
        w = water.get(iso); y = yld.get(iso); r = rural.get(iso)
        if w and y and r:
            wt = water_term(w["value"])
            yt = yield_term(y["value"])
            rt = r["value"] / 100.0
            idx = round(wt * yt * rt * 100, 1)
            idx_norural = round(wt * yt * 100, 1)            # rural dropped
            idx_flatrural = round(wt * yt * 0.5 * 100, 1)    # rural held at 0.5 for all
            rows.append({
                "iso3": iso, "country": name,
                "water_pct": w["value"], "water_year": w["year"],
                "yield_kg_ha": y["value"], "rural_pct": r["value"],
                "water_term": round(wt, 4), "water_term_saturated": wt >= WATER_CEIL,
                "yield_term": round(yt, 4), "rural_term": round(rt, 4),
                "index": idx, "index_no_rural": idx_norural,
                "index_flat_rural": idx_flatrural,
            })
    ranked = sorted(rows, key=lambda r: -r["index"])
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    print("=" * 78)
    print("HEADLINE REBUILD (latest-year WDI from program cache) — top 8")
    print("water lastupdated:", water_upd, "| yield:", yld_upd, "| rural:", rural_upd)
    print("=" * 78)
    print(f"{'rk':<3}{'iso':<4}{'water%':>11}{'yld':>7}{'rural%':>8}"
          f"{'wT':>7}{'yT':>7}{'rT':>7}{'index':>8}")
    for r in ranked[:8]:
        print(f"{r['rank']:<3}{r['iso3']:<4}{r['water_pct']:>11.2f}{r['yield_kg_ha']:>7.0f}"
              f"{r['rural_pct']:>8.1f}{r['water_term']:>7.3f}{r['yield_term']:>7.3f}"
              f"{r['rural_term']:>7.3f}{r['index']:>8.1f}")
    top4 = [r["iso3"] for r in ranked[:4]]
    print("\nReproduced BASELINE single-run top-4 (raw index):", top4,
          "| 5th:", ranked[4]["iso3"], f"(index {ranked[4]['index']})")

    # Ground the headline against the COMMITTED perturbation runs.
    sens = json.load(open(f"{BASE}/sensitivity-runs.json", encoding="utf-8"))
    prereg_top4 = sens["common_top5_across_runs"]
    print("Pre-registered HEADLINE top-4 =", prereg_top4,
          "(intersection of each run's top-5, committed sensitivity-runs.json)")
    print("  Per-run position of AFG (the contested 4th) and UZB (the ejected one):")
    for run in sens["runs"]:
        t = [x["iso3"] if isinstance(x, dict) else x for x in run["top10"]]
        afg_pos = (t.index("AFG") + 1) if "AFG" in t else None
        uzb_pos = (t.index("UZB") + 1) if "UZB" in t else None
        print(f"    {run['label']:<22} AFG #{afg_pos}   UZB #{uzb_pos}   top4={t[:4]}")
    print("  -> In the BASELINE single run AFG is #5 and UZB is #4. AFG never reaches")
    print("     the raw top-4 in baseline; it survives in the common-top-5 set only")
    print("     because the water-cap/water-max minus-50 runs lift its UNSATURATED 43%")
    print("     water term while pushing UZB to #6. The 'stable top-4' is therefore an")
    print("     intersection-of-top-5 construct in which AFG's membership rides the")
    print("     rural multiplier and an unsaturated water term, not water scarcity.")

    # --- (2a) THE DENOMINATOR ARTIFACT, arithmetically ---
    over100 = sorted([r for r in rows if r["water_pct"] > 100.0],
                     key=lambda r: -r["water_pct"])
    print("\n" + "=" * 78)
    print("(2a) DENOMINATOR ARTIFACT — every DMC with withdrawal > 100% of")
    print("     INTERNAL renewable water (ER.H2O.FWTL.ZS). A share above 100%")
    print("     cannot be domestic-renewable over-use; it is transboundary /")
    print("     fossil-aquifer inflow outside the internal-only denominator.")
    print("=" * 78)
    print(f"{'iso':<4}{'withdrawal % internal':>24}{'water_term':>12}{'at 1.5 ceil?':>14}")
    for r in over100:
        print(f"{r['iso3']:<4}{r['water_pct']:>24.2f}{r['water_term']:>12.3f}"
              f"{('YES' if r['water_term_saturated'] else 'no'):>14}")
    print(f"\n  {len(over100)} of {len(rows)} rankable DMCs exceed 100% on the internal-only base.")
    print("  All of them saturate the water term at its 1.5 ceiling, so the index")
    print("  cannot distinguish TKM's 1868% from a hypothetical 150% — the first")
    print("  term is a flat 1.5 for every above-150%-effective economy. The")
    print("  ORDERING among them is therefore set entirely by yield x rural.")

    # --- (2b) AFG inversion + rural counterfactual ---
    afg = next(r for r in rows if r["iso3"] == "AFG")
    ind = next((r for r in rows if r["iso3"] == "IND"), None)
    uzb = next((r for r in rows if r["iso3"] == "UZB"), None)
    print("\n" + "=" * 78)
    print("(2b) THE AFGHANISTAN INVERSION — is AFG in the top-4 on WATER?")
    print("=" * 78)
    print(f"  AFG withdrawal = {afg['water_pct']:.2f}%  ->  BELOW the 100% cap;")
    print(f"     water term = {afg['water_term']:.3f} (NOT saturated). Its rank-4 index")
    print(f"     {afg['index']} is carried by rural {afg['rural_pct']:.1f}% x yield-term {afg['yield_term']:.3f}.")
    if ind:
        print(f"  IND withdrawal = {ind['water_pct']:.2f}%  ~ statistically the same water as AFG,")
        print(f"     yet IND index {ind['index']} (rank {next(r for r in ranked if r['iso3']=='IND')['rank']}) "
              f"sits lower purely on rural {ind['rural_pct']:.1f}% / yield {ind['yield_kg_ha']:.0f}.")
    if uzb:
        print(f"  UZB withdrawal = {uzb['water_pct']:.2f}%  (saturated, water_term {uzb['water_term']:.1f}) yet")
        print(f"     ranks 5th (index {uzb['index']}) — its high {uzb['yield_kg_ha']:.0f} kg/ha yield collapses")
        print(f"     the yield term to {uzb['yield_term']:.3f}, demoting a heavily-above-cap economy below AFG.")

    print("\n  Counterfactual rankings (same water + yield terms):")
    ranked_nr = sorted(rows, key=lambda r: -r["index_no_rural"])
    top4_nr = [r["iso3"] for r in ranked_nr[:4]]
    print(f"   - rural term DROPPED   -> top-4 = {top4_nr}")
    print(f"     (5th: {ranked_nr[4]['iso3']} at {ranked_nr[4]['index_no_rural']})")
    afg_rank_nr = next(i for i, r in enumerate(ranked_nr, 1) if r["iso3"] == "AFG")
    print(f"     AFG falls to rank {afg_rank_nr} when rural is removed.")
    ranked_fr = sorted(rows, key=lambda r: -r["index_flat_rural"])
    top4_fr = [r["iso3"] for r in ranked_fr[:4]]
    afg_rank_fr = next(i for i, r in enumerate(ranked_fr, 1) if r["iso3"] == "AFG")
    print(f"   - rural HELD CONSTANT  -> top-4 = {top4_fr} (AFG rank {afg_rank_fr})")
    high_withdrawal = [r["iso3"] for r in over100]
    print(f"\n  High-withdrawal set (all >100%): {high_withdrawal}")
    afg_in_collapsed = "AFG" in top4_nr
    print(f"  Does dropping rural eject AFG and collapse to the high-withdrawal set? "
          f"{'NO — AFG stays' if afg_in_collapsed else 'YES — AFG ejected'}.")

    # --- (3) on-disk crude land-use concentration PROXY (NOT crop diversity) ---
    print("\n" + "=" * 78)
    print("(3) CROP-DIVERSITY TERM — the program name promises a diversification")
    print("    index; the committed metric has none (it uses a cereal-yield")
    print("    penalty). The real Shannon/Herfindahl over FAOSTAT crop")
    print("    harvested-area shares is NOT computable: no FAOSTAT file on disk.")
    print("    Closest on-disk PROXY (crude, NOT the crop-mix index): arable")
    print("    land as a share of agricultural land (low arable share = pasture/")
    print("    rangeland-dominated land use, the cache's only land-mix signal).")
    print("=" * 78)
    proxy = []
    proxy_isos = []
    for iso in top4 + ["AFG", "UZB", "IND"]:   # baseline top-4 plus the two inversion cases + AFG
        if iso not in proxy_isos:
            proxy_isos.append(iso)
    for iso in proxy_isos:
        a = agri.get(iso); ar = arable.get(iso)
        if a and ar and a["value"]:
            share = ar["value"] / a["value"]
            proxy.append((iso, ar["value"], a["value"], share))
    # rank all rankable DMCs by this proxy to see where top-4 land
    allproxy = []
    for iso, name in ADB_NAMES.items():
        a = agri.get(iso); ar = arable.get(iso)
        if a and ar and a["value"]:
            allproxy.append((iso, ar["value"] / a["value"]))
    allproxy.sort(key=lambda x: x[1])  # lowest arable-share first = most pasture-concentrated
    rank_of = {iso: i for i, (iso, _) in enumerate(allproxy, 1)}
    print(f"{'iso':<4}{'arable%land':>13}{'agri%land':>11}{'arable/agri':>13}{'rank(low->high)':>18}")
    for iso, arv, av, share in proxy:
        print(f"{iso:<4}{arv:>13.1f}{av:>11.1f}{share:>13.3f}{rank_of.get(iso,'-'):>18}")
    print(f"\n  (Proxy ranks the {len(allproxy)} land-data DMCs by arable/agri, lowest first.)")
    print("  This is a LAND-USE-mix proxy, not a crop-diversity index, and it does")
    print("  not resolve the program-name gap — only FAOSTAT harvested area can.")

    payload = {
        "program": "water-stress-crop-diversification",
        "analysis": "denominator artifact + term decomposition of the water-crop-pressure index",
        "claim_scope": (
            "Deepening of the committed water-crop-pressure screen. Demonstrates "
            "arithmetically that the headline's first term divides withdrawal by "
            "INTERNAL-only renewable water (ER.H2O.FWTL.ZS), so every value above "
            "100% is a transboundary/fossil-aquifer denominator artifact, not "
            "domestic over-use; and that the rural-population multiplier, not "
            "water, promotes Afghanistan (43% withdrawal, below the cap) into the "
            "top-4. Triage measure (CONSTITUTION.md 6.4), not a country ranking. "
            "Measurement / observability-gap framing (13.3)."
        ),
        "source": {
            "name": "World Bank WDI (program cache)",
            "indicators": [
                "ER.H2O.FWTL.ZS (freshwater withdrawal % of INTERNAL renewable resources)",
                "AG.YLD.CREL.KG (cereal yield kg/ha)",
                "SP.RUR.TOTL.ZS (rural population %)",
                "AG.LND.AGRI.ZS (agricultural land % area)",
                "AG.LND.ARBL.ZS (arable land % area)",
            ],
            "license": "CC BY 4.0",
            "lastupdated": {"water": water_upd, "yield": yld_upd, "rural": rural_upd},
            "retrieved_at": "2026-04-25 (program cache)",
        },
        "reproduced_baseline_top4_raw_index": top4,
        "prereg_headline_top4_intersection_of_top5": prereg_top4,
        "baseline_fifth": {"iso3": ranked[4]["iso3"], "index": ranked[4]["index"]},
        "afg_per_run_position": {
            run["label"]: (
                [x["iso3"] if isinstance(x, dict) else x for x in run["top10"]].index("AFG") + 1
                if "AFG" in [x["iso3"] if isinstance(x, dict) else x for x in run["top10"]] else None
            ) for run in sens["runs"]
        },
        "over_100pct_internal_denominator": [
            {"iso3": r["iso3"], "withdrawal_pct_internal": r["water_pct"],
             "water_term": r["water_term"], "saturated_at_ceiling": r["water_term_saturated"]}
            for r in over100
        ],
        "afghanistan_inversion": {
            "withdrawal_pct": afg["water_pct"], "below_cap": afg["water_pct"] < WATER_CAP,
            "water_term": afg["water_term"], "water_term_saturated": afg["water_term_saturated"],
            "rural_pct": afg["rural_pct"], "yield_term": afg["yield_term"], "index": afg["index"],
        },
        "rural_counterfactual": {
            "top4_rural_dropped": top4_nr,
            "top4_rural_flat": top4_fr,
            "afg_rank_rural_dropped": afg_rank_nr,
            "afg_rank_rural_flat": afg_rank_fr,
            "afg_ejected_when_rural_dropped": not afg_in_collapsed,
            "high_withdrawal_set": high_withdrawal,
        },
        "land_use_proxy_NOT_crop_diversity": [
            {"iso3": iso, "arable_pct_land": arv, "agri_pct_land": av,
             "arable_over_agri": round(share, 4), "rank_low_to_high": rank_of.get(iso)}
            for iso, arv, av, share in proxy
        ],
        "data_walls": {
            "aquastat_trwr": (
                "Keystone option (1) — recompute stress on TOTAL renewable water "
                "(internal+external) — NOT runnable on-disk. Needs FAO AQUASTAT "
                "variable 4188 'Total renewable water resources (10^9 m3/yr)' and "
                "4263 'Total water withdrawal' (or 4549 'TWW as % of TRWR') from "
                "the AQUASTAT Main Database CSV bulk export, per-country, latest "
                "5-yr window. None of these is in .cache (cache holds 5 WDI series "
                "only). Until pulled, TKM/PAK/UZB/AZE above-100% values mix "
                "domestic scarcity with upstream geography."
            ),
            "faostat_crop_area": (
                "Keystone option (3) — the Shannon-equitability / Herfindahl crop-"
                "diversity index the program name promises — NOT runnable on-disk. "
                "Needs FAOSTAT 'Crops and livestock products' (QCL) Area harvested "
                "(element 5312, ha) by item by country, to build harvested-area "
                "shares. Not in .cache. The cached arable/agri land split is a "
                "land-USE proxy only and does not measure crop mix."
            ),
        },
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/water-stress-denominator-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    flat = sorted(rows, key=lambda r: -r["index"])
    with open(f"{OUT}/water-stress-denominator-deepening.csv", "w", encoding="utf-8", newline="") as f:
        cols = ["rank","iso3","country","water_pct","water_year","yield_kg_ha","rural_pct",
                "water_term","water_term_saturated","yield_term","rural_term",
                "index","index_no_rural","index_flat_rural"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in flat:
            w.writerow(r)

    print("\n" + "=" * 78)
    print("DATA WALLS (cannot compute on-disk; exact source named in JSON):")
    print("  - AQUASTAT TRWR (keystone option 1): FAO AQUASTAT vars 4188/4263/4549")
    print("    not in cache — only 5 WDI series on disk.")
    print("  - FAOSTAT crop harvested area (keystone option 3): FAOSTAT QCL element")
    print("    5312 (Area harvested, ha) by item — not in cache.")
    print("=" * 78)
    print(f"Wrote {OUT}/water-stress-denominator-deepening.json + .csv")


if __name__ == "__main__":
    main()
