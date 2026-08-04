export type TopicFamily =
  | "observability"
  | "invalidation"
  | "distribution"
  | "synthesis";

export type ShellId = "product" | "workbench" | "chapter";

export interface StoryMetric {
  value: string;
  label: string;
  detail?: string;
}

export interface StoryFigure {
  id: string;
  role: string;
  title: string;
  caption: string;
  svg: string;
  png: string;
}

export interface StorySection {
  id: string;
  title: string;
  body: string;
}

export interface WorkbenchColumn {
  key: string;
  label: string;
}

export interface WorkbenchRow {
  id: string;
  label: string;
  values: Record<string, string | number>;
  pattern: string;
  note: string;
}

export interface GateRow {
  label: string;
  status: "pass" | "fail" | "reshape" | "non-claim" | string;
  value: string;
}

export interface StoryDownload {
  label: string;
  href: string;
}

export interface StoryPackage {
  schema_version: number;
  slug: string;
  family: TopicFamily;
  default_shell: ShellId;
  attestation_chain: string;
  maturity: string;
  title: string;
  subtitle: string;
  finding: string;
  finding_short: string;
  limits: string[];
  key_messages: string[];
  metrics: StoryMetric[];
  hero: {
    png: string;
    svg: string;
    title: string;
    caption: string;
    source: string;
  };
  figures: StoryFigure[];
  sections: StorySection[];
  workbench_columns: WorkbenchColumn[];
  workbench_rows: WorkbenchRow[];
  zeros_and_gates: GateRow[];
  downloads: StoryDownload[];
  authors: string[];
  published_at?: string;
  updated_at?: string;
  sources: string[];
  non_claim: string;
  generated_at: string;
  generated_from: string[];
}

export const SHELL_META: Record<
  ShellId,
  { label: string; blurb: string; when: string }
> = {
  product: {
    label: "Product",
    blurb: "Finding-first card. One claim, one hero, short limits.",
    when: "Screening results and short papers a busy reader can finish in ninety seconds.",
  },
  workbench: {
    label: "Workbench",
    blurb: "Filters, domain rows, gates. Absence and disagreement as the object.",
    when: "Observability and source-disagreement programs.",
  },
  chapter: {
    label: "Chapter",
    blurb: "Long-form reading with TOC, metrics band, and print path.",
    when: "Flagship synthesis or a full working-paper session.",
  },
};
