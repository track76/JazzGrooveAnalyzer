# H-CEDVAL006-REAL-LIVE-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01

Status: **PREREGISTERED — NOT EXECUTED**

## Frozen authorities and scientific question

This protocol is bound exclusively to:

- dataset authority
  `PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`, fingerprint
  `9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`;
- analytical-input authority `PR-CEDVAL006-ANALYTICAL-INPUTS-001`,
  fingerprint
  `cf89598f0f198cb14ee4f455b4094cffe3e4b4597da4fd92d2fffba41a233bae`;
- locked AD-037, AD-038 and AD-040 architecture; and
- the unchanged production observation configuration authoritative at future
  execution.

Scientific question: can the unchanged JGA observational stack produce a
deterministic, provenance-complete absolute-time and Drum-relative
`RhythmSectionTimingProfile` from the frozen CED-VAL-006 live-band analytical
inputs, without metric, symbolic, correspondence, calibration-correction,
beat-tracker or interpretive input?

## Frozen inputs and roles

The common distributed-file scope is `[0, 11912868)` at 48,000 Hz, exactly
`992739/4000` seconds.

- `Dums Overheads LCT 640 TS-Dual Output Mode.wav`, SHA-256
  `dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`,
  stereo signed 24-bit PCM, source `Drums`, experiment-local role
  `TEMPORAL_REFERENCE`;
- `BASS - DI.wav`, SHA-256
  `c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9`,
  mono signed 24-bit PCM, source `Double Bass`, experiment-local role
  `ACCOMPANIMENT`.

Both assets remain original raw files. No derived source is permitted. Role
bindings are experiment-local and do not arise automatically from instrument
identity.

## 48 kHz temporal-mapping gate

The gate is **PASS** by read-only implementation inspection. The unchanged
loader calls `librosa.load(path, sr=None, mono=False)`, so both inputs retain
their native 48,000 Hz rate and complete file scope. No library or JGA layer
resamples them. Both sources therefore undergo the same temporal mapping back
to their original distributed-file coordinates.

The existing preprocessing path loads float32 channel data, averages stereo
channels arithmetically to mono, and peak-normalizes non-silent audio in
memory. Thus Drums undergo unchanged stereo averaging and both sources undergo
the existing peak-normalization rule. These amplitude operations preserve
sample count, sample zero and temporal coordinates; they do not modify the raw
assets or authorize a derived analytical asset. `NullSeparator` then preserves
the processed signal's sample rate and scope.

The authoritative analysis hop is the unchanged librosa/JGA default of 512
input samples. At 48,000 Hz its exact spacing is `512 / 48000 = 4 / 375`
seconds (approximately 10.6666666666667 ms).

For this experiment:

- `producer_frame` is the immutable, zero-based onset-analysis frame index
  returned by the unchanged `librosa.onset.onset_detect` path;
- `producer_sample_coordinate = 512 * producer_frame` on the original-file
  sample coordinate; and
- `timestamp_seconds = producer_sample_coordinate / 48000`.

Future execution must preserve the integer frame and sample coordinate
explicitly. For every timestamp it must reconstruct the unique frame with
`round(timestamp_seconds * 48000 / 512)` and require exact binary64 agreement
with `librosa.frames_to_time(frame, sr=48000, hop_length=512)`. Any failure or
ambiguity is an evidence conflict. This mapping is frame-resolved and does not
claim sub-frame or sample-accurate physical-onset precision.

The implementation authorities inspected for this gate are checksum-bound in
future provenance, including the audio loader, audio preprocessor, null
separator, PulseCandidate builder/adapter, AD-037 builder, AD-038 builder,
AD-040 builder and default pipeline. Future execution must verify the same
implementation identities before analysis.

## AD-037 observation authority

Execute the existing observation path without parameter or implementation
change. Preserve every authorized source-specific `PulseCandidate`, including
stable identity, producer frame/sample/time authority, source/contributor
identity, lineage and execution provenance. No candidate may be suppressed for
musical plausibility. Strength and confidence may not be read, serialized as
scientific output, analyzed or used for any decision in this protocol.

AD-037 governs EME materialization: each preserved Domain PulseCandidate
independently supports exactly one source-event `ElementaryMetricEvent`.
Preserve stable EME identity, exact timestamp, producer authority, candidate
lineage, source/contributor identity and provenance. Multiple EME at one
timestamp remain distinct. No timing correction is permitted.

## AD-038 neutral geometry

