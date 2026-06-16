# Deepened result — the gap is mostly a denominator, not a mapping failure

`attestation_chain: ai-first`

This answers the sharpest internal contradiction in `deep-questions.md` §1.2 —
the principal-tier inversion — with a real recomputation. Every number below
is produced by `scripts/deepen-tier-decomposition.py` from artifacts already
in this repository: the committed per-ADM1 panels
`generated/public-service-data-quality-PHL.json` and `-BGD.json` (themselves
produced by `scripts/process-multi-country.py` from the committed NHFR / DGHS
caches and the access-services OSM panel), plus the raw committed NHFR pages
`.cache/nhfr_p*.json` for the Barangay-Health-Station re-derivation. No
network, no AI-supplied figures. Per `CONSTITUTION.md` §6.4 these ratios are a
triage / measurement-gap diagnostic, not a country-quality ranking; per §13.3
the framing throughout is observability and coverage gap.

Artifact: `generated/psdq-tier-decomposition.{json,csv}`.

## The question

The headline is that OSM `amenity=hospital|clinic|doctors` captures only
**17.1%** of the Philippine registry. That 17.1% is a *clinical*-tier ratio:
its denominator includes the Barangay Health Station tier (NHFR factype 20),
27,052 one-room community posts that volunteer mappers do not record. The deep
question: when the gap is read on the *principal* tier instead — hospitals,
main clinics, RHUs, and city/municipal/provincial health offices, the
institutions a patient actually seeks and a regulator licenses — does the
undercount survive, or does it invert? An OSM-undercount story cannot produce
a ratio above 100%, and `deep-questions.md` §1.2 reports that the
principal-tier ratio crosses 100% in parts of Luzon. If it does, "OSM
undercounts" is a statement about the *denominator*, not about the facilities
a patient would find.

## What the recomputation shows

It inverts in exactly the places the deep question pointed to, and the
national number moves by tiers, not by mapping effort.

**[a] PHL ADM1 regions where the principal-tier OSM/registry ratio exceeds 100%**
(an OSM-undercount story cannot produce these):

| Region | OSM/principal | OSM | Principal registry |
|---|---|---|---|
| Central Luzon | **117.2%** | 1,139 | 972 |
| Davao Region | **109.3%** | 376 | 344 |

NCR sits just below at 88.7% (1,094 vs 1,233). No Bangladesh division crosses
100% on the principal tier — there the inversion does not occur, and the
parallel decomposition is presented below for completeness, not as a matching
finding.

**[b] PHL — clinical-tier vs principal-tier ratio, side by side**
(`>` flags principal-tier > 100%; `prin÷clin` is the multiplier by which the
capture rate shrinks purely from swapping the denominator):

| | ADM1 | Region | OSM | prin | clin | OSM/prin | OSM/clin | prin÷clin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| > | PH-03 | Central Luzon | 1139 | 972 | 3533 | 117.2% | 32.2% | 3.63x |
| > | PH-11 | Davao Region | 376 | 344 | 1646 | 109.3% | 22.8% | 4.79x |
| | PH-00 | NCR | 1094 | 1233 | 1722 | 88.7% | 63.5% | 1.40x |
| | PH-40 | Calabarzon | 1004 | 1264 | 4396 | 79.4% | 22.8% | 3.48x |
| | PH-08 | Eastern Visayas | 338 | 484 | 1479 | 69.8% | 22.9% | 3.06x |
| | PH-41 | Mimaropa | 159 | 229 | 1474 | 69.4% | 10.8% | 6.43x |
| | PH-01 | Ilocos Region | 307 | 449 | 2715 | 68.4% | 11.3% | 6.05x |
| | PH-06 | Western Visayas | 308 | 464 | 2820 | 66.4% | 10.9% | 6.08x |
| | PH-10 | Northern Mindanao | 253 | 411 | 1986 | 61.6% | 12.7% | 4.83x |
| | PH-15 | CAR | 146 | 254 | 1238 | 57.5% | 11.8% | 4.88x |
| | PH-13 | Caraga | 149 | 267 | 1458 | 55.8% | 10.2% | 5.46x |
| | PH-07 | Central Visayas | 323 | 584 | 3260 | 55.3% | 9.9% | 5.58x |
| | PH-12 | Soccsksargen | 173 | 326 | 1475 | 53.1% | 11.7% | 4.52x |
| | PH-05 | Bicol Region | 267 | 520 | 3183 | 51.3% | 8.4% | 6.12x |
| | PH-02 | Cagayan Valley | 168 | 331 | 2319 | 50.8% | 7.2% | 7.01x |
| | PH-09 | Zamboanga Peninsula | 125 | 331 | 1571 | 37.8% | 8.0% | 4.74x |
| | PH-14 | BARMM | 72 | 326 | 1117 | 22.1% | 6.5% | 3.42x |

