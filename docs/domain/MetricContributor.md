# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# MetricContributor

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `MetricContributor` entity is to identify whether a `SoundSource`, performing a specific `MusicalFunction`, actively contributes to the construction of the ensemble metric reference.

The MetricContributor represents the interface between musical interpretation and temporal modelling.

---

# 2. Scientific Motivation

Not every musical event contributes equally to the perception of pulse.

Within an ensemble, only specific musical behaviours participate in the emergence of the temporal reference.

The Jazz Groove Analyzer analyses exclusively those behaviours that contribute to the construction of the ensemble pulse.

The MetricContributor explicitly identifies these behaviours.

---

# 3. Scientific Definition

A `MetricContributor` represents a sound-producing source whose current musical function contributes to the construction or maintenance of the ensemble metric reference.

The contribution may change during the performance.

Consequently, MetricContributor is a dynamic property of the musical context.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Cognitive Domain |
| Category | Entity |
| Parent | SoundSource |
| Depends On | MusicalFunction |
| Lifecycle | Dynamic |

---

# 5. Responsibilities

The MetricContributor is responsible for:

- identifying metric participation;
- providing candidate events for metric analysis;
- connecting musical interpretation with temporal modelling.

The MetricContributor never:

- estimates tempo;
- creates metric clusters;
- performs statistical analysis.

---

# 6. Relationships

Every MetricContributor is associated with one SoundSource.

Its existence depends upon the MusicalFunction currently performed.

MetricContributor entities generate ElementaryMetricEvents.

---

# 7. Lifecycle

The MetricContributor exists only while the corresponding SoundSource actively contributes to the metric reference.

Changes in musical behaviour may activate or deactivate metric contribution.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every MetricContributor belongs to exactly one SoundSource.

---

## Invariant 2

Metric contribution is time-dependent.

---

## Invariant 3

Not every SoundSource is necessarily a MetricContributor.

---

## Invariant 4

MetricContributor never defines the metric reference.

It contributes to its emergence.

---

## Invariant 5

The ensemble metric reference emerges collectively from all active MetricContributors.

---

# 9. Constraints

MetricContributor shall never:

- directly estimate tempo;
- generate pulse;
- construct the Internal Metric Timeline.

These operations belong to later stages of the Domain Model.

---

# 10. Observability

Metric contribution is not directly observable.

It is inferred from the interaction between SoundSource and MusicalFunction.

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
InternalMetricTimeline
```

---

# 12. Future Software Representation

MetricContributor will be implemented as a Domain Entity.

Its implementation shall preserve the responsibilities and invariants defined in this specification.

Implementation details remain outside the scope of this document.

---

# 13. Conclusion

MetricContributor represents the first concept directly related to the emergence of the ensemble metric reference.

It establishes the transition between musical understanding and temporal modelling, identifying those musical behaviours that actively participate in the construction of pulse.