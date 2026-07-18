"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Chip, Divider, Kicker, Maturity, Numeral, StatBlock } from "../components/ui";
import {
  BRIEF_DETAILS,
  ROAD_QUALITY_NEXT_TRACK,
  type BriefDetail,
} from "../data/briefs";
import {
  ISSUE_CLOSURE_AS_OF,
  issueClosureDeck,
  issueStatusCards,
  issueTotal,
} from "../data/issueClosure";
import { programs } from "../data/programs";
import type { Maturity as MaturityStatus } from "../lib/claimTiers";
import { INDICATORS, loadIndicator, type IndicatorDef, type IndicatorRow } from "../lib/indicators";

type Filter = "all" | MaturityStatus;

interface ChartPack {
  def: IndicatorDef;
  rows: Array<{ label: string; value: number; highlight?: boolean }>;
  unit: string;
}

const FILTERS: Array<{ key: Filter; label: string }> = [
  { key: "all", label: "All topics" },
  { key: "PR", label: "Publication-ready" },
  { key: "SR", label: "Screening" },
  { key: "PP", label: "Pipeline" },
  { key: "H", label: "Hypothesis" },
];

const FINISH_ORDER: Record<MaturityStatus, number> = {
  PR: 0,
  SR: 1,
  PP: 2,
  H: 3,
  Ret: 4,
};

