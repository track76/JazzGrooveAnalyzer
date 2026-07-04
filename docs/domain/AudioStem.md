# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# AudioStem

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Purpose

The purpose of the `AudioStem` entity is to represent an isolated audio signal derived from an `AudioRecording`.

An `AudioStem` provides a simplified observational representation of the original recording while preserving its complete temporal coherence.

It constitutes the intermediate layer between the complete recording and the recognition of sound-producing sources.

---

# 2. Scientific Motivation

Musical recordings contain multiple simultaneous sound sources whose acoustic superposition complicates direct analysis.

The introduction of the `AudioStem` allows the JGA to observe individual components of the recording independently, reducing signal complexity without altering the temporal structure of the performance.

The `AudioStem` therefore belongs entirely to the observational stage of the analysis.

No musical interpretation is introduced at this level.

---

# 3. Scientific Definition

An `AudioStem` is an isolated audio signal obtained from an `AudioRecording` through a source separation process.

It preserves the temporal continuity of the original recording and represents an observable component of the musical performance.

An `AudioStem` is not a musical object.

It is an observable audio object.

---

# 4. Domain Classification

| Property | Value |
|----------|-------|
| Domain Layer | Physical Domain |
| Category | Entity |
| Parent Entity | AudioRecording |
| Child Entity | SoundSource |
| Lifecycle | Immutable |

---

# 5. Responsibilities

The `AudioStem` is responsible for:

- representing an isolated audio signal;
- preserving temporal alignment with the original recording;
- maintaining traceability to the originating `AudioRecording`;
- providing the observational basis for the identification of `SoundSource` entities.

The `AudioStem` never:

- identifies instruments;
- assigns musical functions;
- estimates temporal structures;
- performs statistical analysis.

---

# 6. Relationships

Each `AudioStem` belongs to exactly one `AudioRecording`.

An `AudioRecording` may generate one or more `AudioStem` entities.

One or more `SoundSource` entities may be identified from an `AudioStem`.

---

# 7. Lifecycle

The lifecycle of an `AudioStem` begins when an `AudioRecording` is decomposed into individual audio components.

Once created, an `AudioStem` remains immutable.

All subsequent stages of the analysis may observe the stem but shall never modify its content.

---

# 8. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every `AudioStem` originates from exactly one `AudioRecording`.

---

## Invariant 2

The temporal structure of an `AudioStem` remains aligned with the originating recording.

---

## Invariant 3

The audio content of an `AudioStem` is immutable.

---

## Invariant 4

An `AudioStem` contains no interpreted musical knowledge.

---

## Invariant 5

The identity of an `AudioStem` remains constant throughout the complete analysis.

---

# 9. Constraints

An `AudioStem` shall never depend on:

- musical notation;
- MIDI information;
- manually inserted annotations;
- tempo estimation;
- beat detection;
- external metadata.

Its existence depends exclusively on the observable audio signal.

---

# 10. Observability

The `AudioStem` belongs entirely to the Physical Domain.

It represents an observable signal obtained from the original recording.

It does not introduce any cognitive interpretation of the musical content.

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
        │
        ▼
Analytical Domain
```

---

# 12. Future Software Representation

Within the software architecture, `AudioStem` will be implemented as a Domain Entity belonging to the Physical Domain.

Its implementation shall preserve all responsibilities, relationships and invariants defined in this specification.

Implementation details remain intentionally outside the scope of this document.

---

# 13. Conclusion

The `AudioStem` represents the first structural decomposition of an `AudioRecording`.

It provides a simplified observational view of the audio signal while preserving complete temporal coherence with the original performance.

As such, it forms the essential bridge between the observable recording and the cognitive recognition of sound-producing sources.