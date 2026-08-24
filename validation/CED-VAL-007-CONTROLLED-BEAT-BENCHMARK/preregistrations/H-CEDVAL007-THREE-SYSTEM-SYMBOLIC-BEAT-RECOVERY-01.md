# H-CEDVAL007-THREE-SYSTEM-SYMBOLIC-BEAT-RECOVERY-01

Status: **PREREGISTERED — NOT EXECUTED**

Authority: PI approval of the controlled authority and response review for
`PR-CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-001`, dataset fingerprint
`cd93455778d1484067f9a3caa3037b6467d27c7e8d5a8c0df694658bad2484e9`,
and `EXEC-CEDVAL007-RENDERED-RESPONSE-20260824-210717`, result commit
`aef1ad9df575869d03f01d31dfb612bd0ed2c734`.

## Scientific question

Given the same checksum-bound controlled `DRUM GT.wav`, how accurately do the
unchanged JGA observational stack, librosa `beat_track`, and Essentia
`RhythmExtractor2013` recover the same prospectively frozen 64-event
`SYMBOLIC_BEAT_GROUND_TRUTH` timeline?

For JGA, “recovery” means the ability of its Drums observational population to
recover the controlled symbolic schedule. It does not promote JGA Core to a
beat detector.

## Ground Truth and common input

The sole scoring target is the frozen population `i=0..63`:

```text
n_GT(i) = 22050 * i samples
t_GT(i) = i / 2 seconds
```

It contains 64 events at 44,100 Hz, from sample 0 / 0 seconds through sample
1,389,150 / 31.5 seconds. It must not be shifted or redefined.

All systems receive the authority of
`CED-VAL-007-CONTROLLED-BEAT-BENCHMARK-v0.1 DRUM GT.wav`, SHA-256
`c673d2c104eb3eb31012154f1bd84ee81313b4fd36b61bf3913686f43e19bb0c`,
signed 24-bit stereo PCM, 44,100 Hz, 1,411,200 frames, scope `[0,1411200)`.
No WAV is copied, normalized, trimmed, shifted, corrected, warped or
resampled externally.

For the two external trackers only, construct one shared array from decoded
signed 24-bit integers:

```text
shared_mono[n] = float32((int64(L[n]) + int64(R[n])) / (2 * 8388608))
```

Freeze its shape `(1411200,)`, dtype `float32`, C-order raw-byte SHA-256,
min/max, sample rate and sample-zero authority before tracker execution. Do
not normalize it. JGA receives the original WAV through its unchanged native
loader. Its existing internal stereo mean and peak normalization remain
system-native implementation behavior, not common-input modification or a
benchmark correction. No derived WAV becomes authority.

## Blind system-output contracts

Ground Truth coordinates, MARKER response values and response displacements
must not be loaded by the output-construction processes. Each complete raw
system output is executed twice, replay-verified, frozen and fingerprinted
before the Ground Truth artifact is opened for scoring.

### System A — JGA

Use the repository environment and unchanged production call:

```python
AnalysisPipeline().analyze(str(DRUM_GT_PATH))
```

Use no declared metric reference, BPM, meter, score, event schedule or tuning.
Preserve every domain PulseCandidate and AD-037 EME with identity, source and
contributor identities, producer frame, `producer_sample_coordinate = 512 *
producer_frame`, `timestamp = producer_sample_coordinate / 44100`, lineage,
asset checksum and provenance. Preserve the full populations without
filtering for this benchmark. Strength and confidence values must not be read,
serialized or used for selection or scoring. JGA output status remains
`FRAME_RESOLVED_JGA_OBSERVATION`.

### System B — librosa

Use `librosa==0.11.0`, native 44,100 Hz shared mono, CPU, and the exact call:

```python
librosa.beat.beat_track(
    y=shared_mono_float32,
    sr=44100,
    onset_envelope=None,
    hop_length=512,
    tightness=100,
    trim=True,
    bpm=None,
    prior=None,
    units="frames",
    sparse=True,
)
```

`start_bpm` is deliberately omitted. The library's generic installed default
is not supplied from the known dataset tempo. Preserve reported tempo as
descriptive output only, complete native beat frames, `beat_sample = 512 *
beat_frame`, `beat_time = beat_sample / 44100`, native types, environment,
configuration and fingerprint.

### System C — Essentia

Use `essentia==2.1b6.dev1389`, pinned CPython 3.13 macOS ARM64 wheel SHA-256
`84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9`,
CPU with all declared thread limits set to one, and:

```python
RhythmExtractor2013(method="multifeature", minTempo=40, maxTempo=208)
```

The bounds are the previously validated generic instrument configuration,
not values derived from CED-VAL-007. Supply the native 44,100 Hz shared mono;
no resampling. Preserve BPM, complete binary64 tick population, intervals,
confidence, estimates/distribution, native types, environment, configuration
and fingerprint. Returned binary64 seconds are primary timing authority and
must not be forced onto a sample lattice.

