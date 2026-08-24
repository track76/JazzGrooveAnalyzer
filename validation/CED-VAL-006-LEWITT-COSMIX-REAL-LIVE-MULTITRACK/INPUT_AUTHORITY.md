# CED-VAL-006 LEWITT COSMIX Real Live Multitrack Input Authority

Authority ID: **PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001**

Status: **FROZEN CANDIDATE REAL LIVE MULTITRACK AUTHORITY**

Dataset fingerprint:
`9d837f710fbf3292c80490d499bc96df0a8fe1140bc9139b65de8a553c4c2eca`

## Identity and provenance

The external authority root is:

`/Volumes/SSD Track/JGA/datasets/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/raw/`

The flat supplied directory contains 17 scientifically relevant assets: 15
WAV files, `Cosmix Video.mov`, and `LEWITT_exploitation-rights.pdf`. Seventeen
AppleDouble `._` sidecars are present as filesystem metadata artifacts. They
have been inventoried but have no scientific authority and were not removed.

The official LEWITT page was retrieved on 2026-08-24:

<https://www.lewitt-audio.com/blog/mix-it-baby>

LEWITT describes a live recording session at COSMIX Studios in Vienna and a
downloadable live recording of a band including drums and upright/double
bass. LEWITT states that no editing and no tuning was applied to these tracks
and calls them the RAW tracks. The page documents its drum microphone setup,
states that double bass used the dynamic capsule of a DTP 640 REX and a DI,
and states that a supplied performance video shows microphone placement at
its beginning.

These are attributable provider declarations. They are not strengthened into
claims about hardware clock, exact session origin, exhaustive processing,
physical onset, detector accuracy, event correspondence, source isolation, or
human microtiming.

## Rights and supporting video

The supplied one-page PDF is checksum-bound at
`ef13b10717ac28b850ec91cb61aa82e2cf6cd9e7a19fbe330d4944aaaecdd2fa`.
It states that publication and public releases require naming the original
artist and song; copyright and owner rights are reserved; commercial
exploitation is not allowed; and infringement will be prosecuted by the
artist. No permission or restriction beyond that document is inferred.

`Cosmix Video.mov` is checksum-bound at
`a2ab56420e605bb065aea252e91419312ae0605b75757f041750dc5b8ff899e7`.
Its QuickTime movie header reports 253.0 seconds. The supplied container has
an `avc1` 1920×1080 track, an `in24` 48 kHz track, and a timecode track. It is
supporting provenance only: no synchronization, annotation, timing analysis,
or Ground Truth authority has been assigned.

## Audio technical authority

All 15 WAV files are readable RIFF/WAVE, signed 24-bit little-endian integer
PCM at 48,000 Hz. Channel counts are either mono or stereo as preserved in the
manifest.

Fourteen WAVs contain exactly 11,912,868 frames per channel
(248.184750 seconds). `VOX LCT 640 TS.wav` contains 11,869,358 frames per
channel (247.27829166666666 seconds). Full cross-file scope equality is
therefore false. All Drum and Double Bass candidate tracks share the
11,912,868-frame scope, but equal scope is supporting technical evidence and
does not prove a common session origin.

First-nonzero frames were measured only as scope diagnostics. They are not
musical or physical onsets. No audio was played, transformed, aligned, or
written.

## Exact supplied source population

The 15 WAV assets are:

1. `BASS - DI.wav`
2. `BASS DTP 640 REX Dynamic Capsule.wav`
3. `Dums Overheads LCT 640 TS-Dual Output Mode.wav`
4. `GUIT MTP 440.wav`
5. `Kick DTP 640 REX Condenser Capsule.wav`
6. `Kick DTP 640 REX Dynamic Capsule.wav`
7. `Rhodes MTP 440.wav`
8. `ROOM LEFT LCT 640 TS.wav`
9. `Room Mono LCT 550.wav`
10. `Room Mono MTP 550.wav`
11. `ROOM RIGHT LCT 640 TS.wav`
12. `Snare MTP 440.wav`
13. `VOX  LCT 240 PRO.wav`
14. `VOX LCT 440 PURE.wav`
15. `VOX LCT 640 TS.wav`

Filename spelling and whitespace are authoritative as supplied.

## Acquisition-authority audit

`PR-JGA-REAL-AUDIO-ACQUISITION-AUTHORITY-01` was applied without weakening
its evidence hierarchy. Overall classification is
**ACQUISITION_AUTHORITY_PARTIAL**.

- Live/same-performance authority is supported by LEWITT's primary provider
  declaration for the live band recording.
- Simultaneous band capture is supported at the provider-declaration level,
  but a technical capture record is not supplied.
- Source identities are supported by exact filenames and LEWITT's microphone
  and DI documentation.
- No-editing/no-tuning/RAW status is supported exactly as LEWITT states it.
  An exhaustive timing-process and export history is not documented.
- Common acquisition system at the required recorder/routing level, shared
  hardware clock, exact common session/file origin, and export-range mapping
  are unestablished/not explicitly documented.
- Each file's immutable sample coordinate is established. Fourteen WAVs have
  identical distributed scope, including every Drum and Double Bass
  candidate. The cross-file coordinate's exact mapping to common acquisition
  time remains unestablished.
- Post-export integrity passes checksum-bound, two-pass read-only
  verification.

Physical-onset Ground Truth is not established. Calibration applicability is
`UNESTABLISHED`.

## Bounded use and analytical-source decision firewall

The dataset is scientifically usable for a future separately approved,
bounded observational study: provenance-bound source-labelled observations
may be made on immutable per-file coordinates, and neutral distributed-file
geometry may be reported with the explicit limitation that common acquisition
clock and exact session-time origin remain unestablished.

This authority does not permit acquisition-time or sample-accurate human
microtiming claims, physical onset, event correspondence, source isolation,
detector accuracy, calibration transfer, synchronization, rushing/dragging,
swing, groove, intention, or performance-quality interpretation.

No analytical input is selected or frozen. Candidate Drum inputs are the
supplied overhead, kick, and snare channels. Candidate Double Bass inputs are
the supplied DI and microphone channels.

Recommendation only, pending PI review: the scientifically simplest direct
strategy is the original unmodified stereo
`Dums Overheads LCT 640 TS-Dual Output Mode.wav` for Drums and the original
unmodified mono `BASS - DI.wav` for Double Bass. This avoids derived mixing
and preserves supplied coordinates. It is not an analytical-input authority.

The complete inventory, checksums, technical measurements, sidecar record,
provenance, evidence statuses, limitations, and deterministic fingerprint are
preserved in `input_authority_manifest.json`. JGA, H02, and strength were not
accessed. Raw assets, production code, and all historical authorities remain
unchanged.
