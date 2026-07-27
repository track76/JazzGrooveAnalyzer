# G-022 — Observable Scientific Coordinates

## Status

Draft

---

## Purpose

Define the requirements that every scientific coordinate shall satisfy before
being introduced into the Jazz Groove Analyzer geometric framework.

---

# Scientific Coordinate

A scientific coordinate is the geometric representation of one observable
musical quantity.

It is never an arbitrary mathematical value.

---

# Requirements

Every coordinate shall be:

- observable
- measurable
- deterministic
- reproducible
- traceable
- independent from every other coordinate

Failure to satisfy one of these requirements automatically excludes the
quantity from the geometric model.

---

# Scientific Traceability

Every coordinate must follow the chain:

Observable Musical Fact
        ↓
Domain Object
        ↓
Scientific Quantity
        ↓
Geometric Coordinate

No intermediate step may introduce arbitrary information.

---

# Coordinate Independence

Each coordinate represents one and only one observable phenomenon.

Two coordinates shall never encode the same information.

---

# Current Validated Coordinate

Coordinate 1

Metric Offset

Observable:

Difference between an Elementary Metric Event and its Beat Reference.

Scientific Quantity:

Offset expressed in milliseconds.

Domain Source:

ElementaryMetricEvent
BeatReference

Implementation:

MetricOffsetCalculator

Reference:

G-020

---

Future coordinates shall follow exactly the same methodology.
