# Explore: diverse reader shells

`attestation_chain: ai-first` · 2026-08-04

Exploration only. Production `Topic.tsx` and Home are unchanged until an
owner decision after live comparison.

## Live story packages (2026-08-04)

| Program | Family | Default shell | Source of package |
|---|---|---|---|
| `public-data-freshness` | observability | product | two clocks |
| `public-service-data-quality` | observability | workbench | registry–map |
| `climate-health-workdays` | invalidation | product | proxy fail |
| `remittance-resilience` | distribution | product | dependence × cost |

Canonical files live at `{program}/story.json` and sync into
`reporting-site/public/programs/{slug}/story.json`.

### Routes
- `/explore` — hub, critique, family table, pilots
- `/explore/{product|workbench|chapter}/{slug}` — side-by-side shells
- `/{slug}` — **default shell** when story package exists
- `/{slug}?shell=workbench|chapter` — other shells on the topic route
- `/{slug}?view=classic` — old tabbed UI
- `/{slug}?view=evidence|data|brief|…` — classic tabs still work

Numbers come from committed results, summaries, and article frontmatter —
not model memory.

## Shells

| Shell | Personality | First interaction |
|---|---|---|
| Product | Modern research product | Finding sentence → hero → metrics → limits |
| Workbench | Evidence lab bench | Gates + filterable domain rows + absence patterns |
| Chapter | Economist / flagship | Hero, key messages, metric band, TOC, serif long-form, print |

Task31 is the **craft reference** for Chapter only.

## Family → default shell (proposal)

| Family | Programs | Default shell |
|---|---|---|
| observability | PSDQ, air-monitoring, access-services, public-data-freshness | workbench (product for pilot freshness) |
| invalidation | climate-health-workdays, disaster-recovery-lag, grid-reliability-heat, school-heat, social-protection, water-stress, port-hinterland, food-price | product |
| distribution | remittance, migration, coastal, flood-market, digital, invisible-urbanization | product |
| synthesis | none in factory; Task31 class | chapter |

## Decision still needed from owner

1. Accept family → shell defaults, or edit the table.
2. Home: pure finding gallery vs hybrid institutional frame.
3. Chapter HTML offline export: first-class route or build artifact only.
4. Which 1–2 topics cut over first after pilot sign-off.

## Non-goals this pass

- No claim changes, no pipeline re-runs, no CONSTITUTION edits.
- No mass rewrite of Showcase pages.
- No forcing Task31 chrome onto every topic.
