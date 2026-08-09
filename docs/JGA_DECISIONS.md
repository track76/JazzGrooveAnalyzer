# Jazz Groove Analyzer (JGA)

# Architectural Decisions Register

This document records every architectural decision that is considered stable and approved.

Once a decision is marked as **LOCKED**, it shall not be reconsidered unless explicitly superseded by a newer decision.

---

# AD-001

## Title

JGA as a Scientific Framework

**Status:** LOCKED

### Decision

The Jazz Groove Analyzer (JGA) is developed as a scientific framework rather than a conventional audio analysis application.

---

# AD-002

## Title

Repository as Source of Truth

**Status:** LOCKED

### Decision

The repository is the single source of truth.

Documentation and implementation shall always be verified against the repository before introducing changes.

---

# AD-003

## Title

Core Independence

**Status:** LOCKED

### Decision

The Core shall remain completely independent from any data acquisition technology.

---

# AD-004

## Title

Logical Core Input

**Status:** LOCKED

### Decision

The logical input of the Core is an `AudioStemCollection`.

The Core shall never depend directly on audio recordings or acquisition mechanisms.

---

# AD-005

## Title

Acquisition Layer

**Status:** LOCKED

### Decision

Audio loading, source separation and every data acquisition mechanism belong to the Acquisition Layer.

The Acquisition Layer is external to the Core.

---

# AD-006

## Title

Observation Layer

**Status:** LOCKED

### Decision

The Observation Layer represents observable physical phenomena extracted from the signal.

It performs no musical interpretation.

---

# AD-007

## Title

DSP Layer

**Status:** LOCKED

### Decision

The DSP Layer transforms and analyses observations without introducing musical semantics.

---

# AD-008

## Title

Domain Layer

**Status:** LOCKED

### Decision

The Domain Layer is responsible for musical interpretation.

Only the Domain may infer musical entities from observations.

---

# AD-009

## Title

Beat Reference

**Status:** LOCKED

### Decision

The Beat Reference is an emergent property of the ensemble.

It shall never be imposed externally.

---

# AD-010

## Title

Pipeline Responsibility

**Status:** LOCKED

### Decision

The Analysis Pipeline orchestrates the processing stages.

It contains no musical logic.

---

# AD-011

## Title

Development Methodology

**Status:** LOCKED

### Decision

Every development step shall follow this workflow:

1. Architecture
2. Repository verification
3. Design
4. Implementation
5. git diff
6. pytest
7. Commit
8. Push

---

# AD-012

## Title

Repository Discipline

**Status:** LOCKED

### Decision

No unnecessary refactoring.

One architectural change at a time.

Every commit must preserve a green test suite.

---

# AD-013

## Title

AudioStemCollection as Core Input

**Status:** LOCKED

### Decision

The logical input of the JGA Core is an AudioStemCollection.

The Acquisition Layer is responsible for producing the AudioStemCollection before handing control to the Core.

The Core never depends directly on audio recordings or source separation technologies.

---

# AD-014

## Title

Core Computational Model

**Status:** LOCKED

### Decision

The Core contains computational objects required by the analysis engine.

Core objects represent computational state and processing structures.

The Domain represents musical knowledge and semantic interpretation.

Although similarly named concepts may exist in both layers, they have different responsibilities.

The Core must not implement musical semantics.

The Domain must remain independent from DSP and signal-processing implementation details.

No direct dependency between Core and Domain is allowed.

---

# AD-015

## Title

Metric Source Identity Preservation

**Status:** LOCKED

### Decision

Every observable rhythmic event that contributes to the Metric Context shall preserve its originating Metric Source throughout the Core computational lifecycle.

The SourcePulseSequence shall maintain the identity of the MetricSource associated with its observable events.

The Translation Layer shall consume this preserved source information without reconstructing or inferring source identity.

### Consequence

The lifecycle preserves source provenance:

MetricSource

↓

SourcePulseSequence

↓

PeriodicitySegment

↓

MetricSegment

↓

MetricContext

↓

τ₈

↓

Domain Objects


# AD-015

## Title

Real Audio Validation Requirement

**Status:** LOCKED

### Decision

Every implementation that introduces, modifies or connects components of the JGA pipeline shall be validated through at least one real audio file test before being considered complete.

Unit tests verify local component correctness.

Real audio validation verifies the coherence of the complete computational chain.

### Consequence

The development workflow becomes:

1. Theory
2. Architecture
3. Implementation
4. Unit Tests
5. Real Audio Validation
6. Commit

