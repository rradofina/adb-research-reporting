import {
  BRIEF_DETAILS,
  FINISH_LABELS,
  type BriefDetail,
  type FinishGroup,
} from "./briefs";
import { programs, type ProgramEntry } from "./programs";

export const ISSUE_CLOSURE_AS_OF = "2026-07-07";

export const ISSUE_FINISH_ORDER: FinishGroup[] = [
  "publication-ready",
  "screening-result",
  "program-prospectus",
  "prepared-pipeline",
  "hypothesis",
];

const ISSUE_STATUS_NOTES: Record<FinishGroup, string> = {
  "publication-ready": "Full current-issue evidence package under the ai-first chain.",
  "screening-result": "Useful public-data signal; not final research output.",
  "program-prospectus": "Computed prospectus; key upgrade still missing.",
  "prepared-pipeline": "Code path exists; empirical output not run.",
  hypothesis: "Question exists; no full repository result here.",
};

export interface IssueProgramRow {
  program: ProgramEntry;
  detail: BriefDetail;
}

export const issueProgramRows: IssueProgramRow[] = programs
  .map((program) => ({
    program,
    detail: BRIEF_DETAILS[program.slug],
  }))
  .filter((row): row is IssueProgramRow => Boolean(row.detail));

export const issueCounts = ISSUE_FINISH_ORDER.reduce(
  (acc, key) => {
    acc[key] = 0;
    return acc;
  },
  {} as Record<FinishGroup, number>,
);

for (const row of issueProgramRows) {
  issueCounts[row.detail.finish] += 1;
}

export const issueTotal = issueProgramRows.length;
export const issueFinishedCount = issueCounts["publication-ready"];
export const issueComputedCount =
  issueCounts["publication-ready"] +
  issueCounts["screening-result"] +
  issueCounts["program-prospectus"];
export const issueHeldBackCount =
  issueCounts["prepared-pipeline"] + issueCounts.hypothesis;

export const issueClosureDeck =
  `${issueTotal} topics are classified: ` +
  `${issueCounts["publication-ready"]} finished for the current issue, ` +
  `${issueCounts["screening-result"]} screening-only, ` +
  `${issueCounts["program-prospectus"]} prospectus, ` +
  `${issueCounts["prepared-pipeline"]} prepared pipeline, and ` +
  `${issueCounts.hypothesis} hypothesis.`;

export const issueHoldBackNotes = [
  "digital-performance is held at prepared pipeline because the Ookla parquet aggregation has not run.",
  "mpi-nighttime-lights remains hypothesis/owner-led until the external nighttime-lights track is reconciled.",
];

export const issueStatusCards = ISSUE_FINISH_ORDER.map((key) => ({
  key,
  label: FINISH_LABELS[key],
  count: issueCounts[key],
  note: ISSUE_STATUS_NOTES[key],
}));
