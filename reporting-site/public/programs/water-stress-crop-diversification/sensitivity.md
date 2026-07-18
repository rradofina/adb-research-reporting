# Sensitivity — Water stress × crop diversification

`attestation_chain: ai-first` · Recomputed 2026-07-18

## Inherited screen

The published set is the actual raw top four in only two of seven saved runs.

| Run | Raw top four | Exact published-set match? |
|---|---|---:|
| Baseline | TKM, PAK, AZE, UZB | No |
| Water cap −50% | TKM, PAK, AFG, AZE | Yes |
| Water cap +50% | TKM, PAK, UZB, AZE | No |
| Water ceiling −50% | TKM, PAK, AFG, AZE | Yes |
| Water ceiling +50% | TKM, PAK, UZB, AZE | No |
| Yield reference −50% | TKM, PAK, AZE, UZB | No |
| Yield reference +50% | PAK, TKM, AZE, UZB | No |

The old “stable top four” was the four-member intersection of seven top-five
lists, not a set occupying the raw top four in every run.

## Source-upgraded diagnostic

The diagnostic uses available-water stress, crop HHI, and rural population.
The arbitrary water ceiling and crop/rural exponents are each tested at 0.5×,
1×, and 1.5×, giving 27 specifications.

- Afghanistan, Sri Lanka, Pakistan, and Turkmenistan appear in all 27 top
  fives.
- Uzbekistan appears in 21.
- Kazakhstan and Tajikistan appear in 3 each.
- Azerbaijan appears in none.
- Each specification shares four or five members with the baseline diagnostic
  top five.

## Component ablation

| Specification | Top five | Published overlap |
|---|---|---:|
| Water only | TKM, UZB, PAK, LKA, TJK | 2 |
| Crop HHI only, aligned sample | MYS, KHM, BGD, KAZ, MNG | 0 |
| Rural share only | PNG, LKA, AFG, TJK, TLS | 1 |
| Water × crop HHI | TKM, AFG, UZB, PAK, LKA | 3 |
| Water × rural share | LKA, TKM, PAK, UZB, TJK | 2 |
| Crop HHI × rural share | AFG, BGD, KHM, MDV, VNM | 1 |
| All three | TKM, AFG, LKA, PAK, UZB | 3 |

The aligned crop-HHI-only set differs from the full 41-economy crop-HHI top
five because all five full-sample leaders lack water data. Sensitivity cannot
repair that coverage selection or the missing basin-crop unit.
