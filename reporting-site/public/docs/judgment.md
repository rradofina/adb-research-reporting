# Judgment — how to think in this factory

This file is the thinking layer of the research factory. `CONSTITUTION.md`
says what is allowed. `research/factory.md` says what steps exist. This file
says how to choose. When the procedure and this file pull in different
directions, the procedure is being misread: no rule in this repository ever
requires building an artifact that does not move a claim.

Read this before starting substantive work. It is short on purpose.

## 1. The unit of progress is the claim, not the artifact

A session made progress if, at the end of it, at least one of these is true:

1. **The claim moved** — a headline claim got stronger evidence, tighter
   scope, or an honest revision.
2. **The claim changed shape** — the evidence forced a narrower, different,
   or negative claim, and the artifacts now say so.
3. **A reader is better off** — an article, chart, page, or packet now
   communicates an existing result more clearly.
4. **A decision was made** — a program was killed, deferred, rotated, or
   reframed, with the reason written down.

A new script, a new generated CSV, a new "wall" markdown, or a new status
entry is **not** progress by itself. Artifacts are receipts for progress,
not the progress. Before building anything, ask: *which of the four outcomes
above does this produce?* If the honest answer is "none — it documents the
same blockage again," do not build it.

## 2. Stopping rule: three passes at the same wall

The factory's historical failure mode is the grind: dozens of consecutive
source scans, audits, ledgers, and gates against the same blocker, each
ending with every claim-enabling count still at zero. Each artifact was
individually defensible; the sequence was a waste and made the public
surface worse.

**The rule.** Count consecutive passes against the same blocker (same
missing evidence, same zero counts). After the **second** pass that leaves
the blocking counts unmoved, a third scan of the same wall is forbidden.
The next session must instead pick one of:

- **Reshape** — restate the claim as the strongest thing the existing
  evidence already supports, and finish that.
- **Publish the absence** — if the search was systematic, the absence of
  public evidence is itself the finding (see §3).
- **Escalate and rotate** — write a five-line blocker note naming the
  exact document or access that would unblock it, whether it is a hard
  wall (owner-only) or genuinely nonexistent in public, and rotate to the
  next program.

"Maybe the next portal has it" is not a reason to take a third pass. If a
new pass is truly justified, it must name, in advance, the specific source
that was not checked before and why it plausibly changes a zero to a
nonzero. Write that sentence first; if it cannot be written, stop.

## 3. Absence is a finding

This lab studies measurement gaps. When a systematic, documented search
shows that something *should* be publicly verifiable and is not — station
calibration records, facility registries, verified reports — that is not a
blocker in front of the research. It **is** the research. Under
Constitution §2.6, null and boring findings are legitimate outputs; a
documented-absence result is the natural flagship product of a
measurement-gap lab.

Recognize the moment: when a search has been systematic (sources named,
retrieval recorded, counts honest) and the target evidence is absent
everywhere, stop treating the absence as an obstacle to claim X and start
writing the paper about the absence. The dozens of scans become the
evidence base of that paper — a strength, not a graveyard. The claim
flips from "coverage is Y%" (blocked) to "no economy in the sample
publishes the evidence needed to verify coverage" (supported, today, by
committed artifacts).

## 4. Choose the highest-leverage move, and say so

At session open, after reading the boards, choose the move explicitly from
this menu and state the choice in one sentence with a reason:

| Move | When it is the right one |
|---|---|
| **Deepen evidence** | A specific new source plausibly changes a headline number or unblocks a claim |
| **Reshape the claim** | Evidence and claim have drifted apart; the honest claim is different from the planned one |
| **Publish** | The result exists but readers cannot see or understand it yet; ladder tiers are missing or weak |
| **Critique** | The result looks finished but has not been seriously attacked |
| **Improve presentation** | The finding is sound but the page/chart/article undersells or obscures it |
| **Kill / defer / rotate** | The stopping rule fired, or the topic failed the taste tests below |

Defaulting to "deepen evidence" every session is how the grind happened.
Publication, critique, and presentation moves are equal-status work, not
dessert.

## 5. Taste tests for topics and claims

Run these before promoting a hook and again before deepening a program.
They are judgment tests, not gates — but write the answers down.

