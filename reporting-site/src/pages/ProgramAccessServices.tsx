import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  country_name: string;
  iso3: string;
  admin1_code: string;
  admin1_name: string;
  population: number;
  health_facilities: number;
  schools: number;
  markets: number;
  total_services: number;
  total_mapped_services_per_million: number | string;
  service_load_score: number | string;
  osm_completeness_risk_score: number | string;
  access_stress_index: number | string;
  bottleneck: string;
  service_query_mode: string;
  osm_timestamp: string;
}

export default function ProgramAccessServices() {
  const [rows, setRows] = useState<Row[]>([]);
  const [country, setCountry] = useState<string>("ALL");

  useEffect(() => {
    fetch("/data/access-services-computed-admin1.json")
      .then((r) => r.json())
      .then((d) => setRows(Array.isArray(d) ? d : (d.rows || d.data || [])));
  }, []);

  const filtered =
    country === "ALL" ? rows : rows.filter((r) => r.iso3 === country);
  const iso3s = Array.from(new Set(rows.map((r) => r.iso3))).sort();

  const ranked = [...filtered].sort(
    (a, b) => Number(b.access_stress_index) - Number(a.access_stress_index),
  );

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Program #1 · access-services
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Climate-adjusted access to services — ADM1 screening
          </h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            National and ADM1 screening index for 104 units across 8 ADB
            DMCs. Built from World Bank WDI, CCKP, geoBoundaries, WorldPop
            stats, PSA OpenSTAT, and OSM/Overpass. Not yet a travel-time
            raster model — this is the triage layer that decides where the
            heavier raster work is worth running.
          </p>
        </div>
        <div className="shrink-0">
          <MaturityChip status="SR" />
        </div>
      </div>

      <section className="mt-10">
        <div className="flex items-center gap-3">
          <span className="text-xs uppercase tracking-wider text-ink-500">Filter country</span>
          <select
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className="border border-ink-200 rounded px-2 py-1 text-sm bg-white"
          >
            <option value="ALL">All ({rows.length} rows)</option>
            {iso3s.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <span className="text-xs text-ink-500 ml-auto tabular">
            Showing {filtered.length} ADM1 units — ranked by access-stress index (highest first).
          </span>
        </div>

        <div className="mt-6 bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>Country</th>
                <th>ADM1</th>
                <th>Region</th>
                <th className="text-right">Population 2020</th>
                <th className="text-right">OSM health</th>
                <th className="text-right">OSM schools</th>
                <th className="text-right">OSM markets</th>
                <th className="text-right">Stress index</th>
                <th>Bottleneck</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((r) => {
                const stress = Number(r.access_stress_index);
                const bucket = stressBucket(stress);
                return (
                  <tr key={r.iso3 + r.admin1_code}>
                    <td>{r.country_name}</td>
                    <td>{r.admin1_code}</td>
                    <td>{r.admin1_name}</td>
                    <td className="text-right">{r.population?.toLocaleString()}</td>
                    <td className="text-right">{r.health_facilities?.toLocaleString()}</td>
                    <td className="text-right">{r.schools?.toLocaleString()}</td>
                    <td className="text-right">{r.markets?.toLocaleString()}</td>
                    <td className={`text-right font-semibold heat-${bucket}`}>
                      {stress}
                    </td>
                    <td>{r.bottleneck}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveat</h2>
        <p className="mt-2 text-ink-700">
          The access-stress index caps at 100; for headline stress regions
          (e.g., Balochistan, Pakistan; Azad Kashmir; Sylhet) rank information
          is lost at the top. Use the stress index as triage; the published
          pipeline's next step is grid-level travel time with road network,
          flood/water penalties, and facility catchments, at which point
          the triage rank will be superseded by a measured travel-time
          access metric.
        </p>
      </section>
    </div>
  );
}

function stressBucket(v: number) {
  if (!Number.isFinite(v)) return 0;
  if (v >= 90) return 5;
  if (v >= 70) return 4;
  if (v >= 50) return 3;
  if (v >= 30) return 2;
  return 1;
}
