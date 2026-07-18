# Reproduce

`attestation_chain: ai-first`

## Environment

Python 3 with `matplotlib`, `numpy`, and `pandas`. Large source archives are
cached under `.cache/coastal-informal-risk-ghs-ucdb-r2024a-v1-2/` and are not
deployed to Vercel or committed to Git.

## Commands

```powershell
python coastal-informal-risk/scripts/acquire-ghs-ucdb.py
python coastal-informal-risk/scripts/build-lecz-growth-object.py
python coastal-informal-risk/scripts/build-figure-dossier.py
python coastal-informal-risk/scripts/build-thumbnail.py
```

## Source custody

- GHS-UCDB R2024A V1.2 General Characteristics archive: 6,902,089 bytes,
  SHA-256 `bc879d82320504f89df2041b7936221c8239cd808abe93980493aed062b4f3d6`.
- GHS-UCDB R2024A V1.2 Exposure archive: 44,408,361 bytes,
  SHA-256 `f0ba93a5faaddadf62f9568b8c421d63a8f583757cde7170ea6ef0ca1102879c`.
- Dataset DOI: `10.2905/1a338be6-7eaf-480c-9664-3a8ade88cbcd`.

`generated/coastal-ghs-ucdb-inventory.json` records URLs, retrieval time,
member names, sizes, hashes, and schema dimensions. Derived CSV and JSON files
are committed; the raw archives remain in the local cache.

