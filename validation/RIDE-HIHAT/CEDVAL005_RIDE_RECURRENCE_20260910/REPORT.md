# CED-VAL-005 Ride-candidate replication

2026-09-10. PI-selected 00:28–01:28; one unchanged Vogl inference followed by the CED-VAL-009 exact-relation method. Recurrence is OBSERVED, but this test does not establish clearer sustained periodicity or a privileged period.

## Input, inference and time authority

Performance: Maurizio Pagnutti Sextet — All The Gin Is Gone. Source: `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/09_Overheads.wav`, SHA-256 `0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`, verified against existing input authority. The PCM24/44.1-kHz input was cropped to samples [1234800,3880800), exactly [28,88) source seconds, without resampling or amplitude processing before supplied model preprocessing. No alternative channel/window was tested. PI musical context was not supplied to inference or recurrence.

The original qualified CRNN_8 ensemble, all bound package/weight files, dependency versions and settings were verified against `/Volumes/SSD Track/JGA/experiments/RIDE-HIHAT-VOGL-2018/execution/freeze.json` (SHA-256 `1e6535e4669bb520882d80b76506d8b1daa3e024f0cd41ae26e62d542ce0d2f4`). The original `DrumPeakPickingProcessor` settings were unchanged. Every MIDI-51 output was retained: **29 VOGL_RIDE_CANDIDATES**, no independent Ride GT or precision/recall claim. The supplied peak picker was neither replaced nor followed by extra merging/deletion.

The output preserves native clip-relative binary64 timestamps, plus exact rational source timestamps obtained by adding integer 28. Approximate source seconds are display-only. Recurrence uses native producer bits exactly as in CED-VAL-009. This avoids adding a floating-point rounding operation solely to change the time origin. Subtraction of the exact rational source coordinates yields identical separations. All arrays retain one-to-one original prediction ordering and lineage; no candidate is repaired or removed.

Candidates span approximately **28.25–87.01 source seconds**, duration **58.76 seconds**. The first three are at 28.25, 29.25 and 32.19 seconds; the other 26 start at 61.68 seconds. The intervening prediction gap is approximately 29.49 seconds. This is a detector-output gap, not evidence that Ride playing ceased, nor an independently identified fill.

## Frozen recurrence and checks

Authority: [CED-VAL-009 report](../CEDVAL009_RIDE_RECURRENCE_20260910/REPORT.md), verified SHA-256 `b80e59397965e74831679499ecfe68bb11f91fe256eb7f2d0636d4161005015b`. The prior external adapter SHA-256 is `378e9e3242ccdc28b0fe4183035812e2d418aadeef40a00cd60d3267aee03e3b`.

Only population admission, source mapping and output paths changed. Core `derive`, `record`, `rat`, `write` and `sha` function ASTs were checked identical to the prior adapter. The same exact pair enumeration, positive rational grouping, shared-endpoint preservation, >=2 distinct-witness recurrence definition and five-leading-rows-plus-cutoff-ties display rule remain. No 41-second split applies to this replication. The accepted generator/checker decoding helpers and transport hashes were verified. Independent reversed traversal/manual binary64 arithmetic agreed on every pair. The same exact/near-distinct synthetic checks passed. Two fresh processes produced byte-identical canonical outputs; bindings, process IDs, execution IDs and checksums are preserved. This is the bounded adapter replay, not a new assertion of the old VAL-001 V2 custody sign-off or separately staffed review.

The complete prediction population was checksum-frozen before recurrence. The CED-VAL-009 comparison was opened only after the new primary result was fixed and replay-verified. No musical information, tolerance, bins, clustering, BPM conversion, missing-event recovery or null test was introduced.

## Observed result and comparison

