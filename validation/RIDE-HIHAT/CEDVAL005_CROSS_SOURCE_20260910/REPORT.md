# CED-VAL-005 Hi-Hat ↔ Ride cross-source relations

2026-09-10. PI-authorized bounded execution. **CROSS_SOURCE_TIMING_STRUCTURE_INSUFFICIENT** to establish one common timing reference. Repeated cross-source offsets exist; this is not NO_COMMON_STRUCTURE in the physical performance. No BeatReference candidate is promoted by this experiment.

## Frozen input and authority

Source interval: [28,88) original distributed-file seconds, exact native candidate rational timestamps plus integer 28. Both populations remain complete, separate and unchanged:

- Hi-Hat: 141 candidates, `/Volumes/SSD Track/JGA/experiments/VOGL-HIHAT-CEDVAL005-20260910/hihat_predictions.json`, SHA-256 `5dbdf4b2984d9f5ca5bfc2bac7da21e191bf1188506a8446b445bb8b3a3b55e3`.
- Ride: 29 candidates, `/Volumes/SSD Track/JGA/experiments/VOGL-CEDVAL005-0028-0128-20260910/ride_predictions.json`, SHA-256 `faeb572d71a7b39f39e0e4e6843b511ea8a07f7119b51652b145a2cbafc6638b`.

Source files under `/Volumes/SSD Track/JGA/datasets/CED-VAL-005-REAL-JAZZ-MULTITRACK/raw/MaurizioPagnuttiSextet_AllTheGinIsGone_Full/`:

- `05_HiHat.wav`, SHA-256 `0e0801cf3d57c06b524aea3e497520f79afe0e7b10401e4cb6f46654ce227253`.
- `09_Overheads.wav`, SHA-256 `0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`.

All four hashes and extraction-freeze bindings were verified before execution. The existing `validation/CED-VAL-005-REAL-JAZZ-MULTITRACK/input_authority_manifest.json` establishes common distributed-file sample zero, but explicitly leaves common session/export timeline, simultaneous acquisition and hardware clock unestablished. Thus the present result describes file-coordinate geometry; physical phase and channel latency remain unverified. Separate model outputs are not independently verified instrument GT or statistically independent measurements. Neither source is globally privileged. The old bootstrap frontier predates the present explicit PI direction; no historical authority is rewritten.

## Prospective test

The external protocol and implementation were frozen before computing results. Enumerate all **141 × 29 = 4,089** cross-source pairs, retaining identity `(HH input hash, HH array index; Ride input hash, Ride array index)`. A signed offset is `Ride time − Hi-Hat time`. Positive means Ride later; negative means Ride earlier on the distributed-file timeline. Ride→Hi-Hat is its exact negation, not a second witness. Zero is retained. No merging, nearest-neighbor selection, tolerance or event reconstruction occurs.

Exact rational differences use the accepted binary64 equality semantics. An independent reverse traversal manually reconstructs binary64 sign/exponent/mantissa and verifies every grouped pair. Shared endpoints and every singleton are preserved. Repeated means >=2 distinct labelled pairs, not statistical independence.

Use the same six non-overlapping ten-second regions, original [28,38) through [78,88), plus five shifted regions [33,43) through [73,83). Both endpoints must be contained in a region; excluded/cross-boundary witnesses remain preserved. Descriptive display order is occupied regions, locally repeated regions, then contained pair count; five rows plus cutoff ties. It is not a metric-period ranking. Long offsets cannot fit ten-second regions and are not thereby rejected globally.

After two fresh primary executions were fixed and byte-identical replay verified, compare the COMPLETE preserved within-source recurrence catalogues: their exact intersection, union, and exact integer ratios among common separations. For every member of the union, preserve all exact timestamp residue classes modulo that value, separately for each source. No phase origin is fitted, no phase tolerance introduced, and no phase score selects a winner. This bounded exact check cannot establish approximate phase coherence. The specific prior 0.500-second result was inspected only after the general cross-source and full-union phase results were fixed. No musical context or timing template was supplied.

## Observed cross-source result

- 4,089 distinct labelled pairs; 3,361 distinct signed offsets.
- **530 repeated signed relations**, supported by **1,258 distinct pairs**; this includes repeated zero offset.
- Four pairs have exactly zero offset. Coincidence does not establish physical synchronization or correct class identity.
- Primary region event counts: Hi-Hat **25,22,21,21,24,28**; Ride **3,0,0,4,10,12**.
- No cross-source offset has local support in all six regions. Regions without Ride predictions have no observable cross-source opportunities; they are not evidence of absent Ride playing.

Leading offsets are approximately displayed; exact rational values and all witnesses are retained. Vectors are chronological six-region contained-pair counts.