No system receives the known 120 BPM. Tracker-reported BPM is metadata only.

## Blind freeze and scoring order

1. Verify dataset, input, preregistration and raw checksum authority.
2. Construct and freeze the shared external-tracker mono authority.
3. Execute JGA twice in fresh processes; require exact replay; freeze output.
4. Execute librosa twice in fresh processes; require exact replay; freeze
   output.
5. Execute Essentia twice in fresh processes; require exact replay; freeze
   output.
6. Freeze and fingerprint all three complete raw-output authorities.
7. Only then open the frozen symbolic Ground Truth.
8. Execute the common scorer twice independently from frozen outputs and
   Ground Truth; require exact scientific-content replay.

No output may be filtered, suppressed or selected after Ground Truth access.

## Common one-to-one assignment

Let the inter-beat interval be `P=1/2` second. The closed admissibility radius
is frozen as `W=P/4=1/8` second, exactly 125 ms or 5,512.5 samples. It is
derived only from controlled beat geometry. Adjacent admissibility windows
are separated by 250 ms and cannot overlap; thus an output cannot be
admissible to two Ground-Truth beats.

For each GT event in ascending index order:

1. collect all as-yet-unmatched system outputs satisfying
   `abs(t_system - t_GT) <= 1/8 second`;
2. if none exist, mark that GT event missed;
3. otherwise select the output with minimum exact absolute displacement;
4. on an exact equal-distance tie, select the earlier timestamp;
5. if timestamps are exact duplicates, select the lower frozen native output
   index; and
6. match the selected output once and only once.

All unselected outputs are extras. Because windows are disjoint and processed
in time order, assignment is monotonic and one-to-one without a
system-specific density rule. For integer sample-coordinate systems, the
exact bound admits integer displacement magnitudes through 5,512 samples;
the rational 5,512.5-sample boundary remains the definition. Essentia uses
its exact stored binary64 value converted to its exact rational value for
comparison; it is not rounded.

The 125 ms window is an assignment admissibility rule, not a correctness
tolerance, calibration window or latency correction. Full raw populations,
misses, extras and matched error distributions remain visible.

## Boundaries, ties, misses and extras

GT event 0 uses its truncated recording-side interval `[0,1/8]`. Other GT
windows retain the same closed radius; the final GT window is wholly inside
the 32-second scope. System outputs are never trimmed to the GT span. Outputs
before sample zero are an authority conflict; outputs at or beyond 32 seconds
are preserved as `OUTSIDE_INPUT_SCOPE_EXTRA` if the system legitimately
returns them, not silently removed.

An unmatched GT event is a miss. Every frozen system output not selected by
the assignment is an extra, including additional observations within a GT
window and observations outside every admissibility window. Exact ties retain
all tied candidate identities plus the deterministic selected identity and
tie reason.

## Metrics

For each system independently:

```text
GT_count = 64
matched_count = number of assigned pairs
missed_GT_count = 64 - matched_count
extra_output_count = raw_output_count - matched_count
precision = matched_count / raw_output_count   (0 if raw_output_count is 0)
recall = matched_count / 64
F1 = 2*precision*recall/(precision+recall)      (0 if both are 0)
```

For every matched pair:

```text
signed_error = system_time - GT_time
absolute_error = abs(signed_error)
RMSE = sqrt(mean(signed_error^2))
```

Preserve complete signed and absolute populations; exact zero coincidence;
minimum, linear-interpolated Q1, median, Q3, maximum, arithmetic mean,
population standard deviation and RMSE. Report exact samples and derived
milliseconds for JGA/librosa. For Essentia report exact binary64/rational
seconds and derived milliseconds; scaled samples are descriptive only and not
sample-coordinate authority. Empty matched populations remain empty and
their timing statistics are `UNDEFINED`.

## Scientific interpretation and firewalls

The same assignment and metrics apply to all systems. JGA's extra
observations are neither specially penalized nor excused; its semantic status
as an observational population must remain explicit. JGA uses librosa-based
observation functionality and is not fully algorithmically independent from
`librosa.beat_track`; strong alignment between them cannot independently
validate JGA. Essentia is the more algorithmically independent comparator.
This caveat does not alter scoring.

The MARKER 64/64 result at +1 sample supports render mapping only. It is not
subtracted. The single localized Drum response is not generalized to the 63
unresolved events. No CED-VAL-004 latency, correction, shift or physical-onset
claim is permitted.

The benchmark can support comparative recovery claims only for this
CED-VAL-007 120-BPM, 44.1-kHz, quarter-note DS-Kick rendering configuration.
It cannot establish universal superiority, human-jazz performance, physical
onset or microtiming accuracy, swing/groove analysis, or production fitness.

No JGA, librosa, Essentia or scoring execution is authorized by this document.
Production code, raw assets and historical authorities remain unchanged.
