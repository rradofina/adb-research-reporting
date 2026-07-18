# Hook card — low-elevation urban growth

`attestation_chain: ai-first` · Design freeze: 2026-07-19

## Source object

GHS-UCDB R2024A V1.2, Exposure and General Characteristics thematic files,
European Commission Joint Research Centre. The unit is a quality-controlled
urban centre delineated by the Degree of Urbanisation. The files report
population and built-up surface inside low-elevation coastal zones (LECZ) at
5-year epochs from 1975 to 2030. Access is anonymous; the license is CC BY 4.0.
Raw ZIP files stay in `.cache/`; scripts, checksums, derived rows, and figures
are committed.

## First visual

A ranked urban-centre chart of the absolute change in population living below
10 metres elevation from 2000 to 2020, with the 5-metre result shown as a
stricter comparison. The old national proxy's named economies appear only as
context, never as the empirical ranking.

## Possible claim

Among ADB developing-economy urban centres with complete GHS-UCDB observations,
growth in low-elevation population is concentrated in a small set of named
settlements, and that settlement-scale pattern differs from the inherited
country score.

## Decision user

City and country climate-resilience teams deciding where a comparable public
screen can justify deeper local validation of elevation, drainage, protection,
tenure, and service conditions.

## Falsifier

Defer the hook if the V1.2 files do not identify DMC urban centres reliably;
if low-elevation population is missing for most centres; or if the only visible
result is a generic country-size ranking with no interpretable settlement-level
heterogeneity.

## Landscape gap

Global LECZ research establishes that people and built assets occupy low-
elevation coastal zones. The contribution tested here is narrower: whether a
single open, harmonised urban-centre database can expose *where recent growth
inside those zones occurred* across ADB developing economies, while preventing
that observable pattern from being mislabeled as informality or policy failure.

## Stop condition

If no stable settlement-scale result survives the 5/10-metre definition and
10/20/30-year windows, retain the source-coverage finding, retire the national
score, and rotate without building a full publication ladder.
