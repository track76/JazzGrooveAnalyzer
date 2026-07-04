# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# InternalMetricTimeline (TMI)

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `InternalMetricTimeline` (TMI) entity is to represent the estimated temporal reference emerging from the collective behaviour of the ensemble.

The Internal Metric Timeline constitutes the central temporal model of the Jazz Groove Analyzer.

It is the reference against which every subsequent temporal analysis is performed.

---

# 2. Scientific Motivation

The metric reference of a musical ensemble is not directly observable.

Instead, it emerges from the coordinated interaction of multiple metric contributors over time.

The Jazz Groove Analyzer models this emergent behaviour through the Internal Metric Timeline.

The TMI therefore represents the ensemble's internal temporal organisation rather than an externally imposed metrical grid.

---

# 3. Scientific Definition

An `InternalMetricTimeline` is an inferred temporal structure composed of an ordered sequence of Pulse entities.

It represents the estimated evolution of the ensemble's internal metric reference throughout the analysed performance.

The TMI is not directly observed.

It is inferred from the temporal organisation of MetricClusters through the estimation of Pulse occurrences.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Metric Domain |
| Category | Entity |
| Parent | Pulse |
| Child | LocalTempo, TemporalDeviation |
| Lifecycle | Immutable |

---

# 5. Responsibilities

The InternalMetricTimeline is responsible for:

- representing the complete temporal reference of the ensemble;
- preserving the chronological ordering of Pulse entities;
- providing the temporal framework for all subsequent analyses;
- serving as the reference against which temporal deviations are measured.

The TMI never:

- performs statistical analysis;
- classifies musical functions;
- identifies sound sources.

---

# 6. Relationships

The InternalMetricTimeline is composed of an ordered sequence of Pulse entities.

Every Pulse belongs to exactly one InternalMetricTimeline.

The TMI provides the temporal reference used by:

- LocalTempo;
- TemporalDeviation;
- MetricStability;
- InstrumentProfile;
- PerformanceProfile.

---

# 7. Lifecycle

The InternalMetricTimeline is created after the Pulse estimation stage.

Once constructed, it remains immutable throughout the complete analysis.

Subsequent analytical stages may reference the TMI but shall never modify it.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

The InternalMetricTimeline is an inferred temporal structure.

It is never directly observable.

---

## Invariant 2

Every Pulse belongs to exactly one InternalMetricTimeline.

---

## Invariant 3

The chronological ordering of Pulse entities is preserved.

---

## Invariant 4

The InternalMetricTimeline represents the collective temporal behaviour of the ensemble.

It never represents the behaviour of an individual performer.

---

## Invariant 5

Every temporal measurement performed by the Jazz Groove Analyzer is referenced to the InternalMetricTimeline.

---

# 9. Constraints

The InternalMetricTimeline shall never depend upon:

- musical notation;
- externally supplied tempo values;
- manually inserted beat annotations;
- MIDI information.

Its construction depends exclusively on the observable audio signal and the inferred Metric Domain.

---

# 10. Observability

The InternalMetricTimeline is not directly observable.

It represents the highest-level inferred temporal structure within the Jazz Groove Analyzer.

Its existence results from the progressive abstraction of observable musical events.

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
        │
        ├──────────────► LocalTempo
        ├──────────────► TemporalDeviation
        ├──────────────► MetricStability
        ├──────────────► InstrumentProfile
        └──────────────► PerformanceProfile
```

---

# 12. Future Software Representation

Within the software architecture, the InternalMetricTimeline will be implemented as an immutable Domain Entity.

Its implementation shall preserve all definitions, responsibilities, relationships and invariants established in this specification.

Implementation details remain intentionally outside the scope of this document.

---

# 13. Conclusion

The InternalMetricTimeline represents the central temporal model of the Jazz Groove Analyzer.

Rather than describing an externally imposed metrical structure, it models the internal temporal organisation emerging from the collective behaviour of the ensemble.

Every subsequent temporal measurement performed by the JGA is referenced to this entity.

For this reason, the InternalMetricTimeline constitutes the core abstraction of the entire Jazz Groove Analyzer.