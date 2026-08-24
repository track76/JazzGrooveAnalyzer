# H-CEDVAL006-EXTERNAL-BEAT-POSITION-FEASIBILITY-01

Status: **PREREGISTERED — NOT EXECUTED**

## Scientific question and frozen input

Can Essentia and librosa independently produce deterministic, nonuniform
beat-position timelines from the frozen CED-VAL-006 Drum-overhead recording,
suitable for later neutral comparison with the already-frozen JGA Drums
observations?

This external-only protocol is bound to dataset authority
`PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`, fingerprint
`9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`,
and analytical-input authority `PR-CEDVAL006-ANALYTICAL-INPUTS-001`,
fingerprint
`cf89598f0f198cb14ee4f455b4094cffe3e4b4597da4fd92d2fffba41a233bae`.

Its only audio asset is the original
`Dums Overheads LCT 640 TS-Dual Output Mode.wav`, SHA-256
`dbfc4c3c59cac2c42cb2bbd33f1e55dbb1ec8c2fe6c6d095e30efc791dd57b8d`:
stereo signed 24-bit PCM, 48,000 Hz, 11,912,868 frames per channel, exact
duration `992739/4000` seconds (`248.184750` seconds), and original
distributed-file sample zero as temporal origin. `BASS - DI.wav` is excluded.

The existing CED-VAL-006 JGA execution and its EME, PulseCandidate, AD-038 and
AD-040 artifacts are forbidden input until both tracker outputs have been
independently frozen.

## Native shared mono authority

Before either tracker runs, an external validation-only decoder shall verify
the WAVE/checksum authority and decode every frame directly from signed 24-bit
little-endian PCM. For integer channel samples `L[n]` and `R[n]`, construct:

`native_mono[n] = float32((int64(L[n]) + int64(R[n])) / (2 * 8388608))`.

Equal channel weights are fixed. Evaluation uses the int64 sum, binary64
division, then one explicit float32 cast. The result must be a C-contiguous,
one-dimensional, little-endian/native float32 array of exactly 11,912,868
samples at 48,000 Hz with sample zero unchanged. Freeze its shape, dtype,
complete raw-byte SHA-256, minimum, maximum, sample rate, scope and construction
implementation/environment before any tracker execution.

No normalization, gain, trimming, padding, shift, warp, filtering, source
separation or other native preprocessing is permitted. The mono authority is
constructed without consulting tracker or JGA output.

## Tracker A — Essentia and external-only resampling

Tracker A is `Essentia RhythmExtractor2013` in standard mode:

- package `essentia==2.1b6.dev1389`;
- wheel `essentia-2.1b6.dev1389-cp313-cp313-macosx_15_0_arm64.whl`;
- wheel SHA-256
  `84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9`;
