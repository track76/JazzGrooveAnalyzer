# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# Pulse

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `Pulse` entity is to represent the estimated occurrence of the ensemble pulse inferred from one or more `MetricCluster` instances.

The Pulse provides the first explicit representation of the ensemble temporal reference.

It does not correspond to a directly observable event.

---

# 2. Scientific Motivation

The temporal organisation of an ensemble cannot be reduced to isolated musical events.

Instead, the perception of pulse emerges from the collective temporal behaviour represented by MetricClusters.

The Pulse formalises this emergence by representing the estimated temporal position of each pulse occurrence.

---

# 3. Scientific Definition

A `Pulse` is an inferred temporal entity representing one occurrence of the ensemble pulse.

Each Pulse is estimated from one MetricCluster.

It represents the temporal reference upon which higher-level temporal structures are constructed.

The Pulse is an estimation.

It is not an observation.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Metric Domain |
| Category | Entity |
| Parent | MetricCluster |
| Child | InternalMetricTimeline |
| Lifecycle | Immutable |

---

# 5. Responsibilities

The Pulse is responsible for:

- representing one estimated pulse occurrence;
- preserving its temporal position;
- providing the elementary units composing the Internal Metric Timeline.

The Pulse never:

- estimates tempo;
- estimates meter;
- performs statistical analysis.

---

# 6. Relationships

Each Pulse is derived from one MetricCluster.

A sequence of Pulse entities forms the Internal Metric Timeline.

---

# 7. Lifecycle

A Pulse is created after the corresponding MetricCluster has been estimated.

Once created, it remains immutable.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every Pulse originates from one MetricCluster.

---

## Invariant 2

Every Pulse possesses exactly one temporal position.

---

## Invariant 3

A Pulse is an inferred temporal entity.

It is never directly observable.

---

## Invariant 4

The temporal position of a Pulse never changes after creation.

---

## Invariant 5

The identity of a Pulse remains constant throughout the analysis.

---

# 9. Constraints

A Pulse shall never:

- estimate tempo;
- estimate meter;
- compute temporal deviations.

These responsibilities belong to subsequent stages of the Domain Model.

---

# 10. Observability

The Pulse is not directly observable.

It is inferred from MetricClusters.

It represents the first explicit estimation of the ensemble temporal reference.

---

# 11. Position within the Domain Model

```
AudioRecording
        │
        ▼
AudioStem
        │
        ▼
SoundSource
        │
        ▼
MusicalFunction
        │
        ▼
MetricContributor
        │
        ▼
ElementaryMetricEvent
        │
        ▼
MetricCluster
        │
        ▼
Pulse
        │
        ▼
InternalMetricTimeline
```

---

# 12. Future Software Representation

Within the software architecture, Pulse will be implemented as an immutable Domain Entity.

Its implementation shall preserve all responsibilities, relationships and invariants defined in this specification.

Implementation details remain outside the scope of this document.

---

# 13. Conclusion

The Pulse represents the first explicit temporal reference inferred from the collective behaviour of the ensemble.

It constitutes the elementary component of the Internal Metric Timeline and provides the temporal framework upon which the subsequent stages of the Jazz Groove Analyzer are built.