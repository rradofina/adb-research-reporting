import Link from "next/link";
import { getReproducibilityProfile } from "@/data/reproducibility";

export function ReproducibilityPanel({ slug }: { slug: string }) {
  const profile = getReproducibilityProfile(slug);

  return (
    <section className="border-y border-zinc-800 bg-zinc-950">
      <div className="mx-auto grid max-w-7xl gap-8 px-4 py-14 sm:px-6 lg:grid-cols-[360px_minmax(0,1fr)] lg:px-8">
        <div className="min-w-0">
          <p className="font-mono text-xs uppercase tracking-widest text-emerald-400">
            Reproducibility and AI disclosure
          </p>
          <h2 className="mt-3 text-2xl font-semibold text-white">
            Trust record for this program
          </h2>
          <p className="mt-3 text-sm leading-6 text-zinc-500">
            This section states what can be rerun, what AI helped with, what was
            checked, and what is still not strong enough to claim.
          </p>
          <Link
            href="/methodology/reproducibility"
            className="mt-5 inline-flex text-sm font-medium text-zinc-300 transition-colors hover:text-white"
          >
            Open full reproducibility standard
          </Link>
        </div>

        <div className="min-w-0 space-y-5">
          <div className="grid gap-4 md:grid-cols-3">
            <InfoBlock label="Status" value={profile.status} />
            <InfoBlock label="Claim scope" value={profile.claimScope} />
            <InfoBlock label="Rerun command" value={profile.command} mono />
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <ListBlock title="Inputs" items={profile.inputs} />
            <ListBlock title="Outputs" items={profile.outputs} mono />
            <ListBlock title="Rerun steps" items={profile.rerunSteps} />
            <ListBlock title="AI assistance disclosure" items={profile.aiDisclosure} />
            <ListBlock title="Human checks" items={profile.humanChecks} />
            <ListBlock title="Limits before publication" items={profile.limitations} />
          </div>
        </div>
      </div>
    </section>
  );
}

function InfoBlock({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-4">
      <p className="font-mono text-xs uppercase tracking-wider text-zinc-600">
        {label}
      </p>
      <p
        className={`mt-2 text-sm leading-6 text-zinc-300 ${
          mono ? "font-mono text-xs" : ""
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function ListBlock({
  title,
  items,
  mono,
}: {
  title: string;
  items: string[];
  mono?: boolean;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 p-5">
      <h3 className="font-semibold text-zinc-100">{title}</h3>
      <ul className="mt-4 space-y-3">
        {items.map((item) => (
          <li
            key={item}
            className={`text-sm leading-6 text-zinc-500 ${
              mono ? "font-mono text-xs" : ""
            }`}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
