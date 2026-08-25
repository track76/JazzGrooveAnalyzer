# H-CEDVAL008-THREE-SYSTEM-VARIABLE-TEMPO-SYMBOLIC-BEAT-RECOVERY-01

Status: **PREREGISTERED — NOT EXECUTED**

Authority: PI approval to preregister against
`PR-CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-001`, authority commit `241f490`,
dataset fingerprint
`9aab028fb1ac6740f1e257d0254afea485225879be888d0e4b60c20ba46ee86d`.
The authority verifier passed before this record was created.

## Scientific question and falsifiable purpose

Given the same checksum-bound controlled `DRUM GT`, how do unchanged JGA
observational timing, librosa `beat_track`, and Essentia
`RhythmExtractor2013` recover the same independently frozen, deliberately
nonuniform 64-event `SYMBOLIC_BEAT_GROUND_TRUTH`?

The future evidence must distinguish event localization, nonuniform timeline
recovery, adaptation around known tempo changes, and usefulness as a possible
higher-level external rhythmic reference. Each system may fail through
misses, extras, timing error, interval error, transition discontinuity, or
non-reproducibility. This preregistration selects no winner and authorizes no
architecture.

## Frozen input and Ground Truth authority

The sole audio input is
`CED-VAL-008-VARIABLE-TEMPO-BENCHMARK-v0.1  DRUM GT.wav` (exactly two spaces
after `v0.1`), SHA-256
`cfeb385ab00320f654453a1ff64c6dce9d1d0e80c2008dade847df671a744848`:
readable signed 24-bit linear PCM, stereo, 44,100 Hz, 1,463,433 frames, scope
`[0,1463433)`. No MARKER waveform is an input, correction, or scoring target.

The sole scoring target is the existing frozen 64-event schedule, indices
0–63, in `symbolic_beat_reference.json`. Its exact rational seconds and sample
coordinates remain authoritative; non-integer coordinates are never rounded.
Meter is 4/4. The frozen segments are:

| Segment | Measures | GT beats | BPM | Exact spacing |
|---|---:|---:|---:|---:|
| S1 | 1–4 | 0–15 | 120 | `1/2 s = 22050 samples` |
| S2 | 5–8 | 16–31 | 100 | `3/5 s = 26460 samples` |
| S3 | 9–12 | 32–47 | 140 | `3/7 s = 18900 samples` |
| S4 | 13–16 | 48–63 | 110 | `6/11 s = 264600/11 samples` |

Transitions are T1 at beat 16 / `5.1.1`, T2 at beat 32 / `9.1.1`, and T3 at
beat 48 / `13.1.1`. No process constructing raw system output may read this
schedule, its BPM values, boundaries, cells, or derived metrics.

## Common-input fairness

For the two external trackers only, decode the authoritative signed 24-bit
stereo samples and construct once:

```text
shared_mono[n] = float32((int64(L[n]) + int64(R[n])) / (2 * 8388608))
```

Before tracker execution freeze its shape `(1463433,)`, dtype `float32`,
C-order raw-byte SHA-256, minimum, maximum, sample rate, sample-zero mapping,
construction implementation identity, and provenance. No derived WAV is
authority. Apply no normalization, trimming, shifting, latency correction,
resampling, or Ground-Truth-derived preprocessing.

JGA receives the original checksum-bound WAV through its unchanged loader and
system-native preprocessing. JGA is not modified to share the external
frontend. This deliberate input-path difference is retained as methodology
and provenance, not hidden as nominal frontend equivalence.

## Blind raw-output contracts

### System A — JGA observation

Future execution uses unchanged production JGA:

```python
AnalysisPipeline().analyze(str(DRUM_GT_PATH))
```

Supply no BPM, tempo map, meter, declared metric reference, symbolic schedule,
or tuning. Preserve every relevant Drum PulseCandidate and corresponding
AD-037 EME with immutable identity, frozen native index, source/contributor
identity, producer frame, exact producer sample coordinate, timestamp and
binary representation, lineage, source checksum, environment, commit, and
provenance. The scored JGA output population is the complete Drum AD-037 EME
population; PulseCandidates are retained as lineage evidence and are not a
second scored population. Require the established producer mapping
`producer_sample_coordinate = 512 * producer_frame`. Strength must not be
read or serialized. Confidence must not select, filter, or score output. JGA
remains `FRAME_RESOLVED_JGA_OBSERVATION`, not a beat tracker.

### System B — librosa baseline

Use `librosa==0.11.0`, CPU, the frozen shared mono at native 44.1 kHz, and:

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

