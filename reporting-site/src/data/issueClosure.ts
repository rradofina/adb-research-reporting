import { programs } from "./programs";
import type { Maturity } from "../lib/claimTiers";

export const ISSUE_CLOSURE_AS_OF = "2026-07-19";

export const ISSUE_STATUS_ORDER: Maturity[] = ["PR", "SR", "PP", "H", "Ret"];

const STATUS_COPY: Record<Maturity, { label: string; note: string }> = {
  PR: {
    label: "Publication-ready",
    note: "A full evidence package has passed the repository's current publication gate.",
  },
  SR: {
    label: "Screening result",
    note: "A useful public-data signal exists, with explicit limits and an upgrade path.",
  },
  PP: {
    label: "Prepared pipeline",
    note: "The question or pipeline is prepared, but the evidence does not support a finished claim.",
  },
  H: {
    label: "Hypothesis",
    note: "A research question exists; a complete empirical result is not present in this repository.",
  },
  Ret: {
    label: "Retired",
    note: "The program is retained for provenance but is no longer active.",
  },
};

export const issueCounts = ISSUE_STATUS_ORDER.reduce(
  (acc, status) => {
    acc[status] = programs.filter((program) => program.status === status).length;
    return acc;
  },
  {} as Record<Maturity, number>,
);

export const issueTotal = programs.length;
export const issueFinishedCount = issueCounts.PR;
export const issueComputedCount = issueCounts.PR + issueCounts.SR;
export const issueHeldBackCount = issueCounts.PP + issueCounts.H + issueCounts.Ret;

export const issueClosureDeck =
  `${issueTotal} programs are registered: ` +
  `${issueCounts.PR} publication-ready, ` +
  `${issueCounts.SR} screening results, ` +
  `${issueCounts.PP} prepared pipelines, ` +
  `${issueCounts.H} hypothesis, and ` +
  `${issueCounts.Ret} retired.`;

export const issueHoldBackNotes = [
  "Prepared-pipeline and hypothesis programs remain visible so readers can see the question, data gap, and next viable research move.",
  "Only the constitutional program register controls these labels; article or showcase metadata cannot promote a topic.",
];

export const issueStatusCards = ISSUE_STATUS_ORDER
  .filter((status) => status !== "Ret" || issueCounts.Ret > 0)
  .map((status) => ({
    key: status,
    label: STATUS_COPY[status].label,
    count: issueCounts[status],
    note: STATUS_COPY[status].note,
  }));
