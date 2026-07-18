// Cross-program indicator extractor.
// Pulls a normalized "value per DMC" from each generated JSON file so a
// country profile page can render every program's headline metric.

export interface IndicatorRow {
  iso3: string;
  value: number | null;
  raw?: Record<string, unknown>;
}

export interface IndicatorDef {
  programSlug: string;
  programTitle: string;
  programNumber: number;
  domain: string;
  unit: string;
  /** Higher = more vulnerable (used for heatmap direction). */
  higherIsWorse: boolean;
  /** Short headline metric for cards. */
  metricLabel: string;
  /** Full sentence used in DMC profile. */
  sentenceTemplate: (v: number, raw?: any) => string;
  /** URL to the program detail page. */
  href: string;
  /** Optional thumbnail color */
  accent?: "crimson" | "sage" | "ochre" | "ink";
  /** JSON file path under /data/ + extractor */
  source: {
    path: string;
    extract: (
      json: any,
    ) => IndicatorRow[];
  };
}


function fromArrayOfRows(
  jsonKey: string | null,
  iso3Field: string,
  valueField: string,
): (json: any) => IndicatorRow[] {
  return (json: any) => {
    const arr = jsonKey === null
      ? Array.isArray(json) ? json : (json.rows ?? json.data ?? [])
      : (json[jsonKey] ?? json.rows ?? []);
    if (!Array.isArray(arr)) return [];
    return arr
      .filter((r: any) => r && r[iso3Field])
      .map((r: any) => ({
        iso3: r[iso3Field],
        value:
          typeof r[valueField] === "number"
            ? (r[valueField] as number)
            : null,
        raw: r,
      }));
  };
}


