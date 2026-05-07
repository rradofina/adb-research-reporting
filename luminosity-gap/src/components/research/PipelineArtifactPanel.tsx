import ooklaData from "@/data/generated/digital-performance-ookla-pilots.json";
import openAqData from "@/data/generated/air-monitoring-openaq-pilots.json";

export function PipelineArtifactPanel({ kind }: { kind: "ookla" | "openaq" }) {
  if (kind === "ookla") {
    return (
      <section className="border-y border-zinc-800 bg-zinc-950">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <p className="font-mono text-xs uppercase tracking-widest text-sky-400">
            Pipeline artifact
          </p>
          <h2 className="mt-3 text-2xl font-semibold text-white">
            Ookla download and aggregation scripts are ready.
          </h2>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-500">
            The generated manifest targets {ooklaData.metadata.year} Q
            {ooklaData.metadata.quarter} mobile and fixed parquet files and
            writes DuckDB SQL for Philippines and Bangladesh bounding-box
            aggregation.
          </p>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {ooklaData.manifests.map((manifest) => (
              <div
                key={manifest.type}
                className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-4"
              >
                <h3 className="font-semibold text-zinc-100">
                  {manifest.type} performance
                </h3>
                <p className="mt-2 break-all text-xs leading-5 text-zinc-500">
                  {manifest.url}
                </p>
                <p className="mt-3 font-mono text-xs text-zinc-600">
                  SQL: {manifest.duckdbSqlPath}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  const openAqComputed = openAqData.metadata.status === "computed";
  const openAqSummary = openAqData.summary;
  const highlightedEconomies = openAqData.countries.filter((country) =>
    ["PHL", "BGD"].includes(country.iso3)
  );
  const topPm25GapEconomies = [...openAqData.countries]
    .filter((country) => country.metrics.pm25ObservabilityGapScore !== null)
    .sort((a, b) => (b.publicLocations ?? 0) - (a.publicLocations ?? 0))
    .sort(
      (a, b) =>
        (b.metrics.pm25ObservabilityGapScore ?? 0) -
        (a.metrics.pm25ObservabilityGapScore ?? 0)
    )
    .slice(0, 12);
  const monitorDesertEconomies = [...openAqData.countries]
    .filter(
      (country) =>
        country.metrics.pm25ObservabilityStatus === "no_public_pm25_monitor"
    )
    .sort((a, b) => (b.population?.value ?? 0) - (a.population?.value ?? 0))
    .slice(0, 4);

  return (
    <section className="border-y border-zinc-800 bg-zinc-950">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <p className="font-mono text-xs uppercase tracking-widest text-rose-400">
          Pipeline artifact
        </p>
        <h2 className="mt-3 text-2xl font-semibold text-white">
          {openAqComputed
            ? "OpenAQ, population, and PM2.5 validation have been computed."
            : "OpenAQ aggregation script is wired for API-key execution."}
        </h2>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-zinc-500">
          {openAqComputed
            ? `The script queried ${openAqSummary.economiesQueried} ADB regional member economies and found public OpenAQ locations in ${openAqSummary.economiesWithLocations}. This is monitor observability metadata, not yet a satellite-linked exposure gap.`
            : "OpenAQ API v3 requires an API key, so this run wrote a reproducible blocked-state artifact instead of fabricating monitor counts. Set OPENAQ_API_KEY and rerun npm run research:openaq."}
        </p>

        {openAqComputed && (
          <>
            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <OpenAQSummaryStat
                label="Economies queried"
                value={formatMaybe(openAqSummary.economiesQueried)}
              />
              <OpenAQSummaryStat
                label="With locations"
                value={formatMaybe(openAqSummary.economiesWithLocations)}
              />
              <OpenAQSummaryStat
                label="Zero-location economies"
                value={formatMaybe(openAqSummary.economiesWithNoLocations)}
              />
              <OpenAQSummaryStat
                label="Public locations"
                value={formatMaybe(openAqSummary.totalPublicLocations)}
              />
            </div>
            <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <OpenAQSummaryStat
                label="Population known"
                value={formatMaybe(openAqSummary.populationKnownEconomies)}
              />
              <OpenAQSummaryStat
                label="PM2.5 exposure known"
                value={formatMaybe(openAqSummary.pm25ExposureKnownEconomies)}
              />
              <OpenAQSummaryStat
                label="WHO city PM2.5 economies"
                value={formatMaybe(openAqSummary.whoCityPm25KnownEconomies)}
              />
              <OpenAQSummaryStat
                label="WHO city PM2.5 records"
                value={formatMaybe(openAqSummary.whoCityPm25Cities)}
              />
            </div>
            <div className="mt-3 grid gap-3 sm:grid-cols-2">
              <OpenAQSummaryStat
                label="In high-PM2.5 economies"
                value={formatMaybe(
                  openAqSummary.populationInAboveGuidelinePm25Economies
                )}
              />
              <OpenAQSummaryStat
                label="High PM2.5 + no PM2.5 monitor"
                value={formatMaybe(openAqSummary.populationWithNoPublicPm25Monitor)}
              />
            </div>
          </>
        )}

        {openAqComputed && (
          <div className="mt-4 flex flex-wrap gap-3">
            <a
              href="/data/air-monitoring-openaq-economies.csv"
              download
              className="rounded-lg bg-rose-400 px-4 py-2 text-sm font-semibold text-zinc-950 transition-opacity hover:opacity-90"
            >
              Download CSV
            </a>
            <a
              href="/data/air-monitoring-openaq-pilots.json"
              download
              className="rounded-lg border border-zinc-700 px-4 py-2 text-sm font-semibold text-zinc-200 transition-colors hover:border-zinc-500"
            >
              Download JSON
            </a>
          </div>
        )}

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {(openAqComputed ? highlightedEconomies : openAqData.countries).map((country) => (
            <div
              key={country.iso3}
              className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-4"
            >
              <h3 className="font-semibold text-zinc-100">{country.name}</h3>
              {openAqComputed ? (
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  <OpenAQStat
                    label="Public locations"
                    value={formatMaybe(country.publicLocations)}
                  />
                  <OpenAQStat
                    label="Unknown freshness"
                    value={formatMaybe(country.unknownFreshness)}
                  />
                  <OpenAQStat
                    label="PM2.5 coverage"
                    value={formatMaybe(country.parameterCoverage.pm25)}
                  />
                  <OpenAQStat
                    label="PM10 coverage"
                    value={formatMaybe(country.parameterCoverage.pm10)}
                  />
                  <OpenAQStat
                    label="PM2.5 exposure"
                    value={formatUnit(country.pm25Exposure?.value, "ug/m3")}
                  />
                  <OpenAQStat
                    label="People / PM2.5 monitor"
                    value={formatMaybe(country.metrics.peoplePerPm25Location)}
                  />
                  <OpenAQStat
                    label="WHO city PM2.5 mean"
                    value={formatUnit(
                      country.whoCityValidation.pm25CityMean,
                      "ug/m3"
                    )}
                  />
                  <OpenAQStat
                    label="WHO city records"
                    value={formatMaybe(country.whoCityValidation.citiesWithPm25)}
                  />
                </div>
              ) : (
                <>
                  <p className="mt-2 text-sm text-zinc-500">
                    Status: {openAqData.metadata.status}
                  </p>
                  <p className="mt-3 font-mono text-xs text-zinc-600">
                    Script: {openAqData.metadata.script}
                  </p>
                </>
              )}
            </div>
          ))}
        </div>

        {openAqComputed && (
          <div className="mt-6 grid gap-6 lg:grid-cols-[420px_minmax(0,1fr)]">
            <ObservabilityBubbleMap countries={topPm25GapEconomies.slice(0, 10)} />
            <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5">
              <h3 className="font-semibold text-zinc-100">
                Monitor desert watchlist
              </h3>
              <p className="mt-2 text-xs leading-5 text-zinc-600">
                Above-guideline WDI PM2.5 exposure and no public PM2.5 monitor
                in OpenAQ.
              </p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {monitorDesertEconomies.map((country) => (
                  <div
                    key={country.iso3}
                    className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                  >
                    <h4 className="font-semibold text-zinc-100">
                      {country.name}
                    </h4>
                    <div className="mt-3 grid gap-3">
                      <OpenAQStat
                        label="Population"
                        value={formatMaybe(country.population?.value)}
                      />
                      <OpenAQStat
                        label="PM2.5 exposure"
                        value={formatUnit(country.pm25Exposure?.value, "ug/m3")}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {openAqComputed && (
          <div className="mt-6">
            <h3 className="font-semibold text-zinc-100">
              Highest PM2.5 observability gaps
            </h3>
            <p className="mt-2 max-w-3xl text-xs leading-5 text-zinc-600">
              Ranked by a first-pass score combining national PM2.5 exposure
              and public PM2.5 monitor scarcity.
            </p>
            <div className="mt-4 max-w-full overflow-x-auto rounded-lg border border-zinc-800">
            <table className="w-full min-w-[820px] text-left text-sm">
              <thead className="bg-zinc-900 text-xs uppercase tracking-wider text-zinc-500">
                <tr>
                  <th className="px-4 py-3 font-medium">Economy</th>
                  <th className="px-4 py-3 font-medium">Subregion</th>
                  <th className="px-4 py-3 font-medium">Gap</th>
                  <th className="px-4 py-3 font-medium">Population</th>
                  <th className="px-4 py-3 font-medium">PM2.5 Exposure</th>
                  <th className="px-4 py-3 font-medium">WHO City Mean</th>
                  <th className="px-4 py-3 font-medium">PM2.5</th>
                  <th className="px-4 py-3 font-medium">People / PM2.5</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800 bg-zinc-950">
                {topPm25GapEconomies.map((country) => (
                  <tr key={country.iso3}>
                    <td className="px-4 py-3 font-medium text-zinc-100">
                      {country.name}
                    </td>
                    <td className="px-4 py-3 text-zinc-500">
                      {country.subregion}
                    </td>
                    <td className="px-4 py-3 text-zinc-300">
                      {formatMaybe(country.metrics.pm25ObservabilityGapScore)}
                    </td>
                    <td className="px-4 py-3 text-zinc-400">
                      {formatMaybe(country.population?.value)}
                    </td>
                    <td className="px-4 py-3 text-zinc-400">
                      {formatUnit(country.pm25Exposure?.value, "ug/m3")}
                    </td>
                    <td className="px-4 py-3 text-zinc-400">
                      {formatUnit(
                        country.whoCityValidation.pm25CityMean,
                        "ug/m3"
                      )}
                    </td>
                    <td className="px-4 py-3 text-zinc-400">
                      {formatMaybe(country.parameterCoverage.pm25)}
                    </td>
                    <td className="px-4 py-3 text-zinc-400">
                      {formatMaybe(country.metrics.peoplePerPm25Location)}
                    </td>
                    <td className="px-4 py-3 text-zinc-500">
                      {country.metrics.pm25ObservabilityStatus.replaceAll("_", " ")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          </div>
        )}

        <p className="mt-5 text-xs leading-5 text-zinc-600">
          Caveat: {openAqData.metadata.caveat} The PM2.5 gap score is a national
          screening metric, not a local exposure model. WHO city PM2.5 is used
          as validation context where available. Sentinel-5P NO2 exposure is
          documented as a next export step, not computed in this local run.
        </p>
      </div>
    </section>
  );
}

function formatMaybe(value: number | null | undefined): string {
  if (typeof value !== "number") {
    return "Not computed";
  }

  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 1,
  }).format(value);
}

function formatUnit(value: number | null | undefined, unit: string): string {
  if (typeof value !== "number") {
    return "Not computed";
  }

  return `${new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 1,
  }).format(value)} ${unit}`;
}

function OpenAQStat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-1 text-sm font-semibold text-zinc-200">{value}</p>
    </div>
  );
}

function OpenAQSummaryStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-4">
      <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p className="mt-2 text-xl font-semibold text-zinc-100">{value}</p>
    </div>
  );
}

const BUBBLE_POSITIONS: Record<string, { x: number; y: number }> = {
  AZE: { x: 18, y: 24 },
  UZB: { x: 38, y: 22 },
  CHN: { x: 73, y: 26 },
  TJK: { x: 45, y: 41 },
  AFG: { x: 21, y: 52 },
  PAK: { x: 35, y: 67 },
  IND: { x: 54, y: 63 },
  BGD: { x: 72, y: 55 },
  MMR: { x: 82, y: 74 },
  LKA: { x: 60, y: 84 },
  NPL: { x: 57, y: 47 },
  IDN: { x: 78, y: 88 },
};

function ObservabilityBubbleMap({
  countries,
}: {
  countries: typeof openAqData.countries;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5">
      <h3 className="font-semibold text-zinc-100">Ranked Observability Map</h3>
      <p className="mt-2 text-xs leading-5 text-zinc-600">
        Bubble size follows the PM2.5 observability gap score. Positions are a
        lightweight regional sketch for scanning, not survey-grade geography.
      </p>
      <div className="relative mt-5 aspect-[4/3] overflow-hidden rounded-lg border border-zinc-800 bg-[linear-gradient(135deg,_#09090b,_#18181b)]">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:42px_42px]" />
        {countries.map((country) => {
          const position = BUBBLE_POSITIONS[country.iso3] ?? { x: 50, y: 50 };
          const score = country.metrics.pm25ObservabilityGapScore ?? 0;
          const size = 30 + score * 0.42;

          return (
            <div
              key={country.iso3}
              className="absolute -translate-x-1/2 -translate-y-1/2"
              style={{ left: `${position.x}%`, top: `${position.y}%` }}
            >
              <div
                className="grid place-items-center rounded-full border border-white/20 bg-rose-400 text-xs font-bold text-zinc-950 shadow-[0_0_36px_rgba(244,63,94,0.22)]"
                style={{ width: size, height: size }}
              >
                {score}
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-4 grid gap-2 sm:grid-cols-2">
        {countries.map((country, index) => (
          <div
            key={country.iso3}
            className="flex items-center justify-between gap-3 rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-xs"
          >
            <span className="min-w-0 truncate text-zinc-300">
              {index + 1}. {country.name}
            </span>
            <span className="font-mono text-rose-300">
              {country.metrics.pm25ObservabilityGapScore}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
