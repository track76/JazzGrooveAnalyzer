# Hi-Hat candidate recurrence: CED-VAL-009 and CED-VAL-005

2026-09-10. PI-authorized bounded comparison. CED-VAL-005: HIHAT_TEMPORAL_RECURRENCE_PROMISING. CED-VAL-009: HIHAT_TEMPORAL_RECURRENCE_INSUFFICIENT. Across datasets: NO_CLEAR_ADVANTAGE. These are descriptive judgments, not statistical or BeatReference thresholds.

## Inputs and frozen extraction

- CED-VAL-009: `/Volumes/SSD Track/JGA/datasets/CED-VAL-009-JESPER-BUHL-TRIO/raw/MR0804_JesperBuhlTrio_Full/04_Overheads.wav`, [0,60) source seconds. The six-channel original inventory contains no dedicated Hi-Hat channel. Reused every MIDI-42 event from the checksum-verified, unchanged first-60-second Vogl all-class output in `VOGL-CEDVAL009-FIRST60-20260910/all_predictions.json`. No repeated inference, channel audition or window search. Source SHA-256 `573ed86d61717c40c32ca71bccb2bba98e99a01602b28d9a0a27ff3d5b97d884` was verified.
- CED-VAL-005: `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/05_HiHat.wav`, [28,88) source seconds, samples [1234800,3880800) at 44.1 kHz. Source SHA-256 `0e0801cf3d57c06b524aea3e497520f79afe0e7b10401e4cb6f46654ce227253` verified. One new inference on the dedicated spot channel, PCM24 crop without resampling/amplitude adjustment before supplied preprocessing.

The original CRNN_8 ensemble and supplied peak picker remain unchanged. Model/package and dependency bindings were checked for the new inference against the accepted model freeze SHA-256 `1e6535e4669bb520882d80b76506d8b1daa3e024f0cd41ae26e62d542ce0d2f4`; CED-VAL-009 reuses its verified prior frozen execution. MIDI-42 is the combined HH output, not a separately established closed/open/pedal identity. Every output is VOGL_HIHAT_CANDIDATE / HIHAT_COMPATIBLE candidate evidence, not independently verified Ground Truth. No additional cleaning or merging occurred. The prediction at the CED-VAL-005 crop boundary was retained rather than repaired or excluded.

Both populations were frozen before recurrence. Native clip-relative binary64 timestamps are canonical; exact rational source coordinates add the integer source offset (0 or 28). Display approximations are not used for equality. Original all-class output is preserved; other instruments are not recurrence input. No contextual musical observations or 2-and-4 interpretation entered computation or conclusions.

## Same recurrence method and verification

Reused the adapter from [CED-VAL-005 Ride replication](../CEDVAL005_RIDE_RECURRENCE_20260910/REPORT.md) and [CED-VAL-009 Ride test](../CEDVAL009_RIDE_RECURRENCE_20260910/REPORT.md). Changes are population/field names, source class, offset and output bindings. The `derive` function AST was verified identical. All unordered pairs, exact positive binary64-rational differences, >=2 distinct-pair recurrence, shared endpoints, singletons, integer multiples and five-leading-rows-plus-cutoff-ties display remain unchanged. No approximate equality, binning, null or new periodicity algorithm was introduced.

The accepted exact decoder and independently implemented binary64/integer-arithmetic checker agreed through reversed pair traversal. The existing exact/near-distinct synthetic checks passed. Two fresh processes per population produced byte-identical canonical files; input/software/environment binding equality and distinct execution IDs/process IDs were checked. This is bounded adapter replay, not a claim of separately staffed review or the former VAL-001 custody protocol. Both new primary results were fixed and replay-verified before opening the preserved Ride summaries for comparison. Inference manifests were reverified after execution.

## Results

| Quantity | CED-VAL-009 HH | CED-VAL-005 HH |
|---|---:|---:|
| Candidates | 10 | 141 |
| Source-time span (s) | 22.00–58.54 | 28.00–87.71 |
| Span duration (s) | 36.54 | 59.71 |
| Unordered pairs | 45 | 9,870 |
| Distinct exact positive separations | 45 | 6,075 |
| Recurrent relations | 0 | 1,649 |
| Distinct pairs supporting recurrence | 0 | 5,444 |
| Singletons | 45 | 4,426 |
| Exact integer-multiple records | 0 | 555 |