export const INDICATORS: IndicatorDef[] = [
  {
    programSlug: "public-service-data-quality",
    programTitle: "Service registry gap",
    programNumber: 13,
    domain: "Measurement",
    unit: "% gap",
    higherIsWorse: true,
    metricLabel: "OSM clinical-registry gap",
    sentenceTemplate: (v, r) =>
      `OSM clinical-registry gap ${v.toFixed(1)}% — OSM captures ${((r?.totals?.ratio_osm_to_clinical ?? 0) * 100).toFixed(1)}% of the clinical-tier registry.`,
    href: "/program/public-service-data-quality",
    accent: "crimson",
    source: {
      path: "/data/public-service-data-quality-summary.json",
      extract: (json: any) => {
        const arr = json.countries ?? [];
        return arr.map((r: any) => ({
          iso3: r.iso3,
          value:
            typeof r?.totals?.ratio_osm_to_clinical === "number"
              ? (1 - r.totals.ratio_osm_to_clinical) * 100
              : null,
          raw: r,
        }));
      },
    },
  },
  {
    programSlug: "access-services",
    programTitle: "Access-stress pilot",
    programNumber: 1,
    domain: "Access",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Access stress",
    sentenceTemplate: (v, r) =>
      `Access-stress ${v.toFixed(1)} across ${r?.n_adm1_units ?? "—"} ADM1 units; worst observed ADM1 ${r?.worst_adm1_name ?? "—"}.`,
    href: "/program/access-services",
    accent: "sage",
    source: {
      path: "/programs/access-services/generated/access-services-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "population_weighted_access_stress"),
    },
  },
  {
    programSlug: "coastal-informal-risk",
    programTitle: "Coastal informal pressure",
    programNumber: 6,
    domain: "Built form",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Coastal informal pressure",
    sentenceTemplate: (v, r) =>
      `Coastal informal-pressure ${v.toFixed(1)} — urban share ${r?.urban_pct?.toFixed?.(1) ?? "—"}%, slum share ${r?.slum_pct_urban?.toFixed?.(1) ?? "—"}%.`,
    href: "/program/coastal-informal-risk/evidence",
    accent: "crimson",
    source: {
      path: "/programs/coastal-informal-risk/generated/coastal-informal-risk-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "coastal_informal_risk_index"),
    },
  },
  {
    programSlug: "flood-market-access",
    programTitle: "Sylhet flood-route access",
    programNumber: 8,
    domain: "Access",
    unit: "% disconnected",
    higherIsWorse: true,
    metricLabel: "Modeled market disconnection",
    sentenceTemplate: (v, r) =>
      `In the Sylhet construct-validation pilot, ${v.toFixed(1)}% of baseline-accessible covered population is disconnected after mechanically removing flood-intersecting road edges (${Math.round(r?.disconnected_population ?? 0).toLocaleString()} people).`,
    href: "/program/flood-market-access/evidence",
    accent: "sage",
    source: {
      path: "/programs/flood-market-access/generated/flood-sylhet-route-pilot.json",
      extract: (json: any) => [{
        iso3: "BGD",
        value: typeof json?.headline?.base_disconnected_share_pct === "number"
          ? json.headline.base_disconnected_share_pct
          : null,
        raw: json?.base_result,
      }],
    },
  },
  {
    programSlug: "invisible-urbanization",
    programTitle: "Urban-classification lag",
    programNumber: 4,
    domain: "Built form",
    unit: "signal",
    higherIsWorse: true,
    metricLabel: "Invisible urbanization signal",
    sentenceTemplate: (v, r) =>
      `Urbanization signal ${v.toFixed(1)} — rural share ${r?.rural_pct?.toFixed?.(1) ?? "—"}% and urban-population growth ${r?.urban_pop_growth_pct?.toFixed?.(2) ?? "—"}%.`,
    href: "/program/invisible-urbanization/evidence",
    accent: "ochre",
    source: {
      path: "/programs/invisible-urbanization/generated/invisible-urbanization-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "invisible_urbanization_signal"),
    },
  },
  {
    programSlug: "remittance-resilience",
    programTitle: "Remittance fragility",
    programNumber: 14,
    domain: "Finance",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Fragility index",
    sentenceTemplate: (v, r) =>
      `Fragility index ${v.toFixed(1)} — ${r?.wdi_remittance_pct_gdp?.toFixed?.(1) ?? "—"}% of GDP from remittances, paid through corridors averaging ${r?.rpw_mean_cost_pct?.toFixed?.(2) ?? "—"}%.`,
    href: "/program/remittance-resilience",
    accent: "crimson",
    source: {
      path: "/data/remittance-resilience-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "fragility_index"),
    },
  },
  {
    programSlug: "grid-reliability-heat",
    programTitle: "Grid concentration",
    programNumber: 10,
    domain: "Energy",
    unit: "Herfindahl",
    higherIsWorse: true,
    metricLabel: "Fuel mix Herfindahl",
    sentenceTemplate: (v, r) =>
      `Herfindahl ${v.toFixed(2)} on ${r?.plant_count ?? "—"} plants, dominated by ${r?.top_fuel ?? "?"} (${((r?.top_fuel_share ?? 0) * 100).toFixed(0)}% of capacity).`,
    href: "/program/grid-reliability-heat",
    accent: "ochre",
    source: {
      path: "/data/grid-reliability-heat-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "fuel_herfindahl"),
    },
  },
  {
    programSlug: "disaster-recovery-lag",
    programTitle: "Disaster burden",
    programNumber: 7,
    domain: "Disaster",
    unit: "events / year",
    higherIsWorse: true,
    metricLabel: "Events / year",
    sentenceTemplate: (v, r) =>
      `${v.toFixed(2)} disasters/year (2000–2025), affecting ${(r?.total_affected ? Number(r.total_affected).toLocaleString() : "—")} people cumulatively.`,
    href: "/program/disaster-recovery-lag",
    accent: "crimson",
    source: {
      path: "/data/disaster-recovery-lag-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "events_per_year"),
    },
  },
  {
    programSlug: "migration-displacement-signals",
    programTitle: "Emigration",
    programNumber: 11,
    domain: "Migration",
    unit: "people",
    higherIsWorse: true,
    metricLabel: "Emigrant stock 2024",
    sentenceTemplate: (v, r) =>
      `${(v / 1e6).toFixed(1)}M emigrants in 2024; top destination ${r?.top_destinations?.[0]?.dest_name ?? "—"}.`,
    href: "/program/migration-displacement-signals",
    accent: "sage",
    source: {
      path: "/data/migration-displacement-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "emigrant_stock_2024"),
    },
  },
  {
    programSlug: "port-hinterland-friction",
    programTitle: "Trade friction",
    programNumber: 12,
    domain: "Trade",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Friction exposure",
    sentenceTemplate: (v, r) =>
      `Friction-exposure ${v.toFixed(2)} (LPI overall ${r?.lpi_overall?.toFixed?.(2) ?? "—"}, imports $${((r?.imports_usd ?? 0) / 1e9).toFixed(1)}B).`,
    href: "/program/port-hinterland-friction",
    accent: "ink",
    source: {
      path: "/data/port-hinterland-friction-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "friction_exposure_index"),
    },
  },
  {
    programSlug: "water-stress-crop-diversification",
    programTitle: "Water stress",
    programNumber: 17,
    domain: "Environment",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Water-crop pressure",
    sentenceTemplate: (v, r) =>
      `Pressure index ${v.toFixed(1)} — freshwater withdrawal at ${r?.water_withdrawal_pct_resources?.toFixed?.(0) ?? "—"}% of internal resources, ${r?.rural_population_pct?.toFixed?.(0) ?? "—"}% rural.`,
    href: "/program/water-stress-crop-diversification",
    accent: "sage",
    source: {
      path: "/data/water-stress-crop-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "water_crop_pressure_index"),
    },
  },
  {
    programSlug: "climate-health-workdays",
    programTitle: "Climate-health pressure",
    programNumber: 5,
    domain: "Health",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Workday-loss pressure",
    sentenceTemplate: (v, r) =>
      `Pressure ${v.toFixed(1)} — ${r?.outdoor_labor_share_pct?.toFixed?.(0) ?? "—"}% outdoor labor exposed to PM2.5 ${r?.pm25_exposure_ugm3?.toFixed?.(1) ?? "—"} µg/m³.`,
    href: "/program/climate-health-workdays",
    accent: "ochre",
    source: {
      path: "/data/climate-health-workdays-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "workday_loss_pressure_index"),
    },
  },
  {
    programSlug: "school-heat-disruption",
    programTitle: "School heat",
    programNumber: 15,
    domain: "Education",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "School-heat pressure",
    sentenceTemplate: (v, r) =>
      `Pressure ${v.toFixed(1)} — ${r?.children_0_14_millions?.toFixed?.(1) ?? "—"}M children, tasmax ${r?.annual_tasmax_1995_2014_celsius?.toFixed?.(1) ?? "—"}°C, PTR ${r?.primary_pupil_teacher_ratio?.toFixed?.(0) ?? "—"}.`,
    href: "/program/school-heat-disruption",
    accent: "ochre",
    source: {
      path: "/data/school-heat-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "school_heat_pressure_index"),
    },
  },
  {
    programSlug: "social-protection-shock-coverage",
    programTitle: "Shock readiness",
    programNumber: 16,
    domain: "Social protection",
    unit: "gap",
    higherIsWorse: true,
    metricLabel: "Readiness gap",
    sentenceTemplate: (v, r) =>
      `Gap ${v.toFixed(1)} — ${r?.poverty_headcount_215_pct?.toFixed?.(1) ?? "—"}% poverty, ${r?.sp_coverage_pct?.toFixed?.(0) ?? "—"}% SP coverage, ${r?.findex_account_pct?.toFixed?.(0) ?? "—"}% account ownership.`,
    href: "/program/social-protection-shock-coverage",
    accent: "sage",
    source: {
      path: "/data/social-protection-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "shock_payment_readiness_gap"),
    },
  },
  {
    programSlug: "food-price-climate-transmission",
    programTitle: "Food-price vulnerability",
    programNumber: 9,
    domain: "Food security",
    unit: "index",
    higherIsWorse: true,
    metricLabel: "Food vulnerability",
    sentenceTemplate: (v, r) =>
      `Vulnerability ${v.toFixed(2)} — CPI ${r?.cpi_inflation_pct?.toFixed?.(1) ?? "—"}%, ag imports ${r?.ag_imports_pct_merch?.toFixed?.(1) ?? "—"}% of merchandise.`,
    href: "/program/food-price-climate-transmission",
    accent: "ochre",
    source: {
      path: "/data/food-price-adb-panel.json",
      extract: fromArrayOfRows("rows", "iso3", "food_price_vulnerability"),
    },
  },
  {
    programSlug: "air-monitoring",
    programTitle: "Air observability",
    programNumber: 3,
    domain: "Environment",
    unit: "score",
    higherIsWorse: true,
    metricLabel: "Observability gap",
    sentenceTemplate: (v, r) =>
      `Gap score ${Math.round(v)} — ${r?.publicLocations ?? r?.public_locations ?? "—"} OpenAQ public monitors against PM2.5 ${(r?.pm25?.wdiAnnualUgM3 ?? r?.pm25_exposure_ugm3)?.toFixed?.(1) ?? "—"} µg/m³.`,
    href: "/program/air-monitoring",
    accent: "ink",
    source: {
      path: "/data/air-monitoring-openaq-pilots.json",
      extract: (json: any) => {
        const arr = json.countries ?? [];
        return arr.map((r: any) => ({
          iso3: r.iso3,
          value:
            r.pm25?.observabilityGapScore ??
            r.pm25_observability_gap_score ??
            null,
          raw: r,
        }));
      },
    },
  },
];


