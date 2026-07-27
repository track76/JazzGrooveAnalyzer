# AD-016 — AnalyticalBar Temporal Boundaries

Status: LOCKED

## Decision

AnalyticalBar must represent a complete temporal observational segment.

Therefore AnalyticalBar must expose:

- start_time_seconds
- end_time_seconds

as direct representations of the corresponding values contained in
ReconstructedMeasure.


## Context

The ReconstructedMeasure domain entity represents a scientifically
reconstructed musical measure.

It contains:

- measure number
- internal metric signature
- internal BPM
- temporal boundaries
- beat references
- metric clusters


The reporting layer must not lose scientific information during translation.


## Problem

The first AnalyticalBar representation contained only:

- time_seconds

This representation was insufficient because it collapsed a temporal interval
into a single point.


A musical measure is not a point in time.
It is an observable temporal segment.


## Decision Rationale

The transformation:

ReconstructedMeasure
        ↓
AnalyticalBar

must preserve temporal information.

Therefore:

ReconstructedMeasure.start_time_seconds
        ↓
AnalyticalBar.start_time_seconds


ReconstructedMeasure.end_time_seconds
        ↓
AnalyticalBar.end_time_seconds


## AD-015 Traceability

INPUT:

ReconstructedMeasure


OUTPUT:

AnalyticalBar


RESPONSIBLE TRANSFORMATION:

AnalyticalBarBuilder


TRACEABILITY:

ReconstructedMeasure
        ↓
AnalyticalBar
        ↓
AnalyticalScore
        ↓
Renderer


## Scope

This decision concerns only temporal representation.

It does not introduce:

- instrument attribution
- timing offsets
- behavioural interpretation
- graphical rendering rules


## Future Extensions

Future analytical layers may use the temporal boundaries for:

- score visualization
- measure comparison
- behavioural evolution analysis
- geometric representation


## Status

Architectural decision locked for M22.4 AnalyticalBar Population.
