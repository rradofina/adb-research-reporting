# Reproduce — School heat disruption

`attestation_chain: ai-first`

Run from the repository root with Python 3.11+.

## Claim-enabling pipeline

```powershell
python school-heat-disruption/scripts/deepen-sensitivity-audit.py
python school-heat-disruption/scripts/build-construct-validation.py
python school-heat-disruption/scripts/build-figure-dossier.py
```

Use `--refresh` with `build-construct-validation.py` to replace cached public
responses.

## Public inputs

- Committed `sensitivity-runs.json`, derived from the inherited WDI/CCKP panel.
- UNICEF *Learning Interrupted* 2024 public PDF, Annex 1.
- World Bank Indicators API: `SE.PRE.ENRL`, `SE.PRM.ENRL`, and `SE.SEC.ENRL`.

The script checks each transcribed UNICEF country, count, and hazard against PDF
text before analysis. Raw PDF and API responses are cached under `.cache/` and
excluded from version control. Generated evidence stores URLs, retrieval time,
response hashes, coverage counts, fixed bootstrap seeds, and limitations.

## Expected checks

```text
UNICEF ADB rows: 21
Old-panel overlap: 19
Heatwave-major rows: 6
Heatwave-major affected students: 154888029
Cambodia direct rank: 6
Old index vs count Spearman: 0.028571...
Child population vs count Spearman: 0.942857...
```

Any source change requires regenerating the figures and reconsidering the
claim decision before publication.
