# Jazz Groove Analyzer (JGA)

# Domain Value Object Specification

# MetricStability

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `MetricStability` value object is to quantify the temporal stability of the Internal Metric Timeline throughout a musical performance.

MetricStability describes the consistency of the ensemble metric reference rather than the behaviour of individual performers.

---

# 2. Scientific Motivation

The metric reference of an ensemble is not perfectly constant.

Its temporal behaviour may exhibit stable regions, gradual transitions or abrupt changes.

The Jazz Groove Analyzer evaluates these characteristics through the concept of MetricStability.

This measurement provides an objective description of the robustness of the ensemble temporal organisation.

---

# 3. Scientific Definition

A `MetricStability` represents the analytical evaluation of the consistency of the Internal Metric Timeline over a specified temporal interval.

It is derived from the temporal relationships among consecutive Pulse entities and from the distribution of TemporalDeviation values.

MetricStability is an analytical measurement.

It is not directly observable.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Analytical Domain |
| Category | Value Object |
| Derived From | InternalMetricTimeline + TemporalDeviation |
| Mutability | Immutable |

---

# 5. Responsibilities

The MetricStability is responsible for:

- describing the temporal consistency of the Internal Metric Timeline;
- identifying regions of stable or unstable metric behaviour;
- providing analytical support for higher-level performance analysis.

The MetricStability never:

- modifies the Internal Metric Timeline;
- estimates pulse;
- identifies musical events.

---

# 6. Relationships

Every MetricStability is derived from:

- one InternalMetricTimeline;
- one collection of TemporalDeviation values.

MetricStability contributes to the construction of InstrumentProfile and PerformanceProfile.

---

# 7. Lifecycle

MetricStability exists only after the InternalMetricTimeline has been estimated and the corresponding TemporalDeviation values have been calculated.

Once computed, it remains immutable.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

MetricStability always refers to one InternalMetricTimeline.

---

## Invariant 2

MetricStability represents an analytical quantity.

It is never directly observed.

---

## Invariant 3

Equal MetricStability values are indistinguishable.

---

## Invariant 4

MetricStability possesses no identity.

It is defined exclusively by its analytical value.

---

## Invariant 5

MetricStability never alters the temporal reference from which it is derived.

---

# 9. Constraints

MetricStability shall never depend upon:

- manually annotated tempo values;
- external beat references;
- MIDI timing information.

Its estimation depends exclusively on the Internal Metric Timeline and TemporalDeviation.

---

# 10. Observability

MetricStability is not directly observable.

It is inferred from the temporal behaviour of the ensemble represented by the Internal Metric Timeline.

---

# 11. Position within the Domain Model

```
InternalMetricTimeline
        │
        ▼
TemporalDeviation
        │
        ▼
MetricStability
        │
        ├────────────► InstrumentProfile
        └────────────► PerformanceProfile
```

---

# 12. Future Software Representation

Within the software architecture, MetricStability will be implemented as an immutable Value Object.

Its implementation shall preserve all definitions, relationships and invariants established in this specification.

Implementation details remain outside the scope of this document.

---

# 13. Conclusion

MetricStability represents the analytical evaluation of the consistency of the ensemble metric reference.

By describing the stability of the Internal Metric Timeline, it provides a quantitative foundation for the objective analysis of rhythmic behaviour within the Jazz Groove Analyzer.