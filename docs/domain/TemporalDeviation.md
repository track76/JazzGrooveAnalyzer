# Jazz Groove Analyzer (JGA)

# Domain Value Object Specification

# TemporalDeviation

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `TemporalDeviation` value object is to represent the temporal difference between an observed musical event and the corresponding reference defined by the Internal Metric Timeline.

TemporalDeviation quantifies microtiming behaviour without altering the reference timeline.

---

# 2. Scientific Motivation

Musical performances naturally contain temporal variations.

These variations are not necessarily errors but often represent intentional expressive behaviour.

The Jazz Groove Analyzer measures these deviations relative to the Internal Metric Timeline in order to characterise the temporal behaviour of the ensemble and of individual sound sources.

---

# 3. Scientific Definition

A `TemporalDeviation` represents the signed temporal distance between an observed ElementaryMetricEvent and the corresponding reference position on the Internal Metric Timeline.

A positive or negative deviation indicates the relative temporal displacement of the event with respect to the estimated metric reference.

TemporalDeviation is an analytical measurement.

It is not directly observable.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Analytical Domain |
| Category | Value Object |
| Derived From | InternalMetricTimeline + ElementaryMetricEvent |
| Mutability | Immutable |

---

# 5. Responsibilities

The TemporalDeviation is responsible for:

- representing temporal displacement relative to the Internal Metric Timeline;
- supporting microtiming analysis;
- providing quantitative information for statistical evaluation.

The TemporalDeviation never:

- modifies the Internal Metric Timeline;
- estimates tempo;
- identifies musical functions.

---

# 6. Relationships

Every TemporalDeviation is calculated from:

- one ElementaryMetricEvent;
- one InternalMetricTimeline reference.

Collections of TemporalDeviation values are used to estimate MetricStability and PerformanceProfile.

---

# 7. Lifecycle

A TemporalDeviation exists only after the InternalMetricTimeline has been established.

Once computed, it remains immutable.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every TemporalDeviation is referenced to exactly one InternalMetricTimeline.

---

## Invariant 2

Every TemporalDeviation corresponds to exactly one ElementaryMetricEvent.

---

## Invariant 3

TemporalDeviation represents a measurement.

It never modifies the analysed performance.

---

## Invariant 4

Equal TemporalDeviation values are indistinguishable.

---

## Invariant 5

TemporalDeviation possesses no identity.

It is defined exclusively by its numerical value and its reference.

---

# 9. Constraints

TemporalDeviation shall never depend upon:

- manually annotated beat locations;
- external tempo references;
- MIDI timing information.

Its computation depends exclusively on the InternalMetricTimeline and the observed ElementaryMetricEvents.

---

# 10. Observability

TemporalDeviation is not directly observable.

It is analytically derived from the relationship between observed events and the estimated metric reference.

---

# 11. Position within the Domain Model

```
ElementaryMetricEvent
        │
        ├─────────────┐
        ▼             │
InternalMetricTimeline│
        │             │
        └──────► TemporalDeviation
                        │
                        ▼
                 MetricStability
```

---

# 12. Future Software Representation

Within the software architecture, TemporalDeviation will be implemented as an immutable Value Object.

Its implementation shall preserve all definitions, relationships and invariants established in this specification.

Implementation details remain intentionally outside the scope of this document.

---

# 13. Conclusion

TemporalDeviation represents the fundamental quantitative measurement of microtiming behaviour within the Jazz Groove Analyzer.

By expressing the temporal distance between observed musical events and the Internal Metric Timeline, it enables objective analysis of expressive timing while preserving the integrity of the ensemble metric reference.