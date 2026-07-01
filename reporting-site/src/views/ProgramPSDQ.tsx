"use client";

import { useEffect, useMemo, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface Row {
  iso3: string;
  admin1_code: string;
  admin1_name: string;
  population_2020: number;
  osm_health: number;
  registry_principal: number;
  registry_clinical: number;
  registry_all: number;
  ratio_osm_to_principal: number | null;
  ratio_osm_to_clinical: number | null;
  ratio_osm_to_all: number | null;
  osm_per_100k: number | null;
  registry_principal_per_100k: number | null;
  osm_timestamp: string;
  registry_retrieved_at: string;
}

interface CountryPayload {
  iso3: string;
  country: string;
  source: { name: string; api: string; access_model: string; license: string; retrieved_at: string; total_active: number; pages: number; unmapped: number };
  totals: { osm_health: number; registry_principal: number; registry_clinical: number; registry_all: number; ratio_osm_to_principal: number; ratio_osm_to_clinical: number; ratio_osm_to_all: number };
  rows: Row[];
  generated_at: string;
}

interface Summary {
  generated_at: string;
  countries: Array<{
    iso3: string;
    country: string;
    source: string;
    totals: CountryPayload["totals"];
    num_admin1: number;
    admin1_min_ratio_clinical: number;
    admin1_max_ratio_clinical: number;
    worst_admin1: string;
    best_admin1: string;
  }>;
  interpretation: string;
}

interface BgdFacilitySummary {
  generated_at: string;
  records: number;
  valid_coordinate_records: number;
  coordinate_coverage_pct: number;
  catchment_records: number;
  catchment_coverage_pct: number;
  admin_units: number;
  cache: {
    pages_cached: number[];
    last_page: number | null;
    total_reported: number | null;
  };
}

interface BgdAdminRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  facilities: number;
  active_facilities: number;
  coordinate_facilities: number;
  catchment_facilities: number;
  clinical_tier_facilities: number;
  coordinate_coverage_pct: number;
  catchment_coverage_pct: number;
}

interface BgdAdminPayload {
  generated_at: string;
  rows: BgdAdminRow[];
}

interface OpenBuildingsTileStat {
  tile_id: string;
  rows_processed: number;
  inside_bangladesh: number;
  assigned_within_5km: number;
  confidence_threshold_85_precision: number | null;
  confidence_threshold_90_precision: number | null;
}

interface OpenBuildingsAdminRow {
  division_name: string;
  district_name: string;
  upazila_name: string | null;
  coordinate_facilities: number;
  clinical_tier_facilities: number;
  buildings_nearest_1km_all: number;
  buildings_nearest_3km_all: number;
  buildings_nearest_5km_all: number;
  buildings_nearest_1km_p85: number;
  buildings_nearest_3km_p85: number;
  buildings_nearest_5km_p85: number;
  buildings_nearest_1km_p90: number;
  buildings_nearest_3km_p90: number;
  buildings_nearest_5km_p90: number;
}

interface OpenBuildingsBufferSummary {
  generated_at: string;
  source: string;
  method: string;
  tiles: OpenBuildingsTileStat[];
  facilities: number;
  totals: {
    buildings_nearest_1km_all: number;
    buildings_nearest_3km_all: number;
    buildings_nearest_5km_all: number;
    buildings_nearest_1km_p85: number;
    buildings_nearest_3km_p85: number;
    buildings_nearest_5km_p85: number;
    buildings_nearest_1km_p90: number;
    buildings_nearest_3km_p90: number;
    buildings_nearest_5km_p90: number;
  };
  top_admin_by_3km_p85: OpenBuildingsAdminRow[];
  non_claim: string;
}

interface ExposureGapRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  active_clinical_facilities: number;
  coordinate_facilities: number;
  osm_health: number;
  osm_to_active_clinical_ratio: number | null;
  registry_minus_osm_clinical: number;
  registry_gap_share: number;
  buildings_nearest_3km_p85: number;
  underobserved_buildings_3km_p85_proxy: number;
}

interface ExposureGapSummary {
  generated_at: string;
  method: string;
  osm: {
    osm_elements: number;
    assigned_features: number;
    unassigned_features: number;
    missing_coordinate_features: number;
    timestamp_osm_base: string;
    timestamp_areas_base: string;
  };
  exposure: {
    registry_admin_rows: number;
    matched_osm_features: number;
    osm_features_not_joined_to_registry: number;
    rows_with_open_buildings_denominator: number;
    active_clinical_facilities: number;
    osm_health_joined: number;
    registry_minus_osm_clinical: number;
    buildings_nearest_3km_p85: number;
    underobserved_buildings_3km_p85_proxy: number;
  };
  top_exposure_gap_upazilas: ExposureGapRow[];
  non_claim: string;
}

interface RoadSurfaceRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  join_key: string;
  total_road_km: number;
  classified_surface_km: number;
  paved_km: number;
  unpaved_km: number;
  classified_surface_share: number | null;
  classified_unpaved_share: number | null;
}

interface RoadSurfaceSummary {
  generated_at: string;
  source: string;
  road_source_url: string;
  method: string;
  stats: {
    road_features: number;
    assigned_features: number;
    unassigned_features: number;
    features_with_osm_length: number;
    surface_classified_features: number;
    total_road_km: number;
    classified_surface_km: number;
    paved_km: number;
    unpaved_km: number;
    unknown_surface_km: number;
    classified_surface_share: number | null;
    classified_paved_share: number | null;
    classified_unpaved_share: number | null;
  };
  top_unpaved_km_upazilas: RoadSurfaceRow[];
  top_unpaved_share_upazilas: RoadSurfaceRow[];
  top_total_road_km_upazilas: RoadSurfaceRow[];
  non_claim: string;
}

interface ExposureRoadContextRow {
  division_name: string;
  district_name: string;
  upazila_name: string;
  underobserved_buildings_3km_p85_proxy: number | string;
  total_road_km: number;
  classified_surface_km: number;
  paved_km: number;
  unpaved_km: number;
  classified_surface_share: number;
  classified_unpaved_share: number;
  road_context_score: number;
}

interface ExposureRoadContextSummary {
  generated_at: string;
  method: string;
  stats: {
    exposure_rows: number;
    rows_with_road_context: number;
    rows_with_surface_context: number;
    min_classified_surface_km_for_score: number;
    min_classified_surface_share_for_score: number;
  };
  top_exposure_road_context_upazilas: ExposureRoadContextRow[];
  non_claim: string;
}

interface PhlAdmin3TileStat {
  tile_id: string;
  rows_processed: number;
  assigned_to_adm3: number;
  confidence_threshold_85_precision: number | null;
  confidence_threshold_90_precision: number | null;
  buildings_all_assigned: number;
  buildings_p85_assigned: number;
  buildings_p90_assigned: number;
}

interface PhlAdmin3Row {
  adm3_name: string;
  adm3_pcode: string;
  adm2_name: string;
  adm1_name: string;
  area_sqkm: number | null;
  buildings_p85: number;
  buildings_p90: number;
  registry_clinical: number;
  osm_health: number;
  registry_minus_osm_clinical: number;
  registry_gap_share: number | null;
  underobserved_buildings_adm3_p85_proxy: number;
  buildings_p85_per_sqkm: number | null;
}

interface PhlUnmatchedCityCode {
  attempted_adm3_pcode: string;
  records: number;
  principal: number;
  clinical: number;
  top_regcodes: Array<{ regcode: string; records: number }>;
  top_provcodes: Array<{ provcode: string; records: number }>;
}

