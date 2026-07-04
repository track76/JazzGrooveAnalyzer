# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# InstrumentProfile

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `InstrumentProfile` entity is to represent the complete temporal behaviour of a single SoundSource throughout the analysed performance.

It provides a structured description of the rhythmic characteristics associated with one sound-producing source.

---

# 2. Scientific Motivation

Every performer exhibits characteristic temporal behaviour.

Rather than describing isolated temporal events, the Jazz Groove Analyzer aggregates analytical measurements into an InstrumentProfile, allowing the behaviour of each SoundSource to be studied as a coherent whole.

---

# 3. Scientific Definition

An `InstrumentProfile` is an analytical entity describing the temporal characteristics of one SoundSource during a musical performance.

It integrates the analytical measurements derived from the Internal Metric Timeline without modifying the underlying temporal model.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Analytical Domain |
| Category | Entity |
| Parent | SoundSource |
| Derived From | TemporalDeviation, MetricStability |
| Lifecycle | Immutable |

---

# 5. Responsibilities

The InstrumentProfile is responsible for:

- representing the temporal behaviour of one SoundSource;
- collecting analytical measurements associated with that SoundSource;
- supporting comparisons between performances;
- providing structured information for higher-level analysis.

The InstrumentProfile never:

- modifies the Internal Metric Timeline;
- estimates pulse;
- identifies MetricContributors.

---

# 6. Relationships

Each InstrumentProfile is associated with exactly one SoundSource.

It is derived from:

- TemporalDeviation;
- MetricStability;
- LocalTempo.

Multiple InstrumentProfiles contribute to the construction of a PerformanceProfile.

---

# 7. Lifecycle

The InstrumentProfile is generated after all analytical measurements have been completed.

Once generated, it remains immutable.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every InstrumentProfile refers to exactly one SoundSource.

---

## Invariant 2

The InstrumentProfile never modifies analytical measurements.

---

## Invariant 3

The InstrumentProfile represents analytical knowledge.

It is never directly observable.

---

## Invariant 4

The InstrumentProfile preserves traceability to the analysed SoundSource.

---

## Invariant 5

The InstrumentProfile remains immutable after creation.

---

# 9. Constraints

InstrumentProfile shall never depend upon:

- manually inserted annotations;
- external performer evaluations;
- subjective musical judgement.

Its construction depends exclusively on analytical results produced by the Jazz Groove Analyzer.

---

# 10. Observability

The InstrumentProfile is not directly observable.

It represents an analytical synthesis of the temporal behaviour of a SoundSource.

---

# 11. Position within the Domain Model

```
SoundSource
        │
        ▼
TemporalDeviation
        │
        ▼
MetricStability
        │
        ▼
InstrumentProfile
        │
        ▼
PerformanceProfile
```

---

# 12. Future Software Representation

Within the software architecture, InstrumentProfile will be implemented as an immutable Domain Entity.

Its implementation shall preserve all definitions, relationships and invariants established in this specification.

Implementation details remain intentionally outside the scope of this document.

---

# 13. Conclusion

The InstrumentProfile represents the complete analytical description of the temporal behaviour of a single SoundSource.

It provides the foundation for comparing performers, analysing rhythmic behaviour and constructing higher-level performance summaries within the Jazz Groove Analyzer.