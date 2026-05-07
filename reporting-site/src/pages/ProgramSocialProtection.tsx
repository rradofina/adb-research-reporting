import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string; country: string;
  sp_coverage_pct: number | null; sp_coverage_year: number | null;
  findex_account_pct: number | null; findex_year: number | null;
  poverty_headcount_215_pct: number | null; poverty_year: number | null;
  poverty_gap_pct: number | null;
  shock_payment_readiness_gap: number | null;
}
interface Payload { rows: Row[]; sources: any; generated_at: string; }

export default function ProgramSocialProtection() {
  const [data, setData] = useState<Payload | null>(null);
  useEffect(() => { fetch("/data/social-protection-adb-panel.json").then((r) => r.json()).then(setData); }, []);
  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort((a, b) => (b.shock_payment_readiness_gap ?? -1) - (a.shock_payment_readiness_gap ?? -1));

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #16 · social-protection-shock-coverage</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Shock-payment readiness gap.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            When a shock hits, does the state have a way to reach
            low-income households quickly? Combines ASPIRE
            social-protection coverage, Findex account ownership, and
            poverty headcount. Readiness gap = (poverty) × (1 - mean of
            SP coverage & account ownership).
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
              <th className="text-right">Poverty % ($2.15/day)</th>
              <th className="text-right">SP coverage %</th>
              <th className="text-right">Findex account %</th>
              <th className="text-right">Poverty gap %</th>
              <th className="text-right">Readiness gap</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => {
              const v = r.shock_payment_readiness_gap ?? 0;
              const b = v >= 15 ? 5 : v >= 10 ? 4 : v >= 5 ? 3 : v >= 2 ? 2 : v > 0 ? 1 : 0;
              return (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <td className="text-right">{r.poverty_headcount_215_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.sp_coverage_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.findex_account_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.poverty_gap_pct?.toFixed(1) ?? "—"}</td>
                  <td className={`text-right font-semibold heat-${b}`}>
                    {r.shock_payment_readiness_gap?.toFixed(1) ?? "—"}
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
          <li>ASPIRE "total SP coverage" aggregates all programs (social insurance + assistance + labor); does not distinguish universal from targeted.</li>
          <li>Findex account ownership is measured biennially; many ADB DMCs have 2021 values and will update with 2025 round.</li>
          <li>Poverty headcount uses $2.15/day 2017 PPP (international poverty line); this misses near-poor households who would be most exposed to shocks.</li>
          <li>Vanuatu and other small Pacific DMCs have high readiness gap partly because Findex doesn't cover them; the "mean of SP and accounts" falls back to SP only and may be biased.</li>
          <li>Does not measure <em>payment speed</em> (the core of shock-responsive SP). Needs G2P disbursement-time records.</li>
        </ul>
      </section>
    </div>
  );
}
