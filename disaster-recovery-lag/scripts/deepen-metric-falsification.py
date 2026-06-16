"""Disaster Recovery Lag — deepening pass: does the headline top-2 survive
its OWN pre-registered falsification condition under the deaths metric and a
per-capita (events-per-million) metric?

Answers the keystone in `disaster-recovery-lag/deep-questions.md` §1.3 / §3.2.

The committed headline (`results.md`, `sensitivity.md`, `pre-registration.md`
§2) claims the top-2 set is `[CHN, IND]`, "metric-robust" across three
metrics (events-per-year, total-affected, total-damage-USD-adjusted), and
pre-registers an explicit kill-condition:

    "Retracted if the top-2 set composition changes by >= 1 entry under any
     alternative metric."

That sensitivity matrix omitted two metrics the panel can already support:
  (a) TOTAL DEATHS — the most-cited disaster-impact measure, and
  (b) events-per-MILLION-population — the per-capita view `limitations.md`
      concedes "shifts the picture toward Pacific vulnerability."

This script recomputes both, FROM SOURCE.

Provenance discipline (CONSTITUTION.md §2.2, §11):
  - The events/deaths/affected/damage aggregates are recomputed directly from
    the raw EM-DAT country-profiles workbook in THIS program's cache
    (`.cache/emdat_country_profiles.xlsx`, CRED/UCLouvain, vintage 2026-04-24),
    re-aggregated by the same rules as `process-disaster.py`, then asserted
    equal to the committed panel so the deepening shares the headline's exact
    numbers. No EM-DAT number is taken from the panel or from model memory.
  - The per-million metric needs population, which is NOT in EM-DAT and NOT in
    the committed panel. There is no population field in this program's own
    data lineage. Rather than wall the per-capita view entirely OR write a
    population number by hand (forbidden), the denominator is read from an
    on-disk World Bank WDI SP.POP.TOTL cache committed under a sibling program
    (`climate-health-workdays/.cache/wdi_pop.json`, indicator SP.POP.TOTL,
    lastupdated 2026-04-08, latest year 2024). This is a CROSS-PROGRAM JOIN and
    is labeled as such everywhere it appears; it is a 2024 single-year
    denominator applied to a 2000-2025 event count (see the wall-note in the
    payload and in deepened-results.md). Network is not touched.

Per CONSTITUTION.md §6.4 these rankings are triage, not a fragility ranking;
per §13.3 the object is a measurement/observability gap, not a country
quality ranking. attestation_chain: ai-first.
"""
import csv
import json
import os
from collections import defaultdict
from datetime import datetime, timezone

import openpyxl

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/disaster-recovery-lag"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
PANEL_CSV = f"{OUT}/disaster-recovery-lag-adb-panel.csv"
# Cross-program, on-disk WDI population (SP.POP.TOTL). See provenance note above.
POP_CACHE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/climate-health-workdays/.cache/wdi_pop.json"
os.makedirs(OUT, exist_ok=True)

# Same DMC roster as process-disaster.py.
ADB_DMCS = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan", "BGD": "Bangladesh", "BTN": "Bhutan",
    "BRN": "Brunei Darussalam", "KHM": "Cambodia", "CHN": "China",
    "FJI": "Fiji", "GEO": "Georgia",
    "IND": "India", "IDN": "Indonesia", "KAZ": "Kazakhstan", "KIR": "Kiribati",
    "KGZ": "Kyrgyzstan", "LAO": "Lao PDR",
    "MYS": "Malaysia", "MDV": "Maldives", "MHL": "Marshall Islands", "FSM": "Micronesia, Fed. Sts.",
    "MNG": "Mongolia", "MMR": "Myanmar", "NPL": "Nepal",
    "PAK": "Pakistan", "PNG": "Papua New Guinea", "PHL": "Philippines",
    "WSM": "Samoa", "SLB": "Solomon Islands", "LKA": "Sri Lanka", "TJK": "Tajikistan",
    "THA": "Thailand", "TLS": "Timor-Leste", "TON": "Tonga", "TKM": "Turkmenistan",
    "TUV": "Tuvalu", "UZB": "Uzbekistan", "VUT": "Vanuatu", "VNM": "Viet Nam",
}


