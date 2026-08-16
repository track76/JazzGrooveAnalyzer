# AD-018 — Metric Movement Based Event Representation

Status: LOCKED


## Decision

An ElementaryMetricEvent does not represent a single
audio onset.

An ElementaryMetricEvent represents the temporal position
of one Metric Contributor with respect to one reconstructed
metric movement.


## Context

Audio recordings contain many observable events.

A performer may produce multiple notes inside one metric
movement:

Example:

4/4 meter:

Beat:

1        2        3        4

A saxophone may play:

♪ ♪ ♪♪ ♪♪♪

These audio events do not automatically correspond to
different metric events.


## Problem

If every audio onset becomes an ElementaryMetricEvent,
the analysis would measure note density instead of groove
behaviour.

The Jazz Groove Analyzer does not analyse the quantity
of notes.

It analyses how performers position themselves in time
with respect to the internal metric reference.


## Decision Rationale

The metric movement is the fundamental analytical unit.

Therefore:

Audio Onsets

        ↓

Temporal Association

        ↓

Metric Movement

        ↓

ElementaryMetricEvent


## Definition

An ElementaryMetricEvent is:

"An observation of one contributor's temporal position
relative to one reconstructed metric movement."


## Irregular Timing Principle

A temporal deviation is not considered an error.

An irregular placement is represented as a deviation
from the Metric Reference.


Example:

BeatReference:

1.000 seconds


Observed contributor event:

0.982 seconds


Result:

ElementaryMetricEvent

offset:

-18 ms


The deviation becomes analytical information.


## Relationship With MetricCluster

A MetricCluster represents one reconstructed metric
movement.

It may contain multiple contributor observations.


Example:

MetricCluster

    BeatReference:
    10.000 seconds


    Events:

        Bass EME
        +18 ms


        Piano EME
        -8 ms


        Drums EME
        +4 ms


## Architectural Consequence

The pipeline must not transform every audio onset
directly into ElementaryMetricEvents.


Required transformation:

Audio Signal

        ↓

Detected Audio Events

        ↓

Movement Association

        ↓

ElementaryMetricEvent


## AD-015 Traceability

INPUT:

Audio observations associated with a reconstructed
metric movement.


OUTPUT:

ElementaryMetricEvent


RESPONSIBLE TRANSFORMATION:

Metric Event Association Layer


## Authoritative EME Association Contract

ElementaryMetricEvent construction requires:

- the complete ordered source-specific Domain PulseCandidate population;
- the SoundSource to MetricContributor mapping;
- an authorized BeatReference reconstructed from pre-EME metric evidence;
- an explicit deterministic association result;
- temporal scope and provenance.

BeatReference reconstruction must not consume the ElementaryMetricEvents
whose existence depends on that BeatReference. Existing pre-EME ensemble
consensus evidence, together with declared context where applicable, is the
authorized input to movement reconstruction.

An observation may support at most one ElementaryMetricEvent in one
analysis. For one contributor and one movement, zero or more observations
may produce no more than one ElementaryMetricEvent. Every produced event
must retain the identities of all supporting observations, the source and
contributor identities, the movement identity, and the association rule.

Ambiguous association produces no ElementaryMetricEvent. Absence of an
authorized movement or a valid contributor-position association likewise
produces no event. Unassociated observations remain preserved as Domain
PulseCandidates; they are not discarded or duplicated.


TRACEABILITY:

Audio Event

        ↓

ElementaryMetricEvent

        ↓

MetricCluster

        ↓

AnalyticalCell


## Scope

Included:

- metric movement association
- contributor temporal position
- timing deviation preservation


Excluded:

- melodic analysis
- harmonic analysis
- note transcription
- performance interpretation


## Status

Architectural foundation for future EME refinement.
