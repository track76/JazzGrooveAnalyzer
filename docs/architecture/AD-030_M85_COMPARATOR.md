# AD-030 — M85 Scientific Comparator

Status: LOCKED

## Scientific Protocol and Schema

Comparator protocol identity:

`JGA-COMPARATOR-001`

Comparator schema version:

`1`

The explicitly compatible input schemas are:

- Ground Truth schema `1`;
- Validation Item schema `1`; and
- Immutable Analysis Representation schema revision `1`.

Catalogue schema is not a Comparator input.

## Responsibility

The Comparator binds one Validation Item, one Immutable Analysis Representation
and one Ground Truth Model. It compares only approved quantities, preserves
differences and correspondence evidence, and produces an immutable result for a
later Scientific Validation Record.

It does not execute analysis, generate Ground Truth, normalize or repair inputs,
calculate accuracy, define tolerances, classify results, or produce conclusions.

## Approved Scope

M85 compares only:

- tempo;
- time signature;
- section boundaries and lengths; and
- instrumentation.

Pickup presence, normalized measure count, GroundTruthBeat and GroundTruthEvent
are outside M85 scope.

## Binding

Before comparison:

- Validation Item identity must equal Ground Truth Validation Item identity;
- Validation Item Ground Truth identity must equal Ground Truth identity; and
- analysis audio checksum must equal the Validation Item MP3 checksum.

Binding or schema failure stops comparison and produces no scientific
comparison evidence.

## Availability

Analysis outputs explicitly preserve one state:

- `PRESENT`;
- `EMPTY`;
- `NOT_PRODUCED`;
- `UNAVAILABLE`; or
- `OUT_OF_SCOPE`.

The Comparator preserves those states without inference. Comparator evidence
also defines `INCOMPATIBLE` for two present tempo values with different beat
units.

## Tempo

When beat units match, signed BPM difference is observed minus expected. The
evidence preserves expected, observed, signed and absolute differences in
`beats_per_minute`.

Different beat units produce `INCOMPATIBLE` evidence without normalization or a
numeric difference.

## Time Signature

The evidence preserves expected and observed beats and beat type with an exact
match flag. No numeric score is produced.

## Sections

Sections correspond only by exact canonical name.

- exactly one observed match: `MATCHED`;
- no observed match: `MISSING_EXPECTED`;
- multiple observed matches: `AMBIGUOUS_CORRESPONDENCE`;
- observed name absent from Ground Truth: `UNEXPECTED_OBSERVED`.

Matched start and length differences are observed minus expected. No section is
silently discarded and no equivalence is inferred from order, position,
similarity, neighbors or duration.

## Instrumentation

Canonical instrument categories are compared as sets. Evidence preserves
expected, observed, matching, missing and unexpected categories. Ordering has no
scientific meaning.

## Identity and Provenance

Every execution, complete result and evidence item has a unique identity.
Execution identity is distinct from scientific content equivalence.

Provenance preserves protocol, schemas and the bound Validation Item, Ground
Truth and analysis identities.

## Governing References

- `docs/architecture/AD-027_IMMUTABLE_ANALYSIS_REPRESENTATION.md`
- `docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`
- `docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`
- `docs/scientific/m81/M81_GROUND_TRUTH_MODEL.md`
