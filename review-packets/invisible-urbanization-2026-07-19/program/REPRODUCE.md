# Reproduce the invisible-urbanization measurement study

`attestation_chain: ai-first`

## Environment

- Python 3.11 or newer
- `pandas`, `numpy`, `matplotlib`
- approximately 1 GB free disk space for the source archive, partial transfer,
  and decompression buffers
- network access for the first GHS-DUC and WDI retrieval

## Run order

```powershell
python invisible-urbanization/scripts/acquire-ghsl-duc.py
python invisible-urbanization/scripts/build-definition-gap-object.py
python invisible-urbanization/scripts/build-transition-diagnostics.py
python invisible-urbanization/scripts/build-figure-dossier.py
```

The first command downloads the 362.6 MB GHS-DUC archive. If interrupted, it
resumes from the `.zip.part` file when the server returns HTTP 206. Later runs
use the repository-level cache.

## Expected checks

- GHS-DUC SHA-256:
  `4ac3eebb1674d7adce2391f223159ec1cbd20f2b88e794ab6c3f7b4b100c6a09`
- 74 archive members, including 72 CSV files and six distinct schemas
- 40 complete GHSL–WDI cases in 2020
- 34 economies and 7,918 matched units in each level-2 transition window
- transition decompositions close for 10, 20, and 30 years
- 11 PNG and 11 SVG evidence figures plus a dossier JSON

## Committed outputs

- `generated/invisible-urbanization-ghsl-duc-inventory.json`
- `generated/invisible-urbanization-definition-gap-panel.csv`
- `generated/invisible-urbanization-embedded-urban-panel.csv`
- `generated/invisible-urbanization-level2-transitions.csv`
- `generated/invisible-urbanization-definition-gap.json`
- `generated/invisible-urbanization-transition-diagnostics.json`
- `generated/invisible-urbanization-figure-dossier.json`
- `generated/charts/invisible-urbanization-01-*.{png,svg}` through
  `invisible-urbanization-11-*.{png,svg}`

## Data storage design

Raw public data belongs in `.cache`, not Git and not Vercel. Git stores small
derived tables, checksums, scripts, narratives, and publication-ready figures.
The reporting site copies only committed artifacts. If this factory later
serves interactive row-level queries or hundreds of studies, move metadata,
lineage, and derived analytical tables to Postgres/object storage; retain Git
as the versioned research and publication layer.