| Quantity | CED-VAL-005 | Preserved CED-VAL-009 |
|---|---:|---:|
| Candidates | 29 | 113 |
| Unordered pairs | 406 | 6,328 |
| Distinct positive exact separations | 382 | 4,986 |
| Recurrent exact relations | 22 | 962 |
| Distinct pairs supporting recurrence | 46 | 2,304 |
| Singleton relations | 360 | 4,024 |
| Maximum support | 3, tied | 8, tied |

Leading values below are approximations for display. Every exact numerator/denominator, pair identity, endpoint reuse and support location is preserved externally.

| Approximate seconds | Distinct-pair support |
|---|---:|
| 0.49 | 3 |
| 2.46 | 3 |
| 1.00, 1.45, 1.47, 1.94, 1.96, 2.79, 3.39, 3.64, 3.95, 4.35 | 2 each |
| 6.68, 7.23, 7.72, 7.73, 8.22, 9.19, 9.20, 10.63, 16.93, 51.01 | 2 each |

All 22 rows are retained by the pre-existing cutoff-ties rule. There is no exact common leading relation between the experiments. Approximate cross-performance correspondence is INDETERMINATE because no justified similarity rule was introduced. In particular, decimal resemblance is not used to collapse relations or establish a common periodicity.

There are **zero exact integer-multiple records among the 22 recurring values** under the unchanged ratio test. Multiple competing separations remain; subdivisions/harmonic families are not established. Other exact rational ratios remain derivable from the preserved complete catalogue, but any two rational separations have a rational ratio, which alone supplies no musical hierarchy.

## Bounded interpretation

The second population independently repeats the observation that exact pair recurrence exists. It does **not** produce a substantially clearer dominant relation: maximum support remains tied, and prediction coverage is sparse and uneven. Raw cross-dataset counts are not normalized measures of clarity or statistical significance; event populations, detection behavior and all-pairs dependence differ. Detector false positives/misses, timestamp-grid collisions and physical accuracy remain unresolved. The 100-fps timestamp representation and exact binary64 equality are retained without repair.

Whether this strengthens evidence for stable Ride timing is INDETERMINATE. A bounded local-persistence test is justified as the next investigation, not as an already demonstrated property. BeatReference discrimination is not yet justified by a stable privileged relation. No timing reference, BPM, meter, subdivision, swing or fill-robustness claim is made.

**Next PI action:** authorize design of a bounded local-persistence test on the two preserved candidate populations. No tuning, additional inference, production integration, unrelated work, commit or push occurred.

## Preservation

Inference root: `/Volumes/SSD Track/JGA/experiments/VOGL-CEDVAL005-0028-0128-20260910/` (crop, unchanged inference bindings, activations, all class outputs, complete Ride population and verified seven-file checksum manifest).

Recurrence root: `/Volumes/SSD Track/JGA/experiments/VOGL-CEDVAL005-RECURRENCE-20260910/` (adapter, comparison script, two runs, every event/pair relation including singletons, exact integer-multiple list, independent check/replay and comparison).

| Record | SHA-256 |
|---|---|
| Inference `ride_predictions.json` | `faeb572d71a7b39f39e0e4e6843b511ea8a07f7119b51652b145a2cbafc6638b` |
| Inference `freeze.json` | `66b0e078a245b0e1ad919fbd7b49d71fe0fe97c400da3bb614c830f9da128cd2` |
| Recurrence `run.py` | `84b4c983d6d2720476d064b807a8a5f258abf7add4a8029510477938954a1cf5` |
| Recurrence `run_1/primary.json` | `f89dac8eb6c33286f2827fdea641f882248ea479f33713c22f1487254c21f96e` |
| Recurrence `run_1/relations.json` | `dd05b4c02c773a26fff1b5a037868f06c3d87a2b956938670f0b6cc8432d1525` |
| Recurrence `comparison.json` | `b84903a11978628ae28b37b8eb4ff70350b068c0718d054a58116d85d3b38a6d` |
| Recurrence `replay.json` | `516ecfbc08138ae40f6ea4be19c6509ac34f7c28f42b9e0542fcec0fc6c54e55` |
