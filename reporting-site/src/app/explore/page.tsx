import type { Metadata } from "next";
import Link from "next/link";
import "@/components/shells/shells.css";
import { SHELL_META, type ShellId } from "@/components/shells/types";

export const metadata: Metadata = {
  title: "Explore reader shells",
  description:
    "Side-by-side Product, Workbench, and Chapter presentations of the same evidence package.",
};

const PILOTS: Array<{
  slug: string;
  family: string;
  defaultShell: ShellId;
  label: string;
}> = [
  {
    slug: "public-data-freshness",
    family: "observability",
    defaultShell: "product",
    label: "Two clocks (data freshness)",
  },
  {
    slug: "public-service-data-quality",
    family: "observability",
    defaultShell: "workbench",
    label: "Health map disagreement",
  },
  {
    slug: "climate-health-workdays",
    family: "invalidation",
    defaultShell: "product",
    label: "PM2.5 proxy vs heat loss",
  },
  {
    slug: "remittance-resilience",
    family: "distribution",
    defaultShell: "product",
    label: "Remittance dependence × cost",
  },
];

const FAMILY_TABLE: Array<{
  program: string;
  family: string;
  defaultShell: ShellId;
  note: string;
}> = [
  {
    program: "public-service-data-quality",
    family: "observability",
    defaultShell: "workbench",
    note: "Registry–map disagreement",
  },
  {
    program: "air-monitoring",
    family: "observability",
    defaultShell: "workbench",
    note: "Station QA observability zeros",
  },
  {
    program: "access-services",
    family: "observability",
    defaultShell: "workbench",
    note: "OSM vs registry ranks",
  },
  {
    program: "public-data-freshness",
    family: "observability",
    defaultShell: "product",
    note: "Pilot · two clocks",
  },
  {
    program: "climate-health-workdays",
    family: "invalidation",
    defaultShell: "product",
    note: "Proxy fails heat signal",
  },
  {
    program: "disaster-recovery-lag",
    family: "invalidation",
    defaultShell: "product",
    note: "Ranking fails validity gates",
  },
  {
    program: "grid-reliability-heat",
    family: "invalidation",
    defaultShell: "product",
    note: "Regional measurement wall",
  },
  {
    program: "school-heat-disruption",
    family: "invalidation",
    defaultShell: "product",
    note: "Proxy vs observed heat",
  },
  {
    program: "social-protection-shock-coverage",
    family: "invalidation",
    defaultShell: "product",
    note: "Missing-data fixed ranking",
  },
  {
    program: "water-stress-crop-diversification",
    family: "invalidation",
    defaultShell: "product",
    note: "Top four fails own measures",
  },
  {
    program: "port-hinterland-friction",
    family: "invalidation",
    defaultShell: "product",
    note: "Trade volume vs delay",
  },
  {
    program: "food-price-climate-transmission",
    family: "invalidation",
    defaultShell: "product",
    note: "Spikes vs dry rainfall",
  },
  {
    program: "remittance-resilience",
    family: "distribution",
    defaultShell: "product",
    note: "Dependence + corridor costs",
  },
  {
    program: "migration-displacement-signals",
    family: "distribution",
    defaultShell: "product",
    note: "Per-capita origin switch",
  },
  {
    program: "coastal-informal-risk",
    family: "distribution",
    defaultShell: "product",
    note: "Low-elevation growth",
  },
  {
    program: "flood-market-access",
    family: "distribution",
    defaultShell: "product",
    note: "Flood cuts market access",
  },
  {
    program: "digital-performance",
    family: "distribution",
    defaultShell: "product",
    note: "Coverage vs use gap",
  },
  {
    program: "invisible-urbanization",
    family: "distribution",
    defaultShell: "product",
    note: "Urban share disagreement",
  },
];

export default function ExploreHubPage() {
  return (
    <div className="shell-page explore-hub">
      <div>
        <div className="product-kicker">Exploration · not production yet</div>
        <h1>Three shells, one evidence package</h1>
        <p>
          Four live story packages — one per evidence family — share the same
          three shells. Production topics with a <code>story.json</code> now
          open in their default shell; use <code>?view=classic</code> for the
          old tabbed UI. Task31 is the quality bar for Chapter only.
        </p>
      </div>

      <section>
        <h2 className="product-kicker" style={{ marginBottom: "0.75rem" }}>
          Live pilots (default shell)
        </h2>
        <div className="explore-cards">
          {PILOTS.map((pilot) => (
            <Link
              key={pilot.slug}
              href={`/explore/${pilot.defaultShell}/${pilot.slug}`}
              className="explore-card"
            >
              <b>{pilot.label}</b>
              <span>
                {pilot.family} · default {SHELL_META[pilot.defaultShell].label}
              </span>
              <em>
                Open default shell → · also /{pilot.slug}
              </em>
            </Link>
          ))}
        </div>
      </section>

      <section>
        <h2 className="product-kicker" style={{ marginBottom: "0.75rem" }}>
          Shells (same package, different UI)
        </h2>
        <div className="explore-cards">
          {(Object.keys(SHELL_META) as ShellId[]).map((id) => (
            <Link
              key={id}
              href={`/explore/${id}/public-data-freshness`}
              className="explore-card"
            >
              <b>{SHELL_META[id].label}</b>
              <span>{SHELL_META[id].blurb}</span>
              <em>Try on two-clocks pilot →</em>
            </Link>
          ))}
        </div>
      </section>

      <section className="explore-critique">
        <h2 className="product-kicker">Why the live topic UI feels weak</h2>
        <article>
          <h3>Same shell for unlike findings</h3>
          <p>
            Observability zeros, ranking invalidation, and corridor maps all
            wear Overview / Paper / Brief / Blog / Slides / Data / Evidence.
            The first interaction should match the claim shape.
          </p>
        </article>
        <article>
          <h3>Audit before argument</h3>
          <p>
            Attestation codes and file inventories compete with the finding in
            the first viewport. DESIGN.md already wants finding → hero →
            limits → ledger; the page still opens like a lab notebook.
          </p>
        </article>
        <article>
          <h3>Task31 is a quality bar, not a universal layout</h3>
          <p>
            A dramatic long-form chapter is right for synthesis. It is wrong
            as the only costume for a short screening result or a
            filterable disagreement table.
          </p>
        </article>
      </section>

      <section>
        <h2 className="product-kicker" style={{ marginBottom: "0.75rem" }}>
          Proposed family → default shell
        </h2>
        <div className="workbench-table-wrap">
          <table className="explore-table">
            <thead>
              <tr>
                <th>Program</th>
                <th>Family</th>
                <th>Default shell</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              {FAMILY_TABLE.map((row) => (
                <tr key={row.program}>
                  <td>
                    <code>{row.program}</code>
                  </td>
                  <td>{row.family}</td>
                  <td>{row.defaultShell}</td>
                  <td>{row.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <p className="product-nonclaim">
        Topics with a story package now render shells by default. Classic
        tabbed UI remains at <code>?view=evidence</code>,{" "}
        <code>?view=data</code>, or <code>?view=classic</code>. Example:{" "}
        <Link href="/public-data-freshness">/public-data-freshness</Link>{" "}
        (shell) vs{" "}
        <Link href="/public-data-freshness?view=classic">
          /public-data-freshness?view=classic
        </Link>
        .
      </p>
    </div>
  );
}
