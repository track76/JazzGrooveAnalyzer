# CED-VAL-005 original-channel synchronization check

PI-authorized bounded original-audio verification, 2026-09-10. **Practical distributed-file alignment is supported; identical sample-level physical origin and a unique fixed offset remain unestablished. No correction was applied.**

PI observational evidence: the PI independently imported original overhead and Hi-Hat files at the same Ableton timeline position and found shared transient structures, including large terminal transients, visually aligned with no apparent offset. This observation is preserved independently of the measurements below.

Inputs: original `05_HiHat.wav` and stereo `09_Overheads.wav` under `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/`. SHA-256 respectively `0e0801cf3d57c06b524aea3e497520f79afe0e7b10401e4cb6f46654ce227253` and `0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`, verified before execution. Both have 10,068,072 frames, 44,100 Hz, PCM24, equal duration 228.30095238 s. Both Broadcast WAV `bext` headers declare **TimeReference = 0 samples**. Thus the same declared file time origin is verified, although a zero metadata field alone does not prove physical acquisition synchronization. WAV chunk inventories are preserved; no inferred event labels or model predictions were loaded.

## One predeclared test

Protocol/implementation were frozen before measurements. Nine five-second windows were selected without content search: starts 0,30,60,90,120,150,180,210 s and the last five seconds (223.30095238 s). Compare Hi-Hat independently with each overhead channel. Measure demeaned raw-waveform overlap-normalized cross-correlation at integer sample lags in +/-2 s; select absolute correlation to allow polarity differences. Also measure a 10-ms moving mean-square energy envelope, as an auxiliary broad-transient alignment diagnostic, not exact onset authority. A +/-10-ms diagnostic neighborhood is preserved without substituting its maxima for the full-search results. A synthetic 37-sample delay fixture verified lag sign and indexing. Positive lag means overhead later than Hi-Hat. These are cross-channel similarity lags, not periodicity measurements.

No waveform was shifted, no event classified, no period/BPM/metric quantity computed, and no input overwritten. The window grid and lag bounds are operational choices, not statistical thresholds. No waveform feature can by itself distinguish microphone propagation from export delay without independent capture information.

## Observed result

| Window start (s) | Raw full-search peak, OH1 (samples) | Raw full-search peak, OH2 (samples) |
|---|---:|---:|
| 0 | +143 | +76 |
| 30 | +17 | +12 |
| 60 | -131 | +83 |
| 90 | +15 | +85 |
| 120 | +16 | +13 |
| 150 | +22 | +83 |
| 180 | +156 | -6 |
| 210 | -219 | +82 |
| 223.30095238 | +79917 | +11599 |

All 16 raw full-search peaks in the eight windows through 210 s are within -219 to +156 samples (approximately -4.966 to +3.537 ms). Their absolute correlation coefficients range approximately 0.061–0.351. These low/moderate coefficients and varying signs/lags reflect different microphone mixtures; they do not establish a sample-exact common origin or a constant delay. No drift fit or sample-rate correction is justified from them.

The terminal five-second window is ambiguous: raw full-search maxima are +1.812 s and +0.263 s, while its energy-envelope zero-lag correlations are high (0.906 and 0.866). Energy full-search maxima occur at -74.99 and +87.64 ms; they differ between overhead channels and do not identify a unique terminal offset. Elsewhere the envelope can favor distant unrelated structure (up to approximately 1.94 s), so an envelope peak must not be silently treated as a true delay. All contrary/ambiguous results are preserved, not excluded.

Together with the PI observation, the numerous near-zero raw maxima support **practical alignment on the distributed-file timeline**. The results do not support imposing one fixed file shift. **Fixed export offset: INDETERMINATE, no correction estimated. Exact sample-zero physical synchronization: NOT ESTABLISHED.** Equal file scope is observed; identical hardware clock, simultaneous capture and absence of editing are not proven. Millisecond-scale microphone/propagation/content-dependent delays remain possible. The near-zero lag range is observed diagnostic variation, not a confidence interval on export offset.

## Consequence for the preserved cross-source result

No Vogl or timestamp experiment was rerun. The [cross-source result](../CEDVAL005_CROSS_SOURCE_20260910/REPORT.md) remains byte-preserved: 4,089 labelled pairs, 530 repeated signed relations, 17 common within-source separations, no unique common reference and sparse Ride coverage in two regions. The new check reduces concern about gross file misplacement, and supports treating its offsets as practically co-timed distributed-file observations. It does not establish sample-exact physical phase, model-latency equality, candidate correctness or resolve the competing temporal structures.

Thus the earlier synchronization limitation can be narrowed: **coarse practical alignment supported; exact physical/channel timing remains unverified**. Synchronization is not evidence that one relation is BeatReference. The cross-source conclusion remains INSUFFICIENT to select a common reference; no candidate is promoted or corrected. This is an additive interpretation, not a rewrite of accepted evidence. No further task was executed. Stop for PI review; no commit/push.

## Preservation

External package: `/Volumes/SSD Track/JGA/experiments/CEDVAL005-SYNC-20260910/` (original hashes, WAV metadata, pre-execution protocol, implementation, complete per-window results and checksums).

- `protocol.json` SHA-256 `3714bbf8af3fe5fd4491d30ebc5e68152725329cb18dbd9ef49cce450eb0d0b8`
- `run.py` SHA-256 `2f84ff24a9aabef7ef7603e9cd3a22325c273d43dface71846a15b3fdc674b14`
- `result.json` SHA-256 `b92104e80d416c110fb665bef50a88af0a99cc8531843609296142a9ae35d694`
- `SHA256.json` SHA-256 `41d7a932cd7397fec8b7de8483c08d633c2add1632fa7eebae0e1ffc8d3cb94f`