### Scientific Motivation

The JGA analysis chain transforms continuous audio through multiple
architectural boundaries:

Audio Signal

↓

Observation Model

↓

Computational Representations

↓

Translation Boundary

↓

Domain Model

A component may be locally correct while producing inconsistencies
when integrated into the complete pipeline.

Real audio validation is therefore required to verify:

- information preservation;
- architectural compatibility;
- absence of implicit assumptions;
- correct behaviour of the complete analysis pipeline.


# AD-014

## Title

MetricContributor Resolution Boundary

**Status:** LOCKED

### Decision

The resolution between observable musical sources and metric contributors
belongs exclusively to `MetricContributorResolver`.

The mapping chain is:

SoundSource.id

↓

MetricContributor.sound_source_id

↓

MetricContributor.id


`PulseCandidate` shall preserve the originating `SoundSource` identity.

`ElementaryMetricEvent` shall reference the resolved `MetricContributor`
identity.

No component shall bypass this resolution step.


---

# AD-015

## Title

Architectural Output/Input Contract Validation

**Status:** LOCKED

### Decision

Every architectural component shall produce an output formally compatible
with the declared input contract of the following component.

Implicit transformations between architectural layers are forbidden.

Each transition shall explicitly define:

- input representation;
- output representation;
- responsible transformation;
- traceability to the previous layer.

Example:

MetricContext

↓

τ₈ Representation Translation

↓

Domain PulseCandidate

↓

MetricContributor Resolution

↓

ElementaryMetricEvent


No component may bypass an intermediate semantic layer.

---

# AD-016 — Scientific Geometric Plane

## Status

LOCKED

## Context

M17 introduces the scientific geometric framework of the Jazz Groove Analyzer.

The project requires a geometric representation that remains scientifically
interpretable and directly traceable to observable musical facts.

## Decision

The scientific geometry of the Jazz Groove Analyzer is defined on a
two-dimensional plane (XY).

Each axis shall represent exactly one validated observable quantity.

No axis may represent an arbitrary mathematical construct.

A third coordinate shall not be introduced unless supported by a future
scientific theory and an independent architectural decision.

## Consequences

- Scientific Geometry is defined on the XY plane.
- Every coordinate remains independently observable.
- Representation remains simple and scientifically interpretable.
- Future extensions require scientific validation before implementation.


------------------------------------------------------------
AD-016
Scientific Behaviour Space
------------------------------------------------------------

Status:
LOCKED

Decision

The Behaviour Geometry layer shall represent observable behaviours inside a
Scientific Behaviour Space.

The Behaviour Space is a scientific mathematical representation rather than
a visualization layer.

All future behavioural analyses shall operate on this representation.

Rationale

Separating Behaviour Space from graphical visualization preserves the
scientific independence of the analytical model.


------------------------------------------------------------
AD-017
Behaviour Space Invariants
------------------------------------------------------------

Status:
LOCKED

Decision

The Scientific Behaviour Space shall preserve:

- cardinality
- temporal ordering
- deterministic projection
- immutability
- scientific traceability

These invariants are mandatory for every future Behaviour Space
implementation.


------------------------------------------------------------
AD-018

Behaviour Distance Vector

Status

LOCKED

Decision

Behaviour comparison shall never be reduced to a single
measurement.

Every comparison is represented by a scientific vector whose
components remain individually observable.

Scalar indicators may be derived afterwards.

The vector remains the primary scientific representation.


------------------------------------------------------------
AD-019

Behaviour Space Geometry

Status

LOCKED

Decision

Scientific Behaviour Spaces are compared as complete
trajectories.

No comparison shall be performed using isolated Behaviour
Points only.


------------------------------------------------------------
AD-020

Behaviour Scan First

Status

LOCKED

Decision

Behaviour evolution shall always be observed before
computing any quantitative comparison.

Behaviour Distance is a derived scientific quantity.

Behaviour Change Events are primary observations.


------------------------------------------------------------
AD-021

Observation Before Diagnosis

Status

LOCKED

Decision

Behaviour observations shall always be preserved.

Diagnostic information shall be added without modifying
the original observations.

No observation may be removed from the scientific record.


------------------------------------------------------------
AD-021

Observation Before Diagnosis

Status

LOCKED

Decision

Every Behaviour Observation Frame shall be preserved.

Diagnostic components may enrich observations but shall
never modify or remove them.

The complete observation history constitutes the scientific
record of the analysed performance.


------------------------------------------------------------
AD-022

Observation Builder

