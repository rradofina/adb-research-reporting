# Sensitivity — Food-price construct validation

`attestation_chain: ai-first` · 2026-07-19

The main definition uses a 20% year-on-year log price-change threshold, a
one-month-lag precipitation z-score of -1 or lower, a 50% market-share rule for
broad waves, and a 34% maximum dry share for a non-dry wave.

Each arbitrary threshold is varied by ±50%:

- price change: 10%, 20%, 30%;
- dry-rainfall z-score: -0.5, -1.0, -1.5;
- broad-wave market share: 25%, 50%, 75%;
- maximum dry share: 17%, 34%, 51%.

The 3×3×3×3 factorial contains 81 runs. Dry alignment ranges from 0% to
48.84% of corrected spike cells and remains a minority in every run. That
direction is stable.

Broad non-dry wave counts range from 0 to 44 months; dry-cluster counts range
from 0 to 27. These counts are threshold-sensitive and are not headline
quantities.

Rainfall-lag checks at 0, 1, 3, and 6 months produce dry-aligned shares of
11.84%, 11.18%, 5.92%, and 8.55%, respectively. The result does not depend on a
single lag producing a majority alignment.
