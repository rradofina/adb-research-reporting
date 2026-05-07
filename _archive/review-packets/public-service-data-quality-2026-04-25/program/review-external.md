# External red-team review — Public Service Data Quality

Status: **open** — reviewers not yet recruited.

Per `CONSTITUTION.md` §9.3 and `red-team.md`. The roster is empty as of
2026-04-25 and the program owner is recruiting. The minimum roster
required by §9.3 before this gate can advance is two named reviewers
spanning measurement, domain, and DMC-affiliated competencies. AI does
not fill names.

---

## 1. Reviewers

| Name | Affiliation | Competency | DMC focus | COI disclosure | Acceptance date |
|---|---|---|---|---|---|
| *(pending)* | *(institution)* | Measurement / Domain / Stats | *(DMC or regional)* | *(none / disclosed in §1.1)* | *(YYYY-MM-DD)* |
| *(pending)* | *(institution)* | Measurement / Domain / Stats | *(DMC or regional)* | *(none / disclosed in §1.1)* | *(YYYY-MM-DD)* |

### 1.1 COI disclosures

(quoted from each reviewer's written acceptance email)

### 1.2 Sourcing strategy applied to this program

Per `red-team.md` §sourcing-strategy, the targeted institutions for this
program's first SR → PR gate are:

- **Measurement:** OPHI (Oxford), UNDP HDRO, World Bank DECDG / SPI team.
  Highest priority because the program's claim depends on what
  "measurement gap" means.
- **Domain — health geography:** Macharia / Snow / Okiro network
  (KEMRI–Wellcome / WorldPop), Ray (University of Geneva), Maina, South
  (the same authors who wrote the Africa-side methodological literature
  this program builds on, per `literature.md`).
- **Domain — OSM data quality:** Herfort / Zipf (HeiGIT, Heidelberg);
  the authors of `herfort2023osm`.
- **DMC-affiliated, Philippines:** PIDS (Philippine Institute for
  Development Studies); UPecon Foundation; Asian Institute of Management
  Policy Center.
- **DMC-affiliated, Bangladesh:** BIDS (Bangladesh Institute of
  Development Studies); BRAC Institute of Governance and Development;
  BRAC James P. Grant School of Public Health.

The owner's outreach uses the template at `red-team.md` §outreach-template.

## 2. What is reviewed

(send the same evidence packet committed at the time of the review request)

- `literature.md` (commit *(hash)*)
- `pre-registration.md` (commit *(hash)*)
- `sensitivity.md` and `sensitivity-runs.json` (commit *(hash)*)
- `coverage.md` (commit *(hash)*)
- `results.md` (commit *(hash)*)
- `review-internal.md` (commit *(hash)*)
- `generated/public-service-data-quality-{PHL,BGD}.{json,csv}` (commit *(hash)*)
- `articles/measurement-gap-philippines-bangladesh.md` (commit *(hash)*)
- `limitations.md` (commit *(hash)*)

The packet is built by `scripts/build-review-packet.sh` (TODO) which
copies these files into a single archive and writes a manifest of
included files with their SHA-256 hashes.

## 3. Reviewer comments — verbatim

(quoted verbatim from each reviewer's written response, with the
reviewer's permission. Reviewers who decline to make their comments
public are listed only by name; their feedback informs the response but
is not quoted here.)

### 3.1 Reviewer 1 — *(name pending)*

> *(comment)*

### 3.2 Reviewer 2 — *(name pending)*

> *(comment)*

## 4. Owner responses — written

(item-by-item)

### 4.1 Response to reviewer 1

> *(response)*

### 4.2 Response to reviewer 2

> *(response)*

## 5. Unresolved items

| Reviewer | Objection (verbatim) | Treatment |
|---|---|---|

Unresolved objections move to `limitations.md` §5 verbatim with the
reviewer's permission.

## 6. Acknowledgments

> Acknowledgments: *(Reviewer 1 name, affiliation), (Reviewer 2 name,
> affiliation)* reviewed an earlier draft and provided written comments;
> any remaining errors are the author's.

## 7. Owner attestation

| Field | Value |
|---|---|
| ≥ 2 named external reviewers from `red-team.md` roster | *(yes / no)* |
| `red-team.md` §minimum-roster-size met | *(yes / no)* |
| All written comments quoted verbatim above | *(yes / no)* |
| Each comment has a written response | *(yes / no)* |
| Unresolved comments quoted in `limitations.md` §5 | *(yes / no)* |
| Reviewer acknowledgment paragraph drafted with reviewer permission | *(yes / no)* |
| Date closed | *(YYYY-MM-DD)* |
| Commit hash | *(hash)* |
