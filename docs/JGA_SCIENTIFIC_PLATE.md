# JGA Scientific Plate

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna

---

# Purpose

The Scientific Plate is the official graphical representation
produced by the Jazz Groove Analyzer.

Its purpose is not aesthetic rendering.

Its purpose is the communication of scientifically observable
musical behaviour.

Every graphical element must correspond to a precise
musicological concept.

No decorative element is allowed.

---

# Fundamental Principles

## Representation before interpretation

The Plate visualizes analytical results.

It must never infer information that is not explicitly
produced by the analytical pipeline.

---

## Scientific traceability

Every graphical element shall be traceable to one or more
domain objects.

Examples:

- Measure
- Beat Reference
- Metric Cluster
- Metric Event
- Behaviour Observation

No graphical element exists without a scientific origin.

---

## Layered representation

The Plate is composed of independent visual layers.

Typical layers include:

Layer 0
Metadata

Layer 1
Formal structure
(measures, sections, time)

Layer 2
Metric framework
(beats, tempo, references)

Layer 3
Metric events

Layer 4
Relationships
(clusters, connections, trajectories)

Layer 5
Analytical annotations

Each layer can evolve independently.

---

## Renderer independence

The Scientific Plate is independent of the rendering technology.

Possible renderers include:

- Matplotlib
- SVG
- PDF
- Interactive HTML
- Future publication formats

The Plate model remains identical.

---

## Deterministic rendering

Rendering shall be deterministic.

The same Scientific Plate model must always produce
the same graphical output.

---

## No hidden computation

Renderers must never perform analytical computation.

They only transform an already-defined Scientific Plate
into a visual representation.

---

# Scientific Hierarchy

The visual hierarchy follows the analytical hierarchy.

Metadata

↓

Sections

↓

Measures

↓

Beat References

↓

Metric Events

↓

Relationships

↓

Annotations

This hierarchy shall remain stable across all renderers.

---

# Future Evolution

Future versions may include:

- Ensemble trajectories
- Metric tension visualization
- Stability indicators
- Swing profile
- Confidence intervals
- Comparative analyses
- Multi-performance alignment

without modifying the underlying architectural principles.

