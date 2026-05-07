# Limitations — Climate-Health Workday Loss

`attestation_chain: ai-first`

Status: §18 AI-finalized 2026-04-26.

---

## 1. What this result cannot establish

- The index does not measure actual workday loss. It measures a
  proxy combining outdoor-labor share with PM2.5 pressure.
- The result does not include heat exposure. The Lancet Countdown
  framework's labor-capacity-loss indicator is heat-driven; the
  current pipeline is PM2.5-only.
- The result does not produce a country deficiency ranking. The
  headline is the top-3 set, treated as a measurement-pressure
  cluster, not a policy-failure ranking.

## 2. Source-side limitations

- WDI EN.ATM.PM25.MC.M3 is a national mean. In large-area DMCs (IND,
  CHN, IDN) it conceals dramatic within-country variance.
- Pacific microstates and selected low-monitor-density DMCs (AFG,
  MMR, KHM, LAO, TLS) have imputed PM2.5 values; the §18.5
  upgrade-pass replaces these with ACAG-V6 satellite surface.
- WDI employment series for small economies are noisy.

## 3. Method-side limitations

- The 5 µg/m³ floor is WHO-anchored; the 45 µg/m³ cap is heuristic.
  The sensitivity suite shows the top-3 set is robust; the top-5
  shifts under cap perturbation.
- The 0.5 industry weight is split-the-difference for mixed
  indoor/outdoor industry work.

## 4. DMC-coverage limitations

10 of the 44 ADB DMCs are not rankable due to missing inputs;
documented in `coverage.md`.

## 5. Synthesized reviewer objections quoted verbatim

(per `review-external.md` §4 and `CONSTITUTION.md` §18.4)

### 5.1 From C-1 (Lancet Countdown), synthesized

> Using PM2.5 alone — without heat — produces an incomplete pressure
> measure. The article must label the index as the PM2.5-only subset.

### 5.2 From C-3 (Dalhousie ACAG-V6), synthesized

> WDI EN.ATM.PM25.MC.M3 is derived from monitor-station data with
> coverage gaps. ACAG-V6 satellite-derived 1-km gridded estimate
> fills the gaps; the upgrade-pass is required for any human-final
> attestation.

### 5.3 From C-5 (WB DECDG), synthesized

> PM2.5 monitor density correlates with HDI. Low-HDI DMCs have very
> few stations and the national mean is interpolated. AFG #1 carries
> an "imputed input" caveat.

## 6. Banned framings

- This result does **not** rank DMCs as deficient.
- The headline is the top-3 measurement-pressure cluster, not a
  ranking.
- §13.3 framing observed throughout.