Status

LOCKED

Decision

Behaviour Observation Frames shall always be generated from
Scientific Behaviour Space.

The builder performs no scientific interpretation.


------------------------------------------------------------
AD-023

Behaviour Diagnostics Layer

Status

LOCKED

Decision

Behaviour Diagnostics analyses Observation Frames.

It never accesses Scientific Behaviour Space directly.


------------------------------------------------------------
AD-024

Behaviour Diagnostics Independence

Status

LOCKED

Decision

Behaviour Diagnostics operates exclusively on
Behaviour Observation Frames.

No dependency on previous scientific layers is permitted.


------------------------------------------------------------
AD-018 — Analytical Score as Primary Scientific Representation
Status
LOCKED
------------------------------------------------------------

Decision

The Analytical Score is the primary scientific
representation produced by the Jazz Groove Analyzer.

All visual outputs shall derive from the same
Analytical Score model.

Examples include:

- PDF Reports
- Interactive GUI
- Scientific Publications
- Presentation Material

The rendering system shall never reconstruct
scientific information.

It shall only visualize information already
contained in the Analytical Score domain model.

------------------------------------------------------------

Scientific Principle

The Internal Timing reconstructed by JGA is the
absolute temporal reference.

Every observed musical event shall be represented
with respect to the reconstructed Internal Timing.

No observed event shall be omitted.

No averaging shall replace the original
observations in the primary representation.

------------------------------------------------------------

Representation Principle

The Analytical Score follows the grammar of a
musical score while representing temporal
behaviour instead of musical notation.

Each bar shall contain:

- Bar Number
- Musical Time
- Time Signature
- Internal BPM

Each instrument shall occupy one dedicated row.

Each detected event shall display:

- Event Position
- Offset from Internal Timing (ms)

Significant variations may be highlighted,
but every observation shall remain visible.

------------------------------------------------------------

Future Extensions

The Analytical Score shall support:

- Instrument Behaviour Graphs
- Internal BPM Evolution
- Ensemble Behaviour Analysis
- Scientific PDF Export
- Interactive Visualization


------------------------------------------------------------

# AD-016

## Temporal Continuity Connectivity Rule

**Status:** LOCKED

### Context

M5 Behaviour Analysis introduces quantitative Behaviour
Descriptors derived from validated BehaviourObservation objects.

The TemporalContinuity Descriptor (D-001) requires a
deterministic definition of temporal connectivity.

### Decision

Temporal connectivity is determined from the ordered Pulse
indices contained in the Internal Metric Timeline.

A Pulse is considered connected when its index is consecutive
with respect to the previous Pulse.

For the TemporalContinuity Descriptor:

```
N = total number of Pulses in the BehaviourObservation

C = number of Pulses belonging to the longest consecutive
    Pulse index sequence

TemporalContinuity = C / N
```

### Rationale

This definition:

- uses only validated Domain information;
- introduces no additional observable variables;
- preserves determinism and reproducibility;
- respects the mathematical specification M-001;
- avoids musical interpretation.

### Consequences

The implementation of D-001 shall compute the descriptor from
Pulse index continuity and shall not introduce alternative
connectivity models without a new architectural decision.

------------------------------------------------------------

------------------------------------------------------------

# AD-017

## Behaviour Quantification Input Contract

**Status:** LOCKED

### Context

M5 Behaviour Analysis introduces quantitative Behaviour
Descriptors derived from validated Behaviour representations.

Some descriptors require analytical results produced by
previous stages, such as Metric Stability from M4.

Passing these values implicitly would break layer separation.

### Decision

Behaviour Quantification shall operate on an explicit
BehaviourQuantificationContext.

The context shall contain:

- BehaviourProfile
- validated metric analysis outputs required by descriptors

M4 produces analytical measurements.

M5 transforms validated measurements into Behaviour
Descriptors.

### Rationale

This decision:

- preserves M4/M5 separation;
- avoids recalculation of metric properties;
- keeps descriptors deterministic;
- supports future descriptors requiring additional
  validated inputs.

### Consequences

New Behaviour Descriptors shall declare their required inputs
through the BehaviourQuantificationContext contract.

------------------------------------------------------------

# AD-018

## Musical Function Separation

**Status:** LOCKED

### Context

M25 Ensemble Understanding introduces the interpretation
of musical roles performed by observed sources inside an
ensemble.

Previous layers determine the identity of observed sources
through InstrumentClassification.

Instrument identity and musical function represent different
concepts and must not be merged.

