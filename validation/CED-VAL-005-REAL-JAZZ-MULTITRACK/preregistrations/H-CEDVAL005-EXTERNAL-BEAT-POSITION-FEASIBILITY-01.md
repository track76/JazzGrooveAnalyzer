# H-CEDVAL005-EXTERNAL-BEAT-POSITION-FEASIBILITY-01

Status: **PREREGISTERED — NOT EXECUTED**

## Scientific question and authority

Can two existing external beat trackers independently produce deterministic
beat-position timelines from the frozen CED-VAL-005 Drum analytical input,
suitable for later neutral comparison with immutable JGA EME timestamps?

This protocol is bound to dataset authority
`PR-CED-VAL-005-REAL-JAZZ-MULTITRACK-001` and analytical-input authority
`PR-CEDVAL005-ANALYTICAL-INPUTS-001`. Its sole audio input is the original raw
asset `09_Overheads.wav`, SHA-256
`0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`,
stereo signed 24-bit PCM, 44,100 Hz, 10,068,072 sample frames, with
distributed-file sample zero as temporal origin. `11_BassDI.wav` is excluded.

Tracker output has epistemic status
`CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`. It is not Ground Truth,
`BeatReference` authority, correspondence, calibration, correction or musical
interpretation.

## Shared external input construction

Before either tracker runs, an external validation-only decoder shall verify
the input checksum and WAVE authority, decode every stereo frame directly from
signed 24-bit little-endian PCM, and construct one shared mono array. For each
sample frame `n`, using signed integer channel samples `L[n]` and `R[n]`:

`mono[n] = float32((int64(L[n]) + int64(R[n])) / (2 * 8388608))`.

The arithmetic mean uses equal fixed channel weights. The resulting contiguous
10,068,072-element float32 array is the identical in-memory signal supplied to
both trackers. Its complete raw byte representation and SHA-256 shall be frozen
before tracker execution. No tool-specific audio loader may redefine decoding,
mono conversion, sample zero or sample count.

No trimming, padding, time shift, warp, normalization, gain adjustment,
filtering, source separation, onset processing, resampling or other
preprocessing is permitted. The sample rate passed to both trackers is exactly
44,100 Hz. If either pinned tracker cannot consume this array unchanged, stop
with `TRACKER_INPUT_INCOMPATIBLE`; do not adapt the signal.

## Tracker A — Essentia

Tracker A is the standard-mode Essentia `RhythmExtractor2013` algorithm:

- package: `essentia==2.1b6.dev1389`;
- wheel:
  `essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl`;
- wheel SHA-256:
  `84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9`;
- runtime: CPython 3.13.14, macOS arm64; CPU only;
- threading: `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1` before process start;
- input: the shared float32 mono array, with no `MonoLoader` or resampling;
- `method="multifeature"`;
- `minTempo=40`;
- `maxTempo=208`.

These are the complete public parameters of `RhythmExtractor2013`; the tempo
bounds are frozen package defaults and do not consume the Readme BPM. Before
execution, installation must occur in a dedicated external environment and
freeze the wheel, complete resolved dependency manifest, imported Essentia
version/build string, Python/runtime, OS, architecture, environment variables
and executable identity. An inability to install or import the exact wheel is
`TRACKER_ENVIRONMENT_FAILURE`, not authority to substitute another build.

Preserve the five native outputs without alteration:

- `bpm`: one tracker-estimated global BPM descriptor;
- `ticks`: the complete ordered beat-position population in binary64 seconds
  relative to distributed-file sample zero;
- `confidence`: one track-level multifeature confidence value, not per-beat
  confidence and not probability of correctness;
- `estimates`: the native BPM-estimate population; and
- `bpmIntervals`: the native ordered inter-beat intervals in seconds.

Essentia exposes no authoritative native sample/frame index for these ticks in
this contract. Preserve each seconds value both as decimal and binary64 hex.
`tick * 44,100` may be stored as an exact derived binary64 scale value, but no
rounded sample coordinate gains authority. Reject non-finite values,
non-monotonic tick order, negative ticks or ticks outside input scope as
`TRACKER_OUTPUT_AUTHORITY_CONFLICT`. A successful empty tick population remains
`EMPTY_TRACKER_OUTPUT`; an exception or process failure is
`TRACKER_EXECUTION_FAILURE`. Do not repair either result.

Essentia is available under its AGPLv3/open non-commercial licensing path and
separate proprietary licensing. This benchmark authorizes research execution
only, not distribution or production integration.

## Tracker B — librosa

Tracker B is installed `librosa==0.11.0`, using exactly
`librosa.beat.beat_track` with:

