import { useEffect, useState } from "react";
import { Link, useParams, Navigate } from "react-router-dom";
import { dmcByIso, DMCS } from "../lib/dmcs";
import {
  INDICATORS,
  loadIndicator,
  computeRank,
  type IndicatorRow,
  type IndicatorDef,
} from "../lib/indicators";
import { Kicker, Numeral, Divider, DistributionDots, Bar } from "../components/ui";

interface IndicatorView {
  def: IndicatorDef;
  rows: IndicatorRow[];
  row: IndicatorRow | null;
  rank: { rank: number; total: number } | null;
}

export default function DMC() {
  const { iso3 = "" } = useParams();
  const dmc = dmcByIso.get(iso3.toUpperCase());
  const [views, setViews] = useState<IndicatorView[] | null>(null);

  useEffect(() => {
    if (!dmc) return;
    Promise.all(
      INDICATORS.map(async (def) => {
        try {
          const rows = await loadIndicator(def);
          const row = rows.find((r) => r.iso3 === dmc.iso3) ?? null;
          const rank = row?.value !== null && row?.value !== undefined
            ? computeRank(rows, dmc.iso3, def.higherIsWorse)
            : null;
          return { def, rows, row, rank };
        } catch {
          return { def, rows: [] as IndicatorRow[], row: null, rank: null };
        }
      }),
    ).then((arr) => setViews(arr));
  }, [dmc?.iso3]);

  if (!dmc) {
    if (DMCS.find((d) => d.iso3.toLowerCase() === iso3.toLowerCase())) {
      return <Navigate to={`/dmc/${iso3.toUpperCase()}`} replace />;
    }
    return (
      <div className="py-20 text-center">
        <Kicker>Atlas · 404</Kicker>
        <h1 className="display-lg text-3xl mt-4">No dossier for {iso3.toUpperCase()}</h1>
        <Link to="/atlas" className="ed-link mt-6 inline-block">Back to atlas</Link>
      </div>
    );
  }

  const ordered = views
    ? [...views].sort((a, b) => {
        // Show coverage first, then by domain
        if (!!a.row !== !!b.row) return a.row ? -1 : 1;
        return a.def.programNumber - b.def.programNumber;
      })
    : null;

  const numericViews = ordered?.filter((v) => v.row?.value !== null && v.row?.value !== undefined) ?? [];

  // Cross-program composite vulnerability: average normalized rank-percentile
  const compositeAvg =
    numericViews.length > 0
      ? Math.round(
          (numericViews.reduce((s, v) => {
            if (!v.rank) return s;
            const pct = v.def.higherIsWorse
              ? (v.rank.total - v.rank.rank + 1) / v.rank.total
              : v.rank.rank / v.rank.total;
            return s + (1 - pct) * 100; // higher = more vulnerable, 0-100
          }, 0) / numericViews.length),
        )
      : null;

  return (
    <div className="reveal">
      {/* Dossier head */}
      <header className="grid grid-cols-12 gap-6 lg:gap-10 mb-12">
        <div className="col-span-12 lg:col-span-7">
          <div className="flex items-baseline gap-6 mb-4">
            <Kicker>Dossier</Kicker>
            <span className="font-mono text-xs uppercase tracking-[0.18em] text-ink-faint">
              {dmc.iso3} · {dmc.iso2}
            </span>
            <span className="font-mono text-xs uppercase tracking-[0.18em] text-ink-faint">
              {dmc.subregion}
            </span>
          </div>
          <h1 className="masthead-display text-[clamp(3rem,8vw,6rem)] leading-[0.9]">
            {dmc.name}
          </h1>
          <p className="lede mt-7 max-w-[58ch]">
            Cross-program profile. Every measurement-gap signal we have
            computed for {dmc.name}, ordered by program number. Each row
            shows where this economy stands within the cross-DMC
            distribution and links to the underlying program.
          </p>
        </div>
        <aside className="col-span-12 lg:col-span-5 lg:pl-10 lg:border-l lg:border-[var(--rule)]">
          <div className="kicker mb-4">Coverage summary</div>
          <div className="grid grid-cols-2 gap-6">
            <Stat label="Indicators registered" value={INDICATORS.length} />
            <Stat label="Computed for this DMC" value={numericViews.length} />
            <Stat
              label="Composite vulnerability"
              value={compositeAvg !== null ? compositeAvg : "—"}
              hint="0–100 across covered indicators"
            />
            <Stat
              label="Rank-distribution density"
              value={
                <DistributionDots
                  values={numericViews
                    .map((v) =>
                      v.rank
                        ? (v.def.higherIsWorse
                            ? (v.rank.total - v.rank.rank + 1) / v.rank.total
                            : v.rank.rank / v.rank.total) * 100
                        : NaN,
                    )
                    .filter(Number.isFinite)}
                  highlightColor="var(--crimson)"
                  color="var(--ink)"
                />
              }
              hint={null}
            />
          </div>
        </aside>
      </header>

      <Divider />

      {/* Indicator list */}
      <section>
        <div className="grid grid-cols-12 gap-6 mb-8">
          <div className="col-span-12 md:col-span-3">
            <Kicker>The findings</Kicker>
          </div>
          <div className="col-span-12 md:col-span-7 md:col-start-5 marginalia">
            Vulnerability rank is computed within the cross-DMC
            distribution of each indicator. A rank of 1 means most
            vulnerable observed; rank N means least. Programs without
            coverage for this DMC are listed at the bottom with a
            note explaining the gap.
          </div>
        </div>

        <ul className="divide-y divide-[var(--rule-soft)] reveal-stagger">
          {ordered?.map((v) => (
            <IndicatorRowView key={v.def.programSlug} view={v} />
          ))}
        </ul>
      </section>

      <Divider wide />

      {/* Footer nav */}
      <nav className="flex items-center justify-between gap-4 flex-wrap">
        <Link to="/atlas" className="ed-link text-sm uppercase tracking-[0.18em] font-mono">
          ← Back to atlas
        </Link>
        <div className="flex gap-3 flex-wrap">
          {[
            "PHL", "BGD", "IND", "PAK", "TKM", "KGZ", "TON", "VUT",
          ]
            .filter((c) => c !== dmc.iso3)
            .slice(0, 6)
            .map((c) => (
              <Link
                key={c}
                to={`/dmc/${c}`}
                className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint hover:text-ink transition-colors"
              >
                → {c}
              </Link>
            ))}
        </div>
      </nav>
    </div>
  );
}

