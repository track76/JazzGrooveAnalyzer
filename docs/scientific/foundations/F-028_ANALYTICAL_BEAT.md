# F-028 — Analytical Beat

Status: DRAFT

## Purpose

Define the scientific meaning of the Analytical Beat representation.


## Scientific Position

The Analytical Beat is a reporting representation of one
reconstructed metric position inside an Analytical Bar.

It does not detect beats.
It does not reconstruct metric information.
It only represents metric structures already produced by
the scientific reconstruction layer.


## Source of Truth

The source entity is:

ReconstructedMeasure

through:

BeatReference


Transformation:

BeatReference
        ↓
AnalyticalBeat


## Architectural Principle

The reporting layer must preserve scientific information
without creating new musical interpretation.


## Input

Scientific input:

BeatReference


A BeatReference contains the reconstructed temporal position
of one metric event.


## Output

AnalyticalBeat contains:

- beat number
- analytical cells associated with the beat


## Relationship

AnalyticalBeat belongs to:

AnalyticalBar


Structure:

AnalyticalScore
        ↓
AnalyticalBar
        ↓
AnalyticalBeat
        ↓
AnalyticalCell


## First Implementation Scope

Included:

- beat numbering
- temporal position preservation
- association with reconstructed metric events


Excluded:

- instrument attribution
- performer timing offsets
- behavioural interpretation
- expressive analysis


## AD-015 Traceability

INPUT:

BeatReference


OUTPUT:

AnalyticalBeat


RESPONSIBLE TRANSFORMATION:

AnalyticalBeatBuilder


TRACEABILITY:

BeatReference
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

- instrument timing position
- metric deviation visualization
- behavioural comparison


## Status

Foundation created for M22.5 AnalyticalBeat Population.