- `y=shared_mono_float32`;
- `sr=44100`;
- `onset_envelope=None` (use the function's internal onset-envelope path);
- `hop_length=512`;
- `start_bpm=120.0` (the package default, not the Readme BPM);
- `tightness=100`;
- `trim=True` (tracker output trimming only; the input signal is never
  trimmed);
- `bpm=None`;
- `prior=None`;
- `units="frames"`; and
- `sparse=True`.

No external onset envelope and no dynamic or human-supplied tempo track is
permitted. The tempo return is the tracker's global estimate and is descriptive
metadata only. Before execution, freeze the installed distribution identity,
complete dependency manifest and hashes, Python executable, Python 3.13.14,
librosa 0.11.0, NumPy 2.4.6, SciPy 1.18.0, Numba 0.65.1, macOS/arm64 identity,
thread environment and full callable signature/source checksum.

Preserve:

- the returned global tempo array/value exactly, including dtype, shape,
  decimal and binary representation;
- the complete ordered native integer beat-frame population;
- `beat_sample = 512 * beat_frame` as the exact derived distributed-file
  sample coordinate; and
- `beat_seconds = beat_sample / 44,100`, preserving decimal and binary64 hex.

The native temporal resolution is the 512-sample lattice
(`512/44,100` seconds, approximately 11.609977324263 ms). It is not
sample-accurate onset authority. librosa supplies no native beat-level
confidence in this API and no confidence field may be invented. Non-integer,
negative, unordered or out-of-scope frames are
`TRACKER_OUTPUT_AUTHORITY_CONFLICT`. A successful empty frame population is
`EMPTY_TRACKER_OUTPUT`; an exception is `TRACKER_EXECUTION_FAILURE`. No repair
or fallback is permitted.

librosa is ISC-licensed. This preregistration makes no distribution or
production-integration decision.

## Variable tempo and output freeze

Preserve each tracker’s nonuniform beat positions exactly. Do not create,
regularize or extrapolate a constant BPM grid. Global BPM values are only
tracker-reported descriptive metadata. Essentia intervals are native outputs;
librosa inter-beat intervals may be derived only as exact successive
differences between its frozen beat seconds and must be labelled derived.

Each tracker record shall preserve the study/tracker identity, package and
binary authority, input and mono-array checksums, complete configuration,
environment, ordered native outputs, all permitted coordinate
representations, native confidence status, output/failure status, execution
provenance and one deterministic output fingerprint.

## Blind execution and replay order

Future execution must occur in this order:

1. verify the frozen input checksum, format and scope;
2. construct and fingerprint the shared mono array;
3. execute Tracker A twice in fresh processes;
4. require exact Tracker A identity, native output, dtype/shape, binary64,
   status and fingerprint replay, then freeze Tracker A;
5. execute Tracker B twice in fresh processes;
6. require exact Tracker B identity, native output, frame/sample/time,
   dtype/shape, status and fingerprint replay, then freeze Tracker B;
7. freeze a combined authority containing both independent records, manifests,
   checksums, replay evidence and aggregate fingerprint; and
8. only after that combined freeze may a separately authorized protocol open
   frozen JGA EME artifacts.

Any replay disagreement is `DETERMINISTIC_REPLAY_FAILURE`. Do not average,
select or reconcile outputs. No random algorithmic parameter is exposed by the
frozen calls; nevertheless preserve process environment and any library random
state/seed interfaces as `NOT_USED`, and run on CPU with the frozen thread
limits.

During steps 1–7, JGA EME, PulseCandidates, strength, H02, Readme BPM, musical
content annotations and prior CED-VAL-005 visualization/geometry outcomes are
forbidden inputs. Human validation is not part of this study. If later needed,
it requires an independent preregistration with annotations concealed from
tracker output.

## Architecture and future comparison firewall

`JGA CORE IS NOT A BEAT DETECTOR` remains authoritative. Both trackers,
wrappers, environments, BPM estimates, beat arrays, tempo priors, confidence
and model state remain outside JGA Core and production code. The only future
architectural candidate is a separate external-temporal-reference boundary.

This benchmark ends after tracker-output freeze. It defines no JGA comparison,
nearest-neighbor rule, tolerance, matching, scoring, BeatReference promotion,
event correspondence, calibration, correction or interpretation. A later
independent protocol may compare the frozen Essentia ticks, frozen librosa beat
times and immutable JGA EME timestamps on the shared absolute distributed-file
coordinate.

JGA Core, production code, raw assets, frozen scientific authorities and
historical results remain unchanged. Neither tracker has been installed,
imported on the target audio, or executed by this preregistration.
