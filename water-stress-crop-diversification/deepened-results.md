# Deepened result — direct water and crop measures reject the country ranking

`attestation_chain: ai-first` · 2026-07-18

The earlier denominator audit showed that the old formula saturated its water
term for all four baseline leaders and used inverse cereal yield as a crop proxy.
The current pass closes the two public-source gaps with WDI/AQUASTAT SDG 6.4.2
and FAOSTAT 2024 harvested-area crop shares.

## Claim decision

Reject the inherited Afghanistan–Azerbaijan–Pakistan–Turkmenistan country set.

- It is the raw top four in **2 of 7** inherited runs.
- Direct available-water stress retains **2 of 4** published members.
- Direct crop HHI retains **0 of 4**.
- All **5 of 5** full-sample crop-HHI leaders lack water-stress rows.
- Available-water stress and crop HHI have Spearman **-0.242** across 30
  aligned rows, with 95% bootstrap interval **[-0.592, +0.152]**.
- The replacement diagnostic correlates **+0.922** with water stress and
  **+0.049** with crop HHI.

## What changed

The previous “data wall” is no longer the finding. The public national objects
were acquired and joined. They disagree, and their disagreement reveals that
the research question requires a different unit. The next evidence object is
basin × crop × irrigation × year, not another national formula.

## Generated evidence

- `generated/water-construct-validation.json`
- `generated/water-construct-diagnostics.csv`
- `generated/water-construct-sensitivity.csv`
- nine article figures and one 16:9 hero thumbnail under `generated/charts/`

## Reproduce

```bash
python water-stress-crop-diversification/scripts/deepen-denominator.py
python water-stress-crop-diversification/scripts/audit-water-source-readiness.py
python water-stress-crop-diversification/scripts/build-construct-validation.py
python water-stress-crop-diversification/scripts/build-figure-dossier.py
```