CED-VAL-009 has no leading recurrent interval. CED-VAL-005 leading values are shown approximately except 0.5, which is exactly 1/2 second. All exact ratios and witnesses remain in the external catalogue.

| CED-VAL-005 interval (s) | Pair support | First–last supporting endpoint, original source seconds |
|---|---:|---|
| 0.5 exact | 24 | 28.48–86.27 |
| ≈1.46 | 20 | 39.79–85.77 |
| ≈1.93 | 19 | 32.44–83.37 |
| ≈3.39 | 18 | 39.29–86.76 |
| ≈0.47 | 17 | 45.60–87.71 |
| ≈0.48 | 17 | 32.92–58.63 |
| ≈2.43 | 17 | 33.40–87.71 |

Multiple competing relations remain. Broad endpoint span is not continuous persistence. No interval has been established as a preferred reference, and exact integer multiples are not labelled subdivisions or metric hierarchy.

## Comparison and limits

Preserved Ride CED-VAL-009: 113 candidates, 962 recurrent relations, 2,304 supporting pairs, maximum support 8 tied. Preserved Ride CED-VAL-005: 29 candidates, 22 recurrent relations, 46 supporting pairs, maximum support 3 tied. CED-VAL-005 Hi-Hat has greater observed support and better populated temporal coverage, but it also uses a dedicated spot instead of the Ride overhead. Source identity, channel isolation, detector response, event density and all-pairs combinatorics are therefore confounded. Higher counts do not prove greater physical correctness or cleaner event precision. CED-VAL-009 Hi-Hat provides less usable exact recurrence than its preserved Ride population. Neither absence of exact recurrence nor sparse detections proves absent physical Hi-Hat playing.

The counts retain output-grid quantization, binary64 exact-equality splitting and witness dependence. A single interval's substantially greater local persistence has not been tested or established in either dataset. There is no general cross-dataset Hi-Hat advantage. No Ground Truth accuracy, significance, robustness, BeatReference, meter or BPM claim follows.

Next minimal PI-authorized action: design a bounded local-persistence test on the preserved CED-VAL-005 Hi-Hat population. This is justified by its descriptive support, not a completed persistence result. No model tuning, new dataset research, Double-Bass work, commit or push occurred. Prior Ride reports and canonical primary summaries remain unchanged.

## External preservation

Bulk inference/reused predictions and both recurrence runs remain under `/Volumes/SSD Track/JGA/experiments/`. Run bindings contain environment, helper and adapter hashes; all events, pairs and incidence-by-endpoint are retained. Comparison record hashes:

| Record | SHA-256 |
|---|---|
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL009-20260910/hihat_predictions.json` | `664a0c94e58f97526a626a54e304df62890c611cbdbde3b1dc90adb0e28fc9e9` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL009-20260910/freeze.json` | `639552527a3a7c74f7cab910f375438e0368d20c79b69715dc345eb7b7d2200a` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL009-RECURRENCE-20260910/run.py` | `203035ae2aab7fa6826688f77a1aaccab3cb658ebb79f29f12c1169a1aa7c650` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL009-RECURRENCE-20260910/run_1/primary.json` | `d3d48b2f17f6cc8b5d1b6f5c7a86e3216862ae69caf086397ade8a5c67cd8eb6` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL009-RECURRENCE-20260910/replay.json` | `36e9b3b065717cf0a16f0cae225c6b8431bece65a8b11b1ad7196cc67e4cb2fc` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL005-20260910/hihat_predictions.json` | `5dbdf4b2984d9f5ca5bfc2bac7da21e191bf1188506a8446b445bb8b3a3b55e3` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL005-20260910/freeze.json` | `b2faa18487c1e64eff67f4596869c7eeca0d55fece490091de402f377e92701e` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL005-RECURRENCE-20260910/run.py` | `81585f4631d96ae02b0da1a759ebe167550f9e9c6b506652180603fbca503d79` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL005-RECURRENCE-20260910/run_1/primary.json` | `423c7c6f0f72abe2a161edaaf8b61a5f9c368dcf45c0125e4dd53045c0f5e4ab` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL005-RECURRENCE-20260910/replay.json` | `12e9318c301c765b3098c75f22a428dd997e3bcbf21a326daa3eacc2ec4d243f` |
| `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-COMPARISON-20260910/comparison.json` | `5f91c790601b1b0aea6810cc34a3336e5d702ccdb86d617aa9aa96b1728401fe` |
