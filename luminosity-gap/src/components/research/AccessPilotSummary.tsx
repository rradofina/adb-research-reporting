"use client";

import accessData from "@/data/generated/access-services-pilots.json";
import adminData from "@/data/generated/access-services-admin1.json";
import computedData from "@/data/generated/access-services-computed-admin1.json";
import frontierData from "@/data/generated/access-services-frontier-admin1.json";
import nextWaveData from "@/data/generated/access-services-nextwave-admin1.json";
import scaleoutData from "@/data/generated/access-services-adb-scaleout.json";
import { useState } from "react";

type ComputedCountry =
  | (typeof accessData.countries)[number]
  | (typeof nextWaveData.countries)[number]
  | (typeof frontierData.countries)[number];
type ComputedAdminUnit = (typeof computedData.admin1)[number];
type ScaleoutEconomy = (typeof scaleoutData.economies)[number];
type PressureLens =
  | "All"
  | "Health load"
  | "School load"
  | "Market load"
  | "Climate stress"
  | "OSM risk";

const PRESSURE_LENSES: {
  value: PressureLens;
  shortLabel: string;
  description: string;
}[] = [
  {
    value: "All",
    shortLabel: "All",
    description: "Every computed ADM1 row.",
  },
  {
    value: "Health load",
    shortLabel: "Health",
    description: "ADM1 rows where health-facility load is the strongest service gap.",
  },
  {
    value: "School load",
    shortLabel: "School",
    description: "ADM1 rows where school load is the strongest service gap.",
  },
  {
    value: "Market load",
    shortLabel: "Market",
    description: "ADM1 rows where market access load is the strongest service gap.",
  },
  {
    value: "Climate stress",
    shortLabel: "Climate",
    description: "Rows flagged by heat/rainfall bottlenecks or upper-quartile climate change.",
  },
  {
    value: "OSM risk",
    shortLabel: "OSM risk",
    description: "Rows in the upper quartile of OSM completeness-risk scores.",
  },
];

function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 0,
  }).format(value);
}

