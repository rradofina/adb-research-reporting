import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string; country: string;
  water_withdrawal_pct_resources: number | null;
  water_withdrawal_year: number | null;
  agri_land_pct: number | null;
  arable_land_pct: number | null;
  cereal_yield_kg_per_ha: number | null;
  rural_population_pct: number | null;
  water_crop_pressure_index: number | null;
}
interface Payload { rows: Row[]; sources: any; methodology: any; generated_at: string; }

export default function ProgramWaterCrop() {
  const [data, setData] = useState<Payload | null>(null);
  useEffect(() => { fetch("/data/water-stress-crop-adb-panel.json").then((r) => r.json()).then(setData); }, []);
  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort((a, b) => (b.water_crop_pressure_index ?? -1) - (a.water_crop_pressure_index ?? -1));

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #17 · water-stress-crop-diversification</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Water stress × crop yield × rural dependence.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            Per-DMC water-crop pressure signal from World Bank WDI.
            Combines freshwater withdrawal (as % of internal resources —
            values over 100% indicate transboundary / external water
            dependence), cereal yield (kg/ha, inverse), and rural
            population share.
          </p>
        </div>
        <div className="shrink-0"><MaturityChip status="H" /></div>
      </div>

      <div className="mt-10 bg-white border border-ink-200 rounded-md overflow-x-auto">
        <table className="data-table tabular w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ISO3</th>
              <th>Country</th>
              <th className="text-right">Water withdrawal % internal</th>
              <th className="text-right">Agri land %</th>
              <th className="text-right">Arable land %</th>
              <th className="text-right">Cereal yield kg/ha</th>
              <th className="text-right">Rural pop %</th>
              <th className="text-right">Pressure index</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => {
              const v = r.water_crop_pressure_index ?? 0;
              const b = v >= 60 ? 5 : v >= 40 ? 4 : v >= 25 ? 3 : v >= 12 ? 2 : v > 0 ? 1 : 0;
              return (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <td className={"text-right " + ((r.water_withdrawal_pct_resources ?? 0) >= 100 ? "text-signal-urgent font-semibold" : "")}>
                    {r.water_withdrawal_pct_resources !== null ? r.water_withdrawal_pct_resources.toFixed(1) + "%" : "—"}
                  </td>
                  <td className="text-right">{r.agri_land_pct !== null ? r.agri_land_pct.toFixed(1) + "%" : "—"}</td>
                  <td className="text-right">{r.arable_land_pct !== null ? r.arable_land_pct.toFixed(1) + "%" : "—"}</td>
                  <td className="text-right">{r.cereal_yield_kg_per_ha !== null ? Math.round(r.cereal_yield_kg_per_ha).toLocaleString() : "—"}</td>
                  <td className="text-right">{r.rural_population_pct !== null ? r.rural_population_pct.toFixed(1) + "%" : "—"}</td>
                  <td className={`text-right font-semibold heat-${b}`}>
                    {r.water_crop_pressure_index !== null ? r.water_crop_pressure_index.toFixed(1) : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveats</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li><strong>Freshwater withdrawal &gt; 100%</strong> (TKM 1,868%, PAK 326%, UZB 263%, AZE 161%) means the country extracts more water than its internal renewable resources, implying reliance on transboundary inflow — a major vulnerability.</li>
          <li>Cereal yield is a proxy for agricultural efficiency/diversification; low yield with high rural share amplifies the pressure signal but does not capture crop-type concentration (a proper Herfindahl on FAOSTAT crop-production shares is the next step).</li>
          <li>WDI vintages differ per indicator; some 2020 values mixed with 2022/2023. Cross-year inconsistency is acceptable for triage but a publication-grade version should align retrieval windows.</li>
          <li>This is not a drought-risk metric. Drought risk requires CHIRPS rainfall anomaly × crop-calendar × storage-capacity analysis, which is in the pipeline, not here.</li>
        </ul>
      </section>
    </div>
  );
}
