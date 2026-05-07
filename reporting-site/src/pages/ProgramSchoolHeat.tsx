import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string; country: string;
  primary_pupil_teacher_ratio: number | null;
  ptr_year: number | null;
  pop_0_14_pct: number | null;
  pop_total: number | null;
  children_0_14_millions: number | null;
  annual_tasmax_1995_2014_celsius: number | null;
  school_heat_pressure_index: number | null;
}
interface Payload { rows: Row[]; sources: any; methodology: any; generated_at: string; }

export default function ProgramSchoolHeat() {
  const [data, setData] = useState<Payload | null>(null);
  useEffect(() => { fetch("/data/school-heat-adb-panel.json").then((r) => r.json()).then(setData); }, []);
  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort((a, b) => (b.school_heat_pressure_index ?? -1) - (a.school_heat_pressure_index ?? -1));
  const totalChildren = data.rows.reduce((s, r) => s + (r.children_0_14_millions ?? 0), 0);

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #15 · school-heat-disruption</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">Heat on learning.</h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            First-pass school-heat-pressure composite for ADB DMCs.
            Combines CCKP historical (1995–2014) annual mean daily tasmax
            with WDI school-age child share and primary pupil-teacher
            ratio. Higher value = more children in hotter countries with
            higher PTR.
          </p>
        </div>
        <div className="shrink-0"><MaturityChip status="H" /></div>
      </div>

      <div className="mt-10 grid md:grid-cols-2 gap-4">
        <div className="bg-white border border-ink-200 rounded-md p-5">
          <div className="text-xs uppercase tracking-wider text-ink-500">Children 0–14 in ADB DMCs (coverage)</div>
          <div className="mt-2 text-3xl font-semibold tabular">{Math.round(totalChildren).toLocaleString()}M</div>
          <div className="mt-1 text-xs text-ink-500">India alone: ~357M</div>
        </div>
        <div className="bg-white border border-ink-200 rounded-md p-5">
          <div className="text-xs uppercase tracking-wider text-ink-500">Hottest DMC by historical tasmax</div>
          <div className="mt-2 text-3xl font-semibold tabular">
            {Math.max(...ranked.map((r) => r.annual_tasmax_1995_2014_celsius ?? 0)).toFixed(1)}°C
          </div>
          <div className="mt-1 text-xs text-ink-500">Cambodia (31.9°C, annual daily mean max)</div>
        </div>
      </div>

      <div className="mt-10 bg-white border border-ink-200 rounded-md overflow-x-auto">
        <table className="data-table tabular w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ISO3</th>
              <th>Country</th>
              <th className="text-right">Children 0–14 (M)</th>
              <th className="text-right">0–14 % pop</th>
              <th className="text-right">Primary PTR</th>
              <th className="text-right">Annual tasmax °C</th>
              <th className="text-right">Pressure</th>
            </tr>
          </thead>
          <tbody>
            {ranked.map((r) => {
              const v = r.school_heat_pressure_index ?? 0;
              const b = v >= 12 ? 5 : v >= 7 ? 4 : v >= 4 ? 3 : v >= 2 ? 2 : v > 0 ? 1 : 0;
              return (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <td className="text-right">{r.children_0_14_millions?.toLocaleString() ?? "—"}</td>
                  <td className="text-right">{r.pop_0_14_pct?.toFixed(1) ?? "—"}</td>
                  <td className="text-right">{r.primary_pupil_teacher_ratio?.toFixed(1) ?? "—"}</td>
                  <td className={"text-right " + ((r.annual_tasmax_1995_2014_celsius ?? 0) >= 30 ? "text-signal-urgent font-semibold" : "")}>
                    {r.annual_tasmax_1995_2014_celsius?.toFixed(1) ?? "—"}
                  </td>
                  <td className={`text-right font-semibold heat-${b}`}>
                    {r.school_heat_pressure_index?.toFixed(1) ?? "—"}
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
          <li>Historical tasmax (1995–2014) understates current heat. A 2040–2059 SSP2-4.5 projection would be the right lens for forward-looking vulnerability; this version uses the baseline.</li>
          <li>Country-mean tasmax masks intra-country variation. Southern India is meaningfully hotter than northern India; single-value metrics lose that.</li>
          <li>Primary PTR is missing for several small Pacific DMCs (Samoa, Fiji). Where missing, the index defaults to neutral multiplier of 1.0, which may understate pressure.</li>
          <li>Does not measure <em>learning loss</em> — requires PISA / TIMSS assessments paired with heat-day records, which is a separate pipeline.</li>
        </ul>
      </section>
    </div>
  );
}
