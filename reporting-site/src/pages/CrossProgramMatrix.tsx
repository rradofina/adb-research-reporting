import { useEffect, useMemo, useState } from "react";

/**
 * Cross-program DMC vulnerability matrix.
 *
 * Pulls per-DMC scores from each computed program and presents a single
 * matrix where rows = DMCs, columns = programs. Cells show normalized
 * vulnerability rank within each program (0–100, higher = more vulnerable).
 *
 * Data sources:
 *  - Program 13 PSDQ: OSM/clinical (lower = more vulnerable; flipped for matrix)
 *  - Program 14 Remittance: fragility_index (higher = more vulnerable)
 *  - Program 10 Grid: fuel_herfindahl (higher = more concentrated, ie more vulnerable)
 *  - Program 1 Access services: access_stress_index (we aggregate to country mean)
 *  - Program 3 Air monitoring: pm25_observability_gap_score
 */
const PROGRAM_LABELS: Record<string, string> = {
  psdq: "P13 Data Quality",
  remit: "P14 Remittance",
  grid: "P10 Grid Concentration",
  access: "P1 Access Services",
  air: "P3 Air Observability",
  disaster: "P7 Disaster Burden",
  migration: "P11 Emigration",
  port: "P12 Trade Friction",
};

interface DMCRow {
  iso3: string;
  country: string;
  scores: Partial<Record<keyof typeof PROGRAM_LABELS, number>>;
  rawValues: Partial<Record<string, number | string>>;
}

