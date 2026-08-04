# Task 31 source queue

`attestation_chain: ai-first` · Last updated 2026-08-05

What remains before this review is citable under `CONSTITUTION.md` §2.7. Every
item here is blocked on access we do not lawfully have, or on a document whose
correct location we could not determine automatically. None of it is blocked on
analysis.

## Where the register stands

| State | Count | What it means |
|---|---|---|
| Locator confirmed | 22 | Every quoted figure was read in the source's own prose; the supporting sentence is quoted in `locators.json` |
| Read, partly unsupported | 7 | Most figures confirmed, but at least one could not be found in reachable text — see the per-row note |
| Register URL wrong | 3 | The cited document exists, but the recorded URL points somewhere else |
| Unreachable | 18 | Paywalled, bot-blocked, or landing-page-only; no lawful open-access copy found |
| Qualitative | 3 | Estimate carries no numeric token to screen |

Reading the located pages produced a third class of defect, distinct from the
transposed figures found earlier: **country attributions the source never
makes.** Record N07 credited Diffenbaugh and Burke (2019) with per-capita GDP
losses of 31% for India, 27% for Indonesia, and 12% for Bangladesh. Indonesia
and Bangladesh appear nowhere in that paper; the 31% is a decile range and the
27% a low-emitter median. Corrected in the register and the manuscript.

Two rows also show why a located figure is not a verified one, in both
directions. In `C05` the screen matched "20" against "20 years" — a
coincidence — yet the claim turned out to be supported verbatim elsewhere. In
`N01` the screen matched "20" against "bottom 20 percent", and the resilience
claim it was supposed to support is *not* in the text. Same signal, opposite
truths; only reading separates them.

Citation identity is separately clean: 22 of 22 DOIs resolve with matching
journal, year, and first author (`verify_citations.py` exits 0).

## Queue 1 — replace three wrong URLs

These are the highest-value items: the cited work is almost certainly right,
but the recorded link does not reach it, so §2.7 bars the figures from any
headline, table, figure, or synthesis sentence.

| ID | Cited work | Recorded URL points at | Needed |
|---|---|---|---|
| `E06` | Lao PDR Economic Monitor and Household Welfare Monitoring | a COVID-monitoring brief without the wage tables | the Economic Monitor edition carrying the 39% inflation / 5.7% nominal wage / 33% real wage figures |
| `N02` | ADB Asia-Pacific Climate Report 2024 | the report's landing page | the report PDF carrying the US$300 billion adaptation-finance figure |
| `N16` | Tropical Cyclone Pam Post-Disaster Needs Assessment (2015) | a 2024 World Bank results story | the Government of Vanuatu PDNA itself |

## Queue 2 — 26 unreachable sources

Split by why, because the remedies differ:

- **Publisher bot-blocked (403) or cookie-walled.** A browser session reaches
  these; an HTTP client does not. ADB Library credentials or a manual download
  resolves them.
- **Closed access with no OA copy.** Unpaywall found nothing lawful. These need
  subscription full text — the ADB Library route named in `review_protocol.md`.

`locator_ledger.json` records the exact reason per record. Nothing here should
be resolved by guessing: a source we cannot read is a source we cannot cite.

## Queue 3 — coverage gaps

Not access problems; genuine holes against the commissioning brief.

- **Ten of the eighteen named journals have zero records**, and the literature
  is demonstrably there. Measured against OpenAlex on 2026-08-05, papers
  published 2015 onward in those journals whose title or abstract mentions
  shock, welfare, poverty, climate, disaster, pandemic, or inflation:

  | Journal | 2015+ works | on-topic |
  |---|---:|---:|
  | American Economic Review | 2,708 | 493 |
  | Journal of Development Economics | 1,556 | 383 |
  | Journal of Environmental Economics and Management | 1,199 | 380 |
  | The Lancet Public Health | 1,640 | 303 |
  | Review of Economics and Statistics | 1,216 | 284 |
  | Climate Change Economics | 338 | 255 |
  | Nature Human Behaviour | 2,495 | 239 |
  | Journal of Health Economics | 1,078 | 179 |
  | Economic Development and Cultural Change | 521 | 89 |

  This settles a question the register could not answer on its own: the gap is
  a search failure, not an absent literature. Three records have since been
  added from that literature and verified — `N25` (Journal of Development
  Economics: heat in pregnancy raises Indian infant mortality by about two
  deaths per 1,000 births), `N26` and `N27` (Economic Development and Cultural
  Change: monsoon rainfall and child nutrition in Nepal; the 2014 Bangladesh
  flood, migration, and remittances). Each was built from text actually read,
  never from recall. **JDE and EDCC are now represented; AER, REStat, JEEM,
  JHE and QJE remain at zero**, and their candidates are closed access. The workbook's Search Log sheet
  lists "JDE; World Development; QJE; JPE; REStat; JEEM; JHE" as an economics
  channel that was searched. Six of those seven yielded nothing. Either the
  search did not actually run against them or it ran badly; the log should be
  corrected to say which, because a log that claims coverage the register does
  not show is worse than no log.

- **Central Asia rests on one record.** The brief asks for it as a named
  subregion for comparison. One record cannot support a subregional comparison.

## Standing rule

A record without a confirmed locator may sit in the evidence register. It may
not appear in a headline, abstract, table, figure, annotated bibliography, or
synthesis sentence. That is `CONSTITUTION.md` §2.7, and it is the reason this
queue is a gate rather than a wish list.
