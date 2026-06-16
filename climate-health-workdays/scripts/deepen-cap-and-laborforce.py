"""Climate-Health Workdays — deepening pass: two linked recomputes.

Answers the keystone in `climate-health-workdays/deep-questions.md` §1.1
(cap-saturation) and §3.2 (wrong denominator), with real recomputations
over data already on disk. No network, no AI-supplied figures.

(a) CAP-SATURATION (deep-questions §1.1). The committed PM2.5 ramp is
    clamp((pm25 - 5) / 45, 0, 1). The pre-registration admits the *top-5*
    breaks specifically at `pm25_cap_minus50` (cap = 22.5). At cap = 22.5
    the ramp saturates at any PM2.5 >= 27.5, so the dirtiest DMCs all peg
    pressure = 1.0 and the pollution axis stops discriminating. This script
    recomputes the index at the baseline cap (45) and at the saturating cap
    (22.5) and measures, by Spearman rank correlation, how far the index
    ranking collapses toward a pure outdoor-labor-share ranking. The Nepal
    case is the smoking gun and is printed explicitly: ~3rd-dirtiest air
    (~45.7 ug/m3, near AFG's ~46.1) yet ~6th by index, because its
    outdoor-labor share (~39) is below AFG's (~61) — the labor axis sets the
    order, not the air.

(b) WRONG DENOMINATOR (deep-questions §3.2). The committed panel computes
    `exposed_outdoor_millions = outdoor_labor_share/100 x TOTAL population`.
    But the WDI employment-share series are "% of total EMPLOYMENT", not of
    population, so the correct base is the *employed* labor force, not
    headcount — multiplying a share-of-employment by total population counts
    children and retirees as exposed outdoor workers. The honest base is
    employment = total_population x employment-to-population ratio.

    WALL: the employment-to-population ratio (WDI SL.EMP.TOTL.SP.ZS) is NOT
    on disk in this program's .cache (only SL.AGR.EMPL.ZS, SL.IND.EMPL.ZS,
    EN.ATM.PM25.MC.M3, SP.URB.TOTL.IN.ZS, SP.POP.TOTL are cached), and the
    network is blocked, so a per-DMC WDI emp-to-pop value cannot be fetched
    here. We therefore (i) restate the published total-population figure from
    disk, and (ii) bound the corrected count across an EXPLICIT, LABELLED
    sweep of employment-to-population ratios (0.40 / 0.50 / 0.60). These
    sweep values are script assumptions, NOT WDI data, and are printed as
    such; no emp-to-pop number is asserted as observed. The real WDI-derived
    quantities (outdoor share, total population) come only from disk.

Every WDI-derived number traces to the committed program cache (WDI,
CC BY 4.0), re-read here. Per CONSTITUTION.md §6.4 the index is a triage
measure, not a ranking. §13.3 framing: this is a measurement/construct gap,
not a country-deficiency ranking. attestation_chain: ai-first.
"""
import json
import os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/climate-health-workdays"
PANEL = f"{BASE}/generated/climate-health-workdays-adb-panel.json"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

BASELINE_CAP = 45.0
SATURATING_CAP = 22.5   # = pm25_cap_minus50, the row the pre-registration says breaks top-5
PM25_FLOOR = 5.0
INDUSTRY_WEIGHT = 0.5

# Labelled assumption sweep for recompute (b). NOT WDI data. See WALL above.
EMP_TO_POP_SWEEP = [0.40, 0.50, 0.60]


def index_at_cap(outdoor_share_pct, pm25, cap):
    """Committed index formula, parameterised on the PM2.5 ramp cap."""
    pressure = max(pm25 - PM25_FLOOR, 0.0) / cap
    pressure = min(max(pressure, 0.0), 1.0)
    return round((outdoor_share_pct / 100.0) * pressure * 100.0, 2), round(min(max(pressure, 0.0), 1.0), 4)


