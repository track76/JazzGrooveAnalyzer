# H-CEDVAL002-CALIBRATION-ZERO-01

Status: **FROZEN — NOT EXECUTED**

Authority: PI decision, corrected authority `PR-CED-VAL-002-SWING-002`,
AD-039, AD-037, AD-038, AD-040, SVP-001 and F-030.

## Frozen Scientific Question

When authoritative symbolic event timing is known for corrected controlled
dataset `PR-CED-VAL-002-SWING-002`, what signed temporal difference is
observed through:

```text
symbolic timing
→ controlled Sibelius rendering
→ physical audio observation
→ JGA detection
→ immutable EME timestamp
```

for Drums, Double Bass and Piano, and what pairwise measurement behaviour
applies to Piano–Drums and Double Bass–Drums before unchanged H02 out-of-sample
validation?

This experiment characterizes combined rendering/measurement behaviour. It
does not isolate detector error, interpret performance, authorize correction
or execute H02.

## Execution and Historical State

This protocol is frozen before event-level symbolic/JGA comparison,
measurement-error calculation, pairwise-error calculation or H02 access. It
shall not execute without separate PI approval and shall not be retuned after
result access.

The following history is immutable:

```text
CED-VAL-002-SWING initial authority at 64c8c93
→ PI identified a source-duration issue
→ PI corrected the Sibelius/symbolic source
→ pre-correction authority retained as SUPERSEDED_PRE_CORRECTION_AUTHORITY
→ PR-CED-VAL-002-SWING-002 frozen at f966d6e
→ this Calibration Zero preregistration
```

Only corrected provenance revision `PR-CED-VAL-002-SWING-002` may execute this
protocol. The prior authority remains historical evidence and is not an input.

## Frozen Input Authority

Execution fails closed unless it verifies exactly:

- dataset ID `CED-VAL-002-SWING`;
- Dataset Generation Record `DGR-CED-VAL-002-SWING-002`;
- Provenance Revision `PR-CED-VAL-002-SWING-002`;
- corrected-authority commit
  `f966d6e8c98e0b330a9b5ab7b0d3f8f541499727`;
- corrected manifest
  `validation/CED-VAL-002-SWING/input_authority_manifest_v2_corrected.json`;
- dataset fingerprint
  `631eaf017cfaf335ee2945bfbe0df19221a0a0d069fee3602880eda7a851ade1`;
- external dataset root
  `/Volumes/SSD Track/JGA/datasets/CED-VAL-002-SWING/` and exact discovered
  audio directory `steams/`;
- PI-declared common origin `Sibelius Export from beginning`;
- stereo 24-bit PCM, 44,100 Hz and exactly 2,478,080 frames per channel;
- exact audio scope `[0, 123904/2205)` seconds; and
- the following assets:

| Authority | Exact path below dataset root | SHA-256 |
|---|---|---|
| Drums WAV | `steams/CED-VAL-002-swing_drums.wav` | `f3f75d95b05e7710dce5c35b68a7c54f2241a3d24177fc92f723b2ddeccbfbbb` |
| Double Bass WAV | `steams/CED-VAL-002-swing_bass.wav` | `dc71100c99526bbb6c1d4a6626cacae55db3d434a8cfc1216dfeda15a65549d4` |
| Piano WAV | `steams/CED-VAL-002-swing_piano.wav` | `4d2b03e7740d7487c365b2049959dd5cdc4f3b623fa9a4497bc698201c9bd75a` |
| corrected MusicXML | `symbolic/CED-VAL-002-swing.musicxml` | `0ae6ed241699b65f2e6d120c08f18e132781109f5f3d35335a9efe094e2ceb39` |
| corrected Sibelius | `symbolic/CED-VAL-002-swing.sib` | `d03ddd65eb02f3dae1ea775df0a43b599610fb201d3c1abc976d149b25cbf132` |

Before EME timestamp access, freeze the effective observation configuration,
512-sample hop owned by `PulseCandidateBuilder.FRAME_LENGTH_SAMPLES`, detector
implementation/source revision, environment and dependency versions,
contributor/SoundSource identities, numeric scope/origin, asset identities,
execution identity and complete PulseCandidate/EME lineage.

No numerical bias, correction, source error, pairwise error, frame-offset or
residual distribution, or uncertainty estimate transfers from CED-VAL-001.
Its scientific definitions and logically dataset-independent frozen methods
are prior methodological authority only.

