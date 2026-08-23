# H-CEDVAL003-CALIBRATION-ZERO-01

Status: **FROZEN — NOT EXECUTED**

Authority: PI decision, `PR-CED-VAL-003-SWING-3-4-001`, AD-039, AD-037,
AD-038, AD-040, SVP-001 and F-030.

## Frozen Scientific Question

When authoritative symbolic event timing is known for controlled dataset
`PR-CED-VAL-003-SWING-3-4-001`, what signed temporal difference is observed
through symbolic timing → controlled Sibelius rendering → physical audio
observation → JGA detection → immutable EME timestamp for Drums, Double Bass
and Piano, and what pairwise measurement behaviour applies to Piano–Drums and
Double Bass–Drums before unchanged H02 validation?

This characterizes combined rendering/measurement behaviour. It does not
isolate detector error, interpret performance, authorize correction or execute
H02. Execution requires separate PI approval and no criterion may be retuned
after result access.

## Frozen Input Authority

Execution fails closed unless it verifies exactly:

- dataset `CED-VAL-003-SWING-3-4`, DGR
  `DGR-CED-VAL-003-SWING-3-4-001`, and provenance revision
  `PR-CED-VAL-003-SWING-3-4-001` at commit `424bdfae4f4174f16d9ac78c4ecd3a0e5de22033`;
- manifest `validation/CED-VAL-003-SWING-3-4/input_authority_manifest.json`;
- dataset fingerprint
  `9345f5923055a7ed1c953eee4b8613f2b2262c55cd2e5f094d489d097c37f790`;
- actual external root `/Volumes/SSD Track/JGA/datasets/CED-VAL-003-SWING/`
  and audio directory `steams/`;
- PI-declared common origin `Sibelius Export from beginning`;
- stereo 24-bit PCM, 44,100 Hz, 2,150,400 frames/channel and WAV scope
  `[0, 1024/21)` seconds; and
- Drums WAV `steams/CED-VAL-003-SWING-3-4_drums.wav`, SHA-256
  `11bd51037126608d7052ae0bb2b01d77b86eccae46d60ca088d3d5f57cccc44d`;
- Double Bass WAV `steams/CED-VAL-003-SWING-3-4_bass.wav`, SHA-256
  `bd702128f0b6e9887ccfae104ee0af6b2b4307c2021bb826fd85fec669322429`;
- Piano WAV `steams/CED-VAL-003-SWING-3-4_piano.wav`, SHA-256
  `64b95f5c41bb2bc102c68ffb2fa9b0215a2397e749f671ba2891378533302065`;
- MusicXML `symbolic/CED-VAL-003-SWING-3-4.musicxml`, SHA-256
  `f74856b2766db824536bdbab0b3ab62dbcf8460c780272b88df13dec8620f4c2`;
- Sibelius `symbolic/CED-VAL-003-SWING-3-4.sib`, SHA-256
  `f5d67d5e612e820ee8213ed02bf0d3303056ae5101d08f7c6e881b8e4252c477`.

Before EME timestamp access, freeze the effective observation configuration,
512-sample hop owned by `PulseCandidateBuilder.FRAME_LENGTH_SAMPLES`, detector
revision, environment/dependencies, source identities, exact scope/origin,
execution identity and complete PulseCandidate/EME lineage. No numerical
calibration result transfers from CED-VAL-001 or CED-VAL-002.

## CalibrationSymbolicEvent Authority

Before any observed EME timestamp is loaded:

1. Parse only the checksum-bound MusicXML.
2. Preserve part, measure, voice, staff, note locator and exact rational onset.
3. Exclude rests and non-attacking tie continuations, preserving every item
   and reason.
4. Group attack-bearing notes at exactly equal rational onset within source,
   preserving sorted constituents.
5. Convert quarter positions using only declared symbolic Ground Truth:
   quarter = 140/minute = exactly `3/7` second. Declared 3/4 is provenance and
   is not needed by observational detection or H02.
6. Derive deterministic identities from dataset fingerprint, provenance
   revision, source, exact onset and constituent locators; order by onset then
   identity.
7. Freeze events, exclusions, schema, checksums and fingerprint.

Authority must reproduce exactly Drums 155, Double Bass 100 and Piano 57
events. Failure or ambiguity produces `INSUFFICIENT_EVENT_AUTHORITY` and stops
before comparison.

