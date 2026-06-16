# L2 Hook Sprint: Shock-Payment Rails After Disasters

`attestation_chain: ai-first`
Date: 2026-06-16
Goal level: L2 hook sprint

## Decision

Promote this as a new program prospectus candidate.

The hook is not a public finding yet. It is a topic-creation result: public
sources can be joined into a first visual that separates disaster exposure,
social-protection coverage, account ownership, and actual digital-payment use.
That creates a sharper question than a generic "digital payments and social
protection" topic.

## Question Tested

Where do public sources show disaster exposure, but also show that headline
account ownership is a weak proxy for the payment-use rails needed for
post-shock delivery?

## Public Data Object

The sprint joins three public-source objects already aligned to DMCs:

- The repo's social-protection panel from World Bank ASPIRE, Global Findex,
  and WDI poverty indicators.
- The repo's disaster exposure panel from EM-DAT country profiles via the HDX
  mirror.
- Fresh World Bank API pulls for account ownership, electronic payment use,
  government-payment account use, and active account use.

The payment-use upgrade matters because account ownership and payment use are
not the same concept. The sprint keeps those variables separate and treats the
account-minus-digital-use gap as a source-disagreement diagnostic, not a
readiness score.

## Generated Artifacts

| Artifact | Path |
|---|---|
| Script | `research/topic-sprints/scripts/sprint-shock-payment-rails.py` |
| CSV | `research/topic-sprints/generated/shock-payment-rails-sprint.csv` |
| JSON | `research/topic-sprints/generated/shock-payment-rails-sprint.json` |
| Rough chart | `research/topic-sprints/generated/charts/shock-payment-rails-scatter.png` and `.svg` |

Reproduce:

```powershell
python research/topic-sprints/scripts/sprint-shock-payment-rails.py
```

## Data Sanity Checks

The script produced 42 DMC rows. It joined disaster-event frequency for 38
rows, direct digital-payment-use data for 27 rows, government-payment account
use for 21 rows, and active-account data for 26 rows. The first scatter visual
has 26 plotted rows with both disaster frequency and digital-payment-use data.

World Bank API metadata in the generated JSON records these source update
dates: account ownership `2026-04-08`, electronic payment use `2022-09-23`,
government-payment account use `2022-09-23`, and active account `2019-02-27`.
That vintage spread is part of the caveat, not a nuisance to hide.

The sprint table shows why the topic is non-generic. Among economies with
joined rows, India has 15.54 recorded EM-DAT disasters per year and 24.69% of
adults using electronic payments, while its account-minus-digital-use gap is
64 percentage points. Viet Nam has 7.69 recorded disasters per year, 16.10%
digital-payment use, and a 54 percentage point account-minus-digital-use gap.
Pakistan has 6.12 recorded disasters per year and 14.90% digital-payment use.
Those are screening facts, not a ranked headline.

## Visual QA

The chart rendered as a nonblank PNG and SVG. The left panel is a scatter:
EM-DAT recorded disasters per year on the x-axis, electronic payment use on
the y-axis, bubble size from total affected event records, color from ASPIRE
social-protection coverage, and hollow markers where ASPIRE coverage is
missing. The right panel shows the largest account-minus-digital-payment-use
gaps.

What the chart makes visible:

- Disaster exposure, social-protection coverage, and payment-use rails do not
  collapse into one simple readiness measure.
- Account ownership can materially exceed digital-payment use, so account
  ownership should not be used as the delivery-rail proxy without a caveat.
- The strongest next question is about source observability and payment-use
  validation, not about ranking economies.

## What This Does Not Mean

This is not evidence that emergency transfers failed or succeeded in any
economy. Electronic payment use is not shock-payment receipt. Government
payment account use is not an emergency-transfer channel measure. ASPIRE
coverage pools multiple social-protection instruments and reporting years.
EM-DAT affected totals are event records and may double-count people across
events.

This is also not a readiness index. Composite scoring would be premature at
this stage. The sprint only shows that the public data surface is strong enough
to justify a prospectus on the mismatch between shock exposure and observable
payment rails.

## Prospectus If Promoted

Working title:

**After the Shock, Can the Payment Rail Be Seen?**

First program question:

Where do public disaster, social-protection, and financial-inclusion sources
show that post-shock delivery capacity is hard to observe because coverage,
ownership, and actual payment use are measured by different systems and
vintages?

First L3 tasks:

1. Verify the World Bank/DataBank metadata and licenses for each payment-use
   indicator and preserve a retrieval record.
2. Add ID4D or comparable public identity-coverage variables only if they can
   be joined with transparent vintages.
3. Split ASPIRE coverage by social-assistance type where public source detail
   allows it.
4. Add one event-timeline case check for a high-exposure DMC so the topic does
   not stay at national annual averages.
5. Design a publication visual that shows source vintage, concept mismatch,
   and non-claims as first-class chart elements.
