# G-012 — Metric Point Projection

---

## Purpose

This document formally defines the scientific
projection that transforms one
Elementary Metric Event into one MetricPoint.

The projection belongs to the Representation Layer.

It never modifies Domain semantics.

---

## Fundamental Principle

MetricPoint is not an observation.

MetricPoint is a geometric representation of an
already validated Elementary Metric Event.

The projection preserves scientific traceability.

---

## Input

ElementaryMetricEvent

The projection may also use validated contextual
information already contained in the Domain Layer.

No additional information may be inferred.

---

## Output

MetricPoint

Every MetricPoint preserves an explicit reference
to its originating ElementaryMetricEvent.

---

## Scientific Traceability

The projection is deterministic.

Identical Domain inputs always produce identical
MetricPoint representations.

---

## Offset

offset_ms represents the metric displacement
associated with the originating
ElementaryMetricEvent.

Its mathematical definition will be introduced
after the projection model has been completely
formalized.

Until then, offset_ms remains a validated
scientific placeholder.

---

## Forbidden Operations

The projection must never:

- infer missing observations;
- modify Domain objects;
- create synthetic timing information;
- depend on visualization.

---

## Representation Principle

Projection changes representation.

Projection never changes scientific meaning.

