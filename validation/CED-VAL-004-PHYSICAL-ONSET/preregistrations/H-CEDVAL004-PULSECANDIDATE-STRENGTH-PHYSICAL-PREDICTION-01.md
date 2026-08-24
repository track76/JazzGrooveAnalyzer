# H-CEDVAL004-PULSECANDIDATE-STRENGTH-PHYSICAL-PREDICTION-01

Status: **PREREGISTERED NEW PROSPECTIVE HYPOTHESIS — NOT EXECUTED**

Authority: PI authorization following read-only audit
`AUD-CEDVAL004-PREEXISTING-STRENGTH-AUTHORITY-01`, which concluded
`NOT_READY_FOR_PROSPECTIVE_VALIDATION`; dataset
`PR-CED-VAL-004-PHYSICAL-ONSET-001`; frozen physical-onset authority
`H-CEDVAL004-PHYSICAL-ONSET-MEASUREMENT-01`, scientific fingerprint
`7b2ec48f0ff0afca54849b5847f5ebd637c8d672eb2b88247ea6a1841af99062`;
and frozen physical-to-JGA comparison
`H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01`, scientific fingerprint
`cebccb70224dce4e519197e84178e11afdc1e98b8148914a7512ac6df06ef22e`.

## New-hypothesis status and scientific question

This is explicitly a **new prospective hypothesis**. It is not a validation,
transfer, continuation or reinterpretation of the identity-bound historical
CED-VAL-003 strength-max predictor. It is frozen before any CED-VAL-004
strength value is read, any CED-VAL-004 candidate is ranked, or frozen
physical-onset authority is opened for scoring.

Scientific question: within a marker-defined event domain containing more
than one eligible same-source Domain PulseCandidate, does the PulseCandidate
with greatest exact preserved strength predict the PulseCandidate temporally
closest to independently frozen `t_physical`?

## Frozen blind candidate population

The candidate object is the immutable Domain `PulseCandidate` produced by the
unchanged observation path. Its authoritative temporal coordinate must
round-trip uniquely to producer frame `f_candidate`, with
`n_candidate = 512 * f_candidate`; its identity, source, observation index,
asset, scope and provenance must be complete and deterministic.

Population construction transfers only the already-frozen source-separated
marker-midpoint cells from
`H-CEDVAL004-PHYSICAL-TO-JGA-COMPARISON-01`. For each scheduled event, include
every and only same-source Domain PulseCandidate whose producer-frame sample
coordinate lies inside that event's frozen cell. The first cell begins at
sample zero, the last ends at sample 8,820,000, internal boundaries are exact
rational midpoints of consecutive same-source markers, ordinary cells are
left-closed/right-open, and a candidate exactly on an internal boundary is an
authority conflict for that event and is not silently assigned. Unconsumed or
out-of-scope candidates remain preserved and cannot be added to an event.

Source, marker-cell geometry and immutable PulseCandidate authority are the
only population inputs. `t_physical`, EME correspondence status,
physical-to-JGA error, strength and confidence cannot include, exclude, move
or rematch a candidate.

Freeze each population as:

- `NONVACUOUS_CANDIDATE_POPULATION`: at least two eligible candidates;
- `SINGLETON_CANDIDATE_POPULATION`: exactly one eligible candidate;
- `NO_CANDIDATES`: zero eligible candidates; or
- `CANDIDATE_AUTHORITY_CONFLICT`: boundary, identity, frame, source,
  provenance or replay authority is inconsistent.

Singleton and empty populations produce no strength prediction and never
count as success. No candidate may be manufactured. Zero non-vacuous
populations overall, or zero in either preregistered source, yields
`INSUFFICIENT_NONVACUOUS_CANDIDATES`; no numerical minimum beyond the logical
requirement of at least one non-vacuous population per source is introduced.

## Frozen blind predictor

Only after complete population identities are frozen may execution read the
existing exact binary64 `PulseCandidate.strength`. For every
`NONVACUOUS_CANDIDATE_POPULATION`:

- a single candidate with strictly greatest exact strength becomes
  `PREDICTED_PULSECANDIDATE`;
- two or more candidates sharing the exact greatest strength produce
  `STRENGTH_TIED`, with no prediction; and
- absent strength or incomplete identity, lineage, provenance or replay
  authority produces `STRENGTH_UNRESOLVED`, with no prediction.

No normalization, rescaling, threshold, epsilon, tolerance, transformation,
confidence, timing combination, source weighting or cross-source strength
comparison is permitted. Exact binary64 values and hexadecimal
representations must be preserved.

