# CED-VAL-005 controlled-mix htdemucs_ft JGA preservation replication

Protocol: `H-CEDVAL005-CONTROLLED-MIX-HTDEMUCSFT-JGA-PRESERVATION-01`

Outcome: **PRESERVATION_REPLICATED_WITHIN_MARGIN**

The two complete executions produced byte-identical controlled mixes and byte-identical Demucs stems. Both unchanged-JGA runs produced identical scientific counts and timing metrics. The frozen scoring executions replayed byte-identically.

## Authorities and controlled mix

- Original Double Bass: 1,138 frozen BassDI EME. BassMic was included in the complete mix but was not used or combined as reference authority.
- Original Drums: 907 frozen Overheads EME.
- Controlled mix: all 16 musical WAVs, exact unity integer sum, mono duplication/stereo preservation, global gain `8388607/12931347`, stereo signed 24-bit PCM at 44,100 Hz, 10,068,072 frames.
- Controlled-mix SHA-256: `7d9d3f1f07f7760152ce560ae0bbb6f1706b443278a41af4a31dfb2638396a0f`.
- htdemucs_ft Bass SHA-256: `fdf281989b90fc2fbd1c477319d5fcbd9edfe10e0576bce8474b2b28e3bd7b73`.
- htdemucs_ft Drums SHA-256: `643a94086f898a9c4dfc5de5e323658eb373e16360ed0e63b255635714432cf7`.

## Bass correspondence — identical in both runs

- Separated EME: 825
- Matched: 782
- Original-only: 356
- Separated-only: 43
- Precision: 0.9478787878787879
- Recall: 0.687170474516696
- F1: 0.7967396841569027
- Median absolute displacement: 0.0 s
- RMSE: 0.015163725350568698 s
- Maximum displacement: 0.23219954648526078 s

Relative to frozen CED-VAL-006 htdemucs_ft:

- `DELTA_BASS_RECALL = +0.10044061669679083`; relative change `+17.118715769808457%`.
- `DELTA_BASS_F1 = +0.06893251190528604`; relative change `+9.47126031913501%`.

These are descriptive cross-material differences only and did not affect the outcome gates.

## Drum correspondence — identical in both runs

- Separated EME: 1,070
- Matched: 826
- Original-only: 81
- Separated-only: 244
- Precision: 0.77196261682243
- Recall: 0.9106945975744212
- F1: 0.8356095093576126
- Median absolute displacement: 0.0 s
- RMSE: 0.01663620532479997 s
- Maximum displacement: 0.16253968253968254 s

Compared with CED-VAL-006, CED-VAL-005 has higher Drum candidate count and materially lower Drum precision/F1, while its recall remains above the preregistered 0.90 control gate.

## AD-038 and AD-040

- Candidate AD-038: 825 eligible, 825 localized, 0 unresolved, 15 equal-distance ties.
- Among 701 Bass matches whose selected separated Drum reference could also be mapped, 654 preserved the original nearest-Drum identity; 538 preserved the preceding identity and 458 preserved the following identity.
- Candidate AD-040: 825 Double Bass plus 1,070 Drum observations, 1,895 represented observations, and 825 `GEOMETRIC_ONLY` relationships.
- Original AD-040: 1,138 Double Bass plus 907 Drum observations, 2,045 represented observations.

## Replay, limits, and interpretation

- Mix replay: byte-identical PASS.
- Demucs replay: every native stem byte-identical PASS.
- JGA scientific metrics: identical PASS; serialized identities differ by the prospectively distinct execution IDs.
- Scoring replay: byte-identical PASS; both files SHA-256 `f5f7fe410cea8bd68ff0a5e0f40528642adc9c6576a823447622e481e191f2d4`.
- Result fingerprint: `548d6c0efd1c411695db037eeabd08683095994649bf8271050cacb596011de0`.
- Separator runtime: run 1 `641.21 s`; run 2 `776.34 s`.
- A first pre-inference CLI attempt used the stock repository loader and failed to resolve safetensors by signature. The frozen offline Hugging Face loader was then used; no model, checkpoint, dependency, or inference parameter changed.
- The comparison is source-labelled JGA-observation preservation on a distributed-file coordinate. It is not physical-onset accuracy or human-microtiming Ground Truth.
- Differences from CED-VAL-006 jointly reflect material, acquisition, controlled-mixture, separator, and observation conditions. No causal genre, swing, walking-bass, kick, recording-practice, or instrumentation conclusion is authorized.
