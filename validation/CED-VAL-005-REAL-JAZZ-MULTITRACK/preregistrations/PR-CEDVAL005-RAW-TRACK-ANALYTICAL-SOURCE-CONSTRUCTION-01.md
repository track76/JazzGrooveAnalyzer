# PR-CEDVAL005-RAW-TRACK-ANALYTICAL-SOURCE-CONSTRUCTION-01

Status: **PREREGISTERED — NOT EXECUTED — PI REVIEW REQUIRED**

Authority: `PR-CED-VAL-005-REAL-JAZZ-MULTITRACK-001`, dataset fingerprint
`d9d6341f837bc5f56054ffd6c91f6be65a7bdbb8043526a9ac70d924a81335af`,
authority commit `5d9f8a9fdbd617737656958c1e1eddb29281c85e`.

## Frozen scientific question

Before JGA output exists, what is the scientifically minimal deterministic
rule by which the supplied raw channels represent the `DRUMS` and
`DOUBLE_BASS` analytical sources in the first bounded real-human-jazz
observational study?

This record freezes input selection only. It neither runs JGA nor authorizes
profile construction, correspondence, calibration transfer, derived audio or
musical interpretation.

## Drums analytical source

The authorized raw population is `01_KickIn.wav`, `02_KickOut.wav`,
`03_SnareUp.wav`, `04_SnareDown.wav`, `05_HiHat.wav`, `06_Tom1.wav`,
`07_Tom2.wav`, `08_Tom3.wav` and `09_Overheads.wav`.

The frozen analytical representation is the existing raw file
`09_Overheads.wav`, unchanged and checksum-bound by the dataset authority as:

- supplied source label: `Overheads`;
- SHA-256:
  `0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a`;
- WAVE, stereo, signed 24-bit little-endian PCM, 44,100 Hz;
- exactly 10,068,072 frames per channel.

This is the single supplied track labelled as an overhead observation of the
Drums population and therefore the simplest existing whole-kit channel. A
close-microphone track would privilege one component, while combining nine
channels would introduce arbitrary gain, summation, phase and clipping
decisions without equivalent additional authority. Selection is based only
on supplied channel identity and methodological simplicity, not JGA output.

No derived Drums asset is required or authorized. Stereo-to-mono handling and
any normalization performed by the already-authorized immutable observation
pipeline remain pipeline behavior, not a new analytical-source construction
or derived asset authorized by this record.

## Double Bass analytical source

The authorized raw population is `10_BassMic.wav` and `11_BassDI.wav`.

The frozen analytical representation is the existing raw file
`11_BassDI.wav`, unchanged and checksum-bound by the dataset authority as:

- supplied source label: `BassDI`;
- SHA-256:
  `2c4c06b9b5d4b18e00000bc2c036207fc68fb722c5854e0a30107ad4594a910b`;
- WAVE, mono, signed 24-bit little-endian PCM, 44,100 Hz;
- exactly 10,068,072 frames.

The supplied DI channel is the simplest single-channel direct representation
of the labelled Bass source. It avoids constructing an arbitrary Mic/DI blend
and avoids adding gain, phase and clipping choices. This does not claim that
DI is the physical acoustic onset, a complete representation of radiated
Double Bass sound, or universally preferable to a microphone. Selection is
fixed before JGA inspection and is specific to this bounded study.

No derived Double Bass asset is required or authorized.

## Identity, bleed and timeline authority

`DRUMS` and `DOUBLE_BASS` identify physical source roles in the future bounded
analysis; `Overheads` and `BassDI` identify their selected observation
channels. A channel is not an independent instrument, and its selection does
not create isolated-source or physical-onset Ground Truth.

Room sound, cross-instrument bleed and the recording/transduction properties
already present in the selected raw tracks remain untouched. No separation,
denoising, gating, equalization, compression or transient shaping is
authorized.

Both selected files retain the frozen distributed-file coordinate exactly:
frame zero through frame 10,068,071 at 44,100 Hz. No trimming, leading-silence
removal, time shift, latency or transient correction, phase alignment,
resampling, warp or quantization is authorized. The selection does not
strengthen the unestablished common-session, simultaneous-acquisition,
hardware-clock, editing or physical-onset authorities recorded by
`PR-CED-VAL-005-REAL-JAZZ-MULTITRACK-001`.

## Amplitude and derivation firewall

Source construction applies unit identity to the original file bytes: no
gain, summation, normalization, format conversion or rendered output exists.
Consequently there is no construction clipping policy beyond `NOT_APPLICABLE`
and no new output filename, checksum or derived-source fingerprint. Future JGA
execution may use only the existing immutable pipeline; it may not be tuned
because these inputs are real audio.

Piano, Trumpet, Trombone and Saxophone source construction remains outside
this preregistration.

## Scientific status and replay

The selected files are provenance-bound analytical representations of the
supplied real multitrack. They are not physical-onset Ground Truth,
isolated-source Ground Truth, event-correspondence authority or sample-accurate
human-microtiming authority. Calibration applicability remains
`UNESTABLISHED`, correspondence remains `GEOMETRIC_ONLY`, and no controlled
dataset numerical calibration may transfer. H02 and PulseCandidate strength
are excluded.

Before any later JGA execution, perform at least two independent read-only
verification passes. Each must recover the exact selected relative paths,
raw-input SHA-256 values, channel counts, 44,100 Hz sample rate, 24-bit PCM
encoding and 10,068,072-frame scope. Both passes must agree exactly; otherwise
stop with `AUTHORITY_CONFLICT`. Because no derived file exists, replay tests
selection and raw authority rather than audio rendering.

Architecture impact: **NONE**. Production impact: **NONE**. Production code,
raw assets and prior scientific authorities remain unchanged.
