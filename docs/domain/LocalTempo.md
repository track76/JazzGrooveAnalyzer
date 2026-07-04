# Jazz Groove Analyzer (JGA)

# Domain Value Object Specification

# LocalTempo

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `LocalTempo` value object is to represent the instantaneous tempo estimated from the Internal Metric Timeline at a specific temporal region of the performance.

Unlike a global tempo indication, LocalTempo describes the local temporal behaviour emerging from the ensemble.

---

# 2. Scientific Motivation

Musical performances rarely maintain a perfectly constant tempo.

Instead, tempo continuously evolves as a consequence of the collective interaction among performers.

The Jazz Groove Analyzer models these local variations by introducing the concept of LocalTempo.

---

# 3. Scientific Definition

A `LocalTempo` represents the estimated tempo associated with a specific segment of the Internal Metric Timeline.

It is derived exclusively from the temporal relationships among consecutive Pulse entities.

LocalTempo is an analytical quantity.

It is not directly observable.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Analytical Domain |
| Category | Value Object |
| Derived From | InternalMetricTimeline |
| Mutability | Immutable |

---

# 5. Responsibilities

The LocalTempo is responsible for:

- representing the estimated local tempo;
- describing tempo evolution throughout the performance;
- providing reference values for higher-level temporal analysis.

The LocalTempo never:

- modifies the Internal Metric Timeline;
- identifies musical events;
- performs statistical analysis.

---

# 6. Relationships

Every LocalTempo is derived from the InternalMetricTimeline.

Multiple LocalTempo instances may describe different temporal regions of the same performance.

LocalTempo provides the basis for TemporalDeviation and MetricStability analyses.

---

# 7. Lifecycle

A LocalTempo exists only after the InternalMetricTimeline has been estimated.

Once calculated, it remains immutable.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every LocalTempo is derived exclusively from the InternalMetricTimeline.

---

## Invariant 2

A LocalTempo represents an estimated value.

It is never directly observed.

---

## Invariant 3

A LocalTempo possesses no identity.

Equal values are indistinguishable.

---

## Invariant 4

The estimation of LocalTempo never modifies the InternalMetricTimeline.

---

## Invariant 5

LocalTempo always refers to a specific temporal region of the performance.

---

# 9. Constraints

LocalTempo shall never depend upon:

- externally supplied tempo values;
- manually inserted annotations;
- MIDI tempo information.

Its estimation depends exclusively on the InternalMetricTimeline.

---

# 10. Observability

LocalTempo is not directly observable.

It is analytically inferred from the InternalMetricTimeline.

---

# 11. Position within the Domain Model

```
InternalMetricTimeline
        │
        ▼
LocalTempo
        │
        ▼
TemporalDeviation
        │
        ▼
MetricStability
```

---

# 12. Future Software Representation

Within the software architecture, LocalTempo will be implemented as an immutable Value Object.

Its implementation shall preserve all definitions and invariants established in this specification.

Implementation details remain outside the scope of this document.

---

# 13. Conclusion

LocalTempo represents the local temporal behaviour of the ensemble derived from the Internal Metric Timeline.

It provides the analytical foundation upon which tempo evolution and temporal deviations are subsequently measured.