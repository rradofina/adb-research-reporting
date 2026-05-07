# Skill: Systematic Literature Scan (Constitution §4.2)

## Purpose
Run a Tier-A/B/C systematic literature scan for a given research program
and return verified BibTeX entries ready to commit to `references.bib`.

## Invocation
> "Run a systematic literature scan for program-slug `<slug>` on topic `<topic>`."

## Constraints
- Every returned entry must be verified at canonical source (DOI page,
  PMC, publisher landing). No fabricated authors, years, or DOIs.
- Cite by BibTeX key only; bare URLs are not citations.
- Tier A (always): ADBI, ADB ERCD, WB PRWP, IMF WP, OECD, UNDP HDRO,
  UNU-WIDER, UNESCAP, plus topic-specific WHO / ILO / FAO / UNICEF /
  UN-Habitat as relevant.
- Tier B (always): NBER, IZA, CEPR, RePEc, SSRN, BREAD/PEDL/STEG/Y-RISE,
  EconStor, OSF, SocArXiv, EarthArXiv, plus core development journals
  (JDE, WD, WBER, EDCC, RDE, Oxford Dev Studies, JAE, JHDC, Progress in
  Development Studies, JDS, EJDR).
- Tier C (when topic applies): topic-specific journals per `sources.md`.
- Honest exclusion: if a database returns no hits, say so. Do not paper
  over gaps.
- National-language passes are out of scope for this skill (delegate to
  red-team members per Constitution §9.3).

## Output format
A single Markdown response containing:

1. **Search record** — date, queries used, databases consulted.
2. **Verified entries** — for each: BibTeX key, full citation,
   2-sentence summary, fit to the program (anchor / template / framing /
   tangential).
3. **PRISMA-lite flow** — identified / screened / included counts.
4. **Gap statement** — what's NOT in the literature that this program
   would add. 3–5 sentences.
5. **Files changed** — append the verified entries to `references.bib`
   and update `<program>/literature.md` with the systematic scan record.

## Stopping criteria
- 8–15 verified entries, or all promising hits exhausted.
- Stop early if a single canonical paper covers the topic comprehensively.

## Tools
- WebSearch / WebFetch for canonical-source verification.
- Read / Edit / Write for committing to `references.bib` and `literature.md`.
- (Future) OpenAlex MCP server for unified database queries.

## What this skill does NOT do
- Does not promote a program past Hypothesis. Owner attests via
  Constitution §7.2 gates.
- Does not write the program's first testable claim or falsification
  condition. Those are owner judgments.
- Does not substitute for a publication-ready PRISMA review. This is a
  Tier-floor scan; the publication-grade scan is a separate human-led
  effort with formal pre-registration.
