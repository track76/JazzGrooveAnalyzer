# AD-027 — Immutable Analysis Representation

Status: LOCKED

## Context

Scientific validation requires a stable representation of one completed blind
JGA analysis.

The runtime `AnalysisContext` is mutable shared execution state. Direct
consumption of that state by validation would couple the Validation Layer to
runtime orchestration and would not satisfy the requirement that validation
compare immutable representations.

Existing scientific results remain authoritative for their respective layers,
but no existing contract defines the immutable boundary between completed
analysis and validation.

## Decision

The Immutable Analysis Representation is the canonical boundary between one
completed JGA analysis and the Scientific Validation Layer.

It is a frozen scientific representation of the analysis outputs required by
the declared validation scope. It is not a runtime object, `AnalysisContext`,
Ground Truth, a Validation Record, or a complete pipeline snapshot.

The analysis side owns the represented scientific content and provenance. The
Validation Layer consumes the representation without modifying it. Ground
Truth remains independently owned by the Ground Truth Layer.

## Scientific Responsibility

The representation exposes only:

- the smallest set of completed analysis outputs required by the declared
  validation scope;
- identity and provenance required for reproducibility and traceability;
- explicit completeness, absence and limitation information; and
- stable integrity information.

It contains no expected values, Ground Truth, comparisons, accuracy measures,
validation classifications or conclusions.

## Lifecycle

The representation becomes available only after blind analysis is complete and
the selected outputs have been captured consistently.

It has no mutable or partially initialized state. Correction, enrichment,
migration or re-extraction produces a new representation. The original remains
unchanged.

## Identity

Each representation identifies exactly one analysis execution. Its identity is
distinct from content equivalence, dataset identity, validation-run identity,
Ground Truth identity and report identity.

The contract preserves:

- analysis-execution identity;
- input-audio content identity and checksum;
- source revision and pipeline version;
- effective analysis configuration;
- boundary-schema revision; and
- a deterministic content fingerprint.

## Immutability

Immutability is deep and transitive. No exposed collection, nested scientific
value, provenance value or external artifact reference may depend on mutable
runtime state.

The representation never exposes `AnalysisContext` or another live runtime
object.

## Scientific Outputs

The first approved validation-facing schema revision is `1`.

For M85, the representation exposes only these typed canonical outputs with
explicit availability:

- `tempo`;
- `time_signature`;
- `sections`; and
- `instrumentation`.

Their contracts are defined by
`docs/architecture/AD-030_M85_COMPARATOR.md`. They do not expose runtime
objects.

Scientific outputs are conditional on the declared validation scope. A result
from an analysis stage is included only when required for validation,
reproducibility, traceability or scientific evidence preservation.

The contract distinguishes an observed empty result from an output that was not
produced, unavailable, failed or outside the declared scope.

## Dependencies

Permitted dependencies are canonical completed scientific values, stable
provenance concepts, schema definitions, measurement units and stable artifact
identities.

Dependencies on runtime orchestration, mutable runtime state, Ground Truth,
comparators, validation criteria, validation records, validation reports,
exporters or persistence mechanisms are forbidden.

The dependency direction is:

Completed Analysis

↓

Immutable Analysis Representation

↓

Scientific Validation

## Traceability

The representation preserves the temporal reference and measurement units
needed to interpret included values, the completeness state of scoped outputs,
scientifically relevant limitations, and stable identities and checksums for
referenced evidence artifacts.

Evidence lineage is included only where required to validate the declared
scientific claim. It shall not be used to duplicate the complete execution
pipeline.

## Consequences

The Scientific Validation Layer no longer requires mutable `AnalysisContext` as
comparison input.

Ground Truth comparison, baseline comparison, difference classification and
validation-record preservation remain separate validation responsibilities.

## Governing References

- `docs/JGA_DEVELOPMENT_CONSTITUTION.md`
- `docs/scientific/JGA_SCIENTIFIC_VALIDATION_PROTOCOL.md`
- `docs/scientific/foundations/JGA_KNOWLEDGE_MODEL.md`
- `docs/scientific/foundations/F-030_SCIENTIFIC_KNOWLEDGE_RECORD.md`
- `docs/scientific/m81/M81_GROUND_TRUTH_MODEL.md`
