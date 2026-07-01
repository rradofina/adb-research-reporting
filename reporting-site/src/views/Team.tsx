"use client";

import Link from "next/link";
import { Kicker, Divider, Numeral } from "../components/ui";

export default function Team() {
  return (
    <div className="reveal">
      <header className="grid grid-cols-12 gap-6 mb-14">
        <div className="col-span-12 md:col-span-8">
          <Kicker variant="sage">Team — masthead</Kicker>
          <h1 className="masthead-display text-[clamp(2.6rem,6vw,5rem)] mt-3">
            Who reads this{" "}
            <span className="display-italic" style={{ color: "var(--sage)" }}>
              before
            </span>{" "}
            you do.
          </h1>
          <p className="lede mt-7 max-w-[58ch]">
            Authors, supervisors, and the external red team. Current-issue
            AI-first work discloses synthesized review. Human-final
            publication claims require named external readers spanning
            measurement, domain, and statistical expertise.
          </p>
        </div>
      </header>

      <Divider />

      {/* Authors */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Kicker>Authors</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-9 grid sm:grid-cols-2 gap-px bg-[var(--rule-soft)]">
          <Person
            n={1}
            name="Raymond Adofina"
            role="Lead author"
            affiliation="Asian Development Bank"
            bio="Data analyst at ADB. MSCI background. Designed and writes the program register; co-author with Arturo Martinez Jr on the MPI × nighttime-lights track."
          />
          <Person
            n={2}
            name="Arturo Martinez Jr"
            role="Co-author (legacy track)"
            affiliation="Asian Development Bank"
            bio="Co-author on the MPI × NTL decomposition program (Program 0). The legacy program predates the broader Blindspots Lab register and remains an active collaboration."
          />
        </div>
      </section>

      <Divider />

      {/* Red team */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-12">
        <header className="col-span-12 lg:col-span-3">
          <Kicker variant="crimson">External red team</Kicker>
          <p className="marginalia mt-3">
            Roster sourced per Constitution §9.3. Composition target: 2 measurement, 2 domain, 1 DMC-affiliated reviewer per program before any human-final publication gate.
          </p>
        </header>
        <div className="col-span-12 lg:col-span-9">
          <div className="ed-card p-8">
            <h3 className="display-md text-[1.4rem]">Roster — recruiting</h3>
            <p className="mt-3 text-ink-soft leading-relaxed max-w-prose">
              The human-final red team is empty by design. The Constitution
              requires named, COI-disclosed external reviewers before any
              program advances to human-final publication status. AI cannot
              fabricate names; the repository owner recruits from the
              institutional sources below before that upgrade.
            </p>
            <ul className="mt-6 grid sm:grid-cols-2 gap-x-8 gap-y-3 marginalia">
              <li><span className="kicker-crimson font-mono">M-1</span> &nbsp; OPHI · measurement / capability approach</li>
              <li><span className="kicker-crimson font-mono">M-2</span> &nbsp; UNDP HDRO technical staff</li>
              <li><span className="kicker-crimson font-mono">M-3</span> &nbsp; World Bank DECDG / SPI team</li>
              <li><span className="kicker-crimson font-mono">D-1</span> &nbsp; KEMRI–Wellcome / WorldPop network</li>
              <li><span className="kicker-crimson font-mono">D-2</span> &nbsp; Lancet Countdown · climate-health</li>
              <li><span className="kicker-crimson font-mono">D-3</span> &nbsp; HeiGIT / Zipf — OpenStreetMap data</li>
              <li><span className="kicker-crimson font-mono">DMC</span> &nbsp; PIDS, BIDS, SMERU, PIDE, IPS, SPC</li>
            </ul>
          </div>
        </div>
      </section>

      <Divider />

      {/* Review process */}
      <section className="grid grid-cols-12 gap-6 lg:gap-10 my-16">
        <header className="col-span-12 lg:col-span-3">
          <Kicker>Review process</Kicker>
        </header>
        <div className="col-span-12 lg:col-span-7">
          <ol className="space-y-6 text-ink-soft leading-relaxed">
            {[
              "Self-review: the program owner writes a skeptical-reviewer simulation before any promotion request.",
              "Internal review: ADB-facing outputs reviewed by the supervisor; comments addressed in writing and committed.",
              "External red team: ≥2 readers from the roster, drawn to span measurement, domain, and DMC affiliation; 4-week turnaround.",
              "Publication: claim moves to human-final status only after objections are resolved or quoted verbatim in the limitations section.",
            ].map((step, i) => (
              <li key={i} className="grid grid-cols-12 gap-4">
                <span className="col-span-1"><Numeral n={i + 1} /></span>
                <span className="col-span-11">{step}</span>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <Divider wide />

      <section className="text-center">
        <Kicker>Continue</Kicker>
        <div className="mt-4 flex flex-wrap justify-center gap-4">
          <Link href="/about#governance" className="ed-link">Constitution highlights</Link>
          <Link href="/about#reproducibility" className="ed-link">Reproducibility</Link>
          <Link href="/about#ai" className="ed-link">AI transparency</Link>
        </div>
      </section>
    </div>
  );
}

function Person({
  n,
  name,
  role,
  affiliation,
  bio,
}: {
  n: number;
  name: string;
  role: string;
  affiliation: string;
  bio: string;
}) {
  return (
    <div className="bg-paper p-8">
      <div className="flex items-baseline gap-4 mb-3">
        <Numeral n={n} />
        <span className="kicker">{role}</span>
      </div>
      <h3 className="display-md text-[1.6rem]">{name}</h3>
      <div className="marginalia mt-1">{affiliation}</div>
      <p className="mt-4 text-ink-soft leading-relaxed">{bio}</p>
    </div>
  );
}
