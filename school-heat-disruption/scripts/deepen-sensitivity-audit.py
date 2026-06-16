"""School Heat Disruption — deepening pass: audit the top-1 robustness
claim against the committed sensitivity runs.

Answers the keystone in `school-heat-disruption/deep-questions.md` §1.1:
the headline asserts Cambodia (KHM) "persistently holds the top position
across every ±50% perturbation," but the committed `sensitivity-runs.json`
appears to contradict it. This script parses that file — nothing else —
and reports, run by run:

  - KHM's rank and value,
  - the run's top economy and value,
  - whether KHM is #1 in the run,
  - whether the run is DEGENERATE (every economy scores exactly 0.0, an
    all-zeros tie that cannot discriminate any economy and so cannot
    confirm a #1), and
  - whether the run is RANK-LOSING for KHM (KHM is not #1).

It then re-states the robustness honestly: strip the degenerate and
rank-losing runs and report across how many DISCRIMINATING runs KHM is
actually #1, versus the "every perturbation" the headline claims.

Every number is read from the committed `sensitivity-runs.json`
(generated 2026-04-26 by the program's own perturbation harness over the
on-disk WDI/CCKP panel). No new data, no network, no AI-supplied figures.
Per CONSTITUTION.md §6.4 the school-heat-pressure index is a triage
measure, not a ranking of school quality; per §13.3 the object is the
unobserved thermal exposure of school-age children during instructional
time, not a country deficiency. attestation_chain: ai-first.
"""
import json, os
from datetime import datetime, timezone

BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/school-heat-disruption"
RUNS = f"{BASE}/sensitivity-runs.json"
PANEL = f"{BASE}/generated/school-heat-adb-panel.json"
OUT = f"{BASE}/generated"
os.makedirs(OUT, exist_ok=True)

ZERO_EPS = 1e-9  # treat |value| <= eps as zero when testing for an all-zeros tie


def classify(run):
    """Return a dict describing KHM's standing and the run's character.

    A run is read exactly as committed. `top10` is the run's ranked head;
    the first element is the run's top economy. A run is degenerate when
    every reported value is (within eps) zero — an all-zeros tie in which
    no economy is distinguished from any other, so no #1 can be inferred.
    """
    rows = run["top10"]
    top = rows[0]
    top_iso = top["iso3"]
    top_val = top["value"]

    # KHM's rank within the reported head (1-indexed). If KHM is not in the
    # head we record rank as None and the run as rank-losing for KHM.
    khm_rank = None
    khm_val = None
    for i, r in enumerate(rows, start=1):
        if r["iso3"] == "KHM":
            khm_rank = i
            khm_val = r["value"]
            break

    all_zero = all(abs(r["value"]) <= ZERO_EPS for r in rows)
    khm_is_top1 = (top_iso == "KHM") and not all_zero

    if all_zero:
        verdict = "DEGENERATE (all-zeros tie; cannot discriminate)"
        discriminating = False
    elif khm_is_top1:
        verdict = "KHM #1 (discriminating)"
        discriminating = True
    else:
        verdict = f"RANK-LOSING for KHM (top = {top_iso})"
        discriminating = True  # it discriminates; KHM just loses it

    return {
        "label": run["label"],
        "knob": {k: v for k, v in run.items() if k not in ("label", "top10")},
        "top_iso": top_iso,
        "top_value": top_val,
        "khm_rank": khm_rank,
        "khm_value": khm_val,
        "all_zero": all_zero,
        "khm_is_top1": khm_is_top1,
        "discriminating": discriminating,
        "verdict": verdict,
        "n_reported": len(rows),
    }


