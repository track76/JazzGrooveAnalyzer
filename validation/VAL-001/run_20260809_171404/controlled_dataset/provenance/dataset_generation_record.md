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

No authoritative repository rendering mechanism is available. Required audio
assets remain externally generated. Rendering configuration and generation
date are `not specified` until the human export is completed. Licensing status
is `not_specified`; no permission is inferred from repository presence.

Required export: PCM WAV, 24-bit, 44.1 kHz, stereo, exported from score time
zero with identical settings and identical total sample count for A, A repeat,
B, and B repeat. Leading, internal, and trailing silence must be preserved.
