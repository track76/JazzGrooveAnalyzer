# CED-VAL-002-SWING — Independent Controlled Swing Dataset

Status: **SUPERSEDED PRE-CORRECTION INPUT AUTHORITY**

This document preserves the initial freeze at commit
`64c8c934d819e95cbb0bc294729b31f2dc02be53`. It is historical evidence and
must not govern future Calibration Zero or H02 work. The corrected authority
is `CED-VAL-002-SWING_CORRECTED.md`; the original manifest remains unchanged.

## Identities and Scope

- Controlled Dataset ID: `CED-VAL-002-SWING`
- Dataset Generation Record ID: `DGR-CED-VAL-002-SWING-001`
- Provenance Revision ID: `PR-CED-VAL-002-SWING-001`
- External location: `$JGA_EXTERNAL_ROOT/datasets/CED-VAL-002-SWING/`
- Exact audio subdirectory discovered: `steams/` (declared expected name was
  `stems/`; nothing was renamed)
- Temporal scope: WAV sample zero through sample frame 2,478,080 per channel,
  exact duration `123904/2205` seconds (`56.192290249433107` seconds)

The dataset is distinct by identity and asset checksum from `CED-VAL-001`.
The PI declares it was not used to construct, tune, audit or evaluate
`H-VAL001-RHYTHM-CORRESPONDENCE-01` or `-02`. This supports procedural
out-of-sample status; no statistical-independence claim is made.

## Epistemic Classification and Export Provenance

Checksums, file sizes and audio format measurements are **Observed Facts**.
The export procedure and common sample-zero relationship are **Declared
Experimental Procedure** supplied by the PI.

Each source was exported directly from its Sibelius part as 24-bit, 44.1 kHz
WAV, from the beginning, using Sibelius 7 Sounds (Jazz). No trimming,
normalization, conversion, Ableton processing, manual alignment or other
subsequent processing occurred.

The authoritative common origin is Sibelius `Export from beginning` sample
zero. No detected onset is used to shift or align a stem. Leading and trailing
silence is preserved.

## Authoritative Audio Assets

All three files are stereo WAVE linear PCM, 24-bit little-endian signed
integer, 44,100 Hz, 2,478,080 sample frames per channel, 14,872,576 bytes and
exactly `123904/2205` seconds long.

| Source | Exact external path below dataset root | SHA-256 |
|---|---|---|
| Drums | `steams/CED-VAL-002-swing_drums.wav` | `f3f75d95b05e7710dce5c35b68a7c54f2241a3d24177fc92f723b2ddeccbfbbb` |
| Double Bass | `steams/CED-VAL-002-swing_bass.wav` | `dc71100c99526bbb6c1d4a6626cacae55db3d434a8cfc1216dfeda15a65549d4` |
| Piano | `steams/CED-VAL-002-swing_piano.wav` | `4d2b03e7740d7487c365b2049959dd5cdc4f3b623fa9a4497bc698201c9bd75a` |

Cross-stem sample rate, bit depth, channel count, sample count and duration are
identical. The three files remain external and are not copied into Git.

## Symbolic Source Authority

The well-formed `score-partwise` MusicXML 3.0 file is:

`symbolic/CED-VAL-002-swing.musicxml`

SHA-256:
`f7f22a09410d05dc2fc2c341ebd0279603ef39339bed291f24700017390223fa`.

It identifies the score as `On Green Dolphin Street`, declares export by
Sibelius 25.12.1 directly rather than Dolet, and contains exactly Piano (`P1`),
Bass (`P3`) and Drums (`P4`) parts. Exact-rational parsing independent of JGA
observations yields 64 Piano, 127 Double Bass and 192 Drum onset groups over
128 quarter-note units. The file's own declared temporal conversion yields an
exact score extent of `256/5` seconds; the first event is at score time zero
and the final event onset is at 48 seconds.

These counts characterize symbolic input authority only. No H02 candidate,
EME comparison, event correspondence or validation outcome was constructed or
inspected. The structure is sufficient for a later deterministic event-level
authority build under a separately approved Calibration Zero protocol.

The preserved Sibelius source is:

`symbolic/CED-VAL-002-swing.sib`

SHA-256:
`abbda6256b217636bba3ac53410da2f454de25865044cdb7148b7d6e0ae72851`.

It is checksum-bound but not parsed. The adjacent `._CED-VAL-002-swing.sib`
AppleDouble sidecar is classified as operational metadata, not a scientific
source asset; it is neither deleted nor included in symbolic authority.

## Calibration and H02 Status

A new provenance-bound Calibration Zero characterization is required. Missing
authority comprises event-level symbolic Calibration Zero identity,
source-specific combined rendering/measurement behavior for Drums, Double
Bass and Piano, pairwise Piano–Drums and Double Bass–Drums applicability and
uncertainty, deterministic replay and a calibration fingerprint.

No numerical result from `CED-VAL-001` is transferred. No correction is
authorized. The frozen H02 rule is structurally applicable without
modification after Calibration Zero authority and separate PI execution
approval exist; H02 is not executed here.

## Canonical Manifest and History

Machine-readable authority:
`validation/CED-VAL-002-SWING/input_authority_manifest.json`.

Dataset/manifest scientific fingerprint:
`8a32b9296056d465312ede6cb7de5a8ccf2decc323aa289dbc7b4200ec73afd4`.

The preserved history remains:

```text
CED-VAL-001
→ Calibration Zero
→ Pairwise Calibration Zero
→ H01 negative result and failure-mode audit
→ H02 high-precision / low-recall evidence
→ independent validation required
→ CED-VAL-002-SWING input-authority freeze
```

No production code, detector configuration, EME, AD-038 localization, AD-040
profile or previous scientific record is changed.
