# G-023 — Observable Quantities

## Status

Draft

---

## Purpose

Identify the observable musical quantities currently available in the Domain
Model that may become future scientific geometric coordinates.

Only quantities already represented by the Domain are considered.

---

# Observable Quantities

## Metric Offset

Domain Objects

- ElementaryMetricEvent
- BeatReference

Scientific Quantity

Difference between an Elementary Metric Event and its Beat Reference,
expressed in milliseconds.

Status

Validated (G-020)

---

## Metric Position

Domain Object

- ElementaryMetricEvent

Scientific Quantity

Observed metric position of the event inside its Metric Cluster.

Status

Candidate

---

## Metric Cluster

Domain Object

- MetricCluster

Scientific Quantity

Observed metric context to which an event belongs.

Status

Context only

Not a coordinate.

---

## Pulse

Domain Object

- Pulse

Scientific Quantity

Observed pulse reconstructed from the ensemble.

Status

Reference object

Not a coordinate.

---

## Internal Metric Timeline

Domain Object

- InternalMetricTimeline

Scientific Quantity

Ordered succession of reconstructed pulses.

Status

Reference structure

Not a coordinate.

---

# Scientific Rule

Only observable quantities may become scientific coordinates.

Context objects and organizational structures shall never be used directly as
geometric axes.