### Decision

InstrumentClassification and MusicalFunction assignment
shall remain separate architectural layers.

InstrumentClassification describes the observed sound source.

MusicalFunction describes the role performed by that source
inside the ensemble context.

Musical function assignment shall be implemented by a
dedicated service operating after Source Understanding.

### Rationale

This decision:

- preserves separation between observation and interpretation;
- avoids coupling instrument identity with musical role;
- allows the same instrument to perform different functions;
- maintains deterministic and explainable analysis;
- preserves the scientific layered architecture.

### Consequences

InstrumentClassification shall not contain musical role data.

New ensemble interpretation components shall operate on
validated ObservedSource information.

MusicalFunction assignment shall produce higher-level
ensemble representations without modifying lower layers.

------------------------------------------------------------

# AD-019

## EnsembleProfile Domain Ownership

**Status:** LOCKED

### Context

M25 Ensemble Understanding requires a representation of the
musical state of an ensemble.

A domain-level EnsembleProfile already exists and contains
musical context information such as sound sources,
musical functions and metric contributors.

A second reduced EnsembleProfile representation exists inside
Source Understanding and only describes instrument families.

These two objects represent different abstraction levels.

### Decision

The official EnsembleProfile model belongs to the Domain Layer.

Source Understanding shall not define an independent
EnsembleProfile entity.

Source Understanding outputs ObservedSourceCollection.

Higher-level ensemble interpretation shall produce the
domain EnsembleProfile.

### Rationale

This decision:

- preserves layer separation;
- avoids duplicated domain concepts;
- keeps Source Understanding focused on observation;
- keeps musical interpretation inside higher-level layers.

### Consequences

The Source Understanding EnsembleProfile representation
shall be migrated or removed.

All future ensemble interpretation components shall use:

jga.domain.ensemble_profile.EnsembleProfile

as the authoritative model.

------------------------------------------------------------

# AD-020

## Source Musical Function Assignment Model

**Status:** LOCKED

### Context

M25 Ensemble Understanding requires assigning musical
functions to observed sound sources.

A MusicalFunction alone does not describe which source
performs that function.

The relationship between a SoundSource and a MusicalFunction
must therefore be explicitly represented.

### Decision

The assignment between SoundSource and MusicalFunction shall
be represented as an explicit domain relationship.

MusicalFunction shall not be stored as an unassociated list.

The model shall preserve:

- source identity;
- assigned musical function;
- assignment confidence;
- assignment rationale.

### Rationale

This decision:

- preserves contextual meaning;
- avoids losing source/function relationships;
- supports explainable ensemble interpretation;
- maintains domain consistency.

### Consequences

M25 implementation shall introduce an explicit assignment
model before building EnsembleProfile generation.

------------------------------------------------------------

# AD-021

## Rule Based Musical Function Assignment Contract

**Status:** LOCKED

### Context

The existing musical function assignment service produced
MusicalFunction objects directly from SoundSource names.

This approach loses the explicit relationship between a source
and its assigned musical function.

### Decision

Musical function assignment shall produce
SourceMusicalFunctionAssignment objects.

Assignments shall preserve:

- source identity;
- assigned function;
- confidence;
- rationale.

Function inference shall use validated source information
and deterministic rules.

Source names shall not be used as the primary classification
mechanism.

### Rationale

This decision:

- respects AD-020;
- preserves explainability;
- avoids hidden assumptions;
- maintains layer separation.

### Consequences

RuleBasedMusicalFunctionAssignmentService shall return
explicit source/function assignments.

------------------------------------------------------------

# AD-022

## EnsembleProfile Source Function Assignment Integration

**Status:** LOCKED

### Context

M25 introduces explicit relationships between sound sources
and their assigned musical functions through
SourceMusicalFunctionAssignment.

The existing EnsembleProfile already contains musical
functions but does not preserve the explicit relationship
between each source and its function.

### Decision

EnsembleProfile shall include explicit source/function
assignment information through
SourceMusicalFunctionAssignment.

Existing musical_functions information shall be preserved.

The new assignment relationship becomes the authoritative
representation of source-role association.

### Rationale

This decision:

- preserves backward compatibility;
- respects AD-020;
- avoids losing source/function relationships;
- keeps EnsembleProfile as the ensemble context container.

### Consequences

EnsembleProfile shall contain:

- sound sources;
- musical functions;
- source musical function assignments;
- metric contributors.

Future ensemble analysis shall use the explicit assignment
relationship when source-role information is required.

------------------------------------------------------------

