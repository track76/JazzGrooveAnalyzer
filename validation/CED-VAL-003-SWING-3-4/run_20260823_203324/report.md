# H-CEDVAL003-CALIBRATION-ZERO-01 Result

Status: **PASS — FROZEN EXECUTION RESULT**

Dataset authority `PR-CED-VAL-003-SWING-3-4-001`, fingerprint `9345f592…`,
preregistration commit `6a373b9` and every asset checksum passed before
comparison. Exact-rational symbolic authority contains 155 Drum, 100 Double
Bass and 57 Piano events; fingerprint `3d97ff352fa0ca3ca5317d1584ec57b62eec368cd3595529f4659321e8a0bda0`.

## Absolute calibration

All statistics are milliseconds and describe combined controlled-rendering
and JGA measurement behaviour.

| Source | Symbolic / observed / valid | Unmatched symbolic / observed | Ambiguous multiple / boundary | Signed min / Q1 / median / Q3 / max | Signed mean / population SD | Absolute min / Q1 / median / Q3 / max | Absolute mean / population SD |
|---|---:|---:|---:|---|---|---|---|
| Drums | 155 / 155 / 47 | 54 / 0 | 54 / 0 | 34.829932 / 81.587302 / 84.625850 / 87.755102 / 96.643991 | 83.649346 / 9.097055 | 34.829932 / 81.587302 / 84.625850 / 87.755102 / 96.643991 | 83.649346 / 9.097055 |
| Double Bass | 100 / 100 / 96 | 2 / 0 | 2 / 0 | 25.963719 / 62.380952 / 68.163265 / 71.768707 / 79.183673 | 63.161376 / 13.293104 | 25.963719 / 62.380952 / 68.163265 / 71.768707 / 79.183673 | 63.161376 / 13.293104 |
| Piano | 57 / 50 / 50 | 7 / 0 | 0 / 0 | 6.462585 / 25.691610 / 37.800454 / 61.020408 / 74.829932 | 41.936508 / 19.267976 | 6.462585 / 25.691610 / 37.800454 / 61.020408 / 74.829932 | 41.936508 / 19.267976 |

Frozen full/first-half/second-half primary median bootstrap intervals are:

- Drums: `[82.630385, 86.258503]`, `[83.356009, 87.346939]`,
  `[80.770975, 86.439909]`. Primary evidence passes, but ambiguity sensitivity
  retains only one/zero records across partitions; frozen classification:
  `INSUFFICIENT_EVIDENCE`.
- Double Bass: `[66.213152, 70.113379]`, `[64.263039, 69.071429]`,
  `[68.480726, 71.700680]`; stable `CANDIDATE_SYSTEMATIC_BIAS`.
- Piano: `[30.680272, 48.537415]`, `[31.814059, 60.272109]`,
  `[21.247166, 50.430839]`; stable `CANDIDATE_SYSTEMATIC_BIAS`.

The frozen overall absolute outcome is `SOURCE_SPECIFIC_CANDIDATE_BIAS`.
Absolute frame offsets span 1 through 8. No absolute error is an exact frame
multiple; residuals span -5.804989 to +5.736961 ms. The frozen measurement
structure outcome is `MIXED_MEASUREMENT_BEHAVIOUR`.

## Pairwise calibration

Pair authority fingerprint is
`9e29b12eec72d6a121868bdfe8e5a29808b70d69c184233c2c1f919ff253eaf5`.
It comes solely from exact rational symbolic timestamp equality; AD-038
geometry was not used.

| Pair | Symbolic / valid-symbolic / valid-JGA | Unmatched-symbolic / unresolved-JGA / ambiguous | Signed min / Q1 / median / Q3 / max | Signed mean / population SD | Absolute min / Q1 / median / Q3 / max | Full median 95% interval | Classification |
|---|---:|---:|---|---|---|---|---|
| Piano–Drums | 57 / 21 / 12 | 36 / 9 / 0 | -46.439909 / -23.219955 / -11.609977 / -11.609977 / 0 | -15.479970 / 11.928118 | 0 / 11.609977 / 11.609977 / 23.219955 / 46.439909 | `[-23.219955, -11.609977]` | `INSUFFICIENT_EVIDENCE` |
| Double Bass–Drums | 100 / 78 / 32 | 22 / 46 / 0 | -23.219955 / -23.219955 / -11.609977 / -11.609977 / 11.609977 | -13.786848 / 7.364275 | 0 / 11.609977 / 11.609977 / 23.219955 / 23.219955 | `[-11.609977, -11.609977]` | `INSUFFICIENT_EVIDENCE` |

Both primary populations meet overall/partition support, but ambiguity
sensitivity retains only one valid pair and none in the second partition.
Consequently neither pair may receive a bias classification. Pair residuals
are within approximately `±0.000000000006 ms` of integer frame multiples;
this is descriptive structure only.

## Post-freeze descriptive comparison

CED-VAL-001 reported source-independent candidate absolute bias and no
detectable Piano–Drums or Double Bass–Drums pairwise bias. CED-VAL-002 reported
source-specific candidate absolute bias and candidate bias for both pairs.
This independently frozen CED-VAL-003 result reports source-specific candidate
absolute bias, while both pairwise classifications are insufficient after the
frozen ambiguity-sensitivity gate. This comparison is descriptive only and did
not alter inputs, criteria, calculations or classifications.

Two complete executions produced scientifically identical symbolic, observed,
correspondence, pair, statistical and classification content. Independent
arithmetic verification passed for 305 observed EME, 193 valid absolute
correspondences and 44 valid JGA pairs. The deterministic 10,000-resample
bootstrap completed for every applicable frozen label.

Raw observations remain unchanged, no correction is authorized, and H02 was
not executed or inspected. Full-suite result under non-GUI Matplotlib was
1087 passed / 1 known environment-dependent external-storage failure.

Scientific fingerprint:
`589ee3c15783556bd0e5b7b6df53822dff56c1eddfb6d17476aa3152adef5270`.