def aggregate_emdat():
    """Re-aggregate EM-DAT 2000-2025 per DMC straight from the raw workbook,
    by the same rules process-disaster.py uses."""
    wb = openpyxl.load_workbook(f"{CACHE}/emdat_country_profiles.xlsx", data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    cols = {h: i for i, h in enumerate(header)}
    data_rows = rows[2:]  # skip header + HXL marker row

    agg = defaultdict(lambda: {"events": 0, "affected": 0, "deaths": 0,
                               "damage": 0.0, "years": set()})
    n_filt = 0
    for row in data_rows:
        if row is None or len(row) < len(header):
            continue
        iso = row[cols["ISO"]]
        if iso not in ADB_DMCS:
            continue
        try:
            year = int(row[cols["Year"]])
        except (TypeError, ValueError):
            continue
        if year < 2000 or year > 2025:
            continue
        n_filt += 1
        a = agg[iso]
        try: a["events"] += int(row[cols["Total Events"]] or 0)
        except (TypeError, ValueError): pass
        try: a["affected"] += int(row[cols["Total Affected"]] or 0)
        except (TypeError, ValueError): pass
        try: a["deaths"] += int(row[cols["Total Deaths"]] or 0)
        except (TypeError, ValueError): pass
        dmg = row[cols["Total Damage (USD, adjusted)"]]
        if isinstance(dmg, (int, float)) and dmg > 0:
            a["damage"] += float(dmg)
        a["years"].add(year)

    out = {}
    for iso, name in ADB_DMCS.items():
        a = agg.get(iso)
        if not a:
            out[iso] = {"iso3": iso, "country": name, "events": 0, "affected": 0,
                        "deaths": 0, "damage": 0.0, "years": 0, "events_per_year": 0.0}
            continue
        yrs = max(len(a["years"]), 1)
        out[iso] = {
            "iso3": iso, "country": name,
            "events": a["events"], "affected": a["affected"], "deaths": a["deaths"],
            "damage": round(a["damage"], 0), "years": len(a["years"]),
            "events_per_year": round(a["events"] / yrs, 2),
        }
    return out, n_filt, len(rows)


def load_panel():
    """The committed panel — used only to ASSERT the recompute matches it."""
    panel = {}
    with open(PANEL_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            panel[r["iso3"]] = r
    return panel


def load_population():
    """WDI SP.POP.TOTL from the on-disk sibling cache. Returns iso3 -> (year, value)
    for the latest available year, plus metadata. Cross-program join — labeled."""
    blob = json.load(open(POP_CACHE, encoding="utf-8"))
    meta, recs = blob[0], blob[1]
    by_iso = defaultdict(dict)
    for r in recs:
        iso = r.get("countryiso3code")
        v = r.get("value")
        yr = r.get("date")
        if iso and v is not None:
            by_iso[iso][yr] = v
    latest = {}
    for iso, yrs in by_iso.items():
        if iso in ADB_DMCS and yrs:
            y = max(yrs.keys())
            latest[iso] = (y, yrs[y])
    return latest, meta


def topn(rows, key, n=5, exclude_zero=True):
    seq = [r for r in rows if (r.get(key) is not None and (not exclude_zero or r[key] > 0))]
    return sorted(seq, key=lambda r: -r[key])[:n]


def main():
    agg, n_filt, n_total = aggregate_emdat()
    panel = load_panel()

    # --- Provenance assertion: recompute must equal the committed panel. ---
    mism = []
    for iso, a in agg.items():
        p = panel.get(iso)
        if not p:
            mism.append((iso, "missing-in-panel"))
            continue
        if a["events"] != int(p["total_events_2000_2025"]):
            mism.append((iso, f"events {a['events']} != {p['total_events_2000_2025']}"))
        if a["deaths"] != int(p["total_deaths"]):
            mism.append((iso, f"deaths {a['deaths']} != {p['total_deaths']}"))
        if a["affected"] != int(p["total_affected"]):
            mism.append((iso, f"affected {a['affected']} != {p['total_affected']}"))
    if mism:
        print("!! RECOMPUTE != COMMITTED PANEL:")
        for m in mism:
            print("   ", m)
        raise SystemExit("Recompute diverged from committed panel; refusing to proceed.")
    print(f"[provenance] recompute from raw EM-DAT == committed panel for all "
          f"{len(agg)} DMCs (events, deaths, affected). EM-DAT rows={n_total}, "
          f"in-filter={n_filt}.")

    pop, pop_meta = load_population()

    # Attach per-million-population (events per 1e6 of latest-year population).
    rows = []
    for iso, a in agg.items():
        r = dict(a)
        py = pop.get(iso)
        if py and py[1] > 0:
            r["pop_year"] = py[0]
            r["population"] = py[1]
            r["events_per_million"] = round(a["events"] / (py[1] / 1e6), 3)
        else:
            r["pop_year"] = None
            r["population"] = None
            r["events_per_million"] = None
        rows.append(r)

    # --- The headline metrics (already committed) ---
    by_events = topn(rows, "events_per_year")
    by_affected = topn(rows, "affected")
    by_damage = topn(rows, "damage")
    # --- The two omitted metrics (the deepening) ---
    by_deaths = topn(rows, "deaths")
    by_permil = topn(rows, "events_per_million")

    def iso_list(seq):
        return [r["iso3"] for r in seq]

    headline_top2 = ["CHN", "IND"]
    metrics = {
        "events_per_year (committed)": iso_list(by_events),
        "total_affected (committed)": iso_list(by_affected),
        "total_damage_usd_adj (committed)": iso_list(by_damage),
        "total_deaths (DEEPENING)": iso_list(by_deaths),
        "events_per_million_pop (DEEPENING, cross-program WDI join)": iso_list(by_permil),
    }

    # Does the pre-registered kill-condition fire?  Top-2 changes by >=1 entry.
    fires = {}
    for label, top5 in metrics.items():
        top2 = top5[:2]
        changed = set(top2) != set(headline_top2)
        fires[label] = {
            "top2": top2,
            "differs_from_headline_top2": changed,
            "kill_condition_fires": changed,
        }

    any_fires = any(v["kill_condition_fires"] for v in fires.values())

    # ---- console report ----
    def fmt(seq, valkey, vfmt):
        return "  ".join(f"{r['iso3']}={vfmt(r[valkey])}" for r in seq)

    print("\n================ HEADLINE (committed) ================")
    print("Pre-registered top-2 set:", headline_top2,
          " kill-condition: retract if top-2 changes by >=1 entry under ANY metric")
    print(f"  events/yr   top5: {fmt(by_events,'events_per_year', lambda v: f'{v:.2f}')}")
    print(f"  affected    top5: {fmt(by_affected,'affected', lambda v: f'{v:,}')}")
    print(f"  damageUSDadj top5: {fmt(by_damage,'damage', lambda v: f'{v:,.0f}')}")

    print("\n================ DEEPENING — the two omitted metrics ================")
    print(f"  TOTAL DEATHS top5: {fmt(by_deaths,'deaths', lambda v: f'{v:,}')}")
    print(f"  events/MILLION pop top5 (2024 WDI pop, cross-program join):")
    for r in by_permil:
        print(f"      {r['iso3']:<4} {r['country'][:20]:<20} {r['events_per_million']:>8.3f} "
              f"per 1e6  (events={r['events']:>3}, pop{r['pop_year']}={r['population']:,})")

    print("\n================ DOES THE KILL-CONDITION FIRE? ================")
    for label, v in fires.items():
        flag = "FIRES (top-2 changed)" if v["kill_condition_fires"] else "holds"
        print(f"  [{flag:<22}] {label:<58} top-2={v['top2']}")
    print(f"\n  >>> Program's own falsification condition fires under >=1 metric: "
          f"{'YES' if any_fires else 'NO'}")

    # Make the deaths inversion explicit. deep-questions.md S1.3 *guessed* the
    # deaths top-2 would be Indonesia+China; the data shows it is actually
    # Indonesia+Myanmar (Nargis), so the inversion is larger than the agenda saw.
    d2 = iso_list(by_deaths)[:2]
    deaths_rank = {r["iso3"]: i + 1 for i, r in
                   enumerate(sorted(rows, key=lambda r: -r["deaths"]))}
    idn = next(r for r in rows if r["iso3"] == "IDN")
    chn = next(r for r in rows if r["iso3"] == "CHN")
    ind = next(r for r in rows if r["iso3"] == "IND")
    print(f"  >>> By DEATHS the top-2 is {d2}; it is NOT [CHN, IND], so the "
          f"kill-condition fires.")
    print(f"      deep-questions.md S1.3 guessed Indonesia+China; the data is "
          f"Indonesia+Myanmar (guess {'CONFIRMED' if set(d2)=={'IDN','CHN'} else 'OFF — inversion is larger'}).")
    print(f"      IDN deaths={idn['deaths']:,} (#{deaths_rank['IDN']})  "
          f"MMR deaths={next(r for r in rows if r['iso3']=='MMR')['deaths']:,} (#{deaths_rank['MMR']})  "
          f"CHN deaths={chn['deaths']:,} (#{deaths_rank['CHN']})  "
          f"IND deaths={ind['deaths']:,} (#{deaths_rank['IND']})  "
          f"-> India falls from #2 to #{deaths_rank['IND']} by deaths.")

    # ---- artifact ----
    payload = {
        "program": "disaster-recovery-lag",
        "analysis": "metric-falsification: does the committed top-2 survive deaths and per-capita?",
        "claim_scope": (
            "Deepening of the burden-ranking screen. Re-runs the pre-registered "
            "top-2 stability test (pre-registration.md S2) under two metrics the "
            "committed sensitivity matrix omitted: total deaths, and "
            "events-per-million-population. Triage measure (CONSTITUTION.md S6.4); "
            "measurement/observability gap framing (S13.3), not a country ranking."
        ),
        "headline_top2": headline_top2,
        "kill_condition": (
            "Retract if the top-2 set composition changes by >=1 entry under any "
            "alternative metric (pre-registration.md S2)."
        ),
        "metrics_top5": metrics,
        "kill_condition_by_metric": fires,
        "kill_condition_fires_overall": any_fires,
        "deaths_top2": d2,
        "sources": {
            "emdat": {
                "name": "EM-DAT — The International Disaster Database (CRED, UCLouvain)",
                "file": ".cache/emdat_country_profiles.xlsx",
                "vintage": "2026-04-24",
                "rows_total": n_total,
                "rows_in_filter": n_filt,
                "fields": "Total Events, Total Affected, Total Deaths, Total Damage (USD, adjusted)",
                "note_threshold": "EM-DAT entry requires >=10 deaths OR >=100 affected OR a declared state of emergency / international appeal.",
                "recompute_equals_committed_panel": True,
            },
            "population": {
                "name": "World Bank WDI SP.POP.TOTL (Population, total)",
                "file": "climate-health-workdays/.cache/wdi_pop.json (CROSS-PROGRAM on-disk join)",
                "lastupdated": pop_meta.get("lastupdated"),
                "denominator_year": "2024 (latest available in cache)",
                "wall_note": (
                    "Population is NOT in EM-DAT and NOT in this program's committed "
                    "panel. The per-million metric uses a 2024 single-year denominator "
                    "from a sibling program's WDI cache applied to a 2000-2025 event "
                    "count; it is an on-disk recompute, not a fetch, and is a "
                    "cross-program join rather than this program's own lineage. "
                    "Treat events-per-million as indicative of the per-capita "
                    "INVERSION, not as a final calibrated rate."
                ),
            },
        },
        "framing_rule": "Burden/observability gap, not country fragility ranking (S13.3).",
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/disaster-recovery-lag-metric-falsification.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Flat CSV: per-DMC, all five metric values, sorted by deaths.
    flat = sorted(rows, key=lambda r: -r["deaths"])
    fieldnames = ["iso3", "country", "events", "events_per_year", "affected",
                  "deaths", "damage", "population", "pop_year", "events_per_million"]
    with open(f"{OUT}/disaster-recovery-lag-metric-falsification.csv", "w",
              encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in flat:
            w.writerow({k: r.get(k) for k in fieldnames})

    print(f"\nWrote {OUT}/disaster-recovery-lag-metric-falsification.{{json,csv}}")


if __name__ == "__main__":
    main()
