# CED-VAL-003-SWING-3-4 — Input Authority

Status: **FROZEN INPUT AUTHORITY — CALIBRATION PENDING**

## Discovery and Operational History

The initial authorized discovery attempt found no CED-VAL-003 dataset and
stopped without modifying the repository. After the PI reported correcting
external availability, the expected root
`datasets/CED-VAL-003-SWING-3-4/` was still absent. Read-only discovery found
the complete assets under the actual external root `datasets/CED-VAL-003-SWING/`.
The scientific filenames retain `CED-VAL-003-SWING-3-4`; the audio directory is
actually named `steams/`. No path or asset was renamed.

This record preserves the sequence:

```text
initial discovery failure
→ PI external-availability correction notice
→ expected root still absent
→ actual sibling root discovered
→ assets independently reverified
→ input authority frozen with path deviation documented
```

## Authoritative Assets

All three WAVs are stereo WAVE 24-bit little-endian signed integer PCM at
44,100 Hz, with 2,150,400 frames per channel, exact duration `1024/21` seconds
(`48.761904761904762`) and size 12,906,496 bytes.

| Source | Exact path below `/Volumes/SSD Track/JGA/` | SHA-256 |
|---|---|---|
| Drums | `datasets/CED-VAL-003-SWING/steams/CED-VAL-003-SWING-3-4_drums.wav` | `11bd51037126608d7052ae0bb2b01d77b86eccae46d60ca088d3d5f57cccc44d` |
| Double Bass | `datasets/CED-VAL-003-SWING/steams/CED-VAL-003-SWING-3-4_bass.wav` | `bd702128f0b6e9887ccfae104ee0af6b2b4307c2021bb826fd85fec669322429` |
| Piano | `datasets/CED-VAL-003-SWING/steams/CED-VAL-003-SWING-3-4_piano.wav` | `64b95f5c41bb2bc102c68ffb2fa9b0215a2397e749f671ba2891378533302065` |
| MusicXML | `datasets/CED-VAL-003-SWING/symbolic/CED-VAL-003-SWING-3-4.musicxml` | `f74856b2766db824536bdbab0b3ab62dbcf8460c780272b88df13dec8620f4c2` |
| Sibelius | `datasets/CED-VAL-003-SWING/symbolic/CED-VAL-003-SWING-3-4.sib` | `f5d67d5e612e820ee8213ed02bf0d3303056ae5101d08f7c6e881b8e4252c477` |

Cross-stem technical compatibility passes. The common sample-zero origin is
bound as a PI-declared Sibelius export-from-beginning procedure, not inferred
from acoustic onset coincidence. No onset alignment, trimming, shifting,
normalization, resampling or metadata alteration occurred.

## Symbolic Authority

The checksum-bound, well-formed MusicXML score-partwise 3.0 source is titled
*Someday My Prince Will Come* and represents Piano (`P1`), Bass/Double Bass
(`P3`) and Drums (`P4`). It explicitly and consistently declares 3/4 and
quarter = 140/minute. These are controlled symbolic Ground Truth declarations,
not observational inputs to JGA or H02. One quarter unit is exactly `3/7`
second.

Exact-rational onset grouping, excluding rests and non-attacking tie
continuations and grouping simultaneous attacks within each source, yields:

- Drums: 155 symbolic events;
- Double Bass: 100 symbolic events; and
- Piano: 57 symbolic events.

The score spans exactly 102 quarter units or `306/7` seconds
(`43.714285714285714`). The first symbolic onset is 0; the last is 96 quarter
units or `288/7` seconds.

The equal WAV scope contains the complete symbolic scope and preserves an
untrimmed tail of `106/21` seconds (`5.047619047619048`) beyond score extent,
or `160/21` seconds after the last symbolic onset. The duration difference is
not classified as measurement error.

The source is sufficient to construct deterministic event-level
`CalibrationSymbolicEvent` authority later. None is constructed here; no EME,
H02 candidate, correspondence, calibration error or scoring outcome was
accessed.

## Independence, Calibration and H02

Dataset identity and every authoritative asset checksum differ from
CED-VAL-001 and corrected CED-VAL-002-SWING. PI provenance states that this
dataset was created after H02 and both prior evaluations were frozen and was
not used for rule construction or tuning. No statistical-independence claim is
made.

A new provenance-bound absolute and pairwise Calibration Zero is mandatory.
No numerical bias, uncertainty, frame distribution or correction transfers
from either prior dataset. No correction is authorized.

Frozen H02 remains unchanged and later applicable only after Calibration Zero,
PI review and separate execution authorization. Its 3/4 declaration cannot
alter H02. No H03 or source-specific rule is created.

Canonical manifest:
`validation/CED-VAL-003-SWING-3-4/input_authority_manifest.json`.

Dataset/manifest fingerprint:
`9345f5923055a7ed1c953eee4b8613f2b2262c55cd2e5f094d489d097c37f790`.

Production impact: **NONE**.
