# CED-VAL-002-SWING — Corrected Input Authority

Status: **FROZEN CORRECTED INPUT AUTHORITY — CALIBRATION PENDING**

This provenance revision supersedes the pre-correction authority frozen at
commit `64c8c934d819e95cbb0bc294729b31f2dc02be53` for all future Calibration
Zero and H02 out-of-sample work. It does not delete, amend or conceal that
historical record.

## Correction History

The PI identified a source-duration issue after the initial freeze and before
Calibration Zero preregistration, corrected the Sibelius/symbolic source, and
requested complete reverification. The exact history is:

```text
initial CED-VAL-002-SWING freeze
→ PI identified a source-duration issue
→ PI corrected the Sibelius/symbolic source
→ corrected dataset reverified
→ corrected authority frozen
```

The three WAV assets are byte-identical to the initial freeze. The MusicXML
and Sibelius assets changed. The initial manifest remains at
`validation/CED-VAL-002-SWING/input_authority_manifest.json` with fingerprint
`8a32b9296056d465312ede6cb7de5a8ccf2decc323aa289dbc7b4200ec73afd4`
and status `SUPERSEDED_PRE_CORRECTION_AUTHORITY` by this revision.

## Corrected Authoritative Assets

External root-relative dataset path: `datasets/CED-VAL-002-SWING/`.
The exact discovered audio directory remains `steams/`; nothing was renamed.

All WAVs are stereo WAVE 24-bit little-endian signed integer PCM at 44,100 Hz,
with 2,478,080 frames per channel, exact duration `123904/2205` seconds
(`56.192290249433107`) and size 14,872,576 bytes.

| Source | Exact path below dataset root | SHA-256 | Changed |
|---|---|---|---|
| Drums | `steams/CED-VAL-002-swing_drums.wav` | `f3f75d95b05e7710dce5c35b68a7c54f2241a3d24177fc92f723b2ddeccbfbbb` | No |
| Double Bass | `steams/CED-VAL-002-swing_bass.wav` | `dc71100c99526bbb6c1d4a6626cacae55db3d434a8cfc1216dfeda15a65549d4` | No |
| Piano | `steams/CED-VAL-002-swing_piano.wav` | `4d2b03e7740d7487c365b2049959dd5cdc4f3b623fa9a4497bc698201c9bd75a` | No |
| MusicXML | `symbolic/CED-VAL-002-swing.musicxml` | `0ae6ed241699b65f2e6d120c08f18e132781109f5f3d35335a9efe094e2ceb39` | Yes |
| Sibelius | `symbolic/CED-VAL-002-swing.sib` | `d03ddd65eb02f3dae1ea775df0a43b599610fb201d3c1abc976d149b25cbf132` | Yes |

The `._CED-VAL-002-swing.sib` AppleDouble sidecar remains excluded operational
metadata; it is not symbolic authority.

## Corrected Symbolic Characterization

The MusicXML is well-formed `score-partwise` 3.0 and represents Piano (`P1`),
Bass/Double Bass (`P3`) and Drums (`P4`). Exact-rational onset grouping,
without JGA observation access, yields:

- Piano: 64 symbolic events;
- Double Bass: 127 symbolic events; and
- Drums: 192 symbolic events.

The score spans exactly 128 quarter units. Two consistent MusicXML declarations
state quarter = 150 per minute, providing the non-inferred conversion of one
quarter unit to `2/5` seconds. Symbolic scope is therefore exactly `256/5`
seconds (51.2 seconds). The first symbolic onset is 0 and the last is exactly
48 seconds.

Every equal WAV scope contains the complete symbolic scope and extends by
exactly `11008/2205` seconds (`4.992290249433107`) beyond it. This is
temporally coherent with the declared common sample-zero origin and an
untrimmed rendered duration/release tail. Equality with the last onset is not
required and no tail is trimmed.

The MusicXML is sufficient to construct deterministic event-level
`CalibrationSymbolicEvent` authority later. None is constructed here; no EME,
measurement error, H02 candidate or correspondence outcome is accessed.

## Independence, Calibration and H02

The corrected revision remains distinct from `CED-VAL-001` by identity and
authoritative asset checksums. PI provenance declares it was not used to
construct or tune H01/H02. No statistical-independence claim is made.

A new Calibration Zero characterization remains mandatory. CED-VAL-001
numerical results are not reused. After corrected Calibration Zero authority
and separate PI approval, frozen H02 can be applied without modification.

Canonical corrected manifest:
`validation/CED-VAL-002-SWING/input_authority_manifest_v2_corrected.json`.

Corrected dataset/manifest fingerprint:
`631eaf017cfaf335ee2945bfbe0df19221a0a0d069fee3602880eda7a851ade1`.

No production code or external asset was modified by reverification.
