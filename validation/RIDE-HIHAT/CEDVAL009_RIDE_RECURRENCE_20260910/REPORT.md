# CED-VAL-009 frozen Ride-candidate exact recurrence

2026-09-10. PI-authorized timestamp-only execution. Observed recurrence; a unique stable periodicity is not established. No audio inference, timing repair, null experiment, BeatReference or BPM computation was performed.

## Input and method

Input: `/Volumes/SSD Track/JGA/experiments/VOGL-CEDVAL009-FIRST60-20260910/ride_predictions.json`, SHA-256 `c386e9c28e84ce5e929cec1937f69e7b9ddecd174ebc36cfdf14f2d55715369a`, verified unchanged after execution. All 113 array entries were retained as VOGL_RIDE_CANDIDATES, not independently verified Ride Ground Truth. The source interval is [0,60) seconds; candidate events span 5.02–59.64 seconds (approximately 54.62 seconds). Absence of predictions before 5.02 seconds is not evidence of absent Ride playing.

Reused the exact binary64-to-rational decoding and independent integer-arithmetic decoding from `validation/VAL-001/exact_relation_witness_audit_20260910/generator.py` and `checker.py`. Their hashes and transport helper hash were checked before execution and bound in each run. The old 63-EME input admission, catalogue and source identity were not repurposed. This is a new, bounded population instantiation of the accepted exact-relation method, not execution of the old VAL-001 experiment or a complete local complex periodicity map.

Each witness identity is `(input SHA-256, lesser original array index, greater original array index)`. All 6,328 unordered pairs were enumerated once. Positive differences were computed as exact differences of the preserved binary64 timestamps, not rounded decimal differences. Repeated means at least two distinct pairs; shared endpoints do not imply statistical independence. No epsilon, bins, clustering, event deletion, interpolation or musical information was used. The independent arithmetic check uses a reversed pair traversal and reconstructs binary64 manually through the accepted checker. It shares source records and serialization with the adapter; this is not a separately staffed review or the original V2 custody-runner sign-off.

Synthetic arithmetic checks covered exact repetition and binary64-near-but-distinct differences. Two fresh Python processes independently produced byte-identical events, relations, integer multiples and primary summary files. Primary results were written and replay-verified before applying the descriptive 41-second split.

## Observed result

- 4,986 distinct exact positive separations; no coincident pairs.
- 962 recurrent relations, supported by 2,304 distinct pairs; 4,024 singleton relations.
- 221 exact integer-multiple relationships among recurrent values, preserved without metric interpretation.

The display rule was fixed before execution: five highest witness-count rows plus all ties at the cutoff. This is descriptive support ordering, not preference for a musical period. Seconds below are display approximations; exact numerators/denominators and every supporting pair are preserved in `relations.json`.

| Approximate separation (s) | Distinct pairs | Wholly before 41 s | Wholly after 41 s |
|---|---:|---:|---:|
| 0.5700000000000003 | 8 | 5 | 3 |
| 0.8200000000000003 | 8 | 4 | 4 |
| 0.28000000000000114 | 7 | 1 | 6 |
| 0.46000000000000085 | 7 | 4 | 3 |
| 0.8399999999999963 | 7 | 1 | 6 |
| 2.210000000000001 | 7 | 3 | 4 |

Post-hoc split: 67 events before 41 seconds, 46 at/after 41 seconds. There are 23 exact relations with at least two wholly contained witnesses on each side. Crossing pairs are preserved separately; none occur in the displayed rows. This establishes two-sided support, not continuous persistence through the transition. The split neither defines a detected transition nor supplies timing input.

## Claim limits and next action

Exact recurrence is observed in the frozen candidate population. No single dominant periodicity is established: the highest support is tied, and multiple competing separations remain. Integer ratios are mathematical relationships, not demonstrated subdivisions or a temporal hierarchy.

Detector timestamps are quantized at the supplied 100-fps output resolution. Exact collision counts can reflect this representation; conversely, nominally equal decimal differences can split into different exact binary64 rational differences. These are preserved rather than repaired. All-pairs construction creates dependence and many relations. No above-chance, physical precision, recurrence-sufficiency or stable-period claim follows from these counts alone.

No independent fill labels exist in this input. Consecutive gaps are preserved without identifying them as fills or detector misses. Fill/gap robustness and stable periodicity across 41 seconds are INDETERMINATE. Candidate classification error remains unknown. The result supports a next bounded design to test local persistence of competing relations; it does not yet supply a justified privileged reference for BeatReference discrimination. That design requires PI authorization. No further experiment was executed.

## Preserved package

External root: `/Volumes/SSD Track/JGA/experiments/VOGL-CEDVAL009-RIDE-RECURRENCE-20260910/`.

| Record | SHA-256 |
|---|---|
| `run.py` | `378e9e3242ccdc28b0fe4183035812e2d418aadeef40a00cd60d3267aee03e3b` |
| `run_1/primary.json` | `a8ed406d9b69b526690c6ea640bdea5429bd7ab182d74ee8ceff426550c8691a` |
| `run_1/relations.json` | `4713ca48ae5f2d239e44ab77486d9513a250a90d67f3dbcea1ed87f1389b10f8` |
| `run_1/integer_multiples.json` | `609a396895b37c069cb3d07504f0fddddd5eeadc6617d9f78f926b792d6fa855` |
| `replay.json` | `fbf82001e56d84e68d3d4314e117fd28861fe9a32e4d5f8e004dc4998d0c8742` |
| `posthoc.json` | `79d5e8fa13348bc61b716881f33e1ebb2c61f5dfade15bbcd4a47e1014138a16` |

Both run directories preserve bindings, event lineage, all relations including singletons, exact shared-endpoint information and scientific-file checksums. The adapter hash, Python version/executable hash, helper hashes, process IDs and distinct execution IDs are recorded before computation. All exact rational ratios remain derivable from the complete relation list; only exact integer multiples were materialized. No accepted scientific record was modified. No commit or push.