## Event Correspondence and Absolute Measurement

Correspondence is source-separated. For ordered distinct exact symbolic times,
construct capture cells over `[0, 1024/21)`: adjacent boundaries are exact
midpoints; the first cell begins at zero; the final cell ends at WAV scope;
ordinary cells are left-closed/right-open. An observed timestamp exactly on an
internal midpoint is `AMBIGUOUS_BOUNDARY` and belongs to neither valid cell.

Exactly one in-cell EME is `VALID`; zero is `UNMATCHED_SYMBOLIC`; more than one
is `AMBIGUOUS_MULTIPLE_OBSERVED` with all candidates preserved and none
selected. Every unconsumed, out-of-scope or boundary EME is
`UNMATCHED_OBSERVED` or `AMBIGUOUS_BOUNDARY`. Preserve a sensitivity marker for
valid cells adjacent to unmatched/ambiguous cells. No tolerance, forced
nearest match, sequence optimization, count forcing or rematching is allowed.

For every `VALID` record preserve identities, lineage, provenance and:

```text
t_GT
t_JGA
e_i              = t_JGA - t_GT
absolute_error_i = abs(e_i)
```

Report per source and overall symbolic/observed N, all correspondence statuses,
complete signed/absolute distributions, minimum, maximum, arithmetic mean,
median, population standard deviation and Q1/Q2/Q3 using linear empirical
quantile interpolation. Raw `t_JGA` is immutable.

## Symbolic Pair Authority and Pairwise Measurement

Freeze pair authority from `CalibrationSymbolicEvent` authority before loading
absolute correspondence results. For each Piano or Double Bass event, exactly
one Drum event at exactly equal rational `t_GT` gives `VALID_SYMBOLIC_PAIR`;
none gives `UNMATCHED_SYMBOLIC_PAIR`; multiple gives
`AMBIGUOUS_SYMBOLIC_PAIR`, preserving all and selecting none. Deterministic
pair identity binds the symbolic-authority fingerprint, pair type and event
identities. AD-038 geometry, tolerances and observed results cannot create pair
authority.

A pair becomes `VALID_JGA_PAIR` only when both members have one frozen absolute
`VALID` correspondence. Preserve:

```text
Delta_GT        = t_source_GT  - t_drum_GT
Delta_JGA       = t_source_JGA - t_drum_JGA
e_pair          = Delta_JGA - Delta_GT
absolute_e_pair = abs(e_pair)
```

Report Piano–Drums and Double Bass–Drums independently with complete statuses,
signed/absolute descriptive distributions, partitions, sensitivity and replay.

## Frame Characterization

Freeze `h = 512 / 44100` seconds. For every valid absolute and pair error,
choose integer `k` minimizing `abs(error - k*h)`; exact ties select smaller
absolute `k`, then lower signed `k`. Preserve `k`, signed residual
`error - k*h`, normalized residual and complete distributions. Frame spacing
is descriptive measurement structure—not accuracy, tolerance, bias,
correction or correspondence authority.

## Minimum Support, Partitions and Bootstrap

The authority-derived WAV midpoint is exactly `512/21` seconds. Partition 1 is
`[0, 512/21)` and partition 2 is `[512/21, 1024/21)`, assigned by exact
symbolic `t_GT`; the midpoint belongs to partition 2. These scopes have no
musical meaning.

Every source and pairwise bias decision requires at least 10 valid records
overall and at least 5 in each partition. Otherwise report
`INSUFFICIENT_EVIDENCE` and make no bias claim.

Transfer unchanged the deterministic bootstrap: 10,000 replacement resamples
of the applicable event/pair population; median signed error (or declared
source-median difference); percentile 95% interval with linear interpolation
at 0.025/0.975; seed from the first 16 hex digits of
`SHA256(frozen_input_manifest_sha256 + ":" + analysis_label)`; independent
pre-frozen labels for full, partition, sensitivity and source-difference
calculations.

## Frozen Classification Criteria

A source has candidate systematic bias only if: support passes; replay is
exact; full and both partition median bootstrap intervals exclude zero; all
three medians have one nonzero sign; each partition interval overlaps the full
interval; the conclusion survives exclusion of cells adjacent to
unmatched/ambiguous cells; and provenance is complete/conflict-free.

