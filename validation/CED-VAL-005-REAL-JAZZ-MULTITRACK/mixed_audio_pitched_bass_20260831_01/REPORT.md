# CED-VAL-005 mixed-audio pitched Bass evidence study

## Authority and preregistration

- Protocol: `H-CEDVAL005-MIXED-AUDIO-PITCHED-BASS-EVIDENCE-01`.
- Protocol fingerprint: `12a5f79ca02165752b711c25a9e4966a5b2da187b63b11d71aaced01934bf5ba`.
- Preregistration commit: `d76e99e`.
- Controlled mix SHA-256: `7d9d3f1f07f7760152ce560ae0bbb6f1706b443278a41af4a31dfb2638396a0f`.
- BassDI evaluation authority SHA-256: `2c4c06b9b5d4b18e00000bc2c036207fc68fb722c5854e0a30107ad4594a910b`.
- Frozen correspondence: 1,138 BassDI EME; 782 recovered and 356 missed.

The mix-only candidate stage was executed twice without opening BassDI. Both files are byte-identical (SHA-256 `6cd9ef10fb3444cc56d1b2bc27c6e1c24d9997b35365734c234141653f01e6a7`) and were locked in commit `2455274` before evaluation. Candidate fingerprint: `a9ba6a830dc347ecc6d7cb8943ae7d89f2533dd6919d16fe3a59f31a7d079db0`.

## Frozen signal method

At every frozen EME timestamp the candidate stage examined only the controlled mix from +40 to +300 ms. It used 4,096-sample periodic-Hann frames, 1,024-sample hop, 16,384-point FFT, and an E1–G3 (41.2034–195.998 Hz) F0 grid at 5-cent spacing. Scores combined up to eight harmonics, local spectral-noise prominence, harmonic-band energy, missing-fundamental support, three-frame pitch stability, and persistence across at least half the frames. Outputs could be present, absent, or indeterminate; no event was forced to a note. Nearest-note mapping used A4=440 Hz and retained signed cents deviation.

Only after candidate locking was the identical fixed analysis applied to BassDI as an independent pitch proxy. Agreement required at least one frozen mix/reference candidate pair within 50 cents, without octave folding. BassDI is an isolated microphone observation and estimator-derived pitch proxy, not symbolic-note or physical-onset Ground Truth.

## Primary missed-Bass result

Of 356 `MISSED_BASS` observations:

- mix evidence present: 239; absent: 9; indeterminate: 108;
- BassDI reference evaluable: 334/356 (93.82%);
- compatible mixed-audio evidence: 69/334 evaluable (20.6587%); Wilson 95% CI 16.6623–25.3223%;
- conservative all-missed denominator: 69/356 (19.3820%);
- among mix-present missed events: 69/239 (28.8703%) were independently compatible;
- compatible-event pitch error: median 10 cents, Q1 5, Q3 25, RMSE 19.07 cents.

This meets the preregistered `PARTIAL` gate (evaluability at least 80%, compatible proportion at least 20%, Wilson lower bound at least 10%) and does not meet `STRONG`.

## Recovered-Bass control

Of 782 `RECOVERED_BASS` observations:

- mix evidence present: 519; absent: 13; indeterminate: 250;
- BassDI reference evaluable: 761/782 (97.31%);
- compatible mixed-audio evidence: 127/761 evaluable (16.6886%); Wilson 95% CI 14.2080–19.5037%;
- all-recovered denominator: 127/782 (16.2404%);
- compatible-event pitch error: median 10 cents, Q1 5, Q3 25, RMSE 19.07 cents.

The missed-compatible proportion is descriptively 3.97 percentage points above the recovered control. This was not a preregistered superiority test and supports no causal claim.

## Descriptive Kick subdivisions

- `MISSED_BASS_WITH_KICK`: 31 total; 28 evaluable; 4 compatible (14.29% of evaluable; Wilson 95% CI 5.70–31.49%); mix present/absent/indeterminate 20/0/11.
- `MISSED_BASS_WITHOUT_KICK`: 325 total; 306 evaluable; 65 compatible (21.24%; Wilson 95% CI 17.03–26.17%); mix present/absent/indeterminate 219/9/97.
- `RECOVERED_BASS_WITH_KICK`: 139 total; 131 evaluable; 25 compatible (19.08%; Wilson 95% CI 13.27–26.66%).
- `RECOVERED_BASS_WITHOUT_KICK`: 643 total; 630 evaluable; 102 compatible (16.19%; Wilson 95% CI 13.52–19.27%).

Kick labels were never inputs to pitch generation. The small missed-with-Kick population gives wide uncertainty and does not support masking or causal interpretation.

## Interpretation and limitations

The result establishes a bounded, practically relevant subset: 69 frozen missed Bass observations had a signal-derived pitched candidate in the full mix compatible with the independently estimated BassDI pitch. It does not establish that the candidate energy originated uniquely from Bass: piano, saxophone, bleed, coincident harmony, and estimator octave/harmonic ambiguity can create compatible evidence. The fixed estimator also marked 358/1,138 events indeterminate and does not estimate physical onsets. No complete transcription, causal masking, groove/swing, or production-readiness claim is authorized.

The SciPy reader emitted `WavFileWarning: Chunk (non-data) not understood, skipping it` for BassDI metadata; PCM decoding and both deterministic evaluations completed without event failures or truncation.

## Reproducibility and decision

- Candidate replay: `BYTE_IDENTICAL`.
- Evaluation replay: `BYTE_IDENTICAL`.
- Result JSON SHA-256: `6a9eeb21a75a5e0c68c09b316dd1a5bf65f64341d952a5dcb6ad87784e3fcb24`.
- Scientific result fingerprint: `8a1fd4dc0364d4f399e81778cf493e524079e83fc555f2723652a0c5127f0d41`.
- Classification: `MIXED_AUDIO_PITCHED_BASS_EVIDENCE: PARTIAL`.

Exactly one recommended next experiment requiring PI approval: on independent CED-VAL-006, freeze an event-blind continuous mixed-audio candidate scan derived from this signal-only method, then determine whether its candidates add one-to-one matches to the frozen missed-Bass population at an acceptable false-candidate burden before considering any contribution to `RhythmSectionTimingProfile`.

JGA was not modified. No detector or recovery path was implemented. Nothing was pushed.
