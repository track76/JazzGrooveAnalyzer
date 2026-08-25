# CED-VAL-006 Deterministic Controlled Mix-Down Authority

Authority ID: `PR-CEDVAL006-CONTROLLED-MIXDOWN-001`

Status: **FROZEN — VERIFIED — DERIVED EXPERIMENTAL ASSET**

This authority binds a deterministic controlled stereo mix derived from all
15 provider-supplied musical WAVs in
`PR-CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK-001`. It supersedes only
the procedural requirement that a future robustness experiment use a
provider-supplied mix. The earlier `MIX_INPUT_AUTHORITY_MISSING` stop remains
valid chronology and is not rewritten.

## Source and coordinate authority

Every source identity, checksum, 48 kHz signed-24-bit PCM property, channel
count, frame count, duration, inclusion status and provider label is frozen in
`source_manifest.json`. All 15 musical WAVs are included. Mono samples are
duplicated exactly to Left and Right; stereo samples preserve their supplied
channels. File sample zero is unchanged.

Fourteen sources span `[0,11912868)`. `VOX LCT 640 TS.wav` spans
`[0,11869358)` and contributes exact mathematical zero only after its
authoritative end. This is no shift, alignment, trim or resampling decision;
the output preserves the maximum frozen distributed-file scope. Common
acquisition clock/session origin remains unestablished.

## Exact reconstruction

`generate.py` decodes signed 24-bit little-endian PCM exactly to int64 and
adds sources in UTF-8 filename-byte lexicographic order. Mono duplication and
stereo preservation occur before exact integer addition. No individual gain,
effect, temporal operation, artistic balance or listening-based decision is
used.

The unscaled sum has absolute peak `21047280`. Before WAV generation,
`mix_plan.json` froze one complete-sum global coefficient:

`8388607 / 21047280`

Quantization uses exact integer round-to-nearest, with half cases away from
zero. Output is stereo RIFF/WAVE, signed 24-bit PCM, 48,000 Hz,
11,912,868 frames. Its exact absolute peak is 8,388,607, so no clipping occurs.

## Derived asset and replay

Dataset-relative identity:

`derived/PR-CEDVAL006-CONTROLLED-MIXDOWN-001/CED-VAL-006-CONTROLLED-MIXDOWN-v0.1.wav`

SHA-256:

`32845a5d05538524b19c8f857b0a908f6618cc4b95110a14169f1e450ddfe6e0`

Two independent complete generations produced byte-identical WAVs and the
same technical authority. The generated asset remains on authorized external
storage and is not committed to Git. Repository evidence preserves the source
manifest, frozen plan, exact generator, authority, verifier and checksum.

## Scientific limits

This is a `DETERMINISTIC_CONTROLLED_DERIVED_MIX`. It is not provider-supplied,
an original/commercial mix, Ground Truth, physical-onset or acquisition-clock
authority, an artist/engineer intended balance, a perceptually optimal mix, or
representative of real-world mixes generally. No separator or JGA analysis was
executed. Original WAVs and historical authorities are unchanged.