`start_bpm` is deliberately omitted; its installed generic default is not a
dataset-tempo input. Preserve every returned native frame, native index,
`beat_sample = 512 * beat_frame`, exact derived rational time, binary values,
reported tempo information, callable signature/source identity, package,
environment, configuration, provenance, and fingerprint. If this exact call
natively returns a time-varying tempo representation, preserve it unmodified
as secondary raw metadata; do not retrospectively derive one from Ground
Truth.

### System C — Essentia comparator

Use `essentia==2.1b6.dev1389`, pinned wheel SHA-256
`84e5167b95d9e74b2ddd928555d5a1e11997a458dae25e653544a953bc3068b9`,
CPU, all declared thread limits equal to one, native 44.1 kHz frozen shared
mono, no resampling, and:

```python
RhythmExtractor2013(method="multifeature", minTempo=40, maxTempo=208)
```

Preserve the complete tick population and native indices, reported BPM,
intervals, confidence, estimates, exact binary64 values, package/wheel,
environment, configuration, provenance, and fingerprint. Binary64 seconds
are primary Essentia timing authority; descriptive scaled samples do not
become lattice authority.

No system receives 120, 100, 140, or 110 BPM, the boundaries, or any GT beat
position. Native tempo metadata is output, never an assignment input.

## Mandatory blind freeze and replay order

1. Verify the frozen CED-VAL-008 authority, input checksum, preregistration,
   environment, and dependency authority.
2. Construct and freeze the shared external mono authority.
3. Execute JGA twice in separate fresh processes.
4. Require exact JGA scientific-content, population, coordinate, and
   fingerprint replay; freeze both evidence records and one raw authority.
5. Execute librosa twice in separate fresh processes.
6. Require exact librosa scientific-content, population, coordinate, and
   fingerprint replay; freeze both evidence records and one raw authority.
7. Execute Essentia twice in separate fresh processes.
8. Require exact Essentia scientific-content, population, coordinate, and
   fingerprint replay; freeze both evidence records and one raw authority.
9. Freeze and fingerprint all raw outputs before Ground Truth access.
10. Only then open the frozen symbolic Ground Truth.
11. Execute scoring independently twice from frozen raw outputs and GT.
12. Require exact assignment, complete metric population, summary, and
    fingerprint replay; otherwise `FAIL / STOP`.

No output may influence GT, admissibility, assignment, segment or transition
definitions, metric definitions, or output filtering.

## Common one-to-one assignment and exact Voronoi cells

Let exact GT times be `g[0]..g[63]` and input-scope end be
`1463433/44100 = 487811/14700` seconds. Freeze cells:

```text
left(0)  = 0
left(i)  = (g[i-1] + g[i]) / 2                  for i > 0
right(i) = (g[i] + g[i+1]) / 2                  for i < 63
right(63)= 487811/14700
cell(i)  = [left(i), right(i))
```

All boundaries are computed as exact rationals from frozen authority. Cells
are contiguous, mutually exclusive, locally tempo-sensitive, and never
replaced by one global-BPM window.

Process GT events in increasing index. Among unmatched outputs in `cell(i)`,
select exactly one by: (1) minimum exact absolute displacement from `g[i]`;
(2) earlier exact timestamp; (3) lower frozen native output index. Each GT and
output can match at most once. Retain every eligible candidate, tied identity,
selected identity, displacement, and selection/tie reason. JGA/librosa lattice
coordinates remain exact samples/rationals. Essentia binary64 seconds are
converted to their exact rational values for comparison without rounding.

A **MISS** is a GT event with no selected eligible output. An **EXTRA** is
every frozen raw output not selected, including additional outputs inside a
GT cell and outputs outside the symbolic beat span. Outputs are not trimmed
before assignment. Any negative-time output is an authority failure. Outputs
at or beyond the half-open input end remain explicit out-of-scope extras and
cannot match.

## Global recovery and timing metrics

For each system freeze raw output count, matched count, missed count, extra
count, and:

```text
precision = matched / raw_output_count       (0 when raw_output_count = 0)
recall    = matched / 64
F1        = 2PR / (P + R)                    (0 when P + R = 0)
```

For every match preserve `signed_error = system_time - GT_time` and
`absolute_error = abs(signed_error)`. For both complete populations report
exact-zero count, minimum, linear-interpolated Q1, median, Q3, maximum, mean,
and population SD; also report signed-error RMSE. Linear interpolation uses
sorted values and rank `(n-1)p` for `p = .25, .5, .75`. Empty timing
populations have `UNDEFINED` summaries. Preserve exact samples for lattice
systems and exact binary64/rational seconds for Essentia. No latency
correction is permitted.

## Segment-specific analysis