- **The one-sentence test.** Can the finding be said in one sentence with
  a number and a place, such that a busy economist would look up? If the
  sentence needs three clauses of caveats to be honest, the claim is not
  ready to headline.
- **The so-what test.** Name the person whose decision changes if this is
  true. "A reader finds it interesting" is not a decision.
- **The forwardability test.** Would a senior colleague forward the chart
  to someone with "look at this"? If the best visual is a country ranking
  or a generic trend, the answer is no — defer the hook.
- **The surprise test.** Does the result differ from what an informed
  reader would have guessed? Confirming the obvious with better plumbing
  is maintenance, not research.
- **The honest-title test.** Write the title that the evidence actually
  supports. If it embarrasses the effort spent, either the claim needs
  reshaping or the program needed killing earlier — both are better than
  inflating the title.

### Topic selection: source object first

A good topic in this factory is not "climate," "health," or "digital
development." It is a public data object that exposes a measurement problem a
reader can see. Before creating or reviving a program, write a hook card with
these seven fields:

1. **Source object.** Dataset, institution, unit, period, access route,
   license, and retrieval risk.
2. **First visual.** The rough chart, map, matrix, timeline, network, or
   source-disagreement table the script will produce first.
3. **Possible claim.** One sentence with place, unit, and quantity shape. The
   number can be a placeholder until a script runs; the unit cannot be vague.
4. **Decision user.** The person or team whose decision would change if the
   claim survives.
5. **What would falsify it.** The source, join, sensitivity, or comparison
   that would make the hook weak.
6. **Why existing work does not already answer it.** One paragraph after the
   landscape check, not a guess from memory.
7. **Stop condition.** The exact result that would make the hook a defer note
   instead of a program.

If the hook card cannot name a source object and first visual, keep the idea in
brainstorming notes. Do not create a program folder, article, or showcase page
for it. The fastest way to build a strong research factory is to be ruthless
with weak hooks before they become status-board debt.

## 6. Visual thinking

Every program has **one hero visual** — the single chart, map, or matrix
that carries the argument. It is chosen (and sketched roughly) before the
polish phase, because if no visual can carry the argument, the argument is
usually not there yet.

- The hero visual shows the *finding*, not the *inventory*. A map of where
  evidence exists and where it is absent is a finding. Sixty stacked
  audit-wall tables are an inventory; readers will not scroll them, and
  they dilute the pages they sit on. Consolidate walls into one honest
  summary surface with drill-down links to the packet.
- Annotation beats legend: label the interesting point on the chart
  itself. The reader should get the point before reading the caption.
- Honest axes, visible uncertainty, sources on the figure. A beautiful
  chart of a triage metric labeled as triage is fine; a beautiful chart
  that implies more maturity than the label allows is a §18.2 problem.
- Follow `research/style-guide.md` for the house look. One consistent
  system across programs reads as a lab; per-page improvisation reads as
  a template farm.

## 7. Write like a researcher, not a clerk

The status boards decayed into multi-thousand-word run-on inventories
because each session appended its receipts. That style is now banned:

- A status cell or entry states the **finding or decision first**, then at
  most a few supporting facts. Ten lines is the budget. Artifact
  inventories belong in the program folder and git history, not the board.
- Never list more than five artifacts by name in prose. "The 60+ scan
  artifacts are indexed in `{program}/README.md`" is the correct form.
- Prefer "we found X" over "a scan was performed that records N rows of
  context toward X." If nothing was found, say "we found nothing" — that
  sentence is allowed and often the most useful one in the file.
- The register of banned words (§14) and framings still applies. Plain,
  confident, caveated prose; no hedging cascades, no procedural voice.

## 8. What this file does not change

Non-negotiables stay non-negotiable: public data only, every number from a
committed script, sensitivity at ±50%, honest maturity labels and
`attestation_chain`, citations by BibTeX key, the §14 banned list, the
ethics rules, and the hard walls in `CLAUDE.md`. Judgment operates inside
those walls. The point of this file is that inside the walls there is a
large space of possible next actions, and the factory is obligated to pick
the valuable one, not the one that most resembles the previous session.
