# G-020 — Metric Offset Definition

Status: DRAFT

Layer: Domain → Representation

Depends on:

- G-013 Scientific Coordinate System
- G-016 Scientific Coordinate Definition
- G-018 Scientific Distance
- G-019 Coordinate Invariants

---

# 1. Purpose

This document defines the scientific meaning of Metric Offset inside
the Jazz Groove Analyzer.

Metric Offset is an observable temporal quantity.

It is not a graphical coordinate.

It is not an arbitrary correction.

---

# 2. Scientific Definition

Metric Offset is the observed temporal displacement of one
ElementaryMetricEvent relative to the BeatReference of the
MetricCluster that contains it.

The offset is expressed in milliseconds.

---

# 3. Scientific Interpretation

Metric Offset represents the internal temporal position of an observed
musical event with respect to the inferred metric reference.

It does not express:

- expressive quality;
- performance quality;
- rhythmic correctness;
- stylistic judgement.

It represents only an observable temporal relationship.

---

# 4. Provenance

Every Metric Offset shall remain traceable to:

- one ElementaryMetricEvent;
- one BeatReference;
- one MetricCluster.

No Metric Offset may exist without complete provenance.

---

# 5. Determinism

Given identical observations, Metric Offset shall always produce the
same measured value.

No stochastic component is permitted.

---

# 6. Representation

Metric Offset is the scientific quantity used by the Representation
Layer to construct MetricPoint.

MetricPoint stores the measurement.

It never estimates it.

---

# 7. Future Evolution

The mathematical measurement algorithm is intentionally left
undefined.

Only scientifically validated observation rules may determine the
final computation.

---

# E0F-011

- [x] Observation remains primary.
- [x] Offset is measurable.
- [x] Provenance preserved.
- [x] Representation remains deterministic.
- [x] No musical interpretation introduced.

Result: PASS.

