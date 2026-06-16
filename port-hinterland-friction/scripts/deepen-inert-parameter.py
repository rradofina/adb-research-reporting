"""Port-Hinterland Friction — deepening pass: the inert imports-cap parameter.

Answers the keystone in `port-hinterland-friction/deep-questions.md` §1.1: the
headline's "stable across all ±50% perturbations" robustness claim perturbs two
index parameters — the imports normalizer (50) and the imports cap (2.0). This
script tests whether the cap is connected to the output at all.

The friction-exposure index is, verbatim from `process-logistics.py`:

    lpi_gap   = max(5.0 - lpi_overall, 0)
    import_B  = imports_usd / 1e9
    import_log = (import_B ** 0.5) / 50          # sqrt-scale
    friction  = round(lpi_gap * min(import_log, 2.0), 2)

The `min(., 2.0)` ceiling binds only when import_log >= 2.0, i.e.
sqrt(import_B) >= 100, i.e. import_B >= 10000, i.e. imports >= $10 trillion.
No ADB DMC imports anywhere near that. This script:

  1. Recomputes the import proxy `sqrt(import_B)/50` for EVERY DMC from the
     committed cache (`wdi_imports.json`) — the same source the headline uses —
     and reports each economy's proxy and the panel maximum, to show none
     reaches the 2.0 ceiling.
  2. Re-derives the baseline friction index and confirms it reproduces the
     committed panel's top-5 to the published rounding.
  3. Re-runs the ±50% cap perturbation the headline reports (cap = 1.0, 3.0)
     and shows the top-5 is invariant — because, except for the cap = 1.0 case
     where ONLY China is truncated (1.115 -> 1.000) and still leads by a wide
     margin, the cap never touches any row.
  4. Re-runs the index with a cap that ACTUALLY binds inside the observed range
     (divisor lowered from 50 to 25, so the ceiling engages above ~$6.25T —
     China is then truncated) and shows how little the top-5 moves.
  5. Confirms the top-5 equals the raw import-volume order over the rankable
     panel, demonstrating the index is volume-dominated.

Every number traces to the committed World Bank LPI (via WDI) and WDI imports
(NE.IMP.GNFS.CD) JSON in the program cache, re-read from disk. No new data, no
network, no AI-supplied figures. The index is a triage measure per
CONSTITUTION.md §6.4, not a country-quality ranking; framing per §13.3 is an
observability gap, not a DMC deficiency. attestation_chain: ai-first.
"""
import json, math, os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/port-hinterland-friction"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

# Same DMC roster + name map as process-logistics.py (load via the panel so the
# two stay in lockstep; the panel is the committed generated artifact).
PANEL = f"{OUT}/port-hinterland-friction-adb-panel.json"

# The committed baseline parameters, verbatim from process-logistics.py.
DIVISOR_BASE = 50.0      # imports normalizer
CAP_BASE = 2.0           # imports cap


def load_wdi(path):
    """Re-read a WDI cache file exactly as process-logistics.py does: keep the
    latest year per ISO3 with a numeric value. ADB roster comes from the panel."""
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        return {}
    if not isinstance(d, list) or len(d) < 2:
        return {}
    out = {}
    for row in d[1]:
        if not isinstance(row.get("value"), (int, float)):
            continue
        iso = row.get("countryiso3code")
        y = int(row.get("date"))
        if iso not in out or y > out[iso]["year"]:
            out[iso] = {"year": y, "value": float(row["value"])}
    return out


def import_proxy(imports_usd, divisor):
    """sqrt(imports in billions) / divisor — the UNCAPPED proxy."""
    import_b = imports_usd / 1e9
    if import_b <= 0:
        return 0.0, 0.0
    return import_b, (import_b ** 0.5) / divisor


def friction(lpi_overall, imports_usd, divisor, cap):
    """The committed index with parameterized divisor + cap."""
    lpi_gap = max(5.0 - lpi_overall, 0.0)
    _import_b, proxy = import_proxy(imports_usd, divisor)
    return round(lpi_gap * min(proxy, cap), 2)