// Country-level loader. Caches in module scope.
const cache = new Map<string, IndicatorRow[]>();

export async function loadIndicator(def: IndicatorDef): Promise<IndicatorRow[]> {
  const key = def.source.path;
  if (cache.has(key)) return cache.get(key)!;
  const json = await fetch(def.source.path).then((r) => r.json());
  const rows = def.source.extract(json);
  cache.set(key, rows);
  return rows;
}


export async function loadAllForCountry(iso3: string) {
  const out: Array<{ def: IndicatorDef; row: IndicatorRow | null }> = [];
  for (const def of INDICATORS) {
    try {
      const rows = await loadIndicator(def);
      const row = rows.find((r) => r.iso3 === iso3) ?? null;
      out.push({ def, row });
    } catch {
      out.push({ def, row: null });
    }
  }
  return out;
}


/** Compute distribution rank for a given indicator value (1 = worst observed, N = best). */
export function computeRank(rows: IndicatorRow[], iso3: string, higherIsWorse: boolean) {
  const valid = rows.filter((r) => r.value !== null) as { iso3: string; value: number }[];
  valid.sort((a, b) => (higherIsWorse ? b.value - a.value : a.value - b.value));
  const idx = valid.findIndex((r) => r.iso3 === iso3);
  return idx === -1 ? null : { rank: idx + 1, total: valid.length };
}
