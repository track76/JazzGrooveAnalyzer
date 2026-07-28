# F-029 — Analytical Cell

Status: LOCKED


## Purpose

Define the scientific meaning of the Analytical Cell
representation.


## Scientific Position

The Analytical Cell is a reporting representation of one
ElementaryMetricEvent positioned inside a reconstructed
metric structure.

It does not detect audio events.
It does not classify notes.
It does not infer musical behaviour.

It only represents a previously produced scientific
observation.


## Source of Truth

The source entity is:

ElementaryMetricEvent


Transformation:

ElementaryMetricEvent

        ↓

AnalyticalCell


## Architectural Principle

The reporting layer must preserve scientific observations
without introducing new musical interpretation.


## Input

Scientific input:

ElementaryMetricEvent


An ElementaryMetricEvent represents:

- one metric contributor
- one reconstructed metric movement
- one temporal position relative to the internal metric reference


The event is not equivalent to an audio onset.

Multiple audio notes may contribute to the same
ElementaryMetricEvent.


## Output

AnalyticalCell contains:

- beat association
- metric cluster association
- absolute temporal position
- timing deviation from the metric reference


## Relationship

Structure:


AnalyticalScore

        ↓

AnalyticalBar

        ↓

AnalyticalBeat

        ↓

AnalyticalCell


## Timing Representation

AnalyticalCell preserves the relationship between:

Metric Reference:

BeatReference.timestamp


and observed contributor position:

ElementaryMetricEvent.timestamp


The difference represents timing behaviour.


Example:

BeatReference:

10.000 seconds


Contributor observation:

10.018 seconds


AnalyticalCell:

offset:

+18 ms


The deviation is analytical information,
not an error.


## First Implementation Scope

Included:

- metric movement representation
- temporal position preservation
- metric cluster association
- beat association


Excluded:

- performer identification
- instrument classification
- melodic transcription
- harmonic analysis
- behavioural interpretation


## AD-015 Traceability

INPUT:

ElementaryMetricEvent


OUTPUT:

AnalyticalCell


RESPONSIBLE TRANSFORMATION:

AnalyticalCellBuilder


TRACEABILITY:


ElementaryMetricEvent

        ↓

AnalyticalCell

        ↓

AnalyticalBeat

        ↓

AnalyticalBar

        ↓

AnalyticalScore

        ↓

Renderer


## Future Extensions

Future analytical layers may add:

- instrument attribution
- contributor behaviour
- ensemble timing interaction
- section-based analysis


## Status

Scientific foundation aligned with
AD-018 Metric Movement Based Event Representation.