# AD-023

## Ensemble Understanding Service Input Contract

**Status:** LOCKED

### Context

M25 introduces the interpretation of observed sources into
ensemble-level musical roles.

Source Understanding already produces
ObservedSourceCollection containing instrument observations.

Ensemble Understanding must not repeat source observation
or instrument classification.

### Decision

The Ensemble Understanding Service shall receive
ObservedSourceCollection as its input.

The service shall translate observed sources into domain
entities and produce EnsembleProfile.

Source identification and instrument classification remain
outside the Ensemble Understanding layer.

### Rationale

This decision:

- preserves layer separation;
- avoids duplicated interpretation;
- keeps Source Understanding observational;
- keeps Ensemble Understanding contextual.

### Consequences

The M25 flow becomes:

ObservedSourceCollection
        ↓
EnsembleUnderstandingService
        ↓
EnsembleProfile

------------------------------------------------------------

# AD-024

## EnsembleAnalysisResult Assignment Relationship Ownership

**Status:** LOCKED

### Context

M25 introduces explicit source/function relationships through
SourceMusicalFunctionAssignment.

The existing EnsembleAnalysisResult contains separate
collections of SoundSource and MusicalFunction.

This representation does not preserve the relationship
between a source and its assigned function.

### Decision

EnsembleAnalysisResult shall include
SourceMusicalFunctionAssignment information.

The assignment relationship becomes the authoritative
representation of source-role association.

Existing musical_functions information shall be preserved
for compatibility with previous analysis stages.

### Rationale

This decision:

- preserves explicit relationships;
- avoids information loss between layers;
- maintains backward compatibility;
- aligns A0 analysis output with EnsembleProfile.

------------------------------------------------------------

# AD-025

## Metric Contributor Assignment Input Contract

**Status:** LOCKED

### Context

M25 introduces explicit source/function relationships through
SourceMusicalFunctionAssignment.

Metric contributor assignment previously consumed isolated
MusicalFunction objects.

This loses the explicit relationship between source and
musical role.

### Decision

MetricContributorAssignmentService shall consume
SourceMusicalFunctionAssignment objects.

Metric contribution inference shall use the assigned
musical function contained in the relationship.

### Rationale

This decision:

- preserves source/function traceability;
- avoids detached musical functions;
- aligns metric analysis with AD-021;
- keeps contributor assignment deterministic.

### Consequences

The A0 analysis flow becomes:

SoundSource
        ↓
SourceMusicalFunctionAssignment
        ↓
MetricContributor

------------------------------------------------------------

# AD-026

## Musical Function Assignment Result Contract

**Status:** LOCKED

### Context

M25 introduced explicit source/function relationships through
SourceMusicalFunctionAssignment.

The assignment entity contains only the relationship
identifiers and does not contain the MusicalFunction
definition.

The current assignment service creates relationships without
preserving the assigned MusicalFunction objects.

### Decision

MusicalFunction assignment shall return an explicit result
containing:

- MusicalFunction objects;
- SourceMusicalFunctionAssignment objects.

The result shall preserve the relationship between each
SoundSource and its assigned MusicalFunction.

### Rationale

This decision:

- avoids detached function identifiers;
- preserves domain traceability;
- provides complete input for metric contributor analysis;
- maintains deterministic interpretation.

### Consequences

The ensemble analysis flow becomes:

SoundSource

↓

MusicalFunctionAssignmentResult

↓

SourceMusicalFunctionAssignment

↓

MetricContributor

------------------------------------------------------------

------------------------------------------------------------
Architectural Review — M25.7
------------------------------------------------------------

Result

No new Architectural Decision identified.

Current architecture remains consistent with:

AD-019
AD-020
AD-021
AD-022
AD-023
AD-024
AD-025
AD-026

Next step

Verify implementation against existing contracts before
continuing development.


-------------------------------------------------------------------------------
AD-016 — Visualization Projection Pipeline
-------------------------------------------------------------------------------

Status:
LOCKED

Date:
2026-08-02

Context

The Visualization Layer evolved from rendering a single
VisualTrajectory into supporting immutable transformations
over complete ScientificVisualizationScene objects.

Temporal visualization introduced the need to apply one or
more visualization transformations before rendering while
preserving scientific meaning.

Decision

Introduce the VisualizationProjectionPipeline.

The pipeline applies one or more visualization projectors
sequentially.

Each projector:

    ScientificVisualizationScene
            ↓
    ScientificVisualizationScene

The pipeline performs only visualization-level
transformations.