## Frozen blind-first execution order

1. Verify all frozen authorities, assets, code and configuration.
2. Execute the unchanged JGA observation path.
3. Construct every marker-defined PulseCandidate population without reading
   strength, confidence, `t_physical` or physical-to-JGA results.
4. Freeze and fingerprint complete population identities and statuses.
5. Read exact strength only for authorized eligible candidates and apply the
   frozen maximum rule.
6. Freeze predictor identities, ties, unresolved cases and complete blind
   predictor fingerprint.
7. Perform deterministic blind replay and require exact agreement.
8. Only after the blind predictor freeze, open frozen `t_physical` authority.
9. Score without changing populations, predictions or rules.

## Independent physical outcome and scoring

For each non-vacuous population with a unique strength prediction, calculate
for every eligible candidate only after blind freeze:

```text
d(c) = abs(n_candidate - n_physical)
```

The candidate with the unique minimum exact integer-sample distance is the
independently authorized `PHYSICAL_NEAREST_PULSECANDIDATE`. This is scoring
authority only; it cannot influence population construction or prediction.
If two or more eligible candidates share the minimum exact distance, classify
`PHYSICAL_OUTCOME_TIED`; the event is unscorable. Strength, confidence,
temporal direction, EME identity and musical plausibility cannot break the
tie.

For every independently scorable non-vacuous population:

- `STRENGTH_MAX_CORRECT` when the frozen predicted PulseCandidate identity is
  the unique physical-nearest identity; or
- `STRENGTH_MAX_INCORRECT` otherwise.

`STRENGTH_TIED`, `STRENGTH_UNRESOLVED`, `PHYSICAL_OUTCOME_TIED` and authority
conflicts are unscorable and remain individually preserved. Every record must
preserve population/event identity, source, all candidate identities and
producer frames, exact strengths, frozen predictor identity, physical-onset
identity and sample, every exact physical distance, physical-nearest identity,
status and provenance.

## Reporting, metric and frozen outcomes

Report Drums and Double Bass independently before secondary overall results:
total event cells, non-vacuous, singleton, empty, authority-conflict,
strength-tied, strength-unresolved, physical-outcome-tied, scorable, correct
and incorrect counts. Primary descriptive metric among scorable non-vacuous
populations is exact accuracy:

```text
STRENGTH_MAX_CORRECT /
(STRENGTH_MAX_CORRECT + STRENGTH_MAX_INCORRECT)
```

No precision, recall, inferential significance test or numerical success
threshold is authorized. Apply outcomes in this exact precedence:

1. `INSUFFICIENT_NONVACUOUS_CANDIDATES` if either source has zero non-vacuous
   populations.
2. `INSUFFICIENT_SCORABLE_EVIDENCE` if either source with non-vacuous
   populations has zero scorable predictions.
3. `SUPPORTS_STRENGTH_AS_PHYSICAL_CANDIDATE_PREDICTOR` only if every
   non-vacuous population is scorable and every scorable prediction is
   correct in both sources.
4. `DOES_NOT_SUPPORT_STRENGTH_AS_PHYSICAL_CANDIDATE_PREDICTOR` only if both
   sources have scorable evidence and no scorable prediction is correct.
5. `PARTIAL_SOURCE_SPECIFIC_SUPPORT` for every other mixture of correct,
   incorrect or incompletely scorable source-specific evidence.

These are logical classifications, not performance thresholds. Exact
source-specific counts and accuracies remain primary evidence.

## Resolution, replay and firewalls

PulseCandidate timing remains a 512-sample frame-lattice coordinate with
spacing `512/44100` seconds, not sample-level detector precision. Physical
onset remains sample-addressable. Nearest-outcome scoring uses these exact
authorized coordinates without tolerance or correction.

Perform at least two complete executions. Require exact reproduction of
observation and candidate identities, frames, populations, statuses, binary64
strengths, predictor identities, blind fingerprint, physical-authority joins,
distances, scoring statuses, counts, accuracies and scientific fingerprint.

JGA detection, thresholds, windows, frame geometry, PulseCandidate/EME
generation and source handling cannot be tuned. PulseCandidates, EME,
`t_physical`, physical-to-JGA results and all historical evidence remain
immutable. This study cannot modify or rescore CED-VAL-003, H02 is unchanged,
no H03 is created, no production integration is authorized and
`GEOMETRIC_ONLY` remains authoritative. Architecture and production impact at
preregistration are none; production code is unchanged.
