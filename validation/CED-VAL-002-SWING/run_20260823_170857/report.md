# H-CEDVAL002-CALIBRATION-ZERO-01 Result

Status: **PASS — FROZEN EXECUTION RESULT**

Dataset authority `PR-CED-VAL-002-SWING-002` and every corrected asset checksum
passed before symbolic or observed-event comparison. Deterministic symbolic
authority contains 192 Drum, 127 Double Bass and 64 Piano events; its
fingerprint is `7fb4e7f3cbe8ecfa93fcfd9774256219daba2c4c1c70d07e04d913cb5e779642`.

## Absolute calibration

All quantities are milliseconds and describe combined controlled-rendering and
JGA measurement behaviour.

| Source | Symbolic / observed / valid | Unmatched symbolic / observed | Ambiguous multiple / boundary | Signed min / Q1 / median / Q3 / max | Signed mean / population SD | Absolute min / Q1 / median / Q3 / max | Absolute mean / population SD |
|---|---:|---:|---:|---|---|---|---|
| Drums | 192 / 192 / 188 | 2 / 0 | 2 / 0 | 7.256236 / 32.970522 / 37.551020 / 88.616780 / 98.412698 | 53.824963 / 27.548496 | 7.256236 / 32.970522 / 37.551020 / 88.616780 / 98.412698 | 53.824963 / 27.548496 |
| Double Bass | 127 / 127 / 127 | 0 / 0 | 0 / 0 | -1.224490 / 14.875283 / 17.959184 / 20.861678 / 34.829932 | 17.539582 / 5.313897 | 0.680272 / 14.875283 / 17.959184 / 20.861678 / 34.829932 | 17.569578 / 5.213862 |
| Piano | 64 / 63 / 63 | 1 / 0 | 0 / 0 | -14.285714 / -8.299320 / 2.040816 / 18.321995 / 34.829932 | 5.267970 / 14.100388 | 0.589569 / 6.167800 / 11.746032 / 18.321995 / 34.829932 | 12.743044 / 8.011696 |

Frozen full/first-half/second-half bootstrap median intervals are respectively:

- Drums: `[36.281179, 38.730159]`, `[36.281179, 39.727891]`,
  `[35.192744, 39.183673]`; stable candidate systematic bias.
- Double Bass: `[16.689342, 18.866213]`, `[16.235828, 19.047619]`,
  `[16.642574, 19.773243]`; stable candidate systematic bias.
- Piano: `[-3.764172, 11.791383]`, `[-6.848073, 12.380952]`,
  `[-3.401361, 17.414966]`; no detectable systematic bias.

The frozen overall absolute outcome is `SOURCE_SPECIFIC_CANDIDATE_BIAS`.
Frame offsets span -1 through 8. No absolute error is an exact frame multiple;
residuals span -5.804989 to +5.804989 ms. The combined systematic, framewise
and residual evidence is `MIXED_MEASUREMENT_BEHAVIOUR`.

## Pairwise calibration

Pair authority comes only from exact rational symbolic timestamp equality.
AD-038 nearest geometry was not used.

| Pair | Symbolic / valid | Unmatched symbolic / unresolved / ambiguous | Signed min / Q1 / median / Q3 / max | Signed mean / population SD | Absolute min / Q1 / median / Q3 / max | Full median 95% interval | Classification |
|---|---:|---:|---|---|---|---|---|
| Piano–Drums | 64 / 24 | 38 / 2 / 0 | -34.829932 / -23.219955 / -11.609977 / -11.609977 / 11.609977 | -13.544974 / 9.866583 | 0 / 11.609977 / 11.609977 / 23.219955 / 34.829932 | `[-23.219955, -11.609977]` | `CANDIDATE_PAIRWISE_BIAS` |
| Double Bass–Drums | 127 / 118 | 7 / 2 / 0 | -23.219955 / -23.219955 / -11.609977 / -11.609977 / 11.609977 | -15.545563 / 6.796723 | 0 / 11.609977 / 11.609977 / 23.219955 / 23.219955 | `[-11.609977, -11.609977]` | `CANDIDATE_PAIRWISE_BIAS` |

Both classifications satisfy full, fixed-half, sensitivity, minimum-support,
sign, overlap, provenance and replay requirements. Pair residuals are within
approximately `±0.000000000007 ms` of integer frame multiples; this is
descriptive structure, not a correction authorization.

## Post-freeze descriptive comparison

CED-VAL-001 reported source-independent candidate absolute bias and no
detectable Piano–Drums or Double Bass–Drums pairwise bias. This independently
frozen render instead reports source-specific candidate absolute bias and
candidate pairwise bias for both evaluated pairs. The difference is descriptive
across distinct controlled datasets and does not transfer, retune or authorize
any numerical correction.

Two complete executions produced byte-identical input, event, pair, scientific
content and result artifacts. Independent arithmetic verification passed for
382 observed EME, 378 valid absolute correspondences and 142 valid pairs.
Raw observations are unchanged, no correction is authorized, and H02 was not
executed or inspected.

Scientific fingerprint:
`d4b0b18766cf2c69a367014704f2c2dc4429d977cdf8ddd27d767276b603d4e7`.
