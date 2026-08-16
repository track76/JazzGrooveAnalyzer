# H-VAL001-RHYTHM-TEMPO-01 — Frozen Result

Status: COMPLETE

Blind classification: `MULTIPLE_COMMON_PERIODS`

## Input fingerprints

| Contributor | EME | Fingerprint |
|---|---:|---|
| Drums | 63 | `bdd609584ae58c3897691b1c400a3829b45dd637fe1fcc432cbdadc574b251ed` |
| Double Bass | 27 | `80896b766d87b9a6d820223dfee5b928adab76397960fe2b728b6a8e158b6164` |
| Piano | 49 | `357be2d0c1ad88d8dccf4513c1aab165d7b48286861fff62ea954a62d99f72a2` |

Only absolute EME timestamps and source/observation provenance entered blind
discovery. Every EME was retained.

## Source-periodicity evidence

Every period has measurement uncertainty ±1 frame, where one frame is
`512/44100` seconds. `E/L` gives early/late occurrence counts.

### Drums

| Frames | Seconds | Recurrences | E/L | Persistence |
|---:|---:|---:|---:|---|
| 30 | 0.348299320 | 7 | 1/6 | PERSISTENT |
| 33 | 0.383129252 | 19 | 7/12 | PERSISTENT |
| 37 | 0.429569161 | 3 | 0/3 | LIMITED_SCOPE |
| 66 | 0.766258503 | 15 | 8/7 | PERSISTENT |
| 67 | 0.777868481 | 6 | 3/3 | PERSISTENT |
| 70 | 0.812698413 | 3 | 2/1 | PERSISTENT |

Candidate population replay: `PASS`; five of six candidates are eligible for
consensus.

### Double Bass

| Frames | Seconds | Recurrences | E/L | Persistence |
|---:|---:|---:|---:|---|
| 33 | 0.383129252 | 8 | 3/5 | PERSISTENT |
| 132 | 1.532517007 | 2 | 0/2 | LIMITED_SCOPE |
| 232 | 2.693514739 | 6 | 4/2 | PERSISTENT |
| 265 | 3.076643991 | 2 | 2/0 | LIMITED_SCOPE |

Candidate population replay: `PASS`; two of four candidates are eligible for
consensus.

### Piano

| Frames | Seconds | Recurrences | E/L | Persistence |
|---:|---:|---:|---:|---|
| 17 | 0.197369615 | 4 | 0/4 | LIMITED_SCOPE |
| 32 | 0.371519274 | 5 | 3/2 | PERSISTENT |
| 33 | 0.383129252 | 6 | 1/5 | PERSISTENT |
| 34 | 0.394739229 | 13 | 7/6 | PERSISTENT |
| 65 | 0.754648526 | 5 | 3/2 | PERSISTENT |
| 66 | 0.766258503 | 3 | 2/1 | PERSISTENT |
| 100 | 1.160997732 | 2 | 2/0 | LIMITED_SCOPE |
| 132 | 1.532517007 | 3 | 1/2 | PERSISTENT |
| 165 | 1.915646259 | 2 | 2/0 | LIMITED_SCOPE |
| 166 | 1.927256236 | 4 | 1/3 | PERSISTENT |

Candidate population replay: `PASS`; seven of ten candidates are eligible for
consensus.

## Frozen rhythm-section common periods

Sources have equal weight. Correspondence uses only overlapping ±1-frame
measurement intervals; a common candidate requires at least two sources.

| Source frames | Sources | Equal-source period (s) | Corresponding rate | Common frame interval |
|---|---|---:|---:|---|
| 30, 32 | Drums, Piano | 0.359909297 | 166.708669 | [31,31] |
| 33, 33, 32 | Bass, Drums, Piano | 0.379259259 | 158.203125 | [32,33] |
| 33, 33, 33 | Bass, Drums, Piano | 0.383129252 | 156.605114 | [32,34] |
| 33, 33, 34 | Bass, Drums, Piano | 0.386999244 | 155.039063 | [33,34] |
| 66, 65 | Drums, Piano | 0.760453515 | 78.900286 | [65,66] |
| 67, 65 | Drums, Piano | 0.766258503 | 78.302557 | [66,66] |
| 66, 66 | Drums, Piano | 0.766258503 | 78.302557 | [65,67] |
| 67, 66 | Drums, Piano | 0.772063492 | 77.713816 | [66,67] |

All eight common candidates are `FULL_SCOPE_PERSISTENT` under the frozen
early/late rule. This demonstrates recurrence in both temporal halves; the
protocol does not estimate continuous drift or a local tempo trajectory.

Twelve preserved `1:2_MEASUREMENT_INTERVAL_OVERLAP` relations connect the
shorter and longer candidate families. No member is assigned metric role.

## Post-freeze validation

Blind result SHA-256:
`0f6d8162053142893d4f938f32c73174b26dd8c783a457ad98e6e491ecb369cd`.

Scientific fingerprint:
`238be4910504e6d2b570a47b6cb1d4ded21a280fddbe300c9f09f88af4b11d38`.

Only after that freeze, `GT-VAL-001-v1` revealed 78 quarter BPM, reference
period `10/13` seconds or `66.256009615...` observation frames. Two frozen
long-period candidates contain that reference within their measurement
interval; two frozen short-period candidates contain it after exact doubling.
Four other frozen tuples do not correspond under those tests.

Rhythm-section consensus materially improves the earlier evidence by adding
independent source provenance and equal-source support. It does not select
between the preserved hierarchical families. Metric-reference role remains
unjustified; autonomous BPM inference status is `PARTIAL`.
