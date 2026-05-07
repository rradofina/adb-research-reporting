# Literature Review — {program-title}

Status: **{ai-drafted | human-reviewed | human-finalized}**

Governed by `CONSTITUTION.md` §4 and §5. The systematic Tier-A/B/C scan
must be complete before this program may advance past Hypothesis. The
human owner reviews line-by-line and attests in the commit message.

Scoring of this program against `CONSTITUTION.md` §3.3 is in `scoring.md`.

---

## 1. Search record

### 1.1 First-pass scan — YYYY-MM-DD

Tool used: {general web search | scholar | DOI lookup}.

Queries:

1. `…`
2. `…`

Inclusion: {open-access peer-reviewed articles, institutional reports, working
papers from named research institutions}.

Exclusion: {commercial blog posts, vendor white papers, unverifiable preprints}.

Result: N verified entries. See §2 below.

### 1.2 Systematic scan (Tier A/B/C per Constitution §4.2) — YYYY-MM-DD

Tier A databases (peer-reviewed journals, NBER, World Bank PRWP,
ADBI, IZA, CGD): N queries, M verified entries.

Tier B databases (institutional working-paper series, IGC, 3ie,
J-PAL, Brookings): N queries, M verified entries.

Tier C databases (preprints, technical reports, blog posts from
named research institutions): N queries, M verified entries.

Queries (numbered continuation from §1.1):

7. `…`

Result: M further verified entries. Total N+M after dedupe.

---

## 2. Entries

Each entry below is a verified canonical source. BibTeX keys live in
`/references.bib`. Every empirical claim cites by key.

### 2.1 {first-author year-shortword}

- **Title:** …
- **Authors:** …
- **Venue:** …, year.
- **DOI:** …
- **Why this is in scope:** {1–2 sentences on the program-relevant claim}
- **Limit / caveat:** {what the paper does not establish}

(repeat per entry)

---

## 3. Synthesis — what is established

A short narrative (≤ 600 words) summarizing what the cited literature
collectively establishes. No new claims here; only reads-from-the-literature.

---

## 4. Gap — what remains unestablished

A short narrative (≤ 400 words) on the unfilled gap this program targets.
The gap must be specific (not "more research needed") and must be
addressable with public data per §6.

---

## 5. Risk of redundancy

If a paper materially overlaps with this program's first testable claim,
quote it here. The program owner attests in the commit message that the
overlap has been read in full and that the marginal contribution remains
defensible.

---

## 6. First testable claim

The exact claim sentence the program intends to test. This is frozen by
the pre-registration step (`pre-registration.md`) before the pipeline
runs.

> *{Claim sentence}*

### 6.1 Falsification condition

The empirical signature that would constitute disproof. Per §3.2.

> *{Falsification condition}*

---

## 7. Owner attestation

| Field | Value |
|---|---|
| Searched: Tier A / B / C complete | *(yes / no)* |
| Read each entry's main result section | *(yes / no)* |
| Marginal contribution defensible after read-through | *(yes / no)* |
| Date attested | *(YYYY-MM-DD)* |
| Commit hash for attestation | *(hash)* |

A program may not advance past Hypothesis until every owner field above
is filled.
