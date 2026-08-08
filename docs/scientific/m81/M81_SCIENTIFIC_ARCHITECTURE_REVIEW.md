# M81 — Scientific Architecture Review

Status

WORK IN PROGRESS

Copyright © 2026 Angelo Tracanna

---

## Purpose

This document reviews the complete scientific
architecture of Jazz Groove Analyzer before the
implementation of the Ground Truth Layer.

The objective is to verify that every layer has
a unique scientific responsibility and that no
architectural dependency violates the scientific
principles of JGA.

---

## Scientific Layers

1.
Audio Observation Layer

2.
Metric Observation Layer

3.
Translation Layer (τ₈)

4.
Domain Reconstruction Layer

5.
Behaviour Layer

6.
Representation Layer

7.
Scientific Geometry Layer

8.
Validation Layer

---

## Review Objective

For every layer we verify:

- responsibility
- inputs
- outputs
- dependencies
- scientific invariants


---

# Layer 1

Audio Observation Layer

Purpose

Acquire observable acoustic information.

Input

Physical audio signal.

Output

SignalRepresentation

Scientific Responsibility

Describe only the observable acoustic signal.

This layer never performs:

- metric interpretation
- rhythmic reconstruction
- musical analysis
- behaviour analysis

Architectural Dependencies

None.

Scientific Invariants

The original signal remains immutable.

Every subsequent layer depends on this
observable representation.


---

## Scientific Responsibility Principle

Every architectural layer contributes exactly
one scientific abstraction.

A layer must never perform responsibilities
belonging to subsequent layers.

Scientific knowledge is accumulated
incrementally.

Observable Signal
        ↓
Signal Representation
        ↓
Metric Observation
        ↓
Metric Context
        ↓
Domain Reconstruction
        ↓
Behaviour Quantification
        ↓
Scientific Representation
        ↓
Scientific Validation

No architectural layer may skip an intermediate
scientific abstraction.


---

## Scientific Knowledge Levels

JGA distinguishes different epistemological
levels of knowledge.

Level 0

Physical Reality

Observed acoustic phenomenon.

---

Level 1

Observable Representation

Signal representations derived directly from
the audio.

No musical assumptions are introduced.

---

Level 2

Observable Metric Behaviour

Metric phenomena extracted from the observable
signal.

Still independent from musical interpretation.

---

Level 3

Domain Reconstruction

Observable phenomena become musical domain
objects.

Examples:

- BeatReference
- MetricCluster
- Pulse

---

Level 4

Behaviour Quantification

The reconstructed metric behaviour is
quantified through scientific descriptors.

---

Level 5

Scientific Representation

Behaviour is represented geometrically and
analytically.

---

Level 6

Scientific Validation

Independent comparison between reconstructed
knowledge and Ground Truth.


---

## Forbidden Architectural Transitions

The scientific architecture intentionally
forbids direct transitions between non-adjacent
knowledge levels.

The following transitions are prohibited.

Physical Reality

×

Domain Reconstruction

Reason:

Domain objects cannot be produced directly from
raw audio.

---

Signal Representation

×

Behaviour Quantification

Reason:

Behaviour requires reconstructed musical
entities.

---

Observable Metric Behaviour

×

Scientific Representation

Reason:

Scientific representation requires validated
Domain objects.

---

Ground Truth

×

Domain Reconstruction

Reason:

Ground Truth is used exclusively during
validation.

It never participates in the reconstruction
pipeline.

---

Validation

×

Analysis

Reason:

Validation never modifies the analysis
pipeline.

Scientific validation remains an independent
process.

The boundary between completed analysis and
validation is the Immutable Analysis Representation
defined by AD-027.