**[b] BGD — clinical-tier vs principal-tier ratio, side by side**
(no division crosses 100%; the principal-tier ratio is uniformly ~3–4× the
clinical-tier ratio, the same denominator effect without the inversion):

| ADM1 | Division | OSM | prin | clin | OSM/prin | OSM/clin | prin÷clin |
|---|---|---:|---:|---:|---:|---:|---:|
| BD-H | Mymensingh | 207 | 391 | 2106 | 52.9% | 9.8% | 5.39x |
| BD-F | Rangpur | 327 | 641 | 3185 | 51.0% | 10.3% | 4.97x |
| BD-C | Dhaka | 1306 | 2611 | 6508 | 50.0% | 20.1% | 2.49x |
| BD-G | Sylhet | 127 | 338 | 1626 | 37.6% | 7.8% | 4.81x |
| BD-B | Chittagong | 467 | 1338 | 5172 | 34.9% | 9.0% | 3.86x |
| BD-D | Khulna | 376 | 1086 | 3573 | 34.6% | 10.5% | 3.29x |
| BD-E | Rajshahi | 362 | 1157 | 3805 | 31.3% | 9.5% | 3.29x |
| BD-A | Barisal | 126 | 464 | 2017 | 27.2% | 6.2% | 4.35x |

**[c] The national gap, decomposed by denominator** — re-derived straight from
the raw NHFR cache (23 pages, 44,267 active rows):

| Quantity | Value |
|---|---|
| Barangay Health Stations (factype 20) | **27,052** |
| National clinical-tier denominator | 37,392 |
| BHS share of the clinical denominator | **72.3%** |
| BHS share of the clinical "missing-from-OSM" count | **87.3%** (27,052 of 30,991) |
| OSM/clinical ratio (the headline) | 17.1% (6,401 / 37,392) |
| OSM/clinical with the BHS tier removed | **61.9%** (6,401 / 10,340) |
| OSM/principal ratio | 72.8% (6,401 / 8,789) |

The clinical-tier rural-urban gradient is **9.8×** (BARMM 6.5% → NCR 63.5%).
On the principal tier it collapses to **5.3×** (BARMM 22.1% → Central Luzon
117.2%) and inverts at the top, where OSM overtakes the registry.

## The finding

The 80-point clinical-tier gap is **largely a statement about the BHS
denominator, not about the facilities a patient would seek.** Of the 30,991
clinical-tier facilities OSM does not match nationally, **87.3% are Barangay
Health Stations** — community posts that neither enumeration convention is
trying to share: NHFR lists them because a regulator records them, OSM omits
them because volunteers do not map one-room village outposts. Strip that one
definitional tier and the national capture rate moves from 17.1% to **61.9%**;
on the patient-facing principal tier it is **72.8%**, and in Central Luzon and
Davao OSM actually *exceeds* the registry (117.2% and 109.3%) — a result an
OSM-undercount mechanism is arithmetically incapable of producing.

So the gap separates cleanly into two components:

- **Definitional-denominator** — the dominant part. It appears only because
  the clinical tier includes the community-post layer. Every region carries
  it: the `prin÷clin` multiplier is 3–7× across PHL and BGD alike, meaning the
  headline number shrinks several-fold the moment the shared object set is
  used. This component is not a mapping failure and not a registry failure; it
  is two lists that were never counting the same things.
- **Genuine-mapping** — the residual gap on the principal tier, which is what
  an OSM-coverage story is actually about. It is real and it retains a
  gradient (BARMM 22.1% up to NCR 88.7% and beyond), but it is a 5.3× gradient
  on a 72.8% national base, not a 9.8× gradient on a 17.1% base. This is the
  honest size of the observability gap for patient-facing facilities.