function formatCompact(value: number): string {
  return new Intl.NumberFormat("en-US", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

function riskColor(index: number): string {
  if (index >= 65) return "#f43f5e";
  if (index >= 45) return "#f59e0b";
  return "#22c55e";
}

function percentile(values: number[], p: number): number {
  const sorted = [...values].sort((a, b) => a - b);
  const index = Math.min(sorted.length - 1, Math.max(0, (sorted.length - 1) * p));
  const lower = Math.floor(index);
  const upper = Math.ceil(index);

  if (lower === upper) return sorted[lower] || 1;

  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
}

const PRESSURE_BASELINES = {
  health: percentile(
    computedData.admin1.map((admin) => admin.metrics.peoplePerHealthFacility),
    0.75
  ),
  school: percentile(
    computedData.admin1.map((admin) => admin.metrics.peoplePerSchool),
    0.75
  ),
  market: percentile(
    computedData.admin1.map((admin) => admin.metrics.peoplePerMarket),
    0.75
  ),
  heat: percentile(
    computedData.admin1.map((admin) => Math.abs(admin.climate.heatDeltaC)),
    0.75
  ),
  rainfall: percentile(
    computedData.admin1.map((admin) => Math.abs(admin.climate.precipChangePct)),
    0.75
  ),
  osmRisk: percentile(
    computedData.admin1.map((admin) => admin.metrics.osmCompletenessRiskScore),
    0.75
  ),
};

function normalized(value: number, baseline: number): number {
  return value / Math.max(1, baseline);
}

function serviceLensScores(admin: ComputedAdminUnit) {
  return {
    "Health load": normalized(
      admin.metrics.peoplePerHealthFacility,
      PRESSURE_BASELINES.health
    ),
    "School load": normalized(admin.metrics.peoplePerSchool, PRESSURE_BASELINES.school),
    "Market load": normalized(admin.metrics.peoplePerMarket, PRESSURE_BASELINES.market),
  };
}

function dominantServiceLens(admin: ComputedAdminUnit): PressureLens {
  const scores = serviceLensScores(admin);

  return (Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0] ||
    "Health load") as PressureLens;
}

function climateLensScore(admin: ComputedAdminUnit): number {
  return Math.max(
    normalized(Math.abs(admin.climate.heatDeltaC), PRESSURE_BASELINES.heat),
    normalized(Math.abs(admin.climate.precipChangePct), PRESSURE_BASELINES.rainfall)
  );
}

function adminMatchesPressureLens(
  admin: ComputedAdminUnit,
  selectedPressureLens: PressureLens
): boolean {
  if (selectedPressureLens === "All") return true;
  if (selectedPressureLens === "Climate stress") {
    return (
      admin.metrics.bottleneck === "heat stress" ||
      admin.metrics.bottleneck === "rainfall change" ||
      climateLensScore(admin) >= 1
    );
  }
  if (selectedPressureLens === "OSM risk") {
    return admin.metrics.osmCompletenessRiskScore >= PRESSURE_BASELINES.osmRisk;
  }

  return dominantServiceLens(admin) === selectedPressureLens;
}

function countPressureLenses(admins: ComputedAdminUnit[]) {
  return Object.fromEntries(
    PRESSURE_LENSES.map((lens) => [
      lens.value,
      admins.filter((admin) => adminMatchesPressureLens(admin, lens.value)).length,
    ])
  ) as Record<PressureLens, number>;
}

export function AccessPilotSummary() {
  const countries = allComputedCountries();
  const averageIndex = Math.round(
    countries.reduce((sum, country) => sum + country.metrics.accessStressIndex, 0) /
      countries.length
  );
  return (
    <div className="mt-5 grid gap-3 sm:grid-cols-3">
      <MiniStat
        label="Computed layer"
        value={`${computedData.summary.economiesComputed} economies / ${computedData.summary.admin1Units} ADM1`}
      />
      <MiniStat label="National avg. stress" value={String(averageIndex)} />
      <MiniStat
        label="ADB scale-out"
        value={`${scaleoutData.summary.admin1ScreeningCandidates}/${scaleoutData.summary.economiesAssessed} ready`}
      />
    </div>
  );
}

export function AccessServicesPilotEvidence() {
  const [selectedCountry, setSelectedCountry] = useState("All");
  const [selectedPressureLens, setSelectedPressureLens] =
    useState<PressureLens>("All");
  const countries = allComputedCountries();
  const allRankedAdmin = [...computedData.admin1].sort(
    (a, b) => b.metrics.accessStressIndex - a.metrics.accessStressIndex
  );
  const countryFilteredAdminUnits =
    selectedCountry === "All"
      ? computedData.admin1
      : computedData.admin1.filter((admin) => admin.countryName === selectedCountry);
  const lensCounts = countPressureLenses(countryFilteredAdminUnits);
  const filteredAdminUnits = countryFilteredAdminUnits.filter((admin) =>
    adminMatchesPressureLens(admin, selectedPressureLens)
  );
  const rankedComputed = [...filteredAdminUnits].sort(
    (a, b) => b.metrics.accessStressIndex - a.metrics.accessStressIndex
  );
  const generatedDate = new Date(
    computedData.metadata.generatedAt
  ).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
  const computedEconomyNames = new Set<string>(computedData.summary.economies);
  const remainingQueue = scaleoutData.economies.filter(
    (economy) =>
      economy.metrics.nextPipelineMode === "admin1_screening_candidate" &&
      !computedEconomyNames.has(economy.name)
  );

  return (
    <section className="border-y border-zinc-800 bg-zinc-950">
      <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="mb-8 grid min-w-0 gap-6 lg:grid-cols-[360px_minmax(0,1fr)]">
          <div className="min-w-0">
            <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
              Computed multi-country output
            </p>
            <h2 className="mt-3 text-2xl font-semibold text-white">
              8 ADB economies, 104 ADM1 screening rows
            </h2>
            <p className="mt-3 text-sm leading-6 text-zinc-500">
              Generated from World Bank WDI, World Bank CCKP climate data,
              geoBoundaries, PSA OpenSTAT, WorldPop, and OSM service counts via
              Overpass. The first view now shows all currently computed
              economies; the original Philippines/Bangladesh pilot detail stays
              below as the first audited ADM1 batch.
            </p>
            <CoverageScopeBadge remainingCount={remainingQueue.length} />
            <div className="mt-5 flex flex-wrap gap-2">
              <ExportButton href="/data/access-services-admin1.csv" label="Download CSV" />
              <ExportButton href="/data/access-services-admin1.json" label="Download JSON" />
              <ExportButton
                href="/data/access-services-computed-admin1.csv"
                label="Combined CSV"
              />
            </div>
          </div>

          <div className="grid min-w-0 gap-3 sm:grid-cols-3">
            <MiniStat
              label="Generated"
              value={generatedDate}
            />
            <MiniStat
              label="Mapped services"
              value={formatNumber(computedData.summary.totalMappedServices)}
            />
            <MiniStat
              label="Population covered"
              value={formatCompact(computedData.summary.totalPopulation)}
            />
          </div>
        </div>

        <div className="mb-8">
          <ComputedCoveragePanel admins={allRankedAdmin.slice(0, 12)} />
        </div>

        <div className="grid min-w-0 gap-6 lg:grid-cols-[420px_minmax(0,1fr)]">
          <ComputedEconomyMap countries={countries} />
          <PilotMetricTable countries={countries} />
        </div>

        <div className="mt-8">
          <AdminFilterPanel
            countries={computedData.summary.economies}
            selectedCountry={selectedCountry}
            onSelectCountry={setSelectedCountry}
            selectedPressureLens={selectedPressureLens}
            onSelectPressureLens={setSelectedPressureLens}
            lensCounts={lensCounts}
            filteredCount={filteredAdminUnits.length}
            countryFilteredCount={countryFilteredAdminUnits.length}
            totalCount={computedData.summary.admin1Units}
          />
        </div>

        <div className="mt-8 grid min-w-0 gap-6 lg:grid-cols-[minmax(0,1fr)_390px]">
          <AdminStressMap
            adminUnits={filteredAdminUnits}
            rankedAdmin={rankedComputed}
            selectedCountry={selectedCountry}
            selectedPressureLens={selectedPressureLens}
          />
          <AdminWatchlist admins={rankedComputed.slice(0, 5)} />
        </div>

        <div className="mt-6">
          <AdminMetricTable admins={rankedComputed} />
        </div>

        <div className="mt-8">
          <ScaleoutPanel economies={remainingQueue.slice(0, 12)} />
        </div>

        <p className="mt-5 text-xs leading-5 text-zinc-600">
          Caveat: {adminData.metadata.caveat} {adminData.metadata.populationCaveat}{" "}
          {adminData.metadata.serviceCaveat} {computedData.metadata.caveat}{" "}
          {computedData.metadata.populationCaveat} {scaleoutData.metadata.caveat}
        </p>
      </div>
    </section>
  );
}

function CoverageScopeBadge({ remainingCount }: { remainingCount: number }) {
  return (
    <div className="mt-5 rounded-lg border border-emerald-400/40 bg-emerald-400/10 p-4">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="font-mono text-xs uppercase tracking-widest text-emerald-300">
            Current coverage scope
          </p>
          <p className="mt-2 text-sm leading-6 text-zinc-200">
            Showing the combined computed layer, not only the
            Philippines/Bangladesh pilot: {computedData.summary.economiesComputed} ADB
            economies, {computedData.summary.admin1Units} ADM1 rows,{" "}
            {formatNumber(computedData.summary.totalPopulation)} people.
          </p>
        </div>
        <span className="rounded-md border border-emerald-400/40 bg-zinc-950 px-3 py-2 font-mono text-xs text-emerald-300">
          {remainingCount} queued next
        </span>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {computedData.summary.batches.map((batch) => (
          <span
            key={batch.name}
            className="rounded-md border border-zinc-800 bg-zinc-950 px-2 py-1 text-xs text-zinc-400"
          >
            {batch.name.replace("_", " ")}: {batch.economies.join(", ")} /{" "}
            {batch.admin1Units} ADM1
          </span>
        ))}
      </div>
    </div>
  );
}

function AdminFilterPanel({
  countries,
  selectedCountry,
  onSelectCountry,
  selectedPressureLens,
  onSelectPressureLens,
  lensCounts,
  filteredCount,
  countryFilteredCount,
  totalCount,
}: {
  countries: string[];
  selectedCountry: string;
  onSelectCountry: (country: string) => void;
  selectedPressureLens: PressureLens;
  onSelectPressureLens: (lens: PressureLens) => void;
  lensCounts: Record<PressureLens, number>;
  filteredCount: number;
  countryFilteredCount: number;
  totalCount: number;
}) {
  const [countryQuery, setCountryQuery] = useState("");
  const normalizedQuery = countryQuery.trim().toLowerCase();
  const visibleCountries = countries.filter((country) =>
    country.toLowerCase().includes(normalizedQuery)
  );
  const selectCountries =
    selectedCountry !== "All" && !visibleCountries.includes(selectedCountry)
      ? [selectedCountry, ...visibleCountries]
      : visibleCountries;

  return (
    <div className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/50 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
            Country filter
          </p>
          <p className="mt-1 text-xs text-zinc-600">
            Filter the ADM1 map, watchlist, and table below by economy and
            pressure lens.
          </p>
        </div>
        <span className="rounded-md border border-zinc-800 bg-zinc-950 px-2 py-1 font-mono text-xs text-zinc-500">
          {filteredCount}/{selectedCountry === "All" ? totalCount : countryFilteredCount}{" "}
          rows
        </span>
      </div>

      <div className="mt-4 grid gap-4 lg:grid-cols-[minmax(220px,320px)_minmax(0,1fr)]">
        <div className="min-w-0">
          <label className="font-mono text-[11px] uppercase tracking-wider text-zinc-600">
            Economy
          </label>
          <input
            className="mt-2 w-full rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-zinc-100 outline-none transition focus:border-emerald-400"
            onChange={(event) => setCountryQuery(event.target.value)}
            placeholder="Search country"
            type="search"
            value={countryQuery}
          />
          <select
            className="mt-2 w-full rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-zinc-100 outline-none transition focus:border-emerald-400"
            onChange={(event) => onSelectCountry(event.target.value)}
            value={selectedCountry}
          >
            <option value="All">All countries</option>
            {selectCountries.map((country) => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>
          {visibleCountries.length === 0 ? (
            <p className="mt-2 text-[11px] leading-5 text-rose-300">
              No country names match the search.
            </p>
          ) : null}
          <p className="mt-2 text-[11px] leading-5 text-zinc-600">
            {selectedCountry === "All" ? "All computed economies" : selectedCountry} |{" "}
            {countryFilteredCount} ADM1 before pressure-lens filtering
          </p>
        </div>

        <div className="min-w-0">
          <p className="font-mono text-[11px] uppercase tracking-wider text-zinc-600">
            Pressure lens
          </p>
          <div className="mt-2 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {PRESSURE_LENSES.map((lens) => {
              const active = lens.value === selectedPressureLens;

              return (
                <button
                  className={`min-h-20 rounded-md border p-3 text-left transition ${
                    active
                      ? "border-emerald-400 bg-emerald-400 text-zinc-950"
                      : "border-zinc-800 bg-zinc-950 text-zinc-300 hover:border-emerald-400 hover:text-emerald-300"
                  }`}
                  key={lens.value}
                  onClick={() => onSelectPressureLens(lens.value)}
                  type="button"
                >
                  <span className="flex items-center justify-between gap-2">
                    <span className="text-sm font-semibold">{lens.shortLabel}</span>
                    <span className="font-mono text-xs">{lensCounts[lens.value]}</span>
                  </span>
                  <span
                    className={`mt-2 block text-[11px] leading-4 ${
                      active ? "text-zinc-800" : "text-zinc-600"
                    }`}
                  >
                    {lens.description}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

function allComputedCountries(): ComputedCountry[] {
  return [
    ...accessData.countries,
    ...nextWaveData.countries,
    ...frontierData.countries,
  ].sort((a, b) => b.metrics.accessStressIndex - a.metrics.accessStressIndex);
}

function ComputedCoveragePanel({ admins }: { admins: ComputedAdminUnit[] }) {
  const tiledPopulationUnits = computedData.admin1.filter((admin) =>
    admin.population.method.includes("clipped polygon tiles")
  ).length;
  const highest = computedData.summary.highestStressAdmin;

  return (
    <div className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
      <div className="grid min-w-0 gap-6 lg:grid-cols-[360px_minmax(0,1fr)]">
        <div className="min-w-0">
          <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
            Computed ADM1 coverage
          </p>
          <h3 className="mt-2 font-semibold text-white">
            Eight economies now have real subnational screening rows
          </h3>
          <p className="mt-2 text-xs leading-5 text-zinc-600">
            The default access pipeline now produces pilot, South Asia, and
            frontier batches, then merges them into one auditable ADM1 table.
            Larger candidates stay queued for separate batch runs.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <ExportButton
              href="/data/access-services-computed-admin1.csv"
              label="Computed CSV"
            />
            <ExportButton
              href="/data/access-services-computed-admin1.json"
              label="Computed JSON"
            />
            <ExportButton
              href="/data/access-services-frontier-admin1.csv"
              label="Frontier CSV"
            />
          </div>
        </div>

        <div className="grid min-w-0 gap-3 sm:grid-cols-4">
          <MiniStat
            label="Economies"
            value={String(computedData.summary.economiesComputed)}
          />
          <MiniStat
            label="ADM1 units"
            value={String(computedData.summary.admin1Units)}
          />
          <MiniStat
            label="Population"
            value={formatCompact(computedData.summary.totalPopulation)}
          />
          <MiniStat
            label="Tiled population"
            value={String(tiledPopulationUnits)}
          />
        </div>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        {computedData.summary.batches.map((batch) => (
          <div
            key={batch.name}
            className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-950 p-4"
          >
            <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
              {batch.name.replaceAll("_", " ")}
            </p>
            <p className="mt-2 text-sm font-semibold text-zinc-100">
              {batch.admin1Units} ADM1
            </p>
            <p className="mt-2 text-xs leading-5 text-zinc-600">
              {batch.economies.join(", ")}
            </p>
          </div>
        ))}
      </div>

      {highest ? (
        <div className="mt-5 rounded-lg border border-zinc-800 bg-zinc-950 p-4">
          <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
            Highest computed gap
          </p>
          <div className="mt-3 flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-lg font-semibold text-zinc-100">
                {highest.admin1Name}, {highest.countryName}
              </p>
              <p className="mt-1 text-xs text-zinc-600">
                {highest.admin1Code} | bottleneck: {highest.bottleneck}
              </p>
            </div>
            <span
              className="rounded-md px-3 py-2 text-sm font-bold text-zinc-950"
              style={{
                backgroundColor: riskColor(highest.accessStressIndex),
              }}
            >
              {highest.accessStressIndex}
            </span>
          </div>
        </div>
      ) : null}

      <div className="mt-5 max-w-full overflow-x-auto rounded-lg border border-zinc-800">
        <table className="w-full min-w-[900px] text-left text-sm">
          <thead className="bg-zinc-900 text-xs uppercase tracking-wider text-zinc-500">
            <tr>
              <th className="px-4 py-3 font-medium">ADM1</th>
              <th className="px-4 py-3 font-medium">Stress</th>
              <th className="px-4 py-3 font-medium">Population</th>
              <th className="px-4 py-3 font-medium">Services</th>
              <th className="px-4 py-3 font-medium">People / Health</th>
              <th className="px-4 py-3 font-medium">Services / Million</th>
              <th className="px-4 py-3 font-medium">Population Method</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800 bg-zinc-950">
            {admins.map((admin) => (
              <tr key={admin.admin1Code} className="align-top">
                <td className="px-4 py-4">
                  <p className="font-medium text-zinc-100">{admin.admin1Name}</p>
                  <p className="mt-1 text-xs text-zinc-600">
                    {admin.countryName} | {admin.admin1Code}
                  </p>
                </td>
                <td className="px-4 py-4">
                  <span
                    className="rounded-md px-2 py-1 text-xs font-bold text-zinc-950"
                    style={{
                      backgroundColor: riskColor(admin.metrics.accessStressIndex),
                    }}
                  >
                    {admin.metrics.accessStressIndex}
                  </span>
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {formatNumber(admin.population.value)}
                  <p className="mt-1 text-[11px] text-zinc-600">
                    {admin.population.year}
                  </p>
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {formatNumber(admin.services.total)}
                  <p className="mt-1 text-[11px] text-zinc-600">
                    {admin.services.queryMode === "osm_area_iso3166_2"
                      ? "OSM area"
                      : "BBox"}
                  </p>
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {formatNumber(admin.metrics.peoplePerHealthFacility)}
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {admin.metrics.totalMappedServicesPerMillion.toFixed(1)}
                </td>
                <td className="px-4 py-4 text-zinc-500">
                  {admin.population.method.includes("clipped polygon tiles")
                    ? "WorldPop tiled"
                    : "WorldPop polygon"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="mt-4 text-xs leading-5 text-zinc-600">
        Population note: {computedData.metadata.populationCaveat} Current batch
        totals: next-wave {nextWaveData.summary.admin1Units} ADM1 and frontier{" "}
        {frontierData.summary.admin1Units} ADM1. Each row records the exact
        population method used.
      </p>
    </div>
  );
}

function ScaleoutPanel({ economies }: { economies: ScaleoutEconomy[] }) {
  return (
    <div className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
      <div className="grid min-w-0 gap-6 lg:grid-cols-[360px_minmax(0,1fr)]">
        <div className="min-w-0">
          <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
            ADB regional scale-out
          </p>
          <h3 className="mt-2 font-semibold text-white">
            Which economies can move next?
          </h3>
          <p className="mt-2 text-xs leading-5 text-zinc-600">
            This is a source-readiness screen across ADB regional member
            economies. It checks boundary, population, rural-share, and land-area
            availability before making any service-access claim.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <ExportButton
              href="/data/access-services-adb-scaleout.csv"
              label="Scale-out CSV"
            />
            <ExportButton
              href="/data/access-services-adb-scaleout.json"
              label="Scale-out JSON"
            />
          </div>
        </div>

        <div className="grid min-w-0 gap-3 sm:grid-cols-4">
          <MiniStat
            label="Economies assessed"
            value={String(scaleoutData.summary.economiesAssessed)}
          />
          <MiniStat
            label="ADM1 available"
            value={String(scaleoutData.summary.adm1BoundaryAvailable)}
          />
          <MiniStat
            label="Admin candidates"
            value={String(scaleoutData.summary.admin1ScreeningCandidates)}
          />
          <MiniStat
            label="Need review"
            value={String(scaleoutData.summary.sourceReviewRequired)}
          />
        </div>
      </div>

      <div className="mt-5 max-w-full overflow-x-auto rounded-lg border border-zinc-800">
        <table className="w-full min-w-[820px] text-left text-sm">
          <thead className="bg-zinc-900 text-xs uppercase tracking-wider text-zinc-500">
            <tr>
              <th className="px-4 py-3 font-medium">Economy</th>
              <th className="px-4 py-3 font-medium">Subregion</th>
              <th className="px-4 py-3 font-medium">Population</th>
              <th className="px-4 py-3 font-medium">ADM1 Units</th>
              <th className="px-4 py-3 font-medium">Source</th>
              <th className="px-4 py-3 font-medium">Impact</th>
              <th className="px-4 py-3 font-medium">Priority</th>
              <th className="px-4 py-3 font-medium">Next Mode</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800 bg-zinc-950">
            {economies.map((economy) => (
              <tr key={economy.iso3} className="align-top">
                <td className="px-4 py-4">
                  <p className="font-medium text-zinc-100">{economy.name}</p>
                  <p className="mt-1 text-xs text-zinc-600">{economy.iso3}</p>
                </td>
                <td className="px-4 py-4 text-zinc-400">{economy.subregion}</td>
                <td className="px-4 py-4 text-zinc-400">
                  {economy.population
                    ? formatNumber(economy.population.value)
                    : "Review"}
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {economy.boundaries.adm1.admUnitCount ?? "Review"}
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {economy.metrics.sourceReadinessScore}
                </td>
                <td className="px-4 py-4 text-zinc-400">
                  {economy.metrics.impactPriorityScore}
                </td>
                <td className="px-4 py-4">
                  <span className="rounded-md bg-emerald-400 px-2 py-1 text-xs font-bold text-zinc-950">
                    {economy.metrics.scalePriorityScore}
                  </span>
                </td>
                <td className="px-4 py-4 text-zinc-500">
                  {economy.metrics.nextPipelineMode.replaceAll("_", " ")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ComputedEconomyMap({ countries }: { countries: ComputedCountry[] }) {
  return (
    <div className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h3 className="font-semibold text-white">Computed Economy Stress Map</h3>
          <p className="mt-1 text-xs text-zinc-600">
            Marker size and color use the computed national access stress index.
          </p>
        </div>
      </div>

      <div className="relative mt-5 aspect-[4/3] overflow-hidden rounded-lg border border-zinc-800 bg-[radial-gradient(circle_at_center,_rgba(34,197,94,0.10),_transparent_34%),linear-gradient(135deg,_#09090b,_#18181b)]">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:48px_48px]" />
        {countries.map((country) => {
          const position = projectComputed(country.centroid.lon, country.centroid.lat);
          const size = 34 + country.metrics.accessStressIndex * 0.45;

          return (
            <div
              key={country.iso3}
              className="absolute -translate-x-1/2 -translate-y-1/2"
              style={{ left: `${position.x}%`, top: `${position.y}%` }}
            >
              <div
                className="grid place-items-center rounded-full border border-white/20 text-xs font-semibold text-zinc-950 shadow-[0_0_40px_rgba(255,255,255,0.16)]"
                style={{
                  width: size,
                  height: size,
                  backgroundColor: riskColor(country.metrics.accessStressIndex),
                }}
              >
                {country.metrics.accessStressIndex}
              </div>
              <div className="mt-2 whitespace-nowrap rounded-md border border-zinc-800 bg-zinc-950/90 px-2 py-1 text-xs font-medium text-zinc-200">
                {country.name}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 grid gap-2 text-xs text-zinc-500">
        <Legend label="Lower screening risk" color="#22c55e" />
        <Legend label="Moderate screening risk" color="#f59e0b" />
        <Legend label="Higher screening risk" color="#f43f5e" />
      </div>
    </div>
  );
}

function AdminStressMap({
  adminUnits,
  rankedAdmin,
  selectedCountry,
  selectedPressureLens,
}: {
  adminUnits: ComputedAdminUnit[];
  rankedAdmin: ComputedAdminUnit[];
  selectedCountry: string;
  selectedPressureLens: PressureLens;
}) {
  const pressureLabel =
    selectedPressureLens === "All" ? "all pressure lenses" : selectedPressureLens;

  return (
    <div className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
            ADM1 screening layer
          </p>
          <h3 className="mt-2 font-semibold text-white">
            Multi-Country Service Pressure Map
          </h3>
          <p className="mt-1 max-w-xl text-xs leading-5 text-zinc-600">
            Bubble size and color show service-load and climate stress by
            ADM1 unit across all currently computed economies. Labels below rank
            the highest computed gaps for the selected country filter.
          </p>
        </div>
        <span className="rounded-md border border-zinc-800 bg-zinc-950 px-2 py-1 font-mono text-xs text-zinc-500">
          {selectedCountry === "All" ? "All countries" : selectedCountry} |{" "}
          {pressureLabel} | {adminUnits.length} ADM1
        </span>
      </div>

      <div className="relative mt-5 aspect-[16/10] overflow-hidden rounded-lg border border-zinc-800 bg-[radial-gradient(circle_at_25%_55%,_rgba(16,185,129,0.16),_transparent_24%),radial-gradient(circle_at_72%_36%,_rgba(244,63,94,0.13),_transparent_22%),linear-gradient(135deg,_#09090b,_#18181b)]">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:44px_44px]" />
        {adminUnits.map((admin) => {
          const position = projectComputed(admin.centroid.lon, admin.centroid.lat);
          const size = 10 + admin.metrics.accessStressIndex * 0.18;

          return (
            <div
              key={admin.admin1Code}
              className="absolute -translate-x-1/2 -translate-y-1/2"
              style={{ left: `${position.x}%`, top: `${position.y}%` }}
              title={`${admin.admin1Name}: ${admin.metrics.accessStressIndex}`}
            >
              <div
                className="rounded-full border border-white/20 shadow-[0_0_28px_rgba(255,255,255,0.12)]"
                style={{
                  width: size,
                  height: size,
                  backgroundColor: riskColor(admin.metrics.accessStressIndex),
                }}
              />
            </div>
          );
        })}
        {adminUnits.length === 0 ? (
          <div className="absolute inset-0 grid place-items-center px-6 text-center">
            <p className="max-w-sm text-sm leading-6 text-zinc-500">
              No ADM1 rows match the selected country and pressure lens.
            </p>
          </div>
        ) : null}
      </div>

      <div className="mt-4 grid gap-2 sm:grid-cols-2">
        {rankedAdmin.length === 0 ? (
          <div className="rounded-md border border-zinc-800 bg-zinc-950 px-3 py-3 text-xs text-zinc-500 sm:col-span-2">
            No ranked ADM1 rows for this filter.
          </div>
        ) : null}
        {rankedAdmin.slice(0, 6).map((admin, index) => (
          <div
            key={admin.admin1Code}
            className="flex min-w-0 items-center gap-3 rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2"
          >
            <span className="w-5 shrink-0 font-mono text-xs text-zinc-600">
              {index + 1}
            </span>
            <span
              className="h-2.5 w-2.5 shrink-0 rounded-full"
              style={{
                backgroundColor: riskColor(admin.metrics.accessStressIndex),
              }}
            />
            <div className="min-w-0">
              <p className="truncate text-xs font-medium text-zinc-100">
                {admin.admin1Name}
              </p>
              <p className="truncate text-[11px] text-zinc-600">
                {admin.countryName} | {formatNumber(admin.population.value)} people
              </p>
            </div>
            <span className="ml-auto font-mono text-xs text-zinc-300">
              {admin.metrics.accessStressIndex}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function AdminWatchlist({ admins }: { admins: ComputedAdminUnit[] }) {
  return (
    <div className="min-w-0 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
      <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
        Watchlist
      </p>
      <h3 className="mt-2 font-semibold text-white">
        Highest Service-Pressure Gaps
      </h3>
      <div className="mt-5 grid gap-3">
        {admins.length === 0 ? (
          <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4 text-sm leading-6 text-zinc-500">
            No watchlist rows match the selected filters.
          </div>
        ) : null}
        {admins.map((admin) => (
          <div
            key={admin.admin1Code}
            className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0">
                <p className="truncate font-medium text-zinc-100">
                  {admin.admin1Name}
                </p>
                <p className="mt-1 text-xs text-zinc-600">
                  {admin.countryName} | {admin.metrics.bottleneck}
                </p>
              </div>
              <span
                className="rounded-md px-2 py-1 text-xs font-bold text-zinc-950"
                style={{
                  backgroundColor: riskColor(admin.metrics.accessStressIndex),
                }}
              >
                {admin.metrics.accessStressIndex}
              </span>
            </div>
            <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
              <WatchMetric
                label="Health load"
                value={formatNumber(admin.metrics.peoplePerHealthFacility)}
              />
              <WatchMetric
                label="School load"
                value={formatNumber(admin.metrics.peoplePerSchool)}
              />
              <WatchMetric
                label="Market load"
                value={formatNumber(admin.metrics.peoplePerMarket)}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PilotMetricTable({ countries }: { countries: ComputedCountry[] }) {
  return (
    <div className="max-w-full overflow-x-auto rounded-lg border border-zinc-800">
      <table className="w-full min-w-[760px] text-left text-sm">
        <thead className="bg-zinc-900 text-xs uppercase tracking-wider text-zinc-500">
          <tr>
            <th className="px-4 py-3 font-medium">Economy</th>
            <th className="px-4 py-3 font-medium">Stress</th>
            <th className="px-4 py-3 font-medium">People / Health</th>
            <th className="px-4 py-3 font-medium">People / School</th>
            <th className="px-4 py-3 font-medium">People / Market</th>
            <th className="px-4 py-3 font-medium">Heat Delta</th>
            <th className="px-4 py-3 font-medium">Rain Change</th>
            <th className="px-4 py-3 font-medium">Bottleneck</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-800 bg-zinc-950">
          {countries.map((country) => (
            <tr key={country.iso3} className="align-top">
              <td className="px-4 py-4">
                <p className="font-medium text-zinc-100">{country.name}</p>
                <p className="mt-1 text-xs text-zinc-600">
                  Pop. {formatNumber(country.population.value)} | OSM{" "}
                  {country.services.osmTimestamp ?? "timestamp unavailable"}
                </p>
              </td>
              <td className="px-4 py-4">
                <span
                  className="rounded-md px-2 py-1 text-xs font-bold text-zinc-950"
                  style={{
                    backgroundColor: riskColor(country.metrics.accessStressIndex),
                  }}
                >
                  {country.metrics.accessStressIndex}
                </span>
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(country.metrics.peoplePerHealthFacility)}
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(country.metrics.peoplePerSchool)}
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(country.metrics.peoplePerMarket)}
              </td>
              <td className="px-4 py-4 text-zinc-400">
                +{country.climate.heatDeltaC.toFixed(2)} C
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {country.climate.precipChangePct > 0 ? "+" : ""}
                {country.climate.precipChangePct.toFixed(2)}%
              </td>
              <td className="px-4 py-4 text-zinc-500">
                {country.metrics.bottleneck}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function AdminMetricTable({ admins }: { admins: ComputedAdminUnit[] }) {
  return (
    <div className="max-w-full overflow-x-auto rounded-lg border border-zinc-800">
      <table className="w-full min-w-[980px] text-left text-sm">
        <thead className="bg-zinc-900 text-xs uppercase tracking-wider text-zinc-500">
          <tr>
            <th className="px-4 py-3 font-medium">ADM1</th>
            <th className="px-4 py-3 font-medium">Stress</th>
            <th className="px-4 py-3 font-medium">Population</th>
            <th className="px-4 py-3 font-medium">Services</th>
            <th className="px-4 py-3 font-medium">People / Health</th>
            <th className="px-4 py-3 font-medium">People / School</th>
            <th className="px-4 py-3 font-medium">People / Market</th>
            <th className="px-4 py-3 font-medium">OSM Risk</th>
            <th className="px-4 py-3 font-medium">Bottleneck</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-800 bg-zinc-950">
          {admins.length === 0 ? (
            <tr>
              <td className="px-4 py-6 text-sm text-zinc-500" colSpan={9}>
                No ADM1 rows match the selected country and pressure lens.
              </td>
            </tr>
          ) : null}
          {admins.map((admin) => (
            <tr key={admin.admin1Code} className="align-top">
              <td className="px-4 py-4">
                <p className="font-medium text-zinc-100">{admin.admin1Name}</p>
                <p className="mt-1 text-xs text-zinc-600">
                  {admin.countryName} | {admin.admin1Code}
                </p>
              </td>
              <td className="px-4 py-4">
                <span
                  className="rounded-md px-2 py-1 text-xs font-bold text-zinc-950"
                  style={{
                    backgroundColor: riskColor(admin.metrics.accessStressIndex),
                  }}
                >
                  {admin.metrics.accessStressIndex}
                </span>
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(admin.population.value)}
                <p className="mt-1 text-[11px] text-zinc-600">
                  {admin.population.year}
                </p>
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(admin.services.total)}
                <p className="mt-1 text-[11px] text-zinc-600">
                  {admin.services.queryMode === "osm_area_iso3166_2"
                    ? "OSM area"
                    : "BBox"}
                </p>
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(admin.metrics.peoplePerHealthFacility)}
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(admin.metrics.peoplePerSchool)}
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {formatNumber(admin.metrics.peoplePerMarket)}
              </td>
              <td className="px-4 py-4 text-zinc-400">
                {admin.metrics.osmCompletenessRiskScore.toFixed(1)}
              </td>
              <td className="px-4 py-4 text-zinc-500">
                {admin.metrics.bottleneck}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-3">
      <p className="font-mono text-[11px] uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-1 text-sm font-semibold text-zinc-100">{value}</p>
    </div>
  );
}

function WatchMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-md border border-zinc-800 bg-zinc-900 p-2">
      <p className="truncate text-[10px] uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-1 truncate text-xs font-semibold text-zinc-100">{value}</p>
    </div>
  );
}

function ExportButton({ href, label }: { href: string; label: string }) {
  return (
    <a
      className="rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs font-medium text-zinc-200 transition hover:border-emerald-400 hover:text-emerald-300"
      href={href}
    >
      {label}
    </a>
  );
}

function Legend({ label, color }: { label: string; color: string }) {
  return (
    <div className="flex items-center gap-2">
      <span
        className="h-2.5 w-2.5 rounded-full"
        style={{ backgroundColor: color }}
      />
      <span>{label}</span>
    </div>
  );
}

function projectComputed(lon: number, lat: number): { x: number; y: number } {
  const minLon = 58;
  const maxLon = 130;
  const minLat = -12;
  const maxLat = 38;

  return {
    x: ((lon - minLon) / (maxLon - minLon)) * 100,
    y: ((maxLat - lat) / (maxLat - minLat)) * 100,
  };
}
