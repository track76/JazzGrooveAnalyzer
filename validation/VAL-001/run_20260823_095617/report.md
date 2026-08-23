# H-VAL001-CALIBRATION-PAIRWISE-01

Status: **PASS — MIXED SOURCE-SPECIFIC OUTCOME**

The frozen pair authority was constructed by exact rational timestamp equality
before access to pairwise JGA quantities. It has fingerprint
`f5c424a3f8de3b35c60d2ae9e3f41527a93ed4f84f5d8cc992a837a2489f5b28`.

| Pair | Symbolic pairs | Valid JGA pairs | Unmatched symbolic | Ambiguous symbolic | Unresolved JGA |
|---|---:|---:|---:|---:|---:|
| Piano–Drums | 36 | 36 | 13 | 0 | 0 |
| Double Bass–Drums | 19 | 18 | 9 | 0 | 1 |
| Tenor Sax–Drums | 9 | 5 | 3 | 0 | 4 |

Piano–Drums and Double Bass–Drums satisfy the frozen
`NO_DETECTABLE_PAIRWISE_BIAS` rule and its temporal/sensitivity stability
requirements. Tenor Sax–Drums is `INSUFFICIENT_EVIDENCE` because only five
valid pairs remain and the sensitivity population contains one pair.

All 59 valid pairwise errors lie at integer frame offsets to within the exact
stored-timestamp residuals; residual magnitudes are no greater than
`6.0771e-12 ms`. This is descriptive frame-related structure and does not
establish its cause or authorize correction.

The absolute candidate component is compatible with cancellation under the
frozen pairwise criterion for Piano–Drums and Double Bass–Drums. Evidence for
Tenor Sax–Drums is partial because the frozen minimum support is not met.

Deterministic replay and the 10,000-resample frozen bootstrap reproduce
exactly. Raw observations are unchanged, Voice remains `DEFERRED`, and no
mathematical correction is authorized.

Scientific fingerprint:
`38740f74ab22c5c17b4400a6fac3823cbf4ead8650f77d6a5ab81e8ee7921b27`.