## CalibrationSymbolicEvent Authority Construction

Before any observed EME timestamp is loaded for correspondence, construct and
freeze corrected calibration-only symbolic authority:

1. Parse only the checksum-bound corrected MusicXML.
2. Preserve part, measure, voice, staff, note locator and exact rational onset
   from score origin.
3. Exclude rests and tied continuations that do not initiate a new attack;
   preserve every exclusion and reason.
4. Within each source, group attack-bearing notes with exactly equal rational
   onset into one `CalibrationSymbolicEvent`, preserving sorted constituents.
5. Convert exact quarter positions to absolute controlled time using only the
   MusicXML declaration quarter = 150/minute, hence exactly `2/5` second per
   quarter. This is symbolic Ground Truth conversion, not JGA inference.
6. Assign deterministic identity from dataset fingerprint, corrected
   provenance revision, source identity, exact onset and sorted constituent
   locators.
7. Order by exact onset then identity and freeze events, exclusions, schema,
   checksums and scientific fingerprint.

The construction must reproduce exactly 192 Drum, 127 Double Bass and 64
Piano symbolic events. Failure, ambiguity or any undocumented assumption gives
`INSUFFICIENT_EVENT_AUTHORITY` and stops before error calculation.

## Frozen Absolute Event-Correspondence Rule

Correspondence is source-separated. For ordered distinct exact symbolic times
`g_0 ... g_(n-1)`, construct deterministic capture cells over the exact WAV
scope `[0, 123904/2205)`:

- adjacent boundaries are exact arithmetic midpoints;
- the first cell begins at exact scope start;
- the final cell ends at exact WAV scope end;
- ordinary cells are left-closed and right-open; and
- an observed timestamp exactly equal to an internal midpoint is
  `AMBIGUOUS_BOUNDARY` and belongs to neither valid cell.

For each symbolic cell:

- exactly one in-cell EME: `VALID`;
- zero: `UNMATCHED_SYMBOLIC`;
- more than one: `AMBIGUOUS_MULTIPLE_OBSERVED`, preserving every candidate and
  selecting none.

Every EME outside scope, on a boundary or not consumed by a valid cell remains
`UNMATCHED_OBSERVED` or `AMBIGUOUS_BOUNDARY` with complete lineage. No
millisecond tolerance, nearest optimization, count forcing, sequence alignment
or post-result rematching is permitted. Preserve a sensitivity marker for
valid cells immediately adjacent to any unmatched or ambiguous cell; primary
evidence is never deleted.

## Absolute Measurement

For every `VALID` correspondence preserve exact identities, provenance and:

```text
t_GT
t_JGA
e_i              = t_JGA - t_GT
absolute_error_i = abs(e_i)
```

Preserve exact/rational seconds where possible plus millisecond projections.
`t_JGA` is immutable. Error means empirical combined rendering/measurement
difference, not detector error or human timing.

Report per source and overall: symbolic N, observed EME N, valid,
unmatched-symbolic, unmatched-observed, ambiguous-multiple, ambiguous-boundary,
complete signed/absolute distributions, min, max, arithmetic mean, median,
population standard deviation and Q1/Q2/Q3 using linear empirical quantile
interpolation. No observation is suppressed.

## Frozen Symbolic Pair Authority and Pairwise Quantities

Construct pair authority solely from frozen `CalibrationSymbolicEvent`
authority before absolute correspondence results are loaded:

1. For each Piano or Double Bass symbolic event, compare exact rational
   `t_GT` with every Drum symbolic event.
2. Exactly one Drum event at equal `t_GT`: `VALID_SYMBOLIC_PAIR`.
3. None: `UNMATCHED_SYMBOLIC_PAIR`.
4. More than one: `AMBIGUOUS_SYMBOLIC_PAIR`, preserve all and select none.
5. Assign deterministic pair ID from symbolic-authority fingerprint, pair
   type and exact symbolic identities; freeze all records and fingerprint.

No AD-038 nearest relation, tolerance or observed result creates pair
authority. A symbolic pair becomes `VALID_JGA_PAIR` only when both members have
exactly one frozen absolute `VALID` correspondence.

For every `VALID_JGA_PAIR` preserve:

```text
Delta_GT       = t_source_GT  - t_drum_GT
Delta_JGA      = t_source_JGA - t_drum_JGA
e_pair         = Delta_JGA - Delta_GT
absolute_e_pair = abs(e_pair)
```

