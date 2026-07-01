"use client";

import Link from "next/link";
import { Kicker, Divider } from "../components/ui";

interface Term {
  term: string;
  expansion?: string;
  body: string;
  see?: { label: string; to: string }[];
}

const TERMS: Term[] = [
  { term: "ADB", expansion: "Asian Development Bank", body: "Multilateral development bank serving 50 regional developing member economies plus 19 non-regional members. The lab's research scope is the 50 regional DMCs." },
  { term: "DMC", expansion: "Developing Member Country / Country", body: "ADB's term for the 50 regional economies it serves. Used throughout the lab's framing.", see: [{ label: "Atlas (all 45 covered)", to: "/atlas" }] },
  { term: "ADM1, ADM2", body: "Administrative-division levels. ADM1 = first-level subdivision (PHL: 17 regions; BGD: 8 divisions; IND: 28+ states); ADM2 = second-level (PHL: 81 provinces; etc.)." },
  { term: "PR", expansion: "Internal Publication-Ready code", body: "Public UI label: Finished for current issue. Full current-issue evidence package is complete for the stated attestation chain; human-final publication status requires the §18.5 upgrade path.", see: [{ label: "Methods", to: "/methods" }] },
  { term: "SR", expansion: "Screening Result", body: "Pipeline ran; output is preliminary triage. Quotable with caveats from limitations.md. Not policy-actionable.", see: [{ label: "Reader's guide §2", to: "/how-to-read" }] },
  { term: "PP", expansion: "Prepared Pipeline", body: "Script runs end-to-end; nothing has been concluded yet." },
  { term: "H", expansion: "Hypothesis", body: "An idea or proposed metric. Not a finding." },
  { term: "ai-first", body: "Attestation chain under Constitution §18. Gate actions are AI-attested and disclosed rather than implied as human-final. Currently the 16 finished or screening programs in this issue use this chain.", see: [{ label: "Reader's guide §3", to: "/how-to-read" }] },
  { term: "human-final", body: "Attestation chain. Every gate-action by the human owner per the pre-§18 Constitution. Currently zero programs." },
  { term: "Constitution", body: "The lab's binding governing document. 18 sections covering principles, problem selection, originality, methods, scope, claim maturity, review, publication, ethics, taste, AI assistance.", see: [{ label: "About — Governance", to: "/about#governance" }] },
  { term: "§18 ACTIVE", body: "Constitution §18 (AI-First Operating Mode) is currently toggled ON. AI executes gate-actions previously reserved to the human owner; every artifact carries `attestation_chain: ai-first`. Revertible by a single commit." },
  { term: "Sensitivity at ±50%", body: "Constitution §6.6. Every arbitrary numeric (threshold, weight, buffer, cutoff) in a program's index formula is tested at half and 1.5× its baseline value. The headline claim must survive every perturbation row." },
  { term: "WDI", expansion: "World Development Indicators", body: "World Bank's reference dataset of country-level development indicators. 1500+ series; CC BY 4.0; the lab's primary source for many programs." },
  { term: "OSM", expansion: "OpenStreetMap", body: "Volunteer-mapped global geospatial database. Used as a comparator against official registries in PSDQ. License ODbL." },
  { term: "NHFR", expansion: "National Health Facility Registry (Philippines)", body: "DOH-operated registry of 44,267 active health facilities (2026-04-25 retrieval). Used in PSDQ as the official-side comparator against OSM." },
  { term: "DGHS", expansion: "Directorate General of Health Services (Bangladesh)", body: "Public dashboard of 39,421 active facilities. PSDQ-BGD official-side comparator." },
  { term: "RPW", expansion: "Remittance Prices Worldwide", body: "World Bank quarterly dataset of corridor-firm-period transfer-cost observations. ~198,000 globally; the remittance-resilience program's source." },
  { term: "ASPIRE", body: "World Bank Atlas of Social Protection Indicators of Resilience and Equity. Source for SP-coverage indicators in social-protection-shock-coverage." },
  { term: "Findex", body: "World Bank Global Findex Database. Account-ownership and financial-inclusion indicators. 2021 vintage was elevated by pandemic emergency cash transfers." },
  { term: "EM-DAT", body: "International Disaster Database (CRED, UCLouvain). Disaster events with ≥10 deaths or ≥100 affected or declared emergency. 1767 ADB-DMC events 2000–2025." },
  { term: "LPI", expansion: "Logistics Performance Index", body: "World Bank perception-based survey of logistics quality. Used in port-hinterland-friction." },
  { term: "PM2.5", body: "Atmospheric particulate matter ≤2.5 µm. WHO 2021 annual-mean guideline 5 µg/m³. Used in climate-health-workdays as the pollution-exposure axis." },
  { term: "WRI Global Power Plant Database", body: "World Resources Institute plant-level power generation database. v1.3.0 (2022 freeze). 7,071 ADB-DMC plants; used in grid-reliability-heat." },
  { term: "Permanent archive (§10.3)", body: "Self-hosted at /program/{slug}/evidence on the reporting site. The URL plus the publication commit SHA is the citation handle. Replaced mandatory Zenodo as of the 2026-04-26 amendment.", see: [{ label: "/archive", to: "/archive" }] },
  { term: "Attestation chain", body: "Field on every artifact's frontmatter. Records who attested the gates: ai-first, human-final, or mixed. §18.2 makes it mandatory." },
  { term: "§18.5 upgrade-pass", body: "The path that converts an ai-first artifact to mixed or human-final: owner reads literature, freezes pre-registration, recruits reviewers, signs commits. Each program's review-external.md §5 documents the specific scope." },
  { term: "Honest narrowing", body: "When the original claim fails the ±50% sensitivity gate, the article narrows to the subset that does survive (e.g., school-heat top-1 only; water-crop top-4 only). Documented in pre-registration.md §8 decision rule." },
];

export default function Glossary() {
  return (
    <div className="reveal">
      <header className="mb-12 pb-8 border-b border-[var(--rule)]">
        <Kicker>Glossary</Kicker>
        <h1 className="masthead-display text-[clamp(2.4rem,5vw,4.6rem)] mt-3">
          The{" "}
          <span className="display-italic" style={{ color: "var(--ink-faint)" }}>
            terms
          </span>{" "}
          you'll meet.
        </h1>
        <p className="lede mt-7 max-w-[60ch]">
          Every acronym, every claim-maturity tier, every Constitutional section
          referenced on the site. Read top-to-bottom or jump in.
        </p>
      </header>

      <ul className="space-y-8 max-w-[68ch]">
        {TERMS.map((t) => (
          <li key={t.term} className="border-b border-[var(--rule-soft)] pb-6">
            <div className="flex items-baseline gap-3 flex-wrap">
              <span className="display-md text-[1.4rem]" style={{ color: "var(--crimson)" }}>
                {t.term}
              </span>
              {t.expansion && (
                <span className="font-mono text-sm text-ink-faint">{t.expansion}</span>
              )}
            </div>
            <p className="mt-2 text-ink-soft leading-relaxed">{t.body}</p>
            {t.see && t.see.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-3 marginalia">
                {t.see.map((s) => (
                  <Link key={s.to} href={s.to} className="ed-link">
                    → {s.label}
                  </Link>
                ))}
              </div>
            )}
          </li>
        ))}
      </ul>

      <Divider wide />

      <nav className="flex items-center justify-between flex-wrap gap-4 pb-12">
        <Link href="/how-to-read" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          ← Reader's guide
        </Link>
        <Link href="/findings" className="ed-link font-mono text-xs uppercase tracking-[0.18em]">
          Findings →
        </Link>
      </nav>
    </div>
  );
}
