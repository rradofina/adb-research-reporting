"use client";

import Link from "next/link";
import { Chip, Divider, Kicker, Maturity, Numeral, StatBlock } from "../components/ui";
import { BRIEF_DETAILS, FINISH_LABELS } from "../data/briefs";
import { programs } from "../data/programs";
import {
  PRIORITY_META,
  ROAD_QUALITY_UPGRADE,
  SOURCE_UPGRADES,
  type SourceUpgrade,
  type UpgradePriority,
} from "../data/sourceUpgrades";

const PRIORITY_ORDER: UpgradePriority[] = ["P1", "P2", "P3", "Watch"];

export default function DataUpgrades() {
  const rows = programs
    .map((program) => {
      const detail = BRIEF_DETAILS[program.slug];
      const upgrade = SOURCE_UPGRADES.find((item) => item.slug === program.slug);
      if (!detail || !upgrade) return null;
      return { program, detail, upgrade };
    })
    .filter((row): row is NonNullable<typeof row> => row !== null)
    .sort((a, b) => {
      const priority = PRIORITY_META[a.upgrade.priority].weight - PRIORITY_META[b.upgrade.priority].weight;
      return priority || a.program.id - b.program.id;
    });

  const counts = PRIORITY_ORDER.reduce(
    (acc, priority) => {
      acc[priority] = rows.filter((row) => row.upgrade.priority === priority).length;
      return acc;
    },
    {} as Record<UpgradePriority, number>,
  );

  const claimChanging = counts.P1;
  const currentTopics = rows.length;

  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-12">
        <div className="col-span-12 lg:col-span-8">
          <Kicker variant="ochre">Data-source upgrade pass</Kicker>
          <h1 className="masthead-display text-[clamp(2.5rem,6vw,4.8rem)] mt-3">
            What would make the research{" "}
            <span className="display-italic" style={{ color: "var(--ochre)" }}>
              sharper
            </span>
            .
          </h1>
          <p className="lede mt-6 max-w-[66ch]">
            This matrix separates the source list from the research roadmap:
            current source, current unit, better source, better policy unit,
            and priority. The aim is to move strong country screens into
            province, district, municipality, grid, facility, corridor, market,
            household, and road-segment evidence.
          </p>
        </div>
        <aside className="col-span-12 lg:col-span-4 lg:pl-6 lg:border-l lg:border-[var(--rule-soft)]">
          <Kicker>Upgrade state</Kicker>
          <div className="grid grid-cols-2 gap-5 mt-5">
            <StatBlock label="Topics" value={currentTopics} note="Current issue topics covered by the matrix." />
            <StatBlock label="P1" value={claimChanging} note="Claim-changing upgrades before strong subnational claims." />
            <StatBlock label="Next track" value="1" note="Road quality and poverty access kept outside the current count." />
            <StatBlock label="Unit goal" value="ADM2+" note="Lower than national wherever data can support it." />
          </div>
        </aside>
      </header>

      <section className="grid grid-cols-12 gap-6 lg:gap-10 mb-12">
        <div className="col-span-12 lg:col-span-5 border-y border-[var(--ink)] py-6">
          <Kicker variant="crimson">Priority shape</Kicker>
          <div className="mt-6 space-y-4">
            {PRIORITY_ORDER.map((priority) => (
              <PriorityRow key={priority} priority={priority} count={counts[priority]} total={currentTopics} />
            ))}
          </div>
        </div>
        <div className="col-span-12 lg:col-span-7 border-y border-[var(--ink)] py-6">
          <Kicker variant="sage">Reading rule</Kicker>
          <div className="grid sm:grid-cols-3 gap-5 mt-6">
            <RuleCard label="Good now" text="A current screen can be credible even when the next unit is not yet implemented." />
            <RuleCard label="Not enough" text="Country-level WDI signals should not be sold as granular policy evidence." />
            <RuleCard label="Best path" text="Use public source triangulation plus a pinned spatial unit before making strong claims." />
          </div>
        </div>
      </section>

      <section className="mb-10 flex flex-wrap items-center gap-3">
        <Link href="/briefs" className="ed-link text-sm uppercase tracking-[0.16em] font-mono">
          Research Briefs
        </Link>
        <Link href="/data" className="ed-link text-sm uppercase tracking-[0.16em] font-mono">
          Data catalog
        </Link>
        <Link href="/data/matrix" className="ed-link text-sm uppercase tracking-[0.16em] font-mono">
          Cross-program matrix
        </Link>
      </section>

      <Divider />

      <section>
        <div className="flex flex-wrap items-end justify-between gap-4 mb-4">
          <div>
            <Kicker>Current topics</Kicker>
            <h2 className="display-lg text-[clamp(1.7rem,3vw,2.5rem)] mt-2">
              Source-to-unit upgrade matrix
            </h2>
          </div>
          <div className="marginalia max-w-[42ch]">
            Priority is editorial, not a quality score. P1 means the better
            data source would materially change the claim a researcher should
            be willing to defend.
          </div>
        </div>

        <div className="overflow-x-auto border-y border-[var(--rule)]">
          <table className="data-table min-w-[1180px]">
            <thead>
              <tr>
                <th>Topic</th>
                <th>Current source</th>
                <th>Current unit</th>
                <th>Better source</th>
                <th>Better unit</th>
                <th>Priority</th>
                <th>Why it matters</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(({ program, detail, upgrade }) => (
                <tr key={program.slug}>
                  <td className="align-top min-w-[210px]">
                    <div className="flex items-baseline gap-3">
                      <Numeral n={program.id} />
                      <div>
                        <Link href={program.href ?? `/program/${program.slug}/evidence`}
                          className="ed-link display-md text-base"
                        >
                          {program.title}
                        </Link>
                        <div className="mt-2 flex flex-wrap gap-2">
                          <Maturity status={program.status} />
                          <Chip variant={priorityTone(upgrade.priority)}>
                            {FINISH_LABELS[detail.finish]}
                          </Chip>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="align-top text-ink-soft max-w-[260px]">{detail.sourceNote}</td>
                  <td className="align-top text-ink-soft max-w-[240px]">{detail.granularity.currentUnit}</td>
                  <td className="align-top max-w-[290px]">
                    <div className="text-ink-soft">{upgrade.betterSource}</div>
                    <SourceLinks links={upgrade.sourceLinks} />
                  </td>
                  <td className="align-top text-ink-soft max-w-[250px]">{upgrade.betterUnit}</td>
                  <td className="align-top min-w-[150px]">
                    <PriorityChip priority={upgrade.priority} />
                  </td>
                  <td className="align-top text-ink-soft max-w-[310px]">{upgrade.rationale}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <Divider wide />

      <NextTrackCard upgrade={ROAD_QUALITY_UPGRADE} />
    </div>
  );
}

function PriorityRow({
  priority,
  count,
  total,
}: {
  priority: UpgradePriority;
  count: number;
  total: number;
}) {
  const meta = PRIORITY_META[priority];
  const width = `${Math.max(4, (count / Math.max(total, 1)) * 100)}%`;
  return (
    <div>
      <div className="flex items-baseline justify-between gap-4">
        <div>
          <PriorityChip priority={priority} />
          <p className="marginalia mt-1">{meta.short}</p>
        </div>
        <div className="font-mono text-sm tabular text-ink">{count}</div>
      </div>
      <div className="mt-2 h-2 bg-[var(--rule-soft)]">
        <div
          className="h-2"
          style={{ width, background: priorityColor(priority) }}
        />
      </div>
    </div>
  );
}

function RuleCard({ label, text }: { label: string; text: string }) {
  return (
    <div className="border-l-2 border-[var(--sage)] bg-paper-deep px-4 py-3">
      <div className="kicker mb-2">{label}</div>
      <p className="text-ink-soft leading-relaxed">{text}</p>
    </div>
  );
}

function NextTrackCard({ upgrade }: { upgrade: SourceUpgrade }) {
  return (
    <section className="grid grid-cols-12 gap-6 lg:gap-10">
      <div className="col-span-12 lg:col-span-3">
        <Kicker variant="ochre">Next-track candidate</Kicker>
        <h2 className="display-md text-[clamp(1.4rem,2.5vw,2rem)] mt-3">
          Road quality and poverty access
        </h2>
        <div className="mt-4">
          <PriorityChip priority={upgrade.priority} />
        </div>
      </div>
      <div className="col-span-12 lg:col-span-9 grid md:grid-cols-2 gap-5">
        <UpgradeBlock label="Better source" text={upgrade.betterSource} links={upgrade.sourceLinks} />
        <UpgradeBlock label="Better unit" text={upgrade.betterUnit} />
        <UpgradeBlock label="Why it matters" text={upgrade.rationale} />
        <UpgradeBlock
          label="Count rule"
          text="This is deliberately outside the 18 current topics. It is a next-track candidate because it can connect ADB road-quality ML, poverty, service access, and climate passability."
        />
      </div>
    </section>
  );
}

function UpgradeBlock({
  label,
  text,
  links,
}: {
  label: string;
  text: string;
  links?: SourceUpgrade["sourceLinks"];
}) {
  return (
    <div className="bg-paper-deep border border-[var(--rule-soft)] p-5">
      <div className="kicker mb-2">{label}</div>
      <p className="text-ink-soft leading-relaxed">{text}</p>
      {links && <SourceLinks links={links} />}
    </div>
  );
}

function SourceLinks({ links }: { links: SourceUpgrade["sourceLinks"] }) {
  return (
    <div className="mt-3 flex flex-wrap gap-x-4 gap-y-2">
      {links.map((link) => (
        <a
          key={link.href}
          href={link.href}
          target="_blank"
          rel="noreferrer"
          className="ed-link font-mono text-[0.68rem] uppercase tracking-[0.12em]"
        >
          {link.label}
        </a>
      ))}
    </div>
  );
}

function PriorityChip({ priority }: { priority: UpgradePriority }) {
  const meta = PRIORITY_META[priority];
  return <Chip variant={meta.tone}>{meta.label}</Chip>;
}

function priorityTone(priority: UpgradePriority) {
  return PRIORITY_META[priority].tone;
}

function priorityColor(priority: UpgradePriority) {
  if (priority === "P1") return "var(--crimson)";
  if (priority === "P2") return "var(--ochre)";
  if (priority === "P3") return "var(--sage)";
  return "var(--ink)";
}
