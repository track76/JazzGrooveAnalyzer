# H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01

Status: **FROZEN — NOT YET EXECUTED**

Authority: PI approval of
`EG-CEDVAL003-AMBIGUOUS-PHYSICAL-AUTHORITY-01` at commit `a022570`;
`AUD-CEDVAL003-H02-SCORABILITY-01`; `PR-CED-VAL-003-SWING-3-4-001`;
AD-037/038/039/040.

## Frozen scientific question

For each of the 112 observations in the frozen CED-VAL-003
`AMBIGUOUS_MULTIPLE_OBSERVED` cells, can its lineage-bound existing
`PulseCandidate.strength` value be recovered from the checksum-bound WAV and
frozen observation configuration, joined exactly to its existing identity,
and reproduced exactly as a provenance-complete within-source physical
measurement?

This study establishes measurement authority only. It cannot establish
discrimination authority, select or rank an observation, score correspondence,
or authorize production use.

## Frozen population and inputs

The input population is frozen before strength recovery in
`frozen_ambiguous_population.json`, derived mechanically from Calibration Zero
event authority SHA-256 `3c2d2230…` and containing no symbolic timestamp,
symbolic proximity, TP/FP/FN or H02 outcome. Expected population:

- Drums: 54 cells / 108 observations;
- Double Bass: 2 cells / 4 observations;
- Piano: 0 cells / 0 observations;
- overall: 56 cells / 112 observations, exactly two observations per cell.

Execution must fail closed on any mismatch in the population manifest,
accepted dataset fingerprint `9345f592…`, asset checksums, evidence-gap SHA-256
`77885fcd…`, audit-result SHA-256 `5da81ca5…`, or these observation-code
checksums:

- `PulseCandidateBuilder`: `788c13ac…`;
- `PulseCandidateFilter`: `a0982865…`;
- `SourcePulseCandidateBuilder`: `5b270f35…`;
- `DomainPulseCandidateAdapter`: `6a3d276b…`;
- `ElementaryMetricEventBuilder`: `137e390a…`;
- `AnalysisPipeline`: `04ecdfee…`.

## Frozen recovery and exact join

Run the existing `AnalysisPipeline` independently on the checksum-bound Drum
and Double Bass WAVs with no declared metric reference, meter or symbolic
input. Execute the complete recovery twice.

For every frozen observation, require exactly one reproduced EME with the same
EME ID and exactly one supporting Domain PulseCandidate with the same frozen
PulseCandidate ID. Require exact agreement of timestamp float/hex,
sound-source/contributor identity, asset SHA-256, temporal scope,
materialization rule and one-to-one lineage. Preserve the Domain
PulseCandidate `observation_index`; derive the observation frame only by exact
consistency with the configured 512/44100 frame authority and fail if the
timestamp is not frame-consistent. No approximate identity or timestamp join
is permitted.

Preserve strength and confidence as their Python binary64 hexadecimal form and
round-trip JSON number. Do not normalize, rescale, threshold, rank or compare
strength across observations or sources.

## Replay, summaries and success criterion

The two executions must have identical EME/PulseCandidate identities,
timestamps, frames, observation indices, raw binary64 strength/confidence
values, source assignments, population membership and canonical scientific
fingerprint. Any mismatch is `INSUFFICIENT_MEASUREMENT_AUTHORITY`.

Report Drums and Double Bass independently using N, minimum, maximum, mean,
median, population standard deviation and Q1/Q2/Q3. Quartiles use NumPy linear
quantiles at 0.25/0.50/0.75. Statistics are descriptive only and do not imply
preference. Piano reports N=0/not applicable.

`PASS` means only that strength is frozen as a deterministic,
provenance-bound, within-source physical measurement for all 112 observations.
It does not authorize within-cell discrimination, cross-source comparability,
correspondence resolution, H02 rescoring or production use.

## Firewalls

Execution may access only the stripped frozen population manifest, immutable
WAV assets and observation code. It must not open symbolic authority, symbolic
correspondence, H02 scoring or TP/FP/FN artifacts. It must not compute strength
order, extrema by cell, ranks, thresholds or candidate preference.

Historical candidates remain unscorable. H02, H03, Calibration Zero, raw EME,
PulseCandidates, AD-037/038/039/040 and production code remain unchanged.
Architecture and production impact are none; `GEOMETRIC_ONLY` remains
authoritative.