function IndicatorRowView({ view }: { view: IndicatorView }) {
  const { def, rows, row, rank } = view;
  const v = row?.value;
  const hasValue = v !== null && v !== undefined;

  return (
    <li className="py-7">
      <div className="grid grid-cols-12 gap-4 items-start">
        <div className="col-span-12 sm:col-span-1">
          <Numeral n={def.programNumber} />
        </div>

        <div className="col-span-12 sm:col-span-7">
          <Link to={def.href} className="group block">
            <Kicker>{def.domain}</Kicker>
            <h3 className="display-md text-[clamp(1.15rem,1.6vw,1.4rem)] mt-2 group-hover:text-crimson transition-colors">
              {def.programTitle}
            </h3>
            {hasValue ? (
              <p className="mt-2 text-ink-soft leading-relaxed max-w-prose">
                {def.sentenceTemplate(v as number, row?.raw)}
              </p>
            ) : (
              <p className="mt-2 marginalia max-w-prose">
                No value computed for this DMC. The program may not yet
                cover this economy, or the country fell outside the
                indicator's available data window.
              </p>
            )}
          </Link>
        </div>

        <div className="col-span-12 sm:col-span-4 marginalia">
          {hasValue && rank ? (
            <>
              <div className="flex items-baseline gap-2 mb-2">
                <span className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">Rank</span>
                <span className="font-mono tabular text-base text-ink">
                  {rank.rank}
                </span>
                <span className="text-ink-faint">/ {rank.total}</span>
              </div>
              <DistributionDots
                values={rows
                  .filter((r) => r.value !== null)
                  .map((r) => r.value as number)}
                highlight={v as number}
              />
              <div className="mt-3 flex items-baseline gap-2">
                <span className="font-mono text-xs uppercase tracking-[0.16em] text-ink-faint">{def.metricLabel}</span>
                <span className="font-mono tabular text-ink">
                  {(v as number).toFixed(2)}
                </span>
                <span className="text-ink-faint text-xs">{def.unit}</span>
              </div>
            </>
          ) : (
            <span className="text-ink-faint">No data.</span>
          )}
        </div>
      </div>
    </li>
  );
}

function Stat({ label, value, hint }: { label: string; value: any; hint?: string | null }) {
  return (
    <div>
      <div className="kicker">{label}</div>
      <div className="display-md text-[1.7rem] mt-1 tabular">{value}</div>
      {hint !== null && hint !== undefined && (
        <div className="marginalia mt-1">{hint}</div>
      )}
    </div>
  );
}
