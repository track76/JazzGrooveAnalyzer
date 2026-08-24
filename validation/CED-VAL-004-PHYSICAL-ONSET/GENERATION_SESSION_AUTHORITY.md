# CED-VAL-004 Physical-Onset Generation Session Authority

Authority ID: **PR-CED-VAL-004-PHYSICAL-ONSET-001**

Generation record: **DGR-CED-VAL-004-PHYSICAL-ONSET-001**

Status: **FROZEN MARKER AND RAW WAVEFORM AUTHORITY — PASS**

## Authority

This record freezes the manually constructed common-clock generation session
and existing external assets for `CED-VAL-004-PHYSICAL-ONSET`. It implements
the protocol frozen by
`PR-CED-VAL-004-PHYSICAL-ONSET-GENERATION-01` at commit
`3a91c30703d42f4cedff1b0d4a7254aac1dd0b9e`.

The external root is
`/Volumes/SSD Track/JGA/datasets/CED-VAL-004-PHYSICAL-ONSET/`. Large Ableton
and audio assets remain external and are bound by the checksums in
`input_authority_manifest.json`. AppleDouble sidecars are excluded from
scientific authority.

## Verified common-clock evidence

- Ableton Live 11.3.43 canonical session SHA-256:
  `a8acdd7575ec191366b660aa5070ca10c061f200d90035517fa27ec36f566335`.
- Marker, Drums and Double Bass canonical exports are stereo 44.1 kHz,
  signed 24-bit PCM, exactly 8,820,000 frames and 200 seconds.
- The marker has exactly 20 non-zero frames at
  `88,200 + 441,000 × k`, `k = 0…19`. Both channels equal `+4,194,304` at
  each marker and all other marker samples are digital zero.
- The canonical Live Set contains 10 C3/velocity-100 Drums events and 10
  E2/velocity-100 Double Bass events at the alternating frozen schedule.
- The Drums and Double Bass no-event controls have equal scope and contain
  zero non-zero audio bytes.
- A second complete export produced byte-identical Marker, Drums and Double
  Bass files. This establishes repeatability for the two performed renders;
  it is not a universal render-determinism claim.
- The PI-declared same-session individual-track export establishes the shared
  sample-zero procedure. Equal technical scope, the checksum-bound Live Set,
  exact marker content and asset hashes corroborate that authority. No
  detected-onset alignment, temporal shift, trimming, normalization or
  resampling is authorized or reported.

## Session and source configuration

The checksum-bound Live Set preserves the complete saved device state and
routing. The Drums track uses Ableton Simpler with collected
`00DB_Kick_2.aif`, C3, velocity 100, one-quarter duration, 1-Shot Trigger,
Warp/Filter/LFO off, Vol&lt;Vel 0%, 0.10 ms fades, −12 dB device volume and Snap
off. The Double Bass track uses Ableton Tension from `Upright Basic Bass.adv`,
E2, velocity 100 and one-quarter duration; saved `KeyboardError` is zero and
saved `ExcitatorType` is numeric value 3. The Plectrum label for that value is
PI-declared. The export-dialog configuration and that semantic label are not
fully serialized in the Live Set; they remain declared experimental procedure
bound to the frozen output hashes. All other device values are preserved
transitively by the Live Set checksum rather than duplicated here.

## Scientific limit

This PASS establishes exact scheduled-excitation and marker authority,
common-clock raw waveform authority, silence-control authority and exact
two-render replay. Marker authority is not physical-onset authority.
`t_physical` was not measured; no source onset was searched. JGA,
PulseCandidate strength, AD-038 and H02 were not executed. The record does not
establish correspondence, detector accuracy, predictor correctness or
production fitness.

Dataset fingerprint:
`704ce5926852a2ff62d9794dbee48156f875016979214cf7ef3ab93aa35ec772`.
