"""Grid Reliability — deepening pass: fuel concentration on GENERATION,
not installed capacity.

Answers the keystone in `grid-reliability-heat/deep-questions.md` §1.1:
the headline single-fuel cluster is computed on installed CAPACITY, which
assumes every plant runs at nameplate. A grid can be single-fuel in
capacity yet diverse in what it actually generates — most sharply where
thermal backup plants exist precisely to cover a dominant hydro fleet in
the dry season (Tajikistan's Dushanbe/Yavan thermal units behind the Nurek
dam are the textbook case).

This script recomputes the exact same fuel-Herfindahl the committed
`process-grid.py` produces, but on each plant's annual generation instead
of its capacity. Generation is WRI's reported `generation_gwh_2017` where
available, else WRI's modeled `estimated_generation_gwh_2017`. Coverage
(share of national capacity carrying a generation value) is reported per
DMC; the generation-Herfindahl is withheld where coverage < 80%.

Every number traces to the same committed public source the headline uses
(WRI Global Power Plant Database v1.3.0, CC BY 4.0), re-read from the
program cache. No new data, no network, no AI-supplied figures.
Per CONSTITUTION.md §6.4 the Herfindahl is a triage measure, not a
reliability ranking. attestation_chain: ai-first.
"""
import csv, json, os
from collections import defaultdict
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/grid-reliability-heat"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

# Same DMC roster as process-grid.py.
ADB_DMCS = {
    "AFG":"Afghanistan","ARM":"Armenia","AZE":"Azerbaijan","BGD":"Bangladesh","BTN":"Bhutan",
    "BRN":"Brunei Darussalam","KHM":"Cambodia","CHN":"China",
    "FJI":"Fiji","GEO":"Georgia","HKG":"Hong Kong SAR, China",
    "IND":"India","IDN":"Indonesia","KAZ":"Kazakhstan","KIR":"Kiribati",
    "KGZ":"Kyrgyzstan","LAO":"Lao PDR",
    "MYS":"Malaysia","MDV":"Maldives","MHL":"Marshall Islands","FSM":"Micronesia, Fed. Sts.",
    "MNG":"Mongolia","MMR":"Myanmar","NPL":"Nepal",
    "PAK":"Pakistan","PNG":"Papua New Guinea","PHL":"Philippines",
    "WSM":"Samoa","SLB":"Solomon Islands","LKA":"Sri Lanka","TJK":"Tajikistan",
    "THA":"Thailand","TLS":"Timor-Leste","TON":"Tonga","TKM":"Turkmenistan",
    "TUV":"Tuvalu","UZB":"Uzbekistan","VUT":"Vanuatu","VNM":"Viet Nam",
    "TWN":"Taiwan",
}
COVERAGE_MIN = 0.80  # withhold generation-Herfindahl below this capacity coverage


def best_generation(row):
    """Reported 2017 generation if present, else WRI's modeled 2017 estimate."""
    for col in ("generation_gwh_2017", "estimated_generation_gwh_2017"):
        v = (row.get(col) or "").strip()
        if v:
            try:
                f = float(v)
                if f > 0:
                    return f, ("reported" if col.startswith("generation") else "estimated")
            except ValueError:
                pass
    return None, None


def herfindahl(shares_by_fuel, total):
    if not total:
        return None, None, None
    shares = {k: v / total for k, v in shares_by_fuel.items()}
    h = round(sum(s * s for s in shares.values()), 4)
    top = max(shares.items(), key=lambda x: x[1])
    return h, top[0], round(top[1], 4)


