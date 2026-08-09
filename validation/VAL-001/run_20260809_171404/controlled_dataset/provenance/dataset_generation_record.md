# DGR-CED-VAL-001-RD-001-001 — Controlled Rhythmic-Density Dataset Generation Record

## Identities

- Controlled Dataset ID: `CED-VAL-001-RD-001`
- Dataset Generation Record ID: `DGR-CED-VAL-001-RD-001-001`
- Provenance Revision ID: `PR-CED-VAL-001-RD-001-001`
- Condition A ID: `CED-VAL-001-RD-001-A`
- Condition B ID: `CED-VAL-001-RD-001-B`
- Event-removal inventory ID: `ERI-CED-VAL-001-RD-001-001`

## Declared Experimental Procedure

Condition A is an exact copy of the authoritative VAL-001 MusicXML source.
Condition B was mechanically derived without JGA analysis. Within every score
part, sounding onset events were counted in stable MusicXML document order.
Odd ordinals were retained and even ordinals were removed. All segments of a
tied event inherited the initiating event decision. Removed duration was
represented as silence; retained notes were not retimed.

The following remain declared identical: meter, tempo, instrumentation,
retained-event timing, temporal origin, total duration, rendering
configuration, sample rate, bit depth, and channel configuration.

## Symbolic assets

- Condition A: `validation/VAL-001/run_20260809_171404/controlled_dataset/symbolic/condition_a.musicxml` — `809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`
- Condition B: `validation/VAL-001/run_20260809_171404/controlled_dataset/symbolic/condition_b.musicxml` — `4cb09a0a2753abd2dbdb21fd8a20845d08f5995fdb9eb17bf5eecf46c5446b1b`
- Inventory: `validation/VAL-001/run_20260809_171404/controlled_dataset/provenance/event_removal_inventory.json` — `4eac5571204c8906720577fcd50f09c0cab09288d4297b3ee358650e6e31be59`

## Rendering boundary

No authoritative repository rendering mechanism is available. The audio
assets were externally generated. Rendering application, rendering-library
version, rendering configuration beyond the declared format, generation date,
and MP3 encoder configuration are `not specified`. Licensing status is
`not_specified`; no permission is inferred from repository presence.

Required export: PCM WAV, 24-bit, 44.1 kHz, stereo, exported from score time
zero with identical settings and identical total sample count for A, A repeat,
B, and B repeat. Leading, internal, and trailing silence must be preserved.

## Supplied Audio Assets
The following file identities and measurements are **Observed Facts**.
- `audio/condition_a.wav` — SHA-256 `33f8089ca9a09f711674dc272d7e3b6e2437080539aa046ed244158e599a08fd`
- `audio/condition_a_repeat.wav` — SHA-256 `f1f751d8a8b84fe87d790d32e91458ec20e4d2b2937af1e30410884ee31f804b`
- `audio/condition_b.wav` — SHA-256 `474b2e46ad2216f3d2d2446086c46bb2bcb93561effcf1c86e5bc6700e901b2e`
- `audio/condition_b_repeat.wav` — SHA-256 `8081c634bcc6017c19d7d27068b9084ba5ada20246c585fa5c958c5db1fec71a`
- `audio/condition_a.mp3` — SHA-256 `7fbbc692188805453f7b905d9bff9e678fdf9a91c38d612a10f71e5e2d0b7399`
- `audio/condition_b.mp3` — SHA-256 `bea3d25c38bba49f523eda7cf16d34613f1ba8e1711d28098a396d1ab594dda5`

All WAV assets are stereo 24-bit PCM at 44.1 kHz with 1983488 samples per channel. The generating application, rendering library, generation date, and MP3 encoder configuration remain `not specified`.
