# Digital-performance source cache

This directory stores reproducible public-source responses and is ignored by
Git except for this note. Rehydrate it with:

```powershell
python digital-performance/scripts/build-coverage-use-gap.py --refresh
```

The script fetches the ITU DataHub catalogue metadata and annual observations
for 4G/LTE population coverage and individuals using the Internet. It writes a
committed source inventory with URLs, retrieval timestamps, byte counts, and
SHA-256 digests. Raw responses remain here rather than being shipped with the
site or stored in Vercel.