def main():
    doc = json.load(open(RUNS, encoding="utf-8"))
    runs = doc["runs"]
    file_claim = doc.get("common_top5_across_runs")

    audited = [classify(r) for r in runs]

    n_total = len(audited)
    n_degenerate = sum(1 for a in audited if a["all_zero"])
    n_rank_losing = sum(1 for a in audited if a["discriminating"] and not a["khm_is_top1"])
    n_discriminating = sum(1 for a in audited if a["discriminating"])
    n_khm_top1_all = sum(1 for a in audited if a["khm_is_top1"])
    # Among runs that actually discriminate (not all-zeros), how often is
    # KHM genuinely #1?
    n_khm_top1_discriminating = sum(
        1 for a in audited if a["discriminating"] and a["khm_is_top1"]
    )

    degenerate_labels = [a["label"] for a in audited if a["all_zero"]]
    rank_losing_labels = [
        a["label"] for a in audited if a["discriminating"] and not a["khm_is_top1"]
    ]
    khm_top1_labels = [a["label"] for a in audited if a["khm_is_top1"]]

    # ---- console report -------------------------------------------------
    print("=" * 74)
    print("SCHOOL-HEAT-DISRUPTION -- top-1 robustness audit (sensitivity-runs.json)")
    print("=" * 74)
    print(f"runs file generated_at : {doc.get('generated_at', '(none)')}")
    print(f"metric                 : {doc.get('metric')}")
    print(f"file's own claim       : common_top5_across_runs = {file_claim}")
    print(f"runs in file           : {n_total}")
    print()

    hdr = f"{'run':<20} {'knob':<24} {'top_iso':<8} {'top_val':>9}  {'KHM#':>4} {'KHM_val':>9}  verdict"
    print(hdr)
    print("-" * len(hdr))
    for a in audited:
        knob = ", ".join(f"{k}={v}" for k, v in a["knob"].items()) or "(none)"
        khm_rank = "-" if a["khm_rank"] is None else str(a["khm_rank"])
        khm_val = "-" if a["khm_value"] is None else f"{a['khm_value']:.2f}"
        print(
            f"{a['label']:<20} {knob[:24]:<24} {a['top_iso']:<8} "
            f"{a['top_value']:>9.2f}  {khm_rank:>4} {khm_val:>9}  {a['verdict']}"
        )

    print()
    print("-" * 74)
    print("HONEST RE-STATEMENT OF ROBUSTNESS")
    print("-" * 74)
    print(f"  total perturbation runs (incl. baseline)        : {n_total}")
    print(f"  degenerate all-zeros runs (cannot discriminate) : {n_degenerate}  {degenerate_labels}")
    print(f"  rank-losing runs (KHM is NOT #1)                : {n_rank_losing}  {rank_losing_labels}")
    print(f"  discriminating runs (not all-zeros)             : {n_discriminating}")
    print()
    print(f"  KHM #1 counting EVERY run as the headline does  : {n_khm_top1_all} / {n_total}")
    print(f"  KHM #1 among DISCRIMINATING runs                : {n_khm_top1_discriminating} / {n_discriminating}")
    print(f"      (these are: {khm_top1_labels})")
    print()
    # The strict denominator the deep-question asks for: strip BOTH the
    # degenerate run AND the rank-losing run, then ask how many remain and
    # whether KHM tops all of them.
    n_after_strip = n_total - n_degenerate - n_rank_losing
    print(f"  After stripping degenerate + rank-losing runs   : {n_after_strip} runs remain")
    print(f"  KHM #1 across those {n_after_strip} surviving runs          : "
          f"{n_khm_top1_discriminating == n_after_strip and n_after_strip > 0}")
    print()

    headline_ok = (n_khm_top1_all == n_total)
    print(f"  Headline 'KHM #1 across EVERY perturbation' true? : {headline_ok}")
    if not headline_ok:
        print(f"      -> FALSE. KHM loses {n_rank_losing} run(s) outright "
              f"({rank_losing_labels}) and 'passes' {n_degenerate} only by "
              f"an all-zeros tie ({degenerate_labels}).")

    # ---- machine artifact ----------------------------------------------
    payload = {
        "program": "school-heat-disruption",
        "analysis": "top-1 robustness audit of the school-heat-pressure index",
        "claim_scope": (
            "Re-reads the committed sensitivity-runs.json and reports, run by "
            "run, KHM's rank, the top economy, and whether the run discriminates "
            "(not an all-zeros tie). Strips degenerate and rank-losing runs and "
            "restates across how many discriminating runs KHM is actually #1. "
            "Triage measure (CONSTITUTION.md §6.4); the object is the unobserved "
            "in-session thermal exposure of school-age children (§13.3), not a "
            "country quality ranking."
        ),
        "source": {
            "name": "school-heat-disruption/sensitivity-runs.json (committed)",
            "runs_generated_at": doc.get("generated_at"),
            "upstream": (
                "perturbation harness over the on-disk WDI (SE.PRM.ENRL.TC.ZS, "
                "SP.POP.0014.TO.ZS, SP.POP.TOTL) + CCKP CMIP6 tasmax 1995-2014 "
                "panel; no network"
            ),
        },
        "file_claim_common_top5_across_runs": file_claim,
        "counts": {
            "runs_total": n_total,
            "degenerate_all_zero": n_degenerate,
            "rank_losing_for_khm": n_rank_losing,
            "discriminating": n_discriminating,
            "khm_top1_counting_all_runs": n_khm_top1_all,
            "khm_top1_among_discriminating": n_khm_top1_discriminating,
            "runs_after_stripping_degenerate_and_rank_losing": n_after_strip,
        },
        "degenerate_labels": degenerate_labels,
        "rank_losing_labels": rank_losing_labels,
        "khm_top1_labels": khm_top1_labels,
        "headline_every_perturbation_true": headline_ok,
        "per_run": audited,
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out_path = f"{OUT}/school-heat-sensitivity-audit.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
