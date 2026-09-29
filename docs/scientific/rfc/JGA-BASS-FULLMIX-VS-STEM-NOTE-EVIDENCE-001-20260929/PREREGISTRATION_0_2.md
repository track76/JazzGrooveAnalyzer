# Preregistration 0.2 — as-fixed record
## JGA-BASS-FULLMIX-VS-STEM-NOTE-EVIDENCE-001-20260929

This file records the parameters actually used. It is written *after* execution and is a
record of the fixed configuration, not a prospective commitment. Nothing here was selected
in response to results.

## Hypothesis
H1: bass note candidates detected in the isolated bass stem and in the full mix correspond
within fixed temporal tolerances.
H0: no such correspondence beyond chance coincidence at the same density.

## Inputs (frozen, SHA-256)
- full mix: `c890658d8c8f67e0d295d7ab334712227c2c2c999283a1fdb5cf32e6af7a467f`
- bass stem: `8ca185528ce4c50f7a318fb21e9e49ee68b76c7fbede9e7dace5b61120c46952`
- sample rate 44100 Hz; total 15,338,496 frames (347.811755 s)
- evaluation interval: native `[2107392, 3643392)` = 47.786667–82.616599 s (34.829932 s)
- processing guard: native `[2062268, 3688516)`, 1,626,248 samples, 3177 STFT frames
- timestamp mapping: `native_sample = 2062268 + frame_index*512`, no correction

## Extractor (identical code both arms; 21-key frozen block)
frozen block SHA-256 `a0dd5fcbfc15d9d7086cc6b7135806725069e17f44f29309a7f4ecc1bc6b9663`
- STFT n_fft 2048, hop 512
- pYIN: fmin 41.2, fmax 350.0, frame 2048, hop 512, resolution 0.1, n_thresholds 100,
  boltzmann 2.0, max_transition_rate 35.92, switch 0.01, no_trough 0.01
- flux peak picking with prominence/iqr/std from the entire processing context
- dedup spacing 80 ms; cluster span 120 ms
- states: BASS_COMPATIBLE, BASS_POSSIBLE, AMBIGUOUS, UNRESOLVED

## Matching
- tolerance families T0=0, T1=512, T2=1024, T4=2048 samples (primary)
- connected components over all candidate events
- **no** nearest-neighbour selection, **no** one-to-one assignment, **no** pitch threshold,
  **no** cent acceptance rule, **no** candidate deletion
- every event is retained, matched or not, in every family

## Reporting
- population A: ALL_F0_BOTH_VALID (finite F0 on both sides)
- population B: VALIDITY_QUALIFIED, using the fixed reporting boundary 43.06640625 Hz
- the boundary is a reporting descriptor only; it never accepts or rejects a pair
- quantiles: PREREGISTERED_ROUNDED_INDEX_QUANTILE, defined exactly as
  `index = round(f * (n - 1))` applied to the sorted population, clamped to [0, n-1].
  This is a preregistered formula, NOT the conventional nearest-rank order statistic, and
  is never to be recomputed or described as nearest-rank.

## Prohibited
PLP, Global, quarter files, Method P/D, human annotation, tuning, timestamp correction,
cherry-picking, and any claim of verified notes, Ground Truth, independent confirmation,
accuracy, STEM_BETTER or FULLMIX_BETTER.