def spearman(xs, ys):
    """Spearman rank correlation (ties via average rank). Self-contained."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
    return round(num / (dx * dy), 4) if dx and dy else None


def main():
    panel = json.loads(open(PANEL, encoding="utf-8").read())
    rows = [r for r in panel["rows"]
            if r.get("workday_loss_pressure_index") is not None
            and r.get("pm25_exposure_ugm3") is not None
            and r.get("outdoor_labor_share_pct") is not None]

    # ---- Recompute (a): cap-saturation -------------------------------------
    recomputed = []
    for r in rows:
        outdoor = r["outdoor_labor_share_pct"]
        pm25 = r["pm25_exposure_ugm3"]
        idx_base, pres_base = index_at_cap(outdoor, pm25, BASELINE_CAP)
        idx_sat, pres_sat = index_at_cap(outdoor, pm25, SATURATING_CAP)
        recomputed.append({
            "iso3": r["iso3"], "country": r["country"],
            "outdoor_labor_share_pct": outdoor,
            "pm25_ugm3": pm25,
            "pressure_cap45": pres_base, "index_cap45": idx_base,
            "pressure_cap22_5": pres_sat, "index_cap22_5": idx_sat,
        })

    rank_base = sorted(recomputed, key=lambda r: -r["index_cap45"])
    rank_sat = sorted(recomputed, key=lambda r: -r["index_cap22_5"])
    rank_labor = sorted(recomputed, key=lambda r: -r["outdoor_labor_share_pct"])

    for i, r in enumerate(rank_base, 1):
        r["rank_cap45"] = i
    for i, r in enumerate(rank_sat, 1):
        r["rank_cap22_5"] = i
    for i, r in enumerate(rank_labor, 1):
        r["rank_labor"] = i

    n = len(recomputed)
    isos = [r["iso3"] for r in recomputed]
    idx_base_v = [r["index_cap45"] for r in recomputed]
    idx_sat_v = [r["index_cap22_5"] for r in recomputed]
    labor_v = [r["outdoor_labor_share_pct"] for r in recomputed]

    rho_base_labor = spearman(idx_base_v, labor_v)
    rho_sat_labor = spearman(idx_sat_v, labor_v)
    rho_base_sat = spearman(idx_base_v, idx_sat_v)

    n_saturated_base = sum(1 for r in recomputed if r["pressure_cap45"] >= 0.999)
    n_saturated_sat = sum(1 for r in recomputed if r["pressure_cap22_5"] >= 0.999)

    print("=" * 74)
    print("RECOMPUTE (a) — CAP-SATURATION  (deep-questions.md §1.1, the keystone)")
    print("=" * 74)
    print(f"Rankable DMCs: {n}.  PM2.5 floor {PM25_FLOOR}, industry weight {INDUSTRY_WEIGHT}.")
    print(f"Saturating cap = {SATURATING_CAP} (= pm25_cap_minus50). Ramp pegs at PM2.5 >= "
          f"{PM25_FLOOR + SATURATING_CAP:.1f} ug/m3.")
    print(f"PM2.5 pressure pegged at 1.0:  cap45 -> {n_saturated_base} DMC(s);  "
          f"cap22.5 -> {n_saturated_sat} DMC(s).")
    print()
    print("Spearman rank correlation of the index with the PURE outdoor-labor-share order:")
    print(f"  index@cap45   vs labor-share order : rho = {rho_base_labor}")
    print(f"  index@cap22.5 vs labor-share order : rho = {rho_sat_labor}   "
          f"(closer to 1.0 = index has collapsed toward a pure labor ranking)")
    print(f"  index@cap45   vs index@cap22.5      : rho = {rho_base_sat}")
    print()
    print("Top-8 by index, baseline cap=45 vs saturating cap=22.5 "
          "(rank_L = pure outdoor-labor-share rank):")
    print(f"  {'iso':<4} {'outdoor%':>8} {'PM2.5':>6} | {'pres@45':>7} {'idx@45':>7} {'rk@45':>5} "
          f"| {'pres@22.5':>9} {'idx@22.5':>8} {'rk@22.5':>7} | {'rk_L':>4}")
    for r in rank_sat[:8]:
        print(f"  {r['iso3']:<4} {r['outdoor_labor_share_pct']:>8.1f} {r['pm25_ugm3']:>6.1f} "
              f"| {r['pressure_cap45']:>7.3f} {r['index_cap45']:>7.2f} {r['rank_cap45']:>5} "
              f"| {r['pressure_cap22_5']:>9.3f} {r['index_cap22_5']:>8.2f} {r['rank_cap22_5']:>7} "
              f"| {r['rank_labor']:>4}")

    # Smoking-gun NPL vs AFG, at baseline cap, before any perturbation.
    npl = next(r for r in recomputed if r["iso3"] == "NPL")
    afg = next(r for r in recomputed if r["iso3"] == "AFG")
    bgd = next(r for r in recomputed if r["iso3"] == "BGD")
    print()
    print("Smoking gun already visible at the BASELINE cap (no perturbation):")
    for r in (afg, npl, bgd):
        print(f"  {r['iso3']}: PM2.5={r['pm25_ugm3']:.1f} ug/m3 (pressure@45={r['pressure_cap45']:.3f}), "
              f"outdoor-labor={r['outdoor_labor_share_pct']:.1f}%  ->  index@45={r['index_cap45']:.2f}, "
              f"rank@45={r['rank_cap45']} (labor-rank={r['rank_labor']})")
    print(f"  NPL air ({npl['pm25_ugm3']:.1f}) is within {abs(afg['pm25_ugm3'] - npl['pm25_ugm3']):.1f} "
          f"ug/m3 of AFG ({afg['pm25_ugm3']:.1f}) and above BGD ({bgd['pm25_ugm3']:.1f}), yet NPL "
          f"ranks #{npl['rank_cap45']} vs AFG #{afg['rank_cap45']} / BGD #{bgd['rank_cap45']}.")
    print(f"  At cap=22.5 AFG, NPL, BGD pressures are {afg['pressure_cap22_5']:.3f} / "
          f"{npl['pressure_cap22_5']:.3f} / {bgd['pressure_cap22_5']:.3f} — identical (all pegged); the "
          f"order is then set ONLY by outdoor-labor share.")

    # ---- Recompute (b): wrong denominator ----------------------------------
    print()
    print("=" * 74)
    print("RECOMPUTE (b) — WRONG DENOMINATOR  (deep-questions.md §3.2)")
    print("=" * 74)
    print("Published `exposed_outdoor_millions` = outdoor_labor_share/100 x TOTAL population.")
    print("WDI employment shares are '% of total EMPLOYMENT', so the correct base is the")
    print("EMPLOYED labor force = total_population x employment-to-population ratio.")
    print()
    print("WALL: employment-to-population ratio (WDI SL.EMP.TOTL.SP.ZS) is NOT on disk in")
    print("this program's .cache and the network is blocked. The ratios below are LABELLED")
    print("SCRIPT ASSUMPTIONS (0.40 / 0.50 / 0.60), NOT observed WDI values. Only the")
    print("outdoor share and total population are WDI-on-disk numbers.")
    print()

    top = [r for r in panel["rows"] if r["iso3"] in ("AFG", "IND", "BGD")]
    top.sort(key=lambda r: -(r["workday_loss_pressure_index"] or 0))
    lab_rows = []
    hdr = (f"  {'iso':<4} {'outdoor%':>8} {'pop(M)':>9} {'PUBLISHED':>10} "
           + " ".join(f"{'e/p='+format(e,'.2f'):>10}" for e in EMP_TO_POP_SWEEP))
    print(hdr)
    print(f"  {'':4} {'':8} {'':9} {'(x TOTAL)':>10} "
          + " ".join(f"{'(workers)':>10}" for _ in EMP_TO_POP_SWEEP))
    for r in top:
        outdoor = r["outdoor_labor_share_pct"]
        popM = r["population_total"] / 1e6
        published = r["exposed_outdoor_millions"]
        corrected = {f"{e:.2f}": round((outdoor / 100.0) * (r["population_total"] * e) / 1e6, 1)
                     for e in EMP_TO_POP_SWEEP}
        cells = " ".join(f"{corrected[f'{e:.2f}']:>10.1f}" for e in EMP_TO_POP_SWEEP)
        print(f"  {r['iso3']:<4} {outdoor:>8.1f} {popM:>9.1f} {published:>10.1f} {cells}")
        lab_rows.append({
            "iso3": r["iso3"], "country": r["country"],
            "outdoor_labor_share_pct": outdoor,
            "population_total": r["population_total"],
            "published_exposed_outdoor_millions_x_total_pop": published,
            "labor_force_exposed_millions_by_assumed_emp_to_pop": corrected,
        })

    ind = next(r for r in top if r["iso3"] == "IND")
    ind_pub = ind["exposed_outdoor_millions"]
    ind_lo = round((ind["outdoor_labor_share_pct"] / 100.0) * (ind["population_total"] * EMP_TO_POP_SWEEP[0]) / 1e6, 1)
    ind_hi = round((ind["outdoor_labor_share_pct"] / 100.0) * (ind["population_total"] * EMP_TO_POP_SWEEP[-1]) / 1e6, 1)
    print()
    print(f"India: published {ind_pub} M shrinks to {ind_lo}-{ind_hi} M once a labor-force base")
    print(f"replaces total population (assumed emp/pop {EMP_TO_POP_SWEEP[0]}-{EMP_TO_POP_SWEEP[-1]}); "
          f"the published figure is {round(ind_pub/ind_hi,2)}x-{round(ind_pub/ind_lo,2)}x the")
    print("labor-force count because children and retirees are inside the total-population base.")

    payload = {
        "program": "climate-health-workdays",
        "analysis": "cap-saturation of the workday-loss index + labor-force denominator correction",
        "claim_scope": (
            "Deepening of the PM2.5-only triage index. (a) recomputes the committed index at "
            "the saturating PM2.5 cap (22.5 = pm25_cap_minus50) and measures how far the ranking "
            "collapses to a pure outdoor-labor-share order; (b) restates the exposed-worker count "
            "on a labor-force base instead of total population. Triage measure (CONSTITUTION.md "
            "§6.4), not a country ranking. §13.3 measurement/construct-gap framing."
        ),
        "source": {
            "name": "World Development Indicators (program cache)",
            "indicators": [
                "SL.AGR.EMPL.ZS", "SL.IND.EMPL.ZS", "EN.ATM.PM25.MC.M3",
                "SP.URB.TOTL.IN.ZS", "SP.POP.TOTL",
            ],
            "license": "CC BY 4.0",
            "retrieved_at": "2026-04-25 (program cache)",
            "panel": "generated/climate-health-workdays-adb-panel.json",
        },
        "params": {
            "pm25_floor": PM25_FLOOR, "industry_weight": INDUSTRY_WEIGHT,
            "baseline_cap": BASELINE_CAP, "saturating_cap": SATURATING_CAP,
        },
        "cap_saturation": {
            "rankable_dmcs": n,
            "n_pressure_saturated_cap45": n_saturated_base,
            "n_pressure_saturated_cap22_5": n_saturated_sat,
            "spearman_index_cap45_vs_labor_share": rho_base_labor,
            "spearman_index_cap22_5_vs_labor_share": rho_sat_labor,
            "spearman_index_cap45_vs_cap22_5": rho_base_sat,
            "rows": recomputed,
            "ranking_cap45": [r["iso3"] for r in rank_base],
            "ranking_cap22_5": [r["iso3"] for r in rank_sat],
            "ranking_labor_share": [r["iso3"] for r in rank_labor],
        },
        "denominator_correction": {
            "wall_note": (
                "employment-to-population ratio (WDI SL.EMP.TOTL.SP.ZS) is NOT on disk and the "
                "network is blocked; the emp_to_pop_sweep values are LABELLED SCRIPT ASSUMPTIONS, "
                "not observed WDI data. Only outdoor share and total population are WDI-on-disk."
            ),
            "emp_to_pop_sweep_ASSUMED_not_WDI": EMP_TO_POP_SWEEP,
            "rows": lab_rows,
        },
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/climate-health-workdays-deepening.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print()
    print(f"Wrote {OUT}/climate-health-workdays-deepening.json")


if __name__ == "__main__":
    main()
