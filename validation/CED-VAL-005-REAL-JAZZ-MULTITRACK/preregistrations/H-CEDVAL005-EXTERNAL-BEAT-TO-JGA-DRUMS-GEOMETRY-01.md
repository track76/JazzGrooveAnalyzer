# H-CEDVAL005-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY-01

Status: **PREREGISTERED — NOT EXECUTED**

## Frozen authorities and scientific question

This protocol is bound exclusively to:

- JGA execution `EXEC-CEDVAL005-REAL-AUDIO-20260824-112305`, scientific
  fingerprint
  `074d84768f508e6ceee9c9225c34e9ea881ce50d88e0d5f930525b92e87bd9d6`,
  and its frozen `elementary_metric_events.json`, SHA-256
  `81e45700196b7f712237da5ac6bbb32324a3f782bb66022e2427b08d9e342f2d`;
- exactly 907 frozen Drums EME from that execution; Double Bass EME are
  excluded; and
- external execution
  `EXEC-CEDVAL005-EXTERNAL-BEAT-BENCHMARK-20260824-164758`, combined
  fingerprint
  `accf7ae656178cb04fb798795658b7d4f6e2bd5a7616f47755d7579435100e38`;
  its 468 frozen Essentia ticks from `essentia_output.json`, SHA-256
  `b630ba72957c2fa6ec2e67e825cc17ceb3a9c4a27a75743e08a39658ae21443d`;
  and its 464 frozen librosa beats from `librosa_output.json`, SHA-256
  `1ab3bed4271746300ce50d92d82cbd0a532d47ff74598b89c212b88e3010c926`.

No population may be recomputed, filtered, augmented or altered.

Scientific question: on the common absolute distributed-file time coordinate,
what is the neutral temporal geometry between (A) frozen Essentia beat
positions and frozen JGA Drums EME, and (B) frozen librosa beat positions and
frozen JGA Drums EME?

This is descriptive geometry, not beat validation.

## Coordinate authority

All comparisons use exact absolute distributed-file time with origin at file
sample zero and sample rate 44,100 Hz.

- For each JGA Drums EME, preserve immutable `producer_frame` and require
  `producer_sample_coordinate = 512 * producer_frame`. Its exact comparison
  coordinate is the rational number
  `producer_sample_coordinate / 44,100`. Its frozen binary64 timestamp must
  equal the correctly rounded representation of that rational and round-trip
  to its frozen hexadecimal representation.
- For each librosa beat, preserve its frozen native integer frame and require
  `beat_sample = 512 * beat_frame`. Its exact comparison coordinate is
  `beat_sample / 44,100`; its frozen decimal and binary64 hex must round-trip
  exactly.
- For each Essentia tick, preserve the frozen binary64 seconds and hex. For
  exact comparison, interpret that binary64 value by its exact
  `as_integer_ratio()` rational. Do not quantize it onto the JGA lattice and do
  not infer an authoritative sample coordinate.

No coordinate may be rounded, interpolated, shifted, corrected, resampled or
aligned before comparison. Every rational signed/absolute result shall be
preserved as numerator and denominator; a derived binary64 seconds value and
milliseconds value may also be reported with binary64 hex.

## Frozen nearest geometry

Apply the following independently to every external beat of each tracker
against the complete 907-EME Drums population. Sort Drum observations by exact
time, then stable EME identity; retain distinct equal-time EME identities.

For external time `b` and each Drum EME time `d`:

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

The required scalar signed-displacement population uses one deterministic
serialization representative without changing the preserved nearest set:
order nearest identities by (1) preceding-or-equal before following, (2) exact
Drum time ascending, and (3) stable EME identity ascending; serialize the first.
This is a record-stability convention only, not preferred correspondence. All
tied identities and their signed values remain explicit. Absolute distance is
identical across the nearest set.

Boundary status is:

