"use client";

import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string; country: string;
  cpi_inflation_pct: number | null;
  cpi_year: number | null;
  ag_imports_pct_merch: number | null;
  food_production_index: number | null;
  food_price_vulnerability: number | null;
}
interface Payload { rows: Row[]; sources: any; generated_at: string; }

export default function ProgramFoodPrice() {
  const [data, setData] = useState<Payload | null>(null);
  useEffect(() => { fetch("/data/food-price-adb-panel.json").then((r) => r.json()).then(setData); }, []);
  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;
  const ranked = [...data.rows].sort((a, b) => (b.food_price_vulnerability ?? -1) - (a.food_price_vulnerability ?? -1));
  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #9 · food-price-climate-transmission</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Food-price vulnerability macro.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            First-pass macro composite: CPI inflation × ag-import share ×
            food production shortfall. Climate-transmission (CHIRPS
            rainfall anomaly → price pass-through) is NOT yet in this
            version — it needs WFP VAM or FAOSTAT FPMA local price series
            joined to sub-national rainfall.
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
              <th className="text-right">CPI inflation %</th>
              <th className="text-right">Ag imports %</th>
              <th className="text-right">Food prod index</th>
              <th className="text-right">Vulnerability</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => (
              <tr key={r.iso3}>
                <td>{r.iso3}</td>
                <td>{r.country}</td>
                <td className="text-right">{r.cpi_inflation_pct?.toFixed(2) ?? "—"}</td>
                <td className="text-right">{r.ag_imports_pct_merch?.toFixed(2) ?? "—"}</td>
                <td className="text-right">{r.food_production_index?.toFixed(1) ?? "—"}</td>
                <td className="text-right font-semibold">{r.food_price_vulnerability?.toFixed(1) ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveats</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li>CPI inflation is headline, not food-specific. Food-CPI disaggregation by DMC is the next step (available in FAOSTAT FPMA).</li>
          <li>"Ag imports % merchandise" is a proxy for food import-dependence; coastal small islands with tourism-dominant economies read low here but are still import-food-reliant.</li>
          <li>Climate-price transmission is the core program concept and is NOT yet in this version. Requires CHIRPS rainfall anomaly × WFP VAM local food-price series at ADM1/ADM2 + lag analysis.</li>
          <li>2022 CPI inflation spikes (post-shock global food crisis) have largely moderated in 2024 values; the current vulnerability ranking will look different with 2025 updates.</li>
        </ul>
      </section>
    </div>
  );
}
