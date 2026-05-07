import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string;
  country: string;
  plant_count: number;
  total_capacity_mw: number;
  top_fuel: string | null;
  top_fuel_share: number | null;
  fuel_herfindahl: number | null;
  wdi_elec_access_pct: number | null;
  wdi_elec_access_year: number | null;
  wdi_energy_use_kgoe_per_capita: number | null;
  fuel_mix_capacity_mw: Record<string, number>;
}

interface Payload {
  generated_at: string;
  rows: Row[];
  global_fuel_distribution_in_adb_plants: Record<string, number>;
  sources: any;
}

const FUEL_COLORS: Record<string, string> = {
  Hydro: "#3a7d8a",
  Coal: "#3d3a36",
  Gas: "#c37721",
  Oil: "#7a4a2e",
  Solar: "#e0a93f",
  Wind: "#6f9d6e",
  Biomass: "#7d6b4a",
  Nuclear: "#9a4f7e",
  Geothermal: "#b8322d",
  Waste: "#7a7a7a",
  Unknown: "#bbbbbb",
};

export default function ProgramGrid() {
  const [data, setData] = useState<Payload | null>(null);

  useEffect(() => {
    fetch("/data/grid-reliability-heat-adb-panel.json")
      .then((r) => r.json())
      .then(setData);
  }, []);

  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort(
    (a, b) => (b.fuel_herfindahl ?? 0) - (a.fuel_herfindahl ?? 0),
  );

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Program #10 · grid-reliability-heat
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Where the grid is one fuel away from a problem.
          </h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            Structural-exposure layer. Combines plant-level capacity from
            the WRI Global Power Plant Database v1.3.0 (frozen 2022) with
            World Bank WDI electricity-access and energy-use indicators
            for the 39 ADB regional DMCs with WRI coverage. Fuel-mix
            concentration (Herfindahl-style) flags single-fuel grids that
            are exposed to a single-shock pathway.
          </p>
        </div>
        <div className="shrink-0">
          <MaturityChip status="H" />
        </div>
      </div>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-5">
        <div className="text-xs uppercase tracking-wider text-ink-500">
          Plants in WRI database, ADB DMCs total
        </div>
        <div className="mt-2 flex items-end gap-4">
          <div className="text-3xl font-semibold tabular">
            {data.rows.reduce((s, r) => s + r.plant_count, 0).toLocaleString()}
          </div>
          <div className="text-sm text-ink-500 mb-1">
            {Math.round(
              data.rows.reduce((s, r) => s + r.total_capacity_mw, 0),
            ).toLocaleString()}{" "}
            MW total installed capacity
          </div>
        </div>
        <div className="mt-5">
          <div className="text-xs uppercase tracking-wider text-ink-500 mb-2">
            Fuel mix — count of plants
          </div>
          <FuelBar dist={data.global_fuel_distribution_in_adb_plants} />
        </div>
      </section>

      <section className="mt-10">
        <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
          Fuel-mix concentration ranked
        </h2>
        <p className="mt-2 text-sm text-ink-700 max-w-3xl">
          Herfindahl close to 1 = single-fuel grid. Top of the table
          carries the most concentrated risk: a single shock to that fuel
          (drought for Hydro-dominant; coal-supply or carbon-policy for
          Coal-dominant; gas-supply or geopolitical for Gas-dominant)
          moves a large share of the country's generation at once.
        </p>
        <div className="mt-6 bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>ISO3</th>
                <th>Country</th>
                <th className="text-right">Plants</th>
                <th className="text-right">Capacity MW</th>
                <th>Top fuel</th>
                <th className="text-right">Top share</th>
                <th className="text-right">Herfindahl</th>
                <th>Fuel mix</th>
                <th className="text-right">Elec access %</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((r) => {
                const bucket = herfBucket(r.fuel_herfindahl);
                return (
                  <tr key={r.iso3}>
                    <td>{r.iso3}</td>
                    <td>{r.country}</td>
                    <td className="text-right">
                      {r.plant_count.toLocaleString()}
                    </td>
                    <td className="text-right">
                      {r.total_capacity_mw.toLocaleString()}
                    </td>
                    <td>
                      {r.top_fuel && (
                        <span
                          className="inline-block w-3 h-3 rounded-sm mr-2 align-middle"
                          style={{
                            background: FUEL_COLORS[r.top_fuel] ?? "#bbb",
                          }}
                        />
                      )}
                      {r.top_fuel ?? "—"}
                    </td>
                    <td className="text-right">
                      {r.top_fuel_share !== null
                        ? (r.top_fuel_share * 100).toFixed(1) + "%"
                        : "—"}
                    </td>
                    <td className={`text-right font-semibold heat-${bucket}`}>
                      {r.fuel_herfindahl ?? "—"}
                    </td>
                    <td className="min-w-[200px]">
                      <FuelBar dist={r.fuel_mix_capacity_mw} />
                    </td>
                    <td className="text-right">
                      {r.wdi_elec_access_pct !== null
                        ? r.wdi_elec_access_pct.toFixed(1) + "%"
                        : "—"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-12 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveats</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li>
            <strong>WRI Global Power Plant DB is frozen at v1.3.0 since 2022.</strong> New plants
            (e.g., 2022–2025 solar buildouts) are missing. The fuel-mix
            here may overstate fossil shares for DMCs with rapid recent
            renewable additions.
          </li>
          <li>
            Many small Pacific DMCs are not in the WRI dataset (off-grid /
            diesel-genset, not centralized plants). Pacific island
            "fragility" requires a separate diesel-import + outage analysis.
          </li>
          <li>
            This is an exposure layer, not a reliability metric. Frequency
            and duration of outages — the actual reliability variable —
            require ERA5-Land × outage-event data, which the program
            scaffold reserves for the next pipeline.
          </li>
          <li>
            Hydro dominance has a different shock signature than coal
            dominance. Treat the Herfindahl rank as a flag for "look here
            next," not a unified risk score.
          </li>
        </ul>
      </section>
    </div>
  );
}

function FuelBar({ dist }: { dist: Record<string, number> }) {
  const total = Object.values(dist).reduce((s, n) => s + n, 0);
  if (total === 0) return <div className="text-xs text-ink-500">no data</div>;
  return (
    <div className="flex h-3 w-full overflow-hidden rounded">
      {Object.entries(dist).map(([fuel, n]) => (
        <div
          key={fuel}
          title={`${fuel}: ${n} ${typeof n === "number" && Number.isFinite(n) ? "" : ""}(${((n / total) * 100).toFixed(1)}%)`}
          style={{
            width: `${(n / total) * 100}%`,
            background: FUEL_COLORS[fuel] ?? "#bbb",
          }}
        />
      ))}
    </div>
  );
}

function herfBucket(v: number | null) {
  if (v === null) return 0;
  if (v >= 0.85) return 5;
  if (v >= 0.65) return 4;
  if (v >= 0.45) return 3;
  if (v >= 0.30) return 2;
  return 1;
}
