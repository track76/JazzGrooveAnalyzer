# TAC Observation Model

Version: 0.2

Status:
DRAFT

Author:
Angelo Tracanna


# 1. Purpose

The Temporal Alignment Context (TAC) defines the scientific model
used to describe temporal relationships between observable musical
events before metric interpretation.

The purpose of TAC is to formalize the temporal organization
emerging from a musical performance without introducing metric
assumptions or interpretative hypotheses.


# 2. Scientific Position

TAC belongs to the transition layer between physical observation
and musical representation.

TAC describes temporal relationships among observable events.

TAC does not represent:

- detected beat;
- estimated pulse;
- tempo grid;
- quantized timing;
- metric correctness.

TAC represents temporal organization derived from the physical
audio signal while preserving observational traceability.


# 3. Relationship with F-001 Scientific Observation

F-001 establishes the fundamental principle:

Observation always precedes interpretation.

The Observation Layer extracts observable events from the audio
signal without introducing musical meaning.

TAC does not replace the Observation Layer.

TAC operates after observation and provides temporal
contextualization of observable events before metric interpretation.


# 4. Relationship with RFC-001 Observation Model Review

RFC-001 confirms that no additional generic Observation entity
is required.

The original performance remains the source of truth.

Every higher-level representation must remain traceable to
physical observations.

TAC therefore is not a new observation entity.

TAC is a model of temporal relationships between observations.


# 5. Relationship with F-003 Observable Metric Context

The Observable Metric Context is constructed after temporal
relationships among observable events have been identified.

F-003 defines the context required for subsequent analysis,
including:

- meter;
- local tempo;
- ensemble pulse;
- metric contributors;
- musical functions.

TAC does not determine these concepts.

TAC provides the temporal organization required before the
Observable Metric Context can emerge.


# 6. Relationship with RFC-002 PulseCandidate

RFC-002 identifies an ambiguity in the scientific role of
PulseCandidate.

Repository analysis shows two different concepts:

## Core PulseCandidate

Represents an onset-derived observable temporal candidate.

Characteristics:

- timestamp;
- onset strength;
- confidence.

It belongs to the observation/computational layer.


## Domain PulseCandidate

Represents a domain-level candidate temporal contribution
associated with a musical source.

Characteristics:

- identity;
- sound source;
- timestamp;
- confidence.

It belongs to the representation layer.


The shared name creates semantic ambiguity.

TAC provides the missing conceptual boundary between observable
temporal events and metric representation.


# 7. TAC Temporal Observation

A TAC temporal observation represents an observable occurrence
derived from the audio signal.

A TAC temporal observation may contain:

- timestamp;
- duration;
- source information;
- acoustic confidence;
- observable characteristics.

A TAC temporal observation does not contain:

- beat position;
- metric subdivision;
- harmonic interpretation;
- stylistic judgement.


# 8. Temporal Relations

The fundamental purpose of TAC is describing relationships
between observable temporal events.

Possible temporal relations include:

- temporal distance;
- anticipation;
- delay;
- coincidence;
- persistence;
- recurrence.

These relations describe what happens in the performance
without declaring why it happens.


# 9. TAC Context

A Temporal Alignment Context is a collection of temporally related
observable events belonging to a defined performance segment.

A TAC Context describes:

- which events occur;
- when they occur;
- how events relate temporally;
- how temporal relationships evolve over time.


# 10. Relationship with Elementary Metric Event

The Elementary Metric Event remains a domain-level temporal
representation derived from observable evidence.

TAC does not replace EME.

TAC provides temporal evidence and relational structure before
metric representation.

The transition is:

Observable Event

        ↓

TAC Temporal Relations

        ↓

Observable Metric Context

        ↓

Elementary Metric Event


Every abstraction must remain traceable to the original audio.


# 11. Non Goals

TAC does not:

- estimate tempo;
- detect beat;
- create a metric grid;
- quantize performance;
- evaluate musicianship;
- determine correctness of timing.


# 12. Scientific Constraints

The following principles are invariant:

- Observation precedes interpretation.
- Observable evidence precedes musical meaning.
- No hidden metric assumption may be introduced.
- Every abstraction must remain traceable to the original audio.
- Intentional rhythmic variation is not treated as error.


# 13. Open Questions

The following points require further investigation:

1. Should TAC become an explicit software model?

2. Should Core PulseCandidate receive a different name?

3. Should Domain PulseCandidate remain part of the Domain Model?

4. Which temporal relations are necessary for metric emergence?

5. Does TAC require a dedicated mathematical representation?


# 14. Repository Status

This document defines a scientific specification only.

No implementation change is introduced until the model is approved
and mapped to the Domain Model.

