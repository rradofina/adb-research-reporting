import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string;
  country: string;
  total_events_2000_2025: number;
  total_affected: number;
  total_deaths: number;
  total_damage_usd_adj: number;
  events_per_year: number;
  type_distribution: Record<string, number>;
  biggest_event: { year: number; type: string; subtype: string; deaths: number; affected: number } | null;
  years_covered: number;
}

interface Payload {
  rows: Row[];
  sources: any;
  generated_at: string;
}

export default function ProgramDisaster() {
  const [data, setData] = useState<Payload | null>(null);
  const [sortBy, setSortBy] = useState<"events_per_year" | "total_affected" | "total_deaths" | "total_damage_usd_adj">("events_per_year");

  useEffect(() => {
    fetch("/data/disaster-recovery-lag-adb-panel.json")
      .then((r) => r.json())
      .then(setData);
  }, []);

  if (!data) return <div className="p-12 text-ink-500">Loading…</div>;

  const ranked = [...data.rows].sort((a, b) => (b[sortBy] ?? 0) - (a[sortBy] ?? 0));

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Program #7 · disaster-recovery-lag
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Disaster burden — 2000 to 2025.
          </h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            Per-DMC structural-burden layer from EM-DAT (CRED). Counts of
            events, total affected, deaths, and CPI-adjusted damage USD
            across 2000–2025. NOT yet a recovery-lag metric — that
            requires indicator-recovery-curve analysis around event
            timestamps. This is the burden layer that lag analysis sits on.
          </p>
        </div>
        <div className="shrink-0">
          <MaturityChip status="H" />
        </div>
      </div>

      <section className="mt-10 grid md:grid-cols-4 gap-4">
        <Stat label="Total events (ADB DMCs)" value={data.rows.reduce((s, r) => s + r.total_events_2000_2025, 0).toLocaleString()} />
        <Stat label="Total affected" value={(data.rows.reduce((s, r) => s + r.total_affected, 0) / 1e9).toFixed(2) + "B"} />
        <Stat label="Total deaths" value={data.rows.reduce((s, r) => s + r.total_deaths, 0).toLocaleString()} />
        <Stat label="Adjusted damage USD" value={"$" + (data.rows.reduce((s, r) => s + r.total_damage_usd_adj, 0) / 1e9).toFixed(0) + "B"} />
      </section>

      <section className="mt-8">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-xs uppercase tracking-wider text-ink-500">Sort by</span>
          {([
            ["events_per_year", "events/year"],
            ["total_affected", "affected"],
            ["total_deaths", "deaths"],
            ["total_damage_usd_adj", "damage USD"],
          ] as const).map(([k, label]) => (
            <button
              key={k}
              onClick={() => setSortBy(k as any)}
              className={
                "px-3 py-1 rounded border text-sm transition " +
                (sortBy === k
                  ? "bg-ink-900 text-ink-50 border-ink-900"
                  : "bg-white text-ink-700 border-ink-200 hover:border-ink-500")
              }
            >
              {label}
            </button>
          ))}
        </div>

        <div className="mt-4 bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>ISO3</th>
                <th>Country</th>
                <th className="text-right">Events 2000–2025</th>
                <th className="text-right">Events / yr</th>
                <th className="text-right">Total affected</th>
                <th className="text-right">Total deaths</th>
                <th className="text-right">Damage USD (adj)</th>
                <th>Biggest single event</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((r) => (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <td className="text-right">{r.total_events_2000_2025.toLocaleString()}</td>
                  <td className={`text-right font-semibold heat-${eventBucket(r.events_per_year)}`}>
                    {r.events_per_year.toFixed(2)}
                  </td>
                  <td className="text-right">{r.total_affected.toLocaleString()}</td>
                  <td className="text-right">{r.total_deaths.toLocaleString()}</td>
                  <td className="text-right">
                    {r.total_damage_usd_adj > 0 ? "$" + (r.total_damage_usd_adj / 1e9).toFixed(2) + "B" : "—"}
                  </td>
                  <td className="text-xs">
                    {r.biggest_event
                      ? `${r.biggest_event.year} ${r.biggest_event.type}: ${r.biggest_event.deaths.toLocaleString()} deaths`
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Caveats</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li><strong>EM-DAT inclusion threshold</strong> requires ≥10 deaths or ≥100 affected or a state of emergency declaration. Smaller events are missed; the burden numbers under-count.</li>
          <li><strong>Damage USD reporting is sparse.</strong> Several DMCs report damage for high-profile events only; the cumulative total is a floor, not a ceiling.</li>
          <li><strong>Population growth confounds time-series.</strong> "Total affected" rises mechanically with population. For trend analysis, normalize by population each year.</li>
          <li><strong>Biggest single event ≠ biggest disaster.</strong> Slow-onset disasters (drought, food insecurity) underrepresent in this view because they affect many years.</li>
          <li><strong>Recovery lag is not measured here.</strong> A separate analysis pairing event timestamps with HMIS / school enrollment / GDP per-capita curves is the next pipeline step.</li>
        </ul>
      </section>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="bg-white border border-ink-200 rounded-md p-5">
      <div className="text-xs uppercase tracking-wider text-ink-500">{label}</div>
      <div className="mt-2 text-2xl font-semibold tabular">{value}</div>
    </div>
  );
}

function eventBucket(v: number) {
  if (v >= 15) return 5;
  if (v >= 8) return 4;
  if (v >= 4) return 3;
  if (v >= 2) return 2;
  if (v > 0) return 1;
  return 0;
}
