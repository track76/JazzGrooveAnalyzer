# AD-033 — M90 Controlled Dataset Provenance

Status: LOCKED

## Decision

Controlled Dataset Provenance is the repository authority for the declared
generation procedure of a controlled experimental dataset. It preserves the
identity, generation record, provenance revision, generating conditions,
source references, generated-asset references, checksums, and temporal-origin
declaration required to reproduce and audit the dataset.

It does not own authoritative musical truth, catalogue validation assets,
execute validation, or preserve validation conclusions.

## Responsibility

Controlled Dataset Provenance owns:

- Controlled Dataset identity;
- Dataset Generation Record identity;
- provenance revision identity;
- the declared experimental generation procedure;
- known and explicitly unspecified generation conditions;
- the declared relationship between symbolic and sampled temporal origins;
- source and generated-asset references; and
- reproducibility limitations of the generation record.

Statements in a generation record must retain their Knowledge Model
classification. A declared procedure is not promoted to an Observed Fact by
agreement with file measurements.

## Ownership Boundaries

Ground Truth continues to own only authoritative musical truth derived from its
approved symbolic source. It never owns dataset generation procedure.

The Validation Catalog continues to own Validation Item identity, immutable
asset identity, catalogue metadata, licensing status, and references. It may
refer to a Controlled Dataset but never owns its generation procedure.

F-030 continues to govern preservation, traceability, revision, and scientific
record semantics. This decision supplies dataset-generation provenance and
does not replace those general rules.

The Scientific Validation Protocol continues to own validation execution.
Controlled Dataset Provenance does not perform analysis, comparison, or
validation.

## Temporal-Origin Declaration

The Dataset Generation Record owns an explicit declared relationship between
the symbolic source origin and generated sampled-asset origin. The declaration
does not require embedded WAV metadata and must remain classified as a
Declared Experimental Procedure rather than an Observed Fact.

## Reproducibility

A generation record preserves, when available:

- dataset and record identities;
- generation date;
- generating software and version;
- export and rendering configuration;
- sample rate, bit depth, and channel configuration;
- temporal-origin definition;
- source identities;
- generated-asset identities and checksums; and
- provenance revision.

Unavailable historical parameters are recorded explicitly as `not specified`.
They must not be inferred from repository presence, file metadata, or asset
compatibility. Such omissions are reproducibility limitations of the record.

## Canonical VAL-001 Record

The approved Controlled Dataset and its generation provenance are recorded in:

- `docs/scientific/controlled_datasets/CED-VAL-001.md`

## Governing References

- `docs/JGA_DEVELOPMENT_CONSTITUTION.md`
- `docs/scientific/foundations/JGA_KNOWLEDGE_MODEL.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`
- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`
