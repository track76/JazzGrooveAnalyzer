# CED-VAL-006 blind-candidate Piano contamination audit

## Decision

`PIANO_CONTAMINATION: HIGH`

The primary 127 newly recovered candidates contained extensive signal support at their frozen F0s in the isolated Rhodes/electric-piano track. This is retrospective source-consistency evidence, not proof that Rhodes caused any mixed-audio candidate.

## Authorities and method

- Protocol: `H-CEDVAL006-BLIND-CANDIDATE-PIANO-CONTAMINATION-AUDIT-01`.
- Protocol fingerprint: `61e568108ea6dceb179932fd6abf0a0da0e85d0714241a27b5014a23d015a894`.
- Frozen 593-candidate SHA-256: `879411caa2be9b9c5d37f5f2b0e057884c10ba692864c262c5dc3bffcd3e26c8`.
- Frozen candidate fingerprint: `cc268f0dc517a92f2dc27ed68e300ad6e3d1f58381adebcb673a16a88041ccdb`.
- Frozen group/evaluation SHA-256: `a5ff33f95e5e1f67d7ac01a70137c8c294cc4ffcada65cf3df09ecb12a9d6889`.
- Bass authority: original `BASS - DI.wav`, SHA-256 `c0a99f65158d12a69e062cc990e86631a0d29d7e83f30537d34eb301516855a9`.
- Piano-family authority: sole isolated keyboard track `Rhodes MTP 440.wav`, SHA-256 `ffe3b202c7fc2f3349832b7095ba21a331306f5056a94f5382b72d0fa5dc4e6e`.

The result is specifically an audit of Rhodes/electric-piano support. No acoustic-piano track exists in the supplied source population. Room microphones were not combined with Rhodes, and the Bass microphone was not combined with BassDI.

At each unchanged candidate timestamp, duration, and frozen F0 set, both isolated sources were tested with the preregistered eight-harmonic, +/-35-cent, local-prominence, harmonic-energy, and persistence rules. No new source-specific F0 was estimated. A source required at least three consecutive supported frames and support in at least half its valid frames. The five classes were determined solely from the two resulting support flags.

## All 593 candidates

- `BASS_DOMINANT_SUPPORT`: 62 (10.46%; Wilson 95% CI 8.24–13.18%).
- `PIANO_DOMINANT_SUPPORT`: 265 (44.69%; 40.73–48.71%).
- `BOTH_SUPPORTED`: 218 (36.76%; 32.98–40.72%).
- `NEITHER_SUPPORTED`: 48 (8.09%; 6.16–10.57%).
- `INDETERMINATE`: 0 (0%; upper 95% bound 0.64%).
- `ANY_PIANO_SUPPORT`: 483/593 (81.45%; 78.12–84.37%).
- `ANY_BASS_SUPPORT`: 280/593 (47.22%; 43.23–51.24%).

## A — 127 newly recovered missed-Bass candidates

- `BASS_DOMINANT_SUPPORT`: 8 (6.30%; 3.23–11.94%).
- `PIANO_DOMINANT_SUPPORT`: 59 (46.46%; 38.01–55.11%).
- `BOTH_SUPPORTED`: 49 (38.58%; 30.57–47.27%).
- `NEITHER_SUPPORTED`: 11 (8.66%; 4.91–14.85%).
- `INDETERMINATE`: 0.
- `ANY_PIANO_SUPPORT`: 108/127 (85.04%; 77.81–90.21%).
- `ANY_BASS_SUPPORT`: 57/127 (44.88%; 36.51–53.56%).

The preregistered bounded filtering quantity is 59–108 of 127: 59 Rhodes-only candidates are the lower bound and all 108 with any Rhodes support are the upper bound on candidates that may require source-specific filtering. This range is not a revised recovery count and does not prove contamination.

## B — 263 candidates unmatched to original Bass

- `BASS_DOMINANT_SUPPORT`: 21 (7.98%; 5.28–11.90%).
- `PIANO_DOMINANT_SUPPORT`: 132 (50.19%; 44.19–56.19%).
- `BOTH_SUPPORTED`: 86 (32.70%; 27.31–38.58%).
- `NEITHER_SUPPORTED`: 24 (9.13%; 6.21–13.22%).
- `INDETERMINATE`: 0.
- `ANY_PIANO_SUPPORT`: 218/263 (82.89%; 77.87–86.96%).
- `ANY_BASS_SUPPORT`: 107/263 (40.68%; 34.92–46.71%).

Unmatched candidates are not automatically false positives. BassDI support outside the bounded original EME population and same-F0 simultaneous-source activity remain possible.

## C — 203 candidates matching already-recovered Bass

- `BASS_DOMINANT_SUPPORT`: 33 (16.26%; 11.82–21.95%).
- `PIANO_DOMINANT_SUPPORT`: 74 (36.45%; 30.14–43.27%).
- `BOTH_SUPPORTED`: 83 (40.89%; 34.35–47.76%).
- `NEITHER_SUPPORTED`: 13 (6.40%; 3.78–10.65%).
- `INDETERMINATE`: 0.
- `ANY_PIANO_SUPPORT`: 157/203 (77.34%; 71.10–82.56%).
- `ANY_BASS_SUPPORT`: 116/203 (57.14%; 50.26–63.76%).

The high simultaneous Rhodes support even among already-recovered Bass matches demonstrates why temporal coincidence or pitch agreement alone cannot provide unique attribution.

## Gate audit and interpretation

For the primary 127, indeterminate evidence was 0%. `LOW` required Piano-dominant <=10%, any-Piano <=25%, and any-Bass >=50%; the observed values were 46.46%, 85.04%, and 44.88%. `HIGH` was triggered independently by Piano-dominant >=30% and any-Piano >=60%. No threshold changed after inspection.

The previous 127 newly recovered observations and 70.71% retrospective combined-coverage quantity remain frozen and unaltered. This audit shows that much of that apparent increment lacks Bass-specific support under this bounded two-source test and may require a future independently preregistered source-specific filter before any RhythmSectionTimingProfile experiment. No filter was designed or applied.

Acquisition authority remains partial: identical distributed file scope supports coordinate comparison, but shared hardware clock and exact common session origin are unestablished. Close-microphone bleed, simultaneous notes, source dynamics, and spectral overlap can yield support in both isolated tracks. Bass-supported is not synonymous with a true Bass event; Rhodes-supported is not synonymous with contamination or unique physical source identity.

SciPy skipped an unrecognized non-data WAV metadata chunk during source decoding. PCM analysis completed without truncation or candidate failure.

## Reproducibility

- Preregistration commit: `8794221`.
- Attribution replay: `BYTE_IDENTICAL`.
- Result JSON SHA-256: `bd8d5f788127ae2f84666214a2e28ab7f393d73d294738fa7f40f22b77acc38c`.
- Scientific result fingerprint: `887f14f2d489653cce2465b32a97afa4889fc2009746662ede2150f832617f5c`.
- JGA modification: none.
- Previous experiment modification: none.
- Push: not performed.
