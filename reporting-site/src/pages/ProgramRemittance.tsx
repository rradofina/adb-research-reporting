import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string;
  country: string;
  wdi_remittance_pct_gdp: number | null;
  wdi_year: number | null;
  rpw_period: string | null;
  rpw_corridors_observed: number;
  rpw_firms_observed: number | null;
  rpw_mean_cost_pct: number | null;
  rpw_median_cost_pct: number | null;
  rpw_min_cost_pct: number | null;
  rpw_max_cost_pct: number | null;
  fragility_index: number | null;
}

interface Corridor {
  source_iso3: string; source: string;
  dest_iso3: string; dest: string;
  n_quotes: number;
  mean_cost_pct: number;
  median_cost_pct: number;
  min_cost_pct: number;
  max_cost_pct: number;
}

interface Payload {
  generated_at: string;
  sources: any;
  rows: Row[];
  expensive_corridors_top50: Corridor[];
  totals: { dmcs_with_wdi: number; dmcs_with_rpw: number; dmcs_with_both: number };
}

export default function ProgramRemittance() {
  const [data, setData] = useState<Payload | null>(null);
  const [view, setView] = useState<"fragility" | "dependence" | "cost">("fragility");

  useEffect(() => {
    fetch("/data/remittance-resilience-adb-panel.json")
      .then((r) => r.json())
      .then(setData);
  }, []);

  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const sortKey: Record<typeof view, keyof Row> = {
    fragility: "fragility_index",
    dependence: "wdi_remittance_pct_gdp",
    cost: "rpw_mean_cost_pct",
  };

  const ranked = [...data.rows].sort((a, b) => {
    const av = (a[sortKey[view]] as number | null) ?? -1;
    const bv = (b[sortKey[view]] as number | null) ?? -1;
    return bv - av;
  });

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Program #14 · remittance-resilience
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Where remittance flows are both important and expensive.
          </h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            For each ADB DMC, combines{" "}
            <strong>macro-level dependence</strong> (WDI personal
            remittances received as % GDP, latest year) with{" "}
            <strong>inbound transfer cost</strong> (mean across corridors
            in the latest Q1 2025 RPW period). The fragility index is{" "}
            <code className="font-mono text-sm">min(dep/25, 1) × min(cost/15, 1) × 100</code>
            — triage only.
          </p>
        </div>
        <div className="shrink-0">
          <MaturityChip status="PR" />
          <p className="mt-2 text-xs text-signal-warn max-w-[18ch] text-right">
            Flagship paper; AI-first, human-final upgrade pending.
          </p>
        </div>
      </div>

      <section className="mt-10 grid md:grid-cols-3 gap-4">
        <Stat label="DMCs with WDI dependence" value={data.totals.dmcs_with_wdi} note="of 44 ADB regional DMCs" />
        <Stat label="DMCs with RPW cost" value={data.totals.dmcs_with_rpw} note="latest period 2025_1Q" />
        <Stat label="DMCs with both" value={data.totals.dmcs_with_both} note="basis for fragility ranking" />
      </section>

      <section className="mt-10">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-xs uppercase tracking-wider text-ink-500">Sort by</span>
          {(["fragility", "dependence", "cost"] as const).map((v) => (
            <button
              key={v}
              onClick={() => setView(v)}
              className={
                "px-3 py-1 rounded border text-sm transition " +
                (view === v
                  ? "bg-ink-900 text-ink-50 border-ink-900"
                  : "bg-white text-ink-700 border-ink-200 hover:border-ink-500")
              }
            >
              {v}
            </button>
          ))}
          <span className="ml-auto text-xs text-ink-500">
            Sources: <strong>RPW Q1 2025</strong> + <strong>WDI BX.TRF.PWKR.DT.GD.ZS</strong>
          </span>
        </div>

        <div className="mt-6 bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>ISO3</th>
                <th>Country</th>
                <th className="text-right">Remittance %GDP</th>
                <th className="text-right">WDI year</th>
                <th className="text-right">Corridors observed</th>
                <th className="text-right">Mean cost %</th>
                <th className="text-right">Median cost %</th>
                <th className="text-right">Range</th>
                <th className="text-right">Fragility</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((r) => {
                const bucket = fragBucket(r.fragility_index);
                return (
                  <tr key={r.iso3}>
                    <td>{r.iso3}</td>
                    <td>{r.country}</td>
                    <td className="text-right">
                      {r.wdi_remittance_pct_gdp !== null
                        ? r.wdi_remittance_pct_gdp.toFixed(2)
                        : "—"}
                    </td>
                    <td className="text-right">{r.wdi_year ?? "—"}</td>
                    <td className="text-right">{r.rpw_corridors_observed}</td>
                    <td className="text-right">
                      {r.rpw_mean_cost_pct !== null
                        ? r.rpw_mean_cost_pct.toFixed(2)
                        : "—"}
                    </td>
                    <td className="text-right">
                      {r.rpw_median_cost_pct !== null
                        ? r.rpw_median_cost_pct.toFixed(2)
                        : "—"}
                    </td>
                    <td className="text-right text-xs text-ink-500">
                      {r.rpw_min_cost_pct !== null
                        ? `${r.rpw_min_cost_pct.toFixed(1)}–${r.rpw_max_cost_pct?.toFixed(1)}`
                        : "—"}
                    </td>
                    <td className={`text-right font-semibold heat-${bucket}`}>
                      {r.fragility_index !== null ? r.fragility_index.toFixed(1) : "—"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-12">
        <h2 className="text-lg font-semibold">
          Top 30 most-expensive corridors (Q1 2025, ADB-DMC destination)
        </h2>
        <p className="mt-2 text-sm text-ink-500">
          Mean across all observed firm × payment-instrument × access-point
          combinations for that source → destination pair in the period.
        </p>
        <div className="mt-4 bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>Source</th>
                <th>Destination</th>
                <th className="text-right">N quotes</th>
                <th className="text-right">Mean cost %</th>
                <th className="text-right">Median %</th>
                <th className="text-right">Min</th>
                <th className="text-right">Max</th>
              </tr>
            </thead>
            <tbody>
              {data.expensive_corridors_top50.slice(0, 30).map((c, i) => (
                <tr key={i}>
                  <td>
                    <span className="text-xs text-ink-500">{c.source_iso3}</span>{" "}
                    {c.source}
                  </td>
                  <td>
                    <span className="text-xs text-ink-500">{c.dest_iso3}</span>{" "}
                    {c.dest}
                  </td>
                  <td className="text-right">{c.n_quotes}</td>
                  <td className="text-right font-semibold">
                    {c.mean_cost_pct.toFixed(2)}
                  </td>
                  <td className="text-right">{c.median_cost_pct.toFixed(2)}</td>
                  <td className="text-right text-xs text-ink-500">
                    {c.min_cost_pct.toFixed(1)}
                  </td>
                  <td className="text-right text-xs text-ink-500">
                    {c.max_cost_pct.toFixed(1)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-12 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveats</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li>
            RPW only monitors selected corridors. Intra-regional corridors
            (e.g., Thailand → Lao PDR) are under-sampled.
          </li>
          <li>
            Mean cost across observed corridors is biased toward the
            corridors that are <em>actually monitored</em>; thin-sample
            Pacific destinations read with high variance.
          </li>
          <li>
            % GDP measures macro reliance but misses household-level
            concentration. One district may carry most flows; invisible
            here.
          </li>
          <li>
            Fragility = dependence × cost is multiplicative. Zero
            dependence yields zero fragility — but that does not mean
            "resilient." It only means this channel is small.
          </li>
        </ul>
      </section>
    </div>
  );
}

function Stat({ label, value, note }: { label: string; value: number; note?: string }) {
  return (
    <div className="bg-white border border-ink-200 rounded-md p-5">
      <div className="text-xs uppercase tracking-wider text-ink-500">{label}</div>
      <div className="mt-2 text-3xl font-semibold tabular">{value}</div>
      {note && <div className="mt-1 text-xs text-ink-500">{note}</div>}
    </div>
  );
}

function fragBucket(v: number | null) {
  if (v === null) return 0;
  if (v >= 50) return 5;
  if (v >= 30) return 4;
  if (v >= 15) return 3;
  if (v >= 5) return 2;
  return 1;
}