interface PhlAdmin3Summary {
  generated_at: string;
  method: string;
  admin3_units: number;
  tiles: PhlAdmin3TileStat[];
  building_totals: {
    buildings_all: number;
    building_area_m2_all: number;
    buildings_p85: number;
    building_area_m2_p85: number;
    buildings_p90: number;
    building_area_m2_p90: number;
  };
  tiles_missing_precision_thresholds: string[];
  nhfr: {
    records: number;
    clinical_records: number;
    direct_adm3_matched_records: number;
    direct_adm3_matched_clinical: number;
    direct_only_matched_records?: number;
    direct_only_matched_clinical?: number;
    adm3_matched_records?: number;
    adm3_matched_clinical?: number;
    psgc_crosswalk_matched_records?: number;
    psgc_special_rule_matched_records?: number;
    match_method_counts?: Record<string, number>;
    unmatched_records: number;
    direct_match_share: number;
    direct_clinical_match_share: number;
    adm3_match_share?: number;
    adm3_clinical_match_share?: number;
    top_unmatched_city_codes: PhlUnmatchedCityCode[];
    code_match_note: string;
  };
  osm: {
    osm_elements: number;
    assigned_features: number;
    unassigned_features: number;
    timestamp_osm_base: string;
    timestamp_areas_base: string;
  };
  joined_rows: {
    admin3_rows: number;
    rows_with_p85_buildings: number;
    rows_with_direct_registry_clinical: number;
    rows_with_osm_health: number;
    rows_with_positive_gap: number;
    underobserved_buildings_adm3_p85_proxy: number;
  };
  top_adm3_exposure_gap: PhlAdmin3Row[];
  top_adm3_building_denominator: PhlAdmin3Row[];
  non_claim: string;
}

interface PhlPovertyContextRow {
  adm3_name: string;
  adm3_pcode: string;
  adm2_name: string;
  adm1_name: string;
  poverty_incidence_2023: number;
  poverty_source_type: string;
  registry_gap_share: number | null;
  buildings_p85: number;
  underobserved_buildings_adm3_p85_proxy: number;
  gap_poverty_context_p85_proxy: number;
}

interface PhlPovertyContextSummary {
  generated_at: string;
  status: string;
  admin3_rows: number;
  rows_with_poverty: number;
  rows_with_sae_poverty: number;
  rows_with_openstat_direct_poverty: number;
  rows_without_poverty: number;
  poverty_join_status_counts: Record<string, number>;
  sources: {
    psa_sae_cached: boolean;
    psa_sae_page_url: string;
    openstat_api_url: string;
  };
  top_gap_poverty_context_p85_proxy: PhlPovertyContextRow[];
  non_claim: string;
}

const COUNTRIES = [
  { iso3: "PHL", name: "Philippines", file: "public-service-data-quality-PHL.json" },
  { iso3: "BGD", name: "Bangladesh", file: "public-service-data-quality-BGD.json" },
];

