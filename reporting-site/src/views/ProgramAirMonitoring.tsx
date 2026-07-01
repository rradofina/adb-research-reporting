"use client";

import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface EconomyRow {
  iso2: string;
  iso3: string;
  name: string;
  subregion: string;
  population?: number;
  public_locations?: number;
  pm25_locations?: number;
  pm25_exposure_ugm3?: number;
  pm25_above_who_guideline_5_ugm3?: boolean;
  pm25_observability_gap_score?: number;
  pm25_observability_status?: string;
  who_city_pm25_mean?: number;
  who_highest_pm25_city?: string;
}

export default function ProgramAirMonitoring() {
  const [payload, setPayload] = useState<any | null>(null);

  useEffect(() => {
    fetch("/data/air-monitoring-openaq-pilots.json")
      .then((r) => r.json())
      .then(setPayload);
  }, []);

  const economies: EconomyRow[] = payload?.economies || payload?.data || payload?.rows || [];

  const ranked = [...economies].sort(
    (a, b) =>
      (b.pm25_observability_gap_score ?? 0) -
      (a.pm25_observability_gap_score ?? 0),
  );

  return (
    <div>
      <div className="flex items-start justify-between gap-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Program #3 · air-monitoring
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Air pollution where ground monitoring is weak
          </h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            OpenAQ v3 public-monitor metadata + World Bank WDI PM2.5 +
            WHO AAQ v6.1 city PM2.5 validation across 50 ADB regional
            member economies. Measures the <em>observability gap</em>:
            where exposure is high but monitoring is sparse.
          </p>
        </div>
        <div className="shrink-0">
          <MaturityChip status="SR" />
        </div>
      </div>

      {payload && (
        <section className="mt-10">
          <div className="grid md:grid-cols-3 gap-4">
            <Stat
              label="Economies queried"
              value={economies.length}
              note="ADB regional members"
            />
            <Stat
              label="Economies with PM2.5 above WHO guideline"
              value={economies.filter(
                (e) => e.pm25_above_who_guideline_5_ugm3,
              ).length}
              note="≥5 µg/m³ annual exposure"
            />
            <Stat
              label="Economies without any public PM2.5 monitor"
              value={
                economies.filter(
                  (e) => e.pm25_observability_status === "no_public_pm25_monitor",
                ).length
              }
              note="zero OpenAQ coverage"
            />
          </div>
        </section>
      )}

      <section className="mt-10">
        <h2 className="text-lg font-semibold">Observability gap score — ranked</h2>
        <p className="mt-2 text-sm text-ink-500">
          First-pass national screening: 65% WDI PM2.5 exposure pressure ×
          35% public-monitor scarcity. Triage, not an epidemiological measure.
        </p>
        <div className="mt-6 bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>Economy</th>
                <th>Subregion</th>
                <th className="text-right">Pop</th>
                <th className="text-right">Public OpenAQ locs</th>
                <th className="text-right">PM2.5 locs</th>
                <th className="text-right">WDI PM2.5 (µg/m³)</th>
                <th className="text-right">Gap score</th>
                <th>Status</th>
                <th>Highest-PM2.5 city (WHO)</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((e) => {
                const bucket = gapBucket(e.pm25_observability_gap_score);
                return (
                  <tr key={e.iso3}>
                    <td>{e.name} ({e.iso3})</td>
                    <td>{e.subregion}</td>
                    <td className="text-right">{e.population?.toLocaleString() ?? "—"}</td>
                    <td className="text-right">{e.public_locations ?? "—"}</td>
                    <td className="text-right">{e.pm25_locations ?? "—"}</td>
                    <td className="text-right">
                      {e.pm25_exposure_ugm3 !== undefined
                        ? e.pm25_exposure_ugm3.toFixed(1)
                        : "—"}
                    </td>
                    <td className={`text-right font-semibold heat-${bucket}`}>
                      {e.pm25_observability_gap_score ?? "—"}
                    </td>
                    <td className="text-xs">{e.pm25_observability_status}</td>
                    <td className="text-xs">{e.who_highest_pm25_city ?? "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
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

function gapBucket(v?: number) {
  if (v === undefined) return 0;
  if (v >= 80) return 5;
  if (v >= 60) return 4;
  if (v >= 40) return 3;
  if (v >= 20) return 2;
  return 1;
}
