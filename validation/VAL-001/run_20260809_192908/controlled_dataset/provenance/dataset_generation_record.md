# DGR-CED-VAL-001-TS-001-001 — Controlled Temporal-Scaling Dataset Generation Record

## Identities

- Controlled Dataset ID: `CED-VAL-001-TS-001`
- Dataset Generation Record ID: `DGR-CED-VAL-001-TS-001-001`
- Provenance Revision ID: `PR-CED-VAL-001-TS-001-001`
- Condition A ID: `CED-VAL-001-TS-001-A`
- Condition B ID: `CED-VAL-001-TS-001-B`

## Declared Experimental Procedure

Condition A is an exact copy of the authoritative VAL-001 MusicXML source and
declares quarter note = 78 BPM. Condition B is derived from the same source by
changing only both authoritative `<per-minute>` declarations from `78` to
`110`. No JGA output participates in this transformation.

Symbolic event identities, document order, pitches, score positions, symbolic
durations, meter, instrumentation, dynamics, articulations and source identity
remain identical. Only authoritative tempo differs.

## Symbolic assets

- Condition A: `validation/VAL-001/run_20260809_192908/controlled_dataset/symbolic/condition_a.musicxml` — `809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`
- Condition B: `validation/VAL-001/run_20260809_192908/controlled_dataset/symbolic/condition_b.musicxml` — `708dcbec3228fc4af2d79fed1dcee7b903a8ea162da224a4d613a434cf8093f8`

## External rendering procedure

Render both conditions from score time zero using the same Sibelius version,
sound library, playback configuration, mixer settings and export settings.
Preserve leading, internal and trailing silence. Export each canonical WAV and
each repeated WAV independently. Do not reuse or time-stretch an existing
render.

Required WAV format: PCM, 24-bit, 44.1 kHz, stereo. The A and B sample counts
are expected to differ because tempo is the controlled variable; canonical and
repeat renders within each condition must preserve the same temporal extent.
Create one MP3 derivative from each canonical condition for the existing
schema-1 Validation Item binding, using identical MP3 export settings.

Generating application version, rendering-library version, generation date,
rendering configuration and MP3 encoder configuration remain `not specified`
until supplied by the human renderer. Licensing status is `not_specified`.

## Supplied audio assets

The following identities are Observed Facts:

- `audio/condition_a.wav` — `33f8089ca9a09f711674dc272d7e3b6e2437080539aa046ed244158e599a08fd`
- `audio/condition_a_repeat.wav` — `f1f751d8a8b84fe87d790d32e91458ec20e4d2b2937af1e30410884ee31f804b`
- `audio/condition_a.mp3` — `7fbbc692188805453f7b905d9bff9e678fdf9a91c38d612a10f71e5e2d0b7399`
- `audio/condition_b.wav` — `d05a259bc2f8468c9160cfec6efa7643bc1176354898fcf9e8336db09bee7c10`
- `audio/condition_b_repeat.wav` — `d05a259bc2f8468c9160cfec6efa7643bc1176354898fcf9e8336db09bee7c10`
- `audio/condition_b.mp3` — `d99574c296ea874c5b5c1faaa9c96943f924f4f2f7fd59d6ed99ebb65bead83b`

All WAV assets are stereo 24-bit PCM at 44.1 kHz. Condition A contains
1,983,488 samples per channel; Condition B contains 1,470,464. Independent
render initiation remains a Declared Experimental Procedure. The byte-identical
Condition B renders establish numerical reproduction but do not independently
prove how the second file was generated.
