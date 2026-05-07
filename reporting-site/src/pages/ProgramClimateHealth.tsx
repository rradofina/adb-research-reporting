import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string; country: string;
  emp_agri_pct: number | null;
  emp_industry_pct: number | null;
  outdoor_labor_share_pct: number | null;
  pm25_exposure_ugm3: number | null;
  pm25_year: number | null;
  urban_pop_pct: number | null;
  population_total: number | null;
  exposed_outdoor_millions: number | null;
  workday_loss_pressure_index: number | null;
}
interface Payload { rows: Row[]; sources: any; methodology: any; generated_at: string; }

export default function ProgramClimateHealth() {
  const [data, setData] = useState<Payload | null>(null);
  useEffect(() => { fetch("/data/climate-health-workdays-adb-panel.json").then((r) => r.json()).then(setData); }, []);
  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort((a, b) => (b.workday_loss_pressure_index ?? -1) - (a.workday_loss_pressure_index ?? -1));
  const totalExposed = data.rows.reduce((s, r) => s + (r.exposed_outdoor_millions ?? 0), 0);

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #5 · climate-health-workdays</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Outdoor labor × pollution exposure.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            First-pass screening of hidden labor-productivity pressure.
            Combines WDI employment-in-agriculture and half of employment-
            in-industry (as outdoor-labor proxy) with annual mean PM2.5
            exposure (WDI). Heat (CCKP tasmax × work-hours) is the next
            pipeline step, not included here.
          </p>
        </div>
        <div className="shrink-0"><MaturityChip status="H" /></div>
      </div>

      <div className="mt-10 grid md:grid-cols-2 gap-4">
        <div className="bg-white border border-ink-200 rounded-md p-5">
          <div className="text-xs uppercase tracking-wider text-ink-500">Outdoor-labor people in above-WHO-guideline PM2.5</div>
          <div className="mt-2 text-3xl font-semibold tabular">
            {totalExposed.toLocaleString(undefined, { maximumFractionDigits: 0 })}M
          </div>
          <div className="mt-1 text-xs text-ink-500">across ADB DMCs with WDI coverage; India alone contributes ~800M</div>
        </div>
        <div className="bg-white border border-ink-200 rounded-md p-5">
          <div className="text-xs uppercase tracking-wider text-ink-500">Highest single-DMC pressure index</div>
          <div className="mt-2 text-3xl font-semibold tabular">
            {ranked[0]?.workday_loss_pressure_index?.toFixed(1) ?? "—"}
          </div>
          <div className="mt-1 text-xs text-ink-500">{ranked[0]?.country}</div>
        </div>
      </div>

      <div className="mt-10 bg-white border border-ink-200 rounded-md overflow-x-auto">
        <table className="data-table tabular w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ISO3</th>
              <th>Country</th>
              <th className="text-right">Agri emp %</th>
              <th className="text-right">Industry emp %</th>
              <th className="text-right">Outdoor labor %</th>
              <th className="text-right">PM2.5 µg/m³</th>
              <th className="text-right">Exposed outdoor (M)</th>
              <th className="text-right">Pressure</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => {
              const v = r.workday_loss_pressure_index ?? 0;
              const b = v >= 50 ? 5 : v >= 35 ? 4 : v >= 22 ? 3 : v >= 10 ? 2 : v > 0 ? 1 : 0;
              return (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <td className="text-right">{r.emp_agri_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.emp_industry_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.outdoor_labor_share_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.pm25_exposure_ugm3?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.exposed_outdoor_millions?.toLocaleString() ?? "—"}</td>
                  <td className={`text-right font-semibold heat-${b}`}>
                    {r.workday_loss_pressure_index?.toFixed(1) ?? "—"}
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
          <li><strong>Heat is not in this metric.</strong> Program 5's full scope targets heat × humidity × sector-specific work-hours. This first-pass uses PM2.5 only as the exposure side.</li>
          <li>Industry share × 0.5 as "outdoor" is a rough proxy; some industries are indoor (manufacturing) and some outdoor (construction, mining). A proper industry-level cut needs ILOSTAT ISIC rev.4 splits.</li>
          <li>PM2.5 country-means miss intra-country heterogeneity. Urban industrial corridors have far higher exposure than rural outdoor workers see.</li>
          <li>India's 800M headline is real (outdoor-share × total population), but the *productivity-loss* translation needs sector-specific dose-response coefficients (Lancet Countdown, ILO heat-stress models).</li>
        </ul>
      </section>
    </div>
  );
}