def main():
    cap_by_fuel = defaultdict(lambda: defaultdict(float))   # iso -> fuel -> MW
    gen_by_fuel = defaultdict(lambda: defaultdict(float))   # iso -> fuel -> GWh
    cap_total = defaultdict(float)
    cap_with_gen = defaultdict(float)                       # capacity carrying a gen value
    plant_n = defaultdict(int)

    with open(f"{CACHE}/global_power_plant_database.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            iso = (row.get("country") or "").strip()
            if iso not in ADB_DMCS:
                continue
            try:
                cap = float(row.get("capacity_mw") or 0)
            except ValueError:
                cap = 0.0
            fuel = (row.get("primary_fuel") or "Unknown").strip()
            cap_by_fuel[iso][fuel] += cap
            cap_total[iso] += cap
            plant_n[iso] += 1
            gen, _src = best_generation(row)
            if gen is not None:
                gen_by_fuel[iso][fuel] += gen
                cap_with_gen[iso] += cap

    rows = []
    for iso, name in ADB_DMCS.items():
        if cap_total[iso] <= 0:
            continue
        h_cap, top_cap, share_cap = herfindahl(cap_by_fuel[iso], cap_total[iso])
        gen_total = sum(gen_by_fuel[iso].values())
        coverage = cap_with_gen[iso] / cap_total[iso] if cap_total[iso] else 0.0
        if coverage >= COVERAGE_MIN and gen_total > 0:
            h_gen, top_gen, share_gen = herfindahl(gen_by_fuel[iso], gen_total)
        else:
            h_gen, top_gen, share_gen = None, None, None
        rows.append({
            "iso3": iso, "country": name, "plant_count": plant_n[iso],
            "total_capacity_mw": round(cap_total[iso], 1),
            "total_generation_gwh_2017": round(gen_total, 1),
            "generation_coverage": round(coverage, 3),
            "herfindahl_capacity": h_cap,
            "top_fuel_capacity": top_cap, "top_share_capacity": share_cap,
            "herfindahl_generation": h_gen,
            "top_fuel_generation": top_gen, "top_share_generation": share_gen,
            "herfindahl_delta": (round(h_gen - h_cap, 4) if h_gen is not None else None),
        })

    # Cluster = top-5 by each Herfindahl (single-fuel concentration).
    by_cap = sorted(rows, key=lambda r: -(r["herfindahl_capacity"] or 0))
    eligible = [r for r in rows if r["herfindahl_generation"] is not None]
    by_gen = sorted(eligible, key=lambda r: -(r["herfindahl_generation"] or 0))
    cap_top5 = [r["iso3"] for r in by_cap[:5]]
    gen_top5 = [r["iso3"] for r in by_gen[:5]]
    dropped = [i for i in cap_top5 if i not in gen_top5]
    entered = [i for i in gen_top5 if i not in cap_top5]

    payload = {
        "program": "grid-reliability-heat",
        "analysis": "fuel-concentration on generation vs installed capacity",
        "claim_scope": (
            "Deepening of the capacity-based single-fuel screen. Recomputes the "
            "identical fuel-Herfindahl on WRI reported/modeled 2017 generation "
            "instead of installed capacity. Triage measure (CONSTITUTION.md §6.4), "
            "not a reliability ranking. Generation-Herfindahl withheld where "
            f"generation covers < {int(COVERAGE_MIN*100)}% of national capacity."
        ),
        "source": {
            "name": "WRI Global Power Plant Database v1.3.0",
            "fields": "capacity_mw, primary_fuel, generation_gwh_2017, estimated_generation_gwh_2017",
            "license": "CC BY 4.0", "retrieved_at": "2026-04-25 (program cache)",
        },
        "capacity_top5": cap_top5,
        "generation_top5": gen_top5,
        "dropped_from_cluster_on_generation": dropped,
        "entered_cluster_on_generation": entered,
        "rows_by_generation_herfindahl": by_gen,
        "rows_withheld_low_coverage": [r["iso3"] for r in rows if r["herfindahl_generation"] is None],
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/grid-generation-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    flat = [{k: v for k, v in r.items()} for r in sorted(rows, key=lambda r:-(r["herfindahl_capacity"] or 0))]
    with open(f"{OUT}/grid-generation-deepening.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(flat[0].keys())); w.writeheader()
        for r in flat: w.writerow(r)

    print("=== Capacity top-5 (headline):", cap_top5)
    print("=== Generation top-5 (deepened):", gen_top5)
    print("=== Dropped on generation:", dropped, " Entered:", entered)
    print("\niso  cap-herf  top(cap)        gen-herf  top(gen)        delta  coverage")
    for r in sorted(rows, key=lambda r:-(r["herfindahl_capacity"] or 0))[:14]:
        print(f"{r['iso3']:<4} {str(r['herfindahl_capacity']):<8} "
              f"{str(r['top_fuel_capacity'])[:14]:<14}  {str(r['herfindahl_generation']):<8} "
              f"{str(r['top_fuel_generation'])[:14]:<14}  {str(r['herfindahl_delta']):<6} "
              f"{r['generation_coverage']*100:.0f}%")
    print(f"\nWrote {OUT}/grid-generation-deepening.json + .csv")


if __name__ == "__main__":
    main()
