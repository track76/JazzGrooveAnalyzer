# Scientific Validation Campaign 1 — Candidate Period Discovery

Experiment ID: `H-VAL001-C1-03`

Run ID: `run_20260809_100843`

Hypothesis: The preserved VAL-001 temporal observations contain reproducible
evidence for more than one candidate periodicity, and those candidates can be
described without assigning musical metric meaning.

Status: COMPLETED

## Repository authority and controls

- Branch: `scientific/translation-layer-finalization`
- Source revision: `0b322875360311c5fe990be94aa253eb275ad0f6`
- Bootstrap revision: `0b32287`
- Current phase: Phase II Scientific Validation
- Governing theory: `F-031`
- Validation protocol: `SVP-001`
- Validation Item: `VAL-001`
- Controlled Dataset: `CED-VAL-001`
- Ground Truth: `GT-VAL-001-v1`, loaded only after the blind record was frozen

The pre-existing Baseline Evidence Conflict, Document-State Evidence Conflict,
and Experimental Artifact Path Evidence Conflict remain preserved. The
historical run under `validation/VAL-001/runs/` was not modified.

## Blind discovery protocol

Observed event timestamps were converted back to the existing librosa frame
grid using `round(timestamp × sample_rate / 512)`. Discovery inspected exact
consecutive positive frame gaps. A candidate was recorded when the same exact
gap occurred at least twice. This is the minimum evidence of recurrence and is
not a support-strength threshold.

No candidate selection, metric-level interpretation, Ground Truth quantity,
or production BeatPeriodEstimator output participated in discovery.

The blind execution began at `2026-08-09T10:12:01.544857+00:00` and completed
at `2026-08-09T10:12:10.823927+00:00` after two complete executions of the
full mix and five canonical WAV stems.

## Blind candidate evidence — Observed Facts

One frame is `512 / 44100 = 0.011609977324263039` seconds.

| Source | Events | Recurrent exact frame intervals: occurrence count |
|---|---:|---|
| Full mix | 77 | 3:3, 31:9, 32:9, 33:16, 34:7, 35:2, 36:3, 64:2, 66:8, 67:2, 69:5, 101:2 |
| Double bass | 27 | 33:8, 132:2, 232:6, 265:2 |
| Drums | 63 | 30:7, 33:19, 37:3, 66:15, 67:6, 70:3 |
| Piano | 49 | 17:4, 32:5, 33:6, 34:13, 65:5, 66:3, 100:2, 132:3, 165:2, 166:4 |
| Tenor sax | 16 | 3:2, 265:2 |
| Voice | 150 | 3:10, 4:12, 5:7, 6:13, 7:5, 8:5, 9:8, 10:6, 11:10, 12:11, 13:7, 14:4, 15:5, 16:5, 17:5, 18:3, 19:4, 20:6, 21:3, 22:2, 23:2, 24:3, 32:3 |

Exact timestamps, frames, complete interval populations, relative frequencies,
occurrence positions and temporal scopes are preserved in
`blind_candidate_discovery.json`.

The full-mix 33-frame candidate is `0.3831292517006803` seconds, occurs 16
times, and has relative frequency `16/76 = 0.21052631578947367`. The 66-frame
candidate is `0.7662585034013606` seconds, occurs 8 times, and has relative
frequency `8/76 = 0.10526315789473684`.

No canonical strong/weak threshold exists. Support is therefore reported only
as occurrence count, relative frequency, source identity and temporal scope.

## EnsembleMetricEvent audit — Observed Facts

For double bass, drums, and piano, the recurrent interval inventories are
identical to their ElementaryMetricEvent/PulseCandidate inventories. Tenor sax
retains only its recurrent 265-frame gap.

The full-mix EnsembleMetricEvent population contains recurrent gaps:

`31:8, 32:8, 33:17, 34:8, 35:2, 36:3, 64:2, 66:7, 67:4, 69:5, 101:2`.

Its 3-frame candidate disappears because observations within the existing
0.05-second consensus window are aggregated. Counts around 31–34 and 66–67
also change.

The voice EnsembleMetricEvent population differs substantially because the
same consensus aggregation operates on its dense events. All exact values are
preserved in the blind record.

## Average-spacing audit — Observed Facts

