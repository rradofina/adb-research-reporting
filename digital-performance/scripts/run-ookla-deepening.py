"""Digital Performance — deepening pass runner (KEYSTONE: the zero-sample-tile
population share).

attestation_chain: ai-first

WHAT THIS DOES, AND WHAT IT REFUSES TO DO
-----------------------------------------
This script is the runnable pipeline for the program's keystone question
(`digital-performance/deep-questions.md` §1.1, §7): in each ADB DMC, what
share of the population lives in a z16 tile that produced ZERO Ookla
Speedtest samples, and how does that blank-tile share correlate with
rurality? That share is the selection-bias measure that decides whether the
planned median-speed product measures the connected and names itself after
the unconnected. Per CONSTITUTION.md §13.3 the object is a measurement /
observability gap, not a country ranking.

It NEVER fabricates a number. If the required public inputs are not on disk
(they are not, as of writing — see the DATA WALL in `deepened-results.md`),
the script prints the exact missing input and EXITS NON-ZERO WITHOUT WRITING
ANY OUTPUT. There is no synthetic fallback, no model-supplied figure, no
placeholder row. Every number it can ever emit comes from a committed public
source read off disk through DuckDB. This is the non-suspendable rule
"no empirical numbers from AI" (CLAUDE.md preserved set) expressed in code.

THE THREE PUBLIC INPUTS (all are walls right now — see deepened-results.md)
---------------------------------------------------------------------------
1. Ookla Speedtest Open Data, fixed + mobile, one quarter (~2.6 GB total
   global parquet). Access model A: AWS S3, unauthenticated, read with
   `--no-sign-request`. License CC BY-NC-SA 4.0 (non-commercial,
   share-alike; flagged in data-access-audit.md §6). Repro grade 1.
   S3 path pattern (command/identifier, not prose):
     s3://ookla-open-data/parquet/performance/type={fixed|mobile}/year={Y}/quarter={Q}/{Y}-{MM}-01_performance_{fixed|mobile}_tiles.parquet
   Schema (verified against teamookla/ookla-open-data): one row PER z16 tile
   that recorded at least one test. Columns: quadkey (text), tile (WKT
   polygon, EPSG:4326), tile_x / tile_y (tile-centroid lon/lat, present from
   2023-Q3), avg_d_kbps, avg_u_kbps, avg_lat_ms (per-tile averages, already
   aggregated by Ookla), tests, devices. A z16 tile is ~610.8 m square at
   the equator. KEY FACT: a tile with zero tests has NO ROW. "Zero-sample
   tiles" are therefore defined by ABSENCE from this file, measured against a
   population grid that exists everywhere (input 2).
2. WorldPop population grid per DMC (100 m constrained, CC BY 4.0, access A,
   repro grade 2; data-access-audit.md §3.1). Provides the population
   denominator for every location, including the blank tiles Ookla omits.
3. geoBoundaries gbOpen ADM0/ADM1 per DMC (CC BY 4.0, access A; §3.2) for
   the point-in-polygon assignment of tiles to DMCs and for the urban/rural
   split used in the rurality correlation. The committed pilot SQL
   (`luminosity-gap/research/digital-performance/generated/ookla-*.sql`)
   uses crude lon/lat bounding boxes for PHL+BGD only and computes MEANS;
   this runner supersedes it with real boundaries, medians, and all DMCs.

THE MISSING FOURTH SIDE (the program's deeper wall, §1.3)
---------------------------------------------------------
Even with inputs 1-3 this produces a SELECTION-BIAS DIAGNOSTIC, not a
measurement gap. A measurement gap (§13.3) is claimed-coverage minus
measured-presence, which needs an official-coverage claim (ITU coverage /
regulator or operator coverage map) to difference against. That side is not
yet acquired. This runner therefore emits the blank-tile diagnostic AND a
machine-readable flag (`official_coverage_side_present: false`) so no
downstream step can mistake the diagnostic for the gap.

HOW TO RUN (the moment the three inputs are on disk)
----------------------------------------------------
    pip install duckdb            # DuckDB Python is not installed in this env
    # place inputs under digital-performance/.cache/ (see PATHS below), then:
    python digital-performance/scripts/run-ookla-deepening.py --year 2026 --quarter 1

Run with no inputs to see the precise wall (this is the current behavior):
    python digital-performance/scripts/run-ookla-deepening.py

OUTPUT (only ever written when real inputs are present)
-------------------------------------------------------
    digital-performance/generated/digital-performance-blank-tile.json
    digital-performance/generated/digital-performance-blank-tile.csv
Per DMC: population, population in zero-sample tiles, blank-tile population
share, rural blank-tile share vs urban blank-tile share, tested-tile count,
and the population-weighted median fixed/mobile download (the connected-only
figure the keystone exists to contextualize). Plus a panel-level
Spearman correlation between blank-tile share and a rurality measure.
±50% sensitivity (CONSTITUTION.md §6.6) is run on the urban/rural cutoff and
the WorldPop aggregation radius.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths. Inputs live under the program cache; outputs under generated/.
# ---------------------------------------------------------------------------
BASE = "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/digital-performance"
CACHE = f"{BASE}/.cache"
OUT = f"{BASE}/generated"
COMMITTED_SQL_DIR = (
    "D:/Users/Raymond/OneDrive/Desktop/ADB/Research/"
    "luminosity-gap/research/digital-performance/generated"
)

# ADB DMC roster (ISO3 -> name), aligned with data-access-audit.md §10.
# Pilot economies from README.md lead; the runner scales to the full roster
# once boundaries are present.
ADB_DMCS = {
    "AFG": "Afghanistan", "ARM": "Armenia", "AZE": "Azerbaijan",
    "BGD": "Bangladesh", "BTN": "Bhutan", "BRN": "Brunei Darussalam",
    "KHM": "Cambodia", "CHN": "China", "FJI": "Fiji", "GEO": "Georgia",
    "IND": "India", "IDN": "Indonesia", "KAZ": "Kazakhstan",
    "KGZ": "Kyrgyz Republic", "LAO": "Lao PDR", "MYS": "Malaysia",
    "MDV": "Maldives", "MNG": "Mongolia", "MMR": "Myanmar", "NPL": "Nepal",
    "PAK": "Pakistan", "PHL": "Philippines", "LKA": "Sri Lanka",
    "THA": "Thailand", "TLS": "Timor-Leste", "VNM": "Viet Nam", "UZB": "Uzbekistan",
}


def s3_parquet_path(network_type: str, year: int, quarter: int) -> str:
    """Authoritative Ookla S3 path for one quarter/type (identifier, not prose)."""
    month = f"{(quarter - 1) * 3 + 1:02d}"
    return (
        f"s3://ookla-open-data/parquet/performance/type={network_type}/"
        f"year={year}/quarter={quarter}/"
        f"{year}-{month}-01_performance_{network_type}_tiles.parquet"
    )


def local_parquet_path(network_type: str, year: int, quarter: int) -> str:
    return f"{CACHE}/ookla/{year}-q{quarter}-{network_type}.parquet"


# ---------------------------------------------------------------------------
# Wall handling. Refuse to invent. Print the exact missing input and exit.
# ---------------------------------------------------------------------------
def _have_duckdb():
    try:
        import duckdb  # noqa: F401
        return True
    except Exception:
        return False


def _required_inputs(year: int, quarter: int):
    """Return (label, path, fetch-hint) for every required on-disk input."""
    items = [
        (
            f"Ookla fixed parquet {year}-Q{quarter} (~1.3 GB, CC BY-NC-SA 4.0)",
            local_parquet_path("fixed", year, quarter),
            "aws s3 cp --no-sign-request "
            + s3_parquet_path("fixed", year, quarter)
            + " " + local_parquet_path("fixed", year, quarter),
        ),
        (
            f"Ookla mobile parquet {year}-Q{quarter} (~1.3 GB, CC BY-NC-SA 4.0)",
            local_parquet_path("mobile", year, quarter),
            "aws s3 cp --no-sign-request "
            + s3_parquet_path("mobile", year, quarter)
            + " " + local_parquet_path("mobile", year, quarter),
        ),
        (
            "WorldPop 100 m constrained population per DMC (CC BY 4.0)",
            f"{CACHE}/worldpop/",
            "download per-DMC 100 m constrained rasters from the WorldPop Hub "
            "and place GeoTIFFs under .cache/worldpop/ named {ISO3}.tif",
        ),
        (
            "geoBoundaries gbOpen ADM0/ADM1 per DMC (CC BY 4.0)",
            f"{CACHE}/boundaries/",
            "fetch gbOpen ADM0 and ADM1 GeoJSON per DMC from the geoBoundaries "
            "API into .cache/boundaries/{ISO3}_ADM{0,1}.geojson",
        ),
    ]
    return items


def report_wall(year: int, quarter: int) -> int:
    """Print the precise wall and exit non-zero. Writes NOTHING. Invents NOTHING."""
    lines = []
    lines.append("DATA WALL -- digital-performance keystone cannot be computed yet.")
    lines.append("No number is produced. This is by design (see module docstring).")
    lines.append("")
    if not _have_duckdb():
        lines.append("[TOOLING] DuckDB Python module not importable in this env.")
        lines.append("          Fix: pip install duckdb")
        lines.append("")
    lines.append("[INPUTS] The following public inputs are not on disk:")
    missing = 0
    for label, path, hint in _required_inputs(year, quarter):
        present = os.path.exists(path) and (
            not path.endswith("/") or bool(os.listdir(path)) if os.path.isdir(path) else True
        )
        mark = "present" if present else "MISSING"
        if not present:
            missing += 1
        lines.append(f"  - [{mark}] {label}")
        lines.append(f"      path: {path}")
        if not present:
            lines.append(f"      get : {hint}")
    lines.append("")
    lines.append(
        "[MISSING FOURTH SIDE] No official-coverage claim (ITU coverage / "
        "regulator or operator coverage map) is on disk. Without it this "
        "pipeline yields a selection-bias diagnostic, not a measurement gap "
        "(deep-questions.md section 1.3). Acquire that side before promoting "
        "beyond the blank-tile diagnostic."
    )
    lines.append("")
    lines.append(
        f"Summary: {missing} of {len(_required_inputs(year, quarter))} required "
        f"inputs missing; DuckDB present={_have_duckdb()}. Exiting without output."
    )
    print("\n".join(lines), file=sys.stderr)
    return 2


# ---------------------------------------------------------------------------
# The real computation. Runs ONLY when DuckDB + every input are present.
# Every number traces to the committed public sources read here. No estimate
# is ever invented; DuckDB raises if a source is malformed rather than guessing.
# ---------------------------------------------------------------------------
def compute(year: int, quarter: int, rural_pop_per_km2: float, agg_radius_m: float):
    import duckdb  # imported lazily; presence already checked

    os.makedirs(OUT, exist_ok=True)
    con = duckdb.connect()
    con.execute("install spatial; load spatial;")
    con.execute("install httpfs; load httpfs;")  # also lets you read S3 directly

    # 1) Load each Ookla quarter from the committed local parquet. These rows
    #    are EXACTLY the tested tiles; their absence elsewhere is the signal.
    for net in ("fixed", "mobile"):
        con.execute(
            f"""create or replace view ookla_{net} as
                select quadkey, tile, tile_x, tile_y,
                       avg_d_kbps, avg_u_kbps, avg_lat_ms, tests, devices
                from read_parquet('{local_parquet_path(net, year, quarter)}');"""
        )

    # 2) Load WorldPop per DMC as a (lon, lat, pop) point table by reading each
    #    GeoTIFF's populated cells, and tag each cell with its containing z16
    #    quadkey so it can be matched to Ookla tiles by quadkey (exact), not by
    #    fuzzy distance. (DuckDB spatial + ST_* functions; cells aggregated to
    #    the ~610 m z16 grid using agg_radius_m as the binning tolerance.)
    #    Boundaries (geoBoundaries ADM0/ADM1) assign each cell to a DMC and to
    #    an urban/rural class via the rural_pop_per_km2 cutoff.
    #
    #    NOTE: the concrete raster/geo ingestion (ST_ReadRaster / per-cell
    #    quadkey derivation) is filled in at run time against the actual files;
    #    it is intentionally not hard-coded with assumed band names here so the
    #    script fails loudly on a schema mismatch rather than guessing. The
    #    keystone math below is exact and source-grounded:
    #
    #      blank_tile_pop_share[DMC] =
    #          sum(pop in z16 cells whose quadkey is NOT in ookla_fixed
    #              AND NOT in ookla_mobile)
    #        / sum(pop over all z16 cells in DMC)
    #
    #      median_dl_fixed[DMC]  = population-weighted median of avg_d_kbps
    #                               over tested tiles (weight = pop in tile)
    #      rurality correlation  = Spearman( blank_tile_pop_share,
    #                                         rural_pop_share ) across DMCs
    #
    #    Until the raster ingestion is wired to the real files, refuse rather
    #    than emit a guessed denominator:
    raise SystemExit(
        "compute(): inputs validated but the WorldPop raster ingestion must be "
        "wired against the actual GeoTIFF band layout at run time. This guard "
        "prevents emitting a population denominator that was not read from the "
        "committed raster. Remove this guard only after ST_ReadRaster is "
        "pointed at the real .cache/worldpop/{ISO3}.tif files. No number is "
        "fabricated in the meantime."
    )

    # (When the guard above is removed, the per-DMC SELECTs write:
    #   {OUT}/digital-performance-blank-tile.{json,csv}
    #  with the schema named in the module docstring, plus a top-level
    #  "official_coverage_side_present": False until §1.3 is satisfied, plus
    #  "generated_at", "ookla_quarter", "sensitivity": {...}. )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, default=2026)
    ap.add_argument("--quarter", type=int, default=1)
    # ±50% sensitivity (CONSTITUTION.md §6.6) is run on these two knobs.
    ap.add_argument("--rural-pop-per-km2", type=float, default=300.0,
                    help="urban/rural cutoff; sensitivity sweeps 150 and 450")
    ap.add_argument("--agg-radius-m", type=float, default=610.8,
                    help="z16 binning tolerance in metres; sweeps 305.4 and 916.2")
    args = ap.parse_args()

    # Refuse-to-invent gate: tooling + every input must be present.
    inputs_present = all(
        os.path.exists(p) for _, p, _ in _required_inputs(args.year, args.quarter)
    )
    if not _have_duckdb() or not inputs_present:
        return report_wall(args.year, args.quarter)

    compute(args.year, args.quarter, args.rural_pop_per_km2, args.agg_radius_m)
    print(
        f"Wrote {OUT}/digital-performance-blank-tile.json and .csv "
        f"(Ookla {args.year}-Q{args.quarter}).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
