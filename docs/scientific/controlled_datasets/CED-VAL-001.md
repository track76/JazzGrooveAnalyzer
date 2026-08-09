# CED-VAL-001 — VAL-001 Controlled Experimental Dataset

Status: CANONICAL

## Identities

- Controlled Dataset ID: `CED-VAL-001`
- Dataset Generation Record ID: `DGR-CED-VAL-001-001`
- Provenance Revision ID: `PR-CED-VAL-001-001`
- Related Validation Item ID: `VAL-001`

## Scientific Classification

The generation statements in this record are **Declared Experimental
Procedure**. They are declarations by the dataset creator and are not Observed
Facts.

File checksums and format measurements are **Observed Facts** obtained from the
repository assets identified below.

## Dataset Generation Record

The dataset creator declares that the five authoritative WAV stems were:

- generated from the Sibelius score;
- exported one instrument at a time;
- exported from the beginning of the score;
- exported using identical settings for every instrument;
- exported as PCM WAV, 24-bit, 44.1 kHz; and
- intentionally aligned to the temporal-origin declaration below.

The following historical generation details are unavailable and are preserved
without inference:

- generation date: `not specified`;
- generating software: `Sibelius`;
- generating software version: `not specified`;
- rendering/playback library: `not specified`;
- rendering/playback library version: `not specified`; and
- additional rendering configuration: `not specified`.

The generating-software name follows the creator's declaration that the assets
were generated from the Sibelius score. No version or hidden configuration is
inferred.

## Temporal-Origin Declaration

**Declared Experimental Procedure:**

```text
MusicXML score time zero = WAV sample zero
```

This equality is an intentional generation declaration. It is not classified
as an Observed Fact, even where measured asset properties are mutually
compatible with it.

## Source References

The declared symbolic generation sources are preserved by repository-relative
identity:

- Sibelius score: `recordings/03 THE COST OF LIVING versione intro + 8 bar.sib`
- authoritative MusicXML: `recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml`

The MusicXML authority and checksum remain owned by AD-028. This record does
not duplicate or modify Ground Truth content.

- Sibelius score checksum: `not specified` because the exact generation-source
  revision was not preserved;
- MusicXML SHA-256: `809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`.

## Authoritative Generated Assets

All measurements below are Observed Facts. Every asset is stereo PCM WAV,
24-bit, 44.1 kHz, with exactly 1,865,728 samples per channel and duration
42.30675736961451 seconds.

| Repository-relative asset | SHA-256 |
|---|---|
| `recordings/validation/stems/double_bass.wav` | `31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5` |
| `recordings/validation/stems/drums.wav` | `d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd` |
| `recordings/validation/stems/piano.wav` | `26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e` |
| `recordings/validation/stems/tenor_sax.wav` | `89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e` |
| `recordings/validation/stems/voice.wav` | `0fa95a3eff06d1ab075caf2f388c17d536e614aca397647967805045521c655a` |

## Excluded Assets

The MP3 files in `recordings/validation/stems/` are obsolete experimental
artifacts. They are not members of `CED-VAL-001`, are not authoritative
generated assets, and are excluded from canonical provenance.

## Reproducibility Limitations

Exact byte-for-byte regeneration is not established because the generation
date, exact Sibelius version, rendering/playback library version, and further
rendering configuration were not preserved. The authoritative WAV content is
therefore fixed by repository-relative identity and SHA-256 checksum, while
the available declared procedure supports procedural audit without inventing
missing historical parameters.

## Governing References

- `docs/architecture/AD-033_M90_CONTROLLED_DATASET_PROVENANCE.md`
- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`
- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
