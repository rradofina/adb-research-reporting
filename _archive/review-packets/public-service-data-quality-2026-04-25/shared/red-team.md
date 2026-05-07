# External Red Team Roster

Governed by `CONSTITUTION.md` §9.3. This file is a cross-cutting governance
asset. Publication-ready claims (§7.2) require review by at least two
external readers drawn from this roster before release. Their comments and
our responses are committed as `review-external.md` inside the program
folder.

Updated: 2026-04-24 *(roster empty; sourcing strategy committed below so the
owner can populate with real names).*

---

## Reviewer criteria

Each reader should bring one of the following competencies; combined, the
team must cover all three for any given program:

1. **Measurement** — statistical measurement, index construction,
   aggregation methods, or population/geographic weighting.
2. **Domain** — subject matter of the specific program (health-service
   access, air quality, ICT, urbanization, remittances, climate risk, etc.).
3. **Statistical or econometric** — identification, sensitivity testing,
   causal or descriptive inference, reproducibility review.

Where possible, at least one reader should be affiliated with an ADB DMC
research institution, to ground the review in local data realities.

---

## Conflict of interest

A reader may not review a program where they:

- Co-authored the program's first testable claim or any of its inputs.
- Have a financial or supervisory relationship with the program owner at
  the time of review.
- Are currently in the ADB promotion, hiring, or grant-decision chain
  affecting the program owner.

Reviewers disclose any other potential conflict in writing before
accepting. Disclosures are committed alongside their review.

---

## Review process

1. Program owner emails a draft evidence packet (code, generated
   artifacts, `literature.md`, sensitivity tables, draft write-up) to two
   or more roster members.
2. Readers return written comments within 4 weeks. Shorter turnarounds are
   not expected; longer must be negotiated in advance.
3. Program owner responds in writing, item by item, committed as
   `review-external.md`.
4. Where a reviewer's objection is not resolved, it is quoted verbatim in
   the output's limitations section.
5. Reviewers are credited by name in the acknowledgments, with their
   permission. They are not authors.

Reviewers are not paid by the program. Compensation, if any, follows ADB
or institutional norms and is disclosed.

---

## Sourcing strategy

The repository owner populates this roster before the first program
reaches the publication-ready gate. The strategy below is the target
portfolio; actual names are the owner's to recruit and are not generated
by AI.

### Measurement / statistical competency

Target at least three named readers from:

- OPHI (Oxford) research fellows working on multidimensional poverty,
  capability approach, or measurement methodology — especially those
  connected to the Alkire group.
- UNDP HDRO technical staff and consultants working on HDI, GDI, and
  related indices.
- World Bank Development Data Group (DECDG) researchers and Statistical
  Performance Indicators (SPI) team.
- ADBI research fellows working on measurement and statistical capacity
  in Asia and the Pacific.
- Academic measurement specialists at LSE International Development, OPHI,
  Ibero-American Institute for Economic Research (IAI), University of
  Göttingen, and equivalent programs publishing in Journal of Economic
  and Social Measurement, Demography, or Population and Development
  Review.

### Domain competency (varies by program)

Target readers whose program-specific expertise is published in the
journals the program targets under §10.2:

- **Access to services / health geography:** Population Health Metrics,
  KEMRI-Wellcome Trust Research Programme, WorldPop Hub (Southampton),
  Macharia / Snow network, Nicolas Ray (University of Geneva).
- **Pollution / air quality:** WHO Air Quality team, HEI (Health Effects
  Institute), Chalmers/Stockholm Environment Institute, IIASA pollution
  group, Dalhousie atmospheric composition (van Donkelaar / Martin).
- **Digital development:** ITU Telecom Development Bureau researchers,
  IFMR LEAD, M-Lab research affiliates, Oxford Internet Institute.
- **Urbanization / building growth:** Joint Research Centre GHSL team,
  HeiGIT/Heidelberg (Zipf, Herfort), Microsoft AI for Good (building
  footprints), UN-Habitat Global Urban Observatory.
- **Remittances / migration:** KNOMAD researchers, World Bank Global
  Knowledge Partnership on Migration and Development, IZA migration
  cluster.