Report Piano–Drums and Double Bass–Drums independently: symbolic/valid pair N,
unmatched/ambiguous evidence, full signed/absolute distributions, min, max,
mean, median, population standard deviation, linear Q1/Q2/Q3, fixed temporal
partitions, sensitivity and deterministic replay.

## Frame-Resolution Characterization

Freeze nominal spacing:

```text
h = 512 / 44100 seconds
```

For every valid `e_i` and `e_pair`, choose integer `k` minimizing
`abs(error - k*h)`. An exact tie selects smaller absolute `k`, then lower
signed `k`. Preserve `k`, residual `error - k*h`, normalized residual and
complete empirical distributions per source/pair and overall.

Frame structure is descriptive only. It is not accuracy, error, tolerance,
bias, correspondence authority or correction. Describe whether errors
concentrate on frame multiples, occur around them with dispersion, exhibit
stable signed displacement, or show no visible frame-related structure.

## Frozen Temporal Partitions and Minimum Support

The exact WAV scope midpoint is:

```text
61952 / 2205 seconds
```

Partition 1 is `[0, 61952/2205)` and partition 2 is
`[61952/2205, 123904/2205)`. Assignment uses exact symbolic `t_GT`; the
midpoint belongs to partition 2. Partitions are fixed descriptive/calibration
scopes and have no musical meaning.

Every source candidate-bias decision and pairwise-bias decision requires at
least 10 valid records overall and at least 5 in each fixed partition.
Insufficient support produces no bias claim and the applicable
`INSUFFICIENT_EVIDENCE` outcome.

## Frozen Bootstrap

Transfer unchanged the authorized deterministic nonparametric procedure:

- 10,000 resamples with replacement of the applicable event/pair population;
- statistic: median signed error or difference of source medians as declared;
- percentile 95% interval using linear quantile interpolation at 0.025/0.975;
- seed: first 16 hexadecimal digits of
  `SHA256(frozen_input_manifest_sha256 + ":" + analysis_label)` interpreted as
  an integer; and
- independent labels for every full source/pair, partition, sensitivity and
  source-median-difference calculation.

Configuration, seed and labels freeze before error access. No bootstrap result
authorizes correction or causal decomposition.

## Frozen Absolute Systematic-Bias Criteria

A source has candidate systematic bias only when all conditions hold:

1. minimum support above;
2. exact replay of authority, status and quantities;
3. full and both partition 95% bootstrap median intervals exclude zero;
4. full and partition median signed errors share one nonzero sign;
5. each partition interval overlaps the full-source interval;
6. the same conclusion holds after excluding valid cells immediately adjacent
   to unmatched/ambiguous cells; and
7. identity, authority, provenance and execution are complete and conflict
   free.

`SOURCE_SPECIFIC_CANDIDATE_BIAS` requires at least one qualifying source and at
least one qualifying-source median-difference interval excluding zero.
`SOURCE_INDEPENDENT_CANDIDATE_BIAS` requires at least two qualifying sources,
every qualifying-source median-difference interval to include zero, and the
pooled qualifying-source median interval to exclude zero. If support/authority
is sufficient but neither applies, report `NO_DETECTABLE_SYSTEMATIC_BIAS`.

Measurement-structure outcomes transfer unchanged and are determined from the
complete signed, frame-offset and residual distributions:

- `QUANTIZATION_DOMINATED_MEASUREMENT` when frame-multiple concentration alone
  adequately describes the preserved distribution;
- `RESIDUAL_OR_UNSTABLE_MEASUREMENT_VARIABILITY` when stable systematic/frame
  structure is not demonstrated and residual variability remains;
- `MIXED_MEASUREMENT_BEHAVIOUR` when multiple descriptive structures remain
  and no single description is adequate; or
- `INSUFFICIENT_EVIDENCE` when mandatory authority/support is absent.

This retains the previously authorized descriptive—not numerical-threshold—
measurement-structure criterion and creates no correction.

## Frozen Pairwise Bias and Stability Criteria

A pair type is `CANDIDATE_PAIRWISE_BIAS` only when all hold:

1. pairwise minimum support above;
2. exact deterministic replay;
3. full and both partition median `e_pair` 95% intervals exclude zero;
4. all three medians are nonzero with one sign;
5. each partition interval overlaps the full interval;
6. the conclusion is unchanged after excluding pairs adjacent to any
   unmatched/ambiguous absolute cell; and
