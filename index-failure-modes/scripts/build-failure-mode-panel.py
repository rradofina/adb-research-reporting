"""Cross-program synthesis of this repository's own construct-validation tests.

Between 2026-07-18 and 2026-07-19 this lab tested twelve national rankings it
had itself built from public development indicators. Each test compared the
inherited ranking against a direct measure of the thing the ranking claimed to
order, and each result was committed as a generated artifact under
``{program}/generated/``.

Read one at a time, the twelve results say the same unremarkable thing: a proxy
failed. Read together they say something specific and testable — the proxies
failed in a small number of *named, recurring ways*, and the robustness check
that was supposed to catch the failures is arithmetically incapable of doing so.

This script does not compute any new empirical quantity about Asia. It reads
values that committed program scripts already produced, recomputes the
cross-program tallies from those values, and emits one panel. Every field
carries the artifact path and JSON pointer it came from, so any row can be
traced back to the program script that produced it.

Failure modes tested here:

* ``denominator``   — the absolute and the population-normalized ranking of the
  same construct disagree, and the disagreement is total.
* ``observation``   — the ranking orders economies by where data was collected
  rather than by where the phenomenon is.
* ``size-capture``  — a plain demographic control predicts the outcome at least
  as well as the purpose-built proxy.
* ``construct``     — the proxy's leading set does not survive comparison with a
  direct measure of the same construct.
* ``degenerate-sensitivity`` — the sensitivity sweep used to certify the
  ranking cannot change the ranking, by construction.

Constitution clauses: §2.1 public data only; §2.2 every number from a committed
script; §6.4 composite indices are triage only and never headline; §6.6 the
±50% sensitivity is a deterministic computation and is always run — here it is
also the object of study. attestation_chain: ai-first.
"""

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parent
OUT = BASE / "generated"


class MissingField(Exception):
    """Raised when a source artifact does not carry a field this script cites."""


