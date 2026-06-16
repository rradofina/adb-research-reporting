/**
 * NativeDeepenings.tsx — /deepenings.
 *
 * Renders the marquee deepening recomputes as native charts, each read
 * from the committed artifact a `deepen-*.py` script produced from cached
 * public data. No number is hard-coded here — every value is derived from
 * the fetched JSON, the same files a reviewer downloads on each program's
 * Data tab. These are the "real output + charts" layer over the
 * deep-questions agenda; the full narrative for each lives in the
 * program's `deepened-results.md`.
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ChartFrame, RankedBar, Scatter, type BarDatum, type PointDatum } from "../components/charts";

async function getJSON<T>(url: string): Promise<T | null> {
  try {
    const r = await fetch(url);
    return r.ok ? ((await r.json()) as T) : null;
  } catch {
    return null;
  }
}

const GRID = "/programs/grid-reliability-heat/generated/grid-generation-deepening.json";
const MIG = "/programs/migration-displacement-signals/generated/migration-per-population-deepening.json";
const MPI = "/programs/mpi-nighttime-lights/generated/mpi-dimension-decomposition.json";
const INDEX = "/deepenings-index.json";

export default function NativeDeepenings() {
  const [grid, setGrid] = useState<any>(null);
  const [mig, setMig] = useState<any>(null);
  const [mpi, setMpi] = useState<any>(null);
  const [index, setIndex] = useState<any>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancel = false;
    Promise.all([getJSON<any>(GRID), getJSON<any>(MIG), getJSON<any>(MPI), getJSON<any>(INDEX)]).then(
      ([g, m, p, i]) => {
        if (cancel) return;
        setGrid(g);
        setMig(m);
        setMpi(p);
        setIndex(i);
        setLoaded(true);
      },
    );
    return () => {
      cancel = true;
    };
  }, []);

  // --- Grid: capacity vs generation single-fuel concentration ---
  const gridRows: any[] = grid?.rows_by_generation_herfindahl ?? [];
  const gridCluster = new Set<string>([...(grid?.capacity_top5 ?? []), ...(grid?.generation_top5 ?? [])]);
  const gridPoints: PointDatum[] = gridRows
    .filter((r) => r.herfindahl_capacity != null && r.herfindahl_generation != null)
    .map((r) => ({
      label: r.iso3,
      x: r.herfindahl_capacity,
      y: r.herfindahl_generation,
      highlight: gridCluster.has(r.iso3),
      tip: [
        { k: "On capacity", v: r.herfindahl_capacity.toFixed(2) },
        { k: "On generation", v: r.herfindahl_generation.toFixed(2), accent: true },
        { k: "Top fuel", v: String(r.top_fuel_generation ?? r.top_fuel_capacity ?? "—") },
      ],
    }));
  const gridMoreConc = gridPoints.filter((p) => p.y > p.x).length;

  // --- Migration: absolute stock vs share of population (disjoint top-5s) ---
  const migRows: any[] = mig?.rows_by_share ?? [];
  const byStock = migRows
    .filter((r) => typeof r.emigrant_stock_2024 === "number")
    .sort((a, b) => b.emigrant_stock_2024 - a.emigrant_stock_2024)
    .slice(0, 6);
  const byShare = migRows
    .filter((r) => typeof r.emigrant_pct_of_population === "number")
    .sort((a, b) => b.emigrant_pct_of_population - a.emigrant_pct_of_population)
    .slice(0, 6);
  const absBars: BarDatum[] = byStock.map((r) => ({
    label: r.iso3,
    value: r.emigrant_stock_2024 / 1e6,
    highlight: true,
    tip: [
      { k: "Emigrants", v: `${(r.emigrant_stock_2024 / 1e6).toFixed(1)}M`, accent: true },
      { k: "Of population", v: `${r.emigrant_pct_of_population.toFixed(1)}%` },
      { k: "Rank by share", v: `#${r.rank_share}` },
    ],
  }));
  const shareBars: BarDatum[] = byShare.map((r) => ({
    label: r.iso3,
    value: r.emigrant_pct_of_population,
    highlight: false,
    tip: [
      { k: "Of population", v: `${r.emigrant_pct_of_population.toFixed(1)}%`, accent: true },
      { k: "Emigrants", v: `${(r.emigrant_stock_2024 / 1e3).toFixed(0)}k` },
      { k: "Rank by stock", v: `#${r.rank_absolute}` },
    ],
  }));
  const overlap = (mig?.survivors_in_both_top5 ?? []).length;

  // --- MPI: share of MPI a nighttime-lights signal cannot see ---
  const mpiRows: any[] = mpi?.rows_by_ntl_blind_dimension ?? [];
  const mpiBars: BarDatum[] = [...mpiRows]
    .sort((a, b) => b.ntl_blind_dim_pct - a.ntl_blind_dim_pct)
    .slice(0, 14)
    .map((r) => ({
      label: r.iso3,
      value: r.ntl_blind_dim_pct,
      highlight: r.ntl_blind_dim_pct >= 50,
      tip: [
        { k: "NTL-blind (health+ed)", v: `${r.ntl_blind_dim_pct.toFixed(1)}%`, accent: true },
        { k: "NTL-visible (living)", v: `${r.ntl_visible_dim_pct?.toFixed(1)}%` },
        { k: "MPI value", v: String(r.mpi_value ?? "—") },
      ],
    }));
  const mpiMean = mpi?.mean_ntl_blind_dim_pct;

  return (
    <div style={{ maxWidth: "var(--measure-wide-copy)", margin: "0 auto" }}>
      <header style={{ marginBottom: 24 }}>
        <p className="kicker kicker-crimson">Deepenings · real recomputes</p>
        <h1 className="home-title" style={{ marginTop: 8 }}>
          What the screens look like when you compute the harder number
        </h1>
        <p className="home-lede measure-wide-copy" style={{ marginTop: 12 }}>
          Each chart below is a native render of a real recomputation — every
          value comes from a committed <code className="inline-code-token">deepen-*.py</code>{" "}
          script run over the same public data the headline uses, never
          hand-written. They answer the keystone questions in each program's{" "}
          <Link to="/native-charts" className="token-link">deep-questions</Link>.
          Full per-program narrative is in each <code className="inline-code-token">deepened-results.md</code>;
          the portfolio pattern is in{" "}
          <Link to="/factory" className="token-link">the research docs</Link>.
        </p>
      </header>

      {!loaded && <div className="loading-message">Loading committed deepening artifacts…</div>}

      {loaded && (
        <div style={{ display: "grid", gap: 28 }}>
          {/* ALL-18 SCOREBOARD */}
          {index?.rows && (
            <section>
              <div className="kicker" style={{ marginBottom: 10 }}>
                All {index.counts.total} programs · {index.counts.computed} recomputed from cached public data ·{" "}
                {index.counts.walls} named data wall
              </div>
              <div style={{ display: "grid", gap: 10 }}>
                {index.rows.map((r: any) => (
                  <div
                    key={r.slug}
                    style={{
                      border: "1px solid var(--rule-soft)",
                      borderRadius: 8,
                      padding: "12px 14px",
                      background: "var(--paper)",
                    }}
                  >
                    <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 8, justifyContent: "space-between" }}>
                      <Link
                        to={`/${r.slug}`}
                        style={{ fontFamily: '"JetBrains Mono", monospace', fontWeight: 700, fontSize: 13.5, color: "var(--accent-strong)" }}
                      >
                        {r.slug}
                      </Link>
                      <span className={"chip " + (r.has_artifact ? "chip-sage" : "chip-ochre")}>{r.outcome}</span>
                    </div>
                    {r.finding && (
                      <p style={{ margin: "7px 0 0", fontSize: 13.5, lineHeight: 1.45, color: "var(--ink-soft)" }}>{r.finding}</p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* GRID */}
          {gridPoints.length > 0 && (
            <ChartFrame
              kicker="Grid · capacity vs generation"
              title="What these grids run on is more single-fuel than what they are built with"
              subtitle="Each point is a DMC grid: single-fuel concentration (Herfindahl) measured on installed capacity (x) vs on 2017 generation (y). Almost every point sits above the y = x line — the secondary capacity that makes a grid look diversified is barely dispatched. The headline screen had the right worry and the wrong variable."
              headline={{ value: `${gridMoreConc}/${gridPoints.length}`, label: "grids more concentrated on generation than capacity" }}
              source="WRI Global Power Plant Database v1.3.0 (program cache)"
              program="grid-reliability-heat → grid-generation-deepening.json"
            >
              <Scatter
                data={gridPoints}
                xLabel="Single-fuel concentration on CAPACITY →"
                yLabel="…on GENERATION →"
                diagonal={{ label: "equal" }}
              />
            </ChartFrame>
          )}

          {/* MIGRATION */}
          {absBars.length > 0 && (
            <ChartFrame
              kicker="Migration · stock vs rate"
              title="Rank by emigrant count and you rank population; rank by rate and the list is disjoint"
              subtitle="Left: the headline top economies by absolute emigrant stock (millions) — the most populous economies. Right: the top economies by emigrants as a share of population. There is zero overlap between the two top-5s: the absolute ranking was a population ranking, not a measure of migration intensity."
              headline={{ value: `${overlap}/5`, label: "economies common to both top-5 rankings" }}
              source="UN DESA International Migrant Stock 2024 + WDI population (cache)"
              program="migration-displacement-signals → migration-per-population-deepening.json"
            >
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 20 }}>
                <div>
                  <div className="kicker" style={{ marginBottom: 8 }}>By absolute stock (millions) — the headline</div>
                  <RankedBar data={absBars} unit="M" valueDp={1} />
                </div>
                <div>
                  <div className="kicker" style={{ marginBottom: 8 }}>By share of population (%)</div>
                  <RankedBar data={shareBars} unit="%" valueDp={0} />
                </div>
              </div>
            </ChartFrame>
          )}

          {/* MPI */}
          {mpiBars.length > 0 && (
            <ChartFrame
              kicker="MPI × nighttime lights · dimensional scope"
              title="Nighttime lights are blind to most of multidimensional poverty"
              subtitle="For each ADB economy, the share of its Multidimensional Poverty Index that sits in the health and education dimensions — child mortality, nutrition, schooling, attendance — which a satellite radiance signal cannot observe. Bars above the 50% line are economies where lights would miss the majority of the deprivation. This bounds the eventual NTL × MPI study before it is built."
              headline={mpiMean ? { value: `${mpiMean.toFixed(0)}%`, label: "of MPI is in dimensions nighttime lights cannot see (mean)" } : undefined}
              source="OPHI Global MPI 2024 (committed); NTL join is owner-gated (Earth Engine)"
              program="mpi-nighttime-lights → mpi-dimension-decomposition.json"
              note={
                <>Program 0 is co-authored and owner-led; this scopes the joint study from the committed MPI side only and does not advance it.</>
              }
            >
              <RankedBar data={mpiBars} unit="%" valueDp={0} reference={{ value: 50, label: "half of MPI" }} />
            </ChartFrame>
          )}

          <p style={{ fontSize: 13, color: "var(--ink-faint)", lineHeight: 1.5 }}>
            These three are the marquee cases; all 18 programs carry a{" "}
            <code className="inline-code-token">deepened-results.md</code> with a real recompute
            or a precisely-named data wall (the few keystones that need owner-gated
            data — IMF bilateral flows, DHS microdata, Earth Engine, the Ookla pull).
            Every chart on this page reads a committed artifact; resize the window and
            the type stays crisp.
          </p>
        </div>
      )}
    </div>
  );
}
