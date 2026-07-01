"use client";

import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string; country: string;
  lpi_overall: number | null; lpi_overall_year: number | null;
  lpi_infrastructure: number | null; lpi_customs: number | null;
  imports_usd: number | null; imports_usd_year: number | null;
  friction_exposure_index: number | null;
}
interface Payload { rows: Row[]; sources: any; methodology: any; generated_at: string; }

export default function ProgramPortFriction() {
  const [data, setData] = useState<Payload | null>(null);

  useEffect(() => { fetch("/data/port-hinterland-friction-adb-panel.json").then((r) => r.json()).then(setData); }, []);
  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort((a, b) => (b.friction_exposure_index ?? -1) - (a.friction_exposure_index ?? -1));

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #12 · port-hinterland-friction</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Logistics deficit × trade dependence.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            Friction-exposure index combines World Bank LPI (Logistics
            Performance Index, 1–5 scale, higher = better) with WDI
            imports in USD (trade-dependence proxy). Flags where low
            logistics performance meets high trade reliance.
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
              <th className="text-right">LPI overall</th>
              <th className="text-right">LPI infra</th>
              <th className="text-right">LPI customs</th>
              <th className="text-right">Imports USD</th>
              <th className="text-right">Friction</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => {
              const b = r.friction_exposure_index === null ? 0 : r.friction_exposure_index >= 1 ? 5 : r.friction_exposure_index >= 0.7 ? 4 : r.friction_exposure_index >= 0.4 ? 3 : r.friction_exposure_index >= 0.2 ? 2 : 1;
              return (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <td className="text-right">{r.lpi_overall?.toFixed(2) ?? "—"}</td>
                  <td className="text-right">{r.lpi_infrastructure?.toFixed(2) ?? "—"}</td>
                  <td className="text-right">{r.lpi_customs?.toFixed(2) ?? "—"}</td>
                  <td className="text-right">{r.imports_usd !== null ? "$" + (r.imports_usd / 1e9).toFixed(1) + "B" : "—"}</td>
                  <td className={`text-right font-semibold heat-${b}`}>
                    {r.friction_exposure_index !== null ? r.friction_exposure_index.toFixed(2) : "—"}
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
          <li>LPI is survey-based (freight forwarders' perceptions). It measures logistics friction on aggregate, not the actual port-to-hinterland inland corridor that the program's full scope targets.</li>
          <li>Imports-in-USD is a crude trade-dependence proxy; imports ÷ GDP would be better. Pending pipeline.</li>
          <li>Landlocked DMCs (AFG, UZB, KGZ, TJK, LAO, MNG) have port-hinterland friction structurally different from coastal DMCs. Treat as two separate stories when reading the table.</li>
          <li>The full scope of Program 12 — inland transport-cost curves from ports to ADM1 origin/destination points — needs road-network data + customs clearance times per corridor, which this layer does not have.</li>
        </ul>
      </section>
    </div>
  );
}