| Signed offset, Ride − Hi-Hat (s) | Global pair support | Primary local counts |
|---|---:|---|
| +0.25 exactly | 7 | 1,0,0,2,1,3 |
| ≈+0.73 | 7 | 0,0,0,3,1,3 |
| ≈−2.18 | 5 | 1,0,0,1,0,2 |
| ≈−1.21 | 6 | 0,0,0,1,1,2 |
| ≈−0.73 | 4 | 0,0,0,1,1,2 |
| ≈+0.26 | 4 | 0,0,0,1,1,2 |
| ≈+1.22 | 4 | 0,0,0,1,1,2 |

The +0.25-second offset is present in all four primary regions containing Ride observations, but repeats in only two. Its shifted-grid counts are 0,0,0,2,1. The +0.73-second offset's shifted counts are 0,0,0,4,1. These results demonstrate some local cross-source repetition, not stability across the whole minute. No claim about fills, physical omissions or robustness to density changes is established.

## Common within-source structure and post-freeze 0.500-second check

**17 exact separations recur within both sources**, displayed approximately as 0.49, 1.00, 1.45, 1.47, 1.94, 1.96, 2.46, 3.39, 3.64, 4.35, 7.23, 7.72, 7.73, 8.22, 9.19, 9.20 and 10.63 seconds. They remain distinct rational values; no approximate equivalence is claimed. There are no exact integer-multiple links among this intersection under the recorded check. The complete union contains 1,654 values; all per-source exact residue classes are preserved.

The prior exact 0.5-second Hi-Hat relation has 24 within-HH witnesses and no repeated within-Ride relation. A direct +0.5-second cross-source lag has one witness, in the last primary region; no −0.5-second pair is present. Modulo 0.5 seconds there are 71 exact Hi-Hat phase classes and 23 Ride phase classes, with largest class sizes 7 and 3 respectively. This does not establish a shared fixed phase or refute an approximately varying one.

The exact common 1-second relation (HH support 4, Ride support 2) is mathematically twice 0.5 seconds, and the +0.25-second offset is mathematically half of it. These arithmetic identities alone do not make either a subdivision, beat, common phase model or missing-stroke explanation. Hence **HIHAT 0.500-S RELATION CROSS-SOURCE SUPPORT: INDETERMINATE** as a common temporal-reference hypothesis. Direct repeated exact 0.5-lag support was not observed.

## Interpretation and stop

There are multiple common separations, but no materially better-supported common temporal reference is established. The intersection narrows a list mathematically; ambiguity about a reference remains **UNCHANGED**. No candidate is discarded from preserved evidence. Missing-event/fill robustness remains indeterminate: detections were neither synthesized nor deleted, and independent omission labels do not exist. Quantized timestamps, exact-equality splitting, shared model errors, bleed and sparse Ride observations limit interpretation. Channel-specific detector latency and physical synchronization are unverified.

**BEATREFERENCE_CANDIDATE: NONE promoted by this experiment.** This leaves all earlier evidence intact, including the Hi-Hat local-persistence result. Internal BeatReference qualification is not justified by this cross-source result. The next minimal action is to establish inter-channel timing authority for the existing inputs before interpreting physical cross-source phase. No new Vogl execution, audio analysis, model change, BPM, BeatReference, Double-Bass work, commit or push occurred.

## Preservation and verification

External package: `/Volumes/SSD Track/JGA/experiments/VOGL-CEDVAL005-CROSS-SOURCE-20260910/`. It preserves the pre-execution protocol, source hashes, labelled witnesses, signed/reverse offsets, exact zeros and singletons, local/shifted incidence, shared endpoints, two fresh-process bindings/results, replay, complete exact phase classes and post-freeze comparison. Synthetic positive/negative binary64 reconstruction checks passed. Independent exact cross-pair enumeration agreed; fresh results were byte-identical. This is bounded computational checking, not separately staffed review or the old VAL-001 custody sign-off.

| Record | SHA-256 |
|---|---|
| `protocol.json` | `7c4ff9b92afe902948a57b4a6c429c58400a4e77c74364b751c3573120df0b77` |
| `run.py` | `5bf33e2ad20b744f2acbba00801839f78fa2f419178ad2f4ee2a774ad4ba2177` |
| `run_1/result.json` | `cb6329aa6c8afe45c008c326e169c8690c4e51afa627b1006e3dd9d715172eed` |
| `replay.json` | `2b0892f7bad32e36e50e84e71cdc86e46900a128962c20dda5548674526abee2` |
| `comparison.json` | `d3b0bedad70ef685094f17df5604cd16c68959eb9c6e4995f35a8dba358e3135` |
| `exact_phase_classes.json` | `4f1ae747894611bd244e3c361c4104e484a3e969b43afc8f510fc4d622ea3f94` |
