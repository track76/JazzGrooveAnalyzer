# Jazz Groove Analyzer (JGA)

# Domain Value Object Specification

# MusicalFunction

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `MusicalFunction` value object is to represent the musical behaviour currently performed by a `SoundSource` during a musical performance.

A MusicalFunction describes **what the sound source is doing**, independently of **who is producing the sound**.

It represents the first level of musical interpretation within the Jazz Groove Analyzer.

---

# 2. Scientific Motivation

The same sound-producing source may perform different musical behaviours during a performance.

Likewise, the same musical behaviour may be performed by different sound sources.

Separating the identity of the sound producer from its musical behaviour allows the JGA to analyse musical interaction independently of instrumentation.

---

# 3. Scientific Definition

A `MusicalFunction` is the description of the musical behaviour performed by a `SoundSource` within a given temporal context.

A MusicalFunction represents behaviour rather than identity.

It is therefore independent from the physical characteristics of the sound-producing source.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Cognitive Domain |
| Category | Value Object |
| Parent Entity | SoundSource |
| Mutability | Immutable |

---

# 5. Responsibilities

A MusicalFunction is responsible for:

- describing the current musical behaviour of a SoundSource;
- providing semantic information for higher-level analysis;
- supporting the identification of Metric Contributors.

A MusicalFunction never:

- represents a physical object;
- owns temporal information;
- generates analytical results.

---

# 6. Relationships

Every MusicalFunction is associated with one SoundSource.

A SoundSource may assume different MusicalFunctions during a performance.

The same MusicalFunction may occur in multiple SoundSources.

MetricContributor identification is based on the current MusicalFunction.

---

# 7. Lifecycle

A MusicalFunction exists only while the corresponding musical behaviour is observed.

Changes in musical behaviour produce a different MusicalFunction.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

A MusicalFunction possesses no identity.

---

## Invariant 2

Equal MusicalFunctions are indistinguishable.

---

## Invariant 3

A MusicalFunction never represents a sound-producing source.

---

## Invariant 4

A MusicalFunction never contains temporal measurements.

---

## Invariant 5

A MusicalFunction always describes musical behaviour.

---

# 9. Constraints

A MusicalFunction shall never depend upon:

- performer identity;
- recording metadata;
- instrument ownership;
- statistical analysis.

It depends exclusively on the observed musical behaviour.

---

# 10. Observability

A MusicalFunction is not directly observable.

It is inferred from the behaviour exhibited by a SoundSource.

It therefore belongs to the Cognitive Domain.

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

Within the software architecture, MusicalFunction will be implemented as an immutable Value Object.

Its implementation shall preserve the definitions and invariants established in this specification.

Implementation details remain outside the scope of this document.

---

# 13. Conclusion

The MusicalFunction value object separates musical behaviour from sound-producing identity.

This distinction enables the Jazz Groove Analyzer to analyse the functional interaction of the ensemble independently of instrumentation, providing the conceptual bridge between sound recognition and metric analysis.