7. correspondence/provenance is stable and conflict free.

`NO_DETECTABLE_PAIRWISE_BIAS` requires sufficient support/provenance, replay,
a full interval containing zero, both partition intervals overlapping the full
interval and unchanged sensitivity conclusion. Sufficient support satisfying
neither rule is `UNSTABLE_PAIRWISE_MEASUREMENT`; absent mandatory authority or
support is `INSUFFICIENT_EVIDENCE`. The overall pairwise result may be
`MIXED_SOURCE_SPECIFIC_OUTCOME`. Zero is neither favored nor disfavored.

## Allowed Outcomes

Absolute bias-evidence vocabulary:

- `NO_DETECTABLE_SYSTEMATIC_BIAS`;
- `SOURCE_INDEPENDENT_CANDIDATE_BIAS`;
- `SOURCE_SPECIFIC_CANDIDATE_BIAS`; or
- `INSUFFICIENT_EVIDENCE`.

Measurement-structure vocabulary:

- `QUANTIZATION_DOMINATED_MEASUREMENT`;
- `RESIDUAL_OR_UNSTABLE_MEASUREMENT_VARIABILITY`;
- `MIXED_MEASUREMENT_BEHAVIOUR`; or
- `INSUFFICIENT_EVIDENCE`.

Per-pair vocabulary:

- `NO_DETECTABLE_PAIRWISE_BIAS`;
- `CANDIDATE_PAIRWISE_BIAS`;
- `UNSTABLE_PAIRWISE_MEASUREMENT`; or
- `INSUFFICIENT_EVIDENCE`.

An overall `MIXED_SOURCE_SPECIFIC_OUTCOME` may describe differing pair types.
Negative, mixed, unstable and insufficient outcomes are valid results. No
outcome authorizes correction or H02 execution.

## Symbolic/WAV Tail Treatment

The symbolic scope is exactly `[0, 256/5]` seconds, with final onset at 48
seconds. Equal WAV scope ends at `123904/2205` seconds and preserves an
untrimmed `11008/2205`-second tail beyond symbolic scope.

The tail is part of physical audio observation and declared analysis scope. It
is not trimmed, shifted or itself classified as error. Calibration compares
authorized symbolic events with observations under the frozen cells; it does
not require score-duration/WAV-duration equality. Tail EME remain subject to
the frozen final-cell/unmatched/ambiguity rules without suppression.

## Ground Truth, H02 and Raw-Immutability Firewalls

Ground Truth may construct frozen `CalibrationSymbolicEvent` and symbolic-pair
authority, establish correspondence under the frozen rules and characterize
measurement difference. It may not create/move EME, tune detection, force or
optimize correspondence, alter role assignment, predict H02 candidates,
manufacture tempo/meter or introduce musical interpretation.

H02 remains frozen exactly as validated. This experiment does not execute or
inspect it and cannot change mutual-nearest, signature, recurrence, boundary or
tie rules. Future H02 execution requires this Calibration Zero execution,
frozen result, PI review and explicit separate authorization.

WAV, MusicXML, Sibelius, corrected manifest, EME, PulseCandidates, AD-038,
AD-040 and all existing validation artifacts are immutable. Calibration
evidence is downstream and separate. No timestamp, displacement or correction
value is modified or produced for production.

## Determinism and Reproducibility

Preserve a checksum-bound input manifest; dataset fingerprint and every asset
checksum; symbolic and pair authority with fingerprints; declared origin and
exact scopes; effective environment/configuration; complete event/pair-level
evidence; two complete executions; descriptive, partition, bootstrap,
sensitivity and outcome records; artifact SHA-256 manifest; scientific
fingerprint over canonical scientific content excluding local paths/times; and
a completion protocol.

Both executions must reproduce symbolic and pair identities, EME identities,
statuses, exact quantities, statistics, outcomes and scientific fingerprints.
Any mismatch prevents a passing calibration record.

## Transfer Audit and Production Exclusion

All CED-VAL-001 methodological criteria above transfer without mathematical
change. Dataset-specific bindings, source population, exact scope/midpoint and
source/pair set are necessarily replaced by corrected CED-VAL-002 authority.
Tenor Sax criteria are not applicable because no Tenor Sax source exists.
These are authority substitutions, not methodological retuning.

No methodological criterion is non-transferable. No production code,
dependency, detector/configuration change, correction, tolerance, event
suppression, H02 execution or musical interpretation is authorized.