export default function CrossProgramMatrix() {
  const [psdq, setPsdq] = useState<any | null>(null);
  const [remit, setRemit] = useState<any | null>(null);
  const [grid, setGrid] = useState<any | null>(null);
  const [access, setAccess] = useState<any | null>(null);
  const [air, setAir] = useState<any | null>(null);
  const [disaster, setDisaster] = useState<any | null>(null);
  const [migration, setMigration] = useState<any | null>(null);
  const [port, setPort] = useState<any | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/data/public-service-data-quality-summary.json").then((r) => r.json()),
      fetch("/data/remittance-resilience-adb-panel.json").then((r) => r.json()),
      fetch("/data/grid-reliability-heat-adb-panel.json").then((r) => r.json()),
      fetch("/data/access-services-computed-admin1.json").then((r) => r.json()),
      fetch("/data/air-monitoring-openaq-pilots.json").then((r) => r.json()),
      fetch("/data/disaster-recovery-lag-adb-panel.json").then((r) => r.json()),
      fetch("/data/migration-displacement-adb-panel.json").then((r) => r.json()),
      fetch("/data/port-hinterland-friction-adb-panel.json").then((r) => r.json()),
    ]).then(([p, r, g, a, ai, d, m, pt]) => {
      setPsdq(p); setRemit(r); setGrid(g); setAccess(a); setAir(ai);
      setDisaster(d); setMigration(m); setPort(pt);
    });
  }, []);

  const matrix: DMCRow[] = useMemo(() => {
    const dmcMap = new Map<string, DMCRow>();
    const upsert = (iso3: string, country: string) => {
      if (!dmcMap.has(iso3)) {
        dmcMap.set(iso3, { iso3, country, scores: {}, rawValues: {} });
      }
      return dmcMap.get(iso3)!;
    };

    // PSDQ: rank by OSM/clinical (lower = more vulnerable; flip)
    if (psdq?.countries) {
      const cs = psdq.countries as any[];
      const sorted = [...cs].sort((a, b) => (a.totals.ratio_osm_to_clinical ?? 1) - (b.totals.ratio_osm_to_clinical ?? 1));
      sorted.forEach((c, i) => {
        const r = upsert(c.iso3, c.country);
        r.scores.psdq = sorted.length > 1 ? Math.round(((sorted.length - 1 - i) / (sorted.length - 1)) * 100) : 50;
        r.rawValues.psdq_osm_clin = (c.totals.ratio_osm_to_clinical * 100).toFixed(1) + "%";
      });
    }

    // Remittance: fragility_index direct
    if (remit?.rows) {
      const rows = (remit.rows as any[]).filter((r) => r.fragility_index !== null);
      const max = Math.max(...rows.map((r) => r.fragility_index));
      rows.forEach((row) => {
        const r = upsert(row.iso3, row.country);
        r.scores.remit = Math.round((row.fragility_index / max) * 100);
        r.rawValues.remit_frag = row.fragility_index;
      });
    }

    // Grid: fuel_herfindahl direct (* 100)
    if (grid?.rows) {
      const rows = (grid.rows as any[]).filter((r) => r.fuel_herfindahl !== null);
      rows.forEach((row) => {
        const r = upsert(row.iso3, row.country);
        r.scores.grid = Math.round(row.fuel_herfindahl * 100);
        r.rawValues.grid_top = row.top_fuel + " " + ((row.top_fuel_share ?? 0) * 100).toFixed(0) + "%";
      });
    }

    // Access services: country-mean access_stress_index
    if (Array.isArray(access)) {
      const byIso = new Map<string, number[]>();
      const names = new Map<string, string>();
      (access as any[]).forEach((row) => {
        if (!byIso.has(row.iso3)) byIso.set(row.iso3, []);
        byIso.get(row.iso3)!.push(Number(row.access_stress_index));
        names.set(row.iso3, row.country_name);
      });
      byIso.forEach((scores, iso) => {
        const mean = scores.reduce((s, n) => s + n, 0) / scores.length;
        const r = upsert(iso, names.get(iso)!);
        r.scores.access = Math.round(mean);
        r.rawValues.access_mean = mean.toFixed(1);
      });
    }

    // Air monitoring: pm25_observability_gap_score
    if (air?.economies) {
      const rows = (air.economies as any[]).filter((r) => r.pm25_observability_gap_score !== undefined);
      rows.forEach((row) => {
        const r = upsert(row.iso3, row.name);
        r.scores.air = Math.round(row.pm25_observability_gap_score);
        r.rawValues.air_pm25 = row.pm25_exposure_ugm3 ? row.pm25_exposure_ugm3.toFixed(1) + " µg/m³" : "—";
      });
    }

    // Disaster: events_per_year normalized
    if (disaster?.rows) {
      const rows = (disaster.rows as any[]).filter((r) => r.events_per_year > 0);
      const max = Math.max(...rows.map((r) => r.events_per_year));
      rows.forEach((row) => {
        const r = upsert(row.iso3, row.country);
        r.scores.disaster = Math.round((row.events_per_year / max) * 100);
        r.rawValues.disaster_evyr = row.events_per_year.toFixed(2) + " /yr";
      });
    }

    // Migration: emigrant_stock normalized (higher = more mobility signal)
    if (migration?.rows) {
      const rows = (migration.rows as any[]).filter((r) => r.emigrant_stock_2024 > 0);
      const max = Math.max(...rows.map((r) => r.emigrant_stock_2024));
      rows.forEach((row) => {
        const r = upsert(row.iso3, row.country);
        r.scores.migration = Math.round((row.emigrant_stock_2024 / max) * 100);
        r.rawValues.migration_emig = row.emigrant_stock_2024.toLocaleString();
      });
    }

    // Port: friction_exposure_index normalized
    if (port?.rows) {
      const rows = (port.rows as any[]).filter((r) => r.friction_exposure_index !== null);
      const max = Math.max(...rows.map((r) => r.friction_exposure_index));
      rows.forEach((row) => {
        const r = upsert(row.iso3, row.country);
        r.scores.port = Math.round((row.friction_exposure_index / max) * 100);
        r.rawValues.port_frict = row.friction_exposure_index.toFixed(2);
      });
    }

    // Return rows sorted by composite of available scores
    const arr = Array.from(dmcMap.values());
    arr.forEach((r) => {
      const vals = Object.values(r.scores).filter((v): v is number => typeof v === "number");
      r.scores._composite = vals.length ? Math.round(vals.reduce((s, n) => s + n, 0) / vals.length) : 0;
    });
    arr.sort((a, b) => (b.scores._composite ?? 0) - (a.scores._composite ?? 0));
    return arr;
  }, [psdq, remit, grid, access, air, disaster, migration, port]);

  if (!psdq || !remit || !grid || !access || !air || !disaster || !migration || !port) {
    return <div className="p-12 text-ink-500">Loading cross-program data…</div>;
  }

  return (
    <div>
      <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
         Cross-program · 8 computed programs
      </p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">
        Vulnerability matrix.
      </h1>
      <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
        For each ADB DMC, normalized rank (0–100, higher = more
        vulnerable) on each program with a computed screening artifact.
        Programs measure different things — read this as <em>signal
        density</em> across measurement gaps, not as a unified risk
        score. Each cell links to its source program for the raw value.
      </p>

      <div className="mt-3 text-xs text-ink-500">
        Per Constitution §6.4 / §14: composite indices are triage; this
        matrix is a navigation aid, not a country ranking.
      </div>

      <section className="mt-8">
        <div className="bg-white border border-ink-200 rounded-md overflow-x-auto">
          <table className="data-table tabular w-full text-sm">
            <thead>
              <tr className="text-left">
                <th>ISO3</th>
                <th>Country</th>
                <th className="text-center">P13 Data Quality</th>
                <th className="text-center">P14 Remittance</th>
                <th className="text-center">P10 Grid</th>
                <th className="text-center">P1 Access</th>
                <th className="text-center">P3 Air</th>
                <th className="text-center">P7 Disaster</th>
                <th className="text-center">P11 Emigration</th>
                <th className="text-center">P12 Friction</th>
                <th className="text-center">Composite</th>
              </tr>
            </thead>
            <tbody>
              {matrix.map((r) => (
                <tr key={r.iso3}>
                  <td>{r.iso3}</td>
                  <td>{r.country}</td>
                  <Cell score={r.scores.psdq} raw={r.rawValues.psdq_osm_clin as string} />
                  <Cell score={r.scores.remit} raw={r.rawValues.remit_frag as number} />
                  <Cell score={r.scores.grid} raw={r.rawValues.grid_top as string} />
                  <Cell score={r.scores.access} raw={r.rawValues.access_mean as string} />
                  <Cell score={r.scores.air} raw={r.rawValues.air_pm25 as string} />
                  <Cell score={r.scores.disaster} raw={r.rawValues.disaster_evyr as string} />
                  <Cell score={r.scores.migration} raw={r.rawValues.migration_emig as string} />
                  <Cell score={r.scores.port} raw={r.rawValues.port_frict as string} />
                  <td className="text-center font-semibold">
                    {r.scores._composite ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-8 bg-white border border-ink-200 rounded-md p-6 text-sm">
        <h2 className="font-semibold">Reading guide</h2>
        <ul className="mt-3 list-disc ml-6 space-y-1 text-ink-700">
          <li><strong>Higher number = more measurement-gap signal.</strong> 100 = worst observed in that program; 0 = best.</li>
          <li>An <strong>empty cell</strong> means the program does not yet cover that DMC.</li>
          <li>The composite is a simple mean of available cells. Programs measure orthogonal phenomena, so a high composite means the DMC has many vulnerability signals; not necessarily that it has any single severe one.</li>
          <li>This view is most useful when paired with the per-program detail pages — click through to see what is actually behind a high cell.</li>
        </ul>
      </section>
    </div>
  );
}

function Cell({ score, raw }: { score?: number; raw?: number | string }) {
  if (score === undefined) return <td className="text-center text-ink-300">—</td>;
  return (
    <td className={`text-center font-semibold heat-${heatBucket(score)}`} title={raw !== undefined ? String(raw) : undefined}>
      {score}
    </td>
  );
}

function heatBucket(v: number) {
  if (v >= 80) return 5;
  if (v >= 60) return 4;
  if (v >= 40) return 3;
  if (v >= 20) return 2;
  if (v > 0) return 1;
  return 0;
}
