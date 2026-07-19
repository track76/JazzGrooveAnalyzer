# RFC-003 — Metric Context Lifecycle

Status: Proposed

---

# Purpose

This RFC defines the ownership and lifecycle of the Metric Context.

It resolves the architectural question of where the Metric Context
is constructed, who owns it, and how it reaches the Translation Layer.

---

# Scientific Principle

The Metric Context is an observable computational representation.

It belongs to the Observation Model.

It is not part of the Domain Model.

It introduces no semantic interpretation.

---

# Ownership

Observation Model
    owns the Metric Context.

Translation Layer
    consumes the Metric Context.

Domain Model
    consumes the translated representation.

---

# Lifecycle

Audio Signal

↓

Observable Events

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

The Metric Context exists only after sufficient observable
evidence has been accumulated.

---

# Architectural Consequences

MetricContext is not a Runtime object.

MetricContext is not a Domain object.

MetricContext is the terminal observable representation of
the computational Core.

The Translation Layer begins exactly at the MetricContext boundary.

---

# Consequences for Implementation

No Domain entity may be instantiated before a MetricContext
has been established.

The Translation Layer consumes MetricContext and produces
canonical Domain inputs.

