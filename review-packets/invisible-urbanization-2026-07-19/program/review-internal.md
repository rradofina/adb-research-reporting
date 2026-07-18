# Internal adversarial review

`attestation_chain: ai-first` · Closed 2026-07-19

## 1. Is the definition gap an error metric?

**Critique.** No. WDI and GHSL use different constructs and population
systems. Calling the gap “under-counting” would assume GHSL is ground truth.

**Response.** Accepted. The paper uses “difference,” “gap,” and “disagreement.”
It reports both directions, does not convert percentage points to people, and
states that the measures answer different questions.

## 2. Does the paper finally measure legal invisibility?

**Critique.** No. GHS-DUC classifies GADM units with a standardized rule; it
does not contain national statutes, census designation histories, municipal
boundaries, or service mandates.

**Response.** Accepted. The title and claims are about definition dependence.
The phrase “embedded urban population” is defined mechanically. Legal
misclassification and policy neglect remain gated.

## 3. Are country values duplicated by territories?

**Critique.** The raw GHS-DUC level-0 file contains multiple GADM fragments for
some `GID_0GHSL` codes. A direct WDI join duplicated China, India, and Pakistan
in the first run.

**Response.** Fixed. The script now sums population counts by `GID_0GHSL`
before recomputing the GHSL urban share. The corrected 2020 panel has 43 unique
GHSL economies and 40 complete GHSL–WDI pairs.

## 4. Is the scale comparison confounded by coverage?

**Critique.** Yes in the first draft: levels 1, 2, and 3 covered 40, 34, and 13
economies. The rising share could have reflected sample composition.

**Response.** Fixed. The headline scale comparison uses the same 13-economy
intersection at all three levels. Changing-sample estimates remain in the JSON
and are labelled non-comparable.

## 5. Does a declining embedded share refute ongoing hidden growth?

**Critique.** Not necessarily. Units can accumulate urban-cell population and
then cross the GHS-DUC threshold.

**Response.** Tested. The 2000–2020 unit decomposition closes exactly. Units
that remained rural gained 13.9 million urban-cell residents, while 678 units
crossing to town/city removed 43.3 million from the embedded stock.

## 6. Is ±50% sensitivity satisfied?

**Critique.** The 20-year window is arbitrary.

**Response.** The analysis recomputes the transition result at 10 and 30 years.
The embedded-stock change remains negative in all three windows. The headline
definition gap itself has no analyst-set threshold.

## 7. Is the result actionable?

**Critique.** A cross-definition gap alone cannot allocate budgets.

**Response.** Accepted. The action is diagnostic: display both measures and
trigger a country-specific legal, boundary, and service validation when they
diverge. Resource allocation remains out of scope.

## Review decision

The measurement claim passes at PP. A legal-classification, service, or welfare
claim does not pass and requires the next evidence upgrade.
