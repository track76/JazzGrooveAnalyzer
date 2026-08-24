# H-CEDVAL006-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY-01

Status: **PREREGISTERED — NOT EXECUTED**

## Frozen authorities and scientific question

This protocol is bound exclusively to:

- JGA execution `EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919`, scientific
  fingerprint
  `8c5723fbeabe2031516b2eeee0c83fb42ad84f46824cf65f5d485c6cf6c82b5c`,
  and its frozen `elementary_metric_events.json`, SHA-256
  `64db95d8feeb6ab7ca22aa8081e177c57d6ab57c9f0aaf3bb4a5650db28329f5`;
- exactly 909 frozen Drums EME from that execution; Double Bass EME are
  excluded; and
- external execution
  `EXEC-CEDVAL006-EXTERNAL-BEAT-BENCHMARK-20260824-191341`, combined
  fingerprint
  `d3e5ea9c6bea7bd0a9c81cb6044fa469dc1f33bc2f70788cd4a027f30491ee6a`;
  its 527 frozen Essentia ticks from `essentia_output.json`, SHA-256
  `3f3ff0e855b646c29ee56e775c3d2a20a0cf37468242137e3406dc9203cb9b45`,
  scientific fingerprint
  `1e52e479e9be6bb80f7b36a781031ab343523c4e6d7d248eecfaf4cb9bd284dd`;
  and its 466 frozen librosa beats from `librosa_output.json`, SHA-256
  `8ff07eb46d7f8c734d64c37874e595d1c4172cab1a9d66d03b930bf3cec6dea0`,
  scientific fingerprint
  `780f9691dd13bb7bf30858ff8a7d76628958f42b8e56430798554981ef65b318`.

No population may be recomputed, filtered, augmented or altered.

Scientific question: on the common elapsed-time coordinate originating at
distributed-file sample zero, what is the neutral temporal geometry between
(A) each frozen Essentia beat position and the frozen JGA Drums EME, and (B)
each frozen librosa beat position and the frozen JGA Drums EME?

This is descriptive geometry, not beat validation.

## Coordinate authority

All comparisons use exact elapsed seconds from the common distributed-file
sample-zero origin of the frozen CED-VAL-006 Drum input.

- For each JGA Drums EME, preserve immutable `producer_frame` and require
  `producer_sample_coordinate = 512 * producer_frame`. Its exact comparison
  coordinate is the rational number `producer_sample_coordinate / 48,000`.
  Its frozen binary64 timestamp must equal the correctly rounded
  representation of that rational and round-trip to its frozen hexadecimal
  representation.
- For each librosa beat, preserve its frozen native integer frame and require
  `beat_sample = 512 * beat_frame`. Its exact comparison coordinate is
  `beat_sample / 48,000`; its frozen decimal and binary64 hexadecimal value
  must round-trip exactly.
- For each Essentia tick, preserve the frozen binary64 seconds and hexadecimal
  value. For exact comparison, interpret that binary64 value through its exact
  `as_integer_ratio()` rational. Do not quantize it onto the JGA lattice and do
  not infer an authoritative original-file sample coordinate.

No coordinate may be rounded, interpolated, shifted, corrected, resampled or
aligned before comparison. Every rational signed and absolute result shall be
preserved as numerator and denominator; derived binary64 seconds and
milliseconds values may also be reported with binary64 hexadecimal values.

## Methodological dependency caveat

The frozen librosa `beat_track` pipeline and the JGA observation frontend are
not fully algorithmically independent. The frozen librosa beat scope begins at
26.528 seconds, equal to the first frozen JGA Drums EME time. This equality is
a frozen methodological observation only: it shall not change a rule, establish
agreement, establish correctness or receive musical interpretation.

Essentia is the more algorithmically independent comparator. That distinction
is a dependency limitation, not a basis for preference, weighting, pooling or
different geometry. Both tracker populations receive the identical rules below.

## Frozen nearest geometry

Apply the following independently to every external beat of each tracker
against the complete 909-EME Drums population. Sort Drum observations by exact
time, then stable EME identity; retain distinct equal-time EME identities.

For external beat time `b` and each Drum EME time `d`:

- signed displacement is `d - b`;
- absolute displacement is `abs(d - b)`;
- preceding time is the maximum Drum time satisfying `d <= b`, when present;
- following time is the minimum Drum time satisfying `d > b`, when present;
  and
- nearest distance is the minimum exact absolute displacement over all Drum
  EME.

Preserve every EME identity at the preceding time, every identity at the
following time and every identity attaining the nearest distance. Do not
enforce one-to-one matching; one Drum EME may be nearest to multiple external
beats.

Nearest status is `UNIQUE_NEAREST` when the nearest identity set contains one
EME and `EQUAL_DISTANCE_TIE` when it contains more than one, including
equal-time duplicate identities and equal-distance observations on opposite
sides.

The required scalar displacement populations use one deterministic
serialization representative without changing the preserved nearest set:
order nearest identities by (1) preceding-or-equal before following, (2) exact
Drum time ascending and (3) stable EME identity ascending; serialize the first.
This is record stability only, not preferred correspondence. Preserve every
tied identity and its signed value. Absolute distance is identical across the
nearest set.

Boundary status is:

- `BEFORE_FIRST_JGA_OBSERVATION` when `b` precedes the earliest Drum time;
- `AFTER_LAST_JGA_OBSERVATION` when `b` follows the latest Drum time; or
- `INTERIOR_OR_ENDPOINT` otherwise.

Before-first cases have no predecessor; after-last cases have no follower. The
available side remains eligible as nearest. A beat exactly at an endpoint is
not outside. `UNRESOLVED` is permitted only if the frozen Drum population is
absent, malformed or fails coordinate authority; such a condition stops the
study with `EVIDENCE_CONFLICT` rather than forcing geometry.

The complete frozen populations remain primary. Essentia shall not be trimmed
to the librosa or JGA scope, librosa shall not be trimmed, and no beginning or
ending beat shall be discarded. Boundary cases remain evidence. No secondary
common-overlap statistics are preregistered: boundary-status counts already
describe scope effects without creating another analysis population.

## Outputs and descriptive statistics

For Essentia and librosa separately preserve:

- external beat count, localized count and unresolved count;
- predecessor, follower and nearest availability counts;
- tie and boundary-status counts;
- complete case-level external identities and coordinates, complete
  predecessor, follower and nearest identity sets, serialization
  representative, rational signed displacement and rational absolute
  displacement;
- complete ordered scalar signed-displacement and absolute-displacement
  populations; and
- provenance and deterministic scientific fingerprints.

For signed and absolute scalar populations report minimum, linear-interpolated
Q1, median, Q3, maximum, arithmetic mean and population standard deviation.
Quantiles use index `(n - 1) * p` for `p = 0.25, 0.50, 0.75`; population SD
divides by `n`. Statistics are computed from exact rational values where
algebraically supported, with binary64 descriptive renderings preserved. No
tolerance, threshold or exclusion is permitted.

## Frame-lattice descriptive counts

Let `F = 512 / 48,000` seconds exactly, approximately
10.6666666666667 milliseconds. Using each beat's exact nearest absolute
distance, report these cumulative descriptive quantities separately per
tracker:

- `exact_zero_count`: distance `= 0`;
- `within_one_jga_frame_count`: distance `<= F`, including exact zero;
- `within_two_jga_frames_count`: distance `<= 2F`, including the one-frame
  population; and
- `beyond_two_jga_frames_count`: distance `> 2F`.

Also preserve the disjoint audit partition `=0`, `(0,F]`, `(F,2F]` and `>2F`
so arithmetic cardinality can be verified. These are descriptive geometry
bins, not accuracy thresholds, correctness criteria, matching tolerances or
calibration windows. Essentia timestamps remain off-lattice when frozen that
way.

## Separate analyses and future five-window projection

Essentia-to-JGA and librosa-to-JGA results remain separate. No
Essentia-to-librosa matching, comparison, agreement, preference, pooling or
ranking is permitted.

A later separately authorized visualization may project the three frozen
observational layers onto the existing source-sample-coordinate windows:

1. `W1 [1071286, 1311286)`
2. `W2 [3453860, 3693860)`
3. `W3 [5836434, 6076434)`
4. `W4 [8219007, 8459007)`
5. `W5 [10601581, 10841581)`

JGA and librosa membership uses each frozen exact integer sample coordinate.
Essentia membership uses exact rational comparison of its frozen binary64
seconds against `start_sample/48,000 <= tick < end_sample/48,000`; this does
not create an Essentia original-file sample coordinate. No overlay is rendered
by this preregistration.

Any future figure must use separate or unambiguously distinguished layers and
state:

- `OBSERVATIONAL / DESCRIPTIVE TEMPORAL GEOMETRY`;
- `JGA: FRAME-RESOLVED OBSERVATION`; and
- `ESSENTIA / LIBROSA: CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`.

No beat correctness, correspondence, synchronization, groove,
rushing/dragging, performance-quality or physical-onset language is permitted.

## Replay, success and firewalls

Future execution is a pure derivation from the checksum-bound frozen JSON
artifacts. Perform two complete independent executions and require exact
agreement of authorities, case identities, predecessor/follower/nearest sets,
serialization representatives, rational and binary displacement values, ties,
boundaries, statistics, frame-bin counts and scientific fingerprints. Any
material disagreement is `DETERMINISTIC_REPLAY_FAILURE` and stops the study.

`PASS` means only that each frozen external population can be compared
deterministically with frozen JGA Drums observations on the common elapsed-time
coordinate. It does not mean either tracker is musically correct.

External beats remain `CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`; JGA Drums EME
remain `FRAME-RESOLVED OBSERVATION`. Neither is Ground Truth. Every resulting
relation remains `DESCRIPTIVE TEMPORAL GEOMETRY ONLY`: geometry is not
correspondence, a shared event, detector accuracy, synchronization, physical
onset or performance timing.

Tracker-reported BPM values and any supplied or inferred BPM are forbidden
comparison inputs. No BPM reasoning, meter, measure, downbeat, beat number,
symbolic information, H02, strength, human validation or musical
interpretation is permitted.

JGA, Essentia and librosa are not rerun. JGA Core, production code, raw assets,
frozen populations and historical authorities remain unchanged. No tracker is
preferred and no future integration is authorized.