It must never:

- modify scientific meaning;
- infer musical semantics;
- access Domain objects directly.

Consequences

- composable visualization transformations;
- immutable visualization workflow;
- renderer independence;
- explicit input/output contracts;
- additive future extensions
  (temporal navigation, zoom, viewport,
   trajectory filtering, etc.).


---

## AD-016 — Ensemble Metric Consensus Layer

Status:
LOCKED

Date:
2026-08-07

---

### Context

JGA reconstructs metric behaviour from observable audio evidence.

A PulseCandidate represents a temporal event detected from an
individual sound source.

A PulseCandidate is not necessarily a beat.

The metric reference must emerge from the temporal relationship
between multiple contributing sources.

---

### Problem

The current observation-to-domain transition preserves source
provenance but does not explicitly model collective temporal
consensus.

Direct translation of isolated PulseCandidates may confuse
individual source activity with ensemble metric behaviour.

---

### Decision

Introduce an Ensemble Metric Consensus Layer between the
Observation Model and the τ8 Translation Layer.

The component receives:

- PulseCandidate sequences
- MetricContributor information

and produces:

- EnsembleMetricEvent sequences

---

### Input Representation

PulseCandidate:

- sound_source_id
- timestamp
- confidence


MetricContributor:

- sound_source_id
- musical_function_id
- active

---

### Output Representation

EnsembleMetricEvent:

- collective temporal position
- contributing metric sources
- confidence value

---

### Responsibilities

The Ensemble Metric Consensus Layer:

- aligns temporal events from multiple sources;
- groups compatible temporal observations;
- estimates collective metric events;
- preserves source contribution information.

---

### Non Responsibilities

The Ensemble Metric Consensus Layer does not:

- determine time signature;
- receive BPM metadata;
- receive musical labels;
- identify groove style;
- introduce external musical knowledge.

---

### Scientific Principle

The metric pulse is an emergent property of the temporal
interaction between multiple musical sources.

A beat is not assigned to one source.

A beat is reconstructed from collective temporal evidence.


---

## AD-016 — Source-level Pulse Extraction before Ensemble Metric Consensus

### Status

LOCKED

### Context

The Ensemble Metric Consensus Layer requires independent temporal
evidence from multiple Metric Sources.

The current PulseCandidateBuilder operates on the global processed
audio signal and produces ensemble-level PulseCandidates.

Duplicating these PulseCandidates into multiple SourcePulseSequence
objects would create artificial source agreement and would not
represent independent rhythmic behaviour.

### Decision

Introduce a source-level pulse extraction boundary before the
Ensemble Metric Consensus Layer.

Each MetricSource must provide an independent
SourcePulseSequence generated from its own audio representation.

### Updated Flow

AudioStemCollection

↓

Source-level Pulse Extraction

↓

SourcePulseSequence

↓

MetricContext

↓

EnsembleMetricConsensus

↓

EnsembleMetricEvent

### Input Representation

AudioStem:

- source identity
- isolated audio signal

### Output Representation

SourcePulseSequence:

- MetricSource identity
- source-specific PulseCandidates

### Non Responsibilities

Source-level Pulse Extraction does not:

- determine beat;
- determine meter;
- estimate BPM;
- create BeatReference;
- introduce musical interpretation.

### Scientific Principle

Ensemble metric behaviour emerges from the temporal interaction
of independent observable rhythmic sources.

Consensus requires independent evidence.


---

## AD-017 — DummyMultiStemSeparator Limitation

### Status

LOCKED

### Context

The Ensemble Metric Consensus Layer requires independent
temporal evidence produced by multiple observable rhythmic
sources.

The current DummyMultiStemSeparator creates multiple
AudioStem objects but does not perform source separation.

All generated stems currently contain the same audio signal.

Example:

AudioStem("Bass").signal
=
AudioStem("Ride").signal
=
AudioStem("Kick").signal

### Decision

The DummyMultiStemSeparator is considered a structural
placeholder only.

It may be used to validate:

- pipeline contracts;
- source identity propagation;
- data flow;
- architectural integration.

It must not be used to validate:

- source independence;
- ensemble metric consensus;
- emergent rhythmic behaviour.

### Scientific Consequence

A valid Ensemble Metric Consensus validation requires:

- independent temporal observations;
- independent PulseCandidate sequences;
- observable differences between Metric Sources.

### Future Validation Strategy

Consensus validation must use either:

1. Real source-separated audio stems;

or

