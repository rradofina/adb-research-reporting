"use client";

import Link from "next/link";
import {
  ISSUE_CLOSURE_AS_OF,
  issueClosureDeck,
  issueStatusCards,
} from "../data/issueClosure";
import { programs } from "../data/programs";
import { Numeral, Kicker, Maturity, Divider, StatBlock } from "../components/ui";

const DOMAIN_MAP: Record<string, { domain: string; description: string }> = {
  "mpi-nighttime-lights": {
    domain: "Poverty",
    description: "Multidimensional poverty × satellite economic activity.",
  },
  "access-services": {
    domain: "Access",
    description: "Climate-adjusted travel-time access to clinics, schools, markets.",
  },
  "digital-performance": {
    domain: "Connectivity",
    description: "Measured speed × population-weighted digital usability.",
  },
  "air-monitoring": {
    domain: "Environment",
    description: "Pollution exposure where ground monitoring is sparse or stale.",
  },
  "invisible-urbanization": {
    domain: "Built form",
    description: "Settlement growth before official urban classification follows.",
  },
  "climate-health-workdays": {
    domain: "Health",
    description: "Heat and pollution as hidden labor productivity loss.",
  },
  "coastal-informal-risk": {
    domain: "Built form",
    description: "Recorded population and built-up growth inside low-elevation urban-centre footprints.",
  },
  "disaster-recovery-lag": {
    domain: "Disaster",
    description: "Post-disaster recovery hidden by national rebound indicators.",
  },
  "flood-market-access": {
    domain: "Access",
    description: "Observed flood water, historical roads, mapped markets, and population joined into a routed access pilot.",
  },
  "food-price-climate-transmission": {
    domain: "Food",
    description: "Local climate anomalies transmitting into food-price stress.",
  },
  "grid-reliability-heat": {
    domain: "Energy",
    description: "Electricity reliability stress hidden by high connection rates.",
  },
  "migration-displacement-signals": {
    domain: "Migration",
    description: "Public-data signals of climate-linked mobility pressure.",
  },
  "port-hinterland-friction": {
    domain: "Trade",
    description: "Inland exposure to fragile trade and food-logistics paths.",
  },
  "public-service-data-quality": {
    domain: "Measurement",
    description: "Where public maps and admin registries diverge enough to mislead planning.",
  },
  "remittance-resilience": {
    domain: "Finance",
    description: "Remittances as informal shock-absorbers, with corridor friction.",
  },
  "school-heat-disruption": {
    domain: "Education",
    description: "Heat pressure on learning time and school usability.",
  },
  "social-protection-shock-coverage": {
    domain: "Social protection",
    description: "Shock exposure versus payment-system readiness.",
  },
  "water-stress-crop-diversification": {
    domain: "Environment",
    description: "Water stress combined with crop concentration and rural exposure.",
  },
};

export default function Research() {
  // Group programs by domain
  const grouped = new Map<string, typeof programs>();
  for (const p of programs) {
    const meta = DOMAIN_MAP[p.slug];
    const key = meta?.domain ?? "Other";
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key)!.push(p);
  }

  const orderedDomains = [
    "Measurement",
    "Poverty",
    "Health",
    "Education",
    "Environment",
    "Energy",
    "Disaster",
    "Food",
    "Access",
    "Built form",
    "Connectivity",
    "Trade",
    "Migration",
    "Finance",
    "Social protection",
    "Other",
  ];

  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-12">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="crimson">Index — programs</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,4.6rem)] mt-3">
            Eighteen programs.{" "}
            <span className="display-italic" style={{ color: "var(--crimson)" }}>
              Clear status.
            </span>
          </h1>
          <p className="lede mt-6 max-w-[60ch]">
            Each program targets a different measurement gap, but the
            reader should never have to guess whether it is publication-ready,
            screening-only, pipeline-only, or still a hypothesis. Program
            register snapshot as of {ISSUE_CLOSURE_AS_OF}:{" "}
            {issueClosureDeck}
          </p>
          <Link href="/briefs"
            className="mt-7 inline-flex ed-link text-sm uppercase tracking-[0.18em] font-mono"
          >
            Open research briefs
          </Link>
        </div>
        <div className="col-span-12 md:col-span-4 md:pl-6 md:border-l md:border-[var(--rule-soft)] marginalia">
          <div className="grid grid-cols-2 gap-5">
            {issueStatusCards.map((card) => (
              <StatBlock key={card.key} label={card.label} value={card.count} />
            ))}
          </div>
        </div>
      </header>

      <Divider />

      {orderedDomains.map((domain) => {
        const list = grouped.get(domain);
        if (!list || list.length === 0) return null;
        return (
          <section key={domain} className="grid grid-cols-12 gap-6 lg:gap-10 py-12 border-b border-[var(--rule-soft)]">
            <header className="col-span-12 lg:col-span-3 lg:sticky lg:top-8 self-start">
              <Kicker variant="sage">Domain</Kicker>
              <h2 className="display-md text-[1.8rem] mt-2">{domain}</h2>
              <p className="mt-3 marginalia">{list.length} program{list.length === 1 ? "" : "s"}</p>
            </header>

            <div className="col-span-12 lg:col-span-9">
              <ul className="divide-y divide-[var(--rule-soft)]">
                {list.map((p) => {
                  const meta = DOMAIN_MAP[p.slug];
                  const Wrap = ({ children }: any) => (
                    <Link href={`/${p.slug}`}
                      className="group block py-7 -mx-2 px-2 transition-colors hover:bg-paper-deep"
                    >
                      {children}
                    </Link>
                  );
                  return (
                    <li key={p.slug}>
                      <Wrap>
                        <div className="grid grid-cols-12 gap-4 items-baseline">
                          <div className="col-span-12 sm:col-span-1">
                            <Numeral n={p.id} />
                          </div>
                          <div className="col-span-12 sm:col-span-9">
                            <h3 className="display-md text-[clamp(1.2rem,1.8vw,1.6rem)] group-hover:text-crimson transition-colors">
                              {p.title}
                            </h3>
                            <p className="mt-2 text-ink-soft max-w-prose leading-relaxed">
                              {meta?.description ?? p.summary}
                            </p>
                            {p.summary && p.summary !== meta?.description && (
                              <p className="mt-2 marginalia max-w-prose">
                                {p.summary}
                              </p>
                            )}
                          </div>
                          <div className="col-span-12 sm:col-span-2 sm:text-right">
                            <Maturity status={p.status} />
                          </div>
                        </div>
                      </Wrap>
                    </li>
                  );
                })}
              </ul>
            </div>
          </section>
        );
      })}
    </div>
  );
}
