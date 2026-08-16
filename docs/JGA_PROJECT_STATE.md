# JGA Project State

## Declared Metric-Reference Vertical Slice

Status:

COMPLETED

- The analysis input may supply an immutable metric reference with explicit
  `DECLARED` origin, authority identity, source kind, SHA-256 identity and
  temporal scope.
- The controlled VAL-001 context supplies 78 quarter BPM from
  `GT-VAL-001-v1`; this value is contextual validation authority and is never
  represented as detected or inferred from audio.
- The declared reference crosses the existing Translation boundary and drives
  Domain beat-period and reconstructed-measure timing without entering or
  changing Core observation.
- Validation-facing immutable and analytical outputs preserve the declared
  origin and source identity. Without declared context, tempo and reconstructed
  measures are not produced; no silent 120 BPM fallback remains active.
- Autonomous BPM inference remains `DEFERRED`, not solved.
- Meter interpretation remains outside this milestone and is the next separate
  development item.
- Focused Domain, Translation, representation, reporting and controlled-audio
  validation: 593 passed.
- Complete automated suite excluding the environment-blocked Demucs integration
  test: 1043 passed, 3 warnings. The excluded test could not access the
  configured `JGA_EXTERNAL_ROOT`; no heavy write was attempted.

## M93 — Validation Dataset Generalization

Status:

COMPLETED

- AD-036 defines the operational generalization without changing scientific
  validation architecture or schemas.
- `recordings/validation/catalog.json` owns data-defined catalogue registration.
- MusicXML-adjacent `.ground_truth.json` data owns the existing Ground Truth
  identity, provenance and approved normalization values for each source.
- Repository loading verifies registered asset identities and materializes the
  existing immutable Validation Catalog and Ground Truth models.
- Complete validation execution selects a registered item by identity and
  composes the unchanged analysis materializer, Comparator and Scientific
  Validation Record boundaries.
- VAL-001 retains identical identities, checksums, Ground Truth content,
  availability states, Candidate Period population and scientific comparison
  behaviour.
- Focused operational and scientific regression validation: 56 passed.
- Complete automated suite: 1003 passed, 1 known environment-dependent Demucs
  MPS failure, 3 warnings.

## Phase II Validation Block 1

Status:

COMPLETED

- The completed block is summarized by
  `docs/scientific/PHASE_II_VALIDATION_BLOCK_1_COMPLETION_REPORT.md`.
- F-031 and F-032 provide the governing scientific foundations.
- H-VAL001-C1-03 and H-VAL001-C1-04 preserve the controlled experimental
  evidence.
- M91, M91.1 and M92 complete the minimum representation and production
  discovery responsibility supported by that evidence.
- The post-M92 Repository Authority Review found no remaining scientifically
  demonstrated insufficiency requiring implementation.
- No further implementation milestone is currently scientifically justified;
  future implementation requires new reproducible evidence demonstrating an
  actual insufficiency.

## M92 — Candidate Period Discovery

Status:

COMPLETED

- AD-035 defines the first production Candidate Period discovery rule.
- Input is limited to the existing filtered Core PulseCandidate population.
- Discovery preserves every exact consecutive positive frame interval
  occurring at least twice and every supporting adjacent observation pair.
- Frame length is explicit PulseCandidate observation/discovery configuration;
  no library default is recovered silently.
- The immutable CandidatePeriodPopulation is preserved on AnalysisContext
  immediately after filtering and does not feed or alter metric reconstruction.
- No selection, ranking, metric interpretation, phase, non-consecutive lag or
  cross-source candidate abstraction is introduced.
- Focused immutable/discovery validation: 19 passed.
- VAL-001 full mix and all five canonical WAV stems reproduce the complete
  accepted C1-03/C1-04 candidate inventories exactly.

## M91.1 — Candidate Period Representation Responsibility Correction

Status:

COMPLETED

- AD-034 now separates intrinsic Candidate evidence, runtime provenance and
  experimental-validation metadata.
- Experiment ID, validation run ID, validation protocol ID and repeated-run
  fingerprints are no longer mandatory Core representation fields.
- Asset identity and explicit discovery configuration preserve runtime
  traceability; source revision is retained only when available.
- Temporal unit remains population evidence. Frame length is not an intrinsic
  Candidate Period field and may only appear as explicit discovery
  configuration when a discovery procedure requires it.
- H-VAL001-C1-03 and H-VAL001-C1-04 retain their experimental identities and
  reproduction fingerprints in their F-030/SVP-001 records.
- Focused M91 compatibility validation: 12 passed.

## M91 — Scientific Representation of Candidate Periods

Status:

COMPLETED

- AD-034 places already-produced, pre-interpretive Candidate Period evidence
  in the existing Core observational representation location.
- The immutable representation preserves duration, recurrence occurrences,
  observation scope, provenance and reproducibility metadata only.
- It performs no discovery, generation, selection, consumption or metric
  interpretation.
