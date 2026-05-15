export type Maturity = "H" | "PP" | "SR" | "PR" | "Ret";

export const maturityLabels: Record<Maturity, string> = {
  H: "Hypothesis",
  PP: "Prepared pipeline",
  SR: "Screening result",
  PR: "Finished for issue",
  Ret: "Retired",
};

export const maturityColor: Record<Maturity, string> = {
  H: "maturity-chip-h",
  PP: "maturity-chip-pp",
  SR: "maturity-chip-sr",
  PR: "maturity-chip-pr",
  Ret: "maturity-chip-ret",
};

export function MaturityChip({ status }: { status: Maturity }) {
  return (
    <span
      className={
        "maturity-chip " +
        maturityColor[status]
      }
    >
      {maturityLabels[status]}
    </span>
  );
}