`SOURCE_SPECIFIC_CANDIDATE_BIAS` requires a qualifying source and at least one
qualifying-source median-difference interval excluding zero.
`SOURCE_INDEPENDENT_CANDIDATE_BIAS` requires at least two qualifying sources,
all qualifying-source median-difference intervals including zero, and pooled
qualifying-source median interval excluding zero. Sufficient evidence meeting
neither is `NO_DETECTABLE_SYSTEMATIC_BIAS`.

Measurement structure is described, without numerical thresholds, as
`QUANTIZATION_DOMINATED_MEASUREMENT`,
`RESIDUAL_OR_UNSTABLE_MEASUREMENT_VARIABILITY`,
`MIXED_MEASUREMENT_BEHAVIOUR`, or `INSUFFICIENT_EVIDENCE` according to the
complete signed, offset and residual evidence.

A pair is `CANDIDATE_PAIRWISE_BIAS` only if support/replay pass; full and both
partition median intervals exclude zero; all medians share one nonzero sign;
partition intervals overlap the full interval; sensitivity exclusion leaves
the conclusion unchanged; and authority/provenance are conflict-free.
`NO_DETECTABLE_PAIRWISE_BIAS` requires support, replay, full interval containing
zero, both partition intervals overlapping it and stable sensitivity.
Otherwise use `UNSTABLE_PAIRWISE_MEASUREMENT` or `INSUFFICIENT_EVIDENCE`.
Differing pair types may yield `MIXED_SOURCE_SPECIFIC_OUTCOME`.

No outcome authorizes correction. Zero is neither favored nor disfavored.

## Allowed Outcomes and Tail Treatment

Allowed absolute outcomes are `NO_DETECTABLE_SYSTEMATIC_BIAS`,
`SOURCE_INDEPENDENT_CANDIDATE_BIAS`, `SOURCE_SPECIFIC_CANDIDATE_BIAS`, and
`INSUFFICIENT_EVIDENCE`; measurement-structure and pairwise vocabularies are
those frozen above. Negative, mixed, unstable and insufficient results are
valid.

Symbolic scope is `[0, 306/7)` seconds, first onset zero and last onset `288/7`.
WAV scope is `[0, 1024/21)`, preserving the `106/21`-second rendered tail
beyond symbolic scope. It is not trimmed, shifted or itself called error. Tail
EME remain governed by final-cell/unmatched/ambiguity rules without suppression.

## Ground Truth, H02 and Immutability Firewalls

Ground Truth may construct symbolic and pair authority, establish calibration
correspondence under frozen rules and characterize measurement difference. It
may not create/move EME, tune detection, force/optimize correspondence, enter
observational detection, predict H02, manufacture timing authority or add
musical interpretation. Declared 3/4 and quarter = 140/minute are calibration
Ground Truth only.

H02 remains completely frozen and is neither executed nor inspected. This
protocol cannot alter mutual-nearest, signature, recurrence, boundary or tie
rules. H02 requires completed/frozen Calibration Zero, PI review and separate
explicit authorization. No H03 is created.

WAV, MusicXML, Sibelius, input manifest, EME, PulseCandidates, AD-038, AD-040
and prior validation artifacts remain immutable. Calibration is downstream;
no timestamp, displacement or production correction is modified or produced.

## Determinism, Reproducibility and Transfer Audit

Future execution must preserve dataset and asset checksums; input manifest;
symbolic and pair authority plus fingerprints; exact origin/scopes;
environment/configuration; complete event/pair results; two complete
executions; descriptive, partition, bootstrap, sensitivity and outcome
records; artifact checksum manifest; scientific fingerprint over canonical
scientific content excluding local paths/times; and completion protocol.

Both executions must reproduce identities, populations, statuses, exact
measurements, statistics, classifications and fingerprints. Any mismatch
prevents a passing record.

All established methodological criteria transfer without mathematical change.
Only dataset identity/assets, exact-rational `3/7`-second symbolic conversion,
populations, source set, scopes and scope-derived midpoint are replaced by
frozen CED-VAL-003 authority. These are authority bindings, not retuning. No
methodological criterion is non-transferable.

Production impact: **NONE**. No execution, dependency, detector/configuration
change, correction, tolerance, suppression, H02 access or musical
interpretation is authorized.
