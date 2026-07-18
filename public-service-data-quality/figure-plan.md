# PSDQ figure plan

`attestation_chain: ai-first`

The figure spine communicates source disagreement, robustness, and the
validation boundary. It does not treat either registry or OpenStreetMap as
ground truth and does not convert a mapping gap into a service-access claim.

## Figure contract

| Figure | Research role | Literature link | Source object | Unit and coverage | Transform | Claim test | Uncertainty | Claim role | Mobile proof | Fallback |
|---|---|---|---|---|---|---|---|---|---|---|
| Philippines ADM1 choropleth | Show the spatial distribution of registry-map disagreement | `macharia2025mapping`; `maina2019africa` | `generated/public-service-data-quality-PHL.csv` | 17 Philippine ADM1 regions; clinical-tier OSM features and NHFR registry rows | `scripts/build-choropleth.py` | The claim weakens if most regions approach the planning screen or the pattern is driven by one region | Registry definition, OSM completeness, and polygon assignment | Descriptive / main claim | Existing 375 px route QA | ADM1 table in `results.md` |
| Bangladesh ADM1 choropleth | Show whether the second pilot displays the same broad disagreement | `macharia2025mapping`; `maina2019africa` | `generated/public-service-data-quality-BGD.csv` | 8 Bangladesh divisions; clinical-tier OSM features and DGHS registry rows | `scripts/build-choropleth.py` | The cross-pilot statement weakens if division ratios approach the screen or reverse the source relationship | Only 8 divisions; registry and OSM definitions differ | Descriptive / cross-pilot validation | Existing 375 px route QA | Bangladesh ADM1 table in `results.md` |
| Philippines ADM3 poverty context | Make the official poverty-data coverage and missingness visible without claiming causality | `psa2023sae` | `generated/psdq-phl-admin3-poverty-context.csv` | 1,642 Philippine city/municipality polygons; 2023 official poverty incidence where sourced | `scripts/build-choropleth.py` | The context layer is unusable if joins fail or missing rows are hidden | Ten source-missing polygons remain gray; no causal link is estimated | Context / limitation | Existing 375 px route QA | Coverage counts and joined CSV |
| Research hero | State the cross-source disagreement in one view | `macharia2025mapping` | Committed PHL and BGD summary outputs | Two public-data pilots | `scripts/build-thumbnail.py` | Remove if it implies a facility-quality or access ranking | Summary view suppresses subnational heterogeneity | Hero | Existing 375 px route QA | Headline and country ratios |
| Sensitivity range | Show whether completed definition changes move either pilot above the planning screen | `macharia2025mapping` and pre-registration §6 | `sensitivity-runs.json` | Country clinical-tier ratios across every completed PHL and BGD sensitivity run | `scripts/build-figure-dossier.py` | The headline weakens if a tested definition reaches or crosses 30% | The polygon-dilation run remains uncompleted and is excluded | Sensitivity / robustness | Required after embedding | Sensitivity table in `sensitivity.md` |
| Validation wall | Show what the public-source review resolved and what it could not resolve | PSDQ evidence-ladder methods; no external validation claim | `generated/evidence-ledger.json` | Targeted Bangladesh validation rows and closure permissions | `scripts/build-figure-dossier.py` | Any nonzero AI-actionable closure count would change the visual and require a row-level audit | Human/source-owner validation was not performed | Limitation as evidence / infographic | Required after embedding | Headline counts in the evidence ledger |

## Placement

1. Keep the two ADM1 maps beside their country results.
2. Keep the poverty-context map in the data-upgrade passage with its non-causal label.
3. Place the sensitivity range inside the sensitivity suite, immediately before the numeric table.
4. Place the validation-wall infographic in limitations, beside the statement that public review did not authorize row closure.

The six logical figures meet the lower diagnostic range for a PR package. No
additional chart is authorized until it adds a distinct claim test,
heterogeneity result, falsification, uncertainty view, or limitation.