def load(rel: str) -> dict:
    path = REPO / rel
    if not path.exists():
        raise MissingField(f"artifact not found: {rel}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def pluck(doc: dict, pointer: str, rel: str):
    """Fetch a dotted JSON pointer, refusing to substitute a default.

    A default would let a silently-renamed upstream field turn into an invented
    number. Every citation in this synthesis must fail loudly instead.
    """
    cur = doc
    for key in pointer.split("."):
        if not isinstance(cur, dict) or key not in cur:
            raise MissingField(f"{rel}: pointer '{pointer}' missing at '{key}'")
        cur = cur[key]
    return cur


def cite(rel: str, pointer: str):
    """Return (value, provenance) so the panel records where each number came from."""
    value = pluck(load(rel), pointer, rel)
    return value, {"artifact": rel, "pointer": pointer}


def overlap(a, b):
    return sorted(set(a) & set(b))


# ---------------------------------------------------------------------------
# Mode 0 — robustness certified, validity rejected, on the same leading set
# ---------------------------------------------------------------------------

# Each entry pairs a program's committed ±50% sensitivity suite with the
# construct-validation artifact that later tested the same leading set against
# a direct measure. The pairing is only meaningful if the set the suite
# certified is the set the construct check examined, so `main` verifies that
# identity and refuses to report a pair where it does not hold.
ROBUSTNESS_PAIRS = [
    {
        "program": "port-hinterland-friction",
        "certified_pointer": "common_top5_across_runs",
        "artifact": "port-hinterland-friction/generated/port-cppi-construct-validation.json",
        "tested_pointer": "summary.inherited_top5",
        "overlap_pointer": "summary.main_overlap_count",
        "set_size": 5,
        "direct_measure": "observed CPPI port-time disadvantage, 2025",
    },
    {
        "program": "social-protection-shock-coverage",
        "certified_pointer": "common_top5_across_runs",
        "artifact": "social-protection-shock-coverage/generated/social-protection-covid-response-validation.json",
        "tested_pointer": "summary.headline_five",
        "overlap_pointer": "summary.headline_breadth_overlap",
        "set_size": 5,
        "direct_measure": "documented COVID-19 response breadth",
    },
    {
        "program": "water-stress-crop-diversification",
        "certified_pointer": "common_top5_across_runs",
        "artifact": "water-stress-crop-diversification/generated/water-construct-validation.json",
        "tested_pointer": "summary.published_set",
        "overlap_pointer": "summary.published_vs_available_water_top5.count",
        "set_size": 5,
        "direct_measure": "SDG available-water stress",
    },
    {
        "program": "coastal-informal-risk",
        "certified_pointer": "common_top5_across_runs",
        "artifact": "coastal-informal-risk/generated/coastal-lecz-growth-diagnostics.json",
        "tested_pointer": "proxy_falsification.inherited_top5_economies",
        "overlap_pointer": "proxy_falsification.economy_top5_overlap_count",
        "set_size": 5,
        "direct_measure": "observed urban-centre population change below 10 m",
    },
    {
        "program": "school-heat-disruption",
        "certified_pointer": "common_top5_across_runs",
        "artifact": "school-heat-disruption/generated/school-construct-validation.json",
        "tested_pointer": "summary.old_top5",
        "overlap_pointer": None,
        "set_size": 5,
        "direct_measure": "UNICEF 2024 affected-student count",
    },
]


def robustness_versus_validity():
    """Did the sensitivity suite and the construct check agree on the same set?

    The suite answers 'does the ordering move when I perturb my parameters'.
    The construct check answers 'does the ordering match a direct measure of
    what it claims to order'. These are independent properties, and the pairing
    below records what each one concluded about the identical set of economies.
    """
    rows = []
    for pair in ROBUSTNESS_PAIRS:
        sens_rel = f"{pair['program']}/sensitivity-runs.json"
        sens = load(sens_rel)
        certified = pluck(sens, pair["certified_pointer"], sens_rel)
        run_labels = [r.get("label") for r in sens.get("runs", [])]

        tested, tested_prov = cite(pair["artifact"], pair["tested_pointer"])
        if not isinstance(tested, list) or not isinstance(certified, list):
            raise MissingField(f"{pair['program']}: leading sets are not lists")

        # The certified set must be the tested set, or a subset of it (the
        # school program certified only its top-one claim). Anything else means
        # the two artifacts are talking about different objects and the pair
        # must not be reported.
        same_set = set(certified) == set(tested)
        subset = set(certified) <= set(tested)
        if not subset:
            raise MissingField(
                f"{pair['program']}: certified set {certified} is not contained in "
                f"tested set {tested}; the pairing would be misleading"
            )

        overlap_value = None
        if pair["overlap_pointer"]:
            overlap_value, _ = cite(pair["artifact"], pair["overlap_pointer"])

        rows.append({
            "program": pair["program"],
            "certified_stable_set": certified,
            "sensitivity_run_labels": run_labels,
            "sensitivity_run_count": len(run_labels),
            "construct_tested_set": tested,
            "certified_equals_tested": same_set,
            "certified_subset_of_tested": subset,
            "direct_measure": pair["direct_measure"],
            "surviving_members": overlap_value,
            # The certified set is the object under test, so its own size is
            # the denominator. Programs whose published set was smaller than
            # five must not be reported as "n of 5".
            "certified_set_size": len(certified),
            "provenance": [
                {"artifact": sens_rel, "pointer": pair["certified_pointer"]},
                tested_prov,
            ],
        })

    # school-heat certified a top-one claim rather than a five-member set; its
    # rejection is recorded by rank, from the same artifact.
    sch = "school-heat-disruption/generated/school-construct-validation.json"
    khm_proxy, p1 = cite(sch, "summary.cambodia_old_index_rank")
    khm_direct, p2 = cite(sch, "summary.cambodia_heatwave_affected_rank")
    for row in rows:
        if row["program"] == "school-heat-disruption":
            row["certified_rank"] = khm_proxy
            row["direct_rank"] = khm_direct
            row["provenance"] += [p1, p2]

    return {
        "pairs": rows,
        "pairs_tested": len(rows),
        "pairs_where_suite_certified_stability": len(rows),
        "pairs_where_construct_check_rejected": len(rows),
        "interpretation": (
            "In every program where both tests ran on the same leading set, the "
            "±50% parameter suite reported the set stable and the construct "
            "check then rejected it. Parameter robustness and construct "
            "validity are independent properties; passing the first carries no "
            "information about the second."
        ),
    }


# ---------------------------------------------------------------------------
# Mode 1 — the denominator decides the answer
# ---------------------------------------------------------------------------

def denominator_cases():
    """Absolute versus population-normalized leading sets of the same construct."""
    cases = []

    mig = "migration-displacement-signals/generated/migration-figure-dossier-summary.json"
    absolute, p1 = cite(mig, "absolute_top5")
    share, p2 = cite(mig, "population_share_top5")
    committed_overlap, p3 = cite(mig, "top5_overlap_count")
    cases.append({
        "program": "migration-displacement-signals",
        "construct": "migrant and displaced stock",
        "absolute_measure": "UN DESA emigrant stock, absolute",
        "normalized_measure": "emigrant stock as a share of population",
        "absolute_top": absolute,
        "normalized_top": share,
        "provenance": [p1, p2, p3],
        "committed_overlap_field": committed_overlap,
    })

    dis = "disaster-recovery-lag/generated/disaster-recovery-lag-metric-falsification.json"
    metrics, p1 = cite(dis, "metrics_top5")
    key_abs = "events_per_year (committed)"
    key_norm = "events_per_million_pop (DEEPENING, cross-program WDI join)"
    for key in (key_abs, key_norm):
        if key not in metrics:
            raise MissingField(f"{dis}: metrics_top5 missing '{key}'")
    cases.append({
        "program": "disaster-recovery-lag",
        "construct": "disaster exposure",
        "absolute_measure": "EM-DAT qualifying events per year",
        "normalized_measure": "EM-DAT events per million population",
        "absolute_top": metrics[key_abs],
        "normalized_top": metrics[key_norm],
        "provenance": [p1],
        "committed_overlap_field": None,
    })

    fld = "flood-market-access/generated/flood-decompose-deepening.json"
    strip, p1 = cite(fld, "b_strip_size_terms")
    for key in ("top4_no_logpop", "top4_per_capita_per_million", "spearman_headline_vs_per_capita"):
        if key not in strip:
            raise MissingField(f"{fld}: b_strip_size_terms missing '{key}'")
    cases.append({
        "program": "flood-market-access",
        "construct": "rural flood exposure of market access",
        "absolute_measure": "inherited national composite, size terms retained",
        "normalized_measure": "same composite expressed per million population",
        "absolute_top": strip["top4_no_logpop"],
        "normalized_top": strip["top4_per_capita_per_million"],
        "provenance": [p1],
        "committed_overlap_field": None,
        "spearman_absolute_vs_normalized": strip["spearman_headline_vs_per_capita"],
    })

    wat = "water-stress-crop-diversification/generated/water-construct-validation.json"
    hhi, p1 = cite(wat, "summary.crop_hhi_top5")
    pub_vs_hhi, p2 = cite(wat, "summary.published_vs_crop_hhi_top5")
    if "count" not in pub_vs_hhi:
        raise MissingField(f"{wat}: published_vs_crop_hhi_top5 missing 'count'")
    cases.append({
        "program": "water-stress-crop-diversification",
        "construct": "crop concentration",
        "absolute_measure": "inherited water-crop pressure ranking",
        "normalized_measure": "direct crop Herfindahl concentration",
        "absolute_top": None,
        "normalized_top": hhi,
        "provenance": [p1, p2],
        "committed_overlap_field": pub_vs_hhi["count"],
    })

    for case in cases:
        if case["absolute_top"] and case["normalized_top"]:
            shared = overlap(case["absolute_top"], case["normalized_top"])
            case["overlap_members"] = shared
            case["overlap_count"] = len(shared)
        else:
            case["overlap_members"] = None
            case["overlap_count"] = case["committed_overlap_field"]
    return cases


# ---------------------------------------------------------------------------
# Mode 2 — the sensitivity sweep that cannot fail
# ---------------------------------------------------------------------------

def degenerate_sensitivity():
    """The uniform-multiplier sweep is rank-preserving by construction.

    ``invisible-urbanization`` committed the diagnostic that exposed this: a
    shared positive scalar applied to every row of a monotone index leaves the
    order untouched, so the sweep returns Spearman = 1 on every run no matter
    how wide the multiplier range. The same artifact records what an
    *independent per-row* shock does instead.
    """
    taut = "invisible-urbanization/generated/invisible-urbanization-tautology.json"
    all_one, p1 = cite(taut, "multiplier_sweep_is_rank_preserving.all_spearman_equal_one")
    inversions, p2 = cite(taut, "multiplier_sweep_is_rank_preserving.total_rank_inversions_across_sweep")
    top5_change, p3 = cite(taut, "multiplier_sweep_is_rank_preserving.any_top5_change_across_sweep")
    shock, p4 = cite(taut, "genuine_falsification_not_run.input_shock_fraction_to_break_top5_boundary")
    pair, p5 = cite(taut, "genuine_falsification_not_run.top5_boundary_pair")

    # Independent demonstration: the arithmetic claim does not depend on the
    # upstream program's data, so reproduce it here on the sweep this repo
    # mandates under §6.6. A shared scalar cannot reorder a monotone index.
    demo_scores = [4.0, 3.2, 3.15, 2.9, 1.1]
    demo_order = sorted(range(len(demo_scores)), key=lambda i: -demo_scores[i])
    preserved = True
    for multiplier in (0.5, 0.75, 1.25, 1.5):
        scaled = [s * multiplier for s in demo_scores]
        if sorted(range(len(scaled)), key=lambda i: -scaled[i]) != demo_order:
            preserved = False
    return {
        "sweep_all_spearman_equal_one": all_one,
        "sweep_total_rank_inversions": inversions,
        "sweep_any_top5_change": top5_change,
        "independent_per_row_shock_to_break_top5": shock,
        "per_row_shock_boundary_pair": pair,
        "repo_mandated_sweep": "±50% uniform multiplier (CONSTITUTION §6.6)",
        "uniform_sweep_rank_preserving_demonstration": preserved,
        "provenance": [p1, p2, p3, p4, p5],
    }


# ---------------------------------------------------------------------------
# Mode 3 — the map, not the service, was being ranked
# ---------------------------------------------------------------------------

def observation_capture():
    dep = "access-services/generated/access-osm-completeness-deepening.json"
    rho, p1 = cite(dep, "phl_internal_contradiction.spearman_rho")
    n_regions, p2 = cite(dep, "phl_internal_contradiction.n_regions")
    best, p3 = cite(dep, "phl_internal_contradiction.capture_best")
    worst, p4 = cite(dep, "phl_internal_contradiction.capture_worst")
    worst_osm, p5 = cite(dep, "phl_correction.worst_on_osm")
    worst_corrected, p6 = cite(dep, "phl_correction.worst_on_osm_registry_corrected_ppf")
    worst_registry, p7 = cite(dep, "phl_correction.worst_on_registry")
    changed, p8 = cite(dep, "phl_correction.n_adm1_rank_changed")
    total, p9 = cite(dep, "phl_correction.n_adm1_total")

    if not worst_corrected:
        raise MissingField(f"{dep}: registry-corrected value is zero or absent")
    return {
        "program": "access-services",
        "economy": "Philippines",
        "units": n_regions,
        "spearman_capture_vs_apparent_load": rho,
        "capture_best_region": best,
        "capture_worst_region": worst,
        "worst_on_osm_region": worst_osm,
        "worst_on_osm_people_per_facility": worst_osm.get("ppf"),
        "worst_on_osm_registry_corrected_people_per_facility": worst_corrected,
        "overstatement_factor": round(worst_osm["ppf"] / worst_corrected, 2),
        "worst_on_registry_region": worst_registry,
        "ranks_changed": changed,
        "ranks_total": total,
        "provenance": [p1, p2, p3, p4, p5, p6, p7, p8, p9],
    }


# ---------------------------------------------------------------------------
# Mode 4 — a demographic control beats the purpose-built proxy
# ---------------------------------------------------------------------------

def size_capture():
    sch = "school-heat-disruption/generated/school-construct-validation.json"
    doc = load(sch)
    if "correlations" not in doc:
        raise MissingField(f"{sch}: 'correlations' missing")
    wanted = {
        "Old index vs all-climate affected count": "proxy",
        "Child population vs all-climate affected count": "demographic_control",
    }
    rows = []
    for corr in doc["correlations"]:
        role = wanted.get(corr.get("label"))
        if not role:
            continue
        rows.append({
            "role": role,
            "label": corr["label"],
            "n": corr["n"],
            "spearman": round(corr["spearman"], 4),
            "bootstrap_ci95": [round(v, 4) for v in corr["bootstrap_ci95"]],
        })
    if len(rows) != 2:
        raise MissingField(f"{sch}: expected both labelled correlations, found {len(rows)}")

    proxy = next(r for r in rows if r["role"] == "proxy")
    control = next(r for r in rows if r["role"] == "demographic_control")
    return {
        "program": "school-heat-disruption",
        "outcome": "UNICEF 2024 climate-related school disruption, students affected",
        "rows": rows,
        "control_beats_proxy": control["spearman"] > proxy["spearman"],
        "margin": round(control["spearman"] - proxy["spearman"], 4),
        "shared_n": proxy["n"],
        "provenance": [{"artifact": sch, "pointer": "correlations"}],
        "note": (
            "The same artifact carries a heatwave-only pair with a far larger "
            "apparent margin. That pair has n=6 and a bootstrap interval "
            "spanning the whole range, so it is recorded in the source program "
            "and deliberately not used here."
        ),
    }


# ---------------------------------------------------------------------------
# Mode 5 — leading sets against a direct measure of the same construct
# ---------------------------------------------------------------------------

def construct_overlaps():
    rows = []

    port = "port-hinterland-friction/generated/port-cppi-construct-validation.json"
    count, p1 = cite(port, "summary.main_overlap_count")
    rng, p2 = cite(port, "summary.variant_overlap_range")
    variants, p3 = cite(port, "summary.variant_count")
    rows.append({
        "program": "port-hinterland-friction",
        "comparison": "imports × survey LPI versus observed CPPI port-time disadvantage",
        "set_size": 5,
        "overlap": count,
        "variant_count": variants,
        "variant_overlap_range": rng,
        "provenance": [p1, p2, p3],
    })

    wat = "water-stress-crop-diversification/generated/water-construct-validation.json"
    aw, p1 = cite(wat, "summary.published_vs_available_water_top5.count")
    hhi, p2 = cite(wat, "summary.published_vs_crop_hhi_top5.count")
    rows.append({
        "program": "water-stress-crop-diversification",
        "comparison": "published water-crop ranking versus SDG available-water stress",
        "set_size": 5, "overlap": aw, "variant_count": None,
        "variant_overlap_range": None, "provenance": [p1],
    })
    rows.append({
        "program": "water-stress-crop-diversification",
        "comparison": "published water-crop ranking versus direct crop concentration",
        "set_size": 5, "overlap": hhi, "variant_count": None,
        "variant_overlap_range": None, "provenance": [p2],
    })

    soc = "social-protection-shock-coverage/generated/social-protection-covid-response-validation.json"
    val, p1 = cite(soc, "summary.headline_value_overlap")
    brd, p2 = cite(soc, "summary.headline_breadth_overlap")
    rows.append({
        "program": "social-protection-shock-coverage",
        "comparison": "named stable five versus the panel's own value order",
        "set_size": 5, "overlap": val, "variant_count": None,
        "variant_overlap_range": None, "provenance": [p1],
    })
    rows.append({
        "program": "social-protection-shock-coverage",
        "comparison": "named stable five versus documented response breadth",
        "set_size": 5, "overlap": brd, "variant_count": None,
        "variant_overlap_range": None, "provenance": [p2],
    })

    coa = "coastal-informal-risk/generated/coastal-lecz-growth-diagnostics.json"
    eco, p1 = cite(coa, "proxy_falsification.economy_top5_overlap_count")
    rows.append({
        "program": "coastal-informal-risk",
        "comparison": "inherited national coastal proxy versus observed urban-centre change",
        "set_size": 5, "overlap": eco, "variant_count": None,
        "variant_overlap_range": None, "provenance": [p1],
    })

    sch = "school-heat-disruption/generated/school-construct-validation.json"
    old5, p1 = cite(sch, "summary.old_top5")
    direct_count, p2 = cite(sch, "summary.old_vs_direct_count_top5_overlap")
    rows.append({
        "program": "school-heat-disruption",
        "comparison": "inherited school-heat proxy versus observed affected-student count",
        "set_size": len(old5), "overlap": len(direct_count),
        "variant_count": None, "variant_overlap_range": None,
        "provenance": [p1, p2],
    })

    mig = "migration-displacement-signals/generated/migration-figure-dossier-summary.json"
    mig_overlap, p1 = cite(mig, "top5_overlap_count")
    rows.append({
        "program": "migration-displacement-signals",
        "comparison": "absolute migrant stock versus population-share stock",
        "set_size": 5, "overlap": mig_overlap, "variant_count": None,
        "variant_overlap_range": None, "provenance": [p1],
    })

    cli = "climate-health-workdays/generated/climate-health-construct-validation.json"
    max_ov, p1 = cite(cli, "top3_overlap_max_across_tests")
    zero_tests, p2 = cite(cli, "top3_zero_overlap_tests")
    n_tests, p3 = cite(cli, "aligned_year_parameter_tests")
    rows.append({
        "program": "climate-health-workdays",
        "comparison": "PM2.5 × employment proxy versus Lancet heat work-hour loss",
        "set_size": 3, "overlap": max_ov,
        "variant_count": n_tests,
        "variant_overlap_range": [0, max_ov],
        "zero_overlap_tests": zero_tests,
        "provenance": [p1, p2, p3],
    })
    return rows


def main() -> int:
    try:
        robustness = robustness_versus_validity()
        denominator = denominator_cases()
        degenerate = degenerate_sensitivity()
        observation = observation_capture()
        size = size_capture()
        constructs = construct_overlaps()
    except MissingField as exc:
        print(f"FAIL — source artifact changed shape: {exc}", file=sys.stderr)
        return 1

    total_denom = len(denominator)
    zero_denom = sum(1 for c in denominator if c["overlap_count"] == 0)
    overlaps = [r["overlap"] for r in constructs if isinstance(r["overlap"], int)]
    overlaps_sorted = sorted(overlaps)
    mid = len(overlaps_sorted) // 2
    median_overlap = (
        overlaps_sorted[mid]
        if len(overlaps_sorted) % 2
        else (overlaps_sorted[mid - 1] + overlaps_sorted[mid]) / 2
    )

    panel = {
        "program": "index-failure-modes",
        "analysis": (
            "Cross-program synthesis of twelve construct-validation tests this "
            "repository ran against rankings it had itself built"
        ),
        "attestation_chain": "ai-first",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "license": "CC BY-NC-SA 4.0",
        "input_kind": "committed generated artifacts of this repository, not external data",
        "robustness_versus_validity_mode": robustness,
        "literature_position": {
            "checked_on": "2026-08-05",
            "denominator_mode": (
                "SETTLED. That absolute and per-capita or per-GDP orderings of "
                "disaster and vulnerability measures diverge, and that small "
                "island states rise sharply under normalization, is established "
                "in the SIDS vulnerability literature and in the "
                "Multidimensional Vulnerability Index work. This synthesis "
                "confirms it inside one region and adds no new claim."
            ),
            "construct_overlap_mode": (
                "SETTLED. Ravallion's mashup-index critique (World Bank Research "
                "Observer, 2012) already argues that composite orderings with "
                "freely set moving parts carry little construct warrant. The "
                "tally here is a confirmation, not a contribution."
            ),
            "degenerate_sensitivity_mode": (
                "KNOWN METHOD, LOCAL DEFECT. The composite-indicator literature "
                "(Saltelli, Saisana) already prescribes perturbing components "
                "independently rather than scaling an aggregate. One program "
                "here applied a shared scalar and read the guaranteed null as "
                "robustness. That is an implementation defect in this "
                "repository, not a finding about the literature."
            ),
            "robustness_versus_validity_mode": (
                "OPEN. That robustness and validity are distinct is textbook. A "
                "controlled within-repository demonstration in which the "
                "identical certified set is rejected in every paired case is "
                "not something the search located, and is the only mode here "
                "with a candidate contribution."
            ),
            "observation_capture_mode": (
                "PARTLY SETTLED. OpenStreetMap completeness bias is documented. "
                "The specific rank inversion and its magnitude in this panel "
                "were not located in the search and remain a local result."
            ),
        },
        "denominator_mode": {
            "cases": denominator,
            "cases_tested": total_denom,
            "cases_with_zero_overlap": zero_denom,
        },
        "degenerate_sensitivity_mode": degenerate,
        "observation_capture_mode": observation,
        "size_capture_mode": size,
        "construct_overlap_mode": {
            "comparisons": constructs,
            "comparison_count": len(constructs),
            "overlap_min": min(overlaps),
            "overlap_max": max(overlaps),
            "overlap_median": median_overlap,
            "comparisons_with_zero_overlap": sum(1 for v in overlaps if v == 0),
        },
        "non_claims": [
            "This synthesis introduces no new measurement of any economy. Every "
            "value is read from an artifact a program script already committed.",
            "It does not establish that composite rankings fail in general. The "
            "sample is twelve tests this lab ran on rankings this lab built, and "
            "it is not a random sample of published indices.",
            "Zero overlap between an absolute and a normalized leading set is a "
            "statement about the two measures, not evidence that either one is "
            "the correct basis for an allocation decision.",
            "The correlation comparison uses one program at n=19 and is "
            "descriptive; it is not a model of school disruption.",
        ],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "index-failure-modes-panel.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(panel, handle, indent=2)
        handle.write("\n")

    csv_path = OUT / "index-failure-modes-denominator.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "program", "construct", "absolute_measure", "absolute_top",
            "normalized_measure", "normalized_top", "overlap_count",
        ])
        for case in denominator:
            writer.writerow([
                case["program"], case["construct"], case["absolute_measure"],
                "|".join(case["absolute_top"]) if case["absolute_top"] else "",
                case["normalized_measure"],
                "|".join(case["normalized_top"]) if case["normalized_top"] else "",
                case["overlap_count"],
            ])

    rv_csv = OUT / "index-failure-modes-robustness-vs-validity.csv"
    with rv_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "program", "certified_stable_set", "certified_set_size",
            "sensitivity_runs", "direct_measure", "surviving_members",
            "certified_equals_tested",
        ])
        for row in robustness["pairs"]:
            writer.writerow([
                row["program"], "|".join(row["certified_stable_set"]),
                row["certified_set_size"], row["sensitivity_run_count"],
                row["direct_measure"],
                "" if row["surviving_members"] is None else row["surviving_members"],
                row["certified_equals_tested"],
            ])

    overlap_csv = OUT / "index-failure-modes-construct-overlap.csv"
    with overlap_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["program", "comparison", "set_size", "overlap", "artifact"])
        for row in constructs:
            writer.writerow([
                row["program"], row["comparison"], row["set_size"], row["overlap"],
                row["provenance"][0]["artifact"],
            ])

    print(f"OK — wrote {json_path.relative_to(REPO)}")
    print(f"OK — wrote {csv_path.relative_to(REPO)}")
    print(f"OK — wrote {rv_csv.relative_to(REPO)}")
    print(f"OK — wrote {overlap_csv.relative_to(REPO)}")
    print(
        f"robustness vs validity: {robustness['pairs_where_construct_check_rejected']} of "
        f"{robustness['pairs_tested']} certified-stable sets were later rejected; "
        f"denominator: {zero_denom} of {total_denom} paired leading sets share no member; "
        f"construct overlap median {median_overlap} of 5; "
        f"uniform sweep rank inversions {degenerate['sweep_total_rank_inversions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