| Source | Arithmetic mean (frames) | Duration (s) | Exact recurrent candidate? |
|---|---:|---:|:---:|
| Full mix | 41.8421052631579 | 0.48578589330469035 | No |
| Double bass | 122.26923076923077 | 1.419542996685854 | No |
| Drums | 50.70967741935484 | 0.5887382049594031 | No |
| Piano | 62.833333333333336 | 0.729493575207861 | No |
| Tenor sax | 136.93333333333334 | 1.5897928949357523 | No |
| Voice | 13.825503355704697 | 0.16051378045625408 | No |

## Numerical relationships — Logical Inferences

- `66 / 33 = 2` exactly.
- Exact and approximate ratios among every pair of recurrent full-mix
  candidates are preserved in `post_blind_analysis.json`.
- These numerical relationships do not assign hierarchy or musical meaning.

## Post-blind Ground Truth comparison

Ground Truth was loaded after the blind record and fingerprint were frozen.
The authoritative value is quarter note = `78` BPM.

Derived durations — Logical Inferences:

- `60 / 78 = 0.7692307692307693` seconds;
- half: `0.38461538461538464` seconds;
- twice: `1.5384615384615385` seconds.

Independently discovered numerical correspondences:

- Full-mix 66-frame candidate differs from the derived quarter duration by
  `-0.0029722658294086823` seconds.
- Full-mix 33-frame candidate differs from half that duration by
  `-0.0014861329147043412` seconds.
- Drums contain the same 33- and 66-frame candidates 19 and 15 times.
- Piano contains them 6 and 3 times.
- Double bass contains 33 frames 8 times and 132 frames
  (`1.5325170068027212` seconds) twice.
- No musical identity is assigned to any candidate by these comparisons.

## Reproducibility — Observed Facts

- First blind numerical fingerprint:
  `2825974a1c91c2b1645240e712bd90e27a568fba1336c82cebe27527c8bc43b9`
- Repeated blind numerical fingerprint: identical
- Blind record fingerprint:
  `7a1ebec978115094e751f78eee84abd718933d6cff91200a2920adbd83c6de3c`
- Post-blind record fingerprint:
  `4d629f352348463523d92892642030b85aa184b3e79562a79e5d4909901806e0`

## F-031 proposition validation

| Proposition | Result | Evidence |
|---|---|---|
| Multiple periodicities may coexist | SUPPORTED | Every source contains at least two exact recurrent gaps; the full mix contains twelve. |
| Average spacing need not identify a recurrent candidate | SUPPORTED | The mean is not an exact recurrent candidate for any of the six sources. |
| Candidates can be preserved before metric interpretation | SUPPORTED | Blind populations and fingerprint were frozen without Ground Truth or level assignment. |
| Ratios alone do not establish hierarchy | QUALIFIED | Exact ratios exist, but the experiment contains no independent hierarchy-identifying evidence. |
| Ground Truth can evaluate without participating in discovery | SUPPORTED | Ground Truth was loaded only after blind freezing and did not alter candidates. |

## Scientific conclusion

The hypothesis `H-VAL001-C1-03` is **SUPPORTED within the tested scope**.
The preserved consecutive-event observations contain multiple deterministic,
exactly recurring frame intervals. They can be represented quantitatively
without assigning beat, tactus, tempo, subdivision, meter or metric level.

This conclusion does not establish that every recurrent gap is scientifically
salient, that any candidate is a musical beat, or that the observed ratios form
a metric hierarchy.

## Risks and limitations

- Only exact consecutive gaps on the existing 512-sample frame grid were
  tested.
- Non-consecutive lag recurrence, phase persistence and local-window recurrence
  were not tested.
- No canonical support-strength thresholds exist.
- The full-mix separator duplicates one observation population across five
  placeholder source identities.
- EnsembleMetricEvent `beat_time` may be an average within the existing
  consensus window rather than an original event timestamp.
- Sparse tenor-sax evidence provides only two exact recurrent gaps under this
  protocol.

## Architectural impact assessment

The current architecture preserves enough temporal evidence to perform
experiment-local multi-candidate discovery. It does not currently preserve a
canonical candidate-period population as a scientific representation.

This experiment demonstrates a possible future representational need but does
not by itself approve an architecture or implementation. Any proposal must
preserve candidate multiplicity, source evidence, occurrence counts, temporal
scope and the distinction from metric interpretation.

## Smallest next objective

Perform a controlled candidate-relationship experiment over the already frozen
candidate populations, testing phase persistence and non-consecutive lag
recurrence before considering metric-level interpretation.