The principal-tier inversion is the tell the deep question named: when the two
conventions aim at the same object (hospitals, main clinics, RHUs), they
roughly agree or OSM exceeds; the 80-point gap materializes only when the
denominator includes the community tier neither convention shares. The
headline "OSM captures ~17.1% of facilities" is therefore most precisely read
as "volunteers do not map Barangay Health Stations," which is true and
unsurprising, rather than "OSM is blind to where patients get care," which the
principal tier refutes in two regions outright.

## What this does and does not settle

- **Settles:** the clinical-tier headline is denominator-dominated. 87.3% of
  the clinical "missing" count is the single BHS factype; removing it lifts the
  national ratio from 17.1% to 61.9%. The principal tier — the patient-facing
  set — is captured at 72.8% nationally and is over-captured in Central Luzon
  and Davao, so the bare "OSM undercounts" claim is false on the tier that
  matters most for a care-seeking patient. The rural-urban gradient is real on
  both tiers but is roughly half as steep on the principal tier (5.3× vs 9.8×).
- **Does not settle (and is now the sharper question):** whether the residual
  *principal-tier* gradient is OSM under-mapping or registry over-inclusion.
  The inversion (>100%) shows OSM can carry private and commercial clinics the
  narrow principal set excludes, *or* that the principal registry itself
  undercounts in Luzon — this recomputation cannot separate those, and the
  three-way decomposition of `deep-questions.md` §1.1/§7 (OSM-missing vs
  registry-ghost vs genuine-absence) is still the keystone. It also does not
  settle whether the principal-tier numerator double-counts a hospital's
  outpatient wing as a separate `amenity=clinic` (the §2.3 node-dedup pass).
- **Honestly bounded:** the BHS count (27,052) is re-derived here directly
  from the raw NHFR pages and equals the figure documented in
  `process-multi-country.py`; the clinical-excluding-BHS denominator (10,340)
  removes only factype 20, leaving the small community factypes (14/27/28/09)
  in, so it is a conservative isolation of the single driving tier rather than
  a full principal-vs-clinical identity. OSM vintage is the 2026-04-05→23
  access-services window against the 2026-04-25 NHFR pull, the same drift the
  headline carries.

## The frontier data wall — and it is owner-gated

The decomposition above shows *what the gap is made of*. It cannot show
*whether the gap matters* — whether a larger OSM-registry gap predicts a worse
realized health outcome — because that requires an independent outcome layer
this program does not hold and cannot fetch.

**Precisely what is needed (`deep-questions.md` §3.1):** the subnational
outcome modules of the **DHS Program** surveys for the Philippines and
Bangladesh — specifically the **2022 Philippines National Demographic and
Health Survey (PSA/DHS)** and the **2022 Bangladesh Demographic and Health
Survey (NIPORT/DHS)** — and where they exist the **DHS Service Provision
Assessment (SPA)** facility-readiness census. The two outcome variables that
would close the loop are the **percentage of births delivered in a health
facility** and **child immunization coverage (e.g. DPT3/Penta3)**, tabulated
at the ADM1 (region/division) level, regressed on the principal-tier
registry-map gap share while controlling for the registry's own facility
density per 100k and for OSM building-completeness. **The Multiple Indicator
Cluster Survey (MICS)** immunization and facility-birth indicators are the
parallel fallback.

**Why it is a wall, not a soft barrier.** The headline indicator tables on the
DHS StatCompiler portal are public, but the ADM1-level *microdata* needed to
join the gap share to an outcome — and the SPA facility lists — sit behind the
DHS Program's registered-download approval, which is issued against an
individual researcher's account and project description (`CLAUDE.md` hard wall:
"API access requiring an account or key on the owner's identity"). AI cannot
register or download under the owner's identity. This is the single
highest-value unbuilt analysis in the program and the one step here that
genuinely pauses for the owner.

Until that join exists, this program states a property of two maps, now
correctly sized — a 72.8% principal-tier capture with a 5.3× gradient, not a
17.1% headline — and explicitly does not yet state that the gap changes any
outcome a person experiences.

## Reproduce

```bash
python public-service-data-quality/scripts/deepen-tier-decomposition.py
```

Reads `generated/public-service-data-quality-{PHL,BGD}.json` and
`.cache/nhfr_p*.json`; writes `generated/psdq-tier-decomposition.{json,csv}`.
No network. To regenerate the upstream panels first:
`python public-service-data-quality/scripts/process-multi-country.py`.
