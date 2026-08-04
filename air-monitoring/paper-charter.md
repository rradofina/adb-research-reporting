# Paper Charter — Air Monitoring Observability

`attestation_chain: ai-first`

A national PM2.5 figure can appear on a dashboard even when the public
ground-monitor trail is thin, model-dependent, or not auditable at station
level. ADB country teams, national statistics offices, environment agencies,
and health ministries need to know whether that figure is supported by
public station evidence they can actually inspect.

The decision problem is not "which economy is worst." It is where a
monitoring investment, data-sharing agreement, or station documentation
request would most improve the public evidence base for PM2.5 measurement.

## 1. Policy/statistical problem

Air-quality exposure statistics are only as strong as the public monitor
evidence behind them. National series, open station maps, and regulator
portals each answer a different question; none by itself proves that a named
station is the same physical monitor, currently operating to a verified
grade, or ready for a population-coverage claim.

## 2. Measurement blind spot

Existing public views are incomplete in different ways:

- National PM2.5 exposure series are too coarse for station-siting questions.
- OpenAQ-visible station counts do not by themselves prove regulatory-grade
  measurement, current operation, calibration status, or official network
  completeness.
- Official portals can show station rows and live values without proving a
  same-station OpenAQ crosswalk or complete grade basis.
- Satellite-derived PM2.5 surfaces can fill geographic coverage, but they do
  not replace station-level evidence for regulatory enforcement, calibration,
  public alerting, or source attribution.

The report should therefore study **public observability of the monitoring
system**, not only pollution exposure.

## 3. Reader-facing question

Which public station, method, identity, grade, and denominator evidence is
strong enough to support air-monitoring coverage language, and where do the
public sources still block that language?

## 4. Unit of analysis

The program now has four nested units:

- Economy-level screen: OpenAQ-visible PM2.5 monitoring and national PM2.5
  context.
- Station-row evidence: official station rows, OpenAQ rows, station names,
  IDs, coordinates, owner/provider fields, dashboard status, and method text.
- Candidate identity join: whether an official row and an OpenAQ row can be
  treated as the same station.
- Radius-denominator diagnostic: GHSL/ACAG cells near candidate station rows,
  explicitly blocked from coverage claims until identity and grade gates pass.

The paper should lead with the station-row and gate logic, not with a country
ranking.

## 5. Source hierarchy

Use this public-source ladder in the article and evidence page:

1. Official regulator or meteorological agency station inventory.
2. Official station detail/dashboard/API page with station-specific evidence.
3. Public OpenAQ row with owner/provider and `isMonitor` metadata.
4. Public method, SOP, calibration, maintenance, or standards source.
5. Public source-access route for missing station-specific documents.
6. Satellite/gridded population context for denominator diagnostics.

Lower rungs can support follow-up and context. They cannot override a failed
station identity, current-status, or monitor-grade closure gate.

## 6. Claim type

Current claim type: **diagnostic measurement audit**.

Allowed language:

- public evidence can identify station rows, source trails, and claim blockers;
- station-radius denominator joins can be dry-run as diagnostics;
- the current public record blocks monitor-grade and coverage claims where
  station identity, current-status, calibration, or certificate evidence is
  absent.

Blocked language:

- station service-area estimates;
- people served by monitors;
- complete regulatory network inventories;
- reference-grade monitor counts;
- PM2.5 exposure changes caused by monitoring coverage;
- country performance ranking.

## 7. Main visual

The lead visual should be an evidence ladder, not a leaderboard:

`OpenAQ row -> official row -> candidate same-station evidence -> method/status evidence -> grade closure -> radius denominator -> coverage language`

Each gate should show which rows pass, which rows remain blocked, and which
public document would be needed next. The existing BMKG closure gate, Georgia
verification wall, station-identity validation gate, and station-radius
coverage-claim gate are the model panels.

## 8. Validation target

The program becomes stronger if at least one of these public validation targets
is obtained:

- an official station-ID crosswalk between public OpenAQ rows and regulator
  station rows;
- station-specific calibration certificate, inspection log, operational-status
  record, or explicit grade classification;
- verified monthly or annual regulator report that names the target station
  and pollutant without a provisional-data warning;
- public source-owner confirmation that an OpenAQ provider is the official
  regulator or a documented co-location partner.

If none can be obtained from public sources, that negative result is still a
valid output: a public-evidence wall for station-grade air-monitoring claims.

## 9. Caveat box

The article needs a visible caveat box with four sentences:

1. OpenAQ visibility is not the same as official network completeness.
2. A station row is not a monitor-grade classification.
3. A radius denominator is not a service area or people-served estimate.
4. A satellite PM2.5 grid supports context, not station-level regulatory
   verification.

## 10. Policy use case

The immediate use is a monitoring-evidence request packet. A country team or
statistics partner can use the row-level ledger to ask the source agency for
specific missing documents: station ID crosswalk, current operating status,
calibration or inspection record, certificate or grade basis, and verified
report status.

This keeps the output actionable without overstating what the public evidence
currently proves.

## 11. Publication target

Best current format: **ADB/ERDI data note plus evidence page**.

Not yet ready as a working paper headline because the current evidence package
is mostly a closure and blocker audit. It can become a working-paper candidate
only after the program either validates a nontrivial set of station-grade rows
or reframes the negative result as the paper's contribution: public air-monitor
systems are visible in fragments, but coverage claims fail without station
identity and grade documentation.

## 12. Next loop question

Do not ask "can we find one more source?" first. Ask:

What exact public document would convert one blocked row into a station-radius
claim-eligible row, and is that document publicly available?

If the answer is no after the named source-access routes are checked, stop
source-mining that lane and publish the wall honestly.
