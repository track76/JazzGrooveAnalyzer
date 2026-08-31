# CED-VAL-006 event-blind continuous pitched-Bass recovery test

## Decision

`EVENT_BLIND_PITCHED_BASS_RECOVERY: PARTIAL`

The continuous full-mix scanner autonomously recovered a substantial temporal subset of the frozen missed-Bass population with moderate bounded precision. It did not meet the preregistered `USEFUL` false-burden and pitch-compatibility requirements.

## Preregistration and ordering evidence

- Protocol: `H-CEDVAL006-EVENT-BLIND-CONTINUOUS-PITCHED-BASS-RECOVERY-01`.
- Protocol fingerprint: `eda2bbe72c7a870e00c3d0d1ec5b90e100c29d93bf0d81d33a4141de729c9672`.
- Preregistration commit: `b8743e2`.
- Controlled mix SHA-256: `32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0`.
- Candidate scanner CLI accepted only mix path, expected checksum, and output path. It had no authority path or interface for Bass, Demucs, Kick, Drum, or metric evidence.
- Both complete blind scans were byte-identical, then locked in commit `45493e3` before evaluation code was executed against the frozen Bass authorities.
- Candidate stream SHA-256: `879411caa2be9b9c5d37f5f2b0e057884c10ba692864c262c5dc3bffcd3e26c8`.
- Candidate fingerprint: `cc268f0dc517a92f2dc27ed68e300ad6e3d1f58381adebcb673a16a88041ccdb`.

## Frozen continuous method

The 48 kHz stereo mix was averaged to mono and deterministically resampled to the transferred 44.1 kHz analysis rate. The CED-VAL-005 method remained E1–G3, 5-cent F0 grid, eight partials, >=3 partials at >=6 dB local prominence, harmonic-energy ratio >=0.12, missing-fundamental support, 4,096-sample Hann frames, 1,024-sample hop, and 16,384-point FFT.

Eligible frames were linked across no more than two intervening ineligible frames while F0 changed by no more than 70 cents. Activation required three consecutive stable frames spanning no more than 35 cents. The timestamp was the first frame start of the earliest qualifying triple. A >70-cent change terminated a track. Events under 120 ms apart were deterministically suppressed by persistence, score, then time. No note or event was forced.

The scan processed 10,685 frames: 6,235 eligible and 4,450 ineligible. It formed 593 candidates. Candidate-duration median was 185.76 ms (Q1 162.54, Q3 232.20; range 139.32–1,230.66 ms).

## Temporal evaluation

Frozen one-to-one matching used a +/-50 ms tolerance with global edge ordering by absolute displacement and deterministic tie breaks.

- Original Bass observations: 1,055.
- Frozen htdemucs_ft recovered: 619.
- Frozen htdemucs_ft missed: 436.
- Blind scanner candidates: 593.
- Candidates matched to any original Bass: 330.
- Matches to already-recovered Bass: 203.
- `NEWLY_RECOVERED_MISSED_BASS`: 127.
- Unmatched candidates: 263.
- Candidate precision: 0.556492 (55.65%); Wilson 95% CI 51.63–59.60%.
- Recall on frozen missed population: 0.291284 (29.13%); Wilson 95% CI 25.06–33.56%.
- Incremental all-original coverage: 127/1,055 = 0.120379 (12.04 percentage points).
- Retrospective combined recall: (619+127)/1,055 = 0.707109 (70.71%), versus frozen baseline 58.67%.
- Scanner-only all-original recall: 330/1,055 = 0.312796.
- Scanner-only F1 against bounded original-Bass authority: 0.400485.
- Omnibus false-candidate burden: 263 unmatched; 2.07087 unmatched candidates per newly recovered missed event.

Absolute timing displacement was median 21.44 ms, Q1 9.90 ms, Q3 34.68 ms, RMSE 26.54 ms, and maximum 49.78 ms. Median signed displacement was -0.69 ms. These are observation-to-observation displacements, not physical-onset errors.

## Independent pitch validation

Pitch validation remained separate from temporal matching. The fixed transferred +40 to +300 ms method was applied to the original Bass microphone only after candidate locking, with agreement <=50 cents and no octave folding.

- Newly recovered missed matches: 127.
- Pitch-evaluable missed matches: 104/127 (81.89%).
- Pitch-compatible missed matches: 41/104 (39.42%); Wilson 95% CI 30.57–49.03%.
- Compatible missed-match error: median 5 cents, Q1 0, Q3 15, RMSE 13.00 cents.
- Already-recovered matches: 188/203 evaluable; 86/188 compatible (45.74%).
- All temporal matches: 292/330 evaluable; 127/292 compatible (43.49%).

A temporal match does not imply pitch correctness. Pitch compatibility does not uniquely attribute the mixed energy to Double Bass.

## Gate audit

The `PARTIAL` gate passed: missed recall 29.13% >=5%; precision 55.65% >=15%; unmatched/new ratio 2.071 <=5; median timing 21.44 ms <=40 ms; pitch evaluability 81.89% >=50%; pitch compatibility 39.42% >=25%.

The `USEFUL` gate failed despite recall, precision, and timing passing. The unmatched/new ratio exceeded its <=2 limit (`2.071`), and pitch compatibility was below its >=50% requirement (`39.42%`). No threshold was changed after evaluation.

## Specificity and limitations

The 263 unmatched candidates are the preregistered omnibus burden from other pitched instruments, ensemble harmony, bleed, sustained material, estimator ambiguity, and any Bass-like evidence outside the bounded original EME authority. No source was removed. Some unmatched candidates may reflect real sound not represented by original Bass EME, so they are evaluation-unmatched rather than proven acoustic false positives.

The original Bass authority is a JGA observation authority, not physical-onset Ground Truth. The isolated Bass microphone and estimator provide a pitch proxy, not symbolic notes. No unique source attribution, complete transcription, causal masking, groove/swing, beat/meter, production-readiness, or authorized JGA union claim follows.

SciPy warned that it skipped an unrecognized non-data WAV metadata chunk while decoding the original Bass authority. PCM evaluation completed without truncation or event failure.

## Reproducibility

- Candidate replay: `BYTE_IDENTICAL`.
- Evaluation replay: `BYTE_IDENTICAL`.
- Evaluation JSON SHA-256: `a5ff33f95e5e1f67d7ac01a70137c8c294cc4ffcada65cf3df09ecb12a9d6889`.
- Scientific result fingerprint: `6cbcf9e29629ba2322d554382de6be11e2c746122f1b3beb28db61ad7835f4ce`.
- JGA modification: none.
- Push: not performed.

Exactly one recommended next experiment requiring PI approval: in an isolated retrospective CED-VAL-006 evaluation, add only independently signal-grounded, temporally matched blind candidates to a copy of the frozen Bass observation population and test whether the resulting `RhythmSectionTimingProfile` preserves or improves AD-037/AD-038/AD-040 coverage without materially shifting Bass timing-displacement and relationship distributions; do not alter JGA or construct a production selector.
