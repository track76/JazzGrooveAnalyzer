# AD-029 — M84 Scientific Validation Catalog

Status: LOCKED

## Context

Scientific validation requires a reproducible catalogue of immutable validation
assets. This catalogue responsibility is distinct from the existing
analysis-produced `ValidationDataset`, which remains an observational artifact
of the current runtime pipeline.

## Decision

The scientific validation catalogue identity is:

`JGA-VALIDATION-CATALOG-v1`

The catalogue contains immutable Validation Items. Its sole responsibility is
to catalogue the assets and provenance required to identify a validation item.

The first Validation Item identity is:

`VAL-001`

## VAL-001 Asset Binding

VAL-001 binds, by identity only:

- Ground Truth `GT-VAL-001-v1`;
- the approved authoritative MusicXML asset;
- the approved MP3 recording;
- asset checksums and repository revisions;
- immutable catalogue provenance and metadata; and
- explicit asset licensing status.

Ground Truth content is not duplicated inside the Validation Item.

## Authoritative MusicXML Asset

Repository-relative identity:

`recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml`

SHA-256:

`809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778`

Repository revision:

`c50abd435097b8f335a53b4146d9fa933764b15f`

Licensing status:

`not_specified`

## MP3 Asset

Repository-relative identity:

`recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3`

SHA-256:

`d358d1bca5144ea1dabee4d970fa5deabf81a209922481a77db0f01bd8bdbbbb`

Repository revision:

`1b4ebfdcef25dc3e897b691d5149f52dce0d29fd`

Licensing status:

`not_specified`

No copyright ownership, usage permission, publication permission or
redistribution right is inferred from repository presence.

## M83 Identity Correction

GT-VAL-001-v1 is bound to Validation Item `VAL-001`. The Ground Truth field is
therefore `validation_item_id`, not `validation_dataset_id`.

This correction changes identity ownership only. It does not change Ground
Truth content, generation, provenance or normalization.

## Metadata and Provenance

The catalogue preserves schema and catalogue versions. Each Validation Item
preserves its item version and stable reference title. Asset identity preserves
repository-relative path, checksum, repository revision and licensing status.

## Independence

The catalogue does not:

- perform or initiate analysis;
- generate or load Ground Truth content;
- perform comparison;
- compute validation metrics; or
- depend on runtime analysis outputs.

## Controlled Experimental Dataset Reference

The independently governed controlled experimental dataset related to VAL-001
is identified as `CED-VAL-001`. Its generation procedure and temporal-origin
declaration are owned by AD-033 and are not duplicated by this catalogue.

## Dependency Direction

Immutable Asset Identities

↓

Validation Item

↓

Scientific Validation Catalog

## Governing References

- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/scientific/JGA_VALIDATION_DATASET.md`
- `docs/scientific/VAL-001_REFERENCE_DATASET.md`
- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`
- `docs/architecture/AD-033_M90_CONTROLLED_DATASET_PROVENANCE.md`
