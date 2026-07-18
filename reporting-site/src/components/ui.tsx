import Link from "next/link";
import type { ReactNode, CSSProperties } from "react";

/** Editorial number marker, e.g. "№ 03" */
export function Numeral({ n }: { n: number | string }) {
  return (
    <span className="numeral text-[1.6rem] leading-none">
      <span className="text-ink-faint">№</span>{" "}
      <span style={{ fontStyle: "italic" }}>
        {typeof n === "number" ? String(n).padStart(2, "0") : n}
      </span>
    </span>
  );
}

/** Monospaced kicker label */
export function Kicker({
  children,
  variant = "default",
}: {
  children: ReactNode;
  variant?: "default" | "crimson" | "sage" | "ochre";
}) {
  const cls =
    variant === "crimson"
      ? "kicker-crimson"
      : variant === "sage"
        ? "kicker-sage"
        : variant === "ochre"
          ? "kicker-ochre"
          : "";
  return <div className={"kicker " + cls}>{children}</div>;
}

/** Big stat block, magazine-style */
export function StatBlock({
  label,
  value,
  unit,
  note,
}: {
  label: string;
  value: ReactNode;
  unit?: string;
  note?: string;
}) {
  return (
    <div>
      <div className="kicker mb-2">{label}</div>
      <div className="display-lg text-[clamp(2rem,4vw,3.2rem)] tabular text-ink leading-none">
        {value}
        {unit && (
          <span className="display-italic text-[0.6em] text-ink-faint ml-2 font-light">
            {unit}
          </span>
        )}
      </div>
      {note && <div className="mt-3 marginalia max-w-[28ch]">{note}</div>}
    </div>
  );
}

/** Tiny inline sparkline-style value bar */
export function Bar({
  fraction,
  accent = "ink",
  height = 3,
}: {
  fraction: number;
  accent?: "ink" | "crimson" | "sage" | "ochre";
  height?: number;
}) {
  const color =
    accent === "crimson"
      ? "var(--crimson)"
      : accent === "sage"
        ? "var(--sage)"
        : accent === "ochre"
          ? "var(--ochre)"
          : "var(--ink)";
  return (
    <div
      className="w-full overflow-hidden"
      style={{
        height,
        background: "var(--rule-soft)",
        borderRadius: 1,
      }}
    >
      <div
        style={{
          width: `${Math.max(0, Math.min(1, fraction)) * 100}%`,
          background: color,
          height: "100%",
        }}
      />
    </div>
  );
}

/** Inline distribution dots — small tick chart for ~50 values */
export function DistributionDots({
  values,
  highlight,
  color = "var(--ink)",
  highlightColor = "var(--crimson)",
}: {
  values: number[];
  highlight?: number;
  color?: string;
  highlightColor?: string;
}) {
  if (values.length === 0) return null;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const sorted = [...values].sort((a, b) => a - b);
  return (
    <div className="relative h-6 w-full" aria-hidden>
      {sorted.map((v, i) => {
        const x = ((v - min) / range) * 100;
        const isHi = highlight !== undefined && Math.abs(v - highlight) < 1e-6;
        return (
          <span
            key={i}
            className="absolute top-1/2 -translate-y-1/2 rounded-full"
            style={{
              left: `${x}%`,
              width: isHi ? 7 : 3,
              height: isHi ? 7 : 3,
              background: isHi ? highlightColor : color,
              opacity: isHi ? 1 : 0.32,
              transform: `translate(-50%, -50%)`,
              transition: "opacity 200ms",
            }}
          />
        );
      })}
    </div>
  );
}

/** Editorial section header with kicker + number */
export function SectionHead({
  number,
  kicker,
  title,
  align = "left",
}: {
  number?: number | string;
  kicker?: string;
  title: ReactNode;
  align?: "left" | "center";
}) {
  return (
    <div className={align === "center" ? "text-center" : ""}>
      <div className="flex items-baseline gap-4">
        {number !== undefined && <Numeral n={number} />}
        {kicker && <Kicker>{kicker}</Kicker>}
      </div>
      <h2 className="display-lg mt-3 text-[clamp(1.8rem,3vw,2.6rem)]">{title}</h2>
    </div>
  );
}

/** Pull-quote */
export function PullQuote({
  children,
  attribution,
}: {
  children: ReactNode;
  attribution?: string;
}) {
  return (
    <blockquote className="pullquote my-10">
      {children}
      {attribution && (
        <footer className="mt-3 kicker block">— {attribution}</footer>
      )}
    </blockquote>
  );
}

/** Flex chip */
export function Chip({
  children,
  variant = "default",
  filled = false,
}: {
  children: ReactNode;
  variant?: "default" | "crimson" | "sage" | "ochre";
  filled?: boolean;
}) {
  const cls = [
    "chip",
    variant === "crimson" ? "chip-crimson" : "",
    variant === "sage" ? "chip-sage" : "",
    variant === "ochre" ? "chip-ochre" : "",
    filled ? "chip-filled" : "",
  ]
    .filter(Boolean)
    .join(" ");
  return <span className={cls}>{children}</span>;
}

/** Article / program card */
export function FeatureCard({
  href,
  number,
  kicker,
  title,
  excerpt,
  meta,
  accent = "ink",
}: {
  href: string;
  number?: number | string;
  kicker: string;
  title: string;
  excerpt: string;
  meta?: string;
  accent?: "ink" | "crimson" | "sage" | "ochre";
}) {
  const titleColor: CSSProperties =
    accent === "crimson"
      ? { color: "var(--crimson)" }
      : accent === "sage"
        ? { color: "var(--sage)" }
        : accent === "ochre"
          ? { color: "var(--ochre)" }
          : {};
  return (
    <Link href={href}
      className="group relative block py-7 first:pt-0 border-b border-[var(--rule-soft)] transition-colors hover:border-[var(--rule)]"
    >
      <div className="grid grid-cols-12 gap-6 items-start">
        <div className="col-span-12 md:col-span-2 flex md:flex-col items-baseline gap-3">
          {number !== undefined && <Numeral n={number} />}
          <Kicker>{kicker}</Kicker>
        </div>
        <div className="col-span-12 md:col-span-7">
          <h3
            className="display-md text-[clamp(1.3rem,2vw,1.85rem)] group-hover:[background-size:100%_2px] [background-image:linear-gradient(currentColor,currentColor)] [background-size:100%_0px] [background-repeat:no-repeat] [background-position:0_92%] transition-[background-size]"
            style={titleColor}
          >
            {title}
          </h3>
          <p className="mt-3 text-ink-soft leading-relaxed max-w-prose">{excerpt}</p>
        </div>
        <div className="col-span-12 md:col-span-3 marginalia">{meta}</div>
      </div>
    </Link>
  );
}

/** Short hairline divider */
export function Divider({ wide = false }: { wide?: boolean }) {
  return <div className={"rule " + (wide ? "my-16" : "my-10")} />;
}

/** Maturity chip with new colors (replaces older claimTiers component) */
export function Maturity({ status }: { status: "H" | "PP" | "SR" | "PR" | "Ret" }) {
  const map: Record<string, { label: string; cls: string }> = {
    H: { label: "Hypothesis", cls: "chip" },
    PP: { label: "Prepared pipeline", cls: "chip chip-ochre" },
    SR: { label: "Screening result", cls: "chip chip-sage" },
    PR: { label: "Publication-ready", cls: "chip chip-crimson chip-filled" },
    Ret: { label: "Retired", cls: "chip" },
  };
  const m = map[status] ?? map.H;
  return <span className={m.cls}>{m.label}</span>;
}
