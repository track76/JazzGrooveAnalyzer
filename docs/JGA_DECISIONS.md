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
