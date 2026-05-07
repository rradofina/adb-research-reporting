export type Maturity = "H" | "PP" | "SR" | "PR" | "Ret";

export const maturityLabels: Record<Maturity, string> = {
  H: "Hypothesis",
  PP: "Prepared pipeline",
  SR: "Screening result",
  PR: "Finished for issue",
  Ret: "Retired",
};

export const maturityColor: Record<Maturity, string> = {
  H: "bg-ink-200 text-ink-700",
  PP: "bg-signal-info/10 text-signal-info",
  SR: "bg-signal-warn/10 text-signal-warn",
  PR: "bg-signal-ok/10 text-signal-ok",
  Ret: "bg-ink-100 text-ink-500",
};

export function MaturityChip({ status }: { status: Maturity }) {
  return (
    <span
      className={
        "inline-block rounded px-2 py-0.5 text-[0.7rem] font-semibold uppercase tracking-wider " +
        maturityColor[status]
      }
    >
      {maturityLabels[status]}
    </span>
  );
}
