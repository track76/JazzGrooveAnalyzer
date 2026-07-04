# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# SoundSource

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Identity

A SoundSource is a domain entity representing a sound-producing source identified within an AudioRecording.

It represents the first cognitive interpretation performed by the Jazz Groove Analyzer after the observation of the physical audio signal.

A SoundSource is not an isolated audio signal.

Nor is it a musical function.

It is the recognised origin of one or more sound events within the performance.

---

# 2. Scientific Definition

Within the Jazz Groove Analyzer, a SoundSource represents a physical sound-producing object inferred from one or more AudioStem entities.

Typical examples include:

- Double Bass
- Drum Kit
- Piano
- Tenor Saxophone
- Trumpet
- Voice

A SoundSource represents the identity of the sound producer independently of its musical behaviour during the performance.

---

# 3. Rationale

The purpose of introducing the SoundSource concept is to separate physical observation from musical interpretation.

The JGA first observes the audio signal.

It then recognises the physical source responsible for producing that signal.

Only after the source has been recognised can the system determine:

- which element of the source is active;
- which musical role it is performing;
- whether it contributes to the ensemble pulse.

This separation preserves the conceptual independence between observation and interpretation.

---

# 4. Responsibilities

A SoundSource is responsible for:

- representing a recognised sound-producing source;
- preserving its identity throughout the performance;
- providing the parent entity for SourceElement;
- maintaining traceability to the originating AudioRecording.

The SoundSource never:

- performs musical analysis;
- assigns musical roles;
- identifies metric contributors;
- estimates temporal structures;
- performs statistical analysis.

---

# 5. Relationships

Each SoundSource belongs to exactly one AudioRecording.

A SoundSource may be associated with one or more AudioStem entities.

Each SoundSource owns one or more SourceElement entities.

The SoundSource therefore represents the parent object of all elements capable of producing musical events.

---

# 6. Lifecycle

A SoundSource is created once the system has recognised the existence of a sound-producing source.

Its identity remains constant throughout the complete analysis.

The musical behaviour associated with the SoundSource may change over time.

Its identity never changes.

---

# 7. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every SoundSource belongs to exactly one AudioRecording.

---

## Invariant 2

A SoundSource represents a physical sound-producing source.

It never represents a musical role.

---

## Invariant 3

A SoundSource preserves its identity during the entire performance.

---

## Invariant 4

Different SourceElement entities may belong to the same SoundSource.

---

## Invariant 5

The SoundSource contains no temporal information.

Temporal behaviour belongs to later stages of the Domain Model.

---

# 8. Constraints

A SoundSource shall never depend on:

- tempo;
- meter;
- musical function;
- timing behaviour;
- statistical analysis.

Those concepts belong to subsequent domain entities.

---

# 9. Observability

The existence of a SoundSource is inferred from the observable audio signal.

Its musical meaning is not yet interpreted.

The SoundSource therefore occupies the conceptual boundary between the Physical Domain and the Cognitive Domain.

It is the first recognised object derived from the observable recording.

---

# 10. Position within the Domain Model

AudioRecording

↓

AudioStem

↓

SoundSource

↓

SourceElement

↓

MusicalRole

↓

MetricContributor

↓

ElementaryMetricEvent

↓

MetricCluster

↓

InternalMetricTimeline

↓

Analytical Domain

---

# 11. Future Software Representation

Within the software architecture, SoundSource will be implemented as a Domain Entity.

It represents the stable identity of a sound-producing source independently from the musical behaviour performed during the execution.

Implementation details remain intentionally outside the scope of this specification.

---

# 12. Conclusion

The SoundSource represents the first cognitive object introduced by the Jazz Groove Analyzer.

It establishes the connection between the observable audio signal and the musical concepts developed by the subsequent layers of the Domain Model.

By separating physical sound production from musical interpretation, the SoundSource preserves the conceptual integrity of the JGA architecture and provides the foundation upon which every higher-level domain concept is built.