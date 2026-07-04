# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# MetricCluster

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `MetricCluster` entity is to represent a collection of temporally related `ElementaryMetricEvent` (EME) instances that jointly describe a single metric occurrence within the ensemble.

A MetricCluster is the first inferred temporal structure of the Jazz Groove Analyzer.

It is not directly observed.

It emerges from the organisation of multiple ElementaryMetricEvents.

---

# 2. Scientific Motivation

Musical pulse is not produced by isolated events.

Instead, it emerges from the coordinated temporal behaviour of multiple metric contributors.

The MetricCluster formalises this collective behaviour by grouping ElementaryMetricEvents that belong to the same metric occurrence.

This concept constitutes the bridge between observable temporal events and the internal metric representation of the ensemble.

---

# 3. Scientific Definition

A `MetricCluster` is an inferred temporal structure composed of one or more ElementaryMetricEvents that belong to the same metric occurrence.

The MetricCluster represents the collective manifestation of the ensemble at a given moment of the performance.

It is not equivalent to a beat.

It is the observable evidence from which the beat is later inferred.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Metric Domain |
| Category | Entity |
| Parent | ElementaryMetricEvent |
| Child | Pulse |
| Lifecycle | Immutable |

---

# 5. Responsibilities

The MetricCluster is responsible for:

- grouping temporally related ElementaryMetricEvents;
- preserving the temporal relationships among its constituent events;
- representing a single collective metric occurrence;
- providing the observational basis for pulse estimation.

The MetricCluster never:

- estimates tempo;
- defines the beat;
- generates statistical information.

---

# 6. Relationships

Every MetricCluster contains one or more ElementaryMetricEvents.

Every ElementaryMetricEvent belongs to exactly one MetricCluster.

MetricClusters constitute the input for Pulse estimation.

---

# 7. Lifecycle

A MetricCluster is created once a coherent set of ElementaryMetricEvents has been identified.

After creation, the MetricCluster remains immutable.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every MetricCluster contains at least one ElementaryMetricEvent.

---

## Invariant 2

Every ElementaryMetricEvent belongs to exactly one MetricCluster.

---

## Invariant 3

The MetricCluster is an inferred structure.

It is never directly observable.

---

## Invariant 4

The temporal relationships among the contained ElementaryMetricEvents remain preserved.

---

## Invariant 5

The identity of a MetricCluster never changes after creation.

---

# 9. Constraints

A MetricCluster shall never:

- estimate tempo;
- define pulse;
- define meter;
- estimate the Internal Metric Timeline.

Those responsibilities belong to subsequent stages of the Domain Model.

---

# 10. Observability

The MetricCluster is not directly observable.

It is inferred from the temporal organisation of ElementaryMetricEvents.

It represents the first collective temporal structure recognised by the Jazz Groove Analyzer.

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

Within the software architecture, MetricCluster will be implemented as an immutable Domain Entity.

Its implementation shall preserve all relationships, responsibilities and invariants defined in this specification.

Implementation details remain outside the scope of this document.

---

# 13. Conclusion

The MetricCluster represents the first collective temporal structure of the Jazz Groove Analyzer.

By organising ElementaryMetricEvents into coherent metric occurrences, it provides the observational foundation from which the ensemble pulse and the Internal Metric Timeline are subsequently inferred.

It therefore constitutes the central structural element of the JGA metric model.