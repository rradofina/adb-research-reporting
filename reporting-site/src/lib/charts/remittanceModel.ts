/**
 * remittanceModel.ts — derive the native-chart inputs for the remittance
 * flagship from its committed panel JSON. Shared by the /native-charts
 * showcase page and the in-context Topic hero so the two never drift.
 *
 * No value is hard-coded: dependence (% GDP), cost, corridor counts and
 * the cluster all come from the fetched panel. The cluster is the top-5
 * by the triage composite (used only to SELECT the set, never surfaced
 * as a headline number — CONSTITUTION.md §6.4). SDG_CAP is a published
 * policy threshold (SDG 10.c.1), labeled as such.
 */
import { num, type Panel, type PanelRow } from "./data";

export const SDG_CAP = 5;

export interface Callout {
  iso3: string;
  valueText: string;
  name?: string;
  note?: string;
  kind?: "cluster" | "excluded";
  labelDx?: number;
  labelDy?: number;
  anchor?: "start" | "middle" | "end";
}
export interface BarDatum {
  label: string;
  value: number;
  highlight?: boolean;
  tip?: Array<{ k: string; v: string; accent?: boolean }>;
}
export interface PointDatum {
  label: string;
  x: number;
  y: number;
  size?: number;
  highlight?: boolean;
  tip?: Array<{ k: string; v: string; accent?: boolean }>;
}

// Caller-driven label placement so the dense Pacific cluster never collides.
const PLACEMENT: Record<string, Partial<Callout>> = {
  KGZ: { labelDx: 8, labelDy: -20, anchor: "start" },
  NPL: { labelDx: 9, labelDy: 17, anchor: "start" },
  TON: { labelDx: -12, labelDy: 20, anchor: "end" },
  WSM: { labelDx: -12, labelDy: -8, anchor: "end" },
  VUT: { labelDx: -12, labelDy: 24, anchor: "end" },
  TJK: { labelDx: -10, labelDy: 20, anchor: "end" },
};

export interface RemittanceModel {
  headline: string;
  values: Record<string, number>;
  maxGdp: number;
  domain: [number, number];
  callouts: Callout[];
  bar: BarDatum[];
  scatter: PointDatum[];
  clusterSize: number;
}

export function buildRemittanceModel(panel: Panel): RemittanceModel | null {
  if (!panel?.rows) return null;
  const rows = panel.rows;
  const gdp = (r: PanelRow) => num(r.wdi_remittance_pct_gdp);
  const cost = (r: PanelRow) => num(r.rpw_mean_cost_pct);
  const frag = (r: PanelRow) => num(r.fragility_index);
  const corr = (r: PanelRow) => num(r.rpw_corridors_observed);
  const firms = (r: PanelRow) => num(r.rpw_firms_observed);

  const cluster = new Set(
    rows
      .filter((r) => frag(r) != null)
      .sort((a, b) => (frag(b) as number) - (frag(a) as number))
      .slice(0, 5)
      .map((r) => r.iso3),
  );

  const ton = rows.find((r) => r.iso3 === "TON");
  const headline = ton ? `${(gdp(ton) as number).toFixed(1)}%` : "";

  const values: Record<string, number> = {};
  for (const r of rows) {
    const g = gdp(r);
    if (g != null) values[r.iso3] = g;
  }
  const maxGdp = Math.max(...Object.values(values));

  const callouts: Callout[] = [];
  for (const r of rows) {
    if (!cluster.has(r.iso3)) continue;
    callouts.push({
      iso3: r.iso3,
      valueText: `${(gdp(r) as number).toFixed(1)}%`,
      kind: "cluster",
      ...PLACEMENT[r.iso3],
    });
  }
  const tjk = rows.find((r) => r.iso3 === "TJK");
  if (tjk) {
    callouts.push({
      iso3: "TJK",
      valueText: `${(gdp(tjk) as number).toFixed(1)}%`,
      kind: "excluded",
      note: `excluded — only ${corr(tjk)} corridor / ${firms(tjk)} firm in RPW`,
      ...PLACEMENT.TJK,
    });
  }

  const bar: BarDatum[] = rows
    .filter((r) => gdp(r) != null)
    .sort((a, b) => (gdp(b) as number) - (gdp(a) as number))
    .slice(0, 12)
    .map((r) => ({
      label: r.iso3,
      value: gdp(r) as number,
      highlight: cluster.has(r.iso3),
      tip: [
        { k: "Remittances/GDP", v: `${(gdp(r) as number).toFixed(1)}%`, accent: true },
        { k: "Avg cost", v: cost(r) != null ? `${(cost(r) as number).toFixed(1)}%` : "no RPW data" },
        { k: "RPW corridors", v: corr(r) != null ? String(corr(r)) : "0" },
      ],
    }));

  const scatter: PointDatum[] = rows
    .filter((r) => gdp(r) != null && cost(r) != null && (corr(r) ?? 0) > 0)
    .map((r) => ({
      label: r.iso3,
      x: gdp(r) as number,
      y: cost(r) as number,
      size: corr(r) ?? 1,
      highlight: cluster.has(r.iso3),
      tip: [
        { k: "Remittances/GDP", v: `${(gdp(r) as number).toFixed(1)}%`, accent: true },
        { k: "Avg cost", v: `${(cost(r) as number).toFixed(1)}%`, accent: (cost(r) as number) > SDG_CAP },
        { k: "Corridors", v: String(corr(r)) },
        { k: "Firms", v: String(firms(r) ?? "—") },
      ],
    }));

  const domain: [number, number] = [0, Math.ceil(maxGdp)];
  return { headline, values, maxGdp, domain, callouts, bar, scatter, clusterSize: cluster.size };
}
