# JGA Project State

## M89 — PulseCandidate Strength Preservation

Status:

COMPLETED

- AD-032 restores the Translation observation-preservation invariant.
- Core `PulseCandidate.strength` is preserved unchanged in immutable Domain
  PulseCandidate representations.
- No downstream scientific or analytical semantics are introduced.
- Focused and real VAL-001 validation: 20 passed.
- Complete automated suite: 981 passed, 1 known environment-dependent Demucs
  MPS failure, 3 warnings.

## Current Branch

scientific/translation-layer-finalization

## Current Milestone

M42 — Scientific Visualization Evolution

Status:

COMPLETED

## Completed

### M42.1

- Scientific Visualization Semantics
- Multi-Trajectory Visualization
- ScientificVisualizationScene
- VisualizationTrajectoryDescriptor

### M42.2

- TemporalVisualizationWindow
- VisualPoint temporal contract
- TemporalVisualizationProjector
- DefaultTemporalVisualizationProjector
- VisualizationProjectionPipeline

### Consensus Layer Integration

- Ensemble Metric Consensus Layer operational
- DomainPulseCandidateAdapter introduced
- Core PulseCandidate → Domain PulseCandidate translation boundary
- Source identity propagation through:
  AudioStem → MetricSource → MetricContributor → Domain PulseCandidate
- VAL-001 to VAL-004 validation flows completed

## Validation

- 108 tests passed
- No architectural regressions

## Notes

The Visualization Layer now supports immutable,
composable projection stages operating on
ScientificVisualizationScene objects.

Real audio visualization validation is intentionally
deferred until the visualization layer supports
interactive temporal exploration.

------------------------------------------------------------
M33 — COMPLETE OBSERVATION MODEL
------------------------------------------------------------

Status:
IN PROGRESS

Architectural Direction

The project is evaluating the complete removal of the
Analysis Start Filtering mechanism.

Current hypothesis:

The complete observable audio signal shall always be
processed.

Metric Stability is considered an observable property
of the performance rather than a prerequisite for
analysis.

Architectural Decision

AD-021
Status: PROPOSED

Validation

VAL-001


------------------------------------------------------------
M35 — COMPLETE OBSERVATION MODEL
------------------------------------------------------------

Status

COMPLETED

Summary

AD-021 has been accepted.

The analytical pipeline now processes the complete
observable musical signal.

No component of the pipeline discards observations based
on an estimated analysis starting point.

Validation

926 tests passed.

VAL-001 passed.


------------------------------------------------------------
M81 — SCIENTIFIC VALIDATION ARCHITECTURE
------------------------------------------------------------

Status

IN PROGRESS

Completed

- AD-027 Immutable Analysis Representation approved and specified.
- Immutable boundary contract introduced between completed analysis and
  scientific validation.

Pending

- Validation comparator integration.

Validation

- Immutable Analysis Representation contract tests passed.
- VAL-001 scientific validation passed.
- Full suite: 925 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M83 — GROUND TRUTH LAYER
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-028 M83 Ground Truth Reference approved and specified.
- GT-VAL-001-v1 identity and VAL-001 binding preserved.
- Authoritative MusicXML identity and checksum enforced.
- Immutable time signature, tempo, section, instrumentation and minimum
  metric-position representations implemented.
- Pickup and full-measure identity mapping preserved.
- Original MusicXML and canonical instrument designations preserved.
- Ground Truth loader remains independent from analysis, runtime, Comparator
  and validation outputs.

Pending

- Ground Truth Comparator implementation under a separate approved decision.

Validation

- Ground Truth focused tests: 11 passed.
- Ground Truth plus VAL-001 scientific validation: 19 passed.
- Full suite: 936 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M84 — SCIENTIFIC VALIDATION CATALOG
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-029 Scientific Validation Catalog approved and specified.
- `JGA-VALIDATION-CATALOG-v1` introduced as an immutable asset catalogue.
- `VAL-001` established as the first Validation Item.
- M83 Ground Truth binding corrected from Validation Dataset identity to
  Validation Item identity.
- GT-VAL-001-v1, authoritative MusicXML and MP3 identities bound without
  duplicating Ground Truth content.
- Asset checksums and definitive repository revisions preserved.
- Licensing status preserved explicitly as `not_specified` for both assets.
- Existing observational `ValidationDataset` retained unchanged and
  scientifically distinct.

Pending

- Comparator and validation metrics under separate approved decisions.

Validation

- Validation Catalog plus Ground Truth focused tests: 21 passed.
- Validation Catalog, Ground Truth and VAL-001 scientific validation:
  29 passed.
- Full suite: 946 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M85 — SCIENTIFIC COMPARATOR
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-030 Scientific Comparator approved and specified.
- Immutable Analysis Representation schema revision `1` and typed
  validation-facing outputs recorded.
- `JGA-COMPARATOR-001` schema compatibility and mandatory bindings enforced.
- Tempo differences and incompatible beat-unit evidence preserved.
- Exact time-signature evidence preserved without scoring.
- Exact-name section correspondence and signed boundary/length differences
  preserved without inference.
- Instrument categories compared as sets without aggregate accuracy.
- Availability states preserved without value inference.
- Unique execution, result and evidence identities introduced.
- Comparator output remains immutable and suitable for a later Scientific
  Validation Record.

Pending

- Scientific metrics, tolerances, classifications and conclusions under
  separate approved decisions.

Validation

- Comparator and validation-boundary focused tests: 23 passed.
- Comparator through VAL-001 scientific validation: 52 passed.
- Full suite: 967 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.
