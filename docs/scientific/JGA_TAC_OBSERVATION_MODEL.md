# TAC Observation Model

Version: 0.1

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

TAC belongs to the observation-to-representation transition layer.

TAC does not represent:

- detected beat;
- estimated pulse;
- tempo grid;
- quantized timing;
- metric correctness.

TAC represents relationships between observable temporal events
derived from the physical audio signal.


# 3. Relationship with RFC-001 Observation Model Review

RFC-001 establishes the fundamental principle:

Observation always precedes interpretation.

No additional generic Observation entity is introduced.

The original performance remains the source of truth.

Every higher-level representation must remain traceable to physical
observations.

TAC therefore does not replace the Observation Layer.

TAC operates on observable events while preserving their temporal
and acoustic provenance.


# 4. Relationship with RFC-002 PulseCandidate

RFC-002 identifies an unresolved ambiguity concerning the scientific
role of PulseCandidate.

Current implementation shows that PulseCandidate:

- derives from onset detection;
- contains onset-related information;
- carries confidence;
- does not perform pulse inference;
- does not perform beat estimation;
- does not introduce musical interpretation.

Therefore PulseCandidate cannot be considered an already established
metric entity.

TAC provides the temporal relational context required between
observable events and later metric representation.


# 5. TAC Temporal Observation

A TAC temporal event represents an observable occurrence extracted
from the audio signal.

A temporal event may contain:

- timestamp;
- duration;
- source identity;
- acoustic confidence;
- observable characteristics.

A TAC event does not contain:

- beat position;
- metric subdivision;
- harmonic interpretation;
- stylistic judgement.


# 6. Temporal Relations

The fundamental purpose of TAC is describing relationships between
observable events.

Possible temporal relations include:

- temporal distance;
- anticipation;
- delay;
- coincidence;
- persistence;
- recurrence.

These relations describe what happens in the performance without
declaring why it happens.


# 7. TAC Context

A Temporal Alignment Context is a collection of temporally related
observable events belonging to a defined performance segment.

A TAC Context describes:

- which events occur;
- when they occur;
- how events relate temporally;
- how temporal relationships evolve over time.


# 8. Relationship with Elementary Metric Event

The Elementary Metric Event remains the first domain-level metric
representation of JGA.

TAC does not replace EME.

TAC provides the observable temporal evidence from which metric
representation can emerge.

The transition:

Observable Event
        ↓
TAC Temporal Relation
        ↓
Elementary Metric Event

must remain traceable.


# 9. Non Goals

TAC does not:

- estimate tempo;
- detect beat;
- create a metric grid;
- quantize performance;
- evaluate musicianship;
- determine correctness of timing.


# 10. Scientific Constraints

The following principles are invariant:

- Observation precedes interpretation.
- Observable evidence precedes musical meaning.
- No hidden metric assumption may be introduced.
- Every abstraction must remain traceable to the original audio.


# 11. Open Questions

The following points require further investigation:

1. Is PulseCandidate a TAC input object?

2. Should TAC become a Domain Model entity?

3. Which temporal relations are necessary for metric emergence?

4. Does TAC require a dedicated mathematical representation?

5. How does TAC interact with Metric Cluster construction?




# 12. Repository Status

This document defines a scientific specification only.

No implementation change is introduced until the model is approved
and mapped to the Domain Model.
