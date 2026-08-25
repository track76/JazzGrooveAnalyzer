# CED-VAL-006 Controlled-Mix Separation → JGA Robustness

Preregistration ID:
`H-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01`

Status: **FROZEN PREREGISTRATION — NOT EXECUTED**

## Scientific question and authorities

This characterization measures how CED-VAL-006 JGA temporal evidence changes
when the frozen `DETERMINISTIC_CONTROLLED_DERIVED_MIX` is passed through the
existing production Demucs runner before unchanged JGA v0.3.0-alpha analysis.
It compares against immutable original-stem acceptance
`ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-02` without using its results to
tune separation or JGA.

- JGA: `v0.3.0-alpha`, commit
  `c7b9b65362303ff17c48897c4d26a518595fe9c5`.
- Mix authority: `PR-CEDVAL006-CONTROLLED-MIXDOWN-001`, fingerprint
  `ed01d1d09b62cec41c36214d45027eb246e765dcec21d18456a9452cbba3e40c`.
- Mix SHA-256:
  `32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0`.
- Reference acceptance fingerprint:
  `ea1490dc0171631381186b6728ee1b49ce5549041c38410b06132d021ee7e100`.

The complete machine-readable protocol and exact fingerprint are in the
same-ID JSON record. The JSON controls if this summary conflicts with it.

## Frozen separation authority

Use existing `DemucsRunner.separate` directly with the frozen executable,
model `htdemucs`, and its supported `device="cpu"` parameter. CPU is selected
prospectively because the installed MPS backend is unavailable; this requires
no production change. The runner command does not expose other overrides, so
Demucs 4.1.0 defaults remain: one random shift, split processing, overlap
0.25, jobs 0, default segment, default `rescale` clipping policy, and 16-bit
WAV output.

The cached `htdemucs` bag contains model signature `955717e8`, checkpoint
`955717e8-8726e21a.th`, SHA-256
`8726e21a993978c7ba086d3872e7608d7d5bfca646ca4aca459ffda844faa8b4`.
Its exact taxonomy is `drums`, `bass`, `other`, `vocals`; all outputs are
stereo 44.1 kHz. Map only `drums.wav` to explicit `Drums /
TEMPORAL_REFERENCE` and `bass.wav` to explicit `Double Bass /
ACCOMPANIMENT`. Preserve all four stems as raw experimental outputs.

Input decoding uses sphn, stereo is preserved, and Julius resamples 48 kHz to
the model's 44.1 kHz. Demucs mean/std normalization and inverse scaling are
model processing. Output uses per-stem default rescale clipping prevention and
16-bit PCM encoding. No experiment-authored preprocessing or postprocessing is
allowed.

One random shift is part of the unchanged production command, so separation
is prospectively `POTENTIALLY_NONDETERMINISTIC`. Execute twice in independent
fresh processes with CPU thread environment variables frozen to 1. Preserve
both complete outputs. Classify `BYTE_IDENTICAL` only on complete four-stem
byte/checksum/technical equality; otherwise `SCIENTIFICALLY_NONIDENTICAL`.
Never select or average a run.

## Freeze and execution order

Verify every authority; execute and freeze two separation populations; classify
their replay; run the canonical JGA report independently on each run's Drum
and Bass stems; freeze raw reports; only then access complete original event
and relation records for scoring. Score twice independently and require exact
replay. Generated stems are experimental outputs, never Ground Truth.

## Level 1 — population robustness

For Drums and Bass independently preserve original/separated EME counts,
signed/absolute/relative count difference, first/last event times, temporal
span, exact scope duration, and count-per-scope-duration density. Count
equality is not event identity.

## Level 2 — cross-condition temporal stability

Construct half-open original-event Voronoi cells in absolute seconds. Interior
boundaries are exact midpoints between adjacent original EME; the first begins
at zero and the final ends at exact original scope end
`11912868/48000`. A separated EME is eligible only in its original cell.
Select minimum absolute displacement, then earlier separated time, then lower
frozen native output index. Each event is used at most once; preserve every
unmatched event and all tied identities.

Report matched/original-only/separated-only, descriptive precision/recall/F1,
complete signed and absolute displacement populations, exact-zero count,
minimum, linearly interpolated Q1, median, Q3, maximum, mean, population SD,
and RMSE. These describe cross-condition stability, not physical-onset error.

## Level 3 — AD-038 / AD-040 stability

For each matched Bass target, map original predecessor/follower/nearest Drum
references through the frozen Drum Level-2 mapping. Identity comparisons are
scorable only when required reference mappings exist; otherwise preserve
`UNSCORABLE_UNMATCHED_REFERENCE`. Compare relation counts, ties, geometry
populations and paired displacement differences without claiming musical
correspondence. Compare AD-040 represented counts, scope, structure,
relationship/status populations and the calibration triad.

## Firewalls

No latency correction, shift, alignment, retuning, EME editing, run selection,
normalization for agreement, H02, strength or calibration transfer is allowed.
The outcome is quantitative characterization without an arbitrary threshold.
It cannot establish general separator quality, universal JGA robustness, beat,
tempo/BPM, meter/downbeat, musical correspondence, swing/groove,
rushing/dragging, intention, human microtiming, physical onset,
acquisition-clock synchrony or calibration correction. No production,
architecture, Candidate Period, raw-asset or controlled-mix change is made.