2. Synthetic independent rhythmic sources specifically created
for algorithm validation.

### Principle

Named sources are not equivalent to independent sources.

Source identity and source signal independence are separate
architectural concepts.


---

## AD-018 — Ensemble Metric Consensus Validation Principle

### Status

LOCKED

### Context

The metric pulse of a musical ensemble cannot be
identified by selecting one dominant rhythmic source.

The observable rhythmic behaviour emerges from the
temporal interaction between multiple independent
Metric Sources.

### Decision

The Ensemble Metric Consensus Layer is the architectural
boundary responsible for reconstructing collective
metric events.

It receives:

- independent PulseCandidate sequences;
- MetricContributor information.

It produces:

- EnsembleMetricEvent sequences.

### Input Representation

PulseCandidate:

- sound_source_id;
- timestamp;
- confidence.

MetricContributor:

- sound_source_id;
- active state;
- contributor metadata.

### Output Representation

EnsembleMetricEvent:

- collective temporal position;
- contributing Metric Sources;
- temporal consensus confidence.

### Non Responsibilities

The Ensemble Metric Consensus Layer does not:

- select a privileged rhythmic source;
- determine meter;
- determine BPM metadata;
- identify musical style;
- introduce semantic interpretation.

### Scientific Principle

A metric event is not assigned to a single source.

A metric event is reconstructed from the temporal
agreement of multiple observable sources.



---

# AD-026 — Domain Pulse Candidate Translation Boundary

## Status

LOCKED

## M89 Supersession

AD-032 explicitly supersedes only this decision's omission of `strength` from
the Domain PulseCandidate output mapping. All other provisions remain in
force. See `docs/architecture/AD-032_M89_PULSE_STRENGTH_PRESERVATION.md`.

## Context

The Core Observation Layer and the Domain Reconstruction Layer
operate on different abstraction levels.

Core PulseCandidates represent observable temporal events
extracted from audio processing.

Domain PulseCandidates represent reconstructed temporal events
associated with stable musical sources.

Direct consumption of Core PulseCandidates by Domain analysis
components would violate the separation between observation
and reconstruction layers.

## Decision

A dedicated translation boundary is required between:

- Core PulseCandidate representation;
- Domain PulseCandidate representation.

The responsible component is:

`DomainPulseCandidateAdapter`

## Transformation

Input:

Core PulseCandidate:

- time;
- strength;
- confidence.

Output:

Domain PulseCandidate:

- id;
- sound_source_id;
- timestamp;
- confidence;
- creation metadata.

## Pipeline Contract

Canonical flow:
Core PulseCandidate
|
v
DomainPulseCandidateAdapter
|
v
Domain PulseCandidate
|
v
Ensemble Metric Consensus
|
v
EnsembleMetricEvent

## Non Responsibilities

The adapter does not:

- infer beat;
- infer meter;
- estimate BPM;
- classify instruments;
- introduce semantic interpretation.

## Scientific Principle

Observable temporal evidence must be translated explicitly
before entering semantic reconstruction layers.

No implicit representation conversion is allowed.


------------------------------------------------------------
AD-021
------------------------------------------------------------

Title

Complete Observation Model

Status

PROPOSED

Summary

JGA shall analyze the complete observable audio signal.

Metric Stability is an observable property of the
performance and shall not determine the beginning of the
analysis.

Reference

docs/architecture/AD-021_COMPLETE_OBSERVATION_MODEL.md

Validation

VAL-001


------------------------------------------------------------
AD-021
------------------------------------------------------------

Status

ACCEPTED

Title

Complete Observation Model

Summary

The complete observable musical signal is now the scientific
object of analysis.

Metric Stability is treated as an observable descriptor of
musical behaviour and no longer determines where analysis
begins.

Validation

VAL-001
PASSED


------------------------------------------------------------

# AD-027 — Immutable Analysis Representation

## Status

LOCKED

## Decision

Completed blind analysis shall be exposed to the Scientific Validation Layer
only through an immutable, scope-minimal scientific representation.

The representation shall not expose mutable runtime state and shall not contain
Ground Truth or validation conclusions.

## Canonical Specification

`docs/architecture/AD-027_IMMUTABLE_ANALYSIS_REPRESENTATION.md`


------------------------------------------------------------

# AD-028 — M83 Ground Truth Reference

## Status

LOCKED

## Decision

GT-VAL-001-v1 is the independent immutable Ground Truth reference bound to
VAL-001. It is constructed only from the approved authoritative MusicXML source
and contains the minimum scientific quantities approved for M83.