- CPython 3.13.14, macOS arm64, CPU only;
- `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, and
  `VECLIB_MAXIMUM_THREADS=1` before process start;
- `method="multifeature"`, `minTempo=40`, `maxTempo=208`.

These are the complete public `RhythmExtractor2013` parameters. The tempo
bounds are frozen package defaults and do not consume any supplied, inferred,
looked-up or video-derived BPM. Before execution, use an isolated external
environment and freeze the wheel, imported version/build, executable,
architecture, thread variables and complete resolved dependency identities.
Essentia must not enter JGA or production requirements.

Essentia requires a 44,100 Hz input. Construct its tracker-only input with
installed `scipy==1.18.0` and exactly:

```python
essentia_mono_44100 = scipy.signal.resample_poly(
    native_mono,
    up=147,
    down=160,
    axis=0,
    window=("kaiser", 5.0),
    padtype="constant",
    cval=0.0,
)
```

The frozen SciPy implementation source authority is
`scipy/signal/_signaltools.py`, SHA-256
`ae162c8d1c43ee90fae826ab9f9232425bf66042b84d97fcd808b270d9309a51`.
Freeze the complete SciPy/NumPy distribution/build identities and thread
environment at execution. The output must be one-dimensional contiguous
float32 with exactly
`ceil(11912868 * 147 / 160) = 10944948` samples at 44,100 Hz. Freeze its raw
bytes, SHA-256, dtype, shape, minimum, maximum, construction configuration and
fingerprint before Essentia runs. Any deviation is
`RESAMPLED_INPUT_AUTHORITY_CONFLICT`.

This is zero-phase rational polyphase filtering with explicit zero-valued
boundary extension. Output sample zero is aligned with native sample zero.
For resampled sample index `m`, its nominal original coordinate is
`m * 160 / 147` samples and its time is exactly `m / 44100` seconds, equal to
that nominal coordinate divided by 48,000. The output array extent is
`10944948/44100 = 130297/525` seconds (`248.1847619047619` seconds), exceeding
the original duration by exactly `1/84000` second solely because output length
is the ceiling of the rational conversion.

Essentia ticks retain the algorithm's returned binary64 seconds as primary
authority. A tick's original distributed-file time is the same elapsed-seconds
value from common sample zero. Do not round a tick to either sample grid and do
not claim sample-exact equivalence. Reject a tick outside the original frozen
scope `[0, 992739/4000]` seconds, including the resampler's possible
ceiling-only tail.

Supply the frozen resampled float32 array directly to
`RhythmExtractor2013`; do not use `MonoLoader` or any further resampling.
Preserve all five native outputs unchanged:

- global `bpm` descriptor;
- complete ordered `ticks` in binary64 seconds;
- track-level `confidence` (not per-beat confidence or correctness);
- native `estimates` BPM population; and
- native ordered `bpmIntervals` population.

Preserve native types/shapes, decimal and binary representations, full
configuration/environment, both input authorities, status, provenance,
replay evidence and scientific fingerprint. Essentia exposes no authoritative
native sample index for ticks in this contract. Non-finite, negative,
non-monotonic or out-of-original-scope ticks are
`TRACKER_OUTPUT_AUTHORITY_CONFLICT`; empty success is
`EMPTY_TRACKER_OUTPUT`; process/algorithm failure is
`TRACKER_EXECUTION_FAILURE`. No repair is allowed.

Essentia remains subject to its AGPLv3/open non-commercial and separate
proprietary licensing paths. This authorizes research execution only.

## Tracker B — librosa on native 48 kHz authority

Tracker B is installed `librosa==0.11.0`, with installed `numpy==2.4.6` and
`scipy==1.18.0`, using exactly:

```python
librosa.beat.beat_track(
    y=native_mono,
    sr=48000,
    onset_envelope=None,
    hop_length=512,
    start_bpm=120.0,
    tightness=100,
    trim=True,
    bpm=None,
    prior=None,
    units="frames",
    sparse=True,
)
```

`start_bpm=120.0` is the unchanged package baseline default, not supplied or
inferred recording tempo. No external onset envelope, tempo track, annotation
or prior is permitted. Freeze the full callable signature/source checksum,
distribution/dependency identities, Python executable, OS/architecture and
thread environment before execution.

Preserve the returned global tempo array/value exactly, including dtype,
shape and binary representation, and the complete ordered integer beat-frame
population. For each frame `f`, preserve exact native coordinates:

`beat_sample = 512 * f`

`beat_seconds = beat_sample / 48000`.

The resolution is exactly `512/48000 = 4/375` seconds, approximately
10.6666666666667 ms. It is frame-resolved, not sample-accurate onset authority.
Preserve derived successive inter-beat intervals as exact differences of the
frozen beat times and label them derived. No beat-level confidence exists in
this API and none may be invented. Non-integer, negative, unordered or
out-of-scope frames are `TRACKER_OUTPUT_AUTHORITY_CONFLICT`; empty success is
`EMPTY_TRACKER_OUTPUT`; exceptions are `TRACKER_EXECUTION_FAILURE`.

librosa is ISC-licensed. No distribution or production-integration decision
is authorized.

## Variable tempo and output contracts

Preserve both complete, nonuniform beat-position sequences exactly. Do not
regularize, extrapolate or construct a constant-BPM grid. Global BPM values are
tracker-reported descriptive metadata only.

Each tracker authority must preserve tracker identity, package/build,
environment, exact input identities and fingerprints, configuration, ordered
native outputs, permitted time/coordinate representations, interval outputs,
confidence semantics, status/failure evidence, two-run replay and a
deterministic scientific fingerprint. Freeze one combined benchmark authority
over both complete independent tracker records, manifests and replay evidence.

## Blind order and deterministic replay

Future execution order is fixed:

1. verify the original WAV authority;
2. construct and freeze the native 48 kHz mono authority;
3. construct and freeze the external-only 44.1 kHz Essentia input;
4. execute Essentia twice in fresh processes;
5. require exact output-contract replay and freeze Essentia;
6. execute librosa twice in fresh processes on native 48 kHz mono;
7. require exact output-contract replay and freeze librosa;
8. freeze the combined external-tracker authority; and
9. only then may a separately preregistered protocol access JGA EME.

Exact replay includes array authorities, tracker identities, native types and
shapes, every binary numeric value, ordered output populations, statuses and
fingerprints. Scientific-content disagreement is
`DETERMINISTIC_REPLAY_FAILURE`; do not average, select or reconcile runs.
Random seeds/state are `NOT_USED`; preserve CPU and thread authority.

## Epistemic, historical and architectural firewall

Both outputs remain `CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE`. They are not
Ground Truth, `BeatReference` authority, correspondence, JGA calibration,
synchronization authority or musical interpretation.

`JGA CORE IS NOT A BEAT DETECTOR` remains authoritative. Trackers,
resampling, BPM metadata, arrays, models and state remain external research
instruments. This benchmark defines no JGA comparison, matching rule,
tolerance, score, correction, tracker preference or human validation.

No JGA EME, JGA rerun, external/supplied/inferred BPM, LEWITT video timing,
H02, PulseCandidate strength, symbolic information or musical interpretation
is permitted. JGA Core, production code, raw assets, historical authorities
and the frozen CED-VAL-006 observational result remain unchanged. Neither
tracker nor the resampler has been executed on the target audio by this
preregistration.
