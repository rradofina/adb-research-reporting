# How development rankings fail

`attestation_chain: ai-first`

A synthesis of the twelve construct-validation tests this repository ran
against national rankings it had built itself. It introduces no new measurement
of any economy: `scripts/build-failure-mode-panel.py` reads values that program
scripts already committed under `{program}/generated/`, cites each one by file
path and JSON pointer, and aborts rather than substitute a default.

## Why this program exists

Twelve programs each closed with a version of the same sentence — the inherited
ranking did not survive its own construct check. Individually that is honest
maintenance and nothing a reader needs. Collectively it is a sample of twelve
failures with recurring structure, and the structure is the finding.

## The failure modes

The literature check of 2026-08-05 is recorded per mode in the panel JSON. Only
the first is an open candidate; the rest are retained because they are the
evidence for it.

| Mode | What it means | Where it shows | Literature |
|---|---|---|---|
| `robustness-vs-validity` | The suite certified a set as stable and a construct check rejected the same set | 5 programs, 5 of 5 | Open |
| `degenerate-sensitivity` | The sweep could not change the answer, by construction | invisible-urbanization | Known method, local defect |
| `observation` | The ordering tracks where data was collected, not where the problem is | access-services | Partly settled |
| `denominator` | Absolute and per-population orderings of one construct disagree totally | migration, disaster, flood, water | Settled |
| `construct` | The proxy's leading set does not survive a direct measure | 7 programs, 9 comparisons | Settled |

## Files

- `results.md` — the findings, each with its literature position and limits.
- `scripts/build-failure-mode-panel.py` — the only script; reads committed artifacts.
- `generated/index-failure-modes-panel.json` — full panel with per-value provenance.
- `generated/index-failure-modes-robustness-vs-validity.csv` — the five paired cases.
- `generated/index-failure-modes-denominator.csv` — the four paired leading sets.
- `generated/index-failure-modes-construct-overlap.csv` — the nine comparisons.

## Status

Unlabeled and deliberately not on the public site. The open question is whether
the robustness-versus-validity pairing earns a hero visual and a page, or
whether the honest end state is a methods note. See `STATUS.md`.