export default function ProgramPSDQ() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [countries, setCountries] = useState<Record<string, CountryPayload>>({});
  const [bgdFacilitySummary, setBgdFacilitySummary] = useState<BgdFacilitySummary | null>(null);
  const [bgdAdminRows, setBgdAdminRows] = useState<BgdAdminRow[]>([]);
  const [openBuildingsSummary, setOpenBuildingsSummary] = useState<OpenBuildingsBufferSummary | null>(null);
  const [exposureGapSummary, setExposureGapSummary] = useState<ExposureGapSummary | null>(null);
  const [roadSurfaceSummary, setRoadSurfaceSummary] = useState<RoadSurfaceSummary | null>(null);
  const [exposureRoadSummary, setExposureRoadSummary] = useState<ExposureRoadContextSummary | null>(null);
  const [phlAdmin3Summary, setPhlAdmin3Summary] = useState<PhlAdmin3Summary | null>(null);
  const [phlPovertySummary, setPhlPovertySummary] = useState<PhlPovertyContextSummary | null>(null);
  const [selected, setSelected] = useState<string>("PHL");
  const [metric, setMetric] = useState<"clinical" | "principal" | "all">("clinical");

  useEffect(() => {
    fetch("/data/public-service-data-quality-summary.json")
      .then((r) => r.json())
      .then(setSummary);
    Promise.all(
      COUNTRIES.map((c) =>
        fetch(`/data/${c.file}`)
          .then((r) => r.json())
          .then((d: CountryPayload) => [c.iso3, d] as const),
      ),
    ).then((pairs) => setCountries(Object.fromEntries(pairs)));
    fetch("/programs/public-service-data-quality/generated/psdq-bgd-facility-coordinate-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: BgdFacilitySummary | null) => setBgdFacilitySummary(d))
      .catch(() => setBgdFacilitySummary(null));
    fetch("/programs/public-service-data-quality/generated/psdq-bgd-admin-coordinate-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: BgdAdminPayload | null) => setBgdAdminRows(d?.rows ?? []))
      .catch(() => setBgdAdminRows([]));
    fetch("/programs/public-service-data-quality/generated/psdq-bgd-open-buildings-buffer-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: OpenBuildingsBufferSummary | null) => setOpenBuildingsSummary(d))
      .catch(() => setOpenBuildingsSummary(null));
    fetch("/programs/public-service-data-quality/generated/psdq-bgd-exposure-ranked-disagreement-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: ExposureGapSummary | null) => setExposureGapSummary(d))
      .catch(() => setExposureGapSummary(null));
    fetch("/programs/public-service-data-quality/generated/psdq-bgd-road-surface-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: RoadSurfaceSummary | null) => setRoadSurfaceSummary(d))
      .catch(() => setRoadSurfaceSummary(null));
    fetch("/programs/public-service-data-quality/generated/psdq-bgd-exposure-road-context-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: ExposureRoadContextSummary | null) => setExposureRoadSummary(d))
      .catch(() => setExposureRoadSummary(null));
    fetch("/programs/public-service-data-quality/generated/psdq-phl-admin3-open-buildings-context-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: PhlAdmin3Summary | null) => setPhlAdmin3Summary(d))
      .catch(() => setPhlAdmin3Summary(null));
    fetch("/programs/public-service-data-quality/generated/psdq-phl-admin3-poverty-context-summary.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: PhlPovertyContextSummary | null) => setPhlPovertySummary(d))
      .catch(() => setPhlPovertySummary(null));
  }, []);

  const current = countries[selected];

  const ranked = useMemo(() => {
    if (!current) return [];
    const key = `ratio_osm_to_${metric}` as keyof Row;
    return [...current.rows].sort(
      (a, b) => (a[key] as number) - (b[key] as number),
    );
  }, [current, metric]);

  const lowCoordinateAdmin = useMemo(() => {
    return [...bgdAdminRows]
      .filter((row) => row.facilities >= 10 && row.upazila_name?.trim())
      .sort((a, b) => a.coordinate_coverage_pct - b.coordinate_coverage_pct || b.facilities - a.facilities)
      .slice(0, 8);
  }, [bgdAdminRows]);

  const topOpenBuildingsAdmin = useMemo(() => {
    return (openBuildingsSummary?.top_admin_by_3km_p85 ?? [])
      .filter((row) => row.upazila_name?.trim())
      .slice(0, 10);
  }, [openBuildingsSummary]);

  const openBuildingsInside = useMemo(() => {
    return openBuildingsSummary?.tiles.reduce((sum, tile) => sum + tile.inside_bangladesh, 0) ?? 0;
  }, [openBuildingsSummary]);

  const topExposureGapRows = useMemo(() => {
    return exposureGapSummary?.top_exposure_gap_upazilas.slice(0, 10) ?? [];
  }, [exposureGapSummary]);

  const topRoadContextRows = useMemo(() => {
    return exposureRoadSummary?.top_exposure_road_context_upazilas.slice(0, 10) ?? [];
  }, [exposureRoadSummary]);

  const topUnpavedRoadRows = useMemo(() => {
    return roadSurfaceSummary?.top_unpaved_km_upazilas.slice(0, 8) ?? [];
  }, [roadSurfaceSummary]);

  const phlAssignedBuildings = useMemo(() => {
    return phlAdmin3Summary?.tiles.reduce((sum, tile) => sum + tile.assigned_to_adm3, 0) ?? 0;
  }, [phlAdmin3Summary]);

  const topPhlExposureRows = useMemo(() => {
    return phlAdmin3Summary?.top_adm3_exposure_gap.slice(0, 10) ?? [];
  }, [phlAdmin3Summary]);

  const topPhlBuildingRows = useMemo(() => {
    return phlAdmin3Summary?.top_adm3_building_denominator.slice(0, 8) ?? [];
  }, [phlAdmin3Summary]);

  const topPhlUnmatchedCodes = useMemo(() => {
    return phlAdmin3Summary?.nhfr.top_unmatched_city_codes.slice(0, 8) ?? [];
  }, [phlAdmin3Summary]);

  const topPhlPovertyRows = useMemo(() => {
    return phlPovertySummary?.top_gap_poverty_context_p85_proxy.slice(0, 8) ?? [];
  }, [phlPovertySummary]);

  const phlAdm3MatchShare = phlAdmin3Summary?.nhfr.adm3_match_share ?? phlAdmin3Summary?.nhfr.direct_match_share ?? 0;
  const phlAdm3MatchedRecords = phlAdmin3Summary?.nhfr.adm3_matched_records ?? phlAdmin3Summary?.nhfr.direct_adm3_matched_records ?? 0;
  const phlCrosswalkMatchedRecords =
    (phlAdmin3Summary?.nhfr.psgc_crosswalk_matched_records ?? 0) +
    (phlAdmin3Summary?.nhfr.psgc_special_rule_matched_records ?? 0);

  return (
    <div>
      <div className="flex flex-col items-start justify-between gap-6 sm:flex-row">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Program #13 · public-service-data-quality
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Where OSM and official health facility registries disagree.
          </h1>
          <p className="mt-3 max-w-3xl text-ink-700 leading-relaxed">
            Compares OSM <code className="font-mono text-sm">amenity=hospital/clinic/doctors</code>{" "}
            counts against each country's official national health-facility
            registry, at ADM1. The upgrade path now tests whether Bangladesh
            can move to facility coordinates, settlement denominators, and
            road-surface context, while the Philippines starts from
            barangay/city Open Buildings denominators.
          </p>
        </div>
        <div className="shrink-0">
          <MaturityChip status="PR" />
          <p className="mt-2 max-w-[18ch] text-left text-xs text-signal-warn sm:text-right">
            Flagship paper; AI-first, human-final upgrade pending.
          </p>
        </div>
      </div>

      <section className="mt-10 border-y border-[var(--rule)] py-8">
        <div className="max-w-3xl">
          <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
            Spatial picture
          </h2>
          <p className="mt-3 text-ink-700 leading-relaxed">
            The same numbers in `results.md`, drawn on the map. Darker shading
            means OpenStreetMap captures a smaller share of the official
            health-facility registry. The Philippines map shows the 9.8×
            best-to-worst gradient between NCR and BARMM as a geographic
            pattern. The Bangladesh map shows Dhaka standing apart from the
            other seven divisions. The Philippines city/municipality poverty
            overlay uses official PSA 2023 SAE estimates plus PSA OpenSTAT
            direct-estimate cities; ten city/municipality polygons remain
            explicitly source-missing rather than imputed.
          </p>
        </div>
        <div className="mt-7 grid gap-7 lg:grid-cols-2">
          <figure className="border border-ink-200 bg-white p-3">
            <img
              src="/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm1.svg"
              alt="Philippines choropleth: OSM-to-NHFR clinical-tier ratio per ADM1 region. NCR shows the highest ratio (about 0.6); BARMM and the rural Mindanao regions show the lowest (about 0.07)."
              className="h-auto w-full"
              loading="lazy"
            />
            <figcaption className="mt-2 text-xs leading-relaxed text-ink-500">
              Philippines — OSM ÷ NHFR clinical-tier ratio per ADM1 region.
              Best: NCR 63.5%. Worst: BARMM 6.5%. 9.8× rural-urban gradient.
              17 regions; ratios from{" "}
              <code className="font-mono">public-service-data-quality-PHL.csv</code>.
            </figcaption>
          </figure>
          <figure className="border border-ink-200 bg-white p-3">
            <img
              src="/programs/public-service-data-quality/generated/charts/psdq-choropleth-bgd-adm1.svg"
              alt="Bangladesh choropleth: OSM-to-DGHS clinical-tier ratio per ADM1 division. Dhaka shows the highest ratio (about 0.20); Sylhet and Barisal show the lowest (about 0.06 to 0.08)."
              className="h-auto w-full"
              loading="lazy"
            />
            <figcaption className="mt-2 text-xs leading-relaxed text-ink-500">
              Bangladesh — OSM ÷ DGHS clinical-tier ratio per ADM1 division.
              Best: Dhaka 20.1%. Worst: Barisal 6.2%. 8 divisions; ratios from{" "}
              <code className="font-mono">public-service-data-quality-BGD.csv</code>.
            </figcaption>
          </figure>
        </div>
        <div className="mt-7">
          <figure className="border border-ink-200 bg-white p-3">
            <img
              src="/programs/public-service-data-quality/generated/charts/psdq-choropleth-phl-adm3-poverty.svg"
              alt="Philippines choropleth at city and municipality level: official 2023 poverty incidence from PSA Small Area Estimates plus PSA OpenSTAT direct estimates. Highest poverty concentrations in BARMM, the Cordillera, and parts of Eastern Visayas. Ten polygons are gray, marking explicit source-missing rows that were not imputed."
              className="h-auto w-full"
              loading="lazy"
            />
            <figcaption className="mt-2 text-xs leading-relaxed text-ink-500">
              Philippines — official 2023 poverty incidence at city/municipality
              level (PSA 2023 SAE + OpenSTAT direct). 1,632 of 1,642 ADM3
              polygons joined; 10 source-missing rows shown in gray and not
              imputed. Source:{" "}
              <code className="font-mono">psdq-phl-admin3-poverty-context.csv</code>.
            </figcaption>
          </figure>
        </div>
        <p className="mt-5 text-xs leading-relaxed text-ink-500">
          Maps are rendered by{" "}
          <code className="font-mono">public-service-data-quality/scripts/build-choropleth.py</code>
          {" "}from the same generated CSVs the working paper cites; the SVGs
          synced here are the deterministic build artifacts. Boundaries:
          PSA/NAMRIA 2023 (Philippines), geoBoundaries v6 (Bangladesh).
        </p>
      </section>

      {phlAdmin3Summary && (
        <section className="mt-10 border-y border-[var(--rule)] py-8">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="max-w-3xl">
              <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
                Granularity upgrade · Philippines city/municipality denominator
              </h2>
              <p className="mt-3 text-ink-700 leading-relaxed">
                The Philippines result now moves below ADM1. Google Open
                Buildings points are assigned to PSA/NAMRIA ADM3
                city/municipality polygons, then joined to NHFR records using
                direct boundary codes plus the PSA PSGC correspondence-code
                crosswalk where needed. Remaining code mismatches are shown as
                a data-quality finding, not filled in silently.
              </p>
            </div>
            <div className="text-right text-xs text-ink-500">
              <div>
                OSM base:{" "}
                <strong className="text-ink-900">
                  {phlAdmin3Summary.osm.timestamp_osm_base?.slice(0, 10) ?? "—"}
                </strong>
              </div>
              <div className="mt-1">
                Open Buildings tiles:{" "}
                <strong className="text-ink-900">
                  {phlAdmin3Summary.tiles.length}
                </strong>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            <ReadinessStat
              label="ADM3 units"
              value={phlAdmin3Summary.admin3_units.toLocaleString()}
              note="PSA/NAMRIA city and municipality polygons"
            />
            <ReadinessStat
              label="p85 buildings"
              value={phlAdmin3Summary.building_totals.buildings_p85.toLocaleString()}
              note={`${phlAssignedBuildings.toLocaleString()} all-confidence points assigned to ADM3`}
            />
            <ReadinessStat
              label="NHFR ADM3 match"
              value={`${(phlAdm3MatchShare * 100).toFixed(1)}%`}
              note={`${phlAdm3MatchedRecords.toLocaleString()} of ${phlAdmin3Summary.nhfr.records.toLocaleString()} active records; ${phlCrosswalkMatchedRecords.toLocaleString()} resolved after direct code match`}
            />
            <ReadinessStat
              label="OSM assigned"
              value={phlAdmin3Summary.osm.assigned_features.toLocaleString()}
              note={`${phlAdmin3Summary.osm.unassigned_features.toLocaleString()} OSM health features outside ADM3 assignment`}
            />
          </div>

          <div className="mt-7 grid gap-7 lg:grid-cols-[1.25fr_0.95fr]">
            {topPhlExposureRows.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold">
                  Top city/municipality exposure screen
                </h3>
                <div className="mt-4 space-y-3">
                  {topPhlExposureRows.map((row) => (
                    <div
                      key={row.adm3_pcode}
                      className="grid grid-cols-[minmax(0,1fr)_78px_58px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(170px,1fr)_minmax(140px,260px)_88px_76px] sm:items-center"
                    >
                      <div className="min-w-0">
                        <div className="truncate font-medium text-ink-900">
                          {row.adm3_name}
                        </div>
                        <div className="truncate text-ink-500">
                          {row.adm2_name}, {row.adm1_name} · NHFR {row.registry_clinical} / OSM {row.osm_health}
                        </div>
                      </div>
                      <div className="order-4 col-span-3 sm:order-none sm:col-span-1">
                        <ScaledBar
                          value={row.underobserved_buildings_adm3_p85_proxy}
                          max={topPhlExposureRows[0].underobserved_buildings_adm3_p85_proxy}
                        />
                      </div>
                      <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                        {row.underobserved_buildings_adm3_p85_proxy.toLocaleString()}
                      </div>
                      <div className="order-3 text-right tabular text-ink-500 sm:order-none">
                        {formatShare(row.registry_gap_share)}
                      </div>
                    </div>
                  ))}
                </div>
                <p className="mt-4 text-xs leading-relaxed text-ink-500">
                  Screen = p85 building denominator multiplied by the
                  ADM3-matched NHFR clinical gap share. It is a local
                  prioritization index, not affected population.
                </p>
              </div>
            )}

            <div>
              <h3 className="text-sm font-semibold">Boundary-code mismatch</h3>
              <div className="mt-4 border border-ink-200 bg-white p-4">
                <div className="text-2xl font-semibold tabular text-ink-900">
                  {phlAdmin3Summary.nhfr.unmatched_records.toLocaleString()}
                </div>
                <div className="mt-1 text-xs text-ink-500">
                  NHFR records remain unresolved after the direct ADM3 code
                  join and PSA PSGC correspondence-code resolver. These are
                  excluded from the city-level exposure score.
                </div>
                <div className="mt-4">
                  <ReadinessBar value={phlAdm3MatchShare * 100} />
                </div>
                <div className="mt-2 text-xs tabular text-ink-500">
                  ADM3 match share: {(phlAdm3MatchShare * 100).toFixed(1)}%
                </div>
              </div>

              {topPhlUnmatchedCodes.length > 0 && (
                <div className="mt-4 space-y-3">
                  {topPhlUnmatchedCodes.map((code) => (
                    <div
                      key={code.attempted_adm3_pcode}
                      className="grid grid-cols-[minmax(0,1fr)_76px] gap-3 text-xs sm:grid-cols-[minmax(120px,1fr)_78px_78px]"
                    >
                      <div className="min-w-0">
                        <div className="truncate font-medium text-ink-900">
                          {code.attempted_adm3_pcode}
                        </div>
                        <div className="truncate text-ink-500">
                          reg {code.top_regcodes[0]?.regcode ?? "—"} · prov {code.top_provcodes[0]?.provcode ?? "—"}
                        </div>
                      </div>
                      <div className="text-right tabular text-ink-700">
                        {code.records.toLocaleString()}
                      </div>
                      <div className="hidden text-right tabular text-ink-500 sm:block">
                        {code.clinical.toLocaleString()} clinical
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {topPhlBuildingRows.length > 0 && (
            <div className="mt-7">
              <h3 className="text-sm font-semibold">
                Largest p85 building denominators in the boundary layer
              </h3>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                {topPhlBuildingRows.map((row) => (
                  <div
                    key={`building-${row.adm3_pcode}`}
                    className="grid grid-cols-[minmax(0,1fr)_92px] gap-3 border border-ink-200 bg-white p-3 text-xs"
                  >
                    <div className="min-w-0">
                      <div className="truncate font-medium text-ink-900">
                        {row.adm3_name}
                      </div>
                      <div className="truncate text-ink-500">
                        {row.adm2_name} · ADM3-matched NHFR clinical {row.registry_clinical}
                      </div>
                    </div>
                    <div className="text-right tabular text-ink-700">
                      {row.buildings_p85.toLocaleString()}
                    </div>
                    <div className="col-span-2">
                      <ScaledBar
                        value={row.buildings_p85}
                        max={topPhlBuildingRows[0].buildings_p85}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {phlPovertySummary && (
            <div className="mt-7 border border-ink-200 bg-white p-5">
              <div className="flex flex-wrap items-start justify-between gap-5">
                <div className="max-w-3xl">
                  <h3 className="text-sm font-semibold">
                    Poverty-source overlay status
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-ink-700">
                    The owner manually downloaded the official PSA
                    city/municipality SAE workbook from the PSA page and seeded
                    the deterministic cache. The overlay now combines PSA SAE
                    city/municipality rows with PSA OpenSTAT direct-estimate
                    city/HUC rows. Remaining nonmatches stay explicitly marked
                    as missing.
                  </p>
                </div>
                <div className="text-left text-xs text-ink-500 sm:text-right">
                  <div>Status</div>
                  <div className="mt-1 font-mono text-ink-900">
                    {phlPovertySummary.status}
                  </div>
                  <div className="mt-2">
                    Generated {phlPovertySummary.generated_at.slice(0, 10)}
                  </div>
                </div>
              </div>

              <div className="mt-5 grid gap-3 md:grid-cols-4">
                <ReadinessStat
                  label="ADM3 rows"
                  value={phlPovertySummary.admin3_rows.toLocaleString()}
                  note="Rows in the Philippines city/municipality context table"
                />
                <ReadinessStat
                  label="Poverty joined"
                  value={phlPovertySummary.rows_with_poverty.toLocaleString()}
                  note={`${phlPovertySummary.rows_with_sae_poverty.toLocaleString()} SAE + ${phlPovertySummary.rows_with_openstat_direct_poverty.toLocaleString()} OpenSTAT`}
                />
                <ReadinessStat
                  label="SAE rows"
                  value={phlPovertySummary.rows_with_sae_poverty.toLocaleString()}
                  note={phlPovertySummary.sources.psa_sae_cached ? "PSA SAE cache present" : "PSA SAE attachment not cached"}
                />
                <ReadinessStat
                  label="Still missing"
                  value={phlPovertySummary.rows_without_poverty.toLocaleString()}
                  note="No poverty value is imputed from buildings or registry gaps"
                />
              </div>

              {topPhlPovertyRows.length > 0 && (
                <div className="mt-6">
                  <h4 className="text-xs uppercase tracking-[0.18em] text-ink-500">
                    Top rows by poverty-context screen
                  </h4>
                  <div className="mt-4 space-y-3">
                    {topPhlPovertyRows.map((row) => (
                      <div
                        key={`poverty-${row.adm3_pcode}`}
                        className="grid grid-cols-[minmax(0,1fr)_70px_76px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(170px,1fr)_minmax(130px,240px)_74px_86px] sm:items-center"
                      >
                        <div className="min-w-0">
                          <div className="truncate font-medium text-ink-900">
                            {row.adm3_name}
                          </div>
                          <div className="truncate text-ink-500">
                            {row.adm2_name}, {row.adm1_name}
                          </div>
                        </div>
                        <div className="order-4 col-span-3 sm:order-none sm:col-span-1">
                          <ScaledBar
                            value={row.gap_poverty_context_p85_proxy}
                            max={topPhlPovertyRows[0].gap_poverty_context_p85_proxy}
                          />
                        </div>
                        <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                          {row.poverty_incidence_2023.toFixed(1).replace(/\.0$/, "")}%
                        </div>
                        <div className="order-3 text-right tabular text-ink-500 sm:order-none">
                          {row.gap_poverty_context_p85_proxy.toLocaleString()}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <p className="mt-5 text-xs leading-relaxed text-ink-500">
                Source note: PSA Small Area Estimates page and PSA OpenSTAT
                Table 2a. {phlPovertySummary.non_claim}
              </p>
            </div>
          )}

          <div className="mt-5 text-xs text-ink-500">
            Source note: DOH NHFR cached v_activefacilities endpoint,
            PSA PSGC correspondence tables, OpenStreetMap Overpass,
            HDX/OCHA Philippines PSA/NAMRIA ADM3, and Google Open Buildings
            V3. {phlAdmin3Summary.non_claim}
          </div>
        </section>
      )}

      {bgdFacilitySummary && (
        <section className="mt-10 border-y border-[var(--rule)] py-8">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="max-w-3xl">
              <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
                Granularity upgrade · Bangladesh coordinate readiness
              </h2>
              <p className="mt-3 text-ink-700 leading-relaxed">
                The richer DGHS public facilities endpoint is now being tested
                as the bridge from ADM1 disagreement to facility-level
                catchments. This is still a readiness layer, not an access or
                service-availability result.
              </p>
            </div>
            <div className="text-right text-xs text-ink-500">
              <div>
                Pages cached:{" "}
                <strong className="text-ink-900">
                  {bgdFacilitySummary.cache.pages_cached.length}
                  {bgdFacilitySummary.cache.last_page
                    ? ` / ${bgdFacilitySummary.cache.last_page}`
                    : ""}
                </strong>
              </div>
              <div className="mt-1">
                Endpoint total:{" "}
                <strong className="text-ink-900">
                  {bgdFacilitySummary.cache.total_reported?.toLocaleString() ?? "—"}
                </strong>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            <ReadinessStat
              label="Facility records parsed"
              value={bgdFacilitySummary.records.toLocaleString()}
              note="Deduplicated by DGHS facility id"
            />
            <ReadinessStat
              label="Valid coordinates"
              value={`${bgdFacilitySummary.coordinate_coverage_pct.toFixed(1)}%`}
              note={`${bgdFacilitySummary.valid_coordinate_records.toLocaleString()} records pass Bangladesh lat/lon bounds`}
            />
            <ReadinessStat
              label="Catchment field"
              value={`${bgdFacilitySummary.catchment_coverage_pct.toFixed(1)}%`}
              note={`${bgdFacilitySummary.catchment_records.toLocaleString()} records have at least one catchment code`}
            />
            <ReadinessStat
              label="Admin units"
              value={bgdFacilitySummary.admin_units.toLocaleString()}
              note="Division / district / upazila rows in chart extract"
            />
          </div>

          <div className="mt-7 grid gap-6 lg:grid-cols-[1fr_1.2fr]">
            <div>
              <h3 className="text-sm font-semibold">Coverage meters</h3>
              <div className="mt-4 space-y-4">
                <ReadinessMeter
                  label="Coordinate coverage"
                  value={bgdFacilitySummary.coordinate_coverage_pct}
                />
                <ReadinessMeter
                  label="Catchment-field coverage"
                  value={bgdFacilitySummary.catchment_coverage_pct}
                />
              </div>
              <p className="mt-4 text-xs leading-relaxed text-ink-500">
                Next computed chart: Open Buildings inside validated facility
                buffers. This panel only says whether the facility points are
                usable enough to attempt that join.
              </p>
            </div>

            {lowCoordinateAdmin.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold">
                  Lowest coordinate coverage among named upazilas
                </h3>
                <div className="mt-4 space-y-3">
                  {lowCoordinateAdmin.map((row) => (
                    <div
                      key={`${row.division_name}-${row.district_name}-${row.upazila_name}`}
                      className="grid grid-cols-[minmax(0,1fr)_64px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(130px,1fr)_minmax(140px,220px)_70px] sm:items-center"
                    >
                      <div className="min-w-0">
                        <div className="truncate font-medium text-ink-900">
                          {row.upazila_name || "Unspecified upazila"}
                        </div>
                        <div className="truncate text-ink-500">
                          {row.district_name}, {row.division_name} · {row.facilities} facilities
                        </div>
                      </div>
                      <div className="order-3 col-span-2 sm:order-none sm:col-span-1">
                        <ReadinessBar value={row.coordinate_coverage_pct} />
                      </div>
                      <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                        {row.coordinate_coverage_pct.toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="mt-5 text-xs text-ink-500">
            Source note: DGHS public facilities JSON endpoint; generated by
            {" "}
            <code className="font-mono">build-bgd-facility-extract.py</code>
            .
            Coordinates are screened against Bangladesh bounds only. This is
            not a population, poverty, Open Buildings, or travel-time measure.
          </div>
        </section>
      )}

      {openBuildingsSummary && (
        <section className="mt-10 border-y border-[var(--rule)] py-8">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="max-w-3xl">
              <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
                Settlement denominator · Open Buildings nearest-facility buffers
              </h2>
              <p className="mt-3 text-ink-700 leading-relaxed">
                Google Open Buildings points inside Bangladesh are assigned to
                the nearest coordinate-ready DGHS facility, then counted inside
                1 km, 3 km, and 5 km bands. The p85/p90 series apply the
                tile-specific Google precision thresholds, so the chart shows
                denominator sensitivity instead of a single fragile number.
              </p>
            </div>
            <div className="text-right text-xs text-ink-500">
              <div>
                Tiles processed:{" "}
                <strong className="text-ink-900">
                  {openBuildingsSummary.tiles.length}
                </strong>
              </div>
              <div className="mt-1">
                Inside Bangladesh:{" "}
                <strong className="text-ink-900">
                  {openBuildingsInside.toLocaleString()}
                </strong>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            <ReadinessStat
              label="Coordinate facilities"
              value={openBuildingsSummary.facilities.toLocaleString()}
              note="DGHS facilities eligible for nearest-building assignment"
            />
            <ReadinessStat
              label="3 km p85 buildings"
              value={openBuildingsSummary.totals.buildings_nearest_3km_p85.toLocaleString()}
              note="Nearest-facility settlement denominator at 85% precision threshold"
            />
            <ReadinessStat
              label="5 km p85 buildings"
              value={openBuildingsSummary.totals.buildings_nearest_5km_p85.toLocaleString()}
              note="Wider buffer sensitivity using the same threshold"
            />
            <ReadinessStat
              label="3 km p90 buildings"
              value={openBuildingsSummary.totals.buildings_nearest_3km_p90.toLocaleString()}
              note="Conservative high-precision sensitivity check"
            />
          </div>

          <div className="mt-7 grid gap-7 lg:grid-cols-[1fr_1.1fr]">
            <div>
              <h3 className="text-sm font-semibold">Radius and confidence sensitivity</h3>
              <ExposureBars summary={openBuildingsSummary} />
              <p className="mt-4 text-xs leading-relaxed text-ink-500">
                Counts are nearest-facility assignments, so a building is not
                double-counted when buffers overlap.
              </p>
            </div>

            {topOpenBuildingsAdmin.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold">
                  Top upazilas by 3 km p85 building denominator
                </h3>
                <div className="mt-4 space-y-3">
                  {topOpenBuildingsAdmin.map((row) => (
                    <div
                      key={`${row.division_name}-${row.district_name}-${row.upazila_name}`}
                      className="grid grid-cols-[minmax(0,1fr)_86px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(150px,1fr)_minmax(140px,240px)_90px] sm:items-center"
                    >
                      <div className="min-w-0">
                        <div className="truncate font-medium text-ink-900">
                          {row.upazila_name}
                        </div>
                        <div className="truncate text-ink-500">
                          {row.district_name}, {row.division_name} · {row.coordinate_facilities} facilities
                        </div>
                      </div>
                      <div className="order-3 col-span-2 sm:order-none sm:col-span-1">
                        <ScaledBar
                          value={row.buildings_nearest_3km_p85}
                          max={topOpenBuildingsAdmin[0].buildings_nearest_3km_p85}
                        />
                      </div>
                      <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                        {row.buildings_nearest_3km_p85.toLocaleString()}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="mt-7 overflow-x-auto border border-ink-200 bg-white">
            <table className="data-table tabular w-full text-xs">
              <thead>
                <tr className="text-left">
                  <th>Open Buildings tile</th>
                  <th className="text-right">Rows processed</th>
                  <th className="text-right">Inside Bangladesh</th>
                  <th className="text-right">Within 5 km</th>
                  <th className="text-right">p85 threshold</th>
                  <th className="text-right">p90 threshold</th>
                </tr>
              </thead>
              <tbody>
                {openBuildingsSummary.tiles.map((tile) => (
                  <tr key={tile.tile_id}>
                    <td>{tile.tile_id}</td>
                    <td className="text-right">{tile.rows_processed.toLocaleString()}</td>
                    <td className="text-right">{tile.inside_bangladesh.toLocaleString()}</td>
                    <td className="text-right">{tile.assigned_within_5km.toLocaleString()}</td>
                    <td className="text-right">
                      {tile.confidence_threshold_85_precision?.toFixed(3) ?? "—"}
                    </td>
                    <td className="text-right">
                      {tile.confidence_threshold_90_precision?.toFixed(3) ?? "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-5 text-xs text-ink-500">
            Source note: Google Open Buildings V3 point CSVs, Google
            tile-specific precision thresholds, geoBoundaries Bangladesh ADM0,
            and DGHS public facilities JSON endpoint. {openBuildingsSummary.non_claim}
          </div>
        </section>
      )}

      {exposureGapSummary && (
        <section className="mt-10 border-y border-[var(--rule)] py-8">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="max-w-3xl">
              <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
                Exposure-ranked gap · registry-map under-observability
              </h2>
              <p className="mt-3 text-ink-700 leading-relaxed">
                This joins OSM health features assigned to geoBoundaries
                upazilas with DGHS active clinical facilities and the Open
                Buildings 3 km p85 denominator. The ranking asks where a
                registry-map mismatch is paired with the largest settlement
                denominator.
              </p>
            </div>
            <div className="text-right text-xs text-ink-500">
              <div>
                OSM assigned:{" "}
                <strong className="text-ink-900">
                  {exposureGapSummary.osm.assigned_features.toLocaleString()}
                </strong>
              </div>
              <div className="mt-1">
                Joined to DGHS:{" "}
                <strong className="text-ink-900">
                  {exposureGapSummary.exposure.matched_osm_features.toLocaleString()}
                </strong>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            <ReadinessStat
              label="Upazila rows"
              value={exposureGapSummary.exposure.registry_admin_rows.toLocaleString()}
              note={`${exposureGapSummary.exposure.rows_with_open_buildings_denominator.toLocaleString()} have an Open Buildings denominator`}
            />
            <ReadinessStat
              label="Active clinical registry"
              value={exposureGapSummary.exposure.active_clinical_facilities.toLocaleString()}
              note="DGHS active clinical-tier records in the upazila join"
            />
            <ReadinessStat
              label="OSM health joined"
              value={exposureGapSummary.exposure.osm_health_joined.toLocaleString()}
              note={`${exposureGapSummary.exposure.osm_features_not_joined_to_registry.toLocaleString()} assigned OSM features remain unmatched to DGHS units`}
            />
            <ReadinessStat
              label="Gap-weighted buildings"
              value={exposureGapSummary.exposure.underobserved_buildings_3km_p85_proxy.toLocaleString()}
              note="3 km p85 denominator multiplied by registry-minus-OSM gap share"
            />
          </div>

          {topExposureGapRows.length > 0 && (
            <div className="mt-7">
              <h3 className="text-sm font-semibold">
                Top upazilas by gap-weighted 3 km p85 denominator
              </h3>
              <div className="mt-4 space-y-3">
                {topExposureGapRows.map((row) => (
                  <div
                    key={`${row.division_name}-${row.district_name}-${row.upazila_name}`}
                    className="grid grid-cols-[minmax(0,1fr)_78px_58px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(150px,1fr)_minmax(130px,220px)_88px_88px] sm:items-center"
                  >
                    <div className="min-w-0">
                      <div className="truncate font-medium text-ink-900">
                        {row.upazila_name}
                      </div>
                      <div className="truncate text-ink-500">
                        {row.district_name}, {row.division_name} · DGHS {row.active_clinical_facilities} / OSM {row.osm_health}
                      </div>
                    </div>
                    <div className="order-4 col-span-3 sm:order-none sm:col-span-1">
                      <ScaledBar
                        value={row.underobserved_buildings_3km_p85_proxy}
                        max={topExposureGapRows[0].underobserved_buildings_3km_p85_proxy}
                      />
                    </div>
                    <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                      {row.underobserved_buildings_3km_p85_proxy.toLocaleString()}
                    </div>
                    <div className="order-3 text-right tabular text-ink-500 sm:order-none">
                      {(row.registry_gap_share * 100).toFixed(0)}% gap
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="mt-5 text-xs text-ink-500">
            Source note: OpenStreetMap Overpass, geoBoundaries BGD ADM3,
            DGHS public facilities JSON endpoint, and Google Open Buildings
            V3. {exposureGapSummary.non_claim}
          </div>
        </section>
      )}

      {roadSurfaceSummary && exposureRoadSummary && (
        <section className="mt-10 border-y border-[var(--rule)] py-8">
          <div className="flex flex-wrap items-start justify-between gap-6">
            <div className="max-w-3xl">
              <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">
                Road-quality context · surface mix and service-gap triage
              </h2>
              <p className="mt-3 text-ink-700 leading-relaxed">
                The exposure-ranked health-facility gap is now joined to a
                Bangladesh road-surface layer from HeiGIT/HDX. The road file
                combines OSM road geometry with Mapillary-derived
                deep-learning paved/unpaved labels. The score is a triage
                screen: it keeps road-surface coverage thresholds visible and
                does not claim travel time, poverty, or service-access impact.
              </p>
            </div>
            <div className="text-right text-xs text-ink-500">
              <div>
                Assigned road features:{" "}
                <strong className="text-ink-900">
                  {roadSurfaceSummary.stats.assigned_features.toLocaleString()}
                </strong>
              </div>
              <div className="mt-1">
                Eligible exposure rows:{" "}
                <strong className="text-ink-900">
                  {exposureRoadSummary.stats.rows_with_surface_context.toLocaleString()}
                </strong>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-4">
            <ReadinessStat
              label="Mapped road length"
              value={`${formatKm(roadSurfaceSummary.stats.total_road_km)} km`}
              note="OSM-length sum after assigning road segments to ADM3"
            />
            <ReadinessStat
              label="Surface-classified"
              value={`${formatKm(roadSurfaceSummary.stats.classified_surface_km)} km`}
              note={`${formatShare(roadSurfaceSummary.stats.classified_surface_share)} of assigned mapped road length`}
            />
            <ReadinessStat
              label="Classified unpaved"
              value={`${formatKm(roadSurfaceSummary.stats.unpaved_km)} km`}
              note={`${formatShare(roadSurfaceSummary.stats.classified_unpaved_share)} of classified surface length`}
            />
            <ReadinessStat
              label="Scored rows"
              value={exposureRoadSummary.stats.rows_with_surface_context.toLocaleString()}
              note={`Requires >= ${exposureRoadSummary.stats.min_classified_surface_km_for_score.toFixed(0)} km classified and >= ${formatShare(exposureRoadSummary.stats.min_classified_surface_share_for_score)} coverage`}
            />
          </div>

          <div className="mt-7 grid gap-7 lg:grid-cols-[0.95fr_1.25fr]">
            <div>
              <h3 className="text-sm font-semibold">Classified surface mix</h3>
              <SurfaceMixStack summary={roadSurfaceSummary} />
              {topUnpavedRoadRows.length > 0 && (
                <div className="mt-5">
                  <h3 className="text-sm font-semibold">
                    Upazilas with the most classified unpaved road length
                  </h3>
                  <div className="mt-4 space-y-3">
                    {topUnpavedRoadRows.map((row) => (
                      <div
                        key={row.join_key}
                        className="grid grid-cols-[minmax(0,1fr)_72px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(130px,1fr)_minmax(120px,210px)_78px] sm:items-center"
                      >
                        <div className="min-w-0">
                          <div className="truncate font-medium text-ink-900">
                            {row.upazila_name}
                          </div>
                          <div className="truncate text-ink-500">
                            {row.district_name}, {row.division_name} · {formatShare(row.classified_unpaved_share)} unpaved
                          </div>
                        </div>
                        <div className="order-3 col-span-2 sm:order-none sm:col-span-1">
                          <ScaledBar
                            value={row.unpaved_km}
                            max={topUnpavedRoadRows[0].unpaved_km}
                          />
                        </div>
                        <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                          {formatKm(row.unpaved_km)} km
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {topRoadContextRows.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold">
                  Service-gap rows with road-surface context
                </h3>
                <div className="mt-4 space-y-3">
                  {topRoadContextRows.map((row) => (
                    <div
                      key={`${row.division_name}-${row.district_name}-${row.upazila_name}`}
                      className="grid grid-cols-[minmax(0,1fr)_78px_58px] gap-x-3 gap-y-2 text-xs sm:grid-cols-[minmax(150px,1fr)_minmax(130px,230px)_86px_86px] sm:items-center"
                    >
                      <div className="min-w-0">
                        <div className="truncate font-medium text-ink-900">
                          {row.upazila_name}
                        </div>
                        <div className="truncate text-ink-500">
                          {row.district_name}, {row.division_name} · {formatShare(row.classified_unpaved_share)} classified unpaved
                        </div>
                      </div>
                      <div className="order-4 col-span-3 sm:order-none sm:col-span-1">
                        <ScaledBar
                          value={toNumber(row.road_context_score)}
                          max={toNumber(topRoadContextRows[0].road_context_score)}
                        />
                      </div>
                      <div className="order-2 text-right tabular text-ink-700 sm:order-none">
                        {toNumber(row.road_context_score).toLocaleString()}
                      </div>
                      <div className="order-3 text-right tabular text-ink-500 sm:order-none">
                        {formatKm(toNumber(row.classified_surface_km))} km
                      </div>
                    </div>
                  ))}
                </div>
                <p className="mt-4 text-xs leading-relaxed text-ink-500">
                  Road-context score = gap-weighted 3 km p85 buildings times
                  one plus classified unpaved share. It appears only where the
                  road-surface classified subset passes the coverage gates.
                </p>
              </div>
            )}
          </div>

          <div className="mt-5 text-xs text-ink-500">
            Source note: HeiGIT Bangladesh Road Surface Data via HDX,
            OpenStreetMap, Mapillary-derived deep-learning classification,
            geoBoundaries BGD ADM3, DGHS public facilities, OSM Overpass, and
            Google Open Buildings V3. {roadSurfaceSummary.non_claim}{" "}
            {exposureRoadSummary.non_claim}
          </div>
        </section>
      )}

      {/* Country selector + summary */}
      {summary && (
        <section className="mt-10">
          <h2 className="text-xs uppercase tracking-[0.2em] text-ink-500">Countries</h2>
          <div className="mt-3 flex flex-wrap gap-3">
            {summary.countries.map((c) => (
              <button
                key={c.iso3}
                onClick={() => setSelected(c.iso3)}
                className={
                  "text-left bg-white border rounded-md px-4 py-3 min-w-[240px] transition " +
                  (selected === c.iso3
                    ? "border-ink-900 shadow-sm"
                    : "border-ink-200 hover:border-ink-500")
                }
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs uppercase tracking-wider text-ink-500">
                    {c.iso3}
                  </span>
                  <span className="text-xs text-ink-500 tabular">
                    {c.num_admin1} ADM1
                  </span>
                </div>
                <div className="mt-1 font-semibold">{c.country}</div>
                <div className="mt-2 text-sm tabular">
                  OSM/clinical ={" "}
                  <strong>{(c.totals.ratio_osm_to_clinical * 100).toFixed(1)}%</strong>
                </div>
                <div className="text-xs text-ink-500 mt-1">
                  {(c.admin1_min_ratio_clinical * 100).toFixed(1)}% ({c.worst_admin1}) →{" "}
                  {(c.admin1_max_ratio_clinical * 100).toFixed(1)}% ({c.best_admin1})
                </div>
              </button>
            ))}
          </div>
        </section>
      )}

      {/* Per-country breakdown */}
      {current && (
        <section className="mt-10">
          <div className="flex items-baseline justify-between flex-wrap gap-3">
            <h2 className="text-xl font-semibold">
              {current.country} ({current.iso3}) — ADM1 breakdown
            </h2>
            <div className="flex items-center gap-3 text-sm">
              <span className="text-ink-500">Metric tier:</span>
              {(["principal", "clinical", "all"] as const).map((m) => (
                <button
                  key={m}
                  onClick={() => setMetric(m)}
                  className={
                    "px-3 py-1 rounded border transition " +
                    (metric === m
                      ? "bg-ink-900 text-ink-50 border-ink-900"
                      : "bg-white text-ink-700 border-ink-200 hover:border-ink-500")
                  }
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-3 text-sm text-ink-700 max-w-3xl">
            <span className="font-semibold">Principal:</span> hospitals + main
            clinics + RHUs + city/municipal health offices.{" "}
            <span className="font-semibold">Clinical:</span> adds barangay /
            community / union health stations + dialysis + social-hygiene.{" "}
            <span className="font-semibold">All:</span> every active registry
            row including diagnostic labs, dental, drug-testing, warehouses.
          </div>

          <div className="mt-6 bg-white border border-ink-200 rounded-md overflow-x-auto">
            <table className="data-table tabular w-full text-sm">
              <thead>
                <tr className="text-left">
                  <th>ADM1</th>
                  <th>Region</th>
                  <th className="text-right">Population 2020</th>
                  <th className="text-right">OSM</th>
                  <th className="text-right">Reg principal</th>
                  <th className="text-right">Reg clinical</th>
                  <th className="text-right">Reg all</th>
                  <th className="text-right">OSM / reg</th>
                </tr>
              </thead>
              <tbody>
                {ranked.map((row) => {
                  const ratio = row[`ratio_osm_to_${metric}` as keyof Row] as number | null;
                  const bucket = heatBucket(ratio);
                  return (
                    <tr key={row.admin1_code}>
                      <td>{row.admin1_code}</td>
                      <td>{row.admin1_name}</td>
                      <td className="text-right">
                        {row.population_2020.toLocaleString()}
                      </td>
                      <td className="text-right">{row.osm_health.toLocaleString()}</td>
                      <td className="text-right">
                        {row.registry_principal.toLocaleString()}
                      </td>
                      <td className="text-right">
                        {row.registry_clinical.toLocaleString()}
                      </td>
                      <td className="text-right">
                        {row.registry_all.toLocaleString()}
                      </td>
                      <td className={`text-right font-semibold heat-${bucket}`}>
                        {ratio !== null ? (ratio * 100).toFixed(1) + "%" : "—"}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
              <tfoot>
                <tr className="font-semibold bg-ink-100">
                  <td colSpan={2}>TOTAL</td>
                  <td className="text-right">
                    {current.rows
                      .reduce((s, r) => s + r.population_2020, 0)
                      .toLocaleString()}
                  </td>
                  <td className="text-right">
                    {current.totals.osm_health.toLocaleString()}
                  </td>
                  <td className="text-right">
                    {current.totals.registry_principal.toLocaleString()}
                  </td>
                  <td className="text-right">
                    {current.totals.registry_clinical.toLocaleString()}
                  </td>
                  <td className="text-right">
                    {current.totals.registry_all.toLocaleString()}
                  </td>
                  <td className="text-right">
                    {(
                      (current.totals[`ratio_osm_to_${metric}` as keyof CountryPayload["totals"]] as number) * 100
                    ).toFixed(1)}
                    %
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>

          <div className="mt-3 text-xs text-ink-500">
            Ranked worst → best on the "OSM / reg" column. Color intensity
            maps the ratio into quintiles (darker = better coverage).
          </div>

          <div className="mt-6 grid md:grid-cols-2 gap-4">
            <div className="bg-white border border-ink-200 rounded-md p-4 text-sm">
              <div className="font-semibold mb-2">Source — registry</div>
              <div className="text-ink-700">{current.source.name}</div>
              <div className="mt-1 text-xs text-ink-500 break-all">
                API: <code className="font-mono">{current.source.api}</code>
              </div>
              <div className="mt-1 text-xs text-ink-500">
                Access model: <strong>{current.source.access_model}</strong>
              </div>
              <div className="mt-1 text-xs text-ink-500">
                License: {current.source.license}
              </div>
              <div className="mt-1 text-xs text-ink-500">
                Retrieved: {current.source.retrieved_at} · {current.source.total_active.toLocaleString()}{" "}
                active facilities across {current.source.pages} pages.
              </div>
            </div>
            <div className="bg-white border border-ink-200 rounded-md p-4 text-sm">
              <div className="font-semibold mb-2">Source — OSM</div>
              <div className="text-ink-700">
                OpenStreetMap Overpass, <code className="font-mono">amenity=hospital/clinic/doctors</code> queried by ISO 3166-2 admin-area.
              </div>
              <div className="mt-1 text-xs text-ink-500">
                Reused from <code className="font-mono">luminosity-gap</code> access-services pipeline cache.
              </div>
              <div className="mt-1 text-xs text-ink-500">License: ODbL (OpenStreetMap contributors)</div>
              <div className="mt-1 text-xs text-ink-500">
                Vintage per row; see <code className="font-mono">osm_timestamp</code> field in the generated JSON.
              </div>
            </div>
          </div>
        </section>
      )}

      <section className="mt-12 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">What the number means</h2>
        <p className="mt-2 text-ink-700 leading-relaxed">
          OSM ÷ official-registry is a <strong>measurement-gap ratio</strong>,
          not a country quality ranking (Constitution §13.3 §14). A low
          ratio means OSM under-represents the registry; we cannot
          conclude without triangulation that the registry is closer to
          ground truth. The sign of the disagreement and its correlation
          with rural/urban structure <em>is</em> policy-relevant: it tells
          you whether a map-based survey will systematically miss people
          in rural / low-HDI admin units.
        </p>
      </section>

      <section className="mt-10 bg-white border border-ink-200 rounded-md p-6">
        <h2 className="text-lg font-semibold">Reproduce</h2>
        <p className="mt-2 text-sm text-ink-700">
          From the repository root:
        </p>
        <pre className="mt-3 bg-ink-900 text-ink-50 rounded-md p-4 text-xs overflow-x-auto font-mono">
{`# Re-fetch registries (polite cadence; uses committed cache by default):
bash public-service-data-quality/scripts/fetch-nhfr.sh            # PHL, ~90 seconds
# BGD uses the same pattern; see process-multi-country.py for both.

# Re-compute disagreement metric:
python public-service-data-quality/scripts/process-multi-country.py
python public-service-data-quality/scripts/build-bgd-facility-extract.py
python public-service-data-quality/scripts/prepare-bgd-open-buildings-manifest.py
python public-service-data-quality/scripts/download-bgd-open-buildings-points.py
python public-service-data-quality/scripts/compute-bgd-open-buildings-facility-buffers.py --chunk-size 500000 --workers 4
python public-service-data-quality/scripts/build-bgd-exposure-ranked-disagreement.py
python public-service-data-quality/scripts/build-bgd-road-surface-context.py --skip-download
python public-service-data-quality/scripts/prepare-phl-open-buildings-manifest.py
python public-service-data-quality/scripts/download-phl-open-buildings-points.py
python public-service-data-quality/scripts/build-phl-admin3-open-buildings-context.py --chunk-size 500000 --workers 4
python public-service-data-quality/scripts/fetch-phl-sae-poverty.py
python public-service-data-quality/scripts/build-phl-admin3-poverty-context.py

# Outputs:
#   public-service-data-quality/generated/public-service-data-quality-PHL.{json,csv}
#   public-service-data-quality/generated/public-service-data-quality-BGD.{json,csv}
#   public-service-data-quality/generated/public-service-data-quality-summary.json
#   public-service-data-quality/generated/psdq-bgd-*.{json,csv}
#   public-service-data-quality/generated/psdq-phl-*.{json,csv}`}
        </pre>
      </section>
    </div>
  );
}

function heatBucket(ratio: number | null) {
  if (ratio === null) return 0;
  if (ratio < 0.08) return 1;
  if (ratio < 0.12) return 2;
  if (ratio < 0.20) return 3;
  if (ratio < 0.40) return 4;
  return 5;
}

function toNumber(value: number | string | null | undefined) {
  if (typeof value === "number") return Number.isFinite(value) ? value : 0;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatShare(value: number | null | undefined) {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return `${(value * 100).toFixed(value < 0.1 ? 1 : 0)}%`;
}

function formatKm(value: number) {
  return value.toLocaleString(undefined, { maximumFractionDigits: 1 });
}

function ReadinessStat({
  label,
  value,
  note,
}: {
  label: string;
  value: string;
  note: string;
}) {
  return (
    <div className="border border-ink-200 bg-white p-4">
      <div className="text-xs uppercase tracking-[0.16em] text-ink-500">
        {label}
      </div>
      <div className="mt-3 text-2xl font-semibold tabular text-ink-900">
        {value}
      </div>
      <div className="mt-2 text-xs leading-snug text-ink-500">{note}</div>
    </div>
  );
}

function ReadinessMeter({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between gap-4 text-xs">
        <span className="font-medium text-ink-900">{label}</span>
        <span className="tabular text-ink-500">{value.toFixed(1)}%</span>
      </div>
      <ReadinessBar value={value} />
    </div>
  );
}

function ReadinessBar({ value }: { value: number }) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className="h-2 w-full border border-ink-200 bg-ink-100">
      <div
        className="h-full bg-ink-900"
        style={{ width: `${clamped}%` }}
        aria-hidden
      />
    </div>
  );
}

function ExposureBars({ summary }: { summary: OpenBuildingsBufferSummary }) {
  const rows = [
    {
      label: "All confidences",
      values: [
        summary.totals.buildings_nearest_1km_all,
        summary.totals.buildings_nearest_3km_all,
        summary.totals.buildings_nearest_5km_all,
      ],
    },
    {
      label: "p85 precision",
      values: [
        summary.totals.buildings_nearest_1km_p85,
        summary.totals.buildings_nearest_3km_p85,
        summary.totals.buildings_nearest_5km_p85,
      ],
    },
    {
      label: "p90 precision",
      values: [
        summary.totals.buildings_nearest_1km_p90,
        summary.totals.buildings_nearest_3km_p90,
        summary.totals.buildings_nearest_5km_p90,
      ],
    },
  ];
  const max = Math.max(...rows.flatMap((row) => row.values));

  return (
    <div className="mt-4 space-y-4">
      {rows.map((row) => (
        <div key={row.label}>
          <div className="mb-2 text-xs font-medium text-ink-900">{row.label}</div>
          <div className="grid grid-cols-3 gap-3">
            {row.values.map((value, idx) => (
              <div key={`${row.label}-${idx}`}>
                <div className="mb-1 flex items-center justify-between gap-2 text-[11px] text-ink-500">
                  <span>{[1, 3, 5][idx]} km</span>
                  <span className="tabular">{value.toLocaleString()}</span>
                </div>
                <ScaledBar value={value} max={max} />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function ScaledBar({ value, max }: { value: number; max: number }) {
  const width = max > 0 ? Math.max(1, Math.min(100, (value / max) * 100)) : 0;
  return (
    <div className="h-2 w-full border border-ink-200 bg-ink-100">
      <div
        className="h-full bg-ink-900"
        style={{ width: `${width}%` }}
        aria-hidden
      />
    </div>
  );
}

function SurfaceMixStack({ summary }: { summary: RoadSurfaceSummary }) {
  const total = Math.max(summary.stats.classified_surface_km, 1);
  const pavedWidth = Math.max(0, Math.min(100, (summary.stats.paved_km / total) * 100));
  const unpavedWidth = Math.max(0, Math.min(100, (summary.stats.unpaved_km / total) * 100));

  return (
    <div className="mt-4">
      <div className="h-6 w-full overflow-hidden border border-ink-200 bg-ink-100">
        <div
          className="inline-block h-full bg-ink-900 align-top"
          style={{ width: `${pavedWidth}%` }}
          aria-hidden
        />
        <div
          className="inline-block h-full bg-signal-warn align-top"
          style={{ width: `${unpavedWidth}%` }}
          aria-hidden
        />
      </div>
      <div className="mt-3 grid grid-cols-2 gap-3 text-xs">
        <div className="border border-ink-200 bg-white p-3">
          <div className="flex items-center gap-2 text-ink-500">
            <span className="h-2 w-2 bg-ink-900" aria-hidden />
            Classified paved
          </div>
          <div className="mt-2 text-lg font-semibold tabular text-ink-900">
            {formatKm(summary.stats.paved_km)} km
          </div>
          <div className="mt-1 text-ink-500">
            {formatShare(summary.stats.classified_paved_share)}
          </div>
        </div>
        <div className="border border-ink-200 bg-white p-3">
          <div className="flex items-center gap-2 text-ink-500">
            <span className="h-2 w-2 bg-signal-warn" aria-hidden />
            Classified unpaved
          </div>
          <div className="mt-2 text-lg font-semibold tabular text-ink-900">
            {formatKm(summary.stats.unpaved_km)} km
          </div>
          <div className="mt-1 text-ink-500">
            {formatShare(summary.stats.classified_unpaved_share)}
          </div>
        </div>
      </div>
      <p className="mt-4 text-xs leading-relaxed text-ink-500">
        The remaining {formatKm(summary.stats.unknown_surface_km)} km
        are mapped roads without a paved/unpaved surface class in this source.
      </p>
    </div>
  );
}