Ground Truth generation shall remain independent from JGA analysis, Immutable
Analysis Representation, Comparator and validation outputs.

## Canonical Specification

`docs/architecture/AD-028_M83_GROUND_TRUTH_REFERENCE.md`


------------------------------------------------------------

# AD-029 — M84 Scientific Validation Catalog

## Status

LOCKED

## Decision

`JGA-VALIDATION-CATALOG-v1` is the immutable scientific catalogue of Validation
Items. `VAL-001` identifies its first item and binds Ground Truth and approved
asset identities without duplicating Ground Truth content.

The existing analysis-produced `ValidationDataset` remains a scientifically
distinct observational artifact.

## Canonical Specification

`docs/architecture/AD-029_M84_VALIDATION_CATALOG.md`


------------------------------------------------------------

# AD-030 — M85 Scientific Comparator

## Status

LOCKED

## Decision

`JGA-COMPARATOR-001`, schema `1`, compares one bound Validation Item,
Immutable Analysis Representation and Ground Truth Model using only the
approved tempo, time-signature, section and instrumentation contracts.

The Comparator preserves deterministic scientific evidence without accuracy,
tolerance, classification or conclusions.

## Canonical Specification

`docs/architecture/AD-030_M85_COMPARATOR.md`


------------------------------------------------------------

# AD-031 — M87 Scientific Validation Record

## Status

LOCKED

## Decision

One completed immutable Comparator Result and its matching Immutable Analysis
Representation are materialized into a permanent immutable Scientific
Validation Record. The boundary preserves identities, provenance, evidence,
availability states and limitations without interpretation or modification.

Record identity and fingerprint are deterministic for the preserved completed
validation execution.

## Canonical Specification

`docs/architecture/AD-031_M87_SCIENTIFIC_VALIDATION_RECORD.md`


------------------------------------------------------------

# AD-032 — M89 PulseCandidate Strength Preservation

## Status

LOCKED

## Decision

`PulseCandidate.strength` is preserved unchanged as an immutable observational
quantity across the Core PulseCandidate to Domain PulseCandidate Translation
boundary. Preservation introduces no musical or interpretative semantics and
does not authorize downstream computation.

AD-032 explicitly supersedes only AD-026's incomplete Domain PulseCandidate
output mapping.

## Canonical Specification

`docs/architecture/AD-032_M89_PULSE_STRENGTH_PRESERVATION.md`


------------------------------------------------------------

# AD-033 — M90 Controlled Dataset Provenance

## Status

LOCKED

## Decision

Controlled Dataset Provenance owns the declared generation procedure,
generation identities, temporal-origin declaration and reproducibility
limitations of a controlled experimental dataset. It does not own Ground Truth,
Validation Catalog asset identity, validation execution or scientific-record
preservation semantics.

The first canonical identities are `CED-VAL-001`,
`DGR-CED-VAL-001-001` and `PR-CED-VAL-001-001`.

## Canonical Specification

`docs/architecture/AD-033_M90_CONTROLLED_DATASET_PROVENANCE.md`


------------------------------------------------------------

# AD-034 — M91 Candidate Period Representation

## Status

LOCKED

## Decision

Already-produced Candidate Period evidence is preserved by a standalone,
deeply immutable Core representation. It preserves duration, recurrence
occurrences, observation scope, provenance and reproducibility metadata
without discovery, generation, selection or musical metric interpretation.

The experiment-local recurrence protocol used by `H-VAL001-C1-03` is not
promoted to production authority.

M91.1 corrects representation responsibility: experiment identity, validation
run identity, validation protocol identity and repeated-execution fingerprints
belong to F-030/SVP-001 records rather than the general Core representation.
The representation retains only Candidate evidence, scope, temporal unit and
minimum runtime provenance, including explicit discovery configuration.

## Canonical Specification

`docs/architecture/AD-034_M91_CANDIDATE_PERIOD_REPRESENTATION.md`


------------------------------------------------------------

# AD-035 — M92 Candidate Period Discovery

## Status

LOCKED

## Decision

M92 discovers and preserves the complete Candidate Period population from
ordered filtered Core PulseCandidate timestamps using only exact recurrent
consecutive positive frame intervals occurring at least twice.

Observation frame length is explicit configuration. Discovery runs immediately
after PulseCandidate filtering and does not feed or modify the existing metric
reconstruction path.

## Canonical Specification

`docs/architecture/AD-035_M92_CANDIDATE_PERIOD_DISCOVERY.md`