- **Climate-health / climate adaptation:** Lancet Countdown on Health and
  Climate Change authors, Tsinghua School of Environment, NUS Lee Kuan
  Yew School climate group.

### DMC-affiliated competency

Target at least one reader per program who is affiliated with a research
institution in a DMC where the program's pilots run:

- **Philippines:** UPecon Foundation, PIDS (Philippine Institute for
  Development Studies), Asian Institute of Management Policy Center, Ateneo
  School of Government.
- **Bangladesh:** BIDS (Bangladesh Institute of Development Studies), BRAC
  Institute of Governance and Development, BRAC James P. Grant School of
  Public Health.
- **Indonesia:** LPEM FEB UI, SMERU Research Institute, CSIS Jakarta.
- **Pakistan:** PIDE (Pakistan Institute of Development Economics), Center
  for Research in Economics and Business (LSE Pakistan), LUMS.
- **Nepal:** Nepal Rastra Bank Research Department, SAWTEE.
- **Vietnam:** CIEM (Central Institute for Economic Management), VASS
  Institute of Economics.
- **Sri Lanka:** IPS (Institute of Policy Studies of Sri Lanka).
- **Pacific DMCs (PNG, Fiji, Solomon Islands, Tonga, Samoa, Vanuatu,
  Timor-Leste, Kiribati, etc.):** Pacific Community (SPC) Statistics for
  Development Division, University of the South Pacific (USP), Pacific
  Islands Forum Secretariat, ANU Development Policy Centre (Devpolicy).
- **Mongolia:** National Statistics Office research unit, Economic Research
  Institute.
- **Central Asia and Caucasus:** OSCE Academy in Bishkek, ADBI Tokyo (for
  Central Asia), University of Central Asia, ISET Policy Institute
  (Tbilisi).

---

## Outreach template

A copy of the template below is adapted per reader. Keep the email short;
reviewers read many requests.

```
Subject: Red-team review request for a research artifact — [program name]

Dear [Name],

I am [Raymond Adofina], working at [role / institution]. I am writing to
ask whether you would be willing to serve as an external red-team reviewer
for a research artifact on [one-line topic]. The artifact is computed
entirely from public data under a committed research constitution; the
repository, reproducibility standard, and AI-transparency disclosure are
at [public repo URL once published].

The artifact I would like your review of is [one-line artifact
description]. Concretely, the review would consist of:

- reading the linked artifact and methodology (approximately [X] pages);
- flagging issues on measurement, identification, or reproducibility;
- optionally writing a short response.

I estimate [Y] hours of effort. Turnaround is 4 weeks from acceptance.
Credit is by acknowledgment; you are not an author. I will commit your
written comments verbatim alongside my written responses.

Would you be willing to review, or recommend someone from your team?

Sincerely,
[Raymond Adofina]
```

---

## Roster template (owner to populate)

Private contact details are held by the repository owner, not committed
to this file. Only name, affiliation, and public competency are public.

| Name | Affiliation | Competency | Region focus | COI notes | Availability | Programs served |
|---|---|---|---|---|---|---|
| *(to be filled)* | *(institution)* | Measurement / Domain / Stats | *(DMC or regional)* | *(none / disclosed)* | *(e.g., 2 reviews/year)* | *(which programs)* |

---

## Minimum roster size

Before the first program reaches publication-ready, this roster must list
at least:

- 2 measurement or statistical reviewers.
- 2 domain reviewers covering the program's specific topic.
- 1 DMC-affiliated reviewer for the economies in scope.

This is the §9.3 precondition. A program owner may not request a
publication-ready gate review until this minimum is met.

## Update cadence

Reviewed yearly by the repository owner. Additions and removals are
recorded in the amendment log below with the date and reason.

### Amendment log

- **2026-04-24** — Roster template committed. No names yet. Sourcing
  strategy (institutions to target and outreach template) added so the
  owner can recruit real readers. AI has not filled names and will not do
  so; per `CLAUDE.md` naming specific humans requires the owner's actual
  network.
