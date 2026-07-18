// Permanent evidence-packet loader. Backs /program/:slug/evidence.

export interface ArtifactMeta {
  key: string;
  file: string;
  label: string;
  size: number;
  size_human: string;
  mtime: string;
  sha256: string;
  attestation_chain: string | null;
}

export interface GeneratedFile {
  file: string;
  size: number;
  size_human: string;
  sha256: string;
}

export interface ScriptFile {
  file: string;
  size: number;
  size_human: string;
  lines: number;
  language: "python" | "javascript";
  sha256: string;
}

export interface ArticleRef {
  slug: string;
  title: string;
  attestation_chain: string;
}

export interface HeroVisual {
  png: string;
  svg: string;
  json: string;
  title: string;
  caption: string;
  headline_number: string | null;
  visual_form: string;
  source: string;
  attestation_chain: string;
  generated_at: string;
  dimensions: { width: number; height: number };
  sha256: { png: string; svg: string };
}

export interface EvidenceManifest {
  program: string;
  permanent_url: string;
  generated_at: string;
  hero: HeroVisual | null;
  artifacts: ArtifactMeta[];
  generated_files: GeneratedFile[];
  scripts?: ScriptFile[];
  articles: ArticleRef[];
  story?: ResearchStorySection[];
  resources?: EvidenceResources;
}

export interface ResearchStoryArtifact {
  key: string;
  file: string;
  label: string;
}

export interface ResearchStorySection {
  key: string;
  title: string;
  available: boolean;
  state?: "missing" | "draft" | "present";
  artifacts: ResearchStoryArtifact[];
}

export interface EvidenceResources {
  reproduce: string | null;
  deck: string | null;
  reviewer_packet: string | null;
  repository: string;
}

const cache = new Map<string, Promise<EvidenceManifest | null>>();

export function loadEvidenceManifest(slug: string): Promise<EvidenceManifest | null> {
  if (!cache.has(slug)) {
    cache.set(
      slug,
      fetch(`/programs/${slug}/manifest.json`, { cache: "no-store" })
        .then((r) => (r.ok ? r.json() : null))
        .catch(() => null),
    );
  }
  return cache.get(slug)!;
}

export async function loadArtifact(slug: string, file: string): Promise<string | null> {
  const r = await fetch(`/programs/${slug}/${file}`);
  if (!r.ok) return null;
  return r.text();
}

export function stripFrontmatter(md: string): string {
  if (!md.startsWith("---")) return md;
  const end = md.indexOf("\n---", 3);
  if (end < 0) return md;
  return md.slice(end + 4).replace(/^\r?\n/, "");
}
