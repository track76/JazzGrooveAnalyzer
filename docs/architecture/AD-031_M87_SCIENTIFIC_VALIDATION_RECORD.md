# AD-031 — M87 Scientific Validation Record

Status: LOCKED

## Decision

The Scientific Validation Record is the permanent, immutable scientific record
of one completed validation execution. It materializes an existing immutable
Comparator Result without executing or modifying comparison.

The matching Immutable Analysis Representation is supplied only to verify its
execution identity and content fingerprint and to preserve its declared
limitations. No runtime object is accepted or retained.

## Preserved Evidence

The record preserves by reference:

- Validation Item and Ground Truth identities;
- Immutable Analysis Representation execution identity and content
  fingerprint;
- Comparator execution, result, protocol and schema identities;
- complete Comparator input provenance;
- the complete immutable Comparison Result, including evidence and availability
  states; and
- Immutable Analysis Representation limitations.

The record identity is `JGA-SVR-` followed by its deterministic SHA-256 record
fingerprint. The fingerprint is calculated from the canonical immutable record
content and therefore remains stable for the same completed comparison
execution and matching analysis representation.

## Binding

Record materialization stops if either the analysis execution identity or
analysis content fingerprint differs from the values preserved by Comparator
provenance. No record is produced for mismatched inputs.

## Exclusions

The boundary does not execute analysis or comparison, modify any input,
calculate metrics or accuracy, define tolerances, classify change, or infer
scientific conclusions.

## Dependencies

The record boundary depends only on the immutable Comparator Result and the
Immutable Analysis Representation contract. It has no Ground Truth, Validation
Catalog, runtime pipeline, metric, or reporting dependency.

## Governing References

- `docs/architecture/AD-027_IMMUTABLE_ANALYSIS_REPRESENTATION.md`
- `docs/architecture/AD-030_M85_COMPARATOR.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
