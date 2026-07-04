# Jazz Groove Analyzer (JGA)

# Domain Entity Specification

# AudioStem

**Version:** 1.0

**Status:** Official

**Author and Creator:** Angelo Tracanna

**Copyright © 2026 Angelo Tracanna. All rights reserved.**

---

# 1. Identity

AudioStem is a domain entity representing a single audio component extracted from an AudioRecording.

It is the first decomposition of the observable audio signal.

An AudioStem does not represent a musical instrument.

It represents an isolated audio signal that may correspond to one or more sound-producing sources.

---

# 2. Scientific Definition

Within the Jazz Groove Analyzer, an AudioStem is a partial representation of an AudioRecording obtained through an audio source separation process.

The AudioStem preserves the temporal continuity of the original recording while reducing the acoustic complexity of the signal.

It remains an observable object.

No musical interpretation is associated with an AudioStem.

---

# 3. Rationale

The complete audio recording contains multiple simultaneous sound sources.

Direct analysis of the complete recording is often insufficient for reliable identification of musical events.

The introduction of the AudioStem enables the decomposition of the recording into simpler observable signals while preserving complete temporal coherence with the original recording.

The AudioStem therefore represents an intermediate observational layer between the complete recording and the musical interpretation of its contents.

---

# 4. Responsibilities

The AudioStem is responsible for:

- representing one isolated audio signal;
- preserving temporal correspondence with the original recording;
- providing an observation layer for subsequent analysis;
- maintaining traceability to the originating AudioRecording.

The AudioStem never:

- recognises instruments;
- assigns musical functions;
- estimates tempo;
- constructs Metric Clusters;
- performs statistical analysis.

---

# 5. Relationships

The AudioStem belongs to exactly one AudioRecording.

One AudioRecording may generate one or more AudioStem entities.

Each AudioStem may later be associated with one or more MusicalSource entities.

The AudioStem therefore acts as the bridge between the physical recording and the musical interpretation of the signal.

---

# 6. Lifecycle

The lifecycle of an AudioStem begins after the source separation stage.

Once generated, the AudioStem remains immutable.

Subsequent analysis stages may observe the AudioStem but shall never modify its content.

---

# 7. Domain Invariants

The following invariants shall always remain true.

## Invariant 1

Every AudioStem originates from exactly one AudioRecording.

---

## Invariant 2

Every AudioStem preserves the temporal alignment of the original recording.

---

## Invariant 3

The audio content of an AudioStem is immutable.

---

## Invariant 4

The AudioStem contains no interpreted musical knowledge.

---

## Invariant 5

Different separation algorithms may generate different AudioStem entities while preserving the same conceptual definition.

---

# 8. Constraints

The AudioStem shall never depend on:

- musical notation;
- MIDI information;
- manually inserted annotations;
- external tempo information.

Its existence depends exclusively on the observable audio signal.

---

# 9. Observability

The AudioStem remains a purely observable object.

It belongs entirely to the Physical Domain.

No cognitive interpretation is introduced at this stage.

---

# 10. Position within the Domain Model

AudioRecording

↓

AudioStem

↓

MusicalSource

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

Within the software architecture, AudioStem will be implemented as a domain entity belonging to the Physical Domain.

Its implementation shall preserve all responsibilities, relationships and invariants defined in this specification.

Implementation details remain intentionally outside the scope of this document.

---

# 12. Conclusion

AudioStem represents the first structural decomposition of the observable audio recording.

It does not simplify the scientific model.

It simplifies the observation of the physical reality while preserving complete temporal coherence with the original recording.

For this reason, it constitutes the second fundamental entity of the Jazz Groove Analyzer Domain Model.