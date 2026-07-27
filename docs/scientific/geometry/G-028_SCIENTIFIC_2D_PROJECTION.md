# G-028 — Scientific 2D Projection

## Status

Proposed

## Purpose

Define the scientific meaning of a two-dimensional geometric point
inside the Jazz Groove Analyzer geometric framework.

The geometric space is not an arbitrary mathematical representation.
Each coordinate must correspond to a formally defined scientific quantity.

---

## Scientific Plane

The first JGA scientific plane is defined as:

X = Metric Offset

Y = Metric Stability

---

## X Coordinate

### Name

Metric Offset

### Unit

milliseconds (ms)

### Origin

G-020 — Scientific Metric Offset

### Meaning

Metric Offset represents the temporal displacement of an
ElementaryMetricEvent relative to its BeatReference.

Positive values represent events occurring after the reference.
Negative values represent events occurring before the reference.

---

## Y Coordinate

### Name

Metric Stability

### Unit

score [0..1]

### Origin

G-026 — Metric Stability Coordinate

### Meaning

Metric Stability represents the temporal coherence of the
observed metric behaviour.

Higher values indicate greater temporal consistency.
Lower values indicate greater temporal variability.

---

## Geometric Point Meaning

A geometric point represents the combination of:

- one temporal position observation;
- one temporal coherence observation.

The point does not represent musical quality.

It represents measurable temporal behaviour.

---

## Projection Rule

A ScientificProjectionInput produces a GeometricPoint.

The projection must preserve:

- coordinate identity;
- measurement unit;
- scientific origin;
- numerical value.

No coordinate may be created without a defined scientific source.

---

## Architectural Rule

Geometry must not access:

- DSP objects;
- Core analysis objects;
- Domain reconstruction objects.

Geometry receives only validated scientific coordinates.

---

## Current Plane

The first JGA scientific plane is:

git status
cat <<'EOF' > docs/scientific/geometry/G-028_SCIENTIFIC_2D_PROJECTION.md
