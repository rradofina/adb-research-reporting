"use client";

import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Corridor { origin_iso3?: string | null; origin_name?: string; dest_iso3?: string | null; dest_name?: string; stock: number; }
interface Row {
  iso3: string;
  country: string;
  immigrant_stock_2024: number;
  emigrant_stock_2024: number;
  net_migrant_stock_2024: number;
  top_origins: Corridor[];
  top_destinations: Corridor[];
}
interface Payload { rows: Row[]; sources: any; generated_at: string; }

export default function ProgramMigration() {
  const [data, setData] = useState<Payload | null>(null);
  const [sort, setSort] = useState<"emigrants" | "immigrants" | "net">("emigrants");

  useEffect(() => {
    fetch("/data/migration-displacement-adb-panel.json").then((r) => r.json()).then(setData);
  }, []);

  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const key: Record<typeof sort, keyof Row> = {
    emigrants: "emigrant_stock_2024",
    immigrants: "immigrant_stock_2024",
    net: "net_migrant_stock_2024",
  };
  const ranked = [...data.rows].sort((a, b) => (b[key[sort]] as number) - (a[key[sort]] as number));

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #11 · migration-displacement-signals</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Legacy stock table — choose the denominator before interpreting rank.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            This retained diagnostic exposes the UN DESA 2024 bilateral stock
            rows behind the research page. Absolute stock measures diaspora
            scale, not current migration intensity. The current paper adds the
            WDI resident-population denominator and a UNHCR forced-displacement
            crosswalk before interpreting any leading set.
          </p>
        </div>
        <div className="shrink-0"><MaturityChip status="PP" /></div>
      </div>

      <section className="mt-10 flex items-center gap-3 flex-wrap">
        <span className="text-xs uppercase tracking-wider text-ink-500">Sort</span>
        {(["emigrants", "immigrants", "net"] as const).map((v) => (
          <button key={v} onClick={() => setSort(v)} className={"px-3 py-1 rounded border text-sm " + (sort === v ? "bg-ink-900 text-ink-50 border-ink-900" : "bg-white text-ink-700 border-ink-200 hover:border-ink-500")}>{v}</button>
        ))}
      </section>

      <div className="mt-6 bg-white border border-ink-200 rounded-md overflow-x-auto">
        <table className="data-table tabular w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ISO3</th>
              <th>Country</th>
              <th className="text-right">Immigrants</th>
              <th className="text-right">Emigrants</th>
              <th className="text-right">Net</th>
              <th>Top destinations (out)</th>
              <th>Top origins (in)</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => (
              <tr key={r.iso3}>
                <td>{r.iso3}</td>
                <td>{r.country}</td>
                <td className="text-right">{r.immigrant_stock_2024.toLocaleString()}</td>
                <td className="text-right">{r.emigrant_stock_2024.toLocaleString()}</td>
                <td className={"text-right " + (r.net_migrant_stock_2024 < 0 ? "text-signal-urgent" : "text-signal-ok")}>
                  {r.net_migrant_stock_2024.toLocaleString()}
                </td>
                <td className="text-xs">
                  {r.top_destinations.slice(0, 3).map((c, i) => (
                    <span key={i} className="mr-2 text-ink-700">
                      {c.dest_name} <span className="text-ink-500">({c.stock.toLocaleString()})</span>
                    </span>
                  ))}
                </td>
                <td className="text-xs">
                  {r.top_origins.slice(0, 3).map((c, i) => (
                    <span key={i} className="mr-2 text-ink-700">
                      {c.origin_name} <span className="text-ink-500">({c.stock.toLocaleString()})</span>
                    </span>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveats</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li>Stock is a point-in-time snapshot, not a flow. It does not distinguish recent arrivals from long-term residents.</li>
          <li>Numbers include both economic migrants and refugees where the host country's census classification does not disaggregate.</li>
          <li>"Net" = immigrants − emigrants. Positive = net destination; negative = net origin.</li>
          <li>Corridors exclude regional aggregates; only country-to-country rows are summed. Minor rollup differences vs. UN headline totals expected.</li>
          <li>The current research result is the denominator switch, not this table's absolute ordering.</li>
        </ul>
      </section>
    </div>
  );
}