- `BEFORE_FIRST_JGA_OBSERVATION` when `b` precedes the earliest Drum time;
- `AFTER_LAST_JGA_OBSERVATION` when `b` follows the latest Drum time; or
- `INTERIOR_OR_ENDPOINT` otherwise.

Before-first cases have no preceding identity; after-last cases have no
following identity. The available side remains eligible as nearest. A beat
exactly at an endpoint is not outside. `UNRESOLVED` is permitted only if the
frozen Drum population is absent, malformed or fails coordinate authority; any
such condition stops the full study with `EVIDENCE_CONFLICT` rather than
forcing geometry.

## Outputs and descriptive statistics

For Essentia and librosa separately preserve:

- external beat count, localized count and unresolved count;
- preceding, following and nearest availability counts;
- tie and boundary-status counts;
- complete case-level external identities/coordinates, complete preceding,
  following and nearest identity sets, serialization representative,
  rational signed displacement and rational absolute displacement;
- complete ordered scalar signed-displacement and absolute-displacement
  populations; and
- provenance and deterministic scientific fingerprints.

For signed and absolute scalar populations report minimum, linear-interpolated
Q1, median, Q3, maximum, arithmetic mean and population standard deviation.
Quantiles use index `(n - 1) * p` for `p = 0.25, 0.50, 0.75`; population SD
divides by `n`. Statistics are computed from exact rational values where
algebraically supported, with binary64 descriptive renderings preserved; no
tolerance or exclusion is permitted.

## Frame-lattice descriptive counts

Let `F = 512 / 44,100` seconds exactly. Using each beat’s exact nearest
absolute distance, report these cumulative/descriptive quantities separately
per tracker:

- `exact_zero_count`: distance `= 0`;
- `within_one_jga_frame_count`: distance `<= F`, including exact zero;
- `within_two_jga_frames_count`: distance `<= 2F`, including the one-frame
  population; and
- `beyond_two_jga_frames_count`: distance `> 2F`.

Also preserve the disjoint audit partition `=0`, `(0,F]`, `(F,2F]`, and
`>2F` so arithmetic cardinality can be verified. These are descriptive bins,
not accuracy thresholds, correctness criteria, matching tolerances or
calibration windows. Essentia timestamps remain off-lattice when frozen that
way.

## Separate analyses and future five-window projection

Essentia-to-JGA and librosa-to-JGA results must remain independent. No
Essentia-to-librosa matching, comparison, agreement, preference, pooling or
ranking is permitted.

A later visualization may project the three frozen observational layers onto
the existing five sample-coordinate windows:

1. `W1 [896557, 1117057)`
2. `W2 [2910171, 3130671)`
3. `W3 [4923786, 5144286)`
4. `W4 [6937400, 7157900)`
5. `W5 [8951014, 9171514)`

JGA and librosa window membership uses their exact integer sample coordinate.
Essentia membership uses exact rational comparison of its frozen binary64
seconds against `start_sample/44,100 <= tick < end_sample/44,100`; this does
not create an Essentia sample coordinate. No overlay is rendered by this
preregistration.

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

`PASS` means only that the two frozen external populations can each be compared
deterministically with frozen JGA Drums observations on the common
distributed-file coordinate. It does not mean either tracker is musically
correct.

External beats remain `CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`; JGA Drums EME
remain `FRAME_RESOLVED_JGA_OBSERVATION`. Neither is Ground Truth. Geometry is
not correspondence, a shared event, detector accuracy, synchronization,
physical onset or performance timing.

The tracker-reported approximately 123 BPM values and Readme approximately 246
BPM value are forbidden interpretation inputs. No BPM reasoning, meter,
measure, downbeat, beat number, symbolic information, H02, strength, human
validation or musical interpretation is permitted.

JGA, Essentia and librosa are not rerun. JGA Core, production code, raw assets,
frozen populations and historical authorities remain unchanged. No tracker is
preferred and no future integration is authorized.
