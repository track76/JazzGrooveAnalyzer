# F-023 — Analytical Score Specification

Status

Draft

------------------------------------------------------------

Purpose

Define the standard scientific representation of
the Jazz Groove Analyzer.

The Analytical Score is the primary visual
representation produced by JGA.

It represents the temporal behaviour of each
instrument with respect to the reconstructed
Internal Timing.

It is not a musical score.

It is an analytical representation of metric
behaviour.

------------------------------------------------------------

Scientific Principle

The Internal Timing reconstructed by JGA is the
absolute reference.

Every detected musical event is represented as
its temporal distance from the Internal Timing.

No event is omitted.

No averaging is performed.

Every measurement is preserved.

------------------------------------------------------------

Horizontal Axis

The horizontal structure follows the musical
timeline.

Bar

↓

Beat

↓

Metric Cluster

------------------------------------------------------------

Vertical Axis

Each row represents one musical source.

Examples

Saxophone

Trumpet

Piano

Double Bass

Ride

Hi-Hat

Kick Drum

...

------------------------------------------------------------

Bar Header

Every bar shall display:

Bar Number

Musical Time

Time Signature

Internal BPM

------------------------------------------------------------

Observed Events

Every detected event shall display:

Detected Event

Offset from Internal Timing (ms)

Example

● +12.3 ms

The value is always expressed with respect to
the reconstructed Internal Timing.

------------------------------------------------------------

Diagnostic Highlight

Only significant variations are highlighted.

The numerical value is always preserved.

------------------------------------------------------------

Summary Graphics

After the Analytical Score, the report shall
contain:

One evolution graph for each instrument.

One evolution graph for the Internal BPM.

A final global ensemble analysis.

------------------------------------------------------------

Design Principle

Observe everything.

Highlight only meaningful variations.

Never replace observations with statistical
summaries.

