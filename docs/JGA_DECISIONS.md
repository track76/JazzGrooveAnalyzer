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