Apply AD-038 unchanged to every eligible Double Bass EME against the complete
Drums EME population. Preserve preceding, following and nearest Drum EME,
signed and absolute displacement, exact tie state, unresolved state,
relationship status and provenance exactly as the existing authority defines
them. Temporal proximity remains `GEOMETRIC_ONLY`; it must not become event
correspondence or shared beat identity.

## AD-040 profile authority

Create exactly one read-only AD-040 `RhythmSectionTimingProfile` from the two
frozen experiment-local roles. Preserve deterministic profile identity,
represented EME and localization references, exact source and relationship
counts, original-file time scope, role bindings, provenance, limitations and
replay authority. Profile construction may not replace or reinterpret AD-037
or AD-038 authority.

## Correspondence, metric, calibration and interpretation firewalls

Correspondence status is `GEOMETRIC_ONLY`. H02, PulseCandidate strength,
Essentia, librosa, BPM, tempo estimates, meter, measures, beats, downbeats,
symbolic score, manual annotations and musical form are forbidden.
`AUTHORIZED_EVENT_RELATION` may not be created.

Calibration applicability is `UNESTABLISHED`. No numerical calibration,
offset or timing correction transfers from CED-VAL-001/002/003/004/005.

No shared beat identity, rushing, dragging, swing, groove, synchronization,
performance quality or performer intention may be inferred or reported.

## Acquisition and Ground Truth status

LEWITT's primary provider declaration supports a live performance containing
Drums and upright/double bass and supports `RAW`, no-editing and no-tuning only
to the extent of its wording. Shared hardware clock and common session-time
origin remain `UNESTABLISHED / NOT EXPLICITLY DOCUMENTED`. Physical-onset
Ground Truth is `NOT ESTABLISHED`. These limitations do not block neutral
distributed-file-coordinate observation, but they prohibit acquisition-time
or human-microtiming claims.

## Frozen future outputs and descriptive rules

For each of Drums and Double Bass preserve and report:

- total PulseCandidate and EME counts;
- complete producer-frame, producer-sample and original-file timestamp
  populations and their scopes;
- source/contributor identity and complete lineage/provenance; and
- deterministic replay status.

For AD-038 preserve and report:

- total eligible, localized and unresolved Double Bass EME;
- predecessor, follower and nearest availability counts;
- nearest-tie count and complete relationship-status counts;
- complete signed and absolute displacement populations; and
- for each population, minimum, linear-interpolated Q1, median, Q3, maximum,
  arithmetic mean and population standard deviation.

Quantiles use linear empirical interpolation at index `(n - 1) * p` for
`p = 0.25, 0.50, 0.75`; population SD divides by `n`. Empty populations remain
explicit and report statistics as unavailable. All quantities are descriptive
geometry only.

For AD-040 preserve profile identity and fingerprint, represented source and
role identities, total represented EME, source-specific counts, localization
references, exact file-coordinate scope, relationship-status counts,
provenance, limitations and replay result.

Preserve a checksum-bound input manifest, complete observation and geometry
populations, source summaries, AD-040 profile, artifact manifest, replay
evidence, report, completion protocol and final scientific fingerprint.

## Deterministic replay

Perform at least two complete independent executions under one frozen
environment and configuration. Require exact agreement of input checksums,
temporal mapping, PulseCandidate identities and producer coordinates, EME
identities/timestamps/lineage, source identities, AD-038 identities and all
reference/status/displacement values, AD-040 identity, counts, artifacts and
scientific fingerprint. Any material disagreement is `FAIL / STOP`; do not
average, reconcile or retune executions.

## Success and stop criteria

`PASS` means only that the unchanged JGA observational stack deterministically
produces a provenance-complete, source-labelled, absolute-time and
Drum-relative profile from the frozen CED-VAL-006 inputs. It does not establish
event correspondence, physical onset, common hardware clock, human
microtiming, beat placement, swing, rushing/dragging, groove, calibration
applicability or generalization.

Stop with `FAIL`, `INSUFFICIENT_AUTHORITY` or `EVIDENCE_CONFLICT` if input
authority fails; the 48 kHz mapping becomes ambiguous; implicit resampling
prevents exact source-file mapping; JGA requires modification; replay differs
materially; identity/provenance is lost; AD-037/038/040 requires unauthorized
interpretation; or any BPM, beat-tracker, metric, correspondence, H02,
strength, symbolic or calibration aid becomes necessary. Do not repair or tune
the experiment to obtain `PASS`.

Architecture impact: **NONE**. Production impact: **NONE**. Production code,
raw assets and every historical CED-VAL authority remain unchanged.
