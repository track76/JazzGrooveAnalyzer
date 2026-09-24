# September-14 continuous Fishman repeatability and 120-event GT

**Decision: repeatability confirmed; expanded validation GT created.** No adjudication triggers were found. This is same-rater reproducibility of the Fishman observable landmark, not physical onset accuracy.

Both original Pass-2 exports were preserved byte-for-byte before parsing. The receipt matches the response SHA-256. Passes were joined by canonical event ID and restored via each independently randomized excerpt’s integer source-sample offset; presentation order was not used for matching.

## Repeatability — 24 audit events

| Metric | 24-event audit | Earlier 36-event pilot |
|---|---:|---:|
| Median signed ms | -0.201 | -0.012 |
| Mean signed ms | -0.230 | 0.037 |
| Median absolute ms | 0.297 | 0.257 |
| IQR signed ms | 0.398 | 0.508 |
| P95 absolute ms | 0.923 | 0.777 |
| Maximum absolute ms | 1.161 | 0.968 |
| Within ±2 / ±5 / ±10 / ±20 ms | 100% at each bound | 100% at each bound |
| Plausible intervals overlap | 24/24 (100%) | 36/36 (100%) |

Signed range: -1.161 to 0.478 ms. No uncertain/incomplete or disjoint-interval cases. The maximum is modestly larger than the previous pilot, while both studies remain entirely inside ±2 ms. No material new repeatability problem is established relative to the intended 10–30 ms validation scale.

**Precision qualification:** the interface used 1 ms marker steps. Fractional restored coordinates and midpoints explain the decimal values; they do not demonstrate sub-millisecond human accuracy. Shared same-rater bias is not tested.

## Descriptive group results

| Group | N | Median signed ms | Mean ms | Median absolute ms | IQR ms | P95 absolute ms | Max absolute ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 6 | -0.321 | -0.393 | 0.321 | 0.407 | 1.015 | 1.161 |
| D | 6 | -0.145 | -0.170 | 0.213 | 0.376 | 0.498 | 0.528 |
| E | 6 | -0.049 | -0.070 | 0.192 | 0.312 | 0.355 | 0.358 |
| G | 6 | -0.228 | -0.285 | 0.390 | 0.676 | 0.912 | 0.941 |
| COMFORTABLE_NATURAL | 8 | 0.045 | -0.123 | 0.236 | 0.449 | 0.720 | 0.823 |
| f | 8 | -0.211 | -0.330 | 0.418 | 0.642 | 1.084 | 1.161 |
| mf | 8 | -0.274 | -0.236 | 0.274 | 0.217 | 0.386 | 0.406 |

Every group has 100% interval overlap and 100% within each ±2/5/10/20 ms bound. Group sizes are small (6 per string, 8 per condition); these are descriptive results. Full group ranges and metrics are in REPEATABILITY_SUMMARY.json; all 24 differences and intervals are in EVENT_REPEATABILITY.csv.

## Final references and preservation

The neutral rule was recorded before Pass-2 comparison in FINAL_REFERENCE_RULE.json, consistent with the prior PI-authorized GT methodology:

- Original 36: exact adjudicated values and provenance preserved, including literal original CSV fields.
- New 24 audit events: midpoint of source-coordinate centers; earliest human earliest bound and latest human latest bound. Both annotations retained.
- New 60 non-repeated events: primary values unchanged, explicitly marked primary-only with cohort audit support. These 60 were not individually repeat-validated.

Definition: **Channel-specific observable onset in the Fishman Full Circle pickup signal; NOT physical string-release Ground Truth.**

120 unique events; exactly ten per each of 12 September-14 continuous Fishman takes. Source hashes, bounds, metadata and final-reference arithmetic verified. No exclusions or unresolved events. September 19 excluded.

## Validation artifact

- Data: GROUND_TRUTH/GALLEGATI_FISHMAN_CONTINUOUS_ONSET_GT_120_V1.json
- Data SHA-256: `a4047bf252f28fa3289279bdcaa5e90226dcf0af994a51e0dd5df05174484631`
- Freeze: GROUND_TRUTH/GT_FREEZE.json
- Freeze SHA-256: `535e3d3d930db323320a5959da3999bc605ba278234671d0540d04b281b3ebd7`

**Ready for take-level continuous detector development/holdout: YES, as reference preparation.** No split or detector is run here. Future selection must occur at the take level. These takes have prior isolated-event research exposure; a later holdout can test new continuous normalization/re-arm logic but must not be described as wholly unseen audio. Retain individual uncertainty intervals, including the wider original adjudicated cases, in timing validation.

Canonical JGA, original GT, PLP, Report 001 and historical analyses unchanged. No Basic Pitch, spectral detector or Ray Brown processing. No commit or push. Stop for PI review.
