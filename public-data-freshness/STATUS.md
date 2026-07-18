# Public data freshness — operating status

`attestation_chain: ai-first` · Last updated: 2026-07-19

- **Finding:** At a three-year rule, calendar age and indicator-relative lag
  disagree for 138 of 709 observed baseline cells (19.5%).
- **Decision:** Reshape the broad claim: removing environment lowers
  disagreement to 9.2%, below the frozen 10% gate.
- **Stage:** AI-first Screening Result; full evidence packet and publication
  ladder prepared for gate and browser verification.
- **Reader value:** A dashboard can distinguish shared production cadence from
  economy-specific lag without hiding calendar age or missingness.
- **Coverage:** 709 of 756 baseline cells observed across 42 economies and 18
  indicators; Pacific small-island coverage is lower than elsewhere.
- **Sensitivity:** Set-size tests pass; the threshold test is large, so the
  cutoff must remain visible.
- **Source limit:** One frozen upper-set WDI code is archived; the ADB context
  CSV is behind a documented Cloudflare challenge and supplies no panel value.
- **Stop:** Do not take another generic portal scan. The next upgrade requires
  formal producer release calendars and ingestion dates.
- **Next move:** Publish, verify, commit, then rotate to the next flagship.
