# F-007 — Metric Context Composition

Status: Draft

---

# Purpose

This document formally defines the observable composition of the
Metric Context.

Its purpose is to identify which computational representations
constitute the complete observable evidence consumed by the
Translation Layer.

---

# Scientific Principle

The Metric Context is not a single observation.

It is the coherent organization of observable computational
representations produced by the Observation Model.

No semantic interpretation is introduced.

---

# Observable Components

The Metric Context is progressively constructed from the following
observable representations:

- SourcePulseSequence
- PeriodicitySegment
- MetricSegment

SourcePulseSequence preserves the observable identity of the
MetricSource associated with its rhythmic events.

These representations describe increasingly stable temporal
organization while remaining entirely observable.

---

# Canonical Representation

The observable composition of the Metric Context is defined at the
scientific level.

The software implementation is not required to expose every
intermediate computational representation as independent fields.

Equivalent software representations are permitted provided that:

- no observable information is lost;
- every observable property required by the Translation Layer remains
  recoverable;
- representational fidelity is preserved;
- complete traceability to the observable evidence is maintained.

Consequently, the scientific composition of the Metric Context and its
software representation are intentionally treated as distinct concepts.

---

# Scientific Invariants

Every component of the Metric Context:

- originates from observable evidence;
- is deterministic;
- preserves temporal ordering;
- preserves physical timestamps;
- introduces no musical semantics.

---

# Relationship with Translation Layer

The Translation Layer (τ₈) consumes the complete Metric Context.

Semantic entities are never generated directly from isolated
computational representations.

Instead, they emerge only after the complete Metric Context has
been scientifically established.

---

# Architectural Consequences

The Metric Context constitutes the canonical observable boundary
between the Observation Model and the Translation Layer.

Its internal composition belongs to the computational Core.

The Translation Layer consumes the Metric Context but does not
construct it.
