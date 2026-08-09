# H-VAL001-C1-06 — Controlled Rhythmic-Density Preparation

## Status

Prepared to the external lossless-audio rendering boundary. No JGA analysis,
Ground Truth comparison, Candidate Period comparison, or interpretation has
executed.

## Identities

- Experiment: `H-VAL001-C1-06`
- Controlled Dataset: `CED-VAL-001-RD-001`
- Dataset Generation Record: `DGR-CED-VAL-001-RD-001-001`
- Provenance Revision: `PR-CED-VAL-001-RD-001-001`
- Condition A: `CED-VAL-001-RD-001-A`
- Condition B: `CED-VAL-001-RD-001-B`
- Event-removal inventory: `ERI-CED-VAL-001-RD-001-001`

## Symbolic preparation

**Observed Fact:** Condition A is byte-identical to the authoritative VAL-001
MusicXML and retains SHA-256
`809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`.

**Declared Experimental Procedure:** For each part independently, sounding
onset events were enumerated in stable MusicXML document order. Odd ordinals
were retained and even ordinals removed. Tied continuations inherited the
decision of the initiating event. The rule used no JGA analytical output.

**Observed Fact:** Condition B has SHA-256
`4cb09a0a2753abd2dbdb21fd8a20845d08f5995fdb9eb17bf5eecf46c5446b1b`.

| Part | Eligible events | Retained | Removed |
|---|---:|---:|---:|
| P1 — Voice | 11 | 6 | 5 |
| P2 — Tenor saxophone | 12 | 6 | 6 |
| P3 — Piano | 60 | 30 | 30 |
| P5 — Double bass | 28 | 14 | 14 |
| P6 — Drum Set | 86 | 43 | 43 |
| Total | 197 | 99 | 98 |

**Observed Fact:** The generated Condition B contains 99 sounding events.
Meter, tempo, part identities, measure identities, symbolic temporal extents,
and existing Ground Truth schema-1 quantities are identical between A and B.
All retained pitch/unpitched identities, onsets, durations, voices, staves, and
measure identities match Condition A.

## External rendering boundary

No authoritative repository mechanism renders MusicXML to lossless audio.
The following assets must be exported externally:

- `controlled_dataset/audio/condition_a.wav`
- `controlled_dataset/audio/condition_a_repeat.wav`
- `controlled_dataset/audio/condition_b.wav`
- `controlled_dataset/audio/condition_b_repeat.wav`
- `controlled_dataset/audio/condition_a.mp3`
- `controlled_dataset/audio/condition_b.mp3`

WAV requirements: PCM, 24-bit, 44.1 kHz, stereo, exported from score time zero
with identical rendering configuration and identical total sample count.
Leading, internal, and trailing silence must remain intact. Repeated exports
must be initiated independently. The MP3 derivatives are only for the existing
schema-1 Validation Catalogue binding and do not replace controlled WAV
evidence.

## Validation gate

The fail-closed package validator rejects the package because the external
audio checksums and common sample count do not yet exist. This is the expected
scientific stop condition. Blind analysis remains prohibited.
