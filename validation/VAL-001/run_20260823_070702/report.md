# H-VAL001-CALIBRATION-ZERO-01

Status: **PASS — SOURCE-INDEPENDENT CANDIDATE BIAS / MIXED MEASUREMENT BEHAVIOUR**

No mathematical correction is authorized.

## Authority and Population

The checksum-bound MusicXML produced sufficient frozen
`CalibrationSymbolicEvent` authority before JGA observations were accessed.
The authority contains Drums 63, Piano 49, Double Bass 28 and Tenor Sax 12
symbolic events. Voice remained `DEFERRED`.

| Source | Symbolic | Observed EME | Valid | Unmatched symbolic | Unmatched observed | Ambiguous multiple cells | Boundary ambiguity |
|---|---:|---:|---:|---:|---:|---:|---:|
| Drums | 63 | 63 | 63 | 0 | 0 | 0 | 0 |
| Piano | 49 | 49 | 49 | 0 | 0 | 0 | 0 |
| Double Bass | 28 | 27 | 27 | 1 | 0 | 0 | 0 |
| Tenor Sax | 12 | 16 | 8 | 0 | 0 | 4 | 0 |
| **Overall** | **152** | **155** | **147** | **1** | **0** | **4** | **0** |

All ambiguous EME remain preserved in the event-level artifact. No
correspondence tolerance, rematching or event suppression was applied.

## Signed Measurement Difference

All units are milliseconds. Signed error is `t_JGA - t_GT`.

| Source | N | Min | Q1 | Median | Q3 | Max | Mean | Population SD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Drums | 63 | 4.270 | 11.003 | 15.322 | 47.507 | 53.591 | 26.446 | 18.398 |
| Piano | 49 | 8.449 | 15.322 | 18.762 | 27.769 | 31.858 | 20.304 | 6.786 |
| Double Bass | 27 | 12.070 | 19.826 | 20.897 | 21.779 | 80.523 | 23.121 | 11.864 |
| Tenor Sax | 8 | 31.669 | 47.864 | 50.849 | 53.912 | 56.375 | 48.846 | 7.428 |
| **Overall** | **147** | **4.270** | **14.183** | **19.780** | **31.439** | **80.523** | **25.007** | **15.136** |

All valid errors are positive in this controlled record, so absolute-error
statistics equal the signed-error statistics numerically. This is an empirical
result, not a correction rule or causal attribution.

## Frame Offset and Residual

Overall frame-offset counts are:

| k | 0 | 1 | 2 | 3 | 4 | 5 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| Count | 2 | 52 | 50 | 11 | 25 | 6 | 1 |

No valid error is exactly a frame multiple. Overall frame residuals range from
−5.763 to +5.756 ms, with Q1 −3.394 ms, median −1.486 ms, Q3 +2.852 ms, mean
−0.425 ms and population SD 3.506 ms. Offsets concentrate at one and two
frames, while residuals span nearly the complete nearest-frame residual range.
The frozen descriptive conclusion is `PARTIAL` evidence of frame-related
structure and `MIXED_MEASUREMENT_BEHAVIOUR`, not quantization-dominated
measurement and not proof of quantization causation.

## Candidate Bias and Temporal Stability

Drums, Piano and Double Bass satisfy the frozen candidate systematic-bias
criterion, including event support, deterministic replay, non-zero full and
temporal-partition bootstrap intervals, consistent sign, interval overlap and
unchanged ambiguity-adjacency sensitivity conclusions. Tenor Sax does not
satisfy the support requirement: 8 valid events, with 4 in each partition;
after sensitivity exclusion only 2 remain.

The three qualifying sources have pairwise median-difference intervals that
include zero. Their pooled median is 19.222 ms with frozen 95% bootstrap
interval `[18.294, 20.708]` ms. The preregistered bias-evidence outcome is
`SOURCE_INDEPENDENT_CANDIDATE_BIAS`.

This is candidate combined rendering/measurement bias only. Fixed-render
evidence cannot separate rendering and detection contributions, and no
correction is authorized.

## Pairwise Descriptive Consequence

| Difference | Median difference (ms) | Frozen 95% bootstrap interval (ms) |
|---|---:|---:|
| Drums − Piano | −3.440 | [−6.593, 21.922] |
| Drums − Double Bass | −5.575 | [−8.268, 20.248] |
| Drums − Tenor Sax | −35.528 | [−39.893, −10.049] |
| Piano − Double Bass | −2.135 | [−3.719, 0.000] |
| Piano − Tenor Sax | −32.088 | [−35.808, −24.985] |
| Double Bass − Tenor Sax | −29.953 | [−33.623, −22.752] |

Tenor Sax does not independently qualify for candidate bias because its valid
support is insufficient. Pairwise differences involving it remain descriptive
combined measurement evidence and cannot authorize correction.

## Reproducibility and Firewall

Two complete executions reproduced symbolic identities, EME identities,
correspondence statuses and exact event-level quantities. Raw EME,
PulseCandidate, Drum-relative and prior validation artifacts were unchanged.
No declared tempo, meter or BeatReference input was supplied to or consumed by
the calibration calculation.

Scientific fingerprint:
`d9ff1dba90cdb8b96e0412d05dd10c8b972f9dd2c2194187addcff4d6bd2050f`.
