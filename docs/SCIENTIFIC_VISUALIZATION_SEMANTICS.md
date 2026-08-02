# Scientific Visualization Semantics

Copyright © 2026 Angelo Tracanna

---

## Purpose

Define the scientific meaning of JGA visual representations.

The Visualization Layer does not perform musical analysis.
It only projects validated Representation Layer objects into visual objects.

---

# Layer Boundary

The transformation chain is:

Metric Representation

↓

Scientific Visualization Frame

↓

Visual Objects

↓

Renderer


The meaning of the data is preserved during visualization.

---

# Scientific Objects

## MetricLandscape

Represents the complete metric geometry of one performance.

It contains the scientific representation produced by the Representation Layer.

The Visualization Layer consumes MetricLandscape without modifying its meaning.

---

## MetricPoint Projection

A visual point represents the projection of one validated metric event.

Source:

MetricPoint

↓

VisualPoint


Meaning:

A point in the visualization corresponds to one metric observation.

---

## VisualTrajectory

A visual trajectory represents the temporal evolution of metric displacement.

The trajectory preserves:

- temporal ordering;
- displacement evolution;
- relationship between metric observations.

---

# Coordinate Semantics

## X Axis

Meaning:

Temporal ordering of metric observations.

The X axis represents progression through the analyzed performance.

---

## Y Axis

Meaning:

Metric temporal displacement.

Source scientific axis:

metric_temporal_displacement

Unit:

milliseconds

Meaning:

Temporal displacement between ElementaryMetricEvent and BeatReference.

---

# Visualization Principle

Visualization must preserve scientific meaning.

The renderer may change graphical appearance,
but must not alter the interpretation of the underlying metric representation.

---

# Architectural Rule

Visualization Layer:

Consumes:
- MetricLandscape
- Representation objects

Produces:
- VisualPoint
- VisualTrajectory
- Scientific figures


Visualization Layer does not:
- detect rhythm;
- calculate metric displacement;
- modify analytical results.