Primary global assignment is immutable. For S1–S4 separately report expected
GT count 16, raw outputs occurring in the union of that segment's frozen GT
cells, matches, misses, extras in those cells, precision, recall, F1, complete
signed/absolute timing-error populations and summaries, and RMSE. Segment
precision uses `segment_matches / segment_raw_outputs` with the same zero-safe
rule; recall uses `segment_matches / 16`. A matched output is attributed by
its matched GT. An unmatched extra is attributed only by the unique cell
containing its timestamp. This reporting cannot alter global matching.

## Prospective transition analysis

The fixed nine-event neighborhoods are:

| Transition | Change | Boundary | Frozen GT identities |
|---|---|---|---|
| T1 | 120→100 BPM | beat 16 / `5.1.1` | beats 12–20 |
| T2 | 100→140 BPM | beat 32 / `9.1.1` | beats 28–36 |
| T3 | 140→110 BPM | beat 48 / `13.1.1` | beats 44–52 |

For each system and neighborhood report matches, misses, extras occurring in
the union of those nine cells, signed and absolute error per GT beat, RMSE,
pre-transition mean signed error over the four pre-boundary beats, boundary
beat error, post-transition mean signed error over the four post-boundary
beats, maximum absolute error, and recovery continuity. Missing-error values
remain missing; a mean is `UNDEFINED` when it has no matched inputs. Recovery
continuity is descriptive `true` only when all nine GT events have selected
outputs; it is not a proprietary score.

## Consecutive-interval and variable-tempo recovery

Include an interval only when consecutive GT events `i` and `i+1` both have
selected outputs. Preserve:

```text
system_interval = system_time(i+1) - system_time(i)
GT_interval     = g[i+1] - g[i]
interval_error  = system_interval - GT_interval
```

Globally and within each constant-tempo segment, preserve every eligible
interval and report interval count; complete signed and absolute interval
error; median and mean absolute interval error; population SD of signed
interval error; and signed interval-error RMSE. Segment populations include
only pairs whose two GT identities lie in that segment. Empty populations are
`UNDEFINED`.

For each transition at boundary `b`, report individually the first exactly
four post-change intervals `(b,b+1)`, `(b+1,b+2)`, `(b+2,b+3)`, and
`(b+3,b+4)` when both endpoint matches exist; otherwise preserve the missing
interval. This evaluates recovery of nonuniform temporal structure and does
not establish broader musical correspondence.

## Native tempo metadata and algorithmic independence

Preserve native tempo/interval trajectory information where a system emits
it, independently and unmodified, as secondary descriptive evidence. Do not
force conceptual equivalence and do not fabricate a JGA tempo trajectory.
The fair common comparison rests primarily on output timestamps and derived
consecutive intervals.

JGA and librosa are not fully algorithmically independent because JGA uses
librosa-based observational functionality. Librosa cannot independently
validate JGA; it remains a baseline and dependency-sensitivity comparator.
Essentia is the more algorithmically independent comparator. This caveat
cannot change assignment or scores.

## Future selection framework and architectural decision gate

Do not create a weighted composite or select a universal winner. Preserve
separate evidence dimensions: recovery (precision/recall/F1), localization
(absolute and signed error/RMSE), variable-tempo structure (interval error and
segment consistency), transition behavior, replay, and scientific
independence/provenance/architectural usefulness.

The result must distinguish `BEST TEMPORAL LOCALIZATION` from
`BEST EXTERNAL RHYTHMIC-REFERENCE CANDIDATE`; they may differ. Review must ask
whether JGA retains the strongest controlled localization, whether an external
tracker more reliably recovers variable structure, whether Essentia supplies
reproducible higher-level evidence absent from JGA, whether librosa adds
independent value, whether an External Temporal Reference Adapter is
scientifically justified, which tracker would be the primary research
candidate, and whether combination adds evidence sufficient to justify its
complexity. When scientifically simpler evidence is equivalent, prefer the
simpler path. No architecture proceeds before PI review.

## Claim and execution firewalls

Any future conclusion is scoped only to CED-VAL-008, controlled DS-Kick,
44.1 kHz, and the prospectively authored four-segment variable-tempo
configuration. It cannot establish universal superiority, jazz-performance
or human-microtiming validity, physical-onset accuracy, groove quality, swing,
rushing/dragging, intention, downbeat/meter validity, production calibration,
fixed latency correction, or universal beat-tracker accuracy.

For this preregistration: JGA, librosa, Essentia, beat detection, onset
detection, Ground Truth scoring, H02, strength, and rendered-response
measurement were not executed or accessed. No MARKER correction, latency
correction, production-code change, raw-asset change, historical-authority
change, or External Temporal Reference Adapter is authorized or performed.