export default function Briefs() {
  const [filter, setFilter] = useState<Filter>("all");
  const [charts, setCharts] = useState<Record<string, ChartPack>>({});

  useEffect(() => {
    let cancelled = false;
    Promise.all(
      INDICATORS.map(async (def) => {
        const rows = await loadIndicator(def);
        return [def.programSlug, buildChartPack(def, rows)] as const;
      }),
    )
      .then((packs) => {
        if (!cancelled) setCharts(Object.fromEntries(packs));
      })
      .catch(() => {
        if (!cancelled) setCharts({});
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const visible = programs
    .filter((program) => {
      const detail = BRIEF_DETAILS[program.slug];
      if (!detail) return false;
      return filter === "all" || program.status === filter;
    })
    .sort((a, b) => {
      const aDetail = BRIEF_DETAILS[a.slug];
      const bDetail = BRIEF_DETAILS[b.slug];
      const flagshipSort = Number(Boolean(bDetail.flagship)) - Number(Boolean(aDetail.flagship));
      if (filter === "all") {
        return FINISH_ORDER[a.status] - FINISH_ORDER[b.status] || flagshipSort || a.id - b.id;
      }
      return flagshipSort || a.id - b.id;
    });

  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-12">
        <div className="col-span-12 lg:col-span-8">
          <Kicker variant="crimson">Research Briefs - status and chart view</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,5rem)] mt-3">
            Every topic,{" "}
            <span className="display-italic" style={{ color: "var(--crimson)" }}>
              plainly
            </span>
            .
          </h1>
          <p className="lede mt-6 max-w-[62ch]">
            One research brief per topic: finish state, main claim, chart,
            source stack, caveat, current unit, target policy unit, and next
            step. Country screens are treated as triage; the serious research
            path is province, district, municipality, grid, facility, corridor,
            and road-segment granularity. Register snapshot as of{" "}
            {ISSUE_CLOSURE_AS_OF}: {issueClosureDeck}
          </p>
        </div>
        <aside className="col-span-12 lg:col-span-4 lg:pl-6 lg:border-l lg:border-[var(--rule-soft)]">
          <Kicker>Current issue state</Kicker>
          <div className="grid grid-cols-2 gap-5 mt-5">
            <StatBlock label="Classified" value={issueTotal} note="All registered current-issue topics now have an explicit finish state." />
            {issueStatusCards.map((card) => (
              <StatBlock key={card.key} label={card.label} value={card.count} note={card.note} />
            ))}
          </div>
        </aside>
      </header>

      <SubnationalLayer />

      <div className="flex flex-wrap items-center gap-3 mb-10">
        <Kicker>Filter</Kicker>
        {FILTERS.map((item) => (
          <button
            key={item.key}
            type="button"
            aria-pressed={filter === item.key}
            onClick={() => setFilter(item.key)}
            className={
              "px-3 py-2 border font-mono text-xs uppercase tracking-[0.16em] transition-colors " +
              (filter === item.key
                ? "bg-ink text-paper border-ink"
                : "border-[var(--rule)] text-ink-faint hover:text-ink hover:border-ink")
            }
          >
            {item.label}
          </button>
        ))}
        <Link href="/research" className="ml-auto ed-link text-sm uppercase tracking-[0.16em] font-mono">
          Program index
        </Link>
        <Link href="/data/upgrades" className="ed-link text-sm uppercase tracking-[0.16em] font-mono">
          Data upgrades
        </Link>
      </div>

      <Divider />

      <div className="space-y-16">
        {visible.map((program) => {
          const detail = BRIEF_DETAILS[program.slug];
          const chart = charts[program.slug];
          return (
            <section
              key={program.slug}
              id={program.slug}
              className="grid grid-cols-12 gap-6 lg:gap-10 pb-16 border-b border-[var(--rule-soft)] scroll-mt-8"
            >
              <div className="col-span-12 lg:col-span-3">
                <div className="lg:sticky lg:top-8">
                  <Numeral n={program.id} />
                  <div className="mt-4 flex flex-wrap gap-2">
                    <Maturity status={program.status} />
                    {detail.flagship && <Chip variant="ochre">Flagship paper</Chip>}
                  </div>
                  <div className="mt-5 marginalia">
                    {detail.domain}
                    <br />
                    {program.slug}
                  </div>
                </div>
              </div>

              <div className="col-span-12 lg:col-span-5">
                <Kicker variant="sage">One-page brief</Kicker>
                <h2 className="display-lg text-[clamp(1.7rem,3vw,2.6rem)] mt-3">
                  {program.title}
                </h2>
                <div className="mt-7 space-y-5">
                  <BriefLine label="Question" text={detail.question} />
                  <BriefLine label="Current output" text={detail.output} />
                  <BriefLine label="Source stack" text={detail.sourceNote} />
                  <BriefLine label="Caveat" text={detail.caveat} />
                  <BriefLine label="Next step" text={detail.nextStep} />
                </div>
                <GranularityPanel detail={detail.granularity} />
                <div className="mt-7 flex flex-wrap gap-3">
                  {detail.articleSlug && (
                    <Link href={`/${program.slug}`}
                      className="ed-link text-sm uppercase tracking-[0.16em] font-mono"
                    >
                      Read write-up
                    </Link>
                  )}
                  <Link href={`/${program.slug}?view=evidence`}
                    className="ed-link text-sm uppercase tracking-[0.16em] font-mono"
                  >
                    Evidence packet
                  </Link>
                </div>
              </div>

              <div className="col-span-12 lg:col-span-4">
                <div className="border-t border-[var(--ink)] pt-4">
                  <Kicker>{detail.chartTitle}</Kicker>
                  <div className="mt-5">
                    {chart ? (
                      <>
                        <BriefBarChart rows={chart.rows} unit={chart.unit} />
                        <p className="marginalia mt-3">
                          Bars show the highest observed values in the current
                          public-data artifact. A chart is not a ranking claim
                          unless the brief says the set is stable.
                        </p>
                      </>
                    ) : (
                      <div className="min-h-[250px] border border-[var(--rule-soft)] p-6 flex flex-col justify-between bg-paper-deep">
                        <div>
                          <div className="display-md text-[1.4rem]">No computed chart yet.</div>
                          <p className="mt-3 text-ink-soft leading-relaxed">
                            This topic is not ready for visual headline
                            treatment because the empirical layer is not yet
                            complete in this repository.
                          </p>
                        </div>
                        <p className="marginalia mt-8">{detail.nextStep}</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function SubnationalLayer() {
  const sourceLinks = ROAD_QUALITY_NEXT_TRACK.sources;

  return (
    <section className="mb-10 border-y border-[var(--ink)] py-7">
      <div className="grid grid-cols-12 gap-6 lg:gap-10 items-start">
        <div className="col-span-12 lg:col-span-4">
          <Kicker variant="crimson">Subnational measurement layer</Kicker>
          <h2 className="display-md text-[clamp(1.55rem,3vw,2.15rem)] mt-3 max-w-[12ch]">
            Granularity is the research claim.
          </h2>
          <p className="mt-4 text-ink-soft leading-relaxed max-w-prose">
            The page now separates the country-level screen from the policy
            unit a researcher would actually trust: district, city, grid,
            facility catchment, corridor, market, household group, or road
            segment.
          </p>
        </div>

        <div className="col-span-12 lg:col-span-4">
          <Kicker variant="sage">Policy unit ladder</Kicker>
          <div className="mt-5 space-y-3">
            {["Country screen", "ADM1/ADM2", "Grid or settlement", "Facility, corridor, road segment"].map(
              (step, index) => (
                <div key={step} className="grid grid-cols-[2.25rem_1fr] gap-3 items-center">
                  <div className="font-mono text-xs text-center py-2 border border-[var(--rule)] bg-paper-deep">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-mono text-[0.72rem] uppercase tracking-[0.12em] text-ink">
                      {step}
                    </div>
                    <div className="mt-1 h-1 bg-[var(--rule-soft)]">
                      <div
                        className="h-1 bg-[var(--sage)]"
                        style={{ width: `${35 + index * 20}%` }}
                      />
                    </div>
                  </div>
                </div>
              ),
            )}
          </div>
        </div>

        <div className="col-span-12 lg:col-span-4 border-l-0 lg:border-l lg:border-[var(--rule-soft)] lg:pl-6">
          <div className="flex flex-wrap gap-2 items-center">
            <Kicker variant="ochre">Next-track candidate</Kicker>
            <Chip variant="ochre">Not in current count</Chip>
          </div>
          <h3 className="display-md text-[clamp(1.35rem,2.5vw,1.85rem)] mt-3">
            {ROAD_QUALITY_NEXT_TRACK.title}
          </h3>
          <div className="mt-5 space-y-4">
            <BriefLine label="Current unit" text={ROAD_QUALITY_NEXT_TRACK.currentUnit} />
            <BriefLine label="Target policy unit" text={ROAD_QUALITY_NEXT_TRACK.targetUnit} />
            <BriefLine label="Granularity gap" text={ROAD_QUALITY_NEXT_TRACK.gap} />
            <BriefLine label="Data needed" text={ROAD_QUALITY_NEXT_TRACK.upgradeData} />
            <BriefLine label="ADB method" text={ROAD_QUALITY_NEXT_TRACK.adbMethod} />
            <BriefLine label="ML stack" text={ROAD_QUALITY_NEXT_TRACK.modelStack} />
            <BriefLine label="Validation" text={ROAD_QUALITY_NEXT_TRACK.validation} />
            <BriefLine label="Research limit" text={ROAD_QUALITY_NEXT_TRACK.limitation} />
          </div>
          <div className="mt-5 flex flex-wrap gap-x-4 gap-y-2">
            {sourceLinks.map((source) => (
              <a
                key={source.href}
                href={source.href}
                target="_blank"
                rel="noreferrer"
                className="ed-link text-xs uppercase tracking-[0.14em] font-mono"
              >
                {source.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function GranularityPanel({ detail }: { detail: BriefDetail["granularity"] }) {
  return (
    <div className="mt-7 border-l-2 border-[var(--sage)] bg-paper-deep px-5 py-4">
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <Kicker variant="sage">Granularity</Kicker>
        <Chip variant="sage">Subnational path</Chip>
      </div>
      <div className="grid sm:grid-cols-2 gap-x-5 gap-y-4">
        <BriefLine label="Current unit" text={detail.currentUnit} />
        <BriefLine label="Target policy unit" text={detail.targetUnit} />
        <BriefLine label="Granularity gap" text={detail.gap} />
        <BriefLine label="Data needed to go lower" text={detail.upgradeData} />
      </div>
    </div>
  );
}

function BriefLine({ label, text }: { label: string; text: string }) {
  return (
    <div>
      <div className="kicker mb-1">{label}</div>
      <p className="text-ink-soft leading-relaxed max-w-prose">{text}</p>
    </div>
  );
}

function BriefBarChart({
  rows,
  unit,
}: {
  rows: Array<{ label: string; value: number; highlight?: boolean }>;
  unit: string;
}) {
  const max = Math.max(...rows.map((row) => row.value), 1);
  return (
    <div className="border border-[var(--rule-soft)] bg-paper p-4">
      <div className="space-y-3">
        {rows.map((row) => {
          const width = `${Math.max(3, (row.value / max) * 100)}%`;
          return (
            <div key={row.label}>
              <div className="flex items-baseline justify-between gap-4 mb-1">
                <div className="font-mono text-[0.68rem] uppercase tracking-[0.08em] text-ink-soft truncate">
                  {row.label}
                </div>
                <div className="font-mono text-[0.7rem] tabular text-ink whitespace-nowrap">
                  {formatChartValue(row.value)}
                  {unit ? ` ${unit}` : ""}
                </div>
              </div>
              <div className="h-3 bg-[var(--rule-soft)]">
                <div
                  className="h-3"
                  style={{
                    width,
                    background: row.highlight ? "var(--crimson)" : "var(--ink)",
                    opacity: row.highlight ? 1 : 0.78,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function formatChartValue(value: number) {
  if (value >= 1000) return Math.round(value).toLocaleString();
  if (value >= 100) return value.toFixed(0);
  if (value >= 10) return value.toFixed(1);
  return value.toFixed(2).replace(/\.?0+$/, "");
}

function buildChartPack(def: IndicatorDef, rows: IndicatorRow[]): ChartPack {
  const valid = rows.filter((row): row is IndicatorRow & { value: number } => row.value !== null);
  valid.sort((a, b) => (def.higherIsWorse ? b.value - a.value : a.value - b.value));
  const unit = displayUnit(def);
  return {
    def,
    unit,
    rows: valid.slice(0, 6).map((row, index) => ({
      label: labelForRow(row),
      value: displayValue(def, row.value),
      highlight: index === 0,
    })),
  };
}

function labelForRow(row: IndicatorRow) {
  const country = row.raw?.country;
  if (typeof country === "string") return country.length > 18 ? row.iso3 : country;
  return row.iso3;
}

function displayValue(def: IndicatorDef, value: number) {
  if (def.metricLabel === "Emigrant stock 2024") return value / 1_000_000;
  if (def.programSlug === "public-service-data-quality") return value;
  return value;
}

function displayUnit(def: IndicatorDef) {
  if (def.metricLabel === "Emigrant stock 2024") return "M";
  if (def.programSlug === "public-service-data-quality") return "%";
  if (def.unit === "people") return "";
  return def.unit;
}