- `H-VAL001-C1-03` is used only as controlled preserved evidence; its
  experiment-local recurrence protocol is not production authority.
- The current `MetricContext`, analysis pipeline, `BeatPeriodEstimator`,
  reconstruction path and validation schemas remain unchanged.
- Focused immutable-representation and preserved-evidence validation:
  10 passed for the VAL-001 full mix and five canonical WAV sources.
- Complete automated suite: 991 passed, 1 known environment-dependent Demucs
  MPS failure, 3 warnings.

## Phase II — Candidate Period Foundation

Status:

CANONICAL

- F-032 defines Recurrence, Candidate Period and Candidate Population.
- Its experimental basis is Campaign 1 experiment `H-VAL001-C1-03`.
- H-VAL001-C1-07 provides the experimental basis for the narrow
  cross-condition correspondence clarification: numerical proximity after a
  controlled transformation is insufficient without an explicitly justified,
  measurement-condition-aware criterion. No such criterion is defined.
- Candidate Periods remain observation-derived and pre-interpretive.
- Blind discovery remains independent from post-blind Ground Truth evaluation.
- No candidate selection, metric interpretation, architecture or implementation
  is introduced.

## Phase II — Hierarchical Metric Periodicity Foundation

Status:

CANONICAL

- F-031 defines observation-derived periodicity, candidate period, metric
  level, metric interpretation, metric reconstruction and hierarchical metric
  periodicity.
- Observation remains free of musical interpretation under AD-006.
- Metric-level interpretation remains owned by the Domain under AD-008.
- Observable Metric Context preserves temporal evidence and organization but
  does not identify meter, tempo, ensemble Pulse or metric level.
- The authoritative `ElementaryMetricEvent → BeatReference → MetricCluster →
  Pulse → InternalMetricTimeline` lineage remains unchanged.
- No production architecture, implementation, validation schema, metric,
  tolerance or algorithm is introduced.

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


------------------------------------------------------------
M86 — END-TO-END SCIENTIFIC VALIDATION
------------------------------------------------------------

Status

COMPLETED

Completed

- Completed Analysis to Immutable Analysis Representation materialization
  boundary implemented for schema revision `1`.
- Real VAL-001 audio checksum, execution provenance, configuration,
  completeness, limitations and deterministic content fingerprint preserved.
- Current pipeline defaults excluded from scientific outputs; all four scoped
  quantities are explicitly represented as `NOT_PRODUCED`.
- Runtime state does not escape the deeply immutable representation.

Validation

- Materializer and immutable-boundary focused tests: 12 passed.
- Materializer through VAL-001 comparison validation: 58 passed.
- Full suite: 973 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M87 — SCIENTIFIC VALIDATION RECORD
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-031 Scientific Validation Record approved and specified.
- Immutable preservation of Comparator evidence, result and input provenance
  implemented.
- Validation Item, Ground Truth, analysis execution, Comparator execution,
  protocol and schema identities preserved.
- Analysis limitations and all Comparator availability states preserved.
- Deterministic record identity and SHA-256 content fingerprint implemented.
- Identity and content binding enforced before record creation.
- Real VAL-001 end-to-end chain completed through the Scientific Validation
  Record without metrics, tolerances, classification or conclusions.

Validation

- Scientific Validation Record focused and real-chain tests: 7 passed.
- M87 boundary through VAL-001 scientific validation: 65 passed.
- Full suite: 980 passed; one pre-existing Demucs/MPS environment integration
  test could not execute successfully because its configured backend requires
  macOS 14 or later.


------------------------------------------------------------
M90 — CONTROLLED DATASET PROVENANCE
------------------------------------------------------------

Status

COMPLETED

Completed

- AD-033 Controlled Dataset Provenance approved and specified.
- `CED-VAL-001`, `DGR-CED-VAL-001-001` and `PR-CED-VAL-001-001`
  established as canonical identities.
- Five authoritative controlled WAV stems preserved by repository-relative
  identity and SHA-256 checksum.
- PCM format, 24-bit depth, 44.1 kHz sample rate, stereo channel configuration,
  sample count and duration preserved as measured Observed Facts.
- Dataset generation and MusicXML-score-time-zero to WAV-sample-zero alignment
  preserved explicitly as Declared Experimental Procedure.
- Unavailable date, software-version and rendering details preserved as
  `not specified` without inference.
- Obsolete MP3 stems excluded from the canonical controlled dataset.
- Ground Truth, Validation Catalog, validation execution and F-030 ownership
  boundaries remain unchanged.

Validation

- Controlled asset identities, checksums and measured format verified against
  all five repository WAV assets.
- M85 focused validation: 23 passed.
- M86 focused validation through the Comparator boundary: 29 passed.
- M87 focused and real VAL-001 chain validation: 7 passed.
- Full suite: 981 passed, one known Demucs/MPS environment integration failure,
  and three warnings. The configured MPS backend requires macOS 14 or later.
