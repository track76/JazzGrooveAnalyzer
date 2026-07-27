# AD-017 — AnalyticalBeat Temporal Reference

Status: LOCKED

## Decision

AnalyticalBeat must preserve the temporal identity of the
BeatReference from which it is generated.

The analytical representation must not lose the temporal
reference of the reconstructed metric grid.


## Context

BeatReference represents one theoretical beat of the
ensemble metric grid.

It contains:

- index
- timestamp
- unique identity


AnalyticalBeat is the reporting representation of this
metric position inside an AnalyticalBar.


## Problem

The initial AnalyticalBeat model contained only:

- beat number
- analytical cells


This representation lost the temporal position of the
metric reference.


## Decision Rationale

A beat is not only an ordinal position.

It is a temporal reference point.

Therefore:

BeatReference.index
        ↓
AnalyticalBeat.number


BeatReference.timestamp
        ↓
AnalyticalBeat.timestamp_seconds


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


## Scope

Included:

- beat numbering
- temporal reference preservation


Excluded:

- instrument timing
- offset calculation
- behavioural interpretation


## Relationship With AnalyticalCell

AnalyticalBeat represents the metric reference.

AnalyticalCell represents an observed event related
to that reference.

Therefore:

AnalyticalBeat.timestamp_seconds

and

AnalyticalCell.absolute_time_seconds

represent different analytical levels.


## Status

Architectural decision locked for M22.5 AnalyticalBeat Population.
