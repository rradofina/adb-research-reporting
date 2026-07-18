"use client";

import { useEffect, useState } from "react";
import { MaturityChip } from "../lib/claimTiers";

interface BaselineYear {
  year: number;
  rankable_dmcs: number;
  proxy_top3: string[];
  heat_top3: string[];
  top3_overlap_count: number;
  spearman_proxy_vs_heat: number;
}

interface Payload {
  aligned_years: number[];
  aligned_year_parameter_tests: number;
  top3_overlap_max_across_tests: number;
  top3_zero_overlap_tests: number;
  top3_one_overlap_tests: number;
  latest_heat_dmcs: number;
  roster_dmcs: number;
  baseline_year_summaries: BaselineYear[];
}

const names: Record<string, string> = {
  IND: "India",
  AFG: "Afghanistan",
  BGD: "Bangladesh",
  KHM: "Cambodia",
  PAK: "Pakistan",
  MMR: "Myanmar",
  THA: "Thailand",
};

function list(isos: string[]) {
  return isos.map((iso) => names[iso] ?? iso).join(", ");
}

export default function ProgramClimateHealth() {
  const [data, setData] = useState<Payload | null>(null);

  useEffect(() => {
    fetch("/programs/climate-health-workdays/generated/climate-health-construct-validation.json")
      .then((response) => response.json())
      .then(setData);
  }, []);

  if (!data) return <div className="p-12 text-ink-500">Loading evidence…</div>;

  return (
    <main className="mx-auto max-w-[92rem] px-5 py-10 sm:px-8 lg:px-12">
      <header className="grid gap-7 border-b border-ink-200 pb-9 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-start">
        <div className="max-w-5xl">
          <p className="text-xs uppercase tracking-[0.2em] text-ink-500">Program #5 · climate-health-workdays</p>
          <h1 className="mt-3 max-w-4xl text-4xl font-semibold tracking-tight text-ink-950 sm:text-5xl">
            A stable proxy can still measure the wrong thing.
          </h1>
          <p className="mt-5 max-w-4xl text-lg leading-8 text-ink-700">
            Across 21 aligned tests, the inherited PM2.5 × employment proxy shares at most one of its top three economies with the Lancet Countdown heat-related potential work-hours-loss measure. The country-ranking story is retired; the construct disagreement is the finding.
          </p>
        </div>
        <MaturityChip status="PP" />
      </header>

      <section className="mt-9 grid gap-4 sm:grid-cols-2 xl:grid-cols-4" aria-label="Headline evidence">
        {[
          ["Maximum overlap", `${data.top3_overlap_max_across_tests} of 3`, "Across every year and parameter test"],
          ["Zero-overlap tests", `${data.top3_zero_overlap_tests} of ${data.aligned_year_parameter_tests}`, "The other five share one economy"],
          ["Aligned sample", "34 economies", `${data.aligned_years.join("–")} annual data`],
          ["2024 heat coverage", `${data.latest_heat_dmcs} of ${data.roster_dmcs}`, "Potential-capacity source, not absence"],
        ].map(([label, value, note]) => (
          <article key={label} className="rounded-xl border border-ink-200 bg-white p-5 shadow-sm">
            <p className="text-xs uppercase tracking-wider text-ink-500">{label}</p>
            <p className="mt-2 text-3xl font-semibold tabular-nums text-ink-950">{value}</p>
            <p className="mt-2 text-sm leading-6 text-ink-600">{note}</p>
          </article>
        ))}
      </section>

      <section className="mt-12 grid gap-8 xl:grid-cols-[minmax(0,1.45fr)_minmax(20rem,0.55fr)] xl:items-start">
        <figure className="overflow-hidden rounded-xl border border-ink-200 bg-white p-3 shadow-sm sm:p-5">
          <img
            src="/programs/climate-health-workdays/generated/charts/climate-construct-rank-disagreement.svg"
            alt="Rank comparison showing sharp disagreement between the PM2.5 employment proxy and heat-related potential work hours lost in 2020."
            className="h-auto w-full"
          />
        </figure>

        <aside className="rounded-xl border border-ink-200 bg-ink-50 p-6">
          <p className="text-xs uppercase tracking-wider text-ink-500">What changed</p>
          <h2 className="mt-2 text-2xl font-semibold text-ink-950">Internal stability was not external validity.</h2>
          <p className="mt-4 leading-7 text-ink-700">
            The old proxy kept naming similar economies when its own settings changed. Once compared with a direct heat-labor construct at the same years and sample, its leading set separated.
          </p>
          <p className="mt-4 leading-7 text-ink-700">
            This does not deny a PM2.5-productivity pathway. It means PM2.5 and heat should remain separate evidence objects unless a joint outcome design identifies both.
          </p>
        </aside>
      </section>

      <section className="mt-12">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-wider text-ink-500">Baseline annual comparison</p>
          <h2 className="mt-2 text-3xl font-semibold text-ink-950">The leading sets are disjoint in every aligned year.</h2>
        </div>
        <div className="mt-6 overflow-x-auto rounded-xl border border-ink-200 bg-white shadow-sm">
          <table className="data-table w-full min-w-[760px] text-sm">
            <thead>
              <tr className="text-left">
                <th>Year</th>
                <th>PM2.5 × employment proxy</th>
                <th>Heat-related potential hours</th>
                <th className="text-right">Shared</th>
                <th className="text-right">Spearman ρ</th>
              </tr>
            </thead>
            <tbody>
              {data.baseline_year_summaries.map((row) => (
                <tr key={row.year}>
                  <td className="font-semibold">{row.year}</td>
                  <td>{list(row.proxy_top3)}</td>
                  <td>{list(row.heat_top3)}</td>
                  <td className="text-right font-semibold tabular-nums">{row.top3_overlap_count}/3</td>
                  <td className="text-right tabular-nums">{row.spearman_proxy_vs_heat.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-12 grid gap-6 lg:grid-cols-2">
        <figure className="overflow-hidden rounded-xl border border-ink-200 bg-white p-3 shadow-sm sm:p-5">
          <img
            src="/programs/climate-health-workdays/generated/charts/climate-construct-sensitivity.svg"
            alt="Sensitivity matrix showing zero or one shared top-three economy in all 21 tests."
            className="h-auto w-full"
          />
        </figure>
        <figure className="overflow-hidden rounded-xl border border-ink-200 bg-white p-3 shadow-sm sm:p-5">
          <img
            src="/programs/climate-health-workdays/generated/charts/climate-source-coverage.svg"
            alt="Coverage chart showing 43 heat-loss rows but no observed absence or hours outcome joined in this package."
            className="h-auto w-full"
          />
        </figure>
      </section>

      <section className="mt-12 rounded-xl border border-amber-200 bg-amber-50 p-6 sm:p-8">
        <h2 className="text-2xl font-semibold text-ink-950">Read the unit before the number.</h2>
        <p className="mt-3 max-w-5xl leading-7 text-ink-700">
          Lancet values are modelled potential work hours lost from heat exposure, workload, employment, and population. They are not recorded absence, observed hours, output, wages, or a causal estimate from this study. The next research step is an observed exposure-outcome panel—not another national composite.
        </p>
      </section>
    </main>
  );
}