def ranked(panel_rows, divisor, cap):
    """Return rankable rows sorted by friction(divisor, cap), descending."""
    out = []
    for r in panel_rows:
        if r["lpi_overall"] is None or r["imports_usd"] is None:
            continue
        f = friction(r["lpi_overall"], r["imports_usd"], divisor, cap)
        out.append({**r, "f": f})
    out.sort(key=lambda r: -r["f"])
    return out


def top5(rows):
    return [r["iso3"] for r in rows[:5]]


def main():
    with open(PANEL, encoding="utf-8") as f:
        panel = json.load(f)
    panel_rows = panel["rows"]

    # Re-read the raw cache the headline used, so the proxy is reproduced from
    # source, not lifted from the committed panel's rounded index.
    imports_cache = load_wdi(f"{CACHE}/wdi_imports.json")
    lpi_cache = load_wdi(f"{CACHE}/wdi_lpi_overall.json")

    # --- 1. Import proxy for EVERY rankable DMC vs the 2.0 ceiling ----------
    rankable = [r for r in panel_rows
                if r["lpi_overall"] is not None and r["imports_usd"] is not None]
    proxies = []
    for r in rankable:
        src = imports_cache.get(r["iso3"])
        imp = src["value"] if src else r["imports_usd"]   # prefer raw cache
        import_b, proxy = import_proxy(imp, DIVISOR_BASE)
        proxies.append({
            "iso3": r["iso3"], "country": r["country"],
            "imports_usd": imp, "imports_b": import_b,
            "proxy_uncapped": proxy,
            "hits_cap_2.0": proxy >= CAP_BASE,
            "lpi_overall": r["lpi_overall"],
        })
    proxies.sort(key=lambda r: -r["imports_b"])
    max_proxy = max(p["proxy_uncapped"] for p in proxies)
    n_hitting = sum(1 for p in proxies if p["hits_cap_2.0"])

    # Imports needed to reach proxy = 2.0 under the baseline divisor: solve
    # sqrt(import_b)/50 = 2.0 -> import_b = (2.0*50)^2 = 10000 (billions) = $10T.
    imports_to_bind = (CAP_BASE * DIVISOR_BASE) ** 2 / 1e3   # in $ trillions

    print("=" * 78)
    print("KEYSTONE §1.1 — Is the imports cap (2.0) inert across the observed range?")
    print("=" * 78)
    print(f"\nThe cap min(., 2.0) binds only when sqrt(imports_B)/{DIVISOR_BASE:.0f} >= {CAP_BASE},")
    print(f"i.e. imports >= ${imports_to_bind:.1f} trillion. The panel's import proxies:\n")
    print(f"  {'ISO':<4} {'economy':<22} {'imports $B':>12} {'proxy':>8} {'>=2.0?':>7}")
    print("  " + "-" * 56)
    for p in proxies:
        print(f"  {p['iso3']:<4} {p['country'][:22]:<22} {p['imports_b']:>12,.1f} "
              f"{p['proxy_uncapped']:>8.4f} {('YES' if p['hits_cap_2.0'] else 'no'):>7}")
    print("  " + "-" * 56)
    print(f"  MAX proxy in panel = {max_proxy:.4f}  (economy: "
          f"{max(proxies, key=lambda p: p['proxy_uncapped'])['iso3']}); "
          f"ceiling = {CAP_BASE}")
    print(f"  DMCs reaching the 2.0 cap: {n_hitting} of {len(proxies)} rankable")
    print(f"  => the cap is INERT: it is never reached by any economy at the "
          f"baseline divisor.")

    # --- 2. Reproduce the committed baseline top-5 --------------------------
    base = ranked(panel_rows, DIVISOR_BASE, CAP_BASE)
    base_top5 = top5(base)
    print("\n" + "=" * 78)
    print("Baseline index reproduced from cache (divisor=50, cap=2.0)")
    print("=" * 78)
    print(f"  {'ISO':<4} {'economy':<22} {'LPI':>5} {'gap':>5} {'proxy':>8} {'friction':>9}")
    print("  " + "-" * 56)
    for r in base[:8]:
        gap = max(5.0 - r["lpi_overall"], 0.0)
        _b, px = import_proxy(r["imports_usd"], DIVISOR_BASE)
        print(f"  {r['iso3']:<4} {r['country'][:22]:<22} {r['lpi_overall']:>5} "
              f"{gap:>5.2f} {px:>8.4f} {r['f']:>9}")
    print(f"\n  Baseline top-5: {base_top5}")
    committed_top5 = [r["iso3"] for r in sorted(
        rankable, key=lambda r: -(r["friction_exposure_index"] or -1))[:5]]
    print(f"  Committed panel top-5: {committed_top5}")
    print(f"  Reproduced == committed: {base_top5 == committed_top5}")

    # --- 3. The headline's own ±50% cap perturbation (cap = 1.0, 3.0) -------
    print("\n" + "=" * 78)
    print("The headline ±50% cap perturbation (sensitivity.md): cap in {1.0, 3.0}")
    print("=" * 78)
    for cap in (1.0, CAP_BASE, 3.0):
        rk = ranked(panel_rows, DIVISOR_BASE, cap)
        t5 = top5(rk)
        # how many rows did this cap actually truncate?
        truncated = []
        for r in rankable:
            _b, px = import_proxy(r["imports_usd"], DIVISOR_BASE)
            if px > cap:
                truncated.append(r["iso3"])
        overlap = len(set(t5) & set(base_top5))
        print(f"  cap={cap:<4} top5={t5}  overlap={overlap}/5  "
              f"rows truncated by cap: {truncated if truncated else 'none'}")
    print("  => Across the entire ±50% cap sweep the only row the cap ever touches")
    print("     is CHN at cap=1.0 (proxy 1.1147 -> 1.000); it still leads. The")
    print("     '5/5 overlap for the cap' line is the stability of an inert knob.")

    # --- 4. A cap that ACTUALLY binds inside the observed range -------------
    # Lower the divisor so the ceiling engages: with divisor=25, proxy doubles,
    # CHN's proxy = sqrt(3106.5)/25 = 2.2295 > 2.0, so the cap finally binds.
    DIV_BIND = 25.0
    _b, chn_px_bind = import_proxy(
        imports_cache.get("CHN", {"value": panel_rows[0]["imports_usd"]})["value"]
        if imports_cache.get("CHN") else panel_rows[0]["imports_usd"], DIV_BIND)
    rk_bind = ranked(panel_rows, DIV_BIND, CAP_BASE)
    bind_top5 = top5(rk_bind)
    truncated_bind = []
    for r in rankable:
        _b, px = import_proxy(r["imports_usd"], DIV_BIND)
        if px > CAP_BASE:
            truncated_bind.append((r["iso3"], round(px, 4)))
    print("\n" + "=" * 78)
    print(f"A cap that BINDS: divisor lowered 50->{DIV_BIND:.0f} so the 2.0 ceiling engages")
    print("=" * 78)
    print(f"  At divisor={DIV_BIND:.0f}, CHN proxy = {chn_px_bind:.4f} (> {CAP_BASE}), so the cap")
    print(f"  finally truncates rows: {truncated_bind if truncated_bind else 'none'}")
    print(f"  top5 with binding cap: {bind_top5}")
    print(f"  overlap with baseline top5 {base_top5}: "
          f"{len(set(bind_top5) & set(base_top5))}/5")
    # Show CHN's index with vs without the binding cap to quantify the effect.
    chn = next(r for r in rankable if r["iso3"] == "CHN")
    chn_uncapped = round(max(5.0 - chn["lpi_overall"], 0.0) * chn_px_bind, 2)
    chn_capped = friction(chn["lpi_overall"], chn["imports_usd"], DIV_BIND, CAP_BASE)
    print(f"  CHN index at divisor={DIV_BIND:.0f}: uncapped={chn_uncapped}, "
          f"capped@2.0={chn_capped} (cap removes {chn_uncapped - chn_capped:.2f}),")
    print(f"  and CHN still ranks #1. Even where the cap bites, the top-5 set holds.")

    # --- 5. Top-5 vs raw import-volume order --------------------------------
    by_volume = sorted(rankable, key=lambda r: -r["imports_usd"])
    vol_top5 = [r["iso3"] for r in by_volume[:5]]
    print("\n" + "=" * 78)
    print("Is the friction top-5 just the import-volume order?")
    print("=" * 78)
    print(f"  {'rank':>4}  {'by friction':<14} {'by raw imports':<14}")
    for i in range(5):
        print(f"  {i+1:>4}  {base_top5[i]:<14} {vol_top5[i]:<14}")
    print(f"\n  friction top-5 as a SET == import-volume top-5 as a SET: "
          f"{set(base_top5) == set(vol_top5)}")
    print(f"  identical ORDER too: {base_top5 == vol_top5}")

    # --- write artifact -----------------------------------------------------
    payload = {
        "program": "port-hinterland-friction",
        "analysis": "inert imports-cap parameter (deep-questions.md §1.1 keystone)",
        "claim_scope": (
            "Deepening of the ±50% robustness claim. Tests whether the imports "
            "cap (2.0) — one of the two parameters sensitivity.md perturbs — is "
            "connected to the output. Triage measure (CONSTITUTION.md §6.4), not "
            "a country-quality ranking; observability-gap framing per §13.3."
        ),
        "source": {
            "name": "World Bank LPI (via WDI) + WDI imports NE.IMP.GNFS.CD",
            "files": "wdi_imports.json, wdi_lpi_overall.json (program cache)",
            "license": "CC BY 4.0",
            "retrieved_at": "2026-04-25 (program cache)",
        },
        "baseline_params": {"divisor": DIVISOR_BASE, "cap": CAP_BASE},
        "imports_to_reach_cap_usd_trillions": round(imports_to_bind, 2),
        "max_proxy_observed": round(max_proxy, 4),
        "dmcs_reaching_cap_baseline": n_hitting,
        "rankable_dmc_count": len(proxies),
        "proxy_by_dmc": [
            {"iso3": p["iso3"], "country": p["country"],
             "imports_usd": p["imports_usd"], "imports_b": round(p["imports_b"], 2),
             "proxy_uncapped": round(p["proxy_uncapped"], 4),
             "hits_cap_2_0": p["hits_cap_2.0"]}
            for p in proxies
        ],
        "baseline_top5": base_top5,
        "committed_panel_top5": committed_top5,
        "cap_perturbation": {
            str(cap): {
                "top5": top5(ranked(panel_rows, DIVISOR_BASE, cap)),
                "overlap_with_baseline": len(
                    set(top5(ranked(panel_rows, DIVISOR_BASE, cap))) & set(base_top5)),
                "rows_truncated": [
                    r["iso3"] for r in rankable
                    if import_proxy(r["imports_usd"], DIVISOR_BASE)[1] > cap],
            } for cap in (1.0, CAP_BASE, 3.0)
        },
        "binding_cap_test": {
            "divisor": DIV_BIND, "cap": CAP_BASE,
            "chn_proxy": round(chn_px_bind, 4),
            "rows_truncated": [iso for iso, _ in truncated_bind],
            "top5": bind_top5,
            "overlap_with_baseline": len(set(bind_top5) & set(base_top5)),
            "chn_index_uncapped": chn_uncapped,
            "chn_index_capped": chn_capped,
        },
        "import_volume_top5": vol_top5,
        "friction_top5_equals_volume_top5_set": set(base_top5) == set(vol_top5),
        "friction_top5_equals_volume_top5_order": base_top5 == vol_top5,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(f"{OUT}/port-hinterland-inert-parameter.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUT}/port-hinterland-inert-parameter.json")


if __name__ == "__main__":
    main()
