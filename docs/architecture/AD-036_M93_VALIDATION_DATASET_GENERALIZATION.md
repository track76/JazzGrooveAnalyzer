# AD-036 — M93 Validation Dataset Generalization

Status: LOCKED

## Context

The post-M92 Repository Authority Review found an operational limitation:
scientific validation models were item-generic, but repository catalogue
loading, MusicXML Ground Truth loading and complete validation execution were
fixed to `VAL-001`.

This prevented an additional validation item from being introduced through
canonical data alone. No scientific or architectural insufficiency was found
in the Validation Catalog, Ground Truth, Immutable Analysis Representation,
Comparator or Scientific Validation Record contracts.

## Decision

Repository validation registration and Ground Truth normalization are loaded
from canonical data while retaining the existing immutable schema-1 models.

The canonical catalogue data is:

- `recordings/validation/catalog.json`

Each registered MusicXML source has an adjacent Ground Truth data file using
the same filename stem and the suffix `.ground_truth.json`. That file supplies
only the existing Ground Truth identity, binding, source provenance,
normalization, section and instrument-category data. Tempo and time signature
continue to be read from the authoritative MusicXML source.

The repository loader verifies every registered asset checksum before
materializing a `ValidationCatalog`. The Ground Truth loader verifies source
identity, checksum, optional repository revision, measure identity and
instrument designations before materializing the existing `GroundTruth` model.

Complete validation execution selects one immutable Validation Item by
identity, performs blind analysis and materialization, then loads Ground Truth
and invokes the existing Comparator and Scientific Validation Record
boundaries.

## Data-Only Addition

A schema-compatible validation item is operationally registered by adding:

- its authoritative MP3 and MusicXML assets;
- its MusicXML-adjacent Ground Truth data;
- its immutable asset identities and item binding to the canonical catalogue;
  and
- the canonical documentation and provenance required by SVP-001 and F-030.

No production loader or validation-chain code change is required for another
item conforming to the existing approved schemas.

## Preserved Responsibilities

M93 does not change:

- Ground Truth scientific quantities or independence;
- Immutable Analysis Representation revision `1`;
- Comparator protocol `JGA-COMPARATOR-001` or schema `1`;
- Scientific Validation Record semantics;
- Candidate Period discovery;
- metric reconstruction;
- Core, Translation or Domain responsibilities; or
- SVP-001 blind/post-blind ordering.

VAL-001 identities, assets, checksums, normalization and scientific results
remain unchanged.

## Governing References

- `docs/architecture/AD-027_IMMUTABLE_ANALYSIS_REPRESENTATION.md`
- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`
- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`
- `docs/architecture/AD-030_M85_COMPARATOR.md`
- `docs/architecture/AD-031_M87_SCIENTIFIC_VALIDATION_RECORD.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
